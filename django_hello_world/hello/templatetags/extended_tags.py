from django.contrib.auth.models import User
from django import template

from django_hello_world.hello.models import UserProfile

register = template.Library()


@register.assignment_tag()
def get_profile(user):
    if isinstance(user, User):
        return UserProfile.objects.get(user=user.id)
    else:
        return None


@register.simple_tag
def edit_link(obj):
    if User.objects.filter(pk=obj.id):
        return "admin/auth/user/%i" % obj.id
    else:
        return None
