import time
import math
import random
from .constraints import ConstraintEvaluator
from core.models import (
    SchoolClass, CurriculumRequirement, TimeSlot, TeacherAvailability,
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

    def solve(self):
        start_time = time.time()

        # 1. Fetch data
        classes = list(SchoolClass.objects.all())
        curricula = list(CurriculumRequirement.objects.select_related('school_class', 'subject', 'teacher').all())
        # Filter regular non-break slots
        slots = list(TimeSlot.objects.filter(is_break=False).order_by('order'))

        # Fetch teacher availabilities: map (teacher_id, day, slot_id) -> status
        avail_qs = TeacherAvailability.objects.all()
        avail_map = {
            (a.teacher_id, a.day_of_week, a.time_slot_id): a.status
            for a in avail_qs
        }

        days = [0, 1, 2, 3, 4] # Seg a Sex (0 a 4)

        # 2. Build list of lessons to allocate per class
        # Each item: { class_id, subject_id, teacher_id, allow_double }
        class_lessons = {}
        for c in classes:
            class_lessons[c.id] = []

        for req in curricula:
            for _ in range(req.weekly_lessons):
                class_lessons[req.school_class_id].append({
                    'class_id': req.school_class_id,
                    'subject_id': req.subject_id,
                    'teacher_id': req.teacher_id,
                    'allow_double': req.double_lessons_allowed,
                })

        # 3. Available grid coordinates: list of (day, slot)

        grid_positions = []
        for d in days:
            for s in slots:
                grid_positions.append((d, s))

        best_assignments = []
        best_eval = {'viability_score': -1, 'hard_violations': 9999, 'soft_penalty': 999999}

        # 4. Multi-restart constructive search + local repair
        max_attempts = 15
        for attempt in range(max_attempts):
            current_assignments = []
            occupied_teacher = set() # (teacher_id, day, slot_id)

            for c in classes:
                lessons = list(class_lessons[c.id])
                # Shuffle lessons prioritizing subjects with double lessons
                random.shuffle(lessons)
                class_grid = list(grid_positions)

                # Prioritize pairing double lessons
                paired_lessons = []
                # Group by subject
                by_subject = {}
                for l in lessons:
                    by_subject.setdefault(l['subject_id'], []).append(l)

                unpaired = []
                for s_id, s_lessons in by_subject.items():
                    while len(s_lessons) >= 2 and s_lessons[0]['allow_double']:
                        paired_lessons.append((s_lessons.pop(), s_lessons.pop()))
                    unpaired.extend(s_lessons)

                # Allocate pairs first
                for l1, l2 in paired_lessons:
                    placed = False
                    for d in days:
                        for s_idx in range(len(slots) - 1):
                            s1 = slots[s_idx]
                            s2 = slots[s_idx + 1]

                            # Check if slots are free for this class
                            pos1_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s1.id for a in current_assignments)
                            pos2_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s2.id for a in current_assignments)

                            if not pos1_used and not pos2_used:
                                t1_free = (l1['teacher_id'], d, s1.id) not in occupied_teacher and avail_map.get((l1['teacher_id'], d, s1.id)) != 'BLOCKED'
                                t2_free = (l2['teacher_id'], d, s2.id) not in occupied_teacher and avail_map.get((l2['teacher_id'], d, s2.id)) != 'BLOCKED'

                                if t1_free and t2_free:
                                    current_assignments.append({
                                        'class_id': c.id, 'day': d, 'slot_id': s1.id, 'slot_order': s1.order,
                                        'teacher_id': l1['teacher_id'], 'subject_id': l1['subject_id']
                                    })
                                    current_assignments.append({
                                        'class_id': c.id, 'day': d, 'slot_id': s2.id, 'slot_order': s2.order,
                                        'teacher_id': l2['teacher_id'], 'subject_id': l2['subject_id']
                                    })
                                    occupied_teacher.add((l1['teacher_id'], d, s1.id))
                                    occupied_teacher.add((l2['teacher_id'], d, s2.id))
                                    placed = True
                                    break
                        if placed:
                            break

                    if not placed:
                        # Add back to unpaired
                        unpaired.extend([l1, l2])

                # Allocate remaining unpaired lessons
                for l in unpaired:
                    placed = False
                    random.shuffle(class_grid)
                    for d, s in class_grid:
                        already_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s.id for a in current_assignments)
                        if not already_used:
                            t_free = (l['teacher_id'], d, s.id) not in occupied_teacher and avail_map.get((l['teacher_id'], d, s.id)) != 'BLOCKED'
                            if t_free:
                                current_assignments.append({
                                    'class_id': c.id, 'day': d, 'slot_id': s.id, 'slot_order': s.order,
                                    'teacher_id': l['teacher_id'], 'subject_id': l['subject_id']
                                })
                                occupied_teacher.add((l['teacher_id'], d, s.id))
                                placed = True
                                break

                    if not placed:
                        # Fallback: place in any remaining free slot for class
                        for d, s in class_grid:
                            already_used = any(a['class_id'] == c.id and a['day'] == d and a['slot_id'] == s.id for a in current_assignments)
                            if not already_used:
                                current_assignments.append({
                                    'class_id': c.id, 'day': d, 'slot_id': s.id, 'slot_order': s.order,
                                    'teacher_id': l['teacher_id'], 'subject_id': l['subject_id']
                                })
                                break

            # Evaluate candidate schedule
            eval_res = self.evaluator.evaluate_schedule(current_assignments, avail_map)
            if eval_res['viability_score'] > best_eval['viability_score']:
                best_eval = eval_res
                best_assignments = current_assignments

                if eval_res['hard_violations'] == 0 and eval_res['viability_score'] >= 98.0:
                    break # Reached high-quality optimal solution

        # 5. Fase 2: Refinamento via Simulated Annealing (Metropolis et al., 1953 / Kirkpatrick et al., 1983)
        # Otimiza restrições soft (janelas e equilíbrio) via swaps intra-turma preservando Hard = 0
        if best_assignments:
            sa_assignments, sa_eval = self._simulated_annealing(
                initial_assignments=best_assignments,
                avail_map=avail_map,
                slots=slots,
                days=days,
                classes=classes,
                max_time_seconds=1.2
            )
            # Adota a solução do SA se melhorou ou manteve a qualidade
            if sa_eval['viability_score'] >= best_eval['viability_score']:
                best_assignments = sa_assignments
                best_eval = sa_eval

        exec_duration = round(time.time() - start_time, 2)

        # 6. Persist to Database
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

        # Build quick lookup for soft warnings
        warning_map = {}
        for s in best_eval.get('soft_details', []):
            if 'teacher_id' in s and 'day' in s:
                warning_map[(s['teacher_id'], s['day'])] = s['message']

        # Save slot assignments
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


        return {
            'schedule_id': schedule.id,
            'schedule_name': schedule.name,
            'viability_score': schedule.viability_score,
            'hard_violations': schedule.hard_violations_count,
            'soft_penalties': schedule.soft_penalties_score,
            'execution_time': schedule.execution_time_seconds,
            'total_assignments': len(slot_assignment_objs),
            'hard_details': best_eval['hard_details'],
            'soft_details': best_eval['soft_details'],
        }

    def _simulated_annealing(self, initial_assignments, avail_map, slots, days, classes, max_time_seconds=1.2):
        """
        Fase 2: Meta-heurística Simulated Annealing (Kirkpatrick et al., 1983 / Metropolis et al., 1953)
        Refina a solução viável gerada pela Fase 1, minimizando o custo soft (janelas e desequilíbrios)
        através de movimentos de vizinhança do tipo Swap Intra-Turma, preservando estritamente Hard = 0.
        """
        sa_start = time.time()
        current_assignments = [dict(a) for a in initial_assignments]
        current_eval = self.evaluator.evaluate_schedule(current_assignments, avail_map)

        best_assignments = [dict(a) for a in current_assignments]
        best_eval = dict(current_eval)

        grid_positions = [(d, s) for d in days for s in slots]

        # Mapeamentos rápidos em memória
        class_slot_map = {(a['class_id'], a['day'], a['slot_id']): a for a in current_assignments}
        teacher_occ = set((a['teacher_id'], a['day'], a['slot_id']) for a in current_assignments)

        # Parâmetros calibrados do SA
        t_initial = 100.0
        t_final = 0.5
        alpha = 0.92
        steps_per_temp = min(30, max(10, len(classes) * 2))

        temp = t_initial
        while temp > t_final and (time.time() - sa_start) < max_time_seconds:
            for _ in range(steps_per_temp):
                c = random.choice(classes)
                (d1, s1), (d2, s2) = random.sample(grid_positions, 2)

                a1 = class_slot_map.get((c.id, d1, s1.id))
                a2 = class_slot_map.get((c.id, d2, s2.id))

                if a1 is None and a2 is None:
                    continue

                # Caso A: Swap entre duas aulas já alocadas da mesma turma
                if a1 is not None and a2 is not None:
                    t1, t2 = a1['teacher_id'], a2['teacher_id']
                    if t1 == t2 and a1['subject_id'] == a2['subject_id']:
                        continue

                    # Viabilidade do professor 1 no slot 2
                    t1_blocked = avail_map.get((t1, d2, s2.id)) == 'BLOCKED'
                    t1_clash = (t1, d2, s2.id) in teacher_occ and t1 != t2
                    if t1_blocked or t1_clash:
                        continue

                    # Viabilidade do professor 2 no slot 1
                    t2_blocked = avail_map.get((t2, d1, s1.id)) == 'BLOCKED'
                    t2_clash = (t2, d1, s1.id) in teacher_occ and t2 != t1
                    if t2_blocked or t2_clash:
                        continue

                    # Executa movimento candidato
                    a1['day'], a1['slot_id'], a1['slot_order'] = d2, s2.id, s2.order
                    a2['day'], a2['slot_id'], a2['slot_order'] = d1, s1.id, s1.order

                    candidate_eval = self.evaluator.evaluate_schedule(current_assignments, avail_map)

                    # Guarda inviolável: Hard violations não podem aumentar
                    if candidate_eval['hard_violations'] > current_eval['hard_violations']:
                        a1['day'], a1['slot_id'], a1['slot_order'] = d1, s1.id, s1.order
                        a2['day'], a2['slot_id'], a2['slot_order'] = d2, s2.id, s2.order
                        continue

                    delta_cost = candidate_eval['soft_penalty'] - current_eval['soft_penalty']

                    # Critério de Aceitação de Metropolis
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
                        a1['day'], a1['slot_id'], a1['slot_order'] = d1, s1.id, s1.order
                        a2['day'], a2['slot_id'], a2['slot_order'] = d2, s2.id, s2.order

                # Caso B: Movimentação de uma aula para um slot vazio da mesma turma
                else:
                    active_a = a1 if a1 is not None else a2
                    from_d, from_s = (d1, s1) if a1 is not None else (d2, s2)
                    to_d, to_s = (d2, s2) if a1 is not None else (d1, s1)

                    t_id = active_a['teacher_id']
                    if avail_map.get((t_id, to_d, to_s.id)) == 'BLOCKED' or (t_id, to_d, to_s.id) in teacher_occ:
                        continue

                    active_a['day'], active_a['slot_id'], active_a['slot_order'] = to_d, to_s.id, to_s.order
                    candidate_eval = self.evaluator.evaluate_schedule(current_assignments, avail_map)

                    if candidate_eval['hard_violations'] > current_eval['hard_violations']:
                        active_a['day'], active_a['slot_id'], active_a['slot_order'] = from_d, from_s.id, from_s.order
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
                        active_a['day'], active_a['slot_id'], active_a['slot_order'] = from_d, from_s.id, from_s.order

            temp *= alpha

        return best_assignments, best_eval
