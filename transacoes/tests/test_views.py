from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from transacoes.models import Transacao
from contas.models import Conta
from datetime import datetime

class TransacaoViewTest(TestCase):
    def setUp(self):
        """Configuração inicial: cria um usuário, conta e transações"""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.client.login(username="testuser", password="123456")
        self.conta = Conta.objects.create(usuario=self.user, nome="Banco", saldo_atual=500)

        for i in range(30):  
            Transacao.objects.create(
                usuario=self.user,
                conta=self.conta,
                valor=10,
                tipo="R" if i % 2 == 0 else "D",  
                descricao=f"Transação {i}",
                data=datetime(2025, 1, 1)  # Todas no mesmo mês
            )
    
    def test_listar_transacoes(self):
        """Testa se a listagem de transações retorna status 200"""
        response = self.client.get(reverse("listar-transacoes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aluguel")

    def test_criar_transacao(self):
        """Testa a criação de uma nova transação via POST"""
        response = self.client.post(reverse("criar-transacao"), {
            "descricao": "Salário",
            "valor": 5000,
            "tipo": "R",  # Receita
            "data": "2025-02-04"
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertTrue(Transacao.objects.filter(descricao="Salário").exists())

    def test_editar_transacao(self):
        """Testa se conseguimos editar uma transação existente"""
        response = self.client.post(reverse("editar-transacao", args=[self.transacao.id]), {
            "descricao": "Aluguel de Fevereiro",
            "valor": 1200,
            "tipo": "D",
            "data": "2025-02-04"
        })
        self.assertEqual(response.status_code, 302)  
        self.transacao.refresh_from_db()
        self.assertEqual(self.transacao.descricao, "Aluguel de Fevereiro")
        self.assertEqual(self.transacao.valor, 1200)

    def test_excluir_transacao(self):
        """Testa se conseguimos excluir uma transação"""
        response = self.client.post(reverse("excluir-transacao", args=[self.transacao.id]))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(Transacao.objects.filter(id=self.transacao.id).exists())
   
    def test_listar_transacoes_com_filtro(self):
        """Testa se a filtragem por mês e ano retorna os resultados corretos"""
        response = self.client.get(reverse("listar-transacoes"), {"mes": 1, "ano": 2025})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Transação 0")  # Verifica se há transações

    def test_listar_transacoes_com_paginacao(self):
        """Testa se a paginação exibe apenas 20 transações por página"""
        response = self.client.get(reverse("listar-transacoes"), {"page": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("page_obj" in response.context)
        self.assertEqual(len(response.context["page_obj"]), 20)
                         
            