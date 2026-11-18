import time
import math
import random
from django.db import transaction
from .constraints import ConstraintEvaluator
from core.models import (
    SchoolClass, CurriculumRequirement, TimeSlot, Teacher, TeacherAvailability,
    TimetableSchedule, TimetableSlotAssignment, ConstraintConfig
)


class TimetablingSolver:
    def __init__(self, schedule_name="Grade Otimizada por IA", semester="1º Semestre 2026"):
        self.schedule_name = schedule_name
        self.semester = semester

        # Load constraint weights from DB
        weights = {}
        for cfg in ConstraintConfig.objects.filter(is_enabled=True):
            weights[cfg.key] = cfg.weight
        self.evaluator = ConstraintEvaluator(weights)

    @staticmethod
    def _has_teacher_clash(teacher_id, day, slot, teacher_day_slots, ignore_class_id=None):
        """Checks exact slot match or overlapping time intervals on the same day for a teacher."""
        for existing in teacher_day_slots.get((teacher_id, day), []):
            if ignore_class_id is not None and existing['class_id'] == ignore_class_id:
                continue
            if existing['slot_id'] == slot.id:
                return True
            if existing['start_time'] < slot.end_time and slot.start_time < existing['end_time']:
                return True
        return False

    @staticmethod
    def _build_assignment(class_id, day, slot, teacher_id, subject_id, regular_order):
        return {
            'class_id': class_id,
            'day': day,
            'slot_id': slot.id,
            'slot_order': slot.order,
            'regular_order': regular_order,
            'shift_id': slot.shift_id,
            'start_time': slot.start_time,
            'end_time': slot.end_time,
            'teacher_id': teacher_id,
            'subject_id': subject_id,
        }

    @staticmethod
    def _apply_slot(assignment, day, slot, regular_order):
        assignment['day'] = day
        assignment['slot_id'] = slot.id
        assignment['slot_order'] = slot.order
        assignment['regular_order'] = regular_order
        assignment['shift_id'] = slot.shift_id
        assignment['start_time'] = slot.start_time
        assignment['end_time'] = slot.end_time

    def solve(self):
        start_time = time.time()

        # 1. Fetch data
        classes = list(SchoolClass.objects.select_related('shift').all())
        curricula = list(CurriculumRequirement.objects.select_related('school_class', 'subject', 'teacher').all())
        teacher_names = {t.id: t.name for t in Teacher.objects.all()}

        # Fetch all slots and organize non-break slots & break orders per shift
        all_slots = list(TimeSlot.objects.all().order_by('shift_id', 'order', 'start_time'))
        slots_by_shift = {}
        breaks_by_shift = {}
        regular_order_by_slot = {}
        for s in all_slots:
            if s.is_break:
                breaks_by_shift.setdefault(s.shift_id, set()).add(s.order)
            else:
                shift_list = slots_by_shift.setdefault(s.shift_id, [])
                shift_list.append(s)
                regular_order_by_slot[s.id] = len(shift_list)

        # Fetch teacher availabilities: map (teacher_id, day, slot_id) -> status
        avail_qs = TeacherAvailability.objects.all()
        avail_map = {
            (a.teacher_id, a.day_of_week, a.time_slot_id): a.status
            for a in avail_qs
        }

        days = [0, 1, 2, 3, 4]  # Seg a Sex (0 a 4)

        # 2. Build list of lessons to allocate per class
        class_lessons = {c.id: [] for c in classes}
        for req in curricula:
            if req.school_class_id in class_lessons:
                for _ in range(req.weekly_lessons):
                    class_lessons[req.school_class_id].append({
                        'class_id': req.school_class_id,
                        'subject_id': req.subject_id,
                        'teacher_id': req.teacher_id,
                        'allow_double': req.double_lessons_allowed,
                    })

        # 3. Available grid coordinates per shift
        grid_by_shift = {
            shift_id: [(d, s) for d in days for s in s_list]
            for shift_id, s_list in slots_by_shift.items()
        }

        best_assignments = []
        best_eval = {'viability_score': -1, 'hard_violations': 9999, 'soft_penalty': 999999}

        # 4. Multi-restart constructive search + local repair across ALL classes
        max_attempts = 15
        for _ in range(max_attempts):
            current_assignments = []
            teacher_day_slots = {}  # (teacher_id, day) -> list of {class_id, slot_id, start_time, end_time}

            # Vary class order across attempts while prioritizing classes with more lessons
            shuffled_classes = list(classes)
            random.shuffle(shuffled_classes)
            shuffled_classes.sort(key=lambda cl: len(class_lessons[cl.id]), reverse=True)

            for c in shuffled_classes:
                lessons = list(class_lessons[c.id])
                c_slots = slots_by_shift.get(c.shift_id, [])
                if not lessons or not c_slots:
                    continue

                break_orders = breaks_by_shift.get(c.shift_id, set())
                class_grid = list(grid_by_shift.get(c.shift_id, []))
                random.shuffle(lessons)

                # Prioritize pairing double lessons
                paired_lessons = []
                by_subject = {}
                for l in lessons:
                    by_subject.setdefault(l['subject_id'], []).append(l)

                unpaired = []
                for s_lessons in by_subject.values():
                    while len(s_lessons) >= 2 and s_lessons[0]['allow_double']:
                        paired_lessons.append((s_lessons.pop(), s_lessons.pop()))
                    unpaired.extend(s_lessons)

                # Allocate pairs first (without crossing break slots)
                for l1, l2 in paired_lessons:
                    placed = False
                    shuffled_days = list(days)
                    random.shuffle(shuffled_days)
                    for d in shuffled_days:
                        for s_idx in range(len(c_slots) - 1):
                            s1 = c_slots[s_idx]
                            s2 = c_slots[s_idx + 1]

                            # Do not pair across a break interval
                            if any(s1.order < bo < s2.order for bo in break_orders):
                                continue

                            pos1_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s1.id for a in current_assignments)
                            pos2_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s2.id for a in current_assignments)

                            if not pos1_used and not pos2_used:
                                t1_free = (
                                    not self._has_teacher_clash(l1['teacher_id'], d, s1, teacher_day_slots)
                                    and avail_map.get((l1['teacher_id'], d, s1.id)) != 'BLOCKED'
                                )
                                t2_free = (
                                    not self._has_teacher_clash(l2['teacher_id'], d, s2, teacher_day_slots)
                                    and avail_map.get((l2['teacher_id'], d, s2.id)) != 'BLOCKED'
                                )

                                if t1_free and t2_free:
                                    current_assignments.append(
                                        self._build_assignment(c.id, d, s1, l1['teacher_id'], l1['subject_id'], regular_order_by_slot[s1.id])
                                    )
                                    current_assignments.append(
                                        self._build_assignment(c.id, d, s2, l2['teacher_id'], l2['subject_id'], regular_order_by_slot[s2.id])
                                    )
                                    teacher_day_slots.setdefault((l1['teacher_id'], d), []).append({
                                        'class_id': c.id, 'slot_id': s1.id, 'start_time': s1.start_time, 'end_time': s1.end_time
                                    })
                                    teacher_day_slots.setdefault((l2['teacher_id'], d), []).append({
                                        'class_id': c.id, 'slot_id': s2.id, 'start_time': s2.start_time, 'end_time': s2.end_time
                                    })
                                    placed = True
                                    break
                        if placed:
                            break

                    if not placed:
                        unpaired.extend([l1, l2])

                # Allocate remaining unpaired lessons
                for l in unpaired:
                    placed = False
                    random.shuffle(class_grid)
                    for d, s in class_grid:
                        already_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s.id for a in current_assignments)
                        if not already_used:
                            t_free = (
                                not self._has_teacher_clash(l['teacher_id'], d, s, teacher_day_slots)
                                and avail_map.get((l['teacher_id'], d, s.id)) != 'BLOCKED'
                            )
                            if t_free:
                                current_assignments.append(
                                    self._build_assignment(c.id, d, s, l['teacher_id'], l['subject_id'], regular_order_by_slot[s.id])
                                )
                                teacher_day_slots.setdefault((l['teacher_id'], d), []).append({
                                    'class_id': c.id, 'slot_id': s.id, 'start_time': s.start_time, 'end_time': s.end_time
                                })
                                placed = True
                                break

                    if not placed:
                        # Fallback: place in any remaining free slot for class
                        for d, s in class_grid:
                            already_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s.id for a in current_assignments)
                            if not already_used:
                                current_assignments.append(
                                    self._build_assignment(c.id, d, s, l['teacher_id'], l['subject_id'], regular_order_by_slot[s.id])
                                )
                                teacher_day_slots.setdefault((l['teacher_id'], d), []).append({
                                    'class_id': c.id, 'slot_id': s.id, 'start_time': s.start_time, 'end_time': s.end_time
                                })
                                break

            # Evaluate candidate schedule
            eval_res = self.evaluator.evaluate_schedule(current_assignments, avail_map, teacher_names=teacher_names)
            if eval_res['viability_score'] > best_eval['viability_score']:
                best_eval = eval_res
                best_assignments = current_assignments

                if eval_res['hard_violations'] == 0 and eval_res['viability_score'] >= 98.0:
                    break  # Reached high-quality optimal solution

        # 5. Fase 2: Refinamento via Simulated Annealing (Metropolis et al., 1953 / Kirkpatrick et al., 1983)
        if best_assignments:
            sa_assignments, sa_eval = self._simulated_annealing(
                initial_assignments=best_assignments,
                avail_map=avail_map,
                slots_by_shift=slots_by_shift,
                regular_order_by_slot=regular_order_by_slot,
                teacher_names=teacher_names,
                days=days,
                classes=classes,
                max_time_seconds=1.2
            )
            if sa_eval['viability_score'] >= best_eval['viability_score']:
                best_assignments = sa_assignments
                best_eval = sa_eval
        else:
            best_eval = {'viability_score': 100.0, 'hard_violations': 0, 'soft_penalty': 0.0, 'hard_details': [], 'soft_details': []}

        exec_duration = round(time.time() - start_time, 2)

        # 6. Persist to Database atomically
        with transaction.atomic():
            TimetableSchedule.objects.filter(is_active=True).update(is_active=False)
            schedule = TimetableSchedule.objects.create(
                name=self.schedule_name,
                semester=self.semester,
                is_active=True,
                viability_score=best_eval['viability_score'],
                hard_violations_count=best_eval['hard_violations'],
                soft_penalties_score=best_eval['soft_penalty'],
                execution_time_seconds=exec_duration,
                algorithm_used="Two-Stage Hybrid Solver: Constructive Heuristic + Simulated Annealing (Metropolis)"
            )

            warning_map = {}
            for s in best_eval.get('soft_details', []):
                if 'teacher_id' in s and 'day' in s:
                    warning_map[(s['teacher_id'], s['day'])] = s['message']

            slot_assignment_objs = []
            for a in best_assignments:
                has_warn = (a['teacher_id'], a['day']) in warning_map
                msg = warning_map.get((a['teacher_id'], a['day']), None)
                slot_assignment_objs.append(
                    TimetableSlotAssignment(
                        timetable_schedule=schedule,
                        school_class_id=a['class_id'],
                        day_of_week=a['day'],
                        time_slot_id=a['slot_id'],
                        subject_id=a['subject_id'],
                        teacher_id=a['teacher_id'],
                        has_conflict=has_warn,
                        conflict_type='SOFT_GAP' if has_warn else None,
                        conflict_message=msg
                    )
                )

            TimetableSlotAssignment.objects.bulk_create(slot_assignment_objs)

        classes_summary = []
        for c in classes:
            allocated_count = sum(1 for a in best_assignments if a['class_id'] == c.id)
            expected_count = len(class_lessons.get(c.id, []))
            classes_summary.append({
                'class_id': c.id,
                'class_name': c.name,
                'shift_name': c.shift.name if c.shift else '',
                'allocated': allocated_count,
                'expected': expected_count,
            })

        return {
            'schedule_id': schedule.id,
            'schedule_name': schedule.name,
            'viability_score': schedule.viability_score,
            'hard_violations': schedule.hard_violations_count,
            'soft_penalties': schedule.soft_penalties_score,
            'execution_time': schedule.execution_time_seconds,
            'total_assignments': len(slot_assignment_objs),
            'classes_summary': classes_summary,
            'hard_details': best_eval['hard_details'],
            'soft_details': best_eval['soft_details'],
        }

    def _simulated_annealing(
        self,
        initial_assignments,
        avail_map,
        slots_by_shift,
        regular_order_by_slot,
        teacher_names,
        days,
        classes,
        max_time_seconds=1.2,
    ):
        """
        Fase 2: Meta-heurística Simulated Annealing (Kirkpatrick et al., 1983 / Metropolis et al., 1953)
        Refina a solução viável gerada pela Fase 1, minimizando o custo soft (janelas e desequilíbrios)
        através de movimentos de vizinhança do tipo Swap Intra-Turma dentro do turno da turma, preservando Hard = 0.
        """
        sa_start = time.time()
        current_assignments = [dict(a) for a in initial_assignments]
        current_eval = self.evaluator.evaluate_schedule(current_assignments, avail_map, teacher_names=teacher_names)

        best_assignments = [dict(a) for a in current_assignments]
        best_eval = dict(current_eval)

        grid_by_class = {
            c.id: [(d, s) for d in days for s in slots_by_shift.get(c.shift_id, [])]
            for c in classes
        }
        classes_with_assignments = {a['class_id'] for a in current_assignments}
        active_sa_classes = [
            c for c in classes
            if c.id in classes_with_assignments and len(grid_by_class.get(c.id, [])) >= 2
        ]
        if not active_sa_classes:
            return best_assignments, best_eval

        class_slot_map = {(a['class_id'], a['day'], a['slot_id']): a for a in current_assignments}
        teacher_occ = set((a['teacher_id'], a['day'], a['slot_id']) for a in current_assignments)

        t_initial = 100.0
        t_final = 0.5
        alpha = 0.92
        steps_per_temp = min(30, max(10, len(active_sa_classes) * 2))

        temp = t_initial
        while temp > t_final and (time.time() - sa_start) < max_time_seconds:
            for _ in range(steps_per_temp):
                c = random.choice(active_sa_classes)
                (d1, s1), (d2, s2) = random.sample(grid_by_class[c.id], 2)

                a1 = class_slot_map.get((c.id, d1, s1.id))
                a2 = class_slot_map.get((c.id, d2, s2.id))

                if a1 is None and a2 is None:
                    continue

                # Caso A: Swap entre duas aulas já alocadas da mesma turma
                if a1 is not None and a2 is not None:
                    t1, t2 = a1['teacher_id'], a2['teacher_id']
                    if t1 == t2 and a1['subject_id'] == a2['subject_id']:
                        continue

                    t1_blocked = avail_map.get((t1, d2, s2.id)) == 'BLOCKED'
                    t1_clash = (t1, d2, s2.id) in teacher_occ and t1 != t2
                    if t1_blocked or t1_clash:
                        continue

                    t2_blocked = avail_map.get((t2, d1, s1.id)) == 'BLOCKED'
                    t2_clash = (t2, d1, s1.id) in teacher_occ and t2 != t1
                    if t2_blocked or t2_clash:
                        continue

                    self._apply_slot(a1, d2, s2, regular_order_by_slot[s2.id])
                    self._apply_slot(a2, d1, s1, regular_order_by_slot[s1.id])

                    candidate_eval = self.evaluator.evaluate_schedule(current_assignments, avail_map, teacher_names=teacher_names)

                    if candidate_eval['hard_violations'] > current_eval['hard_violations']:
                        self._apply_slot(a1, d1, s1, regular_order_by_slot[s1.id])
                        self._apply_slot(a2, d2, s2, regular_order_by_slot[s2.id])
                        continue

                    delta_cost = candidate_eval['soft_penalty'] - current_eval['soft_penalty']

                    accept = False
                    if delta_cost <= 0:
                        accept = True
                    else:
                        exponent = -delta_cost / temp
                        prob = math.exp(exponent) if exponent > -700 else 0.0
                        if random.random() < prob:
                            accept = True

                    if accept:
                        del class_slot_map[(c.id, d1, s1.id)]
                        del class_slot_map[(c.id, d2, s2.id)]
                        class_slot_map[(c.id, d2, s2.id)] = a1
                        class_slot_map[(c.id, d1, s1.id)] = a2

                        teacher_occ.discard((t1, d1, s1.id))
                        teacher_occ.discard((t2, d2, s2.id))
                        teacher_occ.add((t1, d2, s2.id))
                        teacher_occ.add((t2, d1, s1.id))

                        current_eval = candidate_eval

                        if (current_eval['hard_violations'] < best_eval['hard_violations'] or
                            (current_eval['hard_violations'] == best_eval['hard_violations'] and
                             current_eval['soft_penalty'] < best_eval['soft_penalty'])):
                            best_assignments = [dict(a) for a in current_assignments]
                            best_eval = dict(current_eval)
                    else:
                        self._apply_slot(a1, d1, s1, regular_order_by_slot[s1.id])
                        self._apply_slot(a2, d2, s2, regular_order_by_slot[s2.id])

                # Caso B: Movimentação de uma aula para um slot vazio da mesma turma
                else:
                    active_a = a1 if a1 is not None else a2
                    from_d, from_s = (d1, s1) if a1 is not None else (d2, s2)
                    to_d, to_s = (d2, s2) if a1 is not None else (d1, s1)

                    t_id = active_a['teacher_id']
                    if avail_map.get((t_id, to_d, to_s.id)) == 'BLOCKED' or (t_id, to_d, to_s.id) in teacher_occ:
                        continue

                    self._apply_slot(active_a, to_d, to_s, regular_order_by_slot[to_s.id])
                    candidate_eval = self.evaluator.evaluate_schedule(current_assignments, avail_map, teacher_names=teacher_names)

                    if candidate_eval['hard_violations'] > current_eval['hard_violations']:
                        self._apply_slot(active_a, from_d, from_s, regular_order_by_slot[from_s.id])
                        continue

                    delta_cost = candidate_eval['soft_penalty'] - current_eval['soft_penalty']
                    accept = False
                    if delta_cost <= 0:
                        accept = True
                    else:
                        exponent = -delta_cost / temp
                        prob = math.exp(exponent) if exponent > -700 else 0.0
                        if random.random() < prob:
                            accept = True

                    if accept:
                        del class_slot_map[(c.id, from_d, from_s.id)]
                        class_slot_map[(c.id, to_d, to_s.id)] = active_a

                        teacher_occ.discard((t_id, from_d, from_s.id))
                        teacher_occ.add((t_id, to_d, to_s.id))

                        current_eval = candidate_eval

                        if (current_eval['hard_violations'] < best_eval['hard_violations'] or
                            (current_eval['hard_violations'] == best_eval['hard_violations'] and
                             current_eval['soft_penalty'] < best_eval['soft_penalty'])):
                            best_assignments = [dict(a) for a in current_assignments]
                            best_eval = dict(current_eval)
                    else:
                        self._apply_slot(active_a, from_d, from_s, regular_order_by_slot[from_s.id])

            temp *= alpha

        return best_assignments, best_eval
