from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'api', api_views.ProduitViewSet)

urlpatterns = [
    path('', views.liste_produits, name='liste_produits'),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('modifier/<int:id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer/<int:id>/', views.supprimer_produit, name='supprimer_produit'),
    path('alerte/', views.produits_alerte, name='produits_alerte'),
    path('', include(router.urls)),
]   

