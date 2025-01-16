from django import forms
from .models import Transacao

class TransacaoDespesaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['valor', 'categoria', 'data', 'descricao' ]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }