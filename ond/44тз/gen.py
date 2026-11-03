# -*- coding: utf-8 -*-
"""
Генерація DOCX для тематичного заліку № 3
Розділ: Методичні засади організації та проведення науково-педагогічного дослідження
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


def add_question(doc, number, text, options):
    """Запитання з варіантами відповідей."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(f"{number}. ")
    r1.bold = True
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(14)
    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)

    letters = ['А', 'Б', 'В', 'Г']
    for i, opt in enumerate(options):
        op = doc.add_paragraph()
        op.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        op.paragraph_format.first_line_indent = Cm(0)
        op.paragraph_format.left_indent = Cm(1.0)
        op.paragraph_format.space_after = Pt(2)
        ro = op.add_run(f"{letters[i]}) {opt}")
        ro.font.name = 'Times New Roman'
        ro.font.size = Pt(14)


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


def add_page_break(doc):
    doc.add_page_break()


# ============================================================
# 3. SVG-ДІАГРАМИ
# ============================================================

SVG_STRUCTURE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 340" width="820" height="340">
  <rect width="820" height="340" fill="#ffffff"/>
  <text x="410" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура розділу «Методичні засади науково-педагогічного дослідження»</text>

  <rect x="280" y="48" width="260" height="44" rx="10" fill="#1e3a5f"/>
  <text x="410" y="75" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">НАУКОВО-ПЕДАГОГІЧНЕ ДОСЛІДЖЕННЯ</text>

  <line x1="410" y1="92" x2="410" y2="112" stroke="#2980b9" stroke-width="2"/>
  <line x1="85" y1="112" x2="735" y2="112" stroke="#2980b9" stroke-width="2"/>
  <line x1="85" y1="112" x2="85" y2="132" stroke="#2980b9" stroke-width="2"/>
  <line x1="245" y1="112" x2="245" y2="132" stroke="#2980b9" stroke-width="2"/>
  <line x1="410" y1="112" x2="410" y2="132" stroke="#2980b9" stroke-width="2"/>
  <line x1="575" y1="112" x2="575" y2="132" stroke="#2980b9" stroke-width="2"/>
  <line x1="735" y1="112" x2="735" y2="132" stroke="#2980b9" stroke-width="2"/>

  <rect x="15" y="132" width="140" height="90" rx="9" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="85" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">Проблема,</text>
  <text x="85" y="174" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">тема, мета,</text>
  <text x="85" y="190" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">завдання</text>
  <text x="85" y="210" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#2980b9">об'єкт, предмет</text>

  <rect x="175" y="132" width="140" height="90" rx="9" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="245" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e5a3f">Методи</text>
  <text x="245" y="174" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e5a3f">дослідження</text>
  <text x="245" y="194" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60">теоретичні, емпіричні,</text>
  <text x="245" y="210" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60">математико-статистичні</text>

  <rect x="340" y="132" width="140" height="90" rx="9" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="410" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">Методика</text>
  <text x="410" y="174" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">констатувального</text>
  <text x="410" y="190" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">етапу</text>
  <text x="410" y="210" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#e67e22">критерії, показники, рівні</text>

  <rect x="505" y="132" width="140" height="90" rx="9" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="575" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">Методика</text>
  <text x="575" y="174" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">формувального</text>
  <text x="575" y="190" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">етапу</text>
  <text x="575" y="210" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#8e44ad">реалізація в освітньому</text>
  <text x="575" y="222" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#8e44ad">процесі</text>

  <rect x="665" y="132" width="140" height="90" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="735" y="158" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">Обробка</text>
  <text x="735" y="174" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">результатів</text>
  <text x="735" y="190" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">та висновки</text>
  <text x="735" y="210" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#c0392b">таблиці, діаграми</text>

  <text x="410" y="258" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic" fill="#475569">Наскрізні лінії: академічна доброчесність, цитування, етика дослідження</text>
  <text x="410" y="290" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Залікові теми: 1–7 (див. структуру курсу)</text>
