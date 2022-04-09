from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .models import Cidade, Estado
from .serializers import CidadeSerializer, EstadoSerializer

# Create your views here.

@api_view(['GET'])
def get_estado_by_id(request, estado_id):
    try:
        estado = Estado.objects.get(estadoId = estado_id)
    except Estado.DoesNotExist:
        raise Http404()

    serialized_estado = EstadoSerializer(estado)
    return Response(serialized_estado.data)

@api_view(['GET'])
def get_estados(request):
    try:
        estados = Estado.objects.all()
    except Estado.DoesNotExist:
        raise Http404()

    serialized_estados = EstadoSerializer(estados, many=True)
    return Response(serialized_estados.data)

@api_view(['GET'])
def get_cidade_by_id(request, cidade_id):
    try:
        cidade = Cidade.objects.get(cidadeId = cidade_id)
    except Cidade.DoesNotExist:
        raise Http404()

    serialized_cidade = CidadeSerializer(cidade)
    return Response(serialized_cidade.data)

@api_view(['GET'])
def get_cidades(request):
    try:
        cidades = Cidade.objects.all()
    except Cidade.DoesNotExist:
        raise Http404()

    serialized_cidades = CidadeSerializer(cidades, many=True)
    return Response(serialized_cidades.data)

@api_view(['GET'])
def get_cidades_by_estado_id(request, estado_id):
    try:
        cidades = Cidade.objects.filter(estadoId = estado_id)
    except Cidade.DoesNotExist:
        raise Http404()

    serialized_cidades = CidadeSerializer(cidades, many=True)
    return Response(serialized_cidades.data)

@api_view(['POST'])
def add_cidades_in_estado(request, estado_id, cidades):
    cidades = cidades.replace('_', ' ')
    cidades = cidades.split('-')
    for cidade in cidades:
        cid = Cidade()
        cid.estadoId = estado_id
        cid.nome = cidade
        cid.save()

    return Response('Cidades adicionados com sucesso!')

