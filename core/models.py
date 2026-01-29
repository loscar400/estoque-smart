from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    quantidade = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Movimento(models.Model):
    ENTRADA = 'E'
    SAIDA = 'S'

    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.tipo == self.ENTRADA:
            self.produto.quantidade += self.quantidade
        else:
            if self.produto.quantidade < self.quantidade:
                raise ValueError("Estoque insuficiente")
            self.produto.quantidade -= self.quantidade

        self.produto.save()
        super().save(*args, **kwargs)
