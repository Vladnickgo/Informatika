# -*- coding: utf-8 -*-
"""
Генерація DOCX для самостійної роботи № 5
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

    # Поля сторінки: 2 см з усіх боків
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    # Базовий стиль: Times New Roman, 14 pt, інтервал 1.25
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
    """Заголовок розділу: 14 pt, жирний, по ширині, з відступом зверху."""
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
    """Таблиця з шапкою (сірий фон, жирний шрифт)."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Шапка
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
        # Фон шапки
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), '1E3A5F')
        hdr[i]._tc.get_or_add_tcPr().append(shd)

    # Рядки
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
    """Конвертує SVG у PNG і вставляє в документ."""
    tmp_png = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    cairosvg.svg2png(bytestring=svg_string.encode('utf-8'),
                     write_to=tmp_png, output_width=1200)
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

SVG_PRINCIPLES = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" width="800" height="420">
  <rect width="800" height="420" fill="#ffffff"/>
  <text x="400" y="28" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Принципи академічної доброчесності</text>

  <rect x="250" y="50" width="300" height="48" rx="10" fill="#1e3a5f"/>
  <text x="400" y="80" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#ffffff">АКАДЕМІЧНА ДОБРОЧЕСНІСТЬ</text>

  <line x1="400" y1="98" x2="400" y2="118" stroke="#2980b9" stroke-width="2"/>
  <line x1="110" y1="118" x2="690" y2="118" stroke="#2980b9" stroke-width="2"/>
  <line x1="110" y1="118" x2="110" y2="140" stroke="#2980b9" stroke-width="2"/>
  <line x1="255" y1="118" x2="255" y2="140" stroke="#2980b9" stroke-width="2"/>
  <line x1="400" y1="118" x2="400" y2="140" stroke="#2980b9" stroke-width="2"/>
  <line x1="545" y1="118" x2="545" y2="140" stroke="#2980b9" stroke-width="2"/>
  <line x1="690" y1="118" x2="690" y2="140" stroke="#2980b9" stroke-width="2"/>

  <rect x="40" y="140" width="140" height="90" rx="9" fill="#3498db"/>
  <text x="110" y="172" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">Чесність</text>
  <text x="110" y="192" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#ebf5fb">правдиве подання</text>
  <text x="110" y="208" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#ebf5fb">результатів</text>

  <rect x="185" y="140" width="140" height="90" rx="9" fill="#2980b9"/>
  <text x="255" y="172" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">Довіра</text>
  <text x="255" y="192" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#ebf5fb">взаємна повага</text>
  <text x="255" y="208" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#ebf5fb">учасників</text>

  <rect x="330" y="140" width="140" height="90" rx="9" fill="#27ae60"/>
  <text x="400" y="172" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">Повага</text>
  <text x="400" y="192" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#eafaf1">до праці інших</text>
  <text x="400" y="208" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#eafaf1">авторів</text>

  <rect x="475" y="140" width="140" height="90" rx="9" fill="#e67e22"/>
  <text x="545" y="172" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">Відповідальність</text>
  <text x="545" y="192" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#fef9e7">за власні дії</text>
  <text x="545" y="208" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#fef9e7">та рішення</text>

  <rect x="620" y="140" width="140" height="90" rx="9" fill="#8e44ad"/>
  <text x="690" y="172" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">Справедливість</text>
  <text x="690" y="192" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#f4ecf7">рівні умови</text>
  <text x="690" y="208" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#f4ecf7">для всіх</text>

  <text x="400" y="270" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic" fill="#475569">Порушення будь-якого принципу = порушення академічної доброчесності</text>
