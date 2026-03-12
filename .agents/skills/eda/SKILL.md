---
name: eda
description: Skill para Análisis Exploratorio de Datos (EDA) avanzado. Incluye análisis univariado, bivariado, correlaciones, visualizaciones interactivas con Plotly/Seaborn, y análisis de la variable target (desbalance de clases).
---

# 📊 EDA — Análisis Exploratorio de Datos

## Objetivo
Comprender la distribución, relaciones y patrones del dataset bancario antes del modelado predictivo.

---

## 1. Análisis Univariado

### Variables numéricas
```python
import plotly.express as px
import pandas as pd

num_cols = ["age", "call_duration", "contact_attempts", "previous_contacts",
            "employment_variation_rate", "consumer_price_index",
            "consumer_confidence_index", "euribor_3m_rate", "total_employment"]

for col in num_cols:
    fig = px.histogram(df, x=col, nbins=50, title=f"Distribución de {col}",
                       marginal="box", color_discrete_sequence=["#636EFA"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    fig.show()
```

### Variables categóricas
```python
cat_cols = ["job_type", "marital_status", "education_level",
            "credit_default", "has_housing_loan", "has_personal_loan",
            "contact_method", "contact_month", "contact_day",
            "previous_campaign_outcome"]

for col in cat_cols:
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, "count"]
    fig = px.bar(counts, x=col, y="count", title=f"Frecuencia de {col}",
                 color_discrete_sequence=["#EF553B"])
    fig.update_layout(plot_bgcolor="white", xaxis_tickangle=-45)
    fig.show()
```

---

## 2. Análisis de la Variable Target

### Distribución del target (desbalance de clases)
```python
target_dist = df["subscribed"].value_counts(normalize=True).reset_index()
target_dist.columns = ["subscribed", "proportion"]

fig = px.pie(target_dist, values="proportion", names="subscribed",
             title="Distribución de la variable target (subscribed)",
             color_discrete_sequence=["#EF553B", "#00CC96"],
             hole=0.4)
fig.show()

# Tasa de conversión
conversion = (df["subscribed"] == "yes").mean() * 100
print(f"Tasa de conversión global: {conversion:.2f}%")
```

### Tasa de conversión por segmento
```python
def tasa_conversion_por(df, columna):
    tabla = df.groupby(columna)["subscribed"].apply(
        lambda x: (x == "yes").mean() * 100
    ).reset_index()
    tabla.columns = [columna, "conversion_rate"]
    tabla = tabla.sort_values("conversion_rate", ascending=False)
    
    fig = px.bar(tabla, x=columna, y="conversion_rate",
                 title=f"Tasa de conversión por {columna} (%)",
                 color="conversion_rate",
                 color_continuous_scale="RdYlGn")
    fig.update_layout(plot_bgcolor="white", xaxis_tickangle=-45)
    fig.show()
    return tabla
```

---

## 3. Análisis Bivariado

### Numéricas vs Target (boxplots)
```python
for col in num_cols:
    fig = px.box(df, x="subscribed", y=col, color="subscribed",
                 title=f"{col} por subscribed",
                 color_discrete_sequence=["#EF553B", "#00CC96"])
    fig.update_layout(plot_bgcolor="white")
    fig.show()
```

### Categóricas vs Target (stacked bars)
```python
for col in cat_cols:
    ct = pd.crosstab(df[col], df["subscribed"], normalize="index") * 100
    ct = ct.reset_index().melt(id_vars=col)
    fig = px.bar(ct, x=col, y="value", color="subscribed",
                 title=f"{col} vs subscribed (%)",
                 barmode="stack",
                 color_discrete_sequence=["#EF553B", "#00CC96"])
    fig.update_layout(plot_bgcolor="white", yaxis_title="Porcentaje (%)")
    fig.show()
```

---

## 4. Correlaciones

### Heatmap de correlaciones
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
fig.update_layout(title="Matriz de Correlación", width=900, height=700)
fig.show()
```

---

## 5. Análisis de Variables Macroeconómicas

```python
macro_cols = ["employment_variation_rate", "consumer_price_index",
              "consumer_confidence_index", "euribor_3m_rate", "total_employment"]

for col in macro_cols:
    fig = px.violin(df, x="subscribed", y=col, color="subscribed",
                    box=True, points="outliers",
                    title=f"{col} por resultado de campaña",
                    color_discrete_sequence=["#EF553B", "#00CC96"])
    fig.update_layout(plot_bgcolor="white")
    fig.show()
```

---

## 6. Estadísticas Descriptivas Completas

```python
# Resumen general
print(df.describe(include="all").T)

# Estadísticas por grupo target
print(df.groupby("subscribed").describe().T)
```
