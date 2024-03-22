from rolepermissions.roles import AbstractUserRole  


class Professor(AbstractUserRole):
    available_permissions = {'adicionar_notas':True, 'adicionar_ faltas':True, 'ver_alunos':True, 'ver_professores_disciplinas':True}

class Aluno(AbstractUserRole):
    available_permissions = {'ver_notas_faltas':True, 'ver_professores_disciplinas':True, 'ver_info_curso':True}

class Coordenador(AbstractUserRole):
    available_permissions = {'cadastrar_alunos':True, 'cadastrar_professores':True, 'ver_professores_disciplinas':True, 'ver_alunos':True, 'cadastrar_turma':True, 'cadastrar_disciplinas':True}

class Diretor(AbstractUserRole):
    available_permissions = {'cadastrar_alunos':True, 'cadastrar_professores':True, 'cadastrar_coordenador':True, 'ver_professores_disciplinas':True,'cadastar_cursos':True, 'cadastrar_disciplinas':True, 'cadastrar_turma':True}
    