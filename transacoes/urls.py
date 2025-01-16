from django.urls import path
from .views import *

urlpatterns = [
    path('despesa/adicionar', AdicionarDespesa.as_view(), name='adicionar-despesa')
]