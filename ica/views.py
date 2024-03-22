from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import F
from .models import CustomUser, Disciplina, Graduacao, Estatistica, Turma
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from django.core.mail import send_mail
from decouple import config
import random

#HOME PAGE
@login_required(login_url='/login')     
def home_view(request):
    return render(request, 'home.html')

#LOGIN PAGE
def login_view(request):
     if request.method == 'GET':
         return render(request, 'login.html', {
             'incorrect_login': False
         })
     elif request.method == 'POST':
         cpf = request.POST.get('cpf')
         password = request.POST.get('password')
         user = authenticate(request, cpf=cpf, password=password)
         if user is not None:
             login(request, user)
             return HttpResponseRedirect('/home')
         else:
             return render(request, 'login.html', {
             'incorrect_login': True
         })
     else:
         return HttpResponseBadRequest()

#LOGOUT 
@login_required(login_url='/login') 
def logout_view(request):
    logout(request)    
    return HttpResponseRedirect('/')


@login_required(login_url='/login') 
@has_permission_decorator('cadastrar_alunos')
def cadastro_aluno(request):
    if request.method == 'GET':
        turmas = Turma.objects.all()
        return render(request, 'cadastro_aluno.html', {
            'turmas' : turmas,
            'cpf_igual': False,
            'email_igual': False,
            'TelCelular_igual' : False,
        })
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        matricula = random.randint(10000000, 99999999)
        auth_matricula = CustomUser.objects.filter(matricula=matricula)
        if auth_matricula:
           while True:
                matricula = random.randint(10000000, 99999999)
                if not CustomUser.objects.filter(matricula=matricula):
                    return matricula
        email = request.POST.get('email')
        genero = request.POST.get('genero')
        TelCelular = request.POST.get('TelCelular')
        dtNascimento = request.POST.get('dtNascimento')
        cpf = request.POST.get('cpf')       
        turma_aluno = request.POST.get('turma_aluno')
        str_matricula = str(matricula)
        password = str_matricula
        cpf_auth = CustomUser.objects.filter(cpf=cpf)
        email_auth = CustomUser.objects.filter(email=email)
        TelCelular_auth = CustomUser.objects.filter(TelCelular=TelCelular)
        if TelCelular_auth:
            return render(request, 'cadastro_aluno.html', {
                'TelCelular_igual': True,
        })
        if email_auth:
            return render(request, 'cadastro_aluno.html', {
                'email_igual': True,
        })
        if cpf_auth:
            return render(request, 'cadastro_aluno.html', {
                'cpf_igual': True,
        })
        user = CustomUser.objects.create_user(username=first_name + ' ' + str_matricula , cpf=cpf, matricula=matricula)
        user.password = password
        user.genero=genero
        user.email=email
        user.TelCelular=TelCelular
        user.dtNascimento = dtNascimento
        user.first_name=first_name 
        user.last_name=last_name
        user.turma_aluno=turma_aluno
        user.set_password(user.password)
        user.save()
        assign_role(user, 'aluno')
        mensagem='Bem-Vindo(a), a ICA Gestão Acadêmica, segue link para acessar o site http://127.0.0.1:8000. '
        send_mail('Cadastro realizado - ICA Gestão Acadêmica',mensagem,config('EMAIL_HOST_USER'),recipient_list=[email])
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseBadRequest()

@login_required(login_url='/login') 
@has_permission_decorator('cadastrar_professores')
def cadastro_professor(request):
    if request.method == 'GET':
        disciplinas = Disciplina.objects.all()
        return render(request, 'cadastro_professor.html', {
            'disciplinas' : disciplinas,
            'cpf_igual': False,
            'email_igual': False,
            'TelCelular_igual' : False,
        })
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        matricula = random.randint(10000000, 99999999)
        auth_matricula = CustomUser.objects.filter(matricula=matricula)
        if auth_matricula:
           while True:
                matricula = random.randint(10000000, 99999999)
                if not CustomUser.objects.filter(matricula=matricula):
                    return matricula
        email = request.POST.get('email')
        genero = request.POST.get('genero')
        TelCelular = request.POST.get('TelCelular')
        dtNascimento = request.POST.get('dtNascimento')
        cpf = request.POST.get('cpf')       
        contrato = request.POST.get('contrato')
        disciplina = request.POST.get('disciplina_professor')
        disciplina_professor = Disciplina.objects.get(pk=disciplina)
        str_matricula = str(matricula)
        password = str_matricula
        cpf_auth = CustomUser.objects.filter(cpf=cpf)
        email_auth = CustomUser.objects.filter(email=email)
        TelCelular_auth = CustomUser.objects.filter(TelCelular=TelCelular)
        if TelCelular_auth:
            return render(request, 'cadastro_aluno.html', {
                'TelCelular_igual': True,
        })
        if email_auth:
            return render(request, 'cadastro_aluno.html', {
                'email_igual': True,
        })
        if cpf_auth:
            return render(request, 'cadastro_aluno.html', {
                'cpf_igual': True,
        })
        user = CustomUser.objects.create_user(username=first_name + ' ' + str_matricula , cpf=cpf, matricula=matricula)
        user.disciplina_professor=disciplina_professor
        user.password = password
        user.genero=genero
        user.email=email
        user.TelCelular=TelCelular
        user.dtNascimento = dtNascimento
        user.first_name=first_name
        user.last_name=last_name
        user.contrato=contrato
        user.set_password(user.password)
        user.save()
        assign_role(user, 'professor')
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseBadRequest
    
