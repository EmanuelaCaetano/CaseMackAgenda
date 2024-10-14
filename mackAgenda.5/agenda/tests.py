
# tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthenticationTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_cadastro_usuario(self):
        response = self.client.post(reverse('cadastro'), {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertEqual(response.status_code, 302)  # Espera redirecionar após o cadastro
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Verifica se o usuário foi criado

    def test_cadastro_usuario_existente(self):
        response = self.client.post(reverse('cadastro'), {
            'username': self.username,
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertEqual(response.status_code, 200)  # Espera permanecer na mesma página
        self.assertContains(response, 'Usuário já existe')  # Verifica a mensagem de erro

    def test_cadastro_senhas_diferentes(self):
        response = self.client.post(reverse('cadastro'), {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'differentpass',
        })
        self.assertEqual(response.status_code, 200)  # Espera permanecer na mesma página
        self.assertContains(response, 'As senhas são diferentes')  # Verifica a mensagem de erro

    def test_login_usuario(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)  # Espera redirecionar após o login
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # Verifica se o usuário está autenticado

    def test_login_usuario_invalido(self):
        response = self.client.post(reverse('login'), {
            'username': 'invaliduser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Espera permanecer na mesma página
        self.assertContains(response, 'Usuário ou senha estão incorretos')  # Verifica a mensagem de erro


"""from django.test import TestCase
from django.urls import reverse
from .models import Tarefa
from django.contrib.auth.models import User

class TarefaViewTests(TestCase):

    def setUp(self):
        # Cria um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_exibir_tarefas_usuario_logado(self):
        # Cria algumas tarefas associadas ao usuário
        Tarefa.objects.create(
            disciplina='Matemática',
            data_entrega='2024-10-15',
            descricao='Fazer exercícios',
            user=self.user  # Associando ao usuário
        )
        Tarefa.objects.create(
            disciplina='História',
            data_entrega='2024-10-20',
            descricao='Estudar para a prova',
            user=self.user  # Associando ao usuário
        )

        # Faz uma requisição à view que exibe as tarefas
        response = self.client.get(reverse('tarefas'))  # Altere 'tarefas' para o nome correto da URL

        # Verifica se a resposta está correta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')

        # Verifica se as tarefas aparecem no contexto
        self.assertIn('tarefas', response.context)

        # Verifica se as tarefas estão presentes na resposta
        self.assertContains(response, 'Matemática')
        self.assertContains(response, 'História')

    def test_exibir_tarefas_usuario_sem_tarefas(self):
        # Verifica se não há tarefas associadas ao usuário
        response = self.client.get(reverse('tarefas'))

        # Verifica se a resposta está correta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')

        # Verifica se a mensagem de "nenhuma tarefa salva" está presente
        self.assertContains(response, 'Nenhuma tarefa salva.')  # Altere a string para a correta
        """


"""from django.test import TestCase
from django.urls import reverse
from .models import Tarefa
from django.contrib.auth.models import User

class TarefaViewTests(TestCase):

    def setUp(self):
        # Cria um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_exibir_tarefas_usuario_logado(self):
        # Cria algumas tarefas associadas ao usuário
        Tarefa.objects.create(disciplina='Matemática', data_entrega='2024-10-15', descricao='Fazer exercícios')
        Tarefa.objects.create(disciplina='História', data_entrega='2024-10-20', descricao='Estudar para a prova')

        # Faz uma requisição à view que exibe as tarefas
        response = self.client.get(reverse('tarefas'))  # Altere 'tarefas' para o nome correto da URL

        # Verifica se a resposta está correta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')

        # Verifica se as tarefas aparecem no contexto
        self.assertIn('tarefas', response.context)

        # Verifica se as tarefas estão presentes na resposta
        self.assertContains(response, 'Matemática')
        self.assertContains(response, 'História')

    def test_exibir_tarefas_usuario_sem_tarefas(self):
        # Verifica se não há tarefas associadas ao usuário
        response = self.client.get(reverse('tarefas'))

        # Verifica se a resposta está correta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')

        # Verifica se a mensagem de "nenhuma tarefa encontrada" está presente
        self.assertContains(response, 'Nenhuma tarefa encontrada.')"""


"""from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tarefa
from .forms import TarefaForm

class TarefaViewTests(TestCase):
    def setUp(self):
        # Criação de um usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_tarefas_view(self):
        # Testa se a view de tarefas retorna um status 200
        response = self.client.get(reverse('tarefas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')

    def test_criar_tarefa(self):
        # Testa a criação de uma nova tarefa com dados válidos
        data = {
            'disciplina': 'Matemática',
            'data_entrega': '2024-10-20',
            'descricao': 'Entregar o trabalho de cálculo.'
        }
        response = self.client.post(reverse('criar_tarefa'), data=data)
        self.assertEqual(response.status_code, 302)  # Redireciona após criação
        self.assertTrue(Tarefa.objects.filter(disciplina='Matemática').exists())

    def test_criar_tarefa_invalid(self):
        # Testa a criação de uma nova tarefa com dados inválidos
        data = {
            'disciplina': '',
            'data_entrega': '',
            'descricao': ''
        }
        response = self.client.post(reverse('criar_tarefa'), data=data)
        self.assertEqual(response.status_code, 200)  # Permanece na página
        self.assertFormError(response, 'form', 'disciplina', 'Este campo é obrigatório.')

    def test_editar_tarefa(self):
        # Testa a edição de uma tarefa existente
        tarefa = Tarefa.objects.create(disciplina='Física', data_entrega='2024-10-22', descricao='Estudar para a prova.', user=self.user)
        data = {
            'disciplina': 'Física Avançada',
            'data_entrega': '2024-10-25',
            'descricao': 'Estudar para a prova de Física Avançada.'
        }
        response = self.client.post(reverse('editar_tarefa', args=[tarefa.id]), data=data)
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.disciplina, 'Física Avançada')
        self.assertEqual(response.status_code, 302)  # Redireciona após edição

    def test_excluir_tarefa(self):
        # Testa a exclusão de uma tarefa existente
        tarefa = Tarefa.objects.create(disciplina='Química', data_entrega='2024-10-30', descricao='Preparar experimento.', user=self.user)
        response = self.client.post(reverse('excluir_tarefa', args=[tarefa.id]))
        self.assertEqual(response.status_code, 302)  # Redireciona após exclusão
        self.assertFalse(Tarefa.objects.filter(id=tarefa.id).exists())"""



"""from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Tarefa
from .forms import TarefaForm

class TarefaViewsTest(TestCase):

    def setUp(self):
        # Cria um usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # Faz login

    def test_sair(self):
        # Testa a funcionalidade de sair
        response = self.client.post(reverse('sair'))  # Chama a URL de sair
        self.assertRedirects(response, reverse('home'))  # Verifica se redireciona para home
        # Verifica se o usuário foi deslogado
        response = self.client.get(reverse('tarefas'))  # Tenta acessar tarefas após logout
        self.assertEqual(response.status_code, 302)  # Deve redirecionar para login

    def test_tarefas_view(self):
        # Testa a view de tarefas
        response = self.client.get(reverse('tarefas'))  # Chama a URL de tarefas
        self.assertEqual(response.status_code, 200)  # Verifica se a resposta é OK
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')  # Verifica se o template correto foi usado

    def test_criar_tarefa_valid_data(self):
        # Testa a criação de tarefa com dados válidos
        data = {
            'titulo': 'Tarefa Teste',  # Substitua por campos reais do seu formulário
            'descricao': 'Descrição da tarefa',  # Substitua por campos reais do seu formulário
        }
        response = self.client.post(reverse('criar_tarefa'), data)  # Chama a URL de criar tarefa
        self.assertRedirects(response, reverse('tarefas'))  # Verifica se redireciona para tarefas
        self.assertTrue(Tarefa.objects.filter(titulo='Tarefa Teste').exists())  # Verifica se a tarefa foi criada

    def test_criar_tarefa_invalid_data(self):
        # Testa a criação de tarefa com dados inválidos
        data = {
            'titulo': '',  # Título vazio para simular erro
            'descricao': 'Descrição da tarefa',
        }
        response = self.client.post(reverse('criar_tarefa'), data)  # Chama a URL de criar tarefa
        self.assertEqual(response.status_code, 200)  # Verifica se a resposta é OK
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')  # Verifica se o template correto foi usado
        self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')  # Verifica erro de formulário
"""



"""from django.urls import reverse
from django.test import TestCase
from .models import Tarefa
from .forms import TarefaForm  # Certifique-se de importar seu formulário
from django.contrib.auth.models import User

class CriarTarefaTests(TestCase):

    def setUp(self):
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_criar_tarefa_get(self):
        # Faz login do usuário
        self.client.login(username='testuser', password='testpass')
        
        # Envia uma requisição GET para a view
        response = self.client.get(reverse('criar_tarefa'))  # Altere 'criar_tarefa' para o nome correto da URL

        # Verifica se a resposta é 200 e se o formulário está presente no contexto
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/tarefa.html')
        self.assertIsInstance(response.context['form'], TarefaForm)

    def test_criar_tarefa_post_valid(self):
        # Faz login do usuário
        self.client.login(username='testuser', password='testpass')
        
        # Define os dados da tarefa
        data = {
            'titulo': 'Tarefa Válida',
            'descricao': 'Descrição da tarefa válida',
        }

        # Envia uma requisição POST para criar a tarefa
        response = self.client.post(reverse('criar_tarefa'), data)

        # Verifica se a tarefa foi criada
        self.assertEqual(response.status_code, 302)  # Redirecionamento após a criação
        self.assertTrue(Tarefa.objects.filter(titulo='Tarefa Válida').exists())

    def test_criar_tarefa_post_invalid(self):
        # Faz login do usuário
        self.client.login(username='testuser', password='testpass')
        
        # Dados inválidos (faltando título)
        data = {
            'titulo': '',  # Título vazio
            'descricao': 'Descrição da nova tarefa',
        }

        # Envia uma requisição POST para criar a tarefa
        response = self.client.post(reverse('criar_tarefa'), data)

        # Verifica se a tarefa não foi criada
        self.assertEqual(response.status_code, 200)  # Retorna a página do formulário
        self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')  # Mensagem de erro
        self.assertTemplateUsed(response, 'usuarios/tarefa.html')  # Verifica se a template é a correta"""



"""from django.urls import reverse
from django.test import TestCase
from .models import Tarefa
from django.contrib.auth.models import User

class TarefaTests(TestCase):

    def setUp(self):
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_criar_tarefa_view(self):
        # Faz login do usuário
        self.client.login(username='testuser', password='testpass')
        
        # Define os dados da tarefa
        data = {
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da nova tarefa',
        }
        
        # Envia uma requisição POST para criar a tarefa
        response = self.client.post(reverse('criar_tarefa'), data)

        # Verifica se a tarefa foi criada
        self.assertEqual(response.status_code, 302)  # Redirecionamento após a criação
        self.assertTrue(Tarefa.objects.filter(titulo='Nova Tarefa').exists())

    def test_criar_tarefa_view_invalid(self):
        # Faz login do usuário
        self.client.login(username='testuser', password='testpass')

        # Dados inválidos (faltando título)
        data = {
            'titulo': '',  # Título vazio
            'descricao': 'Descrição da nova tarefa',
        }
        
        # Envia uma requisição POST para criar a tarefa
        response = self.client.post(reverse('criar_tarefa'), data)

        # Verifica se a tarefa não foi criada
        self.assertEqual(response.status_code, 200)  # Retorna a página de criação
        self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')  # Mensagem de erro
"""



"""from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tarefa
from .forms import TarefaForm

class TarefaTests(TestCase):

    def setUp(self):
        # Criação de um usuário para os testes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_tarefas_view(self):
        response = self.client.get(reverse('tarefas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/tarefas.html')

    def test_criar_tarefa_view(self):
        response = self.client.post(reverse('criar_tarefa'), {
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da nova tarefa',
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após criar
        self.assertTrue(Tarefa.objects.filter(titulo='Nova Tarefa').exists())

    def test_criar_tarefa_view_invalid(self):
        response = self.client.post(reverse('criar_tarefa'), {
            'titulo': '',  # Título vazio deve ser inválido
            'descricao': 'Descrição da nova tarefa',
        })
        self.assertEqual(response.status_code, 200)  # Retorna ao formulário com erros
        self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')

    def test_editar_tarefa_view(self):
        tarefa = Tarefa.objects.create(titulo='Tarefa para editar', descricao='Descrição', user=self.user)
        response = self.client.post(reverse('editar_tarefa', kwargs={'tarefa_id': tarefa.id}), {
            'titulo': 'Tarefa Editada',
            'descricao': 'Descrição editada',
        })
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.titulo, 'Tarefa Editada')
        self.assertEqual(response.status_code, 302)  # Redireciona após editar

    def test_excluir_tarefa_view(self):
        tarefa = Tarefa.objects.create(titulo='Tarefa para excluir', descricao='Descrição', user=self.user)
        response = self.client.post(reverse('excluir_tarefa', kwargs={'tarefa_id': tarefa.id}))
        self.assertEqual(response.status_code, 302)  # Redireciona após excluir
        self.assertFalse(Tarefa.objects.filter(id=tarefa.id).exists())

    def test_excluir_tarefa_view_not_found(self):
        response = self.client.post(reverse('excluir_tarefa', kwargs={'tarefa_id': 999}))  # ID não existe
        self.assertEqual(response.status_code, 404)  # Retorna 404 para tarefa não encontrada
"""

"""from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tarefa

class TarefaTests(TestCase):
    def setUp(self):
        # Cria um usuário para os testes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        print("\nUsuário testuser criado e logado.")

    def test_criar_tarefa(self):
        print("\nIniciando teste de criação de tarefa.")
        # Simula o envio de dados para criar uma nova tarefa
        response = self.client.post(reverse('criar_tarefa'), {
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da tarefa',
        })

        # Verifica se a tarefa foi criada
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após a criação
        self.assertEqual(Tarefa.objects.count(), 1)  # Verifica se há 1 tarefa no banco de dados
        self.assertEqual(Tarefa.objects.first().titulo, 'Nova Tarefa')  # Verifica o título da tarefa
        print("Tarefa criada com sucesso. Redirecionamento e título da tarefa confirmados.")

    def test_editar_tarefa(self):
        print("\nIniciando teste de edição de tarefa.")
        # Cria uma tarefa
        tarefa = Tarefa.objects.create(titulo='Tarefa Antiga', descricao='Descrição antiga', usuario=self.user)

        # Simula o envio de dados para editar a tarefa
        response = self.client.post(reverse('editar_tarefa', args=[tarefa.id]), {
            'titulo': 'Tarefa Editada',
            'descricao': 'Descrição editada',
        })

        # Verifica se a tarefa foi editada
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após a edição
        tarefa.refresh_from_db()  # Atualiza a instância da tarefa do banco de dados
        self.assertEqual(tarefa.titulo, 'Tarefa Editada')  # Verifica se o título foi editado
        self.assertEqual(tarefa.descricao, 'Descrição editada')  # Verifica se a descrição foi editada
        print("Tarefa editada com sucesso. Redirecionamento e novos valores confirmados.")

    def test_excluir_tarefa(self):
        print("\nIniciando teste de exclusão de tarefa.")
        # Cria uma tarefa
        tarefa = Tarefa.objects.create(titulo='Tarefa para deletar', descricao='Descrição para deletar', usuario=self.user)

        # Simula a requisição para excluir a tarefa
        response = self.client.post(reverse('excluir_tarefa', args=[tarefa.id]))

        # Verifica se a tarefa foi excluída
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após a exclusão
        self.assertEqual(Tarefa.objects.count(), 0)  # Verifica se a tarefa foi removida do banco de dados
        print("Tarefa excluída com sucesso.")

    def test_acesso_sem_login(self):
        print("\nIniciando teste de acesso não autorizado.")
        # Faz logout do usuário autenticado
        self.client.logout()

        # Testa se a criação, edição e exclusão de tarefas redirecionam para a página de login
        response = self.client.get(reverse('criar_tarefa'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
        print("Acesso à criação de tarefas redirecionado para login, conforme esperado.")

        # Cria uma tarefa como o usuário de teste
        tarefa = Tarefa.objects.create(titulo='Tarefa Teste', descricao='Descrição Teste', usuario=self.user)

        # Testa a edição sem login
        response = self.client.get(reverse('editar_tarefa', args=[tarefa.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
        print("Acesso à edição de tarefas redirecionado para login, conforme esperado.")

        # Testa a exclusão sem login
        response = self.client.get(reverse('excluir_tarefa', args=[tarefa.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
        print("Acesso à exclusão de tarefas redirecionado para login, conforme esperado.")

    def test_validacao_campos(self):
        print("\nIniciando teste de validação de campos obrigatórios.")
        # Testa a criação de tarefa sem título
        response = self.client.post(reverse('criar_tarefa'), {
            'descricao': 'Descrição sem título',
        })
        self.assertEqual(response.status_code, 200)  # Deve retornar a página com erro
        self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')
        print("Validação de criação sem título confirmada.")

        # Testa a edição de tarefa sem título
        tarefa = Tarefa.objects.create(titulo='Tarefa com título', descricao='Descrição completa', usuario=self.user)
        response = self.client.post(reverse('editar_tarefa', args=[tarefa.id]), {
            'descricao': 'Descrição editada sem título',
        })
        self.assertEqual(response.status_code, 200)  # Deve retornar a página com erro
        self.assertFormError(response, 'form', 'titulo', 'Este campo é obrigatório.')
        print("Validação de edição sem título confirmada.")
"""

"""from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(TestCase):

    def setUp(self):
        # Cria um usuário de teste
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_cadastro_e_login(self):
        # Tenta acessar a página de login
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)  # Verifica se a página de login está acessível

        # Realiza o login com credenciais corretas
        login_response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        print(f'Login Response: {login_response}')  # Debug: verifique a resposta do login

        # Verifica se o redirecionamento acontece após o login
        self.assertEqual(login_response.status_code, 302)  # Espera um redirecionamento
        self.assertRedirects(login_response, reverse('tarefas'))  # Verifica se redireciona para 'tarefas'

    def test_login_incorreto(self):
        # Tenta realizar login com credenciais incorretas
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        print(f'Login Incorreto Response: {response}')  # Debug: verifique a resposta do login
        self.assertEqual(response.status_code, 200)  # A página de login deve continuar acessível
        self.assertContains(response, 'Usuário ou senha está incorreto')  # Verifica a mensagem de erro

    def test_acesso_tarefas_sem_login(self):
        # Tenta acessar a página de tarefas sem estar logado
        response = self.client.get(reverse('tarefas'))
        print(f'Acesso sem Login Response: {response}')  # Debug: verifique a resposta
        self.assertEqual(response.status_code, 302)  # Espera redirecionamento
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tarefas')}")  # Verifica redirecionamento para login

    def test_criacao_tarefa_apos_login(self):
        # Realiza o login
        self.client.login(username=self.username, password=self.password)
        
        # Acessa a página de tarefas após login
        response = self.client.get(reverse('tarefas'))
        print(f'Acesso Tarefas após Login Response: {response}')  # Debug: verifique a resposta
        self.assertEqual(response.status_code, 200)  # A página de tarefas deve estar acessível
        self.assertContains(response, 'Lista de Tarefas')  # Verifica se a página de tarefas contém este texto
"""


"""from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Tarefa  # Ajuste de acordo com sua estrutura de projetos

class AuthTests(TestCase):
    def test_cadastro_e_login(self):
        # Testar o cadastro
        response = self.client.post(reverse('cadastro'), {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        print("Cadastro Response:", response)  # Verifica a resposta do cadastro
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após cadastro

        # Testar se o usuário foi criado
        user_exists = User.objects.filter(username='testuser').exists()
        print("Usuário criado:", user_exists)  # Verifica se o usuário foi criado
        self.assertTrue(user_exists)  # Verifica que o usuário foi criado

        # Testar o login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        print("Login Response:", response)  # Verifica a resposta do login
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após login
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # Verifica se o usuário está autenticado

        # Testar a criação de uma tarefa
        response = self.client.post(reverse('criar_tarefa'), {
            'nome': 'Tarefa 1'
        })
        print("Criação de Tarefa Response:", response)  # Verifica a resposta da criação de tarefa
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após criar tarefa

        # Testar se a tarefa foi criada
        tarefa_exists = Tarefa.objects.filter(nome='Tarefa 1').exists()
        print("Tarefa criada:", tarefa_exists)  # Verifica se a tarefa foi criada
        self.assertTrue(tarefa_exists)  # Verifica que a tarefa foi criada
        """


"""from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tarefa

class TarefaViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_criar_tarefa(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('criar_tarefa'), {
            'disciplina': 'Matemática',
            'data_entrega': '2024-12-31',
            'descricao': 'Estudar para a prova de matemática',
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após a criação
        self.assertEqual(Tarefa.objects.count(), 1)
        self.assertEqual(Tarefa.objects.get().disciplina, 'Matemática')
        print(response)

    def test_editar_tarefa(self):
        self.client.login(username='testuser', password='testpass')
        tarefa = Tarefa.objects.create(disciplina='Tarefa 1', data_entrega='2024-12-01', descricao='Descrição da tarefa 1', user=self.user)
        response = self.client.post(reverse('editar_tarefa', args=[tarefa.id]), {
            'disciplina': 'Tarefa 1 Editada',
            'data_entrega': '2024-12-10',
            'descricao': 'Descrição editada da tarefa 1',
        })
        tarefa.refresh_from_db()  # Atualiza a instância da tarefa
        self.assertEqual(response.status_code, 302)
        self.assertEqual(tarefa.disciplina, 'Tarefa 1 Editada')
        print(response)

    def test_excluir_tarefa(self):
        self.client.login(username='testuser', password='testpass')
        tarefa = Tarefa.objects.create(disciplina='Tarefa a ser excluída', data_entrega='2024-12-15', descricao='Descrição', user=self.user)
        print(tarefa)
        response = self.client.post(reverse('excluir_tarefa', args=[tarefa.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tarefa.objects.count(), 0)

    def test_listar_tarefas(self):
        self.client.login(username='testuser', password='testpass')
        Tarefa.objects.create(disciplina='Tarefa 1', data_entrega='2024-12-01', descricao='Descrição da tarefa 1', user=self.user)
        response = self.client.get(reverse('tarefas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tarefa 1')
        print(response)

    def test_tarefas_usuario_logado(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='testuser', password='testpass')
        Tarefa.objects.create(disciplina='Tarefa de outro usuário', data_entrega='2024-12-20', descricao='Descrição', user=other_user)
        response = self.client.get(reverse('tarefas'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Tarefa de outro usuário')  # Verifica se não aparece
        print(other_user)
"""