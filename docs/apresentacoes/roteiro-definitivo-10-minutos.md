# 🎙️ Guia & Roteiro Híbrido de Apresentação de TCC (10 Minutos)

> **Projeto:** Sistema de Geração Automática de Horários Escolares e Acadêmicos (TimeTabling)  
> **Formato:** Roteiro Híbrido (Mapa Mental de Objetivos + Fala Exemplo Articulada)  
> **Dupla:** Kauê Loreno Lopes (Tech Lead & Otimização) e Pedro Henrique Dias (Frontend & Demonstração)  
> **Orientador:** Prof. Thailan  
> **Instituição:** Centro Universitário Geraldo Di Biase (UGB) — Curso de Engenharia de Software  

---

## ⏱️ Distribuição de Tempo da Apresentação

```
00:00 ────────────── 01:00 ──────────────────────────────────────── 06:45 ─────────────────────── 10:00
 [ Pedro: Capa e Agenda ]      [ Kauê: Teoria, Arquitetura, RAM e Resultados ]    [ Pedro: Demonstração na Azure ]
       (1m 00s)                                (5m 45s)                                    (3m 15s)
```

---

# PARTE 1: APRESENTAÇÃO DOS SLIDES (00:00 às 06:45)

---

### [Slide 1/15] Capa Institucional
* **Orador:** Pedro  
* **Tempo:** 30 segundos | **Cronômetro:** 00:00 ➔ 00:30  
* **Fio Condutor do Slide:** Título formal com modelo CB-CTT, identificação dos autores, do orientador Prof. Thailan e do curso de Engenharia de Software do UGB.

#### 🎯 Objetivos & Conceitos-Chave:
* Cumprimentar a banca examinadora e o orientador com postura acadêmica e formal;
* Apresentar o título do trabalho destacando que não é apenas um "gerador de horários", mas uma **abordagem heurística desacoplada sob o modelo CB-CTT**;
* Posicionar o projeto na intersecção entre Engenharia de Software e Pesquisa Operacional.

#### 🗣️ Exemplo de Fala Articulada:
> *"Bom dia aos ilustres professores da banca examinadora e ao nosso orientador, Professor Thailan.  
> Meu nome é Pedro Henrique Dias e, juntamente com o Kauê Loreno Lopes, apresentamos a defesa do nosso Trabalho de Conclusão de Curso em Engenharia de Software: **Sistema de Geração Automática de Horários Escolares e Acadêmicos (TimeTabling): Uma Abordagem Heurística Desacoplada sob o Modelo Curriculum-Based Course Timetabling**."*

* **Transição:** Avança para a Agenda.

---

### [Slide 2/15] Agenda da Apresentação
* **Orador:** Pedro  
* **Tempo:** 30 segundos | **Cronômetro:** 00:30 ➔ 01:00  
* **Fio Condutor do Slide:** Diagrama circular em 4 quadrantes numerados situando o fluxo da defesa.

#### 🎯 Objetivos & Conceitos-Chave:
* Situar a banca no encadeamento lógico do trabalho (Introdução ➔ Teoria ➔ Engenharia ➔ Resultados/Demo);
* Deixar claro desde o primeiro minuto que a apresentação culminará em uma demonstração prática ao vivo na nuvem da Microsoft Azure;
* Fazer a transição de voz para o Kauê assumir o desenvolvimento técnico.

#### 🗣️ Exemplo de Fala Articulada:
> *"A nossa apresentação está estruturada em quatro eixos fundamentais:  
> Iniciamos com a **Introdução**, abordando o custo operacional e o impacto social do problema;  
> Passamos pela **Fundamentação Teórica**, com os conceitos de complexidade matemática e heurísticas de saturação;  
> Detalhamos o **Desenvolvimento**, evidenciando nossa arquitetura desacoplada e o motor em memória RAM;  
> E finalizamos com as **Conclusões e Resultados**, seguidas da demonstração ao vivo da aplicação em produção na nuvem da Microsoft Azure.  
> Passo agora a palavra para o Kauê dar início à nossa contextualização."*

