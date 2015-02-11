from django.conf import settings
from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
#from views import newpost, editpost, post
admin.autodiscover()


urlpatterns = patterns('core.views',
    url(r'^$', 'hello_world', {}, name='home'),
    url(r'^u/(?P<username>\w+)/$', 'profile', name="profile"),
    url(r'^feed/$', 'feed', {}, name='feed'),
    url(r'^saved/$', 'saved', {}, name='saved'),
    url(r'^new/$', 'newpost', {}, name='newpost'),
    url(r'^settings/$', 'settings', {}, name='settings'),
    url(r'^post/(?P<post_id>\w+)/$', 'post', name='post'),
    url(r'^post/(?P<post_id>\w+)/edit/$', 'editpost', name='editpost'),
    url(r'^post/(?P<post_id>\w+)/delete/$', 'deletepost', name='deletepost'),
    url(r'^post/(?P<target_id>\w+)/save', 'save', name="save"),
    url(r'^post/(?P<target_id>\w+)/remove', 'remove', name="remove"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
