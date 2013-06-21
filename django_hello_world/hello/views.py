from django.contrib.auth.models import User
from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = 'hello/home.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        user = User.objects.get(email='stu.shurik@gmail.com')
        data = (user.first_name,
                user.last_name,
                user.userprofile.birthday,
                user.userprofile.bio,
                user.email,
                user.userprofile.contacts,
                user.userprofile.jabber,
                user.userprofile.skype,
                user.userprofile.other,
        )
        context['data'] = data
        return context
