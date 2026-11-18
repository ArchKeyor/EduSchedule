# Perguntas Técnicas para o Q&A (Defesa das Outras Equipes)

> **Critério de Avaliação do Prof. Marcelo Arantes:**  
> *"Perguntas e Respostas (Q&A) — 0,5 ponto: Participação crítica durante as defesas. A equipe avaliada deverá obrigatoriamente formular perguntas técnicas às outras equipes durante as demais apresentações."*

Para garantir essa pontuação máxima de 0,5 ponto com elegância e autoridade técnica, utilize o catálogo abaixo. Escolha a pergunta que se encaixe no algoritmo ou na modelagem que o outro grupo estiver apresentando:

---

### 📌 Se a equipe usou **Algoritmo Genético (GA)**:
> *"Vocês mencionaram que usaram Algoritmos Genéticos. Como vocês trataram o operador de Crossover para evitar gerar indivíduos inviáveis? Porque, se você fizer um corte e recombinação direta nos cromossomos de horário, é quase certo que vai duplicar aulas de um professor ou deixar turmas sem professor no mesmo slot. Vocês usaram algum operador de reparo pós-crossover ou modelaram com uma representação indireta (como Permutation Encoding)?"*

* **Por que essa pergunta é excelente:** O Calcanhar de Aquiles dos Algoritmos Genéticos em Timetabling é que o crossover tradicional destrói a viabilidade física. Quase nenhum aluno pensa nisso e essa pergunta demonstra conhecimento profundo de otimização combinatória.

---

### 📌 Se a equipe usou **Busca Tabu (Tabu Search)**:
> *"Na Busca Tabu de vocês, qual foi o critério adotado para definir o tamanho da Lista Tabu (Tabu Tenure)? E vocês implementaram algum 'Critério de Aspiração' para permitir um movimento que esteja na lista tabu caso ele encontre a melhor solução global já vista?"*

* **Por que essa pergunta é excelente:** Lista Tabu e Critério de Aspiração são os dois conceitos centrais de Fred Glover (o criador da Busca Tabu). Se eles implementaram Tabu Search de verdade, saberão responder; se foi superficial, a pergunta mostra rigor técnico da sua equipe.

---

### 📌 Se a equipe usou **Hill Climbing (Subida de Encosta)**:
> *"Vocês utilizaram Hill Climbing como método de busca. Como vocês contornaram o problema crônico do 'Ótimo Local'? A busca de vocês implementou alguma estratégia de 'Random Restart' (reinício aleatório) ou 'Variable Neighborhood Search' para não empacar na primeira colina de custo?"*

* **Por que essa pergunta é excelente:** O professor de Laboratório de Programação adora essa discussão, porque todo Hill Climbing simples é míope e falha em Timetabling.

---

### 📌 Se a equipe usou **Simulated Annealing (SA)** como nós:
> *"Na etapa do Simulated Annealing, qual foi a política adotada para a Temperatura Inicial ($T_0$) e a taxa geométrica de resfriamento ($\alpha$)? Vocês mediram a taxa de aceitação inicial de movimentos de piora para garantir que o algoritmo não congele rápido demais nem fique em passeio aleatório por muito tempo?"*

* **Por que essa pergunta é excelente:** Calibração de temperatura inicial é a decisão mais difícil na engenharia de um Simulated Annealing.

---

### 📌 Pergunta Curinga (Serve para **QUALQUER** equipe — Modelagem de Restrições):
> *"Na função de aptidão (Fitness Function) de vocês, como vocês balancearam o peso das restrições duras (choques) frente às restrições suaves (janelas/preferências)? Vocês usaram pesos fixos dissuasivos, penalidade dinâmica que aumenta com o tempo ou dividiram a resolução em dois estágios independentes?"*

* **Por que essa pergunta é excelente:** É universal, educada, pertinente a qualquer trabalho de Timetabling e toca diretamente no coração da Seção B do trabalho do professor.

---

### 🛡️ Postura Recomendada no Q&A:
1. Comece sempre elogiando a apresentação: *"Parabéns pela apresentação, pessoal. Achei muito interessante a abordagem de vocês..."*
2. Emende a pergunta técnica de forma construtiva: *"...gostaria de tirar uma dúvida sobre como vocês trataram..."*
3. O professor vai registrar imediatamente a participação crítica da equipe de vocês com nota máxima.
