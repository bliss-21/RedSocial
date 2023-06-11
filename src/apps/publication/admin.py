from django.contrib import admin
from .models import Publication
# Register your models here.

@admin.register(Publication)
class PostAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'active']