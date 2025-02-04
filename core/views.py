from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime

from transacoes.models import Transacao
from contas.models import Conta


class Home(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        mes = request.GET.get('mes', datetime.now().month)
        ano = int(request.GET.get('ano', datetime.now().year))

        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
            7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        anos = range(datetime.now().year - 5, datetime.now().year + 1)


        transacoes_filtradas = Transacao.objects.filter(usuario=request.user, data__month=mes, data__year=ano)

        saldo_total = Conta.objects.filter(usuario=request.user).aggregate(Sum('saldo_atual'))['saldo_atual__sum'] or 0


        total_receitas = transacoes_filtradas.filter(tipo='R').aggregate(Sum('valor'))['valor__sum'] or 0
        total_despesas = transacoes_filtradas.filter(tipo='D').aggregate(Sum('valor'))['valor__sum'] or 0

        return render(request, 'home.html', {
            'saldo_total': saldo_total,
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'meses': meses,
            'mes': int(mes),
            'anos': anos,
            'ano': ano
        })