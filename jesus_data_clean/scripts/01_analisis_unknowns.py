"""
==========================================================
  ANALISIS DE VALORES "UNKNOWN" — SOLO LECTURA
  Objetivo: Entender los patrones de unknowns para
  definir la estrategia de limpieza profesional.
==========================================================
"""
import pandas as pd
import numpy as np
import sys, os, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CSV = os.path.join(os.path.dirname(__file__), "..", "datos",
                   "bank-additional_bank-additional-full.csv")
df = pd.read_csv(CSV, sep=";")
n = len(df)

COLS_UNK = ["job", "marital", "education", "default", "housing", "loan"]

print("=" * 90)
print("  ANALISIS DE VALORES 'UNKNOWN' — Patrones y Dependencias")
print("=" * 90)

# 1. Conteo basico
print("\n1. CONTEO DE UNKNOWNS POR COLUMNA:")
print("-" * 60)
for col in COLS_UNK:
    cnt = (df[col] == "unknown").sum()
    print(f"   {col:20s}: {cnt:>6,} ({cnt/n*100:.2f}%)")

# 2. Co-ocurrencia de unknowns
print("\n2. CO-OCURRENCIA DE UNKNOWNS:")
print("-" * 60)
df_unk = pd.DataFrame()
for col in COLS_UNK:
    df_unk[f"{col}_unk"] = (df[col] == "unknown").astype(int)

df_unk["total_unknowns"] = df_unk.sum(axis=1)

print("   Registros con N columnas unknown:")
vc = df_unk["total_unknowns"].value_counts().sort_index()
for k, v in vc.items():
    print(f"     {k} unknowns: {v:>6,} registros ({v/n*100:.2f}%)")

# 3. housing y loan coinciden?
both_unk = ((df["housing"] == "unknown") & (df["loan"] == "unknown")).sum()
only_housing = ((df["housing"] == "unknown") & (df["loan"] != "unknown")).sum()
only_loan = ((df["housing"] != "unknown") & (df["loan"] == "unknown")).sum()
print(f"\n   housing+loan ambos unknown: {both_unk:,}")
print(f"   solo housing unknown: {only_housing:,}")
print(f"   solo loan unknown: {only_loan:,}")

# 4. Tasa de conversion por unknown vs known
print("\n3. TASA DE CONVERSION POR ESTADO unknown/known:")
print("-" * 60)
df_temp = df.copy()
df_temp["y_num"] = (df_temp["y"] == "yes").astype(int)

for col in COLS_UNK:
    is_unk = df_temp[col] == "unknown"
    rate_unk = df_temp.loc[is_unk, "y_num"].mean() * 100
    rate_known = df_temp.loc[~is_unk, "y_num"].mean() * 100
    cnt_unk = is_unk.sum()
    if cnt_unk > 0:
        diff = rate_unk - rate_known
        signal = "+" if diff > 0 else ""
        print(f"   {col:20s}: known={rate_known:.2f}%  unknown={rate_unk:.2f}%  (diff={signal}{diff:.2f}pp, n_unk={cnt_unk:,})")

# 5. default: dado que es 20.9% y casi todo es "no", analizar profundo
print("\n4. ANALISIS PROFUNDO DE 'default' (20.87% unknown):")
print("-" * 60)
print("   Distribucion de default:")
for val, cnt in df["default"].value_counts().items():
    rate = df_temp.loc[df["default"] == val, "y_num"].mean() * 100
    print(f"     {val:10s}: {cnt:>6,} ({cnt/n*100:.2f}%) | conversion={rate:.2f}%")

# 6. Perfil de los clientes con default=unknown
print("\n5. PERFIL de clientes con default='unknown' vs 'no':")
print("-" * 60)
for feat in ["age", "duration", "campaign"]:
    mean_unk = df.loc[df["default"]=="unknown", feat].mean()
    mean_no = df.loc[df["default"]=="no", feat].mean()
    print(f"   {feat:15s}: unknown_mean={mean_unk:.1f}  no_mean={mean_no:.1f}")

# Education breakdown for default groups
print("\n   Education level distribution:")
for dval in ["no", "unknown"]:
    mask = df["default"] == dval
    print(f"\n   default='{dval}':")
    for edu, cnt in df.loc[mask, "education"].value_counts().head(5).items():
        pct = cnt / mask.sum() * 100
        print(f"     {edu:25s}: {cnt:>5,} ({pct:.1f}%)")

# 7. education unknown: analisis por job
print("\n6. EDUCATION='unknown': Distribucion por job_type:")
print("-" * 60)
mask_edu_unk = df["education"] == "unknown"
for job, cnt in df.loc[mask_edu_unk, "job"].value_counts().head(8).items():
    pct = cnt / mask_edu_unk.sum() * 100
    print(f"   {job:20s}: {cnt:>4,} ({pct:.1f}%)")

# 8. Test chi-cuadrado: unknown como predictor
print("\n7. CHI-CUADRADO: Es 'unknown' informativo para la target?")
print("-" * 60)
from scipy.stats import chi2_contingency

for col in COLS_UNK:
    has_unk = (df[col] == "unknown").sum()
    if has_unk == 0:
        continue
    ct = pd.crosstab(df[col] == "unknown", df["y"])
    chi2, p, dof, expected = chi2_contingency(ct)
    sig = "SIGNIFICATIVO" if p < 0.05 else "no significativo"
    print(f"   {col:20s}: chi2={chi2:.2f}, p={p:.6f} -> {sig}")

print("\n" + "=" * 90)
print("  FIN DEL ANALISIS — DATOS NO MODIFICADOS")
print("=" * 90)
