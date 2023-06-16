from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    #if not settings.DEBUG:  # Evita ejecutar esto en entornos de desarrollo
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@mail.com', 'admin')
