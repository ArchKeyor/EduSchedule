import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta de Cores Moderna e Acadêmica
    BG_DARK = RGBColor(15, 23, 42)      # #0F172A
    CARD_BG = RGBColor(30, 41, 59)      # #1E293B
    CARD_BORDER = RGBColor(51, 65, 85)  # #334155
    ACCENT_BLUE = RGBColor(59, 130, 246)# #3B82F6
    ACCENT_CYAN = RGBColor(6, 182, 212) # #06B6D4
    ACCENT_GREEN = RGBColor(16, 185, 129)# #10B981
    ACCENT_AMBER = RGBColor(245, 158, 11)# #F59E0B
    ACCENT_RED = RGBColor(239, 68, 68)  # #EF4444
    TEXT_LIGHT = RGBColor(248, 250, 252)# #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)# #94A3B8

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, tag, title):
        # Tag pill
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title="", border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN
        return card

    # -------------------------------------------------------------
    # SLIDE 1: CAPA
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CENTRO UNIVERSITÁRIO GERALDO DI BIASE (UGB) • VOLTA REDONDA - RJ"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE
    p0.space_after = Pt(20)

    p1 = tf.add_paragraph()
    p1.text = "Abordagem Heurística para o Problema de Alocação de Horários Escolares"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Modelagem Matemática, Espaço de Busca e Framework de Resolução em Dois Estágios (School Timetabling Problem)"
    p2.font.size = Pt(16)
    p2.font.color.rgb = ACCENT_CYAN
    p2.space_after = Pt(36)

    p3 = tf.add_paragraph()
    p3.text = "Disciplina: Laboratório de Programação (6º Período)   |   Professor: Me. Marcelo Arantes de Oliveira\nEquipe: Kauê Loreno Lopes (Tech Lead) • Pedro Henrique Dias Dornellas • Lucas Santana"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: O PROBLEMA E A COMPLEXIDADE
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "1. Contextualização Teórica", "O School Timetabling Problem e a Explosão Combinatória")

    # Card 1: O Desafio
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "O Problema Real de Timetabling", ACCENT_BLUE)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Alocação semanal de aulas entre Turmas e Professores em uma grade de horários finita (time slots).\n\n• Gargalo tradicional nas escolas: montagem puramente manual por coordenadores, consumindo semanas de esforço.\n\n• Impacto Humano Crítico: horários mal distribuídos geram janelas ociosas (gaps), que causam estresse crônico, fadiga e absenteísmo docente (Tardif & Lessard, 2014)."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # Card 2: Intratabilidade
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Por que métodos exatos falham? (NP-Hard)", ACCENT_AMBER)
    tb = s2.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Classificação Formal: NP-Difícil (NP-Hard) comprovado por Even, Itai e Shamir (1976).\n\n• Redução teórica: Coloração de Vértices de Grafos (Graph Vertex Coloring - Karp, 1972).\n\n• Explosão Combinatória Bruta: Para 25 slots semanais e N aulas:\n   Espaço de Busca = 25^N\n   Ex: 10 turmas (N = 250) -> 25^250 ≈ 10^350 combinações!\n\n• Conclusão: Força bruta ou Programação Linear (MILP) esgotam memória RAM (Branch-and-Bound). Heurísticas são indispensáveis."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 3: MODELAGEM MATEMÁTICA FORMAL
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "2. Seção A: Modelagem Matemática", "Definição Formal do Problema e Variáveis de Decisão")

    # Card Conjuntos
    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Conjuntos e Parâmetros Discretos", ACCENT_BLUE)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Turmas (T): Conjunto de turmas/séries fixas da escola.\n• Professores (P): Corpo docente contratado.\n• Disciplinas (D): Matérias da matriz curricular.\n• Dias da Semana (Dia): Dia = {1, 2, 3, 4, 5} (5 dias letivos).\n• Períodos Diários (S): S = {1, 2, 3, 4, 5} (5 horários/dia).\n• Grade Semanal (K): K = Dia x S -> Total de 25 slots.\n• Carga Horária CH(t, d): Total de aulas semanais da matéria d na turma t.\n• Disponibilidade Disp(p, dia, s): 1 se o docente está livre; 0 se bloqueado."
    for p in tf.paragraphs:
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # Card Variáveis
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Variável de Decisão Binária", ACCENT_CYAN)
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "A alocação de cada aula é regida por uma variável de decisão binária multidimensional:\n\n   x_{t, p, d, dia, s} ∈ {0, 1}\n\n• x_{t, p, d, dia, s} = 1: se a aula da disciplina d ministrada pelo professor p para a turma t ocorrer no dia 'dia' e slot 's'.\n• x_{t, p, d, dia, s} = 0: caso contrário.\n\nPropriedade Estrutural:\nComo cada disciplina da turma tem professor pré-atribuído Prof(t, d) = p, o tensor simplifica-se para x_{t, d, dia, s} ∈ {0, 1}, mantendo integridade e alta velocidade de consulta em memória RAM."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 4: RESTRIÇÕES FORTES (HARD CONSTRAINTS)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "3. Seção B: Metodologia", "Restrições Fortes (Hard Constraints) — Invioláveis")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), "Condições Obrigatórias de Viabilidade Física e Matemática", ACCENT_RED)
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(11.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "Se QUALQUER restrição forte for violada, a grade é considerada INVÁLIDA e inutilizável na realidade:\n\n1. UNICIDADE DOCENTE (Sem Choque de Professor):\n   Um professor não pode ministrar aula em mais de uma turma no mesmo período:\n   ∑_{t} ∑_{d} x_{t, p, d, dia, s} ≤ 1,  ∀ p, dia, s\n\n2. UNICIDADE DE TURMA (Sem Choque de Turma):\n   Uma turma não pode ter mais de uma disciplina no mesmo período temporal:\n   ∑_{p} ∑_{d} x_{t, p, d, dia, s} ≤ 1,  ∀ t, dia, s\n\n3. RESPEITO À INDISPONIBILIDADE DOCENTE:\n   Nenhuma aula pode ser agendada em slots bloqueados na agenda do professor:\n   x_{t, p, d, dia, s} ≤ Disp_{p, dia, s},  ∀ t, p, d, dia, s\n\n4. CUMPRIMENTO INTEGRAL DA CARGA HORÁRIA:\n   Todas as aulas da grade curricular devem ser alocadas semanalmente:\n   ∑_{dia} ∑_{s} x_{t, Prof(t,d), d, dia, s} = CH(t, d),  ∀ t, d"
    for p in tf.paragraphs:
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 5: RESTRIÇÕES FRACAS (SOFT CONSTRAINTS)
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "3. Seção B: Metodologia", "Restrições Fracas (Soft Constraints) — Qualidade Pedagógica")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), "Critérios de Ergonomia Docente e Equilíbrio Didático", ACCENT_AMBER)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(11.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "As restrições fracas NÃO invalidam a grade, mas mensuram sua qualidade e conforto ergonômico:\n\n1. MINIMIZAÇÃO DE JANELAS VAGAS DOCENTES (Teacher Gaps) — Peso w_gap = 85:\n   • Penaliza intervalos ociosos na jornada diária do professor entre sua 1ª e última aula.\n   • Gap(p, dia) = (slot_max - slot_min + 1) - TotalAulas(p, dia)\n   • Base científica: Tardif & Lessard (2014) provam que janelas causam desgaste cognitivo agudo.\n\n2. EQUILÍBRIO DIÁRIO DE DISCIPLINAS (Daily Balance) — Peso w_balance = 70:\n   • Evita que a turma assista a muitas aulas da mesma matéria no mesmo dia (máx. 2 períodos).\n   • Excesso(t, d, dia) = max(0, ∑_s x_{t,d,dia,s} - 2)\n   • Previne a exaustão dos alunos e melhora a retenção de aprendizado.\n\n3. PREFERÊNCIAS DOCENTES:\n   • Priorizar alocação em dias/turnos declarados como preferidos pelos docentes quando houver empate de viabilidade."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 6: FUNÇÃO DE APTIDÃO (FITNESS FUNCTION)
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "3. Seção B: Metodologia", "Função de Aptidão e Penalização Ponderada (Fitness Function)")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), "Formulação Escalar da Função Objetivo de Custo", ACCENT_CYAN)
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(11.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "A pontuação de uma grade gerada S é calculada por uma função de custo a ser MINIMIZADA:\n\n   f(S) = W_hard · ∑_{i ∈ Hard} H_i(S) + ∑_{j ∈ Soft} w_j · V_j(S)\n\n• H_i(S): Contabiliza qualquer violação de restrição dura (choque docente, turma ou bloqueio).\n• W_hard = 100.000: Penalidade dissuasiva extrema. Torna a solução instantaneamente inviável.\n• V_j(S): Contabiliza a frequência de penalidades suaves (janelas ociosas, excesso diário de aulas).\n• Pesos calibrados (implementados no ConstraintEvaluator do sistema):\n   w_gap = 85 (evitar janelas vagas docentes)\n   w_balance = 70 (evitar mais de 2 aulas da mesma matéria por dia)\n\nCRITÉRIO FORMAL DE VIABILIDADE:\n   Solução Viável (Feasible) ⇔ ∑ H_i(S) = 0 ⇔ f(S) < 100.000\n   Solução Inviável (Infeasible) ⇔ f(S) ≥ 100.000"
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 7: HEURÍSTICA 1 - DSATUR GULOSO (FASE 1)
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "4. Seção C: Heurísticas Adotadas", "Algoritmo 1: Heurística Construtiva Gulosa por Saturação (DSatur)")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Princípio Teórico 'Fail-First'", ACCENT_BLUE)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Embasamento: Algoritmo DSatur de Daniel Brélaz (1979) e Carter, Laporte & Chinneck (1996).\n\n• Filosofia Fail-First (Falhe Primeiro):\n  Vértices com maior saturação (menos slots livres disponíveis) são agendados primeiro.\n\n• Função de Criticidade:\n  Criticidade(d) = α · CH(d) + β · (1 - DisponibilidadeDocente)\n\n• Professores com poucos horários semanais recebem prioridade máxima de alocação."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Mecanismo de Busca e Desempenho", ACCENT_GREEN)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Pipeline de Execução:\n  1. Mapeia disponibilidades em matriz binária na RAM (GridState).\n  2. Ordena demandas curriculares por criticidade decrescente.\n  3. Para cada aula, seleciona deterministicamente o 1º slot livre na turma e no docente.\n  4. Atualização de estado atômica O(1).\n\n• Papel Estratégico no Sistema:\n  Fase 1 (Warm Start): Entrega uma grade 100% viável (Hard = 0) em menos de 100 milissegundos com complexidade assintótica O(N log N)."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 8: HEURÍSTICA 2 - SIMULATED ANNEALING (FASE 2)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "4. Seção C: Heurísticas Adotadas", "Algoritmo 2: Metaheurística de Busca Local (Simulated Annealing)")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Como escapar de Ótimos Locais?", ACCENT_AMBER)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Embasamento: Kirkpatrick, Gelatt e Vecchi (1983) — analogia com o recozimento térmico de metais.\n\n• O Problema do Hill Climbing:\n  A busca gulosa fica presa em ótimos locais (soluções com janelas que não melhoram por troca direta).\n\n• O Critério de Metropolis:\n  Permite aceitar soluções PIORES com probabilidade controlada pela temperatura T:\n     P(aceitar) = e^{-Δf / T}\n\n• Resfriamento geométrico: T_{k+1} = α · T_k (0.85 ≤ α ≤ 0.98)."
    for p in tf.paragraphs:
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Operadores de Vizinhança (Perturbação)", ACCENT_CYAN)
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Operador 1: Troca Intra-Turma (Swap Move):\n  Permuta duas disciplinas em slots distintos da mesma turma. Preserva 100% da carga horária.\n\n• Operador 2: Deslocamento para Slot Livre (Move to Free):\n  Move aula para período livre adjacente, eliminando janelas docentes (gaps).\n\n• Blindagem de Restrições Fortes:\n  Se a troca gerar choque de professor, o movimento é sumariamente rejeitado (P = 0).\n  A busca opera estritamente dentro da região viável!"
    for p in tf.paragraphs:
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 9: SÍNTESE COMPARATIVA & CONCLUSÃO
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "5. Conclusão", "Síntese Comparativa e o Framework em Dois Estágios")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), "Comparativo Técnico das Abordagens e Encerramento", ACCENT_GREEN)
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(11.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "QUADRO COMPARATIVO DAS HEURÍSTICAS:\n\n• Algoritmo 1 (DSatur Construtivo): Construtivo Determinístico | Fase 1 (Warm Start) | Foco: Hard = 0 | Complexidade: O(N log N) (< 100ms) | Sem escape de ótimo local.\n\n• Algoritmo 2 (Simulated Annealing): Metaheurística Estocástica de Trajetória | Fase 2 (Polimento Suave) | Foco: Soft (Gaps e Equilíbrio) | Operador: Swap Moves | Escape via Metropolis (e^{-Δf/T}).\n\nCONCLUSÃO:\nO paradigma híbrido em dois estágios resolve com perfeição o School Timetabling Problem: o DSatur contorna a barreira da explosão combinatória eliminando todos os choques em milissegundos, enquanto o Simulated Annealing refina a ergonomia da grade docente, garantindo respeito à saúde do professor."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # Salva o arquivo PPTX
    out_path = r"c:\Users\Kauê\Documents\02_Programacao_e_Tech\Projetos\TimeTabling\docs\apresentacoes\apresentacao-seminario-timetabling.pptx"
    prs.save(out_path)
    print("Apresentação gerada com sucesso em:", out_path)

if __name__ == "__main__":
    create_deck()