* **Transição:** Pedro entrega o passador de slides e a fala para o Kauê.

---

### [Slide 3/15] INTRODUÇÃO — O Cenário & Custo de Gestão
* **Orador:** Kauê  
* **Tempo:** 30 segundos | **Cronômetro:** 01:00 ➔ 01:30  
* **Fio Condutor do Slide:** Hexágonos com as dores do processo manual (demora de 2 a 3 semanas, choques, rigidez) e o box conceitual do modelo CB-CTT.

#### 🎯 Objetivos & Conceitos-Chave:
* **A dor da vida real:** Explicar que a montagem manual é um gargalo não por lentidão humana, mas porque o cérebro não processa colisões multidimensionais;
* **O modelo CB-CTT (Curriculum-Based):** Definir as **coortes curriculares** (turmas fechadas que precisam de grade completa) versus **professores compartilhados**;
* **O efeito dominó:** Demonstrar que qualquer alteração de disponibilidade de um professor exige reconstruir a grade de dezenas de turmas.

#### 🗣️ Exemplo de Fala Articulada:
> *"Obrigado, Pedro. A elaboração de horários nas instituições de ensino ainda é realizada de forma artesanal. Coordenadores pedagógicos despendem de duas a três semanas por semestre cruzando murais e planilhas, enfrentando choques de horários e um desgaste extremo.  
> O foco do nosso trabalho é o paradigma **CB-CTT (Curriculum-Based Course Timetabling)**: nele, lidamos com **coortes curriculares** — turmas com pacotes fechados de matérias obrigatórias — e professores que lecionam em múltiplos cursos. Se um docente pede uma troca de turno, cria-se um efeito dominó que inviabiliza a resolução puramente manual."*

* **Transição:** Avança para a complexidade matemática e relevância social.

---

### [Slide 4/15] INTRODUÇÃO — A Barreira Matemática $O(S^A)$ & Relevância Social
* **Orador:** Kauê  
* **Tempo:** 35 segundos | **Cronômetro:** 01:30 ➔ 02:05  
* **Fio Condutor do Slide:** Tabela comparativa à esquerda (Força bruta $O(S^A)$, MILP >262k var vs Heurística em RAM) e o box de Relevância Social de Tardif & Lessard (2014) à direita.

#### 🎯 Objetivos & Conceitos-Chave:
* **A matemática do problema:** Explicar que tentar força bruta gera um espaço de busca exponencial na ordem de **$S$ elevado a $A$ ($O(S^A)$)**, superando centenas de dígitos decimais ($25^{100} > 10^{140}$);
* **A limitação de solvers exatos (MILP):** Provar que métodos de Programação Linear Inteira Mista geram centenas de milhares de variáveis binárias que estouram a memória RAM em produção web;
* **Relevância Social (Tardif & Lessard, 2014):** Defender que horários fragmentados criam **janelas ociosas (gaps)** entre períodos letivos, comprovadas pela sociologia da educação como causadoras de **estresse crônico, absenteísmo e esgotamento profissional (burnout) docente**.

#### 🗣️ Exemplo de Fala Articulada:
> *"Matematicamente, a resolução por força bruta é inviável: para $A$ aulas distribuídas em $S$ slots semanais, o espaço combinatório cresce na **ordem exponencial de S elevado a A**, gerando mais combinações do que átomos no universo observável. Mesmo solucionadores exatos de Programação Linear (MILP) estouram a memória de servidores ao manipular mais de 260 mil variáveis binárias.  
> Além disso, há uma urgente **relevância social**: como comprovado pelos sociólogos **Tardif e Lessard (2014)**, grades fragmentadas que forçam janelas ociosas na rotina do professor são causas diretas de **estresse crônico, absenteísmo e esgotamento profissional (burnout)**. Nosso software atua na proteção à saúde docente."*

