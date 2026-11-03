# -*- coding: utf-8 -*-
"""
Генерація DOCX для практичного заняття № 8
Тема: Формулювання висновків. Узагальнення результатів,
      розробка рекомендацій
Дисципліна: Основи науково-педагогічних досліджень
Спеціальність: Початкова освіта
Вимоги: Times New Roman, 14 pt, інтервал 1.25, вирівнювання по ширині
"""

import os
import tempfile
import cairosvg
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ============================================================
# 1. НАЛАШТУВАННЯ ДОКУМЕНТА
# ============================================================

def setup_document():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(14)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.25
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_after = Pt(6)
    pf.first_line_indent = Cm(1.25)
    return doc


# ============================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ
# ============================================================

def add_title(doc, text, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
              space_after=6, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    if color:
        run.font.color.rgb = RGBColor(*color)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x5F)
    return p


def add_paragraph(doc, text, bold=False, italic=False, indent=True,
                  align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    if not indent:
        p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    return p


def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing = 1.25
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(14)
    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    return p


def add_numbered(doc, text):
    p = doc.add_paragraph(style='List Number')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    return p


def add_table(doc, headers, rows, col_widths=None, font_size=12):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), '1E3A5F')
        hdr[i]._tc.get_or_add_tcPr().append(shd)

    for row_data in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row_data):
            cells[i].text = ''
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(font_size)

    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)

    doc.add_paragraph()
    return table


def add_svg_image(doc, svg_string, width_cm=15, caption=None):
    tmp_png = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    cairosvg.svg2png(bytestring=svg_string.encode('utf-8'),
                     write_to=tmp_png, output_width=1400)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run()
    run.add_picture(tmp_png, width=Cm(width_cm))
    os.unlink(tmp_png)

    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.first_line_indent = Cm(0)
        cap.paragraph_format.space_after = Pt(10)
        r = cap.add_run(caption)
        r.italic = True
        r.font.size = Pt(12)
        r.font.name = 'Times New Roman'
        r.font.color.rgb = RGBColor(0x63, 0x6E, 0x72)


# ============================================================
# 3. SVG-ДІАГРАМИ
# ============================================================

SVG_PYRAMID = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 420" width="760" height="420">
  <rect width="760" height="420" fill="#ffffff"/>
  <text x="380" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Піраміда узагальнення результатів дослідження</text>

  <!-- Рекомендації -->
  <polygon points="380,60 460,120 300,120" fill="#1e3a5f"/>
  <text x="380" y="98" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">РЕКОМЕНДАЦІЇ</text>
  <text x="380" y="114" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#cfe7f7">для практики</text>

  <!-- Висновки -->
  <polygon points="290,130 470,130 540,200 220,200" fill="#2980b9"/>
  <text x="380" y="160" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">ВИСНОВКИ</text>
  <text x="380" y="180" text-anchor="middle" font-family="Arial" font-size="10" fill="#ebf5fb">узагальнені положення</text>

  <!-- Узагальнення -->
  <polygon points="210,210 550,210 620,280 140,280" fill="#27ae60"/>
  <text x="380" y="240" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">УЗАГАЛЬНЕННЯ</text>
  <text x="380" y="260" text-anchor="middle" font-family="Arial" font-size="10" fill="#eafaf1">закономірності, тенденції</text>

  <!-- Результати -->
  <polygon points="130,290 630,290 700,360 60,360" fill="#e67e22"/>
  <text x="380" y="320" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">РЕЗУЛЬТАТИ ДОСЛІДЖЕННЯ</text>
  <text x="380" y="340" text-anchor="middle" font-family="Arial" font-size="10" fill="#fef9e7">емпіричні дані, факти</text>

  <text x="380" y="395" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#475569">Кожен рівень спирається на попередній: без фактів — немає узагальнень,</text>
  <text x="380" y="412" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#475569">без узагальнень — немає обґрунтованих висновків і рекомендацій</text>