@login_required(login_url='/login') 
@has_role_decorator('diretor')
def cadastro_coordenador(request):
    if request.method == 'GET':
        return render(request, 'cadastro_coordenador.html', {
            'cpf_igual': False,
            'email_igual': False,
            'TelCelular_igual' : False,
        })
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        matricula = random.randint(10000000, 99999999)
        auth_matricula = CustomUser.objects.filter(matricula=matricula)
        if auth_matricula:
           while True:
                matricula = random.randint(10000000, 99999999)
                if not CustomUser.objects.filter(matricula=matricula):
                    return matricula
        email = request.POST.get('email')
        genero = request.POST.get('genero')
        TelCelular = request.POST.get('TelCelular')
        dtNascimento = request.POST.get('dtNascimento')
        cpf = request.POST.get('cpf')       
        contrato = request.POST.get('contrato')
        disciplina_professor = request.POST.get('disciplina_professor')
        str_matricula = str(matricula)
        password = str_matricula
        cpf_auth = CustomUser.objects.filter(cpf=cpf)
        email_auth = CustomUser.objects.filter(email=email)
        TelCelular_auth = CustomUser.objects.filter(TelCelular=TelCelular)
        if TelCelular_auth:
            return render(request, 'cadastro_aluno.html', {
                'TelCelular_igual': True,
        })
        if email_auth:
            return render(request, 'cadastro_aluno.html', {
                'email_igual': True,
        })
        if cpf_auth:
            return render(request, 'cadastro_aluno.html', {
                'cpf_igual': True,
        })
        user = CustomUser.objects.create_user(username=first_name + ' ' + str_matricula , cpf=cpf, matricula=matricula)
        user.disciplina_professor=disciplina_professor
        user.password = password
        user.genero=genero
        user.email=email
        user.TelCelular=TelCelular
        user.dtNascimento = dtNascimento
        user.first_name=first_name
        user.last_name=last_name
        user.contrato=contrato
        user.set_password(user.password)
        user.save()

        assign_role(user, 'coordenador')
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseBadRequest


@login_required(login_url='/login') 
@has_role_decorator('diretor') 
def cadastro_curso(request):
    if request.method == 'GET':
        return render(request, 'cadastro_curso.html',{
            'nome_igual': False,
        })
    elif request.method == 'POST':
        nome_curso = request.POST.get('nome_curso')
        duracao_curso = request.POST.get('duracao_curso')
        categoria_curso = request.POST.get('categoria_curso')
        area_curso = request.POST.get('area_curso')
        nome_curso_auth = Graduacao.objects.filter(nome_curso=nome_curso)
        if nome_curso_auth:
            return render(request, 'cadastro_curso.html', {
                'nome_igual': True,
        })
        curso = Graduacao()
        curso.nome_curso = nome_curso
        curso.duracao_curso = duracao_curso
        curso.area_curso = area_curso
        curso.categoria_curso = categoria_curso  
        curso.save()
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseBadRequest

@login_required(login_url='/login') 
@has_role_decorator('diretor') 
def cadastro_disciplina(request):
    cursos = Graduacao.objects.all()
    if request.method == 'GET':
        return render(request, 'cadastro_disciplina.html', {
            'cursos':cursos,
            'graduacao_valida': False,
            'nome_igual': False,
        })
    elif request.method == 'POST':
        nome_disciplina = request.POST.get('nome_disciplina')
        duracao_disciplina = request.POST.get('duracao_disciplina')
        graduacao = request.POST.get('graduacao_disciplina')
        nome_disciplina_auth = Disciplina.objects.filter(nome_disciplina=nome_disciplina)
        if nome_disciplina_auth:
            return render(request, 'cadastro_disciplina.html', {
                'nome_igual': True,
        })
        if graduacao == 'Escolha um Curso de Graduação':
            return render(request, 'cadastro_disciplina.html', {
                'graduacao_valida': True,
        })
        graduacao_disciplina= Graduacao.objects.get(pk=graduacao)
        disci = Disciplina()
        disci.nome_disciplina = nome_disciplina
        disci.duracao_disciplina = duracao_disciplina
        disci.graduacao_disciplina = graduacao_disciplina
        disci.save()
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect

