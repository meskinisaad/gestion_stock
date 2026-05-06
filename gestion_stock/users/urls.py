from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view, logout_view, liste_utilisateurs, creer_utilisateur, modifier_utilisateur, supprimer_utilisateur
from . import api_views

router = DefaultRouter()
router.register(r'utilisateurs/api', api_views.UtilisateurViewSet)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/creer/', creer_utilisateur, name='creer_utilisateur'),
    path('utilisateurs/<int:id>/modifier/', modifier_utilisateur, name='modifier_utilisateur'),
    path('utilisateurs/<int:id>/supprimer/', supprimer_utilisateur, name='supprimer_utilisateur'),
    path('', include(router.urls)),
]
