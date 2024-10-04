from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=255)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'is_empresa', 'is_candidato')

    # Exemplo de validação adicional (opcional)
    def clean(self):
        cleaned_data = super().clean()
        is_empresa = cleaned_data.get("is_empresa")
        is_candidato = cleaned_data.get("is_candidato")

        if is_empresa and is_candidato:
            raise forms.ValidationError("Você não pode ser Empresa e Candidato ao mesmo tempo.")
