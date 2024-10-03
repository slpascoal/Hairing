from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.EmailField(unique=True)

class Vaga(models.Model):
    NIVEIS_ESCOLARIDADE = [
        ('EF', 'Ensino Fundamental'),
        ('EM', 'Ensino Médio'),
        ('TEC', 'Tecnólogo'),
        ('ES', 'Ensino Superior'),
        ('MBA', 'Pós / MBA / Mestrado'),
        ('DR', 'Doutorado')
    ]
    FAIXA_SALARIAL = [
        ('0-1000', 'Até 1.000'),
        ('1000-2000', 'De 1.000 a 2.000'),
        ('2000-3000', 'De 2.000 a 3.000'),
        ('3000+', 'Acima de 3.000'),
    ]
    nome = models.CharField(max_length=255)
    faixa_salarial = models.CharField(max_length=10, choices=FAIXA_SALARIAL)
    requisitos = models.TextField()
    escolaridade_minima = models.CharField(max_length=3, choices=NIVEIS_ESCOLARIDADE)
    empresa = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Candidato(models.Model):
    PRETENSAO_SALARIAL = [
        ('0-1000', 'Até 1.000'),
        ('1000-2000', 'De 1.000 a 2.000'),
        ('2000-3000', 'De 2.000 a 3.000'),
        ('3000+', 'Acima de 3.000'),
    ]
    nome = models.CharField(max_length=255)
    pretensao_salarial = models.CharField(max_length=10, choices=PRETENSAO_SALARIAL)
    experiencia = models.TextField()
    escolaridade = models.CharField(max_length=3, choices=Vaga.NIVEIS_ESCOLARIDADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidatos')

    def __str__(self):
        return self.nome
