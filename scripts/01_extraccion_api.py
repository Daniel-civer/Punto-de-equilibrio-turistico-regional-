"""
=============================================================================
PROYECTO: Punto de equilibrio y sensibilidad en un proyecto turístico regional
CURSO: Finanzas I (055D) - UNCP | 2026-II
DOCENTE: Dr. Ciro Iván Machacuay Meza
ARCHIVO: 01_extraccion_api.py
DESCRIPCIÓN: Vía 1 - Extracción programática de datos macroeconómicos y
             turísticos desde las APIs oficiales de BCRPData y Banco Mundial.
=============================================================================
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests

# ---------------------------------------------------------------------------
# 1. PARÁMETROS GLOBALES Y CONGELAMIENTO DE CONSULTA (Numeral 2.4.5)
# ---------------------------------------------------------------------------
# Se fijan constantes explícitas para garantizar reproducibilidad exacta.
FECHA_INICIO = "2013-1"
FECHA_CORTE = "2025-12"
PAIS_WB = "PER"

# Rutas relativas al proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE_DIR / "datos"
LOGS_FILE = BASE_DIR / "log_ejecucion.txt"

# Crear carpetas si no existen
DATOS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 2. CONFIGURACIÓN DE REGISTRO (LOG DE EJECUCIÓN)
# ---------------------------------------------------------------------------
def registrar_log(mensaje: str):
    """Registra en consola y apenda en log_ejecucion.txt con timestamp exacto."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ahora}] {mensaje}"
    print(linea)
    with open(LOGS_FILE, "a", encoding="utf-8") as f:
        f.write(linea + "\n")

# ---------------------------------------------------------------------------
# 3. EXTRACCIÓN DE BCRPData (API OFICIAL DEL BCRP)
# ---------------------------------------------------------------------------
def extraer_bcrp_series(codigos_series: list, inicio: str, fin: str) -> dict:
    """
    Consume el API REST de BCRPData para las series solicitadas.
    Endpoint: https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{series}/json/{inicio}/{fin}
    """
    codigos_str = "-".join(codigos_series)
    url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{codigos_str}/json/{inicio}/{fin}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Finanzas1-UNCP-Investigacion"
    }
    
    registrar_log(f"Consultando BCRPData API: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        status = response.status_code
        registrar_log(f"Respuesta BCRPData: HTTP {status}")
        
        if status == 200:
            datos_json = response.json()
            num_periodos = len(datos_json.get("periods", []))
            registrar_log(f"BCRPData exitoso: {num_periodos} periodos mensuales descargados.")
            return datos_json
        else:
            registrar_log(f"ERROR: BCRPData respondió con código {status}: {response.text[:200]}")
            return {}
    except requests.exceptions.RequestException as e:
        registrar_log(f"ERROR de conexión en BCRPData: {str(e)}")
        return {}

# ---------------------------------------------------------------------------
# 4. EXTRACCIÓN DE BANCO MUNDIAL (WDI API)
# ---------------------------------------------------------------------------
def extraer_banco_mundial(indicador: str, pais: str = "PER") -> list:
    """
    Consume la API REST de Banco Mundial (World Development Indicators - WDI).
    Endpoint: https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json&per_page=100
    """
    url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json&per_page=100"
    registrar_log(f"Consultando Banco Mundial API: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        status = response.status_code
        registrar_log(f"Respuesta Banco Mundial: HTTP {status}")
        
        if status == 200:
            data = response.json()
            if len(data) > 1:
                registros = data[1]
                registrar_log(f"Banco Mundial exitoso: {len(registros)} observaciones anuales obtenidas.")
                return registros
            else:
                registrar_log("Banco Mundial: Estructura de respuesta sin datos.")
                return []
        else:
            registrar_log(f"ERROR: Banco Mundial respondió con código {status}")
            return []
    except requests.exceptions.RequestException as e:
        registrar_log(f"ERROR de conexión en Banco Mundial: {str(e)}")
        return []

# ---------------------------------------------------------------------------
# 5. EJECUCIÓN PRINCIPAL Y GUARDADO DE DATOS CRUDOS (NUMERAL 2.4.2)
# ---------------------------------------------------------------------------
def main():
    registrar_log("=== INICIO DE EXTRACCIÓN VÍA 1: APIs PROGRAMÁTICAS ===")
    
    # Series macroeconómicas del BCRP:
    # PN01270PM: IPC Lima Metropolitana (Índice Dic.2021=100)
    # PN01288PM: Tasa de interés de referencia de la política monetaria (%)
    # PN01770AM: PBI mensual / Índice de Producción Nacional (Base 2007)
    series_bcrp = ["PN01270PM", "PN01288PM", "PN01770AM"]
    
    data_bcrp = extraer_bcrp_series(series_bcrp, FECHA_INICIO, FECHA_CORTE)
    
    # Serie de Turismo Banco Mundial:
    # ST.INT.ARVL: Arribos de turistas internacionales
    # ST.INT.RCPT.CD: Ingresos por turismo internacional (US$ corrientes)
    data_wb_arribos = extraer_banco_mundial("ST.INT.ARVL", PAIS_WB)
    data_wb_ingresos = extraer_banco_mundial("ST.INT.RCPT.CD", PAIS_WB)
    
    # Estructura cruda combinada tal como sale de la fuente
    datos_crudos_api = {
        "metadatos": {
            "fecha_extraccion": datetime.now().isoformat(),
            "rango_solicitado": {"inicio": FECHA_INICIO, "corte": FECHA_CORTE},
            "fuentes": ["BCRPData", "Banco Mundial WDI"]
        },
        "bcrp": data_bcrp,
        "banco_mundial": {
            "arribos_internacionales": data_wb_arribos,
            "ingresos_turismo_usd": data_wb_ingresos
        }
    }
    
    # Guardado del crudo sin editar (exigencia estricta de la rúbrica)
    archivo_crudo = DATOS_DIR / "datos_crudos_api.json"
    with open(archivo_crudo, "w", encoding="utf-8") as f:
        json.dump(datos_crudos_api, f, ensure_ascii=False, indent=2)
        
    num_bcrp_filas = len(data_bcrp.get("periods", []))
    num_wb_filas = len(data_wb_arribos) + len(data_wb_ingresos)
    
    registrar_log(f"Archivo crudo guardado exitosamente en: {archivo_crudo.name}")
    registrar_log(f"Resumen de registros descargados: BCRP={num_bcrp_filas} meses | Banco Mundial={num_wb_filas} registros")
    registrar_log("=== FIN DE EXTRACCIÓN VÍA 1 ===")

if __name__ == "__main__":
    main()
