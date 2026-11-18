# Metodologia das 3 Camadas para Apresentações Técnicas e Defesas

> **Regra de Ouro:** NUNCA misturar conteúdo, narrativa e design visual ao mesmo tempo. A criação de qualquer apresentação deve seguir estritamente o funil em 3 camadas independentes.

---

## 🏗️ Camada 1: Roteiro & Narrativa Crua (Texto Puro / Markdown)
* **Objetivo:** Fechar 100% da história, dados, dores e métricas antes de pensar em layout ou slides.
* **O que fazer:**
  1. Definir a Dor / O Problema real (tempo gasto manualmente, gargalos, citações de impacto).
  2. Apresentar os dados de choque (ex: complexidade $10^{350}$, $25^{250}$ combinatória).
  3. Definir a Proposta de Valor e a Solução em passos simples.
  4. Levantar as métricas empíricas (tempo de motor, turmas, zero colisões).
  5. Estruturar o roteiro de fala orador por orador.
* ⚠️ **Regra da Camada 1:** Proibido abrir PowerPoint ou pedir geração de slides para IA nesta fase.

---

## 📐 Camada 2: Wireframe de Informação (Função de Cada Slide)
* **Objetivo:** Definir a anatomia de dados de cada slide sem desenhar layouts complexos.
* **O que fazer:**
  - Definir o formato de cada tela:
    * *Slide de Dor:* 3 caixas de texto com ícones de alerta e 1 destaque matemático.
    * *Slide de Arquitetura:* Diagrama de caixas empilhadas com destaque em memória RAM.
    * *Slide de Resultados:* 3 números grandes no topo + 2 caixas com métricas de validação.
    * *Slide de Conclusão:* Síntese em tópicos + Frase de ouro de engenharia.

---

## 🎨 Camada 3: Design System & Render Visual (Onde a IA atua)
* **Objetivo:** Aplicar a casca visual moderna sobre a estrutura já travada.
* **O que fazer:**
  - Definir o Design System no prompt da IA (Claude / ChatGPT):
    * **Capa:** Fundo escuro com elementos gráficos da grade horária e identidade limpa.
    * **Cards 3D Flutuantes:** Fundo branco/tint suave com cantos arredondados, borda de 1px e sombra externa difusa (*drop shadow* com blur amplo e opacidade de 15–20%).
    * **Breadcrumbs:** Barra superior fixa indicando a seção ativa em destaque vibrante e as inativas em tom suave.
  - Exportar o arquivo PPTX finalizado.
