from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http import Http404
from .models import Categoria, Cidade, Cliente, Estado, NotaFiscal, Pagamento, Pedido, Produto, Review, Vendedor, Wishlist, Media
from .serializers import CategoriaSchemaSerializer, CategoriaSerializer, CidadeSchemaSerializer, CidadeSerializer, ClienteCreateSchemaSerializer, ClienteSchemaSerializer, ClienteSerializer, EstadoSchemaSerializer, EstadoSerializer, MediaSerializer, NotaFiscalSchemaSerializer, NotaFiscalSerializer, PagamentoSchemaSerializer, PagamentoSerializer, PedidoSchemaSerializer, PedidoSerializer, ProdutoSchemaSerializer, ProdutoSerializer, ProdutoUpdateSchemaSerializer, ReviewPostSerializer, ReviewProductSerializer, ReviewSchemaSerializer, ReviewSerializer, VendedorSchemaSerializer, VendedorSerializer, WishlistSchemaSerializer, WishlistSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import hashlib
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

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

@api_view(['POST'])
def add_estados(request, estados):
    estados = estados.replace('_', ' ')
    estados = estados.split('-')
    for estado in estados:
        est = Estado()
        est.nome = estado
        est.save()

    return Response('Estado(s) adicionado(s) com sucesso!')

@api_view(['DELETE'])
def delete_estado_by_id(request, estado_id):
    estado = Estado.objects.get(estadoId = estado_id)
    estado.delete()

    return Response('Estado deletado com sucesso!')

