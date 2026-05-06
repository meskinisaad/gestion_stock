from django.db import models
from produits.models import Produit
from fournisseur.models import Fournisseur

class Commande(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50)

    def __str__(self):
        return f"Commande {self.id}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix = models.FloatField()

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"