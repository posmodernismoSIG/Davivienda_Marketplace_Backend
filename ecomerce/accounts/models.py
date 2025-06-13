from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    """
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Teléfono"
    )
    birth_date = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Fecha de nacimiento"
    )
    address = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Dirección"
    )
    
    # Campos adicionales para el e-commerce
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Usuario verificado"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def has_complete_profile(self):
        """Verifica si el perfil está completo"""
        return all([
            self.first_name,
            self.last_name,
            self.email,
            self.phone,
            self.address
        ])