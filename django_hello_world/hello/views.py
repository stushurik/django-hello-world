from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView
from django_hello_world.hello.models import WebRequest


class IndexView(TemplateView):

    template_name = 'hello/home.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(email='stu.shurik@gmail.com')
            context['first_name'] = user.first_name
            context['last_name'] = user.last_name
            context['birthday'] = user.userprofile.birthday
            context['bio'] = user.userprofile.bio
            context['email'] = user.email
            context['contacts'] = user.userprofile.contacts
            context['jabber'] = user.userprofile.jabber
            context['skype'] = user.userprofile.skype
            context['other'] = user.userprofile.other
        except User.DoesNotExist:
            pass
        return context

class ListRequestView(ListView):
    model = WebRequest
    template_name = 'hello/requests.html'
