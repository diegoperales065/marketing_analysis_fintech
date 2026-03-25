"""
============================================================
  AUDITORIA PROFESIONAL (solo-lectura) del dataset
  bank-additional_bank-additional-full.csv
============================================================
Genera un informe completo por consola. No modifica el CSV.
"""

import pandas as pd
import numpy as np
import sys, os, io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── CONFIG ──────────────────────────────────────────────────
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "datos",
                        "bank-additional_bank-additional-full.csv")
SEP = ";"
pd.set_option("display.max_columns", 30)
pd.set_option("display.width", 160)
pd.set_option("display.float_format", "{:.4f}".format)

# ── CARGA ───────────────────────────────────────────────────
print("=" * 90)
print("  AUDITORÍA PROFESIONAL DEL DATASET — SOLO LECTURA")
print("=" * 90)

df = pd.read_csv(CSV_PATH, sep=SEP)
n_rows, n_cols = df.shape

print(f"\n📂 Archivo: {os.path.basename(CSV_PATH)}")
print(f"📐 Dimensiones: {n_rows:,} filas × {n_cols} columnas")
print(f"💾 Memoria total: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ── 1. ESQUEMA DE DATOS ────────────────────────────────────
print("\n" + "=" * 90)
print("  1. ESQUEMA DE DATOS — Tipos y clasificación")
print("=" * 90)

schema_info = pd.DataFrame({
    "dtype_pandas": df.dtypes.astype(str),
    "clasificación": ["numérica" if pd.api.types.is_numeric_dtype(df[c]) else "categórica" for c in df.columns],
    "ejemplo_valor": [df[c].dropna().iloc[0] if len(df[c].dropna()) > 0 else "N/A" for c in df.columns]
})
print(schema_info.to_string())

# ── 2. VALORES NULOS ───────────────────────────────────────
print("\n" + "=" * 90)
print("  2. ANÁLISIS DE VALORES NULOS (NaN)")
print("=" * 90)

null_counts = df.isnull().sum()
null_pct = (df.isnull().mean() * 100).round(4)
null_report = pd.DataFrame({"nulos": null_counts, "% nulos": null_pct})
null_report = null_report[null_report["nulos"] > 0]

if null_report.empty:
    print("✅ El dataset NO contiene valores NaN en ninguna columna.")
else:
    print("⚠️  Columnas con valores nulos:")
    print(null_report.to_string())

total_nulos = null_counts.sum()
print(f"\n   Total NaN globales: {total_nulos} de {n_rows * n_cols:,} celdas ({total_nulos / (n_rows * n_cols) * 100:.4f}%)")

# ── 3. FILAS DUPLICADAS ────────────────────────────────────
print("\n" + "=" * 90)
print("  3. ANÁLISIS DE FILAS DUPLICADAS")
print("=" * 90)

n_dup = df.duplicated().sum()
n_dup_pct = n_dup / n_rows * 100
print(f"   Filas duplicadas exactas: {n_dup:,} ({n_dup_pct:.2f}%)")

if n_dup > 0:
    # Mostrar ejemplo de duplicados
    dup_sample = df[df.duplicated(keep=False)].head(4)
    print("\n   Ejemplo de filas duplicadas:")
    print(dup_sample.to_string())

# ── 4. VALORES "UNKNOWN" Y ESPECIALES ──────────────────────
print("\n" + "=" * 90)
print("  4. VALORES 'UNKNOWN' Y CÓDIGOS ESPECIALES")
print("=" * 90)

cat_cols_raw = df.select_dtypes(include="object").columns.tolist()

print("\n   4.1 Proporción de 'unknown' por columna categórica:")
print("   " + "-" * 60)
for col in cat_cols_raw:
    n_unk = (df[col] == "unknown").sum()
    pct_unk = n_unk / n_rows * 100
    flag = "⚠️  CRÍTICO" if pct_unk > 15 else "⚠️  MODERADO" if pct_unk > 5 else "✅ OK"
    if n_unk > 0:
        print(f"   {flag} | {col:20s} → {n_unk:>6,} unknowns ({pct_unk:>6.2f}%)")

# Código especial: pdays = 999
n_999 = (df["pdays"] == 999).sum()
pct_999 = n_999 / n_rows * 100
print(f"\n   4.2 Código especial pdays = 999 (cliente nunca contactado previamente):")
print(f"       {n_999:,} registros ({pct_999:.2f}%)")

# ── 5. ESTADÍSTICAS DESCRIPTIVAS — NUMÉRICAS ──────────────
print("\n" + "=" * 90)
print("  5. ESTADÍSTICAS DESCRIPTIVAS — Variables Numéricas")
print("=" * 90)

num_cols = df.select_dtypes(include=np.number).columns.tolist()

desc = df[num_cols].describe().T
desc["mediana"] = df[num_cols].median()
desc["asimetría"] = df[num_cols].skew()
desc["curtosis"] = df[num_cols].kurtosis()
desc["rango"] = desc["max"] - desc["min"]
desc["CV%"] = (desc["std"] / desc["mean"].abs() * 100)  # Coef. variación

print(desc[["count", "mean", "mediana", "std", "min", "25%", "50%", "75%", "max", "asimetría", "curtosis", "rango", "CV%"]].round(3).to_string())

# ── 6. DETECCIÓN DE OUTLIERS (IQR) ─────────────────────────
print("\n" + "=" * 90)
print("  6. DETECCIÓN DE OUTLIERS (método IQR × 1.5)")
print("=" * 90)

print(f"\n   {'Variable':<30s} {'Q1':>10s} {'Q3':>10s} {'IQR':>10s} {'Lím.Inf':>10s} {'Lím.Sup':>10s} {'#Outliers':>10s} {'%Outliers':>10s}")
print("   " + "-" * 100)

for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    n_out = ((df[col] < lower) | (df[col] > upper)).sum()
    pct_out = n_out / n_rows * 100
    flag = " ⚠️" if pct_out > 5 else ""
    print(f"   {col:<30s} {Q1:>10.3f} {Q3:>10.3f} {IQR:>10.3f} {lower:>10.3f} {upper:>10.3f} {n_out:>10,} {pct_out:>9.2f}%{flag}")

# ── 7. DISTRIBUCIÓN DE VARIABLES CATEGÓRICAS ──────────────
print("\n" + "=" * 90)
print("  7. DISTRIBUCIÓN DE VARIABLES CATEGÓRICAS")
print("=" * 90)

for col in cat_cols_raw:
    print(f"\n   📊 {col} ({df[col].nunique()} valores únicos):")
    vc = df[col].value_counts()
    pct = df[col].value_counts(normalize=True) * 100
    tbl = pd.DataFrame({"conteo": vc, "porcentaje": pct.round(2)})
    for val, row in tbl.iterrows():
        bar = "█" * int(row["porcentaje"] / 2)
        print(f"      {val:25s} → {row['conteo']:>6,.0f}  ({row['porcentaje']:>5.1f}%) {bar}")

# ── 8. VARIABLE TARGET (y) ────────────────────────────────
print("\n" + "=" * 90)
print("  8. ANÁLISIS DE LA VARIABLE TARGET — y")
print("=" * 90)

vc_y = df["y"].value_counts()
pct_y = df["y"].value_counts(normalize=True) * 100

print(f"   Total registros: {n_rows:,}")
for val in vc_y.index:
    print(f"   {val:>5s}: {vc_y[val]:>6,} ({pct_y[val]:.2f}%)")

ratio = vc_y.iloc[0] / vc_y.iloc[1]
print(f"\n   Ratio de desbalance (mayoría/minoría): {ratio:.2f}:1")

if ratio > 3:
    print("   ⚠️  DESBALANCE SIGNIFICATIVO — Se recomienda SMOTE, class_weight, o undersampling")
elif ratio > 1.5:
    print("   ⚠️  Desbalance moderado — Considerar estratificación en train/test split")
else:
    print("   ✅ Dataset relativamente balanceado")

# ── 9. CORRELACIONES CLAVE ─────────────────────────────────
print("\n" + "=" * 90)
print("  9. CORRELACIONES CON LA TARGET (y → numérica)")
print("=" * 90)

df_temp = df.copy()
df_temp["y_num"] = (df_temp["y"] == "yes").astype(int)

corrs = df_temp[num_cols + ["y_num"]].corr()["y_num"].drop("y_num").sort_values(key=abs, ascending=False)

print(f"\n   {'Variable':<35s} {'Correlación':>12s} {'Fuerza':>12s} {'Dirección':>12s}")
print("   " + "-" * 75)
for col_name, corr_val in corrs.items():
    fuerza = "FUERTE" if abs(corr_val) > 0.3 else "MODERADA" if abs(corr_val) > 0.15 else "DÉBIL"
    direccion = "POSITIVA ↑" if corr_val > 0 else "NEGATIVA ↓"
    print(f"   {col_name:<35s} {corr_val:>12.4f} {fuerza:>12s} {direccion:>12s}")

# ── 10. MULTICOLINEALIDAD ─────────────────────────────────
print("\n" + "=" * 90)
print("  10. DETECCIÓN DE MULTICOLINEALIDAD (|r| > 0.7)")
print("=" * 90)

corr_matrix = df[num_cols].corr()
high_corr_pairs = []

for i in range(len(num_cols)):
    for j in range(i + 1, len(num_cols)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.7:
            high_corr_pairs.append((num_cols[i], num_cols[j], r))

if high_corr_pairs:
    print(f"\n   ⚠️  Pares con correlación alta (|r| > 0.7):")
    print(f"   {'Variable 1':<35s} {'Variable 2':<35s} {'r':>8s}")
    print("   " + "-" * 80)
    for v1, v2, r in sorted(high_corr_pairs, key=lambda x: abs(x[2]), reverse=True):
        print(f"   {v1:<35s} {v2:<35s} {r:>8.4f}")
else:
    print("   ✅ No se detectaron pares con correlación alta (|r| > 0.7)")

# ── 11. ANÁLISIS DE CONSISTENCIA ──────────────────────────
print("\n" + "=" * 90)
print("  11. ANÁLISIS DE CONSISTENCIA Y REGLAS DE NEGOCIO")
print("=" * 90)

# 11.1 Duración = 0 y y = yes?
dur0_yes = ((df["duration"] == 0) & (df["y"] == "yes")).sum()
print(f"   11.1 Registros con duration=0 Y y='yes': {dur0_yes}")
if dur0_yes > 0:
    print("        ⚠️  Inconsistencia: no debería haber conversión sin llamada")
else:
    print("        ✅ Consistente — no hay conversiones sin llamada")

# 11.2 Duración = 0 en general
dur0 = (df["duration"] == 0).sum()
print(f"\n   11.2 Registros con duration=0 (llamada no realizada): {dur0} ({dur0/n_rows*100:.2f}%)")

# 11.3 previous = 0 cuando pdays != 999
prev0_pdays_not999 = ((df["previous"] == 0) & (df["pdays"] != 999)).sum()
print(f"\n   11.3 previous=0 con pdays≠999 (inconsistencia): {prev0_pdays_not999}")
if prev0_pdays_not999 > 0:
    print("        ⚠️  Posible inconsistencia — pdays indica contacto previo pero previous=0")
else:
    print("        ✅ Consistente")

# 11.4 pdays = 999 cuando previous > 0
pdays999_prev_gt0 = ((df["pdays"] == 999) & (df["previous"] > 0)).sum()
print(f"\n   11.4 pdays=999 con previous>0 (inconsistencia): {pdays999_prev_gt0}")
if pdays999_prev_gt0 > 0:
    print("        ⚠️  Inconsistencia — marcado como no contactado pero tiene contactos previos")
else:
    print("        ✅ Consistente")

# 11.5 Valores negativos en variables que no deberían tenerlos
for col in ["age", "duration", "campaign", "pdays", "previous"]:
    n_neg = (df[col] < 0).sum()
    if n_neg > 0:
        print(f"\n   11.5 ⚠️  {col} tiene {n_neg} valores negativos")
    else:
        print(f"   11.5 ✅ {col}: sin valores negativos")

# 11.6 Rango de edad razonable
age_min, age_max = df["age"].min(), df["age"].max()
print(f"\n   11.6 Rango de edad: {age_min} — {age_max}")
if age_min < 16 or age_max > 100:
    print("        ⚠️  Posibles edades fuera de rango razonable")
else:
    print("        ✅ Rango de edad razonable")

# ── 12. RESUMEN EJECUTIVO ─────────────────────────────────
print("\n" + "=" * 90)
print("  12. RESUMEN EJECUTIVO DE LA AUDITORÍA")
print("=" * 90)

issues = []

if total_nulos > 0:
    issues.append(f"Valores nulos encontrados: {total_nulos}")
if n_dup > 0:
    issues.append(f"Filas duplicadas exactas: {n_dup:,} ({n_dup_pct:.2f}%)")

# Unknowns
for col in cat_cols_raw:
    n_unk = (df[col] == "unknown").sum()
    if n_unk > 0:
        pct_unk = n_unk / n_rows * 100
        if pct_unk > 5:
            issues.append(f"'{col}' tiene {pct_unk:.1f}% de valores 'unknown'")

if ratio > 3:
    issues.append(f"Desbalance de clases significativo (ratio {ratio:.1f}:1)")

if dur0 > 0:
    issues.append(f"duration=0 en {dur0} registros (llamadas no realizadas)")

if len(high_corr_pairs) > 0:
    issues.append(f"{len(high_corr_pairs)} par(es) de variables con alta multicolinealidad (|r|>0.7)")

if issues:
    print(f"\n   ⚠️  HALLAZGOS QUE REQUIEREN ATENCIÓN ({len(issues)}):")
    for i, issue in enumerate(issues, 1):
        print(f"   {i}. {issue}")
else:
    print("\n   ✅ No se encontraron problemas críticos de calidad.")

print(f"""
   MÉTRICAS GENERALES:
   ├─ Filas: {n_rows:,}
   ├─ Columnas: {n_cols}
   ├─ Numéricas: {len(num_cols)}
   ├─ Categóricas: {len(cat_cols_raw)}
   ├─ NaN totales: {total_nulos}
   ├─ Duplicados exactos: {n_dup:,}
   ├─ Target 'yes': {vc_y.get('yes', 0):,} ({pct_y.get('yes', 0):.2f}%)
   ├─ Target 'no': {vc_y.get('no', 0):,} ({pct_y.get('no', 0):.2f}%)
   └─ Ratio desbalance: {ratio:.2f}:1
""")

print("=" * 90)
print("  FIN DE LA AUDITORÍA — DATOS NO MODIFICADOS")
print("=" * 90)
