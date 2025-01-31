from django import forms
from .models import Conta


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['saldo_atual', 'nome', 'tipo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.tipo:
            self.fields['tipo'].initial = 'Carteira'
