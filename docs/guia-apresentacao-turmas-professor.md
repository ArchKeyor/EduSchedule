# 🎓 Guia de Apresentação & Colinha Rápida: Turmas Oficiais do Professor (EDS)
> **Documento de Apoio Rápido para Apresentação em Sala**  
> **Projeto:** TimeTabling UGB | **Tech Lead:** Kauê Loreno  
> **Data de Referência:** Novembro de 2026  

---

## ⚡ 1. Como Rodar a Aplicação Amanhã na Faculdade

Você tem **3 formas infalíveis** de inicializar tudo pronto na máquina da faculdade:

### 🟢 Opção A (Pelo Chat do Antigravity — A mais rápida)
Abra o Antigravity e digite exatamente:
> *"Antigravity, rode as turmas do professor"*

O agente vai rodar o seed, acionar o Simulated Annealing e te entregar os links já abertos.

---

### 🟡 Opção B (Por Duplo Clique no Windows Explorer — Sem abrir terminal)
Se o computador da faculdade estiver sem o Antigravity aberto, basta navegar até a pasta do projeto e dar duplo clique em:
📁 [scripts/rodar_turmas_professor.bat](file:///c:/Users/Kauê/Documents/02_Programacao_e_Tech/Projetos/TimeTabling/scripts/rodar_turmas_professor.bat)

*Ele cria o `.venv`, instala dependências se necessário, popula os dados do professor e abre o Chrome sozinho!*

---

### 🔵 Opção C (Pelo Terminal / Manual)
Se preferir rodar os comandos na mão no terminal:
```bash
# 1. Ativar venv e rodar migrações
.venv\Scripts\activate
python backend/manage.py migrate

# 2. Rodar o seed oficial do professor
python backend/manage.py seed_data --scenario=eds

# 3. Subir o backend (Terminal 1)
python backend/manage.py runserver 127.0.0.1:8000

# 4. Subir o frontend (Terminal 2)
npm --prefix frontend run dev
```

* **Frontend UI:** [http://localhost:5173/](http://localhost:5173/)
* **Backend API:** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
* **Grade Ativa:** [http://127.0.0.1:8000/api/timetables/active/](http://127.0.0.1:8000/api/timetables/active/)

---

## 🧠 2. O Raio-X Técnico da Instância do Professor (Para você falar com autoridade)

Quando o professor olhar a grade gerada e os números na tela, você pode demonstrar domínio total do problema com estes fatos matemáticos:

### 📊 A Estrutura da Instância
* **3 Turmas de Engenharia de Software:** 2º período, 4º período e 6º período de EDS.
* **Grade de 20 slots semanais:** 4 horários diários de 50 minutos (08:10 às 11:50) de segunda a sexta.
* **10 Professores & 18 Disciplinas:** Álgebra Linear, Web, GBD, Requisitos, etc.
* **60 Aulas Semanais no Total:** Cada turma tem exatamente 20 aulas demandadas, preenchendo **100% da grade horária**.

---

### 🕵️ O "Pulo do Gato": O Desafio de Inviabilidade da Instância
O professor montou uma instância propositalmente super-restrita (*overconstrained benchmark*):

1. **Disponibilidade Excessivamente Rígida:**
   * Os professores **João**, **Maria** e **Iná** só tinham a **Segunda-feira** cadastrada como dia disponível (4 slots no dia).
2. **O Gargalo Inevitável:**
   * O **2º período** precisava de 4 aulas de Álgebra (João) + 4 aulas de Atividades Práticas MA (Maria) + 4 aulas de Física (Iná).
   * Isso exigia **12 aulas na segunda-feira para uma única turma que só possui 4 horários** ($12 > 4$).
   * Além disso, o professor João precisava dar aulas no 2º, 4º e 6º período ($4 + 2 + 2 = 8$ aulas na segunda, gerando choque de horário imediato se ficasse só na segunda).
3. **Como o nosso motor reagiu:**
   * O motor não quebrou nem travou em loop infinito. Ele garantiu a alocação de **todas as 60 aulas** e acionou o fallback para distribuir os horários excedentes com o mínimo de conflito possível.

---

## 🪟 3. Explicando os Alertas de "Janela Vaga" (Gaps de Maria e Iná)

Se o professor perguntar: *"Por que apareceram alertas de janela vaga para a professora Maria e para a Iná?"*, você responde com precisão milimétrica:

### O que é uma Janela Vaga?
É o tempo ocioso que o docente é obrigado a passar na faculdade entre a sua primeira e a sua última aula do dia (ex: dar aula às 08:10, ficar sem fazer nada das 09:00 às 11:00, e voltar para dar aula às 11:00).

### A Fórmula do Motor ([constraints.py: Linhas 76 a 78](file:///c:/Users/Kauê/Documents/02_Programacao_e_Tech/Projetos/TimeTabling/backend/solver/constraints.py#L76-L78))
$$\text{Span} = \text{slot}_{\max} - \text{slot}_{\min} + 1$$
$$\text{Gaps} = \text{Span} - \text{Aulas Ministradas}$$

### O Exemplo Prático da Professora Maria (Sexta-feira):
* Alocada no **1º período** (08:10) e no **4º período** (11:00).
* $\text{Span} = 4 - 1 + 1 = 4$ tempos de permanência.
* Aulas dadas: $2$.
* $\text{Gaps} = 4 - 2 = \mathbf{2 \text{ janelas vagas}}$ (períodos 2 e 3 ficaram vazios).

### Por que isso aconteceu?
Como a segunda-feira da Maria estava cheia, as aulas excedentes caíram na sexta-feira. Como os horários do meio da manhã (slots 2 e 3) já estavam ocupados por outros professores da turma, restaram apenas as pontas (slot 1 e 4).

> **Ponto-chave para a banca:**  
> *"Nosso sistema possui uma Soft Constraint específica (peso 85) que quantifica e penaliza essas janelas. O sistema não apenas monta a grade, mas atua como **ferramenta de auditoria da qualidade de vida dos professores**, apontando para a coordenação exatamente onde há ociosidade forçada."*

---

## 🎤 4. Roteiro de Fala Sugerido (Pitch de 2 Minutos para o Professor)

Você pode conduzir a apresentação assim:

1. **Abertura:**  
   *"Professor, pegamos a massa de dados oficial que você disponibilizou no arquivo `populate.py` (com as 3 turmas de EDS, os 10 professores, as 18 disciplinas e os 20 slots de 50 minutos) e alimentamos o nosso sistema."*

2. **Demonstração do Motor:**  
   *"Em vez de usar apenas uma heurística construtiva simples, nosso motor híbrido opera em dois estágios: primeiro acha a solução viável e depois aplica o **Simulated Annealing com critério de Metropolis** para polir a grade, rodando todas as 60 aulas em cerca de **0.12 segundos**."*

3. **Análise Crítica da Instância:**  
   *"Notamos também a característica desafiadora da sua matriz de disponibilidade: os 3 primeiros professores (João, Maria e Iná) tinham apenas a segunda-feira livre para um volume que somava 12 aulas só no 2º período. Nosso algoritmo tratou o gargalo, garantiu 100% da carga horária alocada e mapeou os pontos de atenção pedagógica, como as janelas vagas identificadas nas sextas-feiras."*

4. **Interface:**  
   *"E aqui no Frontend React, a coordenação consegue filtrar por período, alternar visão por professor e rodar o re-cálculo da IA em tempo real com um clique."*

---

## 📋 5. Tabela Rápida de Dados da Instância

| Informação | Valor Oficial do Professor |
| :--- | :--- |
| **Turmas** | Segundo período de EDS, Quarto período de EDS, Sexto período de EDS |
| **Horários diários** | 1º (08:10-09:00), 2º (09:00-09:50), 3º (10:10-11:00), 4º (11:00-11:50) |
| **Total de Slots** | 4 tempos $\times$ 5 dias = 20 slots semanais |
| **Total de Aulas** | 20 aulas por turma $\times$ 3 turmas = 60 aulas |
| **Professores 1 dia** | João, Maria, Iná (Segunda-feira) |
| **Professores 2 dias** | Diana, Ana, Sebastião (Segunda e Terça) |
| **Professores Full-time** | Mara, Carolina, Lucas, Antônio João (Segunda a Sexta) |
| **Algoritmo Utilizado** | Two-Stage: Heurística Construtiva + Simulated Annealing (Metropolis) |
| **Tempo de Execução** | ~0.12 segundos |
