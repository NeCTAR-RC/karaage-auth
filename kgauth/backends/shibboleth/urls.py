from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^shibboleth/(?P<next_path>.*)$',
        'kgauth.backends.shibboleth.views.shib_receiver',
        name='kgauth_login_saml'),
)

if ('kgauth.backends.shibboleth.middleware.FakeShibMiddleware'
        in settings.MIDDLEWARE_CLASSES):
    from . import fakeshib
    urlpatterns += patterns(
        '',
        url(r'^fakeshib/(?P<next_path>.*)$', fakeshib.FakeShibView.as_view(),
            name='kgauth_fakeshib'),
    )
