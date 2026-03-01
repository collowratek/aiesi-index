#!/usr/bin/env python3
"""Generate AIESI Methodology PDF document with Czech diacritics"""

from fpdf import FPDF
import os

class MethodologyPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Use built-in fonts that support Czech
        self.add_font('DejaVu', '', '/Users/jirka/Desktop/projects/heatmapaai/docs/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/Users/jirka/Desktop/projects/heatmapaai/docs/DejaVuSans-Bold.ttf', uni=True)

    def header(self):
        self.set_font('DejaVu', '', 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'AIESI Index – Metodologie', align='R')
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

    def link_text(self, text, url):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(0, 102, 204)
        self.multi_cell(0, 5, text + ': ' + url)
        self.set_text_color(60, 60, 60)
        self.ln(1)

def download_fonts():
    """Check DejaVu fonts are present"""
    fonts_dir = '/Users/jirka/Desktop/projects/heatmapaai/docs'
    for font_file in ['DejaVuSans.ttf', 'DejaVuSans-Bold.ttf']:
        font_path = os.path.join(fonts_dir, font_file)
        if not os.path.exists(font_path):
            raise FileNotFoundError(f'Font {font_file} not found in {fonts_dir}')

def create_methodology_pdf():
    # Ensure fonts are available
    download_fonts()

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
    pdf.cell(0, 6, 'Metodologický dokument v1.1')
    pdf.ln(12)

    # 1. Intro
    pdf.chapter_title('1. Co je AIESI Index')
    pdf.body_text(
        'AIESI Index měří, jak moc je umělá inteligence ve vzdělávání „velkým tématem" '
        'v jednotlivých zemích EU27. Index kombinuje tři dimenze: vzdělávací politiky, '
        'praktickou adopci a mediální zájem.'
    )
    pdf.body_text(
        'Index vznikl jako explorativní nástroj pro srovnání připravenosti evropských zemí na integraci '
        'AI do vzdělávacího systému. Vyšší skóre znamená, že země aktivněji řeší téma AI ve vzdělávání.'
    )

    # 2. Dimensions
    pdf.chapter_title('2. Dimenze indexu')

    pdf.section_title('2.1 Vzdělávací politiky (edu_policy_score)')
    pdf.body_text('Měří, zda a jak země systematicky řeší AI ve vzdělávání na úrovni státní politiky.')
    pdf.body_text(
        'Poznámka: Tato dimenze funguje primárně jako checklist – měří existenci politik, '
        'nikoli jejich kvalitu či míru financování. Pro první verzi indexu je to záměrné zjednodušení.'
    )
    pdf.bullet('has_edu_ai_strategy (váha 0,3) – Existuje explicitní strategie AI ve vzdělávání?')
    pdf.bullet('ai_in_curriculum (váha 0,3) – Je AI součástí kurikula? (0 = ne, 0,5 = pilotování, 1 = ano)')
    pdf.bullet('teacher_ai_training_program (váha 0,2) – Existuje státní program školení učitelů?')
    pdf.bullet('edu_ai_pilots (váha 0,2) – Běží pilotní programy AI ve školách?')
    pdf.ln(2)
    pdf.body_text('Vzorec:')
    pdf.set_font('DejaVu', '', 10)
    pdf.set_x(20)
    pdf.cell(0, 6, 'edu_policy = 0,3×strategy + 0,3×curriculum + 0,2×training + 0,2×pilots')
    pdf.ln(6)

    pdf.section_title('2.2 Praktická adopce (adoption_score)')
    pdf.body_text('Měří skutečné využívání AI nástrojů ve vzdělávání.')
    pdf.bullet('teachers_ai_usage – Procento učitelů používajících AI nástroje (normalizováno)')
    pdf.bullet('ai_in_schools_access – Přístup studentů k AI nástrojům (normalizováno)')
    pdf.bullet('edtech_ecosystem – EdTech ekosystém v zemi (normalizováno)')
    pdf.ln(2)
    pdf.body_text('Vzorec (prostý průměr normalizovaných hodnot):')
    pdf.set_font('DejaVu', '', 10)
    pdf.set_x(20)
    pdf.cell(0, 6, 'adoption = (teachers_norm + access_norm + edtech_norm) / 3')
    pdf.ln(6)
    pdf.body_text('Normalizace: min-max na škálu 0–1 pro každý indikátor zvlášť.')

    pdf.section_title('2.3 Mediální zájem (media_score)')
    pdf.body_text('Měří veřejný zájem o téma AI ve vzdělávání.')
    pdf.bullet('Google Trends data pro vyhledávací dotaz „AI education" v dané zemi')
    pdf.bullet('Časové období: rok 2024')
    pdf.bullet('Relativní hodnoty normalizované na škálu 0–1')
    pdf.ln(2)
    pdf.body_text(
        'Upozornění: Tato dimenze je metodicky nejslabší částí indexu. Google Trends má inherentní '
        'omezení – je jazykově biasovaný (anglické dotazy dominují), neodráží skutečný odborný diskurz '
        'a v menších zemích může obsahovat statistický šum. V budoucích verzích by bylo vhodné '
        'kombinovat s dalšími zdroji (počet článků v médiích, parlamentní diskuse, policy dokumenty).'
    )

    pdf.add_page()

    # 3. Calculation
    pdf.chapter_title('3. Výpočet celkového skóre')
    pdf.body_text(
        'Celkové skóre (overall_score_v3) je prostý průměr tří dimenzí s rovnoměrnými vahami:'
    )
    pdf.ln(2)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_x(20)
    pdf.cell(0, 6, 'overall_score = (edu_policy + adoption + media) / 3')
    pdf.ln(8)

    pdf.section_title('3.1 Odůvodnění rovnoměrných vah')
    pdf.body_text(
        'Všechny tři dimenze mají stejnou váhu (33,3 %). Rovnoměrné váhy byly zvoleny z důvodu '
        'absence empirického důkazu o vyšší prediktivní síle některé z dimenzí. V akademických '
        'indexech se obvykle používá expert weighting nebo statistické vážení (PCA / faktorová analýza), '
        'avšak pro explorativní nástroj tohoto typu je rovnoměrné vážení standardním a transparentním přístupem.'
    )
    pdf.body_text(
        'Budoucí verze indexu mohou váhy upravit na základě expertního konsenzu nebo empirických dat '
        'o vztahu jednotlivých dimenzí ke vzdělávacím výsledkům.'
    )

    # 4. Sources
    pdf.chapter_title('4. Zdroje dat')

    pdf.section_title('Primární zdroje')
    pdf.bullet('OECD TALIS 2024 – Teaching and Learning International Survey')
    pdf.link_text('   ', 'https://www.oecd.org/education/talis/')
    pdf.bullet('European Schoolnet 2024 – Agile Collection: AI in School Education')
    pdf.link_text('   ', 'https://www.eun.org/news/detail?articleId=13572286')
    pdf.bullet('Oxford Insights Government AI Readiness Index 2025')
    pdf.link_text('   ', 'https://oxfordinsights.com/ai-readiness/ai-readiness-index/')
    pdf.bullet('GoStudent European Educational AI Index 2025')
    pdf.link_text('   ', 'https://www.gostudent.org/en-gb/blog/which-country-is-best-for-ai-in-education')
    pdf.bullet('Google Trends 2024')
    pdf.link_text('   ', 'https://trends.google.com/')

    pdf.section_title('Sekundární zdroje')
    pdf.bullet('OECD AI Policy Observatory')
    pdf.link_text('   ', 'https://oecd.ai/')
    pdf.bullet('EU AI Act – oficiální dokumentace')
    pdf.link_text('   ', 'https://artificialintelligenceact.eu/')

    # 5. Limitations
    pdf.chapter_title('5. Omezení a limitace')
    pdf.body_text('Při interpretaci dat je třeba zohlednit následující omezení:')

    pdf.section_title('5.1 Datová omezení')
    pdf.bullet('Data o AI v kurikulu jsou založena na sebehodnocení zemí (European Schoolnet survey)')
    pdf.bullet('TALIS data nejsou dostupná pro všechny země (chybí např. Estonsko, Německo) – doplněno odhady')
    pdf.bullet('Soukromé iniciativy nejsou započítány do státní politiky')

    pdf.section_title('5.2 Metodická omezení')
    pdf.bullet('Min-max normalizace může být citlivá na extrémní hodnoty – pokud přibude země s extrémní hodnotou, změní se skóre všech ostatních')
    pdf.bullet('Edu_policy_score měří existenci politik (checklist), nikoli jejich kvalitu, intenzitu či financování')
    pdf.bullet('Rovnoměrné váhy dimenzí nejsou empiricky validovány')

    pdf.section_title('5.3 Omezení media_score')
    pdf.bullet('Google Trends je silně jazykově biasovaný (anglické dotazy dominují)')
    pdf.bullet('Neodráží skutečný odborný diskurz (pouze veřejný zájem)')
    pdf.bullet('V menších zemích může obsahovat statistický šum')
    pdf.bullet('Tato dimenze je metodicky nejslabší částí indexu')

    pdf.add_page()

    # 6. Country notes
    pdf.chapter_title('6. Poznámky k vybraným zemím')

    pdf.section_title('Česko (CZ)')
    pdf.body_text(
        'Česko má paradoxně vysokou adopci (46 % učitelů používá AI – 3. nejvyšší v EU), '
        'ale minimální státní aktivitu ve vzdělávací AI politice. Neexistuje žádná '
        'explicitní strategie AI ve vzdělávání ani začlenění AI do kurikula.'
    )

    pdf.section_title('Dánsko (DK)')
    pdf.body_text(
        'Dánsko dosahuje nejvyššího celkového skóre díky kombinaci silné státní politiky '
        '(AI integrováno do kurikula, 25,5 mil. EUR rozpočet na AI ve vzdělávání) '
        'a významného mediálního zájmu.'
    )

    pdf.section_title('Švédsko (SE)')
    pdf.body_text(
        'Švédsko je jednou ze dvou zemí (spolu s Chorvatskem), kde je AI vyučováno '
        'jako samostatný předmět. Má nejvyšší edu_policy_score (1,0).'
    )

    # 7. Interpretace skóre
    pdf.chapter_title('7. Interpretace skóre')
    pdf.body_text('Pro usnadnění interpretace výsledků používáme následující kategorizaci:')
    pdf.ln(2)
    pdf.bullet('0,00 – 0,33: Nízká salience – téma AI ve vzdělávání není prioritou')
    pdf.bullet('0,34 – 0,66: Střední salience – země se tématem zabývá, ale bez komplexního přístupu')
    pdf.bullet('0,67 – 1,00: Vysoká salience – země aktivně řeší AI ve vzdělávání na více frontách')
    pdf.ln(2)
    pdf.body_text(
        'Tato kategorizace je orientační a slouží pro rychlou interpretaci. '
        'Pro detailnější analýzu doporučujeme zkoumat jednotlivé dimenze zvlášť.'
    )

    # 8. Validita indexu
    pdf.chapter_title('8. Validita a použití indexu')
    pdf.body_text(
        'AIESI Index je explorativní nástroj a neslouží jako prediktivní model vzdělávacích výsledků. '
        'Index neměří kvalitu vzdělávání ani efektivitu implementace AI ve školách.'
    )
    pdf.body_text(
        'Index je vhodný pro:'
    )
    pdf.bullet('Rychlé srovnání přístupů jednotlivých zemí k tématu AI ve vzdělávání')
    pdf.bullet('Identifikaci zemí s komplexním přístupem vs. ad-hoc iniciativami')
    pdf.bullet('Podklad pro policy diskuse a mediální analýzy')
    pdf.ln(2)
    pdf.body_text(
        'Index není vhodný pro:'
    )
    pdf.bullet('Predikci vzdělávacích výsledků či úspěšnosti studentů')
    pdf.bullet('Hodnocení kvality konkrétních AI nástrojů ve školách')
    pdf.bullet('Kauzální závěry o vztahu politiky a adopce')

    # 9. Citlivostní analýza
    pdf.add_page()
    pdf.chapter_title('9. Citlivostní analýza')
    pdf.body_text(
        'Pro ověření robustnosti indexu byla provedena základní citlivostní analýza. '
        'Testovali jsme stabilitu pořadí zemí při změně vah jednotlivých dimenzí o ±10 %.'
    )
    pdf.body_text(
        'Výsledky: Pořadí prvních 5 zemí zůstává stabilní při změnách vah. Střed žebříčku '
        '(pozice 10–20) vykazuje větší citlivost na změny, zejména při posílení váhy media_score. '
        'Doporučujeme interpretovat střední část žebříčku s větší opatrností.'
    )

    # 10. Update info
    pdf.chapter_title('10. Aktualizace dat')
    pdf.body_text('Data byla sebrána v lednu 2025.')
    pdf.body_text('Předpokládaná frekvence aktualizace: ročně.')
    pdf.body_text(
        'Metodika může být v budoucích verzích upravena na základě zpětné vazby a dostupnosti '
        'nových datových zdrojů.'
    )

    # 11. Contact
    pdf.ln(5)
    pdf.chapter_title('11. Kontakt')
    pdf.body_text('Tento index byl vytvořen projektem skolagpt.cz')
    pdf.link_text('Web', 'https://skolagpt.cz')

    # Save
    output_path = 'docs/AIESI_Metodologie.pdf'
    pdf.output(output_path)
    print(f'PDF uloženo: {output_path}')
    return output_path

if __name__ == '__main__':
    create_methodology_pdf()
