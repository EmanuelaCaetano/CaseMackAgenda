from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona a tarefa ao usuário
    disciplina = models.CharField(max_length=100)
    data_entrega = models.DateField()
    descricao = models.TextField()

    def __str__(self):
        return self.disciplina
