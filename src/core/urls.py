from django.urls import path
from .views import home, feed, me

urlpatterns = [
    path('', home, name='home'),
    path('feed', feed, name='feed'),
    path('me', me, name='me'),
]
