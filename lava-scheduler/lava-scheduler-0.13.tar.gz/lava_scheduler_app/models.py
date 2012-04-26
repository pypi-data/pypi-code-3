import logging
import simplejson

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from django_restricted_resource.models import RestrictedResource

from dashboard_app.models import Bundle, BundleStream

from lava_dispatcher.job import validate_job_data

from linaro_django_xmlrpc.models import AuthToken


class JSONDataError(ValueError):
    """Error raised when JSON is syntactically valid but ill-formed."""


class Tag(models.Model):

    name = models.SlugField(unique=True)

    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


def validate_job_json(data):
    try:
        ob = simplejson.loads(data)
        validate_job_data(ob)
    except ValueError, e:
        raise ValidationError(str(e))


class DeviceType(models.Model):
    """
    A class of device, for example a pandaboard or a snowball.
    """

    name = models.SlugField(primary_key=True)

    def __unicode__(self):
        return self.name

    health_check_job = models.TextField(
        null=True, blank=True, default=None, validators=[validate_job_json])


class Device(models.Model):
    """
    A device that we can run tests on.
    """

    OFFLINE = 0
    IDLE = 1
    RUNNING = 2
    OFFLINING = 3

    STATUS_CHOICES = (
        (OFFLINE, 'Offline'),
        (IDLE, 'Idle'),
        (RUNNING, 'Running'),
        (OFFLINING, 'Going offline'),
    )

    # A device health shows a device is ready to test or not
    HEALTH_UNKNOWN, HEALTH_PASS, HEALTH_FAIL = range(3)
    HEALTH_CHOICES = (
        (HEALTH_UNKNOWN, 'Unknown'),
        (HEALTH_PASS, 'Pass'),
        (HEALTH_FAIL, 'Fail'),
    )

    hostname = models.CharField(
        verbose_name = _(u"Hostname"),
        max_length = 200,
        primary_key = True,
    )

    device_type = models.ForeignKey(
        DeviceType, verbose_name=_(u"Device type"))

    current_job = models.ForeignKey(
        "TestJob", blank=True, unique=True, null=True, related_name='+')

    tags = models.ManyToManyField(Tag, blank=True)

    status = models.IntegerField(
        choices = STATUS_CHOICES,
        default = IDLE,
        verbose_name = _(u"Device status"),
    )

    health_status = models.IntegerField(
        choices = HEALTH_CHOICES,
        default = HEALTH_UNKNOWN,
        verbose_name = _(u"Device Health"),
    )

    last_health_report_job = models.ForeignKey(
            "TestJob", blank=True, unique=True, null=True, related_name='+')

    def __unicode__(self):
        return self.hostname

    @models.permalink
    def get_absolute_url(self):
        return ("lava.scheduler.device.detail", [self.pk])

    @models.permalink
    def get_device_health_url(self):
        return ("lava.scheduler.labhealth.detail", [self.pk])

    def recent_jobs(self):
        return TestJob.objects.select_related(
            "actual_device",
            "requested_device",
            "requested_device_type",
            "submitter",
            "user",
            "group",
        ).filter(
            actual_device=self
        ).order_by(
            '-start_time'
        )

    def can_admin(self, user):
        return user.has_perm('lava_scheduler_app.change_device')

    def put_into_maintenance_mode(self, user, reason):
        if self.status in [self.RUNNING, self.OFFLINING]:
            new_status = self.OFFLINING
        else:
            new_status = self.OFFLINE
        DeviceStateTransition.objects.create(
            created_by=user, device=self, old_state=self.status,
            new_state=new_status, message=reason, job=None).save()
        self.status = new_status
        self.save()

    def put_into_online_mode(self, user, reason):
        if self.status not in [Device.OFFLINE, Device.OFFLINING]:
            return
        new_status = self.IDLE
        DeviceStateTransition.objects.create(
            created_by=user, device=self, old_state=self.status,
            new_state=new_status, message=reason, job=None).save()
        self.status = new_status
        self.health_status = Device.HEALTH_UNKNOWN
        self.save()

    #@classmethod
    #def find_devices_by_type(cls, device_type):
    #    return device_type.device_set.all()



