from django.shortcuts import render, redirect
from .models import Produto, Movimento
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Sum
from .forms import ProdutoForm
from .forms import MovimentoForm
from datetime import datetime


@login_required
@permission_required('core.view_produto', raise_exception=True)
def produto_list(request):
    busca = request.GET.get('q')

    produtos = Produto.objects.all()

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    return render(
        request,
        'core/produto_list.html',
        {
            'produtos': produtos,
            'busca': busca
        }
    )


@login_required
@permission_required('core.add_produto', raise_exception=True)
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produto_list')
    else:
        form = ProdutoForm()

    return render(request, 'core/produto_form.html', {'form': form})


@login_required
@permission_required('core.view_movimento', raise_exception=True)
def movimento_list(request):
    movimentos = Movimento.objects.select_related('produto').order_by('-data')

    produto_id = request.GET.get('produto')
    tipo = request.GET.get('tipo')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if produto_id:
        movimentos = movimentos.filter(produto_id=produto_id)

    if tipo:
        movimentos = movimentos.filter(tipo=tipo)

    if data_inicio:
        movimentos = movimentos.filter(data__date__gte=data_inicio)

    if data_fim:
        movimentos = movimentos.filter(data__date__lte=data_fim)

    produtos = Produto.objects.all()

    context = {
        'movimentos': movimentos,
        'produtos': produtos,
        'filtros': {
            'produto': produto_id,
            'tipo': tipo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
        }
    }

    return render(request, 'core/movimento_list.html', context)


@login_required
@permission_required('core.add_movimento', raise_exception=True)
def movimento_create(request):
    if request.method == 'POST':
        form = MovimentoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('movimento_list')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = MovimentoForm()

    return render(request, 'core/movimento_form.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('produto_list')
        else:
            return render(request, 'core/login.html', {'erro': 'Usuário ou senha inválidos'})

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    total_produtos = Produto.objects.count()
    total_estoque = Produto.objects.aggregate(
        total=Sum('quantidade')
    )['total'] or 0

    total_movimentos = Movimento.objects.count()
    ultimos_movimentos = Movimento.objects.select_related('produto').order_by('-data')[:5]

    context = {
        'total_produtos': total_produtos,
        'total_estoque': total_estoque,
        'total_movimentos': total_movimentos,
        'ultimos_movimentos': ultimos_movimentos,
    }

    return render(request, 'core/dashboard.html', context)
