from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Categoria
from .forms import CategoriaForm, SubcategoriaForm

def listar_categorias(categorias, nivel=1):
    lista = []
    for categoria in categorias:
        lista.append((categoria, nivel))
        subcategorias = Categoria.objects.filter(categoria_pai=categoria)
        if subcategorias.exists():
            lista.extend(listar_categorias(subcategorias, nivel + 1))
    return lista

class ListarCategorias(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.filter(usuario=request.user, categoria_pai__isnull=True)
        categorias_hierarquicas = listar_categorias(categorias)
        return render(request, 'categorias/listar_categorias.html', {'categorias': categorias_hierarquicas})


class CriarCategoria(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/criar_categoria.html'
    success_url = reverse_lazy('listar-categorias')

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True})
        form.instance.usuario = self.request.user 
        return super().form_valid(form)

class EditarCategoria(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/editar_categoria.html'
    success_url = reverse_lazy('listar-categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'categoria' not in context:
            context['categoria'] = self.object  # Garante que a categoria está no contexto
        return context

    def form_invalid(self, form):
        print(form.errors) 
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {'form': form, 'categoria': self.object}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
        
    def form_valid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True})
        form.instance.usuario = self.request.user 
        return super().form_valid(form)

class ApagarCategoria(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categorias/apagar_categoria.html'
    success_url = reverse_lazy('listar-categorias')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        return super().post(request, *args, **kwargs)

class CriarSubcategoria(LoginRequiredMixin, CreateView):
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
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True})
        form.instance.usuario = self.request.user 
        return super().form_valid(form)


class EditarSubCategoria(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = SubcategoriaForm
    template_name = 'categorias/editar_subcategoria.html'
    success_url = 'listar-categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria_pai_id = self.kwargs.get('pk')
        categoria_pai = Categoria.objects.get(pk=categoria_pai_id)
        context['categoria'] = categoria_pai
        context['form'].fields['categoria_pai'].initial = categoria_pai
        return context
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {'form': form, 'categoria': self.object}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True})
        form.instance.usuario = self.request.user 
        return super().form_valid(form)