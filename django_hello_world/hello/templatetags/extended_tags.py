from django.core.urlresolvers import NoReverseMatch
from django.contrib.auth.models import User
from django import template

from django_hello_world.hello.models import UserProfile
from django.core import urlresolvers

register = template.Library()


@register.assignment_tag()
def get_profile(user):
    if isinstance(user, User):
        return UserProfile.objects.get(user=user.id)
    else:
        return None


@register.simple_tag
def edit_link(obj):
    change_url = ''
    obj_id = getattr(obj, 'id', None)
    app_label = obj.__module__.split('.')[-2]
    model_name = type(obj).__name__.lower()
    url = 'admin:%s_%s_change' %(app_label, model_name)
    try:
        change_url = urlresolvers.reverse(url, args=(obj_id, ))
    except NoReverseMatch:
        pass
    return change_url