* **Transição:** Avança para o contraste entre Problema e Objetivo.

---

### [Slide 5/15] Problemática & Objetivo Geral
* **Orador:** Kauê  
* **Tempo:** 25 segundos | **Cronômetro:** 02:05 ➔ 02:30  
* **Fio Condutor do Slide:** Duas caixas centrais em alto contraste: o que dói (Problemática) versus a solução de engenharia (Objetivo Geral).

#### 🎯 Objetivos & Conceitos-Chave:
* Estabelecer a declaração de missão técnica do projeto;
* Prometer a entrega de uma aplicação web desacoplada sob Clean Architecture;
* Definir as metas de sucesso mensuráveis: **zero choques de horários** e tempo de resposta **inferior a 1 segundo**.

#### 🗣️ Exemplo de Fala Articulada:
> *"Diante desse cenário, a nossa **Problemática** é eliminar a lentidão operacional, a incidência de conflitos e a sobrecarga docente provocadas pela montagem manual de grades curriculares.  
> E o nosso **Objetivo Geral** é desenvolver uma aplicação web fundamentada em Clean Architecture, dotada de um motor de otimização em memória RAM, capaz de gerar grades matematicamente viáveis — com **zero choques de horários** — em tempo inferior a 1 segundo, operando sob o modelo CB-CTT."*

* **Transição:** Avança para a fundamentação matemática formal.

---

### [Slide 6/15] Fundamentação Teórica — O Modelo CB-CTT & Dualidade de Complexidade
* **Orador:** Kauê  
* **Tempo:** 35 segundos | **Cronômetro:** 02:30 ➔ 03:05  
* **Fio Condutor do Slide:** Card superior definindo Coortes Curriculares e dois cards comparativos: Hard Constraints (NP-Completo) à esquerda e Soft Constraints (NP-Hard) à direita.

#### 🎯 Objetivos & Conceitos-Chave:
* **Coortes no CB-CTT:** Explicar que a unidade básica de planejamento é a turma fechada e não a matrícula individual de alunos;
* **Hard Constraints $\rightarrow$ NP-Completo:** Explicar a versão de **Decisão** (*"Existe uma grade válida com zero colisões?"*), provada formalmente como **NP-Completa** por Even, Itai e Shamir (1976), verificável em tempo polinomial $O(N)$;
* **Soft Constraints $\rightarrow$ NP-Hard:** Explicar a versão de **Otimização** (*"Qual a melhor grade que minimiza janelas vagas?"*), classificada como **NP-Hard (NP-Difícil)** por Schaerf (1999) devido ao espaço de busca multimodal.

#### 🗣️ Exemplo de Fala Articulada:
> *"Entrando na fundamentação teórica, o modelo **CB-CTT** estrutura o planejamento através de **coortes curriculares** — grupos fechados de alunos que cursam as mesmas matérias obrigatórias. A literatura clássica decompõe as restrições em duas naturezas computacionais distintas:  
> 1. As **Hard Constraints** garantem a viabilidade física estrita: proibir choque de professor, choque de turma e respeitar bloqueios de agenda. Esta é a versão de decisão do problema, provada como **NP-Completa** por Even, Itai e Shamir em 1976.  
> 2. As **Soft Constraints** medem a ergonomia pedagógica: minimizar janelas vagas e compactar a jornada. Esta é a versão de otimização, formalmente **NP-Hard** (Schaerf, 1999)."*

* **Transição:** Avança para a estratégia algorítmica de resolução.

---

### [Slide 7/15] Fundamentação Teórica — Princípio Fail-First & Criticidade
* **Orador:** Kauê  
* **Tempo:** 35 segundos | **Cronômetro:** 03:05 ➔ 03:40  
* **Fio Condutor do Slide:** Card de Brélaz (1979 - Saturação DSatur) e Card de Carter et al. (1996 - Criticidade em Timetabling / Pedras grandes).

