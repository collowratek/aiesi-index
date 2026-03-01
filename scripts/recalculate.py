#!/usr/bin/env python3
"""
AIESI Index v5 — Data Recalculation

Two-dimensional index:
1. edu_policy_coverage (50%) — checklist of AI-in-education policies
2. adoption_score (50%) — teacher AI usage + school AI access

media_score retained in CSV as informational column but excluded from
overall_score due to fundamental validity issue (single English-language
Google Trends query → measures anglophone bias, not actual media salience).
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
    # 1. ADOPTION SCORE — transparent recalculation
    # ================================================================
    # Available indicators
    has_teachers = df['teachers_ai_usage_pct'].notna()
    has_access = df['ai_in_schools_access_pct'].notna()
    has_any = has_teachers | has_access
    has_both = has_teachers & has_access
    has_neither = ~has_any

    print("=== ADOPTION DATA AVAILABILITY ===")
    print(f"  teachers_ai_usage_pct:      {has_teachers.sum()}/{n}")
    print(f"  ai_in_schools_access_pct:   {has_access.sum()}/{n}")
    print(f"  Both indicators:            {has_both.sum()}/{n}")
    print(f"  At least one:               {has_any.sum()}/{n}")
    print(f"  Neither (need proxy):       {has_neither.sum()}/{n}")

    # Normalize available indicators to [0,1]
    teachers_norm = minmax(df['teachers_ai_usage_pct'])
    access_norm = minmax(df['ai_in_schools_access_pct'])

    # Pairwise mean of available normalized indicators
    adoption = pd.Series(np.nan, index=df.index)
    adoption[has_both] = (teachers_norm[has_both] + access_norm[has_both]) / 2
    only_t = has_teachers & ~has_access
    only_a = has_access & ~has_teachers
    adoption[only_t] = teachers_norm[only_t]
    adoption[only_a] = access_norm[only_a]

    # --- Proxy imputation for missing countries ---
    # Use gov_ai_readiness_score as proxy (available for all 27)
    gov_norm = minmax(df['gov_ai_readiness_score'])

    # Validate proxy: Spearman correlation with measured adoption
    measured = adoption.notna()
    proxy_rho = spearman(adoption[measured], gov_norm[measured])
    print(f"\n  Proxy validation: rho(measured_adoption, gov_readiness) = {proxy_rho:.3f}")
    print(f"  (n={measured.sum()} countries with measured adoption)")

    # Scale proxy to match measured adoption distribution
    m_mean = adoption[measured].mean()
    m_std = adoption[measured].std()
    g_mean = gov_norm[measured].mean()
    g_std = gov_norm[measured].std()

    if g_std > 0:
        proxy_scaled = m_mean + (gov_norm - g_mean) * (m_std / g_std)
    else:
        proxy_scaled = gov_norm
    proxy_scaled = proxy_scaled.clip(0, 1)

    # Fill missing
    adoption[has_neither] = proxy_scaled[has_neither]
    df['adoption_score'] = adoption.round(2)

    # Quality flag
    df['adoption_method'] = 'proxy'
    df.loc[has_both, 'adoption_method'] = 'measured'
    df.loc[has_any & ~has_both, 'adoption_method'] = 'partial'

    print(f"\n  Method breakdown:")
    print(f"    measured (both indicators): {has_both.sum()}")
    print(f"    partial (one indicator):    {(has_any & ~has_both).sum()}")
    print(f"    proxy (gov_readiness):      {has_neither.sum()}")

    print(f"\n  Country details:")
    for _, r in df.sort_values('adoption_score', ascending=False).iterrows():
        t = f"t={r['teachers_ai_usage_pct']:.0f}%" if pd.notna(r['teachers_ai_usage_pct']) else "t=NA"
        a = f"a={r['ai_in_schools_access_pct']:.0f}%" if pd.notna(r['ai_in_schools_access_pct']) else "a=NA"
        print(f"    {r['country']:15s} → {r['adoption_score']:.2f}  [{r['adoption_method']:8s}]  ({t}, {a})")

    # ================================================================
    # 2. OVERALL SCORE — two dimensions, 50/50
    # ================================================================
    # media_score excluded: single English Google Trends query measures
    # anglophone bias, not actual media salience (Ireland = 1.0, 10 countries = 0.0)
    W_POLICY = 0.5
    W_ADOPTION = 0.5

    df['overall_score'] = (
        W_POLICY * df['edu_policy_coverage'] +
        W_ADOPTION * df['adoption_score']
    ).round(2)

    print(f"\n=== SCORES (P:{W_POLICY} A:{W_ADOPTION}, media excluded) ===")
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
    # 6. CLEAN OUTPUT — media_score kept as informational column
    # ================================================================
    out_cols = [
        'country', 'country_code',
        'has_ai_strategy', 'ai_strategy_year', 'ai_budget_eur_millions',
        'has_edu_ai_strategy', 'ai_in_curriculum', 'ai_curriculum_type',
        'teacher_ai_training_program', 'edu_ai_pilots',
        'teachers_ai_usage_pct', 'ai_in_schools_access_pct',
        'gov_ai_readiness_score',
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
