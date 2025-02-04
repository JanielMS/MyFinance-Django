from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from contas.models import Conta

class ContaViewTest(TestCase):
    def setUp(self):
        """Configuração inicial: cria um usuário autenticado"""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.client.login(username="testuser", password="123456")
        self.conta = Conta.objects.create(usuario=self.user, nome="Banco", saldo_atual=500)

    def test_listar_contas(self):
        """Testa se a página de listagem de contas retorna status 200"""
        response = self.client.get(reverse("listar-contas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Banco")  # Verifica se a conta aparece na página

    def test_criar_conta(self):
        """Testa a criação de uma nova conta via POST"""
        response = self.client.post(reverse("criar-conta"), {"nome": "Carteira", "saldo_atual": 200})
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertTrue(Conta.objects.filter(nome="Carteira").exists())

    def test_editar_conta(self):
        """Testa se uma conta pode ser editada"""
        response = self.client.post(reverse("editar-conta", args=[self.conta.id]), {"nome": "Conta Corrente", "saldo_atual": 700})
        self.assertEqual(response.status_code, 302)  
        self.conta.refresh_from_db()
        self.assertEqual(self.conta.nome, "Conta Corrente")  
        self.assertEqual(self.conta.saldo_atual, 700)

    def test_excluir_conta(self):
        """Testa se uma conta pode ser excluída"""
        response = self.client.post(reverse("excluir-conta", args=[self.conta.id]))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(Conta.objects.filter(nome="Banco").exists())  
