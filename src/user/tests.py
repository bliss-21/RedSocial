from django.test import TestCase,Client
from django.urls import reverse

from .models import Follow, User

# Sección testeo Models
class FollowModelTestCase(TestCase):
    def setUp(self):
        self.follower_user = User.objects.create_user(username='follower', email="follower.test@mail.xyz")
        self.following_user = User.objects.create_user(username='following', email="following.test@mail.xyz")

    def test_follow_creation(self):
        follow = Follow.objects.create(follower=self.follower_user, following=self.following_user)
        
        self.assertEqual(follow.follower, self.follower_user)
        self.assertEqual(follow.following, self.following_user)
        self.assertIsNotNone(follow.created_at)

    def test_unique_follow(self):
        # Intenta crear una relación de seguimiento duplicada
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.follower_user, following=self.following_user)
            Follow.objects.create(follower=self.follower_user, following=self.following_user)

    def test_get_followers(self):
        # Crea algunas relaciones de seguimiento
        Follow.objects.create(follower=self.follower_user, following=self.following_user)
        Follow.objects.create(follower=self.follower_user, following=User.objects.create_user(username='another_user', email="another_user@mail.xyz"))
        Follow.objects.create(follower=User.objects.create_user(username='user3', email="user3@mail.xyz"), following=self.following_user)

        # Obtiene los seguidores del usuario
        followers = self.following_user.followers.all()

        self.assertEqual(followers.count(), 2)
        self.assertTrue(followers.filter(follower=self.follower_user).exists(), 'El usuario seguidor no se encontró en la lista de seguidores.')
        self.assertFalse(followers.filter(follower=self.following_user).exists(), 'El usuario seguido está presente en la lista de seguidores.')

    def test_get_following(self):
        # Crea algunas relaciones de seguimiento
        Follow.objects.create(follower=self.follower_user, following=self.following_user)
        Follow.objects.create(follower=User.objects.create_user(username='another_user', email="another_user@mail.xyz"), following=self.following_user)
        Follow.objects.create(follower=self.follower_user, following=User.objects.create_user(username='user3', email="user3@mail.xyz"))

        # Obtiene los usuarios seguidos por el usuario
        following = self.follower_user.following.all()

        self.assertEqual(following.count(), 2)
        self.assertTrue(following.filter(following=self.following_user).exists(), 'El usuario seguido no se encontró en la lista de usuarios seguidos.')
        self.assertFalse(following.filter(following=self.follower_user).exists(), 'El usuario seguidor está presente en la lista de usuarios seguidos.')
# ...

# Sección testeo Views
class Follow_UserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email="testuser@mail.xyz")
        self.another_user = User.objects.create_user(username='anotheruser', password='testpassword', email="anotheruser@mail.xyz")
        # Simula el inicio de sesión del usuario
        self.client.force_login(self.user)
        
    def test_follow_user(self):
        # Simula una solicitud POST para seguir al usuario
        response = self.client.post('/follow_user/{}/'.format(self.another_user.id))

        # Verifica el resultado de la solicitud
        self.assertEqual(response.status_code, 200)  # Ajusta el código de estado según corresponda

        # Verifica los cambios en la base de datos
        follow = Follow.objects.filter(follower=self.user, following=self.another_user).first()
        self.assertIsNotNone(follow)  # Se espera que se haya creado un registro Follow

        # Simula otra solicitud POST para dejar de seguir al usuario
        response = self.client.post('/follow_user/{}/'.format(self.another_user.id))

        # Verifica el resultado de la segunda solicitud
        self.assertEqual(response.status_code, 200)  # Ajusta el códigwo de estado según corresponda

        # Verifica los cambios en la base de datos
        follow = Follow.objects.filter(follower=self.user, following=self.another_user).first()
        self.assertIsNone(follow)  # Se espera que el registro Follow se haya eliminado
# ...

# Sección testeo Urls
class FollowUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email="testuser@mail.xyz")
        self.another_user = User.objects.create_user(username='anotheruser', password='testpassword', email="anotheruser@mail.xyz")
        # Simula el inicio de sesión del usuario
        self.client.force_login(self.user)
        
    def test_follow_user_login(self):

        # Obtener la URL de la vista follow_user para el usuario self.another_user
        url = reverse('follow_user', kwargs={'id': self.another_user.id})

        # Realizar una solicitud POST a la URL
        response = self.client.post(url)

        # Verificar que la respuesta tenga el código de estado correcto
        self.assertEqual(response.status_code, 200)

    def test_follow_user_logout(self):

        # Desloguear al usuario
        self.client.logout()

        # Iniciar sesión como self.user
        self.client.login(username='testuser', password='testpassword')

        # Obtener la URL de la vista follow_user para el usuario self.another_user
        url = reverse('follow_user', kwargs={'id': self.another_user.id})

        # Realizar una solicitud POST a la URL
        response = self.client.post(url)

        # Verificar que la respuesta tenga el código de estado correcto
        self.assertEqual(response.status_code, 302)
# ...