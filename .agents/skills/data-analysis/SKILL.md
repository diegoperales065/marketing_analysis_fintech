---
name: data-analysis
description: Skill para análisis cuantitativo profundo de datos tabulares. Cubre validación de calidad, estadísticas descriptivas avanzadas, segmentación, análisis de tendencias, derivación de insights accionables y generación de informes estructurados.
---

# 📈 Data Analysis — Análisis Cuantitativo de Datos

## Objetivo
Realizar análisis cuantitativo profundo del dataset bancario para extraer insights accionables que guíen tanto el modelado predictivo como las decisiones de negocio.

> **Diferenciación con otros skills:**
> - `data-cleaning` → Prepara y estandariza los datos (upstream)
> - `eda` → Explora distribuciones y relaciones visuales (descriptivo)
> - **`data-analysis`** → Cuantifica patrones, segmenta, analiza tendencias y genera informes (analítico)
> - `modeling` → Construye modelos predictivos (downstream)

---

## Cuándo Usar Este Skill

- **Análisis de segmentos**: Comparar conversión por perfil demográfico, financiero o de campaña
- **Análisis de tendencias**: Medir evolución temporal de métricas clave
- **Derivación de insights**: Generar conclusiones cuantitativas para el informe del TFM
- **Generación de informes**: Estructurar hallazgos en formato profesional
- **Validación de calidad**: Verificar integridad y consistencia antes del análisis

---

## Paso 1 — Carga y Exploración Inicial

```python
import pandas as pd
import numpy as np

# Cargar dataset bancario
df = pd.read_csv("datos/bank-additional_bank-additional-full.csv", sep=";")

# Inspección rápida
print(f"Registros: {df.shape[0]:,}")
print(f"Columnas: {df.shape[1]}")
print(f"Rango temporal: meses {df['month'].unique()}")

# Información de tipos y memoria
print(df.info(memory_usage="deep"))

# Primeras filas
df.head(10)
```

---

## Paso 2 — Validación de Calidad

```python
def reporte_calidad(df):
    """Genera un informe completo de calidad del dataset."""
    report = pd.DataFrame({
        "tipo": df.dtypes,
        "nulos": df.isnull().sum(),
        "pct_nulos": (df.isnull().mean() * 100).round(2),
        "unicos": df.nunique(),
        "duplicados": df.duplicated().sum()
    })
    print(f"\n{'='*60}")
    print(f"  INFORME DE CALIDAD — {df.shape[0]:,} registros, {df.shape[1]} columnas")
    print(f"{'='*60}")
    print(report.to_string())
    print(f"\nFilas duplicadas totales: {df.duplicated().sum()}")
    return report

quality = reporte_calidad(df)
```

### Verificación de valores especiales
```python
# Proporción de "unknown" en columnas categóricas
cols_con_unknown = ["credit_default", "has_housing_loan", "has_personal_loan",
                    "education_level", "job_type"]

for col in cols_con_unknown:
    pct = (df[col] == "unknown").mean() * 100
    estado = "⚠️" if pct > 5 else "✅"
    print(f"{estado} {col}: {pct:.1f}% unknown")

# Verificación de previously_contacted = 999
pct_999 = (df["previously_contacted"] == 999).mean() * 100
print(f"\n📊 previously_contacted = 999: {pct_999:.1f}% (no contactados previamente)")
```

---

## Paso 3 — Análisis Estadístico Avanzado

### Estadísticas descriptivas completas
```python
# Variables numéricas
num_cols = ["age", "call_duration", "contact_attempts", "previous_contacts",
            "employment_variation_rate", "consumer_price_index",
            "consumer_confidence_index", "euribor_3m_rate", "total_employment"]

# Descriptivas extendidas: media, mediana, desviación, asimetría, curtosis
stats = df[num_cols].describe().T
stats["median"] = df[num_cols].median()
stats["skew"] = df[num_cols].skew()
stats["kurtosis"] = df[num_cols].kurtosis()
stats = stats[["count", "mean", "median", "std", "min", "25%", "75%", "max", "skew", "kurtosis"]]
print(stats.round(3))
```

### Análisis agrupado por target
```python
# Estadísticas por grupo (subscribed: yes vs no)
grouped = df.groupby("subscribed")[num_cols].agg(["mean", "median", "std"])
print(grouped.round(3))

# Diferencia porcentual entre grupos
for col in num_cols:
    mean_yes = df[df["subscribed"] == "yes"][col].mean()
    mean_no = df[df["subscribed"] == "no"][col].mean()
    diff_pct = ((mean_yes - mean_no) / mean_no) * 100
    indicador = "↑" if diff_pct > 0 else "↓"
    print(f"{col}: {indicador} {abs(diff_pct):.1f}% (yes vs no)")
```

