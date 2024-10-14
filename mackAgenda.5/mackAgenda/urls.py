"""
URL configuration for mackAgenda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from agenda import views
#from . import views  # Importa as views do módulo atual
from django.contrib import admin

#urlpatterns = [
#    path('', views.login_view, name='home'),  # Redireciona a URL raiz para a tela de login
#    path('login/', views.login_view, name='login'),
#    path('cadastro/', views.cadastro_view, name='cadastro'),
#    path('tarefas/', views.tarefas_view, name='tarefas'),
#    path('sair/', views.logout_view, name='sair'),
#]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('sair/', views.sair, name='sair'),
    path('tarefas/', views.Tarefas, name='tarefas'),
    path('tarefas/criar/', views.criar_tarefa, name='criar_tarefa'),  # URL para criar tarefa
    path('tarefas/editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),  # URL para editar tarefa
    path('tarefas/excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir_tarefa')
    
  # URL para excluir tarefa

]
