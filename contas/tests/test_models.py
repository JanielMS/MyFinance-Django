from django.test import TestCase
from django.contrib.auth.models import User
from transacoes.models import Transacao
from contas.models import Conta

class ContaModelTest(TestCase):
    def setUp(self):
        """ Configuração inicial: cria um usuário e uma conta """
        self.usuario = User.objects.create_user(username="testuser", password="123456")
        self.conta = Conta.objects.create(
            usuario=self.usuario,
            nome="Carteira",
            saldo_inicial=100,
            saldo_atual=100
        )

    def test_criar_conta(self):
        """Testa se uma conta é criada corretamente"""
        self.assertEqual(self.conta.nome, "Banco")
        self.assertEqual(self.conta.saldo_atual, 1000)

    def test_atualizar_saldo(self):
        """Testa se o saldo da conta é atualizado corretamente"""
        self.conta.saldo_atual += 500  
        self.conta.save()
        self.conta.refresh_from_db()  
        self.assertEqual(self.conta.saldo_atual, 1500)

    def test_saldo_atualizado_apos_transacao(self):
        """ Testa se o saldo da conta é atualizado corretamente após uma transação """
        Transacao.objects.create(
            usuario=self.usuario,
            conta=self.conta,
            valor=50,
            tipo="D",  # Despesa
            descricao="Compra de comida"
        )
        
        self.conta.refresh_from_db()  
        self.assertEqual(self.conta.saldo_atual, 50) 


