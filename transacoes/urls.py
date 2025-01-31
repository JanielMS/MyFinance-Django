from django.urls import path
from .views import *

urlpatterns = [
    path('', ListarTransacoes.as_view(), name='listar-transacoes'),
    path('despesa/adicionar', AdicionarDespesa.as_view(), name='adicionar-despesa'),
    path('despesa/editar/<int:pk>', EditarDespesa.as_view(), name='editar-despesa'),
    path('apagar/<int:pk>', ApagarTransacao.as_view(), name='apagar-transacao'),
]