### Matriz de correlación
```python
import plotly.figure_factory as ff

corr = df[num_cols].corr().round(2)

fig = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    colorscale="RdBu_r",
    showscale=True
)
fig.update_layout(
    title="Matriz de Correlación — Variables Numéricas",
    width=900, height=700
)
fig.show()
```

### Tablas pivot
```python
# Tabla pivot: tasa de conversión por mes y método de contacto
pivot = pd.pivot_table(
    df,
    values="subscribed",
    index="contact_month",
    columns="contact_method",
    aggfunc=lambda x: (x == "yes").mean() * 100
).round(2)

print("Tasa de conversión (%) por mes y método de contacto:")
print(pivot)
```

---

## Paso 4 — Visualización Analítica

> **Convención del proyecto**: usar Plotly para consistencia con los skills `eda` y `modeling`.

### Distribuciones con análisis de normalidad
```python
import plotly.express as px
from scipy import stats as sp_stats

for col in num_cols:
    # Test de normalidad (Shapiro para muestras, D'Agostino para dataset completo)
    stat, p_value = sp_stats.normaltest(df[col].dropna())
    normality = "Normal" if p_value > 0.05 else "No normal"

    fig = px.histogram(
        df, x=col, nbins=50,
        title=f"Distribución de {col} ({normality}, p={p_value:.4f})",
        marginal="box",
        color_discrete_sequence=["#636EFA"]
    )
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    fig.show()
```

### Análisis de conversión por segmento
```python
import plotly.graph_objects as go

cat_cols = ["job_type", "marital_status", "education_level",
            "contact_method", "contact_month", "previous_campaign_outcome"]

def analisis_conversion(df, columna):
    """Analiza la tasa de conversión por categorías de una columna."""
    tabla = df.groupby(columna)["subscribed"].agg(
        total="count",
        conversiones=lambda x: (x == "yes").sum()
    ).reset_index()
    tabla["tasa_conversion"] = (tabla["conversiones"] / tabla["total"] * 100).round(2)
    tabla = tabla.sort_values("tasa_conversion", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=tabla[columna], x=tabla["tasa_conversion"],
        orientation="h",
        text=[f"{v:.1f}% (n={n:,})" for v, n in zip(tabla["tasa_conversion"], tabla["total"])],
        textposition="outside",
        marker_color=tabla["tasa_conversion"],
        marker_colorscale="RdYlGn"
    ))
    fig.update_layout(
        title=f"Tasa de Conversión por {columna}",
        xaxis_title="Conversión (%)",
        yaxis_title=columna,
        plot_bgcolor="white",
        height=max(400, len(tabla) * 35)
    )
    fig.show()
    return tabla

# Ejecutar para cada variable categórica
for col in cat_cols:
    analisis_conversion(df, col)
```

### Mapa de calor: conversión cruzada
```python
# Heatmap de conversión: job_type × education_level
cross = pd.crosstab(
    df["job_type"], df["education_level"],
    values=(df["subscribed"] == "yes").astype(int),
    aggfunc="mean"
) * 100

fig = ff.create_annotated_heatmap(
    z=cross.values.round(1),
    x=list(cross.columns),
    y=list(cross.index),
    colorscale="YlGn",
    showscale=True
)
fig.update_layout(
    title="Tasa de Conversión (%) — Ocupación × Educación",
    width=900, height=600
)
fig.show()
```

---

## Paso 5 — Derivación de Insights

### Top/Bottom analysis
```python
# Top 10 segmentos con mayor conversión
def top_bottom_segmentos(df, columna, n=10):
    """Identifica los segmentos con mayor y menor conversión."""
    tabla = df.groupby(columna).agg(
        total=("subscribed", "count"),
        conversiones=("subscribed", lambda x: (x == "yes").sum())
    ).reset_index()
    tabla["tasa"] = (tabla["conversiones"] / tabla["total"] * 100).round(2)

    print(f"\n🏆 TOP {n} — {columna} (mayor conversión):")
    print(tabla.nlargest(n, "tasa")[[columna, "tasa", "total"]].to_string(index=False))

    print(f"\n⬇️ BOTTOM {n} — {columna} (menor conversión):")
    print(tabla.nsmallest(n, "tasa")[[columna, "tasa", "total"]].to_string(index=False))

    return tabla
```

