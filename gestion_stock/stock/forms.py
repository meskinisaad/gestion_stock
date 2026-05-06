from django import forms
from .models import MouvementStock

class MouvementStockForm(forms.ModelForm):
    class Meta:
        model = MouvementStock
        fields = ['produit', 'type', 'quantite', 'utilisateur']