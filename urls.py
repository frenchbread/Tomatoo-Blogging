from django.conf.urls import *

urlpatterns = patterns(
    '',
    (r'^appengine_sessions/', include('appengine_sessions.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'', include('core.urls')),
)
