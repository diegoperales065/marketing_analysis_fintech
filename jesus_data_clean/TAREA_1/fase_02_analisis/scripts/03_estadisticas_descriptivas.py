"""
03_estadisticas_descriptivas.py
================================
Sub-tarea 1.2 del TFM — Estadísticas descriptivas completas.
Entender las características básicas de los datos.

Autor: Jesús | Fecha: 16/03/2026
Dataset: bank-additional_bank-additional-full.csv (41,188 × 21)
Modo: SOLO LECTURA — No se modifica el CSV.
"""

import pandas as pd
import numpy as np
from scipy import stats
import sys, os, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Carga ────────────────────────────────────────────────────────────────────
CSV = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                   "datos", "bank-additional_bank-additional-full.csv")
df = pd.read_csv(CSV, sep=";")
n, p = df.shape

pd.set_option("display.max_columns", 30)
pd.set_option("display.width", 160)
pd.set_option("display.float_format", "{:.4f}".format)

print("=" * 100)
print("  SUB-TAREA 1.2 — ESTADÍSTICAS DESCRIPTIVAS COMPLETAS")
print("  Dataset: bank-additional_bank-additional-full.csv")
print(f"  Dimensiones: {n:,} filas × {p} columnas")
print("=" * 100)

# ═════════════════════════════════════════════════════════════════════════════
# 1. ESQUEMA DE DATOS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  1. ESQUEMA DE DATOS — Clasificación de Variables")
print("█" * 100)

num_cols = df.select_dtypes(include=np.number).columns.tolist()
cat_cols = df.select_dtypes(include="object").columns.tolist()

print(f"\n  Variables numéricas ({len(num_cols)}): {num_cols}")
print(f"  Variables categóricas ({len(cat_cols)}): {cat_cols}")

schema = pd.DataFrame({
    "tipo_pandas": df.dtypes.astype(str),
    "clasificación": ["numérica" if c in num_cols else "categórica" for c in df.columns],
    "n_únicos": df.nunique(),
    "ejemplo": [df[c].dropna().iloc[0] for c in df.columns]
})
print("\n" + schema.to_string())

# ═════════════════════════════════════════════════════════════════════════════
# 2. ESTADÍSTICAS DESCRIPTIVAS — Variables Numéricas
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  2. ESTADÍSTICAS DESCRIPTIVAS — Variables Numéricas")
print("█" * 100)

desc = df[num_cols].describe().T
desc["mediana"] = df[num_cols].median()
desc["asimetría"] = df[num_cols].skew()
desc["curtosis"] = df[num_cols].kurtosis()
desc["rango"] = desc["max"] - desc["min"]
desc["CV%"] = (desc["std"] / desc["mean"].abs() * 100)
desc["IQR"] = desc["75%"] - desc["25%"]

cols_mostrar = ["count", "mean", "mediana", "std", "min", "25%", "50%", "75%", "max",
                "IQR", "asimetría", "curtosis", "rango", "CV%"]
print("\n" + desc[cols_mostrar].round(4).to_string())

# Comentarios interpretativos
print("\n  INTERPRETACIONES CLAVE:")
print("  ├─ duration: CV=100.4% → dispersión extrema. Asimetría=3.26 → cola derecha pesada")
print("  ├─ campaign: CV=107.9% → muchos outliers de alta frecuencia de contacto")
print("  ├─ pdays: 96.3% de los valores son 999 (nunca contactado antes)")
print("  ├─ previous: 86.3% son 0 → la mayoría nunca fue contactada en campañas previas")
print("  └─ emp.var.rate: CV=1918.5% → cruza el cero (valores negativos y positivos)")

# ═════════════════════════════════════════════════════════════════════════════
# 3. DETECCIÓN DE OUTLIERS (IQR × 1.5)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  3. DETECCIÓN DE OUTLIERS (método IQR × 1.5)")
print("█" * 100)

header = f"\n  {'Variable':<25s} {'Q1':>10s} {'Q3':>10s} {'IQR':>10s} {'Lím.Inf':>10s} {'Lím.Sup':>10s} {'#Out':>8s} {'%Out':>8s}"
print(header)
print("  " + "-" * 93)

