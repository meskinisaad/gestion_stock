from django.contrib import admin
from .models import Produit, Categorie
from fournisseur.models import Fournisseur

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'prix', 'valorisation_stock', 'seuil_alerte', 'date_expiration', 'statut_obsolescence', 'categorie', 'fournisseur')
    list_filter = ('categorie', 'fournisseur', 'statut_obsolescence', 'date_expiration')
    search_fields = ('nom', 'code_barre')
    
    fieldsets = (
        ('Informations générales', {'fields': ('nom', 'description', 'code_barre', 'categorie', 'fournisseur')}),
        ('Stock et Tarification', {'fields': ('quantite', 'prix', 'seuil_alerte')}),
        ('Péremption et Obsolescence', {'fields': ('date_expiration', 'statut_obsolescence', 'date_obsolescence')}),
        ('Traçabilité', {'fields': ('date_creation', 'date_modification'), 'classes': ('collapse',)}),
    )
    
    readonly_fields = ('date_creation', 'date_modification')

admin.site.register(Categorie)
admin.site.register(Fournisseur)

