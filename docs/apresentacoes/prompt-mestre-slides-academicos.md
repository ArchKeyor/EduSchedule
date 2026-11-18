# 🎓 Prompt Mestre — Gerador de Slides Acadêmicos de TCC (Padrão Engenharia & Computação)

> **Propósito:** Este prompt instrui qualquer IA avançada (ChatGPT, Claude ou Gemini) a conceber ou gerar programaticamente (via `python-pptx`) uma apresentação completa de TCC com **15 slides no mais rigoroso padrão acadêmico e visual**, fugindo de "slides de startup" e aplicando a arquitetura lógica exigida por bancas de graduação e pós-graduação.

---

## 📋 Como Usar:
1. Copie o bloco de código abaixo;
2. Preencha as seções entre colchetes (`[...]`) com os dados do seu projeto;
3. Envie para o ChatGPT (GPT-4o) ou Claude. Se quiser o arquivo `.pptx` pronto, peça para a IA executar o script via `python-pptx`!

---

```text
Você é um designer sênior de apresentações acadêmicas e professor orientador de bancas de TCC de Engenharia de Software e Ciência da Computação.

Preciso que você crie a ESTRUTURA VISUAL E DE CONTEÚDO COMPLETA de uma apresentação de TCC de 15 slides (proporção 16:9), rigorosamente formatada nos padrões acadêmicos de bancas avaliadoras.

====================================================================
DADOS DE ENTRADA DO PROJETO:
- Título do Trabalho: [Insira o Título Acadêmico do Projeto]
- Subtítulo Técnico/Metodológico: [Ex: Uma Abordagem Heurística sob o Modelo CB-CTT]
- Autores: [Nome dos Autores e e-mails institucionais]
- Orientador: [Prof. Me. / Prof. Dr. Nome do Orientador]
- Instituição e Curso: [Nome da Faculdade / Universidade — Curso de Engenharia de Software]
- Cidade e Ano: [Ex: Volta Redonda - RJ, 2026]
- O Problema Real: [Descreva em 2 parágrafos a dor operacional e o gargalo manual do problema]
- A Barreira Teórica/Matemática: [Ex: Complexidade NP-Completo / NP-Hard, explosão combinatória O(S^A)]
- A Relevância Social/Humana: [Ex: Citação de autor da área — ergonomia, saúde mental, burnout docente]
- A Solução de Engenharia Proposta: [Ex: Clean Architecture, API REST, motor em memória RAM, heurística construtiva]
- Resultados Empíricos Obtidos: [Ex: Massa real de teste com X turmas e Y professores; tempo obtido vs alvo; zero conflitos]
- Tecnologias do Projeto: [Ex: Python, React, TypeScript, Django REST, PostgreSQL 16, Docker, Nuvem Azure]
====================================================================

DIRETRIZES DE DESIGN SYSTEM ACADÊMICO (PADRÃO BANCA DE ALTO NÍVEL):
1. Proporção: 16:9 Widescreen;
2. Paleta de Cores Institucional: Fundo off-white/branco limpo; caixas modulares em Azul Marinho/Escuro; faixas e destaques centrais em Vermelho Carmim; tipografia sem serifa limpa (Inter, Roboto ou Arial);
3. Zero "Paredes de Texto": Proibido parágrafos longos. Utilize exclusivamente cards modulares, tabelas comparativas, diagramas de caixas conectadas e equações matemáticas;
4. Rigor Conceitual: Toda afirmação deve ter lastro em autores canônicos com ano e taxonomia formal (ex: Decisão vs Otimização, Hard vs Soft Constraints).

====================================================================
ESTRUTURA CANÔNICA DOS 15 SLIDES (ARQUITETURA ACADÊMICA):
====================================================================

[Slide 1/15] Capa Institucional Formal
- Fundo com padrão sutil temático (ex: malha de grafos ou grid de dados);
- Faixa central de alto contraste com Título em caixa alta e Subtítulo técnico;
- Identificação completa: Autores, titulação formal do Orientador, Instituição, Curso, Local e Ano.

[Slide 2/15] Agenda da Apresentação
- Diagrama em 4 quadrantes conectados situando a banca no tempo:
  1. Introdução (Problema, Relevância Social e Objetivos);
  2. Fundamentação Teórica (Modelos, Complexidade e Heurísticas);
  3. Desenvolvimento (Arquitetura, Modelagem de Dados e Algoritmos em RAM);
  4. Conclusão & Demonstração Prática ao Vivo na Nuvem.

[Slide 3/15] Introdução — Cenário Operacional & Complexidade do Domínio
- Diagrama modular de fatores críticos (o processo manual tradicional: lentidão, choques, custo de gestão);
- Card conceitual do modelo de domínio formal adotado pelo trabalho.

[Slide 4/15] Introdução — A Barreira Matemática & Relevância Social
- Lado Esquerdo: Tabela comparativa de complexidade (Força Bruta exponencial vs Métodos Exatos/MILP vs Heurística Proposta);
- Lado Direito: Box de Relevância Social amparado em literatura seminal (o impacto humano e ergonômico da ineficiência do sistema).

[Slide 5/15] Problemática vs Objetivo Geral
- Slide de contraste visual direto (Declaração de Missão):
  • Caixa Superior: Problemática (a dor operacional a ser eliminada);
  • Caixa Inferior: Objetivo Geral com as métricas-alvo (arquitetura proposta, tempo de resposta sub-segundo e tolerância zero a falhas críticas).

[Slide 6/15] Fundamentação Teórica I — O Modelo & Teoria da Computação
- Card Superior: Definição das entidades do modelo canônico;
- Dois Cards Comparativos Lado a Lado (A Dualidade Teórica):
  • Card 1: Restrições Rígidas (Hard Constraints) ➔ Problema de Decisão ➔ NP-Completo (autores e ano);
  • Card 2: Restrições Flexíveis (Soft Constraints) ➔ Problema de Otimização ➔ NP-Hard (autores e ano).

[Slide 7/15] Fundamentação Teórica II — Heurística Construtiva & Princípio Fail-First
- Card 1: O princípio algorítmico abstrato (metáfora das 'pedras grandes no balde' e saturação de grafos);
- Card 2: A adaptação do princípio para o problema prático através de critérios de criticidade;
- Rodapé: Complexidade assintótica do algoritmo (ex: O(N log N)).

[Slide 8/15] Fundamentação Teórica III — Resolução em Dois Estágios (Pipeline)
- Diagrama de fluxo horizontal de resolução em 2 passos:
  • Passo 1 (Entrega Atual da 1ª Fatia): Heurística Construtiva na RAM entregando viabilidade física (Warm Start) em milissegundos;
  • Seta de Conexão: A grade viável serve de semente aceleradora;
  • Passo 2 (Trabalhos Futuros): Busca Local para polimento das restrições flexíveis;
- Frase de conclusão com lastro em autor seminal sobre a superioridade do Warm Start.

[Slide 9/15] Desenvolvimento I — Arquitetura de Software em Camadas Desacopladas
- Diagrama arquitetural de 3 camadas conectadas (Frontend SPA, Backend API REST e Solver isolado em memória RAM);
- Destaque das Decisões de Arquitetura (ADR) e Clean Architecture;
- O diferencial de performance: segregação total de I/O de banco de dados durante o loop combinatorial.

[Slide 10/15] Desenvolvimento II — Modelagem Semântica de Dados
- Diagrama de Entidades demonstrando a separação estrita entre Demanda (Intenção) e Alocação (Resultado);
- Benefício prático: Versionamento de cenários alternativos sem duplicação de cadastros;
- Apresentação formal da Massa de Testes Homologada utilizada na validação.

[Slide 11/15] Desenvolvimento III — Estrutura em Memória RAM & Acesso O(1)
- Representação gráfica das matrizes ou estruturas internas em memória primária;
- Demonstração matemática de como a verificação de conflitos ocorre em tempo constante O(1) através de acesso indexado direto por hardware, sem laços de repetição ou queries de banco.

[Slide 12/15] Análise de Resultados — Benchmark Operacional da Fatia Vertical
- Card Superior de Destaque: O Cenário Experimental Homologado (dimensões exatas da amostra testada);
- Tabela de Métricas Experimentais: Métrica Avaliada | Alvo Estabelecido | Resultado Obtido | Status;
- Box de Conclusões Empíricas com foco em rigor científico (sem exageros publicitários).

[Slide 13/15] Conclusão & Trabalhos Futuros
- Matriz em 4 quadrantes sintetizando:
  1. Viabilidade prática comprovada na primeira fatia;
  2. Escalabilidade e manutenibilidade da arquitetura desacoplada;
  3. Próxima etapa (refinamento ergonômico via busca local);
  4. Extensibilidade para integração de bibliotecas externas via padrão Strategy.

[Slide 14/15] Referências Bibliográficas
- Duas colunas limpas contendo os artigos seminais, livros de arquitetura e periódicos canônicos citados ao longo da apresentação, estritamente no padrão ABNT.

[Slide 15/15] Encerramento & Transição para a Demonstração na Nuvem
- Agradecimento formal ("OBRIGADO");
- Dados de produção (Nuvem, Stack tecnológica e repositório com QR Code);
- Chamada formal para a banca: convite para a demonstração prática ao vivo do sistema em produção.

====================================================================
FORMATO DE SAÍDA EXIGIDO:
- Apresente o conteúdo detalhado de cada um dos 15 slides, especificando títulos, subtítulos, textos exatos de cada card e tabela;
- Se solicitado, gere o código completo em Python utilizando a biblioteca `python-pptx` para compilar diretamente o arquivo `.pptx` pronto para download.
```
