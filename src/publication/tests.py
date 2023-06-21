from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Publication, User, validate_file_size_limit_5mb, generate_permalink

# Models #
class PublicationModelTestCase(TestCase):
    def test_validate_file_size_limit_5mb(self):
        # Prueba cuando el tamaño del archivo es menor a 5 MB
        value = SimpleUploadedFile('file.jpg', b'file_content', content_type='image/jpeg')
        self.assertIsNone(validate_file_size_limit_5mb(value))

        # Prueba cuando el tamaño del archivo es mayor a 5 MB
        large_content = b'large_file_content' * (5 * 1024 * 1024 + 1)  # Genera un contenido mayor a 5 MB
        value = SimpleUploadedFile('large_file.jpg', large_content, content_type='image/jpeg')
        with self.assertRaises(ValidationError):
            validate_file_size_limit_5mb(value)

    def test_generate_permalink(self):
        # Prueba la generación del permalink
        permalink = generate_permalink()
        self.assertIsNotNone(permalink)
        self.assertIsInstance(permalink, str)

    def test_publication_save(self):
        # Crea un objeto de usuario para asignarlo a la publicación
        user = User.objects.create(username='testuser')
        # Prueba que el permalink se genere al guardar la publicación
        publication = Publication(media=SimpleUploadedFile('file.jpg', b'file_content', content_type='image/jpeg'), user=user)
        self.assertIsNone(publication.permalink)
        publication.save()
        self.assertIsNotNone(publication.permalink)
        
        # Limpiar los datos de prueba
        publication.media.delete()

    def test_publication_url(self):
        # Prueba que la URL generada tenga el formato esperado
        publication = Publication(media=SimpleUploadedFile('file.jpg', b'file_content', content_type='image/jpeg'))
        url = publication.url
        self.assertTrue(url.startswith('http://127.0.0.1:8000'))
        self.assertIn(publication.media.url, url)

    def test_publication_str(self):
        # Prueba la representación de la instancia Publication
        publication = Publication()
        self.assertEqual(str(publication), f'id: {publication.id} - create_at: {publication.created_at}')

# Utils #
class UtilsFileTestCase(TestCase):
    def test_validate_file_size_limit_5mb(self):
        # Prueba cuando el tamaño del archivo es menor a 5 MB
        value = SimpleUploadedFile('file.jpg', b'file_content', content_type='image/jpeg')
        self.assertIsNone(validate_file_size_limit_5mb(value))

        # Prueba cuando el tamaño del archivo es mayor a 5 MB
        large_content = b'large_file_content' * (5 * 1024 * 1024 + 1)  # Genera un contenido mayor a 5 MB
        value = SimpleUploadedFile('large_file.jpg', large_content, content_type='image/jpeg')
        with self.assertRaises(ValidationError):
            validate_file_size_limit_5mb(value)

    def test_generate_permalink(self):
        # Prueba la generación del permalink
        permalink = generate_permalink()
        self.assertIsNotNone(permalink)
        self.assertIsInstance(permalink, str)
# ...

# Views #

class CreatePublicationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.client.force_login(self.user)     

    def test_create_publication_post(self):
        # Preparar los datos de prueba
        content = b'This is a test image content.'
        media_file = SimpleUploadedFile('test_image.jpg', content, content_type='image/jpeg')

        # Realizar la solicitud POST a la vista
        response = self.client.post(reverse('create_publication'), {'media': media_file})

        # Verificar que la publicación se haya creado correctamente
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Publication.objects.count(), 1)
        publication = Publication.objects.first()
        self.assertEqual(publication.user, self.user)

        # Limpiar los datos de prueba
        publication.media.delete()

    def test_create_publication_get(self):
        # Realizar la solicitud GET a la vista
        response = self.client.get(reverse('create_publication'))

        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publication/create_publication.html')

# ...