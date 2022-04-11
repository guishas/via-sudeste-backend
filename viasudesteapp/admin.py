from django.contrib import admin

from viasudesteapp.models import Categoria, Cliente, Estado, Cidade, Media, NotaFiscal, Pagamento, Pedido, Produto, Review, Vendedor, Wishlist

# Register your models here.
class EstadoAdmin(admin.ModelAdmin):
    readonly_fields = ['estadoId']

class DateAdmin(admin.ModelAdmin):
    readonly_fields = ['createdAt']

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade)
admin.site.register(Media)
admin.site.register(Wishlist)
admin.site.register(Review, DateAdmin)
admin.site.register(NotaFiscal)
admin.site.register(Pagamento)
admin.site.register(Pedido)
admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Vendedor)
admin.site.register(Cliente)