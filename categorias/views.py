from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, DeleteView
from .models import Categoria
from .forms import CategoriaForm, SubcategoriaForm

def listar_categorias(categorias, nivel=1):
    lista = []
    for categoria in categorias:
        lista.append((categoria, nivel))
        # print(f'Categoria_Raiz: {categoria}')
        subcategorias = Categoria.objects.filter(categoria_pai=categoria)
        if subcategorias.exists():
            lista.extend(listar_categorias(subcategorias, nivel + 1))
    return lista

class ListarCategorias(View):
    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.filter(categoria_pai__isnull=True)
        categorias_hierarquicas = listar_categorias(categorias)
        return render(request, 'categorias/listar_categorias.html', {'categorias': categorias_hierarquicas})


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


class CriarSubcategoria(CreateView):
    model = Categoria
    form_class = SubcategoriaForm
    template_name = 'categorias/criar_subcategoria.html'
    success_url = reverse_lazy('listar-categorias')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria_pai_id = self.kwargs.get('pk')
        categoria_pai = Categoria.objects.get(pk=categoria_pai_id)
        context['categoria'] = categoria_pai
        context['form'].fields['categoria_pai'].initial = categoria_pai
        return context