</svg>
'''

SVG_LEVELS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 320" width="720" height="320">
  <rect width="720" height="320" fill="#ffffff"/>
  <text x="360" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Розподіл балів за рівнями завдань</text>

  <rect x="60" y="60" width="200" height="120" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="160" y="90" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Рівень І</text>
  <text x="160" y="112" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#2980b9">тестові завдання</text>
  <text x="160" y="136" text-anchor="middle" font-family="Arial" font-size="26" font-weight="bold" fill="#2980b9">20 балів</text>
  <text x="160" y="160" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#64748b">14 + 1 завдання</text>

  <rect x="280" y="60" width="180" height="120" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5 4"/>
  <text x="370" y="90" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#475569">Рівень ІІ</text>
  <text x="370" y="112" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#64748b">відкриті завдання</text>
  <text x="370" y="136" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold" fill="#64748b">додатково</text>
  <text x="370" y="160" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#94a3b8">за бажанням</text>

  <rect x="480" y="60" width="180" height="120" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5 4"/>
  <text x="570" y="90" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#475569">Рівень ІІІ</text>
  <text x="570" y="112" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#64748b">творче завдання</text>
  <text x="570" y="136" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold" fill="#64748b">додатково</text>
  <text x="570" y="160" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#94a3b8">для високого балу</text>

  <text x="360" y="225" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">Максимум за обов'язкову частину — 20 балів</text>
  <text x="360" y="252" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Запитання 1–14 — по 1 балу, запитання 15 — 6 балів</text>
  <text x="360" y="278" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Оцінювання: 18–20 — «відмінно», 14–17 — «добре», 10–13 — «задовільно»</text>
</svg>
'''

SVG_TOPICS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 380" width="760" height="380">
  <rect width="760" height="380" fill="#ffffff"/>
  <text x="380" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Теми, охоплені тематичним заліком</text>

  <circle cx="380" cy="210" r="70" fill="#1e3a5f"/>
  <text x="380" y="205" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">ЗАЛІК</text>
  <text x="380" y="224" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">№ 3</text>

  <line x1="380" y1="140" x2="380" y2="80" stroke="#2980b9" stroke-width="2"/>
  <rect x="280" y="42" width="200" height="38" rx="8" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="380" y="66" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">1. Проблема, тема, мета</text>

  <line x1="445" y1="160" x2="530" y2="110" stroke="#27ae60" stroke-width="2"/>
  <rect x="532" y="90" width="210" height="38" rx="8" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="637" y="114" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e5a3f">2. Методи дослідження</text>

  <line x1="450" y1="210" x2="530" y2="210" stroke="#e67e22" stroke-width="2"/>
  <rect x="532" y="190" width="210" height="38" rx="8" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="637" y="214" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">3. Констатувальний етап</text>

  <line x1="445" y1="260" x2="530" y2="310" stroke="#8e44ad" stroke-width="2"/>
  <rect x="532" y="292" width="210" height="38" rx="8" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="637" y="316" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">4. Аналіз літератури, гіпотеза</text>

  <line x1="380" y1="280" x2="380" y2="340" stroke="#c0392b" stroke-width="2"/>
  <rect x="280" y="302" width="200" height="38" rx="8" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="380" y="326" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">5. Формувальний етап</text>

  <line x1="315" y1="260" x2="230" y2="310" stroke="#16a085" stroke-width="2"/>
  <rect x="20" y="292" width="210" height="38" rx="8" fill="#e8f8f5" stroke="#16a085" stroke-width="1.5"/>
  <text x="125" y="316" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#0e6655">6. Академічна доброчесність</text>

  <line x1="310" y1="210" x2="230" y2="210" stroke="#d35400" stroke-width="2"/>
  <rect x="20" y="190" width="210" height="38" rx="8" fill="#fdf2e9" stroke="#d35400" stroke-width="1.5"/>
  <text x="125" y="214" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#a04000">7. Обробка результатів</text>

  <line x1="315" y1="160" x2="230" y2="110" stroke="#2e86c1" stroke-width="2"/>
  <rect x="20" y="90" width="210" height="38" rx="8" fill="#ebf5fb" stroke="#2e86c1" stroke-width="1.5"/>
  <text x="125" y="114" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1a5276">Цитування та джерела</text>