</svg>
'''

SVG_CONCLUSION_FORMULA = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 320" width="820" height="320">
  <rect width="820" height="320" fill="#ffffff"/>
  <text x="410" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Формула наукового висновку</text>

  <rect x="15" y="55" width="180" height="120" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="105" y="80" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">1. ТВЕРДЖЕННЯ</text>
  <text x="105" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">що саме</text>
  <text x="105" y="120" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">встановлено</text>
  <text x="105" y="145" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#2980b9">«Встановлено, що …»</text>

  <rect x="205" y="55" width="180" height="120" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="2"/>
  <text x="295" y="80" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e5a3f">2. ОБҐРУНТУВАННЯ</text>
  <text x="295" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">на основі яких</text>
  <text x="295" y="120" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">даних</text>
  <text x="295" y="145" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#27ae60">«… на основі …»</text>

  <rect x="395" y="55" width="180" height="120" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="2"/>
  <text x="485" y="80" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7e5109">3. ПОЯСНЕННЯ</text>
  <text x="485" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">чому саме так</text>
  <text x="485" y="120" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">(причини)</text>
  <text x="485" y="145" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#e67e22">«… що пояснюється …»</text>

  <rect x="585" y="55" width="220" height="120" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="2"/>
  <text x="695" y="80" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#4a235a">4. ЗНАЧЕННЯ</text>
  <text x="695" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">для теорії</text>
  <text x="695" y="120" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">та практики</text>
  <text x="695" y="145" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#8e44ad">«… має значення для …»</text>

  <text x="410" y="215" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e3a5f">ПРИКЛАД:</text>
  <rect x="60" y="230" width="700" height="70" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="410" y="255" text-anchor="middle" font-family="Arial" font-size="11" fill="#334155">«Встановлено, що систематичне використання дидактичних ігор підвищує</text>
  <text x="410" y="273" text-anchor="middle" font-family="Arial" font-size="11" fill="#334155">пізнавальний інтерес молодших школярів на 25 % (на основі порівняння</text>
  <text x="410" y="291" text-anchor="middle" font-family="Arial" font-size="11" fill="#334155">констатувального й контрольного зрізів), що має значення для методики …»</text>
</svg>
'''

SVG_CONCLUSION_TYPES = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 340" width="760" height="340">
  <rect width="760" height="340" fill="#ffffff"/>
  <text x="380" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Типи висновків у науково-педагогічному дослідженні</text>

  <rect x="20" y="55" width="230" height="125" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="135" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#1e3a5f">Теоретичні</text>
  <text x="135" y="105" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">узагальнення</text>
  <text x="135" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">наукових положень,</text>
  <text x="135" y="139" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">уточнення понять</text>
  <text x="135" y="165" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#2980b9">стосуються теорії</text>

  <rect x="265" y="55" width="230" height="125" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="2"/>
  <text x="380" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#1e5a3f">Емпіричні</text>
  <text x="380" y="105" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">узагальнення</text>
  <text x="380" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">отриманих даних,</text>
  <text x="380" y="139" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">виявлені тенденції</text>
  <text x="380" y="165" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#27ae60">стосуються фактів</text>

  <rect x="510" y="55" width="230" height="125" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="2"/>
  <text x="625" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#7e5109">Практичні</text>
  <text x="625" y="105" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">рекомендації</text>
  <text x="625" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">для вчителів,</text>
  <text x="625" y="139" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">учнів, батьків</text>
  <text x="625" y="165" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#e67e22">стосуються дій</text>

  <rect x="140" y="210" width="480" height="95" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="380" y="235" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#4a235a">Загальна структура розділу «Висновки»</text>
  <text x="380" y="257" text-anchor="middle" font-family="Arial" font-size="11" fill="#6c3483">1) загальний підсумок дослідження;</text>
  <text x="380" y="275" text-anchor="middle" font-family="Arial" font-size="11" fill="#6c3483">2) конкретні результати за кожним завданням;</text>
  <text x="380" y="293" text-anchor="middle" font-family="Arial" font-size="11" fill="#6c3483">3) підтвердження / спростування гіпотези.</text>
