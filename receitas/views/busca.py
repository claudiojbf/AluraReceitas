from django.shortcuts import render
from receitas.models import Receita

def busca(request):
    lista_receita = Receita.objects.filter(publicada = True).order_by('-data_receita')

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_receita = lista_receita.filter(nome_receita__icontains = nome_a_buscar)
    
    dados = {
        'receitas' : lista_receita
    }

    return render(request, 'receitas/buscar.html', dados)