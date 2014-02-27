# -*- coding: utf-8 -*-

import ldap


class LDAP:
    
    def __init__(self, host='ldaps://localhost'):
        
        self.host = host
        self.conn = None

    def bind(self, user, password):
        pass

    def check_password(self, login, password):
        
        return True

    def is_staff(self, cid):
        
        return True
