from sys import stderr

from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = ("prints all project models and \
            the count of objects in every model")
    args = ''

    def handle(self, *args, **options):
        for ct in ContentType.objects.all():
            m = ct.model_class()
            print "%s.%s\t%d" % (m.__module__,
                                 m.__name__,
                                 m._default_manager.count()
                                 )
            print >> stderr, "error:%s.%s\t%d" % (m.__module__,
                                                  m.__name__,
                                                  m._default_manager.count()
                                                  )
