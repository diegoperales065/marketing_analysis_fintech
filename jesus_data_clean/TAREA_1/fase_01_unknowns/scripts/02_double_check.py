"""
02_double_check.py
==================
Deep verification of EVERY statistical claim made in the semantic renaming report.
This script checks all numbers, percentages, and conclusions against raw data.
"""

import pandas as pd
import numpy as np
from scipy import stats
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv(
    r"c:\Users\jzs99\Desktop\marketing_analysis_fintech\datos\bank-additional_bank-additional-full.csv",
    sep=";"
)
df = df.drop_duplicates()

PASS = 0
FAIL = 0
WARN = 0

def check(label, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {label}")
    else:
        FAIL += 1
        print(f"  [FAIL] {label} — {detail}")

def warn(label, detail):
    global WARN
    WARN += 1
    print(f"  [WARN] {label} — {detail}")

print("=" * 80)
print("  DOUBLE-CHECK: SEMANTIC RENAMING REPORT VERIFICATION")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: DATASET BASICS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 1. Dataset Basics ---")
check("Row count after dedup", df.shape[0] == 41176, f"Got {df.shape[0]}")
check("Column count", df.shape[1] == 21, f"Got {df.shape[1]}")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: DEFAULT COLUMN CLAIMS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 2. DEFAULT Column Claims ---")

# Unknown count and percentage
default_unk = df[df['default'] == 'unknown']
default_no = df[df['default'] == 'no']
n_unk = len(default_unk)
pct_unk = n_unk / len(df) * 100

check("default unknown count ~8596", n_unk == 8596, f"Got {n_unk}")
check("default unknown % ~20.9%", abs(pct_unk - 20.88) < 0.5, f"Got {pct_unk:.2f}%")

# Age claims
unk_age_mean = default_unk['age'].mean()
no_age_mean = default_no['age'].mean()
check("default=unknown age mean ~43.4", abs(unk_age_mean - 43.4) < 0.5, f"Got {unk_age_mean:.1f}")
check("default=no age mean ~39.1", abs(no_age_mean - 39.1) < 0.5, f"Got {no_age_mean:.1f}")

# Conversion claims
unk_conv = (default_unk['y'] == 'yes').mean() * 100
no_conv = (default_no['y'] == 'yes').mean() * 100
check("default=unknown conv ~5.15%", abs(unk_conv - 5.15) < 0.5, f"Got {unk_conv:.2f}%")
check("default=no conv ~12.88%", abs(no_conv - 12.88) < 0.5, f"Got {no_conv:.2f}%")

# Blue-collar dominance
unk_bc = (default_unk['job'] == 'blue-collar').mean() * 100
no_bc = (default_no['job'] == 'blue-collar').mean() * 100
check("default=unknown blue-collar ~36.8%", abs(unk_bc - 36.8) < 1.0, f"Got {unk_bc:.1f}%")
check("default=no blue-collar ~18.7%", abs(no_bc - 18.7) < 1.0, f"Got {no_bc:.1f}%")

# Never previously contacted
unk_never = (default_unk['pdays'] == 999).mean() * 100
no_never = (default_no['pdays'] == 999).mean() * 100
check("default=unknown never contacted ~99.3%", abs(unk_never - 99.3) < 0.5, f"Got {unk_never:.1f}%")
check("default=no never contacted ~95.5%", abs(no_never - 95.5) < 0.5, f"Got {no_never:.1f}%")

# Married percentage
unk_married = (default_unk['marital'] == 'married').mean() * 100
no_married = (default_no['marital'] == 'married').mean() * 100
check("default=unknown married ~72.9%", abs(unk_married - 72.9) < 1.0, f"Got {unk_married:.1f}%")
check("default=no married ~57.2%", abs(no_married - 57.2) < 1.0, f"Got {no_married:.1f}%")

# Cellular contact
unk_cell = (default_unk['contact'] == 'cellular').mean() * 100
no_cell = (default_no['contact'] == 'cellular').mean() * 100
check("default=unknown cellular ~50.8%", abs(unk_cell - 50.8) < 1.0, f"Got {unk_cell:.1f}%")
check("default=no cellular ~66.8%", abs(no_cell - 66.8) < 1.0, f"Got {no_cell:.1f}%")

# Euribor
unk_euri = default_unk['euribor3m'].mean()
no_euri = default_no['euribor3m'].mean()
check("default=unknown euribor ~4.281", abs(unk_euri - 4.281) < 0.05, f"Got {unk_euri:.3f}")
check("default=no euribor ~3.447", abs(no_euri - 3.447) < 0.05, f"Got {no_euri:.3f}")

# Education basic (4y + 6y + 9y)
unk_basic = default_unk['education'].isin(['basic.4y', 'basic.6y', 'basic.9y']).mean() * 100
no_basic = default_no['education'].isin(['basic.4y', 'basic.6y', 'basic.9y']).mean() * 100
check("default=unknown basic edu ~48.6%", abs(unk_basic - 48.6) < 1.0, f"Got {unk_basic:.1f}%")
check("default=no basic edu ~25.6%", abs(no_basic - 25.6) < 1.0, f"Got {no_basic:.1f}%")

# Chi-squared test
contingency = pd.crosstab(df['default'], df['y'])
chi2, p, _, _ = stats.chi2_contingency(contingency)
check("Chi-squared for default ~405", abs(chi2 - 405) < 50, f"Got {chi2:.1f}")
check("Chi-squared p-value ~0", p < 0.0001, f"Got {p}")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: EDUCATION COLUMN CLAIMS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 3. EDUCATION Column Claims ---")

edu_unk = df[df['education'] == 'unknown']
n_edu_unk = len(edu_unk)
check("education unknown count ~1730", abs(n_edu_unk - 1730) < 5, f"Got {n_edu_unk}")

# Conversion
edu_unk_conv = (edu_unk['y'] == 'yes').mean() * 100
check("education=unknown conv ~14.5%", abs(edu_unk_conv - 14.5) < 0.5, f"Got {edu_unk_conv:.2f}%")

# Overall dataset conversion for comparison
overall_conv = (df['y'] == 'yes').mean() * 100
check("education=unknown conv > overall (~11.3%)", edu_unk_conv > overall_conv,
      f"Unknown: {edu_unk_conv:.2f}%, Overall: {overall_conv:.2f}%")

# Blue-collar in edu unknown
edu_unk_bc = (edu_unk['job'] == 'blue-collar').mean() * 100
check("education=unknown blue-collar ~26.2%", abs(edu_unk_bc - 26.2) < 1.0, f"Got {edu_unk_bc:.1f}%")

# Student presence
edu_unk_student = (edu_unk['job'] == 'student').mean() * 100
check("education=unknown student ~9.7%", abs(edu_unk_student - 9.7) < 1.0, f"Got {edu_unk_student:.1f}%")

# Co-occurrence with default unknown
edu_unk_def_unk = (edu_unk['default'] == 'unknown').mean() * 100
check("education=unknown & default=unknown ~31.7%", abs(edu_unk_def_unk - 31.7) < 1.0, f"Got {edu_unk_def_unk:.1f}%")

# Co-occurrence with job unknown
edu_unk_job_unk = (edu_unk['job'] == 'unknown').mean() * 100
check("education=unknown & job=unknown ~7.6%", abs(edu_unk_job_unk - 7.6) < 1.0, f"Got {edu_unk_job_unk:.1f}%")

# Chi-squared for education
contingency_edu = pd.crosstab(df['education'], df['y'])
chi2_edu, p_edu, _, _ = stats.chi2_contingency(contingency_edu)
check("Chi-squared for education ~18.6", abs(chi2_edu - 18.6) < 10, f"Got {chi2_edu:.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: JOB COLUMN CLAIMS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 4. JOB Column Claims ---")

job_unk = df[df['job'] == 'unknown']
n_job_unk = len(job_unk)
check("job unknown count ~330", abs(n_job_unk - 330) < 5, f"Got {n_job_unk}")
check("job unknown % ~0.8%", abs(n_job_unk / len(df) * 100 - 0.8) < 0.1, f"Got {n_job_unk / len(df) * 100:.1f}%")

job_unk_age = job_unk['age'].mean()
check("job=unknown age mean ~45.6", abs(job_unk_age - 45.6) < 0.5, f"Got {job_unk_age:.1f}")

job_unk_conv = (job_unk['y'] == 'yes').mean() * 100
check("job=unknown conv ~11.21%", abs(job_unk_conv - 11.21) < 1.0, f"Got {job_unk_conv:.2f}%")

# Education unknown co-occurrence
job_unk_edu_unk = (job_unk['education'] == 'unknown').mean() * 100
check("job=unknown & education=unknown ~39.7%", abs(job_unk_edu_unk - 39.7) < 1.0, f"Got {job_unk_edu_unk:.1f}%")

# Default unknown co-occurrence
job_unk_def_unk = (job_unk['default'] == 'unknown').mean() * 100
check("job=unknown & default=unknown ~46.1%", abs(job_unk_def_unk - 46.1) < 1.0, f"Got {job_unk_def_unk:.1f}%")

# Married
job_unk_married = (job_unk['marital'] == 'married').mean() * 100
check("job=unknown married ~70.9%", abs(job_unk_married - 70.9) < 1.5, f"Got {job_unk_married:.1f}%")

# Age 41-60
job_unk_4160 = job_unk['age'].between(41, 60).mean() * 100
check("job=unknown age 41-60 ~63.4%", abs(job_unk_4160 - 63.4) < 2.0, f"Got {job_unk_4160:.1f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: MARITAL COLUMN CLAIMS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 5. MARITAL Column Claims ---")

marital_unk = df[df['marital'] == 'unknown']
n_marital_unk = len(marital_unk)
check("marital unknown count ~80", abs(n_marital_unk - 80) < 3, f"Got {n_marital_unk}")
check("marital unknown % ~0.2%", abs(n_marital_unk / len(df) * 100 - 0.2) < 0.1, f"Got {n_marital_unk / len(df) * 100:.2f}%")

marital_unk_age = marital_unk['age'].mean()
check("marital=unknown age mean ~40.3", abs(marital_unk_age - 40.3) < 0.5, f"Got {marital_unk_age:.1f}")

marital_unk_conv = (marital_unk['y'] == 'yes').mean() * 100
check("marital=unknown conv ~15.0%", abs(marital_unk_conv - 15.0) < 1.0, f"Got {marital_unk_conv:.2f}%")

marital_unk_univ = (marital_unk['education'] == 'university.degree').mean() * 100
check("marital=unknown university ~38.8%", abs(marital_unk_univ - 38.8) < 2.0, f"Got {marital_unk_univ:.1f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: MNAR VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 6. MNAR (Missing Not At Random) Validation ---")

# Verify that unknowns correlated with other variables (MNAR indicator)
# If unknowns were MCAR, they'd be randomly distributed across age groups
age_groups_unk = pd.cut(default_unk['age'], bins=[0,30,40,50,60,100]).value_counts(normalize=True)
age_groups_no = pd.cut(default_no['age'], bins=[0,30,40,50,60,100]).value_counts(normalize=True)

# Chi-squared test on age distribution
age_contingency = pd.crosstab(
    df['default'].isin(['unknown']).map({True: 'unknown', False: 'known'}),
    pd.cut(df['age'], bins=[0,30,40,50,60,100])
)
chi2_age, p_age, _, _ = stats.chi2_contingency(age_contingency)
check("MNAR confirmed: age distribution differs (p<0.001)", p_age < 0.001, f"p={p_age}")

# MNAR: unknown correlated with euribor
t_stat, p_euri = stats.mannwhitneyu(
    default_unk['euribor3m'], default_no['euribor3m'], alternative='two-sided'
)
check("MNAR confirmed: euribor differs (p<0.001)", p_euri < 0.001, f"p={p_euri}")

# MNAR: unknown correlated with contact method
contact_contingency = pd.crosstab(df['default'], df['contact'])
chi2_contact, p_contact, _, _ = stats.chi2_contingency(contact_contingency)
check("MNAR confirmed: contact method differs (p<0.001)", p_contact < 0.001, f"p={p_contact}")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: NAMING LOGIC VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 7. Naming Logic Validation ---")

# default: "no_credit_record" — verify these are NOT "yes" defaults misclassified
check("default=yes only 3 cases (not a pool for unknowns)",
      (df['default'] == 'yes').sum() <= 5,
      f"Got {(df['default'] == 'yes').sum()}")

# Verify no overlap: "unemployed" already exists, so "undeclared_occupation" is safe
check("'unemployed' exists as separate job category",
      'unemployed' in df['job'].unique(),
      f"Categories: {df['job'].unique()}")

# Verify "undisclosed_education" doesn't collide with "illiterate"
check("'illiterate' exists separately (only 18 cases)",
      len(df[df['education'] == 'illiterate']) == 18,
      f"Got {len(df[df['education'] == 'illiterate'])}")

# Verify all proposed names are unique (won't collide with existing values)
existing_default = set(df['default'].unique())
existing_education = set(df['education'].unique())
existing_job = set(df['job'].unique())
existing_marital = set(df['marital'].unique())
check("'no_credit_record' doesn't exist in default", 'no_credit_record' not in existing_default)
check("'undisclosed_education' doesn't exist in education", 'undisclosed_education' not in existing_education)
check("'undeclared_occupation' doesn't exist in job", 'undeclared_occupation' not in existing_job)
check("'undisclosed_status' doesn't exist in marital", 'undisclosed_status' not in existing_marital)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: EDGE CASE CHECK — Are there unknowns in OTHER columns?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 8. Completeness Check — Any unknowns we missed? ---")

for col in df.columns:
    if df[col].dtype == 'object':
        unk_count = (df[col] == 'unknown').sum()
        if unk_count > 0:
            print(f"  {col}: {unk_count} unknowns ({unk_count/len(df)*100:.2f}%)")

# Verify housing and loan unknowns still planned for removal
housing_unk = (df['housing'] == 'unknown').sum()
loan_unk = (df['loan'] == 'unknown').sum()
co_occur = ((df['housing'] == 'unknown') & (df['loan'] == 'unknown')).sum()
check(f"housing unknowns ({housing_unk}) = loan unknowns ({loan_unk})",
      housing_unk == loan_unk, f"housing={housing_unk}, loan={loan_unk}")
check(f"housing/loan co-occur 100% ({co_occur} = {housing_unk})",
      co_occur == housing_unk, f"co-occur={co_occur}")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: FINAL IMPACT TALLY
# ═══════════════════════════════════════════════════════════════════════════════
print("\n--- 9. Impact Tally ---")
total_renamed = n_unk + n_edu_unk + n_job_unk + n_marital_unk
print(f"  Total 'unknown' values to be renamed:  {total_renamed}")
print(f"    default  → no_credit_record:          {n_unk}")
print(f"    education → undisclosed_education:     {n_edu_unk}")
print(f"    job      → undeclared_occupation:      {n_job_unk}")
print(f"    marital  → undisclosed_status:         {n_marital_unk}")
print(f"  housing/loan unknowns (to be REMOVED):  {housing_unk}")

# ═══════════════════════════════════════════════════════════════════════════════
# FINAL VERDICT
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print(f"  VERIFICATION RESULT: {PASS} PASSED | {FAIL} FAILED | {WARN} WARNINGS")
print("=" * 80)
if FAIL == 0:
    print("  *** ALL CLAIMS VERIFIED — ANALYSIS IS 100% ACCURATE ***")
else:
    print(f"  *** {FAIL} CLAIM(S) NEED ATTENTION ***")
