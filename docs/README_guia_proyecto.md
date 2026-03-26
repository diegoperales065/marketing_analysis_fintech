# 🏦 Proyecto Marketing Analytics para Empresa Fintech

> **Fuente**: `2_marketing_fintech_guía_proyecto.docx.pdf` — Nuclio Digital School  
> **Tipo**: Guía de Proyecto — Trabajo Final de Máster (TFM)  
> **Duplicado legible** generado el 14 de marzo de 2026

---

## 📌 Descripción del Proyecto

Análisis de los datos de campañas de marketing de una empresa Fintech para conseguir **identificar patrones, tendencias y factores** que influyen en que un cliente acabe contratando un **depósito a plazo**.

Tras un análisis exhaustivo de todos sus datos, habrá que:

1. **Implementar un modelo simple** que ayude a entender y predecir la efectividad de las campañas de marketing.
2. **Diseñar un dashboard** para la capa ejecutiva de la fintech con los principales insights y KPIs de los resultados de las campañas.

---

## 📋 Tareas

### Tarea 1 — Análisis de Datos

| Sub-tarea | Descripción |
|:----------|:------------|
| **1.1** Entendimiento de datos | Datos de clientes, detalles de las campañas y sus resultados |
| **1.2** Estadísticas descriptivas | Entender las características básicas de los datos |
| **1.3** Relación demográfica–suscripción | Analizar cómo edad, trabajo y educación se relacionan con la suscripción al depósito a plazo |
| **1.4** Impacto de la campaña | Evaluar cómo el número de contactos, mes y día de la semana afectan al resultado |

### Tarea 2 — Análisis de la Respuesta de la Campaña

| Sub-tarea | Descripción |
|:----------|:------------|
| **2.1** Comparación de tasas de éxito | Entre diferentes tipos/perfiles de clientes |
| **2.2** Indicadores de éxito | Evaluar posibles indicadores como la **duración de la llamada** |

### Tarea 3 — Modelado Predictivo Simple

| Sub-tarea | Descripción |
|:----------|:------------|
| **3.1** Regresión logística | Construir un modelo simple para predecir la probabilidad de suscripción a un depósito a plazo, basado en variables seleccionadas. Puede implementarse en Python, BigQueryML, ChatGPT u otra herramienta |
| **3.2** Evaluación del modelo | Utilizar métricas básicas: **precisión**, **sensibilidad** y **especificidad**. Requiere familiarización previa con estas métricas |

### Tarea 4 — Visualización de Datos y Creación de Dashboards

| Sub-tarea | Descripción |
|:----------|:------------|
| **4.1** Dashboard interactivo | Diseño e implementación con herramienta de visualización libre (Looker, Tableau, etc.) |
| **4.2** Tendencias temporales | Visualizaciones que destaquen la efectividad de la campaña a lo largo del tiempo |
| **4.3** Distribuciones y KPIs | Gráficos de variables clave y principales KPIs |

### Tarea 5 — Interpretación y Recomendaciones

| Sub-tarea | Descripción |
|:----------|:------------|
| **5.1** Patrones y factores clave | Identificar los que contribuyen al éxito de las campañas de marketing |
| **5.2** Recomendaciones estratégicas | Formular recomendaciones para mejorar la efectividad de futuras campañas |

---

## 📦 Entregables

| # | Entregable | Detalle |
|:-:|:-----------|:--------|
| 1 | **Documento técnico** | Memoria de proyecto con metodología y resultados |
| 2 | **Código y notebooks** | Entregables solicitados para cada tarea + dashboard |
| 3 | **Presentación final** | Presentación para la junta ejecutiva de la fintech |

---

## 📊 Cálculo de la Nota

| Componente | Peso |
|:-----------|:----:|
| **Proceso de elaboración y memoria** | **70%** |
| **Defensa del trabajo** | **30%** |

---

## 📁 Contexto Sobre los Datos

> **Periodo**: Las campañas de marketing se basan en llamadas telefónicas que tuvieron lugar de **Mayo 2018** a **Noviembre 2020**.

> [!IMPORTANT]
> Los registros vienen ordenados por fecha, pero **no hay una variable disponible con la fecha completa** en el dataset original.

> [!NOTE]
> Es posible que en algunos casos se requiera de **más de un contacto** con el mismo cliente para determinar si el depósito acaba siendo contratado (`sí`) o no (`no`).

---

## 🗂️ Referencia Rápida del Dataset

**Archivo:** `datos/bank-additional_bank-additional-full.csv`  
**Registros:** 41.188 filas | **Variables:** 21 columnas | **Separador:** `;`

| Variable | Tipo | Descripción |
|:---------|:----:|:------------|
| `age` | numérica | Edad del cliente |
| `job` | categórica | Tipo de ocupación |
| `marital` | categórica | Estado civil |
| `education` | categórica | Nivel educativo |
| `default` | categórica | ¿Tiene crédito en incumplimiento? |
| `housing` | categórica | ¿Tiene hipoteca? |
| `loan` | categórica | ¿Tiene préstamo personal? |
| `contact` | categórica | Método de contacto (celular/fijo) |
| `month` | categórica | Mes del último contacto |
| `day_of_week` | categórica | Día de la semana del último contacto |
| `duration` | numérica | Duración de la llamada (segundos) |
| `campaign` | numérica | Nº de contactos en esta campaña |
| `pdays` | numérica | Días desde último contacto previo (999 = nunca) |
| `previous` | numérica | Nº de contactos antes de esta campaña |
| `poutcome` | categórica | Resultado de campaña anterior |
| `emp.var.rate` | numérica | Tasa de variación del empleo |
| `cons.price.idx` | numérica | Índice de precios al consumidor |
| `cons.conf.idx` | numérica | Índice de confianza del consumidor |
| `euribor3m` | numérica | Euribor a 3 meses |
| `nr.employed` | numérica | Nº total de empleados (miles) |
| **`y`** | **binaria** | **Variable target: ¿contrató el depósito? (`yes`/`no`)** |

---

*Documento generado automáticamente como duplicado legible del PDF original de la guía del proyecto.*
