from django.db import models
from datetime import datetime, timedelta

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom



class Produit(models.Model):
    STATUT_OBSOLESCENCE = [
        ('ACTIF', 'Actif'),
        ('OBSOLETE', 'Obsolète'),
        ('DISCONTINU', 'Discontinu'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    quantite = models.IntegerField()
    seuil_alerte = models.IntegerField()
    code_barre = models.CharField(max_length=100)
    prix = models.FloatField()

    # Champs pour péremption et obsolescence
    date_expiration = models.DateField(null=True, blank=True, help_text="Date de péremption du produit")
    statut_obsolescence = models.CharField(max_length=20, choices=STATUT_OBSOLESCENCE, default='ACTIF')
    date_obsolescence = models.DateField(null=True, blank=True, help_text="Date marquant l'obsolescence")

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey("fournisseur.Fournisseur", on_delete=models.CASCADE)
    
    # Traçabilité
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

    def valorisation_stock(self):
        """Retourne la valorisation totale du stock pour ce produit"""
        return self.quantite * self.prix

    def est_expire(self):
        """Vérifie si le produit est expiré"""
        if self.date_expiration:
            return self.date_expiration <= datetime.now().date()
        return False

    def jours_avant_expiration(self):
        """Retourne le nombre de jours avant expiration"""
        if self.date_expiration:
            delta = self.date_expiration - datetime.now().date()
            return delta.days
        return None

    def est_obsolete(self):
        """Vérifie si le produit est obsolète"""
        return self.statut_obsolescence != 'ACTIF'