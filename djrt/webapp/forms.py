# -*- encoding: utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _


class AddTicketForm(forms.Form):
    
    subject = forms.CharField(label=_("Subject"))
    plcs = settings.PYRT.get('PLACES')
    place = forms.ChoiceField(
        label=_("Place"),
        initial=settings.PYRT.get('IPLACE'),
        choices=plcs)
    message = forms.CharField(label='', widget=forms.Textarea)


class AddCommentForm(forms.Form):
    
    comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 20, 'cols': 70, 'autofocus': 'autofocus'}))


class LoginForm(forms.Form):
    
    login = forms.CharField(label=_("username"))
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput
    )


class RegForm(forms.Form):
    
    login = forms.CharField(label=_("CAS login"))
    password = forms.CharField(
        label=_("CAS password"),
        widget=forms.PasswordInput
    )
    email = forms.EmailField(label=_("Email"))

    langs = (
        ('EN', _("English")),
        ('CS', _("Czech")),
    )
    lang = forms.ChoiceField(
        initial='CS', label=_("Language"), choices=langs)