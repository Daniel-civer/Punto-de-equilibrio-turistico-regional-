# DICCIONARIO DE VARIABLES
## Proyecto: Punto de Equilibrio y Sensibilidad en Proyectos Turísticos Regionales
**Curso:** Finanzas I (055D) — UNCP | Semestre 2026-II  
**Docente:** Dr. Ciro Iván Machacuay Meza  
**Archivo de Datos:** `datos/datos_procesados_turismo.csv`  

---

| Variable | Definición Operacional | Tipo de Variable | Unidad de Medida | Frecuencia | Fuente Exacta | Endpoint o URL de Origen |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id_region` | Código de Ubigeo oficial de 2 dígitos asignado al departamento o provincia constitucional. | Identificador | Numérico / Texto | Estática | INEI (Codificación Ubigeo) | `https://www.inei.gob.pe/` |
| `region` | Nombre oficial del departamento o región política evaluada (25 regiones del Perú). | Identificador | Texto | Estática | INEI / MINCETUR | `https://www.gob.pe/mincetur` |
| `periodo` | Periodo mensual de observación en formato ISO `YYYY-MM` (Llave común de integración). | Temporal | `AAAA-MM` | Mensual | Estándar ISO-8601 | Integración transversal |
| `anio` | Año cronológico de la observación (2013 a 2025). | Temporal | Años | Mensual | Parámetro temporal | N/A |
| `mes` | Mes de calendario de la observación (1 a 12). | Temporal | Número (1-12) | Mensual | Parámetro temporal | N/A |
| `arribos_nacionales` | Número de huéspedes nacionales registrados en establecimientos de hospedaje colectivo. | Sustantiva | Personas | Mensual | MINCETUR - Badatur | `https://www.gob.pe/mincetur` |
| `arribos_extranjeros` | Número de huéspedes no residentes (extranjeros) registrados en hospedajes. | Sustantiva | Personas | Mensual | MINCETUR - Badatur | `https://www.gob.pe/mincetur` |
| `arribos_totales` | Suma de arribos nacionales y extranjeros registrados en el mes y región. | Sustantiva | Personas | Mensual | MINCETUR / INEI | `https://www.gob.pe/mincetur` |
| `pernoctaciones_totales` | Total de noches pernoctadas por turistas en el departamento durante el mes. | Sustantiva | Pernoctaciones | Mensual | MINCETUR - Badatur | `https://www.gob.pe/mincetur` |
| `capacidad_habitaciones_mes` | Capacidad instalada mensual ofertada (habitaciones-noche disponibles). | Sustantiva | Habitaciones-noche | Mensual | MINCETUR - Capacidad hotelera | `https://www.gob.pe/mincetur` |
| `tasa_ocupacion_pct` | Porcentaje de habitaciones ocupadas sobre la capacidad instalada disponible mensual. | Sustantiva | Porcentaje (%) | Mensual | MINCETUR / Elaboración propia | `https://www.gob.pe/mincetur` |
| `bcrp_ipc_indice` | Índice de Precios al Consumidor (IPC Lima Metropolitana / Nacional, Base Dic.2021=100). | Sustantiva | Índice base | Mensual | BCRPData (Serie PN01270PM) | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01270PM/json/2013-1/2025-12` |
| `bcrp_tasa_referencia` | Tasa de interés de referencia de la política monetaria fijada por el BCRP. | Sustantiva | Porcentaje anual (%) | Mensual | BCRPData (Serie PN01288PM) | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01288PM/json/2013-1/2025-12` |
| `bcrp_pbi_indice` | Índice de Producción Nacional mensual (PBI mensual, Base 2007). | Sustantiva | Índice base | Mensual | BCRPData (Serie PN01770AM) | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01770AM/json/2013-1/2025-12` |
| `tarifa_adr_nominal` | Tarifa promedio diaria por habitación vendida (*Average Daily Rate*) en soles corrientes. | Sustantiva | Soles corrientes (S/) | Mensual | Calibración sectorial hotelera | MINCETUR / Cuentas Satélite |
| `tarifa_adr_real` | Tarifa promedio diaria deflactada por el IPC para expresar valor en soles constantes. | Sustantiva | Soles constantes (S/) | Mensual | Elaboración propia | Cálculo: `tarifa_adr_nominal / (ipc/100)` |
| `costo_var_unitario` | Costo variable directo por habitación noche ocupada (amenities, lavandería, suministros). | Sustantiva | Soles por noche (S/) | Mensual | Estructura de costos hotelera | Modelación financiera (28% ADR) |
| `margen_contribucion_unitario`| Margen de contribución unitario por habitación ($MCU = P - CV_u$). | Sustantiva | Soles por noche (S/) | Mensual | Modelo financiero | Cálculo: `ADR - CVu` |
| `costos_fijos_mensual` | Costos fijos operativos mensuales de operación, infraestructura, administración y personal base. | Sustantiva | Soles mensuales (S/) | Mensual | Modelo financiero | $CF = Q_{disp} \times 0.46 \times MCU$ |
| `q_equilibrio_habitaciones` | Cantidad física de habitaciones ocupadas necesarias al mes para cubrir costos totales ($CF/MCU$).| Sustantiva | Habitaciones-noche | Mensual | Modelo financiero | $Q_{eq} = CF / MCU$ |
| `tasa_ocupacion_equilibrio_pct`| Tasa porcentual mínima de ocupación hotelera para no incurrir en pérdidas operativas ($TO_{eq}$).| Sustantiva | Porcentaje (%) | Mensual | Modelo financiero | $TO_{eq} = (Q_{eq} / Q_{disp}) \times 100$ |
| `margen_seguridad_pct` | Margen de seguridad porcentual frente a shocks de caída en la ocupación ($MS$). | Sustantiva | Porcentaje (%) | Mensual | Modelo financiero | $MS = (TO_{real} - TO_{eq}) / TO_{real} \times 100$|
| `deficit_operativo_dummy` | Variable indicadora binaria: 1 si la ocupación observada fue inferior al umbral de equilibrio, 0 si cubrió costos. | Sustantiva | Binaria (0 ó 1) | Mensual | Modelo econométrico | Condicional: $I(TO_{real} < TO_{eq})$ |
