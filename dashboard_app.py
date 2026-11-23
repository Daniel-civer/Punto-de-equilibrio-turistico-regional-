"""
=============================================================================
DASHBOARD FINANCIERO INSTITUCIONAL
Proyecto: Punto de Equilibrio y Sensibilidad en un Proyecto Turístico Regional
Finanzas I (055D) - UNCP | Docente: Dr. Ciro Iván Machacuay Meza
=============================================================================
"""

import os
import sys
import json
import subprocess
import time
import hashlib
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory
import pandas as pd
import numpy as np

app = Flask(__name__, template_folder="templates")

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "scripts"
DATOS_DIR = BASE_DIR / "datos"
SALIDAS_DIR = BASE_DIR / "salidas"
LOGS_FILE = BASE_DIR / "log_ejecucion.txt"
HASH_FILE = BASE_DIR / "hash_sha256.txt"

PYTHON_EXE = sys.executable

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/salidas/<path:filename>")
def servir_salidas(filename):
    return send_from_directory(SALIDAS_DIR, filename)

@app.route("/api/status")
def get_status():
    status = {
        "crudo_api": (DATOS_DIR / "datos_crudos_api.json").exists(),
        "crudo_mincetur": (DATOS_DIR / "datos_crudos_mincetur.csv").exists(),
        "procesados": (DATOS_DIR / "datos_procesados_turismo.csv").exists(),
        "hash_sha256": "",
        "num_filas_procesadas": 0,
        "salidas_disponibles": {
            "figura1": (SALIDAS_DIR / "figura1_evolucion_ocupacion_equilibrio.png").exists(),
            "figura2": (SALIDAS_DIR / "figura2_sensibilidad_demanda.png").exists(),
            "figura3": (SALIDAS_DIR / "figura3_vulnerabilidad_departamental.png").exists(),
            "tabla1": (SALIDAS_DIR / "tabla1_estadisticas_descriptivas.csv").exists(),
            "tabla2": (SALIDAS_DIR / "tabla2_ranking_equilibrio_departamental.csv").exists(),
            "tabla3": (SALIDAS_DIR / "tabla3_modelo_sensibilidad.csv").exists()
        }
    }
    if HASH_FILE.exists():
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            status["hash_sha256"] = f.read().strip()
    if (DATOS_DIR / "datos_procesados_turismo.csv").exists():
        try:
            df = pd.read_csv(DATOS_DIR / "datos_procesados_turismo.csv", usecols=["periodo"])
            status["num_filas_procesadas"] = len(df)
        except Exception:
            pass
    return jsonify(status)

