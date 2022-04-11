from rest_framework.decorators import api_view
from django.urls import path
from rest_framework.response import Response
from django.http import Http404
from .models import Cidade, Cliente, Estado, NotaFiscal, Produto, Review, Wishlist, Media
from .serializers import CidadeSerializer, ClienteSerializer, EstadoSerializer, MediaSerializer, NotaFiscalSerializer, ProdutoSerializer, ReviewSerializer, WishlistSerializer
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title = 'Viasudeste API V1')
# Create your views here.

urlpatterns = [
    path(r'^$', schema_view),
]

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

@api_view(['GET'])
def get_user_wishlist(request, user_id):
    
    wish_list = Wishlist.objects.filter(clienteId = user_id)
    print(wish_list)
    serialized_wishlist = WishlistSerializer(wish_list, many=True)
    
    product_list = []
    for item in serialized_wishlist.data:
        product_list.append(Produto.objects.get(produtoId = item['produtoId']))

    serialized_produtos = ProdutoSerializer(product_list, many=True)

    return Response(serialized_produtos.data)

@api_view(['GET'])
def get_wishlist(request):
    wishlist = Wishlist.objects.all()
    serialized_wishlist = WishlistSerializer(wishlist, many=True)

    return Response(serialized_wishlist.data)

@api_view(['GET'])
def get_medias(request):
    medias = Media.objects.all()
    serialized_medias = MediaSerializer(medias, many=True)
    
    for media in serialized_medias.data:
        media['imagem'] = 'http://localhost:8000' + media['imagem']

    return Response(serialized_medias.data)

@api_view(['GET'])
def get_medias_by_product_id(request, product_id):
    medias = Media.objects.filter(produtoId = product_id)
    serialized_medias = MediaSerializer(medias, many=True)
    
    for media in serialized_medias.data:
        media['imagem'] = 'http://localhost:8000' + media['imagem']

    return Response(serialized_medias.data)

@api_view(['GET'])
def get_reviews(request):
    reviews = Review.objects.all()
    serialized_reviews = ReviewSerializer(reviews, many=True)

    return Response(serialized_reviews.data)

@api_view(['GET'])
def get_reviews_by_product_id(request, product_id):
    reviews = Review.objects.filter(produtoId = product_id)
    serialized_reviews = ReviewSerializer(reviews, many=True)

    return Response(serialized_reviews.data)

@api_view(['GET'])
def get_notas_ficais(request):
    nfes = NotaFiscal.objects.all()
    serialized_nfes = NotaFiscalSerializer(nfes, many=True)

    return Response(serialized_nfes.data)

@api_view(['GET'])
def get_nota_fiscal_by_pedido_id(request, pedido_id):
    nfe = NotaFiscal.objects.get(pedidoId = pedido_id)
    serialized_nfe = NotaFiscalSerializer(nfe)

    return Response(serialized_nfe.data)

@api_view(['GET'])
def get_clientes(request):
    clientes = Cliente.objects.all()
    serialized_clientes = ClienteSerializer(clientes, many=True)

    return Response(serialized_clientes.data)

@api_view(['GET'])
def get_cliente_by_id(request, user_id):
    cliente = Cliente.objects.get(clienteId = user_id)
    serialized_cliente = ClienteSerializer(cliente)

    return Response(serialized_cliente.data)

@api_view(['GET'])
def get_cliente_by_email(request, email):
    try:
        cliente = Cliente.objects.get(clienteEmail = email)
    except Cliente.DoesNotExist:
        return Response('Não existe um usuário com esse e-mail.')

    serialized_cliente = ClienteSerializer(cliente)
    return Response(serialized_cliente.data)