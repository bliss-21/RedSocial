# publications/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Publication

@receiver(pre_delete, sender=Publication)
def delete_media_file(sender, instance, **kwargs):
    # Eliminar el archivo de medios asociado
    instance.media.delete()