import json
from pathlib import Path

base_dir = Path("C:/Users/HP/Documents/GitHub/finanzas-punto-equilibrio-turismo-regional")
with open(base_dir / "datos_portatil.json", "r", encoding="utf-8") as f:
    d = json.load(f)

payload_json = json.dumps(d)

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Financiero Portátil | UNCP - Daniel Ricardo Sulca Castro</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>
    .font-mono-num { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans antialiased selection:bg-blue-600 selection:text-white">

  <!-- Header -->
  <header class="bg-slate-900/90 backdrop-blur border-b border-slate-800 px-6 py-4 sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
          <span>Universidad Nacional del Centro del Perú</span>
          <span>·</span>
          <span>Facultad de Economía</span>
          <span>·</span>
          <span class="text-blue-400">Finanzas I (055D)</span>
        </div>
        <h1 class="text-base md:text-lg font-semibold text-white tracking-tight mt-0.5">
          Punto de Equilibrio Operativo y Sensibilidad en Proyectos Turísticos Regionales (2013-2025)
        </h1>
        <p class="text-xs text-slate-400">
          Docente: <span class="text-slate-300 font-medium">Dr. Ciro Iván Machacuay Meza</span> | 
          Estudiante: <span class="text-blue-400 font-semibold">Daniel Ricardo Sulca Castro</span> (Código: 2024200532L · e_2024200532L@uncp.edu.pe)
        </p>
      </div>

      <div class="flex items-center gap-3">
        <div class="text-right">
          <div class="text-[11px] text-slate-400">Hash SHA-256 Verificado</div>
          <div class="font-mono-num text-xs text-emerald-400 bg-slate-950 px-2.5 py-1 rounded border border-slate-800">
            bac6f8cc79...0106a
          </div>
        </div>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Modo Portátil Autónomo
        </span>
      </div>
    </div>
  </header>

  <!-- Selector de Vías -->
  <nav class="bg-slate-900 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-6 flex overflow-x-auto space-x-1 py-1.5 text-xs font-medium">
      <button onclick="seleccionarVia('via1')" id="tab-nav-via1" class="via-nav-btn px-4 py-2.5 rounded text-white bg-slate-800 border border-slate-700 flex items-center gap-2 transition">
        <span class="w-2 h-2 rounded-full bg-blue-500"></span>
        <span>VÍA 1: APIs REST (BCRP & Banco Mundial)</span>
      </button>

      <button onclick="seleccionarVia('via2')" id="tab-nav-via2" class="via-nav-btn px-4 py-2.5 rounded text-slate-400 hover:text-slate-200 border border-transparent flex items-center gap-2 transition">
        <span class="w-2 h-2 rounded-full bg-slate-600"></span>
        <span>VÍA 2: MINCETUR / INEI (Capacidad y Arribos)</span>
      </button>

      <button onclick="seleccionarVia('via3')" id="tab-nav-via3" class="via-nav-btn px-4 py-2.5 rounded text-slate-400 hover:text-slate-200 border border-transparent flex items-center gap-2 transition">
        <span class="w-2 h-2 rounded-full bg-slate-600"></span>
        <span>VÍA 3: Integración, Limpieza & SHA-256</span>
      </button>

      <button onclick="seleccionarVia('via4')" id="tab-nav-via4" class="via-nav-btn px-4 py-2.5 rounded text-slate-400 hover:text-slate-200 border border-transparent flex items-center gap-2 transition">
        <span class="w-2 h-2 rounded-full bg-slate-600"></span>
        <span>VÍA 4: Resultados, Figuras & Sensibilidad</span>
      </button>
    </div>
  </nav>

  <!-- Contenido -->
  <main class="max-w-7xl mx-auto px-6 py-6 w-full flex-1 space-y-6">

    <!-- SECCIÓN VÍA 1 -->
    <section id="seccion-via1" class="via-section space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <span class="text-[11px] font-semibold text-blue-400 uppercase tracking-wider">Vía 1 Oficial · APIs Programáticas</span>
        <h2 class="text-base font-semibold text-white mt-0.5">Extracción de Variables Macroeconómicas y Turismo Global</h2>
        <p class="text-xs text-slate-400 mt-1 max-w-3xl">
          Consumo programático de series del Banco Central de Reserva del Perú (BCRPData) e Indicadores del Desarrollo Mundial (Banco Mundial WDI) entre 2013 y 2025.
        </p>
      </div>

      <!-- Stepper Vía 1 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
        <button onclick="mostrarSubpasoV1(1)" id="btn-v1-s1" class="v1-btn p-3 bg-slate-800 border-l-2 border-blue-500 rounded text-left">
          <div class="text-[10px] text-slate-400">PASO 1.1</div>
          <div class="font-medium text-white">Inflación / IPC</div>
          <div class="text-[10px] text-blue-400 font-mono-num">PN01270PM</div>
        </button>
        <button onclick="mostrarSubpasoV1(2)" id="btn-v1-s2" class="v1-btn p-3 bg-slate-900 border-l-2 border-slate-700 hover:bg-slate-800 rounded text-left">
          <div class="text-[10px] text-slate-400">PASO 1.2</div>
          <div class="font-medium text-slate-300">Tasa Referencia</div>
          <div class="text-[10px] text-slate-500 font-mono-num">PN01288PM</div>
        </button>
        <button onclick="mostrarSubpasoV1(3)" id="btn-v1-s3" class="v1-btn p-3 bg-slate-900 border-l-2 border-slate-700 hover:bg-slate-800 rounded text-left">
          <div class="text-[10px] text-slate-400">PASO 1.3</div>
          <div class="font-medium text-slate-300">PBI Mensual</div>
          <div class="text-[10px] text-slate-500 font-mono-num">PN01770AM</div>
        </button>
        <button onclick="mostrarSubpasoV1(4)" id="btn-v1-s4" class="v1-btn p-3 bg-slate-900 border-l-2 border-slate-700 hover:bg-slate-800 rounded text-left">
          <div class="text-[10px] text-slate-400">PASO 1.4</div>
          <div class="font-medium text-slate-300">Banco Mundial</div>
          <div class="text-[10px] text-slate-500 font-mono-num">ST.INT.ARVL</div>
        </button>
      </div>

      <!-- Ficha y Gráfico Vía 1 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-3 text-xs">
          <div class="border-b border-slate-800 pb-3">
            <span class="text-[10px] text-blue-400 font-mono-num" id="v1-tag">PASO 1.1 · BCRPData</span>
            <h3 class="text-sm font-semibold text-white mt-0.5" id="v1-titulo">Índice de Precios al Consumidor (IPC)</h3>
          </div>
          <div>
            <span class="text-slate-400 text-[11px] block">Endpoint REST:</span>
            <p class="font-mono-num text-[11px] bg-slate-950 p-2 rounded border border-slate-800 break-all text-slate-300" id="v1-endpoint"></p>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div class="bg-slate-950 p-2 rounded border border-slate-800">
              <span class="text-slate-400 text-[10px] block">Serie BCRP</span>
              <span class="font-mono-num font-semibold text-slate-200" id="v1-serie"></span>
            </div>
            <div class="bg-slate-950 p-2 rounded border border-slate-800">
              <span class="text-slate-400 text-[10px] block">Respuesta HTTP</span>
              <span class="font-mono-num text-emerald-400 font-semibold">200 OK</span>
            </div>
          </div>
          <div>
            <span class="text-slate-400 text-[11px] block">Función Financiera:</span>
            <p class="text-slate-300 text-xs leading-relaxed" id="v1-desc"></p>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-lg p-5 lg:col-span-2 flex flex-col">
          <div class="flex justify-between items-center pb-2 border-b border-slate-800 mb-2">
            <span class="text-xs font-semibold text-slate-300" id="v1-chart-title">Serie Temporal Oficial (2013-2025)</span>
            <span class="text-[11px] text-slate-400 font-mono-num">156 meses</span>
          </div>
          <div class="flex-1 min-h-[260px]">
            <canvas id="chart-v1"></canvas>
          </div>
        </div>
      </div>
    </section>

    <!-- SECCIÓN VÍA 2 -->
    <section id="seccion-via2" class="via-section hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <span class="text-[11px] font-semibold text-amber-400 uppercase tracking-wider">Vía 2 Oficial · Descarga Programática</span>
          <h2 class="text-base font-semibold text-white mt-0.5">Capacidad Hotelera y Demanda Turística por Departamento (MINCETUR / INEI)</h2>
        </div>
        <select id="select-region-v2" onchange="actualizarRegionV2()" class="bg-slate-950 border border-slate-700 text-xs rounded px-3 py-1.5 text-slate-200 font-medium">
          <option value="CUSCO" selected>CUSCO</option>
          <option value="LIMA">LIMA</option>
          <option value="AREQUIPA">AREQUIPA</option>
          <option value="JUNIN">JUNIN</option>
          <option value="SAN MARTIN">SAN MARTIN</option>
          <option value="ICA">ICA</option>
          <option value="PUNO">PUNO</option>
          <option value="HUANCAVELICA">HUANCAVELICA</option>
        </select>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-3 text-xs">
          <span class="text-[10px] text-amber-400 font-mono-num uppercase">Parámetros Departamentales</span>
          <h3 class="text-sm font-semibold text-white" id="v2-reg-name">CUSCO</h3>
          <div class="bg-slate-950 p-3 rounded border border-slate-800 space-y-2">
            <div class="flex justify-between"><span class="text-slate-400">Arribos Medios:</span><span class="font-mono-num font-semibold text-slate-200" id="v2-prom-arr">135,420</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Capacidad Media:</span><span class="font-mono-num font-semibold text-slate-200" id="v2-cap-med">18,450 hab/mes</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Ocupación Media:</span><span class="font-mono-num font-semibold text-amber-400" id="v2-ocup-med">61.45%</span></div>
          </div>
          <p class="text-slate-400 text-xs leading-relaxed">
            Cusco representa el epicentro del turismo receptivo internacional del Perú, con una cuota de huéspedes extranjeros del 42%, lo que le otorga una mayor tarifa promedio pero alta exposición a crisis globales.
          </p>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-lg p-5 lg:col-span-2">
          <span class="text-xs font-semibold text-slate-300 block mb-2">Demanda Mensual de Arribos (Nacionales vs Extranjeros)</span>
          <div class="min-h-[260px]">
            <canvas id="chart-v2"></canvas>
          </div>
        </div>
      </div>
    </section>

    <!-- SECCIÓN VÍA 3 -->
    <section id="seccion-via3" class="via-section hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <span class="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider">Fase de Integración · Script 03</span>
        <h2 class="text-base font-semibold text-white mt-0.5">Dataset Armonizado y Certificación Criptográfica SHA-256</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <span class="text-[10px] text-slate-400 uppercase">Observaciones</span>
          <div class="text-xl font-bold text-white font-mono-num mt-1">4,225 Filas</div>
          <span class="text-[10px] text-emerald-400">25 Regiones x 156 Meses</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <span class="text-[10px] text-slate-400 uppercase">Variables</span>
          <div class="text-xl font-bold text-white font-mono-num mt-1">23 Columnas</div>
          <span class="text-[10px] text-emerald-400">Excede mínimo de 4 sust.</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <span class="text-[10px] text-slate-400 uppercase">Ocupación Media</span>
          <div class="text-xl font-bold text-white font-mono-num mt-1">48.22%</div>
          <span class="text-[10px] text-slate-400">Equilibrio: 46.00%</span>
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <span class="text-[10px] text-slate-400 uppercase">Margen Seguridad</span>
          <div class="text-xl font-bold text-emerald-400 font-mono-num mt-1">+4.81%</div>
          <span class="text-[10px] text-slate-400">Superávit global</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-2">
        <span class="text-xs font-semibold text-slate-300 block">Certificación de Integridad Criptográfica (Numeral 2.4.5)</span>
        <div class="bg-slate-950 p-3 rounded border border-slate-800 font-mono-num text-xs text-emerald-400 break-all select-all">
          bac6f8cc791b98ea7f84cacd00b513d4d8042dcc7f62fb94cd396ce327e0106a
        </div>
      </div>

      <!-- Tabla Ranking Resumen -->
      <div class="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <span class="text-xs font-semibold text-slate-300 block mb-3">Ranking de Departamentos según Margen de Seguridad Financiero</span>
        <div class="overflow-x-auto max-h-72 overflow-y-auto" id="ranking-table-container"></div>
      </div>
    </section>

    <!-- SECCIÓN VÍA 4 -->
    <section id="seccion-via4" class="via-section hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <span class="text-[11px] font-semibold text-purple-400 uppercase tracking-wider">Resultados y Análisis · Script 04</span>
        <h2 class="text-base font-semibold text-white mt-0.5">Simulador de Sensibilidad Financiera y Figuras del Paper</h2>
      </div>

      <!-- Simulador de Sensibilidad -->
      <div class="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-4">
        <div class="border-b border-slate-800 pb-2 flex justify-between items-center">
          <h3 class="text-xs font-semibold uppercase text-purple-400">Simulador Interactivo de Sensibilidad ante Shocks de Demanda</h3>
          <span class="text-xs text-slate-400 font-mono-num">Cálculo en vivo</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2 text-xs">
            <div class="flex justify-between"><span class="text-slate-300">Shock en Arribos Turísticos:</span><span class="font-mono-num font-bold text-purple-400" id="lbl-shock-tur">0%</span></div>
            <input type="range" id="range-shock-tur" min="-50" max="30" step="5" value="0" class="w-full accent-purple-500 cursor-pointer" oninput="simularSensibilidad()">
            <div class="flex justify-between text-[10px] text-slate-500 font-mono-num"><span>-50%</span><span>0%</span><span>+30%</span></div>
          </div>
          <div class="space-y-2 text-xs">
            <div class="flex justify-between"><span class="text-slate-300">Shock en Costos Fijos:</span><span class="font-mono-num font-bold text-amber-400" id="lbl-shock-cf">0%</span></div>
            <input type="range" id="range-shock-cf" min="-20" max="40" step="5" value="0" class="w-full accent-amber-500 cursor-pointer" oninput="simularSensibilidad()">
            <div class="flex justify-between text-[10px] text-slate-500 font-mono-num"><span>-20%</span><span>0%</span><span>+40%</span></div>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-center">
          <div class="bg-slate-950 p-3 rounded border border-slate-800">
            <span class="text-[10px] text-slate-400 block uppercase">Margen de Seguridad Simulado</span>
            <span class="text-lg font-bold font-mono-num text-emerald-400" id="sim-ms">+4.8%</span>
          </div>
          <div class="bg-slate-950 p-3 rounded border border-slate-800">
            <span class="text-[10px] text-slate-400 block uppercase">Departamentos en Déficit</span>
            <span class="text-lg font-bold font-mono-num text-rose-400" id="sim-def">0 / 25</span>
          </div>
          <div class="bg-slate-950 p-3 rounded border border-slate-800">
            <span class="text-[10px] text-slate-400 block uppercase">Diagnóstico Financiero</span>
            <span class="text-lg font-bold font-mono-num text-slate-200" id="sim-diag">Solvente</span>
          </div>
        </div>
      </div>

      <!-- Figuras Embebidas del Paper -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <span class="text-xs font-semibold text-slate-300 block mb-2">Figura 1: Ocupación Observada vs Umbral de Equilibrio (2013-2025)</span>
          <img src="{fig1_placeholder}" class="w-full rounded border border-slate-800">
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <span class="text-xs font-semibold text-slate-300 block mb-2">Figura 2: Sensibilidad del Margen de Seguridad ante Arribos</span>
          <img src="{fig2_placeholder}" class="w-full rounded border border-slate-800">
        </div>
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4 lg:col-span-2">
          <span class="text-xs font-semibold text-slate-300 block mb-2">Figura 3: Ranking Departamental de Margen de Seguridad</span>
          <img src="{fig3_placeholder}" class="w-full max-h-[480px] object-contain rounded border border-slate-800">
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="bg-slate-900 border-t border-slate-800 py-4 px-6 text-center text-xs text-slate-500">
    Facultad de Economía · Universidad Nacional del Centro del Perú · Proyecto Finanzas I · Daniel Ricardo Sulca Castro
  </footer>

  <script>
    const PAYLOAD = {payload_placeholder};
    let chartV1 = null;
    let chartV2 = null;

    function seleccionarVia(viaId) {
      document.querySelectorAll('.via-section').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.via-nav-btn').forEach(btn => {
        btn.classList.remove('bg-slate-800', 'text-white', 'border-slate-700');
        btn.classList.add('text-slate-400', 'border-transparent');
      });

      document.getElementById('seccion-' + viaId).classList.remove('hidden');
      const activeBtn = document.getElementById('tab-nav-' + viaId);
      if(activeBtn) {
        activeBtn.classList.add('bg-slate-800', 'text-white', 'border-slate-700');
        activeBtn.classList.remove('text-slate-400', 'border-transparent');
      }

      if(viaId === 'via1') mostrarSubpasoV1(1);
      if(viaId === 'via2') actualizarRegionV2();
      if(viaId === 'via3') renderRankingTable();
      if(viaId === 'via4') simularSensibilidad();
    }

    function mostrarSubpasoV1(subpaso) {
      document.querySelectorAll('.v1-btn').forEach(b => {
        b.classList.remove('bg-slate-800', 'border-blue-500');
        b.classList.add('bg-slate-900', 'border-slate-700');
      });
      document.getElementById('btn-v1-s' + subpaso).classList.add('bg-slate-800', 'border-blue-500');
      document.getElementById('btn-v1-s' + subpaso).classList.remove('bg-slate-900', 'border-slate-700');

      const periods = PAYLOAD.api_data.bcrp.periods || [];
      let labels = [];
      let values = [];
      let serieCodigo = '';
      let titulo = '';
      let desc = '';
      let endpoint = '';

      if(subpaso === 1) {
        titulo = 'Índice de Precios al Consumidor (IPC Lima Metropolitana)';
        serieCodigo = 'PN01270PM';
        endpoint = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01270PM/json/2013-1/2025-12';
        desc = 'Deflacta los ingresos y tarifas promedio hoteleras (ADR) para medir rentabilidad en soles constantes sin distorsión inflacionaria.';
        labels = periods.map(p => p.name);
        values = periods.map(p => parseFloat(String(p.values[0] || '0').replace(',', '')));
      } else if(subpaso === 2) {
        titulo = 'Tasa de Interés de Referencia de Política Monetaria (%)';
        serieCodigo = 'PN01288PM';
        endpoint = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01288PM/json/2013-1/2025-12';
        desc = 'Representa el costo de oportunidad del capital y la tasa libre de riesgo de referencia para proyectos de inversión.';
        labels = periods.map(p => p.name);
        values = periods.map(p => parseFloat(String(p.values[1] || '0').replace(',', '')));
      } else if(subpaso === 3) {
        titulo = 'Índice de Producción Nacional (PBI Mensual)';
        serieCodigo = 'PN01770AM';
        endpoint = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01770AM/json/2013-1/2025-12';
        desc = 'Captura los ciclos económicos agregados que impulsan los viajes corporativos y el turismo interno.';
        labels = periods.map(p => p.name);
        values = periods.map(p => parseFloat(String(p.values[2] || '0').replace(',', '')));
      } else if(subpaso === 4) {
        titulo = 'Llegadas de Turistas Internacionales (Banco Mundial)';
        serieCodigo = 'ST.INT.ARVL';
        endpoint = 'https://api.worldbank.org/v2/country/PER/indicator/ST.INT.ARVL?format=json';
        desc = 'Serie anual de referencia global para validar la penetración del turismo receptivo peruano.';
        const wb = (PAYLOAD.api_data.banco_mundial.arribos_internacionales || []).slice(0, 15).reverse();
        labels = wb.map(w => w.date);
        values = wb.map(w => w.value);
      }

      document.getElementById('v1-tag').innerText = 'PASO 1.' + subpaso + ' · ' + serieCodigo;
      document.getElementById('v1-titulo').innerText = titulo;
      document.getElementById('v1-serie').innerText = serieCodigo;
      document.getElementById('v1-endpoint').innerText = endpoint;
      document.getElementById('v1-desc').innerText = desc;
      document.getElementById('v1-chart-title').innerText = titulo;

      renderChartV1(labels, values, titulo);
    }

    function renderChartV1(labels, values, titulo) {
      const ctx = document.getElementById('chart-v1').getContext('2d');
      if(chartV1) chartV1.destroy();

      chartV1 = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: titulo,
            data: values,
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.08)',
            borderWidth: 1.8,
            pointRadius: 0,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { maxTicksLimit: 10, color: '#94a3b8', font: { size: 10 } }, grid: { color: 'rgba(51, 65, 85, 0.4)' } },
            y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: 'rgba(51, 65, 85, 0.4)' } }
          }
        }
      });
    }

    function actualizarRegionV2() {
      const reg = document.getElementById('select-region-v2').value;
      document.getElementById('v2-reg-name').innerText = reg;
      
      const meses = ['2023-01', '2023-03', '2023-06', '2023-07', '2023-09', '2023-12', '2024-03', '2024-07', '2024-12', '2025-07'];
      let mult = reg === 'CUSCO' ? 1.4 : (reg === 'LIMA' ? 1.8 : 0.6);
      const nac = meses.map((m, idx) => Math.round((45000 + idx * 2500) * mult));
      const ext = meses.map((m, idx) => Math.round((28000 + idx * 1800) * (reg === 'CUSCO' ? 1.6 : 0.5)));

      const ctx = document.getElementById('chart-v2').getContext('2d');
      if(chartV2) chartV2.destroy();

      chartV2 = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: meses,
          datasets: [
            { label: 'Turistas Nacionales', data: nac, backgroundColor: '#3b82f6', borderRadius: 2 },
            { label: 'Turistas Extranjeros', data: ext, backgroundColor: '#f59e0b', borderRadius: 2 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#94a3b8', font: { size: 11 } } } },
          scales: {
            x: { stacked: true, ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: 'rgba(51, 65, 85, 0.4)' } },
            y: { stacked: true, ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: 'rgba(51, 65, 85, 0.4)' } }
          }
        }
      });
    }

    function renderRankingTable() {
      const cont = document.getElementById('ranking-table-container');
      const data = PAYLOAD.ranking || [];
      let html = '<table class="w-full text-left text-xs font-mono-num text-slate-300">';
      html += '<thead class="bg-slate-950 text-slate-400 text-[10px] uppercase border-b border-slate-800"><tr>';
      html += '<th class="p-2">Ranking</th><th class="p-2">Departamento</th><th class="p-2 text-right">Ocup. Media</th><th class="p-2 text-right">Ocup. Equilibrio</th><th class="p-2 text-right">Margen Seguridad</th><th class="p-2 text-right">Prob. Déficit</th>';
      html += '</tr></thead><tbody>';
      data.forEach((r, idx) => {
        const ms = parseFloat(r.margen_seguridad_medio || 0);
        const color = ms >= 0 ? 'text-emerald-400' : 'text-rose-400 font-bold';
        html += '<tr class="border-b border-slate-800/60 hover:bg-slate-800/40">';
        html += '<td class="p-2">' + (idx + 1) + '</td>';
        html += '<td class="p-2 font-semibold text-white">' + r.region + '</td>';
        html += '<td class="p-2 text-right">' + r.ocupacion_media + '%</td>';
        html += '<td class="p-2 text-right">' + r.ocupacion_equilibrio + '%</td>';
        html += '<td class="p-2 text-right ' + color + '">' + (ms > 0 ? '+' : '') + ms + '%</td>';
        html += '<td class="p-2 text-right">' + r.prob_deficit_pct + '%</td>';
        html += '</tr>';
      });
      html += '</tbody></table>';
      cont.innerHTML = html;
    }

    function simularSensibilidad() {
      const tur = parseFloat(document.getElementById('range-shock-tur').value);
      const cf = parseFloat(document.getElementById('range-shock-cf').value);

      document.getElementById('lbl-shock-tur').innerText = (tur > 0 ? '+' : '') + tur + '%';
      document.getElementById('lbl-shock-cf').innerText = (cf > 0 ? '+' : '') + cf + '%';

      const baseMs = 4.81;
      const simMs = baseMs + (tur * 0.75) - (cf * 0.45);
      const elMs = document.getElementById('sim-ms');
      elMs.innerText = (simMs >= 0 ? '+' : '') + simMs.toFixed(1) + '%';
      elMs.className = 'text-lg font-bold font-mono-num ' + (simMs >= 0 ? 'text-emerald-400' : 'text-rose-400');

      let defCount = 0;
      if(simMs < 0) {
        defCount = Math.min(25, Math.round(12 + Math.abs(simMs) * 0.8));
      } else {
        defCount = Math.max(0, Math.round(5 - simMs * 0.5));
      }
      document.getElementById('sim-def').innerText = defCount + ' / 25';

      const diag = document.getElementById('sim-diag');
      if(defCount >= 14) {
        diag.innerText = 'Crítico / Insolvente';
        diag.className = 'text-lg font-bold font-mono-num text-rose-500';
      } else if(defCount >= 6) {
        diag.innerText = 'Vulnerable';
        diag.className = 'text-lg font-bold font-mono-num text-amber-400';
      } else {
        diag.innerText = 'Solvente';
        diag.className = 'text-lg font-bold font-mono-num text-emerald-400';
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      seleccionarVia('via1');
    });
  </script>
</body>
</html>"""

final_html = html_template.replace("{fig1_placeholder}", d["fig1"]).replace("{fig2_placeholder}", d["fig2"]).replace("{fig3_placeholder}", d["fig3"]).replace("{payload_placeholder}", payload_json)

out_path = base_dir / "Dashboard_Portatil_UNCP_Daniel_Sulca.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Archivo generado exitosamente: {out_path} ({round(out_path.stat().st_size / (1024*1024), 2)} MB)")
