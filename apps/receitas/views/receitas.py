from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from receitas.models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    """Redireciona o usuario para pagina de index com as informações da receita"""
    receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')
    paginator = Paginator(receitas, 6)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)
    dados = {
        'receitas' : receitas_por_pagina
    }
    return render(request, 'receitas/index.html', dados)

def receita(request, receita_id):
    """Demostra a pagina com a receita especifica e suas informações"""
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita' : receita
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)

def criarReceita(request):
    """Cria uma receita """
    if request.user.is_authenticated:
        if request.method == 'POST':
            nome_receita = request.POST['nome_receita']
            ingredientes = request.POST['ingredientes']
            modo_preparo = request.POST['modo_preparo']
            tempo_preparo = request.POST['tempo_preparo']
            rendimento = request.POST['rendimento']
            categoria = request.POST['categoria']
            foto_receita = request.FILES['foto_receita']
            user = get_object_or_404(User, pk = request.user.id)
            receita = Receita.objects.create(
            pessoa = user, 
            nome_receita = nome_receita, 
            ingredientes = ingredientes, 
            modo_de_preparo = modo_preparo, 
            rendimento= rendimento, 
            categoria = categoria, 
            foto_receita = foto_receita,
            tempo_de_preparo = tempo_preparo
            )
            receita.save()
            return redirect('dashboard')
        else:
            return render(request, 'receitas/criar_receita.html')
    else:
        return redirect('index')

def deletarReceita(request, id):
    """Deleta uma receita"""
    receita = get_object_or_404(Receita, pk=id)
    receita.delete()
    return redirect('dashboard')

def editaReceita(request, id):
    """Edita uma receita"""
    receita = get_object_or_404(Receita, pk = id)
    receita_a_editar = {
        "receita": receita,
    }
    return render(request, 'receitas/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
    """Atualiza as informações de uma receita"""
    if request.method == 'POST':
        receita_id =  request.POST.get('receita_id')
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_de_preparo = request.POST['modo_preparo']
        r.tempo_de_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')