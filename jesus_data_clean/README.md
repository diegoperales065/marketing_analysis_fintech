# jesus_data_clean — Análisis de Datos (TFM)

## Estructura

```
jesus_data_clean/
│
├── TAREA_1/
│   ├── Tarea1_Notebook_Unificado.ipynb    ← Notebook único con TODO el análisis
│   │
│   ├── fase_01_unknowns/                  ← Análisis de valores unknown
│   │   ├── scripts/  (01, 02, 02_double_check)
│   │   ├── notebooks/ (01, 02)
│   │   ├── outputs/
│   │   └── utils/
│   │
│   └── fase_02_analisis/                  ← Estadísticas, demográfica, campaña
│       ├── scripts/  (03, 04, 05)
│       ├── notebooks/ (03, 04, 05)
│       └── outputs/
│
├── informes/
│   ├── Informe_Tarea1_y_Tarea2_Final_v4.docx  ← ✅ VERSIÓN FINAL (17 gráficos, 26 tablas)
│   ├── Informe_Tarea1_y_Tarea2_Final_v3.docx  ← Versión intermedia (pre-auditoría)
│   ├── Informe_Tarea1_y_Tarea2_Final.docx      ← Versión original v2
│   ├── Informe_Tarea1_Completo.docx             ← DOCX para tesis (10+ páginas)
│   ├── Informe_Tarea1_Resumen.docx              ← DOCX para compañeros (3-4 páginas)
│   └── figuras/                                  ← 17 PNGs profesionales (300 DPI)
│
├── scripts/                               ← Scripts de generación y auditoría
│   ├── README.md                           ← Documentación de scripts
│   ├── generacion_informe/                 ← Generación de gráficos y DOCX
│   │   ├── generate_charts.py              ← 17 gráficos con paleta corporativa
│   │   ├── rebuild_docx.py                 ← v2→v3: inserción de gráficos
│   │   └── fix_v3_to_v4.py                 ← v3→v4: correcciones de auditoría
│   │
│   ├── auditoria/                          ← Auditoría notebook vs informe
│   │   └── audit_notebook_vs_report.py     ← Auditoría celda-por-celda (14 hallazgos)
│   │
│   ├── extraccion/                         ← Extracción de datos para análisis
│   │   ├── extract_nb_cells.py
│   │   ├── extract_docx_structure.py
│   │   ├── extract_docx_styles.py
│   │   └── extract_v3_content.py
│   │
│   └── verificacion/                       ← Verificación del documento final
│       ├── verify_docx.py
│       ├── verify_v4.py
│       └── verify_v4_file.py
│
├── outputs/                               ← Resultados de análisis y verificación
│   ├── README.md                           ← Documentación de outputs
│   ├── auditoria/
│   │   └── audit_report.txt                ← 14 discrepancias (893 líneas)
│   ├── extraccion/
│   │   ├── nb_cells_output.txt             ← Celdas del notebook
│   │   ├── docx_structure.txt              ← Estructura del DOCX
│   │   ├── docx_styles.txt                 ← Estilos y paleta de colores
│   │   └── v3_exact_content.txt            ← Contenido exacto v3
│   └── verificacion/
│       ├── verification_report.txt         ← Verificación v3
│       └── v4_verification.txt             ← Verificación v4 final
│
└── README.md                              ← Este archivo
```

## Versiones del Informe

| Versión | Archivo | Imágenes | Tablas | Estado |
|:---|:---|:---:|:---:|:---|
| **v4** | `Informe_Tarea1_y_Tarea2_Final_v4.docx` | 17 | 26 | ✅ **FINAL** — Alineado con notebook |
| v3 | `Informe_Tarea1_y_Tarea2_Final_v3.docx` | 17 | 26 | Gráficos añadidos, pre-auditoría |
| v2 | `Informe_Tarea1_y_Tarea2_Final.docx` | 0 | 26 | Original sin gráficos |

## Orden de Lectura

**Opción rápida**: Abrir directamente `TAREA_1/Tarea1_Notebook_Unificado.ipynb` — contiene todo.

**Opción detallada** (por fases):
1. `01_analisis_unknowns` → Conteo y significancia de unknowns
2. `02_semantic_renaming_analysis` → Perfilado y propuesta de renombrado
3. `03_estadisticas_descriptivas` → Descriptivas, outliers, correlaciones
4. `04_relacion_demografica_suscripcion` → Edad, job, educación vs suscripción
5. `05_impacto_campana` → Contactos, mes, duración, poutcome, macro

## Decisiones Clave
- **Unknowns**: Renombrado semántico (no NaN, no eliminación)
- **CSV**: Solo lectura. No se modifica el dataset original
- **Informe v4**: Alineado celda-por-celda con `notebooks/tarea_1_notebook.ipynb`
- **Stack**: Solo librerías realmente usadas (pandas, numpy, matplotlib, seaborn, missingno)
