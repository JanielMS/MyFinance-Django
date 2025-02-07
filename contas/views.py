from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect,render
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ContaForm, Conta

# Create your views here.
class ListarContas(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        contas = Conta.objects.filter(usuario=request.user).order_by('nome')
        return render(request, 'contas/listar_contas.html', {'contas': contas})

class CriarConta(LoginRequiredMixin, CreateView):
    model = Conta
    form_class = ContaForm
    template_name = 'contas/criar_conta.html'
    success_url = reverse_lazy('listar-contas')

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user 
        self.object = form.save()
        
       
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': self.success_url})
        
        return redirect(self.success_url) 
    
class EditarConta(LoginRequiredMixin, UpdateView):
    model = Conta
    form_class = ContaForm
    template_name = 'contas/editar_conta.html'
    success_url = reverse_lazy('listar-contas')

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user 
        self.object = form.save()

        
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': self.success_url})
        
        return redirect(self.success_url) 
    
class ApagarConta(LoginRequiredMixin, DeleteView):
    model = Conta
    template_name = 'contas/apagar_conta.html'
    success_url = reverse_lazy('listar-contas')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'success': True, 'redirect_url': self.success_url})
        
        return redirect(self.success_url) 