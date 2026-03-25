# 📋 Plantillas de Informes de Análisis

> Plantillas reutilizables para estructurar los informes del TFM de marketing bancario.

---

## Plantilla 1 — Informe Completo de Análisis de Campaña

```markdown
# Informe de Análisis: Campaña de Marketing Bancario

**Fecha**: [YYYY-MM-DD]
**Autor**: [Nombre]
**Dataset**: bank-additional-full.csv
**Registros analizados**: [N]

---

## 1. Resumen Ejecutivo

La campaña de telemarketing bancario muestra una tasa de conversión global del **X.XX%**
sobre [N] clientes contactados. Los hallazgos principales indican que:

1. [Hallazgo #1 con métrica cuantificada]
2. [Hallazgo #2 con métrica cuantificada]
3. [Hallazgo #3 con métrica cuantificada]

---

## 2. Dataset Overview

| Métrica              | Valor     |
|:---------------------|:----------|
| Total registros      | X,XXX     |
| Variables            | XX        |
| Variables numéricas  | 9         |
| Variables categóricas| 10        |
| Variables derivadas  | 2         |
| Target (subscribed)  | yes / no  |
| Tasa de conversión   | X.XX%     |

### Calidad de datos
| Columna          | % Unknown | Acción tomada        |
|:-----------------|:----------|:---------------------|
| credit_default   | X.X%      | [Mantener/Imputar]   |
| education_level  | X.X%      | [Mantener/Imputar]   |
| job_type         | X.X%      | [Mantener/Imputar]   |

---

## 3. Estadísticas Descriptivas

### Variables numéricas clave
| Variable                   | Media  | Mediana | Desv. Est. | Asimetría | Curtosis |
|:---------------------------|:-------|:--------|:-----------|:----------|:---------|
| age                        | X.XX   | X.XX    | X.XX       | X.XX      | X.XX     |
| call_duration              | X.XX   | X.XX    | X.XX       | X.XX      | X.XX     |
| contact_attempts           | X.XX   | X.XX    | X.XX       | X.XX      | X.XX     |

### Diferencias significativas (subscribed: yes vs no)
| Variable           | Media (yes) | Media (no) | Diferencia (%) |
|:-------------------|:------------|:-----------|:---------------|
| call_duration      | X.XX        | X.XX       | +XX.X%         |
| euribor_3m_rate    | X.XX        | X.XX       | -XX.X%         |

---

## 4. Análisis de Segmentos

### Top 5 segmentos por conversión
| Segmento                    | Conversión (%) | N contactos |
|:----------------------------|:---------------|:------------|
| [job_type = retired]        | XX.X%          | X,XXX       |
| [job_type = student]        | XX.X%          | X,XXX       |

### Bottom 5 segmentos por conversión
| Segmento                    | Conversión (%) | N contactos |
|:----------------------------|:---------------|:------------|
| [job_type = blue-collar]    | XX.X%          | X,XXX       |

---

## 5. Análisis Macroeconómico

| Variable macro               | Correlación con target | Impacto    |
|:-----------------------------|:-----------------------|:-----------|
| employment_variation_rate    | r = X.XXX              | [FUERTE]   |
| euribor_3m_rate              | r = X.XXX              | [FUERTE]   |
| consumer_confidence_index    | r = X.XXX              | [MODERADO] |

---

## 6. Recomendaciones

1. **[Recomendación 1]**: Basada en [hallazgo + métrica]
2. **[Recomendación 2]**: Basada en [hallazgo + métrica]
3. **[Recomendación 3]**: Basada en [hallazgo + métrica]

---

## 7. Anexos

- Código fuente: `scripts/` o `notebooks/TFM.ipynb`
- Visualizaciones: `informes/figuras/`
- Dataset limpio: `datos/`
```

---

## Plantilla 2 — Resumen Ejecutivo (1 página)

```markdown
# Resumen Ejecutivo — Análisis de Marketing Bancario

**Fecha**: [YYYY-MM-DD] | **N**: [registros] | **Conversión global**: X.XX%

## Hallazgos Clave
| #  | Hallazgo                                          | Métrica         |
|:---|:--------------------------------------------------|:----------------|
| 1  | [Descripción concisa]                             | [Valor]         |
| 2  | [Descripción concisa]                             | [Valor]         |
| 3  | [Descripción concisa]                             | [Valor]         |

## Segmentos Prioritarios
- 🟢 **Alta conversión**: [segmentos] (>X% conversión)
- 🔴 **Baja conversión**: [segmentos] (<X% conversión)

## Variables más influyentes
1. `call_duration` — r = X.XXX
2. `euribor_3m_rate` — r = X.XXX
3. `employment_variation_rate` — r = X.XXX

## Acción recomendada
[Recomendación principal en 2-3 líneas]
```

---

## Plantilla 3 — Análisis de Segmento Específico

```markdown
# Análisis de Segmento: [Nombre del Segmento]

## Definición
- **Filtro**: `[columna] == "[valor]"`
- **N registros**: X,XXX (X.X% del total)
- **Tasa de conversión**: X.XX% (vs X.XX% global)

## Perfil Demográfico
| Variable         | Valor más frecuente | Distribución            |
|:-----------------|:--------------------|:------------------------|
| age              | [rango]             | Media: X.XX, Std: X.XX  |
| marital_status   | [valor]             | XX.X%                   |
| education_level  | [valor]             | XX.X%                   |

## Comportamiento de Campaña
| Métrica               | Segmento | Global  | Diferencia |
|:----------------------|:---------|:--------|:-----------|
| call_duration (media) | X.XX     | X.XX    | +XX%       |
| contact_attempts      | X.XX     | X.XX    | -XX%       |

## Contexto Macroeconómico
[Análisis de variables macro para este segmento]

## Recomendación
[Acción específica para este segmento]
```
