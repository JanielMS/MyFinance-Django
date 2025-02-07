from django.test import TestCase
from django.contrib.auth.models import User
from categorias.models import Categoria

class CategoriaModelTest(TestCase):
    def setUp(self):
        """Cria um usuário e uma categoria inicial"""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.categoria_pai = Categoria.objects.create(nome="Transporte", tipo="D", usuario=self.user)

    def test_criar_subcategoria(self):
        """Testa se uma subcategoria pode ser criada corretamente"""
        subcategoria = Categoria.objects.create(nome="Uber", categoria_pai=self.categoria_pai, tipo="D", usuario=self.user)
        self.assertEqual(subcategoria.categoria_pai, self.categoria_pai)  # Confirma a relação

    def test_nao_permitir_categoria_duplicada(self):
        """Testa se a criação de uma categoria duplicada é impedida"""
        with self.assertRaises(Exception):  
            Categoria.objects.create(nome="Transporte", tipo="D", usuario=self.user)  # Deve falhar
