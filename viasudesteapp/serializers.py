import hashlib
from rest_framework import serializers
from .models import Categoria, Cidade, Cliente, Estado, Media, NotaFiscal, Pagamento, Pedido, Produto, Review, Vendedor, Wishlist


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['estadoId', 'nome']

class EstadoSchemaSerializer(serializers.ModelSerializer):

    estadoId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Estado
        fields = ['estadoId', 'nome']

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['cidadeId', 'estadoId', 'nome']

class CidadeSchemaSerializer(serializers.ModelSerializer):

    cidadeId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Cidade
        fields = ['cidadeId', 'estadoId', 'nome']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class WishlistSchemaSerializer(serializers.ModelSerializer):

    wishlistId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Wishlist
        fields = ['wishlistId', 'clienteId', 'produtoId']

class ProdutoSerializer(serializers.ModelSerializer):

    produtoCategoria = serializers.SerializerMethodField('get_categoria')
    produtoVendedor = serializers.SerializerMethodField('get_vendedor')
    produtoImagem = serializers.SerializerMethodField('get_imagem')

    def get_imagem(self, produto_object):
        try:
            imagem = Media.objects.get(produtoId = produto_object.produtoId)
            serialized_imagem = MediaSerializer(imagem)
        except Media.DoesNotExist:
            return None

        return "https://powerful-shelf-46576.herokuapp.com" + serialized_imagem.data["imagem"]

    def get_vendedor(self, produto_object):
        vendedor = Vendedor.objects.get(vendedorId = produto_object.produtoVendedorId)
        serialized_vendedor = VendedorSerializer(vendedor)
        return serialized_vendedor.data

    def get_categoria(self, produto_object):
        categoria = Categoria.objects.get(categoriaId = produto_object.produtoCategoriaId)
        serialized_categoria = CategoriaSerializer(categoria)
        return serialized_categoria.data

    class Meta:
        model = Produto
        fields = ['produtoId', 'produtoVendedor', 'produtoCategoria', 'produtoNome', 'produtoDescricao',
         'produtoPreco', 'produtoQuantidade', 'produtoAvgScore', 'produtoQuantidadeNotas', 'produtoImagem']

class ProdutoSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['produtoVendedorId', 'produtoCategoriaId', 'produtoNome', 
        'produtoDescricao', 'produtoPreco', 'produtoQuantidade']

class ProdutoUpdateSchemaSerializer(serializers.ModelSerializer):

    produtoId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Produto
        fields = ['produtoId', 'produtoVendedorId', 'produtoCategoriaId', 'produtoNome', 'produtoDescricao', 'produtoPreco',
                  'produtoQuantidade', 'produtoAvgScore', 'produtoQuantidadeNotas']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class CategoriaSchemaSerializer(serializers.ModelSerializer):

    categoriaId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Categoria
        fields = ['categoriaId', 'categoriaNome']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):

    reviewCliente = serializers.SerializerMethodField('get_cliente')

    def get_cliente(self, review_object):
        cliente = Cliente.objects.get(clienteId = review_object.clienteId)
        serialized_cliente = ClienteSerializer(cliente)
        return serialized_cliente.data

    class Meta:
        model = Review
        fields = ['reviewId', 'reviewCliente', 'pedidoId', 'produtoId', 'reviewTitulo', 'reviewComentario', 'reviewScore']

class ReviewProductSerializer(serializers.ModelSerializer):

    reviewCliente = serializers.SerializerMethodField('get_cliente')
    reviewProduto = serializers.SerializerMethodField('get_produto')

    def get_produto(self, review_object):
        produto = Produto.objects.get(produtoId = review_object.produtoId)
        serialized_produto = ProdutoSerializer(produto)
        return serialized_produto.data

    def get_cliente(self, review_object):
        cliente = Cliente.objects.get(clienteId = review_object.clienteId)
        serialized_cliente = ClienteSerializer(cliente)
        return serialized_cliente.data

    class Meta:
        model = Review
        fields = ['reviewId', 'reviewCliente', 'pedidoId', 'reviewProduto', 'reviewTitulo', 'reviewComentario', 'reviewScore']

class ReviewPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class ReviewSchemaSerializer(serializers.ModelSerializer):

    reviewId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Review
        fields = ['reviewId', 'clienteId', 'pedidoId', 'produtoId', 'reviewTitulo', 'reviewComentario', 'reviewScore']

class NotaFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaFiscal
        fields = '__all__'

class NotaFiscalSchemaSerializer(serializers.ModelSerializer):

    nfeId = serializers.UUIDField(write_only = True)

    class Meta:
        model = NotaFiscal
        fields = ['nfeId', 'pedidoId', 'produtoId', 'vendedorId', 'nfeQuantidade', 'nfePreco', 'nfeFrete']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["clienteId", "clienteNome", "clienteEmail", "clienteSenha", "clienteCelular", "clienteCPF",
         "clienteCEP", "clienteEndereco", "clienteCidadeId", "clienteEstadoId", "clienteLatitude", "clienteLongitude", "clienteIsVendedor"]

class ClienteCreateSchemaSerializer(serializers.ModelSerializer):

    clienteSenha = serializers.CharField(write_only = True)

    class Meta:
        model = Cliente
        fields = ["clienteId", "clienteNome", "clienteEmail", "clienteSenha", "clienteCelular", "clienteCPF",
         "clienteCEP", "clienteEndereco", "clienteCidadeId", "clienteEstadoId", "clienteLatitude", "clienteLongitude"]

class ClienteSchemaSerializer(serializers.ModelSerializer):

    clienteId = serializers.UUIDField(write_only = True)
    clienteSenha = serializers.SerializerMethodField('get_senha')

    def get_senha(self, cliente_object):
        return hashlib.md5(cliente_object.clienteSenha.encode()).hexdigest()

    class Meta:
        model = Cliente
        fields = ["clienteId", "clienteNome", "clienteEmail", "clienteSenha", "clienteCelular", "clienteCPF",
         "clienteCEP", "clienteEndereco", "clienteCidadeId", "clienteEstadoId", "clienteLatitude", "clienteLongitude", "clienteIsVendedor"]

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'

class PagamentoSchemaSerializer(serializers.ModelSerializer):

    pagamentoId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Pagamento
        fields = ['pagamentoId', 'clienteId', 'pedidoId', 'pagamentoMetodo', 'pagamentoParcelas', 
                  'pagamentoValorTotal', 'pagamentoFinalCartao']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoSchemaSerializer(serializers.ModelSerializer):

    pedidoId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Pedido
        fields = ['pedidoId', 'produtoId', 'clienteId', 'vendedorId', 'pedidoQuantidadeProduto',
                  'pedidoStatus', 'pedidoDataCompra', 'pedidoDataPagamento', 'pedidoDataTransportadora', 'pedidoDataPrevista',
                  'pedidoDataEntregue']

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

class VendedorSchemaSerializer(serializers.ModelSerializer):

    vendedorId = serializers.UUIDField(write_only = True)

    class Meta:
        model = Vendedor
        fields = ["vendedorId", "vendedorNome", "vendedorEmail", "vendedorCelular", "vendedorCPF",
         "vendedorCEP", "vendedorEndereco", "vendedorCidadeId", "vendedorEstadoId", "vendedorLatitude", "vendedorLongitude"]
