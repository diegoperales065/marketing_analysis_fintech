"""
04_relacion_demografica_suscripcion.py
=======================================
Sub-tarea 1.3 del TFM — Relación demográfica–suscripción.
Analizar cómo edad, trabajo, educación y estado civil se relacionan
con la contratación del depósito a plazo.

Autor: Jesús | Fecha: 16/03/2026
Dataset: bank-additional_bank-additional-full.csv (41,188 × 21)
Modo: SOLO LECTURA — No se modifica el CSV.

NOTA: Se integran los nombres semánticos definidos en fase_01 (unknowns):
  default:   unknown → no_credit_record
  education: unknown → undisclosed_education
  job:       unknown → undeclared_occupation
  marital:   unknown → undisclosed_status
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal
import sys, os, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Carga ────────────────────────────────────────────────────────────────────
CSV = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                   "datos", "bank-additional_bank-additional-full.csv")
df = pd.read_csv(CSV, sep=";")
n = len(df)

# Aplicar nombres semánticos (solo para el análisis, no modifica el CSV)
SEMANTIC_MAP = {
    "default": {"unknown": "no_credit_record"},
    "education": {"unknown": "undisclosed_education"},
    "job": {"unknown": "undeclared_occupation"},
    "marital": {"unknown": "undisclosed_status"},
}
for col, mapping in SEMANTIC_MAP.items():
    df[col] = df[col].replace(mapping)

df["y_num"] = (df["y"] == "yes").astype(int)
overall_conv = df["y_num"].mean() * 100

print("=" * 100)
print("  SUB-TAREA 1.3 — RELACIÓN DEMOGRÁFICA–SUSCRIPCIÓN")
print(f"  Conversión global: {overall_conv:.2f}% ({df['y_num'].sum():,}/{n:,})")
print("=" * 100)

# ═════════════════════════════════════════════════════════════════════════════
# 1. EDAD vs SUSCRIPCIÓN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  1. EDAD vs SUSCRIPCIÓN")
print("█" * 100)

# Bandas etarias
bins = [0, 30, 40, 50, 60, 100]
labels = ["<30", "30-40", "41-50", "51-60", "60+"]
df["age_band"] = pd.cut(df["age"], bins=bins, labels=labels)

print(f"\n  {'Banda':<10s} {'n':>8s} {'%Total':>8s} {'yes':>8s} {'Conv%':>8s} {'vs.Media':>10s}")
print("  " + "-" * 56)
for band in labels:
    subset = df[df["age_band"] == band]
    cnt = len(subset)
    conv = subset["y_num"].mean() * 100
    diff = conv - overall_conv
    sign = "+" if diff > 0 else ""
    print(f"  {band:<10s} {cnt:>8,} {cnt/n*100:>7.1f}% {subset['y_num'].sum():>8,} {conv:>7.2f}% {sign}{diff:>+8.2f}pp")

# Test estadístico
yes_age = df.loc[df["y"] == "yes", "age"]
no_age = df.loc[df["y"] == "no", "age"]
u_stat, p_val = mannwhitneyu(yes_age, no_age, alternative="two-sided")
print(f"\n  Mann-Whitney U test (age × y): U={u_stat:,.0f}, p={p_val:.4e}")
sig = "SÍ SIGNIFICATIVA" if p_val < 0.05 else "NO significativa"
print(f"  → La diferencia de edad entre suscriptores y no suscriptores es {sig}")
print(f"  → Media yes={yes_age.mean():.1f} vs no={no_age.mean():.1f}")

# ═════════════════════════════════════════════════════════════════════════════
# 2. JOB vs SUSCRIPCIÓN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  2. TIPO DE TRABAJO vs SUSCRIPCIÓN")
print("█" * 100)

job_conv = df.groupby("job")["y_num"].agg(["count", "sum", "mean"])
job_conv.columns = ["n", "yes", "conv%"]
job_conv["conv%"] = job_conv["conv%"] * 100
job_conv = job_conv.sort_values("conv%", ascending=False)

print(f"\n  {'Job':<25s} {'n':>8s} {'yes':>6s} {'Conv%':>8s} {'vs.Media':>10s}")
print("  " + "-" * 60)
for job, row in job_conv.iterrows():
    diff = row["conv%"] - overall_conv
    sign = "+" if diff > 0 else ""
    marker = " ★" if abs(diff) > 5 else ""
    print(f"  {job:<25s} {row['n']:>8,.0f} {row['yes']:>6,.0f} {row['conv%']:>7.2f}% {sign}{diff:>+8.2f}pp{marker}")

# Chi-cuadrado
ct_job = pd.crosstab(df["job"], df["y"])
chi2, p, dof, _ = chi2_contingency(ct_job)
print(f"\n  Chi² (job × y): χ²={chi2:.2f}, dof={dof}, p={p:.4e}")
print(f"  → La relación job–suscripción es {'SIGNIFICATIVA' if p < 0.05 else 'no significativa'}")
print("\n  INSIGHT: student (31.5%) y retired (25.2%) convierten muy por encima de la media.")
print("           undeclared_occupation (11.2%) está en línea con la media global.")

# ═════════════════════════════════════════════════════════════════════════════
# 3. EDUCACIÓN vs SUSCRIPCIÓN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  3. NIVEL EDUCATIVO vs SUSCRIPCIÓN (con nombres semánticos)")
print("█" * 100)

edu_conv = df.groupby("education")["y_num"].agg(["count", "sum", "mean"])
edu_conv.columns = ["n", "yes", "conv%"]
edu_conv["conv%"] = edu_conv["conv%"] * 100
edu_conv = edu_conv.sort_values("conv%", ascending=False)

print(f"\n  {'Educación':<30s} {'n':>8s} {'yes':>6s} {'Conv%':>8s} {'vs.Media':>10s}")
print("  " + "-" * 65)
for edu, row in edu_conv.iterrows():
    diff = row["conv%"] - overall_conv
    sign = "+" if diff > 0 else ""
    marker = " ★" if abs(diff) > 3 else ""
    print(f"  {edu:<30s} {row['n']:>8,.0f} {row['yes']:>6,.0f} {row['conv%']:>7.2f}% {sign}{diff:>+8.2f}pp{marker}")

ct_edu = pd.crosstab(df["education"], df["y"])
chi2, p, dof, _ = chi2_contingency(ct_edu)
print(f"\n  Chi² (education × y): χ²={chi2:.2f}, dof={dof}, p={p:.4e}")
print(f"  → La relación educación–suscripción es {'SIGNIFICATIVA' if p < 0.05 else 'no significativa'}")
print("\n  INSIGHT: undisclosed_education convierte 14.5% — POR ENCIMA de la media (11.3%).")
print("           Estos clientes no son ruido: son perfiles valiosos que no comparten su educación.")

# ═════════════════════════════════════════════════════════════════════════════
# 4. ESTADO CIVIL vs SUSCRIPCIÓN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  4. ESTADO CIVIL vs SUSCRIPCIÓN (con nombres semánticos)")
print("█" * 100)

mar_conv = df.groupby("marital")["y_num"].agg(["count", "sum", "mean"])
mar_conv.columns = ["n", "yes", "conv%"]
mar_conv["conv%"] = mar_conv["conv%"] * 100
mar_conv = mar_conv.sort_values("conv%", ascending=False)

print(f"\n  {'Estado Civil':<25s} {'n':>8s} {'yes':>6s} {'Conv%':>8s}")
print("  " + "-" * 52)
for val, row in mar_conv.iterrows():
    print(f"  {val:<25s} {row['n']:>8,.0f} {row['yes']:>6,.0f} {row['conv%']:>7.2f}%")

ct_mar = pd.crosstab(df["marital"], df["y"])
chi2, p, dof, _ = chi2_contingency(ct_mar)
print(f"\n  Chi² (marital × y): χ²={chi2:.2f}, dof={dof}, p={p:.4e}")
print(f"  → La relación estado_civil–suscripción es {'SIGNIFICATIVA' if p < 0.05 else 'no significativa'}")

# ═════════════════════════════════════════════════════════════════════════════
# 5. DEFAULT vs SUSCRIPCIÓN (con perfil semántico)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  5. DEFAULT (CRÉDITO EN INCUMPLIMIENTO) vs SUSCRIPCIÓN")
print("█" * 100)

def_conv = df.groupby("default")["y_num"].agg(["count", "sum", "mean"])
def_conv.columns = ["n", "yes", "conv%"]
def_conv["conv%"] = def_conv["conv%"] * 100
def_conv = def_conv.sort_values("conv%", ascending=False)

print(f"\n  {'Default':<25s} {'n':>8s} {'yes':>6s} {'Conv%':>8s}")
print("  " + "-" * 52)
for val, row in def_conv.iterrows():
    print(f"  {val:<25s} {row['n']:>8,.0f} {row['yes']:>6,.0f} {row['conv%']:>7.2f}%")

ct_def = pd.crosstab(df["default"], df["y"])
chi2, p, dof, _ = chi2_contingency(ct_def)
print(f"\n  Chi² (default × y): χ²={chi2:.2f}, dof={dof}, p={p:.4e}")
print("\n  INSIGHT: no_credit_record convierte solo 5.15% — la MITAD de 'no' (12.88%).")
print("           Son 8,597 clientes (20.9%) con perfil conservador y sin historial crediticio.")
print("           Este grupo es el que más afecta negativamente la tasa de conversión global.")

# ═════════════════════════════════════════════════════════════════════════════
# 6. HOUSING & LOAN vs SUSCRIPCIÓN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  6. HIPOTECA Y PRÉSTAMO PERSONAL vs SUSCRIPCIÓN")
print("█" * 100)

for col_name, label in [("housing", "Hipoteca"), ("loan", "Préstamo Personal")]:
    print(f"\n  {label}:")
    col_conv = df.groupby(col_name)["y_num"].agg(["count", "sum", "mean"])
    col_conv.columns = ["n", "yes", "conv%"]
    col_conv["conv%"] = col_conv["conv%"] * 100
    for val, row in col_conv.iterrows():
        print(f"    {val:<15s}: {row['conv%']:>6.2f}% (n={row['n']:,.0f})")
    ct = pd.crosstab(df[col_name], df["y"])
    chi2, p, _, _ = chi2_contingency(ct)
    print(f"    Chi²: {chi2:.2f}, p={p:.4e} → {'SIGNIFICATIVA' if p < 0.05 else 'no sig.'}")

# ═════════════════════════════════════════════════════════════════════════════
# 7. INTERACCIONES CLAVE
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  7. INTERACCIONES — Cruces Demográficos Clave")
print("█" * 100)

# 7.1 Edad × Educación
print("\n  7.1 EDAD × EDUCACIÓN → Conversión:")
print(f"  {'Banda':<10s}", end="")
for edu in ["university.degree", "high.school", "basic.9y", "basic.4y", "undisclosed_education"]:
    print(f" {edu[:12]:>14s}", end="")
print()
print("  " + "-" * 82)

for band in labels:
    print(f"  {band:<10s}", end="")
    for edu in ["university.degree", "high.school", "basic.9y", "basic.4y", "undisclosed_education"]:
        subset = df[(df["age_band"] == band) & (df["education"] == edu)]
        if len(subset) >= 10:
            conv = subset["y_num"].mean() * 100
            print(f" {conv:>13.1f}%", end="")
        else:
            print(f" {'n<10':>14s}", end="")
    print()

# 7.2 Edad × Job (top 5 jobs)
print("\n  7.2 EDAD × JOB (top 5 jobs) → Conversión:")
top_jobs = df["job"].value_counts().head(5).index.tolist()
print(f"  {'Banda':<10s}", end="")
for job in top_jobs:
    print(f" {job[:12]:>14s}", end="")
print()
print("  " + "-" * 82)

for band in labels:
    print(f"  {band:<10s}", end="")
    for job in top_jobs:
        subset = df[(df["age_band"] == band) & (df["job"] == job)]
        if len(subset) >= 10:
            conv = subset["y_num"].mean() * 100
            print(f" {conv:>13.1f}%", end="")
        else:
            print(f" {'n<10':>14s}", end="")
    print()

# 7.3 Educación × Default (interacción más fuerte)
print("\n  7.3 EDUCACIÓN × DEFAULT → Conversión:")
for edu in ["university.degree", "high.school", "undisclosed_education", "basic.4y"]:
    for def_val in ["no", "no_credit_record"]:
        subset = df[(df["education"] == edu) & (df["default"] == def_val)]
        if len(subset) >= 10:
            conv = subset["y_num"].mean() * 100
            print(f"    {edu[:25]:<25s} + {def_val:<20s}: {conv:.2f}% (n={len(subset):,})")

# ═════════════════════════════════════════════════════════════════════════════
# 8. TESTS ESTADÍSTICOS FORMALES
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  8. RESUMEN DE TESTS ESTADÍSTICOS")
print("█" * 100)

print(f"\n  {'Variable':<25s} {'Test':>15s} {'Estadístico':>15s} {'p-value':>15s} {'Significativa':>15s}")
print("  " + "-" * 88)

# Edad → Mann-Whitney
u, p_age = mannwhitneyu(yes_age, no_age)
print(f"  {'age':<25s} {'Mann-Whitney':>15s} {u:>15,.0f} {p_age:>15.4e} {'SÍ' if p_age < 0.05 else 'NO':>15s}")

# Categóricas → Chi²
for col in ["job", "education", "marital", "default", "housing", "loan"]:
    ct = pd.crosstab(df[col], df["y"])
    chi2, p_cat, dof, _ = chi2_contingency(ct)
    print(f"  {col:<25s} {'Chi²':>15s} {chi2:>15.2f} {p_cat:>15.4e} {'SÍ' if p_cat < 0.05 else 'NO':>15s}")

# ═════════════════════════════════════════════════════════════════════════════
# RESUMEN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 100)
print("  RESUMEN — Sub-tarea 1.3 Completada")
print("=" * 100)
print("""
  HALLAZGOS PRINCIPALES:

  1. EDAD: Los jóvenes (<30) y mayores (60+) convierten más. El rango 30-50 convierte menos.
  2. JOB: student (31.5%) y retired (25.2%) son los top converters. blue-collar es el peor.
  3. EDUCACIÓN: illiterate tiene la mayor conversión pero con solo 18 casos (no representativo).
     university.degree y undisclosed_education son los segmentos grandes con alta conversión.
  4. ESTADO CIVIL: undisclosed_status (15.0%) > single > divorced > married.
  5. DEFAULT: no_credit_record (5.15%) convierte la MITAD que 'no' (12.88%). Es el grupo más
     numeroso de unknowns (20.9%) y el factor demográfico con mayor impacto negativo.
  6. TODAS las variables demográficas tienen relación SIGNIFICATIVA con la suscripción (p<0.001).

  DATOS NO MODIFICADOS — Solo lectura (se aplicaron nombres semánticos solo en pantalla).
""")

# Limpiar columna temporal
df.drop(columns=["age_band", "y_num"], inplace=True)

print("=" * 100)
print("  FIN — Sub-tarea 1.3: Relación Demográfica–Suscripción")
print("=" * 100)