@login_required(login_url='/login') 
@has_permission_decorator('cadastrar_turma')
def cadastro_turma(request):
    cursos = Graduacao.objects.all()
    if request.method == 'GET':
        return render(request, 'cadastro_turma.html', {
            'cursos' : cursos
        })
    elif request.method == 'POST':
        nome_turma = request.POST.get('nome_turma')
        turno_turma = request.POST.get('turno_turma')
        semestre_turma = request.POST.get('semestre_turma')
        graduacao = request.POST.get('graduacao_turma')
        graduacao_turma = Graduacao.objects.get(pk=graduacao)
        turma_cd = Turma()
        turma_cd.nome_turma = nome_turma
        turma_cd.turno_turma = turno_turma
        turma_cd.semestre_turma = semestre_turma
        turma_cd.graduacao_turma = graduacao_turma
        turma_cd.save()
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect   


@login_required(login_url='/login') 
@has_role_decorator('professor')
def cadastro_falta(request):
    if request.method == 'GET':
        matriculas = CustomUser.objects.filter(groups__name='aluno').all()
        disciplinas = Disciplina.objects.all()
        return render(request, 'cadastro_falta.html',{
            'matriculas' : matriculas,
            'disciplinas' : disciplinas,
            'disciplina_valida': False,
        })

    elif request.method == 'POST':
        aluno_matricula = request.POST.get('aluno_matricula')
        aluno_disciplina = request.POST.get('aluno_disciplina')
        aluno_falta_ent = request.POST.get('aluno_falta')
        if aluno_disciplina == 'Escolha uma Disciplina':
            return render(request, 'cadastro_falta.html', {
                'disciplina_valida': True,
        })
        auth_matricula = Estatistica.objects.filter(aluno_matricula=aluno_matricula, aluno_disciplina=aluno_disciplina)
        if auth_matricula:
            ests_falta = Estatistica.objects.filter(aluno_matricula=aluno_matricula, aluno_disciplina=aluno_disciplina).get()
            aluno_falta = F('aluno_falta') + aluno_falta_ent
            ests_falta.aluno_falta = aluno_falta
            ests_falta.save()
        elif not auth_matricula:
            ests = Estatistica()
            ests.aluno_matricula = aluno_matricula
            ests.aluno_disciplina = aluno_disciplina
            ests.aluno_falta = aluno_falta_ent
            ests.save()
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect   


@login_required(login_url='/login') 
@has_role_decorator('professor')
def cadastro_notas(request):
    if request.method == 'GET':
        matriculas = CustomUser.objects.filter(groups__name='aluno').all()
        disciplinas = Disciplina.objects.all()
        return render(request, 'cadastro_notas.html',{
            'matriculas' : matriculas,
            'disciplinas' : disciplinas
        })

    elif request.method == 'POST':
        matricula = request.POST.get('aluno_matricula')
        aluno_matricula = CustomUser.objects.get(pk=matricula)
        disciplina = request.POST.get('aluno_disciplina')
        aluno_disciplina = Disciplina.objects.get(pk=disciplina)
        nota_pb1 = request.POST.get('nota_pb1')
        nota_pb1_ent = float(nota_pb1)
        nota_pb2 = request.POST.get('nota_pb2')
        nota_pb2_ent = float(nota_pb2)
        nota_atv1 = request.POST.get('nota_atv1')
        nota_atv1_ent = float(nota_atv1)
        nota_atv2 = request.POST.get('nota_atv2')
        nota_atv2_ent = float(nota_atv2)
        nota_atv3 = request.POST.get('nota_atv3')
        nota_atv3_ent = float(nota_atv3)
        nota_atv4 = request.POST.get('nota_atv4')
        nota_atv4_ent = float(nota_atv4)
        auth_matricula = Estatistica.objects.filter(aluno_matricula=aluno_matricula, aluno_disciplina=aluno_disciplina)
        if auth_matricula:
            ests_nota = Estatistica.objects.filter(aluno_matricula=aluno_matricula, aluno_disciplina=aluno_disciplina).get()
            ests_nota.aluno_disciplina = aluno_disciplina
            ests_nota.aluno_matricula = aluno_matricula
            ests_nota.nota_atv1 = nota_atv1_ent
            ests_nota.nota_atv2 = nota_atv2_ent
            ests_nota.nota_pb1 = nota_pb1_ent
            ests_nota.nota_atv3 = nota_atv3_ent
            ests_nota.nota_atv4 = nota_atv4_ent
            ests_nota.nota_pb2 = nota_pb2_ent
            media1 = (nota_pb1_ent + (nota_atv1_ent + nota_atv2_ent) ) / 2
            media2 = (nota_pb2_ent + (nota_atv3_ent + nota_atv4_ent) ) / 2
            ests_nota.media_bm1 = media1
            ests_nota.media_bm2 = media2
            media_semestral = (media1 + media2 ) / 2
            ests_nota.media_sm = media_semestral
            if media_semestral >= 7:
                ests_nota.situação_sm = 'Aprovado'
            else:
                ests_nota.situação_sm = 'Reprovado'
            ests_nota.save()

        elif not auth_matricula:
            matricula = request.POST.get('aluno_matricula')
            aluno_matricula = CustomUser.objects.get(pk=matricula)
            disciplina = request.POST.get('aluno_disciplina')
            aluno_disciplina = Disciplina.objects.get(pk=disciplina)
            ests = Estatistica()
            ests.aluno_matricula = aluno_matricula
            ests.aluno_disciplina = aluno_disciplina
            ests.nota_atv1 = nota_atv1_ent
            ests.nota_atv2 = nota_atv2_ent
            ests.nota_pb1 = nota_pb1_ent
            ests.nota_atv3 = nota_atv3_ent
            ests.nota_atv4 = nota_atv4_ent
            ests.nota_pb2 = nota_pb2_ent
            media1 = (nota_pb1_ent + (nota_atv1_ent + nota_atv2_ent) ) / 2
            media2 = (nota_pb2_ent + (nota_atv3_ent + nota_atv4_ent) ) / 2
            ests.media_bm1 = media1
            ests.media_bm2 = media2
            media_semestral = (media1 + media2 ) / 2
            ests.media_sm = media_semestral
            if media_semestral >= 7:
                ests.situação_sm = 'Aprovado'
            else:
                ests.situação_sm = 'Reprovado'
            ests.save()
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect
    
