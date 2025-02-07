from django.test import TestCase
from django.contrib.auth.models import User 
from categorias.forms import CategoriaForm
from categorias.models import Categoria

class CategoriaFormTest(TestCase):
    def setUp(self):
        """ Configuração inicial: cria uma categoria existente """
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.categoria = Categoria.objects.create(nome="Alimentação", tipo="D", usuario=self.user)

    def test_categoria_duplicada(self):
        """ Testa se o formulário não permite categorias com o mesmo nome """
        form_data = {"nome": "Alimentação", "tipo": "D"}
        form = CategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())  
        self.assertIn("nome", form.errors) 
    
    def test_categoria_campos_obrigatorios(self):
        """Testa se o formulário exige que todos os campos sejam preenchidos"""
        form = CategoriaForm(data={})
        self.assertFalse(form.is_valid())  
        self.assertIn("nome", form.errors)
