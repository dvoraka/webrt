# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib import auth
from django.conf import settings

import pyrt
import wldap

from webapp.forms import AddTicketForm
from webapp.forms import AddCommentForm
from webapp.forms import LoginForm
from webapp.forms import RegForm
from webapp.decorators import auth_req


@auth_req
def show_ticket(request, id_):

    rt = pyrt.RT4(
        rest_url=settings.PYRT.get('REST_URL', ''))
    rt.login(
        settings.PYRT.get('ADMIN', ''),
        settings.PYRT.get('PASS', ''),
    )
    ticket = rt.get_ticket(id_)
    ticket.load_all()

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

    rt = pyrt.RT4(
        rest_url=settings.PYRT.get('REST_URL', ''))
    rt.login(
        settings.PYRT.get('ADMIN', ''),
        settings.PYRT.get('PASS', ''),
    )

    tl = rt.search_ticket('creator="{}"'.format(request.user.username))

    tickets = tl.list_all()
    
    return render(request, 'webapp/index.html', {

        'tickets': sorted(tickets, reverse=True)[:25],
        'user': request.user.username,

    })


@auth_req
def add_ticket(request):
    
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

    else:

        form = AddTicketForm()

    return render(request, 'webapp/add_ticket.html', {

        'form': form,

    })


def login(request):

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

            return HttpResponseRedirect('/')

    else:

        form = LoginForm()
   
    return render(request, 'webapp/login.html', {

        'form': form,

    })


@auth_req
def logout(request):
    
    auth.logout(request)

    request.session['message'] = (
        _("You have been logged out!")
    )

    return HttpResponseRedirect('/message/')


@auth_req
def add_comment(request, ticket_id):
    '''Add comment for ticket.

    @type ticket_id: str
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

            ticket = rt.get_ticket(ticket_id)
            ticket.comment(c_text)

            return HttpResponseRedirect('/')

    else:

        rt = pyrt.RT4(
            rest_url=settings.PYRT.get('REST_URL', ''))
        rt.login(
            request.user.username,
            settings.PYRT.get('GLOBAL_PASS', ''),
        )

        ticket = rt.get_ticket(ticket_id)
        ticket.load_all()
        content = ticket.history.history_list[-1].get('Content', '')

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


def registration(request):
    
    if request.method == 'POST':

        form = RegForm(request.POST)

        if form.is_valid():

            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            lang = form.cleaned_data['lang']

################################################
#            myldap = wldap.LDAP()
#            cas_auth = myldap.check_password(login, password)
#            staff = myldap.is_staff(login)
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

                #print(data)
                # create RT user
                rt.create_user(data)

                # create Django user
                dj_pass = settings.PYRT.get('DJ_PASS', 'test')
                from django.contrib.auth.models import User
                user = User.objects.create_user(
                    login, email, dj_pass)
                user.save()

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