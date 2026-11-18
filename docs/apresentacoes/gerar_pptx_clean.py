from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta de Alto Contraste Acadêmica (Light & Navy / Standard PowerPoint compliant)
    # Usando elementos 100% nativos sem tags de linha inválidas
    BG_COLOR = RGBColor(248, 250, 252)    # #F8FAFC (Slate 50)
    NAVY_PRIMARY = RGBColor(15, 23, 42)   # #0F172A (Slate 900)
    NAVY_CARD = RGBColor(255, 255, 255)   # #FFFFFF (Branco limpo)
    BORDER_COLOR = RGBColor(203, 213, 225)# #CBD5E1 (Slate 300)
    ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563EB (Royal Blue)
    ACCENT_RED = RGBColor(220, 38, 38)    # #DC2626 (Red 600)
    ACCENT_AMBER = RGBColor(217, 119, 6)  # #D97706 (Amber 600)
    ACCENT_GREEN = RGBColor(5, 150, 105)  # #059669 (Emerald 600)
    TEXT_DARK = RGBColor(15, 23, 42)      # #0F172A
    TEXT_MUTED = RGBColor(71, 85, 105)    # #475569

    def create_slide_base(title_tag, main_title):
        slide = prs.slides.add_slide(blank_layout)
        
        # Fundo do slide nativo
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

        # Header Pill
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = title_tag.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_BLUE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = main_title
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY_PRIMARY

        return slide

    def add_content_card(slide, left, top, width, height, title, title_color=ACCENT_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = NAVY_CARD
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1.5)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.5), Inches(0.45))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # -------------------------------------------------------------
    # SLIDE 1: CAPA
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.background
    f1 = bg1.fill
    f1.solid()
    f1.fore_color.rgb = NAVY_PRIMARY

    # Caixa central da Capa
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CENTRO UNIVERSITÁRIO GERALDO DI BIASE (UGB) • VOLTA REDONDA - RJ"
    p0.font.name = "Arial"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(96, 165, 250)
    p0.space_after = Pt(22)

    p1 = tf.add_paragraph()
    p1.text = "Abordagem Heurística para o Problema de Alocação de Horários Escolares"
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_after = Pt(14)

    p2 = tf.add_paragraph()
    p2.text = "Modelagem Matemática, Espaço de Busca e Framework de Resolução em Dois Estágios (School Timetabling Problem)"
    p2.font.name = "Arial"
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(147, 197, 253)
    p2.space_after = Pt(36)

    p3 = tf.add_paragraph()
    p3.text = "Disciplina: Laboratório de Programação (6º Período)   |   Professor: Me. Marcelo Arantes de Oliveira\nEquipe: Kauê Loreno Lopes (Tech Lead) • Pedro Henrique Dias Dornellas • Lucas Santana"
    p3.font.name = "Arial"
    p3.font.size = Pt(12.5)
    p3.font.color.rgb = RGBColor(203, 213, 225)

    # -------------------------------------------------------------
    # SLIDE 2: O PROBLEMA E A COMPLEXIDADE COMBINATÓRIA
    # -------------------------------------------------------------
    s2 = create_slide_base("1. Contextualização Teórica", "O School Timetabling Problem e a Explosão Combinatória")
    add_content_card(s2, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "O Problema Real de Timetabling", ACCENT_BLUE)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Desafio Operacional: Alocação semanal de aulas entre turmas fixas e professores em grade de períodos finita.\n\n• Gargalo Histórico: Tradicionalmente feito de forma manual por coordenadores, consumindo semanas de trabalho árduo.\n\n• Impacto Humano & Docente: Grades mal otimizadas geram janelas ociosas (gaps). Tardif & Lessard (2014) comprovam que a fragmentação da jornada é causa direta de estresse crônico, absenteísmo e burnout docente."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    add_content_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Por que métodos exatos falham? (NP-Hard)", ACCENT_AMBER)
    tb = s2.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Classificação Formal: NP-Difícil (NP-Hard) comprovado por Even, Itai e Shamir (1976).\n\n• Redução Clássica: Redução ao problema de Coloração de Vértices de Grafos (Karp, 1972).\n\n• Explosão Combinatória Bruta: Para 25 slots na semana e N aulas:\n   Espaço de Busca = 25^N\n   Ex: Apenas 10 turmas (N = 250) -> 25^250 ≈ 10^350 combinações!\n\n• Conclusão: Força bruta ou MILP puro esgotam memória RAM em árvores de Branch-and-Bound. Heurísticas são vitais."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 3: MODELAGEM MATEMÁTICA FORMAL
    # -------------------------------------------------------------
    s3 = create_slide_base("2. Seção A: Modelagem Matemática", "Definição Formal dos Conjuntos e Variáveis de Decisão")
    add_content_card(s3, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Conjuntos e Parâmetros Discretos", ACCENT_BLUE)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Turmas (T): Classes de alunos (T = {t_1, ..., t_|T|}).\n• Professores (P): Quadro docente contratado.\n• Disciplinas (D): Matérias da matriz curricular.\n• Dias (Dia): Dia = {1, 2, 3, 4, 5} (5 dias letivos).\n• Períodos (S): S = {1, 2, 3, 4, 5} (5 aulas/dia).\n• Slots Semanais (K): K = Dia x S -> Total de 25 slots.\n• Carga Horária CH(t, d): Total de aulas semanais da matéria d.\n• Disponibilidade Disp(p, dia, s): 1 se livre; 0 se bloqueado."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    add_content_card(s3, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Variável de Decisão Binária", ACCENT_GREEN)
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "A decisão de alocação temporal de cada aula é regida por uma variável de decisão binária:\n\n   x_{t, p, d, dia, s} ∈ {0, 1}\n\n• x_{t, p, d, dia, s} = 1: se a aula da disciplina d, ministrada pelo docente p para a turma t, for alocada no dia 'dia' e slot 's'.\n• x_{t, p, d, dia, s} = 0: caso contrário.\n\nPropriedade Estrutural de Otimização:\nComo cada disciplina da turma tem professor pré-atribuído Prof(t, d) = p, o tensor opera em memória RAM simplificado como x_{t, d, dia, s} ∈ {0, 1}, garantindo consultas O(1)."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 4: RESTRIÇÕES FORTES (HARD CONSTRAINTS)
    # -------------------------------------------------------------
    s4 = create_slide_base("3. Seção B: Metodologia", "Restrições Fortes (Hard Constraints) — Invioláveis")
    add_content_card(s4, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1), "Condições Obrigatórias de Viabilidade Física e Matemática", ACCENT_RED)
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(11.1), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "Se QUALQUER restrição forte for violada, a grade é considerada INVÁLIDA e inutilizável:\n\n1. UNICIDADE DOCENTE (Sem Choque de Professor):\n   Um professor não pode ministrar aula em mais de uma turma no mesmo período:\n   ∑_{t} ∑_{d} x_{t, p, d, dia, s} ≤ 1,  ∀ p ∈ P, dia ∈ Dia, s ∈ S\n\n2. UNICIDADE DE TURMA (Sem Choque de Turma):\n   Uma turma não pode ter mais de uma aula alocada no mesmo período de tempo:\n   ∑_{p} ∑_{d} x_{t, p, d, dia, s} ≤ 1,  ∀ t ∈ T, dia ∈ Dia, s ∈ S\n\n3. RESPEITO À INDISPONIBILIDADE DOCENTE:\n   Nenhuma aula pode ser agendada em horários bloqueados pelo professor:\n   x_{t, p, d, dia, s} ≤ Disp_{p, dia, s},  ∀ t, p, d, dia, s\n\n4. CUMPRIMENTO INTEGRAL DA CARGA HORÁRIA:\n   Todas as aulas da grade curricular devem ser alocadas semanalmente:\n   ∑_{dia} ∑_{s} x_{t, Prof(t,d), d, dia, s} = CH(t, d),  ∀ t, d"
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 5: RESTRIÇÕES FRACAS (SOFT CONSTRAINTS)
    # -------------------------------------------------------------
    s5 = create_slide_base("3. Seção B: Metodologia", "Restrições Fracas (Soft Constraints) — Qualidade Pedagógica")
    add_content_card(s5, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1), "Critérios de Ergonomia Docente e Equilíbrio Didático", ACCENT_AMBER)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(11.1), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "As restrições fracas NÃO invalidam a grade, mas mensuram sua qualidade e conforto ergonômico:\n\n1. MINIMIZAÇÃO DE JANELAS VAGAS DOCENTES (Teacher Gaps) — Peso w_gap = 85:\n   • Penaliza intervalos ociosos na jornada diária do professor entre sua 1ª e última aula.\n   • Gap(p, dia) = (slot_max - slot_min + 1) - TotalAulas(p, dia)\n   • Base científica: Tardif & Lessard (2014) provam que janelas causam desgaste cognitivo agudo.\n\n2. EQUILÍBRIO DIÁRIO DE DISCIPLINAS (Daily Balance) — Peso w_balance = 70:\n   • Evita que a turma assista a muitas aulas da mesma matéria no mesmo dia (máx. 2 períodos).\n   • Excesso(t, d, dia) = max(0, ∑_s x_{t,d,dia,s} - 2)\n   • Previne a exaustão dos alunos e melhora a retenção de aprendizado.\n\n3. PREFERÊNCIAS DOCENTES:\n   • Priorizar alocação em dias/turnos declarados como preferidos pelos docentes quando houver empate de viabilidade."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 6: FUNÇÃO DE APTIDÃO (FITNESS FUNCTION)
    # -------------------------------------------------------------
    s6 = create_slide_base("3. Seção B: Metodologia", "Função de Aptidão e Penalização Ponderada (Fitness Function)")
    add_content_card(s6, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1), "Formulação Escalar da Função Objetivo de Custo", ACCENT_BLUE)
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(11.1), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "A pontuação de uma grade gerada S é calculada por uma função de custo a ser MINIMIZADA:\n\n   f(S) = W_hard · ∑_{i ∈ Hard} H_i(S) + ∑_{j ∈ Soft} w_j · V_j(S)\n\n• H_i(S): Contabiliza qualquer violação de restrição dura (choque docente, turma ou bloqueio).\n• W_hard = 100.000: Penalidade dissuasiva extrema. Torna a solução instantaneamente inviável.\n• V_j(S): Contabiliza a frequência de penalidades suaves (janelas ociosas, excesso diário de aulas).\n• Pesos calibrados (implementados no ConstraintEvaluator do sistema):\n   w_gap = 85 (evitar janelas vagas docentes)\n   w_balance = 70 (evitar mais de 2 aulas da mesma matéria por dia)\n\nCRITÉRIO FORMAL DE VIABILIDADE:\n   Solução Viável (Feasible) ⇔ ∑ H_i(S) = 0 ⇔ f(S) < 100.000\n   Solução Inviável (Infeasible) ⇔ f(S) ≥ 100.000"
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 7: HEURÍSTICA 1 - DSATUR GULOSO (FASE 1)
    # -------------------------------------------------------------
    s7 = create_slide_base("4. Seção C: Heurísticas Adotadas", "Algoritmo 1: Heurística Construtiva Gulosa por Saturação (DSatur)")
    add_content_card(s7, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Princípio Teórico 'Fail-First'", ACCENT_BLUE)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Embasamento: Algoritmo DSatur de Daniel Brélaz (1979) e Carter, Laporte & Chinneck (1996).\n\n• Filosofia Fail-First (Falhe Primeiro):\n  Vértices com maior saturação (menos slots livres disponíveis) são agendados primeiro.\n\n• Função de Criticidade:\n  Criticidade(d) = α · CH(d) + β · (1 - DisponibilidadeDocente)\n\n• Professores com poucos horários semanais recebem prioridade máxima de alocação."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    add_content_card(s7, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Mecanismo de Busca e Desempenho", ACCENT_GREEN)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Pipeline de Execução:\n  1. Mapeia disponibilidades em matriz binária na RAM (GridState).\n  2. Ordena demandas curriculares por criticidade decrescente.\n  3. Para cada aula, seleciona deterministicamente o 1º slot livre na turma e no docente.\n  4. Atualização de estado atômica O(1).\n\n• Papel Estratégico no Sistema:\n  Fase 1 (Warm Start): Entrega uma grade 100% viável (Hard = 0) em menos de 100 milissegundos com complexidade assintótica O(N log N)."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 8: HEURÍSTICA 2 - SIMULATED ANNEALING (FASE 2)
    # -------------------------------------------------------------
    s8 = create_slide_base("4. Seção C: Heurísticas Adotadas", "Algoritmo 2: Metaheurística de Busca Local (Simulated Annealing)")
    add_content_card(s8, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), "Como escapar de Ótimos Locais?", ACCENT_AMBER)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Embasamento: Kirkpatrick, Gelatt e Vecchi (1983) — analogia com o recozimento térmico de metais.\n\n• O Problema do Hill Climbing:\n  A busca gulosa fica presa em ótimos locais (soluções com janelas que não melhoram por troca direta).\n\n• O Critério de Metropolis:\n  Permite aceitar soluções PIORES com probabilidade controlada pela temperatura T:\n     P(aceitar) = e^{-Δf / T}\n\n• Resfriamento geométrico: T_{k+1} = α · T_k (0.85 ≤ α ≤ 0.98)."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    add_content_card(s8, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1), "Operadores de Vizinhança (Perturbação)", ACCENT_BLUE)
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Operador 1: Troca Intra-Turma (Swap Move):\n  Permuta duas disciplinas em slots distintos da mesma turma. Preserva 100% da carga horária.\n\n• Operador 2: Deslocamento para Slot Livre (Move to Free):\n  Move aula para período livre adjacente, eliminando janelas docentes (gaps).\n\n• Blindagem de Restrições Fortes:\n  Se a troca gerar choque de professor, o movimento é sumariamente rejeitado (P = 0).\n  A busca opera estritamente dentro da região viável!"
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 9: SÍNTESE COMPARATIVA & CONCLUSÃO
    # -------------------------------------------------------------
    s9 = create_slide_base("5. Conclusão", "Síntese Comparativa e o Framework em Dois Estágios")
    add_content_card(s9, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1), "Comparativo Técnico das Abordagens e Encerramento", ACCENT_GREEN)
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(11.1), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "QUADRO COMPARATIVO DAS HEURÍSTICAS:\n\n• Algoritmo 1 (DSatur Construtivo): Construtivo Determinístico | Fase 1 (Warm Start) | Foco: Hard = 0 | Complexidade: O(N log N) (< 100ms) | Sem escape de ótimo local.\n\n• Algoritmo 2 (Simulated Annealing): Metaheurística Estocástica de Trajetória | Fase 2 (Polimento Suave) | Foco: Soft (Gaps e Equilíbrio) | Operador: Swap Moves | Escape via Metropolis (e^{-Δf/T}).\n\nCONCLUSÃO:\nO paradigma híbrido em dois estágios resolve com perfeição o School Timetabling Problem: o DSatur contorna a barreira da explosão combinatória eliminando todos os choques em milissegundos, enquanto o Simulated Annealing refina a ergonomia da grade docente, garantindo respeito à saúde do professor."
    for p in tf.paragraphs:
        p.font.name = "Arial"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    out_path = r"c:\Users\Kauê\Documents\02_Programacao_e_Tech\Projetos\TimeTabling\docs\apresentacoes\apresentacao-seminario-timetabling.pptx"
    prs.save(out_path)
    print("Sucesso! Apresentação 100% compatível gerada em:", out_path)

if __name__ == "__main__":
    build_presentation()
