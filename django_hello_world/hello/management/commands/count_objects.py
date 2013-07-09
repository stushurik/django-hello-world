from sys import stderr, stdout

from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = ("prints all project models and \
            the count of objects in every model")
    args = ''

    def handle(self, *args, **options):
        for ct in ContentType.objects.all():
            try:
                m = ct.model_class()
                message = (m.__name__,
                           m._default_manager.count()
                           )
                stdout.writelines("%s\t%d\n" % message)
                stderr.writelines("error:%s\t%d\n" % message)
            except:
                pass
