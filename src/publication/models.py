from django.db import models
from django.core.validators import FileExtensionValidator
from .util import validate_file_size_limit_5mb, generate_permalink
from user.models import User

class Publication(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    permalink = models.CharField(max_length=255, blank=True, null=True)

    media = models.FileField(upload_to='publications/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), validate_file_size_limit_5mb])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.permalink:  # Verifica si el permalink ya está generado
            self.permalink = generate_permalink()
        super().save(*args, **kwargs)

    @property
    def url(self):
        # Aquí puedes aplicar la lógica de formateo de la URL según tus necesidades
        return f"http://127.0.0.1:8000{self.media.url}"  # Ejemplo de formateo personalizado

    def __str__(self):
        return f'id: {self.id} - create_at: {self.created_at}'