import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_abnt_docx():
    doc = docx.Document()

    # Configuração de Margens ABNT NBR 14724: Sup 3cm, Esq 3cm, Dir 2cm, Inf 2cm
    for section in doc.sections:
        section.top_margin = Cm(3.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)

    # Estilo Normal
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Arial'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ---------------------------------------------------------
    # CAPA ABNT
    # ---------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.line_spacing = 1.3
    r = p_inst.add_run("CENTRO UNIVERSITÁRIO GERALDO DI BIASE – UGB\nCURSO DE ENGENHARIA DE SOFTWARE\nDISCIPLINA: LABORATÓRIO DE PROGRAMAÇÃO (6º PERÍODO)")
    r.bold = True
    r.font.size = Pt(12)

    for _ in range(6):
        doc.add_paragraph()

    p_autores = doc.add_paragraph()
    p_autores.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_autores.add_run("KAUÊ LORENO LOPES\nPEDRO HENRIQUE DIAS DORNELLAS\nLUCAS SANTANA")
    r.bold = True
    r.font.size = Pt(12)

    for _ in range(7):
        doc.add_paragraph()

    p_titulo = doc.add_paragraph()
    p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_titulo.paragraph_format.line_spacing = 1.3
    r = p_titulo.add_run("ABORDAGEM HEURÍSTICA PARA O PROBLEMA DE ALOCAÇÃO DE HORÁRIOS ESCOLARES\n")
    r.bold = True
    r.font.size = Pt(14)
    r_sub = p_titulo.add_run("Modelagem Matemática Formal, Espaço de Busca e Framework de Resolução em Dois Estágios (School Timetabling Problem)")
    r_sub.font.size = Pt(12)

    for _ in range(4):
        doc.add_paragraph()

    # Natureza do trabalho
    p_natureza = doc.add_paragraph()
    p_natureza.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_natureza.paragraph_format.left_indent = Cm(8.0)
    p_natureza.paragraph_format.line_spacing = 1.15
    r_nat = p_natureza.add_run(
        "Relatório Técnico-Científico apresentado à disciplina de Laboratório de Programação do Curso de Engenharia de Software "
        "como requisito parcial de avaliação acadêmica.\n\n"
        "Professor Orientador: Prof. Me. Marcelo Arantes de Oliveira"
    )
    r_nat.font.size = Pt(10)

    for _ in range(6):
        doc.add_paragraph()

    p_rodape = doc.add_paragraph()
    p_rodape.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rod = p_rodape.add_run("VOLTA REDONDA – RJ\n2026")
    r_rod.bold = True
    r_rod.font.size = Pt(11)

    doc.add_page_break()

    # ---------------------------------------------------------
    # SUMÁRIO
    # ---------------------------------------------------------
    p_sum_title = doc.add_paragraph()
    p_sum_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_sum_title.add_run("SUMÁRIO")
    r.bold = True
    r.font.size = Pt(12)

    itens_sumario = [
        ("1 INTRODUÇÃO E CONTEXTUALIZAÇÃO DO PROBLEMA", "03"),
        ("2 SEÇÃO A: MODELAGEM MATEMÁTICA FORMAL", "04"),
        ("   2.1 Definição dos Conjuntos e Parâmetros", "04"),
        ("   2.2 Variáveis de Decisão", "04"),
        ("   2.3 Espaço de Busca Combinatório e Teoria da Complexidade", "05"),
        ("3 SEÇÃO B: METODOLOGIA (RESTRIÇÕES E FUNÇÃO DE AVALIAÇÃO)", "06"),
        ("   3.1 Restrições Fortes (Hard Constraints)", "06"),
        ("   3.2 Restrições Fracas (Soft Constraints)", "06"),
        ("   3.3 Função de Aptidão / Custo (Fitness Function)", "07"),
        ("4 SEÇÃO C: HEURÍSTICAS E METAHEURÍSTICAS ADOTADAS", "08"),
        ("   4.1 Fase 1: Heurística Construtiva Inspirada em Saturação", "08"),
        ("   4.2 Fase 2: Metaheurística de Busca Local (Simulated Annealing)", "09"),
        ("   4.3 Síntese Comparativa das Abordagens", "10"),
        ("   4.4 Análise Teórica: Limites de Custo, Metropolis e Viabilidade", "10"),
        ("5 CONSIDERAÇÕES FINAIS", "11"),
        ("REFERÊNCIAS", "12")
    ]

    for item, pag in itens_sumario:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.line_spacing = 1.3
        p_item.paragraph_format.space_after = Pt(2)
        r1 = p_item.add_run(item)
        if not item.startswith("   "):
            r1.bold = True
        r2 = p_item.add_run(f"  {pag}")
        r2.bold = True

    doc.add_page_break()

    # Funções auxiliares de títulos
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.left_indent = Cm(0)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(12)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Cm(0)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(12)

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0)
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(text)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Cm(1.5)
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(text)
        return p

    # ---------------------------------------------------------
    # 1 INTRODUÇÃO
    # ---------------------------------------------------------
    add_h1("1 INTRODUÇÃO E CONTEXTUALIZAÇÃO DO PROBLEMA")

    add_p(
        "O Problema de Alocação de Horários Escolares (formalmente designado na literatura científica por School Timetabling Problem - STP) "
        "compreende a tarefa operacional e pedagógica de distribuir um conjunto de aulas curriculares ministradas por docentes específicos a turmas fixas, "
        "ao longo de uma grade semanal finita e estruturada de horários (time slots), sujeita a severas restrições humanas e físicas."
    )

    add_p(
        "Trata-se de um problema canônico de otimização combinatória classificado como NP-difícil (a versão de decisão é NP-completa) (EVEN; ITAI; SHAMIR, 1976). "
        "Na prática administrativa da expressiva maioria das instituições de ensino básico, técnico e superior, a elaboração da grade é historicamente conduzida "
        "de forma manual por coordenadores de curso. Esse processo puramente artesanal consome tempo considerável da gestão e resulta sistematicamente em falhas operacionais, "
        "tais como choques acidentais de turmas ou professores e grades com janelas vagas ociosas (gaps) entre períodos."
    )

    add_p(
        "Conforme discutem Tardif e Lessard (2014), a fragmentação da jornada diária e a presença recorrente de janelas desnecessárias na grade docente constituem "
        "fatores de estresse, absenteísmo e precarização do trabalho dos professores, afetando sensivelmente a qualidade do ambiente escolar."
    )

    add_p(
        "Sob a perspectiva da Teoria da Computação, tentativas de solucionar instâncias reais de agendamento por meio de métodos determinísticos de força bruta "
        "ou formulações puras de Programação Linear Inteira Mista (MILP) esbarram na barreira da explosão combinatória: o número de variáveis binárias cresce exponencialmente, "
        "podendo levar ao esgotamento de memória em árvores de Branch-and-Bound e dificultar a obtenção de soluções em tempo hábil para instâncias reais de médio e grande porte."
    )

    add_p(
        "Por esse motivo, o estado da arte internacional consagrou o uso de Heurísticas Construtivas e Metaheurísticas de Busca Local organizadas sob o paradigma híbrido "
        "em dois estágios (BURKE et al., 1998; LEWIS, 2008). O presente relatório formaliza a modelagem matemática e os algoritmos desenvolvidos para o motor do sistema "
        "TimeTabling, projetado para buscar grades sem violações rígidas e proporcionar conforto ergonômico aos professores."
    )

    # ---------------------------------------------------------
    # 2 SEÇÃO A: MODELAGEM MATEMÁTICA
    # ---------------------------------------------------------
    add_h1("2 SEÇÃO A: MODELAGEM MATEMÁTICA FORMAL")

    add_p(
        "A modelagem matemática visa converter as regras pedagógicas e contratuais da instituição em entidades discretas, conjuntos formais e variáveis de decisão."
    )

    add_h2("2.1 DEFINIÇÃO DOS CONJUNTOS E PARÂMETROS")
    add_p("O universo do problema é delimitado a partir dos seguintes conjuntos e parâmetros discretos:")

    add_bullet("Conjunto de Turmas (T): T = {t₁, t₂, ..., t_|T|}, representando as classes curriculares de alunos.")
    add_bullet("Conjunto de Professores (P): P = {p₁, p₂, ..., p_|P|}, representando o corpo docente cadastrado.")
    add_bullet("Conjunto de Disciplinas (D): D = {d₁, d₂, ..., d_|D|}, representando as matérias da matriz curricular.")
    add_bullet("Conjunto de Dias da Semana (Dia): Dia = {1, 2, 3, 4, 5}, correspondendo à jornada de segunda a sexta-feira (|Dia| = 5).")
    add_bullet("Conjunto de Períodos Diários (S): S = {1, 2, ..., |S|}, onde cada período representa uma aula unitária (fixado em |S| = 5 períodos diários).")
    add_bullet("Conjunto Global de Slots Semanais (K): K = Dia × S, perfazendo |K| = |Dia| · |S| = 25 posições temporais na semana.")
    add_bullet("Carga Horária Semanal (CH): CH(t, d) ∈ ℕ, determinando a quantidade de períodos que a turma t deve cursar da matéria d.")
    add_bullet("Atribuição Docente (Prof): Função Prof(t, d) = p que associa cada disciplina da turma ao seu professor responsável.")
    add_bullet("Disponibilidade Docente (Disp): Tensor binário indicando disponibilidade temporal, onde Disp_{p, dia, s} = 1 se o docente p está liberado no dia dia e período s; 0 se há restrição contratual ou bloqueio.")
    add_bullet("Preferência Docente (Pref): Pref(p) ⊆ Dia, o subconjunto de dias livres que o professor prefere lecionar. Dias com restrição ou bloqueio correspondem a Disp = 0.")

    add_h2("2.2 VARIÁVEIS DE DECISÃO")
    add_p(
        "A atribuição de uma aula na grade horária é formalmente controlada por uma variável de decisão binária multidimensional:"
    )

    p_eq = doc.add_paragraph()
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_eq.add_run("x_{t, p, d, dia, s} ∈ {0, 1}")
    r.bold = True

    add_p(
        "onde x_{t, p, d, dia, s} = 1 se a aula da matéria d, lecionada pelo professor p para a turma t, for posicionada no dia dia durante o período s; "
        "caso contrário, x_{t, p, d, dia, s} = 0. Como a disciplina de uma turma possui um único docente pré-designado pela matriz curricular (Prof(t, d) = p), "
        "a representação simplifica-se sem perda de generalidade para x_{t, d, dia, s} ∈ {0, 1}. Para diferenciar a solução completa de horários do conjunto S de períodos diários, "
        "adota-se a notação 𝒢 para designar uma grade horária candidata."
    )

    add_h2("2.3 ESPAÇO DE BUSCA COMBINATÓRIO E TEORIA DA COMPLEXIDADE")
    add_p(
        "O espaço de busca combinatório Ω reúne todas as permutações possíveis de alocação de aulas nos horários da semana:"
    )

    add_bullet("Seja N o total de aulas letivas demandadas pela totalidade das turmas: N = ∑_{t ∈ T} ∑_{d ∈ D} CH(t, d).")
    add_bullet("Para cada uma das N aulas, existem |K| = |Dia| × |S| = 25 slots temporais elegíveis na semana.")
    add_bullet("Dessa forma, a cardinalidade do espaço de soluções bruto (como um limite superior irrestrito) é expressa por: |Ω| = (|Dia| × |S|)^N = 25^N.")

    add_p(
        "Magnitude Combinatória: Para uma instituição modesta com apenas 10 turmas e 25 aulas semanais por turma (N = 250 aulas), "
        "o espaço bruto atinge |Ω| = 25²⁵⁰ ≈ 3,05 × 10³⁴⁹ (ordem de 10³⁵⁰), muito acima da estimativa de 10⁸⁰ átomos do universo observável, "
        "o que inviabiliza a busca exaustiva por força bruta."
    )

    add_p(
        "A intratabilidade é estabelecida por Even, Itai e Shamir (1976), que demonstraram que a versão de decisão do problema de horários é NP-completa; "
        "logo, a otimização correspondente é NP-difícil. Há semelhança estrutural com a coloração de vértices (KARP, 1972), em que aulas são vértices, conflitos são arestas "
        "e horários são cores, mas este trabalho não apresenta uma redução formal."
    )

    # ---------------------------------------------------------
    # 3 SEÇÃO B: METODOLOGIA
    # ---------------------------------------------------------
    add_h1("3 SEÇÃO B: METODOLOGIA (RESTRIÇÕES E FUNÇÃO DE AVALIAÇÃO)")

    add_h2("3.1 RESTRIÇÕES FORTES (HARD CONSTRAINTS)")
    add_p(
        "As restrições fortes são condições inegociáveis. Se houver ao menos uma violação, a grade é considerada inválida e inutilizável na realidade:"
    )

    add_bullet("1. Unicidade Docente: Um professor não pode lecionar em mais de uma turma no mesmo período:\n   ∑_{t ∈ T} ∑_{d ∈ D} x_{t, p, d, dia, s} ≤ 1,  ∀ p ∈ P, dia ∈ Dia, s ∈ S")
    add_bullet("2. Unicidade de Turma: Uma turma não pode ter aulas simultâneas de matérias distintas:\n   ∑_{p ∈ P} ∑_{d ∈ D} x_{t, p, d, dia, s} ≤ 1,  ∀ t ∈ T, dia ∈ Dia, s ∈ S")
    add_bullet("3. Respeito aos Bloqueios de Agenda: Nenhuma aula pode ser alocada em horários bloqueados:\n   x_{t, p, d, dia, s} ≤ Disp_{p, dia, s},  ∀ t, p, d, dia, s")
    add_bullet("4. Integralidade da Carga Horária Curricular: Todas as aulas devem ser integralmente alocadas:\n   ∑_{dia ∈ Dia} ∑_{s ∈ S} x_{t, Prof(t,d), d, dia, s} = CH(t, d),  ∀ t ∈ T, d ∈ D")

    add_h2("3.2 RESTRIÇÕES FRACAS (SOFT CONSTRAINTS)")
    add_p(
        "As restrições flexíveis não inviabilizam a grade, mas mensuram sua qualidade pedagógica e ergonômica:"
    )

    add_bullet("1. Minimização de Janelas Vagas Docentes (Teacher Gaps): Penaliza intervalos ociosos na jornada diária do professor. Sendo s_min e s_max o primeiro e o último horário de aula do docente no dia: Gap(p, dia) = (s_max - s_min + 1) - TotalAulas(p, dia). Em dias sem aulas, adota-se estritamente Gap(p, dia) = 0.")
    add_bullet("2. Equilíbrio Diário de Disciplinas: Evita que os estudantes tenham mais de 2 aulas da mesma disciplina no mesmo dia, prevenindo a estafa cognitiva: Excesso(t, d, dia) = max(0, ∑_{s ∈ S} x_{t, Prof(t,d), d, dia, s} - 2).")
    add_bullet("3. Preferências Docentes: Penaliza aulas alocadas em dia livre que não seja preferido pelo professor: Pen_pref = ∑ x_{t, Prof(t,d), d, dia, s} sobre os dias pertencentes a Livre(p) \\ Pref(p). Cada aula nessa condição contribui com no máximo 1 ponto de penalidade.")

    add_h2("3.3 FUNÇÃO DE APTIDÃO / CUSTO (FITNESS FUNCTION)")
    add_p(
        "A qualidade de uma grade 𝒢 ∈ Ω é mensurada por uma função escalar de custo a ser minimizada, penalizando severamente qualquer violação dura:"
    )

    p_fit = doc.add_paragraph()
    p_fit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_fit.add_run("f(𝒢) = W_hard · ∑_{i ∈ Hard} H_i(𝒢) + ∑_{j ∈ Soft} w_j · V_j(𝒢)")
    r.bold = True

    add_p(
        "onde H_i(𝒢) contabiliza choques rígidos e V_j(𝒢) as penalidades suaves. Os pesos adotados no sistema são:\n"
        "• W_hard = 100.000 (penalidade dissuasiva extrema para choques e bloqueios);\n"
        "• w_gap = 85 (penalidade por janela ociosa de professor);\n"
        "• w_balance = 70 (penalidade por excesso diário de aulas da mesma matéria);\n"
        "• w_pref = 50 (penalidade por dia não preferido, valor proposto a calibrar)."
    )

    add_p(
        "Condição Formal de Viabilidade: Uma grade é viável se e somente se ∑ H_i = 0. "
        "Se o custo soft máximo de toda grade viável for comprovadamente menor que W_hard, vale também a equivalência f(𝒢) < W_hard ⟺ Viável."
    )

    add_p(
        "Proposição: Para toda grade viável, custo soft ≤ 1.275 · |P| + 1.050 · |T| + w_pref · N. "
        "A demonstração formal e numérica dessa cota superior é apresentada na Seção 4.4."
    )

    # ---------------------------------------------------------
    # 4 SEÇÃO C: HEURÍSTICAS E METAHEURÍSTICAS
    # ---------------------------------------------------------
    add_h1("4 SEÇÃO C: HEURÍSTICAS E METAHEURÍSTICAS ADOTADAS")

    add_p(
        "O sistema adota o paradigma consolidado de Resolução em Dois Estágios (BURKE et al., 1998; LEWIS, 2008): a Fase 1 busca viabilidade física estrita (Hard = 0), "
        "e a Fase 2 atua no refinamento ergonômico (Soft)."
    )

    add_h2("4.1 FASE 1: HEURÍSTICA CONSTRUTIVA INSPIRADA EM SATURAÇÃO")
    add_p(
        "Funcionamento Teórico: Inspirado no clássico princípio de saturação de grafos (BRÉLAZ, 1979) e em estratégias heurísticas para agendamento educacional "
        "(CARTER; LAPORTE; LEE, 1996), este método aplica uma abordagem construtiva baseada na filosofia 'Fail-First' (Falhe Primeiro). "
        "A ordenação é estática; não há recálculo dinâmico da saturação a cada passo, portanto não se trata do DSatur clássico, mas sim de uma adaptação gulosa estática de alto desempenho."
    )

    add_p("Mecanismo de Busca:")
    add_bullet("1. As aulas são ordenadas previamente de forma decrescente pela função de criticidade: Criticidade(d) = α · CH(t, d) + β · (1 - Disp), onde CH(t, d) é a carga semanal da matéria, Disp representa a fração de slots livres do docente na semana (número de slots livres dividido por 25), e α e β são pesos de ajuste.")
    add_bullet("2. O motor percorre a lista ordenada e consulta a matriz em memória RAM (GridState).")
    add_bullet("3. Aloca a aula no primeiro slot compatível (dia, s) livre para a turma e professor sem violar bloqueios.")
    add_bullet("4. Custo Computacional: A ordenação inicial requer O(N log N) e a busca linear no grid consome O(N · |K|); como o número de slots semanais |K| = 25 é constante, a complexidade total assintótica é O(N log N). Para uma instância com N = 250 aulas, isso representa da ordem de 10⁴ operações elementares (análise teórica, sem benchmark formal).")

    add_p(
        "Limitação Teórica: Sem mecanismos de reparo ou retrocesso (backtracking), o método puramente guloso não garante viabilidade em toda instância arbitrária. "
        "Duas condições necessárias fundamentais, verificáveis preliminarmente em tempo linear O(N), são: (a) a carga horária semanal total de cada turma deve ser ≤ 25 períodos; "
        "e (b) a carga horária de cada professor deve ser ≤ ao seu número total de slots livres cadastrados."
    )

    add_h2("4.2 FASE 2: METAHEURÍSTICA DE BUSCA LOCAL (SIMULATED ANNEALING)")
    add_p(
        "Funcionamento Teórico: Inspirado na termodinâmica estatística (METROPOLIS et al., 1953; KIRKPATRICK et al., 1983), o Simulated Annealing (SA) "
        "supera a limitação de buscas gulosas simples (Hill Climbing), que estagnam em ótimos locais. O SA possui a propriedade matemática de aceitar soluções "
        "temporariamente piores para escapar de armadilhas combinatórias."
    )

    add_p(
        "A probabilidade de transição para estados com custo superior (Δf = f(𝒢_novo) - f(𝒢_atual) > 0) segue o Critério de Metropolis:"
    )

    p_met = doc.add_paragraph()
    p_met.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_met.add_run("P(aceitar piora) = e^{-Δf / T}")
    r.bold = True

    add_p(
        "onde T é a temperatura corrente. Parâmetros propostos (a calibrar): Temperatura inicial T₀ = 100, temperatura final T_final = 1, taxa de resfriamento geométrico "
        "λ = 0,95 (resultando em cerca de 90 níveis térmicos) e 250 iterações por temperatura (totalizando cerca de 22.500 avaliações). "
        "Nota-se que se pode manter a notação tradicional T_{k+1} = α · T_k com α = 0,95, tratando-se do mesmo símbolo usado na criticidade, porém em contextos distintos."
    )

    add_p("Estratégias de Geração de Vizinhança e Perturbação:")
    add_bullet("Operador 1 - Troca Intra-Turma (Swap Move): Permuta os horários de duas aulas distintas da mesma turma. Garante preservação integral da carga horária semanal.")
    add_bullet("Operador 2 - Deslocamento para Slot Livre (Move to Free Slot): Move uma aula para um período vago adjacente à outra aula do mesmo professor, aplicável apenas a turmas que possuam slots livres na grade.")
    add_bullet("Blindagem Rígida de Viabilidade: Qualquer movimento de vizinhança que induza violações de restrições rígidas — incluindo violações de disponibilidade declarada e choque de professor em outra turma — é sumariamente descartado (P = 0), garantindo que a busca estocástica opere exclusivamente no espaço de grades viáveis.")

    add_h2("4.3 SÍNTESE COMPARATIVA DAS ABORDAGENS")

    # Tabela ABNT
    p_tab_caption = doc.add_paragraph()
    p_tab_caption.paragraph_format.left_indent = Cm(0)
    p_tab_caption.paragraph_format.space_after = Pt(2)
    r = p_tab_caption.add_run("Tabela 1 – Comparativo técnico das abordagens algorítmicas adotadas.")
    r.bold = True
    r.font.size = Pt(10)

    table = doc.add_table(rows=7, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ["Critério de Análise", "Fase 1: Construtiva Inspirada em Saturação", "Fase 2: Simulated Annealing"]
    data = [
        ["Família Algorítmica", "Heurística Construtiva Determinística", "Metaheurística Estocástica de Trajetória"],
        ["Estágio de Execução", "Fase 1 (Inicialização / Warm Start)", "Fase 2 (Polimento de Qualidade Suave)"],
        ["Objetivo Primário", "Viabilidade física estrita (Hard = 0)", "Minimização de janelas e preferências (Soft)"],
        ["Estado de Partida", "Grade completamente vazia (∅)", "Grade viável gerada pela Fase 1"],
        ["Complexidade Temporal", "O(N log N) (análise teórica)", "O(Iterações × Custo(Δf))"],
        ["Tratamento de Ótimo Local", "Inexistente (decisão estática)", "Escape via Metropolis (sem garantia de ótimo global)"]
    ]

    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = text
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.bold = True
            run.font.size = Pt(9.5)

    for row_idx, row_data in enumerate(data):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = text
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)

    p_fonte = doc.add_paragraph()
    p_fonte.paragraph_format.left_indent = Cm(0)
    p_fonte.paragraph_format.space_before = Pt(2)
    p_fonte.paragraph_format.space_after = Pt(12)
    r = p_fonte.add_run("Fonte: Elaborado pelos autores (2026).")
    r.font.size = Pt(9)

    add_h2("4.4 ANÁLISE TEÓRICA: LIMITES DE CUSTO, METROPOLIS E PRESERVAÇÃO DA VIABILIDADE")

    add_p(
        "1. Limite Superior do Custo Soft: Em uma jornada semanal estruturada em |Dia| = 5 e |S| = 5 períodos diários, "
        "o número máximo de janelas ociosas que um docente pode sofrer em um único dia ocorre quando ele leciona apenas no slot 1 e no slot 5, "
        "perfazendo Gap(p, dia) ≤ 3 janelas/dia. Para os 5 dias da semana, a quantidade acumulada de janelas é limitada por 3 × 5 = 15 janelas por professor. "
        "Analogamente, para cada turma, o excesso máximo de períodos da mesma matéria em um dia é de 3 (caso as 5 aulas do dia sejam da mesma disciplina), "
        "limitando a penalidade a no máximo 15 por turma na semana. Considerando que a penalidade de dia não preferido é no máximo 1 por aula (totalizando N), "
        "o custo suave total é estritamente limitado por:\n"
        "Custo Soft ≤ 85 · (15 · |P|) + 70 · (15 · |T|) + w_pref · N = 1.275 · |P| + 1.050 · |T| + 50 · N."
    )

    add_p(
        "Exemplo Numérico de Validação: Para um cenário acadêmico com |T| = 10 turmas, |P| = 20 professores e N = 250 aulas semanais, temos:\n"
        "Custo Soft ≤ 1.275 · (20) + 1.050 · (10) + 50 · (250) = 25.500 + 10.500 + 12.500 = 48.500.\n"
        "Como 48.500 < 100.000, comprova-se formalmente que, para este cenário, nenhuma grade viável atingirá custo superior a W_hard, "
        "assegurando a equivalência f(𝒢) < W_hard ⟺ Viável."
    )

    add_p(
        "2. Comportamento do Critério de Metropolis: Para uma piora isolada induzida por uma janela docente adicional (Δf = 85), "
        "a probabilidade de aceitação varia dinamicamente segundo a temperatura corrente T:\n"
        "• Na temperatura inicial T = 100: P = e^{-85 / 100} = e^{-0,85} ≈ 0,427 (aproximadamente 43% de chance de aceitação, promovendo ampla exploração);\n"
        "• Na temperatura intermediária T = 10: P = e^{-85 / 10} = e^{-8,5} ≈ 2,03 × 10⁻⁴ (baixa tolerância a pioras);\n"
        "• Na temperatura final T = 1: P = e^{-85 / 1} ≈ 1,2 × 10⁻³⁷ (probabilidade virtualmente nula, convergindo estritamente para o mínimo local).\n"
        "Em contrapartida, qualquer tentativa de perturbação que induza uma violação rígida acarreta Δf ≥ 100.000, "
        "gerando P = e^{-100.000 / T} ≈ 0 para qualquer T operacional, eliminando o risco de escape para regiões inviáveis."
    )

    add_p(
        "3. Preservação Rigorosa da Viabilidade: Como a Fase 2 rejeita compulsoriamente qualquer movimento com violação hard (P = 0), "
        "a metaheurística parte de uma semente viável com Hard = 0 fornecida pela Fase 1 e preserva essa viabilidade estrita durante todas as 22.500 avaliações de busca local."
    )

    # ---------------------------------------------------------
    # 5 CONSIDERAÇÕES FINAIS
    # ---------------------------------------------------------
    add_h1("5 CONSIDERAÇÕES FINAIS")

    add_p(
        "A formalização matemática e a estruturação em dois estágios proposta neste relatório propõem uma arquitetura para tratar "
        "o School Timetabling Problem de forma heurística, articulando uma formulação rigorosa de variáveis de decisão com restrições "
        "fortes e critérios de conforto pedagógico. A integração entre a heurística construtiva na Fase 1 e a metaheurística de Simulated Annealing "
        "na Fase 2 busca atender tanto a integridade matemática da grade quanto a ergonomia e saúde do trabalho docente."
    )

    add_p(
        "Limitações e Trabalhos Futuros: Ressalta-se que o presente estudo constitui uma proposta formal e teórica, sem validação experimental ampla. "
        "Como passos subsequentes para a continuidade da pesquisa, estabelecem-se: (a) a execução de benchmarks computacionais formais sobre instâncias reais de ensino; "
        "(b) a calibração empírica dos pesos (w_gap, w_balance, w_pref) e parâmetros de resfriamento térmico através de análise de sensibilidade; "
        "e (c) a comparação sistemática de qualidade e tempo de resposta frente a solucionadores exatos de Programação Linear Inteira e algoritmos genéticos híbridos."
    )

    # ---------------------------------------------------------
    # REFERÊNCIAS
    # ---------------------------------------------------------
    add_h1("REFERÊNCIAS")

    referencias = [
        "BRÉLAZ, Daniel. New methods to color the vertices of a graph. Communications of the ACM, New York, v. 22, n. 4, p. 251-256, 1979.",
        "BURKE, Edmund K.; NEWALL, J. P.; WEARE, R. F. Initialization strategies and diversity in evolutionary timetabling. Evolutionary Computation, Cambridge, v. 6, n. 1, p. 81-103, 1998.",
        "CARTER, Michael W.; LAPORTE, Gilbert; LEE, S. Y. Examination timetabling: algorithmic strategies and applications. Journal of the Operational Research Society, London, v. 47, n. 3, p. 373-383, 1996.",
        "EVEN, Shimon; ITAI, Alon; SHAMIR, Adi. On the complexity of timetable and multicommodity flow problems. SIAM Journal on Computing, Philadelphia, v. 5, n. 4, p. 691-703, 1976.",
        "KARP, Richard M. Reducibility among Combinatorial Problems. In: MILLER, Raymond E.; THATCHER, James W. (Ed.). Complexity of Computer Computations. New York: Plenum Press, 1972. p. 85-103.",
        "KIRKPATRICK, Scott; GELATT, C. Daniel; VECCHI, Mario P. Optimization by simulated annealing. Science, Washington, v. 220, n. 4598, p. 671-680, 1983.",
        "LEWIS, Rhydian. A survey of metaheuristic-based techniques for university timetabling problems. OR Spectrum, Heidelberg, v. 30, n. 1, p. 167-190, 2008.",
        "METROPOLIS, Nicholas; ROSENBLUTH, Arianna W.; ROSENBLUTH, Marshall N.; TELLER, Augusta H.; TELLER, Edward. Equation of state calculations by fast computing machines. The Journal of Chemical Physics, Melville, v. 21, n. 6, p. 1087-1092, 1953.",
        "PILLAY, Nelishia. A survey of school timetabling research. Annals of Operations Research, Dordrecht, v. 218, n. 1, p. 261-293, 2014.",
        "SCHAERF, Andrea. A survey of automated timetabling. Artificial Intelligence Review, Dordrecht, v. 13, n. 2, p. 87-127, 1999.",
        "TARDIF, Maurice; LESSARD, Claude. O trabalho docente: elementos para uma teoria da docência como profissão de interações humanas. 9. ed. Petrópolis: Vozes, 2014."
    ]

    for ref in referencias:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Cm(0)
        p_ref.paragraph_format.line_spacing = 1.0
        p_ref.paragraph_format.space_after = Pt(8)
        p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ref.add_run(ref)

    out_docx = r"c:\Users\Kauê\Documents\02_Programacao_e_Tech\Projetos\TimeTabling\docs\relatorio-tecnico-heuristica-abnt.docx"
    doc.save(out_docx)
    print("DOCX gerado com sucesso em:", out_docx)

if __name__ == "__main__":
    create_abnt_docx()
