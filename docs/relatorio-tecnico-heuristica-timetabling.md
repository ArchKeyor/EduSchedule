# Relatório Técnico: Abordagem Heurística para o Problema de Alocação de Horários Escolares (*School Timetabling Problem*)

**Instituição:** Centro Universitário Geraldo Di Biase (UGB) — Volta Redonda, RJ  
**Disciplina:** Laboratório de Programação (6º Período)  
**Professor Orientador:** Me. Marcelo Arantes de Oliveira  
**Curso:** Engenharia de Software  
**Autores / Equipe:**  
- Kauê Loreno Lopes (*Tech Lead & Engenheiro de Otimização*)  
- Pedro Henrique Dias Dornellas (*Frontend UI*)  
- Lucas Santana (*Backend & Dados*)  

---

## 1. Introdução e Contextualização do Problema

O Problema de Alocação de Horários Escolares (*School Timetabling Problem* - STP) consiste em atribuir um conjunto de aulas, ministradas por professores específicos a determinadas turmas, dentro de uma grade semanal finita e estruturada de horários (*time slots*).

Trata-se de um problema canônico de otimização combinatória classificado como **NP-difícil (a versão de decisão é NP-completa)** (EVEN; ITAI; SHAMIR, 1976). Na prática administrativa da expressiva maioria das instituições de ensino básico, técnico e superior, a elaboração da grade é historicamente conduzida de forma manual por coordenadores de curso. Esse processo puramente artesanal consome tempo considerável da gestão e resulta sistematicamente em falhas operacionais, tais como choques acidentais de turmas ou professores e grades com janelas vagas ociosas (*gaps*) entre períodos.

Conforme discutem Tardif e Lessard (2014), a fragmentação da jornada diária e a presença recorrente de janelas desnecessárias na grade docente constituem fatores de estresse, absenteísmo e precarização do trabalho dos professores, afetando sensivelmente a qualidade do ambiente escolar.

Sob a perspectiva da Teoria da Computação, tentativas de solucionar instâncias reais de agendamento por meio de métodos determinísticos de força bruta ou formulações puras de Programação Linear Inteira Mista (MILP) esbarram na barreira da explosão combinatória: o número de variáveis binárias cresce exponencialmente, podendo levar ao esgotamento de memória em árvores de *Branch-and-Bound* e dificultar a obtenção de soluções em tempo hábil para instâncias reais de médio e grande porte.

Por esse motivo, o estado da arte internacional consagrou o uso de Heurísticas Construtivas e Metaheurísticas de Busca Local organizadas sob o paradigma híbrido em dois estágios (BURKE et al., 1998; LEWIS, 2008). O presente relatório formaliza a modelagem matemática e os algoritmos desenvolvidos para o motor do sistema *TimeTabling*, projetado para buscar grades sem violações rígidas e proporcionar conforto ergonômico aos professores.

---

## A. Modelagem Matemática Formal

A modelagem matemática tem como propósito mapear a complexidade do domínio educacional em estruturas formais e variáveis quantificáveis.

### A.1. Definição Formal de Conjuntos e Parâmetros

Definem-se os conjuntos e parâmetros fundamentais que compõem o universo do problema:

