from django.conf.urls import url, patterns
from django.conf import settings


from . import views


dashboard_target = settings.OPENSTACK_DASHBOARD_LOGIN_URL

urlpatterns = patterns('',
    url(r'^openstack/$',
        views.redirect_with_keystone_auth(dashboard_target),
        name='kgauth_login_openstack')
)