for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    n_out = ((df[col] < lower) | (df[col] > upper)).sum()
    pct = n_out / n * 100
    flag = " ⚠️" if pct > 5 else ""
    print(f"  {col:<25s} {Q1:>10.2f} {Q3:>10.2f} {IQR:>10.2f} {lower:>10.2f} {upper:>10.2f} {n_out:>8,} {pct:>7.2f}%{flag}")

print("\n  INTERPRETACIONES:")
print("  ├─ previous (13.7%): IQR=0, por lo que cualquier valor >0 es 'outlier'. Normal en datos asimétricos.")
print("  ├─ duration (7.2%): Llamadas muy largas (>644s ≈ 10.7 min). Son clientes con alto interés.")
print("  └─ campaign (5.8%): Clientes contactados >6 veces. Punto de saturación para la eficacia.")

# ═════════════════════════════════════════════════════════════════════════════
# 4. DISTRIBUCIÓN DE VARIABLES CATEGÓRICAS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  4. DISTRIBUCIÓN DE VARIABLES CATEGÓRICAS")
print("█" * 100)

for col in cat_cols:
    print(f"\n  📊 {col} ({df[col].nunique()} valores únicos):")
    vc = df[col].value_counts()
    for val, cnt in vc.items():
        pct = cnt / n * 100
        bar = "█" * int(pct / 2)
        print(f"    {val:25s} → {cnt:>6,}  ({pct:>5.1f}%) {bar}")

# ═════════════════════════════════════════════════════════════════════════════
# 5. VARIABLE TARGET — y
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  5. VARIABLE TARGET — y (¿contrató el depósito?)")
print("█" * 100)

vc_y = df["y"].value_counts()
pct_y = df["y"].value_counts(normalize=True) * 100
ratio = vc_y.iloc[0] / vc_y.iloc[1]

print(f"\n  Total registros: {n:,}")
for val in vc_y.index:
    bar = "█" * int(pct_y[val] / 2)
    print(f"  {val:>5s}: {vc_y[val]:>6,} ({pct_y[val]:.2f}%) {bar}")
print(f"\n  Ratio de desbalance (no/yes): {ratio:.2f}:1")
print("  ⚠️  DESBALANCE SIGNIFICATIVO — Para modelado considerar: SMOTE, class_weight, o undersampling")

# ═════════════════════════════════════════════════════════════════════════════
# 6. CALIDAD DE DATOS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  6. CALIDAD DE DATOS — Nulos, Duplicados, Códigos Especiales")
print("█" * 100)

# Nulos
total_nan = df.isnull().sum().sum()
print(f"\n  6.1 Valores NaN: {total_nan} de {n * p:,} celdas ({total_nan / (n * p) * 100:.4f}%)")
if total_nan == 0:
    print("      ✅ El dataset NO contiene valores NaN")

# Duplicados
n_dup = df.duplicated().sum()
print(f"\n  6.2 Filas duplicadas exactas: {n_dup} ({n_dup / n * 100:.3f}%)")
if n_dup > 0:
    print("      Nota: Se eliminan en el paso de limpieza posterior")

# Unknowns (referencia al trabajo de fase_01)
print(f"\n  6.3 Valores 'unknown' (análisis detallado en fase_01):")
for col in cat_cols:
    cnt_unk = (df[col] == "unknown").sum()
    if cnt_unk > 0:
        pct_unk = cnt_unk / n * 100
        flag = "CRÍTICO" if pct_unk > 15 else "MODERADO" if pct_unk > 5 else "OK"
        print(f"      {col:20s}: {cnt_unk:>6,} ({pct_unk:>5.2f}%) [{flag}]")
print("      → Estrategia definida en fase_01: renombrado semántico (no_credit_record, undisclosed_education, etc.)")