@login_required(login_url='/login') 
@has_role_decorator('professor')    
def cadastro_nota_final(request):
    if request.method == 'GET':
        matriculas = CustomUser.objects.filter(groups__name='aluno').all()
        disciplinas = Disciplina.objects.all()
        return render(request, 'cadastro_notas_final.html',{
            'matriculas' : matriculas,
            'disciplinas' : disciplinas
        })
    elif request.method == 'POST':
        matricula = request.POST.get('aluno_matricula')
        aluno_matricula = CustomUser.objects.get(pk=matricula)
        disciplina = request.POST.get('aluno_disciplina')
        aluno_disciplina = Disciplina.objects.get(pk=disciplina)
        ests_nota = Estatistica.objects.filter(aluno_matricula=aluno_matricula, aluno_disciplina=aluno_disciplina).get()
        nota_pf = request.POST.get('nota_pf')
        nota_pf_ent = float(nota_pf)
        semestral = request.POST.get('media_semestral')
        media_semestral = float(semestral)
        ests_nota.aluno_disciplina = aluno_disciplina
        ests_nota.aluno_matricula = aluno_matricula
        ests_nota.nota_pf = nota_pf_ent
        media_final = (media_semestral + nota_pf_ent) / 2
        ests_nota.media_fn = media_final
        if media_final >= 7:
            ests_nota.situação_fn = 'Aprovado'
        else:
            ests_nota.situação_fn = 'Reprovado'
        ests_nota.save()
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect
    
@login_required(login_url='/login') 
@has_permission_decorator('ver_alunos')
def info_alunos(request):
    info_alunos = CustomUser.objects.filter(groups__name='aluno').all()
    turmas = Turma.objects.all()
    return render(request, 'cadastro_aluno_extra.html', {
         'info_alunos' : info_alunos,
         'turmas' : turmas,
     })

@login_required(login_url='/login') 
@has_permission_decorator('ver_professores_disciplinas')
def info_professores(request):
    info_professores = CustomUser.objects.filter(groups__name='professor').all()
    disciplinas = Disciplina.objects.all()
    return render(request, 'disciplinas_professores.html', {
         'info_professores' : info_professores,
         'disciplinas' : disciplinas,
     })

@login_required(login_url='/login') 
def info_perfil(request):
    turmas = Turma.objects.all()
    return render(request, 'perfil.html',{
        'turmas': turmas
    })

@login_required(login_url='/login') 
def info_cursos(request):
    mat = request.user.matricula
    turma = request.user.turma_aluno
    turmas = Turma.objects.filter(id_turma=turma)
    cursos = Graduacao.objects.filter(id_curso=turma)
    return render(request, 'informações_curso.html',{
        'turmas': turmas,
        'cursos':cursos
    })
        
@login_required(login_url='/login') 
def notas_faltas(request):
    matricula = request.user.matricula
    turma = request.user.turma_aluno
    estatisticas = Estatistica.objects.filter(aluno_matricula=matricula)
    turmas = Turma.objects.filter(pk=turma)
    return render(request, 'notas_faltas.html', {
        'estatisticas' : estatisticas,
        'turmas':turmas, 
    })