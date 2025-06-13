from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Campos a mostrar en la lista
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'is_verified', 'is_staff', 'date_joined'
    ]
    
    # Filtros laterales
    list_filter = [
        'is_staff', 'is_superuser', 'is_active', 
        'is_verified', 'date_joined'
    ]
    
    # Campos de búsqueda
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    # Campos editables en línea
    list_editable = ['is_verified']
    
    # Organización de campos en el formulario
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('phone', 'birth_date', 'address', 'is_verified')
        }),
        ('Fechas Importantes', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    # Campos de solo lectura
    readonly_fields = ['created_at', 'updated_at']
    
    # Campos para agregar usuario
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('email', 'first_name', 'last_name', 'phone')
        }),
    )