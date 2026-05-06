from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'mouvements/api', api_views.MouvementStockViewSet)
router.register(r'suggestions/api', api_views.SuggestionReapprovisionnementViewSet)

urlpatterns = [
    path('', views.liste_mouvements, name='liste_mouvements'),
    path('ajouter/', views.ajouter_mouvement, name='ajouter_mouvement'),
    path('valorisation/', views.valorisation_stock, name='valorisation_stock'),
    path('rotation/', views.analyse_rotation, name='analyse_rotation'),
    path('suggestions/', views.suggestions_reapprovisionnement, name='suggestions_reapprovisionnement'),
    path('suggestions/<int:suggestion_id>/traiter/', views.traiter_suggestion, name='traiter_suggestion'),
    
    # Exports PDF
    path('export/valorisation-pdf/', views.exporter_valorisation_pdf, name='exporter_valorisation_pdf'),
    path('export/mouvements-pdf/', views.exporter_mouvements_pdf, name='exporter_mouvements_pdf'),
    path('export/suggestions-pdf/', views.exporter_suggestions_pdf, name='exporter_suggestions_pdf'),
    path('export/peremption-pdf/', views.exporter_peremption_pdf, name='exporter_peremption_pdf'),
    path('', include(router.urls)),
]