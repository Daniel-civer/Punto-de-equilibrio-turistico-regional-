# ESPECIFICACIONES TÉCNICAS Y METODOLÓGICAS DEL PROYECTO
## Curso: Finanzas I (055D) — UNCP | Semestre 2026-II
**Docente:** Dr. Ciro Iván Machacuay Meza  
**Tema Asignado:** Punto de equilibrio y sensibilidad en un proyecto turístico regional  

---

## 1. TÍTULO Y PLANTEAMIENTO DEL PROBLEMA

### 1.1 Título sugerido para el artículo / póster
> **"Punto de equilibrio operativo y análisis de sensibilidad en proyectos hoteleros departamentales: Un enfoque de datos de panel en el Perú, 2013–2025"**

### 1.2 Pregunta de investigación
*¿Cuál es el nivel crítico de ocupación turística (punto de equilibrio) requerido por proyectos hoteleros a nivel departamental en el Perú, y qué tan sensible es dicho equilibrio ante variaciones exógenas en la demanda turística, el PBI regional y la inflación entre 2013 y 2025?*

### 1.3 Objetivo general
Determinar empíricamente el punto de equilibrio operativo para la capacidad hotelera instalada en los 25 departamentos del Perú y evaluar la sensibilidad financiera de los proyectos hoteleros frente a shocks en los arribos de turistas y variables macroeconómicas.

### 1.4 Hipótesis
1. **$H_1$ (Punto de Equilibrio):** Las regiones con mayor estacionalidad turística requieren una tarifa media diaria (ADR) significativamente mayor o una menor estructura de costos fijos para que su tasa de ocupación de equilibrio no supere la ocupación media histórica observada.
2. **$H_2$ (Sensibilidad y Elasticidad):** La probabilidad de operar por debajo del punto de equilibrio es altamente sensible a la contracción del PBI departamental y a la desaceleración del turismo receptivo frente al turismo interno.

---

## 2. MARCO TEÓRICO Y FINANCIERO

### 2.1 Modelo Financiero: Punto de Equilibrio Hotelero
Para un proyecto hotelero representativo con capacidad disponible de habitaciones-noche por mes ($Q_{disponible}$):

1. **Ingresos Totales ($IT$):**
   $$IT = Q_{ocupadas} \times P$$
   Donde $P$ es la tarifa promedio diaria por habitación (*Average Daily Rate* - ADR) y $Q_{ocupadas} = Q_{disponible} \times \text{Tasa de Ocupación (\%)} $.

2. **Costos Totales ($CT$):**
   $$CT = CF + (CV_u \times Q_{ocupadas})$$
   Donde $CF$ son los costos fijos de operación e infraestructura, y $CV_u$ es el costo variable por habitación noche ocupada (limpieza, suministros, servicios).

3. **Tasa de Ocupación de Equilibrio ($TO_{eq}$):**
   El punto de equilibrio en habitaciones ocupadas ($Q_{eq}$) es:
   $$Q_{eq} = \frac{CF}{P - CV_u} = \frac{CF}{\text{Margen de Contribución Unitario}}$$
   
   En términos porcentuales de capacidad:
   $$TO_{eq} (\%) = \frac{Q_{eq}}{Q_{disponible}} \times 100$$

4. **Margen de Seguridad Financiero ($MS$):**
   $$MS = \frac{\text{Tasa de Ocupación Real} - TO_{eq}}{\text{Tasa de Ocupación Real}}$$

---

## 3. ARQUITECTURA DE DATOS Y FUENTES

Cumpliendo con la rúbrica de la **Unidad II** (dos vías obligatorias, panel $\ge 3\,000$ observaciones, mínimo 4 variables sustantivas):

| Elemento | Especificación |
| :--- | :--- |
| **Cobertura Temporal** | Enero 2013 a Diciembre 2025 (mensual, 156 meses). |
| **Cobertura Geográfica** | 25 departamentos del Perú (24 departamentos + Provincia Constitucional del Callao / Lima Provincias según armonización). |
| **Tamaño Estimado** | $25 \text{ regiones} \times 156 \text{ meses} = 3\,900 \text{ observaciones}$ (supera ampliamente la exigencia de $\ge 3\,000$ obs). |
| **Llave Común de Unión** | `id_region` (código de departamento / ubigeo 2 dígitos) + `periodo` (`YYYY-MM`). |

### 3.1 VÍA 1: Consumo de API Programática
* **Fuente Primaria:** **BCRPData (API oficial del BCRP)**
  * *Endpoint:* `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{codigos}/json/{inicio}/{fin}`
  * *Variables a extraer:*
    1. Índice de Precios al Consumidor (IPC nacional / regional) para deflactar ingresos y costos.
    2. Actividad económica mensual o PBI mensual / trimestralizado departamental.
    3. Tasa de interés de referencia del BCRP (como costo de oportunidad del capital).
* **Fuente Complementaria:** **Banco Mundial WDI API**
  * *Endpoint:* `https://api.worldbank.org/v2/country/PER/indicator/{indicador}?format=json`
  * *Variable:* Gastos en turismo internacional / llegadas turísticas anuales de referencia.

