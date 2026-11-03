# -*- coding: utf-8 -*-
"""
Генерація DOCX для практичного заняття № 9
Тема: Оформлення наукової роботи. Структура наукової статті,
      дипломної роботи, звіту про дослідження
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

SVG_FORMATTING_REQUIREMENTS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" width="800" height="420">
  <rect width="800" height="420" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Загальні вимоги до оформлення наукової роботи</text>

  <!-- Сторінка -->
  <rect x="150" y="55" width="500" height="290" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>

  <!-- Верхнє поле 2 см -->
  <rect x="150" y="55" width="500" height="35" fill="#eaf4fc"/>
  <text x="400" y="78" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold" fill="#1e3a5f">верхнє поле — 2 см</text>

  <!-- Нижнє поле 2 см -->
  <rect x="150" y="310" width="500" height="35" fill="#eaf4fc"/>
  <text x="400" y="333" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold" fill="#1e3a5f">нижнє поле — 2 см</text>

  <!-- Ліве поле 3 см -->
  <rect x="150" y="90" width="75" height="220" fill="#e8f6f3"/>
  <text x="187" y="205" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold" fill="#1e5a3f" transform="rotate(-90 187 205)">ліве поле — 3 см</text>

  <!-- Праве поле 1.5 см -->
  <rect x="612" y="90" width="38" height="220" fill="#fef9e7"/>
  <text x="631" y="205" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold" fill="#7e5109" transform="rotate(90 631 205)">праве поле — 1,5 см</text>

  <!-- Тіло сторінки -->
  <rect x="225" y="90" width="387" height="220" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>

  <!-- Текст-заготовка -->
  <line x1="245" y1="115" x2="590" y2="115" stroke="#cbd5e1" stroke-width="4"/>
  <line x1="245" y1="130" x2="590" y2="130" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="145" x2="560" y2="145" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="160" x2="590" y2="160" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="175" x2="540" y2="175" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="190" x2="590" y2="190" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="205" x2="575" y2="205" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="220" x2="590" y2="220" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="235" x2="555" y2="235" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="250" x2="590" y2="250" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="265" x2="580" y2="265" stroke="#e2e8f0" stroke-width="3"/>
  <line x1="245" y1="280" x2="565" y2="280" stroke="#e2e8f0" stroke-width="3"/>

  <!-- Підпис -->
  <text x="400" y="375" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Шрифт: <tspan font-weight="bold">Times New Roman, 14 pt</tspan> · Інтервал: <tspan font-weight="bold">1,5</tspan></text>
  <text x="400" y="398" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Вирівнювання: <tspan font-weight="bold">по ширині</tspan> · Абзацний відступ: <tspan font-weight="bold">1,25 см</tspan></text>
  <text x="400" y="415" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">Нумерація сторінок — у правому нижньому куті, починаючи з титульної (не проставляється)</text>
</svg>
'''

SVG_ARTICLE_STRUCTURE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480">
  <rect width="800" height="480" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура наукової статті</text>

  <rect x="240" y="45" width="320" height="40" rx="8" fill="#1e3a5f"/>
  <text x="400" y="72" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">НАУКОВА СТАТТЯ</text>

  <line x1="400" y1="85" x2="400" y2="100" stroke="#94a3b8" stroke-width="2"/>

  <rect x="200" y="100" width="400" height="40" rx="6" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="400" y="125" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">1. УДК та бібліографічний опис автора</text>

  <rect x="200" y="148" width="400" height="40" rx="6" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="400" y="173" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e5a3f">2. Назва статті (інформативна, ≤ 10 слів)</text>

  <rect x="200" y="196" width="400" height="40" rx="6" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="400" y="221" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7e5109">3. Анотація (укр. + англ.) та ключові слова</text>

  <rect x="200" y="244" width="400" height="40" rx="6" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="400" y="269" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#4a235a">4. Постановка проблеми та її актуальність</text>

  <rect x="200" y="292" width="400" height="40" rx="6" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="400" y="317" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7b241c">5. Аналіз останніх досліджень і публікацій</text>

  <rect x="200" y="340" width="400" height="40" rx="6" fill="#e8f8f5" stroke="#16a085" stroke-width="1.5"/>
  <text x="400" y="365" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#0e6655">6. Мета, завдання, методи дослідження</text>

  <rect x="200" y="388" width="400" height="40" rx="6" fill="#fdf2e9" stroke="#d35400" stroke-width="1.5"/>
  <text x="400" y="413" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#a04000">7. Виклад основного матеріалу + висновки</text>

  <rect x="200" y="436" width="400" height="30" rx="6" fill="#ebf5fb" stroke="#2e86c1" stroke-width="1.5"/>
  <text x="400" y="456" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1a5276">8. Список використаних джерел</text>

  <!-- Коментарі праворуч -->
  <text x="615" y="125" font-family="Arial" font-size="10.5" fill="#2980b9">обов'язково</text>
  <text x="615" y="173" font-family="Arial" font-size="10.5" fill="#27ae60">без «води»</text>
  <text x="615" y="221" font-family="Arial" font-size="10.5" fill="#e67e22">150–250 слів</text>
  <text x="615" y="269" font-family="Arial" font-size="10.5" fill="#8e44ad">1–2 абзаци</text>
  <text x="615" y="317" font-family="Arial" font-size="10.5" fill="#c0392b">огляд</text>
  <text x="615" y="365" font-family="Arial" font-size="10.5" fill="#16a085">науковий апарат</text>
  <text x="615" y="413" font-family="Arial" font-size="10.5" fill="#d35400">основна частина</text>
  <text x="615" y="456" font-family="Arial" font-size="10.5" fill="#2e86c1">10–25 джерел</text>
</svg>
'''

SVG_DIPLOMA_STRUCTURE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 540" width="820" height="540">
  <rect width="820" height="540" fill="#ffffff"/>
  <text x="410" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура дипломної (кваліфікаційної) роботи</text>

  <rect x="230" y="45" width="360" height="40" rx="8" fill="#1e3a5f"/>
  <text x="410" y="72" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">ДИПЛОМНА РОБОТА</text>

  <!-- Ліва колонка -->
  <rect x="30" y="105" width="360" height="42" rx="6" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="210" y="131" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">Титульна сторінка</text>

  <rect x="30" y="155" width="360" height="42" rx="6" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="210" y="181" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e5a3f">Завдання на роботу (за потреби)</text>

  <rect x="30" y="205" width="360" height="42" rx="6" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="210" y="231" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">Анотація / Реферат</text>

  <rect x="30" y="255" width="360" height="42" rx="6" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="210" y="281" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">Зміст (2–3 сторінки)</text>

  <rect x="30" y="305" width="360" height="42" rx="6" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="210" y="331" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">Перелік умовних позначень</text>

  <rect x="30" y="355" width="360" height="42" rx="6" fill="#e8f8f5" stroke="#16a085" stroke-width="1.5"/>
  <text x="210" y="381" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#0e6655">Вступ (3–5 сторінок)</text>

  <!-- Права колонка -->
  <rect x="430" y="105" width="360" height="42" rx="6" fill="#fdf2e9" stroke="#d35400" stroke-width="1.5"/>
  <text x="610" y="131" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#a04000">Розділ 1. Теоретичний</text>

  <rect x="430" y="155" width="360" height="42" rx="6" fill="#fdf2e9" stroke="#d35400" stroke-width="1.5"/>
  <text x="610" y="181" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#a04000">Розділ 2. Методика</text>

  <rect x="430" y="205" width="360" height="42" rx="6" fill="#fdf2e9" stroke="#d35400" stroke-width="1.5"/>
  <text x="610" y="231" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#a04000">Розділ 3. Емпіричний</text>

  <rect x="430" y="255" width="360" height="42" rx="6" fill="#fdf2e9" stroke="#d35400" stroke-width="1.5"/>
  <text x="610" y="281" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#a04000">Висновки до розділів</text>

  <rect x="430" y="305" width="360" height="42" rx="6" fill="#ebf5fb" stroke="#2e86c1" stroke-width="1.5"/>
  <text x="610" y="331" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1a5276">Загальні висновки</text>

  <rect x="430" y="355" width="360" height="42" rx="6" fill="#f5eef8" stroke="#7d3c98" stroke-width="1.5"/>
  <text x="610" y="381" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#512e5f">Список використаних джерел</text>

  <!-- Нижній ряд -->
  <rect x="130" y="420" width="250" height="42" rx="6" fill="#fef5e7" stroke="#b9770e" stroke-width="1.5"/>
  <text x="255" y="446" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">Додатки (таблиці, анкети)</text>

  <rect x="410" y="420" width="280" height="42" rx="6" fill="#eafaf1" stroke="#1e8449" stroke-width="1.5"/>
  <text x="550" y="446" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#145a32">Презентація / захист (8–10 хв.)</text>

  <text x="410" y="500" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Орієнтовний обсяг: 50–70 сторінок (без додатків)</text>
  <text x="410" y="522" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Кожен розділ завершується висновками; загальні висновки співвідносяться з метою та завданнями</text>
</svg>
'''

SVG_REPORT_STRUCTURE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="800" height="400">
  <rect width="800" height="400" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура звіту про дослідження</text>

  <rect x="180" y="45" width="440" height="42" rx="8" fill="#1e3a5f"/>
  <text x="400" y="72" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">ЗВІТ ПРО ДОСЛІДЖЕННЯ</text>

  <line x1="400" y1="87" x2="400" y2="105" stroke="#94a3b8" stroke-width="2"/>

  <rect x="180" y="105" width="440" height="38" rx="6" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="400" y="128" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">1. Вступна частина (мета, завдання, гіпотеза, методи)</text>

  <rect x="180" y="151" width="440" height="38" rx="6" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="400" y="174" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e5a3f">2. Теоретичне обґрунтування</text>

  <rect x="180" y="197" width="440" height="38" rx="6" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="400" y="220" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">3. Опис методики та вибірки</text>

  <rect x="180" y="243" width="440" height="38" rx="6" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="400" y="266" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">4. Результати (таблиці, діаграми)</text>

  <rect x="180" y="289" width="440" height="38" rx="6" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="400" y="312" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">5. Інтерпретація та обговорення</text>

  <rect x="180" y="335" width="440" height="38" rx="6" fill="#e8f8f5" stroke="#16a085" stroke-width="1.5"/>
  <text x="400" y="358" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#0e6655">6. Висновки та рекомендації</text>

  <rect x="240" y="381" width="320" height="30" rx="6" fill="#ebf5fb" stroke="#2e86c1" stroke-width="1.5"/>
  <text x="400" y="400" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold" fill="#1a5276">7. Додатки та список джерел</text>

  <text x="60" y="270" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">Обсяг:</text>
  <text x="60" y="285" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">10–25 стор.</text>

  <text x="650" y="270" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">Стиль:</text>
  <text x="650" y="285" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">стислий,</text>
  <text x="650" y="300" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">науковий</text>
</svg>
'''

SVG_COMPARISON = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 440" width="800" height="440">
  <rect width="800" height="440" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Порівняння обсягу та призначення видів наукових робіт</text>

  <!-- Стовпчик 1 -->
  <rect x="55" y="80" width="200" height="250" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="155" y="108" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#1e3a5f">СТАТТЯ</text>
  <text x="155" y="145" text-anchor="middle" font-family="Arial" font-size="26" font-weight="bold" fill="#2980b9">8–12</text>
  <text x="155" y="165" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#2980b9">сторінок</text>
  <text x="155" y="195" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Публікація</text>
  <text x="155" y="212" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">результатів</text>
  <text x="155" y="229" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">дослідження</text>
  <text x="155" y="265" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">1 автор або</text>
  <text x="155" y="282" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">2–3 співавтори</text>
  <text x="155" y="308" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">обов'язкова</text>

  <!-- Стовпчик 2 -->
  <rect x="300" y="80" width="200" height="250" rx="10" fill="#fdf2e9" stroke="#d35400" stroke-width="2"/>
  <text x="400" y="108" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#a04000">ДИПЛОМНА</text>
  <text x="400" y="145" text-anchor="middle" font-family="Arial" font-size="26" font-weight="bold" fill="#d35400">50–70</text>
  <text x="400" y="165" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#d35400">сторінок</text>
  <text x="400" y="195" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Кваліфікаційна</text>
  <text x="400" y="212" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">робота на</text>
  <text x="400" y="229" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">здобуття ступеня</text>
  <text x="400" y="265" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">1 автор</text>
  <text x="400" y="282" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">(обов'язково)</text>
  <text x="400" y="308" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#d35400">обов'язковий</text>
  <text x="400" y="325" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#d35400">захист</text>

  <!-- Стовпчик 3 -->
  <rect x="545" y="80" width="200" height="250" rx="10" fill="#eafaf1" stroke="#1e8449" stroke-width="2"/>
  <text x="645" y="108" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#145a32">ЗВІТ</text>
  <text x="645" y="145" text-anchor="middle" font-family="Arial" font-size="26" font-weight="bold" fill="#1e8449">10–25</text>
  <text x="645" y="165" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e8449">сторінок</text>
  <text x="645" y="195" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Опис ходу та</text>
  <text x="645" y="212" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">результатів</text>
  <text x="645" y="229" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">дослідження</text>
  <text x="645" y="265" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">1 автор</text>
  <text x="645" y="282" text-anchor="middle" font-family="Arial" font-size="10.5" font-style="italic" fill="#64748b">або група</text>
  <text x="645" y="308" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#1e8449">може бути</text>
  <text x="645" y="325" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#1e8449">без захисту</text>

  <text x="400" y="375" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">Спільне для всіх видів:</text>
  <text x="400" y="398" text-anchor="middle" font-family="Arial" font-size="11" fill="#475569">чітка структура (вступ → основна частина → висновки),</text>
  <text x="400" y="418" text-anchor="middle" font-family="Arial" font-size="11" fill="#475569">дотримання академічної доброчесності, єдине оформлення за ДСТУ</text>
</svg>
'''

SVG_ERRORS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="800" height="400">
  <rect width="800" height="400" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Типові помилки оформлення наукової роботи</text>

  <rect x="25" y="55" width="365" height="135" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="45" y="82" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">1. Порушення технічних вимог</text>
  <text x="45" y="105" font-family="Arial" font-size="10.5" fill="#a93226">• Невідповідний шрифт (не TNR)</text>
  <text x="45" y="122" font-family="Arial" font-size="10.5" fill="#a93226">• Інший інтервал (1,0 або 2,0)</text>
  <text x="45" y="139" font-family="Arial" font-size="10.5" fill="#a93226">• Неправильні поля (не 3-2-2-1,5 см)</text>
  <text x="45" y="156" font-family="Arial" font-size="10.5" fill="#a93226">• Відсутність нумерації сторінок</text>
  <text x="45" y="178" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Перевіряйте технічні вимоги ЗВН перед поданням</text>

  <rect x="410" y="55" width="365" height="135" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="430" y="82" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">2. Структурні порушення</text>
  <text x="430" y="105" font-family="Arial" font-size="10.5" fill="#a93226">• Відсутність анотації</text>
  <text x="430" y="122" font-family="Arial" font-size="10.5" fill="#a93226">• Немає висновків до розділів</text>
  <text x="430" y="139" font-family="Arial" font-size="10.5" fill="#a93226">• Зміст не відповідає тексту</text>
  <text x="430" y="156" font-family="Arial" font-size="10.5" fill="#a93226">• Порушені пропорції розділів</text>
  <text x="430" y="178" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Складіть структуру ПЕРЕД написанням</text>

  <rect x="25" y="205" width="365" height="135" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="45" y="232" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">3. Оформлення джерел і цитат</text>
  <text x="45" y="255" font-family="Arial" font-size="10.5" fill="#a93226">• Список не за ДСТУ 8302:2015</text>
  <text x="45" y="272" font-family="Arial" font-size="10.5" fill="#a93226">• Покликання не за номером</text>
  <text x="45" y="289" font-family="Arial" font-size="10.5" fill="#a93226">• Джерела не в алфавіті</text>
  <text x="45" y="306" font-family="Arial" font-size="10.5" fill="#a93226">• Плагіат без посилання</text>
  <text x="45" y="328" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Уніфікуйте ВСІ описи за одним зразком</text>

  <rect x="410" y="205" width="365" height="135" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="430" y="232" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">4. Ілюстрації та таблиці</text>
  <text x="430" y="255" font-family="Arial" font-size="10.5" fill="#a93226">• Відсутність номерів і назв</text>
  <text x="430" y="272" font-family="Arial" font-size="10.5" fill="#a93226">• Розрив таблиці між сторінками</text>
  <text x="430" y="289" font-family="Arial" font-size="10.5" fill="#a93226">• Немає посилання в тексті</text>
  <text x="430" y="306" font-family="Arial" font-size="10.5" fill="#a93226">• Різний стиль підписів</text>
  <text x="430" y="328" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Кожна ілюстрація: підпис + посилання в тексті</text>
</svg>
'''

SVG_CHECKLIST = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 460" width="800" height="460">
  <rect width="800" height="460" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Контрольний чек-лист готовності наукової роботи</text>

  <!-- Заголовок чек-листа -->
  <rect x="130" y="50" width="540" height="40" rx="8" fill="#1e3a5f"/>
  <text x="400" y="77" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">Перевірте перед поданням</text>

  <!-- Пункти -->
  <rect x="130" y="100" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="121" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="121" font-family="Arial" font-size="11.5" fill="#334155">Титульна сторінка оформлена за зразком кафедри</text>

  <rect x="130" y="140" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="161" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="161" font-family="Arial" font-size="11.5" fill="#334155">Зміст відповідає структурі та номерам сторінок</text>

  <rect x="130" y="180" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="201" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="201" font-family="Arial" font-size="11.5" fill="#334155">Шрифт Times New Roman, 14 pt, інтервал 1,5</text>

  <rect x="130" y="220" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="241" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="241" font-family="Arial" font-size="11.5" fill="#334155">Поля: ліве 3 см, праве 1,5 см, верхнє і нижнє 2 см</text>

  <rect x="130" y="260" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="281" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="281" font-family="Arial" font-size="11.5" fill="#334155">Кожен розділ має висновки</text>

  <rect x="130" y="300" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="321" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="321" font-family="Arial" font-size="11.5" fill="#334155">Усі таблиці та рисунки пронумеровані й підписані</text>

  <rect x="130" y="340" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="361" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="361" font-family="Arial" font-size="11.5" fill="#334155">Список джерел — за ДСТУ 8302:2015, в алфавітному порядку</text>

  <rect x="130" y="380" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="401" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="401" font-family="Arial" font-size="11.5" fill="#334155">Усі покликання в тексті відповідають номерам у списку</text>

  <rect x="130" y="420" width="540" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="150" y="441" font-family="Arial" font-size="11.5" fill="#1e3a5f">☐</text>
  <text x="175" y="441" font-family="Arial" font-size="11.5" fill="#334155">Унікальність тексту ≥ 70 % (перевірено антиплагіатом)</text>
</svg>
'''


# ============================================================
# 4. ЗМІСТ ДОКУМЕНТА
# ============================================================

def build_document():
    doc = setup_document()

    # ---------- Титульна частина ----------
    add_title(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 9", size=16, space_after=4)
    add_title(doc,
              "Оформлення наукової роботи. Структура наукової статті, "
              "дипломної роботи, звіту про дослідження",
              size=15, space_after=10)
    add_title(doc, "Дисципліна: Основи науково-педагогічних досліджень",
              size=13, bold=False, space_after=2)
    add_title(doc, "Спеціальність: Початкова освіта", size=13, bold=False, space_after=12)

    # ---------- Мета ----------
    add_heading(doc, "Мета та завдання")
    add_paragraph(doc,
        "Мета: ознайомити з вимогами до оформлення наукової роботи, структурою "
        "наукової статті, дипломної роботи та звіту про дослідження; розвивати "
        "вміння структурувати й оформлювати наукові тексти; виховувати "
        "відповідальність за якість і відповідність оформлення наукової роботи.")
    add_paragraph(doc,
        "Завдання: опанувати загальні технічні вимоги до наукового тексту; "
        "вивчити структуру наукової статті, дипломної роботи та звіту; навчитися "
        "оформлювати ілюстрації, таблиці, додатки; перевіряти готовність роботи "
        "за чек-листом.")
    add_paragraph(doc, "Обладнання: інструкційні картки, комп'ютер, проєктор.")

    # ---------- Література ----------
    add_heading(doc, "Література")
    add_numbered(doc, "Лузан П. Г., Сопівник І. В., Виговська С. В. Основи "
                      "науково-педагогічних досліджень. Київ, 2010. 219 с.")
    add_numbered(doc, "Лаппо В. В. Основи педагогічних досліджень. "
                      "Івано-Франківськ: НАІР, 2016. 284 с.")

    # ---------- 1. Загальні вимоги ----------
    add_heading(doc, "1. Загальні вимоги до оформлення наукової роботи")
    add_paragraph(doc,
        "Наукова робота має бути оформлена відповідно до єдиних технічних вимог, "
        "що забезпечують читабельність, уніфікованість і зручність сприйняття тексту. "
        "Порушення цих вимог є підставою для повернення роботи на доопрацювання.")
    add_svg_image(doc, SVG_FORMATTING_REQUIREMENTS, width_cm=15,
                  caption="Рис. 1. Схема технічних вимог до сторінки наукової роботи")

    add_heading(doc, "1.1. Основні параметри оформлення", level=2)
    add_table(doc,
        headers=["Параметр", "Значення"],
        rows=[
            ["Шрифт", "Times New Roman, 14 pt (для таблиць допускається 12 pt)"],
            ["Міжрядковий інтервал", "1,5 (у таблицях — 1,0)"],
            ["Поля", "ліве — 3 см, праве — 1,5 см, верхнє — 2 см, нижнє — 2 см"],
            ["Абзацний відступ", "1,25 см (однаковий по всьому тексту)"],
            ["Вирівнювання", "по ширині сторінки"],
            ["Нумерація сторінок", "арабськими цифрами у правому нижньому куті; "
                                   "на титульній — не проставляється"],
            ["Заголовки", "жирним шрифтом, з абзацу або по центру; "
                          "між заголовком і текстом — 1 порожній рядок"],
            ["Нумерація розділів", "1, 1.1, 1.1.1 — наскрізна, арабськими цифрами"],
        ],
        col_widths=[5.0, 12.0])
    add_paragraph(doc, "Таблиця 1. Основні параметри оформлення наукової роботи",
                  italic=True, indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 2. Стаття ----------
    add_heading(doc, "2. Структура наукової статті")
    add_paragraph(doc,
        "Наукова стаття — це завершений авторський твір, що містить виклад "
        "конкретних результатів дослідження. Вона має обов'язкову структуру, "
        "зумовлену вимогами фахових видань і ДАК України.")
    add_svg_image(doc, SVG_ARTICLE_STRUCTURE, width_cm=15,
                  caption="Рис. 2. Структура наукової статті (8 обов'язкових елементів)")

    add_paragraph(doc,
        "Ключові вимоги до статті: обґрунтована актуальність, чіткий науковий "
        "апарат (мета, завдання, об'єкт, предмет), опис власних результатів, "
        "коректне оформлення покликань, обсяг — від 8 до 12 сторінок.")

    # ---------- 3. Дипломна ----------
    add_heading(doc, "3. Структура дипломної (кваліфікаційної) роботи")
    add_paragraph(doc,
        "Дипломна робота — це кваліфікаційне дослідження, яке засвідчує "
        "відповідність рівня підготовки студента освітньому стандарту. Вона "
        "містить теоретичну та емпіричну частини, а також результати "
        "експериментальної перевірки висунутої гіпотези.")
    add_svg_image(doc, SVG_DIPLOMA_STRUCTURE, width_cm=16,
                  caption="Рис. 3. Структура дипломної роботи (структурні елементи)")

    add_heading(doc, "3.1. Особливості кожного розділу", level=2)
    add_table(doc,
        headers=["Розділ", "Основне призначення", "Орієнтовний обсяг"],
        rows=[
            ["Вступ", "Актуальність, мета, завдання, об'єкт, предмет, "
                     "методи, гіпотеза", "3–5 сторінок"],
            ["Розділ 1", "Теоретичне обґрунтування (аналіз джерел, понятійний "
                        "апарат, модель)", "20–25 сторінок"],
            ["Розділ 2", "Методика дослідження (критерії, рівні, інструментарій)",
             "12–15 сторінок"],
            ["Розділ 3", "Емпірична частина: результати, порівняння, "
                        "інтерпретація", "15–20 сторінок"],
            ["Загальні висновки", "Співвіднесення з метою та гіпотезою",
             "2–3 сторінки"],
            ["Додатки", "Анкети, протоколи, таблиці (допоміжні матеріали)",
             "не обмежено"],
        ],
        col_widths=[3.5, 10.0, 4.5])
    add_paragraph(doc, "Таблиця 2. Призначення та обсяг структурних частин дипломної роботи",
                  italic=True, indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 4. Звіт ----------
    add_heading(doc, "4. Структура звіту про дослідження")
    add_paragraph(doc,
        "Звіт про дослідження — це документ, який містить повний опис ходу та "
        "результатів дослідження (або його окремого етапу). Він може мати "
        "самостійне значення (як форма підсумкової роботи) або бути складовою "
        "курсової чи дипломної роботи.")
    add_svg_image(doc, SVG_REPORT_STRUCTURE, width_cm=14,
                  caption="Рис. 4. Структура звіту про дослідження")

    # ---------- 5. Порівняння ----------
    add_heading(doc, "5. Порівняльна характеристика видів наукових робіт")
    add_paragraph(doc,
        "Наукова стаття, дипломна робота та звіт мають різний обсяг і призначення, "
        "але спільні вимоги до наукового стилю, структури та оформлення.")
    add_svg_image(doc, SVG_COMPARISON, width_cm=16,
                  caption="Рис. 5. Порівняння обсягу та призначення видів наукових робіт")

    # ---------- 6. Помилки ----------
    add_heading(doc, "6. Типові помилки оформлення")
    add_svg_image(doc, SVG_ERRORS, width_cm=16,
                  caption="Рис. 6. Типові помилки оформлення наукової роботи")

    add_heading(doc, "6.1. Як уникнути помилок", level=2)
    add_bullet(doc, "заздалегідь уточніть технічні вимоги на кафедрі / у викладача;")
    add_bullet(doc, "використовуйте шаблон із налаштованими стилями (Word);")
    add_bullet(doc, "перевіряйте відповідність покликань і джерел перед кожним поданням;")
    add_bullet(doc, "ставте назви й номери до ВСІХ таблиць та ілюстрацій;")
    add_bullet(doc, "використовуйте антиплагіатні сервіси для перевірки унікальності.")

    # ---------- 7. Чек-лист ----------
    add_heading(doc, "7. Контрольний чек-лист готовності роботи")
    add_paragraph(doc,
        "Перед поданням роботи пройдіться чек-листом — це допоможе уникнути "
        "технічних зауважень і зосередити увагу викладача на змісті.")
    add_svg_image(doc, SVG_CHECKLIST, width_cm=15,
                  caption="Рис. 7. Контрольний чек-лист готовності наукової роботи")

    # ---------- 8. Завдання ----------
    add_heading(doc, "8. Завдання для практичного виконання")

    add_paragraph(doc, "Завдання 1. Налаштування документа", bold=True,
                  indent=False, space_after=2)
    add_paragraph(doc,
        "У Word створіть новий документ і налаштуйте: Times New Roman 14 pt, "
        "інтервал 1,5, поля 3-2-2-1,5 см, вирівнювання по ширині, абзацний "
        "відступ 1,25 см. Збережіть як шаблон для власних робіт.")

    add_paragraph(doc, "Завдання 2. Структура статті", bold=True,
                  indent=False, space_after=2)
    add_paragraph(doc,
        "Складіть структуру власної наукової статті за темою дослідження "
        "(8 обов'язкових елементів з Рис. 2). Для кожного елемента вкажіть "
        "орієнтовний обсяг і зміст.")

    add_paragraph(doc, "Завдання 3. Оформлення ілюстрацій", bold=True,
                  indent=False, space_after=2)
    add_paragraph(doc,
        "Оформіть 2 таблиці та 2 рисунки для власної роботи: пронумеруйте, "
        "підпишіть, додайте посилання в тексті. Перевірте, що таблиця не "
        "розривається між сторінками.")

    add_paragraph(doc, "Завдання 4. Структура дипломної", bold=True,
                  indent=False, space_after=2)
    add_paragraph(doc,
        "Складіть детальний план (зміст) власної дипломної роботи за темою "
        "дослідження відповідно до Рис. 3. Вкажіть орієнтовні обсяги розділів.")

    add_paragraph(doc, "Завдання 5. Самооцінка за чек-листом", bold=True,
                  indent=False, space_after=2)
    add_paragraph(doc,
        "Перевірте власну роботу (або її фрагмент) за чек-листом (Рис. 7). "
        "Зафіксуйте, які пункти виконано, а які потребують доопрацювання. "
        "Складіть план виправлень.")

    add_heading(doc, "Вимоги до звіту", level=2)
    add_bullet(doc, "оформлений документ Word (або PDF);")
    add_bullet(doc, "структура статті + план дипломної роботи;")
    add_bullet(doc, "2 таблиці та 2 рисунки, оформлені за вимогами;")
    add_bullet(doc, "заповнений чек-лист із зазначенням пунктів доопрацювання;")
    add_bullet(doc, "шрифт Times New Roman, 14 pt, інтервал 1,5;")
    add_bullet(doc, "назва файлу: Прізвище_Ім'я_ПЗ9_Оформлення.")

    # ---------- 9. Критерії ----------
    add_heading(doc, "9. Критерії оцінювання")
    add_table(doc,
        headers=["Критерій", "Показники", "Бали"],
        rows=[
            ["Технічне оформлення", "Шрифт, інтервал, поля, нумерація, вирівнювання", "3"],
            ["Структура", "Повнота структури статті та плану дипломної", "3"],
            ["Ілюстрації", "Нумерація, підписи, посилання в тексті", "2"],
            ["Самооцінка", "Повнота заповнення чек-листа, обґрунтованість виправлень", "2"],
        ],
        col_widths=[3.5, 10.0, 2.0])
    add_paragraph(doc, "Таблиця 3. Критерії оцінювання (максимум — 10 балів)",
                  italic=True, indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 10. Контрольні запитання ----------
    add_heading(doc, "10. Контрольні запитання")
    add_numbered(doc, "Які загальні технічні вимоги висувають до оформлення наукової роботи?")
    add_numbered(doc, "Які поля повинна мати сторінка наукової роботи?")
    add_numbered(doc, "Як оформлюють нумерацію сторінок у науковій роботі?")
    add_numbered(doc, "Назвіть обов'язкові елементи структури наукової статті.")
    add_numbered(doc, "Які особливості має структура дипломної (кваліфікаційної) роботи?")
    add_numbered(doc, "Скільки сторінок орієнтовно займає дипломна робота?")
    add_numbered(doc, "Яка структура звіту про дослідження?")
    add_numbered(doc, "Чим відрізняються наукова стаття, дипломна робота та звіт за обсягом і призначенням?")
    add_numbered(doc, "Назвіть типові помилки оформлення наукової роботи.")
    add_numbered(doc, "Які елементи входять до чек-листа готовності роботи?")
    add_numbered(doc, "Як правильно оформити таблицю та рисунок у науковій роботі?")
    add_numbered(doc, "Чому нумерація покликань має відповідати номерам у списку джерел?")

    # ---------- Файл ----------
    output = "PZ9_Oformlennia_naukovoi_roboty.docx"
    doc.save(output)
    print(f"✅ Документ створено: {output}")


if __name__ == "__main__":
    build_document()