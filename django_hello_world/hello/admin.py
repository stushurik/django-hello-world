from django.contrib import admin

from django_hello_world.hello.models import UserProfile, WebRequest, ModelsOperation


admin.site.register(UserProfile)
admin.site.register(WebRequest)
admin.site.register(ModelsOperation)
