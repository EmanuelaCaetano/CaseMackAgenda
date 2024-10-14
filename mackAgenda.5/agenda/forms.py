from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tarefa

# Formulário de cadastro de usuários
class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ra = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'ra', 'password1', 'password2']

# Formulário de criação de tarefas
class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['disciplina', 'data_entrega', 'descricao']
