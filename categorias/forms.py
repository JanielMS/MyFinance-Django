from django import forms
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        categoria_atual = self.instance  # A categoria que está sendo editada
        
        # Verificar se já existe uma categoria com o mesmo nome, mas ignorar a categoria atual
        if Categoria.objects.filter(nome=nome).exclude(pk=categoria_atual.pk).exists():
            raise forms.ValidationError(f"Categoria com o nome '{nome}' já existe.")
        
        return nome
    
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

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        
        # Verifica se já existe uma categoria com o mesmo nome
        if Categoria.objects.filter(nome=nome).exists():
            raise forms.ValidationError("Já existe uma categoria com esse nome.")
        
        return nome