1. **Conjunto de Turmas ($T$):** $T = \{t_1, t_2, \dots, t_{|T|}\}$, representando as turmas ou classes de estudantes da instituição.
2. **Conjunto de Professores ($P$):** $P = \{p_1, p_2, \dots, p_{|P|}\}$, representando o corpo docente cadastrado.
3. **Conjunto de Disciplinas ($D$):** $D = \{d_1, d_2, \dots, d_{|D|}\}$, representando as matérias curriculares obrigatórias.
4. **Conjunto de Dias da Semana ($Dia$):** $Dia = \{1, 2, 3, 4, 5\}$, correspondendo à jornada letiva de segunda a sexta-feira ($|Dia| = 5$).
5. **Conjunto de Períodos Diários ($S$):** $S = \{1, 2, \dots, |S|\}$, onde cada período representa uma aula unitária (fixado em $|S| = 5$ períodos diários).
6. **Conjunto Global de Slots Semanais ($K$):** $K = Dia \times S$, totalizando $|K| = |Dia| \cdot |S| = 25$ posições temporais por semana.
7. **Matriz de Carga Horária ($CH$):** $CH(t, d) \in \mathbb{N}$, quantidade de aulas semanais obrigatórias que a turma $t$ deve cursar da disciplina $d$.
8. **Atribuição Docente ($Prof$):** Função $Prof(t, d) = p$ que associa unicamente qual professor $p \in P$ leciona a matéria $d$ para a turma $t$.
9. **Matriz de Disponibilidade Docente ($Disp$):**
   $$Disp_{p, dia, s} = \begin{cases} 1, & \text{se o docente } p \text{ está liberado no dia } dia \text{ e período } s \\ 0, & \text{se há restrição contratual / bloqueio} \end{cases}$$
10. **Preferência Docente ($Pref$):** $Pref(p) \subseteq Dia$, o subconjunto de dias livres que o professor prefere lecionar. Dias bloqueados correspondem a $Disp = 0$.

---

### A.2. Variáveis de Decisão

A alocação de cada aula na grade semanal é expressa por uma variável de decisão binária multidimensional:

$$x_{t, p, d, dia, s} \in \{0, 1\}$$

onde $x_{t, p, d, dia, s} = 1$ se a aula da disciplina $d$, ministrada pelo professor $p$ para a turma $t$, for alocada exatamente no dia $dia \in Dia$ e período $s \in S$; 0 caso contrário.

Dada a bijeção definida pela matriz curricular onde cada disciplina de uma turma possui um professor responsável pré-atribuído ($Prof(t, d) = p$), a representação simplifica-se sem perda de generalidade para $x_{t, d, dia, s} \in \{0, 1\}$. Para diferenciar a solução de grade do conjunto $S$ de períodos diários, adota-se a notação $\mathcal{G}$ para representar uma grade horária candidata.

---

### A.3. Representação do Espaço de Busca e Teoria da Complexidade

O espaço de busca $\Omega$ compreende todas as atribuições possíveis de aulas nos horários da semana:
* Seja $N$ o total de aulas letivas que precisam ser distribuídas:
  $$N = \sum_{t \in T} \sum_{d \in D} CH(t, d)$$
* Para cada uma das $N$ aulas, existem $|K| = |Dia| \times |S| = 25$ slots temporais elegíveis.
* Dessa forma, a cardinalidade do espaço de soluções bruto (como um limite superior irrestrito) é dada por:
  $$|\Omega| = (|Dia| \times |S|)^N = 25^N$$

**Magnitude Combinatória:** Para uma instituição modesta com apenas 10 turmas e 25 aulas semanais por turma ($N = 250$ aulas), o espaço bruto atinge $|\Omega| = 25^{250} \approx 3,05 \times 10^{349}$ (ordem de $10^{350}$), muito acima da estimativa de $10^{80}$ átomos do universo observável, o que inviabiliza a busca exaustiva por força bruta.

A intratabilidade é estabelecida por Even, Itai e Shamir (1976), que demonstraram que a versão de decisão do problema de horários é NP-completa; logo, a otimização correspondente é NP-difícil. Há semelhança estrutural com a coloração de vértices (KARP, 1972), em que aulas são vértices, conflitos são arestas e horários são cores, mas este trabalho não apresenta uma redução formal.

---

## B. Metodologia (Restrições e Função de Avaliação)

Para avaliar a viabilidade física e a qualidade pedagógica de uma determinada solução de horários $\mathcal{G} \in \Omega$, o sistema categoriza os requisitos em restrições fortes e fracas.

### B.1. Restrições Fortes (*Hard Constraints*)
As restrições fortes são condições inegociáveis. Se houver ao menos uma violação, a grade é considerada inválida e inutilizável:

