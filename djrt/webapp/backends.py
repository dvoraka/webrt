# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.conf import settings
import pyrt


class CustomBackend(object):
    '''Custom auth backend.
    
    It is disabled in settings.py by default.'''
    
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        
        # auth sequence
        # 1. CAS
        # 2. Django user exists
        # 3. RT user exists

        # CAS
        import wldap # web LDAP module
        ldap = wldap.LDAP()
        authenticated = ldap.check_password(username, password)
        #print('CAS: {}'.format(authenticated))

        # Django user exists
        exists = User.objects.filter(username=username).count()
        #print('Django: {}'.format(bool(exists)))

        # RT user exists
        rt = pyrt.RT4(
            rest_url=settings.PYRT.get('REST_URL', ''))
        rt.login(
            settings.PYRT.get('ADMIN', ''),
            settings.PYRT.get('PASS', ''),
        )
        RT_exists = rt.user_exists(username)
        #print('RT: {}'.format(RT_exists))

### DEBUG ONLY
###################################
#        exists = True
#        authenticated = True
#        RT_exists = True
###################################

        user = None
        if exists and authenticated and RT_exists:
            
            user = User.objects.get(username=username)

        return user

    def get_user(self, user_id):
        
        try:
            
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            
            return None
