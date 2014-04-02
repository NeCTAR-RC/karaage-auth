from django.conf.urls import patterns, url

from .views import LoginSelectView


urlpatterns = patterns('karaage.people.views.profile',
    url(r'^login/select/', LoginSelectView.as_view(), name='kgauth_login_select'),
    url(r'^login/select/', LoginSelectView.as_view(), name='login'),
    # Move the default login view to login_local, so we can reverse it
    # in the login select view.
    url(r'^login/local/$', 'login', name='kgauth_login_local'),
)
