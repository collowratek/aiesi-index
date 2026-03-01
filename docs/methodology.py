#!/usr/bin/env python3
"""Generate AIESI Methodology PDF v6 — two-dimensional index with TALIS + Eurostat"""

from fpdf import FPDF
import os


class MethodologyPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', '/Users/jirka/Desktop/projects/heatmapaai/docs/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/Users/jirka/Desktop/projects/heatmapaai/docs/DejaVuSans-Bold.ttf', uni=True)

    def header(self):
        self.set_font('DejaVu', '', 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'AIESI Index v6 – Metodologie', align='R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'skolagpt.cz  |  Strana {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('DejaVu', 'B', 13)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 8, title)
        self.ln(4)

    def section_title(self, title):
        self.set_font('DejaVu', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 7, title)
        self.ln(3)

    def body_text(self, text):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(60, 60, 60)
        self.set_x(15)
        self.multi_cell(0, 5, '• ' + text)
        self.ln(1)

    def formula(self, text):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(30, 30, 30)
        self.set_x(20)
        self.cell(0, 6, text)
        self.ln(6)

    def link_text(self, text, url):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(0, 102, 204)
        self.multi_cell(0, 5, text + ': ' + url)
        self.set_text_color(60, 60, 60)
        self.ln(1)


def create_methodology_pdf():
    fonts_dir = '/Users/jirka/Desktop/projects/heatmapaai/docs'
    for f in ['DejaVuSans.ttf', 'DejaVuSans-Bold.ttf']:
        if not os.path.exists(os.path.join(fonts_dir, f)):
            raise FileNotFoundError(f'Font {f} not found in {fonts_dir}')

    pdf = MethodologyPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.add_page()

    # Title
    pdf.set_font('DejaVu', 'B', 22)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, 'AIESI Index')
    pdf.ln(10)
    pdf.set_font('DejaVu', '', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'AI in Education Salience Index')
    pdf.ln(5)
    pdf.cell(0, 6, 'Metodologický dokument v6')
    pdf.ln(12)

    # ============================================================
    # 1. Intro
    # ============================================================
    pdf.chapter_title('1. Co je AIESI Index')
    pdf.body_text(
        'AIESI Index měří, jak moc je umělá inteligence ve vzdělávání „velkým tématem" '
        'v jednotlivých zemích EU27. Index kombinuje dvě dimenze: pokrytí vzdělávacích politik '
        'a praktickou adopci AI nástrojů.'
    )
    pdf.body_text(
        'Index je explorativní nástroj pro srovnání přístupů evropských zemí k integraci '
        'AI do vzdělávacího systému. Vyšší skóre znamená, že země aktivněji řeší téma AI ve vzdělávání. '
        'Index neměří kvalitu vzdělávání ani efektivitu implementace.'
    )

    # ============================================================
    # 2. Dimensions
    # ============================================================
    pdf.chapter_title('2. Dimenze indexu')

    # 2.1 Policy coverage
    pdf.section_title('2.1 Pokrytí vzdělávacích politik (edu_policy_coverage)')
    pdf.body_text(
        'Tato dimenze funguje jako checklist existence — měří, zda země má formální politiky '
        'zaměřené na AI ve vzdělávání. Nehodnotí kvalitu, intenzitu ani financování těchto politik. '
        'Název „coverage" (pokrytí) explicitně odráží tento charakter.'
    )
    pdf.bullet('has_edu_ai_strategy (váha 0,3) – Existuje explicitní strategie AI ve vzdělávání? [0/1]')
    pdf.bullet('ai_in_curriculum (váha 0,3) – Je AI součástí kurikula? [0 = ne, 0,5 = pilotování, 1 = ano]')
    pdf.bullet('teacher_ai_training_program (váha 0,2) – Existuje státní program školení učitelů? [0/1]')
    pdf.bullet('edu_ai_pilots (váha 0,2) – Běží pilotní programy AI ve školách? [0/1]')
    pdf.ln(2)
    pdf.body_text('Vzorec:')
    pdf.formula('edu_policy_coverage = 0,3×strategy + 0,3×curriculum + 0,2×training + 0,2×pilots')
    pdf.body_text(
        'Poznámka: Tento přístup má inherentní omezení — např. Francie (budget 1 mld. EUR) a Chorvatsko '
        '(bez explicitního rozpočtu) mohou dosáhnout podobného skóre, přestože se liší v intenzitě '
        'financování. Pro budoucí verze doporučujeme doplnit kvantitativní indikátor investic.'
    )

    # 2.2 Adoption — REWRITTEN for v6
    pdf.section_title('2.2 Praktická adopce (adoption_score)')
    pdf.body_text(
        'Měří skutečné využívání AI nástrojů na základě dvou nezávislých, verifikovaných zdrojů:'
    )
    pdf.bullet('TALIS 2024 (OECD) – procento učitelů nižšího sekundárního vzdělávání '
               'používajících AI nástroje. Pokrytí: 20/27 zemí EU.')
    pdf.bullet('Eurostat 2025 (isoc_ai_iaiu) – procento populace (16–74 let) '
               'používající generativní AI nástroje. Pokrytí: 27/27 zemí EU.')
    pdf.ln(2)
    pdf.body_text('Postup výpočtu:')
    pdf.bullet('Oba indikátory normalizovány min-max na škálu 0–1 (N=27).')
    pdf.bullet('Pro 20 zemí s oběma zdroji: adoption = průměr obou normalizovaných hodnot.')
    pdf.bullet('Pro 7 zemí pouze s Eurostat (DE, IE, HR, SI, CY, EL, LU): '
               'adoption = normalizovaná hodnota Eurostat.')
    pdf.ln(2)
    pdf.body_text('Vzorec:')
    pdf.formula('adoption = mean(TALIS_norm, Eurostat_norm)  [pairwise available]')

    pdf.section_title('2.2.1 Křížová validace zdrojů')
    pdf.body_text(
        'Spearmanova korelace mezi normalizovanými hodnotami TALIS a Eurostat '
        'u 20 zemí s oběma zdroji činí ρ = 0,15. Nízká korelace je očekávaná: '
        'TALIS měří specificky učitele ve školách, zatímco Eurostat měří obecnou populaci. '
        'Jde o odlišné konstrukty — učitelská adopce AI ≠ populační využívání GenAI. '
        'Právě proto je jejich kombinace informativnější než každý zdroj zvlášť.'
    )

    pdf.section_title('2.2.2 Kvalita dat oproti v5')
    pdf.body_text(
        'V předchozích verzích (v1–v5) byla adoption_score založena na heterogenních '
        'zdrojích: teachers_ai_usage_pct (12/27 zemí), ai_in_schools_access_pct (GoStudent, 7/27) '
        'a proxy odhad z Government AI Readiness (Oxford Insights) pro 11 zemí bez dat '
        '(ρ = 0,07 s měřenými hodnotami — prakticky náhodný).'
    )
    pdf.body_text(
        'Ve verzi v6 jsou obě datové řady z oficiálních statistických šetření '
        '(OECD TALIS, Eurostat) s transparentní metodologií sběru. Žádná země '
        'nemá proxy imputaci — všech 27 zemí má alespoň jeden přímý zdroj.'
    )

    # 2.3 Excluded indicator
    pdf.section_title('2.3 Vyloučený indikátor: mediální zájem (media_score)')
    pdf.body_text(
        'V předchozích verzích (v1–v4) index zahrnoval třetí dimenzi — mediální zájem '
        'měřený prostřednictvím Google Trends (dotaz „AI education", rok 2024). '
        'Ve verzi v5 byla tato dimenze vyloučena z výpočtu celkového skóre '
        'z důvodu fundamentálního problému validity.'
    )
    pdf.ln(2)
    pdf.body_text('Důvody vyloučení:')
    pdf.bullet('Jediný anglický dotaz měří anglophone bias, nikoliv skutečný mediální zájem '
               '— Irsko (nativně anglicky mluvící) = 1,0; 10 zemí = 0,0.')
    pdf.bullet('Žádná diskriminační síla pro třetinu vzorku (10/27 zemí se skóre 0,0).')
    pdf.bullet('Neodráží odborný diskurz ani veřejnou debatu v národních jazycích.')
    pdf.ln(2)
    pdf.body_text(
        'Data media_score zůstávají v CSV souboru jako informativní sloupec.'
    )

    pdf.add_page()

    # ============================================================
    # 3. Celkové skóre
    # ============================================================
    pdf.chapter_title('3. Výpočet celkového skóre')
    pdf.body_text('Celkové skóre je prostý průměr dvou dimenzí:')
    pdf.ln(2)
    pdf.formula('overall = 0,5 × policy_coverage + 0,5 × adoption')
    pdf.ln(2)

    pdf.section_title('3.1 Odůvodnění vah')
    pdf.body_text(
        'Rovné váhy 50/50 byly zvoleny na základě následujících úvah:'
    )
    pdf.bullet('Obě dimenze přímo měří aktivitu států v oblasti AI ve vzdělávání — '
               'policy_coverage zachycuje systémový rámec, adoption praktickou implementaci.')
    pdf.bullet('Záporná vzájemná korelace dimenzí (Spearman ρ = −0,16) potvrzuje, že zachycují '
               'odlišné aspekty — existence politik negarantuje adopci a naopak.')
    pdf.bullet('Bez silného teoretického důvodu pro asymetrii jsou rovné váhy '
               'nejtransparentnějším a nejobhajitelnějším přístupem.')
    pdf.bullet('Pro explorativní nástroj s N=27 je expertní '
               'vážení transparentnějším přístupem než statistické metody (PCA).')
    pdf.ln(2)
    pdf.body_text(
        'Citlivostní analýza (viz kapitola 8) potvrzuje, že pořadí zemí je stabilní '
        'při změnách poměru vah v rozsahu 20/80 až 80/20 (Spearmanovo ρ ≥ 0,71).'
    )

    # ============================================================
    # 4. Zdroje dat
    # ============================================================
    pdf.chapter_title('4. Zdroje dat')

    pdf.section_title('Primární zdroje — adopce')
    pdf.bullet('OECD TALIS 2024 – % učitelů nižšího sekundárního vzdělávání používajících AI (20/27 EU)')
    pdf.link_text('   ', 'https://www.oecd.org/education/talis/')
    pdf.bullet('Eurostat 2025 – % populace (16–74) používající generativní AI (dataset isoc_ai_iaiu, 27/27 EU)')
    pdf.link_text('   ', 'https://ec.europa.eu/eurostat/databrowser/view/isoc_ai_iaiu/')

    pdf.section_title('Primární zdroje — politiky')
    pdf.bullet('European Schoolnet 2024 – Agile Collection: AI in School Education')
    pdf.link_text('   ', 'https://www.eun.org/news/detail?articleId=13572286')

    pdf.section_title('Sekundární zdroje')
    pdf.bullet('Oxford Insights Government AI Readiness Index 2025')
    pdf.link_text('   ', 'https://oxfordinsights.com/ai-readiness/ai-readiness-index/')
    pdf.bullet('OECD AI Policy Observatory')
    pdf.link_text('   ', 'https://oecd.ai/')

    # ============================================================
    # 5. Omezení a limitace
    # ============================================================
    pdf.chapter_title('5. Omezení a limitace')
    pdf.body_text('Při interpretaci dat je třeba zohlednit následující omezení:')

    pdf.section_title('5.1 Datová omezení')
    pdf.bullet('TALIS 2024: 7 zemí EU se nezúčastnilo nebo data nebyla publikována '
               '(DE, IE, HR, SI, CY, EL, LU) — jejich adopce je založena pouze na Eurostat.')
    pdf.bullet('Policy data: Založena na sebehodnocení zemí (European Schoolnet survey) '
               '— možný reporting bias.')
    pdf.bullet('Eurostat měří obecnou populaci, ne specificky vzdělávací sektor.')
    pdf.bullet('Soukromé iniciativy nejsou zahrnuty do dimenze pokrytí politik.')

    pdf.section_title('5.2 Metodická omezení')
    pdf.bullet('Min-max normalizace je citlivá na extrémní hodnoty — přidání země s outlier '
               'hodnotou změní skóre všech ostatních.')
    pdf.bullet('Edu_policy_coverage měří existenci politik (checklist), nikoli kvalitu, '
               'intenzitu či financování.')
    pdf.bullet('Rovné váhy (50/50) nejsou empiricky validovány. Citlivostní analýza '
               'ukazuje stabilitu pořadí, ale neprokáže optimalitu vah.')
    pdf.bullet('N = 27. Malý vzorek limituje možnost statistické inference.')

    pdf.add_page()

    # ============================================================
    # 6. Country notes
    # ============================================================
    pdf.chapter_title('6. Poznámky k vybraným zemím')

    pdf.section_title('Švédsko (SE) — 1. místo, skóre 0,83')
    pdf.body_text(
        'Švédsko dosahuje nejvyššího celkového skóre díky maximálnímu policy_coverage (1,0) '
        'a solidní adopci (0,66). Má AI jako samostatný předmět v kurikulu a komplexní '
        'digitalizační strategii 2025. TALIS: 31 % učitelů, Eurostat: 42 % populace.'
    )

    pdf.section_title('Česko (CZ) — 12. místo, skóre 0,50')
    pdf.body_text(
        'Česko má jednu z nejvyšších měřených adopcí učitelů v EU (TALIS: 46 %), '
        'ale nízké pokrytí politik (0,2). Neexistuje explicitní strategie AI '
        've vzdělávání ani začlenění do kurikula. Typický případ bottom-up adopce '
        'bez systémové politické podpory.'
    )

    pdf.section_title('Francie (FR) — 10. místo, skóre 0,56')
    pdf.body_text(
        'Paradox indexu: Francie investuje 1 mld. EUR do AI strategie a má vysoké '
        'policy_coverage (0,8), ale nejnižší měřenou adopci učitelů v EU (TALIS: 14 %). '
        'Ilustruje omezení checklistu — existence politik nezaručuje implementaci.'
    )

    pdf.section_title('Německo (DE) — 7. místo, skóre 0,64')
    pdf.body_text(
        'Německo se nezúčastnilo TALIS 2024, jeho adopce je založena pouze na Eurostat '
        '(32,3 % populace s GenAI). Vysoké policy_coverage (0,8) díky KMK AI guidelines 2024. '
        'Adopce (0,47) je metodou „eurostat_only" — interpretovat s opatrností.'
    )

    # ============================================================
    # 7. Interpretace skóre
    # ============================================================
    pdf.chapter_title('7. Interpretace skóre')
    pdf.body_text('Orientační kategorizace:')
    pdf.bullet('0,0 – 0,3: Nízká salience – téma AI ve vzdělávání není prioritou')
    pdf.bullet('0,3 – 0,7: Střední salience – země se tématem zabývá')
    pdf.bullet('0,7 – 1,0: Vysoká salience – země aktivně řeší AI ve vzdělávání')
    pdf.ln(2)
    pdf.body_text(
        'Hranice kategorií jsou orientační. Pro detailnější analýzu doporučujeme '
        'zkoumat jednotlivé dimenze zvlášť.'
    )

    # ============================================================
    # 8. Citlivostní analýza
    # ============================================================
    pdf.chapter_title('8. Citlivostní analýza')
    pdf.body_text(
        'Pro ověření robustnosti indexu byla provedena kvantitativní citlivostní analýza '
        'perturbací vah dimenzí.'
    )

    pdf.section_title('8.1 Metoda')
    pdf.body_text(
        'Poměr vah dvou dimenzí byl systematicky měněn v rozsahu 20/80 až 80/20 '
        '(krok 5 p.b.), celkem 13 kombinací. Pro každou kombinaci bylo vypočteno '
        'celkové skóre a pořadí zemí, a porovnáno se základním pořadím (50/50) pomocí '
        'Spearmanovy korelace pořadí (ρ).'
    )

    pdf.section_title('8.2 Výsledky')
    pdf.bullet('Spearmanovo ρ: min = 0,709, průměr = 0,912, max = 1,000')
    pdf.bullet('77 % kombinací má ρ ≥ 0,90 (10/13)')
    pdf.bullet('31 % kombinací má ρ ≥ 0,95 (4/13)')
    pdf.bullet('Top-5 zemí identická v 46 % kombinací (6/13)')
    pdf.ln(2)
    pdf.body_text(
        'Závěr: Pořadí zemí je robustní v širokém rozsahu vah. K výrazným změnám '
        'dochází pouze při extrémních poměrech (20/80), kde jedna dimenze dominuje.'
    )

    pdf.section_title('8.3 Korelace dimenzí (Spearman)')
    pdf.body_text(
        'Spearman ρ(policy_coverage, adoption) = −0,16 (N=27). '
        'Záporná korelace potvrzuje, že existence politik a skutečná adopce jsou '
        'nezávislé dimenze. Země s vysokou politickou aktivitou nemusí mít vysokou adopci '
        '(Francie) a naopak (Malta, Česko). To podporuje dvoudimenzionální model.'
    )

    pdf.add_page()

    # ============================================================
    # 9. Validita
    # ============================================================
    pdf.chapter_title('9. Validita a použití indexu')
    pdf.body_text(
        'AIESI Index je explorativní nástroj. Neslouží jako prediktivní model '
        'vzdělávacích výsledků ani jako benchmark kvality vzdělávacích systémů.'
    )
    pdf.body_text('Index je vhodný pro:')
    pdf.bullet('Rychlé srovnání přístupů zemí k tématu AI ve vzdělávání')
    pdf.bullet('Identifikaci zemí s komplexním přístupem vs. ad-hoc iniciativami')
    pdf.bullet('Podklad pro policy diskuse a mediální analýzy')
    pdf.ln(2)
    pdf.body_text('Index není vhodný pro:')
    pdf.bullet('Predikci vzdělávacích výsledků či úspěšnosti studentů')
    pdf.bullet('Hodnocení kvality konkrétních AI nástrojů ve školách')
    pdf.bullet('Kauzální závěry o vztahu politiky a adopce')
    pdf.bullet('Statistickou inferenci (N=27)')

    # ============================================================
    # 10. Deskriptivní statistiky
    # ============================================================
    pdf.chapter_title('10. Deskriptivní statistiky')
    pdf.body_text('Souhrnné statistiky dimenzí (N=27):')
    pdf.ln(2)
    # Table-like display
    pdf.set_font('DejaVu', 'B', 10)
    pdf.cell(55, 6, 'Dimenze', border=1)
    pdf.cell(25, 6, 'M', border=1, align='C')
    pdf.cell(25, 6, 'SD', border=1, align='C')
    pdf.cell(25, 6, 'Min', border=1, align='C')
    pdf.cell(25, 6, 'Max', border=1, align='C')
    pdf.cell(25, 6, 'Median', border=1, align='C')
    pdf.ln()
    pdf.set_font('DejaVu', '', 10)
    for label, vals in [
        ('Overall score', (0.51, 0.19, 0.16, 0.83, 0.48)),
        ('Policy coverage', (0.39, 0.34, 0.00, 1.00, 0.30)),
        ('Adoption', (0.63, 0.21, 0.20, 0.97, 0.66)),
    ]:
        pdf.cell(55, 6, label, border=1)
        for v in vals:
            pdf.cell(25, 6, f'{v:.2f}', border=1, align='C')
        pdf.ln()

    # ============================================================
    # 11. Aktualizace
    # ============================================================
    pdf.ln(4)
    pdf.chapter_title('11. Historie verzí')
    pdf.body_text(
        'v6 (březen 2026): Adopční dimenze přestavěna na dva verifikované zdroje — '
        'TALIS 2024 (OECD, 20/27 zemí) a Eurostat 2025 GenAI (27/27 zemí). '
        'Odstraněna proxy imputace z Government AI Readiness (ρ = 0,07). '
        'Žádná země nemá odhadované hodnoty.'
    )
    pdf.body_text(
        'v5 (únor 2026): Vyloučen media_score z celkového skóre (anglophone bias). '
        'Přechod na dvoudimenzionální model 50/50.'
    )
    pdf.body_text(
        'v1–v4 (leden 2025): Tři dimenze (policy + adoption + media). '
        'Adopce založena na heterogenních zdrojích s proxy imputací.'
    )
    pdf.body_text('Předpokládaná frekvence aktualizace: ročně.')

    # ============================================================
    # 12. Kontakt
    # ============================================================
    pdf.ln(3)
    pdf.chapter_title('12. Kontakt')
    pdf.body_text('Tento index byl vytvořen projektem skolagpt.cz')
    pdf.link_text('Web', 'https://skolagpt.cz')

    # Save
    output_path = 'docs/AIESI_Metodologie.pdf'
    pdf.output(output_path)
    print(f'PDF uloženo: {output_path}')
    return output_path


if __name__ == '__main__':
    create_methodology_pdf()
