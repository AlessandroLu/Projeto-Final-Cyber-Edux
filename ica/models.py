from django.contrib.auth.models import AbstractUser
from rolepermissions.roles import assign_role
from django.db import models




#================================== GRADUAÇÃO ==============================================

class Graduacao(models.Model):

    CATEGORIA_CHOICES = (
        ('1', u'Bacharelado'),
        ('2', u'Licenciatura'),
        ('3', u'Tecnólogo'),
    )
        
    AREA_CHOICES = (
        ('1', u'Ciências Exatas e da Terra'),
        ('2', u'Ciências Biológicas'),
        ('3', u'Engenharias'),
        ('4', u'Ciências da Saúde'),
        ('5', u'Ciências Agrárias'),
        ('6', u'Ciências Humanas'),
        ('7', u'Linguística, Letras e Artes'),
        ('8', u'Ciências Sociais Aplicadas'),

    )
    id_curso = models.AutoField(primary_key=True)
    nome_curso = models.CharField(max_length=100)
    categoria_curso = models.CharField(max_length=1, choices=CATEGORIA_CHOICES)
    duracao_curso = models.CharField(max_length=50)
    area_curso = models.CharField(max_length=1, choices=AREA_CHOICES)


    
#================================== GRADUAÇÃO ==============================================

#================================== DISCIPLINA ==============================================
class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    nome_disciplina = models.CharField(max_length=80)
    duracao_disciplina =  models.CharField(max_length=20)
    graduacao_disciplina = models.ForeignKey(Graduacao, on_delete=models.SET_NULL, null = True)


#================================== DISCIPLINA ==============================================
    
#================================== TURMA ==============================================

class Turma(models.Model):
    TURNO_CHOICES = (
        ('1', u'Matutino'),
        ('2', u'Vespertino'),
        ('3', u'Noturno'),
    )

    SEMESTRE_CHOICES = (
        ('1', u'1° Semestre'),
        ('2', u'2° Semestre'),
        ('3', u'3° Semestre'),
        ('4', u'4° Semestre'),
        ('5', u'5° Semestre'),
        ('6', u'6° Semestre'),
        ('7', u'7° Semestre'),
        ('8', u'8° Semestre'),
        ('9', u'9° Semestre'),
        ('10', u'10° Semestre'),
        ('11', u'11° Semestre'),
        ('12', u'12° Semestre'),

    )
    id_turma = models.AutoField(primary_key=True)
    nome_turma = models.CharField(max_length=50)
    turno_turma = models.CharField(max_length=1, choices=TURNO_CHOICES)
    semestre_turma = models.CharField(max_length=2, choices=SEMESTRE_CHOICES)
    graduacao_turma = models.ForeignKey(Graduacao, on_delete=models.SET_NULL, null = True)




#================================== TURMA ==============================================
    
class CustomUser(AbstractUser):

    GENERO_CHOICES = (
        ('1', u'Masculino'),
        ('2', u'Feminino'),
        ('3', u'Outro'),
    )
    username = models.CharField(max_length=50, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True)
    TelCelular = models.CharField(max_length=16)
    dtNascimento = models.DateField(null=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    matricula = models.CharField(max_length=8, unique=True,primary_key=True)
    turma_aluno = models.CharField(max_length=2)
    disciplina_professor =  models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null = True)
    contrato = models.DateField(null=True, blank=True)

    

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'matricula']




#================================== ALUNO ESTATISTICAS ==============================================    


class Estatistica(models.Model):
    aluno_matricula = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    aluno_disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    aluno_falta = models.CharField(max_length=5)
    nota_pb1 = models.CharField(max_length=5,null=True, blank=True)
    nota_pb2 = models.CharField(max_length=5,null=True, blank=True)
    nota_pf = models.CharField(max_length=5, null=True, blank=True, default='-')
    nota_atv1 = models.CharField(max_length=5,null=True, blank=True)
    nota_atv2 = models.CharField(max_length=5,null=True, blank=True)
    nota_atv3 = models.CharField(max_length=5,null=True, blank=True)
    nota_atv4 = models.CharField(max_length=5,null=True, blank=True)
    media_bm1 = models.CharField(max_length=5,null=True, blank=True)
    media_bm2 = models.CharField(max_length=5,null=True, blank=True)
    media_sm = models.CharField(max_length=5,null=True, blank=True) 
    media_fn = models.CharField(max_length=5, null=True, blank=True, default='-' )
    situação_sm = models.CharField(max_length=20, null=True, blank=True)
    situação_fn = models.CharField(max_length=20, null=True, blank=True, default='-')


#================================== ALUNO ESTATISTICAS ==============================================

