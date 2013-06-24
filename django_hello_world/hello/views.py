import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView, FormView, View
from django_hello_world import settings

from django_hello_world.hello.widgets import ContactForm
from django_hello_world.hello.models import WebRequest, UserProfile


class IndexView(FormView):
    template_name = 'hello/profile.html'
    form_class = ContactForm
    user = User.objects.get(email=u"stu.shurik@gmail.com")
    user_data = {'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email,
                 #'datepicker': user.userprofile.birthday if user.userprofile else None,
                 'bio': user.userprofile.bio if user.userprofile else None,
                 'other': user.userprofile.other if user.userprofile else None,
                 'skype': user.userprofile.skype if user.userprofile else None,
                 'jabber': user.userprofile.jabber if user.userprofile else None,
                 'contacts': user.userprofile.contacts if user.userprofile else None,
                 }

    def get_form(self, form_class):
        return form_class(self.user_data)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['home'] = True
        return context


class ListRequestView(ListView):
    model = WebRequest
    template_name = 'hello/requests.html'


class AuthenticationView(TemplateView):
    template_name = 'hello/login.html'


class UserDataUpdate(FormView):
    template_name = 'hello/profile.html'
    form_class = ContactForm
    user_data = {}

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['pass']
        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            if auth_user.is_active:
                login(request, auth_user)
            self.user_data.update({'first_name': auth_user.first_name,
                                   'last_name': auth_user.last_name,
                                   'email': auth_user.email,
                                   #'datepicker': auth_user.userprofile.birthday if auth_user.userprofile else None,
                                   'bio': auth_user.userprofile.bio if auth_user.userprofile else None,
                                   'other': auth_user.userprofile.other if auth_user.userprofile else None,
                                   'skype': auth_user.userprofile.skype if auth_user.userprofile else None,
                                   'jabber': auth_user.userprofile.jabber if auth_user.userprofile else None,
                                   'contacts': auth_user.userprofile.contacts if auth_user.userprofile else None,
                                   }
                                  )
            return super(UserDataUpdate, self).post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_form(self, form_class):
        return form_class(self.user_data)

    def get_context_data(self, **kwargs):
        context = super(UserDataUpdate, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UploadFile(View):
    def post(self, request, *args, **kwargs):
        if request.FILES:
            user = UserProfile.objects.get(user=request.user)
            uploaded_file = request.FILES['uploaded_file']
            try:
                os.remove(user.avatar.path)
            except ValueError:
                pass
            path = os.path.join(settings.MEDIA_ROOT, 'img/%s' % uploaded_file)
            with open(path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                print destination
                user.avatar = uploaded_file
            user.save()
            os.remove(path)
            return HttpResponse("%s" % user.avatar.path)
        else:
            return HttpResponse("/static/img/default.png")


class DeleteFile(View):
    def post(self, request, *args, **kwargs):
        user = UserProfile.objects.get(user=request.user)
        try:
            os.remove(user.avatar.path)
            user.avatar.name = ''
            user.save()
        except ValueError:
            pass
        return HttpResponse("/static/img/default.png")


class SaveProfile(View):
    def post(self, request, *args, **kwargs):
        try:
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.save()
            request.user.userprofile.birthdate = request.POST['birth']
            request.user.userprofile.bio = request.POST['bio']
            request.user.userprofile.contacts = request.POST['contacts']
            request.user.userprofile.save()
        except:
            pass
        return HttpResponse('Its a trap!')
