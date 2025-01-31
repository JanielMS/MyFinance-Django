from django import forms
from .models import Transacao, Categoria

class TransacaoDespesaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['valor', 'conta', 'categoria', 'data', 'descricao', 'tipo']
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

        self.fields['conta'].initial = 'Carteira'
        
        if self.instance and self.instance.pk:  
            if self.instance.tipo == 'D':  
                self.fields['categoria'].queryset = Categoria.objects.filter(tipo='D')
        else:
            self.fields['categoria'].queryset = Categoria.objects.filter(tipo='D')

class TransacaoReceitaForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['valor', 'conta', 'categoria', 'data', 'descricao', 'tipo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }
    
    # Define o valor padrão para o campo tipo como 'R' (Receita)
    def __init__(self, *args, **kwargs):
        super(TransacaoReceitaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].initial = 'R'
        self.fields['tipo'].widget.attrs['style'] = 'display:none;'
        if 'tipo' in self.fields:
            self.fields['tipo'].label = ''  # Remove a label
            self.fields['tipo'].widget.attrs['aria-label'] = 'Receita'
    
        self.fields['conta'].initial = 'Carteira'
        
        if self.instance and self.instance.pk:  
            if self.instance.tipo == 'R':  
                self.fields['categoria'].queryset = Categoria.objects.filter(tipo='R')
        
        else:
            self.fields['categoria'].queryset = Categoria.objects.filter(tipo='R')