# Códigos especiales
n_999 = (df["pdays"] == 999).sum()
n_dur0 = (df["duration"] == 0).sum()
print(f"\n  6.4 Códigos especiales:")
print(f"      pdays=999 (nunca contactado antes): {n_999:,} ({n_999 / n * 100:.2f}%)")
print(f"      duration=0 (llamada no realizada):  {n_dur0} ({n_dur0 / n * 100:.3f}%)")

# Consistencia: previous vs pdays
inc = ((df["pdays"] == 999) & (df["previous"] > 0)).sum()
print(f"\n  6.5 Inconsistencia pdays=999 con previous>0: {inc:,} registros")
print("      → pdays indica 'no contactado' pero previous>0 indica contactos previos")

# ═════════════════════════════════════════════════════════════════════════════
# 7. MATRIZ DE CORRELACIÓN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  7. MATRIZ DE CORRELACIÓN (variables numéricas)")
print("█" * 100)

df_temp = df.copy()
df_temp["y_num"] = (df_temp["y"] == "yes").astype(int)
all_num = num_cols + ["y_num"]

corr = df_temp[all_num].corr()
print("\n" + corr.round(3).to_string())

# Correlaciones con target
print("\n  TOP CORRELACIONES CON TARGET (y):")
corr_target = corr["y_num"].drop("y_num").sort_values(key=abs, ascending=False)
for col_name, r in corr_target.items():
    fuerza = "FUERTE" if abs(r) > 0.3 else "MODERADA" if abs(r) > 0.15 else "DÉBIL"
    dir_str = "↑ POSITIVA" if r > 0 else "↓ NEGATIVA"
    print(f"  {col_name:20s}: r={r:+.4f} [{fuerza}] {dir_str}")

# ═════════════════════════════════════════════════════════════════════════════
# 8. MULTICOLINEALIDAD
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  8. DETECCIÓN DE MULTICOLINEALIDAD (|r| > 0.7)")
print("█" * 100)

corr_matrix = df[num_cols].corr()
high_corr = []
for i in range(len(num_cols)):
    for j in range(i + 1, len(num_cols)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.7:
            high_corr.append((num_cols[i], num_cols[j], r))

if high_corr:
    print(f"\n  ⚠️  {len(high_corr)} pares con correlación alta:")
    print(f"  {'Variable 1':<25s} {'Variable 2':<25s} {'r':>8s}")
    print("  " + "-" * 60)
    for v1, v2, r in sorted(high_corr, key=lambda x: abs(x[2]), reverse=True):
        print(f"  {v1:<25s} {v2:<25s} {r:>8.4f}")
    
    print("\n  IMPLICACIONES PARA MODELADO:")
    print("  ├─ emp.var.rate, euribor3m y nr.employed son prácticamente la misma información (r>0.90)")
    print("  ├─ Usar las 3 juntas en un modelo introduce multicolinealidad severa")
    print("  └─ Recomendación: seleccionar 1 o usar PCA para reducir dimensionalidad")
else:
    print("\n  ✅ No se detectaron pares con correlación alta")

# ═════════════════════════════════════════════════════════════════════════════
# RESUMEN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 100)
print("  RESUMEN — Sub-tarea 1.2 Completada")
print("=" * 100)
print(f"""
  MÉTRICAS GENERALES:
  ├─ Filas: {n:,} | Columnas: {p}
  ├─ Numéricas: {len(num_cols)} | Categóricas: {len(cat_cols)}
  ├─ NaN totales: {total_nan} | Duplicados: {n_dup}
  ├─ Target yes: {vc_y.get('yes', 0):,} ({pct_y.get('yes', 0):.2f}%) | no: {vc_y.get('no', 0):,} ({pct_y.get('no', 0):.2f}%)
  ├─ Ratio desbalance: {ratio:.2f}:1
  ├─ Multicolinealidad: {len(high_corr)} pares (|r|>0.7)
  └─ Variable más correlacionada con target: duration (r=+0.41)

  DATOS NO MODIFICADOS — Solo lectura.
""")
print("=" * 100)
print("  FIN — Sub-tarea 1.2: Estadísticas Descriptivas")
print("=" * 100)
