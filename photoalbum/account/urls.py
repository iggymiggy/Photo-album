from django.conf.urls import patterns, url

urlpatterns = patterns('account.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='login'),
    url(r'^register/$', 'register', name='register'),
    url(r'^settings/$', 'settings', name='settings'),
)
