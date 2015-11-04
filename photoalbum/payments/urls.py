from django.conf.urls import patterns, url
urlpatterns = patterns('payments.views',  
    url(r'^(?P<album_id>\d+)/$', 'index', name='index'),
    url(r'^pay/$', 'pay', name='pay'),
    url(r'^success/$', 'success', name='success'),
    url(r'^cancel/$', 'cancel', name='cancel'),
    url(r'^error/$', 'error', name='error'),
)
