import React, { useState, useEffect, useMemo } from 'react';
import type {
  SchoolClass, Shift, Subject, Teacher, CurriculumRequirement, TimeSlot
} from '../types';
import { api } from '../services/api';
import {
  GraduationCap, Plus, Search, Pencil, Trash2, Layers, Users, Clock, AlertTriangle, CheckCircle2
} from 'lucide-react';
import { NewClassModal } from '../components/NewClassModal';
import { NewCurriculumModal } from '../components/NewCurriculumModal';
import { BlastRadiusModal } from '../components/BlastRadiusModal';

interface ClassesPageProps {
  classes: SchoolClass[];
  shifts: Shift[];
  subjects: Subject[];
  teachers: Teacher[];
  slots: TimeSlot[];
  onRefresh: () => void;
}

export const ClassesPage: React.FC<ClassesPageProps> = ({
  classes,
  shifts,
  subjects,
  teachers,
  slots,
  onRefresh,
}) => {
  const [selectedClassId, setSelectedClassId] = useState<number>(classes[0]?.id || 0);
  const [searchTerm, setSearchTerm] = useState('');
  const [shiftFilter, setShiftFilter] = useState<number | 'all'>('all');

  const [isClassModalOpen, setIsClassModalOpen] = useState(false);
  const [classToEdit, setClassToEdit] = useState<SchoolClass | null>(null);
  const [classToDelete, setClassToDelete] = useState<SchoolClass | null>(null);
  const [isDeletingClass, setIsDeletingClass] = useState(false);

  const [curriculum, setCurriculum] = useState<CurriculumRequirement[]>([]);
  const [isCurriculumModalOpen, setIsCurriculumModalOpen] = useState(false);
  const [curriculumToEdit, setCurriculumToEdit] = useState<CurriculumRequirement | null>(null);
  const [curriculumToDelete, setCurriculumToDelete] = useState<CurriculumRequirement | null>(null);
  const [isDeletingCurriculum, setIsDeletingCurriculum] = useState(false);

  const loadCurriculum = async () => {
    try {
      const res = await api.getCurriculum();
      setCurriculum(res);
    } catch (err) {
      console.error('Erro ao carregar matriz curricular:', err);
    }
  };

  useEffect(() => {
    loadCurriculum();
  }, [classes]);

  useEffect(() => {
    if (classes.length > 0 && !classes.some(c => c.id === selectedClassId)) {
      setSelectedClassId(classes[0].id);
    }
  }, [classes, selectedClassId]);

  const filteredClasses = useMemo(() => {
    return classes.filter(c => {
      const matchesSearch =
        c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (c.grade_level || '').toLowerCase().includes(searchTerm.toLowerCase());
      const matchesShift = shiftFilter === 'all' || c.shift === shiftFilter;
      return matchesSearch && matchesShift;
    });
  }, [classes, searchTerm, shiftFilter]);

  const selectedClass = classes.find(c => c.id === selectedClassId) || filteredClasses[0] || null;
  const selectedClassCurriculum = useMemo(() => {
    if (!selectedClass) return [];
    return curriculum.filter(item => item.school_class === selectedClass.id);
  }, [curriculum, selectedClass]);

  const selectedShiftSlotsCount = useMemo(() => {
    if (!selectedClass) return 0;
    return slots.filter(s => s.shift === selectedClass.shift && !s.is_break).length * 5;
  }, [slots, selectedClass]);

  const selectedClassWeeklyTotal = selectedClassCurriculum.reduce((acc, r) => acc + r.weekly_lessons, 0);

  const handleConfirmDeleteClass = async () => {
    if (!classToDelete) return;
    setIsDeletingClass(true);
    try {
      await api.deleteClass(classToDelete.id);
      setClassToDelete(null);
      onRefresh();
    } catch (err: any) {
      alert('Erro ao excluir turma: ' + (err.message || err));
    } finally {
      setIsDeletingClass(false);
    }
  };

  const handleConfirmDeleteCurriculum = async () => {
    if (!curriculumToDelete) return;
    setIsDeletingCurriculum(true);
    try {
      await api.deleteCurriculumRequirement(curriculumToDelete.id);
      setCurriculumToDelete(null);
      await loadCurriculum();
      onRefresh();
    } catch (err: any) {
      alert('Erro ao remover disciplina da turma: ' + (err.message || err));
    } finally {
      setIsDeletingCurriculum(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <section className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          <div className="w-11 h-11 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-sm">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900">Cadastro de Turmas & Carga Curricular</h2>
            <p className="text-xs text-slate-500">
              Cadastre turmas por turno e defina as disciplinas e professores de cada turma para geração da grade.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() => {
            setClassToEdit(null);
            setIsClassModalOpen(true);
          }}
          className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl text-xs font-bold shadow-xs transition cursor-pointer shrink-0"
        >
          <Plus className="w-4 h-4" />
          <span>Nova Turma</span>
        </button>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Classes List */}
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200 shadow-xs p-5 space-y-4">
          <div className="flex items-center justify-between gap-2">
            <h3 className="text-sm font-bold text-slate-900">Turmas Cadastradas ({filteredClasses.length})</h3>
          </div>

          <div className="flex flex-col sm:flex-row gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Buscar turma ou série..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <select
              value={shiftFilter}
              onChange={(e) => setShiftFilter(e.target.value === 'all' ? 'all' : Number(e.target.value))}
              className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
            >
              <option value="all">Todos os Turnos</option>
              {shifts.map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2.5 max-h-[540px] overflow-y-auto pr-1">
            {filteredClasses.length === 0 ? (
              <div className="p-6 text-center border-2 border-dashed border-slate-200 rounded-xl text-xs text-slate-500">
                Nenhuma turma encontrada.
              </div>
            ) : (
              filteredClasses.map(c => {
                const isSelected = selectedClass?.id === c.id;
                const shiftObj = shifts.find(s => s.id === c.shift);
                const countCurric = curriculum.filter(r => r.school_class === c.id).reduce((acc, r) => acc + r.weekly_lessons, 0);

                return (
                  <div
                    key={c.id}
                    onClick={() => setSelectedClassId(c.id)}
                    className={`p-3.5 rounded-xl border transition cursor-pointer flex items-center justify-between gap-2 ${
                      isSelected
                        ? 'bg-indigo-50/70 border-indigo-300 shadow-2xs'
                        : 'bg-white border-slate-200 hover:border-indigo-200 hover:bg-slate-50/60'
                    }`}
                  >
                    <div className="min-w-0 space-y-1">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-extrabold text-slate-900 truncate">{c.name}</span>
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-800">
                          {shiftObj?.name || c.shift_name || 'Turno'}
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-500 truncate">{c.grade_level}</div>
                      <div className="flex items-center space-x-3 text-[11px] font-semibold text-slate-600 pt-0.5">
                        <span className="flex items-center space-x-1">
                          <Users className="w-3 h-3 text-slate-400" />
                          <span>{c.student_count} alunos</span>
                        </span>
                        <span className={`flex items-center space-x-1 ${countCurric === 0 ? 'text-amber-600' : 'text-emerald-700'}`}>
                          <Clock className="w-3 h-3" />
                          <span>{countCurric} aulas/sem</span>
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-1 shrink-0">
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setClassToEdit(c);
                          setIsClassModalOpen(true);
                        }}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-white transition cursor-pointer"
                        title="Editar turma"
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setClassToDelete(c);
                        }}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-white transition cursor-pointer"
                        title="Excluir turma"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right: Selected Class Curriculum Panel */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200 shadow-xs p-5 space-y-4">
          {!selectedClass ? (
            <div className="p-10 text-center text-xs text-slate-500">
              Selecione ou cadastre uma turma ao lado para gerenciar sua grade curricular.
            </div>
          ) : (
            <>
              <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-100">
                <div>
                  <div className="flex items-center space-x-2">
                    <h3 className="text-base font-extrabold text-slate-900">
                      Matriz Curricular • {selectedClass.name}
                    </h3>
                    <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                      {shifts.find(s => s.id === selectedClass.shift)?.name || selectedClass.shift_name}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Disciplinas e professores atribuídos para a geração automática do horário desta turma.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => {
                    setCurriculumToEdit(null);
                    setIsCurriculumModalOpen(true);
                  }}
                  className="flex items-center space-x-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-3.5 py-2 rounded-xl text-xs font-bold shadow-xs transition cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Vincular Disciplina</span>
                </button>
              </div>

              {/* Capacity Alert Bar */}
              <div className={`p-3 rounded-xl border text-xs flex items-center justify-between ${
                selectedShiftSlotsCount === 0
                  ? 'bg-amber-50 border-amber-200 text-amber-900'
                  : selectedClassWeeklyTotal > selectedShiftSlotsCount
                  ? 'bg-rose-50 border-rose-200 text-rose-900'
                  : selectedClassWeeklyTotal === 0
                  ? 'bg-amber-50 border-amber-200 text-amber-900'
                  : 'bg-emerald-50 border-emerald-200 text-emerald-900'
              }`}>
                <div className="flex items-center space-x-2 font-semibold">
                  {selectedShiftSlotsCount === 0 || selectedClassWeeklyTotal === 0 || selectedClassWeeklyTotal > selectedShiftSlotsCount ? (
                    <AlertTriangle className="w-4 h-4 shrink-0" />
                  ) : (
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                  )}
                  <span>
                    {selectedShiftSlotsCount === 0
                      ? 'Este turno ainda não possui slots regulares cadastrados em "Slots & Grade".'
                      : selectedClassWeeklyTotal === 0
                      ? 'Esta turma não possui disciplinas vinculadas — ela ficará vazia ao gerar a grade.'
                      : selectedClassWeeklyTotal > selectedShiftSlotsCount
                      ? `Demanda (${selectedClassWeeklyTotal} aulas) excede os ${selectedShiftSlotsCount} tempos disponíveis no turno.`
                      : `Carga curricular configurada: ${selectedClassWeeklyTotal} de ${selectedShiftSlotsCount} tempos semanais do turno.`}
                  </span>
                </div>
              </div>

              {/* Curriculum List */}
              {selectedClassCurriculum.length === 0 ? (
                <div className="p-8 text-center border-2 border-dashed border-slate-200 rounded-xl space-y-3">
                  <Layers className="w-8 h-8 text-slate-300 mx-auto" />
                  <p className="text-xs font-semibold text-slate-600">
                    Nenhuma disciplina vinculada à turma {selectedClass.name}.
                  </p>
                  <button
                    type="button"
                    onClick={() => {
                      setCurriculumToEdit(null);
                      setIsCurriculumModalOpen(true);
                    }}
                    className="inline-flex items-center space-x-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-3.5 py-2 rounded-lg text-xs font-bold transition cursor-pointer"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Adicionar Primeira Disciplina</span>
                  </button>
                </div>
              ) : (
                <div className="divide-y divide-slate-100 border border-slate-200 rounded-xl overflow-hidden">
                  {selectedClassCurriculum.map((req) => (
                    <div
                      key={req.id}
                      className="p-3.5 bg-white hover:bg-slate-50/70 transition flex items-center justify-between gap-3"
                    >
                      <div className="flex items-center space-x-3 min-w-0">
                        <span
                          className="px-2 py-1 rounded-lg font-mono text-[11px] font-extrabold text-white shrink-0"
                          style={{ backgroundColor: req.subject_color || '#4F46E5' }}
                        >
                          {req.subject_code}
                        </span>
                        <div className="min-w-0">
                          <div className="text-xs font-bold text-slate-900 truncate">{req.subject_name}</div>
                          <div className="text-[11px] text-slate-500 truncate">
                            👨‍🏫 {req.teacher_name} • {req.double_lessons_allowed ? 'Aceita geminadas' : 'Aulas isoladas'}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center space-x-3 shrink-0">
                        <span className="text-xs font-extrabold text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-lg border border-indigo-200">
                          {req.weekly_lessons} {req.weekly_lessons === 1 ? 'aula/sem' : 'aulas/sem'}
                        </span>
                        <button
                          type="button"
                          onClick={() => {
                            setCurriculumToEdit(req);
                            setIsCurriculumModalOpen(true);
                          }}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition cursor-pointer"
                          title="Editar requisito curricular"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => setCurriculumToDelete(req)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition cursor-pointer"
                          title="Remover da matriz da turma"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </section>

      {/* Modals */}
      <NewClassModal
        isOpen={isClassModalOpen}
        onClose={() => {
          setIsClassModalOpen(false);
          setClassToEdit(null);
        }}
        onSaved={onRefresh}
        classToEdit={classToEdit}
        shifts={shifts}
      />

      <NewCurriculumModal
        isOpen={isCurriculumModalOpen}
        onClose={() => {
          setIsCurriculumModalOpen(false);
          setCurriculumToEdit(null);
        }}
        onSaved={async () => {
          await loadCurriculum();
          onRefresh();
        }}
        curriculumToEdit={curriculumToEdit}
        classes={classes}
        subjects={subjects}
        teachers={teachers}
        preselectedClassId={selectedClass?.id}
      />

      {classToDelete && (
        <BlastRadiusModal
          isOpen={Boolean(classToDelete)}
          onClose={() => setClassToDelete(null)}
          onConfirm={handleConfirmDeleteClass}
          isDeleting={isDeletingClass}
          title="Excluir Turma Escolar?"
          entityType="Turma"
          entityName={classToDelete.name}
          consequences={[
            {
              title: 'Matriz curricular da turma',
              detail: `${curriculum.filter(r => r.school_class === classToDelete.id).length} vínculo(s) de disciplina/professor serão excluídos.`,
              severity: 'critical',
            },
            {
              title: 'Aulas alocadas na grade horária',
              detail: 'Todas as alocações desta turma nas grades geradas serão removidas.',
              severity: 'high',
            },
          ]}
        />
      )}

      {curriculumToDelete && (
        <BlastRadiusModal
          isOpen={Boolean(curriculumToDelete)}
          onClose={() => setCurriculumToDelete(null)}
          onConfirm={handleConfirmDeleteCurriculum}
          isDeleting={isDeletingCurriculum}
          title="Remover Disciplina da Matriz da Turma?"
          entityType="Carga Curricular"
          entityName={`${curriculumToDelete.subject_name} em ${curriculumToDelete.class_name}`}
          consequences={[
            {
              title: 'Carga semanal removida',
              detail: `${curriculumToDelete.weekly_lessons} aula(s) semanal(is) deixará(ão) de ser alocadas para esta turma.`,
              severity: 'high',
            },
          ]}
        />
      )}
    </div>
  );
};
