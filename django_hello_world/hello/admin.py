from django.contrib import admin
from django_hello_world.hello.models import UserProfile, WebRequest


admin.site.register(UserProfile)
admin.site.register(WebRequest)
