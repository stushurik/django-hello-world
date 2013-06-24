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
