import os
import sys
import django

# Setup django environment
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduschedule_backend.settings')
django.setup()

from core.models import (
    Shift, TimeSlot, Teacher, TeacherAvailability,
    Subject, SchoolClass, CurriculumRequirement, ConstraintConfig,
    TimetableSchedule, TimetableSlotAssignment
)
from solver.engine import TimetablingSolver


def seed_professor_eds(clear=True):
    print("Iniciando carga de dados oficial do professor (EDS)...")

    if clear:
        print("Limpando dados anteriores...")
        TimetableSlotAssignment.objects.all().delete()
        TimetableSchedule.objects.all().delete()
        CurriculumRequirement.objects.all().delete()
        SchoolClass.objects.all().delete()
        TeacherAvailability.objects.all().delete()
        Teacher.objects.all().delete()
        Subject.objects.all().delete()
        TimeSlot.objects.all().delete()
        Shift.objects.all().delete()

    # 1. Turno e Slots (4 tempos diários x 5 dias)
    shift = Shift.objects.create(
        name="Matutino EDS",
        start_time="08:10:00",
        end_time="11:50:00",
        is_active=True
    )

    slots_info = [
        {"order": 1, "name": "1º Período", "start_time": "08:10:00", "end_time": "09:00:00"},
        {"order": 2, "name": "2º Período", "start_time": "09:00:00", "end_time": "09:50:00"},
        {"order": 3, "name": "3º Período", "start_time": "10:10:00", "end_time": "11:00:00"},
        {"order": 4, "name": "4º Período", "start_time": "11:00:00", "end_time": "11:50:00"},
    ]
    slots = []
    for s in slots_info:
        slot = TimeSlot.objects.create(
            shift=shift,
            order=s["order"],
            name=s["name"],
            start_time=s["start_time"],
            end_time=s["end_time"],
            duration_minutes=50,
            is_break=False,
            allow_double_lesson=True
        )
        slots.append(slot)
    print(f"[OK] Turno '{shift.name}' e {len(slots)} slots cadastrados.")

    # 2. Turmas
    turmas_data = [
        {"name": "Segundo período de EDS", "grade_level": "2º Período - Engenharia de Software"},
        {"name": "Quarto período de EDS", "grade_level": "4º Período - Engenharia de Software"},
        {"name": "Sexto período de EDS", "grade_level": "6º Período - Engenharia de Software"},
    ]
    turmas_dict = {}
    for t_data in turmas_data:
        turma = SchoolClass.objects.create(
            name=t_data["name"],
            grade_level=t_data["grade_level"],
            shift=shift,
            student_count=35
        )
        turmas_dict[turma.name] = turma
    print(f"[OK] {len(turmas_dict)} turmas cadastradas.")

    # 3. Professores e Disponibilidades
    professores_data = [
        ("João", "Jão", "#1D4ED8", "joao.eds@ugb.edu.br"),
        ("Maria", "Maria", "#BE123C", "maria.eds@ugb.edu.br"),
        ("Iná", "Iná", "#6D28D9", "ina.eds@ugb.edu.br"),
        ("Diana", "Diana", "#0F766E", "diana.eds@ugb.edu.br"),
        ("Ana", "Ana", "#B45309", "ana.eds@ugb.edu.br"),
        ("Sebastião", "Tião", "#4338CA", "sebastiao.eds@ugb.edu.br"),
        ("Mara", "Mara", "#15803D", "mara.eds@ugb.edu.br"),
        ("Carolina", "Carol", "#DB2777", "carolina.eds@ugb.edu.br"),
        ("Lucas", "Lucas", "#0891B2", "lucas.eds@ugb.edu.br"),
        ("Antônio João", "Antônio", "#EA580C", "antonio.eds@ugb.edu.br"),
    ]

    prof_dict = {}
    for i, (nome, apelido, color, email) in enumerate(professores_data):
        prof = Teacher.objects.create(
            name=nome,
            email=email,
            avatar_initials=apelido[:2].upper(),
            color=color,
            max_weekly_hours=20,
            max_daily_hours=4,
            allow_double_lessons=True,
            is_active=True
        )
        prof_dict[nome] = prof

        # Regra de disponibilidade do professor:
        # i < 3: apenas Segunda-feira (dia 0)
        # i < 6: Segunda e Terça (dias 0 e 1)
        # demais: todos os dias (0 a 4)
        if i < 3:
            available_days = {0}
        elif i < 6:
            available_days = {0, 1}
        else:
            available_days = {0, 1, 2, 3, 4}

        avail_objs = []
        for d in range(5):
            for s in slots:
                st = 'FREE' if d in available_days else 'BLOCKED'
                avail_objs.append(TeacherAvailability(
                    teacher=prof,
                    day_of_week=d,
                    time_slot=s,
                    status=st
                ))
        TeacherAvailability.objects.bulk_create(avail_objs)
    print(f"[OK] {len(prof_dict)} professores cadastrados com matriz de disponibilidade.")

    # 4. Disciplinas
    disciplinas_data = [
        ("Algebra Linear", "ALG", "#3B82F6"),
        ("Atividades Práticas MA", "APMA", "#8B5CF6"),
        ("Física Experimental", "FIS", "#F43F5E"),
        ("Inglês", "ING", "#06B6D4"),
        ("Linguagem de Programação I", "LPI", "#10B981"),
        ("Probabilidade e Estatística", "PEST", "#F59E0B"),
        ("Aptividades Práticas DH", "APDH", "#6366F1"),
        ("Complexidade de Algoritmos", "CALG", "#EC4899"),
        ("Desebvimento de Software - WEB", "DWEB", "#14B8A6"),
        ("Engenharia de Requisitos", "EREQ", "#D97706"),
        ("Gerenciamento de Banco de Dados", "GBD", "#F97316"),
        ("Sistemas Operacionais", "SOP", "#7C3AED"),
        ("Arquitetura de Microservições", "AMIC", "#4338CA"),
        ("Elaboração de Projeto Final", "EPF", "#BE123C"),
        ("Gerenciamento de Projetos", "GPRJ", "#1D4ED8"),
        ("Laboratório de Programação e Desenvolvimento", "LPD", "#15803D"),
        ("Melhores Práticas de Devops", "DVOP", "#0F766E"),
        ("Teste e Manutenção de Software", "TMS", "#DB2777"),
    ]

    disc_dict = {}
    for nome, sigla, color in disciplinas_data:
        disc = Subject.objects.create(
            name=nome,
            code=sigla,
            color=color,
            requires_lab=False
        )
        disc_dict[nome] = disc
    print(f"[OK] {len(disc_dict)} disciplinas cadastradas.")

    # 5. Demandas Curriculares (Alocações)
    alocacoes_data = [
        # Segundo período (20 aulas)
        ("Segundo período de EDS", "Algebra Linear", "João", 4),
        ("Segundo período de EDS", "Atividades Práticas MA", "Maria", 4),
        ("Segundo período de EDS", "Física Experimental", "Iná", 4),
        ("Segundo período de EDS", "Inglês", "Diana", 4),
        ("Segundo período de EDS", "Linguagem de Programação I", "Ana", 2),
        ("Segundo período de EDS", "Probabilidade e Estatística", "Sebastião", 2),

        # Quarto período (20 aulas)
        ("Quarto período de EDS", "Aptividades Práticas DH", "Mara", 4),
        ("Quarto período de EDS", "Complexidade de Algoritmos", "Carolina", 4),
        ("Quarto período de EDS", "Desebvimento de Software - WEB", "Lucas", 4),
        ("Quarto período de EDS", "Engenharia de Requisitos", "Antônio João", 4),
        ("Quarto período de EDS", "Gerenciamento de Banco de Dados", "João", 2),
        ("Quarto período de EDS", "Sistemas Operacionais", "Maria", 2),

        # Sexto período (20 aulas)
        ("Sexto período de EDS", "Arquitetura de Microservições", "Iná", 4),
        ("Sexto período de EDS", "Elaboração de Projeto Final", "Diana", 4),
        ("Sexto período de EDS", "Gerenciamento de Projetos", "Ana", 2),
        ("Sexto período de EDS", "Laboratório de Programação e Desenvolvimento", "Sebastião", 4),
        ("Sexto período de EDS", "Melhores Práticas de Devops", "Mara", 2),
        ("Sexto período de EDS", "Teste e Manutenção de Software", "Carolina", 2),
        ("Sexto período de EDS", "Algebra Linear", "João", 2),
    ]

    curric_objs = []
    for t_nome, d_nome, p_nome, qtd in alocacoes_data:
        curric_objs.append(CurriculumRequirement(
            school_class=turmas_dict[t_nome],
            subject=disc_dict[d_nome],
            teacher=prof_dict[p_nome],
            weekly_lessons=qtd,
            double_lessons_allowed=True
        ))
        disc_dict[d_nome].teachers.add(prof_dict[p_nome])
    CurriculumRequirement.objects.bulk_create(curric_objs)
    print(f"[OK] {len(curric_objs)} demandas curriculares cadastradas.")

    # 6. Configurações de Restrições
    constraints = [
        {'name': 'Sem choque de professor', 'key': 'teacher_clash', 'is_hard': True, 'weight': 100, 'description': 'Inviolável: 1 professor em apenas 1 turma simultânea'},
        {'name': 'Indisponibilidade do docente', 'key': 'teacher_blocked', 'is_hard': True, 'weight': 100, 'description': 'Respeitar dias bloqueados pelo professor'},
        {'name': 'Minimizar janelas vagas', 'key': 'min_gap_weight', 'is_hard': False, 'weight': 85, 'description': 'Penaliza horários ociosos entre aulas do docente'},
        {'name': 'Agrupamento de aulas geminadas', 'key': 'double_lesson_weight', 'is_hard': False, 'weight': 90, 'description': 'Favorece blocos contínuos de 2 aulas'},
        {'name': 'Distribuição homogênea semanal', 'key': 'daily_balance_weight', 'is_hard': False, 'weight': 70, 'description': 'Equilibra matérias durante a semana'},
        {'name': 'Concentração de dias de trabalho', 'key': 'day_concentration_weight', 'is_hard': False, 'weight': 60, 'description': 'Reduz dias de deslocamento do docente'},
    ]
    for c in constraints:
        ConstraintConfig.objects.update_or_create(key=c['key'], defaults=c)

    # 7. Executa o Solver
    print("\nExecutando o motor de otimização (Simulated Annealing)...")
    solver = TimetablingSolver(schedule_name="Grade Oficial EDS 2026.1", semester="1º Semestre 2026")
    res = solver.solve()
    print(f"[SUCESSO] Grade gerada!")
    print(f"  - Viabilidade: {res.get('viability_score')}%")
    print(f"  - Conflitos Rígidos: {res.get('hard_violations')}")
    print(f"  - Penalidades Suaves: {res.get('soft_penalties')}")
    print(f"  - Tempo de Execução: {res.get('execution_time')}s")
    print(f"  - Total de Aulas Alocadas: {res.get('total_assignments')}")
    if res.get('hard_details'):
        print(f"  - Detalhes Hard: {res.get('hard_details')[:5]}")
    return res


if __name__ == '__main__':
    seed_professor_eds()
