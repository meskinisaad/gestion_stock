from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'seuil_alerte': forms.NumberInput(attrs={'class': 'form-control'}),
            'code_barre': forms.TextInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'fournisseur': forms.Select(attrs={'class': 'form-select'}),
            'date_expiration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut_obsolescence': forms.Select(attrs={'class': 'form-select'}),
            'date_obsolescence': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'nom': 'Nom du produit',
            'description': 'Description',
            'quantite': 'Quantité en stock',
            'seuil_alerte': 'Seuil d\'alerte',
            'code_barre': 'Code-barres',
            'prix': 'Prix unitaire (€)',
            'categorie': 'Catégorie',
            'fournisseur': 'Fournisseur',
            'date_expiration': 'Date de péremption',
            'statut_obsolescence': 'Statut d\'obsolescence',
            'date_obsolescence': 'Date d\'obsolescence',
        }
