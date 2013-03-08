__author__ = 'cternus'
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^pdf/$', 'gametex_django_print.views.pdf', name='pdf'),
    )
