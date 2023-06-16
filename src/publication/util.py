import uuid
from datetime import datetime
from django.core.exceptions import ValidationError


def validate_file_size_limit_5mb(value):
    if value.size > 5 * 1024 * 1024:  # Validar si el tamaño del archivo es superior a 5 MB
        raise ValidationError('El tamaño del archivo debe ser menor o igual a 5 MB.')
    
def generate_permalink():
    my_uuid = uuid.uuid4()
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")  # Obtiene la fecha actual y la formatea como cadena
    permalink = f"{current_date}-{my_uuid}"
    return permalink
