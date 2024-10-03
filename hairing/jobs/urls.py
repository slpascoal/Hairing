from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('vagas/', views.lista_vagas, name='lista_vagas'),
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),
    path('vagas/<int:vaga_id>/', views.detalhes_vaga, name='detalhes_vaga'),
    path('vagas/<int:vaga_id>/candidatar/', views.candidatar, name='candidatar'),
]