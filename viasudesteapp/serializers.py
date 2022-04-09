from rest_framework import serializers
from .models import Cidade, Estado


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['estadoId', 'nome']

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['cidadeId', 'estadoId', 'nome']