from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Utilisateur
from .forms import UtilisateurCreationForm, UtilisateurUpdateForm


@admin.register(Utilisateur)
class UtilisateurAdmin(BaseUserAdmin):
    form = UtilisateurUpdateForm
    add_form = UtilisateurCreationForm
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = (
        ('Informations personnelles', {'fields': ('username', 'email', 'first_name', 'last_name')}),
        ('Rôle', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        ('Création d\'utilisateur', {'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')}),
    )
    
    ordering = ('-date_joined',)