### 3.2 VÍA 2: Descarga Programática / Scraping
* **Fuente Primaria:** **MINCETUR / BADATUR / INEI (Estadísticas de Turismo)**
  * *Mecanismo:* Descarga automatizada vía script Python (`requests` + parsing de hojas Excel con `openpyxl`/`pandas`).
  * *Archivos oficiales:* Cuadros estadísticos mensuales de arribos y capacidad hotelera por departamento.
  * *Variables a extraer:*
    1. **Arribos de huéspedes nacionales** (mensual por departamento).
    2. **Arribos de huéspedes extranjeros** (mensual por departamento).
    3. **Pernoctaciones totales** en establecimientos de hospedaje.
    4. **Número de habitaciones y camas disponibles** (capacidad ofertada mensual).
    5. **Tasa de ocupación de habitaciones (%)**.

---

## 4. DICCIONARIO DE VARIABLES PRELIMINAR

| Variable | Tipo | Unidad | Frecuencia | Fuente Exacta | Función en el Modelo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id_region` | Identificador | Categórica (2 dígitos) | Estática | INEI (Ubigeo) | Llave de cruce |
| `region` | Identificador | Texto | Estática | INEI / MINCETUR | Identificador |
| `periodo` | Fecha | `YYYY-MM` | Mensual | Estándar ISO | Llave temporal |
| `arribos_nacionales` | Sustantiva | Personas | Mensual | MINCETUR / INEI | Demanda turística interna |
| `arribos_extranjeros` | Sustantiva | Personas | Mensual | MINCETUR / INEI | Demanda turística externa |
| `capacidad_habitaciones` | Sustantiva | Habitaciones-noche | Mensual | MINCETUR | Oferta instalada ($Q_{disp}$) |
| `tasa_ocupacion` | Sustantiva | Porcentaje (%) | Mensual | MINCETUR / Cálculo | Variable dependiente / Base de equilibrio |
| `ipc_base2021` | Sustantiva | Índice | Mensual | BCRPData (API) | Control macroeconómico |
| `pbi_indice` | Sustantiva | Índice / Variación | Mensual | BCRPData (API) | Shocks de demanda agregada |
| `tarifa_adr_est` | Sustantiva | Soles constantes | Mensual | Estimación calibrada | Ingresos por habitación |
| `pe_ocupacion_critica`| Sustantiva calculada| Porcentaje (%) | Mensual | Modelo financiero | Umbral de rentabilidad |

---

## 5. ESTRUCTURA OBLIGATORIA DE ARCHIVOS (CARPETA N° 3)

Conforme a la rúbrica del profesor Iván Machacuay:

```text
trabajo_daniel/
├── .env.example                     # Plantilla de variables de entorno
├── .gitignore                       # Ignorar caches, virtualenvs y temporales
├── requirements.txt                 # Dependencias congeladas con versiones exactas
├── README.md                        # Documento principal (autor, hash SHA-256, orden de ejecución)
├── diccionario_variables.md         # Ficha técnica completa de cada variable
├── incidencias_fuente.md            # Registro técnico si hay fuentes caídas o cambios
├── log_ejecucion.txt                # Registro con fecha/hora, status HTTP y filas procesadas
│
├── datos/
│   ├── datos_crudos_api.csv         # Salida cruda de BCRPData / Banco Mundial (intacta)
│   ├── datos_crudos_mincetur.xlsx   # Descarga programática original de MINCETUR/INEI
│   └── datos_procesados_TEMA.csv    # Dataset final unificado y limpio
│
├── scripts/
│   ├── 01_extraccion_api.py         # Extracción de BCRP / Banco Mundial (Vía 1)
│   ├── 02_scraping_web.py           # Descarga programática de MINCETUR/INEI (Vía 2)
│   ├── 03_limpieza_datos.py         # Tratamiento, tipificación, merge y cálculo SHA-256
│   └── 04_analisis.py               # Punto de equilibrio, sensibilidad, tablas y gráficos
│
└── salidas/
    ├── tabla1_estadisticas_descriptivas.csv
    ├── tabla2_ranking_punto_equilibrio.csv
    ├── tabla3_modelo_sensibilidad.csv
    ├── figura1_evolucion_ocupacion_regional.png
    ├── figura2_sensibilidad_demanda_turismo.png
    └── figura3_mapa_vulnerabilidad_equilibrio.png
```

---

## 6. ESTÁNDARES DE CALIDAD Y REPRODUCIBILIDAD (2.4.4 Y 2.4.5)

1. **Rutas 100% Relativas:** Uso estricto de la librería `pathlib.Path` de Python para que funcione en cualquier PC sin rutas absolutas (`C:\Users\...`).
2. **Congelamiento de Parámetros:** 
   ```python
   FECHA_INICIO = "2013-01-01"
   FECHA_CORTE = "2025-12-31"
   ```
3. **Código comentado en español:** Explicación funcional paso a paso en cada bloque.
4. **Verificación de Integridad:** El script `03_limpieza_datos.py` calculará e imprimirá el hash **SHA-256** del archivo final `datos_procesados_*.csv` para consignarlo en el `README.md`.
5. **Estrategia de Commits en Git:** Se planificarán al menos 4 commits en fechas/etapas diferenciadas (ej. Commit 1: Arquitectura y scripts de extracción; Commit 2: Limpieza y generación del dataset procesado; Commit 3: Análisis financiero y econométrico; Commit 4: README, salidas y documentación final).
