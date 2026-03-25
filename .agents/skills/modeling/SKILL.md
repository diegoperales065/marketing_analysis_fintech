---
name: modeling
description: Skill para modelado predictivo en clasificación binaria. Incluye encoding, escalado, manejo de desbalance, entrenamiento de modelos (Logistic Regression, Random Forest, XGBoost, LightGBM), validación cruzada, tuning de hiperparámetros, y métricas de evaluación.
---

# 🧠 Modeling — Modelado Predictivo

## Objetivo
Construir modelos de ML para predecir la suscripción a depósito a plazo (`subscribed`), comparar rendimiento y seleccionar el mejor.

---

## 1. Preparación de Features

### Encoding categórico
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd

# Target encoding
df["subscribed_encoded"] = (df["subscribed"] == "yes").astype(int)

# One-Hot para variables nominales de baja cardinalidad
ohe_cols = ["marital_status", "contact_method", "contact_day"]
df_encoded = pd.get_dummies(df, columns=ohe_cols, drop_first=True)

# Label Encoding para variables ordinales
le = LabelEncoder()
ordinal_cols = ["education_level"]
for col in ordinal_cols:
    df_encoded[col] = le.fit_transform(df_encoded[col])
```

### Escalado
```python
from sklearn.preprocessing import StandardScaler

num_features = ["age", "call_duration", "contact_attempts", "previous_contacts",
                "employment_variation_rate", "consumer_price_index",
                "consumer_confidence_index", "euribor_3m_rate", "total_employment"]

scaler = StandardScaler()
df_encoded[num_features] = scaler.fit_transform(df_encoded[num_features])
```

### Nota sobre `call_duration`
> **IMPORTANTE**: La variable `call_duration` se conoce *después* de la llamada, por lo que incluirla sería data leakage en producción. Se recomienda:
> - Entrenar un modelo **CON** `call_duration` (benchmark)
> - Entrenar otro **SIN** `call_duration` (modelo realista)

---

## 2. Split Train/Test

```python
from sklearn.model_selection import train_test_split

X = df_encoded.drop(columns=["subscribed", "subscribed_encoded"])
y = df_encoded["subscribed_encoded"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {X_train.shape}, Test: {X_test.shape}")
print(f"Target distribution train: {y_train.value_counts(normalize=True).to_dict()}")
```

---

## 3. Manejo de Desbalance de Clases

```python
# Opción A: class_weight en el modelo
# model = LogisticRegression(class_weight="balanced")

# Opción B: SMOTE
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
print(f"Después de SMOTE: {y_train_resampled.value_counts().to_dict()}")

# Opción C: Under-sampling
from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state=42)
X_train_under, y_train_under = rus.fit_resample(X_train, y_train)
```

---

## 4. Modelos

### Baseline — Logistic Regression
```python
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
y_prob_lr = lr.predict_proba(X_test)[:, 1]
```

### Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=200, class_weight="balanced",
                            random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]
```

### XGBoost
```python
from xgboost import XGBClassifier

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

xgb = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1,
                     scale_pos_weight=scale_pos_weight,
                     random_state=42, use_label_encoder=False,
                     eval_metric="logloss")
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
y_prob_xgb = xgb.predict_proba(X_test)[:, 1]
```

### LightGBM
```python
from lightgbm import LGBMClassifier

lgbm = LGBMClassifier(n_estimators=300, max_depth=6, learning_rate=0.1,
                       is_unbalance=True, random_state=42, verbose=-1)
lgbm.fit(X_train, y_train)
y_pred_lgbm = lgbm.predict(X_test)
y_prob_lgbm = lgbm.predict_proba(X_test)[:, 1]
```

---

## 5. Evaluación

```python
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve, precision_recall_curve,
    f1_score, accuracy_score
)
import plotly.figure_factory as ff
import plotly.graph_objects as go

def evaluar_modelo(nombre, y_test, y_pred, y_prob):
    print(f"\n{'='*60}")
    print(f"  {nombre}")
    print(f"{'='*60}")
    print(classification_report(y_test, y_pred, target_names=["No", "Yes"]))
    print(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.4f}")
    print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    fig = ff.create_annotated_heatmap(
        z=cm, x=["No", "Yes"], y=["No", "Yes"],
        colorscale="Blues", showscale=False
    )
    fig.update_layout(title=f"Confusion Matrix — {nombre}",
                      xaxis_title="Predicho", yaxis_title="Real")
    fig.show()
    
    return roc_auc_score(y_test, y_prob)
```

### Comparativa ROC
```python
def plot_roc_comparison(models_dict, y_test):
    fig = go.Figure()
    for nombre, y_prob in models_dict.items():
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc = roc_auc_score(y_test, y_prob)
        fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f"{nombre} (AUC={auc:.3f})"))
    
    fig.add_trace(go.Scatter(x=[0,1], y=[0,1], line=dict(dash="dash"),
                             name="Random", showlegend=True))
    fig.update_layout(title="Comparativa ROC Curves",
                      xaxis_title="FPR", yaxis_title="TPR",
                      plot_bgcolor="white", width=800, height=600)
    fig.show()
```

---

## 6. Tuning de Hiperparámetros

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# Ejemplo con Random Forest
param_grid = {
    "n_estimators": [100, 200, 500],
    "max_depth": [5, 10, 15, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(class_weight="balanced", random_state=42),
    param_grid, cv=5, scoring="roc_auc", n_jobs=-1, verbose=1
)
grid_search.fit(X_train, y_train)

print(f"Best AUC: {grid_search.best_score_:.4f}")
print(f"Best Params: {grid_search.best_params_}")
```

---

## 7. Feature Importance / SHAP

```python
import shap

# SHAP values para el mejor modelo
explainer = shap.TreeExplainer(xgb)  # o rf, lgbm
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, show=True)

# Feature importance bar
shap.summary_plot(shap_values, X_test, plot_type="bar", show=True)
```
