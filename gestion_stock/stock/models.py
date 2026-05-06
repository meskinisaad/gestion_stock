from django.db import models
from django.utils import timezone
from datetime import timedelta
from produits.models import Produit
from users.models import Utilisateur

class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='mouvements')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantite = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.type == 'ENTREE':
                self.produit.quantite += self.quantite
            elif self.type == 'SORTIE':
                self.produit.quantite -= self.quantite

            self.produit.save()
    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} - {self.produit.nom}"


class SuggestionReapprovisionnement(models.Model):
    PRIORITE_CHOICES = [
        ('BASSE', 'Basse'),
        ('NORMALE', 'Normale'),
        ('HAUTE', 'Haute'),
        ('CRITIQUE', 'Critique'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='suggestions')
    quantite_suggeree = models.IntegerField()
    priorite = models.CharField(max_length=20, choices=PRIORITE_CHOICES, default='NORMALE')
    raison = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    traitee = models.BooleanField(default=False)

    def __str__(self):
        return f"Suggestion {self.produit.nom} - {self.priorite}"

    class Meta:
        ordering = ['-priorite', '-date_creation']