#### 🎯 Objetivos & Conceitos-Chave:
* **O algoritmo DSatur (Brélaz, 1979):** Explicar o princípio *Fail-First* — alocar primeiro o vértice que possui o menor número de opções disponíveis para prevenir deadlocks combinatórios;
* **A métrica de Carter et al. (1996):** Explicar como Carter adaptou a saturação de grafos para a rotina de escolas reais:
  * *Most Constrained First (MCF):* Docentes com menos dias livres na semana entram primeiro;
  * *Largest Workload:* Disciplinas com maior carga horária entram antes das menores;
* **Complexidade Assintótica:** Destacar que a ordenação da fila de prioridades opera em tempo **$O(N \log N)$**, executando em microssegundos.

#### 🗣️ Exemplo de Fala Articulada:
> *"Para resolver as restrições rígidas em milissegundos sem cair em travamentos combinatórios, adotamos o algoritmo **DSatur de Daniel Brélaz (1979)** aliado ao princípio **Fail-First**.  
> É a metáfora das 'pedras grandes no balde': alocamos o mais difícil primeiro.  
> Aplicando os estudos de **Carter et al. (1996)** específicos para timetabling, o nosso motor calcula a criticidade da demanda: professores com agendas mais rígidas e disciplinas de maior carga horária semanal entram prioritariamente na grade. Essa ordenação inteligente roda em complexidade **$O(N \log N)$** e previne deadlocks antes da inserção."*

* **Transição:** Avança para o pipeline de resolução em dois estágios.

---

### [Slide 8/15] Fundamentação Teórica — Resolução em Dois Estágios & Warm Start
* **Orador:** Kauê  
* **Tempo:** 30 segundos | **Cronômetro:** 03:40 ➔ 04:10  
* **Fio Condutor do Slide:** Diagrama de fluxo conectando o Bloco 1 (Estágio 1 - Entrega Atual da Fatia 1) através da seta de Warm Start até o Bloco 2 (Estágio 2 - Fase 2 / Busca Local).

#### 🎯 Objetivos & Conceitos-Chave:
* **Desacoplamento de complexidade:** Explicar que separar a busca por viabilidade física da busca por qualidade pedagógica é o segredo para não travar o sistema;
* **Estágio 1 (Nossa Fatia 1):** Construtor guloso na RAM focado 100% em viabilidade física (0 choques) entregue em frações de segundo, atuando como semente inicial (**Warm Start**);
* **Estágio 2 (Fase 2 Futura):** Metaheurística de busca local que realiza trocas de vizinhança (*swap moves*) unicamente para polir as restrições flexíveis;
* **Aceleração comprovada:** Citar Burke et al. (1998) — inicializar a busca a partir de um Warm Start viável supera drasticamente abordagens que começam do zero.

#### 🗣️ Exemplo de Fala Articulada:
> *"Com base nessa fundamentação, estruturamos a resolução em **Dois Estágios**:  
> O **Estágio 1** é a entrega central da nossa primeira fatia vertical: uma heurística construtiva gulosa na RAM focada exclusivamente em viabilidade física. Ela gera uma grade sem nenhum choque de horários em milissegundos, fornecendo uma semente de alta qualidade denominada **Warm Start**.  
> O **Estágio 2**, planejado como trabalho futuro, realiza trocas locais de horários (*swap moves*) unicamente para compactar a grade e eliminar janelas vagas, sem quebrar as restrições rígidas já conquistadas. Como provado por Burke et al. (1998), inicializar a busca a partir de um Warm Start acelera drasticamente a convergência."*

* **Transição:** Avança para a arquitetura de software implementada.

---

