from django.urls import path
from . import views

urlpatterns = [
    path('api/estados/<str:estado_id>', views.get_estado_by_id),
    path('api/estados/', views.get_estados),
    path('api/cidades/<str:cidade_id>', views.get_cidade_by_id),
    path('api/cidades/', views.get_cidades),
    path('api/cidades/estado/<str:estado_id>', views.get_cidades_by_estado_id),
    path('api/cidades/adicionar/<str:estado_id>/<str:cidades>', views.add_cidades_in_estado),
    path('api/wishlist/<str:user_id>', views.get_user_wishlist),
    path('api/wishlist/', views.get_wishlist),
    path('api/medias/', views.get_medias),
    path('api/medias/<str:product_id>', views.get_medias_by_product_id),
    path('api/reviews/', views.get_reviews),
    path('api/reviews/<str:product_id>', views.get_reviews_by_product_id),
    path('api/notasfiscais/', views.get_notas_ficais),
    path('api/notasfiscais/<str:pedido_id>', views.get_nota_fiscal_by_pedido_id),
    path('api/clientes/', views.get_clientes),
    path('api/clientes/<str:user_id>', views.get_cliente_by_id),
    path('api/clientes/email/<str:email>', views.get_cliente_by_email),
]