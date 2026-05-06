from django.shortcuts import render, redirect, get_object_or_404
from .models import Commande, LigneCommande
from .forms import CommandeForm, LigneCommandeForm
from django.contrib.auth.decorators import login_required
from users.decorators import admin_or_gestionnaire_required

@login_required
def liste_commandes(request):
    commandes = Commande.objects.all().order_by('-date')
    return render(request, 'commandes/liste_commandes.html', {'commandes': commandes})

@admin_or_gestionnaire_required
def ajouter_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.save()
            return redirect('liste_commandes')
    else:
        form = CommandeForm()

    return render(request, 'commandes/form_commande.html', {'form': form})

@login_required
def detail_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    lignes = commande.lignes.all()
    return render(request, 'commandes/detail_commande.html', {
        'commande': commande,
        'lignes': lignes
    })

@admin_or_gestionnaire_required
def ajouter_ligne_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    if request.method == 'POST':
        form = LigneCommandeForm(request.POST)
        if form.is_valid():
            ligne = form.save(commit=False)
            ligne.commande = commande
            ligne.save()
            return redirect('detail_commande', id=commande.id)
    else:
        form = LigneCommandeForm()

    return render(request, 'commandes/form_ligne_commande.html', {
        'form': form,
        'commande': commande
    })