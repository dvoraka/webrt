from django.http import HttpResponseRedirect
from django.conf import settings


def auth_req(function):
    '''Check for user is logged in.'''

    def wrapper(request, *args, **kw):

        user = request.user
        if not user.is_authenticated():

            return HttpResponseRedirect(
                settings.PYRT.get('LOGIN_PAGE', ''))

        else:

            return function(request, *args, **kw)

    return wrapper
