from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produit
from .forms import ProduitForm
from django.db.models import F
from users.decorators import admin_or_gestionnaire_required


@login_required
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits/liste_produits.html', {'produits': produits})

@admin_or_gestionnaire_required
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'produits/form_produit.html', {'form': form})

@admin_or_gestionnaire_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produits/form_produit.html', {'form': form})

@admin_or_gestionnaire_required
def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'produits/confirmer_suppression.html', {'produit': produit})

@login_required
def produits_alerte(request):
    produits = Produit.objects.filter(quantite__lte=F('seuil_alerte'))
    return render(request, 'produits/produits_alerte.html', {'produits': produits})
