"""
05_impacto_campana.py
======================
Sub-tarea 1.4 del TFM — Impacto de la campaña.
Evaluar cómo el número de contactos, mes, día de la semana,
duración, método de contacto, historial previo y contexto
macroeconómico afectan al resultado de la campaña.

Autor: Jesús | Fecha: 16/03/2026
Dataset: bank-additional_bank-additional-full.csv (41,188 × 21)
Modo: SOLO LECTURA — No se modifica el CSV.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal, spearmanr
import sys, os, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Carga ────────────────────────────────────────────────────────────────────
CSV = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                   "datos", "bank-additional_bank-additional-full.csv")
df = pd.read_csv(CSV, sep=";")
n = len(df)
df["y_num"] = (df["y"] == "yes").astype(int)
overall_conv = df["y_num"].mean() * 100

print("=" * 100)
print("  SUB-TAREA 1.4 — IMPACTO DE LA CAMPAÑA EN LA SUSCRIPCIÓN")
print(f"  Conversión global: {overall_conv:.2f}% ({df['y_num'].sum():,}/{n:,})")
print("=" * 100)

# ═════════════════════════════════════════════════════════════════════════════
# 1. NÚMERO DE CONTACTOS (campaign)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  1. NÚMERO DE CONTACTOS EN ESTA CAMPAÑA (campaign)")
print("█" * 100)

print(f"\n  {'Contactos':>10s} {'n':>8s} {'yes':>6s} {'Conv%':>8s} {'Conv.Acum':>10s}")
print("  " + "-" * 46)

# Detalle por número de contactos (1-15+)
for c in range(1, 16):
    if c < 15:
        subset = df[df["campaign"] == c]
        label = str(c)
    else:
        subset = df[df["campaign"] >= 15]
        label = "15+"
    if len(subset) > 0:
        conv = subset["y_num"].mean() * 100
        # Conversión acumulada (≤c contactos)
        if c < 15:
            cum_subset = df[df["campaign"] <= c]
        else:
            cum_subset = df
        cum_conv = cum_subset["y_num"].mean() * 100
        print(f"  {label:>10s} {len(subset):>8,} {subset['y_num'].sum():>6,} {conv:>7.2f}% {cum_conv:>9.2f}%")

# Análisis de saturación
print("\n  ANÁLISIS DE SATURACIÓN:")
for threshold in [1, 2, 3, 5, 7, 10]:
    above = df[df["campaign"] > threshold]
    below = df[df["campaign"] <= threshold]
    conv_a = above["y_num"].mean() * 100 if len(above) > 0 else 0
    conv_b = below["y_num"].mean() * 100
    diff = conv_a - conv_b
    print(f"    ≤{threshold} contactos: {conv_b:.2f}% (n={len(below):,}) | >{threshold}: {conv_a:.2f}% (n={len(above):,}) | Δ={diff:+.2f}pp")

# Test Spearman
rho, p_spear = spearmanr(df["campaign"], df["y_num"])
print(f"\n  Spearman (campaign × y): ρ={rho:.4f}, p={p_spear:.4e}")
print("  → A más contactos, MENOS probabilidad de suscripción (relación negativa)")
print("\n  INSIGHT: El punto de saturación está alrededor de 3 contactos.")
print("           Después de 3 intentos, la conversión cae de 12.17% a 7.27%.")
print("           Después de 10, baja a ~3%. Insistir más allá es contraproducente.")

# ═════════════════════════════════════════════════════════════════════════════
# 2. MES DEL CONTACTO (month)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  2. MES DEL ÚLTIMO CONTACTO (month)")
print("█" * 100)

# Orden cronológico
month_order = ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

print(f"\n  {'Mes':<6s} {'n':>8s} {'%Vol':>7s} {'yes':>6s} {'Conv%':>8s} {'vs.Media':>10s}")
print("  " + "-" * 50)
for m in month_order:
    subset = df[df["month"] == m]
    if len(subset) > 0:
        conv = subset["y_num"].mean() * 100
        diff = conv - overall_conv
        vol_pct = len(subset) / n * 100
        marker = " ★" if conv > 30 else " ⬇" if conv < 8 else ""
        print(f"  {m:<6s} {len(subset):>8,} {vol_pct:>6.1f}% {subset['y_num'].sum():>6,} {conv:>7.2f}% {diff:>+9.2f}pp{marker}")

chi2, p, _, _ = chi2_contingency(pd.crosstab(df["month"], df["y"]))
print(f"\n  Chi² (month × y): χ²={chi2:.2f}, p={p:.4e}")
print(f"  → La relación mes–suscripción es {'SIGNIFICATIVA' if p < 0.05 else 'no significativa'}")

print("\n  INSIGHT:")
print("    ├─ Mar, Sep, Oct, Dec: conversiones >40% pero con POCO volumen (<750 llamadas)")
print("    ├─ May: es el mes con MÁS volumen (33.4%) pero PEOR conversión (6.43%)")
print("    └─ Patrón: volumen inversamente proporcional a la conversión.")
print("       Los meses de baja actividad pueden coincidir con mejores condiciones económicas.")

# ═════════════════════════════════════════════════════════════════════════════
# 3. DÍA DE LA SEMANA (day_of_week)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  3. DÍA DE LA SEMANA DEL ÚLTIMO CONTACTO")
print("█" * 100)

day_order = ["mon", "tue", "wed", "thu", "fri"]
print(f"\n  {'Día':<6s} {'n':>8s} {'yes':>6s} {'Conv%':>8s}")
print("  " + "-" * 32)
for d in day_order:
    subset = df[df["day_of_week"] == d]
    conv = subset["y_num"].mean() * 100
    print(f"  {d:<6s} {len(subset):>8,} {subset['y_num'].sum():>6,} {conv:>7.2f}%")

chi2, p, _, _ = chi2_contingency(pd.crosstab(df["day_of_week"], df["y"]))
print(f"\n  Chi² (day × y): χ²={chi2:.2f}, p={p:.4e}")
print(f"  → La relación día–suscripción es {'SIGNIFICATIVA' if p < 0.05 else 'no significativa'}")
print("\n  INSIGHT: La diferencia entre días es moderada (9.95%–12.12%).")
print("           Jueves es el mejor día, lunes el peor. El volumen es similar entre días.")

# ═════════════════════════════════════════════════════════════════════════════
# 4. DURACIÓN DE LA LLAMADA (duration) — BUCKETS CLAROS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  4. DURACIÓN DE LA LLAMADA vs SUSCRIPCIÓN")
print("█" * 100)

print("\n  ⚠️  NOTA: 'duration' no se conoce ANTES de la llamada.")
print("       No puede usarse como predictor en producción, pero es el indicador")
print("       más fuerte de interés del cliente durante la llamada.\n")

# Buckets con intervalos cerrado-abierto [a, b) para evitar ambigüedad
buckets = [
    (0,    60,    "< 1 min"),
    (60,   180,   "1–3 min"),
    (180,  300,   "3–5 min"),
    (300,  600,   "5–10 min"),
    (600,  1200,  "10–20 min"),
    (1200, 99999, "20+ min"),
]

print(f"  {'Bucket':<15s} {'Rango (seg)':>15s} {'n':>8s} {'%Total':>8s} {'yes':>6s} {'Conv%':>8s}")
print("  " + "-" * 65)

for lo, hi, label in buckets:
    # Intervalo cerrado-abierto: [lo, hi)
    subset = df[(df["duration"] >= lo) & (df["duration"] < hi)]
    cnt = len(subset)
    conv = subset["y_num"].mean() * 100 if cnt > 0 else 0
    pct_total = cnt / n * 100
    range_str = f"[{lo}s, {hi}s)"
    print(f"  {label:<15s} {range_str:>15s} {cnt:>8,} {pct_total:>7.1f}% {subset['y_num'].sum():>6,} {conv:>7.2f}%")

# Correlación
rho_dur, p_dur = spearmanr(df["duration"], df["y_num"])
print(f"\n  Spearman (duration × y): ρ={rho_dur:.4f}, p={p_dur:.4e}")
print("  → Correlación FUERTE y POSITIVA: llamadas más largas = más suscripciones")

print("\n  INSIGHT: La conversión escala dramáticamente con la duración:")
print("    < 1 min  → 0.02% (prácticamente 0 — llamadas no efectivas)")
print("    1-3 min  → 3.39%")
print("    5-10 min → 18.54%")
print("    20+ min  → 62.33% (2 de cada 3 suscriben)")

# ═════════════════════════════════════════════════════════════════════════════
# 5. MÉTODO DE CONTACTO (contact)
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  5. MÉTODO DE CONTACTO")
print("█" * 100)

for method in df["contact"].unique():
    subset = df[df["contact"] == method]
    conv = subset["y_num"].mean() * 100
    pct = len(subset) / n * 100
    print(f"  {method:<12s}: {conv:>6.2f}% conversión (n={len(subset):,}, {pct:.1f}% del total)")

chi2, p, _, _ = chi2_contingency(pd.crosstab(df["contact"], df["y"]))
print(f"\n  Chi² (contact × y): χ²={chi2:.2f}, p={p:.4e}")
print("\n  INSIGHT: Celular convierte 2.8× más que teléfono fijo (14.74% vs 5.23%).")
print("           Los clientes contactados por celular son más accesibles y receptivos.")

# ═════════════════════════════════════════════════════════════════════════════
# 6. HISTORIAL DE CAMPAÑAS ANTERIORES
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  6. HISTORIAL DE CAMPAÑAS ANTERIORES (pdays, previous, poutcome)")
print("█" * 100)

# 6.1 poutcome
print("\n  6.1 RESULTADO DE CAMPAÑA ANTERIOR (poutcome):")
for outcome in ["success", "failure", "nonexistent"]:
    subset = df[df["poutcome"] == outcome]
    conv = subset["y_num"].mean() * 100
    print(f"    {outcome:<15s}: {conv:>6.2f}% (n={len(subset):,})")

chi2, p, _, _ = chi2_contingency(pd.crosstab(df["poutcome"], df["y"]))
print(f"    Chi² (poutcome × y): χ²={chi2:.2f}, p={p:.4e}")

# 6.2 pdays
print("\n  6.2 DÍAS DESDE EL ÚLTIMO CONTACTO PREVIO (pdays):")
pdays_999 = df[df["pdays"] == 999]
pdays_not999 = df[df["pdays"] != 999]
conv_999 = pdays_999["y_num"].mean() * 100
conv_not999 = pdays_not999["y_num"].mean() * 100
print(f"    pdays=999 (nunca contactado):  {conv_999:.2f}% (n={len(pdays_999):,})")
print(f"    pdays≠999 (contactado antes):  {conv_not999:.2f}% (n={len(pdays_not999):,})")
print(f"    Diferencia: {conv_not999 - conv_999:+.2f}pp")

# Detalle de pdays no-999
if len(pdays_not999) > 0:
    print("\n    Detalle por rango de pdays (solo contactados previamente):")
    pdays_bins = [(0, 7, "0-7 días"), (7, 14, "7-14 días"), (14, 30, "14-30 días"), (30, 999, "30+ días")]
    for lo, hi, label in pdays_bins:
        subset = df[(df["pdays"] >= lo) & (df["pdays"] < hi)]
        if len(subset) > 0:
            conv = subset["y_num"].mean() * 100
            print(f"      {label:<15s}: {conv:.2f}% (n={len(subset):,})")

# 6.3 previous
print("\n  6.3 NÚMERO DE CONTACTOS EN CAMPAÑAS ANTERIORES (previous):")
for prev_val in range(0, 8):
    subset = df[df["previous"] == prev_val]
    if len(subset) > 0:
        conv = subset["y_num"].mean() * 100
        print(f"    previous={prev_val}: {conv:>6.2f}% (n={len(subset):,})")

print("\n  INSIGHT:")
print("    ├─ poutcome=success es el MEJOR PREDICTOR del dataset: 65.11% de conversión")
print("    ├─ Los clientes previamente contactados (pdays≠999) convierten 63.83% vs 9.26%")
print("    └─ El historial previo es MÁS importante que cualquier variable demográfica")

# ═════════════════════════════════════════════════════════════════════════════
# 7. VARIABLES MACROECONÓMICAS vs SUSCRIPCIÓN
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  7. CONTEXTO MACROECONÓMICO vs SUSCRIPCIÓN")
print("█" * 100)

macro_vars = [
    ("emp.var.rate",   "Tasa variación empleo"),
    ("cons.price.idx", "Índice precios consumo"),
    ("cons.conf.idx",  "Índice confianza consumidor"),
    ("euribor3m",      "Euribor 3 meses"),
    ("nr.employed",    "Total empleados (miles)"),
]

print(f"\n  {'Variable':<30s} {'Corr(y)':>8s} {'Mean(yes)':>12s} {'Mean(no)':>12s} {'p-value':>12s} {'Sig.':>6s}")
print("  " + "-" * 84)

for var, desc in macro_vars:
    yes_vals = df.loc[df["y"] == "yes", var]
    no_vals = df.loc[df["y"] == "no", var]
    corr = df[var].corr(df["y_num"])
    u_stat, p_val = mannwhitneyu(yes_vals, no_vals, alternative="two-sided")
    sig = "SÍ" if p_val < 0.05 else "NO"
    print(f"  {var:<30s} {corr:>+8.4f} {yes_vals.mean():>12.4f} {no_vals.mean():>12.4f} {p_val:>12.2e} {sig:>6s}")

print("\n  INTERPRETACIÓN DEL CONTEXTO MACROECONÓMICO:")
print("  ├─ TODAS las 5 variables macro son estadísticamente significativas (p ≈ 0)")
print("  ├─ euribor3m: Los clientes suscriben más cuando el euribor es BAJO (mean 2.12 vs 3.81)")  
print("  ├─ emp.var.rate: Suscripciones aumentan con empleo NEGATIVO (mean -1.23 vs +0.25)")
print("  ├─ nr.employed: Más suscripciones con MENOS empleo total (5095 vs 5176)")
print("  ├─ cons.price.idx: Ligeramente más suscripciones con precios más bajos")
print("  └─ cons.conf.idx: La confianza del consumidor tiene efecto débil (+0.055)")

print("\n  CONCLUSIÓN MACRO: Los depósitos a plazo se contratan MÁS en periodos de")
print("  incertidumbre económica (euribor bajo, empleo en descenso). Esto es lógico:")
print("  en recesión, los depósitos son refugio seguro para el ahorro.")

# Multicolinealidad macro
print("\n  ALERTA DE MULTICOLINEALIDAD ENTRE VARIABLES MACRO:")
macro_names = [v[0] for v in macro_vars]
corr_macro = df[macro_names].corr()
for i in range(len(macro_names)):
    for j in range(i + 1, len(macro_names)):
        r = corr_macro.iloc[i, j]
        if abs(r) > 0.7:
            print(f"    {macro_names[i]:<20s} × {macro_names[j]:<20s}: r={r:.4f} ⚠️ ALTA")

print("  → emp.var.rate, euribor3m y nr.employed son casi la misma variable (r>0.90)")
print("    Para modelado: usar solo 1 o aplicar PCA.")

# ═════════════════════════════════════════════════════════════════════════════
# 8. TABLA RESUMEN DE TESTS ESTADÍSTICOS
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "█" * 100)
print("  8. RESUMEN DE TODOS LOS TESTS ESTADÍSTICOS")
print("█" * 100)

print(f"\n  {'Variable':<25s} {'Test':>15s} {'Estadístico':>15s} {'p-value':>15s} {'Resultado':>15s}")
print("  " + "-" * 88)

# Numéricas → Mann-Whitney U
for var in ["duration", "campaign"] + [v[0] for v in macro_vars]:
    yes_v = df.loc[df["y"] == "yes", var]
    no_v = df.loc[df["y"] == "no", var]
    u, p = mannwhitneyu(yes_v, no_v, alternative="two-sided")
    sig = "SIGNIFICATIVO" if p < 0.05 else "no sig."
    print(f"  {var:<25s} {'Mann-Whitney':>15s} {u:>15,.0f} {p:>15.2e} {sig:>15s}")

# Categóricas → Chi²
for var in ["month", "day_of_week", "contact", "poutcome"]:
    ct = pd.crosstab(df[var], df["y"])
    chi2, p, dof, _ = chi2_contingency(ct)
    sig = "SIGNIFICATIVO" if p < 0.05 else "no sig."
    print(f"  {var:<25s} {'Chi²':>15s} {chi2:>15.2f} {p:>15.2e} {sig:>15s}")

# Spearman correlations
rho_camp, p_camp = spearmanr(df["campaign"], df["y_num"])
rho_dur, p_dur = spearmanr(df["duration"], df["y_num"])
print(f"\n  Correlaciones Spearman:")
print(f"    campaign × y: ρ={rho_camp:.4f} (p={p_camp:.2e}) → Más contactos = MENOS suscripción")
print(f"    duration × y: ρ={rho_dur:.4f} (p={p_dur:.2e}) → Más duración = MÁS suscripción")

# ═════════════════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 100)
print("  RESUMEN — Sub-tarea 1.4 Completada")
print("=" * 100)
print("""
  FACTORES DE CAMPAÑA ORDENADOS POR IMPACTO:

  1. poutcome=success     → 65.11% conversión (el mejor predictor absoluto)
  2. pdays≠999 (previo)   → 63.83% conversión (clientes con historial previo)
  3. duration (20+ min)   → 62.33% conversión (pero no es predictor a priori)
  4. contact=cellular     → 14.74% vs 5.23% telephone (2.8× mejor)
  5. month (mar/sep/oct)  → >40% conversión (pero bajo volumen)
  6. campaign ≤3          → 12.17% vs 7.27% con >3 contactos
  7. Macro (euribor bajo) → Entorno económico favorable a depósitos
  8. day_of_week          → Diferencia moderada (thu mejor, mon peor)

  RECOMENDACIONES INICIALES PARA FUTURAS CAMPAÑAS:
  ├─ Priorizar clientes con éxito en campañas anteriores
  ├─ No superar 3 intentos de contacto por cliente
  ├─ Usar celular como método de contacto preferido
  ├─ Concentrar esfuerzos en meses de menor volumen pero mayor conversión
  └─ Monitorear el entorno macroeconómico (euribor, empleo) para timing

  DATOS NO MODIFICADOS — Solo lectura.
""")
print("=" * 100)
print("  FIN — Sub-tarea 1.4: Impacto de la Campaña")
print("=" * 100)
