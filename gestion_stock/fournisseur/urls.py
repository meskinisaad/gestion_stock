from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'api', api_views.FournisseurViewSet)

urlpatterns = [
    path('', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('ajouter/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('modifier/<int:id>/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('supprimer/<int:id>/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('', include(router.urls)),
]