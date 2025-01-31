from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transacao
from .forms import TransacaoDespesaForm
import locale
from django.utils.timezone import localdate


class ListarTransacoes(View):
    def get(self, request, *args, **kwargs):

        tipo_transacao = request.GET.get('tipo_categoria', None) 
        transacoes = Transacao.objects.filter(usuario=request.user, tipo=tipo_transacao)
        
        if tipo_transacao:
            transacoes = Transacao.objects.filter(usuario=request.user, tipo=tipo_transacao)
        else:
            transacoes = Transacao.objects.filter(usuario=request.user)  # Sem filtro de tipo

         # Agrupar transações por data em Python
        transacoes_por_data = {}
        for transacao in transacoes:
            data = transacao.data  # Data formatada
            if data not in transacoes_por_data:
                transacoes_por_data[data] = []
            transacoes_por_data[data].append(transacao)
       
        return render(request, "transacoes/listar_transacoes.html", {'transacoes_por_data': transacoes_por_data, 'tipo_transacao': tipo_transacao})
    
class AdicionarDespesa(LoginRequiredMixin, CreateView):
    model = Transacao
    form_class = TransacaoDespesaForm
    template_name = 'transacoes/adicionar_despesa.html'
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user 
        self.object = form.save()
        
        success_url = self.request.META.get('HTTP_REFERER', reverse('listar-transacoes')) 
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)

class EditarDespesa(LoginRequiredMixin, UpdateView):
    model = Transacao
    form_class = TransacaoDespesaForm
    template_name = 'transacoes/editar_despesa.html'
    success_url = reverse_lazy('home')
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user 
        self.object = form.save()
        
        success_url = self.request.META.get('HTTP_REFERER', reverse('listar-transacoes')) 
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)


class ApagarTransacao(LoginRequiredMixin, DeleteView):
    model = Transacao
    template_name = "transacoes/apagar_despesa.html"
    success_url = reverse_lazy('listar-transacoes')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        success_url = self.request.META.get('HTTP_REFERER', reverse('listar-transacoes')) 
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)