from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

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