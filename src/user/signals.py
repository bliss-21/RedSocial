from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

@receiver(post_migrate)
def create_admin_user(sender, app_config, **kwargs):
    if app_config.name == 'user' and settings.DEBUG: # Evita ejecutar esto en entornos de desarrollo solo si el nombre de la app corresponde
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@mail.com', 'admin')

@receiver(post_migrate)
def create_users_testing(sender,app_config, **kwargs):
    if app_config.name == 'user' and settings.DEBUG:
        User = get_user_model()
        user = User.objects.filter(is_staff=False)
        if user.count() == 0:
            User.objects.create_user('Alvaro', "Alvaro@mail.xyz", "!pass.123")
            User.objects.create_user('Emilia ', "Emilia@mail.xyz", "!pass.123")
            User.objects.create_user('Loana ', "Loana@mail.xyz", "!pass.123")
            User.objects.create_user('Valentin ', "Valentin@mail.xyz", "!pass.123")
            User.objects.create_user('Ricardo', "Ricardo@mail.xyz", "!pass.123")
            User.objects.create_user('Modesta ', "Modesta@mail.xyz", "!pass.123")

# Idea Futura para iniciar la data
# @receiver(post_migrate)
# def create_initial_data(sender, **kwargs):
#     if kwargs.get('app') == 'tu_app':  # Reemplaza 'tu_app' con el nombre de tu aplicación
#         if not Publication.objects.exists():
#             # Crea una publicación inicial si no existen publicaciones en la base de datos
#             user = User.objects.create(username='admin')
#             Publication.objects.create(content='Contenido de la publicación', user=user)

#         if not Follow.objects.exists():
#             # Crea una relación de seguimiento inicial si no existen relaciones en la base de datos
#             follower = User.objects.create(username='follower')
#             following = User.objects.create(username='following')
#             Follow.objects.create(follower=follower, following=following)
