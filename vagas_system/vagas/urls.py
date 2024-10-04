from django.urls import path
from . import views

urlpatterns = [
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),
    path('vagas/<int:vaga_id>/editar/', views.editar_vaga, name='editar_vaga'),
    path('vagas/<int:vaga_id>/deletar/', views.deletar_vaga, name='deletar_vaga'),
    path('vagas/<int:vaga_id>/candidatos/', views.listar_candidatos, name='listar_candidatos'),
    path('relatorios/vagas/', views.relatorio_vagas, name='relatorio_vagas'),
    path('vagas/', views.listar_vagas_disponiveis, name='listar_vagas_disponiveis'),
    path('vagas/<int:vaga_id>/candidatar/', views.candidatar_vaga, name='candidatar_vaga'),
    path('candidaturas/', views.listar_candidaturas, name='listar_candidaturas'),
]
