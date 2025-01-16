# from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from .models import Transacao
from .forms import TransacaoDespesaForm

class AdicionarDespesa(CreateView):
    model = Transacao
    form_class = TransacaoDespesaForm
    template_name = 'transacoes/adicionar_despesa.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        # Tenta obter a URL anterior a partir do cabeçalho HTTP Referer
        referer = self.request.META.get('HTTP_REFERER')
        return referer if referer else self.success_url
    
    def form_valid(self, form):
        tipo_despesa = Transacao.objects.get(tipo='D')
        form.instance.tipo = tipo_despesa
        return super().form_valid(form)
