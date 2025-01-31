from django.urls import path
from .views import *

urlpatterns = [
    path('', ListarContas.as_view(), name='listar-contas'),
    path('criar', CriarConta.as_view(), name='criar-conta'),
    path('editar/<int:pk>', EditarConta.as_view(), name='editar-conta'),
    path('apagar/<int:pk>', ApagarConta.as_view(), name='apagar-conta'),
]