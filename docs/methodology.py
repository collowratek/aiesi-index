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
    pdf.cell(0, 6, 'Metodologický dokument')
    pdf.ln(12)

    # 1. Intro
    pdf.chapter_title('1. Co je AIESI Index')
    pdf.body_text(
        'AIESI Index měří, jak moc je umělá inteligence ve vzdělávání „velkým tématem" '
        'v jednotlivých zemích EU27. Index kombinuje tři dimenze: vzdělávací politiky, '
        'praktickou adopci a mediální zájem.'
    )
    pdf.body_text(
        'Index vznikl jako nástroj pro srovnání připravenosti evropských zemí na integraci '
        'AI do vzdělávacího systému. Vyšší skóre znamená, že země aktivněji řeší téma AI ve vzdělávání.'
    )

    # 2. Dimensions
    pdf.chapter_title('2. Dimenze indexu')

    pdf.section_title('2.1 Vzdělávací politiky (edu_policy_score)')
    pdf.body_text('Měří, zda a jak země systematicky řeší AI ve vzdělávání na úrovni státní politiky.')
    pdf.bullet('has_edu_ai_strategy (váha 0,3) – Existuje explicitní strategie AI ve vzdělávání?')
    pdf.bullet('ai_in_curriculum (váha 0,3) – Je AI součástí kurikula? (0 = ne, 0,5 = pilotování, 1 = ano)')
    pdf.bullet('teacher_ai_training_program (váha 0,2) – Existuje státní program školení učitelů?')
    pdf.bullet('edu_ai_pilots (váha 0,2) – Běží pilotní programy AI ve školách?')
    pdf.ln(2)
    pdf.body_text('Vzorec: edu_policy_score = 0,3×strategy + 0,3×curriculum + 0,2×training + 0,2×pilots')

    pdf.section_title('2.2 Praktická adopce (adoption_score)')
    pdf.body_text('Měří skutečné využívání AI nástrojů ve vzdělávání.')
    pdf.bullet('teachers_ai_usage_pct – Procento učitelů používajících AI nástroje')
    pdf.bullet('ai_in_schools_access_pct – Přístup studentů k AI nástrojům')
    pdf.bullet('edtech_startups_pct – EdTech ekosystém v zemi')
    pdf.ln(2)
    pdf.body_text('Hodnoty jsou normalizovány na škálu 0–1 pomocí min-max normalizace.')

    pdf.section_title('2.3 Mediální zájem (media_score)')
    pdf.body_text('Měří veřejný zájem o téma AI ve vzdělávání.')
    pdf.bullet('Google Trends data pro vyhledávací dotaz „AI education" v dané zemi')
    pdf.bullet('Časové období: rok 2024')
    pdf.bullet('Relativní hodnoty normalizované na škálu 0–1')

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
    pdf.body_text(
        'Všechny tři dimenze mají stejnou váhu (33,3 %), protože považujeme za stejně důležité '
        'jak státní politiky, tak praktickou adopci i veřejný zájem.'
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
    pdf.bullet('Data o AI v kurikulu jsou založena na sebehodnocení zemí (European Schoolnet survey)')
    pdf.bullet('Google Trends data mohou být ovlivněna jazykovou bariérou')
    pdf.bullet('TALIS data nejsou dostupná pro všechny země (chybí např. Estonsko, Německo)')
    pdf.bullet('Index neměří kvalitu implementace, pouze existenci politik a adopci')
    pdf.bullet('Soukromé iniciativy nejsou započítány do státní politiky')

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

    # 7. Update info
    pdf.chapter_title('7. Aktualizace dat')
    pdf.body_text('Data byla sebrána v lednu 2025.')
    pdf.body_text('Předpokládaná frekvence aktualizace: ročně.')

    # 8. Contact
    pdf.ln(5)
    pdf.chapter_title('8. Kontakt')
    pdf.body_text('Tento index byl vytvořen projektem skolagpt.cz')
    pdf.link_text('Web', 'https://skolagpt.cz')

    # Save
    output_path = 'docs/AIESI_Metodologie.pdf'
    pdf.output(output_path)
    print(f'PDF uloženo: {output_path}')
    return output_path

if __name__ == '__main__':
    create_methodology_pdf()