@swagger_auto_schema(method='put', request_body=EstadoSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_estado(request):
    data = request.data
    estado_id = data["estadoId"]
    estado = Estado.objects.get(estadoId = estado_id)

    estado.nome = data["nome"]
    estado.save()

    serialized_estado = EstadoSerializer(estado)
    return Response(serialized_estado.data)

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

    return Response('Cidades adicionadas com sucesso!')

@api_view(['DELETE'])
def delete_cidade_by_id(request, cidade_id):
    cidade = Cidade.objects.get(cidadeId = cidade_id)
    cidade.delete()

    return Response('Cidade deletada com sucesso')

@swagger_auto_schema(method='put', request_body=CidadeSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_cidade(request):
    data = request.data
    cidade_id = data["cidadeId"]
    cidade = Cidade.objects.get(cidadeId = cidade_id)

    cidade.estadoId = data["estadoId"]
    cidade.nome = data["nome"]
    cidade.save()

    serialized_cidade = CidadeSerializer(cidade)
    return Response(serialized_cidade.data)

@api_view(['GET'])
def get_user_wishlist(request, user_id):
    
    wish_list = Wishlist.objects.filter(clienteId = user_id)
    serialized_wishlist = WishlistSerializer(wish_list, many=True)
    
    product_list = []
    ids_list = []
    for item in serialized_wishlist.data:
        product_list.append(Produto.objects.get(produtoId = item['produtoId']))
        ids_list.append(item['wishlistId'])

    serialized_produtos = ProdutoSerializer(product_list, many=True)

    i = 0
    for prod in serialized_produtos.data:
        prod["wishlistId"] = ids_list[i]
        i+=1

    return Response(serialized_produtos.data)

@api_view(['GET'])
def get_wishlist(request):
    wishlist = Wishlist.objects.all()
    serialized_wishlist = WishlistSerializer(wishlist, many=True)

    return Response(serialized_wishlist.data)

@swagger_auto_schema(method='post', request_body=WishlistSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_wishlist(request):
    data = request.data

    wishlist = Wishlist()
    wishlist.clienteId = data["clienteId"]
    wishlist.produtoId = data["produtoId"]
    wishlist.save()

    serialized_wishlist = WishlistSerializer(wishlist)
    return Response(serialized_wishlist.data)

@api_view(['DELETE'])
def delete_wishlist_by_id(request, wishlist_id):
    wishlist = Wishlist.objects.get(wishlistId = wishlist_id)
    wishlist.delete()

    return Response('Wishlist deletada com sucesso!')

@swagger_auto_schema(method='put', request_body=WishlistSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_wishlist(request):
    data = request.data
    wishlist_id = data["wishlistId"]
    wishlist = Wishlist.objects.get(wishlistId = wishlist_id)

    wishlist.clienteId = data["clienteId"]
    wishlist.produtoId = data["produtoId"]
    wishlist.save()

    serialized_wishlist = WishlistSerializer(wishlist)
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

@swagger_auto_schema(
    operation_id='Send file',
    operation_description='Send file via multipart/form-data',
    method='post',
    manual_parameters=[
        openapi.Parameter('produtoId', openapi.IN_FORM, type=openapi.TYPE_STRING, description='ID do produto'),
        openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='File to upload'),
    ],
    responses={200: openapi.Response('Success')}
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def post_media(request):
    id = request.POST.get('produtoId')
    image = request.FILES.get('file')

    media = Media()
    media.produtoId = id
    media.imagem = image
    media.save()

    serialized_media = MediaSerializer(media)
    
    return Response(serialized_media.data)

@api_view(['DELETE'])
def delete_media(request, media_id):
    media = Media.objects.get(mediaId = media_id)
    media.delete()

    return Response('Media deletada com sucesso!')

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
def get_reviews_by_cliente_id(request, cliente_id):
    reviews = Review.objects.filter(clienteId = cliente_id)
    serialized_reviews = ReviewProductSerializer(reviews, many=True)

    return Response(serialized_reviews.data)

@swagger_auto_schema(method='post', request_body=ReviewPostSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_review(request):
    data = request.data

    review = Review()
    review.clienteId = data["clienteId"]
    review.pedidoId = data["pedidoId"]
    review.produtoId = data["produtoId"]
    review.reviewTitulo = data["reviewTitulo"]
    review.reviewComentario = data["reviewComentario"]
    review.reviewScore = data["reviewScore"]
    review.save()

    serialized_review = ReviewSerializer(review)
    return Response(serialized_review.data)

@api_view(['DELETE'])
def delete_review_by_id(request, review_id):
    review = Review.objects.get(reviewId = review_id)
    review.delete()

    return Response('Review deletada com sucesso!')

@swagger_auto_schema(method='put', request_body=ReviewSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_review(request):
    data = request.data
    review_id = data["reviewId"]
    review = Review.objects.get(reviewId = review_id)

    review.clienteId = data["clienteId"]
    review.pedidoId = data["pedidoId"]
    review.produtoId = data["produtoId"]
    review.reviewTitulo = data["reviewTitulo"]
    review.reviewComentario = data["reviewComentario"]
    review.reviewScore = data["reviewScore"]
    review.save()

    serialized_review = ReviewSerializer(review)
    return Response(serialized_review.data)

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

@swagger_auto_schema(method='post', request_body=NotaFiscalSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_nota_fiscal(request):
    data = request.data

    nfe = NotaFiscal()
    nfe.pedidoId = data["pedidoId"]
    nfe.produtoId = data["produtoId"]
    nfe.vendedorId = data["vendedorId"]
    nfe.nfeQuantidade = data["nfeQuantidade"]
    nfe.nfePreco = data["nfePreco"]
    nfe.nfeFrete = data["nfeFrete"]
    nfe.save()

    serialized_nfe = NotaFiscalSerializer(nfe)
    return Response(serialized_nfe.data)

@api_view(['DELETE'])
def delete_notafiscal_by_id(request, notafiscal_id):
    nfe = NotaFiscal.objects.get(nfeId = notafiscal_id)
    nfe.delete()

    return Response('Nota Fiscal deletada com sucesso!')

@swagger_auto_schema(method='put', request_body=NotaFiscalSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_notafiscal(request):
    data = request.data
    nfe_id = data["nfeId"]
    nfe = NotaFiscal.objects.get(nfeId = nfe_id)
    
    nfe.pedidoId = data["pedidoId"]
    nfe.produtoId = data["produtoId"]
    nfe.vendedorId = data["vendedorId"]
    nfe.nfeQuantidade = data["nfeQuantidade"]
    nfe.nfePreco = data["nfePreco"]
    nfe.nfeFrete = data["nfeFrete"]
    nfe.save()

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

@swagger_auto_schema(method='post', request_body=ClienteCreateSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_cliente(request):
    data = request.data
    email = data["clienteEmail"]
    try:
        vendedor = Vendedor.objects.get(vendedorEmail = email)
    except Vendedor.DoesNotExist:
        try:
            cliente = Cliente.objects.get(clienteEmail = email)
        except Cliente.DoesNotExist:
            cliente = Cliente()
            cliente.clienteNome = data["clienteNome"]
            cliente.clienteEmail = data["clienteEmail"]
            cliente.clienteSenha = data["clienteSenha"]
            cliente.clienteCelular = data["clienteCelular"]
            cliente.clienteCPF = data["clienteCPF"]
            cliente.clienteCEP = data["clienteCEP"]
            cliente.clienteEndereco = data["clienteEndereco"]
            cliente.clienteCidadeId = data["clienteCidadeId"]
            cliente.clienteEstadoId = data["clienteEstadoId"]
            cliente.clienteLatitude = data["clienteLatitude"]
            cliente.clienteLongitude = data["clienteLongitude"]
            cliente.clienteSenha = hashlib.md5(data["clienteSenha"].encode()).hexdigest()

            cliente.save()

            serialized_cliente = ClienteSerializer(cliente)
            return Response({'statusCode': '200', 'data': serialized_cliente.data})
        return Response({'statusCode': '400', 'errorMessage': 'Já existe um usuário com esse email'})
    return Response({'statusCode': '400', 'errorMessage': 'Já existe um usuário com esse email'})

@swagger_auto_schema(method='put', request_body=ClienteSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_cliente(request):
    data = request.data
    cliente_id = data["clienteId"]
    cliente = Cliente.objects.get(clienteId = cliente_id)
    
    cliente.clienteNome = data["clienteNome"]
    cliente.clienteEmail = data["clienteEmail"]
    cliente.clienteCelular = data["clienteCelular"]
    cliente.clienteCPF = data["clienteCPF"]
    cliente.clienteCEP = data["clienteCEP"]
    cliente.clienteEndereco = data["clienteEndereco"]
    cliente.clienteCidadeId = data["clienteCidadeId"]
    cliente.clienteEstadoId = data["clienteEstadoId"]
    cliente.clienteLatitude = data["clienteLatitude"]
    cliente.clienteLongitude = data["clienteLongitude"]
    cliente.clienteIsVendedor = data["clienteIsVendedor"]
    cliente.save()

    serialized_cliente = ClienteSerializer(cliente)

    return Response(serialized_cliente.data)

@api_view(['DELETE'])
def delete_cliente_by_id(request, cliente_id):
    cliente = Cliente.objects.get(clienteId = cliente_id)
    cliente.delete()

    return Response('Cliente deletado com sucesso!')

@api_view(['GET'])
def get_categorias(request):
    try:
        categorias = Categoria.objects.all()
    except Categoria.DoesNotExist:
        raise Http404()
    
    serialized_categorias = CategoriaSerializer(categorias, many=True)
    return Response(serialized_categorias.data)

@api_view(['GET'])
def get_categoria_by_id(request, categoria_id):
    try:
        categoria = Categoria.objects.get(categoriaId = categoria_id)
    except Categoria.DoesNotExist:
        raise Http404()

    serialized_categoria = CategoriaSerializer(categoria)
    return Response(serialized_categoria.data)

@api_view(['POST'])
def create_categoria(request, nome):

    categoria = Categoria()
    categoria.categoriaNome = nome
    categoria.save()

    serialized_categoria = CategoriaSerializer(categoria)
    return Response(serialized_categoria.data)

@api_view(['DELETE'])
def delete_categoria(request, categoria_id):
    categoria = Categoria.objects.get(categoriaId = categoria_id)
    categoria.delete()

    return Response('Categoria deletada com sucesso!')

@swagger_auto_schema(method='put', request_body=CategoriaSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_categoria(request):
    data = request.data
    categoria_id = data["categoriaId"]
    categoria = Categoria.objects.get(categoriaId = categoria_id)

    categoria.categoriaNome = data["categoriaNome"]
    categoria.save()

    serialized_categoria = CategoriaSerializer(categoria)
    return Response(serialized_categoria.data)

@api_view(['GET'])
def get_pagamentos(request):
    pagamentos = Pagamento.objects.all()

    serialized_pagamentos = PagamentoSerializer(pagamentos, many=True)

    return Response(serialized_pagamentos.data)

@api_view(['GET'])
def get_pagamento_by_id(request, pagamento_id):
    pagamento = Pagamento.objects.get(pagamentoId = pagamento_id)
    
    serialized_pagamento = PagamentoSerializer(pagamento)

    return Response(serialized_pagamento.data)

@api_view(['GET'])
def get_pagamento_by_pedido_id(request, pedido_id):
    pagamento = Pagamento.objects.get(pedidoId = pedido_id)

    serialized_pagamento = PagamentoSerializer(pagamento)

    return Response(serialized_pagamento.data)

@swagger_auto_schema(method='post', request_body=PagamentoSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_pagamento(request):
    data = request.data

    pagamento = Pagamento()
    pagamento.clienteId = data["clienteId"]
    pagamento.pedidoId = data["pedidoId"]
    pagamento.pagamentoMetodo = data["pagamentoMetodo"]
    pagamento.pagamentoParcelas = data["pagamentoParcelas"]
    pagamento.pagamentoValorTotal = data["pagamentoValorTotal"]
    pagamento.pagamentoFinalCartao = data["pagamentoFinalCartao"]
    pagamento.save()

    serialized_pagamento = PagamentoSerializer(pagamento)
    return Response(serialized_pagamento.data)

@api_view(['DELETE'])
def delete_pagamento(request, pagamento_id):
    pagamento = Pagamento.objects.get(pagamentoId = pagamento_id)
    pagamento.delete()

    return Response('Pagamento deletado com sucesso!')

@swagger_auto_schema(method='put', request_body=PagamentoSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_pagamento(request):
    data = request.data
    pagamento_id = data["pagamentoId"]
    pagamento = Pagamento.objects.get(pagamentoId = pagamento_id)

    pagamento.clienteId = data["clienteId"]
    pagamento.pedidoId = data["pedidoId"]
    pagamento.pagamentoMetodo = data["pagamentoMetodo"]
    pagamento.pagamentoParcelas = data["pagamentoParcelas"]
    pagamento.pagamentoValorTinal = data["pagamentoValorTinal"]
    pagamento.pagamentoFinalCartao = data["pagamentoFinalCartao"]
    pagamento.save()

    serialized_pagamento = PagamentoSerializer(pagamento)
    return Response(serialized_pagamento.data)

@api_view(['GET'])
def get_pedidos(request):
    pedidos = Pedido.objects.all()

    serialized_pedidos = PedidoSerializer(pedidos, many=True)

    return Response(serialized_pedidos.data)

@api_view(['GET'])
def get_pedido_by_id(request, pedido_id):
    pedido = Pedido.objects.get(pedidoId = pedido_id)

    serialized_pedido = PedidoSerializer(pedido)

    return Response(serialized_pedido.data)

@api_view(['GET'])
def get_pedidos_by_user_id(request, cliente_id):
    pedidos = Pedido.objects.filter(clienteId = cliente_id)

    serialized_pedidos = PedidoSerializer(pedidos, many=True)

    return Response(serialized_pedidos.data)

@swagger_auto_schema(method='post', request_body=PedidoSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_pedido(request):
    data = request.data

    pedido = Pedido()
    pedido.produtoId = data["produtoId"]
    pedido.clienteId = data["clienteId"]
    pedido.vendedorId = data["vendedorId"]
    pedido.pedidoQuantidadeProduto = data["pedidoQuantidadeProduto"]
    pedido.pedidoStatus = data["pedidoStatus"]
    pedido.pedidoDataPagamento = data["pedidoDataPagamento"]
    pedido.pedidoDataTransportadora = data["pedidoDataTransportadora"]
    pedido.pedidoDataPrevista = data["pedidoDataPrevista"]
    pedido.pedidoDataEntregue = data["pedidoDataEntregue"]
    pedido.pedidoAvaliado = False
    pedido.save()

    serialized_pedido = PedidoSerializer(pedido)

    return Response(serialized_pedido.data)

@api_view(['DELETE'])
def delete_pedido_by_id(request, pedido_id):
    pedido = Pedido.objects.get(pedidoId = pedido_id)
    pedido.delete()

    return Response('Pedido deletado com sucesso!')

@swagger_auto_schema(method='put', request_body=PedidoSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_pedido(request):
    data = request.data
    pedido_id = data["pedidoId"]
    pedido = Pedido.objects.get(pedidoId = pedido_id)

    pedido.produtoId = data["produtoId"]
    pedido.clienteId = data["clienteId"]
    pedido.vendedorId = data["vendedorId"]
    pedido.pedidoQuantidadeProduto = data["pedidoQuantidadeProduto"]
    pedido.pedidoStatus = data["pedidoStatus"]
    pedido.pedidoDataPagamento = data["pedidoDataPagamento"]
    pedido.pedidoDataTransportadora = data["pedidoDataTransportadora"]
    pedido.pedidoDataPrevista = data["pedidoDataPrevista"]
    pedido.pedidoDataEntregue = data["pedidoDataEntregue"]
    pedido.pedidoAvaliado = data["pedidoAvaliado"]
    pedido.save()

    serialized_pedido = PedidoSerializer(pedido)
    return Response(serialized_pedido.data)

@api_view(['GET'])
def get_produtos(request):
    produtos = Produto.objects.all()

    serialized_produtos = ProdutoSerializer(produtos, many=True)

    return Response(serialized_produtos.data)

@api_view(['GET'])
def get_produto_by_id(request, produto_id):
    produto = Produto.objects.get(produtoId = produto_id)

    serialized_produto = ProdutoSerializer(produto)

    return Response(serialized_produto.data)

@api_view(['GET'])
def get_produtos_by_categoria_id(request, categoria_id):
    produtos = Produto.objects.filter(categoriaId = categoria_id)

    serialized_produtos = ProdutoSerializer(produtos, many=True)

    return Response(serialized_produtos.data)

@api_view(['GET'])
def get_produtos_by_vendedor_id(request, vendedor_id):
    produtos = Produto.objects.filter(produtoVendedorId = vendedor_id)

    serialized_produtos = ProdutoSerializer(produtos, many=True)

    return Response(serialized_produtos.data)

@swagger_auto_schema(method='post', request_body=ProdutoSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_produto(request):
    data = request.data

    produto = Produto()
    produto.produtoVendedorId = data["produtoVendedorId"]
    produto.produtoCategoriaId = data["produtoCategoriaId"]
    produto.produtoNome = data["produtoNome"]
    produto.produtoDescricao = data["produtoDescricao"]
    produto.produtoPreco = data["produtoPreco"]
    produto.produtoQuantidade = data["produtoQuantidade"]
    produto.produtoAvgScore = 0
    produto.produtoQuantidadeNotas = 0

    produto.save()

    serialized_produto = ProdutoSerializer(produto)

    return Response(serialized_produto.data)

@api_view(['DELETE'])
def delete_all_pedidos(request):
    pedidos = Pedido.objects.all()

    for pedido in pedidos:
        pedido.delete()

    return Response('Deletados com sucesso')

@api_view(['DELETE'])
def delete_produto_by_id(request, produto_id):
    produto = Produto.objects.get(produtoId = produto_id)
    produto.delete()

    return Response('Produto deletado com sucesso!')

@swagger_auto_schema(method='put', request_body=ProdutoUpdateSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_produto(request):
    data = request.data
    produto_id = data["produtoId"]
    produto = Produto.objects.get(produtoId = produto_id)

    produto.produtoVendedorId = data["produtoVendedorId"]
    produto.produtoCategoriaId = data["produtoCategoriaId"]
    produto.produtoNome = data["produtoNome"]
    produto.produtoDescricao = data["produtoDescricao"]
    produto.produtoPreco = data["produtoPreco"]
    produto.produtoQuantidade = data["produtoQuantidade"]
    produto.produtoAvgScore = data["produtoAvgScore"]
    produto.produtoQuantidadeNotas = data["produtoQuantidadeNotas"]
    produto.save()

    serialized_produto = ProdutoSerializer(produto)
    return Response(serialized_produto.data)
    
@api_view(['GET'])
def get_vendedores(request):
    vendedores = Vendedor.objects.all()

    serialized_vendedores = VendedorSerializer(vendedores, many=True)

    return Response(serialized_vendedores.data)

@api_view(['GET'])
def get_vendedor_by_id(request, vendedor_id):
    vendedor = Vendedor.objects.get(vendedorId = vendedor_id)

    serialized_vendedor = VendedorSerializer(vendedor)

    return Response(serialized_vendedor.data)

@api_view(['GET'])
def get_vendedor_by_email(request, email):
    vendedor = Vendedor.objects.get(vendedorEmail = email)

    serialized_vendedor = VendedorSerializer(vendedor)

    return Response(serialized_vendedor.data)

@swagger_auto_schema(method='post', request_body=VendedorSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_vendedor(request):
    data = request.data
    email = data["vendedorEmail"]
    try:
        vendedor = Vendedor.objects.get(vendedorEmail = email)
    except Vendedor.DoesNotExist:
        try:
            cliente = Cliente.objects.get(clienteEmail = email)
        except Cliente.DoesNotExist:
            vendedor = Vendedor()
            vendedor.vendedorNome = data["vendedorNome"]
            vendedor.vendedorEmail = data["vendedorEmail"]
            vendedor.vendedorSenha = data["vendedorSenha"]
            vendedor.vendedorCelular = data["vendedorCelular"]
            vendedor.vendedorCPF = data["vendedorCPF"]
            vendedor.vendedorCEP = data["vendedorCEP"]
            vendedor.vendedorEndereco = data["vendedorEndereco"]
            vendedor.vendedorCidadeId = data["vendedorCidadeId"]
            vendedor.vendedorEstadoId = data["vendedorEstadoId"]
            vendedor.vendedorLatitude = data["vendedorLatitude"]
            vendedor.vendedorLongitude = data["vendedorLongitude"]
            vendedor.vendedorSenha = hashlib.md5(data["vendedorSenha"].encode()).hexdigest()
            vendedor.save()

            serialized_vendedor = VendedorSerializer(vendedor)
            return Response({'statusCode': '200', 'data': serialized_vendedor.data})
        return Response({'statusCode': '400', 'errorMessage': 'Já existe um usuário com esse email'})
    return Response({'statusCode': '400', 'errorMessage': 'Já existe um usuário com esse email'})

@api_view(['DELETE'])
def delete_vendedor_by_id(request, vendedor_id):
    vendedor = Vendedor.objects.get(vendedorId = vendedor_id)
    vendedor.delete()

    return Response('Vendedor deletado com sucesso!')

@swagger_auto_schema(method='put', request_body=VendedorSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['PUT'])
def update_vendedor(request):
    data = request.data
    vendedor_id = data["vendedorId"]
    vendedor = Vendedor.objects.get(vendedorId = vendedor_id)

    vendedor.vendedorNome = data["vendedorNome"]
    vendedor.vendedorEmail = data["vendedorEmail"]
    vendedor.vendedorCelular = data["vendedorCelular"]
    vendedor.vendedorCPF = data["vendedorCPF"]
    vendedor.vendedorCEP = data["vendedorCEP"]
    vendedor.vendedorEndereco = data["vendedorEndereco"]
    vendedor.vendedorCidadeId = data["vendedorCidadeId"]
    vendedor.vendedorEstadoId = data["vendedorEstadoId"]
    vendedor.vendedorLatitude = data["vendedorLatitude"]
    vendedor.vendedorLongitude = data["vendedorLongitude"]
    vendedor.save()

    serialized_vendedor = VendedorSerializer(vendedor)
    return Response(serialized_vendedor.data)

@api_view(['GET'])
def login(request, email, password):
    try:
        cliente = Cliente.objects.get(clienteEmail = email)
        
        if not cliente.clienteSenha == hashlib.md5(password.encode()).hexdigest():
            return Response({'statusCode': '404', 'errorMessage': 'Verifique sua senha.'})

    except Cliente.DoesNotExist:
        try:
            vendedor = Vendedor.objects.get(vendedorEmail = email)

            if not vendedor.vendedorSenha == hashlib.md5(password.encode()).hexdigest():
                return Response({'statusCode': '404', 'errorMessage': 'Verifique sua senha.'})
            
        except Vendedor.DoesNotExist:
            return Response({'statusCode': '404', 'errorMessage': 'Não existe usuário com esse email.'})

        serialized_vendedor = VendedorSerializer(vendedor)
        return Response({'statusCode': '200', 'isVendedor': vendedor.vendedorIsVendedor, 'data': serialized_vendedor.data})

    serialized_cliente = ClienteSerializer(cliente)
    return Response({'statusCode': '200', 'isVendedor': cliente.clienteIsVendedor, 'data': serialized_cliente.data})

def send_email(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            cliente = Cliente.objects.get(clienteEmail = email)

        except Cliente.DoesNotExist:
            try:
                vendedor = Vendedor.objects.get(vendedorEmail = email)
            except Vendedor.DoesNotExist:
                return redirect('/user-not-found')

            d = Context({'email': email})

            subject = 'Recuperar senha ViaSudeste'
            from_email = 'lunettagui@gmail.com'
            to_email = vendedor.vendedorEmail
            print(to_email)

            nome = vendedor.vendedorNome

            if nome == None:
                nome = vendedor.vendedorEmail

            link = 'https://powerful-shelf-46576.herokuapp.com/redefine-password/true/' + str(vendedor.vendedorId)

            text_content = 'Olá ' + nome + '! Clique no link abaixo para redefinir sua senha!\n\n' + link

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.send()

            return redirect('/email-sent')

        d = Context({'email': email})

        subject = 'Recuperar senha ViaSudeste'
        from_email = 'lunettagui@gmail.com'
        to_email = cliente.clienteEmail

        nome = cliente.clienteNome
        if nome == None:
            nome = cliente.clienteEmail
            
        link = 'https://powerful-shelf-46576.herokuapp.com/redefine-password/false/' + str(cliente.clienteId)

        text_content = 'Olá ' + nome + '! Clique no link abaixo para redefinir sua senha!\n\n' + link

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.send()

        return redirect('/email-sent')

    return render(request, 'viasudesteapp/send_email.html')

def error(request):

    if request.method == 'POST':
        return redirect('/send-email')

    return render(request, 'viasudesteapp/error.html')

def email_sent(request):

    return render(request, 'viasudesteapp/email_sent.html')

def redefine(request, id, is_vend):

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password2')

        if password != password_confirm:
            return render(request, 'viasudesteapp/wrong_pass.html')
        else:
            if is_vend == "true":
                vendedor = Vendedor.objects.get(vendedorId = id)
                vendedor.vendedorSenha = password
                vendedor.save()
            else:
                cliente = Cliente.objects.get(clienteId = id)
                cliente.clienteSenha = password
                cliente.save()

            return redirect('/password-redefined')

    return render(request, 'viasudesteapp/redefine_pass.html')

def redefined(request):

    return render(request, 'viasudesteapp/password_redefined.html')