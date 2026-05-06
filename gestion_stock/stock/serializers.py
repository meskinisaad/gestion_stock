from rest_framework import serializers
from .models import MouvementStock, SuggestionReapprovisionnement

class MouvementStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouvementStock
        fields = '__all__'

class SuggestionReapprovisionnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionReapprovisionnement
        fields = '__all__'