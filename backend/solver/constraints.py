DAY_NAMES = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
}


class ConstraintEvaluator:
    def __init__(self, config_weights=None):
        self.weights = {
            'teacher_clash': 100000,
            'class_clash': 100000,
            'teacher_blocked': 100000,
            'min_gap_weight': 85,
            'double_lesson_weight': 90,
            'daily_balance_weight': 70,
            'day_concentration_weight': 60,
        }
        if config_weights:
            self.weights.update(config_weights)

    def evaluate_schedule(self, assignments, teacher_availabilities, max_daily_limits=None, teacher_names=None):
        """
        assignments: list of dicts:
          { 'class_id': int, 'day': int, 'slot_id': int, 'slot_order': int,
            'teacher_id': int, 'subject_id': int,
            optional 'shift_id': int, 'regular_order': int }
        """
        hard_violations = 0
        soft_penalty = 0
        hard_details = []
        soft_details = []
        teacher_names = teacher_names or {}

        # 1. HARD: Teacher Clashes
        # Map (teacher_id, day, slot_id) -> list of classes
        teacher_time_map = {}
        # 2. HARD: Class Clashes (turma com duas aulas simultâneas)
        # Map (class_id, day, slot_id) -> list of assignments
        class_time_map = {}
        # Teacher schedule by day & shift: (teacher_id, day, shift_id) -> list of regular slot positions
        teacher_day_shift_slots = {}
        # Class schedule by day: class_id -> day -> list of subject_ids
        class_day_subjects = {}

        for a in assignments:
            t_key = (a['teacher_id'], a['day'], a['slot_id'])
            teacher_time_map.setdefault(t_key, []).append(a)

            c_key = (a['class_id'], a['day'], a['slot_id'])
            class_time_map.setdefault(c_key, []).append(a)

            # Check teacher blocked availability
            avail_key = (a['teacher_id'], a['day'], a['slot_id'])
            status = teacher_availabilities.get(avail_key, 'FREE')
            if status == 'BLOCKED':
                hard_violations += 1
                t_label = teacher_names.get(a['teacher_id'], f"Professor {a['teacher_id']}")
                d_label = DAY_NAMES.get(a['day'], f"Dia {a['day']}")
                hard_details.append(f"{t_label} alocado em horário bloqueado ({d_label}, Slot {a['slot_id']})")

            # Collect for soft constraints (grouped per shift using regular non-break index)
            pos = a.get('regular_order', a['slot_order'])
            shift_key = a.get('shift_id', 0)
            teacher_day_shift_slots.setdefault((a['teacher_id'], a['day'], shift_key), []).append(pos)
            class_day_subjects.setdefault(a['class_id'], {}).setdefault(a['day'], []).append(a['subject_id'])

        # Check teacher double-booking (exact slot or overlapping time blocks on same day)
        teacher_day_assignments = {}
        for a in assignments:
            teacher_day_assignments.setdefault((a['teacher_id'], a['day']), []).append(a)

        for (t_id, day), a_list in teacher_day_assignments.items():
            # Group by exact slot_id first
            by_slot = {}
            for a in a_list:
                by_slot.setdefault(a['slot_id'], []).append(a)
            for slot_id, slot_list in by_slot.items():
                if len(slot_list) > 1:
                    violation_count = len(slot_list) - 1
                    hard_violations += violation_count
                    hard_details.append(f"Choque: Professor {t_id} alocado em {len(slot_list)} turmas no Dia {day} Slot {slot_id}")

            # Check overlapping time windows across different shifts/slots
            for i in range(len(a_list)):
                a1 = a_list[i]
                s1_start = a1.get('start_time')
                s1_end = a1.get('end_time')
                if s1_start is None or s1_end is None:
                    continue
                for j in range(i + 1, len(a_list)):
                    a2 = a_list[j]
                    if a1['slot_id'] == a2['slot_id']:
                        continue
                    s2_start = a2.get('start_time')
                    s2_end = a2.get('end_time')
                    if s2_start is not None and s2_end is not None:
                        if s1_start < s2_end and s2_start < s1_end:
                            hard_violations += 1
                            hard_details.append(
                                f"Choque de horário entre turnos: Professor {t_id} no Dia {day} ({s1_start}-{s1_end} vs {s2_start}-{s2_end})"
                            )

        # Check class double-booking
        for (c_id, day, slot_id), a_list in class_time_map.items():
            if len(a_list) > 1:
                violation_count = len(a_list) - 1
                hard_violations += violation_count
                hard_details.append(f"Choque: Turma {c_id} possui {len(a_list)} aulas simultâneas no Dia {day} Slot {slot_id}")


        # 3. SOFT CONSTRAINTS
        # A. Minimize Teacher Gaps (Janelas Vagas) - evaluated per shift ignoring break slots
        gap_weight = self.weights.get('min_gap_weight', 85)
        gaps_by_teacher_day = {}
        for (t_id, day, _shift_id), slot_positions in teacher_day_shift_slots.items():
            if len(slot_positions) > 1:
                unique_sorted = sorted(set(slot_positions))
                span = unique_sorted[-1] - unique_sorted[0] + 1
                gaps = span - len(unique_sorted)
                if gaps > 0:
                    gaps_by_teacher_day[(t_id, day)] = gaps_by_teacher_day.get((t_id, day), 0) + gaps

        for (t_id, day), gaps in gaps_by_teacher_day.items():
            soft_penalty += gaps * gap_weight
            t_label = teacher_names.get(t_id, f"Professor {t_id}")
            d_label = DAY_NAMES.get(day, f"Dia {day}")
            soft_details.append({
                'type': 'SOFT_GAP',
                'teacher_id': t_id,
                'day': day,
                'message': f"{t_label} com {gaps} janela(s) vaga(s) em {d_label}"
            })

        # B. Subject Distribution (Avoid too many isolated singles or overcrowding)
        balance_weight = self.weights.get('daily_balance_weight', 70)
        for c_id, days_map in class_day_subjects.items():
            for day, subj_list in days_map.items():
                counts = {}
                for s in subj_list:
                    counts[s] = counts.get(s, 0) + 1
                for s, count in counts.items():
                    if count > 2: # More than 2 lessons of the same subject on the same day
                        soft_penalty += (count - 2) * balance_weight
                        soft_details.append({
                            'type': 'SOFT_BALANCE',
                            'class_id': c_id,
                            'subject_id': s,
                            'day': day,
                            'message': f"Turma {c_id} com {count} aulas da disciplina {s} no mesmo dia"
                        })

        # Viability Score calculation: 100 - (Hard * 25 + Soft normalized)
        viability_score = max(0.0, min(100.0, 100.0 - (hard_violations * 25.0) - (soft_penalty * 0.05)))

        return {
            'hard_violations': hard_violations,
            'soft_penalty': soft_penalty,
            'viability_score': round(viability_score, 1),
            'hard_details': hard_details,
            'soft_details': soft_details,
        }