1. **Unicidade de Atendimento Docente (Sem Choque de Professor):** Um professor não pode ministrar aula em mais de uma turma no mesmo dia e período:
   $$\sum_{t \in T} \sum_{d \in D} x_{t, p, d, dia, s} \le 1, \quad \forall p \in P, \, \forall dia \in Dia, \, \forall s \in S$$

2. **Unicidade de Turma (Sem Choque de Horário da Turma):** Uma turma não pode ter mais de uma aula alocada simultaneamente no mesmo horário:
   $$\sum_{p \in P} \sum_{d \in D} x_{t, p, d, dia, s} \le 1, \quad \forall t \in T, \, \forall dia \in Dia, \, \forall s \in S$$

3. **Respeito aos Bloqueios de Agenda:** Um professor não pode ter aulas atribuídas em horários com restrição declarada:
   $$x_{t, p, d, dia, s} \le Disp_{p, dia, s}, \quad \forall t \in T, \, \forall p \in P, \, \forall d \in D, \, \forall dia \in Dia, \, \forall s \in S$$

4. **Integralidade da Carga Horária Curricular:** Todas as aulas previstas pela matriz curricular devem ser obrigatoriamente alocadas:
   $$\sum_{dia \in Dia} \sum_{s \in S} x_{t, Prof(t,d), d, dia, s} = CH(t, d), \quad \forall t \in T, \, \forall d \in D$$

---

### B.2. Restrições Fracas (*Soft Constraints*)
As restrições fracas não inviabilizam a grade, mas mensuram sua qualidade pedagógica e ergonômica:

1. **Minimização de Janelas Vagas Docentes (*Teacher Gaps*):**
   Penaliza intervalos ociosos na jornada diária do professor entre sua primeira e última aula:
   $$Gap(p, dia) = (s_{max} - s_{min} + 1) - \text{TotalAulas}(p, dia)$$
   Em dias sem aulas, adota-se estritamente $Gap(p, dia) = 0$.

2. **Equilíbrio Diário de Disciplinas:**
   Evita que os estudantes tenham mais de 2 aulas da mesma disciplina no mesmo dia, prevenindo a estafa cognitiva:
   $$Excesso(t, d, dia) = \max\left(0, \sum_{s \in S} x_{t, Prof(t,d), d, dia, s} - 2\right)$$

3. **Preferências Docentes:**
   Penaliza aulas alocadas em dia livre que não seja preferido pelo professor:
   $$Pen\_pref = \sum x_{t, Prof(t,d), d, dia, s} \quad \text{sobre os dias em } Livre(p) \setminus Pref(p)$$
   Cada aula nessa condição contribui com no máximo 1 ponto.

---

### B.3. Função de Aptidão / Custo (*Fitness Function*)

A avaliação de uma grade $\mathcal{G} \in \Omega$ é regida por uma função escalar de custo a ser **minimizada**:

$$f(\mathcal{G}) = W_{hard} \cdot \sum_{i \in \text{Hard}} H_i(\mathcal{G}) + \sum_{j \in \text{Soft}} w_j \cdot V_j(\mathcal{G})$$

onde:
* $H_i(\mathcal{G})$: contador de violações de restrições rígidas;
* $W_{hard} = 100.000$: peso de penalidade dissuasiva extrema;
* $V_j(\mathcal{G})$: frequência das violações de restrições suaves;
* Pesos relativos calibrados no sistema:
  * $w_{gap} = 85$ (penalidade por janela ociosa de professor);
  * $w_{balance} = 70$ (penalidade por excesso diário de aulas da mesma matéria);
  * $w_{pref} = 50$ (penalidade por dia não preferido, valor proposto a calibrar).

**Condição Formal de Viabilidade:**
$$\text{Viável} \iff \sum_{i \in \text{Hard}} H_i(\mathcal{G}) = 0$$
Se o custo soft máximo de toda grade viável for menor que $W_{hard}$, vale também $f(\mathcal{G}) < W_{hard} \iff \text{Viável}$.

