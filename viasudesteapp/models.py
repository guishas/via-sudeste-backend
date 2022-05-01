import datetime
from email.policy import default
import uuid
from django.db import models
import hashlib

# Helper functions
def upload_product_image(instance, filename):
    return f"{instance.produtoId}-{filename}"

# Create your models here.
class Estado(models.Model):
    estadoId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.nome)

class Cidade(models.Model):
    cidadeId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    estadoId = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.nome)

class Wishlist(models.Model):
    clienteId = models.CharField(max_length=200)
    produtoId = models.CharField(max_length=200)

    def __str__(self):
        return 'Cliente ID - {}'.format(self.clienteId)

class Media(models.Model):
    mediaId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    produtoId = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to = upload_product_image, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.produtoId)

class Review(models.Model):
    reviewId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    clienteId = models.CharField(max_length=200)
    pedidoId = models.CharField(max_length=200)
    produtoId = models.CharField(max_length=200)
    reviewTitulo = models.CharField(max_length=200)
    reviewComentario = models.TextField()
    reviewScore = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '{}'.format(self.reviewId)

class NotaFiscal(models.Model):
    nfeId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    pedidoId = models.CharField(max_length=200)
    produtoId = models.CharField(max_length=200)
    vendedorId = models.CharField(max_length=200)
    nfeQuantidade = models.IntegerField()
    nfePreco = models.FloatField()
    nfeFrete = models.FloatField()

    def __str__(self):
        return '{}'.format(self.nfeId)

class Pagamento(models.Model):
    pagamentoId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    clienteId = models.CharField(max_length=200)
    pedidoId = models.CharField(max_length=200)
    pagamentoMetodo = models.CharField(max_length=200)
    pagamentoParcelas = models.IntegerField(blank=True)
    pagamentoValorTotal = models.FloatField()
    pagamentoFinalCartao = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.pagamentoId)

class Pedido(models.Model):
    pedidoId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    produtoId = models.CharField(max_length=200)
    clienteId = models.CharField(max_length=200)
    vendedorId = models.CharField(max_length=200)
    pagamentoId = models.CharField(max_length=200)
    pedidoQuantidadeProduto = models.IntegerField()
    pedidoStatus = models.BooleanField()
    pedidoDataCompra = models.DateTimeField(auto_now_add = True)
    pedidoDataPagamento = models.DateTimeField(blank = True)
    pedidoDataTransportadora = models.DateTimeField(blank = True)
    pedidoDataPrevista = models.DateTimeField()
    pedidoDataEntregue = models.DateTimeField(blank = True)

    def __Str__(self):
        return '{}'.format(self.pedidoId)

class Produto(models.Model):
    produtoId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    produtoVendedorId = models.CharField(max_length=200)
    produtoCategoriaId = models.CharField(max_length=200)
    produtoNome = models.CharField(max_length=200)
    produtoDescricao = models.TextField()
    produtoPreco = models.FloatField()
    produtoQuantidade = models.IntegerField()
    produtoAvgScore = models.FloatField()
    produtoQuantidadeNotas = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.produtoId)

class Categoria(models.Model):
    categoriaId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    categoriaNome = models.CharField(max_length=200)

    def __str__(self):
        return '{} - {}'.format(self.categoriaId, self.categoriaNome)

class Vendedor(models.Model):
    vendedorId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    vendedorNome = models.CharField(max_length=200)
    vendedorEmail = models.EmailField()
    vendedorSenha = models.CharField(max_length=200)
    vendedorCelular = models.CharField(max_length=200)
    vendedorCPF = models.CharField(max_length=20)
    vendedorCEP = models.CharField(max_length=15)
    vendedorEndereco = models.CharField(max_length=200)
    vendedorCidadeId = models.CharField(max_length=200)
    vendedorEstadoId = models.CharField(max_length=200)
    vendedorLatitude = models.FloatField()
    vendedorLongitude = models.FloatField()
    vendedorIsVendedor = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        self.vendedorSenha = hashlib.md5(self.vendedorSenha.encode()).hexdigest()
        super(Vendedor, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.vendedorId)

class Cliente(models.Model):
    clienteId = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    clienteNome = models.CharField(max_length=200)
    clienteEmail = models.EmailField()
    clienteSenha = models.CharField(max_length=200)
    clienteCelular = models.CharField(max_length=200)
    clienteCPF = models.CharField(max_length=20)
    clienteCEP = models.CharField(max_length=15)
    clienteEndereco = models.CharField(max_length=200)
    clienteCidadeId = models.CharField(max_length=200)
    clienteEstadoId = models.CharField(max_length=200)
    clienteLatitude = models.FloatField()
    clienteLongitude = models.FloatField()
    clienteIsVendedor = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        self.clienteSenha = hashlib.md5(self.clienteSenha.encode()).hexdigest()
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.clienteId)