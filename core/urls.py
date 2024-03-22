
from django.contrib import admin
from django.urls import path
from ica import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('home', views.home_view, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('cadastrar-aluno', views.cadastro_aluno, name='cadastro-aluno'),
    path('cadastrar-professor', views.cadastro_professor, name='cadastro-professor'),
    path('cadastrar-coordenador', views.cadastro_coordenador, name='cadastro_coordenador'),
    path('cadastrar-disciplina', views.cadastro_disciplina, name='cadastro-disciplina'),
    path('cadastrar-curso', views.cadastro_curso, name='cadastro-curso'),
    path('cadastrar-turma', views.cadastro_turma, name='cadastro-turma'),
    path('cadastrar-falta', views.cadastro_falta, name='cadastro-falta'),
    path('cadastrar-notas', views.cadastro_notas, name='cadastro-notas'),
    path('cadastrar-nota-final', views.cadastro_nota_final, name='cadastro-nota-final'),
    path('notas-faltas', views.notas_faltas, name='notas-faltas'),
    path('perfil', views.info_perfil, name='perfil'),
    path('info-alunos', views.info_alunos, name='info_alunos'),
    path('info-curso', views.info_cursos, name='info_cursos'),
    path('info-professores', views.info_professores, name='info_professores'),
    path('alterar-senha/', auth_views.PasswordResetView.as_view(template_name='alterar_senha.html'), name="password_reset"),
    path('senha-enviada/', auth_views.PasswordResetDoneView.as_view(template_name='alteracao_enviada.html'), name="password_reset_done"),
    path('alterar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='nova_senha.html'), name="password_reset_confirm"),
    path('alteração-concluida/', auth_views.PasswordResetCompleteView.as_view(template_name='alteracao_completa.html'), name="password_reset_complete"),
] + static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)
