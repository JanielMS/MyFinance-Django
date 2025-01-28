# categorias/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', ListarCategorias.as_view(), name='listar-categorias'),
    path('criar', CriarCategoria.as_view(), name='criar-categoria'),
    path('editar/<int:pk>', EditarCategoria.as_view(), name='editar-categoria'),
    path('apagar/<int:pk>', ApagarCategoria.as_view(), name='apagar-categoria'),

    # SubCategorias 
    path('<int:pk>/criar-subcategoria', CriarSubcategoria.as_view(), name='criar-subcategoria'),
    path('<int:pk>/editar-subcategoria', EditarSubCategoria.as_view(), name='editar-subcategoria'),
]