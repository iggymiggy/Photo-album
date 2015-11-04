from django.conf.urls import patterns, url

urlpatterns = patterns('album.views',
    url(r'^/$', 'index', name="index"),
    url(r'^view/(?P<album_id>\d+)/$', 'view_album', name='view_album'),
    url(r'^view/public/(?P<album_key>\w+)/$', 'view_public_album', name='view_public_album'),
    url(r'^create/$', 'create_album', name='create_album'),
    url(r'^remove/$', 'remove_album', name='remove_album'),
    url(r'^rename/$', 'rename_album', name='rename_album'),
    url(r'^page/create/$', 'create_page', name='create_page'),
    url(r'^page/save/$', 'save_page', name='save_page'),
    url(r'^page/view/$', 'view_page', name='view_page'),
    url(r'^page/remove/$', 'remove_page', name='remove_page'),
    url(r'^page/name/$', 'name_page', name='name_page'),
    url(r'^page/moveleft/$', 'moveleft_page', name='moveleft_page'),
    url(r'^page/moveright/$', 'moveright_page', name='right_page'),
)
