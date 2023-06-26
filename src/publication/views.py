from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Publication
from .util import validate_file_size_limit_5mb,  validate_file_extension

def create_publication(request):
    if request.method == 'POST':
        # Obtener los datos enviados por el usuario
        media = request.FILES.get('media')
        user = request.user

        data = {}

        # Validar el tamaño del archivo
        try:
            validate_file_size_limit_5mb(media)
        except ValidationError as e:
            error_message = e.messages[0]
            # return HttpResponse(error_message, status=400)
            data['error_message'] = error_message
            
        # Validar la extensión del archivo
        try:
            validate_file_extension(media)
        except ValidationError as e:
            error_message = e.messages[0]
            # return HttpResponse(error_message, status=400)
            data['error_message'] = error_message

        if "error_message" in data:
            return render(request, 'publication/create_publication.html', data)

        # Crear una nueva instancia de la publicación
        publication = Publication(media=media, user=user)
        publication.save()

        return redirect('me')  # Redirigir a la lista de publicaciones propias

    return render(request, 'publication/create_publication.html')