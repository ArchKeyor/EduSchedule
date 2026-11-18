from django.test import TestCase
from rest_framework.test import APIClient
from core.models import (
    Shift, TimeSlot, Teacher, Subject, SchoolClass, CurriculumRequirement,
    TimetableSlotAssignment
)
from solver.engine import TimetablingSolver


class TimeSlotAndSubjectTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.shift = Shift.objects.create(name="Matutino", start_time="07:15:00", end_time="12:00:00")
        self.slot1 = TimeSlot.objects.create(
            shift=self.shift, order=1, name="1º Período",
            start_time="07:15:00", end_time="08:05:00", duration_minutes=50
        )
        self.slot2 = TimeSlot.objects.create(
            shift=self.shift, order=2, name="2º Período",
            start_time="08:05:00", end_time="08:55:00", duration_minutes=50
        )
        self.teacher1 = Teacher.objects.create(name="Prof. Roberto", email="roberto@escola.edu.br")
        self.teacher2 = Teacher.objects.create(name="Profª. Mariana", email="mariana@escola.edu.br")

    def test_reorder_slots_updates_order_atomically(self):
        # Arrange
        payload = {'slot_ids': [self.slot2.id, self.slot1.id]}

        # Act
        response = self.client.post('/api/slots/reorder/', payload, format='json')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.slot1.refresh_from_db()
        self.slot2.refresh_from_db()
        self.assertEqual(self.slot2.order, 1)
        self.assertEqual(self.slot1.order, 2)

    def test_subject_connects_multiple_teachers(self):
        # Arrange
        payload = {
            'name': 'Matemática Aplicada',
            'code': 'MAT',
            'color': '#3B82F6',
            'requires_lab': False,
            'teachers': [self.teacher1.id, self.teacher2.id],
        }

        # Act
        response = self.client.post('/api/subjects/', payload, format='json')

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(set(response.data['teachers']), {self.teacher1.id, self.teacher2.id})
        self.assertEqual(len(response.data['teacher_details']), 2)


class MultiShiftSolverTests(TestCase):
    def setUp(self):
        self.morning = Shift.objects.create(name="Matutino", start_time="07:15:00", end_time="11:45:00")
        self.afternoon = Shift.objects.create(name="Vespertino", start_time="13:00:00", end_time="17:30:00")

        self.m_slot1 = TimeSlot.objects.create(
            shift=self.morning, order=1, name="1º Período M",
            start_time="07:15:00", end_time="08:05:00", duration_minutes=50
        )
        self.m_slot2 = TimeSlot.objects.create(
            shift=self.morning, order=2, name="2º Período M",
            start_time="08:05:00", end_time="08:55:00", duration_minutes=50
        )
        self.a_slot1 = TimeSlot.objects.create(
            shift=self.afternoon, order=1, name="1º Período V",
            start_time="13:00:00", end_time="13:50:00", duration_minutes=50
        )
        self.a_slot2 = TimeSlot.objects.create(
            shift=self.afternoon, order=2, name="2º Período V",
            start_time="13:50:00", end_time="14:40:00", duration_minutes=50
        )

        self.teacher = Teacher.objects.create(name="Prof. Carlos", email="carlos@escola.edu.br")
        self.subject = Subject.objects.create(name="Física", code="FIS")
        self.subject.teachers.add(self.teacher)

        self.class_a = SchoolClass.objects.create(name="3º Ano A", shift=self.morning)
        self.class_b = SchoolClass.objects.create(name="3º Ano B", shift=self.afternoon)

        CurriculumRequirement.objects.create(
            school_class=self.class_a, subject=self.subject, teacher=self.teacher, weekly_lessons=4
        )
        CurriculumRequirement.objects.create(
            school_class=self.class_b, subject=self.subject, teacher=self.teacher, weekly_lessons=4
        )

    def test_solver_allocates_all_classes_strictly_within_their_shift(self):
        # Arrange
        solver = TimetablingSolver(schedule_name="Teste Multi-Turno")

        # Act
        result = solver.solve()

        # Assert
        self.assertEqual(result['hard_violations'], 0)
        self.assertEqual(result['total_assignments'], 8)

        a_assignments = TimetableSlotAssignment.objects.filter(
            timetable_schedule_id=result['schedule_id'], school_class=self.class_a
        )
        b_assignments = TimetableSlotAssignment.objects.filter(
            timetable_schedule_id=result['schedule_id'], school_class=self.class_b
        )
        self.assertEqual(a_assignments.count(), 4)
        self.assertEqual(b_assignments.count(), 4)
        self.assertTrue(all(a.time_slot.shift_id == self.morning.id for a in a_assignments))
        self.assertTrue(all(a.time_slot.shift_id == self.afternoon.id for a in b_assignments))

    def test_break_slot_between_lessons_does_not_create_teacher_gap_warning(self):
        # Arrange: Matutino has 2º Período (order=2), Intervalo (order=3, is_break=True), 3º Período (order=4)
        from solver.constraints import ConstraintEvaluator
        evaluator = ConstraintEvaluator()
        assignments = [
            {
                'class_id': self.class_a.id, 'day': 4, 'slot_id': self.m_slot2.id,
                'slot_order': 2, 'regular_order': 2, 'shift_id': self.morning.id,
                'teacher_id': self.teacher.id, 'subject_id': self.subject.id,
            },
            {
                'class_id': self.class_b.id, 'day': 4, 'slot_id': 999,
                'slot_order': 4, 'regular_order': 3, 'shift_id': self.morning.id,
                'teacher_id': self.teacher.id, 'subject_id': self.subject.id,
            },
        ]

        # Act
        res = evaluator.evaluate_schedule(assignments, {}, teacher_names={self.teacher.id: self.teacher.name})

        # Assert
        self.assertEqual(res['soft_penalty'], 0)
        self.assertEqual(res['soft_details'], [])