**Proposição:** Para toda grade viável, o custo soft é limitado por:
$$\text{Custo Soft} \le 1.275 \cdot |P| + 1.050 \cdot |T| + w_{pref} \cdot N$$
A demonstração formal e o exemplo numérico dessa cota superior são detalhados na Seção 4.4.

---

## C. Heurísticas e Metaheurísticas Adotadas

Em conformidade com as melhores práticas da literatura de *Timetabling* (BURKE et al., 1998; LEWIS, 2008), o sistema adota a **Arquitetura em Dois Estágios (*Two-Stage Framework*)**:
* **Fase 1 (Construtiva):** Busca viabilidade física estrita ($Hard = 0$);
* **Fase 2 (Metaheurística de Busca Local):** Parte da grade viável inicial (*Warm Start*) e foca em minimizar as penalidades das restrições suaves ($Soft$).

---

### 4.1. Fase 1: Heurística Construtiva Inspirada em Saturação

**Funcionamento Teórico:** Inspirado no clássico princípio de saturação de grafos (BRÉLAZ, 1979) e em estratégias heurísticas para agendamento educacional (CARTER; LAPORTE; LEE, 1996), este método aplica uma abordagem construtiva baseada na filosofia "Fail-First" (Falhe Primeiro). A ordenação é estática; não há recálculo dinâmico da saturação a cada passo, portanto não se trata do DSatur clássico.

**Mecanismo de Busca:**
1. As aulas são ordenadas previamente de forma decrescente pela função de criticidade:
   $$Criticidade(d) = \alpha \cdot CH(t, d) + \beta \cdot (1 - Disp)$$
   onde $CH(t, d)$ é a carga semanal da matéria, $Disp$ é a fração de slots livres do docente na semana (número de slots livres dividido por 25), e $\alpha$ e $\beta$ são pesos de ajuste.
2. O motor percorre a lista ordenada e consulta a matriz em memória RAM (`GridState`).
3. Aloca a aula no primeiro slot compatível $(dia, s)$ livre para a turma e professor sem violar bloqueios.
4. **Custo Computacional:** A ordenação inicial requer $O(N \log N)$ e a busca no grid consome $O(N \cdot |K|)$; como $|K| = 25$ é constante, a complexidade assintótica total é $O(N \log N)$. Para $N = 250$ aulas, isso representa da ordem de $10^4$ operações elementares (análise teórica, sem benchmark formal).

**Limitação Teórica:** Sem reparo nem retrocesso (*backtracking*), o método não garante viabilidade em toda instância arbitrária. Duas condições necessárias, verificáveis preliminarmente em $O(N)$, são: (a) a carga horária de cada turma deve ser $\le 25$; e (b) a carga horária de cada professor deve ser $\le$ ao seu número total de slots livres cadastrados.

---

### 4.2. Fase 2: Metaheurística de Busca Local (*Simulated Annealing*)

**Funcionamento Teórico:** Inspirado na termodinâmica estatística (METROPOLIS et al., 1953; KIRKPATRICK et al., 1983), o *Simulated Annealing* (SA) supera buscas gulosas simples (*Hill Climbing*), que estagnam em ótimos locais. O SA possui a propriedade matemática de aceitar soluções temporariamente piores para escapar de armadilhas combinatórias.

A probabilidade de transição para estados com custo superior ($\Delta f = f(\mathcal{G}_{novo}) - f(\mathcal{G}_{atual}) > 0$) segue o **Critério de Metropolis**:

$$P(\text{aceitar piora}) = e^{-\frac{\Delta f}{T}}$$

Parâmetros propostos, a calibrar: Temperatura inicial $T_0 = 100$, temperatura final $T_{final} = 1$, taxa de resfriamento geométrico $\lambda = 0,95$ (resultando em cerca de 90 níveis; nota-se que se pode manter a notação tradicional $T_{k+1} = \alpha \cdot T_k$ com $\alpha = 0,95$, tratando-se do mesmo símbolo usado na criticidade, em contextos distintos) e 250 iterações por temperatura (totalizando cerca de 22.500 avaliações).

