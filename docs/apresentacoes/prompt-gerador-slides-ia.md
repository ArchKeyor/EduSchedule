# 🚀 Prompt Mestre para Geração de Apresentação em IA

> **Como usar:** Copie todo o conteúdo do bloco de código abaixo e cole diretamente na IA que você for usar para gerar seus slides (como **Gamma.app**, **ChatGPT / Canvas**, **Claude 3.7**, **Tome.app** ou **Beautiful.ai**).  
> O prompt já contém todo o conteúdo mastigado, estrutura modular, equações, autores canônicos e o roteiro exato de cada um dos 9 slides.

---

```markdown
Você é um Designer Sênior de Apresentações Acadêmicas e Pesquisador Especialista em Otimização Combinatória e Engenharia de Software.

Sua tarefa é gerar uma apresentação de slides de alto impacto visual e rigor acadêmico para um seminário universitário de 10 a 12 minutos.

====================================================================
DADOS DE CONTEXTO E CABEÇALHO DO PROJETO:
====================================================================
- Tema: Abordagem Heurística para o Problema de Alocação de Horários Escolares (School Timetabling Problem - STP)
- Instituição: Centro Universitário Geraldo Di Biase (UGB) — Volta Redonda, RJ
- Curso: Engenharia de Software (6º Período)
- Disciplina: Laboratório de Programação
- Professor Avaliador: Me. Marcelo Arantes de Oliveira
- Equipe de Apresentadores: 
  * Kauê Loreno Lopes (Tech Lead & Engenheiro de Otimização)
  * Pedro Henrique Dias Dornellas (Engenheiro Frontend UI)
  * Lucas Santana (Engenheiro Backend & Dados)

====================================================================
DIRETRIZES DE DESIGN SYSTEM E FORMATAÇÃO:
====================================================================
1. Formato: 16:9 Widescreen;
2. Quantidade Exata: Exatamente 10 Slides (incluindo diagramas visuais e explicativos dos dois algoritmos);
3. Estrutura Modular: Sem blocos corridos de texto. Use cards modulares com bordas coloridas, bullet points objetivos, destaque de equações e tabelas comparativas;
4. Separação de Restrições: O Slide 4 é EXCLUSIVO para Restrições Fortes (Hard Constraints) e o Slide 5 é EXCLUSIVO para Restrições Fracas (Soft Constraints);
5. Rigor Teórico: Manter expressamente as citações de autores canônicos (Karp 1972, Even et al. 1976, Brélaz 1979, Carter, Laporte & Lee 1996, Metropolis et al. 1953, Kirkpatrick et al. 1983, Lewis 2008, Pillay 2014, Schaerf 1999, Tardif & Lessard 2014);
6. Paleta Recomendada: Base escura/navy ou off-white limpo com acentos em Azul Real, Verde Esmeralda, Âmbar e Vermelho para alertas.

====================================================================
CONTEÚDO SLIDE A SLIDE (ESTRUTURA COMPLETA E DETALHADA):
====================================================================

---
[SLIDE 1/9] Capa Oficial Institucional
• Layout: Centralizado, elegante, alto contraste.
• Tag Superior: CENTRO UNIVERSITÁRIO GERALDO DI BIASE (UGB) • VOLTA REDONDA - RJ
• Título Principal: Abordagem Heurística para o Problema de Alocação de Horários Escolares
• Subtítulo Técnico: Modelagem Matemática Formal, Espaço de Busca e Framework de Resolução em Dois Estágios (School Timetabling Problem)
• Metadados:
  - Disciplina: Laboratório de Programação (6º Período)
  - Professor Orientador: Me. Marcelo Arantes de Oliveira
  - Equipe: Kauê Loreno Lopes • Pedro Henrique Dias Dornellas • Lucas Santana
• Notas do Orador: Abertura formal de 30 segundos apresentando a equipe, a disciplina e o tema da modelagem matemática.

---
[SLIDE 2/9] 1. Contextualização Teórica: O Problema e a Explosão Combinatória
• Layout: 2 Colunas (Cards lado a lado).
• Card Esquerdo (Azul): "O Desafio Real nas Instituições de Ensino"
  - O que é: Alocar semanalmente aulas entre turmas fixas e professores em grade de períodos finita.
  - O Gargalo: Processo puramente manual por coordenadores, consumindo semanas exaustivas.
  - Relevância Humana & Saúde Docente: Grades mal distribuídas geram janelas vagas (gaps). Tardif & Lessard (2014) apontam e discutem a fragmentação da jornada docente como um fator direto de estresse, absenteísmo e precarização do trabalho.
• Card Direito (Âmbar/Alerta): "A Barreira Matemática (Por que Força Bruta Falha?)"
  - Classificação Formal: Problema NP-Difícil (NP-Hard), comprovado por Even, Itai e Shamir (1976).
  - Relação Teórica: O School Timetabling generaliza o problema clássico de Coloração de Vértices de Grafos (Graph Vertex Coloring - Karp, 1972).
  - Limite Superior Bruto do Espaço de Busca: Com 25 slots na semana e N aulas a alocar, o limite superior bruto é 25^N.
  - Para 10 turmas (N = 250 aulas), atinge 25^250 ≈ 10^350 combinações (muito superior aos 10^80 átomos do universo!).
  - Métodos exatos (MILP / Branch-and-Bound): Não escalam bem para instâncias reais de médio e grande porte devido à explosão combinatória. Heurísticas são indispensáveis.
• Notas do Orador: Enfatizar o impacto humano das janelas discutido por Tardif & Lessard e o limite superior astronômico de 10^350 que explica por que métodos exatos não escalam.

---
[SLIDE 3/9] 2. Seção A: Modelagem Matemática Formal e Variáveis de Decisão
• Layout: 2 Colunas (Conjuntos à esquerda, Variáveis à direita).
• Card Esquerdo (Azul): "Conjuntos e Parâmetros Discretos"
  - Turmas (T): Classes curriculares de alunos: T = {t_1, t_2, ..., t_|T|}
  - Professores (P): Corpo docente contratado: P = {p_1, p_2, ..., p_|P|}
  - Disciplinas (D): Matérias da matriz curricular: D = {d_1, d_2, ..., d_|D|}
  - Dias da Semana (Dia): Dia = {1, 2, 3, 4, 5} (5 dias úteis)
  - Períodos Diários (S): S = {1, 2, 3, 4, 5} (5 aulas diárias)
  - Grade Semanal (K): K = Dia × S (Total de 25 slots horários)
  - Carga Horária CH(t, d): Quantidade semanal de aulas obrigatórias da matéria
  - Matriz de Disponibilidade Disp(p, dia, s): 1 se o docente está livre; 0 se bloqueado
• Card Direito (Verde): "Variável de Decisão Binária Multidimensional"
  - Definição Formal:
    x_{t, p, d, dia, s} ∈ {0, 1}
  - Significado: Assume 1 se a turma 't' tem aula da disciplina 'd' com o professor 'p' no dia 'dia' e período 's'; 0 caso contrário.
  - Decisão de Arquitetura em Memória RAM:
    Como cada matéria da turma já possui um professor pré-atribuído Prof(t, d) = p, o tensor opera simplificado como x_{t, d, dia, s} ∈ {0, 1}, permitindo consultas e atualizações atômicas em tempo O(1).
• Notas do Orador: Explicar os 25 slots da grade e demonstrar segurança ao falar da variável de decisão binária e da otimização do tensor em memória.

---
[SLIDE 4/9] 3. Seção B: Metodologia — Restrições Fortes (Hard Constraints)
• Layout: Card Único Amplo com Destaque Vermelho/Alerta.
• Título do Card: "Condições Obrigatórias de Viabilidade Física e Matemática (Zero Conflitos)"
• Texto de Abertura: Se qualquer restrição forte for violada, a grade é sumariamente declarada INVÁLIDA e não pode ser aplicada na escola:
• As 4 Regras Invioláveis:
  1. UNICIDADE DOCENTE (Sem Choque de Professor):
     Um professor não pode dar aula para duas turmas no mesmo horário.
     Fórmula: ∑_{t} ∑_{d} x_{t, p, d, dia, s} ≤ 1,  ∀ p, dia, s
  2. UNICIDADE DE TURMA (Sem Choque de Horário da Turma):
     Uma turma não pode assistir a duas matérias simultâneas.
     Fórmula: ∑_{p} ∑_{d} x_{t, p, d, dia, s} ≤ 1,  ∀ t, dia, s
  3. RESPEITO À INDISPONIBILIDADE DOCENTE:
     Nenhuma aula pode ser alocada em períodos com restrição contratual/bloqueio declarado.
     Fórmula: x_{t, p, d, dia, s} ≤ Disp_{p, dia, s},  ∀ t, p, d, dia, s
  4. CUMPRIMENTO INTEGRAL DA CARGA HORÁRIA:
     100% das aulas previstas na matriz curricular devem ser alocadas semanalmente.
     Fórmula: ∑_{dia} ∑_{s} x_{t, Prof(t,d), d, dia, s} = CH(t, d),  ∀ t, d
• Notas do Orador: Frisar que as Hard Constraints garantem a física do mundo real: um professor não tem o dom da ubiquidade e não pode estar em duas salas ao mesmo tempo.

---
[SLIDE 5/9] 3. Seção B: Metodologia — Restrições Fracas (Soft Constraints)
• Layout: Card Único Amplo com Destaque Âmbar/Qualidade.
• Título do Card: "Critérios de Ergonomia Docente e Equilíbrio Didático-Pedagógico"
• Texto de Abertura: As restrições suaves NÃO invalidam a grade física, mas mensuram sua qualidade, conforto humano e excelência pedagógica:
• Os 3 Critérios de Qualidade:
  1. MINIMIZAÇÃO DE JANELAS VAGAS DOCENTES (Teacher Gaps) — Peso w_gap = 85:
     - Penaliza períodos ociosos intermediários entre a primeira e a última aula do professor no mesmo dia.
     - Métrica: Gap(p, dia) = (slot_max - slot_min + 1) - TotalAulas(p, dia).
     - Justificativa: Fundamentado em Tardif & Lessard para evitar fadiga crônica e tempo perdido na escola.
  2. EQUILÍBRIO DIÁRIO DE DISCIPLINAS (Daily Balance) — Peso w_balance = 70:
     - Evita que a mesma turma tenha mais de 2 aulas da mesma matéria no mesmo dia.
     - Métrica: Excesso(t, d, dia) = max(0, ∑_s x_{t,d,dia,s} - 2).
     - Justificativa: Previne estafa cognitiva dos alunos e dispersão de atenção.
  3. ATENDIMENTO A PREFERÊNCIAS DOCENTES:
     - Prioriza os turnos e dias da semana declarados como preferidos pelos professores em situações de empate de viabilidade.
• Notas do Orador: Explicar a diferença prática: Hard diz se a grade é possível; Soft diz se a grade é boa para os seres humanos envolvidos.

---
[SLIDE 6/9] 3. Seção B: Metodologia — Função de Aptidão (Fitness Function)
• Layout: Card Amplo com Destaque Central para a Equação de Custo.
• Título do Card: "Formulação Escalar da Função Objetivo de Minimização de Custo"
• Equação em Caixa de Destaque:
  f(S) = W_hard · ∑_{i ∈ Hard} H_i(S) + ∑_{j ∈ Soft} w_j · V_j(S)
• Detalhamento dos Componentes da Fórmula:
  - H_i(S): Contador de violações de restrições rígidas (choques de professor, turma ou bloqueios).
  - W_hard = 100.000: Peso de penalidade dissuasiva extrema. Torna a solução instantaneamente proibitiva.
  - V_j(S): Quantidade de violações de restrições suaves (janelas ociosas, excesso diário de aulas).
  - Pesos Calibrados no Motor do Sistema:
    * w_gap = 85 (penalidade por janela ociosa do professor)
    * w_balance = 70 (penalidade por excesso diário da mesma matéria)
• Critério Formal de Viabilidade:
  * Solução Viável (Feasible) ⇔ ∑_{i ∈ Hard} H_i(S) = 0 (zero violações duras).
  * O peso W_hard = 100.000 atua como barreira dissuasiva na função de custo f(S).
• Notas do Orador: Mostrar como a matemática penaliza severamente qualquer choque com 100.000 pontos de custo, garantindo que a viabilidade estrita exija soma zero de violações duras.

---
[SLIDE 7/10] 4. Seção C: Heurística 1 — O Pipeline Visual do DSatur (Princípio Fail-First)
• Layout: Fluxograma Visual / Infográfico de Processo em 4 Passos Horizontais (Esquerda para Direita).
• Título do Slide: Algoritmo 1: Heurística Construtiva Inspirada em Saturação (DSatur)
• Subtítulo: Como a ordenação estática por criticidade evita deadlocks e entrega viabilidade em milissegundos
• Os 4 Blocos Visuais do Diagrama:
  - PASSO 1: "Matriz Curricular Bruta"
    Lista desordenada de aulas. Prof. João só tem 4h livres na semana; Prof. Carlos tem 20h livres.
    Alerta: "Se alocar o Prof. Carlos primeiro, os horários do Prof. João podem esgotar e travar a grade!"
  - PASSO 2: "Cálculo do Grau de Saturação (Criticidade)"
    Fórmula: W(r) = α·CargaHoraria + β·(1 - DisponibilidadeDocente).
    Classificação: Prof. João = Peso 95 (Crítico!) | Prof. Carlos = Peso 25 (Fácil).
  - PASSO 3: "Fila Prioritária Fail-First"
    Regra de ouro: Quem tem menos horários disponíveis é ALOCADO PRIMEIRO!
    A aula de Física do Prof. João vai para a frente da fila.
  - PASSO 4: "Preenchimento do Grid em Memória (GridState)"
    Aloca no 1º slot livre na RAM em O(1).
    Resultado: 100% das restrições duras atendidas (Zero Choques) em < 100ms.
• Notas do Orador:
  "Para entenderem este algoritmo, olhem para este fluxo de 4 passos. No Passo 1 temos uma lista bagunçada de professores. No Passo 2, calculamos quem tem a agenda mais apertada: o Prof. João quase não tem horários disponíveis. Pelo princípio Fail-First, no Passo 3 o Prof. João passa para o início da fila. No Passo 4, o computador aloca ele primeiro onde ele pode dar aula. Quando sobram os professores com agenda livre, é fácil encaixá-los. Resultado: geramos uma grade com zero conflitos em menos de 100 milissegundos!"

---
[SLIDE 8/10] 4. Seção C: Heurística 2 — Simulated Annealing: Como Escapar de Ótimos Locais
• Layout: Gráfico Visual de Curva de Energia (Landscape) à esquerda + Caixa de Explicação à direita.
• Título do Slide: Algoritmo 2: Metaheurística de Busca Local por Recozimento Simulado
• Elementos Visuais do Gráfico:
  - Eixo Vertical: Custo f(S) (Penalidade de Janelas Vagas Docentes).
  - Eixo Horizontal: Configurações de Grades Semanais.
  - Curva de Relevo (Landscape):
    * 1º Vale (Raso): "Ótimo Local (Preso com 2 Janelas Vagas)".
      Seta vermelha: "Hill Climbing (Busca Gulosa) trava aqui porque só aceita descida direta!".
    * Morro intermediário: "Barreira de Custo (+Δf piora temporária)".
    * 2º Vale (Profundo): "Ótimo Global (Zero Janelas / Grade Otimizada)".
    * Seta verde curva saltando o morro: "Salto Estocástico do Simulated Annealing via Critério de Metropolis!".
• Caixa de Destaque da Matemática:
  - Critério de Metropolis (Metropolis et al., 1953 / Kirkpatrick et al., 1983):
    P(aceitar piora) = e^{-Δf / T}
  - Se a troca melhora a grade (Δf < 0): Aceita 100%.
  - Se a troca piora a grade (Δf > 0): Aceita com chance P, permitindo 'dar 1 passo atrás para dar 2 à frente'.
  - Resfriamento de T: No início (T alto) salta morros; no final (T baixo) congela no Ótimo Global.
• Notas do Orador:
  "Este gráfico ilustra por que o Simulated Annealing é indispensável. Uma busca gulosa tradicional como o Hill Climbing desce a colina e cai neste primeiro buraco: um ótimo local onde o professor tem 2 janelas vagas, mas qualquer troca simples imediata pioraria o horário. O Hill Climbing morre ali. Já o Simulated Annealing tem calor, tem energia: através do Critério de Metropolis, ele aceita temporariamente uma troca pior para saltar por cima da colina e cair no Ótimo Global, eliminando as janelas de vez."

---
[SLIDE 9/10] 4. Seção C: Operadores de Vizinhança — O Swap Move na Prática
• Layout: Comparativo Visual Lado a Lado ("Antes da Troca" vs "Depois da Troca").
• Título do Slide: Operador de Perturbação: Swap Move Intra-Turma na Prática
• Diagrama Visual do Slide:
  - PAINEL ESQUERDO: "Antes da Troca (Grade com Janela Ociosa)"
    Slot 1: FÍSICA (Prof. João)
    Slot 2: [ VAGO - JANELA DE 1 HORA! ] -> Penalidade de +85 pontos
    Slot 3: FÍSICA (Prof. João)
    Slot 4: MATEMÁTICA (Prof. Marcos)
    Diagnóstico: O Prof. João é obrigado a ficar 1 hora esperando no pátio da escola entre uma aula e outra.
  - SETA CENTRAL: "Operador Swap Move (Troca Horários na Mesma Turma)"
  - PAINEL DIREITO: "Depois da Troca (Grade Compactada e Otimizada)"
    Slot 1: FÍSICA (Prof. João)
    Slot 2: FÍSICA (Prof. João) -> Aulas geminadas consecutivas!
    Slot 3: MATEMÁTICA (Prof. Marcos) -> Antecipada
    Slot 4: [ LIVRE ]
    Resultado: Janela eliminada! O Prof. João dá suas duas aulas direto e vai embora para casa. Custo reduzido em -85 pontos.
  - REGRA DE BLINDAGEM NO RODAPÉ: "A troca SÓ é aceita se o professor de Matemática estiver livre no Slot 3. Se houver choque com outra turma, o movimento é sumariamente cancelado (P = 0)."
• Notas do Orador:
  "Para vocês verem como a busca local opera na prática, vejam este exemplo real da terça-feira de uma turma. À esquerda, o Prof. João dá Física no slot 1 e no slot 3, ficando com o slot 2 vago. Isso é uma janela ociosa: tempo perdido que Tardif e Lessard apontam como causa de estresse. O operador Swap Move permuta as disciplinas: puxa a segunda aula de Física para o slot 2 e antecipa a Matemática. As aulas de Física ficam geminadas, a janela desaparece e o professor é liberado mais cedo. E o mais importante: o motor confere se o professor de Matemática está livre; se houver choque, a troca é cancelada."

---
[SLIDE 10/10] 5. Conclusão: Quadro Comparativo e Encerramento
• Layout: Card Amplo com Tabela Comparativa e Fechamento.
• Tabela Comparativa Síntese:
  | Critério de Análise | Fase 1: DSatur Guloso | Fase 2: Simulated Annealing |
  | :--- | :--- | :--- |
  | Família Algorítmica | Heurística Construtiva Determinística | Metaheurística Estocástica de Trajetória |
  | Objetivo Primário | Viabilidade Física Estrita (Hard = 0) | Minimização de Janelas Docentes (Soft) |
  | Ponto de Partida | Grade Vazia (∅) | Grade Viável da Fase 1 (Warm Start) |
  | Complexidade | O(N log N) (Execução em < 100 ms) | O(Iterações × Custo(Δf)) |
  | Tratamento de Ótimo Local | Inexistente (decisão estática) | Escape via Critério de Metropolis (e^{-Δf/T}) |
• Bloco de Conclusão:
  "O paradigma híbrido em dois estágios resolve com perfeição o School Timetabling Problem: a Heurística Construtiva supera a barreira da explosão combinatória garantindo viabilidade matemática em milissegundos, enquanto o Simulated Annealing atua no refinamento ergonômico, assegurando qualidade de vida ao professor."
• Notas do Orador: Fechamento seguro, sintetizando a complementaridade das duas heurísticas e abrindo espaço formal para perguntas da banca.
```
