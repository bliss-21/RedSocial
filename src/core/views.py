from django.shortcuts import render
from publication.models import Publication

# Create your views here.
def home(request):

    p = Publication.objects.all()
    data = {
        'p':p,
    }

    return render(request, 'core/home.html', data)