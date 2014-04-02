import base64
import functools
import json
import logging

from django.conf import settings
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from karaage.common.decorators import login_required
from . import models


LOG = logging.getLogger(__file__)
REDIRECT_WHITELIST = getattr(settings, 'KEYSTONE_REDIRECT_WHITELIST', [])


def redirect_with_keystone_auth(target_url):
    return functools.partial(keystone_login, target_url=target_url)


@login_required
def keystone_login(request, target_url,
                   redirect_field_name=REDIRECT_FIELD_NAME):
    if target_url not in REDIRECT_WHITELIST:
        raise Http404()

    if redirect_field_name in request.REQUEST:
        next_page = request.REQUEST[redirect_field_name]
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    try:
        token, tenant_id = models.keystone_authenticate(request.user)
    except Exception, e:
        LOG.error("Keystone user login failed: %s", str(e))
        messages.error(request, "Login failed. Please contact support.")
        return redirect('index')

    token_data = base64.encodestring(json.dumps(token))
    return render(request, 'keystone-service/redirect.html',
            {'token': token_data,
             'tenant_id': tenant_id,
             'target': target_url + next_page})
