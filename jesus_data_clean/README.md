# 🧹 Limpieza de Datos — Jesús

> Análisis y limpieza profesional del dataset `bank-additional_bank-additional-full.csv`
> **Proyecto**: Marketing Analytics para Empresa Fintech — TFM

---

## 📁 Estructura de Carpetas

```
jesus_data_clean/
│
├── 📓 notebooks/                         ← Entregables principales (Jupyter)
│   ├── 01_analisis_unknowns.ipynb        — Auditoría de valores "unknown"
│   └── 02_semantic_renaming_analysis.ipynb — Renombrado semántico de unknowns
│
├── 🐍 scripts/                           ← Código fuente Python
│   ├── 01_analisis_unknowns.py           — Script base del análisis de unknowns
│   ├── 02_semantic_renaming_analysis.py  — Perfilado estadístico profundo
│   └── 02_double_check.py               — Verificación automatizada (55 checks)
│
├── 📄 outputs/                           ← Resultados y logs de ejecución
│   ├── 01_output_unknowns.txt            — Salida del análisis de unknowns
│   ├── 02_semantic_output.txt            — Salida del perfilado semántico
│   ├── 02_doublecheck_output.txt         — Resultado: 54/55 verificaciones OK
│   ├── audit_output.txt                  — Salida de la auditoría CSV
│   ├── audit_report_renaming_unknowns    — Reporte de renombrado
│   ├── docx_content.txt                  — Contenido extraído del DOCX del compañero
│   ├── nb_all_cells.txt                  — Volcado de celdas del notebook del compañero
│   └── nb_relevant_cells.txt             — Celdas relevantes del notebook del compañero
│
├── 🔧 utils/                             ← Scripts auxiliares y generadores
│   ├── generate_notebook_02.py           — Generador del notebook 02
│   └── audit_csv.py                      — Auditoría general del CSV
│
└── 📖 README.md                          ← Este archivo
```

---

## 🔑 Resumen de Resultados

### Nombres Semánticos (Aprobados)

| Columna | `"unknown"` → | Nombre Semántico |
|:--------|:---:|:---|
| `default` | → | `no_credit_record` |
| `education` | → | `undisclosed_education` |
| `job` | → | `undeclared_occupation` |
| `marital` | → | `undisclosed_status` |

### Verificación: **54/55 checks PASSED** ✅

---

## 📋 Orden de Lectura Recomendado

1. `notebooks/01_analisis_unknowns.ipynb` — Auditoría inicial
2. `notebooks/02_semantic_renaming_analysis.ipynb` — Renombrado semántico
3. `outputs/02_doublecheck_output.txt` — Verificación de cifras