**Estratégias de Geração de Vizinhança e Perturbação:**
* **Operador 1 - Troca Intra-Turma (*Swap Move*):** Permuta os horários de duas aulas distintas da mesma turma, preservando integralmente a carga horária semanal.
* **Operador 2 - Deslocamento para Slot Livre (*Move to Free Slot*):** Move uma aula para um período vago adjacente, aplicável apenas a turmas com slots livres.
* **Blindagem Rígida de Viabilidade:** Qualquer movimento que induza violações de restrições rígidas — incluindo violações de disponibilidade e choque de professor em outra turma — é sumariamente descartado ($P = 0$), assegurando busca exclusiva na região viável.

---

### 4.3. Síntese Comparativa das Abordagens

| Critério de Análise | Fase 1: Construtiva Inspirada em Saturação | Fase 2: Simulated Annealing |
| :--- | :--- | :--- |
| **Família Algorítmica** | Heurística Construtiva Determinística | Metaheurística Estocástica de Trajetória |
| **Estágio de Execução** | Fase 1 (Inicialização / *Warm Start*) | Fase 2 (Polimento de Qualidade Suave) |
| **Objetivo Primário** | Viabilidade física estrita ($Hard = 0$) | Minimização de janelas e preferências ($Soft$) |
| **Estado de Partida** | Grade completamente vazia ($\emptyset$) | Grade viável gerada pela Fase 1 |
| **Complexidade Temporal** | $O(N \log N)$ (análise teórica) | $O(\text{Iterações} \times \text{Custo}(\Delta f))$ |
| **Tratamento de Ótimo Local** | Inexistente (decisão estática) | Escape via Metropolis (sem garantia de ótimo global) |

---

### 4.4. Análise Teórica: Limites de Custo, Metropolis e Preservação da Viabilidade

1. **Limite Superior do Custo Soft:**  
   Em uma jornada semanal com $|Dia| = 5$ e $|S| = 5$, o número máximo de janelas ociosas que um docente pode sofrer em um único dia ocorre quando ele leciona apenas no slot 1 e no slot 5, perfazendo $Gap(p, dia) \le 3$. Em 5 dias, o total é $\le 15$ por professor. Para cada turma, o excesso diário da mesma matéria é $\le 3$, totalizando $\le 15$ por turma na semana. Como a penalidade de dia não preferido é no máximo 1 por aula (totalizando $N$), o custo soft total é rigorosamente delimitado por:
   $$\text{Custo Soft} \le 85 \cdot 15 \cdot |P| + 70 \cdot 15 \cdot |T| + 50 \cdot N = 1.275 \cdot |P| + 1.050 \cdot |T| + 50 \cdot N$$

   *Exemplo Numérico de Validação:* Para um cenário com $|T| = 10$ turmas, $|P| = 20$ professores e $N = 250$ aulas:
   $$\text{Custo Soft} \le 1.275 \cdot (20) + 1.050 \cdot (10) + 50 \cdot (250) = 25.500 + 10.500 + 12.500 = \mathbf{48.500 < 100.000}$$
   Como $48.500 < 100.000$, comprova-se formalmente que, para este cenário, nenhuma grade viável atingirá custo superior a $W_{hard}$, assegurando a equivalência $f(\mathcal{G}) < W_{hard} \iff \text{Viável}$.

2. **Comportamento Numérico do Critério de Metropolis:**  
   Para uma piora isolada de uma janela docente ($\Delta f = 85$), a probabilidade de aceitação varia conforme a temperatura $T$:
   * Em $T = 100$: $P = e^{-85 / 100} = e^{-0,85} \approx 0,43$ (aproximadamente 43% de chance de aceitação, promovendo ampla exploração estocástica);
   * Em $T = 10$: $P = e^{-85 / 10} = e^{-8,5} \approx 2 \times 10^{-4}$ (baixa tolerância a pioras);
   * Em $T = 1$: $P = e^{-85 / 1} \approx 10^{-37}$ (convergência estrita para o mínimo local).
   
   Em contrapartida, movimentos com violação hard têm $\Delta f \ge 100.000$, gerando $P \approx 0$ para qualquer $T$ operacional.

