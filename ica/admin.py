from django.contrib import admin
from .models import Estatistica, Graduacao, Turma, Disciplina, CustomUser

@admin.register(Estatistica)
class EstatisticaoAdmin(admin.ModelAdmin):
    list_display = ['aluno_matricula', 'aluno_disciplina', 'media_bm1','media_bm2', 'media_fn']

@admin.register(Graduacao)
class GraduacaoAdmin(admin.ModelAdmin):
    list_display = ['id_curso','nome_curso']


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['id_disciplina','nome_disciplina','duracao_disciplina']


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome_turma']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
     list_display = ['matricula', 'username', 'cpf']


