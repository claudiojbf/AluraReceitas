from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from receitas.models import Receita

# Create your views here.
def index(request):
    receitas = Receita.objects.filter(publicada=True).order_by('-data_receita')

    dados = {
        'receitas' : receitas
    }
    return render(request, 'receitas/index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita' : receita
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)

def criarReceita(request):
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
    receita = get_object_or_404(Receita, pk=id)
    receita.delete()
    return redirect('dashboard')

def editaReceita(request, id):
    receita = get_object_or_404(Receita, pk = id)
    receita_a_editar = {
        "receita": receita,
    }
    return render(request, 'receitas/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
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