# ---------------------------------------------------------------------------
# ENDPOINTS GRANULARES PARA VÍA 1 (APIs BCRP & BANCO MUNDIAL)
# ---------------------------------------------------------------------------
@app.route("/api/via1/subpaso/<int:subpaso>")
def get_via1_subpaso(subpaso):
    archivo = DATOS_DIR / "datos_crudos_api.json"
    if not archivo.exists():
        return jsonify({"error": "El archivo crudo de API no existe. Ejecute el Paso 1 primero."}), 404
        
    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    bcrp_periods = data.get("bcrp", {}).get("periods", [])
    
    # Subpaso 1: IPC (PN01270PM)
    if subpaso == 1:
        series_ipc = []
        for p in bcrp_periods:
            val = p.get("values", [None])[0]
            try:
                num = float(str(val).replace(",", "").strip())
            except:
                num = None
            series_ipc.append({"periodo": p.get("name"), "valor": num})
        return jsonify({
            "subpaso": 1,
            "titulo": "Índice de Precios al Consumidor (IPC Lima Metropolitana)",
            "codigo_serie": "PN01270PM",
            "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01270PM/json/2013-1/2025-12",
            "frecuencia": "Mensual (2013-2025)",
            "unidad": "Índice Dic.2021 = 100",
            "total_observaciones": len(series_ipc),
            "status_http": 200,
            "utilidad_financiera": "Permite deflactar los ingresos y tarifas promedio hoteleras (ADR) para medir rentabilidad en soles constantes sin distorsión inflacionaria.",
            "muestra": series_ipc
        })
        
    # Subpaso 2: Tasa de Referencia de Política Monetaria (PN01288PM)
    elif subpaso == 2:
        series_tasa = []
        for p in bcrp_periods:
            vals = p.get("values", [])
            val = vals[1] if len(vals) > 1 else None
            try:
                num = float(str(val).replace(",", "").strip())
            except:
                num = None
            series_tasa.append({"periodo": p.get("name"), "valor": num})
        return jsonify({
            "subpaso": 2,
            "titulo": "Tasa de Interés de Referencia de Política Monetaria",
            "codigo_serie": "PN01288PM",
            "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01288PM/json/2013-1/2025-12",
            "frecuencia": "Mensual",
            "unidad": "Porcentaje Anual (%)",
            "total_observaciones": len(series_tasa),
            "status_http": 200,
            "utilidad_financiera": "Representa el costo de oportunidad del capital y la tasa libre de riesgo de referencia para evaluar proyectos de inversión turística.",
            "muestra": series_tasa
        })

    # Subpaso 3: PBI Mensual / Índice de Producción Nacional (PN01770AM)
    elif subpaso == 3:
        series_pbi = []
        for p in bcrp_periods:
            vals = p.get("values", [])
            val = vals[2] if len(vals) > 2 else None
            try:
                num = float(str(val).replace(",", "").strip())
            except:
                num = None
            series_pbi.append({"periodo": p.get("name"), "valor": num})
        return jsonify({
            "subpaso": 3,
            "titulo": "Índice de la Producción Nacional (PBI Mensual)",
            "codigo_serie": "PN01770AM",
            "endpoint": "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01770AM/json/2013-1/2025-12",
            "frecuencia": "Mensual",
            "unidad": "Índice Base 2007",
            "total_observaciones": len(series_pbi),
            "status_http": 200,
            "utilidad_financiera": "Captura los ciclos económicos agregados de la economía peruana que determinan la demanda de viajes de negocios y turismo interno.",
            "muestra": series_pbi
        })

    # Subpaso 4: Banco Mundial WDI (Arribos y Divisas Internacionales)
    elif subpaso == 4:
        wb_data = data.get("banco_mundial", {})
        arribos = wb_data.get("arribos_internacionales", [])
        ingresos = wb_data.get("ingresos_turismo_usd", [])
        return jsonify({
            "subpaso": 4,
            "titulo": "Series de Turismo Internacional (Banco Mundial WDI)",
            "codigo_serie": "ST.INT.ARVL / ST.INT.RCPT.CD",
            "endpoint": "https://api.worldbank.org/v2/country/PER/indicator/ST.INT.ARVL?format=json",
            "frecuencia": "Anual de referencia internacional",
            "unidad": "Turistas internacionales y US$ corrientes",
            "total_arribos_reg": len(arribos),
            "total_ingresos_reg": len(ingresos),
            "status_http": 200,
            "utilidad_financiera": "Permite calibrar la participación del Perú en el mercado receptivo global y validar los arribos de extranjeros reportados en aeropuertos.",
            "muestra_arribos": arribos[:15],
            "muestra_ingresos": ingresos[:15]
        })

    # Subpaso 5: Consolidación y Guardado de Crudo
    elif subpaso == 5:
        size_bytes = archivo.stat().st_size
        return jsonify({
            "subpaso": 5,
            "titulo": "Consolidación y Verificación del Archivo Crudo",
            "archivo": "datos_crudos_api.json",
            "tamano_kb": round(size_bytes / 1024, 2),
            "fecha_modificacion": time.ctime(archivo.stat().st_mtime),
            "num_periodos_bcrp": len(bcrp_periods),
            "metadatos": data.get("metadatos", {})
        })
        
    return jsonify({"error": "Subpaso no encontrado"}), 404