</svg>
'''

SVG_SCORE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="700" height="320">
  <rect width="700" height="320" fill="#ffffff"/>
  <text x="350" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Шкала переведення балів в оцінку</text>

  <line x1="80" y1="180" x2="620" y2="180" stroke="#cbd5e1" stroke-width="3"/>

  <rect x="80" y="130" width="135" height="50" rx="6" fill="#c0392b"/>
  <text x="147" y="155" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">1–9 балів</text>
  <text x="147" y="172" text-anchor="middle" font-family="Arial" font-size="10" fill="#fdedec">незадовільно</text>

  <rect x="220" y="130" width="135" height="50" rx="6" fill="#e67e22"/>
  <text x="287" y="155" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">10–13 балів</text>
  <text x="287" y="172" text-anchor="middle" font-family="Arial" font-size="10" fill="#fef9e7">задовільно</text>

  <rect x="360" y="130" width="135" height="50" rx="6" fill="#27ae60"/>
  <text x="427" y="155" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">14–17 балів</text>
  <text x="427" y="172" text-anchor="middle" font-family="Arial" font-size="10" fill="#eafaf1">добре</text>

  <rect x="500" y="130" width="135" height="50" rx="6" fill="#1e3a5f"/>
  <text x="567" y="155" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#ffffff">18–20 балів</text>
  <text x="567" y="172" text-anchor="middle" font-family="Arial" font-size="10" fill="#cfe7f7">відмінно</text>

  <text x="350" y="230" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Максимальна кількість балів за обов'язкову частину — 20</text>
  <text x="350" y="255" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Додаткові бали за рівні ІІ та ІІІ можуть зараховуватися за рішенням викладача</text>
  <text x="350" y="290" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">Час виконання: 45 хвилин</text>
</svg>
'''


# ============================================================
# 4. ЗМІСТ ДОКУМЕНТА
# ============================================================

