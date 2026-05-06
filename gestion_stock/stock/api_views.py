from rest_framework import viewsets
from .models import MouvementStock, SuggestionReapprovisionnement
from .serializers import MouvementStockSerializer, SuggestionReapprovisionnementSerializer

class MouvementStockViewSet(viewsets.ModelViewSet):
    queryset = MouvementStock.objects.all()
    serializer_class = MouvementStockSerializer

class SuggestionReapprovisionnementViewSet(viewsets.ModelViewSet):
    queryset = SuggestionReapprovisionnement.objects.all()
    serializer_class = SuggestionReapprovisionnementSerializer