from django.test import TestCase
from contas.forms import ContaForm

class ContaFormTest(TestCase):
    def test_conta_campos_obrigatorios(self):
        """Testa se o formulário exige que todos os campos sejam preenchidos"""
        form = ContaForm(data={})
        self.assertFalse(form.is_valid())  
        self.assertIn("nome", form.errors)
        self.assertIn("saldo_atual", form.errors)

    def test_saldo_nao_pode_ser_negativo(self):
        """Testa se o formulário impede um saldo inicial negativo"""
        form_data = {"nome": "Investimentos", 'tipo': 'Carteira', "saldo_atual": -100}
        form = ContaForm(data=form_data)
        self.assertFalse(form.is_valid())  
        self.assertIn("saldo_atual", form.errors)
