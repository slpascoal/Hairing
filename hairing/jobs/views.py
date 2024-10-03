# jobs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Vaga, Candidato
from .forms import CustomUserCreationForm
# jobs/views.py (adicionando nova view para o relatório)
from django.db.models import Count
from django.http import JsonResponse
import json

def relatorio_vagas(request):
    vagas_por_mes = Vaga.objects.annotate(mes=models.functions.ExtractMonth('created_at')).values('mes').annotate(total=Count('id')).order_by('mes')
    return JsonResponse(list(vagas_por_mes), safe=False)

# Template vai carregar os dados via Ajax e usar Chart.js para gerar os gráficos


# Cadastro de usuário
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Listagem de vagas
def lista_vagas(request):
    vagas = Vaga.objects.all()
    return render(request, 'lista_vagas.html', {'vagas': vagas})

# Detalhes da vaga com candidatos
def detalhes_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)
    return render(request, 'detalhes_vaga.html', {'vaga': vaga})

# Criar vaga
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user
            vaga.save()
            return redirect('lista_vagas')
    else:
        form = VagaForm()
    return render(request, 'criar_vaga.html', {'form': form})

# Editar vaga
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            return redirect('detalhes_vaga', vaga_id=vaga.id)
    else:
        form = VagaForm(instance=vaga)
    return render(request, 'editar_vaga.html', {'form': form})

# Candidatar-se à vaga
def candidatar(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            candidato = form.save(commit=False)
            candidato.vaga = vaga
            candidato.save()
            return redirect('detalhes_vaga', vaga_id=vaga.id)
    else:
        form = CandidatoForm()
    return render(request, 'candidatar.html', {'form': form, 'vaga': vaga})
