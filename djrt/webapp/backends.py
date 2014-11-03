# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.conf import settings
from requests import ConnectionError

import pyrt
# web LDAP module
import wldap


class CustomBackend(object):
    '''Custom auth backend.

    It is disabled in settings.py by default.'''

    supports_inactive_user = False

    def authenticate(self, username=None, password=None):

        # auth sequence
        # 1. LDAP (customizable through wldap module)
        # 2. Django user exists
        # 3. RT user exists

        # LDAP
        ldap = wldap.LDAP()
        authenticated = ldap.check_password(username, password)
        # print('LDAP: {}'.format(authenticated))

        # Django user exists
        exists = User.objects.filter(username=username).count()
        # print('Django: {}'.format(bool(exists)))

        # RT user exists
        rt = pyrt.RT4(
            rest_url=settings.PYRT.get('REST_URL', ''))
        rt.login(
            settings.PYRT.get('ADMIN', ''),
            settings.PYRT.get('PASS', ''),
        )
        try:

            RT_exists = rt.user_exists(username)

        except ConnectionError as e:  # NOQA

            # TODO: logging
            # print(e)
            RT_exists = False

        # print('RT: {}'.format(RT_exists))

# ## DEBUG ONLY
###################################
#        authenticated = True
#        exists = True
#        RT_exists = True
#        print(authenticated, exists, RT_exists)
###################################

        user = None
        if authenticated and exists and RT_exists:

            user = User.objects.get(username=username)

        return user

    def get_user(self, user_id):

        try:

            return User.objects.get(pk=user_id)

        except User.DoesNotExist:

            return None
