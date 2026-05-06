from django.contrib import admin
from .models import Commande, LigneCommande

admin.site.register(Commande)
admin.site.register(LigneCommande)