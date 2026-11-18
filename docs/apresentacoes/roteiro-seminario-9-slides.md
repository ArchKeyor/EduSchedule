# Roteiro de Apresentação Oral (Seminário de Heurísticas)

**Instituição:** Centro Universitário Geraldo Di Biase (UGB) — Volta Redonda, RJ  
**Disciplina:** Laboratório de Programação (6º Período)  
**Professor:** Me. Marcelo Arantes de Oliveira  
**Tema:** Abordagem Heurística para o Problema de Alocação de Horários Escolares (*School Timetabling Problem*)  
**Tempo Total Recomendado:** 10 a 12 minutos (aprox. 1m15s por slide)  
**Divisão da Equipe:** Kauê Loreno (Tech Lead), Pedro Henrique Dias (Frontend) e Lucas Santana (Backend).

---

## ⏱️ Distribuição de Tempo e Papéis por Slide

| Slide | Título do Slide | Apresentador Sugerido | Tempo Alvo |
| :---: | :--- | :---: | :---: |
| **01** | Capa Oficial & Apresentação da Equipe | Lucas | 00:30 min |
| **02** | O Problema e a Explosão Combinatória ($25^N \approx 10^{350}$) | Lucas | 01:15 min |
| **03** | Modelagem Matemática Formal ($x_{t,p,d,dia,s}$) | Lucas | 01:15 min |
| **04** | Restrições Fortes (*Hard Constraints* — Viabilidade) | Pedro | 01:15 min |
| **05** | Restrições Fracas (*Soft Constraints* — Ergonomia e Qualidade) | Pedro | 01:15 min |
| **06** | Função de Aptidão / Custo (*Fitness Function* e Pesos) | Pedro | 01:15 min |
| **07** | Heurística 1: O Pipeline Visual do DSatur (*Fail-First*) | Kauê | 01:15 min |
| **08** | Metaheurística 2: Simulated Annealing (O Gráfico do Ótimo Local) | Kauê | 01:15 min |
| **09** | Operadores de Vizinhança: O Swap Move na Prática (Antes vs Depois) | Kauê | 01:15 min |
| **10** | Quadro Comparativo Síntese & Conclusão | Kauê / Equipe | 01:00 min |

---

## 🎙️ Fala Slide a Slide (O Que Dizer com Domínio)

### Slide 1 — Capa Oficial (00:00 - 00:30)
> *"Boa noite, professor Marcelo e colegas. Nós somos a equipe composta pelo Kauê, Pedro e Lucas. Hoje vamos apresentar a modelagem matemática e a abordagem heurística em dois estágios desenvolvida para solucionar o School Timetabling Problem, o clássico problema de alocação de horários escolares."*

---

### Slide 2 — O Problema e a Explosão Combinatória (00:30 - 01:45)
* **Objetivo:** Mostrar por que força bruta não serve para nada na vida real.
* **Fala sugerida:**  
> *"Na gestão escolar tradicional, montar horários consome semanas de coordenadores e gera grades com janelas vagas — os famosos 'buracos' na jornada do professor, que sociólogos como Tardif e Lessard apontam e discutem como fortes fatores de estresse, absenteísmo e precarização docente.  
> Computacionalmente, o problema é formalmente NP-Difícil (comprovado por Even, Itai e Shamir em 1976), generalizando o clássico problema de Coloração de Vértices de Grafos de Karp.  
> Se considerarmos 25 horários na semana e 10 turmas (250 aulas), o limite superior bruto do espaço de busca é de $25^{250}$, o que dá aproximadamente $10^{350}$ combinações possíveis — muito superior a todas as partículas do universo! Por isso, métodos exatos de programação linear inteira (MILP) não escalam bem para instâncias reais de médio e grande porte devido à explosão combinatória, tornando as abordagens heurísticas obrigatórias."*

---

