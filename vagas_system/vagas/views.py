from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vaga, Candidatura
from .forms import VagaForm
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
import json
from .forms import CandidaturaForm
from django.shortcuts import get_object_or_404, redirect

@login_required
def listar_candidaturas(request):
    candidaturas = Candidatura.objects.filter(candidato=request.user)
    return render(request, 'vagas/listar_candidaturas.html', {'candidaturas': candidaturas})


@login_required
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.method == 'POST':
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.candidato = request.user  # Atribuir o usuário logado como candidato
            candidatura.vaga = vaga  # Atribuir a vaga
            candidatura.save()

            # Calcula a pontuação automaticamente
            candidatura.calcular_pontuacao()

            return redirect('listar_vagas_disponiveis')
    else:
        form = CandidaturaForm()

    return render(request, 'vagas/candidatar_vaga.html', {'form': form, 'vaga': vaga})


@login_required
def listar_vagas_disponiveis(request):
    vagas = Vaga.objects.all()  # Aqui você pode adicionar filtros se desejar
    return render(request, 'vagas/listar_vagas_disponiveis.html', {'vagas': vagas})


@login_required
def relatorio_vagas(request):
    # Agrupando as vagas por mês
    vagas_por_mes = Vaga.objects.filter(empresa=request.user).annotate(mes=TruncMonth('criada_em')).values('mes').annotate(total=Count('id')).order_by('mes')

    # Agrupando candidaturas por mês
    candidatos_por_mes = Candidatura.objects.filter(vaga__empresa=request.user).annotate(mes=TruncMonth('vaga__criada_em')).values('mes').annotate(total=Count('id')).order_by('mes')

    # Formatando para o Chart.js
    meses = [datetime.strftime(vaga['mes'], "%b %Y") for vaga in vagas_por_mes]
    vagas_count = [vaga['total'] for vaga in vagas_por_mes]
    candidatos_count = [candidato['total'] for candidato in candidatos_por_mes]

    return render(request, 'vagas/relatorio_vagas.html', {
        'meses': json.dumps(meses),
        'vagas_por_mes': json.dumps(vagas_count),
        'candidatos_por_mes': json.dumps(candidatos_count),
    })


@login_required
def listar_vagas(request):
    vagas = Vaga.objects.filter(empresa=request.user)
    return render(request, 'vagas/listar_vagas.html', {'vagas': vagas})

@login_required
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user  # Associa a vaga à empresa logada
            vaga.save()
            return redirect('listar_vagas')
    else:
        form = VagaForm()
    return render(request, 'vagas/criar_vaga.html', {'form': form})

@login_required
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            vaga = form.save()

            # Recalcular a pontuação de todos os candidatos, se a vaga foi alterada
            candidaturas = Candidatura.objects.filter(vaga=vaga)
            for candidatura in candidaturas:
                candidatura.calcular_pontuacao()

            return redirect('listar_vagas')
    else:
        form = VagaForm(instance=vaga)
    return render(request, 'vagas/editar_vaga.html', {'form': form, 'vaga': vaga})


@login_required
def deletar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    vaga.delete()
    return redirect('listar_vagas')

@login_required
def listar_candidatos(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    candidaturas = Candidatura.objects.filter(vaga=vaga)
    return render(request, 'vagas/listar_candidatos.html', {'vaga': vaga, 'candidaturas': candidaturas})
