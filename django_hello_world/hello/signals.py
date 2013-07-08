from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_hello_world.hello.models import ModelsOperation


@receiver(post_save)
def callback_save(sender, **kwargs):
    post_save.disconnect(callback_save)
    try:
        mo = ModelsOperation()
        mo.model_class = kwargs['instance'].__class__.__name__
        if kwargs['created']:
            mo.operation = 'Creation'
        else:
            mo.operation = 'Editing'
        mo.save()
    except:
        pass
    post_save.connect(callback_save)


@receiver(post_delete)
def callback_delete(sender, **kwargs):
    post_delete.disconnect(callback_delete)
    try:
        mo = ModelsOperation()
        mo.model_class = kwargs['instance'].__class__.__name__
        mo.operation = 'Deletion'
        mo.save()
    except:
        pass
    post_delete.connect(callback_delete)
