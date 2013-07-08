import json
import os

from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView, View
from django_hello_world import settings

from django_hello_world.hello.forms import UserForm, UserProfileForm
from django_hello_world.hello.models import WebRequest, UserProfile


class DetailFormView(TemplateView):

    template_name = 'hello/profile.html'

    def __init__(self):
        TemplateView.__init__(self)
        self.user_form, self.user_profile_form = None, None

    def get_context_data(self, **kwargs):
        context = super(DetailFormView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['user_form'] = self.user_form
        context['user_profile_form'] = self.user_profile_form
        return context

    def set_forms_data(self, user):
            self.user_form = UserForm(instance=user)
            self.user_profile_form = UserProfileForm(instance=user.userprofile)


class IndexView(DetailFormView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=u"stu.shurik@gmail.com")
            self.set_forms_data(user)
        except:
            pass
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['home'] = True
        return context


class RequestView(TemplateView):
    template_name = 'hello/requests.html'


class RequestListView(ListView):
    template_name = 'hello/request_list.html'

    def post(self, request, *args, **kwargs):
        try:
            start = int(request.POST.get('start', 0))
            end = int(request.POST.get('end', 0))
        except:
            return HttpResponse("Please enter integer value of priority!")
        self.queryset = WebRequest.objects.filter(priority__range=(start, end)).order_by('priority')
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


class LoginFormView(TemplateView):
    template_name = 'hello/login.html'


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class ChangePriority(View):
    def post(self, request, *args, **kwargs):
        response_data = {'success': False,
                         'message': ""
                         }
        request_id = request.POST.get('id')
        if request_id:
            try:
                value = int(request.POST.get('value'))
                try:
                    request_record = WebRequest.objects.get(id=request_id)
                    request_record.priority = value
                    request_record.save()
                    response_data['success'] = True
                    response_data['message'] = "Priority was successful changed!"
                except:
                    response_data['message'] = "Error: with DB operations!"
            except:
                response_data['message'] = "Error: priority value is not integer!"
        else:
            response_data['message'] = "Error: there is no request id!"
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


class Sort(ListView):
    template_name = 'hello/request_list.html'

    def post(self, request, *args, **kwargs):
        field = str(request.POST.get('id'))
        sort_order = request.POST.get('type')
        try:
            start = int(request.POST.get('start', 0))
            end = int(request.POST.get('end', 0))
        except:
            return HttpResponse("Please enter integer value of priority!")
        self.queryset = WebRequest.objects.filter(priority__range=(start, end)).order_by("-" + field if sort_order == 'asc' else field)
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        context['order_' + field] = "desc" if sort_order == 'asc' else 'asc'
        return self.render_to_response(context)


class AuthenticationView(View):

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['pass']

        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('login'))


class UserDataFormView(DetailFormView):

    def get(self, request, *args, **kwargs):
        if get_user(request).is_authenticated():
            self.set_forms_data(get_user(request))
            return super(UserDataFormView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))


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

        def save(obj):
            getattr(obj, 'save')()

        try:
            user = get_user(request)
            user_form = UserForm(instance=user, data=request.POST)
            user_profile_form = UserProfileForm(instance=user.userprofile, data=request.POST)
            for instance in (user_form, user_profile_form):
                save(instance)
        except:
            response_data['success'] = False
            response_data['message'] = "Error while saving data!"
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
