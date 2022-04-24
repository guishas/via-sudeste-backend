from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http import Http404
from .models import Categoria, Cidade, Cliente, Estado, NotaFiscal, Pagamento, Pedido, Produto, Review, Vendedor, Wishlist, Media
from .serializers import CategoriaSchemaSerializer, CategoriaSerializer, CidadeSchemaSerializer, CidadeSerializer, ClienteSchemaSerializer, ClienteSerializer, EstadoSchemaSerializer, EstadoSerializer, MediaSerializer, NotaFiscalSchemaSerializer, NotaFiscalSerializer, PagamentoSerializer, PedidoSerializer, ProdutoSchemaSerializer, ProdutoSerializer, ReviewSerializer, VendedorSerializer, WishlistSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    for item in serialized_wishlist.data:
        product_list.append(Produto.objects.get(produtoId = item['produtoId']))

    serialized_produtos = ProdutoSerializer(product_list, many=True)

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

@swagger_auto_schema(method='post', request_body=ReviewSerializer, responses={200: openapi.Response('Success')})
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

@swagger_auto_schema(method='post', request_body=ClienteSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_cliente(request):
    data = request.data
    cliente = Cliente()
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
def get_pedidos_by_user_id(request, user_id):
    pedidos = Pedido.objects.filter(userId = user_id)

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
    pedido.pagamentoId = data["pagamentoId"]
    pedido.pedidoQuantidadeProduto = data["pedidoQuantidadeProduto"]
    pedido.pedidoStatus = data["pedidoStatus"]
    pedido.pedidoDataPagamento = data["pedidoDataPagamento"]
    pedido.pedidoDataTransportadora = data["pedidoDataTransportadora"]
    pedido.pedidoDataPrevista = data["pedidoDataPrevista"]
    pedido.pedidoDataEntregue = data["pedidoDataEntregue"]
    pedido.save()

    serialized_pedido = PedidoSerializer(pedido)

    return Response(serialized_pedido.data)

@api_view(['DELETE'])
def delete_pedido_by_id(request, pedido_id):
    pedido = Pedido.objects.get(pedidoId = pedido_id)
    pedido.delete()

    return Response('Pedido deletado com sucesso!')

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

@swagger_auto_schema(method='post', request_body=ProdutoSchemaSerializer, responses={200: openapi.Response('Success')})
@api_view(['POST'])
def create_produto(request):
    data = request.data

    produto = Produto()
    produto.produtoCategoriaId = data["produtoCategoriaId"]
    produto.produtoNome = data["produtoNome"]
    produto.produtoDescricao = data["produtoDescricao"]
    produto.produtoPreco = data["produtoPreco"]
    produto.produtoQuantidade = data["produtoQuantidade"]
    produto.produtoAvgScore = data["produtoAvgScore"]
    produto.produtoQuantidadeNotas = data["produtoQuantidadeNotas"]
    produto.save()

    serialized_produto = ProdutoSchemaSerializer(produto)

    return Response(serialized_produto.data)

@api_view(['DELETE'])
def delete_produto_by_id(request, produto_id):
    produto = Produto.objects.get(produtoId = produto_id)
    produto.delete()

    return Response('Produto deletado com sucesso!')

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
    vendedor.vendedorIsVendedor = data["vendedorIsVendedor"]
    vendedor.save()

    serialized_vendedor = VendedorSerializer(vendedor)

    return Response(serialized_vendedor.data)

@api_view(['DELETE'])
def delete_vendedor_by_id(request, vendedor_id):
    vendedor = Vendedor.objects.get(vendedorId = vendedor_id)
    vendedor.delete()

    return Response('Vendedor deletado com sucesso!')