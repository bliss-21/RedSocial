from django.shortcuts import render
from publication.models import Publication

# Create your views here.
def home(request):

    p = Publication.objects.all()
    data = {
        'p':p,
    }

    return render(request, 'core/home.html', data)

def feed(request):
    my_posts = Publication.objects.all()

    data = {
        'my_posts': my_posts,
    }
    
    return render(request, 'core/feed.html', data)

def me(request):
    
    user_id = request.user.id
    my_posts = Publication.objects.filter(user__id = user_id)

    data = {
        'my_posts': my_posts,
    }

    return render(request, 'core/me.html', data)

