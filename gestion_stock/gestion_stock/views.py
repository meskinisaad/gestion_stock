from django.shortcuts import render, redirect
from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from produits.models import Produit
from stock.models import MouvementStock, SuggestionReapprovisionnement

@login_required
def home(request):
    if request.user.role == 'EMPLOYE':
        return redirect('liste_produits')

    total_produits = Produit.objects.count()
    produits_alerte = Produit.objects.filter(quantite__lte=F('seuil_alerte')).count()
    derniers_produits = Produit.objects.all().order_by('-id')[:5]

    # Valorisation du stock
    valorisation_total = sum(p.valorisation_stock() for p in Produit.objects.all())
    
    # Produits expirés
    produits_expires = Produit.objects.filter(date_expiration__lte=timezone.now().date()).count()
    
    # Produits obsolètes
    produits_obsoletes = Produit.objects.filter(statut_obsolescence__in=['OBSOLETE', 'DISCONTINU']).count()
    
    # Suggestions en attente
    suggestions_en_attente = SuggestionReapprovisionnement.objects.filter(traitee=False).count()

    noms = [p.nom for p in derniers_produits]
    quantites = [p.quantite for p in derniers_produits]

    context = {
        'total_produits': total_produits,
        'produits_alerte': produits_alerte,
        'produits': derniers_produits,
        'noms': noms,
        'quantites': quantites,
        'valorisation_total': valorisation_total,
        'produits_expires': produits_expires,
        'produits_obsoletes': produits_obsoletes,
        'suggestions_en_attente': suggestions_en_attente,
    }
    return render(request, 'home.html', context)