### Slide 3 — Modelagem Matemática Formal (01:45 - 03:00)
* **Objetivo:** Demonstrar domínio dos conjuntos discretos e da variável de decisão.
* **Fala sugerida:**  
> *"Para modelar matematicamente a realidade escolar, estruturamos os conjuntos de Turmas $T$, Professores $P$, Disciplinas $D$, além dos 5 dias letivos e 5 períodos diários, totalizando 25 slots semanais $K$.  
> A decisão central de alocação é regida pela variável binária $x_{t,p,d,dia,s} \in \{0, 1\}$, que vale 1 se a turma $t$ tiver aula da disciplina $d$ com o professor $p$ no dia e slot indicados, e 0 caso contrário.  
> Como a nossa matriz curricular já pré-atribui o docente responsável por cada matéria da turma, o tensor opera de forma simplificada em memória RAM, garantindo consultas em tempo constante."*

---

### Slide 4 — Restrições Fortes (*Hard Constraints*) (03:00 - 04:15)
* **Objetivo:** Mostrar as condições inegociáveis de validade matemática.
* **Fala sugerida:**  
> *"Separamos as restrições em dois grupos rigorosos. As Restrições Fortes são invioláveis: se uma única for quebrada, a grade é descartada como nula.  
> São 4 condições centrais:  
> 1. Unicidade Docente: o somatório de aulas de um mesmo professor no mesmo slot deve ser menor ou igual a 1 — zero choque de professor;  
> 2. Unicidade de Turma: uma turma nunca pode ter duas aulas no mesmo horário;  
> 3. Respeito à Indisponibilidade: se o professor declarou bloqueio de agenda ou restrição contratual, nenhuma aula pode ser alocada ali;  
> 4. Cumprimento da Matriz: todas as aulas previstas pela matriz curricular devem ser obrigatoriamente encaixadas."*

---

### Slide 5 — Restrições Fracas (*Soft Constraints*) (04:15 - 05:30)
* **Objetivo:** Mostrar o refinamento da qualidade pedagógica e humana.
* **Fala sugerida:**  
> *"Já as Restrições Fracas não inviabilizam a escola, mas medem o conforto e a ergonomia pedagógica da solução.  
> A principal delas é a Minimização de Janelas Vagas Docentes (os Teacher Gaps). Se um professor dá a primeira aula no slot 1 e a última no slot 5, mas tem períodos vagos no meio, isso é quantificado e penalizado com peso 85.  
> A segunda é o Equilíbrio Diário: limitamos no máximo 2 aulas da mesma disciplina por dia na turma para evitar exaustão cognitiva dos estudantes.  
> Por fim, respeitamos preferências de turnos e dias sempre que houver empates de viabilidade."*

---

### Slide 6 — Função de Aptidão (*Fitness Function*) (05:30 - 06:45)
* **Objetivo:** Explicar como a matemática une as penalidades em um único valor escalar.
* **Fala sugerida:**  
> *"A pontuação da grade é calculada por uma função de custo a ser MINIMIZADA:  
> $f(S) = W_{hard} \cdot \sum H_i(S) + \sum w_j \cdot V_j(S)$.  
> O ponto crucial da nossa modelagem está no peso $W_{hard} = 100.000$, que atua como barreira dissuasiva extrema: qualquer choque explode o custo da solução.  
> Formalmente, a viabilidade da grade independe do custo suave: ela é viável se e somente se o somatório de violações duras for estritamente igual a zero: $\sum H_i(S) = 0$. A partir da garantia de zero choques, os pesos das restrições suaves ($w_{gap}=85$ e $w_{balance}=70$) guiam a metaheurística para lapidar o conforto pedagógico da grade."*

---

