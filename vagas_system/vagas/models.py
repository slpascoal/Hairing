from django.db import models
from users.models import CustomUser

class Vaga(models.Model):
    nome = models.CharField(max_length=255)
    faixa_salarial = models.CharField(max_length=50, choices=[
        ('Ate 1000', 'Até 1.000'),
        ('1000-2000', 'De 1.000 a 2.000'),
        ('2000-3000', 'De 2.000 a 3.000'),
        ('Acima de 3000', 'Acima de 3.000')
    ])
    requisitos = models.TextField()
    escolaridade_minima = models.CharField(max_length=50, choices=[
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('tecnologo', 'Tecnólogo'),
        ('superior', 'Ensino Superior'),
        ('mba', 'Pós / MBA / Mestrado'),
        ('doutorado', 'Doutorado')
    ])
    empresa = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_empresa': True})
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Candidatura(models.Model):
    candidato = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_candidato': True})
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    pretensao_salarial = models.CharField(max_length=50)
    experiencia = models.TextField()
    escolaridade = models.CharField(max_length=50, choices=[
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('tecnologo', 'Tecnólogo'),
        ('superior', 'Ensino Superior'),
        ('mba', 'Pós / MBA / Mestrado'),
        ('doutorado', 'Doutorado')
    ])
    pontuacao = models.IntegerField(default=0)

    def calcular_pontuacao(self):
        pontuacao = 0

        # Faixa salarial
        faixa_salarial_mapping = {
            'Ate 1000': 1000,
            '1000-2000': 2000,
            '2000-3000': 3000,
            'Acima de 3000': 999999,  # Representa salários acima de 3.000
        }

        pretensao_salarial_int = int(self.pretensao_salarial.replace('R$', '').replace('.', '').strip())

        if faixa_salarial_mapping[self.vaga.faixa_salarial] >= pretensao_salarial_int:
            pontuacao += 1

        # Escolaridade
        escolaridade_niveis = {
            'fundamental': 1,
            'medio': 2,
            'tecnologo': 3,
            'superior': 4,
            'mba': 5,
            'doutorado': 6,
        }

        if escolaridade_niveis[self.escolaridade] >= escolaridade_niveis[self.vaga.escolaridade_minima]:
            pontuacao += 1

        self.pontuacao = pontuacao
        self.save()

    def __str__(self):
        return f"{self.candidato.email} - {self.vaga.nome} ({self.pontuacao} pontos)"
