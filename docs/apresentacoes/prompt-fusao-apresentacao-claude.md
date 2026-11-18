# PROMPT MESTRE PARA O CLAUDE: FUSÃO E REESTRUTURAÇÃO DA APRESENTAÇÃO

Atue como um Especialista Sênior em Design Editorial Acadêmico, Engenharia de Software e Apresentações Técnicas de Alto Nível (padrão IEEE/ACM e bancas universitárias rigorosas).

Sua tarefa é criar a estrutura, os textos completos e as diretrizes visuais exatas para uma NOVA apresentação de slides, fundindo o rigor matemático e o estilo visual de "Horários Escolares - Pesquisa Acadêmica" com os dados empíricos e de arquitetura do "TimeTabling Pitch Deck".

---

### DIRETRIZES ESTÉTICAS E VISUAIS (OBRIGATÓRIO):
1. **Linguagem Visual:** Siga rigorosamente a identidade visual elegante, sóbria e técnica da apresentação *"Horários Escolares - Pesquisa Acadêmica"*:
   - Fundo limpo (off-white / slate suave com cartões brancos destacados).
   - Barra superior de navegação com breadcrumbs em caixa alta indicando em qual seção estamos (`PROBLEMA | MODELO | DESENVOLVIMENTO | RESULTADOS | CONCLUSÃO`).
   - Cartões com cantos levemente arredondados, bordas sutis e tipografia sem serifa moderna (Inter / Segoe UI / Roboto).
   - Uso de caixas de destaque com fundo colorido suave para métricas, equações e citações.
   - Zero ilustrações caricatas ou estilo cartoon: foco em dados, caixas, esquemas de blocos, matrizes e rigor de engenharia.

---

### ESTRUTURA DOS SLIDES:

#### SLIDE 1: [1 - Título, Orientador e Autores] (CAPA ORIGINAL EXATA)
- **Cabeçalho Institucional:**
  CENTRO UNIVERSITÁRIO GERALDO DI BIASE (UGB) — VOLTA REDONDA – RJ  
  Curso de Engenharia de Software · 6º período  
  Disciplina: Laboratório de Programação
- **Título Central:**
  **Heurísticas para alocação de horários escolares**  
  *Modelagem matemática e resolução em dois estágios (School Timetabling Problem)*
- **Autores:**
  Kauê Loreno Lopes · Pedro Henrique Dias Dornellas · Lucas Santana
- **Orientador:**
  Prof. Me. Marcelo Arantes de Oliveira

---

#### SLIDE 2: [1.1 - Agenda da Apresentação]
- **Objetivo Visual:** Linha do tempo ou grade de cartões limpos apresentando o roteiro estruturado da defesa:
  - **2. Introdução:** Contextualização, Definição do Problema e Objetivos (Modelo CB-CTT)
  - **3. Fundamentação Teórica:** Cenário de mercado e literatura científica de suporte
  - **4. Desenvolvimento:** Modelagem em dois estágios, heurística DSatur e arquitetura de software
  - **4.1 Resultados Obtidos:** Desempenho no cenário de homologação massivo (0,08s e zero colisões)
  - **5. Conclusão & Trabalhos Futuros:** Síntese, trade-offs e próximos passos
  - **6. Bibliografia:** Referências normatizadas ABNT

---

#### SLIDE 3: [2 & 2.1 - Introdução e Definição do Problema]
- **Subtítulo / Citações no Topo:** *Even, Itai e Shamir (1976) · Tardif e Lessard (2014)*
- **Bloco da Dor Real (Gestão Pedagógica):**
  - Montagem manual consome de 2 a 3 semanas exaustivas da coordenação por semestre.
  - **Efeito Dominó:** A alteração de disponibilidade de 1 docente na véspera exige desmontar a grade de vários outros em cadeia.
  - **Janelas Ociosas:** Fragmentação da jornada docente com horas vagas não remuneradas entre aulas, apontado por Tardif e Lessard (2014) como fator de precarização e desgaste.
