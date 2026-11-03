# -*- coding: utf-8 -*-
"""
Генерація DOCX для практичного заняття № 6
Тема: Первинна обробка та графічне подання результатів педагогічного дослідження
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
                  align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
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


def add_table(doc, headers, rows, col_widths=None):
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
        run.font.size = Pt(12)
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
            run.font.size = Pt(12)

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

SVG_STAGES = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 260" width="820" height="260">
  <rect width="820" height="260" fill="#ffffff"/>
  <text x="410" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Етапи первинної обробки результатів дослідження</text>

  <rect x="20" y="60" width="130" height="90" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="85" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">1. Збір</text>
  <text x="85" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">первинних</text>
  <text x="85" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">даних</text>

  <polygon points="155,105 172,95 172,115" fill="#2980b9"/>

  <rect x="176" y="60" width="130" height="90" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="241" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e5a3f">2. Перевірка</text>
  <text x="241" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">повнота,</text>
  <text x="241" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">коректність</text>

  <polygon points="311,105 328,95 328,115" fill="#2980b9"/>

  <rect x="332" y="60" width="130" height="90" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="397" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7e5109">3. Кодування</text>
  <text x="397" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">бали, шкали,</text>
  <text x="397" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">індекси</text>

  <polygon points="467,105 484,95 484,115" fill="#2980b9"/>

  <rect x="488" y="60" width="130" height="90" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="553" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#4a235a">4. Групування</text>
  <text x="553" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">за рівнями,</text>
  <text x="553" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">групами</text>

  <polygon points="623,105 640,95 640,115" fill="#2980b9"/>

  <rect x="644" y="60" width="150" height="90" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="719" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7b241c">5. Унаочнення</text>
  <text x="719" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#c0392b">таблиці,</text>
  <text x="719" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#c0392b">діаграми</text>

  <text x="410" y="190" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic" fill="#475569">Результат: перетворення «сирих» даних на інформативні показники</text>
  <text x="410" y="220" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic" fill="#475569">для подальшої інтерпретації та висновків</text>
</svg>
'''

SVG_BAR_LEVELS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 380" width="720" height="380">
  <rect width="720" height="380" fill="#ffffff"/>
  <text x="360" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Розподіл учнів за рівнями сформованості (n = 40)</text>

  <line x1="180" y1="50" x2="180" y2="330" stroke="#cbd5e1" stroke-width="1"/>
  <line x1="300" y1="50" x2="300" y2="330" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="420" y1="50" x2="420" y2="330" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="540" y1="50" x2="540" y2="330" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="660" y1="50" x2="660" y2="330" stroke="#cbd5e1" stroke-width="1"/>

  <text x="180" y="348" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">0%</text>
  <text x="300" y="348" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">20%</text>
  <text x="420" y="348" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">40%</text>
  <text x="540" y="348" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">60%</text>
  <text x="660" y="348" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">80%</text>

  <text x="170" y="85" text-anchor="end" font-family="Arial" font-size="12.5" fill="#1e3a5f">Високий</text>
  <rect x="180" y="65" width="120" height="32" rx="5" fill="#27ae60"/>
  <text x="306" y="86" font-family="Arial" font-size="11" fill="#1e3a5f" font-weight="bold">20% (8 учнів)</text>

  <text x="170" y="150" text-anchor="end" font-family="Arial" font-size="12.5" fill="#1e3a5f">Середній</text>
  <rect x="180" y="130" width="270" height="32" rx="5" fill="#e67e22"/>
  <text x="456" y="151" font-family="Arial" font-size="11" fill="#1e3a5f" font-weight="bold">45% (18 учнів)</text>

  <text x="170" y="215" text-anchor="end" font-family="Arial" font-size="12.5" fill="#1e3a5f">Низький</text>
  <rect x="180" y="195" width="210" height="32" rx="5" fill="#c0392b"/>
  <text x="396" y="216" font-family="Arial" font-size="11" fill="#1e3a5f" font-weight="bold">35% (14 учнів)</text>

  <text x="360" y="295" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Графік дає змогу одразу побачити переважання середнього рівня</text>
</svg>
'''

SVG_PIE_GROUPS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340" width="600" height="340">
  <rect width="600" height="340" fill="#ffffff"/>
  <text x="300" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Порівняння контрольної та експериментальної груп</text>

  <circle cx="180" cy="180" r="80" fill="none" stroke="#e2e8f0" stroke-width="44"/>
  <g transform="rotate(-90 180 180)">
    <circle cx="180" cy="180" r="80" fill="none" stroke="#2980b9" stroke-width="44"
            stroke-dasharray="188.5 502.65" stroke-dashoffset="0"/>
    <circle cx="180" cy="180" r="80" fill="none" stroke="#27ae60" stroke-width="44"
            stroke-dasharray="125.66 502.65" stroke-dashoffset="-188.5"/>
    <circle cx="180" cy="180" r="80" fill="none" stroke="#e67e22" stroke-width="44"
            stroke-dasharray="125.66 502.65" stroke-dashoffset="-314.16"/>
  </g>
  <text x="180" y="177" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">Контрольна</text>
  <text x="180" y="194" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">група (n = 20)</text>

  <rect x="330" y="120" width="18" height="18" rx="3" fill="#2980b9"/>
  <text x="356" y="134" font-family="Arial" font-size="12" fill="#1e3a5f">Високий — 30%</text>

  <rect x="330" y="155" width="18" height="18" rx="3" fill="#27ae60"/>
  <text x="356" y="169" font-family="Arial" font-size="12" fill="#1e3a5f">Середній — 50%</text>

  <rect x="330" y="190" width="18" height="18" rx="3" fill="#e67e22"/>
  <text x="356" y="204" font-family="Arial" font-size="12" fill="#1e3a5f">Низький — 20%</text>

  <text x="300" y="270" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Кругова діаграма зручна для подання співвідношення частин цілого</text>
  <text x="300" y="292" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">(частки учнів кожного рівня в групі)</text>
</svg>
'''

SVG_LINE_DYNAMICS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 380" width="720" height="380">
  <rect width="720" height="380" fill="#ffffff"/>
  <text x="360" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Динаміка середнього балу за три зрізи</text>

  <line x1="90" y1="60" x2="90" y2="300" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="90" y1="300" x2="650" y2="300" stroke="#94a3b8" stroke-width="1.5"/>

  <line x1="90" y1="240" x2="650" y2="240" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="90" y1="180" x2="650" y2="180" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="90" y1="120" x2="650" y2="120" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="90" y1="60" x2="650" y2="60" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>

  <text x="80" y="304" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">0</text>
  <text x="80" y="244" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">3</text>
  <text x="80" y="184" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">6</text>
  <text x="80" y="124" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">9</text>
  <text x="80" y="64" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">12</text>

  <text x="180" y="322" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Констатувальний</text>
  <text x="360" y="322" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Проміжний</text>
  <text x="540" y="322" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Контрольний</text>

  <polyline points="180,240 360,180 540,120"
            fill="none" stroke="#2980b9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="180" cy="240" r="6" fill="#2980b9"/>
  <circle cx="360" cy="180" r="6" fill="#2980b9"/>
  <circle cx="540" cy="120" r="6" fill="#2980b9"/>
  <text x="190" y="234" font-family="Arial" font-size="11" fill="#1e3a5f" font-weight="bold">5,4</text>
  <text x="370" y="174" font-family="Arial" font-size="11" fill="#1e3a5f" font-weight="bold">7,8</text>
  <text x="550" y="114" font-family="Arial" font-size="11" fill="#1e3a5f" font-weight="bold">9,6</text>

  <text x="360" y="356" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Лінійний графік — оптимальний для показу тенденцій у часі</text>
</svg>
'''

SVG_PICTOGRAM = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 360" width="600" height="360">
  <rect width="600" height="360" fill="#ffffff"/>
  <text x="300" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Піктограма: кількість учнів, які досягли високого рівня</text>

  <text x="60" y="80" font-family="Arial" font-size="12" fill="#1e3a5f" font-weight="bold">1 клас</text>
  <g>
    <circle cx="160" cy="75" r="11" fill="#27ae60"/>
    <circle cx="190" cy="75" r="11" fill="#27ae60"/>
    <circle cx="220" cy="75" r="11" fill="#27ae60"/>
  </g>
  <text x="245" y="80" font-family="Arial" font-size="11" fill="#1e3a5f">— 3 учні</text>

  <text x="60" y="140" font-family="Arial" font-size="12" fill="#1e3a5f" font-weight="bold">2 клас</text>
  <g>
    <circle cx="160" cy="135" r="11" fill="#27ae60"/>
    <circle cx="190" cy="135" r="11" fill="#27ae60"/>
    <circle cx="220" cy="135" r="11" fill="#27ae60"/>
    <circle cx="250" cy="135" r="11" fill="#27ae60"/>
    <circle cx="280" cy="135" r="11" fill="#27ae60"/>
  </g>
  <text x="305" y="140" font-family="Arial" font-size="11" fill="#1e3a5f">— 5 учнів</text>

  <text x="60" y="200" font-family="Arial" font-size="12" fill="#1e3a5f" font-weight="bold">3 клас</text>
  <g>
    <circle cx="160" cy="195" r="11" fill="#27ae60"/>
    <circle cx="190" cy="195" r="11" fill="#27ae60"/>
    <circle cx="220" cy="195" r="11" fill="#27ae60"/>
    <circle cx="250" cy="195" r="11" fill="#27ae60"/>
    <circle cx="280" cy="195" r="11" fill="#27ae60"/>
    <circle cx="310" cy="195" r="11" fill="#27ae60"/>
    <circle cx="340" cy="195" r="11" fill="#27ae60"/>
  </g>
  <text x="365" y="200" font-family="Arial" font-size="11" fill="#1e3a5f">— 7 учнів</text>

  <text x="60" y="260" font-family="Arial" font-size="12" fill="#1e3a5f" font-weight="bold">4 клас</text>
  <g>
    <circle cx="160" cy="255" r="11" fill="#27ae60"/>
    <circle cx="190" cy="255" r="11" fill="#27ae60"/>
    <circle cx="220" cy="255" r="11" fill="#27ae60"/>
    <circle cx="250" cy="255" r="11" fill="#27ae60"/>
    <circle cx="280" cy="255" r="11" fill="#27ae60"/>
    <circle cx="310" cy="255" r="11" fill="#27ae60"/>
    <circle cx="340" cy="255" r="11" fill="#27ae60"/>
    <circle cx="370" cy="255" r="11" fill="#27ae60"/>
    <circle cx="400" cy="255" r="11" fill="#27ae60"/>
  </g>
  <text x="425" y="260" font-family="Arial" font-size="11" fill="#1e3a5f">— 9 учнів</text>

  <text x="300" y="320" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Піктограма — наочний спосіб для молодшої аудиторії</text>
  <text x="300" y="342" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">(1 символ = 1 учень)</text>
</svg>
'''


# ============================================================
# 4. ЗМІСТ ДОКУМЕНТА
# ============================================================

def build_document():
    doc = setup_document()

    add_title(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 6", size=16, space_after=4)
    add_title(doc,
              "Первинна обробка та графічне подання результатів педагогічного дослідження",
              size=15, space_after=10)
    add_title(doc, "Дисципліна: Основи науково-педагогічних досліджень",
              size=13, bold=False, space_after=2)
    add_title(doc, "Спеціальність: Початкова освіта", size=13, bold=False, space_after=12)

    add_heading(doc, "Мета та завдання")
    add_paragraph(doc,
        "Мета: формувати вміння первинної обробки та графічного подання результатів "
        "педагогічного дослідження; розвивати вміння візуалізувати й інтерпретувати "
        "дослідницькі дані; виховувати точність і наочність у представленні результатів.")
    add_paragraph(doc,
        "Завдання: опанувати послідовність первинної обробки даних; навчитися обирати "
        "доцільний тип діаграми для різних видів даних; формувати вміння коректно "
        "інтерпретувати графічні результати та робити висновки.")
    add_paragraph(doc, "Обладнання: інструкційні картки, комп'ютер, проєктор, Excel / Google Sheets.")

    add_heading(doc, "Література")
    add_numbered(doc, "Методичні рекомендації до виконання та захисту курсових робіт для здобувачів "
                      "ОС «Бакалавр» спеціальності 012 «Дошкільна освіта» / уклад. Н. В. Лісневська та ін. "
                      "Глухів, 2023. 65 с.")
    add_numbered(doc, "Кравець Н. П. Основи наукових досліджень: навчальний посібник. "
                      "Київ: Вид-во НПУ імені М. П. Драгоманова, 2020. 74 с.")

    # ---------- 1. Етапи ----------
    add_heading(doc, "1. Теоретична частина: етапи первинної обробки результатів")
    add_paragraph(doc,
        "Первинна обробка — це впорядкування, систематизація та перетворення «сирих» "
        "даних дослідження на показники, придатні для аналізу й унаочнення. Вона включає "
        "п'ять послідовних етапів.")
    add_svg_image(doc, SVG_STAGES, width_cm=16,
                  caption="Рис. 1. Етапи первинної обробки результатів дослідження")

    add_paragraph(doc,
        "На етапі збору фіксують відповіді, бали, результати спостережень. Далі перевіряють "
        "повноту й коректність заповнення протоколів. Кодування передбачає переведення "
        "якісних відповідей у бали або шкальні оцінки. Групування дає змогу об'єднати учнів "
        "за рівнями. Завершальний етап — унаочнення у вигляді таблиць і діаграм.")

    # ---------- 2. Таблиці ----------
    add_heading(doc, "2. Табличне подання результатів")
    add_paragraph(doc,
        "Таблиця — найточніший спосіб подання числових даних. Вона має містити номер, "
        "назву, чітко підписані рядки та стовпці, одиниці вимірювання.")
    add_paragraph(doc, "Приклад: результати констатувального зрізу в контрольній та експериментальній групах.")
    add_table(doc,
        headers=["Рівень", "Контрольна група (n = 20)", "Експериментальна група (n = 20)"],
        rows=[
            ["Високий", "6 (30 %)", "5 (25 %)"],
            ["Середній", "10 (50 %)", "11 (55 %)"],
            ["Низький", "4 (20 %)", "4 (20 %)"],
        ],
        col_widths=[3.5, 6.0, 7.0])
    add_paragraph(doc, "Таблиця 1. Розподіл учнів за рівнями сформованості", italic=True,
                  indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 3. Графічне подання ----------
    add_heading(doc, "3. Графічне подання результатів")
    add_paragraph(doc,
        "Графіки й діаграми роблять результати наочними та доступними для швидкого "
        "сприйняття. Вибір типу діаграми залежить від характеру даних і мети подання.")

    add_heading(doc, "3.1. Вибір типу діаграми", level=2)
    add_table(doc,
        headers=["Тип діаграми", "Для чого використовують", "Приклад"],
        rows=[
            ["Стовпчикова", "Порівняння категорій між собою", "Рівні сформованості в групах"],
            ["Кругова", "Співвідношення частин цілого", "Частки учнів кожного рівня"],
            ["Лінійна", "Динаміка показника в часі", "Середній бал за три зрізи"],
            ["Піктограма", "Наочне подання для молодшої аудиторії", "Кількість учнів за класами"],
            ["Гістограма", "Розподіл частот числового показника", "Розподіл балів тесту"],
        ],
        col_widths=[4.0, 7.0, 6.0])
    add_paragraph(doc, "Таблиця 2. Рекомендації щодо вибору типу діаграми", italic=True,
                  indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_heading(doc, "3.2. Приклади діаграм", level=2)
    add_svg_image(doc, SVG_BAR_LEVELS, width_cm=15,
                  caption="Рис. 2. Стовпчикова діаграма: розподіл учнів за рівнями")
    add_svg_image(doc, SVG_PIE_GROUPS, width_cm=13,
                  caption="Рис. 3. Кругова діаграма: співвідношення рівнів у групі")
    add_svg_image(doc, SVG_LINE_DYNAMICS, width_cm=15,
                  caption="Рис. 4. Лінійний графік: динаміка середнього балу")
    add_svg_image(doc, SVG_PICTOGRAM, width_cm=14,
                  caption="Рис. 5. Піктограма: кількість учнів високого рівня за класами")

    # ---------- 4. Інтерпретація ----------
    add_heading(doc, "4. Інтерпретація графічних результатів")
    add_paragraph(doc,
        "Побудувати діаграму — лише половина справи. Дослідник має вміти «прочитати» "
        "графік і сформулювати змістовний висновок. Алгоритм інтерпретації:")
    add_numbered(doc, "Визначте, що саме показує діаграма (які показники, які групи).")
    add_numbered(doc, "Порівняйте значення: який рівень переважає, який найменший.")
    add_numbered(doc, "Зверніть увагу на тенденцію: показник зростає, знижується чи стабільний.")
    add_numbered(doc, "Сформулюйте висновок у 2–3 реченнях, спираючись на числові дані.")
    add_numbered(doc, "Пов'яжіть висновок з метою та гіпотезою дослідження.")

    add_heading(doc, "4.1. Типові помилки", level=2)
    add_bullet(doc, "надмірна кількість діаграм, які дублюють одна одну;")
    add_bullet(doc, "відсутність підписів осей, одиниць вимірювання, легенди;")
    add_bullet(doc, "використання кругової діаграми для показу динаміки;")
    add_bullet(doc, "некоректний масштаб осей, що викривлює реальне співвідношення;")
    add_bullet(doc, "відсутність висновку під діаграмою;")
    add_bullet(doc, "різні кольори для одних і тих самих категорій у різних діаграмах.")

    # ---------- 5. Завдання ----------
    add_heading(doc, "5. Завдання для практичного виконання")
    add_numbered(doc, "За наведеними даними побудуйте таблицю розподілу учнів за рівнями "
                      "(високий — 8, середній — 18, низький — 14; усього 40 учнів) та обчисліть відсотки.")
    add_numbered(doc, "Побудуйте стовпчикову діаграму за даними завдання 1 у Excel або Google Sheets.")
    add_numbered(doc, "Побудуйте кругову діаграму для тих самих даних. Порівняйте, яка діаграма "
                      "краще передає інформацію і чому.")
    add_numbered(doc, "За даними динаміки середнього балу (5,4 → 7,8 → 9,6) побудуйте лінійний "
                      "графік і сформулюйте висновок про тенденцію.")
    add_numbered(doc, "Створіть піктограму для даних: 1 клас — 3 учні, 2 клас — 5, 3 клас — 7, "
                      "4 клас — 9 (високий рівень).")
    add_numbered(doc, "Напишіть інтерпретацію (3–5 речень) до однієї з побудованих діаграм.")

    add_heading(doc, "Вимоги до звіту", level=2)
    add_bullet(doc, "звіт оформлюють у Word або PDF;")
    add_bullet(doc, "кожна таблиця і діаграма має номер і назву;")
    add_bullet(doc, "під кожною діаграмою — короткий висновок (2–3 речення);")
    add_bullet(doc, "шрифт Times New Roman, 14 pt, інтервал 1,25, вирівнювання по ширині;")
    add_bullet(doc, "назва файлу: Прізвище_Ім'я_ПЗ6_Обробка_результатів.")

    # ---------- 6. Контрольні запитання ----------
    add_heading(doc, "6. Контрольні запитання")
    add_numbered(doc, "Що таке первинна обробка результатів дослідження і які її етапи?")
    add_numbered(doc, "Які вимоги висувають до оформлення таблиць у науковій роботі?")
    add_numbered(doc, "Як обрати доцільний тип діаграми для різних видів даних?")
    add_numbered(doc, "Чим відрізняються стовпчикова, кругова та лінійна діаграми за призначенням?")
    add_numbered(doc, "У яких випадках доцільно використовувати піктограму?")
    add_numbered(doc, "Назвіть типові помилки графічного подання результатів.")
    add_numbered(doc, "Яким має бути алгоритм інтерпретації діаграми?")
    add_numbered(doc, "Чому під кожною діаграмою потрібно подавати короткий висновок?")

    output = "PZ6_Obrobka_rezultativ.docx"
    doc.save(output)
    print(f"✅ Документ створено: {output}")


if __name__ == "__main__":
    build_document()