import uuid
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_size_limit_5mb(value):
    if value.size > 5 * 1024 * 1024:  # Validar si el tamaño del archivo es superior a 5 MB
        raise ValidationError('El tamaño del archivo debe ser menor o igual a 5 MB.')

def validate_file_extension(value):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    validator = FileExtensionValidator(allowed_extensions)
    validator(value)


def generate_permalink():
    my_uuid = uuid.uuid4()
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")  # Obtiene la fecha actual y la formatea como cadena
    permalink = f"{current_date}-{my_uuid}"
    return permalink
