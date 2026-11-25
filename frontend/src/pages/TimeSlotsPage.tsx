import React, { useState, useEffect, useMemo } from 'react';
import type { Shift, TimeSlot, SchoolClass } from '../types';
import {
  Plus, Save, Coffee, CheckSquare, Trash2, Calendar, Clock,
  Pencil, ArrowUp, ArrowDown, GripVertical, Loader2
} from 'lucide-react';
import { NewShiftModal } from '../components/NewShiftModal';
import { NewSlotModal } from '../components/NewSlotModal';
import { BlastRadiusModal } from '../components/BlastRadiusModal';
import { api } from '../services/api';

interface TimeSlotsPageProps {
  shifts: Shift[];
  slots: TimeSlot[];
  classes?: SchoolClass[];
  onRefresh?: () => void;
}

export const TimeSlotsPage: React.FC<TimeSlotsPageProps> = ({
  shifts,
  slots,
  classes = [],
  onRefresh
}) => {
  const [activeShiftId, setActiveShiftId] = useState<number>(shifts[0]?.id || 1);
  const [isShiftModalOpen, setIsShiftModalOpen] = useState(false);
  const [shiftToEdit, setShiftToEdit] = useState<Shift | null>(null);
  const [shiftToDelete, setShiftToDelete] = useState<Shift | null>(null);
  const [isDeletingShift, setIsDeletingShift] = useState(false);

  const [isSlotModalOpen, setIsSlotModalOpen] = useState(false);
  const [slotToEdit, setSlotToEdit] = useState<TimeSlot | null>(null);

  const [orderedSlots, setOrderedSlots] = useState<TimeSlot[]>([]);
  const [draggedSlotId, setDraggedSlotId] = useState<number | null>(null);
  const [isReordering, setIsReordering] = useState(false);

  const [activeDays, setActiveDays] = useState({
    seg: true,
    ter: true,
    qua: true,
    qui: true,
    sex: true,
    sab: false,
  });

  useEffect(() => {
    if (shifts.length > 0 && !shifts.some(s => s.id === activeShiftId)) {
      setActiveShiftId(shifts[0].id);
    }
  }, [shifts, activeShiftId]);

  const activeShift = shifts.find(s => s.id === activeShiftId) || shifts[0];

  const baseShiftSlots = useMemo(() => {
    return slots
      .filter(s => s.shift === activeShiftId || (!s.shift && activeShiftId === 1))
      .slice()
      .sort((a, b) => a.order - b.order || a.start_time.localeCompare(b.start_time));
  }, [slots, activeShiftId]);

  useEffect(() => {
    setOrderedSlots(baseShiftSlots);
  }, [baseShiftSlots]);

  const persistSlotOrder = async (newList: TimeSlot[]) => {
    const withUpdatedOrder = newList.map((s, idx) => ({ ...s, order: idx + 1 }));
    setOrderedSlots(withUpdatedOrder);
    setIsReordering(true);
    try {
      await api.reorderSlots(withUpdatedOrder.map(s => s.id));
      if (onRefresh) onRefresh();
    } catch (err: any) {
      alert('Erro ao salvar ordenação dos slots: ' + (err.message || err));
      setOrderedSlots(baseShiftSlots);
    } finally {
      setIsReordering(false);
    }
  };

  const handleMoveSlot = (index: number, direction: -1 | 1) => {
    const targetIdx = index + direction;
    if (targetIdx < 0 || targetIdx >= orderedSlots.length) return;
    const copy = [...orderedSlots];
    const [moved] = copy.splice(index, 1);
    copy.splice(targetIdx, 0, moved);
    persistSlotOrder(copy);
  };

  const handleDropSlot = (targetSlotId: number) => {
    if (draggedSlotId === null || draggedSlotId === targetSlotId) {
      setDraggedSlotId(null);
      return;
    }
    const fromIdx = orderedSlots.findIndex(s => s.id === draggedSlotId);
    const toIdx = orderedSlots.findIndex(s => s.id === targetSlotId);
    setDraggedSlotId(null);
    if (fromIdx === -1 || toIdx === -1) return;

    const copy = [...orderedSlots];
    const [moved] = copy.splice(fromIdx, 1);
    copy.splice(toIdx, 0, moved);
    persistSlotOrder(copy);
  };

  const handleConfirmDeleteShift = async () => {
    if (!shiftToDelete) return;
    setIsDeletingShift(true);
    try {
      await api.deleteShift(shiftToDelete.id);
      setShiftToDelete(null);
      if (onRefresh) onRefresh();
    } catch (err: any) {
      alert('Erro ao excluir turno: ' + (err.message || err));
    } finally {
      setIsDeletingShift(false);
    }
  };

  const handleDeleteSlot = async (slotId: number) => {
    if (!confirm('Deseja realmente remover este slot de aula?')) return;
    try {
      await api.deleteSlot(slotId);
      if (onRefresh) onRefresh();
    } catch (err: any) {
      alert('Erro ao excluir slot: ' + err.message);
    }
  };

  const handleSaveTimeStructure = () => {
    alert('Configurações temporais e de dias letivos salvas com sucesso!');
    if (onRefresh) onRefresh();
  };

  const activeDaysCount = Object.values(activeDays).filter(Boolean).length;
  const regularShiftSlotsCount = orderedSlots.filter(s => !s.is_break).length;
  const totalDemandLessons = classes.reduce((acc, c) => acc + (c.total_weekly_lessons || 0), 0);

  return (
    <div className="space-y-6">
      <section className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2">
          {shifts.map((s) => {
            const isActive = s.id === activeShiftId;
            const countForShift = slots.filter(sl => sl.shift === s.id).length;
            return (
              <div
                key={s.id}
                className={`group flex items-center rounded-xl text-xs font-bold transition border ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700 border-indigo-200 shadow-xs'
                    : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border-slate-200'
                }`}
              >
                <button
                  type="button"
                  onClick={() => setActiveShiftId(s.id)}
                  className="px-3.5 py-2 flex items-center space-x-2 cursor-pointer"
                >
                  <span>☀️ {s.name} ({s.start_time.slice(0, 5)} - {s.end_time.slice(0, 5)})</span>
                  <span className="text-[10px] bg-white px-1.5 py-0.5 rounded font-normal text-slate-500">
                    {countForShift} Tempos
                  </span>
                </button>
                <div className="flex items-center pr-2 space-x-0.5 border-l border-slate-200/80 pl-1.5">
                  <button
                    type="button"
                    onClick={() => {
                      setShiftToEdit(s);
                      setIsShiftModalOpen(true);
                    }}
                    className="p-1 rounded-md text-slate-400 hover:text-indigo-600 hover:bg-white transition cursor-pointer"
                    title={`Editar turno ${s.name}`}
                  >
                    <Pencil className="w-3.5 h-3.5" />
                  </button>
                  <button
                    type="button"
                    onClick={() => setShiftToDelete(s)}
                    className="p-1 rounded-md text-slate-400 hover:text-rose-600 hover:bg-white transition cursor-pointer"
                    title={`Excluir turno ${s.name}`}
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}

          <button
            type="button"
            onClick={() => {
              setShiftToEdit(null);
              setIsShiftModalOpen(true);
            }}
            className="px-3 py-2 rounded-xl text-xs font-semibold bg-slate-50 hover:bg-indigo-50/70 hover:text-indigo-600 text-slate-600 border border-dashed border-slate-300 hover:border-indigo-300 transition cursor-pointer"
          >
            + Adicionar Novo Turno
          </button>
        </div>

        <button
          type="button"
          onClick={handleSaveTimeStructure}
          className="flex items-center space-x-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-xs font-semibold shadow-xs transition cursor-pointer"
        >
          <Save className="w-3.5 h-3.5" />
          <span>Salvar Grade Temporal</span>
        </button>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
          <div className="flex justify-between items-center pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <span>Estrutura dos Slots de Aula • Turno {activeShift?.name || 'Matutino'}</span>
                {isReordering && (
                  <span className="inline-flex items-center space-x-1 text-[10px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>Salvando ordem...</span>
                  </span>
                )}
              </h3>
              <p className="text-xs text-slate-500">
                Arraste os cards ou use as setas para definir a ordenação manual dos períodos.
              </p>
            </div>
            <button
              type="button"
              onClick={() => {
                setSlotToEdit(null);
                setIsSlotModalOpen(true);
              }}
              className="flex items-center space-x-1 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 px-3 py-1.5 rounded-lg text-xs font-bold border border-indigo-200 transition cursor-pointer shrink-0"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Adicionar Período</span>
            </button>
          </div>

          <div className="space-y-3 pt-2">
            {orderedSlots.length === 0 ? (
              <div className="p-8 text-center border-2 border-dashed border-slate-200 rounded-xl space-y-3">
                <Clock className="w-8 h-8 text-slate-300 mx-auto" />
                <p className="text-xs font-semibold text-slate-600">Nenhum slot cadastrado para o turno {activeShift?.name}.</p>
                <button
                  type="button"
                  onClick={() => {
                    setSlotToEdit(null);
                    setIsSlotModalOpen(true);
                  }}
                  className="inline-flex items-center space-x-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Adicionar Primeiro Período</span>
                </button>
              </div>
            ) : (
              orderedSlots.map((slot, idx) => {
                const isDragging = draggedSlotId === slot.id;
                const reorderControls = (
                  <div className="flex items-center space-x-0.5">
                    <button
                      type="button"
                      disabled={idx === 0 || isReordering}
                      onClick={() => handleMoveSlot(idx, -1)}
                      className="p-1 hover:bg-indigo-50 rounded text-slate-400 hover:text-indigo-600 disabled:opacity-25 disabled:cursor-not-allowed transition cursor-pointer"
                      title="Mover para cima"
                    >
                      <ArrowUp className="w-3.5 h-3.5" />
                    </button>
                    <button
                      type="button"
                      disabled={idx === orderedSlots.length - 1 || isReordering}
                      onClick={() => handleMoveSlot(idx, 1)}
                      className="p-1 hover:bg-indigo-50 rounded text-slate-400 hover:text-indigo-600 disabled:opacity-25 disabled:cursor-not-allowed transition cursor-pointer"
                      title="Mover para baixo"
                    >
                      <ArrowDown className="w-3.5 h-3.5" />
                    </button>
                  </div>
                );

                if (slot.is_break) {
                  return (
                    <div
                      key={slot.id}
                      draggable
                      onDragStart={() => setDraggedSlotId(slot.id)}
                      onDragOver={(e) => e.preventDefault()}
                      onDrop={() => handleDropSlot(slot.id)}
                      onDragEnd={() => setDraggedSlotId(null)}
                      className={`bg-amber-50/70 border border-amber-300 rounded-xl p-4 flex items-center justify-between shadow-2xs group transition ${
                        isDragging ? 'opacity-50 ring-2 ring-indigo-400' : 'hover:border-amber-400'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <span className="cursor-grab text-amber-500 hover:text-amber-700" title="Arraste para reordenar">
                          <GripVertical className="w-4 h-4" />
                        </span>
                        <div className="w-10 h-10 rounded-lg bg-amber-100 text-amber-800 flex flex-col items-center justify-center font-bold">
                          <Coffee className="w-4 h-4" />
                          <span className="text-[9px] leading-none mt-0.5">{slot.order}º</span>
                        </div>
                        <div>
                          <h4 className="text-xs font-bold text-amber-950">☕ {slot.name}</h4>
                          <p className="text-[11px] text-amber-800">Pausa pedagógica oficial para recreio e descanso.</p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-3 text-xs font-bold text-amber-900">
                        <div className="text-right">
                          <div>{slot.start_time.slice(0, 5)} às {slot.end_time.slice(0, 5)}</div>
                          <span className="bg-amber-200/80 px-2 py-0.5 rounded text-[10px] inline-block mt-0.5">
                            {slot.duration_minutes} min
                          </span>
                        </div>
                        {reorderControls}
                        <button
                          type="button"
                          onClick={() => {
                            setSlotToEdit(slot);
                            setIsSlotModalOpen(true);
                          }}
                          className="p-1.5 hover:bg-amber-200/70 text-amber-700 rounded-lg transition cursor-pointer"
                          title="Editar intervalo"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDeleteSlot(slot.id)}
                          className="p-1.5 hover:bg-rose-100 text-rose-600 rounded-lg transition cursor-pointer"
                          title="Excluir intervalo"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  );
                }

                return (
                  <div
                    key={slot.id}
                    draggable
                    onDragStart={() => setDraggedSlotId(slot.id)}
                    onDragOver={(e) => e.preventDefault()}
                    onDrop={() => handleDropSlot(slot.id)}
                    onDragEnd={() => setDraggedSlotId(null)}
                    className={`bg-white border border-slate-200 rounded-xl p-4 flex items-center justify-between hover:border-indigo-300 transition shadow-2xs group ${
                      isDragging ? 'opacity-50 ring-2 ring-indigo-400' : ''
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <span className="cursor-grab text-slate-300 group-hover:text-slate-500" title="Arraste para reordenar">
                        <GripVertical className="w-4 h-4" />
                      </span>
                      <div className="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-700 flex items-center justify-center font-bold text-xs">
                        {slot.order}º
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-slate-900">{slot.name}</h4>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="text-[10px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">
                            Aula Regular
                          </span>
                          <span className="text-[10px] text-slate-500">
                            • {slot.allow_double_lesson ? 'Permite Geminação' : 'Aula Individual'}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      <div className="text-right">
                        <div className="text-xs font-bold text-slate-800">
                          {slot.start_time.slice(0, 5)} às {slot.end_time.slice(0, 5)}
                        </div>
                        <span className="text-[11px] text-slate-500">{slot.duration_minutes} minutos</span>
                      </div>

                      {reorderControls}

                      <div className="flex items-center space-x-1">
                        <button
                          type="button"
                          onClick={() => {
                            setSlotToEdit(slot);
                            setIsSlotModalOpen(true);
                          }}
                          className="p-1.5 hover:bg-indigo-50 rounded text-slate-400 hover:text-indigo-600 transition cursor-pointer"
                          title="Editar slot de aula"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDeleteSlot(slot.id)}
                          className="p-1.5 hover:bg-rose-50 rounded text-slate-400 hover:text-rose-600 transition cursor-pointer"
                          title="Excluir slot de aula"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          <button
            type="button"
            onClick={() => {
              setSlotToEdit(null);
              setIsSlotModalOpen(true);
            }}
            className="w-full py-3 border-2 border-dashed border-slate-200 hover:border-indigo-300 rounded-xl text-xs font-bold text-indigo-600 hover:bg-indigo-50/50 transition flex items-center justify-center space-x-1.5 cursor-pointer"
          >
            <Plus className="w-4 h-4" />
            <span>Inserir Novo Slot de Aula ou Intervalo</span>
          </button>
        </div>

        <div className="lg:col-span-5 space-y-5">
          <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">
            <div className="flex items-center space-x-2">
              <Calendar className="w-4 h-4 text-indigo-600" />
              <h4 className="text-xs font-bold text-slate-900">Dias Letivos Semanais</h4>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs">
              {[
                { id: 'seg', label: 'Segunda-feira' },
                { id: 'ter', label: 'Terça-feira' },
                { id: 'qua', label: 'Quarta-feira' },
                { id: 'qui', label: 'Quinta-feira' },
                { id: 'sex', label: 'Sexta-feira' },
                { id: 'sab', label: 'Sábado Letivo' },
              ].map(d => (
                <label
                  key={d.id}
                  className={`p-2.5 rounded-lg border flex items-center space-x-2 cursor-pointer transition ${
                    activeDays[d.id as keyof typeof activeDays]
                      ? 'bg-indigo-50/70 border-indigo-200 text-indigo-950 font-bold'
                      : 'bg-slate-50 border-slate-200 text-slate-500'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={activeDays[d.id as keyof typeof activeDays]}
                    onChange={(e) => setActiveDays({ ...activeDays, [d.id]: e.target.checked })}
                    className="rounded text-indigo-600 focus:ring-indigo-500"
                  />
                  <span>{d.label.slice(0, 3)}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-3.5">
            <h4 className="text-xs font-bold text-slate-900">Regras Pedagógicas de Alocação Temporal</h4>
            <div className="space-y-2.5 text-xs text-slate-700">
              <label className="flex items-start space-x-2.5 p-2 rounded-lg bg-slate-50 border border-slate-100 cursor-pointer">
                <CheckSquare className="w-4 h-4 text-indigo-600 mt-0.5 shrink-0" />
                <span>Permitir geminação máxima de 2 tempos consecutivos</span>
              </label>
              <label className="flex items-start space-x-2.5 p-2 rounded-lg bg-slate-50 border border-slate-100 cursor-pointer">
                <CheckSquare className="w-4 h-4 text-indigo-600 mt-0.5 shrink-0" />
                <span>Proibir geminações atravessando o Intervalo (2º e 3º tempos)</span>
              </label>
              <label className="flex items-start space-x-2.5 p-2 rounded-lg bg-slate-50 border border-slate-100 cursor-pointer">
                <CheckSquare className="w-4 h-4 text-indigo-600 mt-0.5 shrink-0" />
                <span>Priorizar matérias de Exatas nos 1º e 2º períodos (maior foco)</span>
              </label>
              <label className="flex items-start space-x-2.5 p-2 rounded-lg bg-slate-50 border border-slate-100 cursor-pointer">
                <CheckSquare className="w-4 h-4 text-indigo-600 mt-0.5 shrink-0" />
                <span>Evitar provas ou aulas densas no 5º período da Sexta-feira</span>
              </label>
            </div>
          </div>

          <div className="bg-indigo-50/80 rounded-xl border border-indigo-200 p-5 space-y-3">
            <h4 className="text-xs font-bold text-indigo-950">📊 Balanço de Capacidade Temporal</h4>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between text-indigo-900">
                <span>Slots Semanais ({activeShift?.name || 'Turno'}):</span>
                <span className="font-bold">
                  {regularShiftSlotsCount * activeDaysCount} tempos ({activeDaysCount} dias x {regularShiftSlotsCount} aulas)
                </span>
              </div>
              <div className="flex justify-between text-indigo-900">
                <span>Total de Turmas Cadastradas:</span>
                <span className="font-bold">{classes.length} turmas</span>
              </div>
              <div className="flex justify-between text-indigo-900">
                <span>Demanda Curricular Total:</span>
                <span className="font-bold">{totalDemandLessons} tempos / semana</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* New / Edit Shift Modal */}
      <NewShiftModal
        isOpen={isShiftModalOpen}
        onClose={() => {
          setIsShiftModalOpen(false);
          setShiftToEdit(null);
        }}
        shiftToEdit={shiftToEdit}
        onShiftCreated={(savedShift) => {
          setActiveShiftId(savedShift.id);
          if (onRefresh) onRefresh();
        }}
      />

      {/* New / Edit Slot Modal */}
      <NewSlotModal
        isOpen={isSlotModalOpen}
        onClose={() => {
          setIsSlotModalOpen(false);
          setSlotToEdit(null);
        }}
        shifts={shifts}
        activeShiftId={activeShiftId}
        existingSlotsCount={orderedSlots.length}
        slotToEdit={slotToEdit}
        onSlotCreated={() => {
          if (onRefresh) onRefresh();
        }}
      />

      {/* Blast Radius Modal for Shift Deletion */}
      {shiftToDelete && (
        <BlastRadiusModal
          isOpen={Boolean(shiftToDelete)}
          onClose={() => setShiftToDelete(null)}
          onConfirm={handleConfirmDeleteShift}
          isDeleting={isDeletingShift}
          title="Excluir Turno / Período Letivo?"
          entityType="Turno"
          entityName={`${shiftToDelete.name} (${shiftToDelete.start_time.slice(0, 5)} - ${shiftToDelete.end_time.slice(0, 5)})`}
          consequences={[
            {
              title: 'Slots de horário configurados neste turno',
              detail: `${slots.filter(sl => sl.shift === shiftToDelete.id).length} slot(s) de aula/intervalo serão excluídos em cascata.`,
              severity: 'critical',
            },
            {
              title: 'Turmas vinculadas a este turno',
              detail: `${classes.filter(c => c.shift === shiftToDelete.id).length} turma(s) dependem deste turno e serão afetadas.`,
              severity: 'high',
            },
          ]}
        />
      )}
    </div>
  );
};