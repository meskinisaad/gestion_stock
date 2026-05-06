from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'api', api_views.CommandeViewSet)

urlpatterns = [
    path('', views.liste_commandes, name='liste_commandes'),
    path('ajouter/', views.ajouter_commande, name='ajouter_commande'),
    path('<int:id>/', views.detail_commande, name='detail_commande'),
    path('<int:commande_id>/ligne/ajouter/', views.ajouter_ligne_commande, name='ajouter_ligne_commande'),
    path('', include(router.urls)),
]