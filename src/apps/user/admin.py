from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Base', {'fields': ('username', 'password')}),
        # ('Redes Sociales', {'fields': ('web_site','twitter')}), #temporal
        ('Informacion Peronal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
