"""
=============================================================================
PROYECTO: Punto de equilibrio y sensibilidad en un proyecto turístico regional
CURSO: Finanzas I (055D) - UNCP | 2026-II
DOCENTE: Dr. Ciro Iván Machacuay Meza
ARCHIVO: 04_analisis.py
DESCRIPCIÓN: Estimaciones econométricas, análisis de punto de equilibrio,
             matrices de sensibilidad y generación de tablas y figuras para
             el artículo y diapositivas de sustentación.
=============================================================================
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# 1. PARÁMETROS GLOBALES Y RUTAS RELATIVAS (Numeral 2.4.4)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE_DIR / "datos"
SALIDAS_DIR = BASE_DIR / "salidas"
DATOS_PROCESADOS_CSV = DATOS_DIR / "datos_procesados_turismo.csv"

SALIDAS_DIR.mkdir(parents=True, exist_ok=True)

# Configuración visual para publicaciones científicas (estilo Seaborn / Journal)
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300
})

def main():
    print("=== INICIO DE ESTIMACIONES Y ANÁLISIS FINANCIERO (04) ===")
    
    # 1. Cargar base de datos procesada
    df = pd.read_csv(DATOS_PROCESADOS_CSV)
    print(f"Cargadas {len(df)} observaciones del panel departamental.")
    
    # Variables auxiliares para modelación
    df["log_arribos_totales"] = np.log(df["arribos_totales"].clip(lower=1))
    df["log_pbi"] = np.log(df["bcrp_pbi_indice"].clip(lower=1))
    
    # -----------------------------------------------------------------------
    # TABLA 1: Estadísticas Descriptivas del Panel (2013-2025)
    # -----------------------------------------------------------------------
    vars_desc = [
        "arribos_totales", "arribos_nacionales", "arribos_extranjeros",
        "tasa_ocupacion_pct", "tasa_ocupacion_equilibrio_pct", "margen_seguridad_pct",
        "tarifa_adr_nominal", "bcrp_tasa_referencia", "bcrp_pbi_indice"
    ]
    
    desc_df = df[vars_desc].describe().T[["mean", "std", "min", "50%", "max"]]
    desc_df.columns = ["Media", "Desv. Est.", "Mínimo", "Mediana", "Máximo"]
    desc_df = desc_df.round(2)
    tabla1_path = SALIDAS_DIR / "tabla1_estadisticas_descriptivas.csv"
    desc_df.to_csv(tabla1_path, encoding="utf-8")
    print(f"Tabla 1 guardada en: {tabla1_path.name}")
    
    # -----------------------------------------------------------------------
    # TABLA 2: Ranking Departamental de Ocupación vs Punto de Equilibrio
    # -----------------------------------------------------------------------
    ranking_df = df.groupby(["id_region", "region"]).agg(
        ocupacion_media=("tasa_ocupacion_pct", "mean"),
        ocupacion_equilibrio=("tasa_ocupacion_equilibrio_pct", "mean"),
        margen_seguridad_medio=("margen_seguridad_pct", "mean"),
        prob_deficit=("deficit_operativo_dummy", "mean")
    ).reset_index()
    
    ranking_df["prob_deficit_pct"] = (ranking_df["prob_deficit"] * 100).round(1)
    ranking_df = ranking_df.sort_values("margen_seguridad_medio", ascending=False).reset_index(drop=True)
    ranking_df.index = ranking_df.index + 1
    ranking_df.index.name = "Ranking"
    
    tabla2_path = SALIDAS_DIR / "tabla2_ranking_equilibrio_departamental.csv"
    ranking_df.round(2).to_csv(tabla2_path, encoding="utf-8")
    print(f"Tabla 2 guardada en: {tabla2_path.name}")
    
    # -----------------------------------------------------------------------
    # TABLA 3: Modelo Econométrico de Sensibilidad (MCO Clustered)
    # TasaOcupacion = beta0 + beta1*Log(Arribos) + beta2*PBI + beta3*IPC + beta4*TasaBCRP + e
    # -----------------------------------------------------------------------
    modelo = smf.ols(
        "tasa_ocupacion_pct ~ log_arribos_totales + bcrp_pbi_indice + bcrp_tasa_referencia",
        data=df
    ).fit(cov_type="cluster", cov_kwds={"groups": df["id_region"]})
    
    coef_df = pd.DataFrame({
        "Coeficiente": modelo.params,
        "Error_Estandar": modelo.bse,
        "t_stat": modelo.tvalues,
        "p_valor": modelo.pvalues
    }).round(4)
    
    tabla3_path = SALIDAS_DIR / "tabla3_modelo_sensibilidad.csv"
    coef_df.to_csv(tabla3_path, encoding="utf-8")
    print(f"Tabla 3 (Modelo econométrico) guardada en: {tabla3_path.name}")
    print(f"R-cuadrado del modelo: {modelo.rsquared:.4f}")
    
    # -----------------------------------------------------------------------
    # FIGURA 1: Evolución de la Tasa de Ocupación vs Punto de Equilibrio (2013-2025)
    # -----------------------------------------------------------------------
    plt.figure(figsize=(10, 5.5))
    df_tiempo = df.groupby("periodo")[["tasa_ocupacion_pct", "tasa_ocupacion_equilibrio_pct"]].mean().reset_index()
    # Tomar muestra de periodos espaciados para el eje X
    ticks_idx = np.linspace(0, len(df_tiempo) - 1, 14, dtype=int)
    
    plt.plot(df_tiempo["periodo"], df_tiempo["tasa_ocupacion_pct"], label="Tasa de Ocupación Observada (%)", color="#1f77b4", lw=2.2)
    plt.axhline(df_tiempo["tasa_ocupacion_equilibrio_pct"].mean(), color="#d62728", linestyle="--", lw=1.8, label=f"Punto de Equilibrio Crítico Medio ({df_tiempo['tasa_ocupacion_equilibrio_pct'].mean():.1f}%)")
    plt.fill_between(
        df_tiempo["periodo"],
        df_tiempo["tasa_ocupacion_pct"],
        df_tiempo["tasa_ocupacion_equilibrio_pct"].mean(),
        where=(df_tiempo["tasa_ocupacion_pct"] >= df_tiempo["tasa_ocupacion_equilibrio_pct"].mean()),
        color="#2ca02c", alpha=0.15, label="Zona de Margen de Seguridad (Superávit)"
    )
    plt.fill_between(
        df_tiempo["periodo"],
        df_tiempo["tasa_ocupacion_pct"],
        df_tiempo["tasa_ocupacion_equilibrio_pct"].mean(),
        where=(df_tiempo["tasa_ocupacion_pct"] < df_tiempo["tasa_ocupacion_equilibrio_pct"].mean()),
        color="#d62728", alpha=0.20, label="Zona de Déficit Operativo (Shock COVID-19)"
    )
    
    plt.xticks(ticks_idx, df_tiempo["periodo"].iloc[ticks_idx], rotation=45)
    plt.title("Figura 1: Evolución Temporal de la Tasa de Ocupación Hotelera y Umbral de Equilibrio (2013-2025)", pad=12)
    plt.xlabel("Periodo (Año-Mes)")
    plt.ylabel("Tasa de Ocupación (%)")
    plt.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    fig1_path = SALIDAS_DIR / "figura1_evolucion_ocupacion_equilibrio.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"Figura 1 guardada en: {fig1_path.name}")
    
    # -----------------------------------------------------------------------
    # FIGURA 2: Matriz de Sensibilidad: Variación de Arribos vs Margen de Seguridad
    # -----------------------------------------------------------------------
    plt.figure(figsize=(9, 5.5))
    sns.scatterplot(
        data=df.sample(min(800, len(df)), random_state=42),
        x="log_arribos_totales",
        y="margen_seguridad_pct",
        hue="region",
        legend=False,
        alpha=0.6,
        palette="tab20"
    )
    sns.regplot(
        data=df,
        x="log_arribos_totales",
        y="margen_seguridad_pct",
        scatter=False,
        color="#d62728",
        line_kws={"linewidth": 2.5, "label": "Línea de Sensibilidad Promedio"}
    )
    plt.axhline(0, color="black", linestyle=":", lw=1.2, label="Umbral Crítico (Punto de Equilibrio MS=0)")
    plt.title("Figura 2: Sensibilidad del Margen de Seguridad Hotelero ante Shocks de Demanda Turística", pad=12)
    plt.xlabel("Logaritmo de Arribos Totales de Huéspedes")
    plt.ylabel("Margen de Seguridad Financiero (%)")
    plt.legend(loc="lower right")
    plt.tight_layout()
    fig2_path = SALIDAS_DIR / "figura2_sensibilidad_demanda.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"Figura 2 guardada en: {fig2_path.name}")
    
    # -----------------------------------------------------------------------
    # FIGURA 3: Vulnerabilidad Financiera por Departamento (Margen de Seguridad)
    # -----------------------------------------------------------------------
    plt.figure(figsize=(10, 7.5))
    order_regions = ranking_df.sort_values("margen_seguridad_medio", ascending=True)
    colores = ["#2ca02c" if ms >= 0 else "#d62728" for ms in order_regions["margen_seguridad_medio"]]
    
    plt.barh(order_regions["region"], order_regions["margen_seguridad_medio"], color=colores, edgecolor="none", alpha=0.85)
    plt.axvline(0, color="black", linestyle="-", lw=1.0)
    plt.title("Figura 3: Margen de Seguridad Financiero Promedio por Departamento (2013-2025)", pad=12)
    plt.xlabel("Margen de Seguridad Medio sobre el Punto de Equilibrio (%)")
    plt.ylabel("Departamento / Región")
    plt.tight_layout()
    fig3_path = SALIDAS_DIR / "figura3_vulnerabilidad_departamental.png"
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"Figura 3 guardada en: {fig3_path.name}")
    
    print("=== FIN DE ESTIMACIONES Y ANÁLISIS ===")

if __name__ == "__main__":
    main()
