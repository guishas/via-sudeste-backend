from django.urls import path
from . import views

urlpatterns = [
    path('api/estados/<str:estado_id>', views.get_estado_by_id),
    path('api/estados/', views.get_estados),
    path('api/cidades/<str:cidade_id>', views.get_cidade_by_id),
    path('api/cidades/', views.get_cidades),
    path('api/cidades/estado/<str:estado_id>', views.get_cidades_by_estado_id),
    path('api/cidades/adicionar/<str:estado_id>/<str:cidades>', views.add_cidades_in_estado)
]