### [Slide 9/15] Desenvolvimento — Arquitetura em 3 Camadas Desacopladas
* **Orador:** Kauê  
* **Tempo:** 35 segundos | **Cronômetro:** 04:10 ➔ 04:45  
* **Fio Condutor do Slide:** Diagrama de 3 camadas conectadas (React SPA ➔ Django REST API ➔ Solver Engine em Python puro) amparadas na ADR 001.

#### 🎯 Objetivos & Conceitos-Chave:
* **Metodologia de Engenharia:** Citar que o projeto seguiu a metodologia de **Pesquisa Aplicada orientada a Fatias Verticais (Vertical Slices)**;
* **Clean Architecture & Strategy:** Explicar que a camada do Solver não conhece banco de dados nem frameworks HTTP;
* **A decisão crítica de performance (Zero I/O):** Destacar que o maior gargalo de softwares acadêmicos é fazer queries SQL dentro do loop do algoritmo. No TimeTabling, o banco só é tocado na leitura inicial e na gravação final.

#### 🗣️ Exemplo de Fala Articulada:
> *"Para materializar essa solução sob a metodologia de **Pesquisa Aplicada e Fatias Verticais**, desenhamos uma arquitetura estritamente desacoplada ([ADR 001](file:///c:/Users/Kauê/Documents/02_Programacao_e_Tech/Projetos/TimeTabling/docs/decisoes-arquiteturais.md)):  
> A Camada de Apresentação em **React 18 com TypeScript**, a Camada de Aplicação em **Django REST Framework** e a Camada do Motor com o **Solver isolado em Python puro**, aderindo aos princípios de Clean Architecture e ao padrão Strategy.  
> A decisão de engenharia mais determinante: **zero queries de banco de dados dentro do loop combinatorial**. O banco de dados só é acionado na carga inicial e na persistência final. Toda a combinatória executa 100% na CPU e na memória RAM, eliminando gargalos de I/O em disco."*

* **Transição:** Avança para a modelagem semântica de dados.

---

### [Slide 10/15] Desenvolvimento — Modelagem Semântica de Dados (ADR 006)
* **Orador:** Kauê  
* **Tempo:** 30 segundos | **Cronômetro:** 04:45 ➔ 05:15  
* **Fio Condutor do Slide:** Diagrama relacional separando `CurriculumRequirement` (intenção) de `TimetableSlotAssignment` (alocação) e os números da massa de testes.

#### 🎯 Objetivos & Conceitos-Chave:
* **Segregação semântica (ADR 006):** Explicar por que não salvar horários na tabela de matérias — isso impediria múltiplos cenários;
* **Versionamento de grades:** Demonstrar que separar intenção de alocação permite gerar múltiplos cenários alternativos (Grade A vs Grade B) para a mesma turma;
* **A massa real homologada (`seed_data.py`):** Apresentar os números reais de teste: 14 turmas ativas, 50 professores e 275 restrições de agenda mapeadas.

#### 🗣️ Exemplo de Fala Articulada:
> *"Na modelagem de dados ([ADR 006](file:///c:/Users/Kauê/Documents/02_Programacao_e_Tech/Projetos/TimeTabling/docs/decisoes-arquiteturais.md)), estabelecemos a separação estrita entre a **Demanda Curricular** (`CurriculumRequirement` — a intenção pedagógica) e a **Alocação de Horário** (`TimetableSlotAssignment` — o resultado calculado pelo solver).  
> Essa segregação confere ao sistema a capacidade de **versionamento de grades**: a coordenação pode gerar múltiplos cenários alternativos para homologação sem duplicar cadastros no banco.  
> Para certificar a aplicação, estruturamos uma massa de testes reais composta por 14 turmas curriculares, 50 professores e 275 bloqueios de disponibilidade mapeados."*

* **Transição:** Avança para a mecânica de memória do motor.

---

