from rest_framework import serializers
from .models import Categoria, Cidade, Cliente, Estado, Media, NotaFiscal, Produto, Review, Wishlist


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