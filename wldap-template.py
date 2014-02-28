# -*- coding: utf-8 -*-

import ldap


class LDAP:
    '''Template LDAP class. Custom backend use this class, so it is good
    to have minimal implementation of it in case you want to use default
    CustomBackend class.'''
    
    def __init__(self, host='ldaps://localhost'):
        
        self.host = host
        self.conn = None

    def bind(self, user, password):
        pass

    def check_password(self, login, password):
        
        return True

    def is_staff(self, cid):
        
        return True
