from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur


class UtilisateurCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, label="Nom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=Utilisateur.ROLE_CHOICES, label="Rôle", widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.current_user = user
        super().__init__(*args, **kwargs)
        if user and getattr(user, 'role', None) == 'GESTIONNAIRE':
            self.fields['role'].choices = [choice for choice in self.fields['role'].choices if choice[0] != 'ADMIN']

        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].help_text = "Au moins 8 caractères"
        self.fields['password2'].help_text = "Confirmation du mot de passe"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet e-mail est déjà utilisé.")
        return email

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role == 'ADMIN' and self.current_user and getattr(self.current_user, 'role', None) == 'GESTIONNAIRE':
            raise forms.ValidationError("Un gestionnaire ne peut pas attribuer le rôle Admin.")
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class UtilisateurUpdateForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.current_user = user
        super().__init__(*args, **kwargs)
        if user and getattr(user, 'role', None) == 'GESTIONNAIRE':
            if self.instance and getattr(self.instance, 'role', None) == 'ADMIN':
                self.fields['role'].disabled = True
            else:
                self.fields['role'].choices = [choice for choice in self.fields['role'].choices if choice[0] != 'ADMIN']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if self.current_user and getattr(self.current_user, 'role', None) == 'GESTIONNAIRE':
            if self.instance and getattr(self.instance, 'role', None) == 'ADMIN' and role != 'ADMIN':
                raise forms.ValidationError("Un gestionnaire ne peut pas modifier le rôle d'un administrateur.")
            if self.instance and getattr(self.instance, 'role', None) != 'ADMIN' and role == 'ADMIN':
                raise forms.ValidationError("Un gestionnaire ne peut pas attribuer le rôle Admin.")
        return role

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse e-mail',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'role': 'Rôle',
            'is_active': 'Actif',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
