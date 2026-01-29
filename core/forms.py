from django import forms
from .models import Produto, Movimento


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao']

class MovimentoForm(forms.ModelForm):
    class Meta:
        model = Movimento
        fields = ['produto', 'tipo', 'quantidade']
