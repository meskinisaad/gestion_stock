from django.contrib import admin
from .models import MouvementStock, SuggestionReapprovisionnement

@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'type', 'quantite', 'utilisateur', 'date')
    list_filter = ('type', 'date', 'utilisateur')
    search_fields = ('produit__nom',)
    readonly_fields = ('date',)

@admin.register(SuggestionReapprovisionnement)
class SuggestionReapprovisionnementAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite_suggeree', 'priorite', 'raison', 'traitee', 'date_creation')
    list_filter = ('priorite', 'traitee', 'date_creation')
    search_fields = ('produit__nom', 'raison')
    readonly_fields = ('date_creation', 'date_traitement')
    
    fieldsets = (
        ('Produit et Suggestion', {'fields': ('produit', 'quantite_suggeree', 'raison')}),
        ('Priorité et Statut', {'fields': ('priorite', 'traitee')}),
        ('Dates', {'fields': ('date_creation', 'date_traitement'), 'classes': ('collapse',)}),
    )