</svg>
'''

SVG_RECOMMENDATIONS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 360" width="760" height="360">
  <rect width="760" height="360" fill="#ffffff"/>
  <text x="380" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Адресати рекомендацій за результатами дослідження</text>

  <circle cx="380" cy="200" r="65" fill="#1e3a5f"/>
  <text x="380" y="194" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">РЕКОМЕНДАЦІЇ</text>
  <text x="380" y="213" text-anchor="middle" font-family="Arial" font-size="11" fill="#cfe7f7">за результатами</text>

  <line x1="380" y1="135" x2="380" y2="90" stroke="#2980b9" stroke-width="2"/>
  <rect x="270" y="50" width="220" height="42" rx="9" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="380" y="76" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">Вчителям початкових класів</text>

  <line x1="445" y1="170" x2="540" y2="135" stroke="#27ae60" stroke-width="2"/>
  <rect x="542" y="110" width="200" height="42" rx="9" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="642" y="136" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e5a3f">Учням початкової школи</text>

  <line x1="445" y1="230" x2="540" y2="260" stroke="#e67e22" stroke-width="2"/>
  <rect x="542" y="240" width="200" height="42" rx="9" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="642" y="266" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7e5109">Батькам молодших школярів</text>

  <line x1="380" y1="265" x2="380" y2="305" stroke="#8e44ad" stroke-width="2"/>
  <rect x="270" y="305" width="220" height="42" rx="9" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="380" y="331" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#4a235a">Адміністрації школи</text>

  <line x1="315" y1="230" x2="220" y2="260" stroke="#c0392b" stroke-width="2"/>
  <rect x="20" y="240" width="200" height="42" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="120" y="266" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7b241c">Методичним об'єднанням</text>

  <line x1="315" y1="170" x2="220" y2="135" stroke="#16a085" stroke-width="2"/>
  <rect x="20" y="110" width="200" height="42" rx="9" fill="#e8f8f5" stroke="#16a085" stroke-width="1.5"/>
  <text x="120" y="136" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#0e6655">Авторам програм і підручників</text>
</svg>
'''

SVG_PRESENTATION_STRUCTURE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="800" height="380">
  <rect width="800" height="380" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура презентації результатів дослідження (10–12 слайдів)</text>

  <rect x="15" y="55" width="150" height="55" rx="8" fill="#1e3a5f"/>
  <text x="90" y="78" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">1. Титульний</text>
  <text x="90" y="96" text-anchor="middle" font-family="Arial" font-size="10" fill="#cfe7f7">тема, автор</text>

  <rect x="175" y="55" width="150" height="55" rx="8" fill="#2471a3"/>
  <text x="250" y="78" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">2. Актуальність</text>
  <text x="250" y="96" text-anchor="middle" font-family="Arial" font-size="10" fill="#ebf5fb">проблема, мета</text>

  <rect x="335" y="55" width="150" height="55" rx="8" fill="#2980b9"/>
  <text x="410" y="78" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">3. Об'єкт, предмет</text>
  <text x="410" y="96" text-anchor="middle" font-family="Arial" font-size="10" fill="#ebf5fb">науковий апарат</text>

  <rect x="495" y="55" width="150" height="55" rx="8" fill="#27ae60"/>
  <text x="570" y="78" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">4. Методи</text>
  <text x="570" y="96" text-anchor="middle" font-family="Arial" font-size="10" fill="#eafaf1">теоретичні, емпіричні</text>

  <rect x="655" y="55" width="130" height="55" rx="8" fill="#16a085"/>
  <text x="720" y="78" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">5. Гіпотеза</text>
  <text x="720" y="96" text-anchor="middle" font-family="Arial" font-size="10" fill="#e8f8f5">припущення</text>

  <rect x="15" y="135" width="150" height="55" rx="8" fill="#e67e22"/>
  <text x="90" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">6. Огляд джерел</text>
  <text x="90" y="176" text-anchor="middle" font-family="Arial" font-size="10" fill="#fef9e7">1–2 слайди</text>

  <rect x="175" y="135" width="150" height="55" rx="8" fill="#d35400"/>
  <text x="250" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">7. Методика</text>
  <text x="250" y="176" text-anchor="middle" font-family="Arial" font-size="10" fill="#fdf2e9">критерії, рівні</text>

  <rect x="335" y="135" width="150" height="55" rx="8" fill="#8e44ad"/>
  <text x="410" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">8. Результати</text>
  <text x="410" y="176" text-anchor="middle" font-family="Arial" font-size="10" fill="#f4ecf7">таблиці, діаграми</text>

  <rect x="495" y="135" width="150" height="55" rx="8" fill="#6c3483"/>
  <text x="570" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">9. Інтерпретація</text>
  <text x="570" y="176" text-anchor="middle" font-family="Arial" font-size="10" fill="#e8daef">порівняння з теорією</text>

  <rect x="655" y="135" width="130" height="55" rx="8" fill="#c0392b"/>
  <text x="720" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">10. Висновки</text>
  <text x="720" y="176" text-anchor="middle" font-family="Arial" font-size="10" fill="#fdedec">узагальнення</text>

  <rect x="270" y="215" width="260" height="55" rx="8" fill="#7b241c"/>
  <text x="400" y="238" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">11. Рекомендації</text>
  <text x="400" y="256" text-anchor="middle" font-family="Arial" font-size="10" fill="#fdedec">за адресатами</text>

  <rect x="545" y="215" width="240" height="55" rx="8" fill="#1e3a5f"/>
  <text x="665" y="238" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">12. Дякую за увагу</text>
  <text x="665" y="256" text-anchor="middle" font-family="Arial" font-size="10" fill="#cfe7f7">контакти, запитання</text>

  <text x="400" y="305" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Орієнтовний час: 7–10 хвилин · 1 слайд = 40–60 секунд усного виступу</text>
  <text x="400" y="328" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">На кожному слайді — не більше 6 рядків тексту та 1 візуальний об'єкт</text>
  <text x="400" y="352" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Головний принцип: мінімум тексту — максимум наочності й аргументації</text>
