from django.conf import settings

THREADED_MESSAGES_USE_SENDGRID = getattr(settings, 'THREADED_MESSAGES_USE_SENDGRID', False)
THREADED_MESSAGES_ID = getattr(settings, 'THREADED_MESSAGES_ID', 'm')

INBOX_COUNT_CACHE = "THREADED_MESSAGES_INBOX_COUNT_%s"
INBOX_COUNT_CACHE_TIME = 60 * 60 * 6
