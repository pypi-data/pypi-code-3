from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
		(r'^$', 'djangowanted.wanted.views.service'),
)
