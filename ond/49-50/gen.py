# -*- coding: utf-8 -*-
"""
Генерація DOCX для самостійної роботи № 6
Тема: Правила цитування, оформлення покликань та списку
      використаних джерел у педагогічних дослідженнях
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

SVG_CITATION_TYPES = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 400" width="820" height="400">
  <rect width="820" height="400" fill="#ffffff"/>
  <text x="410" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Види цитування в науково-педагогічному дослідженні</text>

  <rect x="15" y="55" width="190" height="130" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="110" y="82" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e3a5f">ПРЯМЕ</text>
  <text x="110" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">дослівне</text>
  <text x="110" y="118" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">відтворення</text>
  <text x="110" y="142" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#2980b9">у лапках «…»</text>
  <text x="110" y="160" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#2980b9">з посиланням [3, с. 45]</text>

  <rect x="215" y="55" width="190" height="130" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="2"/>
  <text x="310" y="82" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e5a3f">ПАРАФРАЗ</text>
  <text x="310" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">переказ думки</text>
  <text x="310" y="118" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">своїми словами</text>
  <text x="310" y="142" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#27ae60">без лапок</text>
  <text x="310" y="160" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#27ae60">з посиланням [3]</text>

  <rect x="415" y="55" width="190" height="130" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="2"/>
  <text x="510" y="82" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7e5109">УЗАГАЛЬНЕНЕ</text>
  <text x="510" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">виклад кількох</text>
  <text x="510" y="118" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">позицій</text>
  <text x="510" y="142" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#e67e22">одним реченням</text>
  <text x="510" y="160" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#e67e22">[1; 4; 7]</text>

  <rect x="615" y="55" width="190" height="130" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="2"/>
  <text x="710" y="82" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#4a235a">ЗА ПЕРШОДЖЕРЕЛОМ</text>
  <text x="710" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">посилання на думку</text>
  <text x="710" y="118" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">через інше джерело</text>
  <text x="710" y="142" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#8e44ad">«Цит. за: [5, с. 18]»</text>

  <rect x="60" y="215" width="700" height="90" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="410" y="240" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#334155">Головне правило:</text>
  <text x="410" y="263" text-anchor="middle" font-family="Arial" font-size="11" fill="#475569">будь-яке використання чужої думки — дослівне чи переказане —</text>
  <text x="410" y="283" text-anchor="middle" font-family="Arial" font-size="11" fill="#475569">обов'язково супроводжується посиланням на джерело</text>

  <text x="410" y="345" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#c0392b">Відсутність посилання = плагіат, навіть якщо текст переказано своїми словами</text>
  <text x="410" y="375" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Посилання — «місток» між текстом роботи та списком використаних джерел</text>
</svg>
'''

SVG_IN_TEXT_REFERENCES = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="800" height="360">
  <rect width="800" height="360" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Способи оформлення покликань у тексті</text>

  <rect x="15" y="55" width="380" height="130" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="205" y="80" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e3a5f">Квадратні дужки [номер]</text>
  <text x="35" y="105" font-family="Arial" font-size="10.5" fill="#2980b9">Посилання на джерело за номером у списку:</text>
  <text x="35" y="125" font-family="Arial" font-size="11" fill="#1e3a5f" font-style="italic">«… у працях [3] розглянуто …»</text>
  <text x="35" y="145" font-family="Arial" font-size="10.5" fill="#2980b9">З конкретною сторінкою:</text>
  <text x="35" y="163" font-family="Arial" font-size="11" fill="#1e3a5f" font-style="italic">«… [3, с. 45] …»</text>

  <rect x="405" y="55" width="380" height="130" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="595" y="80" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e5a3f">Декілька джерел</text>
  <text x="425" y="105" font-family="Arial" font-size="10.5" fill="#27ae60">У дужках через крапку з комою:</text>
  <text x="425" y="125" font-family="Arial" font-size="11" fill="#1e3a5f" font-style="italic">«… [1; 4; 7] …»</text>
  <text x="425" y="148" font-family="Arial" font-size="10.5" fill="#27ae60">Діапазон:</text>
  <text x="425" y="166" font-family="Arial" font-size="11" fill="#1e3a5f" font-style="italic">«… [2–5] …»</text>

  <rect x="15" y="200" width="380" height="130" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="205" y="225" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7e5109">Посилання в кінці речення</text>
  <text x="35" y="250" font-family="Arial" font-size="10.5" fill="#e67e22">Розміщується перед крапкою:</text>
  <text x="35" y="270" font-family="Arial" font-size="11" fill="#1e3a5f" font-style="italic">«… це підтверджують дослідження [3].»</text>
  <text x="35" y="295" font-family="Arial" font-size="10.5" fill="#e67e22">Правильно: … [3].</text>
  <text x="35" y="315" font-family="Arial" font-size="10.5" fill="#c0392b">Неправильно: … . [3]</text>

  <rect x="405" y="200" width="380" height="130" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="595" y="225" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#4a235a">Джерело без прямої цитати</text>
  <text x="425" y="250" font-family="Arial" font-size="10.5" fill="#8e44ad">Узагальнена думка кількох авторів:</text>
  <text x="425" y="270" font-family="Arial" font-size="11" fill="#1e3a5f" font-style="italic">«Науковці [1; 3; 5] одностайні …»</text>
  <text x="425" y="295" font-family="Arial" font-size="10.5" fill="#8e44ad">Посилання перед цитатою:</text>
  <text x="425" y="313" font-family="Arial" font-size="11" fill="#1e3a5f" font-style="italic">«За [4, с. 12], «… цитата …»»</text>
</svg>
'''

SVG_BIBLIO_STRUCTURE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="800" height="400">
  <rect width="800" height="400" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура бібліографічного опису (ДСТУ 8302:2015)</text>

  <rect x="40" y="55" width="720" height="60" rx="10" fill="#1e3a5f"/>
  <text x="400" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">Прізвище І. П. Назва праці : підзаголовок / І. П. Прізвище.</text>
  <text x="400" y="102" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#cfe7f7">Місто : Видавництво, Рік. Кількість сторінок.</text>

  <line x1="400" y1="118" x2="400" y2="140" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="140" x2="690" y2="140" stroke="#94a3b8" stroke-width="2"/>
  <line x1="110" y1="140" x2="110" y2="155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="255" y1="140" x2="255" y2="155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="400" y1="140" x2="400" y2="155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="545" y1="140" x2="545" y2="155" stroke="#94a3b8" stroke-width="2"/>
  <line x1="690" y1="140" x2="690" y2="155" stroke="#94a3b8" stroke-width="2"/>

  <rect x="40" y="155" width="140" height="90" rx="8" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="110" y="180" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">Автор</text>
  <text x="110" y="200" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#2980b9">Прізвище,</text>
  <text x="110" y="215" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#2980b9">ініціали</text>

  <rect x="185" y="155" width="140" height="90" rx="8" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="255" y="180" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e5a3f">Назва</text>
  <text x="255" y="200" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60">заголовок</text>
  <text x="255" y="215" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60">праці</text>

  <rect x="330" y="155" width="140" height="90" rx="8" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="400" y="180" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">Місто</text>
  <text x="400" y="200" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#e67e22">Київ,</text>
  <text x="400" y="215" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#e67e22">Львів …</text>

  <rect x="475" y="155" width="140" height="90" rx="8" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="545" y="180" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">Видавництво</text>
  <text x="545" y="200" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#8e44ad">назва</text>
  <text x="545" y="215" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#8e44ad">установи</text>

  <rect x="620" y="155" width="140" height="90" rx="8" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="690" y="180" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">Рік, сторінки</text>
  <text x="690" y="200" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#c0392b">2016.</text>
  <text x="690" y="215" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#c0392b">284 с.</text>

  <rect x="40" y="265" width="720" height="115" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="400" y="290" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">ПРИКЛАДИ</text>
  <text x="60" y="315" font-family="Arial" font-size="10.5" fill="#334155">Книга:</text>
  <text x="130" y="315" font-family="Arial" font-size="10.5" fill="#1e3a5f" font-style="italic">Кравець Н. П. Основи наукових досліджень : навч. посіб. Київ : Вид-во НПУ ім. М. П. Драгоманова, 2020. 74 с.</text>
  <text x="60" y="340" font-family="Arial" font-size="10.5" fill="#334155">Стаття:</text>
  <text x="130" y="340" font-family="Arial" font-size="10.5" fill="#1e3a5f" font-style="italic">Пріма Р. М. Сучасна наукова стаття: технологія творчості. Науковий вісник. 2020. № 4. С. 99–103.</text>
  <text x="60" y="365" font-family="Arial" font-size="10.5" fill="#334155">Електронне:</text>
  <text x="155" y="365" font-family="Arial" font-size="10.5" fill="#1e3a5f" font-style="italic">МОН України. URL: https://mon.gov.ua (дата звернення: 15.10.2026).</text>
</svg>
'''

SVG_BIBLIO_ORDER = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 360" width="760" height="360">
  <rect width="760" height="360" fill="#ffffff"/>
  <text x="380" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Правила впорядкування списку використаних джерел</text>

  <rect x="30" y="55" width="330" height="120" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="195" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#1e3a5f">АЛФАВІТНИЙ ПОРЯДОК</text>
  <text x="195" y="107" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">за прізвищем автора</text>
  <text x="195" y="125" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">або назвою праці</text>
  <text x="195" y="150" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#2980b9">найпоширеніший варіант</text>
  <text x="195" y="167" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#2980b9">для курсових і кваліфікаційних робіт</text>

  <rect x="400" y="55" width="330" height="120" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="2"/>
  <text x="565" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#1e5a3f">ПОРЯДОК ЗГАДУВАННЯ</text>
  <text x="565" y="107" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">у порядку появи</text>
  <text x="565" y="125" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">посилань у тексті</text>
  <text x="565" y="150" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#27ae60">використовують у статтях,</text>
  <text x="565" y="167" text-anchor="middle" font-family="Arial" font-size="10" font-style="italic" fill="#27ae60">дисертаціях</text>

  <rect x="30" y="195" width="330" height="130" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="2"/>
  <text x="195" y="222" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#7e5109">ОБОВ'ЯЗКОВІ ЕЛЕМЕНТИ</text>
  <text x="55" y="248" font-family="Arial" font-size="10.5" fill="#e67e22">✓ автор (прізвище, ініціали)</text>
  <text x="55" y="266" font-family="Arial" font-size="10.5" fill="#e67e22">✓ повна назва праці</text>
  <text x="55" y="284" font-family="Arial" font-size="10.5" fill="#e67e22">✓ місто, видавництво, рік</text>
  <text x="55" y="302" font-family="Arial" font-size="10.5" fill="#e67e22">✓ кількість сторінок (для книг)</text>

  <rect x="400" y="195" width="330" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="2"/>
  <text x="565" y="222" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#7b241c">ТИПОВІ ПОМИЛКИ</text>
  <text x="425" y="248" font-family="Arial" font-size="10.5" fill="#c0392b">✗ відсутність сторінок</text>
  <text x="425" y="266" font-family="Arial" font-size="10.5" fill="#c0392b">✗ неповне видавництво</text>
  <text x="425" y="284" font-family="Arial" font-size="10.5" fill="#c0392b">✗ джерела не в алфавіті</text>
  <text x="425" y="302" font-family="Arial" font-size="10.5" fill="#c0392b">✗ різні стилі опису</text>
</svg>
'''

SVG_MISTAKES = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 380" width="780" height="380">
  <rect width="780" height="380" fill="#ffffff"/>
  <text x="390" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Типові помилки в оформленні посилань і цитат</text>

  <rect x="20" y="55" width="360" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="40" y="80" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">1. Відсутність посилання</text>
  <text x="40" y="102" font-family="Arial" font-size="10.5" fill="#a93226">Переказ думки автора без посилання</text>
  <text x="40" y="120" font-family="Arial" font-size="10.5" fill="#a93226">= плагіат, навіть якщо переказано</text>
  <text x="40" y="137" font-family="Arial" font-size="10.5" fill="#a93226">своїми словами</text>
  <text x="40" y="163" font-family="Arial" font-size="10" font-style="italic" fill="#c0392b">Правильно: завжди ставити [номер]</text>
  <text x="40" y="178" font-family="Arial" font-size="10" font-style="italic" fill="#c0392b">навіть у парафразі</text>

  <rect x="400" y="55" width="360" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="420" y="80" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">2. Неправильна нумерація</text>
  <text x="420" y="102" font-family="Arial" font-size="10.5" fill="#a93226">Номер посилання не відповідає</text>
  <text x="420" y="120" font-family="Arial" font-size="10.5" fill="#a93226">номеру джерела у списку</text>
  <text x="420" y="137" font-family="Arial" font-size="10.5" fill="#a93226">використаних джерел</text>
  <text x="420" y="163" font-family="Arial" font-size="10" font-style="italic" fill="#c0392b">Правильно: перевіряти відповідність</text>
  <text x="420" y="178" font-family="Arial" font-size="10" font-style="italic" fill="#c0392b">номерів після кожного редагування</text>

  <rect x="20" y="200" width="360" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="40" y="225" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">3. Відсутність сторінки</text>
  <text x="40" y="247" font-family="Arial" font-size="10.5" fill="#a93226">Пряма цитата без зазначення</text>
  <text x="40" y="265" font-family="Arial" font-size="10.5" fill="#a93226">сторінки джерела</text>
  <text x="40" y="289" font-family="Arial" font-size="10" font-style="italic" fill="#c0392b">Неправильно: [3]</text>
  <text x="40" y="306" font-family="Arial" font-size="10" font-style="italic" fill="#27ae60">Правильно: [3, с. 45]</text>

  <rect x="400" y="200" width="360" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="420" y="225" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">4. Неохайне оформлення</text>
  <text x="420" y="247" font-family="Arial" font-size="10.5" fill="#a93226">Різні стилі опису джерел,</text>
  <text x="420" y="265" font-family="Arial" font-size="10.5" fill="#a93226">пропущені елементи,</text>
  <text x="420" y="283" font-family="Arial" font-size="10.5" fill="#a93226">непослідовне оформлення</text>
  <text x="420" y="308" font-family="Arial" font-size="10" font-style="italic" fill="#c0392b">Правильно: єдиний зразок за ДСТУ</text>
</svg>
'''

SVG_PRESENTATION_STRUCTURE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="800" height="400">
  <rect width="800" height="400" fill="#ffffff"/>
  <text x="400" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура презентації «Правила цитування та оформлення джерел»</text>

  <rect x="40" y="60" width="170" height="55" rx="8" fill="#1e3a5f"/>
  <text x="125" y="83" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">1. Титульний</text>
  <text x="125" y="101" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#cfe7f7">тема, автор</text>

  <rect x="230" y="60" width="170" height="55" rx="8" fill="#2471a3"/>
  <text x="315" y="83" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">2. Актуальність</text>
  <text x="315" y="101" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#ebf5fb">плагіат, доброчесність</text>

  <rect x="420" y="60" width="170" height="55" rx="8" fill="#2980b9"/>
  <text x="505" y="83" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">3. Види цитування</text>
  <text x="505" y="101" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#ebf5fb">пряме, парафраз</text>

  <rect x="610" y="60" width="170" height="55" rx="8" fill="#27ae60"/>
  <text x="695" y="83" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">4. Покликання</text>
  <text x="695" y="101" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#eafaf1">[3], [3; 5]</text>

  <rect x="40" y="140" width="170" height="55" rx="8" fill="#16a085"/>
  <text x="125" y="163" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">5. Список джерел</text>
  <text x="125" y="181" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#e8f8f5">за ДСТУ 8302:2015</text>

  <rect x="230" y="140" width="170" height="55" rx="8" fill="#e67e22"/>
  <text x="315" y="163" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">6. Приклад книги</text>
  <text x="315" y="181" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#fef9e7">опис, елементи</text>

  <rect x="420" y="140" width="170" height="55" rx="8" fill="#d35400"/>
  <text x="505" y="163" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">7. Приклад статті</text>
  <text x="505" y="181" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#fdf2e9">журнал, сторінки</text>

  <rect x="610" y="140" width="170" height="55" rx="8" fill="#8e44ad"/>
  <text x="695" y="163" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">8. Електронні</text>
  <text x="695" y="181" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#f4ecf7">URL, дата звернення</text>

  <rect x="120" y="220" width="240" height="55" rx="8" fill="#6c3483"/>
  <text x="240" y="243" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">9. Типові помилки</text>
  <text x="240" y="261" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#e8daef">4 основні групи</text>

  <rect x="380" y="220" width="220" height="55" rx="8" fill="#c0392b"/>
  <text x="490" y="243" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">10. Висновки</text>
  <text x="490" y="261" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#fdedec">головні тези</text>

  <rect x="620" y="220" width="160" height="55" rx="8" fill="#1e3a5f"/>
  <text x="700" y="243" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#ffffff">11. Дякую</text>
  <text x="700" y="261" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#cfe7f7">запитання</text>

  <text x="400" y="315" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Обов'язкові елементи: теоретичний мінімум + 2–3 приклади + 1 діаграма + висновок</text>
  <text x="400" y="340" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Орієнтовна тривалість виступу: 5–7 хвилин</text>
  <text x="400" y="368" text-anchor="middle" font-family="Arial" font-size="11" fill="#1e3a5f">Головний принцип: показувати, а не переказувати; наводити приклади з власного досвіду</text>
</svg>
'''


# ============================================================
# 4. ЗМІСТ ДОКУМЕНТА
# ============================================================

def build_document():
    doc = setup_document()

    # ---------- Титульна частина ----------
    add_title(doc, "САМОСТІЙНА РОБОТА № 6", size=16, space_after=4)
    add_title(doc,
              "Правила цитування, оформлення покликань та списку "
              "використаних джерел у педагогічних дослідженнях",
              size=15, space_after=10)
    add_title(doc, "Дисципліна: Основи науково-педагогічних досліджень",
              size=13, bold=False, space_after=2)
    add_title(doc, "Спеціальність: Початкова освіта", size=13, bold=False, space_after=12)

    # ---------- Мета ----------
    add_heading(doc, "Мета та завдання")
    add_paragraph(doc,
        "Мета: формувати знання про правила цитування, оформлення покликань і списку "
        "використаних джерел; розвивати вміння оформлювати науковий апарат дослідження; "
        "виховувати академічну доброчесність і точність в оформленні джерел.")
    add_paragraph(doc,
        "Завдання: опанувати види цитування та способи оформлення покликань; вивчити "
        "структуру бібліографічного опису за ДСТУ 8302:2015; навчитися укладати список "
        "використаних джерел; підготувати презентацію за темою.")
    add_paragraph(doc, "Обладнання: інструкційні картки, комп'ютер, PowerPoint / Canva.")

    # ---------- Література ----------
    add_heading(doc, "Література")
    add_numbered(doc, "Аносов І. П., Елькін М. В., Головкова М. М., Коробченко А. А. "
                      "Основи науково-педагогічних досліджень. Мелітополь: ТОВ "
                      "«Видавничий будинок ММД», 2015. 218 с.")
    add_numbered(doc, "Кравець Н. П. Основи наукових досліджень: навчальний посібник. "
                      "Київ: Вид-во НПУ імені М. П. Драгоманова, 2020. 74 с.")

    # ---------- 1. Види цитування ----------
    add_heading(doc, "1. Теоретична частина: цитування в науковій роботі")
    add_paragraph(doc,
        "Цитування — це включення в науковий текст фрагментів з інших джерел з "
        "обов'язковим посиланням на автора та видання. Коректне цитування є головним "
        "інструментом дотримання академічної доброчесності та уникнення плагіату.")
    add_svg_image(doc, SVG_CITATION_TYPES, width_cm=16,
                  caption="Рис. 1. Види цитування в науково-педагогічному дослідженні")

    # ---------- 2. Покликання ----------
    add_heading(doc, "2. Оформлення покликань у тексті")
    add_paragraph(doc,
        "Покликання — це вказівка на джерело, з якого взято думку, факт або цитату. "
        "Покликання розміщують у квадратних дужках безпосередньо після цитати або "
        "перед нею, залежно від способу оформлення.")
    add_svg_image(doc, SVG_IN_TEXT_REFERENCES, width_cm=15,
                  caption="Рис. 2. Способи оформлення покликань у тексті")

    add_heading(doc, "2.1. Правила розміщення покликань", level=2)
    add_bullet(doc, "покликання ставиться перед крапкою, а не після неї;")
    add_bullet(doc, "пряма цитата — у лапках + посилання з номером і сторінкою;")
    add_bullet(doc, "парафраз — без лапок, але з посиланням;")
    add_bullet(doc, "кілька джерел — через крапку з комою в одних дужках;")
    add_bullet(doc, "номер у покликанні має відповідати номеру джерела у списку.")

    # ---------- 3. Бібліографічний опис ----------
    add_heading(doc, "3. Бібліографічний опис за ДСТУ 8302:2015")
    add_paragraph(doc,
        "Бібліографічний опис — це впорядкована сукупність відомостей про джерело, "
        "що дає змогу його ідентифікувати. В Україні діє стандарт ДСТУ 8302:2015 "
        "«Інформація та документація. Бібліографічне посилання. Загальні положення "
        "та правила складання».")
    add_svg_image(doc, SVG_BIBLIO_STRUCTURE, width_cm=16,
                  caption="Рис. 3. Структура бібліографічного опису за ДСТУ 8302:2015")

    add_heading(doc, "3.1. Приклади оформлення різних типів джерел", level=2)
    add_table(doc,
        headers=["Тип джерела", "Приклад"],
        rows=[
            ["Книга (1–3 автори)",
             "Кравець Н. П. Основи наукових досліджень : навч. посіб. Київ : "
             "Вид-во НПУ ім. М. П. Драгоманова, 2020. 74 с."],
            ["Книга (4 і більше авторів)",
             "Основи науково-педагогічних досліджень / І. П. Аносов, М. В. Елькін, "
             "М. М. Головкова та ін. Мелітополь : ММД, 2015. 218 с."],
            ["Стаття в журналі",
             "Пріма Р. М. Сучасна наукова стаття: технологія творчості. Науковий "
             "вісник. 2020. № 4 (408). С. 99–103."],
            ["Стаття в збірнику",
             "Лаппо В. В. Етичні аспекти досліджень. Проблеми сучасної педагогіки : "
             "зб. наук. пр. Київ, 2016. Вип. 12. С. 45–52."],
            ["Дисертація",
             "Мартиненко С. М. Теоретико-методичні засади підготовки майбутніх "
             "учителів : дис. … д-ра пед. наук : 13.00.04. Київ, 2020. 420 с."],
            ["Електронний ресурс",
             "МОН України. Нова українська школа. URL: https://mon.gov.ua/ua/tag/"
             "nova-ukrayinska-shkola (дата звернення: 15.10.2026)."],
        ],
        col_widths=[4.5, 12.5])
    add_paragraph(doc, "Таблиця 1. Приклади бібліографічного опису різних типів джерел",
                  italic=True, indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 4. Список джерел ----------
    add_heading(doc, "4. Правила впорядкування списку використаних джерел")
    add_paragraph(doc,
        "Список використаних джерел — обов'язковий структурний елемент наукової роботи. "
        "Він засвідчує наукову обґрунтованість дослідження та коректність використання "
        "джерел.")
    add_svg_image(doc, SVG_BIBLIO_ORDER, width_cm=15,
                  caption="Рис. 4. Правила впорядкування списку використаних джерел")

    add_heading(doc, "4.1. Вимоги до списку джерел", level=2)
    add_bullet(doc, "усі джерела зі списку повинні мати хоча б одне покликання в тексті;")
    add_bullet(doc, "на кожне покликання в тексті має бути джерело у списку;")
    add_bullet(doc, "неприпустимо включати до списку праці, на які немає покликань;")
    add_bullet(doc, "бібліографічні описи мають бути оформлені за єдиним зразком (ДСТУ 8302:2015);")
    add_bullet(doc, "у курсових роботах — не менше 25–30 джерел, у кваліфікаційних — 50 і більше.")

    # ---------- 5. Помилки ----------
    add_heading(doc, "5. Типові помилки в оформленні посилань і цитат")
    add_svg_image(doc, SVG_MISTAKES, width_cm=16,
                  caption="Рис. 5. Типові помилки в оформленні посилань і цитат")
    add_paragraph(doc,
        "Уникати цих помилок допомагає уважне перечитування роботи, автоматична "
        "перевірка відповідності номерів покликань і джерел, а також використання "
        "єдиного зразка оформлення для всіх джерел.")

    # ---------- 6. Презентація ----------
    add_heading(doc, "6. Підготовка презентації")
    add_paragraph(doc,
        "Результат самостійної роботи — презентація (10–12 слайдів) за темою "
        "«Правила цитування та оформлення джерел». Презентація має містити "
        "теоретичний мінімум, 2–3 приклади з вашого досвіду (або навчальних робіт) "
        "та власні висновки.")
    add_svg_image(doc, SVG_PRESENTATION_STRUCTURE, width_cm=16,
                  caption="Рис. 6. Структура презентації «Правила цитування та оформлення джерел»")

    # ---------- 7. Завдання ----------
    add_heading(doc, "7. Завдання для самостійного виконання")

    add_paragraph(doc, "Завдання 1. Аналіз цитат", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Опрацюйте 3 наукові джерела за темою власного дослідження. Для кожного "
        "складіть 1 пряму цитату та 1 парафраз. Оформіть покликання коректно.")

    add_paragraph(doc, "Завдання 2. Список джерел", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Складіть список із 10 джерел за темою дослідження (не менше 3 різних типів: "
        "книга, стаття, електронний ресурс) відповідно до ДСТУ 8302:2015.")

    add_paragraph(doc, "Завдання 3. Аналіз помилок", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Наведіть 3 приклади неправильного оформлення покликань або цитат. Поясніть, "
        "у чому полягає помилка, і запропонуйте правильний варіант.")

    add_paragraph(doc, "Завдання 4. Презентація", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Створіть презентацію (10–12 слайдів) за темою «Правила цитування та "
        "оформлення джерел» у PowerPoint або Canva за структурою з Рис. 6.")

    add_paragraph(doc, "Завдання 5. Усний виступ", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Підготуйте усний виступ (5–7 хвилин), що супроводжує презентацію. "
        "Презентація і виступ подаються викладачу.")

    add_heading(doc, "Вимоги до звіту", level=2)
    add_bullet(doc, "файл презентації у форматі .pptx або .pdf;")
    add_bullet(doc, "текст виступу (1–1,5 сторінки, Times New Roman 14 pt, інтервал 1,25);")
    add_bullet(doc, "список із 10 джерел за ДСТУ 8302:2015;")
    add_bullet(doc, "приклади цитат і парафразів (завдання 1);")
    add_bullet(doc, "аналіз 3 помилок (завдання 3);")
    add_bullet(doc, "назва файлу: Прізвище_Ім'я_СР6_Цитування.")

    # ---------- 8. Критерії оцінювання ----------
    add_heading(doc, "8. Критерії оцінювання")
    add_table(doc,
        headers=["Критерій", "Показники", "Бали"],
        rows=[
            ["Змістовність", "Повнота розкриття теми, коректність прикладів", "4"],
            ["Оформлення джерел", "Дотримання ДСТУ 8302:2015 у списку та покликаннях", "3"],
            ["Презентація", "Структура (10–12 слайдів), візуалізація, єдність стилю", "2"],
            ["Усний виступ", "Вільне володіння матеріалом, дотримання часу", "1"],
        ],
        col_widths=[3.5, 10.0, 2.0])
    add_paragraph(doc, "Таблиця 2. Критерії оцінювання (максимум — 10 балів)",
                  italic=True, indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 9. Контрольні запитання ----------
    add_heading(doc, "9. Контрольні запитання")
    add_numbered(doc, "Що таке цитування і які його основні види?")
    add_numbered(doc, "Чим відрізняється пряме цитування від парафразу (переказу)?")
    add_numbered(doc, "Яких правил слід дотримуватися при оформленні прямого цитування?")
    add_numbered(doc, "Як оформлюють покликання на джерело в тексті наукової роботи?")
    add_numbered(doc, "Що таке бібліографічний опис і який стандарт його регулює в Україні?")
    add_numbered(doc, "Назвіть обов'язкові елементи бібліографічного опису книги.")
    add_numbered(doc, "Як оформлюють бібліографічний опис статті в журналі?")
    add_numbered(doc, "Як оформлюють опис електронного ресурсу?")
    add_numbered(doc, "У якому порядку впорядковують список використаних джерел?")
    add_numbered(doc, "Чому не можна включати до списку джерела, на які немає покликань у тексті?")
    add_numbered(doc, "Назвіть типові помилки в оформленні покликань і цитат.")
    add_numbered(doc, "Які вимоги висувають до презентації за темою цитування?")

    # ---------- Файл ----------
    output = "SR6_Tsytuvannia_dzherel.docx"
    doc.save(output)
    print(f"✅ Документ створено: {output}")


if __name__ == "__main__":
    build_document()