</svg>
'''

SVG_SLIDE_TEMPLATE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 420" width="760" height="420">
  <rect width="760" height="420" fill="#ffffff"/>
  <text x="380" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Шаблон слайда з результатами</text>

  <!-- Рамка слайда -->
  <rect x="60" y="45" width="640" height="340" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>

  <!-- Заголовок -->
  <rect x="60" y="45" width="640" height="45" rx="6" fill="#1e3a5f"/>
  <text x="380" y="74" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#ffffff">Динаміка рівнів сформованості за результатами дослідження</text>

  <!-- Графік -->
  <line x1="120" y1="270" x2="120" y2="130" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="120" y1="270" x2="400" y2="270" stroke="#94a3b8" stroke-width="1.5"/>

  <line x1="120" y1="250" x2="400" y2="250" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="120" y1="220" x2="400" y2="220" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="120" y1="190" x2="400" y2="190" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="120" y1="160" x2="400" y2="160" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="120" y1="130" x2="400" y2="130" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>

  <rect x="150" y="200" width="28" height="70" fill="#c0392b"/>
  <text x="164" y="194" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#c0392b" font-weight="bold">20%</text>

  <rect x="230" y="170" width="28" height="100" fill="#c0392b"/>
  <text x="244" y="164" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#c0392b" font-weight="bold">45%</text>

  <rect x="310" y="190" width="28" height="80" fill="#c0392b"/>
  <text x="324" y="184" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#c0392b" font-weight="bold">35%</text>

  <rect x="185" y="170" width="28" height="100" fill="#27ae60"/>
  <text x="199" y="164" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60" font-weight="bold">45%</text>

  <rect x="265" y="180" width="28" height="90" fill="#27ae60"/>
  <text x="279" y="174" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60" font-weight="bold">40%</text>

  <rect x="345" y="240" width="28" height="30" fill="#27ae60"/>
  <text x="359" y="234" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60" font-weight="bold">15%</text>

  <text x="164" y="290" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#1e3a5f">Високий</text>
  <text x="244" y="290" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#1e3a5f">Середній</text>
  <text x="324" y="290" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#1e3a5f">Низький</text>

  <!-- Права колонка: висновок -->
  <rect x="440" y="110" width="240" height="180" rx="8" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="560" y="135" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7e5109">Висновок за слайдом</text>
  <text x="460" y="162" font-family="Arial" font-size="10.5" fill="#7e5109">✓ Високий рівень зріс</text>
  <text x="460" y="182" font-family="Arial" font-size="10.5" fill="#7e5109">✓ Низький знизився</text>
  <text x="460" y="202" font-family="Arial" font-size="10.5" fill="#7e5109">✓ Відмінності статистично</text>
  <text x="472" y="220" font-family="Arial" font-size="10.5" fill="#7e5109">значущі (p&lt;0.05)</text>
  <text x="460" y="245" font-family="Arial" font-size="10.5" font-style="italic" fill="#b9770e">Порівняння з теорією:</text>
  <text x="460" y="263" font-family="Arial" font-size="10.5" font-style="italic" fill="#b9770e">узгоджується з працями</text>
  <text x="460" y="280" font-family="Arial" font-size="10.5" font-style="italic" fill="#b9770e">[Автор, рік]</text>

  <!-- Підпис -->
  <text x="380" y="405" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#475569">На слайді — лише найсуттєвіше: діаграма + 3–5 ключових тез + посилання на джерело</text>
</svg>
'''


