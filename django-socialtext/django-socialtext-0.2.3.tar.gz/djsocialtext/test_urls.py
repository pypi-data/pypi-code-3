from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^djsocialtext/', include('djsocialtext.urls')),
)