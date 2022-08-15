from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:receita_id>', receita, name='receita'),
    path('buscar', busca, name = 'buscar'),
    path('criar_receita', criarReceita, name='criar_receita'),
    path('deleta/<int:id>', deletarReceita, name='deleta_receita'),
    path('edita/<int:id>', editaReceita, name="edita_receita"),
    path('atualiza_receita', atualiza_receita, name='atualiza_receita'),
]