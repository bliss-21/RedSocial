from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from apps.user.models import User

def validate_file_size_limit_5mb(value):
    if value.size > 5 * 1024 * 1024:  # Validar si el tamaño del archivo es superior a 5 MB
        raise ValidationError('El tamaño del archivo debe ser menor o igual a 5 MB.')

class Publication(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    permalink = models.CharField(max_length=255)

    media = models.FileField(upload_to='publications/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), validate_file_size_limit_5mb])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.permalink