# ============================================================
# 4. ЗМІСТ ДОКУМЕНТА
# ============================================================

def build_document():
    doc = setup_document()

    # ---------- Титульна частина ----------
    add_title(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 8", size=16, space_after=4)
    add_title(doc,
              "Формулювання висновків. Узагальнення результатів, "
              "розробка рекомендацій",
              size=15, space_after=10)
    add_title(doc, "Дисципліна: Основи науково-педагогічних досліджень",
              size=13, bold=False, space_after=2)
    add_title(doc, "Спеціальність: Початкова освіта", size=13, bold=False, space_after=12)

    # ---------- Мета ----------
    add_heading(doc, "Мета та завдання")
    add_paragraph(doc,
        "Мета: формувати вміння формулювати висновки, узагальнювати результати та "
        "розробляти рекомендації; розвивати вміння узагальнювати й практично "
        "застосовувати результати дослідження; виховувати відповідальність за "
        "практичне значення результатів.")
    add_paragraph(doc,
        "Завдання: опанувати структуру наукового висновку; навчитися формулювати "
        "висновки різних типів; розробляти рекомендації для різних адресатів; "
        "створювати презентацію результатів дослідження.")
    add_paragraph(doc, "Обладнання: інструкційні картки, комп'ютер, PowerPoint / Canva, проєктор.")

    # ---------- Література ----------
    add_heading(doc, "Література")
    add_numbered(doc, "Дубасенюк О. А. Методологія та методи науково-педагогічного "
                      "дослідження. Житомир: Полісся, 2016. 256 с.")
    add_numbered(doc, "Оліяр М. П., Русин Г. А., Червінька І. Б. Основи науково-педагогічних "
                      "досліджень (модульно-рейтинговий підхід). Івано-Франківськ: «Наїр», "
                      "2013. 214 с.")

    # ---------- 1. Піраміда ----------
    add_heading(doc, "1. Теоретична частина: від результатів до рекомендацій")
    add_paragraph(doc,
        "Завершальний етап дослідження — перетворення емпіричних даних на узагальнені "
        "висновки та практичні рекомендації. Це своєрідна «піраміда»: від конкретних "
        "фактів — через узагальнення — до обґрунтованих висновків і конкретних порад.")
    add_svg_image(doc, SVG_PYRAMID, width_cm=15,
                  caption="Рис. 1. Піраміда узагальнення результатів дослідження")

    # ---------- 2. Формула висновку ----------
    add_heading(doc, "2. Структура наукового висновку")
    add_paragraph(doc,
        "Науковий висновок — це не просто констатація факту, а логічно побудоване "
        "твердження, яке містить чотири обов'язкові компоненти.")
    add_svg_image(doc, SVG_CONCLUSION_FORMULA, width_cm=16,
                  caption="Рис. 2. Формула наукового висновку")

    add_heading(doc, "2.1. Вимоги до висновків", level=2)
    add_bullet(doc, "відповідність поставленим завданням (кожне завдання — хоча б один висновок);")
    add_bullet(doc, "лаконічність (1–3 речення на один висновок);")
    add_bullet(doc, "опора на отримані дані (без «води» та загальних фраз);")
    add_bullet(doc, "однозначність формулювань (без подвійного тлумачення);")
    add_bullet(doc, "коректність щодо гіпотези: підтверджено / частково підтверджено / спростовано;")
    add_bullet(doc, "відсутність нових фактів, яких не було в дослідженні.")

    # ---------- 3. Типи висновків ----------
    add_heading(doc, "3. Типи висновків")
    add_svg_image(doc, SVG_CONCLUSION_TYPES, width_cm=15,
                  caption="Рис. 3. Типи висновків у науково-педагогічному дослідженні")

    add_heading(doc, "3.1. Порівняльна таблиця типів висновків", level=2)
    add_table(doc,
        headers=["Тип", "На що спирається", "Приклад початку"],
        rows=[
            ["Теоретичний", "Аналіз джерел, уточнення понять",
             "«Уточнено зміст поняття … як …»"],
            ["Емпіричний", "Отримані дані, вимірювання",
             "«Встановлено, що рівень … зріс на … %»"],
            ["Практичний", "Потреби освітньої практики",
             "«Доцільно використовувати … для …»"],
        ],
        col_widths=[3.5, 6.5, 6.5])
    add_paragraph(doc, "Таблиця 1. Типи висновків та їхні особливості", italic=True,
                  indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 4. Рекомендації ----------
    add_heading(doc, "4. Розробка рекомендацій")
    add_paragraph(doc,
        "Рекомендації — це конкретні поради щодо практичного застосування результатів "
        "дослідження. Вони мають бути адресними, конкретними та реалістичними.")
    add_svg_image(doc, SVG_RECOMMENDATIONS, width_cm=15,
                  caption="Рис. 4. Адресати рекомендацій за результатами дослідження")

    add_heading(doc, "4.1. Алгоритм розробки рекомендацій", level=2)
    add_numbered(doc, "Визначте адресата: для кого саме призначена порада.")
    add_numbered(doc, "Сформулюйте конкретну дію, яку потрібно виконати.")
    add_numbered(doc, "Обґрунтуйте її результатами власного дослідження.")
    add_numbered(doc, "Вкажіть очікуваний ефект від впровадження.")
    add_numbered(doc, "Перевірте реалістичність: чи можна це зробити в умовах початкової школи.")

    add_heading(doc, "4.2. Приклади рекомендацій", level=2)
    add_bullet(doc, "«Вчителям початкових класів доцільно систематично (2–3 рази на тиждень) "
                    "використовувати дидактичні ігри з елементами змагання на уроках "
                    "математики, оскільки це, за нашими даними, підвищує пізнавальний "
                    "інтерес учнів на 25 %».",
               bold_prefix="Для вчителів: ")
    add_bullet(doc, "«Батькам рекомендується підтримувати пізнавальну активність дитини "
                    "вдома, заохочуючи самостійні спостереження та експерименти».",
               bold_prefix="Для батьків: ")
    add_bullet(doc, "«Адміністрації школи варто передбачити в плані методичної роботи "
                    "семінар-практикум з питань використання ігрових технологій».",
               bold_prefix="Для адміністрації: ")

    # ---------- 5. Презентація ----------
    add_heading(doc, "5. Створення презентації результатів дослідження")
    add_paragraph(doc,
        "Підсумковий результат практичної роботи — презентація дослідження. Вона має "
        "містити 10–12 слайдів і тривати 7–10 хвилин. Головний принцип — мінімум "
        "тексту, максимум наочності та аргументації.")
    add_svg_image(doc, SVG_PRESENTATION_STRUCTURE, width_cm=16,
                  caption="Рис. 5. Структура презентації результатів дослідження")

    add_heading(doc, "5.1. Вимоги до окремого слайда", level=2)
    add_bullet(doc, "один слайд — одна думка;")
    add_bullet(doc, "не більше 6 рядків тексту;")
    add_bullet(doc, "один візуальний об'єкт (таблиця, діаграма, схема) на слайді;")
    add_bullet(doc, "шрифт не менше 20 pt;")
    add_bullet(doc, "єдиний стиль оформлення всіх слайдів;")
    add_bullet(doc, "обов'язковий висновок під кожною діаграмою.")

    add_heading(doc, "5.2. Шаблон слайда з результатами", level=2)
    add_svg_image(doc, SVG_SLIDE_TEMPLATE, width_cm=15,
                  caption="Рис. 6. Шаблон слайда з результатами")

    # ---------- 6. Завдання ----------
    add_heading(doc, "6. Завдання для практичного виконання")
    add_numbered(doc, "Сформулюйте 3–4 висновки за результатами власного дослідження "
                      "(або навчального прикладу). Кожен висновок має містити всі "
                      "4 компоненти формули.")
    add_numbered(doc, "Розробіть 3 рекомендації для різних адресатів (учитель, батьки, "
                      "адміністрація) на основі отриманих висновків.")
    add_numbered(doc, "Створіть презентацію (10–12 слайдів) за темою власного дослідження "
                      "у PowerPoint або Canva, дотримуючись структури з Рис. 5.")
    add_numbered(doc, "На слайді з результатами використайте шаблон з Рис. 6: "
                      "діаграма + 3–5 тез + висновок під діаграмою.")
    add_numbered(doc, "Підготуйте усний виступ на 7 хвилин, що супроводжує презентацію "
                      "(тези — не читати зі слайдів, а розкривати їх).")
    add_numbered(doc, "Проведіть самооцінку презентації за критеріями нижче.")

    add_heading(doc, "Вимоги до звіту", level=2)
    add_bullet(doc, "файл презентації у форматі .pptx або .pdf;")
    add_bullet(doc, "окремий текст виступу (1–1,5 сторінки, шрифт Times New Roman 14 pt, "
                    "інтервал 1,25);")
    add_bullet(doc, "висновки оформлені окремим розділом;")
    add_bullet(doc, "рекомендації — за адресатами;")
    add_bullet(doc, "назва файлу: Прізвище_Ім'я_ПЗ8_Презентація.")

    # ---------- Критерії оцінювання ----------
    add_heading(doc, "7. Критерії оцінювання презентації")
    add_table(doc,
        headers=["Критерій", "Показники", "Бали"],
        rows=[
            ["Змістовність", "Повнота розкриття теми, логічність, обґрунтованість висновків", "4"],
            ["Структура", "Дотримання структури (12 слайдів), логіка викладу", "2"],
            ["Візуалізація", "Доречність діаграм і таблиць, єдність стилю, читабельність", "2"],
            ["Усний виступ", "Вільне володіння матеріалом, дотримання часу, відповіді на запитання", "1"],
            ["Рекомендації", "Адресність, конкретність, реалістичність", "1"],
        ],
        col_widths=[3.5, 10.0, 2.0])
    add_paragraph(doc, "Таблиця 2. Критерії оцінювання презентації (максимум — 10 балів)",
                  italic=True, indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 8. Контрольні запитання ----------
    add_heading(doc, "8. Контрольні запитання")
    add_numbered(doc, "Що таке науковий висновок і які його обов'язкові компоненти?")
    add_numbered(doc, "Чим відрізняються теоретичні, емпіричні та практичні висновки?")
    add_numbered(doc, "Які вимоги висувають до формулювання висновків у курсовій роботі?")
    add_numbered(doc, "Що таке рекомендації та кому вони можуть адресуватися?")
    add_numbered(doc, "Назвіть алгоритм розробки практичних рекомендацій.")
    add_numbered(doc, "Якою має бути структура презентації результатів дослідження?")
    add_numbered(doc, "Скільки слайдів доцільно мати в підсумковій презентації та чому?")
    add_numbered(doc, "Які вимоги висувають до окремого слайда (текст, візуалізація, шрифт)?")
    add_numbered(doc, "Чому не можна просто прочитати текст слайда під час виступу?")
    add_numbered(doc, "Як пов'язані висновки, рекомендації та гіпотеза дослідження?")

    # ---------- Файл ----------
    output = "PZ8_Vysnovky_Recomendatsii.docx"
    doc.save(output)
    print(f"✅ Документ створено: {output}")


if __name__ == "__main__":
    build_document()