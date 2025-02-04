from django.test import TestCase
from transacoes.forms import TransacaoForm

class TransacaoFormTest(TestCase):
    def test_campos_obrigatorios(self):
        """Testa se o formulário exige que todos os campos sejam preenchidos"""
        form = TransacaoForm(data={})
        self.assertFalse(form.is_valid())  
        self.assertIn("descricao", form.errors)
        self.assertIn("valor", form.errors)
        self.assertIn("tipo", form.errors)

    def test_valor_negativo_para_receitas(self):
        """Testa se o formulário impede valores negativos para receitas"""
        form_data = {"descricao": "Salário", "valor": -1000, "tipo": "R", "data": "2024-02-10"}
        form = TransacaoForm(data=form_data)
        self.assertFalse(form.is_valid())  
        self.assertIn("valor", form.errors)
