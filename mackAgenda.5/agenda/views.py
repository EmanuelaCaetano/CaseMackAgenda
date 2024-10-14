from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Tarefa
from .forms import TarefaForm
from .forms import CadastroForm
from django.contrib.sessions.models import Session

# Create your views here.

# Home do Projeto
def home(request):
    return render(request, 'usuarios/home.html')

def cadastro_view(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html', {
            'form': UserCreationForm()
        })   
    else: 
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],  # Adiciona o email
                    first_name=request.POST.get('first_name', ''),  # Adiciona o primeiro nome, se disponível
                    last_name=request.POST.get('last_name', '')  # Adiciona o sobrenome, se disponível
                )
                user.save()
                login(request, user)
                return redirect('tarefas')  # Redireciona para a página de tarefas
                
            except Exception as e:
                return render(request, 'usuarios/cadastro.html', { 
                    'form': UserCreationForm(),
                    'error': 'Usuário já existe'
                }) 
           
        return render(request, 'usuarios/cadastro.html', { 
            'form': UserCreationForm(),
            'error': 'As senhas são diferentes'
        })  

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Passa os dados POST para o formulário
        if form.is_valid():  # Verifica se os dados são válidos
            user = form.get_user()  # Obtém o usuário autenticado
            login(request, user)  # Faz o login do usuário
            return redirect('tarefas')  # Redireciona para a página de tarefas
        else:
            return render(request, 'usuarios/login.html', {
                'form': form,  # Retorna o formulário com os erros se houver
                'error': 'Usuário ou senha estão incorretos'
            })
    else:
        form = AuthenticationForm()  # Exibe o formulário vazio se for uma requisição GET
        return render(request, 'usuarios/login.html', {
            'form': form
        })
        
@login_required      
def listar_tarefas(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Filtra as tarefas do usuário logado
        tarefas = Tarefa.objects.filter(user=request.user)
    else:
        # Se o usuário não estiver autenticado, pode retornar uma lista vazia ou redirecionar
        tarefas = []  # Ou você pode redirecionar para a página de login

    # Renderiza o template com as tarefas
    return render(request, 'usuarios/tarefas.html', {'tarefas': tarefas})

@login_required
def tarefas_view(request):
    tarefas = Tarefa.objects.filter(user=request.user) #Filtra as tarefas do usuário 
    return render(request, 'usuarios/tarefas.html', {'tarefas': tarefas})

@login_required       
def sair(request):
    request.session.flush()
    Session.objects.filter(session_key=request.session.session_key).delete()
    logout(request)
    return redirect('home')

@login_required       
def Tarefas(request):
    tarefas = Tarefa.objects.filter(user=request.user)
    #tarefas = Tarefa.objects.all()
    return render(request, 'usuarios/tarefas.html', {'tarefas': tarefas})  # Certifique-se de que a rota está correta

@login_required
def criar_tarefa(request):
    tarefas = Tarefa.objects.filter(user=request.user)
    if request.method == 'POST':  # Verifica se a requisição é POST para salvar a tarefa
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.user = request.user  # Associa a tarefa ao usuário logado
            tarefa.save()
            return redirect('tarefas')  # Redireciona para a página de listagem de tarefas
    else:
        form = TarefaForm()  # Se não for POST, exibe o formulário vazio
    
    tarefas = Tarefa.objects.filter(user=request.user)  # Pega as tarefas do usuário logado
    return render(request, 'usuarios/tarefas.html', {'form': form, 'tarefas': tarefas})  # Passa o formulário e as tarefas no mesmo dicionário

@login_required  
def editar_tarefa(request, tarefa_id):

    tarefa = get_object_or_404(Tarefa, id=tarefa_id, user=request.user)
    
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)  # Verifique se o form está sendo usado corretamente
        if form.is_valid():
            form.save()
            return redirect('tarefas')
    else:
        form = TarefaForm(instance=tarefa)  # Para o método GET, preenche o formulário com a tarefa existente
    return render(request, 'usuarios/tarefas.html', {'form': form, 'tarefa': tarefa})  # Certifique-se de passar a tarefa

@login_required  
def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, user=request.user)

    if request.method == 'POST':
        tarefa.delete()
        return redirect('tarefas')




