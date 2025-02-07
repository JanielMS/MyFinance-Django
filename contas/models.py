from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Conta(models.Model):
    TIPO_CONTA = [
        ('Carteira', 'Carteira'),
        ('Poupança', 'Poupança'),
        ('Conta Corrente', 'Conta Corrente'),
        ('Investimentos', 'Investimentos'),
        ('VR/VA', 'VR/VA'),
        ('Outro', 'Outro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, unique=True) 
    saldo_atual = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tipo = models.CharField(max_length=15, choices=TIPO_CONTA)

    
    def calcular_saldo(self):
        receitas = self.transacoes.filter(tipo='R').aggregate(models.Sum('valor'))['valor__sum'] or 0
        despesas = self.transacoes.filter(tipo='D').aggregate(models.Sum('valor'))['valor__sum'] or 0
        return self.saldo_atual + (receitas - despesas)

    def atualizar_saldo(self):
        """ Atualiza o saldo com base nas transações associadas. """
        self.saldo_atual = self.calcular_saldo()
        self.save()

    def __str__(self):
        return f"{self.nome}"
