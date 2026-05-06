from django.shortcuts import render, redirect, get_object_or_404
from .models import MouvementStock, SuggestionReapprovisionnement
from .forms import MouvementStockForm
from .pdf_reports import (
    generer_rapport_valorisation_pdf,
    generer_rapport_mouvements_pdf,
    generer_rapport_suggestions_pdf,
    generer_rapport_produits_expires_pdf,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from users.decorators import admin_or_gestionnaire_required
from produits.models import Produit


@login_required
def liste_mouvements(request):
    mouvements = MouvementStock.objects.all().order_by('-date')
    return render(request, 'stock/liste_mouvements.html', {'mouvements': mouvements})

@admin_or_gestionnaire_required
def ajouter_mouvement(request):
    if request.method == 'POST':
        form = MouvementStockForm(request.POST)
        if form.is_valid():
            mouvement = form.save(commit=False)
            mouvement.utilisateur = request.user
            mouvement.save()
            
            # Générer une suggestion de réapprovisionnement si le stock est faible
            if mouvement.type == 'SORTIE' and mouvement.produit.quantite <= mouvement.produit.seuil_alerte:
                generer_suggestion_reapprovisionnement(mouvement.produit)
            
            return redirect('liste_mouvements')
    else:
        form = MouvementStockForm()

    return render(request, 'stock/form_mouvement.html', {'form': form})


@login_required
def valorisation_stock(request):
    """Affiche la valorisation complète du stock"""
    produits = Produit.objects.all()
    
    valorisations = []
    valorisation_total = 0
    
    for produit in produits:
        valeur = produit.valorisation_stock()
        valorisation_total += valeur
        valorisations.append({
            'produit': produit,
            'quantite': produit.quantite,
            'prix_unitaire': produit.prix,
            'valeur_totale': valeur,
        })
    
    # Trier par valeur totale décroissante
    valorisations.sort(key=lambda x: x['valeur_totale'], reverse=True)
    
    context = {
        'valorisations': valorisations,
        'valorisation_total': valorisation_total,
    }
    return render(request, 'stock/valorisation_stock.html', context)


@login_required
def analyse_rotation(request):
    """Analyse la rotation des produits (mouvements par période)"""
    produits = Produit.objects.all()
    
    # Période d'analyse (par défaut 30 jours)
    jours = int(request.GET.get('jours', 30))
    date_debut = timezone.now() - timedelta(days=jours)
    
    rotations = []
    for produit in produits:
        # Compter les mouvements
        total_mouvements = MouvementStock.objects.filter(
            produit=produit,
            date__gte=date_debut
        ).count()
        
        # Somme des sorties
        total_sorties = MouvementStock.objects.filter(
            produit=produit,
            type='SORTIE',
            date__gte=date_debut
        ).aggregate(Sum('quantite'))['quantite__sum'] or 0
        
        # Somme des entrées
        total_entrees = MouvementStock.objects.filter(
            produit=produit,
            type='ENTREE',
            date__gte=date_debut
        ).aggregate(Sum('quantite'))['quantite__sum'] or 0
        
        if total_mouvements > 0:
            rotations.append({
                'produit': produit,
                'total_mouvements': total_mouvements,
                'total_entrees': total_entrees,
                'total_sorties': total_sorties,
                'ratio_rotation': total_sorties / produit.quantite if produit.quantite > 0 else 0,
            })
    
    # Trier par rotation décroissante
    rotations.sort(key=lambda x: x['total_mouvements'], reverse=True)
    
    context = {
        'rotations': rotations,
        'jours': jours,
    }
    return render(request, 'stock/analyse_rotation.html', context)


@login_required
def suggestions_reapprovisionnement(request):
    """Affiche les suggestions de réapprovisionnement"""
    suggestions = SuggestionReapprovisionnement.objects.all()
    
    # Filtrer par statut
    traitees = request.GET.get('traitees')
    if traitees == 'oui':
        suggestions = suggestions.filter(traitee=True)
    elif traitees == 'non':
        suggestions = suggestions.filter(traitee=False)
    
    context = {
        'suggestions': suggestions,
        'suggestions_critiques': suggestions.filter(priorite='CRITIQUE').count(),
        'suggestions_en_attente': suggestions.filter(traitee=False).count(),
    }
    return render(request, 'stock/suggestions_reapprovisionnement.html', context)


@admin_or_gestionnaire_required
def traiter_suggestion(request, suggestion_id):
    """Marquer une suggestion comme traitée"""
    suggestion = get_object_or_404(SuggestionReapprovisionnement, id=suggestion_id)
    suggestion.traitee = True
    suggestion.date_traitement = timezone.now()
    suggestion.save()
    return redirect('suggestions_reapprovisionnement')


def generer_suggestion_reapprovisionnement(produit):
    """Génère une suggestion de réapprovisionnement pour un produit"""
    # Éviter les doublons
    if not SuggestionReapprovisionnement.objects.filter(
        produit=produit, 
        traitee=False
    ).exists():
        # Calculer la quantité suggérée (seuil d'alerte * 2)
        quantite_suggeree = produit.seuil_alerte * 2 - produit.quantite
        
        # Déterminer la priorité
        if produit.quantite == 0:
            priorite = 'CRITIQUE'
            raison = 'Stock épuisé'
        elif produit.quantite <= produit.seuil_alerte / 2:
            priorite = 'HAUTE'
            raison = 'Stock critique'
        else:
            priorite = 'NORMALE'
            raison = 'Stock faible'
        
        SuggestionReapprovisionnement.objects.create(
            produit=produit,
            quantite_suggeree=quantite_suggeree,
            priorite=priorite,
            raison=raison,
        )


# ===== VUES D'EXPORT PDF =====

@login_required
def exporter_valorisation_pdf(request):
    """Exporte le rapport de valorisation en PDF"""
    pdf_buffer = generer_rapport_valorisation_pdf()
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_valorisation.pdf"'
    return response


@login_required
def exporter_mouvements_pdf(request):
    """Exporte le rapport des mouvements en PDF"""
    jours = int(request.GET.get('jours', 30))
    pdf_buffer = generer_rapport_mouvements_pdf(jours)
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rapport_mouvements_{jours}j.pdf"'
    return response


@login_required
def exporter_suggestions_pdf(request):
    """Exporte le rapport des suggestions en PDF"""
    pdf_buffer = generer_rapport_suggestions_pdf()
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_suggestions.pdf"'
    return response


@login_required
def exporter_peremption_pdf(request):
    """Exporte le rapport de péremption/obsolescence en PDF"""
    pdf_buffer = generer_rapport_produits_expires_pdf()
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_peremption.pdf"'
    return response