class TestJob(RestrictedResource):
    """
    A test job is a test process that will be run on a Device.
    """

    SUBMITTED = 0
    RUNNING = 1
    COMPLETE = 2
    INCOMPLETE = 3
    CANCELED = 4
    CANCELING = 5

    STATUS_CHOICES = (
        (SUBMITTED, 'Submitted'),
        (RUNNING, 'Running'),
        (COMPLETE, 'Complete'),
        (INCOMPLETE, 'Incomplete'),
        (CANCELED, 'Canceled'),
        (CANCELING, 'Canceling'),
    )

    id = models.AutoField(primary_key=True)

    submitter = models.ForeignKey(
        User,
        verbose_name = _(u"Submitter"),
        related_name = '+',
    )

    submit_token = models.ForeignKey(AuthToken, null=True, blank=True)

    description = models.CharField(
        verbose_name = _(u"Description"),
        max_length = 200,
        null = True,
        blank = True,
        default = None
    )

    health_check = models.BooleanField(default=False)

    # Only one of these two should be non-null.
    requested_device = models.ForeignKey(
        Device, null=True, default=None, related_name='+', blank=True)
    requested_device_type = models.ForeignKey(
        DeviceType, null=True, default=None, related_name='+', blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    # This is set once the job starts.
    actual_device = models.ForeignKey(
        Device, null=True, default=None, related_name='+', blank=True)

    #priority = models.IntegerField(
    #    verbose_name = _(u"Priority"),
    #    default=0)
    submit_time = models.DateTimeField(
        verbose_name = _(u"Submit time"),
        auto_now = False,
        auto_now_add = True
    )
    start_time = models.DateTimeField(
        verbose_name = _(u"Start time"),
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        editable = False
    )
    end_time = models.DateTimeField(
        verbose_name = _(u"End time"),
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        editable = False
    )

    @property
    def duration(self):
        if self.end_time is None:
            return None
        return self.end_time - self.start_time

    status = models.IntegerField(
        choices = STATUS_CHOICES,
        default = SUBMITTED,
        verbose_name = _(u"Status"),
    )

    definition = models.TextField(
        editable = False,
    )

    log_file = models.FileField(
        upload_to='lava-logs', default=None, null=True, blank=True)

    results_link = models.CharField(
        max_length=400, default=None, null=True, blank=True)

    @property
    def results_bundle(self):
        # XXX So this is clearly appalling (it depends on the format of bundle
        # links, for example).  We should just have a fkey to Bundle.
        if not self.results_link:
            return None
        sha1 = self.results_link.strip('/').split('/')[-1]
        try:
            return Bundle.objects.get(content_sha1=sha1)
        except Bundle.DoesNotExist:
            return None

    def __unicode__(self):
        r = "%s test job" % self.get_status_display()
        if self.requested_device:
            r += " for %s" % (self.requested_device.hostname,)
        return r

    @models.permalink
    def get_absolute_url(self):
        return ("lava.scheduler.job.detail", [self.pk])

    @classmethod
    def from_json_and_user(cls, json_data, user):
        job_data = simplejson.loads(json_data)
        validate_job_data(job_data)
        if 'target' in job_data:
            target = Device.objects.get(hostname=job_data['target'])
            device_type = None
        elif 'device_type' in job_data:
            target = None
            device_type = DeviceType.objects.get(name=job_data['device_type'])
        else:
            raise JSONDataError(
                "Neither 'target' nor 'device_type' found in job data.")

        for email_field in 'notify', 'notify_on_incomplete':
            if email_field in job_data:
                value = job_data[email_field]
                msg = ("%r must be a list of email addresses if present"
                       % email_field)
                if not isinstance(value, list):
                    raise ValueError(msg)
                for address in value:
                    if not isinstance(address, basestring):
                        raise ValueError(msg)
                    try:
                        validate_email(address)
                    except ValidationError:
                        raise ValueError(
                            "%r is not a valid email address." % address)

        job_name = job_data.get('job_name', '')

        is_check = job_data.get('health_check', False)

        submitter = user
        group = None
        is_public = True

        for action in job_data['actions']:
            if not action['command'].startswith('submit_results'):
                continue
            stream = action['parameters']['stream']
            try:
                bundle_stream = BundleStream.objects.get(pathname=stream)
            except BundleStream.DoesNotExist:
                raise ValueError("stream %s not found" % stream)
            if not bundle_stream.can_upload(submitter):
                raise ValueError(
                    "you cannot submit to the stream %s" % stream)
            if not bundle_stream.is_anonymous:
                user, group, is_public = (bundle_stream.user,
                                          bundle_stream.group,
                                          bundle_stream.is_public)

        tags = []
        for tag_name in job_data.get('device_tags', []):
            try:
                tags.append(Tag.objects.get(name=tag_name))
            except Tag.DoesNotExist:
                raise JSONDataError("tag %r does not exist" % tag_name)
        job = TestJob(
            definition=json_data, submitter=submitter,
            requested_device=target, requested_device_type=device_type,
            description=job_name, health_check=is_check, user=user,
            group=group, is_public=is_public)
        job.save()
        for tag in tags:
            job.tags.add(tag)
        return job

    def can_cancel(self, user):
        return user.is_superuser or user == self.submitter

    def cancel(self):
        if self.status == TestJob.RUNNING:
            self.status = TestJob.CANCELING
        else:
            self.status = TestJob.CANCELED
        self.save()

    def _generate_summary_mail(self):
        domain = '???'
        try:
            site = Site.objects.get_current()
        except (Site.DoesNotExist, ImproperlyConfigured):
            pass
        else:
            domain = site.domain
        url_prefix = 'http://%s' % domain
        return render_to_string(
            'lava_scheduler_app/job_summary_mail.txt',
            {'job': self, 'url_prefix': url_prefix})

    def _get_notification_recipients(self):
        job_data = simplejson.loads(self.definition)
        recipients = job_data.get('notify', [])
        if self.status != self.COMPLETE:
            recipients.extend(job_data.get('notify_on_incomplete', []))
        return recipients

    def send_summary_mails(self):
        recipients = self._get_notification_recipients()
        if not recipients:
            return
        mail = self._generate_summary_mail()
        description = self.description.splitlines()[0]
        if len(description) > 200:
            description = description[197:] + '...'
        logger = logging.getLogger(self.__class__.__name__ + '.' + str(self.pk))
        logger.info("sending mail to %s", recipients)
        send_mail(
            "LAVA job notification: " + description, mail,
            settings.SERVER_EMAIL, recipients)


class DeviceStateTransition(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True)
    device = models.ForeignKey(Device, related_name='transitions')
    job = models.ForeignKey(TestJob, null=True, blank=True)
    old_state = models.IntegerField(choices=Device.STATUS_CHOICES)
    new_state = models.IntegerField(choices=Device.STATUS_CHOICES)
    message = models.TextField(null=True, blank=True)
