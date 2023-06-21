from django.shortcuts import render, redirect
from .models import Publication

def create_publication(request):
    if request.method == 'POST':
        # Obtener los datos enviados por el usuario
        media = request.FILES.get('media')
        user = request.user

        # Crear una nueva instancia de la publicación
        publication = Publication(media=media, user=user)
        publication.save()

        return redirect('me')  # Redirigir a la lista de publicaciones propias

    return render(request, 'publication/create_publication.html')