def build_document():
    doc = setup_document()

    # ---------- Титульна частина ----------
    add_title(doc, "ТЕМАТИЧНИЙ ЗАЛІК № 3", size=16, space_after=4)
    add_title(doc, "Контрольна робота", size=15, space_after=2)
    add_title(doc,
              "Розділ: Методичні засади організації та проведення "
              "науково-педагогічного дослідження",
              size=14, space_after=10)
    add_title(doc, "Дисципліна: Основи науково-педагогічних досліджень",
              size=13, bold=False, space_after=2)
    add_title(doc, "Спеціальність: Початкова освіта", size=13, bold=False, space_after=12)

    # ---------- Мета ----------
    add_heading(doc, "Мета та завдання")
    add_paragraph(doc,
        "Мета: систематизувати й узагальнити знання з розділу «Методичні засади "
        "організації та проведення науково-педагогічного дослідження»; розвивати "
        "здатність до самооцінювання та самоконтролю; виховувати відповідальне "
        "ставлення до навчальних досягнень.")
    add_paragraph(doc,
        "Завдання: перевірити рівень засвоєння теоретичних знань; оцінити вміння "
        "застосовувати знання в практичних ситуаціях; виявити прогалини для подальшої "
        "підготовки до курсової роботи.")
    add_paragraph(doc, "Обладнання: інструкційні картки, бланк відповідей.")
    add_paragraph(doc, "Час виконання: 45 хвилин.")

    # ---------- Література ----------
    add_heading(doc, "Література для підготовки")
    add_paragraph(doc,
        "1. Лаппо В. В. Основи педагогічних досліджень. Івано-Франківськ: НАІР, 2016. 284 с.",
        indent=False, space_after=2)
    add_paragraph(doc,
        "2. Методичні рекомендації щодо написання та оформлення курсової роботи. "
        "Путивль: КЗСОР «Путивльський педагогічний фаховий коледж імені С. В. Руднєва», 2024. 14 с.",
        indent=False, space_after=6)

    # ---------- Структура ----------
    add_heading(doc, "Структура заліку")
    add_svg_image(doc, SVG_LEVELS, width_cm=15,
                  caption="Рис. 1. Розподіл балів за рівнями завдань")
    add_svg_image(doc, SVG_TOPICS, width_cm=15,
                  caption="Рис. 2. Теми, охоплені тематичним заліком")
    add_svg_image(doc, SVG_STRUCTURE, width_cm=16,
                  caption="Рис. 3. Структура розділу «Методичні засади науково-педагогічного дослідження»")
    add_svg_image(doc, SVG_SCORE, width_cm=15,
                  caption="Рис. 4. Шкала переведення балів в оцінку")

    # ---------- Інструкція ----------
    add_heading(doc, "Інструкція до виконання")
    add_paragraph(doc,
        "Залік складається з 15 тестових завдань. Запитання 1–14 — з однією правильною "
        "відповіддю (по 1 балу). Запитання 15 — на встановлення відповідності (6 балів: "
        "по 1 балу за кожну правильну пару). Максимальна кількість балів — 20.")
    add_paragraph(doc,
        "Відповіді фіксуються в бланку. У завданнях 1–14 оберіть одну літеру. "
        "У завданні 15 запишіть послідовність цифр і літер (наприклад, 1-Б, 2-А …).")

    add_page_break(doc)

    # ============================================================
    # РІВЕНЬ І. ТЕСТОВІ ЗАВДАННЯ
    # ============================================================

    add_heading(doc, "Рівень І. Тестові завдання (20 балів)")

    # --- Запитання 1–14 ---
    add_question(doc, 1,
        "Що таке проблема дослідження?",
        ["Сукупність методів вивчення явища",
         "Суперечність між існуючим і бажаним станом явища",
         "Коротке формулювання напряму дослідження",
         "Кінцевий результат дослідження"])

    add_question(doc, 2,
        "Яка вимога НЕ висувається до теми дослідження?",
        ["Конкретність",
         "Актуальність",
         "Обов'язкова наявність експерименту",
         "Логічний зв'язок з проблемою"])

    add_question(doc, 3,
        "Що є об'єктом дослідження?",
        ["Конкретна частина об'єкта, яка вивчається",
         "Кінцевий результат, якого прагне дослідник",
         "Широкий клас явищ або процесів, що існують об'єктивно",
         "Сукупність конкретних кроків для досягнення мети"])

    add_question(doc, 4,
        "Яка група методів забезпечує безпосередній контакт дослідника з педагогічною реальністю?",
        ["Теоретичні", "Емпіричні", "Математико-статистичні", "Прогностичні"])

    add_question(doc, 5,
        "Який метод передбачає активне втручання дослідника в педагогічний процес?",
        ["Спостереження", "Бесіда", "Педагогічний експеримент", "Аналіз документації"])

    add_question(doc, 6,
        "Що таке констатувальний етап експерименту?",
        ["Впровадження авторської методики",
         "Встановлення вихідного рівня сформованості явища",
         "Порівняння результатів контрольної та експериментальної груп",
         "Формулювання робочої гіпотези"])

    add_question(doc, 7,
        "Який компонент методики констатувального експерименту визначає конкретні вимірювані прояви критерію?",
        ["Мета", "Показник", "Вибірка", "Гіпотеза"])

    add_question(doc, 8,
        "Що таке робоча гіпотеза дослідження?",
        ["Остаточний висновок дослідження",
         "Науково обґрунтоване припущення, що потребує перевірки",
         "Перелік методів дослідження",
         "Опис вибірки учасників"])

    add_question(doc, 9,
        "Яка вимога до робочої гіпотези є обов'язковою?",
        ["Наявність статистичних даних",
         "Перевірюваність емпіричним шляхом",
         "Обов'язкове використання експерименту",
         "Наявність не менше 10 джерел"])

    add_question(doc, 10,
        "Що таке формувальний етап експерименту?",
        ["Встановлення вихідного рівня явища",
         "Впровадження авторської методики та перевірка її ефективності",
         "Аналіз наукової літератури",
         "Оформлення результатів дослідження"])

    add_question(doc, 11,
        "Що таке плагіат?",
        ["Вигадування даних дослідження",
         "Привласнення чужих ідей або текстів без належного посилання",
         "Викривлення результатів дослідження",
         "Використання сторонніх джерел під час роботи"])

    add_question(doc, 12,
        "Як оформлюють пряме цитування в науковій роботі?",
        ["Без лапок, але з посиланням на джерело",
         "У лапках, обов'язково з посиланням на сторінку",
         "Без лапок і без посилання",
         "Лише з посиланням на автора без сторінки"])

    add_question(doc, 13,
        "Який тип діаграми доцільно використовувати для показу динаміки показника в часі?",
        ["Кругова", "Стовпчикова", "Лінійна", "Піктограма"])

    add_question(doc, 14,
        "Що таке первинна обробка результатів дослідження?",
        ["Формулювання гіпотези",
         "Впорядкування та перетворення «сирих» даних на показники для аналізу",
         "Проведення експерименту",
         "Написання висновків"])

    # --- Запитання 15: відповідність ---
    add_paragraph(doc, "", indent=False, space_after=2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run("15. ")
    r1.bold = True
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(14)
    r2 = p.add_run("Установіть відповідність між поняттям (1–6) та його визначенням (А–Ж). "
                   "Запишіть послідовність пар (наприклад, 1-Б, 2-А …).")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)

    add_table(doc,
        headers=["Поняття", "Визначення"],
        rows=[
            ["1. Проблема дослідження",
             "А. Конкретні кроки, які необхідно виконати для досягнення мети"],
            ["2. Мета дослідження",
             "Б. Суперечність між існуючим і бажаним станом явища"],
            ["3. Завдання дослідження",
             "В. Конкретна частина об'єкта, яка безпосередньо вивчається"],
            ["4. Об'єкт дослідження",
             "Г. Кінцевий результат, якого прагне досягти дослідник"],
            ["5. Предмет дослідження",
             "Д. Широкий клас явищ або процесів, що існують об'єктивно"],
            ["6. Робоча гіпотеза",
             "Е. Науково обґрунтоване припущення, що потребує перевірки"],
            ["", "Ж. Сукупність методів вивчення педагогічного явища"],
        ],
        col_widths=[5.0, 12.0])

    add_paragraph(doc, "Відповідь: _______________________________________________________",
                  indent=False, space_after=10)

    add_page_break(doc)

    # ============================================================
    # ДОДАТКОВІ ЗАВДАННЯ (РІВНІ ІІ ТА ІІІ)
    # ============================================================

    add_heading(doc, "Додаткові завдання (за бажанням)")

    add_heading(doc, "Рівень ІІ. Відкриті завдання", level=2)
    add_paragraph(doc,
        "16. Сформулюйте робочу гіпотезу для теми «Формування пізнавального інтересу "
        "молодших школярів засобами ігрових технологій». Використайте схему "
        "«якщо … то … оскільки …». (3 бали)", indent=False, space_after=6)
    add_paragraph(doc,
        "17. Наведіть по одному прикладу порушення академічної доброчесності та "
        "коректного використання джерела. Поясніть різницю. (3 бали)",
        indent=False, space_after=6)
    add_paragraph(doc,
        "18. За даними (високий — 8 учнів, середній — 18, низький — 14; усього 40) "
        "обчисліть відсотки та запропонуйте тип діаграми для унаочнення. Обґрунтуйте вибір. (4 бали)",
        indent=False, space_after=10)

    add_heading(doc, "Рівень ІІІ. Творче завдання", level=2)
    add_paragraph(doc,
        "19. Складіть план констатувального етапу експерименту для власної теми "
        "дослідження: мета, критерії, показники, рівні, методики. Обґрунтуйте вибір "
        "інструментарію. (5 балів)", indent=False, space_after=10)

    # ---------- Бланк відповідей ----------
    add_heading(doc, "Бланк відповідей")
    add_paragraph(doc, "ПІБ студента: ____________________________________________________",
                  indent=False, space_after=4)
    add_paragraph(doc, "Група: ______________    Дата: ______________",
                  indent=False, space_after=10)

    # Таблиця для відповідей 1–14
    headers = [str(i) for i in range(1, 15)]
    rows = [["" for _ in range(14)]]
    add_table(doc, headers, rows, font_size=11)

    add_paragraph(doc, "15. Відповідність: 1-___  2-___  3-___  4-___  5-___  6-___",
                  indent=False, space_after=10)
    add_paragraph(doc, "Кількість балів: ________ / 20",
                  indent=False, space_after=4)
    add_paragraph(doc, "Оцінка: ________",
                  indent=False, space_after=10)

    # ---------- Ключ відповідей (для викладача) ----------
    add_page_break(doc)
    add_heading(doc, "Ключ відповідей (для викладача)")

    add_paragraph(doc, "Запитання 1–14 (по 1 балу):", bold=True, indent=False, space_after=4)
    add_table(doc,
        headers=["№", "1", "2", "3", "4", "5", "6", "7"],
        rows=[["Відповідь", "Б", "В", "В", "Б", "В", "Б", "Б"]],
        font_size=11)
    add_table(doc,
        headers=["№", "8", "9", "10", "11", "12", "13", "14"],
        rows=[["Відповідь", "Б", "Б", "Б", "Б", "Б", "В", "Б"]],
        font_size=11)

    add_paragraph(doc, "Запитання 15 (6 балів, по 1 за пару):", bold=True,
                  indent=False, space_after=4)
    add_paragraph(doc,
        "1-Б, 2-Г, 3-А, 4-Д, 5-В, 6-Е",
        indent=False, space_after=10)

    add_paragraph(doc, "Шкала оцінювання обов'язкової частини:", bold=True,
                  indent=False, space_after=4)
    add_table(doc,
        headers=["Бали", "Оцінка"],
        rows=[
            ["18–20", "відмінно"],
            ["14–17", "добре"],
            ["10–13", "задовільно"],
            ["1–9", "незадовільно"],
        ],
        col_widths=[5.0, 5.0])

    # ---------- Файл ----------
    output = "Zalik3_Kontrolna_robota.docx"
    doc.save(output)
    print(f"✅ Документ створено: {output}")


if __name__ == "__main__":
    build_document()