</svg>
'''

SVG_VIOLATIONS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 380" width="720" height="380">
  <rect width="720" height="380" fill="#ffffff"/>
  <text x="360" y="28" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Основні порушення академічної доброчесності</text>

  <rect x="60" y="55" width="600" height="42" rx="8" fill="#c0392b"/>
  <text x="360" y="82" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#ffffff">ПОРУШЕННЯ</text>

  <line x1="360" y1="97" x2="360" y2="115" stroke="#94a3b8" stroke-width="2"/>
  <line x1="120" y1="115" x2="600" y2="115" stroke="#94a3b8" stroke-width="2"/>
  <line x1="120" y1="115" x2="120" y2="135" stroke="#94a3b8" stroke-width="2"/>
  <line x1="280" y1="115" x2="280" y2="135" stroke="#94a3b8" stroke-width="2"/>
  <line x1="440" y1="115" x2="440" y2="135" stroke="#94a3b8" stroke-width="2"/>
  <line x1="600" y1="115" x2="600" y2="135" stroke="#94a3b8" stroke-width="2"/>

  <rect x="40" y="135" width="160" height="85" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="120" y="163" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">Плагіат</text>
  <text x="120" y="182" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">привласнення</text>
  <text x="120" y="197" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">чужих ідей</text>

  <rect x="200" y="135" width="160" height="85" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="280" y="163" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">Фабрикація</text>
  <text x="280" y="182" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">вигадування</text>
  <text x="280" y="197" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">даних</text>

  <rect x="360" y="135" width="160" height="85" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="440" y="163" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">Фальсифікація</text>
  <text x="440" y="182" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">викривлення</text>
  <text x="440" y="197" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">результатів</text>

  <rect x="520" y="135" width="160" height="85" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="600" y="163" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">Списування</text>
  <text x="600" y="182" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">та обман</text>
  <text x="600" y="197" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">під час робіт</text>

  <rect x="150" y="255" width="420" height="85" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="360" y="280" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">Хабарництво та необ'єктивне оцінювання</text>
  <text x="360" y="302" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">отримання неправомірної вигоди</text>
  <text x="360" y="322" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#a93226">або упереджене ставлення до учасників</text>
</svg>
'''

SVG_CITATION = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 320" width="760" height="320">
  <rect width="760" height="320" fill="#ffffff"/>
  <text x="380" y="28" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Структура цитування наукового джерела</text>

  <rect x="40" y="55" width="220" height="80" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="150" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#1e3a5f">1. ВСТУП</text>
  <text x="150" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">автор, контекст,</text>
  <text x="150" y="118" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">проблема</text>

  <line x1="262" y1="95" x2="300" y2="95" stroke="#94a3b8" stroke-width="2"/>
  <polygon points="295,88 305,95 295,102" fill="#94a3b8"/>

  <rect x="302" y="55" width="220" height="80" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="2"/>
  <text x="412" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#1e5a3f">2. ЦИТАТА / ІДЕЯ</text>
  <text x="412" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">дослівна цитата або</text>
  <text x="412" y="118" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">переказ думки</text>

  <line x1="524" y1="95" x2="562" y2="95" stroke="#94a3b8" stroke-width="2"/>
  <polygon points="557,88 567,95 557,102" fill="#94a3b8"/>

  <rect x="564" y="55" width="180" height="80" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="2"/>
  <text x="654" y="82" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#4a235a">3. ПОСИЛАННЯ</text>
  <text x="654" y="102" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">[джерело, рік,</text>
  <text x="654" y="118" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">сторінка]</text>

  <rect x="40" y="175" width="380" height="115" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="230" y="200" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7e5109">Пряме цитування:</text>
  <text x="60" y="222" font-family="Arial" font-size="10.5" fill="#7e5109">«Дослівний текст висловлювання</text>
  <text x="60" y="240" font-family="Arial" font-size="10.5" fill="#7e5109">дослідника» [3, с. 45].</text>
  <text x="60" y="265" font-family="Arial" font-size="10.5" font-style="italic" fill="#b9770e">Береться у лапки, обов'язково</text>
  <text x="60" y="282" font-family="Arial" font-size="10.5" font-style="italic" fill="#b9770e">з посиланням на сторінку</text>

  <rect x="440" y="175" width="304" height="115" rx="10" fill="#ebf5fb" stroke="#2980b9" stroke-width="1.5"/>
  <text x="592" y="200" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e3a5f">Переказ (парафраз):</text>
  <text x="460" y="222" font-family="Arial" font-size="10.5" fill="#1e3a5f">На думку автора, основною</text>
  <text x="460" y="240" font-family="Arial" font-size="10.5" fill="#1e3a5f">умовою є … [3].</text>
  <text x="460" y="265" font-family="Arial" font-size="10.5" font-style="italic" fill="#2980b9">Без лапок, але з посиланням</text>
  <text x="460" y="282" font-family="Arial" font-size="10.5" font-style="italic" fill="#2980b9">на джерело</text>
