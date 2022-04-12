from rest_framework import serializers
from .models import Categoria, Cidade, Cliente, Estado, Media, NotaFiscal, Pagamento, Pedido, Produto, Review, Vendedor, Wishlist


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['estadoId', 'nome']

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['cidadeId', 'estadoId', 'nome']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['clienteId', 'produtoId']

class ProdutoSerializer(serializers.ModelSerializer):

    produtoCategoria = serializers.SerializerMethodField('get_categoria')

    def get_categoria(self, produto_object):
        categoria = Categoria.objects.get(categoriaId = produto_object.produtoCategoriaId)
        serialized_categoria = CategoriaSerializer(categoria)
        return serialized_categoria.data

    class Meta:
        model = Produto
        fields = ['produtoId', 'produtoCategoria', 'produtoNome', 'produtoDescricao',
         'produtoPreco', 'produtoQuantidade', 'produtoAvgScore', 'produtoQuantidadeNotas']

class ProdutoSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class NotaFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaFiscal
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

