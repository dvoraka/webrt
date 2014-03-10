# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib import auth
from django.conf import settings
from django.db.models.base import ObjectDoesNotExist

from requests import ConnectionError

import pyrt
import wldap

from webapp.forms import AddTicketForm
from webapp.forms import AddCommentForm
from webapp.forms import LoginForm
from webapp.forms import RegForm
from webapp.forms import SettingsForm
from webapp.decorators import auth_req


@auth_req
def show_ticket(request, id_):
    '''Show full ticket.
    
    Args:
        id_ (str): Ticket's ID.
    '''

    rt = pyrt.RT4(
        rest_url=settings.PYRT.get('REST_URL', ''))
    # load ticket with admin
    rt.login(
        settings.PYRT.get('ADMIN', ''),
        settings.PYRT.get('PASS', ''),
    )
    try:

        ticket = rt.get_ticket(id_)
        ticket.load_all()

    except ConnectionError as e:
        
        print(e)
        return show_msg(request, _("Connection to RT server failed"))

    if ticket.creator != request.user.username:

        request.session['message'] = (
            _("Permission denied.")
        )

        return HttpResponseRedirect('/message/')

    # after checks load ticket with user's account
    rt.login(
        request.user.username,
        settings.PYRT.get('GLOBAL_PASS', ''),
    )
    try:

        ticket = rt.get_ticket(id_)
        ticket.load_all()

    except ConnectionError as e:
        
        print(e)
        return show_msg(request, _("Connection to RT server failed"))

    # set user's timezone
    for history in ticket.history.history_list:

        utc_str = history['Created']
        utc = datetime.datetime.strptime(utc_str, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(
            hours=settings.PYRT.get('TIME_DELTA', 0))
        history['Created'] = (utc + delta).isoformat(str(' '))
 
    return render(request, 'webapp/show_ticket.html', {

        'ticket': ticket,

    })


@auth_req
def index(request):
    '''Index page with user's tickets.'''

    rt = pyrt.RT4(
        rest_url=settings.PYRT.get('REST_URL', ''))
    rt.login(
        settings.PYRT.get('ADMIN', ''),
        settings.PYRT.get('PASS', ''),
    )

    try:

        tl = rt.search_ticket('creator="{}"'.format(request.user.username))
        tickets = tl.list_all()

    except ConnectionError as e:
        
        print(e)
        return show_msg(request, _("Connection to RT server failed"))

    return render(request, 'webapp/index.html', {

        'tickets': sorted(tickets, reverse=True)[:25],
        'user': request.user.username,

    })


@auth_req
def add_ticket(request):
    '''Show new ticket form.'''
    
    if request.method == 'POST':

        form = AddTicketForm(request.POST)

        if form.is_valid():

            username = request.user.username

            rt = pyrt.RT4(
                rest_url=settings.PYRT.get('REST_URL', ''))
            rt.login(
                username,
                settings.PYRT.get('GLOBAL_PASS', ''),
            )

            queue = settings.PYRT.get('QUEUE', 'support')

            text = form.cleaned_data['message']
            c_text = text.replace('\n', '\n ')
            c_text = c_text.replace('\r', '')
            subject = form.cleaned_data['subject']

            place = form.cleaned_data['place']

            try:

                mail = rt.get_usermail(username)

                ticket_data = {
                    'content':
                    'Queue: {}\nSubject: {} - {}\n'.format(
                        queue,
                        subject,
                        place) +
                    'Text: {}\nRequestor: {}\n'.format(
                        c_text,
                        mail)
                }

                rt.create_ticket(ticket_data)

                return HttpResponseRedirect('/')

            except ConnectionError as e:
                
                print(e)
                return show_msg(
                    request, _("Connection to RT server failed"))

    else:

        form = AddTicketForm()

    return render(request, 'webapp/add_ticket.html', {

        'form': form,

    })


def login(request):
    '''Login page.'''

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            login = form.cleaned_data['login']
            pwd = form.cleaned_data['password']

            user = auth.authenticate(
                username=login, password=pwd)

            #print(user)
            if user and user.is_active:

                auth.login(request, user)

                lang = 'en'
                try:

                    lang = user.i18nuser.lang.lower()

                except ObjectDoesNotExist as e:

                    pass

                request.session['django_language'] = lang

            return HttpResponseRedirect('/')

    else:

        form = LoginForm()
   
    return render(request, 'webapp/login.html', {

        'form': form,

    })


@auth_req
def logout(request):
    '''Logout user, set session message and redirect.'''
    
    auth.logout(request)

    request.session['message'] = (
        _("You have been logged out!")
    )

    return HttpResponseRedirect('/message/')


@auth_req
def add_comment(request, ticket_id):
    '''Add comment for ticket.

    Args:
        ticket_id (str): Ticket's ID.
    '''
    
    if request.method == 'POST':

        form = AddCommentForm(request.POST)

        if form.is_valid():

            rt = pyrt.RT4(
                rest_url=settings.PYRT.get('REST_URL', ''))
            rt.login(
                request.user.username,
                settings.PYRT.get('GLOBAL_PASS', ''),
            )

            text = form.cleaned_data['comment']
            c_text = text.replace('\n', '\n ')
            c_text = c_text.replace('\r', '')

            try:

                ticket = rt.get_ticket(ticket_id)
                ticket.comment(c_text)

            except ConnectionError as e:
                
                print(e)
                return show_msg(
                    request, _("Connection to RT server failed"))

            return HttpResponseRedirect('/')

    else:

        rt = pyrt.RT4(
            rest_url=settings.PYRT.get('REST_URL', ''))
        rt.login(
            request.user.username,
            settings.PYRT.get('GLOBAL_PASS', ''),
        )

        try:

            ticket = rt.get_ticket(ticket_id)
            ticket.load_all()
            content = ticket.history.history_list[-1].get('Content', '')

        except ConnectionError as e:

                print(e)
                return show_msg(
                    request, _("Connection to RT server failed"))

        content2 = ''
        correspond_history = []
        for history in ticket.history.history_list:

            htype = history.get('Type', '')
            if htype in ('Correspond', 'Create'):

                correspond_history.append(history)

        content2 = correspond_history[-1].get('Content', '')
        ch = correspond_history[-1]
        text = []
        text.append('\n')
        text.append(
            ch.get('Creator', '') + ':')

        for line in content2.split('\n'):

            text.append('> ' + line)

        content3 = '\n'.join(text)
        form = AddCommentForm(initial={'comment': content3})

    return render(request, 'webapp/comment.html', {

        'form': form,
        'ticket_id': ticket_id,
        'content': content,

    })


@auth_req
def user_settings(request):
    '''User settings page.'''

    if request.method == 'POST':

        form = SettingsForm(request.POST)

        if form.is_valid():

            lang = form.cleaned_data['lang']
            i18nuser = request.user.i18nuser
            i18nuser.lang = lang
            i18nuser.save()

            request.session['django_language'] = i18nuser.lang

            # RT4 settings
            rt = pyrt.RT4(
                rest_url=settings.PYRT.get('REST_URL', ''))
            rt.login(
                settings.PYRT.get('ROOT', ''),
                settings.PYRT.get('ROOT_PASS', ''),
            )

            # prepare data
            user_data = {
                'content':
                'id: {}\nLang: {}\n'.format(
                    request.user.username,
                    lang,
                 )
            }

            try:

                rt.set_userlang(request.user.username, user_data)

            except ConnectionError as e:
                
                print(e)
                return show_msg(request, _("Connection to RT server failed"))

            return HttpResponseRedirect('/')

    else:

        lang = 'en'
        try:

            lang = request.user.i18nuser.lang.lower()

        except Exception as e:
            
            print(e)

        form = SettingsForm(initial={'lang': lang})

    return render(request, 'webapp/settings.html', {

        'form': form,

    })


def registration(request):
    '''Default registration page.'''
    
    if request.method == 'POST':

        form = RegForm(request.POST)

        if form.is_valid():

            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            lang = form.cleaned_data['lang']

            myldap = wldap.LDAP()
            cas_auth = myldap.check_password(login, password)
            staff = myldap.is_staff(login)
################################################
### DEBUG ONLY
#####################
#            cas_auth = True
#            staff = True
#####################
            if cas_auth and staff:

                #print('Creating user...')
                rt = pyrt.RT4(
                    rest_url=settings.PYRT.get('REST_URL', ''))
                rt.login(
                    settings.PYRT.get('ROOT', ''),
                    settings.PYRT.get('ROOT_PASS', ''),
                )

                data = {
                    'content':
                    ('Name: {}\n'
                     'RealName: {}\n'
                     'Password: {}\n'
                     'EmailAddress: {}\n'
                     'Lang: {}\n'
                     'Privileged: 1\n').format(
                         login,
                         login,
                         settings.PYRT.get('GLOBAL_PASS', ''),
                         email,
                         lang)
                }

                try:

                    #TODO: check user and mail in RT
                    #print(data)
                    # create RT user
                    rt.create_user(data)

                except ConnectionError as e:
                    
                    print(e)
                    return show_msg(
                        request, _("Connection to RT server failed"))

                # create Django user
                dj_pass = settings.PYRT.get('DJ_PASS', 'test')
                from django.contrib.auth.models import User
                from webapp.models import I18nUser
                user = User.objects.create_user(
                    login, email, dj_pass)
                iuser = I18nUser.objects.create(
                    user=user)
                iuser.lang = lang

                user.save()
                iuser.save()

            request.session['message'] = (
                _("User account has been created.")
            )

            return HttpResponseRedirect('/message/')

    else:

        form = RegForm()

    return render(request, 'webapp/registration.html', {

        'form': form,

    })


def message(request):
    '''Show message according to session.'''

    message = request.session.get('message', None)
    request.session['message'] = ''

    return render(request, 'webapp/message.html', {

        'message': message,

    })


def show_msg(request, message):
    '''Set session field and redirect.

    Args:
        message (str): Message string.
    '''

    request.session['message'] = message

    return HttpResponseRedirect('/message/')