### Slide 7 — Heurística 1: O Pipeline Visual do DSatur (06:45 - 08:00)
* **Objetivo:** Explicar o fluxo Fail-First apontando para os 4 passos do diagrama.
* **Fala sugerida:**  
> *"Para resolver o problema, adotamos a arquitetura em Dois Estágios.  
> No Estágio 1, usamos uma Heurística Construtiva Gulosa inspirada no princípio de saturação do DSatur de Daniel Brélaz.  
> Olhem para o diagrama na tela: ele resume a intuição do algoritmo em 4 passos:  
> No Passo 1, temos a lista crua de matérias. O Prof. João só pode dar aula em 4 horários da semana, enquanto outros têm 20 horários livres.  
> No Passo 2, calculamos a Criticidade: quem tem menos opções livres recebe o maior peso.  
> No Passo 3, entra o princípio 'Fail-First' (Falhe Primeiro): o Prof. João vai para o início da fila prioritária! Por que? Porque se deixarmos para alocar o professor difícil no final, os horários dele terão esgotado e a grade vai travar em conflito.  
> No Passo 4, alocamos o João primeiro na matriz em memória RAM (o GridState). O resultado é espetacular: geramos uma grade com ZERO choques em menos de 100 milissegundos com complexidade $O(N \log N)$, entregando a semente inicial perfeita para a fase 2."*

---

### Slide 8 — Metaheurística 2: Simulated Annealing e o Gráfico de Energia (08:00 - 09:15)
* **Objetivo:** Explicar a curva de custo (Landscape) e por que o Simulated Annealing salta morros que travam o Hill Climbing.
* **Fala sugerida:**  
> *"Com a grade viável na mão, entramos no Estágio 2: a metaheurística de Simulated Annealing, formalizada por Kirkpatrick a partir do Critério de Metropolis.  
> Este gráfico de relevo de custo ilustra com clareza o maior problema da otimização:  
> Uma busca gulosa tradicional como o Hill Climbing desce a ladeira e cai neste primeiro vale raso: o ÓTIMO LOCAL. Aqui a grade tem 2 janelas vagas, mas nenhuma troca simples imediata melhora a situação. O Hill Climbing não tem visão de futuro: ele morre preso no ótimo local.  
> É aqui que brilha o Simulated Annealing: quando a temperatura $T$ está alta, o algoritmo tem licença matemática para aceitar pioras temporárias através da probabilidade $P = e^{-\Delta f / T}$. Ele aceita dar 'um passo atrás para dar dois à frente', saltando a barreira de custo e caindo no vale profundo do ÓTIMO GLOBAL, onde todas as janelas são eliminadas."*

---

### Slide 9 — Operadores de Vizinhança: O Swap Move na Prática (09:15 - 10:30)
* **Objetivo:** Mostrar o exemplo visual de terça-feira com a janela sendo eliminada e a blindagem.
* **Fala sugerida:**  
> *"E como o Simulated Annealing mexe na grade na prática? Através de operadores de perturbação de vizinhança, como o Swap Move intra-turma que vocês vêem neste slide.  
> Vejam o lado esquerdo: na terça-feira dessa turma, o Prof. João dá Física no Slot 1 e no Slot 3. O Slot 2 ficou vago. Isso é uma janela ociosa: o professor é obrigado a ficar 1 hora esperando no pátio da escola, o que gera estresse e cansaço.  
> O operador Swap Move faz uma troca cirúrgica: puxa a segunda aula de Física para o Slot 2 e antecipa a Matemática. As aulas de Física ficam geminadas consecutivas, a janela é eliminada e o custo cai 85 pontos de penalidade!  
> E um detalhe de segurança crucial: a troca SÓ é confirmada se o professor de Matemática estiver livre no novo slot. Se gerar choque com outra turma, o movimento é sumariamente cancelado. A busca opera 100% blindada dentro da região viável!"*

---

### Slide 10 — Síntese Comparativa & Conclusão (10:30 - 11:30)
* **Objetivo:** Fechar com autoridade técnica, contrastando os dois métodos.
* **Fala sugerida:**  
> *"Para sintetizar: o Algoritmo 1 é determinístico, constrói a grade do vazio em $O(N \log N)$ e seu foco é zerar restrições duras. O Algoritmo 2 é estocástico, parte da grade viável e usa perturbações de vizinhança guiadas por resfriamento para eliminar janelas vagas e otimizar as restrições fracas.  
> Essa hibridização em dois estágios contorna a barreira da explosão combinatória, permitindo entregar horários matematicamente perfeitos e humanamente confortáveis em frações de segundo.  
> Agradecemos a atenção do professor e dos colegas e estamos abertos às perguntas!"*