- **Bloco da Barreira Computacional (Pesquisa Operacional):**
  - O STP (*School Timetabling Problem*) é comprovadamente **NP-difícil**.
  - O espaço de busca bruto de uma grade típica (25 slots × 250 aulas) atinge $|\Omega| = 25^{250} \approx 3,05 \times 10^{349}$ (ordem de $10^{350}$).
  - Magnitude que supera brutalmente os $10^{80}$ átomos do universo observável, inviabilizando qualquer busca exaustiva por força bruta.

---

#### SLIDE 4: [2.2 - Objetivo (O Porquê da Solução)]
- **Objetivo Central:** Desenvolver uma aplicação web desacoplada para geração automatizada de grades horárias no modelo internacional **CB-CTT (Curriculum-Based Course Timetabling)**.
- **Os 4 Pilares de Engenharia:**
  1. **Modelar:** Formalização matemática de turmas por coortes curriculares e professores.
  2. **Implementar:** Motor heurístico desacoplado com consulta de colisão ultrarrápida.
  3. **Validar:** Comprovar a viabilidade estrita ($Zero\ Colisões$) e mensurar tempo de convergência.
  4. **Disponibilizar:** Aplicação web real, moderna e conteinerizada em nuvem.
- **Proposta de Valor:** Transformar semanas de angústia em uma operação de 3 passos: Você informa a demanda ➔ O motor arranja ➔ A grade surge pronta e viável.

---

#### SLIDE 5: [3 - Fundamentação Teórica (Mercado & Literatura)]
- **O Cenário de Mercado:**
  - Softwares legados pecam por tentar abordagens exaustivas (MILP) que não escalam em instâncias reais, ou realizam consultas pesadas de banco de dados a cada passo, gerando travamentos.
- **Autores e Teorias que Validam a Abordagem:**
  - **Even, Itai e Shamir (1976):** Demonstração da NP-completude da decisão de horários.
  - **Karp (1972):** Semelhança estrutural com a coloração de grafos (aulas como vértices, conflitos como arestas, slots como cores).
  - **Brélaz (1979) & Carter et al. (1996):** Estratégia de saturação e priorização dos nós mais restritos.
  - **Metropolis et al. (1953) & Kirkpatrick et al. (1983):** Aceitação de pioras controladas (Simulated Annealing) para escapar de ótimos locais.
  - **Lewis (2008) & Schaerf (1999):** Surveys internacionais que consagram meta-heurísticas em dois estágios para timetabling.

---

#### SLIDE 6: [4 - Desenvolvimento: Modelagem Matemática e Heurística]
- **Modelo em Dois Estágios:**
  - **Restrições Rígidas (Hard Constraints - Invioláveis):** Unicidade docente ($\forall p, dia, s$), unicidade de turma ($\forall t, dia, s$), respeito à disponibilidade ($Disp$) e cumprimento integral da carga horária semanal ($CH(t,d)$).
  - **Restrições Flexíveis (Soft Constraints - Otimização):** Minimização de janelas docentes (peso 85), equilíbrio diário (peso 70) e atendimento às preferências docentes ($w_{pref} = 50$).
- **Fase 1 (Construtiva - Guloso DSatur + Fail-First):**
  - Ordenação estática por grau de criticidade das disciplinas.
  - Princípio *Fail-First*: alocar primeiro os casos mais difíceis (docentes com menos slots livres).
  - Complexidade algorítmica: $O(N \log N) + O(N \cdot |K|) = O(N \log N)$, pois $|K| = 25$ é constante.
- **Separação Estrita de Viabilidade (Proposição):**
  - Custo soft máximo de qualquer grade viável é $\le 48.500 < 100.000$ ($W_{hard}$), garantindo que $Viável \iff Hard = 0$.

---

#### SLIDE 7: [4 - Desenvolvimento: Arquitetura de Software e GridState]
- **Stack Tecnológica Completa:**
  - **Frontend:** React 18 com TypeScript, renderizando grades dinâmicas interativas.
  - **Backend:** API Django REST (Python 3.12) desacoplada do motor.
  - **Persistência:** PostgreSQL 16 relacional.
  - **Infraestrutura:** Docker e deploy em nuvem na Microsoft Azure.
