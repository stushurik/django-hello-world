from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, FormView

from django_hello_world.hello.widgets import ContactForm
from django_hello_world.hello.models import WebRequest


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
