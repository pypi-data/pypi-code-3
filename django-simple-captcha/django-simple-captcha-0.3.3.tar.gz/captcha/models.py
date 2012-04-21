from captcha.conf import settings as captcha_settings
from django.db import models
import datetime
import random
import time
import unicodedata

# Heavily based on session key generation in Django
# Use the system (hardware-based) random number generator if it exists.
if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange
MAX_RANDOM_KEY = 18446744073709551616L     # 2 << 63


try:
    import hashlib  # sha for Python 2.5+
except ImportError:
    import sha  # sha for Python 2.4 (deprecated in Python 2.6)
    hashlib = False


def get_safe_now():
    try:
        from django.utils.timezone import utc
        return datetime.datetime.utcnow().replace(tzinfo=utc)
    except:
        return datetime.datetime.now()


class CaptchaStore(models.Model):
    challenge = models.CharField(blank=False, max_length=32)
    response = models.CharField(blank=False, max_length=32)
    hashkey = models.CharField(blank=False, max_length=40, unique=True)
    expiration = models.DateTimeField(blank=False)

    def save(self, *args, **kwargs):
        self.response = self.response.lower()
        if not self.expiration:
            #self.expiration = datetime.datetime.now() + datetime.timedelta(minutes=int(captcha_settings.CAPTCHA_TIMEOUT))
            self.expiration = get_safe_now() + datetime.timedelta(minutes=int(captcha_settings.CAPTCHA_TIMEOUT))
        if not self.hashkey:
            key_ = unicodedata.normalize('NFKD', str(randrange(0, MAX_RANDOM_KEY)) + str(time.time()) + unicode(self.challenge)).encode('ascii', 'ignore') + unicodedata.normalize('NFKD', unicode(self.response)).encode('ascii', 'ignore')
            if hashlib:
                self.hashkey = hashlib.sha1(key_).hexdigest()
            else:
                self.hashkey = sha.new(key_).hexdigest()
            del(key_)
        super(CaptchaStore, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.challenge

    def remove_expired(cls):
        cls.objects.filter(expiration__lte=get_safe_now()).delete()
    remove_expired = classmethod(remove_expired)
