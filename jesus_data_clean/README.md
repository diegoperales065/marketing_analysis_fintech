# jesus_data_clean — Analisis de Datos (TFM)

## Estructura

```
jesus_data_clean/
│
├── TAREA_1/
│   ├── Tarea1_Notebook_Unificado.ipynb    ← Notebook unico con TODO el analisis
│   │
│   ├── fase_01_unknowns/                  ← Analisis de valores unknown
│   │   ├── scripts/  (01, 02, 02_double_check)
│   │   ├── notebooks/ (01, 02)
│   │   ├── outputs/
│   │   └── utils/
│   │
│   └── fase_02_analisis/                  ← Estadisticas, demografica, campana
│       ├── scripts/  (03, 04, 05)
│       ├── notebooks/ (03, 04, 05)
│       └── outputs/
│
├── informes/
│   ├── Informe_Tarea1_Completo.docx       ← DOCX para tesis (10+ paginas)
│   └── Informe_Tarea1_Resumen.docx        ← DOCX para companeros (3-4 paginas)
│
└── README.md
```

## Orden de lectura

**Opcion rapida**: Abrir directamente `TAREA_1/Tarea1_Notebook_Unificado.ipynb` — contiene todo.

**Opcion detallada** (por fases):
1. `01_analisis_unknowns` → Conteo y significancia de unknowns
2. `02_semantic_renaming_analysis` → Perfilado y propuesta de renombrado
3. `03_estadisticas_descriptivas` → Descriptivas, outliers, correlaciones
4. `04_relacion_demografica_suscripcion` → Edad, job, educacion vs suscripcion
5. `05_impacto_campana` → Contactos, mes, duracion, poutcome, macro

## Decisiones Clave
- **Unknowns**: Renombrado semantico (no NaN, no eliminacion)
- **CSV**: Solo lectura. No se modifica el dataset original.
- **Tests**: Chi2, Mann-Whitney U, Kruskal-Wallis, Spearman