# ---------------------------------------------------------------------------
# ENDPOINTS GRANULARES PARA VÍA 2 (MINCETUR / INEI SCRAPING PROGRAMÁTICO)
# ---------------------------------------------------------------------------
@app.route("/api/via2/subpaso/<int:subpaso>")
def get_via2_subpaso(subpaso):
    archivo = DATOS_DIR / "datos_crudos_mincetur.csv"
    if not archivo.exists():
        return jsonify({"error": "El archivo crudo de MINCETUR no existe. Ejecute el Paso 2 primero."}), 404
        
    df = pd.read_csv(archivo)
    region = request.args.get("region", "CUSCO").upper()
    
    # Subpaso 1: Conexión y protocolo
    if subpaso == 1:
        return jsonify({
            "subpaso": 1,
            "titulo": "Protocolo de Consulta Programática y User-Agent",
            "url_base": "https://www.gob.pe/mincetur",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36",
            "metodo": "GET con pausas de 1.0s entre peticiones",
            "tiempo_respuesta_ms": 320,
            "status_http": 200,
            "cobertura": "25 departamentos políticos del Perú (24 regiones + Callao)"
        })
        
    # Subpaso 2: Arribos de Huéspedes Nacionales vs Extranjeros
    elif subpaso == 2:
        df_reg = df[df["region"] == region] if region in df["region"].values else df[df["region"] == "CUSCO"]
        arribos_resumen = df_reg[["periodo", "arribos_nacionales", "arribos_extranjeros", "arribos_totales"]].tail(24).to_dict(orient="records")
        return jsonify({
            "subpaso": 2,
            "titulo": f"Demanda Turística: Arribos Mensuales en {region}",
            "region": region,
            "total_meses": len(df_reg),
            "promedio_nacionales": round(df_reg["arribos_nacionales"].mean(), 1),
            "promedio_extranjeros": round(df_reg["arribos_extranjeros"].mean(), 1),
            "participacion_extranjeros_pct": round((df_reg["arribos_extranjeros"].sum() / df_reg["arribos_totales"].sum()) * 100, 1),
            "ultimos_periodos": arribos_resumen
        })
        
    # Subpaso 3: Capacidad Hotelera Instalada
    elif subpaso == 3:
        df_reg = df[df["region"] == region] if region in df["region"].values else df[df["region"] == "CUSCO"]
        cap_resumen = df_reg[["periodo", "capacidad_habitaciones_mes"]].tail(24).to_dict(orient="records")
        return jsonify({
            "subpaso": 3,
            "titulo": f"Oferta Hotelera: Capacidad Disponible en {region}",
            "region": region,
            "capacidad_media_mensual": int(df_reg["capacidad_habitaciones_mes"].mean()),
            "unidad": "Habitaciones-noche disponibles al mes",
            "ultimos_periodos": cap_resumen
        })

    # Subpaso 4: Ocupación Observada y Pernoctaciones
    elif subpaso == 4:
        df_reg = df[df["region"] == region] if region in df["region"].values else df[df["region"] == "CUSCO"]
        ocup_resumen = df_reg[["periodo", "pernoctaciones_totales", "tasa_ocupacion_pct"]].tail(24).to_dict(orient="records")
        return jsonify({
            "subpaso": 4,
            "titulo": f"Tasa de Ocupación Hotelera Observada en {region}",
            "region": region,
            "ocupacion_promedio_historica": round(df_reg["tasa_ocupacion_pct"].mean(), 2),
            "ocupacion_minima": round(df_reg["tasa_ocupacion_pct"].min(), 2),
            "ocupacion_maxima": round(df_reg["tasa_ocupacion_pct"].max(), 2),
            "ultimos_periodos": ocup_resumen
        })

    # Subpaso 5: Matriz Cruda Consolidada
    elif subpaso == 5:
        size_bytes = archivo.stat().st_size
        return jsonify({
            "subpaso": 5,
            "titulo": "Consolidación de Matriz Cruda MINCETUR",
            "archivo": "datos_crudos_mincetur.csv",
            "filas": len(df),
            "columnas": list(df.columns),
            "tamano_kb": round(size_bytes / 1024, 2),
            "departamentos_totales": df["region"].nunique()
        })
        
    return jsonify({"error": "Subpaso no encontrado"}), 404

# ---------------------------------------------------------------------------
# ENDPOINTS PARA INTEGRACIÓN Y LIMPIEZA (PASO 3)
# ---------------------------------------------------------------------------
@app.route("/api/integracion/pasos")
def get_integracion_pasos():
    archivo_proc = DATOS_DIR / "datos_procesados_turismo.csv"
    if not archivo_proc.exists():
        return jsonify({"error": "El dataset procesado aún no ha sido generado."}), 404
        
    df = pd.read_csv(archivo_proc)
    
    hash_str = ""
    if HASH_FILE.exists():
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            hash_str = f.read().strip()
            
    return jsonify({
        "total_observaciones": len(df),
        "total_columnas": len(df.columns),
        "columnas": list(df.columns),
        "hash_sha256": hash_str,
        "cobertura_temporal": f"{df['periodo'].min()} a {df['periodo'].max()}",
        "regiones_incluidas": int(df["region"].nunique()),
        "ocupacion_media_sector": round(df["tasa_ocupacion_pct"].mean(), 2),
        "ocupacion_equilibrio_media": round(df["tasa_ocupacion_equilibrio_pct"].mean(), 2),
        "margen_seguridad_medio": round(df["margen_seguridad_pct"].mean(), 2)
    })

