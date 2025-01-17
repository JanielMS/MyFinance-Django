from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Categoria
from .forms import CategoriaForm

class ListarCategorias(ListView):
    model = Categoria
    template_name = 'categorias/listar_categorias.html'
    context_object_name = 'categorias'
    ordering = 'nome'

class CriarCategoria(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/criar_categoria.html'
    success_url = reverse_lazy('listar-categorias')

class EditarCategoria(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/editar_categoria.html'
    success_url = reverse_lazy('listar-categorias')

class ApagarCategoria(DeleteView):
    model = Categoria
    template_name = 'categorias/apagar_categoria.html'
    success_url = reverse_lazy('listar-categorias')
