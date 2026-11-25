import React, { useState, useMemo } from 'react';
import type { Subject, Teacher } from '../types';
import { api } from '../services/api';
import {
  BookOpen, Plus, Search, FlaskConical, Users, Pencil, Trash2, UserPlus
} from 'lucide-react';
import { NewSubjectModal } from '../components/NewSubjectModal';
import { BlastRadiusModal } from '../components/BlastRadiusModal';

interface SubjectsPageProps {
  subjects: Subject[];
  teachers: Teacher[];
  onRefresh: () => void;
}

export const SubjectsPage: React.FC<SubjectsPageProps> = ({
  subjects,
  teachers,
  onRefresh,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterMode, setFilterMode] = useState<'all' | 'lab' | 'unassigned'>('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [subjectToEdit, setSubjectToEdit] = useState<Subject | null>(null);
  const [subjectToDelete, setSubjectToDelete] = useState<Subject | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const getConnectedTeachers = (subject: Subject) => {
    if (subject.teacher_details && subject.teacher_details.length > 0) {
      return subject.teacher_details;
    }
    const ids = subject.teachers || [];
    return teachers
      .filter(t => ids.includes(t.id))
      .map(t => ({
        id: t.id,
        name: t.name,
        avatar_initials: t.avatar_initials,
        color: t.color,
      }));
  };

  const filteredSubjects = useMemo(() => {
    return subjects.filter(s => {
      const matchesSearch =
        s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
        getConnectedTeachers(s).some(t => t.name.toLowerCase().includes(searchTerm.toLowerCase()));

      if (!matchesSearch) return false;
      if (filterMode === 'lab') return s.requires_lab;
      if (filterMode === 'unassigned') return getConnectedTeachers(s).length === 0;
      return true;
    });
  }, [subjects, teachers, searchTerm, filterMode]);

  const totalConnected = subjects.filter(s => getConnectedTeachers(s).length > 0).length;
  const totalLab = subjects.filter(s => s.requires_lab).length;
  const totalWithoutTeachers = subjects.length - totalConnected;

  const handleConfirmDelete = async () => {
    if (!subjectToDelete) return;
    setIsDeleting(true);
    try {
      await api.deleteSubject(subjectToDelete.id);
      setSubjectToDelete(null);
      onRefresh();
    } catch (err: any) {
      alert('Erro ao excluir disciplina: ' + (err.message || err));
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <section className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          <div className="w-11 h-11 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-sm">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900">Cadastro de Disciplinas</h2>
            <p className="text-xs text-slate-500">
              Gerencie as matérias curriculares e conecte diretamente os professores habilitados (N:N).
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() => {
            setSubjectToEdit(null);
            setIsModalOpen(true);
          }}
          className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl text-xs font-bold shadow-xs transition cursor-pointer shrink-0"
        >
          <Plus className="w-4 h-4" />
          <span>Nova Disciplina</span>
        </button>
      </section>

      {/* KPI Row */}
      <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-semibold text-slate-500">Total de Disciplinas</div>
          <div className="text-2xl font-extrabold text-slate-900 mt-1">{subjects.length}</div>
          <div className="text-[11px] text-slate-400 mt-1">{totalConnected} com professores conectados</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-semibold text-slate-500">Exigem Laboratório</div>
          <div className="text-2xl font-extrabold text-violet-600 mt-1">{totalLab}</div>
          <div className="text-[11px] text-slate-400 mt-1">Disciplinas práticas / especiais</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-semibold text-slate-500">Sem Professor Vinculado</div>
          <div className={`text-2xl font-extrabold mt-1 ${totalWithoutTeachers > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
            {totalWithoutTeachers}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            {totalWithoutTeachers > 0 ? 'Conecte docentes para facilitar a matriz' : 'Todas as disciplinas têm docente'}
          </div>
        </div>
      </section>

      {/* Filters + Search */}
      <section className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-wrap items-center justify-between gap-3">
        <div className="relative flex-1 min-w-[240px]">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Buscar por nome, sigla ou professor conectado..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <button
            type="button"
            onClick={() => setFilterMode('all')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition cursor-pointer ${
              filterMode === 'all' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            Todas ({subjects.length})
          </button>
          <button
            type="button"
            onClick={() => setFilterMode('lab')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition cursor-pointer ${
              filterMode === 'lab' ? 'bg-violet-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            Laboratório ({totalLab})
          </button>
          <button
            type="button"
            onClick={() => setFilterMode('unassigned')}
            className={`px-3 py-1.5 rounded-lg font-semibold transition cursor-pointer ${
              filterMode === 'unassigned' ? 'bg-amber-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            Sem Professor ({totalWithoutTeachers})
          </button>
        </div>
      </section>

      {/* Subjects Grid */}
      {filteredSubjects.length === 0 ? (
        <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-10 text-center space-y-2">
          <BookOpen className="w-8 h-8 text-slate-300 mx-auto" />
          <p className="text-xs font-bold text-slate-600">Nenhuma disciplina encontrada com os filtros atuais.</p>
        </div>
      ) : (
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredSubjects.map((subject) => {
            const connected = getConnectedTeachers(subject);
            return (
              <div
                key={subject.id}
                className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs hover:border-indigo-300 transition flex flex-col justify-between space-y-4"
                style={{ borderTopWidth: '4px', borderTopColor: subject.color }}
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center space-x-2.5 min-w-0">
                      <span
                        className="px-2.5 py-1 rounded-lg font-mono text-xs font-extrabold text-white shadow-2xs shrink-0"
                        style={{ backgroundColor: subject.color }}
                      >
                        {subject.code}
                      </span>
                      <div className="min-w-0">
                        <h3 className="text-sm font-bold text-slate-900 truncate" title={subject.name}>
                          {subject.name}
                        </h3>
                        <div className="flex items-center space-x-1.5 mt-0.5">
                          {subject.requires_lab ? (
                            <span className="inline-flex items-center space-x-1 text-[10px] font-bold text-violet-700 bg-violet-50 px-2 py-0.5 rounded border border-violet-200">
                              <FlaskConical className="w-3 h-3" />
                              <span>Requer Lab</span>
                            </span>
                          ) : (
                            <span className="text-[10px] text-slate-400 font-medium">Sala Regular</span>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-1 shrink-0">
                      <button
                        type="button"
                        onClick={() => {
                          setSubjectToEdit(subject);
                          setIsModalOpen(true);
                        }}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition cursor-pointer"
                        title="Editar disciplina e professores"
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => setSubjectToDelete(subject)}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition cursor-pointer"
                        title="Excluir disciplina"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {/* Connected Teachers */}
                  <div className="pt-2 border-t border-slate-100 space-y-2">
                    <div className="flex items-center justify-between text-[11px] font-bold text-slate-600">
                      <span className="flex items-center space-x-1">
                        <Users className="w-3.5 h-3.5 text-indigo-500" />
                        <span>Professores Conectados ({connected.length})</span>
                      </span>
                      <button
                        type="button"
                        onClick={() => {
                          setSubjectToEdit(subject);
                          setIsModalOpen(true);
                        }}
                        className="text-indigo-600 hover:text-indigo-800 inline-flex items-center space-x-1 cursor-pointer"
                      >
                        <UserPlus className="w-3 h-3" />
                        <span>Gerenciar</span>
                      </button>
                    </div>

                    {connected.length === 0 ? (
                      <div className="p-2.5 rounded-lg bg-amber-50/70 border border-amber-200 text-[11px] text-amber-800 font-medium">
                        Nenhum professor conectado ainda.
                      </div>
                    ) : (
                      <div className="flex flex-wrap gap-1.5">
                        {connected.map((t) => (
                          <span
                            key={t.id}
                            className="inline-flex items-center space-x-1.5 px-2 py-1 rounded-lg bg-slate-50 border border-slate-200 text-[11px] font-semibold text-slate-700"
                          >
                            <span
                              className="w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-bold"
                              style={{ backgroundColor: `${t.color}25`, color: t.color }}
                            >
                              {t.avatar_initials}
                            </span>
                            <span>{t.name}</span>
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </section>
      )}

      {/* New / Edit Subject Modal */}
      <NewSubjectModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSubjectToEdit(null);
        }}
        onSaved={onRefresh}
        subjectToEdit={subjectToEdit}
        teachers={teachers}
      />

      {/* Blast Radius Modal */}
      {subjectToDelete && (
        <BlastRadiusModal
          isOpen={Boolean(subjectToDelete)}
          onClose={() => setSubjectToDelete(null)}
          onConfirm={handleConfirmDelete}
          isDeleting={isDeleting}
          title="Excluir Disciplina do Catálogo?"
          entityType="Disciplina"
          entityName={`${subjectToDelete.name} (${subjectToDelete.code})`}
          consequences={[
            {
              title: 'Vínculos com professores conectados',
              detail: `${getConnectedTeachers(subjectToDelete).length} professor(es) conectado(s) perderão este vínculo.`,
              severity: 'medium',
            },
            {
              title: 'Demandas curriculares e alocações na grade',
              detail: 'Todas as cargas curriculares e aulas alocadas desta disciplina serão removidas.',
              severity: 'critical',
            },
          ]}
        />
      )}
    </div>
  );
};
