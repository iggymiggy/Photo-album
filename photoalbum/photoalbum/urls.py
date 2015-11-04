from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',  
    url(r'^$', 'photoalbum.views.index', name='index'),
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^account/', include('account.urls')),
    url(r'^album/', include('album.urls')),
    url(r'^payments/',include('payments.urls'))
)
