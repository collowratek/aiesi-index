#!/usr/bin/env python3
"""
AIESI Index v4 — Data Recalculation

Addresses academic review:
1. Adoption_score: transparent calculation, documented imputation
2. Media_score: reduced weight (33% → 20%)
3. Edu_policy: renamed to edu_policy_coverage (checklist, not quality)
4. Legacy columns removed
5. Sensitivity analysis: actual Spearman rank correlations
6. Descriptive statistics with SD
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
    # 2. RENAME edu_policy_score → edu_policy_coverage
    # ================================================================
    df['edu_policy_coverage'] = df['edu_policy_score']

    # ================================================================
    # 3. REWEIGHT: 40% policy, 40% adoption, 20% media
    # ================================================================
    W_POLICY = 0.4
    W_ADOPTION = 0.4
    W_MEDIA = 0.2

    df['overall_score'] = (
        W_POLICY * df['edu_policy_coverage'] +
        W_ADOPTION * df['adoption_score'] +
        W_MEDIA * df['media_score']
    ).round(2)

    print(f"\n=== REWEIGHTED SCORES (P:{W_POLICY} A:{W_ADOPTION} M:{W_MEDIA}) ===")
    for _, r in df.sort_values('overall_score', ascending=False).iterrows():
        print(f"  {r['country']:15s}  overall={r['overall_score']:.2f}  "
              f"(P:{r['edu_policy_coverage']:.1f} A:{r['adoption_score']:.2f} M:{r['media_score']:.2f})")

    # ================================================================
    # 4. SENSITIVITY ANALYSIS — actual computation
    # ================================================================
    base_rank = df['overall_score'].rank(ascending=False)

    sa_results = []
    for dp in np.arange(-0.15, 0.16, 0.05):
        for da in np.arange(-0.15, 0.16, 0.05):
            dm = -(dp + da)
            w = [round(W_POLICY + dp, 2), round(W_ADOPTION + da, 2), round(W_MEDIA + dm, 2)]
            if min(w) < 0.05 or max(w) > 0.70:
                continue
            scores = (w[0] * df['edu_policy_coverage'] +
                      w[1] * df['adoption_score'] +
                      w[2] * df['media_score'])
            new_rank = scores.rank(ascending=False)
            rho = spearman(base_rank, new_rank)
            sa_results.append({
                'w_policy': w[0], 'w_adoption': w[1], 'w_media': w[2],
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
        scores = (sr['w_policy'] * df['edu_policy_coverage'] +
                  sr['w_adoption'] * df['adoption_score'] +
                  sr['w_media'] * df['media_score'])
        top5_new = set(df.loc[scores.nlargest(5).index, 'country'])
        if top5_base == top5_new:
            stable_count += 1
    print(f"  Top-5 identical across combinations: {stable_count}/{len(sa_df)}")

    # ================================================================
    # 5. CORRELATION MATRIX (Spearman)
    # ================================================================
    dims = df[['edu_policy_coverage', 'adoption_score', 'media_score']]
    corr = dims.corr(method='spearman')
    print(f"\n=== SPEARMAN CORRELATION MATRIX ===")
    print(corr.round(3).to_string())

    # ================================================================
    # 6. DESCRIPTIVE STATISTICS
    # ================================================================
    print(f"\n=== DESCRIPTIVE STATISTICS ===")
    for col, label in [
        ('overall_score', 'Overall'),
        ('edu_policy_coverage', 'Policy coverage'),
        ('adoption_score', 'Adoption'),
        ('media_score', 'Media')
    ]:
        s = df[col]
        print(f"  {label:18s}: M={s.mean():.2f}, SD={s.std():.2f}, "
              f"min={s.min():.2f}, max={s.max():.2f}, median={s.median():.2f}")

    # ================================================================
    # 7. CLEAN OUTPUT — remove legacy columns
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
