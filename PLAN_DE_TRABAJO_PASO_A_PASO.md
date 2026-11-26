# PLAN DE TRABAJO PASO A PASO
## Proyecto: Punto de Equilibrio y Sensibilidad en Proyectos Turísticos Regionales
**Curso:** Finanzas I (055D) — UNCP | Dr. Ciro Iván Machacuay Meza

---

## FASE 1: Aprobación y Consolidación del Diseño Metodológico (HOY)
- [x] Revisión exhaustiva de la rúbrica y consignas (Criterios de la Unidad II).
- [x] Análisis del modelo de referencia (presentación de Renzo Ignacio Paucar y repositorio de Xiomara Turín).
- [x] Creación de `ESPECIFICACIONES_PROYECTO.md` con objetivos, fórmulas y variables.


---

## FASE 2: Extracción de Datos (Scripts 01 y 02)
- [ ] **Script `01_extraccion_api.py`:**
  - Conectar a la API de **BCRPData** sin necesidad de API key obligatoria.
  - Extraer series mensuales 2013-2025: Inflación/IPC, PBI mensual (IMAE) y tasa de referencia.
  - Conectar a la API del **Banco Mundial (WDI)** para series internacionales de turismo.
  - Guardar el archivo crudo en `datos/datos_crudos_api.json` o `.csv` sin modificar.
  - Registrar en `log_ejecucion.txt` fecha, hora, código HTTP (200) y número de filas.
- [ ] **Script `02_scraping_web.py`:**
  - Descarga programática de series de **MINCETUR / INEI**:
    - Arribos mensuales por región (turistas nacionales vs extranjeros).
    - Capacidad hotelera instalada (habitaciones y camas disponibles).
    - Tasa de ocupación mensual por región.
  - Configuración con `headers` y `User-Agent` estándar para evitar bloqueos.
  - Guardar crudo en `datos/datos_crudos_mincetur.xlsx` o `.csv`.
  - Registrar en `log_ejecucion.txt` las descargas correspondientes.

---

## FASE 3: Limpieza, Armonización y Generación del Dataset (Script 03)
- [ ] **Script `03_limpieza_datos.py`:**
  - Estandarización de nombres de regiones y creación de código de llave (`id_region`).
  - Creación de llave común temporal: `periodo` formato `YYYY-MM`.
  - Tratamiento de datos faltantes (*missing values*) y valores atípicos (*outliers* con winsorización al 1%-99% si aplica).
  - Unión (*inner join / left join*) entre datos turísticos regionales y variables macroeconómicas del BCRP.
  - Verificación del cumplimiento estricto: panel balanceado o semi-balanceado con $\ge 3\,000$ observaciones y mínimo 6 columnas (con $\ge 4$ sustantivas).
  - Exportación de `datos/datos_procesados_turismo.csv`.
  - Cálculo del hash **SHA-256** del archivo generado y guardado automático para el README.

---

## FASE 4: Modelación Financiera y Análisis de Sensibilidad (Script 04)
- [ ] **Script `04_analisis.py`:**
  - **Cálculo de Punto de Equilibrio:**
    - Determinación de la tasa de ocupación de equilibrio por región y por año.
    - Margen de seguridad operativo frente a la ocupación real registrada.
  - **Análisis de Sensibilidad:**
    - Simulación ante caídas de arribos de turistas (-10%, -20%, -30%).
    - Sensibilidad ante shocks en la tasa de interés / inflación o variaciones del PBI regional.
  - **Modelación Econométrica de Panel:**
    - Regresión con errores estándar agrupados por región (similar al modelo del compañero Renzo Ignacio Paucar):
      $$\text{TasaOcupacion}_{it} = \beta_0 + \beta_1 \ln(\text{Arribos}_{it}) + \beta_2 \text{PBI}_{it} + \beta_3 \text{IPC}_{it} + \varepsilon_{it}$$
  - **Generación de Entregables Visuales:**
    - Guardar en carpeta `salidas/` todas las tablas (`.csv` / `.tex`) y gráficos en alta resolución (`.png` a 300 DPI) para la exposición y el artículo.

---

## FASE 5: Documentación Final y Control de Calidad
- [ ] Redacción del `diccionario_variables.md` con URL exacta, unidad y fuente.
- [ ] Generación de `requirements.txt` con versiones congeladas (`pip freeze`).
- [ ] Redacción de `README.md` completo:
  - Instrucciones de clonación y ejecución paso a paso (`python scripts/01_...`).
  - Tabla de variables.
  - Hash SHA-256 verificado.
  - Enlace al repositorio de GitHub.
- [ ] Estructura de commits para Git (distribuidos en el tiempo según exige la rúbrica).
