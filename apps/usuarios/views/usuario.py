from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    """Cadastra uma nova pessoa no sistema """
    if request.method =='POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'Nome Invalido')
            return redirect('cadastro')
        if User.objects.filter(username = nome).exists():
            messages.error(request, 'Nome de usuario já existe')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'Email invalido')
            return redirect('cadastro')
        if senhas_nao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email = email).exists():
            messages.error(request, 'Email invalido')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('login')
    return render(request, 'usuarios/cadastro.html')

def login(request):
    """Realiza o Login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email == "" or senha == "":
            return redirect('login')
        if User.objects.filter(email = email).exists():
            nome = User.objects.filter(email = email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username = nome, password = senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')    
    return render(request, 'usuarios/login.html')

def logout(request):
    """Desconecta uma pessoa do sistema"""
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """Direciona uma pessoa para o dashbord enviando as informações nescessarias"""
    if request.user.is_authenticated:
        user = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa = user)
        return render(request, 'usuarios/dashboard.html',{'receitas':receitas})
    else:
        return redirect('index')

def campo_vazio(campo):
    return not campo.strip()

def senhas_nao_iguais(senha, senha2):
    return senha != senha2