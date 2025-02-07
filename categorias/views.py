from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
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
        tipo_categoria = request.GET.get('tipo_categoria', 'D') 
        categorias = Categoria.objects.filter(usuario=request.user, categoria_pai__isnull=True, tipo=tipo_categoria)
        categorias_hierarquicas = listar_categorias(categorias)
        return render(request, 'categorias/listar_categorias.html', {'categorias': categorias_hierarquicas, 'tipo_categoria': tipo_categoria})


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
        form.instance.usuario = self.request.user 
        self.object = form.save()
         
        tipo_categoria = self.object.tipo 
        

        success_url = reverse('listar-categorias') + f'?tipo_categoria={tipo_categoria}'
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)  

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
        form.instance.usuario = self.request.user 
        self.object = form.save()
         
        tipo_categoria = self.object.tipo  # 'D' para Despesa, 'R' para Receita
        
        
        success_url = reverse('listar-categorias') + f'?tipo_categoria={tipo_categoria}'
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)  
       

class ApagarCategoria(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categorias/apagar_categoria.html'
    success_url = reverse_lazy('listar-categorias')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        tipo_categoria = self.object.tipo  # 'D' para Despesa, 'R' para Receita
        
       
        success_url = reverse('listar-categorias') + f'?tipo_categoria={tipo_categoria}'
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url) 

class CriarSubcategoria(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = SubcategoriaForm
    template_name = 'categorias/criar_subcategoria.html'
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
        form.instance.usuario = self.request.user 
        self.object = form.save()
        
        print(self.object)
        tipo_categoria = self.object.categoria_pai.tipo  # 'D' para Despesa, 'R' para Receita
        
        
        success_url = reverse('listar-categorias') + f'?tipo_categoria={tipo_categoria}'
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)  


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
        form.instance.usuario = self.request.user 
        
        tipo_categoria = self.object.tipo  # 'D' para Despesa, 'R' para Receita
        
        
        success_url = reverse('listar-categorias') + f'?tipo_categoria={tipo_categoria}'
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)  
