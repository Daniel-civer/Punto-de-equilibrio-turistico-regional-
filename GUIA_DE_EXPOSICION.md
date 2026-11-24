# GUÍA DE EXPOSICIÓN Y DEFENSA DEL ARTÍCULO
## Curso: Finanzas I (055D) — UNCP | Cátedra: Dr. Ciro Iván Machacuay Meza
**Tema:** Punto de equilibrio y sensibilidad en un proyecto turístico regional  
**Expositores:** Daniel Ricardo Sulca Castro 

**Código de Matrícula:** 2024200532L (e_2024200532L@uncp.edu.pe)  
**Tiempo estimado:** 8 a 10 minutos + ronda de preguntas  

---

## ESTRUCTURA DE DIAPOSITIVAS (10 Diapositivas según Plantilla Oficial)

### Diapositiva 1: Portada
* **Título:** Punto de equilibrio operativo y análisis de sensibilidad en proyectos hoteleros departamentales: Un enfoque de datos de panel en el Perú, 2013–2025.
* **Autores:** Daniel Ricardo Sulca Castro & Coautor (2024200532L)
* **Institución:** Facultad de Economía · Universidad Nacional del Centro del Perú · Huancayo, 2026.
* **Docente:** Dr. Ciro Iván Machacuay Meza.
* **Guion de presentación:**  
  > *"Buenas tardes, estimado doctor Machacuay y compañeros. Hoy presentamos nuestra investigación sobre la viabilidad y sensibilidad financiera de la capacidad hotelera en las 25 regiones del Perú, analizando el periodo mensual 2013 a 2025."*

---

### Diapositiva 2: Introducción y Pregunta de Investigación
* **Contexto:**
  * El sector hotelero tiene un **alto apalancamiento operativo** (muchos costos fijos: infraestructura, planillas base, licencias).
  * Entre 2013 y 2025 enfrentó ciclos extremos: estabilidad inicial, el shock devastador de la pandemia de COVID-19, y la subida de tasas del BCRP de 0.25% a 7.75%.
* **Pregunta de Investigación:**  
  *¿Cuál es la tasa de ocupación mínima para no quebrar (punto de equilibrio) en cada departamento del Perú, y qué tan sensible es la rentabilidad ante caídas en los arribos turísticos?*
* **Objetivo:** Comparar el punto de equilibrio regional y modelar la elasticidad ante shocks turísticos y macroeconómicos.
* **Hipótesis:** Las regiones con mayor dependencia del turismo receptivo requieren tarifas superiores y sufren una mayor volatilidad en su margen de seguridad.

---

### Diapositiva 3: Marco Teórico y Literatura
* **Fórmulas clave:**
  1. **Habitaciones de Equilibrio:**  
     $$Q_{eq} = \frac{CF}{P - CV_u} = \frac{CF}{MCU}$$
  2. **Tasa de Ocupación Crítica ($TO_{eq}$):**  
     $$TO_{eq} (\%) = \frac{Q_{eq}}{\text{Capacidad Disponible}} \times 100$$
  3. **Margen de Seguridad Financiero ($MS$):**  
     $$MS = \frac{TO_{real} - TO_{eq}}{TO_{real}} \times 100$$
* **Literatura:**
  * Brealey, Myers & Allen (2020): Teoría del apalancamiento operativo.
  * Emin et al. (2025) y Tran et al. (2024): Transmisión monetaria y sensibilidad de la demanda de servicios.

---

### Diapositiva 4: Datos y Metodología (Las Dos Vías Obligatorias)
* **Vía 1 (API REST):**
  * BCRPData: IPC Lima (deflactor de tarifas), Tasa de Referencia del BCRP y PBI mensual (`PN01270PM`, `PN01288PM`, `PN01770AM`).
  * Banco Mundial WDI: Arribos de turistas internacionales (`ST.INT.ARVL`).
* **Vía 2 (Descarga Programática / Web):**
  * MINCETUR / INEI: Arribos nacionales, extranjeros, pernoctaciones y habitaciones disponibles por región.
* **Panel Construido:**
  * 25 regiones $\times$ 156 meses = **4,225 observaciones** (supera con creces el mínimo de 3,000 exigido).
  * Llave común: `periodo (YYYY-MM)` + `id_region (Ubigeo)`.
* **Modelo Econométrico:** MCO con errores estándar agrupados por departamento (*Clustered Standard Errors*).

---

### Diapositiva 5: Demostración en Vivo de la Extracción y Reproducibilidad
* **Los 4 scripts ejecutados en orden:**
  1. `01_extraccion_api.py`: Consume APIs del BCRP y Banco Mundial (HTTP 200) $\rightarrow$ `datos_crudos_api.json`.
  2. `02_scraping_web.py`: Descarga programática de MINCETUR $\rightarrow$ `datos_crudos_mincetur.csv`.
  3. `03_limpieza_datos.py`: Merge, tratamiento de outliers y cálculo de hash SHA-256 $\rightarrow$ `datos_procesados_turismo.csv`.
  4. `04_analisis.py`: Regresión de panel y salidas gráficas a 300 DPI en `/salidas`.
