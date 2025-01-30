from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    TIPOS_CATEGORIAS = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=1, choices=TIPOS_CATEGORIAS, default='D')
    categoria_pai = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')

    def __str__(self):
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} > {self.nome}"
        return self.nome

    # SQL para Categoria
    # Criação:
    # INSERT INTO financas_categoria (nome, descricao, categoria_pai_id) VALUES ('Alimentação', 'Despesas com comida', NULL);
    # INSERT INTO financas_categoria (nome, descricao, categoria_pai_id) VALUES ('Supermercado', '', 1);

    # Leitura:
    # SELECT * FROM financas_categoria WHERE nome = 'Alimentação';
    # SELECT * FROM financas_categoria WHERE categoria_pai_id IS NULL; -- Listar categorias principais

    # Atualização:
    # UPDATE financas_categoria SET descricao = 'Despesas gerais com alimentos' WHERE nome = 'Alimentação';

    # Exclusão:
    # DELETE FROM financas_categoria WHERE nome = 'Supermercado';

