import os

def create_svg_dsatur():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="960" height="480">
  <defs>
    <style>
      .bg { fill: #0f172a; }
      .box { rx: 8; ry: 8; stroke-width: 2; }
      .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 20px; font-weight: bold; fill: #ffffff; text-anchor: middle; }
      .subtitle { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; fill: #94a3b8; text-anchor: middle; }
      .step-num { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; font-weight: bold; fill: #38bdf8; letter-spacing: 0.1em; }
      .step-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 14px; font-weight: bold; fill: #f8fafc; }
      .step-desc { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11.5px; fill: #cbd5e1; line-height: 1.4; }
      .arrow { stroke: #38bdf8; stroke-width: 2.5; fill: none; stroke-linecap: round; }
      .arrow-head { fill: #38bdf8; }
      .badge-crit { fill: #ef4444; font-size: 10px; font-weight: bold; font-family: sans-serif; }
    </style>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" class="arrow-head" />
    </marker>
  </defs>

  <!-- Fundo Dark -->
  <rect width="960" height="480" class="bg" />

  <!-- Cabeçalho -->
  <text x="480" y="42" class="title">PIPELINE DA HEURÍSTICA CONSTRUTIVA: PRINCÍPIO FAIL-FIRST</text>
  <text x="480" y="65" class="subtitle">Como o DSatur ordena e aloca aulas na memória RAM para garantir zero conflitos rígidos em milissegundos</text>

  <!-- ETAPA 1: Demandas Brutas -->
  <g transform="translate(40, 100)">
    <rect width="180" height="280" fill="#1e293b" stroke="#334155" class="box" />
    <rect x="0" y="0" width="180" height="38" fill="#334155" rx="8" ry="8" />
    <rect x="0" y="26" width="180" height="12" fill="#334155" />
    <text x="14" y="24" class="step-num">PASSO 1</text>
    <text x="75" y="24" class="step-title">Matriz Curricular</text>

    <!-- Itens não ordenados -->
    <rect x="14" y="55" width="152" height="42" fill="#0f172a" stroke="#475569" rx="5" />
    <text x="22" y="73" class="step-desc" font-weight="bold">Turma A • Hist (2h)</text>
    <text x="22" y="88" class="step-desc" fill="#94a3b8">Prof. Carlos (Livre 20h)</text>

    <rect x="14" y="108" width="152" height="42" fill="#450a0a" stroke="#dc2626" rx="5" />
    <text x="22" y="126" class="step-desc" font-weight="bold" fill="#fca5a5">Turma A • Fís (4h)</text>
    <text x="22" y="141" class="step-desc" fill="#f87171">Prof. João (Só 4h livres!)</text>

    <rect x="14" y="161" width="152" height="42" fill="#0f172a" stroke="#475569" rx="5" />
    <text x="22" y="179" class="step-desc" font-weight="bold">Turma B • Mat (5h)</text>
    <text x="22" y="194" class="step-desc" fill="#94a3b8">Prof. Marcos (Livre 15h)</text>

    <text x="90" y="235" font-family="sans-serif" font-size="11" fill="#64748b" text-anchor="middle">Lista desordenada de aulas</text>
    <text x="90" y="252" font-family="sans-serif" font-size="10.5" fill="#ef4444" text-anchor="middle">⚠️ Risco alto de bloqueio!</text>
  </g>

  <!-- Seta 1 -> 2 -->
  <line x1="225" y1="240" x2="265" y2="240" class="arrow" marker-end="url(#arrowhead)" />

  <!-- ETAPA 2: Cálculo de Criticidade -->
  <g transform="translate(275, 100)">
    <rect width="180" height="280" fill="#1e293b" stroke="#3b82f6" class="box" />
    <rect x="0" y="0" width="180" height="38" fill="#1d4ed8" rx="8" ry="8" />
    <rect x="0" y="26" width="180" height="12" fill="#1d4ed8" />
    <text x="14" y="24" class="step-num" fill="#bfdbfe">PASSO 2</text>
    <text x="75" y="24" class="step-title">Grau de Saturação</text>

    <text x="90" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="#38bdf8" text-anchor="middle">Fórmula de Criticidade</text>
    
    <rect x="12" y="78" width="156" height="44" fill="#0f172a" stroke="#1e3a8a" rx="5" />
    <text x="90" y="96" font-family="monospace" font-size="11" fill="#93c5fd" text-anchor="middle">W(r) = α·CH + β·(1-Disp)</text>
    <text x="90" y="112" font-family="sans-serif" font-size="9.5" fill="#60a5fa" text-anchor="middle">Pesa carga e bloqueios</text>

    <text x="14" y="145" class="step-desc" font-weight="bold">Classificação dos Professores:</text>
    
    <rect x="12" y="155" width="156" height="32" fill="#7f1d1d" rx="4" />
    <text x="18" y="175" font-family="sans-serif" font-size="11" fill="#fecaca">1º Prof. João &rarr; Peso: 95/100</text>

    <rect x="12" y="193" width="156" height="32" fill="#0f172a" rx="4" />
    <text x="18" y="213" font-family="sans-serif" font-size="11" fill="#cbd5e1">2º Prof. Marcos &rarr; Peso: 65</text>

    <rect x="12" y="231" width="156" height="32" fill="#0f172a" rx="4" />
    <text x="18" y="251" font-family="sans-serif" font-size="11" fill="#cbd5e1">3º Prof. Carlos &rarr; Peso: 25</text>
  </g>

  <!-- Seta 2 -> 3 -->
  <line x1="460" y1="240" x2="500" y2="240" class="arrow" marker-end="url(#arrowhead)" />

  <!-- ETAPA 3: Fila Ordenada Fail-First -->
  <g transform="translate(510, 100)">
    <rect width="180" height="280" fill="#1e293b" stroke="#f59e0b" class="box" />
    <rect x="0" y="0" width="180" height="38" fill="#b45309" rx="8" ry="8" />
    <rect x="0" y="26" width="180" height="12" fill="#b45309" />
    <text x="14" y="24" class="step-num" fill="#fde68a">PASSO 3</text>
    <text x="75" y="24" class="step-title">Fila "Fail-First"</text>

    <text x="90" y="65" font-family="sans-serif" font-size="11" fill="#fbbf24" text-anchor="middle">Quem tem menos slots</text>
    <text x="90" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">É ALOCADO PRIMEIRO!</text>

    <!-- Fila ordenada com badge -->
    <rect x="14" y="95" width="152" height="46" fill="#78350f" stroke="#f59e0b" rx="5" />
    <text x="22" y="114" class="step-desc" font-weight="bold" fill="#fef3c7">1. Física (João)</text>
    <text x="22" y="130" class="step-desc" fill="#fde68a">Aloca antes que esgote!</text>

    <rect x="14" y="150" width="152" height="42" fill="#0f172a" stroke="#475569" rx="5" />
    <text x="22" y="168" class="step-desc" font-weight="bold">2. Matemática (Marcos)</text>
    <text x="22" y="183" class="step-desc" fill="#94a3b8">Aloca intermediário</text>

    <rect x="14" y="200" width="152" height="42" fill="#0f172a" stroke="#475569" rx="5" />
    <text x="22" y="218" class="step-desc" font-weight="bold">3. História (Carlos)</text>
    <text x="22" y="233" class="step-desc" fill="#94a3b8">Fácil de encaixar no final</text>
  </g>

  <!-- Seta 3 -> 4 -->
  <line x1="695" y1="240" x2="735" y2="240" class="arrow" marker-end="url(#arrowhead)" />

  <!-- ETAPA 4: Preenchimento do Grid em RAM -->
  <g transform="translate(745, 100)">
    <rect width="180" height="280" fill="#1e293b" stroke="#10b981" class="box" />
    <rect x="0" y="0" width="180" height="38" fill="#047857" rx="8" ry="8" />
    <rect x="0" y="26" width="180" height="12" fill="#047857" />
    <text x="14" y="24" class="step-num" fill="#a7f3d0">PASSO 4</text>
    <text x="75" y="24" class="step-title">Grid em Memória</text>

    <!-- Mini Grid semanal 5x3 -->
    <text x="90" y="65" font-family="sans-serif" font-size="11" font-weight="bold" fill="#34d399" text-anchor="middle">Matriz RAM: GridState</text>
    
    <g transform="translate(20, 78)">
      <!-- Cabeçalho Seg Ter Qua Qui Sex -->
      <text x="8" y="10" font-family="sans-serif" font-size="9" fill="#94a3b8">S</text>
      <text x="36" y="10" font-family="sans-serif" font-size="9" fill="#94a3b8">T</text>
      <text x="64" y="10" font-family="sans-serif" font-size="9" fill="#94a3b8">Q</text>
      <text x="92" y="10" font-family="sans-serif" font-size="9" fill="#94a3b8">Q</text>
      <text x="120" y="10" font-family="sans-serif" font-size="9" fill="#94a3b8">S</text>

      <!-- Linha 1 -->
      <rect x="0" y="16" width="24" height="20" fill="#dc2626" rx="3" /><text x="4" y="30" font-size="8" fill="#fff" font-weight="bold">FÍS</text>
      <rect x="28" y="16" width="24" height="20" fill="#dc2626" rx="3" /><text x="32" y="30" font-size="8" fill="#fff" font-weight="bold">FÍS</text>
      <rect x="56" y="16" width="24" height="20" fill="#2563eb" rx="3" /><text x="60" y="30" font-size="8" fill="#fff">MAT</text>
      <rect x="84" y="16" width="24" height="20" fill="#2563eb" rx="3" /><text x="88" y="30" font-size="8" fill="#fff">MAT</text>
      <rect x="112" y="16" width="24" height="20" fill="#16a34a" rx="3" /><text x="116" y="30" font-size="8" fill="#fff">HIS</text>

      <!-- Linha 2 -->
      <rect x="0" y="40" width="24" height="20" fill="#475569" rx="3" />
      <rect x="28" y="40" width="24" height="20" fill="#475569" rx="3" />
      <rect x="56" y="40" width="24" height="20" fill="#2563eb" rx="3" /><text x="60" y="54" font-size="8" fill="#fff">MAT</text>
      <rect x="84" y="40" width="24" height="20" fill="#16a34a" rx="3" /><text x="88" y="54" font-size="8" fill="#fff">HIS</text>
      <rect x="112" y="40" width="24" height="20" fill="#475569" rx="3" />
    </g>

    <rect x="12" y="160" width="156" height="52" fill="#064e3b" stroke="#10b981" rx="5" />
    <text x="90" y="180" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#a7f3d0" text-anchor="middle">✓ ZERO CHOQUES</text>
    <text x="90" y="196" font-family="sans-serif" font-size="10" fill="#d1fae5" text-anchor="middle">Execução em &lt; 100 ms!</text>

    <text x="90" y="240" font-family="sans-serif" font-size="10.5" fill="#34d399" font-weight="bold" text-anchor="middle">Entrega o "Warm Start"</text>
    <text x="90" y="255" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Semente pronta p/ Fase 2</text>
  </g>

  <!-- Rodapé Explicativo -->
  <text x="480" y="420" font-family="sans-serif" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">
    Moral da História: "Alocar quem tem menos opções no início evita o beco sem saída no final."
  </text>
  <text x="480" y="442" font-family="sans-serif" font-size="11.5" fill="#94a3b8" text-anchor="middle">
    Complexidade O(N log N) da ordenação garante agilidade instantânea antes da metaheurística estocástica.
  </text>
</svg>'''
    with open(r"docs\apresentacoes\diagrama-dsatur-fluxo.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("diagrama-dsatur-fluxo.svg criado com sucesso!")

def create_svg_simulated_annealing():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="960" height="480">
  <defs>
    <style>
      .bg { fill: #0f172a; }
      .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 20px; font-weight: bold; fill: #ffffff; text-anchor: middle; }
      .subtitle { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; fill: #94a3b8; text-anchor: middle; }
      .axis-label { font-family: sans-serif; font-size: 12px; font-weight: bold; fill: #94a3b8; }
      .curve { fill: none; stroke: #38bdf8; stroke-width: 3.5; stroke-linecap: round; }
      .hill-climb-arrow { stroke: #ef4444; stroke-width: 3; stroke-dasharray: 6,4; fill: none; }
      .sa-jump-arrow { stroke: #10b981; stroke-width: 3.5; fill: none; }
      .card-box { rx: 8; ry: 8; }
    </style>
    <marker id="arrow-red" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#ef4444" />
    </marker>
    <marker id="arrow-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#10b981" />
    </marker>
  </defs>

  <!-- Fundo Dark -->
  <rect width="960" height="480" class="bg" />

  <!-- Cabeçalho -->
  <text x="480" y="42" class="title">SIMULATED ANNEALING: COMO ESCAPAR DO ÓTIMO LOCAL</text>
  <text x="480" y="65" class="subtitle">O Critério de Metropolis permite aceitar pioras temporárias (+Δf) para saltar barreiras de energia</text>

  <!-- Painel Esquerdo: O Gráfico da Curva de Energia (Landscape) -->
  <g transform="translate(60, 100)">
    <!-- Eixos -->
    <line x1="40" y1="280" x2="480" y2="280" stroke="#475569" stroke-width="2" />
    <line x1="40" y1="40" x2="40" y2="280" stroke="#475569" stroke-width="2" />
    
    <text x="260" y="305" class="axis-label" text-anchor="middle">Espaço de Configurações de Horários</text>
    <text x="15" y="30" class="axis-label">Custo f(S) (Penalidade de Janelas)</text>

    <!-- Curva de Energia (Landscape com 1 Ótimo Local raso e 1 Ótimo Global fundo) -->
    <!-- Pontos: (40, 100) -> descida até (150, 190) [Ótimo Local] -> sobe até (260, 120) [Barreira] -> desce até (390, 250) [Ótimo Global] -> sobe até (470, 130) -->
    <path d="M 50,110 C 90,120 120,200 160,200 C 200,200 220,115 270,115 C 320,115 340,260 400,260 C 440,260 455,170 470,140" class="curve" />

    <!-- Ponto A: Ótimo Local -->
    <circle cx="160" cy="200" r="7" fill="#ef4444" stroke="#ffffff" stroke-width="2" />
    <rect x="90" y="215" width="140" height="42" fill="#1e293b" stroke="#ef4444" rx="4" />
    <text x="160" y="232" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fca5a5" text-anchor="middle">ÓTIMO LOCAL</text>
    <text x="160" y="247" font-family="sans-serif" font-size="10" fill="#cbd5e1" text-anchor="middle">Grade com 2 janelas vagas</text>

    <!-- Hill Climbing preso -->
    <path d="M 120,150 L 150,190" class="hill-climb-arrow" marker-end="url(#arrow-red)" />
    <rect x="50" y="130" width="85" height="24" fill="#7f1d1d" rx="4" />
    <text x="92" y="146" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fecaca" text-anchor="middle">Hill Climbing Trava!</text>

    <!-- Barreira de Custo +Δf -->
    <circle cx="270" cy="115" r="5" fill="#f59e0b" />
    <text x="270" y="98" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fbbf24" text-anchor="middle">Barreira (+Δf)</text>
    <text x="270" y="112" font-family="sans-serif" font-size="9.5" fill="#94a3b8" text-anchor="middle">Piora temporária</text>

    <!-- Ponto B: Ótimo Global -->
    <circle cx="400" cy="260" r="8" fill="#10b981" stroke="#ffffff" stroke-width="2" />
    <rect x="330" y="195" width="140" height="42" fill="#1e293b" stroke="#10b981" rx="4" />
    <text x="400" y="212" font-family="sans-serif" font-size="11" font-weight="bold" fill="#86efac" text-anchor="middle">ÓTIMO GLOBAL</text>
    <text x="400" y="227" font-family="sans-serif" font-size="10" fill="#a7f3d0" text-anchor="middle">Grade perfeita (0 Janelas!)</text>

    <!-- Salto do Simulated Annealing -->
    <path d="M 165,190 C 200,60 300,60 390,245" class="sa-jump-arrow" marker-end="url(#arrow-green)" />
    <rect x="225" y="45" width="170" height="30" fill="#064e3b" stroke="#10b981" rx="5" />
    <text x="310" y="65" font-family="sans-serif" font-size="11" font-weight="bold" fill="#a7f3d0" text-anchor="middle">Salto do Simulated Annealing</text>
  </g>

  <!-- Painel Direito: A Matemática Explicada de Forma Simples -->
  <g transform="translate(580, 105)">
    <!-- Card 1: O Segredo de Metropolis -->
    <rect width="330" height="150" fill="#1e293b" stroke="#3b82f6" class="card-box" stroke-width="1.5" />
    <rect x="0" y="0" width="330" height="32" fill="#1e3a8a" rx="8" ry="8" />
    <rect x="0" y="20" width="330" height="12" fill="#1e3a8a" />
    <text x="165" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#bfdbfe" text-anchor="middle">O CRITÉRIO DE METROPOLIS (1953)</text>
    
    <rect x="20" y="42" width="290" height="36" fill="#0f172a" stroke="#334155" rx="5" />
    <text x="165" y="65" font-family="monospace" font-size="14" font-weight="bold" fill="#38bdf8" text-anchor="middle">P(aceitar piora) = e^(-Δf / T)</text>

    <text x="20" y="98" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Se a troca for melhor (Δf &lt; 0): <strong>Aceita 100%</strong>.</text>
    <text x="20" y="116" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Se a troca for pior (Δf &gt; 0): <strong>Calcula a chance P</strong>.</text>
    <text x="20" y="134" font-family="sans-serif" font-size="10.5" fill="#94a3b8">  Permite dar "1 passo atrás para dar 2 à frente"!</text>

    <!-- Card 2: O Papel da Temperatura -->
    <rect y="165" width="330" height="135" fill="#1e293b" stroke="#f59e0b" class="card-box" stroke-width="1.5" />
    <rect y="165" width="330" height="32" fill="#b45309" rx="8" ry="8" />
    <rect y="185" width="330" height="12" fill="#b45309" />
    <text x="165" y="187" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fef3c7" text-anchor="middle">O RESFRIAMENTO DA TEMPERATURA (T)</text>

    <text x="20" y="218" font-family="sans-serif" font-size="11" fill="#fde68a">🔥 <strong>Início (T Alto):</strong> Muita energia.</text>
    <text x="20" y="233" font-family="sans-serif" font-size="10.5" fill="#cbd5e1">Explora o espaço e salta morros com facilidade.</text>

    <text x="20" y="258" font-family="sans-serif" font-size="11" fill="#93c5fd">❄️ <strong>Fim (T Baixo):</strong> Resfriamento gradual.</text>
    <text x="20" y="273" font-family="sans-serif" font-size="10.5" fill="#cbd5e1">Só aceita melhorias até convergir no Ótimo Global.</text>
  </g>

  <!-- Rodapé -->
  <text x="480" y="435" font-family="sans-serif" font-size="13" font-weight="bold" fill="#10b981" text-anchor="middle">
    Por que é perfeito para o Timetabling?
  </text>
  <text x="480" y="455" font-family="sans-serif" font-size="11.5" fill="#94a3b8" text-anchor="middle">
    Porque desatar janelas vagas exige desmanchar temporariamente blocos de aulas para reorganizá-los em seguida.
  </text>
</svg>'''
    with open(r"docs\apresentacoes\diagrama-simulated-annealing-landscape.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("diagrama-simulated-annealing-landscape.svg criado com sucesso!")

def create_svg_swap_move():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="960" height="480">
  <defs>
    <style>
      .bg { fill: #0f172a; }
      .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 20px; font-weight: bold; fill: #ffffff; text-anchor: middle; }
      .subtitle { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; fill: #94a3b8; text-anchor: middle; }
      .slot-box { rx: 6; ry: 6; stroke-width: 1.5; }
      .arrow { stroke: #38bdf8; stroke-width: 3; fill: none; }
      .arrow-curve { stroke: #f59e0b; stroke-width: 3; stroke-dasharray: 6,4; fill: none; }
    </style>
    <marker id="arrow-blue" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#38bdf8" />
    </marker>
    <marker id="arrow-amber" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#f59e0b" />
    </marker>
  </defs>

  <rect width="960" height="480" class="bg" />

  <text x="480" y="42" class="title">OPERADOR DE PERTURBAÇÃO: SWAP MOVE INTRA-TURMA</text>
  <text x="480" y="65" class="subtitle">Como a troca controlada de horários elimina janelas docentes preservando 100% da carga horária</text>

  <!-- CENÁRIO ANTES: COM JANELA VAGA -->
  <g transform="translate(60, 100)">
    <rect width="380" height="280" fill="#1e293b" stroke="#ef4444" rx="8" stroke-width="2" />
    <rect x="0" y="0" width="380" height="38" fill="#7f1d1d" rx="8" />
    <rect x="0" y="26" width="380" height="12" fill="#7f1d1d" />
    <text x="190" y="24" font-family="sans-serif" font-size="14" font-weight="bold" fill="#fecaca" text-anchor="middle">ESTADO ATUAL (Solução com Janela Ociosa)</text>

    <text x="25" y="65" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8">Grade de Terça-feira (Turma 6º Período):</text>

    <!-- Slots de Terça -->
    <rect x="25" y="80" width="60" height="75" fill="#1e3a8a" stroke="#3b82f6" class="slot-box" />
    <text x="55" y="100" font-family="sans-serif" font-size="10" fill="#93c5fd" text-anchor="middle">Slot 1</text>
    <text x="55" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">FÍSICA</text>
    <text x="55" y="140" font-family="sans-serif" font-size="9" fill="#bfdbfe" text-anchor="middle">Prof. João</text>

    <!-- Slot 2: JANELA! -->
    <rect x="95" y="80" width="60" height="75" fill="#450a0a" stroke="#dc2626" class="slot-box" stroke-dasharray="4,2" />
    <text x="125" y="100" font-family="sans-serif" font-size="10" fill="#fca5a5" text-anchor="middle">Slot 2</text>
    <text x="125" y="122" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#f87171" text-anchor="middle">VAGO</text>
    <text x="125" y="140" font-family="sans-serif" font-size="8.5" fill="#fca5a5" text-anchor="middle">JANELA!</text>

    <!-- Slot 3 -->
    <rect x="165" y="80" width="60" height="75" fill="#1e3a8a" stroke="#3b82f6" class="slot-box" />
    <text x="195" y="100" font-family="sans-serif" font-size="10" fill="#93c5fd" text-anchor="middle">Slot 3</text>
    <text x="195" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">FÍSICA</text>
    <text x="195" y="140" font-family="sans-serif" font-size="9" fill="#bfdbfe" text-anchor="middle">Prof. João</text>

    <!-- Slot 4: MATEMÁTICA -->
    <rect x="235" y="80" width="60" height="75" fill="#064e3b" stroke="#10b981" class="slot-box" />
    <text x="265" y="100" font-family="sans-serif" font-size="10" fill="#a7f3d0" text-anchor="middle">Slot 4</text>
    <text x="265" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">MAT</text>
    <text x="265" y="140" font-family="sans-serif" font-size="9" fill="#a7f3d0" text-anchor="middle">Prof. Marcos</text>

    <!-- Slot 5: VAGO -->
    <rect x="305" y="80" width="50" height="75" fill="#0f172a" stroke="#475569" class="slot-box" />
    <text x="330" y="122" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Livre</text>

    <!-- Diagnóstico da Situação -->
    <rect x="25" y="175" width="330" height="85" fill="#0f172a" stroke="#7f1d1d" rx="6" />
    <text x="35" y="198" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#fca5a5">⚠️ O que está acontecendo aqui?</text>
    <text x="35" y="218" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Prof. João dá aula no Slot 1 e Slot 3.</text>
    <text x="35" y="235" font-family="sans-serif" font-size="11" fill="#f87171">• Slot 2 ocioso = 1 HORA VAGA perdida na escola!</text>
    <text x="35" y="252" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fca5a5">• Penalidade Soft incorrida: +85 pontos de custo.</text>
  </g>

  <!-- Seta Central de Mutação / Swap -->
  <g transform="translate(455, 210)">
    <circle cx="25" cy="25" r="24" fill="#1e293b" stroke="#f59e0b" stroke-width="2" />
    <text x="25" y="22" font-family="sans-serif" font-size="10" font-weight="bold" fill="#f59e0b" text-anchor="middle">SWAP</text>
    <text x="25" y="34" font-family="sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">MOVE</text>
    <path d="M 5,50 C 25,65 25,65 45,50" class="arrow" marker-end="url(#arrow-blue)" />
  </g>

  <!-- CENÁRIO DEPOIS: OTIMIZADO E COMPACTADO -->
  <g transform="translate(520, 100)">
    <rect width="380" height="280" fill="#1e293b" stroke="#10b981" rx="8" stroke-width="2" />
    <rect x="0" y="0" width="380" height="38" fill="#065f46" rx="8" />
    <rect x="0" y="26" width="380" height="12" fill="#065f46" />
    <text x="190" y="24" font-family="sans-serif" font-size="14" font-weight="bold" fill="#a7f3d0" text-anchor="middle">NOVO ESTADO (Após o Swap Move)</text>

    <text x="25" y="65" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8">Grade Reorganizada (Mesma Turma):</text>

    <!-- Slots Otimizados -->
    <rect x="25" y="80" width="60" height="75" fill="#1e3a8a" stroke="#3b82f6" class="slot-box" />
    <text x="55" y="100" font-family="sans-serif" font-size="10" fill="#93c5fd" text-anchor="middle">Slot 1</text>
    <text x="55" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">FÍSICA</text>
    <text x="55" y="140" font-family="sans-serif" font-size="9" fill="#bfdbfe" text-anchor="middle">Prof. João</text>

    <!-- Slot 2: FÍSICA GEMINADA! -->
    <rect x="95" y="80" width="60" height="75" fill="#1e3a8a" stroke="#38bdf8" class="slot-box" stroke-width="2.5" />
    <text x="125" y="100" font-family="sans-serif" font-size="10" fill="#bae6fd" text-anchor="middle">Slot 2</text>
    <text x="125" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">FÍSICA</text>
    <text x="125" y="140" font-family="sans-serif" font-size="9" fill="#bae6fd" text-anchor="middle">Prof. João</text>

    <!-- Slot 3: MATEMÁTICA ANTECIPADA -->
    <rect x="165" y="80" width="60" height="75" fill="#064e3b" stroke="#10b981" class="slot-box" />
    <text x="195" y="100" font-family="sans-serif" font-size="10" fill="#a7f3d0" text-anchor="middle">Slot 3</text>
    <text x="195" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">MAT</text>
    <text x="195" y="140" font-family="sans-serif" font-size="9" fill="#a7f3d0" text-anchor="middle">Prof. Marcos</text>

    <!-- Slot 4: LIVRE -->
    <rect x="235" y="80" width="60" height="75" fill="#0f172a" stroke="#475569" class="slot-box" />
    <text x="265" y="122" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Livre</text>

    <!-- Slot 5: LIVRE -->
    <rect x="305" y="80" width="50" height="75" fill="#0f172a" stroke="#475569" class="slot-box" />
    <text x="330" y="122" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Livre</text>

    <!-- Validação de Sucesso -->
    <rect x="25" y="175" width="330" height="85" fill="#064e3b" stroke="#10b981" rx="6" />
    <text x="35" y="198" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#a7f3d0">✓ Resultado da Perturbação:</text>
    <text x="35" y="218" font-family="sans-serif" font-size="11" fill="#ecfdf5">• Aulas de Física ficaram consecutivas (geminadas).</text>
    <text x="35" y="235" font-family="sans-serif" font-size="11" fill="#ecfdf5">• JANELA ELIMINADA! Prof. João sai mais cedo.</text>
    <text x="35" y="252" font-family="sans-serif" font-size="11" font-weight="bold" fill="#34d399">• Custo Reduzido: Δf = -85 pontos (Melhoria direta!).</text>
  </g>

  <!-- Rodapé com a Regra de Ouro -->
  <text x="480" y="420" font-family="sans-serif" font-size="13" font-weight="bold" fill="#f59e0b" text-anchor="middle">
    Blindagem de Restrições Fortes: "A troca SÓ é aceita se o professor estiver livre no novo slot."
  </text>
  <text x="480" y="442" font-family="sans-serif" font-size="11.5" fill="#94a3b8" text-anchor="middle">
    Se a troca causar choque de professor com outra turma, o movimento é abortado imediatamente (P = 0).
  </text>
</svg>'''
    with open(r"docs\apresentacoes\diagrama-swap-move.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("diagrama-swap-move.svg criado com sucesso!")

if __name__ == "__main__":
    create_svg_dsatur()
    create_svg_simulated_annealing()
    create_svg_swap_move()