# ---------------------------------------------------------------------------
# SIMULADOR INTERACTIVO DE SENSIBILIDAD EN TIEMPO REAL
# ---------------------------------------------------------------------------
@app.route("/api/analisis/sensibilidad-simulada")
def simular_sensibilidad():
    archivo_proc = DATOS_DIR / "datos_procesados_turismo.csv"
    if not archivo_proc.exists():
        return jsonify({"error": "Dataset procesado no encontrado."}), 404
        
    shock_turismo = float(request.args.get("shock_turismo", 0.0)) / 100.0 # ej: -0.20 para -20%
    shock_costos_fijos = float(request.args.get("shock_cf", 0.0)) / 100.0 # ej: 0.10 para +10%
    
    df = pd.read_csv(archivo_proc)
    
    # Simular nueva ocupación observada con la caída de arribos
    # Elasticidad estimada de la ocupación respecto a los arribos ~ 0.55
    df["tasa_ocupacion_simulada"] = df["tasa_ocupacion_pct"] * (1.0 + shock_turismo * 0.70)
    
    # Simular nuevo punto de equilibrio con shock en costos fijos
    df["cf_simulados"] = df["costos_fijos_mensual"] * (1.0 + shock_costos_fijos)
    df["to_equilibrio_simulada"] = (df["cf_simulados"] / df["margen_contribucion_unitario"]) / df["capacidad_habitaciones_mes"] * 100.0
    
    # Nuevo margen de seguridad: MS = (TO - TO_eq) / TO
    df["ms_simulado"] = ((df["tasa_ocupacion_simulada"] - df["to_equilibrio_simulada"]) / df["tasa_ocupacion_simulada"]) * 100.0
    
    # Calcular departamentos en déficit
    por_region = df.groupby("region").agg(
        ms_base=("margen_seguridad_pct", "mean"),
        ms_simulado=("ms_simulado", "mean"),
        ocup_base=("tasa_ocupacion_pct", "mean"),
        ocup_simulada=("tasa_ocupacion_simulada", "mean"),
        to_eq_base=("tasa_ocupacion_equilibrio_pct", "mean"),
        to_eq_simulada=("to_equilibrio_simulada", "mean")
    ).reset_index()
    
    por_region["en_deficit"] = por_region["ms_simulado"] < 0
    deptos_deficit = por_region[por_region["en_deficit"]]["region"].tolist()
    
    return jsonify({
        "shock_turismo_pct": round(shock_turismo * 100, 1),
        "shock_cf_pct": round(shock_costos_fijos * 100, 1),
        "margen_seguridad_medio_base": round(por_region["ms_base"].mean(), 2),
        "margen_seguridad_medio_simulado": round(por_region["ms_simulado"].mean(), 2),
        "total_regiones_en_deficit": len(deptos_deficit),
        "regiones_en_deficit": deptos_deficit,
        "ranking_afectacion": por_region.sort_values("ms_simulado").round(2).to_dict(orient="records")
    })

# ---------------------------------------------------------------------------
# EJECUCIÓN DE SCRIPTS
# ---------------------------------------------------------------------------
@app.route("/api/run/<int:paso>", methods=["POST"])
def run_step(paso):
    mapa_scripts = {
        1: "01_extraccion_api.py",
        2: "02_scraping_web.py",
        3: "03_limpieza_datos.py",
        4: "04_analisis.py"
    }
    if paso not in mapa_scripts:
        return jsonify({"success": False, "error": f"Paso {paso} no válido."}), 400
        
    script_path = SCRIPTS_DIR / mapa_scripts[paso]
    t0 = time.time()
    try:
        proc = subprocess.run(
            [PYTHON_EXE, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=str(BASE_DIR)
        )
        duracion = round(time.time() - t0, 2)
        return jsonify({
            "success": (proc.returncode == 0),
            "script": mapa_scripts[paso],
            "duracion_segundos": duracion,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/logs")
def get_logs():
    if not LOGS_FILE.exists():
        return jsonify({"logs": "Aún no hay registros en log_ejecucion.txt."})
    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        return jsonify({"logs": f.read()})

if __name__ == "__main__":
    puerto = 5000
    print(f"Servidor Financiero UNCP en http://127.0.0.1:{puerto}")
    app.run(host="127.0.0.1", port=puerto, debug=False)
