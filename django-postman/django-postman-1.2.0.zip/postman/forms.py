"""
You may define your own custom forms, based or inspired by the following ones.

Examples of customization:
    recipients = CommaSeparatedUserField(label=("Recipients", "Recipient"),
        min=2,
        max=5,
        user_filter=my_user_filter,
        channel='my_channel',
    )
    can_overwrite_limits = False
    exchange_filter = staticmethod(my_exchange_filter)

"""
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _

from postman.fields import CommaSeparatedUserField
from postman.models import Message
from postman.utils import WRAP_WIDTH

class BaseWriteForm(forms.ModelForm):
    """The base class for other forms."""
    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            # for better confort, ensure a 'cols' of at least
            # the 'width' of the body quote formatter.
            'body': forms.Textarea(attrs={'cols': WRAP_WIDTH, 'rows': 12}),
        }

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        exchange_filter = kwargs.pop('exchange_filter', None)
        user_filter = kwargs.pop('user_filter', None)
        max = kwargs.pop('max', None)
        channel = kwargs.pop('channel', None)
        super(BaseWriteForm, self).__init__(*args, **kwargs)

        self.instance.sender = sender if (sender and sender.is_authenticated()) else None
        if exchange_filter:
            self.exchange_filter = exchange_filter
        if 'recipients' in self.fields:
            if user_filter and hasattr(self.fields['recipients'], 'user_filter'):
                self.fields['recipients'].user_filter = user_filter

            if getattr(settings, 'POSTMAN_DISALLOW_MULTIRECIPIENTS', False):
                max = 1
            if max is not None and hasattr(self.fields['recipients'], 'set_max') \
            and getattr(self, 'can_overwrite_limits', True):
                self.fields['recipients'].set_max(max)

            if channel and hasattr(self.fields['recipients'], 'set_arg'):
                self.fields['recipients'].set_arg(channel)

    error_messages = {
        'filtered': _("Writing to some users is not possible: {users}."),
        'filtered_user': _("{user.username}"),
        'filtered_user_with_reason': _("{user.username} ({reason})"),
    }
    def clean_recipients(self):
        """Check no filter prohibit the exchange."""
        recipients = self.cleaned_data['recipients']
        exchange_filter = getattr(self, 'exchange_filter', None)
        if exchange_filter:
            errors = []
            filtered_names = []
            recipients_list = recipients[:]
            for u in recipients_list:
                try:
                    reason = exchange_filter(self.instance.sender, u, recipients_list)
                    if reason is not None:
                        recipients.remove(u)
                        filtered_names.append(
                            self.error_messages[
                                'filtered_user_with_reason' if reason else 'filtered_user'
                            ].format(user=u, reason=reason)
                        )
                except forms.ValidationError, e:
                    recipients.remove(u)
                    errors.extend(e.messages)
            if filtered_names:
                errors.append(self.error_messages['filtered'].format(users=', '.join(filtered_names)))
            if errors:
                raise forms.ValidationError(errors)
        return recipients

    @transaction.commit_on_success
    def save(self, recipient=None, parent=None, auto_moderators=[]):
        """
        Save as many messages as there are recipients.

        Additional actions:
        - If it's a reply, build a conversation
        - Call auto-moderators
        - Notify parties if needed

        Return False if one of the messages is rejected.

        """
        recipients = self.cleaned_data.get('recipients', [])
        if parent and not parent.thread_id: # at the very first reply, make it a conversation
            parent.thread = parent
            parent.save()
            # but delay the setting of parent.replied_at to the moderation step
        if parent:
            self.instance.parent = parent
            self.instance.thread_id = parent.thread_id
        initial_moderation = self.instance.get_moderation()
        initial_dates = self.instance.get_dates()
        initial_status = self.instance.moderation_status
        if recipient:
            if isinstance(recipient, User) and recipient in recipients:
                recipients.remove(recipient)
            recipients.insert(0, recipient)
        is_successful = True
        for r in recipients:
            if isinstance(r, User):
                self.instance.recipient = r
            else:
                self.instance.recipient = None
                self.instance.email = r
            self.instance.pk = None # force_insert=True is not accessible from here
            self.instance.auto_moderate(auto_moderators)
            self.instance.clean_moderation(initial_status)
            self.instance.clean_for_visitor()
            m = super(BaseWriteForm, self).save()
            if self.instance.is_rejected():
                is_successful = False
            self.instance.update_parent(initial_status)
            self.instance.notify_users(initial_status)
            # some resets for next reuse
            if not isinstance(r, User):
                self.instance.email = ''
            self.instance.set_moderation(*initial_moderation)
            self.instance.set_dates(*initial_dates)
        return is_successful

class WriteForm(BaseWriteForm):
    """The form for an authenticated user, to compose a message."""
    recipients = CommaSeparatedUserField(label=(_("Recipients"), _("Recipient")))

    class Meta(BaseWriteForm.Meta):
        fields = ('recipients', 'subject', 'body')

class AnonymousWriteForm(BaseWriteForm):
    """The form for an anonymous user, to compose a message."""
    # The 'max' customization should not be permitted here.
    # The features available to anonymous users should be kept to the strict minimum.
    can_overwrite_limits = False

    email = forms.EmailField(label=_("Email"))
    recipients = CommaSeparatedUserField(label=(_("Recipients"), _("Recipient")), max=1) # one recipient is enough

    class Meta(BaseWriteForm.Meta):
        fields = ('email', 'recipients', 'subject', 'body')

class BaseReplyForm(BaseWriteForm):
    """The base class for a reply to a message."""
    def __init__(self, *args, **kwargs):
        recipient = kwargs.pop('recipient', None)
        super(BaseReplyForm, self).__init__(*args, **kwargs)
        self.recipient = recipient

    def clean(self):
        """Check that the recipient is correctly initialized."""
        if not self.recipient:
            raise forms.ValidationError(ugettext("Undefined recipient."))
        return super(BaseReplyForm, self).clean()

    def save(self, *args, **kwargs):
        return super(BaseReplyForm, self).save(self.recipient, *args, **kwargs)

class QuickReplyForm(BaseReplyForm):
    """
    The form to use in the view of a message or a conversation, for a quick reply.

    The recipient is imposed and a default value for the subject will be provided.

    """
    pass

allow_copies = not getattr(settings, 'POSTMAN_DISALLOW_COPIES_ON_REPLY', False)
class FullReplyForm(BaseReplyForm):
    """The complete reply form."""
    if allow_copies:
        recipients = CommaSeparatedUserField(label=(_("Additional recipients"), _("Additional recipient")), required=False)

    class Meta(BaseReplyForm.Meta):
        fields = (['recipients'] if allow_copies else []) + ['subject', 'body']
