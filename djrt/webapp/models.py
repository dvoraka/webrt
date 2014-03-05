from django.db import models

from django.contrib.auth.models import User

class I18nUser(models.Model):
    user = models.OneToOneField(User)
    lang = models.CharField(
        max_length=10,
        default='en')
