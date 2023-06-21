from django.urls import path
from .views import create_publication

urlpatterns = [
    path('create_publication', create_publication, name='create_publication'),
]