### [Slide 11/15] Desenvolvimento — O Motor em RAM (`GridState`) & Acesso em $O(1)$
* **Orador:** Kauê  
* **Tempo:** 35 segundos | **Cronômetro:** 05:15 ➔ 05:50  
* **Fio Condutor do Slide:** Matrizes binárias de 0 e 1 (`MatrizDocente` e `MatrizTurma`) indexadas por `[dia, slot]` e o fluxo sequencial atômico 1-2-3-4.

#### 🎯 Objetivos & Conceitos-Chave:
* **O tensor matricial:** Explicar que o estado das alocações é representado por matrizes bidimensionais em Python puro mantidas na memória primária;
* **Acesso em tempo constante $O(1)$:** Desmistificar o conceito técnico — checar disponibilidade acessando índices da matriz (`matriz[dia][slot]`) é uma instrução direta de hardware de 1 ciclo de clock de CPU, sem nenhum laço de repetição (`for`);
* **Escalabilidade:** Demonstrar que testar uma colisão leva nanossegundos, independentemente de a escola ter 10 ou 1.000 professores.

#### 🗣️ Exemplo de Fala Articulada:
> *"No núcleo do solver, instanciamos a estrutura `GridState`: matrizes tensoriais por dia e período letivo mantidas na memória primária.  
> Em vez de percorrer listas com laços de repetição ou executar consultas SQL, a verificação de colisões ocorre por acesso indexado direto às matrizes binárias de docentes e turmas.  
> Como o acesso por coordenada em memória é uma operação de **tempo constante O(1)**, testar se um professor e uma turma estão simultaneamente disponíveis consome apenas um ciclo de instrução de CPU. Esse processamento atômico em memória RAM é o que viabiliza gerar a grade completa de forma instantânea."*

* **Transição:** Avança para a validação experimental e resultados.

---

### [Slide 12/15] Análise de Resultados — Benchmark Operacional
* **Orador:** Kauê  
* **Tempo:** 30 segundos | **Cronômetro:** 05:50 ➔ 06:20  
* **Fio Condutor do Slide:** Card superior com o Cenário de Teste Homologado e a tabela de métricas comparando alvos estabelecidos versus resultados obtidos na Fatia 1.

#### 🎯 Objetivos & Conceitos-Chave:
* **Rigor experimental da amostra:** Deixar explícito que os 0,08 segundos foram mensurados sobre a **massa homologada** (14 turmas, 50 professores e 275 bloqueios de agenda), estabelecendo postura científica honesta;
* **Superação de meta:** Comparar com a especificação original: nosso teto era de 5,0 segundos e atingimos **0,08 segundos na RAM**, sendo mais de **60 vezes mais rápido** que o limite aceitável;
* **Viabilidade estrita (100%):** Enfatizar zero choques de turmas, zero choques de professores, respeito total às restrições contratuais e persistência atômica via `transaction.atomic` no PostgreSQL 16.

#### 🗣️ Exemplo de Fala Articulada:
> *"No Slide 12, apresentamos o benchmark operacional da nossa primeira fatia vertical.  
> Pontuamos com transparência acadêmica: **este resultado de 0,08 segundos refere-se estritamente à nossa massa experimental de testes**, composta por 14 turmas, 50 docentes e 275 restrições de agenda.  
> Para esse cenário representativo, o motor executou **60 vezes mais rápido** do que o teto de 5 segundos estipulado pelo projeto.  
> Atingimos **100% de viabilidade física estrita**: zero choques de professores, zero choques de turmas e respeito integral a todos os bloqueios de disponibilidade, com persistência transacional atômica assegurada no PostgreSQL."*

* **Transição:** Avança para as considerações finais e trabalhos futuros.

---

### [Slide 13/15] Conclusão & Trabalhos Futuros
* **Orador:** Kauê  
* **Tempo:** 20 segundos | **Cronômetro:** 06:20 ➔ 06:40  
* **Fio Condutor do Slide:** 4 quadrantes sintetizando viabilidade comprovada, arquitetura desacoplada, busca local pedagógica e integração de solvers externos.