</svg>
'''

SVG_ETHICS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420" width="720" height="420">
  <rect width="720" height="420" fill="#ffffff"/>
  <text x="360" y="28" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Етичні вимоги до науково-педагогічного дослідження</text>

  <circle cx="360" cy="220" r="75" fill="#1e3a5f"/>
  <text x="360" y="212" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">ЕТИКА</text>
  <text x="360" y="232" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#ffffff">ДОСЛІДЖЕННЯ</text>

  <line x1="360" y1="145" x2="360" y2="90" stroke="#2980b9" stroke-width="2"/>
  <rect x="270" y="50" width="180" height="45" rx="9" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="360" y="72" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">Добровільність</text>
  <text x="360" y="88" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#2980b9">згода учасників</text>

  <line x1="435" y1="185" x2="520" y2="140" stroke="#27ae60" stroke-width="2"/>
  <rect x="522" y="105" width="180" height="45" rx="9" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="612" y="127" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e5a3f">Конфіденційність</text>
  <text x="612" y="143" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#27ae60">захист даних</text>

  <line x1="435" y1="240" x2="520" y2="270" stroke="#e67e22" stroke-width="2"/>
  <rect x="522" y="248" width="180" height="45" rx="9" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="612" y="270" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7e5109">Не нашкодь</text>
  <text x="612" y="286" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#e67e22">безпека учасників</text>

  <line x1="360" y1="295" x2="360" y2="340" stroke="#8e44ad" stroke-width="2"/>
  <rect x="270" y="342" width="180" height="45" rx="9" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="360" y="364" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#4a235a">Правдивість</text>
  <text x="360" y="380" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#8e44ad">достовірні дані</text>

  <line x1="285" y1="240" x2="200" y2="270" stroke="#c0392b" stroke-width="2"/>
  <rect x="20" y="248" width="180" height="45" rx="9" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="110" y="270" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#7b241c">Повага до гідності</text>
  <text x="110" y="286" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#c0392b">гідне ставлення</text>

  <line x1="285" y1="185" x2="200" y2="140" stroke="#3498db" stroke-width="2"/>
  <rect x="20" y="105" width="180" height="45" rx="9" fill="#ebf5fb" stroke="#3498db" stroke-width="1.5"/>
  <text x="110" y="127" text-anchor="middle" font-family="Arial" font-size="11.5" font-weight="bold" fill="#1e3a5f">Прозорість</text>
  <text x="110" y="143" text-anchor="middle" font-family="Arial" font-size="9.5" fill="#3498db">відкритість методів</text>
</svg>
'''


# ============================================================
# 4. ЗМІСТ ДОКУМЕНТА
# ============================================================