3. **Preservação Rigorosa da Viabilidade:**  
   Como a Fase 2 rejeita compulsoriamente qualquer movimento com violação hard ($P = 0$), ela parte de uma semente viável com $Hard = 0$ fornecida pela Fase 1 e mantém essa viabilidade durante todas as 22.500 avaliações de busca local.

---

## 5. Considerações Finais

A formalização matemática e a estruturação em dois estágios proposta neste relatório propõem uma arquitetura para tratar o *School Timetabling Problem* de forma heurística, articulando uma formulação rigorosa de variáveis de decisão com restrições fortes e critérios de conforto pedagógico. A integração entre a heurística construtiva na Fase 1 e a metaheurística de *Simulated Annealing* na Fase 2 busca atender tanto a integridade matemática da grade quanto a ergonomia e saúde do trabalho docente.

**Limitações e Trabalhos Futuros:** Ressalta-se que o presente estudo constitui uma proposta formal e teórica, sem validação experimental ampla. Como passos subsequentes para a continuidade da pesquisa, estabelecem-se: (a) a execução de benchmarks computacionais formais sobre instâncias reais de ensino; (b) a calibração empírica dos pesos ($w_{gap}, w_{balance}, w_{pref}$) e parâmetros de resfriamento térmico através de análise de sensibilidade; e (c) a comparação sistemática de qualidade e tempo de resposta frente a solucionadores exatos de Programação Linear Inteira e algoritmos genéticos híbridos.

---

## Referências Bibliográficas

* BRÉLAZ, Daniel. New methods to color the vertices of a graph. **Communications of the ACM**, New York, v. 22, n. 4, p. 251-256, 1979.
* BURKE, Edmund K.; NEWALL, J. P.; WEARE, R. F. Initialization strategies and diversity in evolutionary timetabling. **Evolutionary Computation**, Cambridge, v. 6, n. 1, p. 81-103, 1998.
* CARTER, Michael W.; LAPORTE, Gilbert; LEE, S. Y. Examination timetabling: algorithmic strategies and applications. **Journal of the Operational Research Society**, London, v. 47, n. 3, p. 373-383, 1996.
* EVEN, Shimon; ITAI, Alon; SHAMIR, Adi. On the complexity of timetable and multicommodity flow problems. **SIAM Journal on Computing**, Philadelphia, v. 5, n. 4, p. 691-703, 1976.
* KARP, Richard M. Reducibility among Combinatorial Problems. In: MILLER, Raymond E.; THATCHER, James W. (Ed.). **Complexity of Computer Computations**. New York: Plenum Press, 1972. p. 85-103.
* KIRKPATRICK, Scott; GELATT, C. Daniel; VECCHI, Mario P. Optimization by simulated annealing. **Science**, Washington, v. 220, n. 4598, p. 671-680, 1983.
* LEWIS, Rhydian. A survey of metaheuristic-based techniques for university timetabling problems. **OR Spectrum**, Heidelberg, v. 30, n. 1, p. 167-190, 2008.
* METROPOLIS, Nicholas; ROSENBLUTH, Arianna W.; ROSENBLUTH, Marshall N.; TELLER, Augusta H.; TELLER, Edward. Equation of state calculations by fast computing machines. **The Journal of Chemical Physics**, Melville, v. 21, n. 6, p. 1087-1092, 1953.
* PILLAY, Nelishia. A survey of school timetabling research. **Annals of Operations Research**, Dordrecht, v. 218, n. 1, p. 261-293, 2014.
* SCHAERF, Andrea. A survey of automated timetabling. **Artificial Intelligence Review**, Dordrecht, v. 13, n. 2, p. 87-127, 1999.
* TARDIF, Maurice; LESSARD, Claude. **O trabalho docente: elementos para uma teoria da docência como profissão de interações humanas**. 9. ed. Petrópolis: Vozes, 2014.
