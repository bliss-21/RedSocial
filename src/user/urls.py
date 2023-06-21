from django.contrib.auth import views as auth_views
from django.urls import path
from .views import follow_user
urlpatterns = [
    path('follow_user/<id>/', follow_user, name="follow_user"),

    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
