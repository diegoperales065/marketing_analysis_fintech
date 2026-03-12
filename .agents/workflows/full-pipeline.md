---
description: Pipeline completo del TFM — desde datos en bruto hasta modelo final
---

# Pipeline Completo del TFM

## Fase 1 — Limpieza de Datos
> Skill: `data-cleaning`

1. Cargar CSV con `sep=";"`
2. Renombrar columnas según diccionario del README
3. Tratar valores `"unknown"` (análisis + decisión)
4. Tratar `pdays = 999` → crear `is_new_campaign_client`
5. Detectar outliers en `age`, `call_duration`, `contact_attempts`
6. Crear `high_contact_attempts`
7. Castear tipos (categóricos explícitos)
8. Guardar dataset limpio en `datos/`

## Fase 2 — Análisis Exploratorio (EDA)
> Skill: `eda`

1. Análisis uni-variado (histogramas + countplots)
2. Análisis del target (distribución + tasa de conversión)
3. Análisis bi-variado vs `subscribed`
4. Matriz de correlación
5. Variables macroeconómicas vs target
6. Documentar hallazgos clave

## Fase 2.5 — Análisis Cuantitativo de Datos
> Skill: `data-analysis`

1. Validación de calidad (unknowns, tipos, integridad)
2. Estadísticas descriptivas avanzadas (asimetría, curtosis, CV)
3. Análisis agrupado por target (yes vs no)
4. Análisis de conversión por segmento (job_type, education_level, etc.)
5. Análisis de tendencias temporales (por mes de contacto)
6. Análisis de contexto macroeconómico (correlación con target)
7. Derivación de insights cuantificados
8. Generación de informe estructurado en `informes/`

## Fase 3 — Feature Engineering & Preprocessing
> Skill: `modeling` (sección 1)

1. Encoding categórico (OneHot / Label / Target)
2. Escalado de numéricas (StandardScaler)
3. Decisión sobre `call_duration` (leakage warning)
4. Feature selection (importancia, correlación)
5. Split train/test (80/20 estratificado)
6. Manejo de desbalance (SMOTE vs class_weight)

## Fase 4 — Modelado
> Skill: `modeling` (secciones 4-6)

1. Baseline: Logistic Regression
2. Random Forest
3. XGBoost
4. LightGBM
5. Validación cruzada (5-fold)
6. Tuning con GridSearchCV / RandomizedSearchCV
7. Comparativa de métricas (AUC, F1, Precision, Recall)

## Fase 5 — Interpretación
> Skill: `modeling` (sección 7)

1. Feature importance (modelo + SHAP)
2. Análisis del mejor modelo
3. Conclusiones de negocio
4. Recomendaciones de campaña

## Fase 6 — Reporting
> Skill: `pdf` (si se genera informe en PDF)

1. Documentar resultados en `informes/`
2. Registrar experimentos en `Bitácora de experimentos/`
3. Generar informe final del TFM
