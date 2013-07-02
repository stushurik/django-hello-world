from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


def make_upload_path(instance, filename):
    return u"img/%s_%s" % (now(), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField(default=now())
    bio = models.TextField(blank=True)
    contacts = models.CharField(blank=True, max_length=255)
    jabber = models.CharField(blank=True, max_length=255)
    skype = models.CharField(blank=True, max_length=255)
    other = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=make_upload_path, null=True, blank=True)

    def __unicode__(self):
        return self.user.email


class WebRequest(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=2000)
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    remote_addr = models.IPAddressField()
    remote_addr_fwd = models.IPAddressField(blank=True, null=True)
    meta = models.TextField()
    cookies = models.TextField(blank=True, null=True)
    get = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    raw_post = models.TextField(blank=True, null=True)
    is_secure = models.BooleanField()
    is_ajax = models.BooleanField()
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.time, self.host)
