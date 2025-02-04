from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from categorias.models import Categoria

class CategoriaViewTest(TestCase):
    def setUp(self):
        """Configuração inicial: cria um usuário autenticado"""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.client.login(username="testuser", password="123456")
        self.categoria = Categoria.objects.create(nome="Lazer", tipo="D")

    def test_listar_categorias(self):
        """Testa se a página de listagem de categorias retorna status 200"""
        response = self.client.get(reverse("listar-categorias"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lazer")  # Confirma que a categoria aparece na página

    def test_criar_categoria(self):
        """Testa a criação de uma nova categoria via POST"""
        response = self.client.post(reverse("criar-categoria"), {"nome": "Saúde", "tipo": "D"})
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso
        self.assertTrue(Categoria.objects.filter(nome="Saúde").exists())

    def test_editar_categoria(self):
        """Testa se uma categoria pode ser editada"""
        response = self.client.post(reverse("editar-categoria", args=[self.categoria.id]), {"nome": "Entretenimento"})
        self.assertEqual(response.status_code, 302)  
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nome, "Entretenimento")  

    def test_excluir_categoria(self):
        """Testa se uma categoria pode ser excluída"""
        response = self.client.post(reverse("excluir-categoria", args=[self.categoria.id]))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(Categoria.objects.filter(nome="Lazer").exists())  