#### 🎯 Objetivos & Conceitos-Chave:
* Consolidar a vitória técnica da primeira fatia vertical;
* Apontar a continuidade da pesquisa com busca local para otimização ergonômica (combate ao burnout docente de Tardif & Lessard);
* Destacar a extensibilidade do padrão Strategy para plugar solvers de mercado como o Google OR-Tools (CP-SAT), utilizando a solução atual como Warm Start.

#### 🗣️ Exemplo de Fala Articulada:
> *"Concluímos comprovando a viabilidade do modelo CB-CTT com heurística construtiva para geração em tempo real de grades viáveis em ambiente web.  
> Como trabalhos futuros, a Fase 2 focará na busca local para redução de janelas vagas na jornada docente, bem como na experimentação de solvers alternativos como o **Google OR-Tools CP-SAT**, que poderá ser acoplado com facilidade graças ao padrão Strategy da nossa Clean Architecture."*

* **Transição:** Passagem ágil pelas referências bibliográficas.

---

### [Slide 14/15] Referências Bibliográficas
* **Orador:** Kauê  
* **Tempo:** 05 segundos | **Cronômetro:** 06:40 ➔ 06:45  
* **Fio Condutor do Slide:** Duas colunas com a literatura canônica citada ao longo da defesa.

#### 🎯 Objetivos & Conceitos-Chave:
* Demonstrar solidez teórica formal sem interromper a fluidez da apresentação.

#### 🗣️ Exemplo de Fala Articulada:
> *"Aqui listamos as referências canônicas de Pesquisa Operacional e Engenharia de Software que fundamentaram rigorosamente o nosso trabalho..."*

* **Transição:** Avança para o slide de encerramento e transição.

---

### [Slide 15/15] Transição para a Demonstração Prática na Nuvem
* **Orador:** Kauê  
* **Tempo:** 10 segundos | **Cronômetro:** 06:45 ➔ 06:55  
* **Fio Condutor do Slide:** Card de fechamento com logo da nuvem Microsoft Azure e chamada formal para a banca.

#### 🎯 Objetivos & Conceitos-Chave:
* Fazer a transição de voz para o Pedro de forma confiante, convidando a banca a ver o sistema funcionando em ambiente de produção real.

#### 🗣️ Exemplo de Fala Articulada:
> *"E para comprovar que o TimeTabling não é apenas um modelo conceitual, passo a palavra de volta ao Pedro, que conduzirá a demonstração prática da aplicação operando ao vivo na nuvem da Microsoft Azure."*

* **Transição:** Kauê encerra os slides. Pedro assume o mouse e a tela cheia no navegador com a Azure aberta!

---

# PARTE 2: DEMONSTRAÇÃO PRÁTICA NA AZURE (06:55 às 10:00)

* **Orador:** Pedro  
* **Tempo Total da Demo:** 3 minutos e 05 segundos | **Cronômetro:** 06:55 ➔ 10:00  

---

### 1. Visão Geral da Arquitetura em Produção e Telas (40 segundos | até 07:35)
* **Ação na Tela:** Navegar pelo menu lateral do sistema na Azure (Painel Geral, Turmas, Professores e Disciplinas).
* **Fio Condutor:** Mostrar que o software está conteinerizado e online na nuvem, com dados reais carregados.
* **🗣️ Fala do Pedro:**  
> *"Obrigado, Kauê. Senhores da banca, esta é a aplicação TimeTabling operando em ambiente de produção na nuvem da Microsoft Azure, conteinerizada sob Docker com banco de dados PostgreSQL 16.  
> A interface reativa foi construída em React 18 com Tailwind CSS, proporcionando uma experiência fluida para a equipe gestora.  
> Como podem observar no painel de administração, o sistema já se encontra populado com a nossa massa homologada de dados reais: temos aqui as 14 turmas cadastradas, os 50 professores e a relação de disciplinas da instituição."*

