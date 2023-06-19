from django.urls import path
from .views import follow_user
urlpatterns = [
    path('follow_user/<id>/', follow_user, name="follow_user"),
]
