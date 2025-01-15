from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import date

# TEMA ESCOLHIDO: Gerenciamento de Finanças Pessoais

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
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


class Transacao(models.Model):
    TIPOS_TRANSACAO = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=1, choices=TIPOS_TRANSACAO)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    data = models.DateField()
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.valor:.2f}"

    class Meta:
        ordering = ['-data']

    # SQL para Transacao
    # Criação:
    # INSERT INTO financas_transacao (usuario_id, categoria_id, tipo, valor, data, descricao, criado_em)
    # VALUES (1, 2, 'D', 250.00, '2025-01-05', 'Compras no mercado', NOW());

    # Leitura:
    # SELECT * FROM financas_transacao WHERE tipo = 'D' AND data BETWEEN '2025-01-01' AND '2025-01-31';
    # SELECT * FROM financas_transacao WHERE usuario_id = 1 AND categoria_id = 2;

    # Atualização:
    # UPDATE financas_transacao SET valor = 260.00 WHERE id = 1;

    # Exclusão:
    # DELETE FROM financas_transacao WHERE id = 1;


class ResumoFinanceiro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    total_receitas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_despesas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_final = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Resumo {self.data_inicio} a {self.data_fim} - Saldo: {self.saldo_final:.2f}"

    def atualizar_resumo(self):
        """Atualiza os valores de receitas, despesas e saldo final com base nas transações do período."""
        receitas = Transacao.objects.filter(
            usuario=self.usuario, tipo='R', data__range=[self.data_inicio, self.data_fim]
        ).aggregate(total=models.Sum('valor'))['total'] or 0

        despesas = Transacao.objects.filter(
            usuario=self.usuario, tipo='D', data__range=[self.data_inicio, self.data_fim]
        ).aggregate(total=models.Sum('valor'))['total'] or 0

        self.total_receitas = receitas
        self.total_despesas = despesas
        self.saldo_final = receitas - despesas
        self.save()

    class Meta:
        ordering = ['data_inicio']

    # SQL para ResumoFinanceiro
    # Criação:
    # INSERT INTO financas_resumofinanceiro (usuario_id, data_inicio, data_fim, total_receitas, total_despesas, saldo_final)
    # VALUES (1, '2025-01-01', '2025-01-31', 500.00, 330.00, 170.00);

    # Leitura:
    # SELECT * FROM financas_resumofinanceiro WHERE usuario_id = 1 AND data_inicio = '2025-01-01';

    # Atualização:
    # UPDATE financas_resumofinanceiro SET saldo_final = 180.00 WHERE id = 1;

    # Exclusão:
    # DELETE FROM financas_resumofinanceiro WHERE id = 1;
