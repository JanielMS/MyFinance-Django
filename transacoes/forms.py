from django import forms
from .models import Transacao

class TransacaoDespesaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['valor', 'categoria', 'data', 'descricao', 'tipo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }
    
    # Define o valor padrão para o campo tipo como 'D' (Despesa)
    def __init__(self, *args, **kwargs):
        super(TransacaoDespesaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].initial = 'D'
        self.fields['tipo'].widget.attrs['style'] = 'display:none;'
        if 'tipo' in self.fields:
            self.fields['tipo'].label = ''  # Remove a label
            self.fields['tipo'].widget.attrs['aria-label'] = 'Despesas'

        if self.instance and self.instance.pk:
            if self.instance.data:
                self.fields['data'].initial = self.instance.data.strftime('%Y-%m-%d')  