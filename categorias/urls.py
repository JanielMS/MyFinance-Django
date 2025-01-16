from django.urls import path
from .views import *

urlpatterns = [
    path('', ListarCategorias.as_view(), name='listar-categorias'),
    path('categorias/criar', CriarCategoria.as_view(), name='criar-categoria')
]