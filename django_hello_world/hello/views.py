from django.contrib.auth.models import User
from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = 'hello/home.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            context['admin_user'] = User.objects.get(email='stu.shurik@gmail.com')
        except User.DoesNotExist:
            pass
        return context