* **Hash SHA-256 verificado en vivo:**  
  `bac6f8cc791b98ea7f84cacd00b513d4d8042dcc7f62fb94cd396ce327e0106a`
* **Dashboard Interactivo:** Demostración visual opcional en `http://localhost:5000`.

---

### Diapositiva 6: Resultado 1 — Evolución de la Tasa de Ocupación vs Equilibrio
* **Mostrar Figura 1 (`figura1_evolucion_ocupacion_equilibrio.png`):**
  * Tasa de ocupación promedio observada: **48.2%**.
  * Punto de equilibrio crítico medio: **46.0%**.
  * **Margen de seguridad promedio:** **+4.8%**.
  * **El quiebre del COVID-19:** En abril de 2020 la ocupación colapsó a 18%, llevando al 100% de los hoteles a operar en déficit operativo durante casi dos años.

---

### Diapositiva 7: Resultado 2 — Ranking Departamental de Margen de Seguridad
* **Mostrar Figura 3 y Tabla 2:**
  * **Regiones con holgura financiera ($MS > 15\%$):** Cusco (+25.1%), Lima (+23.1%), Arequipa (+15.1%). Tienen ocupaciones medias superiores al 55% y alta afluencia de turistas extranjeros y corporativos.
  * **Regiones vulnerables ($MS < 0$):** Pasco (-19.8%), Apurímac (-27.1%), Huancavelica (-43.3%). Operan con ocupaciones medias menores al 38%, por debajo de su punto de equilibrio.
* **Mensaje clave:** *La rentabilidad de un proyecto hotelero no depende solo de construir el hotel, sino de la densidad y estacionalidad del flujo de su región.*

---

### Diapositiva 8: Resultado 3 — Modelo Econométrico de Sensibilidad
* **Mostrar Tabla 3 (`tabla3_modelo_sensibilidad.csv`):**
  * $R^2 = 0.6172$ (El modelo explica el 61.7% de la varianza de la ocupación hotelera).
  * **Elasticidad de Arribos ($\beta_1 = +8.14$, $p < 0.01$):** Por cada 10% que crecen los arribos, la tasa de ocupación sube 0.81 puntos porcentuales.
  * **PBI Nacional ($\beta_2 = +0.12$, $p < 0.01$):** El sector es netamente procíclico.
  * **Tasa del BCRP ($\beta_3 = -0.34$, $p < 0.05$):** Tasas de interés altas encarecen el financiamiento y deprimen la afluencia turística.

---

### Diapositiva 9: Discusión y Conclusiones Financieras
1. **Punto de equilibrio sectorial:** Se ubica en el 46.0% de ocupación de las habitaciones disponibles.
2. **Alta sensibilidad ante caídas de demanda:** Una caída del 20% en los arribos turísticos pone en insolvencia operativa a 14 de los 25 departamentos.
3. **Recomendación para inversionistas:** No proyectar ocupaciones lineales; en departamentos de sierra y selva con alta estacionalidad, se deben negociar costos fijos variables o tercerizados para bajar el $TO_{eq}$ por debajo del 35%.

---

### Diapositiva 10: Referencias y Repositorio GitHub
* Código QR hacia el repositorio: `https://github.com/Adat13/finanzas-punto-equilibrio-turismo-regional`
* Cumplimiento estricto de los 3 commits en fechas distintas y hash SHA-256 verificado.

---

## BANCO DE PREGUNTAS DEL DOCENTE (¿Qué responder si pregunta el Dr. Machacuay?)

**Pregunta 1: ¿Por qué usaron errores estándar agrupados (Clustered Errors) por departamento?**  
* *Respuesta:* *"Porque dentro de un mismo departamento, las observaciones mensuales sucesivas están correlacionadas en el tiempo (autocorrelación y heterocedasticidad regional). Agrupar por cluster regional corrige los errores estándar y evita inflar falsamente la significancia estadística de los coeficientes."*

**Pregunta 2: ¿Cómo garantizan que la extracción de datos es reproducible si las fuentes de internet cambian?**  
* *Respuesta:* *"Cumpliendo el numeral 2.4.5 de la consigna: congelamos la fecha de consulta mediante constantes fijas (`FECHA_INICIO = 2013-1` y `FECHA_CORTE = 2025-12`), guardamos los datos crudos originales sin tocar en `datos/` y certificamos la base con el hash SHA-256 (`bac6f8cc...`). Al reejecutar el script en otra máquina, se genera exactamente el mismo archivo."*

**Pregunta 3: ¿Qué diferencia hay entre la ocupación de equilibrio y el margen de seguridad?**  
* *Respuesta:* *"La ocupación de equilibrio ($TO_{eq}$) es el porcentaje mínimo de habitaciones que se deben llenar al mes para que la utilidad operativa sea cero ($IT = CT$). El margen de seguridad ($MS$) mide la distancia porcentual entre lo que realmente se llena y ese punto crítico. Si el margen de seguridad es +25%, significa que los arribos pueden caer hasta un 25% antes de que el hotel empiece a perder plata."*
