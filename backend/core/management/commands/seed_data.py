import sys
from django.core.management.base import BaseCommand
from core.seeds import seed_professor_eds
from core.models import (
    Shift, TimeSlot, Subject, Teacher, TeacherAvailability,
    SchoolClass, CurriculumRequirement, ConstraintConfig,
    TimetableSchedule, TimetableSlotAssignment
)


class Command(BaseCommand):
    help = "Popula o banco de dados com dados iniciais. Suporta o cenário oficial de EDS do professor ou Ensino Médio."

    def add_arguments(self, parser):
        parser.add_argument(
            '--scenario',
            type=str,
            default='eds',
            choices=['eds', 'medio'],
            help="Cenário de seed: 'eds' (Oficial do Professor - Graduação EDS) ou 'medio' (Ensino Médio)",
        )
        parser.add_argument(
            '--with-solver',
            action='store_true',
            help='Executa o solver após o seed para gerar a grade inicial alocada.',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            default=True,
            help='Limpa dados anteriores antes do seed.',
        )

    def handle(self, *args, **options):
        scenario = options.get('scenario', 'eds')

        if scenario == 'eds':
            self.stdout.write(self.style.NOTICE("Executando seed oficial do professor: Graduação em Engenharia de Software (EDS)..."))
            res = seed_professor_eds(clear=options.get('clear', True))
            self.stdout.write(self.style.SUCCESS(f"\n[SUCESSO] Base de EDS populada com sucesso!"))
            return

        # Cenário Ensino Médio
        self.stdout.write(self.style.NOTICE("Executando seed: Ensino Médio (3º Ano A e B)..."))
        if options.get('clear', True):
            TimetableSlotAssignment.objects.all().delete()
            TimetableSchedule.objects.all().delete()
            CurriculumRequirement.objects.all().delete()
            SchoolClass.objects.all().delete()
            TeacherAvailability.objects.all().delete()
            Teacher.objects.all().delete()
            Subject.objects.all().delete()
            TimeSlot.objects.all().delete()
            Shift.objects.all().delete()

        # 1. Turno Padrão & Slots de Tempo
        shift, _ = Shift.objects.get_or_create(
            name="Matutino",
            defaults={'start_time': '07:15:00', 'end_time': '12:00:00'}
        )

        slots_data = [
            {'order': 1, 'name': '1º Período', 'start_time': '07:15:00', 'end_time': '08:05:00', 'duration_minutes': 50, 'is_break': False},
            {'order': 2, 'name': '2º Período', 'start_time': '08:05:00', 'end_time': '08:55:00', 'duration_minutes': 50, 'is_break': False},
            {'order': 3, 'name': 'Intervalo / Recreio', 'start_time': '08:55:00', 'end_time': '09:15:00', 'duration_minutes': 20, 'is_break': True},
            {'order': 4, 'name': '3º Período', 'start_time': '09:15:00', 'end_time': '10:05:00', 'duration_minutes': 50, 'is_break': False},
            {'order': 5, 'name': '4º Período', 'start_time': '10:05:00', 'end_time': '10:55:00', 'duration_minutes': 50, 'is_break': False},
            {'order': 6, 'name': '5º Período', 'start_time': '10:55:00', 'end_time': '11:45:00', 'duration_minutes': 50, 'is_break': False},
        ]
        created_slots = []
        for s in slots_data:
            slot, _ = TimeSlot.objects.update_or_create(
                shift=shift, order=s['order'],
                defaults=s
            )
            created_slots.append(slot)

        # 2. Disciplinas
        subjects_data = [
            {'name': 'Matematica I & II', 'code': 'MAT', 'color': '#3B82F6', 'requires_lab': False},
            {'name': 'Fisica', 'code': 'FIS', 'color': '#8B5CF6', 'requires_lab': True},
            {'name': 'Quimica Organica & Geral', 'code': 'QUI', 'color': '#F43F5E', 'requires_lab': True},
            {'name': 'Biologia', 'code': 'BIO', 'color': '#10B981', 'requires_lab': True},
            {'name': 'Lingua Portuguesa & Literatura', 'code': 'POR', 'color': '#6366F1', 'requires_lab': False},
            {'name': 'Historia', 'code': 'HIS', 'color': '#F59E0B', 'requires_lab': False},
            {'name': 'Geografia', 'code': 'GEO', 'color': '#D97706', 'requires_lab': False},
            {'name': 'Ingles Instrumental', 'code': 'ING', 'color': '#06B6D4', 'requires_lab': False},
            {'name': 'Educacao Fisica', 'code': 'EDF', 'color': '#F97316', 'requires_lab': False},
            {'name': 'Sociologia', 'code': 'SOC', 'color': '#EC4899', 'requires_lab': False},
            {'name': 'Filosofia', 'code': 'FIL', 'color': '#14B8A6', 'requires_lab': False},
            {'name': 'Artes Visuais', 'code': 'ART', 'color': '#A855F7', 'requires_lab': False},
        ]
        created_subjects = {}
        for s in subjects_data:
            subj, _ = Subject.objects.update_or_create(code=s['code'], defaults=s)
            created_subjects[s['code']] = subj

        # 3. Professores
        teachers_data = [
            {'name': 'Prof. Roberto Silva', 'email': 'roberto.silva@escola.edu.br', 'avatar_initials': 'RS', 'color': '#1D4ED8', 'max_weekly_hours': 20},
            {'name': 'Profª. Mariana Costa', 'email': 'mariana.costa@escola.edu.br', 'avatar_initials': 'MC', 'color': '#6D28D9', 'max_weekly_hours': 16},
            {'name': 'Prof. Carlos Eduardo', 'email': 'carlos.eduardo@escola.edu.br', 'avatar_initials': 'CE', 'color': '#BE123C', 'max_weekly_hours': 14},
            {'name': 'Profª. Beatriz Lima', 'email': 'beatriz.lima@escola.edu.br', 'avatar_initials': 'BL', 'color': '#4338CA', 'max_weekly_hours': 22},
            {'name': 'Profª. Aline Mendes', 'email': 'aline.mendes@escola.edu.br', 'avatar_initials': 'AM', 'color': '#15803D', 'max_weekly_hours': 18},
            {'name': 'Prof. Fernando Dias', 'email': 'fernando.dias@escola.edu.br', 'avatar_initials': 'FD', 'color': '#B45309', 'max_weekly_hours': 16},
            {'name': 'Prof. Lucas Ribeiro', 'email': 'lucas.ribeiro@escola.edu.br', 'avatar_initials': 'LR', 'color': '#0F766E', 'max_weekly_hours': 12},
            {'name': 'Profª. Julia Smith', 'email': 'julia.smith@escola.edu.br', 'avatar_initials': 'JS', 'color': '#0891B2', 'max_weekly_hours': 10},
            {'name': 'Prof. Marcos Paulo', 'email': 'marcos.paulo@escola.edu.br', 'avatar_initials': 'MP', 'color': '#EA580C', 'max_weekly_hours': 10},
            {'name': 'Profª. Helena Ramos', 'email': 'helena.ramos@escola.edu.br', 'avatar_initials': 'HR', 'color': '#DB2777', 'max_weekly_hours': 12},
            {'name': 'Profª. Laura Meireles', 'email': 'laura.meireles@escola.edu.br', 'avatar_initials': 'LM', 'color': '#7C3AED', 'max_weekly_hours': 8},
        ]
        created_teachers = {}
        for t in teachers_data:
            teacher, _ = Teacher.objects.update_or_create(email=t['email'], defaults=t)
            created_teachers[t['name']] = teacher

        # 4. Disponibilidade Docente
        non_break_slots = [s for s in created_slots if not s.is_break]
        for teacher in created_teachers.values():
            for d in range(5):
                for s in non_break_slots:
                    st = 'FREE'
                    if teacher.name == 'Prof. Roberto Silva' and d == 4:
                        st = 'BLOCKED'
                    elif teacher.name == 'Prof. Roberto Silva' and (d == 0 or d == 2):
                        st = 'PREFERENTIAL'
                    TeacherAvailability.objects.update_or_create(
                        teacher=teacher, day_of_week=d, time_slot=s,
                        defaults={'status': st}
                    )

        # 5. Turmas
        c3a, _ = SchoolClass.objects.update_or_create(
            name="3º Ano A",
            defaults={'grade_level': '3º Ano Ensino Médio', 'shift': shift, 'student_count': 35}
        )
        c3b, _ = SchoolClass.objects.update_or_create(
            name="3º Ano B",
            defaults={'grade_level': '3º Ano Ensino Médio', 'shift': shift, 'student_count': 32}
        )

        # 6. Demandas Curriculares (3º Ano A)
        curric_3a = [
            (created_subjects['MAT'], created_teachers['Prof. Roberto Silva'], 4),
            (created_subjects['FIS'], created_teachers['Profª. Mariana Costa'], 3),
            (created_subjects['QUI'], created_teachers['Prof. Carlos Eduardo'], 3),
            (created_subjects['BIO'], created_teachers['Profª. Aline Mendes'], 3),
            (created_subjects['POR'], created_teachers['Profª. Beatriz Lima'], 4),
            (created_subjects['HIS'], created_teachers['Prof. Fernando Dias'], 2),
            (created_subjects['GEO'], created_teachers['Prof. Lucas Ribeiro'], 2),
            (created_subjects['ING'], created_teachers['Profª. Julia Smith'], 1),
            (created_subjects['EDF'], created_teachers['Prof. Marcos Paulo'], 1),
            (created_subjects['SOC'], created_teachers['Profª. Helena Ramos'], 1),
            (created_subjects['ART'], created_teachers['Profª. Laura Meireles'], 1),
        ]
        for subj, teach, hours in curric_3a:
            CurriculumRequirement.objects.update_or_create(
                school_class=c3a, subject=subj,
                defaults={'teacher': teach, 'weekly_lessons': hours, 'double_lessons_allowed': True}
            )

        # 7. Restrições
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

        # 8. Solver Opcional
        if options.get('with_solver'):
            from solver.engine import TimetablingSolver
            solver = TimetablingSolver(schedule_name="Grade Oficial 2026.1", semester="1º Semestre 2026")
            solver.solve()

        self.stdout.write(self.style.SUCCESS("\nSeed concluído com sucesso!"))
