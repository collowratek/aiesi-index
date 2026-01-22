# AIESI Data Collection - AI in Education Salience Index

## Overview

Tato složka obsahuje data sesbíraná pro vytvoření heatmapy znázorňující, jak moc je AI ve vzdělávání "velkým tématem" v jednotlivých zemích EU27.

**Datum sběru:** 2025-01-22

## Struktura dat

```
data/
├── raw/                    # Surová data (prázdné - použity API zdroje)
│   ├── policy/
│   ├── media/
│   └── adoption/
├── processed/
│   ├── aiesi_data.csv     # Hlavní datový soubor (CSV)
│   └── aiesi_data.json    # Strukturovaná verze (JSON)
└── README.md              # Tento soubor
```

## Popis sloupců (CSV)

| Sloupec | Popis | Zdroj |
|---------|-------|-------|
| country | Název země | - |
| country_code | ISO 3166-1 alpha-2 kód | - |
| has_ai_strategy | Má národní AI strategii (0/1) | OECD AI Policy Observatory |
| ai_strategy_year | Rok přijetí AI strategie | OECD AI Policy Observatory |
| ai_budget_eur_millions | Rozpočet na AI v milionech EUR | OECD 2024 Report |
| ai_budget_dedicated | Má dedikovaný AI rozpočet (0/1) | OECD 2024 Report |
| teachers_ai_usage_pct | % učitelů používajících AI | TALIS 2024 |
| teachers_ai_training_pct | % učitelů s AI školením | TALIS 2024 |
| gov_ai_readiness_score | Skóre vládní AI připravenosti | Oxford Insights 2025 |
| gov_ai_readiness_rank | Pořadí ve vládní AI připravenosti | Oxford Insights 2025 |
| edu_ai_index_score | Skóre vzdělávacího AI indexu | GoStudent 2025 |
| edtech_startups_pct | % EdTech startupů v Evropě | HolonIQ 2025 |
| ai_in_schools_access_pct | % studentů s přístupem k AI | GoStudent 2024 Report |
| ai_firm_adoption_pct | % firem používajících AI | Eurostat 2024 |
| ict_graduates_pct | % ICT absolventů | DESI 2024 |
| policy_score | Normalizované skóre politiky (0-1) | Kalkulované |
| adoption_score | Normalizované skóre adopce (0-1) | Kalkulované |
| overall_score | Celkové AIESI skóre (0-1) | Kalkulované |
| data_quality | Kvalita dat (low/medium/high) | - |
| notes | Poznámky a dodatečné informace | - |

## Hlavní zdroje dat

### 1. Policy Data (Politická priorita)

- **OECD AI Policy Observatory** - https://oecd.ai/en/
- **OECD Progress in Implementing EU Coordinated Plan on AI (2024)** - Hlavní zdroj pro národní strategie a rozpočty
- **Oxford Insights Government AI Readiness Index 2025** - https://oxfordinsights.com/ai-readiness/government-ai-readiness-index-2025/
- **GoStudent European Educational AI Index 2025** - https://www.gostudent.org/en-gb/blog/which-country-is-best-for-ai-in-education

### 2. Adoption Data (Praktické nasazení)

- **OECD TALIS 2024** - https://www.oecd.org/en/publications/results-from-talis-2024_90df6235-en.html
  - Procento učitelů používajících AI: rozsah 14% (Francie) až 52% (Albánie)
  - EU-22 průměr: 32%
  - OECD průměr: 36%

- **GoStudent Future of Education Report 2024** - Data o přístupu studentů k AI ve školách
- **HolonIQ Europe EdTech 200 (2025)** - Distribuce EdTech startupů
- **Eurostat/DESI 2024** - Adopce AI firmami, ICT absolventi

### 3. Media Data (Mediální pozornost)

- Proxy data odvozená z policy aktivity a veřejného diskurzu
- Přímé mediální metriky (EventRegistry) nebyly použity z důvodu omezení API

## Klíčová zjištění

### Nejvyšší skóre (TOP 5)
1. **Španělsko** (0.68) - Nejvyšší Edu AI Index (4.6), EUR 500M rozpočet
2. **Dánsko** (0.65) - EUR 225M, 25%+ firemní adopce
3. **Finsko** (0.63) - EUR 200M, 25%+ firemní adopce
4. **Německo** (0.63) - EUR 5B strategie, nejvíce ICT absolventů
5. **Estonsko** (0.63) - AI Leap iniciativa, 11% ICT absolventů

### Paradox Francie
- **Vysoká policy priorita** (3. místo gov readiness, EUR 4B rozpočet)
- **Nejnižší adopce učiteli** (14%)
- **Pouze 9% učitelů** absolvovalo AI školení

### Vysoká adopce učiteli (ale nižší policy)
- Česko, Malta, Rumunsko: 46% učitelů používá AI
- Polsko: 45%
- Tyto země mají nižší gov readiness skóre

## Datové mezery

### Země s chybějícími daty o učitelích
Austria, Cyprus, Estonia, Germany, Greece, Ireland, Latvia, Lithuania, Luxembourg, Netherlands, Portugal, Slovenia, Spain, Sweden

### Země s chybějícími rozpočtovými daty
Austria, Croatia, Czechia, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Netherlands, Poland, Portugal, Romania, Slovakia, Sweden

### Země s nízkou kvalitou dat
Bulgaria, Croatia, Cyprus, Greece, Hungary, Latvia, Lithuania, Luxembourg, Slovakia, Slovenia

## Metodologie výpočtu skóre

### Policy Score (0-1)
Vážený průměr:
- Gov AI Readiness: 40%
- Edu AI Index: 30% (pokud dostupný)
- Existence dedikovaného rozpočtu: 15%
- Velikost rozpočtu: 15%

### Adoption Score (0-1)
Vážený průměr:
- Teacher AI Usage: 50%
- AI in Schools Access: 25%
- Firm AI Adoption: 15%
- EdTech Ecosystem: 10%

### Overall Score
Průměr Policy Score a Adoption Score

## Aktualizace dat

Data jsou platná k datu sběru (2025-01-22). Pro aktualizaci:

1. **TALIS** - Další vlna očekávána 2029
2. **Oxford Insights** - Roční aktualizace
3. **GoStudent Edu AI Index** - Roční aktualizace
4. **OECD AI Policy Observatory** - Průběžně aktualizováno

## Citace

Při použití těchto dat prosím citujte:

```
AIESI Data Collection (2025). AI in Education Salience Index - EU27 Data.
Sources: OECD TALIS 2024, Oxford Insights 2025, GoStudent 2025, OECD AI Policy Observatory.
```

## Licence

Data jsou kompilací z veřejně dostupných zdrojů. Při použití respektujte původní licence jednotlivých zdrojů.
