#!/usr/bin/env python3
"""
AIESI v6 — Data upgrade with real adoption data

New data sources:
1. TALIS 2024 (OECD): % teachers using AI — 20/27 EU countries
   Source: OECD TALIS 2024 Results, published Oct 2025
2. Eurostat 2025: % population (16-74) using generative AI
   Source: Eurostat isoc_ai_iaiu, published Dec 2025

Replaces the old adoption_score which relied on:
- teachers_ai_usage_pct from unknown mix of sources (12/27)
- ai_in_schools_access_pct from GoStudent (7/27)
- gov_ai_readiness proxy (11/27, rho=0.07)
"""

import pandas as pd

def main():
    df = pd.read_csv("data/processed/aiesi_data.csv")
    print(f"Loaded {len(df)} countries\n")

    # ================================================================
    # TALIS 2024 — % lower secondary teachers using AI (OECD, Oct 2025)
    # Sources: IndexBox, Euronews, OECD TALIS 2024 country notes
    # ================================================================
    talis_2024 = {
        'MT': 46.0, 'CZ': 46.0, 'RO': 46.0,
        'PL': 45.0,
        'AT': 39.0,
        'LT': 39.0,
        'NL': 37.0,
        'DK': 36.0,
        'LV': 35.0, 'EE': 35.0, 'ES': 35.0,
        'SE': 31.0,
        'PT': 30.0,
        'SK': 29.0,
        'FI': 27.0,
        'IT': 25.0,
        'HU': 23.0,
        'BG': 22.0,
        'FR': 14.0,
        # Belgium: Flemish 40%, French 23% → population-weighted ~33%
        'BE': 33.0,
    }
    # Missing TALIS: DE, IE, HR, SI, CY, EL, LU (did not participate or data not published)

    # ================================================================
    # Eurostat 2025 — % population 16-74 using generative AI tools
    # Source: Eurostat ddn-20251216-3, dataset isoc_ai_iaiu
    # ================================================================
    eurostat_genai = {
        'DK': 48.4, 'EE': 46.6, 'MT': 46.5, 'FI': 46.3,
        'IE': 44.9, 'NL': 44.7, 'CY': 44.2, 'GR': 44.1,
        'LU': 42.5, 'BE': 42.0, 'SE': 42.0,
        'AT': 39.4, 'PT': 38.7, 'ES': 37.9,
        'SI': 37.6, 'FR': 37.5, 'LT': 36.9,
        'CZ': 35.4, 'LV': 33.4, 'DE': 32.3,
        'SK': 30.8, 'HU': 29.6, 'HR': 27.5,
        'PL': 22.7, 'BG': 22.5, 'IT': 19.9, 'RO': 17.8,
    }

    # Update teachers_ai_usage_pct with TALIS 2024 data
    print("=== UPDATING TALIS 2024 DATA ===")
    updated = 0
    added = 0
    for _, row in df.iterrows():
        cc = row['country_code']
        if cc in talis_2024:
            old = row['teachers_ai_usage_pct']
            new = talis_2024[cc]
            if pd.isna(old):
                print(f"  {row['country']:15s} NEW: {new}%")
                added += 1
            elif old != new:
                print(f"  {row['country']:15s} {old}% → {new}%")
                updated += 1
            df.loc[df['country_code'] == cc, 'teachers_ai_usage_pct'] = new
    print(f"  Added: {added}, Updated: {updated}")

    # Add eurostat_genai_pct column
    print("\n=== ADDING EUROSTAT 2025 GENAI DATA ===")
    df['eurostat_genai_pct'] = df['country_code'].map(eurostat_genai)
    missing = df[df['eurostat_genai_pct'].isna()]['country'].tolist()
    if missing:
        print(f"  WARNING: Missing Eurostat data for: {missing}")
    else:
        print(f"  All 27 countries have Eurostat GenAI data")

    # Show comparison
    print("\n=== DATA OVERVIEW ===")
    print(f"{'Country':15s} {'TALIS':>8s} {'Eurostat':>10s}")
    for _, r in df.sort_values('country').iterrows():
        t = f"{r['teachers_ai_usage_pct']:.0f}%" if pd.notna(r['teachers_ai_usage_pct']) else "—"
        e = f"{r['eurostat_genai_pct']:.1f}%" if pd.notna(r['eurostat_genai_pct']) else "—"
        print(f"  {r['country']:15s} {t:>8s} {e:>10s}")

    has_talis = df['teachers_ai_usage_pct'].notna().sum()
    has_eurostat = df['eurostat_genai_pct'].notna().sum()
    print(f"\n  TALIS coverage: {has_talis}/27")
    print(f"  Eurostat coverage: {has_eurostat}/27")
    print(f"  Both sources: {(df['teachers_ai_usage_pct'].notna() & df['eurostat_genai_pct'].notna()).sum()}/27")

    # Save updated raw data
    df.to_csv("data/processed/aiesi_data.csv", index=False)
    print(f"\nSaved: data/processed/aiesi_data.csv")

    return df


if __name__ == '__main__':
    main()
