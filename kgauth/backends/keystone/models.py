from django.conf import settings
from keystoneclient.v2_0 import client as keystoneclient

from karaage import datastores


KEYSTONE_CONF = getattr(settings, 'KEYSTONE_CONFIG', {})


def keystone_authenticate(person):
    """Authenticate a user as their default tenant.
    """
    details = datastores.get_person_details(person)
    keystone_user_details = details['keystone'][0]

    kwargs = {'username': keystone_user_details['name'],
              'password': KEYSTONE_CONF['authenticate_password'],
              'auth_url': KEYSTONE_CONF['admin_url']}

    client = keystoneclient.Client(**kwargs)
    token = client.auth_ref
    return token, keystone_user_details.get('default_project_id')
