#!/usr/bin/env python3
"""
AIESI Index v6 — Data Recalculation

Two-dimensional index with verified adoption data:
1. edu_policy_coverage (50%) — checklist of AI-in-education policies
2. adoption_score (50%) — from two independent sources:
   a) TALIS 2024 (OECD): % teachers using AI (20/27 EU countries)
   b) Eurostat 2025: % population using generative AI (27/27)

No more proxy imputation from gov_ai_readiness (rho=0.07).
media_score retained in CSV as informational column only.
"""

import pandas as pd
import numpy as np


def minmax(s):
    """Min-max normalize to [0,1], preserving NaN."""
    v = s.dropna()
    if len(v) < 2 or v.max() == v.min():
        return s.apply(lambda x: 0.5 if pd.notna(x) else np.nan)
    return (s - v.min()) / (v.max() - v.min())


def spearman(x, y):
    """Spearman rank correlation using pandas (no scipy needed)."""
    return x.rank().corr(y.rank())


def main():
    df = pd.read_csv("data/processed/aiesi_data.csv")
    n = len(df)
    print(f"Loaded {n} countries\n")

    # ================================================================
    # 1. ADOPTION SCORE — two independent sources
    # ================================================================
    has_talis = df['teachers_ai_usage_pct'].notna()
    has_eurostat = df['eurostat_genai_pct'].notna()

    print("=== ADOPTION DATA AVAILABILITY ===")
    print(f"  TALIS 2024 (teachers AI %):     {has_talis.sum()}/{n}")
    print(f"  Eurostat 2025 (GenAI pop %):    {has_eurostat.sum()}/{n}")
    print(f"  Both sources:                   {(has_talis & has_eurostat).sum()}/{n}")

    # Normalize each to [0,1]
    talis_norm = minmax(df['teachers_ai_usage_pct'])
    eurostat_norm = minmax(df['eurostat_genai_pct'])

    # Cross-validate: correlation between the two indicators
    both = has_talis & has_eurostat
    if both.sum() >= 5:
        cross_rho = spearman(talis_norm[both], eurostat_norm[both])
        print(f"\n  Cross-validation: rho(TALIS_norm, Eurostat_norm) = {cross_rho:.3f}")
        print(f"  (n={both.sum()} countries with both sources)")

    # Adoption = mean of available normalized indicators
    adoption = pd.Series(np.nan, index=df.index)

    # Both sources available: average
    adoption[both] = (talis_norm[both] + eurostat_norm[both]) / 2

    # Only Eurostat (7 countries: DE, IE, HR, SI, CY, EL, LU)
    only_eurostat = ~has_talis & has_eurostat
    adoption[only_eurostat] = eurostat_norm[only_eurostat]

    df['adoption_score'] = adoption.round(2)

    # Quality flag
    df['adoption_method'] = 'eurostat_only'
    df.loc[both, 'adoption_method'] = 'both'

    print(f"\n  Method breakdown:")
    print(f"    both (TALIS + Eurostat): {both.sum()}")
    print(f"    eurostat_only:           {only_eurostat.sum()}")

    print(f"\n  Country details:")
    for _, r in df.sort_values('adoption_score', ascending=False).iterrows():
        t = f"T={r['teachers_ai_usage_pct']:.0f}%" if pd.notna(r['teachers_ai_usage_pct']) else "T=—"
        e = f"E={r['eurostat_genai_pct']:.0f}%" if pd.notna(r['eurostat_genai_pct']) else "E=—"
        print(f"    {r['country']:15s} → {r['adoption_score']:.2f}  "
              f"[{r['adoption_method']:14s}]  ({t}, {e})")

    # ================================================================
    # 2. OVERALL SCORE — two dimensions, 50/50
    # ================================================================
    W_POLICY = 0.5
    W_ADOPTION = 0.5

    df['overall_score'] = (
        W_POLICY * df['edu_policy_coverage'] +
        W_ADOPTION * df['adoption_score']
    ).round(2)

    print(f"\n=== SCORES (P:{W_POLICY} A:{W_ADOPTION}) ===")
    for _, r in df.sort_values('overall_score', ascending=False).iterrows():
        print(f"  {r['country']:15s}  overall={r['overall_score']:.2f}  "
              f"(P:{r['edu_policy_coverage']:.1f} A:{r['adoption_score']:.2f})")

    # ================================================================
    # 3. SENSITIVITY ANALYSIS — 2D weight sweep
    # ================================================================
    base_rank = df['overall_score'].rank(ascending=False)

    sa_results = []
    for wp in np.arange(0.20, 0.81, 0.05):
        wa = round(1.0 - wp, 2)
        wp = round(wp, 2)
        scores = wp * df['edu_policy_coverage'] + wa * df['adoption_score']
        new_rank = scores.rank(ascending=False)
        rho = spearman(base_rank, new_rank)
        sa_results.append({
            'w_policy': wp, 'w_adoption': wa,
            'spearman_rho': round(rho, 3)
        })

    sa_df = pd.DataFrame(sa_results)
    print(f"\n=== SENSITIVITY ANALYSIS ({len(sa_df)} weight combinations) ===")
    print(f"  Spearman rho: min={sa_df['spearman_rho'].min():.3f}, "
          f"mean={sa_df['spearman_rho'].mean():.3f}, "
          f"max={sa_df['spearman_rho'].max():.3f}")
    print(f"  Combinations with rho >= 0.95: {(sa_df['spearman_rho'] >= 0.95).sum()}/{len(sa_df)}")
    print(f"  Combinations with rho >= 0.90: {(sa_df['spearman_rho'] >= 0.90).sum()}/{len(sa_df)}")

    # Top-5 stability check
    top5_base = set(df.nlargest(5, 'overall_score')['country'])
    stable_count = 0
    for _, sr in sa_df.iterrows():
        scores = sr['w_policy'] * df['edu_policy_coverage'] + sr['w_adoption'] * df['adoption_score']
        top5_new = set(df.loc[scores.nlargest(5).index, 'country'])
        if top5_base == top5_new:
            stable_count += 1
    print(f"  Top-5 identical across combinations: {stable_count}/{len(sa_df)}")

    # ================================================================
    # 4. CORRELATION (Spearman) — two dimensions
    # ================================================================
    rho_dims = spearman(df['edu_policy_coverage'], df['adoption_score'])
    print(f"\n=== DIMENSION CORRELATION ===")
    print(f"  Spearman rho(policy, adoption) = {rho_dims:.3f}")

    # ================================================================
    # 5. DESCRIPTIVE STATISTICS
    # ================================================================
    print(f"\n=== DESCRIPTIVE STATISTICS ===")
    for col, label in [
        ('overall_score', 'Overall'),
        ('edu_policy_coverage', 'Policy coverage'),
        ('adoption_score', 'Adoption'),
    ]:
        s = df[col]
        print(f"  {label:18s}: M={s.mean():.2f}, SD={s.std():.2f}, "
              f"min={s.min():.2f}, max={s.max():.2f}, median={s.median():.2f}")

    # ================================================================
    # 6. CLEAN OUTPUT
    # ================================================================
    out_cols = [
        'country', 'country_code',
        'has_ai_strategy', 'ai_strategy_year', 'ai_budget_eur_millions',
        'has_edu_ai_strategy', 'ai_in_curriculum', 'ai_curriculum_type',
        'teacher_ai_training_program', 'edu_ai_pilots',
        'teachers_ai_usage_pct', 'eurostat_genai_pct',
        'ai_in_schools_access_pct', 'gov_ai_readiness_score',
        'edu_policy_coverage', 'adoption_score', 'media_score', 'overall_score',
        'adoption_method', 'notes'
    ]

    out = df[out_cols].copy()
    out = out.sort_values('overall_score', ascending=False).reset_index(drop=True)
    out.to_csv("data/processed/aiesi_data.csv", index=False)
    print(f"\nSaved: data/processed/aiesi_data.csv ({len(out)} rows, {len(out_cols)} cols)")

    sa_df.to_csv("data/processed/sensitivity_analysis.csv", index=False)
    print(f"Saved: data/processed/sensitivity_analysis.csv ({len(sa_df)} rows)")

    return out, sa_df


if __name__ == '__main__':
    main()
