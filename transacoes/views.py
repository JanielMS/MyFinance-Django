from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Transacao
from .forms import TransacaoDespesaForm, TransacaoReceitaForm
from datetime import datetime



class ListarTransacoes(View):
    def get(self, request, *args, **kwargs):
        mes = int(request.GET.get('mes', datetime.now().month))
        ano = int(request.GET.get('ano', datetime.now().year))

        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        anos = range(datetime.now().year - 5, datetime.now().year + 1)

        tipo_transacao = request.GET.get('tipo_categoria', None) 

        transacoes = Transacao.objects.filter(usuario=request.user, data__month=mes, data__year=ano)
           
        if tipo_transacao:
            transacoes = transacoes.filter(tipo=tipo_transacao)
            
        
        transacoes = transacoes.order_by('-data')

        
        paginator = Paginator(transacoes, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        transacoes_por_data = {}
        for transacao in page_obj:
            data = transacao.data
            if data not in transacoes_por_data:
                transacoes_por_data[data] = []
            transacoes_por_data[data].append(transacao)

        context = {
            'transacoes_por_data': transacoes_por_data, 
            'tipo_transacao': tipo_transacao,
            'page_obj': page_obj, 
            'page_number': page_number,
            'meses': meses,
            'anos': anos,
            'mes': mes,
            'ano': ano,
        }
       
        return render(request, "transacoes/listar_transacoes.html", context)
    
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
    template_name = "transacoes/apagar_transacao.html"
    success_url = reverse_lazy('listar-transacoes')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        success_url = self.request.META.get('HTTP_REFERER', reverse('listar-transacoes')) 
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'success': True, 'redirect_url': success_url})
        
        return redirect(success_url)
    
class AdicionarReceita(LoginRequiredMixin, CreateView):
    model = Transacao
    form_class = TransacaoReceitaForm
    template_name = 'transacoes/adicionar_receita.html'
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

class EditarReceita(LoginRequiredMixin, UpdateView):
    model = Transacao
    form_class = TransacaoReceitaForm
    template_name = 'transacoes/editar_receita.html'
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