def build_document():
    doc = setup_document()

    # ---------- Титульна частина ----------
    add_title(doc, "САМОСТІЙНА РОБОТА № 5", size=16, space_after=4)
    add_title(doc,
              "Академічна доброчесність та етика науково-педагогічних досліджень. "
              "Використання джерел і правила цитування",
              size=15, bold=True, space_after=10)
    add_title(doc, "Дисципліна: Основи науково-педагогічних досліджень",
              size=13, bold=False, space_after=2)
    add_title(doc, "Спеціальність: Початкова освіта", size=13, bold=False, space_after=12)

    # ---------- Мета ----------
    add_heading(doc, "Мета та завдання")
    add_paragraph(doc,
        "Мета: формувати знання про академічну доброчесність, етику науково-педагогічних "
        "досліджень і правила цитування; розвивати вміння коректно використовувати джерела "
        "та оформлювати цитування; виховувати академічну доброчесність і повагу до "
        "інтелектуальної власності.")
    add_paragraph(doc,
        "Завдання: опанувати принципи академічної доброчесності; вивчити види порушень "
        "і етичні вимоги до дослідження; опанувати правила цитування та оформлення "
        "покликань; підготувати повідомлення за результатами самостійної роботи.")
    add_paragraph(doc,
        "Обладнання: інструкційні картки, доступ до бібліотеки та онлайн-баз.")

    # ---------- Література ----------
    add_heading(doc, "Література")
    add_numbered(doc, "Лимар Ю. М. Основи науково-педагогічних досліджень. Чернігів: "
                      "Чернігівський національний педагогічний університет імені Т. Г. Шевченка, 2011. 56 с.")
    add_numbered(doc, "Дубасенюк О. А. Методологія та методи науково-педагогічного дослідження. "
                      "Житомир: Полісся, 2016. 256 с.")

    # ---------- 1. Академічна доброчесність ----------
    add_heading(doc, "1. Теоретична частина: академічна доброчесність")
    add_paragraph(doc,
        "Академічна доброчесність — це сукупність етичних принципів і визначених законом "
        "правил, якими мають керуватися учасники освітнього процесу під час навчання, "
        "викладання та провадження наукової діяльності. Її основою є чесність, довіра, "
        "повага, відповідальність і справедливість.")
    add_svg_image(doc, SVG_PRINCIPLES, width_cm=15,
                  caption="Рис. 1. Принципи академічної доброчесності")

    add_heading(doc, "1.1. Основні порушення академічної доброчесності", level=2)
    add_paragraph(doc, "До типових порушень належать:")
    add_bullet(doc, "привласнення чужих ідей, текстів або результатів досліджень без "
                    "належного посилання.", bold_prefix="Плагіат — ")
    add_bullet(doc, "вигадування даних або фактів, яких не існує.", bold_prefix="Фабрикація — ")
    add_bullet(doc, "навмисне викривлення або зміна результатів дослідження.",
               bold_prefix="Фальсифікація — ")
    add_bullet(doc, "використання сторонніх джерел під час виконання завдань.",
               bold_prefix="Списування — ")
    add_bullet(doc, "отримання неправомірної вигоди або упереджене оцінювання.",
               bold_prefix="Хабарництво — ")
    add_svg_image(doc, SVG_VIOLATIONS, width_cm=15,
                  caption="Рис. 2. Основні порушення академічної доброчесності")

    # ---------- 2. Етика дослідження ----------
    add_heading(doc, "2. Етика науково-педагогічного дослідження")
    add_paragraph(doc,
        "Етика науково-педагогічного дослідження — це система моральних норм, що регулюють "
        "взаємини дослідника з учасниками освітнього процесу, науковою спільнотою та "
        "суспільством загалом. Особливої ваги етичні вимоги набувають у дослідженнях "
        "з дітьми молодшого шкільного віку.")
    add_svg_image(doc, SVG_ETHICS, width_cm=15,
                  caption="Рис. 3. Етичні вимоги до науково-педагогічного дослідження")

    add_heading(doc, "2.1. Ключові етичні вимоги", level=2)
    add_table(doc,
        headers=["Вимога", "Зміст"],
        rows=[
            ["Добровільність", "Участь у дослідженні — лише за згодою; для молодших школярів — "
                               "з письмовою згодою батьків."],
            ["Конфіденційність", "Персональні дані учасників не розголошуються; у звітах "
                                 "використовуються узагальнені результати."],
            ["Не нашкодь", "Дослідження не повинно завдавати фізичної чи психологічної шкоди."],
            ["Правдивість", "Дані подаються достовірно, без викривлень і вигадок."],
            ["Повага до гідності", "Ставлення до учасників — шанобливе, без тиску й маніпуляцій."],
            ["Прозорість", "Методи й результати дослідження мають бути відкритими для перевірки."],
        ],
        col_widths=[4.5, 12.0])

    # ---------- 3. Правила цитування ----------
    add_heading(doc, "3. Використання джерел і правила цитування")
    add_paragraph(doc,
        "Цитування — це включення в науковий текст фрагментів інших джерел з обов'язковим "
        "посиланням на автора й видання. Коректне цитування є головним інструментом "
        "уникнення плагіату.")
    add_svg_image(doc, SVG_CITATION, width_cm=15,
                  caption="Рис. 4. Структура цитування наукового джерела")

    add_heading(doc, "3.1. Види цитування", level=2)
    add_table(doc,
        headers=["Вид", "Особливості", "Приклад"],
        rows=[
            ["Пряме (дослівне)", "Текст у лапках, обов'язково з посиланням на сторінку.",
             "«Текст цитати» [3, с. 45]."],
            ["Переказ (парафраз)", "Виклад думки автора своїми словами, без лапок, але з посиланням.",
             "На думку автора, основними є … [3]."],
            ["Узагальнене посилання", "Виклад кількох позицій одним реченням з кількома джерелами.",
             "Аналіз праць [1; 4; 7] засвідчує …"],
            ["Цитування за першоджерелом", "Посилання на автора, чию думку наведено в іншого дослідника.",
             "Цит. за: [5, с. 18]."],
        ],
        col_widths=[3.5, 7.0, 6.0])

    add_heading(doc, "3.2. Правила оформлення цитат", level=2)
    add_bullet(doc, "цитата береться в лапки («…»), якщо наводиться дослівно;")
    add_bullet(doc, "обов'язково вказується джерело та сторінка: [номер, с. X];")
    add_bullet(doc, "якщо цитата неповна, пропуск позначають трикрапкою: «…»;")
    add_bullet(doc, "у переказі лапки не ставлять, але посилання зберігають;")
    add_bullet(doc, "кожне джерело зі списку використаних має мати хоча б одне посилання в тексті;")
    add_bullet(doc, "бібліографічний опис оформлюють за ДСТУ 8302:2015.")

    # ---------- 4. Завдання ----------
    add_heading(doc, "4. Завдання для самостійного виконання")
    add_paragraph(doc,
        "Результати виконання всіх завдань оформіть у вигляді єдиного повідомлення.")
    add_numbered(doc, "Проаналізуйте 3 наукові джерела за темою власного дослідження. Для кожного "
                      "визначте, які саме ідеї ви будете використовувати, та складіть коректне "
                      "посилання (пряме цитування або переказ).")
    add_numbered(doc, "Наведіть 2 приклади порушень академічної доброчесності (з поясненням, "
                      "чому це порушення) та 2 приклади коректного використання джерел.")
    add_numbered(doc, "Складіть список із 5 джерел за темою вашого дослідження, оформлений "
                      "за ДСТУ 8302:2015.")
    add_numbered(doc, "Підготуйте текст (250–300 слів) із 2–3 цитатами та 2–3 переказами, "
                      "коректно оформивши всі посилання.")
    add_numbered(doc, "Оформіть повідомлення за вимогами (див. нижче) та подайте викладачу.")

    add_heading(doc, "Вимоги до оформлення повідомлення", level=2)
    add_bullet(doc, "обсяг — 3–5 сторінок без титульної сторінки та списку джерел;")
    add_bullet(doc, "структура: титульна сторінка, вступ, теоретична частина, практична "
                    "частина (завдання 1–4), висновки, список джерел;")
    add_bullet(doc, "шрифт Times New Roman, 14 pt, інтервал 1,25, вирівнювання по ширині, "
                    "поля 2 см;")
    add_bullet(doc, "джерела — за ДСТУ 8302:2015; усі цитати — з посиланнями;")
    add_bullet(doc, "унікальність тексту — не менше 70 %;")
    add_bullet(doc, "формат здачі — Word або PDF; назва файлу: Прізвище_Ім'я_СР5_Доброчесність.")

    # ---------- 5. Контрольні запитання ----------
    add_heading(doc, "5. Контрольні запитання")
    add_numbered(doc, "Що таке академічна доброчесність і які її основні принципи?")
    add_numbered(doc, "Назвіть і охарактеризуйте основні види порушень академічної доброчесності.")
    add_numbered(doc, "Чим відрізняються плагіат, фабрикація та фальсифікація?")
    add_numbered(doc, "Яких етичних норм має дотримуватися дослідник у роботі з молодшими школярами?")
    add_numbered(doc, "Які вимоги висувають до прямого цитування та переказу (парафразу)?")
    add_numbered(doc, "Як оформлюють посилання на джерело в тексті наукової роботи?")
    add_numbered(doc, "Що таке цитування за першоджерелом і коли його застосовують?")
    add_numbered(doc, "Які наслідки порушення академічної доброчесності для студента?")

    # ---------- Файл ----------
    output = "SR5_Akademichna_dobrochesnist.docx"
    doc.save(output)
    print(f"✅ Документ створено: {output}")


if __name__ == "__main__":
    build_document()