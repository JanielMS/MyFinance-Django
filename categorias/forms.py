from django import forms
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['tipo', 'nome']
    
class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['categoria_pai','nome']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.categoria_pai:
            # Desativa o campo para edição no HTML, mas ainda permite que o valor seja enviado
            self.fields['categoria_pai'].widget.attrs['disabled'] = True
            self.fields['categoria_pai'].widget.attrs['style'] = 'background-color: #f0f0f0;'
