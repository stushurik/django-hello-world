import json
import os
from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView, FormView, View
from django_hello_world import settings

from django_hello_world.hello.forms import ContactForm
from django_hello_world.hello.models import WebRequest, UserProfile


def set_user_data(dct, user):
    dct.update({'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'bio': user.userprofile.bio if user.userprofile else None,
                'other': user.userprofile.other if user.userprofile else None,
                'skype': user.userprofile.skype if user.userprofile else None,
                'jabber': user.userprofile.jabber if user.userprofile else None,
                'contacts': user.userprofile.contacts if user.userprofile else None,
                }
               )


class DetailFormView(FormView):
    template_name = 'hello/profile.html'
    form_class = ContactForm
    user_data = {}

    def get_form(self, form_class):
        return form_class(self.user_data)

    def get_context_data(self, **kwargs):
        context = super(DetailFormView, self).get_context_data(**kwargs)
        context['host'] = self.request.get_host()
        return context


class IndexView(DetailFormView):
    def get(self, request, *args, **kwargs):
        try:
            self.user = User.objects.get(email=u"stu.shurik@gmail.com")
            set_user_data(self.user_data, self.user)
        except:
            pass
        return super(IndexView, self).get(request, *args, **kwargs)

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


class UserDataUpdate(DetailFormView):

    def get(self, request, *args, **kwargs):
        if get_user(request).is_authenticated():
            set_user_data(self.user_data, get_user(request))
            return super(UserDataUpdate, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['pass']

        auth_user = authenticate(username=username, password=password)
        if auth_user is not None and auth_user.is_active:
            login(request, auth_user)
            set_user_data(self.user_data, auth_user)
            return super(UserDataUpdate, self).post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))

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
        response_data = {'success': True,
                         'message': "Data was successful saved!"
                         }
        try:
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.save()
            request.user.userprofile.birthday = request.POST['birth']
            request.user.userprofile.bio = request.POST['bio']
            request.user.userprofile.contacts = request.POST['contacts']
            request.user.userprofile.skype = request.POST['skype']
            request.user.userprofile.jabber = request.POST['jabber']
            request.user.userprofile.other = request.POST['other']
            request.user.userprofile.email = request.POST['email']
            request.user.userprofile.save()
        except:
            response_data['success'] = False
            response_data['message'] = "Error while saving data!"
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