---

### 2. Demonstração de CRUD & Regra de Negócio Dinâmica (50 segundos | até 08:25)
* **Ação na Tela:** Acessar o módulo de **Professores**, selecionar um docente e **bloquear um horário de aula na semana** (ex: marcar indisponibilidade na sexta-feira de manhã), salvando com confirmação na tela.
* **Fio Condutor:** Provar que as restrições são dinâmicas e persistem atomicamente no banco PostgreSQL.
* **🗣️ Fala do Pedro:**  
> *"Para demonstrar o fluxo de negócio em tempo real, vou acessar o painel do corpo docente.  
> Suponhamos que um determinado professor nos comunique formalmente que não poderá mais lecionar na sexta-feira pela manhã por compromissos em outra instituição. Eu seleciono a matriz de disponibilidade deste professor, bloqueio o período correspondente e aciono o salvamento.  
> A alteração é despachada para a nossa API em Django REST e persistida atomicamente no banco PostgreSQL, atualizando instantaneamente as matrizes de restrição do sistema."*

---

### 3. O Ponto Alto: Disparo do Solver e Renderização da Grade (60 segundos | até 09:25)
* **Ação na Tela:** Navegar para a tela de **Geração de Horários**. Selecionar o turno e clicar no botão de ação principal: **"Gerar Grade Horária"**. A grade semanal completa deve ser preenchida instantaneamente na tela.
* **Fio Condutor:** Demonstrar visualmente a ausência de colisões e o respeito integral à regra cadastrada minutos antes.
* **🗣️ Fala do Pedro:**  
> *"Agora vamos ao núcleo da nossa solução: a geração automática da grade semanal.  
> Ao acionar o botão 'Gerar Grade', a API despacha as matrizes de demanda para o nosso motor de cálculo isolado em memória RAM.  
> [Pedro clica no botão — a grade semanal é preenchida instantaneamente na tela].  
> Notem que, em fração de segundo, a grade curricular completa foi calculada e renderizada.  
> E o mais importante: com **100% de conformidade às restrições rígidas**. Não há choque de professores, as turmas não possuem disciplinas sobrepostas e o bloqueio de sexta-feira que acabamos de cadastrar foi rigorosamente respeitado pelo algoritmo."*

---

### 4. Fechamento e Encerramento com a Banca (35 segundos | até 10:00)
* **Ação na Tela:** Manter a grade gerada na tela ou exibir o painel de integridade com zero conflitos.
* **Fio Condutor:** Conclusão segura, agradecimento aos professores e abertura para a arguição.
* **🗣️ Fala do Pedro:**  
> *"Com esta demonstração, comprovamos o cumprimento integral dos objetivos da nossa primeira fatia vertical: entregamos uma aplicação web estável, arquiteturalmente desacoplada, fundamentada na literatura de otimização combinatória e capaz de gerar grades viáveis em tempo real na nuvem.  
> Agradecemos imensamente a atenção de todos os professores da banca examinadora e do nosso orientador, Professor Thailan. Estamos abertos e à inteira disposição para as perguntas e considerações da banca."*

---

## 💡 Dicas de Execução para a Dupla
1. **O slide é o gatilho, não a leitura:** Quando o Kauê estiver no Slide 11, basta olhar para as matrizes na tela para lembrar: *"matrizes em RAM, índice [dia, slot], tempo O(1), ciclo de instrução de hardware"*. O cérebro puxa o resto naturalmente.
2. **Postura de Tech Lead do Kauê:** Nos slides 6, 9 e 11, fale com calma e firmeza. Demonstrar que você entende o porquê do algoritmo ser rápido impressiona muito mais do que falar depressa.
3. **Pedro com a máquina quente:** Deixe o navegador na Azure já logado e testado antes da banca começar. A demo de 3 minutos é o golpe final para garantir nota 10.
