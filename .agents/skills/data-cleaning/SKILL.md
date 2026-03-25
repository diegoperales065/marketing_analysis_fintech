---
name: data-cleaning
description: Skill para limpieza, transformación y preparación de datos tabulares. Cubre tratamiento de nulos, outliers, renombrado de columnas, casting de tipos, y validación de integridad del dataset.
---

# 🧹 Data Cleaning — Limpieza y Preparación de Datos

## Objetivo
Estandarizar y limpiar el dataset bancario para garantizar calidad de datos antes del análisis y modelado.

---

## Paso 1 — Carga del dataset

```python
import pandas as pd

df = pd.read_csv("datos/bank-additional_bank-additional-full.csv", sep=";")
print(f"Shape: {df.shape}")
print(f"Columnas: {list(df.columns)}")
```

---

## Paso 2 — Renombrado de columnas

Mapeo de columnas originales → nombres descriptivos definidos en el README:

```python
column_mapping = {
    "age": "age",
    "job": "job_type",
    "marital": "marital_status",
    "education": "education_level",
    "default": "credit_default",
    "housing": "has_housing_loan",
    "loan": "has_personal_loan",
    "contact": "contact_method",
    "month": "contact_month",
    "day_of_week": "contact_day",
    "duration": "call_duration",
    "campaign": "contact_attempts",
    "pdays": "previously_contacted",
    "previous": "previous_contacts",
    "poutcome": "previous_campaign_outcome",
    "emp.var.rate": "employment_variation_rate",
    "cons.price.idx": "consumer_price_index",
    "cons.conf.idx": "consumer_confidence_index",
    "euribor3m": "euribor_3m_rate",
    "nr.employed": "total_employment",
    "y": "subscribed",
}

df.rename(columns=column_mapping, inplace=True)
```

---

## Paso 3 — Tratamiento de valores "unknown"

Las columnas `credit_default`, `has_housing_loan`, `has_personal_loan`, `education_level` y `job_type` contienen `"unknown"` como valor.

### Estrategias:
| Estrategia | Cuándo usarla |
|:---|:---|
| Mantener como categoría propia | Si `"unknown"` tiene significado semántico |
| Imputar con la moda | Si son pocos casos y no aportan info |
| Crear flag `_is_unknown` | Si la ausencia de info puede ser predictiva |

```python
# Verificar proporción de unknowns
for col in ["credit_default", "has_housing_loan", "has_personal_loan", "education_level", "job_type"]:
    pct = (df[col] == "unknown").mean() * 100
    print(f"{col}: {pct:.1f}% unknown")
```

---

## Paso 4 — Tratamiento de `previously_contacted = 999`

El valor `999` indica que el cliente **nunca fue contactado** en campañas anteriores.

```python
# Opción A: Crear flag binaria
df["is_new_campaign_client"] = (df["previously_contacted"] == 999).astype(int)

# Opción B: Reemplazar 999 por 0 o NaN según análisis
# df["previously_contacted"] = df["previously_contacted"].replace(999, 0)
```

---

## Paso 5 — Detección y tratamiento de outliers

```python
import numpy as np

def detect_outliers_iqr(series, k=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - k * IQR
    upper = Q3 + k * IQR
    return (series < lower) | (series > upper)

# Aplicar a variables numéricas clave
for col in ["age", "call_duration", "contact_attempts"]:
    outliers = detect_outliers_iqr(df[col])
    print(f"{col}: {outliers.sum()} outliers ({outliers.mean()*100:.1f}%)")
```

---

## Paso 6 — Casting de tipos

```python
# Variables categóricas explícitas
cat_cols = [
    "job_type", "marital_status", "education_level",
    "credit_default", "has_housing_loan", "has_personal_loan",
    "contact_method", "contact_month", "contact_day",
    "previous_campaign_outcome", "subscribed"
]

for col in cat_cols:
    df[col] = df[col].astype("category")
```

---

## Paso 7 — Validación final

```python
# Verificar que no hay nulos
assert df.isnull().sum().sum() == 0, "¡Hay valores nulos!"

# Verificar types
print(df.dtypes)

# Shape final
print(f"Dataset limpio: {df.shape}")
```

---

## Variables derivadas

```python
# is_new_campaign_client: ¿es la primera campaña para este cliente?
df["is_new_campaign_client"] = (df["previously_contacted"] == 999).astype(int)

# high_contact_attempts: ¿se contactó al cliente más de 3 veces?
df["high_contact_attempts"] = (df["contact_attempts"] > 3).astype(int)
```
