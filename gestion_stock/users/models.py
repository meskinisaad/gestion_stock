from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('GESTIONNAIRE', 'Gestionnaire'),
        ('EMPLOYE', 'Employé'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYE')
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_gestionnaire(self):
        return self.role == 'GESTIONNAIRE'
    
    def is_employe(self):
        return self.role == 'EMPLOYE'
