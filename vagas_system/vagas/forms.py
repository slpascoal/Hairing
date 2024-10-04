from django import forms
from .models import Vaga
from .models import Candidatura


class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ['pretensao_salarial', 'experiencia', 'escolaridade']


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['nome', 'faixa_salarial', 'requisitos', 'escolaridade_minima']