- **Diferencial de Engenharia — GridState em Memória RAM:**
  - Em vez de realizar queries SQL dentro do loop combinatório, a grade é instanciada em matrizes multidimensionais na RAM.
  - **Consulta de colisão em tempo constante $O(1)$**.
  - Isolamento de I/O de disco: o banco de dados é acessado apenas no início (carga) e no final (persistência).

---

#### SLIDE 8: [4.1 - Resultados Obtidos no Cenário Validado]
- **Massa de Testes Homologada (Cenário de Estresse Combinatório):**
  - **14 turmas curriculares ativas** simultâneas.
  - **50 professores** com diferentes especialidades.
  - **275 bloqueios de disponibilidade docente** cadastrados.
- **Métricas de Performance Alcançadas:**
  - **0 Colisões Rígidas** ($Hard = 0$): 100% de viabilidade matemática alcançada.
  - **Tempo do Motor de Cálculo:** **0,08 segundos**.
- **Rigor e Transparência Científica:**
  - Deixar explícito no rodapé: *"Validação executada em massa de testes teórica desenhada para estressar a combinatória do sistema. Tempo referente ao motor em RAM, sem overhead de rede."*

---

#### SLIDE 9: [5 - Conclusão e Trabalhos Futuros]
- **Síntese dos Resultados:**
  - Viabilidade prática comprovada: desacoplamento arquitetural e heurística Fail-First eliminam o gargalo das 3 semanas manuais.
  - A separação entre viabilidade e otimização protege a escola contra grades inválidas.
- **Limitações e Trabalhos Futuros:**
  - Transição da massa de testes teórica para homologação em secretarias acadêmicas reais com dados empíricos.
  - Acoplamento da Fase 2 (Simulated Annealing com critérios de Metropolis) para refinar janelas e preferências de forma contínua.
- **Máxima de Engenharia em Destaque:**
  - *"Uma solução viável, robusta e entregue no prazo vale infinitamente mais do que uma solução 'teoricamente ótima' que nunca roda."*

---

#### SLIDE 10: [6 - Bibliografia Completa (Normas ABNT NBR 6023)]
Apresente a lista em duas colunas organizadas:
- BRÉLAZ, D. New methods to color the vertices of a graph. *Communications of the ACM*, v. 22, n. 4, p. 251-256, 1979.
- BURKE, E. K.; NEWALL, J. P.; WEARE, R. F. Initialization strategies and diversity in evolutionary timetabling. *Evolutionary Computation*, v. 6, n. 1, p. 81-103, 1998.
- CARTER, M. W.; LAPORTE, G.; LEE, S. Y. Examination timetabling: algorithmic strategies and applications. *Journal of the Operational Research Society*, v. 47, n. 3, p. 373-383, 1996.
- EVEN, S.; ITAI, A.; SHAMIR, A. On the complexity of timetable and multicommodity flow problems. *SIAM Journal on Computing*, v. 5, n. 4, p. 691-703, 1976.
- KARP, R. M. Reducibility among combinatorial problems. *Complexity of Computer Computations*, Plenum Press, p. 85-103, 1972.
- KIRKPATRICK, S.; GELATT, C. D.; VECCHI, M. P. Optimization by simulated annealing. *Science*, v. 220, n. 4598, p. 671-680, 1983.
- LEWIS, R. A survey of metaheuristic-based techniques for university timetabling problems. *OR Spectrum*, v. 30, n. 1, p. 167-190, 2008.
- METROPOLIS, N. et al. Equation of state calculations by fast computing machines. *The Journal of Chemical Physics*, v. 21, n. 6, p. 1087-1092, 1953.
- TARDIF, M.; LESSARD, C. *O trabalho docente: elementos para uma teoria da docência como profissão de interações humanas*. 9. ed. Petrópolis: Vozes, 2014.
