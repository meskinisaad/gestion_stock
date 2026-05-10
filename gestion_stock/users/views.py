from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Utilisateur
from .forms import UtilisateurCreationForm, UtilisateurUpdateForm
from .decorators import admin_or_gestionnaire_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name or user.username} !')
            if user.role == 'EMPLOYE':
                return redirect('liste_produits')
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')


@admin_or_gestionnaire_required
def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all().order_by('-date_joined')
    return render(request, 'users/liste_utilisateurs.html', {'utilisateurs': utilisateurs})


@admin_or_gestionnaire_required
def creer_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Utilisateur {user.username} créé avec succès en tant que {user.get_role_display()}.')
            return redirect('liste_utilisateurs')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UtilisateurCreationForm(user=request.user)
    
    return render(request, 'users/form_utilisateur.html', {'form': form, 'titre': 'Créer un nouvel utilisateur'})


@admin_or_gestionnaire_required
def modifier_utilisateur(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    
    if request.method == 'POST':
        form = UtilisateurUpdateForm(request.POST, instance=utilisateur, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Utilisateur {utilisateur.username} modifié avec succès.')
            return redirect('liste_utilisateurs')
    else:
        form = UtilisateurUpdateForm(instance=utilisateur, user=request.user)
    
    return render(request, 'users/form_utilisateur.html', {'form': form, 'utilisateur': utilisateur, 'titre': f'Modifier {utilisateur.username}'})


@admin_or_gestionnaire_required
def supprimer_utilisateur(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    
    if request.user.id == utilisateur.id:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte.')
        return redirect('liste_utilisateurs')
    
    if request.method == 'POST':
        nom = utilisateur.username
        utilisateur.delete()
        messages.success(request, f'Utilisateur {nom} supprimé avec succès.')
        return redirect('liste_utilisateurs')
    
    return render(request, 'users/confirmer_suppression.html', {'utilisateur': utilisateur})
