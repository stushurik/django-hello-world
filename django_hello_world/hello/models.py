from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField(default=now())
    bio = models.TextField(blank=True)
    contacts = models.CharField(blank=True, max_length=255)
    jabber = models.TextField(blank=True)
    skype = models.TextField(blank=True)
    other = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.email
