# Punto de Equilibrio y Sensibilidad en Proyectos Hoteleros Regionales en el Perú (2013-2025)

**Universidad Nacional del Centro del Perú (UNCP)**  
**Facultad de Economía** — Escuela Profesional de Economía  
**Asignatura:** Finanzas I (055D) — Semestre 2026-II  
**Docente:** Dr. Ciro Iván Machacuay Meza  

* **Estudiante:** Daniel Ricardo Sulca Castro
* **Código de Matrícula:** 2024200532L
* **Correo Institucional:** e_2024200532L@uncp.edu.pe
* **Tema Asignado:** Punto de equilibrio y sensibilidad en un proyecto turístico regional
* **Repositorio GitHub:** [https://github.com/Adat13/finanzas-punto-equilibrio-turismo-regional](https://github.com/Adat13/finanzas-punto-equilibrio-turismo-regional)

---

## 1. Resumen de la Investigación

El presente trabajo evalúa empíricamente la sostenibilidad financiera y el umbral de rentabilidad operativa en proyectos hoteleros departamentales en el Perú durante el periodo mensual 2013–2025. Mediante la construcción de un panel balanceado que integra estadísticas oficiales de arribos y capacidad hotelera de **MINCETUR / INEI** con series macroeconómicas del **Banco Central de Reserva del Perú (BCRP)** y del **Banco Mundial (WDI)**, se cuantifica la tasa de ocupación de equilibrio ($TO_{eq}$) y el margen de seguridad financiero ($MS$), modelando la sensibilidad del sector hotelero ante contracciones en la demanda turística, shocks en la tasa de política monetaria y variaciones en el PBI.

---

## 2. Fuentes y Endpoints Oficiales Utilizados

Cumpliendo con la exigencia de la Unidad II (dos vías obligatorias):

1. **Vía 1: APIs Programáticas**
   * **BCRPData (API Pública REST):**  
     Endpoint: `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{codigos}/json/{inicio}/{fin}`  
     *Series:* `PN01270PM` (IPC Lima Metropolitana Base Dic.2021=100), `PN01288PM` (Tasa de referencia de política monetaria %), `PN01770AM` (Índice de Producción Nacional / PBI mensual).
   * **Banco Mundial WDI (API REST):**  
     Endpoint: `https://api.worldbank.org/v2/country/PER/indicator/{indicador}?format=json`  
     *Series:* `ST.INT.ARVL` (Llegadas de turistas internacionales) y `ST.INT.RCPT.CD` (Ingresos por turismo internacional en US$).

2. **Vía 2: Descarga Programática y Scraping Web**
   * **MINCETUR / Badatur e INEI:**  
     URL base: `https://www.gob.pe/mincetur`  
     *Estadísticas:* Arribos mensuales de huéspedes nacionales y extranjeros, pernoctaciones totales y capacidad instalada de habitaciones-noche por departamento.

* **Llave común de integración:** `periodo` (`AAAA-MM`) + `id_region` (Código de Ubigeo departamental de 2 dígitos).
* **Cobertura:** 25 departamentos $\times$ 156 meses (2013-01 a 2025-12) $\rightarrow$ **4,225 observaciones** (supera con holgura el mínimo de 3,000 obs).
* **Fecha de corte de la consulta:** 31 de Diciembre de 2025 (`FECHA_CORTE = "2025-12"`).

---

## 3. Verificación de Integridad Criptográfica (Numeral 2.4.5)

El archivo consolidado y procesado de datos cuenta con el siguiente hash criptográfico verificable:

* **Archivo final:** `datos/datos_procesados_turismo.csv`
* **Algoritmo:** SHA-256
* **Hash SHA-256:**
  ```text
  bac6f8cc791b98ea7f84cacd00b513d4d8042dcc7f62fb94cd396ce327e0106a
  ```

*(El hash se coteja contra el archivo generado y no se altera bajo ninguna circunstancia, garantizando reproducibilidad científica).*

---

## 4. Entorno de Ejecución y Librerías

* **Lenguaje:** Python 3.13.14 (64-bit)
* **Librerías principales y versiones exactas:**
  * `requests==2.34.2`
  * `pandas==3.1.1`
  * `numpy==2.5.5`
  * `scipy==1.18.1`
  * `statsmodels==0.15.0`
  * `matplotlib==3.11.2`
  * `seaborn==0.13.2`
  * `openpyxl==3.1.5`
  *(Consultar `requirements.txt` para la lista completa congelada).*

---

## 5. Orden Estricto de Ejecución

Para replicar de forma 100% autónoma todos los resultados, tablas y figuras desde cero, ejecute los scripts en el siguiente orden secuencial:

```bash
# 1. Extracción de APIs (BCRPData y Banco Mundial)
python scripts/01_extraccion_api.py

# 2. Descarga programática de estadísticas regionales (MINCETUR / INEI)
python scripts/02_scraping_web.py

# 3. Limpieza, armonización, merge y verificación de hash SHA-256
python scripts/03_limpieza_datos.py

# 4. Estimación del punto de equilibrio, modelo de sensibilidad y generación de figuras
python scripts/04_analisis.py
```

---

## 6. Estructura de Entregables Generados

Todos los resultados se guardan automáticamente en la carpeta `salidas/`:
* `tabla1_estadisticas_descriptivas.csv`: Estadísticas sumarias del panel de 25 departamentos.
* `tabla2_ranking_equilibrio_departamental.csv`: Ranking de los 25 departamentos por margen de seguridad financiero ($MS$) y tasa de ocupación observada vs equilibrio.
* `tabla3_modelo_sensibilidad.csv`: Regresión econométrica con errores estándar agrupados por departamento (Clustered Standard Errors).
* `figura1_evolucion_ocupacion_equilibrio.png`: Evolución temporal de la ocupación hotelera vs umbral de equilibrio (2013–2025).
* `figura2_sensibilidad_demanda.png`: Sensibilidad del margen de seguridad ante shocks de demanda turística.
* `figura3_vulnerabilidad_departamental.png`: Gráfico horizontal de ordenamiento por margen de seguridad departamental.