### Análisis de tendencias temporales
```python
# Evolución mensual de la tasa de conversión
meses_orden = ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

monthly = df.groupby("contact_month").agg(
    total=("subscribed", "count"),
    conversiones=("subscribed", lambda x: (x == "yes").sum())
).reindex(meses_orden)
monthly["tasa"] = (monthly["conversiones"] / monthly["total"] * 100).round(2)
monthly["crecimiento"] = monthly["tasa"].pct_change() * 100

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly.index, y=monthly["tasa"],
    mode="lines+markers+text",
    text=[f"{v:.1f}%" for v in monthly["tasa"]],
    textposition="top center",
    line=dict(color="#636EFA", width=3),
    marker=dict(size=10)
))
fig.update_layout(
    title="Evolución Mensual de la Tasa de Conversión",
    xaxis_title="Mes", yaxis_title="Conversión (%)",
    plot_bgcolor="white", width=900, height=500
)
fig.show()
```

### Análisis de contexto macroeconómico
```python
macro_cols = ["employment_variation_rate", "consumer_price_index",
              "consumer_confidence_index", "euribor_3m_rate", "total_employment"]

# Correlación con tasa de conversión
df_temp = df.copy()
df_temp["subscribed_num"] = (df_temp["subscribed"] == "yes").astype(int)

for col in macro_cols:
    corr_val = df_temp["subscribed_num"].corr(df_temp[col])
    signo = "+" if corr_val > 0 else ""
    impacto = "FUERTE" if abs(corr_val) > 0.3 else "MODERADO" if abs(corr_val) > 0.1 else "DÉBIL"
    print(f"📊 {col}: r={signo}{corr_val:.3f} ({impacto})")
```

---

## Paso 6 — Generación de Informe

> Para plantillas detalladas de informes, ver [TEMPLATES.md](./resources/TEMPLATES.md).

### Estructura del informe de análisis
```markdown
# Informe de Análisis de Datos — Campaña de Marketing Bancario

## 1. Resumen del Dataset
- **Registros**: X,XXX
- **Variables**: XX (demográficas, financieras, campaña, macro)
- **Target**: subscribed (yes/no)
- **Tasa de conversión global**: X.XX%

## 2. Hallazgos Clave
- Hallazgo 1: [cuantificado con métrica]
- Hallazgo 2: [cuantificado con métrica]
- Hallazgo 3: [cuantificado con métrica]

## 3. Resumen Estadístico
| Variable | Media | Mediana | Desv. Est. | Asimetría |
|:---------|:------|:--------|:-----------|:----------|
| age      | X.XX  | X.XX    | X.XX       | X.XX      |
| ...      | ...   | ...     | ...        | ...       |

## 4. Análisis de Segmentos
- Segmentos con mayor conversión: [top 3]
- Segmentos con menor conversión: [bottom 3]
- Variables macroeconómicas más influyentes: [top 2]

## 5. Recomendaciones
1. [Recomendación basada en datos]
2. [Recomendación basada en datos]
```

---

## Mejores Prácticas

1. **Primero entender, luego analizar**: Estudiar la estructura y el significado del dataset antes de computar métricas
2. **Análisis incremental**: Ir de lo simple a lo complejo — descriptivas → agrupadas → cruzadas → temporales
3. **Cuantificar todo**: Cada insight debe ir acompañado de una métrica (%, correlación, conteo)
4. **Visualizar con propósito**: Cada gráfico debe responder una pregunta específica del análisis
5. **Reproducibilidad**: Documentar cada paso del análisis con código completo y comentarios
6. **Preservar datos originales**: Trabajar siempre sobre copias, nunca modificar el CSV fuente
7. **Validar supuestos**: Verificar normalidad, independencia y homogeneidad antes de interpretar

---

## Restricciones

### Reglas obligatorias (DEBE)
1. Preservar los datos en bruto (trabajar sobre copia)
2. Documentar el proceso de análisis completo
3. Validar resultados contra el diccionario de datos del README
4. Usar nombres de columnas del proyecto (ver README)

### Prohibido (NO DEBE)
1. No exponer datos personales sensibles
2. No extraer conclusiones sin respaldo cuantitativo
3. No modificar el CSV fuente directamente
4. No usar Matplotlib puro (usar Plotly para consistencia)

---

## Referencias

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Python](https://plotly.com/python/)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Plantillas de informes](./resources/TEMPLATES.md)
- [Referencia técnica avanzada](./resources/REFERENCE.md)
