from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_empresa = models.BooleanField(default=False)
    is_candidato = models.BooleanField(default=False)

    # Definindo que o email será o campo usado para login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Campos obrigatórios além de email e senha
