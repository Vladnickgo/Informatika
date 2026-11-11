#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор конспекту практичного заняття.
Тема: Програмні засоби обробки документів та інформації.
Види систем обробки текстів. Комунікаційні технології.
"""

import os
import cairosvg
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

IMAGES_DIR = "images"
OUTPUT_FILE = "konspekt_praktyka.docx"
os.makedirs(IMAGES_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════
#  1.  SVG-ДІАГРАМИ
# ═══════════════════════════════════════════════════════════════════

SVG_CLASSIFICATION = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 620"
     font-family="Arial, Liberation Sans, sans-serif">
  <rect width="1000" height="620" fill="#f4f7fb"/>

  <rect x="230" y="15" width="540" height="55" rx="10" fill="#1F3864"/>
  <text x="500" y="50" text-anchor="middle" font-size="22"
        font-weight="bold" fill="#ffffff">Класифікація систем обробки тексту</text>

  <line x1="500" y1="70" x2="500" y2="95" stroke="#1F3864" stroke-width="2.5"/>
  <line x1="170" y1="95" x2="830" y2="95" stroke="#1F3864" stroke-width="2.5"/>
  <line x1="170" y1="95" x2="170" y2="110" stroke="#1F3864" stroke-width="2.5"/>
  <line x1="500" y1="95" x2="500" y2="110" stroke="#1F3864" stroke-width="2.5"/>
  <line x1="830" y1="95" x2="830" y2="110" stroke="#1F3864" stroke-width="2.5"/>

  <!-- Column 1 -->
  <rect x="25" y="110" width="290" height="52" rx="8" fill="#2E75B6"/>
  <text x="170" y="143" text-anchor="middle" font-size="18"
        font-weight="bold" fill="#ffffff">Текстові редактори</text>
  <rect x="25" y="170" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="170" y="197" text-anchor="middle" font-size="14" fill="#1F3864">Введення та редагування тексту</text>
  <rect x="25" y="220" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="170" y="247" text-anchor="middle" font-size="14" fill="#1F3864">Робота з буфером обміну</text>
  <rect x="25" y="270" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="170" y="297" text-anchor="middle" font-size="14" fill="#1F3864">Пошук і заміна символів</text>
  <rect x="25" y="320" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="170" y="347" text-anchor="middle" font-size="14" fill="#1F3864">Збереження у файлах .txt</text>
  <rect x="25" y="370" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="170" y="397" text-anchor="middle" font-size="14" fill="#1F3864">Друк тексту</text>
  <rect x="25" y="420" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="170" y="447" text-anchor="middle" font-size="14" fill="#1F3864">Приклад: Блокнот (Notepad)</text>

  <!-- Column 2 -->
  <rect x="355" y="110" width="290" height="52" rx="8" fill="#2E75B6"/>
  <text x="500" y="143" text-anchor="middle" font-size="18"
        font-weight="bold" fill="#ffffff">Текстові процесори</text>
  <rect x="355" y="170" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="500" y="197" text-anchor="middle" font-size="14" fill="#1F3864">Форматування тексту</text>
  <rect x="355" y="220" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="500" y="247" text-anchor="middle" font-size="14" fill="#1F3864">Перевірка правопису</text>
  <rect x="355" y="270" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="500" y="297" text-anchor="middle" font-size="14" fill="#1F3864">Вставлення таблиць, формул, графіки</text>
  <rect x="355" y="320" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="500" y="347" text-anchor="middle" font-size="14" fill="#1F3864">Автоматизація роботи користувача</text>
  <rect x="355" y="370" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="500" y="397" text-anchor="middle" font-size="14" fill="#1F3864">Оформлення сторінок</text>
  <rect x="355" y="420" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="500" y="447" text-anchor="middle" font-size="14" fill="#1F3864">Принцип WYSIWYG</text>

  <!-- Column 3 -->
  <rect x="685" y="110" width="290" height="52" rx="8" fill="#2E75B6"/>
  <text x="830" y="143" text-anchor="middle" font-size="18"
        font-weight="bold" fill="#ffffff">Видавничі системи</text>
  <rect x="685" y="170" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="830" y="197" text-anchor="middle" font-size="14" fill="#1F3864">Маніпулювання блоками тексту</text>
  <rect x="685" y="220" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="830" y="247" text-anchor="middle" font-size="14" fill="#1F3864">Робота з ілюстраціями</text>
  <rect x="685" y="270" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="830" y="297" text-anchor="middle" font-size="14" fill="#1F3864">Зміна формату документа</text>
  <rect x="685" y="320" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="830" y="347" text-anchor="middle" font-size="14" fill="#1F3864">Поліграфічна якість продукції</text>
  <rect x="685" y="370" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="830" y="397" text-anchor="middle" font-size="14" fill="#1F3864">Приклад: Adobe InDesign</text>
  <rect x="685" y="420" width="290" height="42" rx="6" fill="#DEEBF7"/>
  <text x="830" y="447" text-anchor="middle" font-size="14" fill="#1F3864">Scribus, QuarkXPress</text>

  <!-- arrows between columns (inheritance) -->
  <text x="325" y="500" text-anchor="middle" font-size="13"
        font-style="italic" fill="#C00000">↓ включає функції редакторів</text>
  <text x="655" y="500" text-anchor="middle" font-size="13"
        font-style="italic" fill="#C00000">↓ включає функції процесорів</text>

  <text x="500" y="570" text-anchor="middle" font-size="14"
        fill="#404040">Кожен наступний рівень успадковує можливості попереднього</text>
</svg>'''


SVG_COMMUNICATIONS = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 540"
     font-family="Arial, Liberation Sans, sans-serif">
  <rect width="1000" height="540" fill="#f4f7fb"/>

  <rect x="280" y="15" width="440" height="55" rx="10" fill="#1F3864"/>
  <text x="500" y="50" text-anchor="middle" font-size="22"
        font-weight="bold" fill="#ffffff">Види комунікацій</text>

  <!-- Column 1 -->
  <rect x="15" y="95" width="235" height="50" rx="8" fill="#2E75B6"/>
  <text x="132" y="127" text-anchor="middle" font-size="16"
        font-weight="bold" fill="#ffffff">За способом</text>
  <rect x="15" y="155" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="132" y="180" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Письмова</text>
  <text x="132" y="202" text-anchor="middle" font-size="13" fill="#333333">статут, звіти,</text>
  <text x="132" y="222" text-anchor="middle" font-size="13" fill="#333333">протоколи, e-mail</text>
  <rect x="15" y="260" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="132" y="285" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Усна</text>
  <text x="132" y="307" text-anchor="middle" font-size="13" fill="#333333">наради, обговорення,</text>
  <text x="132" y="327" text-anchor="middle" font-size="13" fill="#333333">свята</text>

  <!-- Column 2 -->
  <rect x="260" y="95" width="235" height="50" rx="8" fill="#2E75B6"/>
  <text x="377" y="127" text-anchor="middle" font-size="16"
        font-weight="bold" fill="#ffffff">За характером</text>
  <rect x="260" y="155" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="377" y="180" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Формальна</text>
  <text x="377" y="202" text-anchor="middle" font-size="13" fill="#333333">звіти, накази,</text>
  <text x="377" y="222" text-anchor="middle" font-size="13" fill="#333333">офіційні документи</text>
  <rect x="260" y="260" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="377" y="285" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Неформальна</text>
  <text x="377" y="307" text-anchor="middle" font-size="13" fill="#333333">записки,</text>
  <text x="377" y="327" text-anchor="middle" font-size="13" fill="#333333">особисті листи</text>

  <!-- Column 3 -->
  <rect x="505" y="95" width="235" height="50" rx="8" fill="#2E75B6"/>
  <text x="622" y="127" text-anchor="middle" font-size="16"
        font-weight="bold" fill="#ffffff">За напрямком</text>
  <rect x="505" y="155" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="622" y="180" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Внутрішня</text>
  <text x="622" y="202" text-anchor="middle" font-size="13" fill="#333333">всередині</text>
  <text x="622" y="222" text-anchor="middle" font-size="13" fill="#333333">проєкту</text>
  <rect x="505" y="260" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="622" y="285" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Зовнішня</text>
  <text x="622" y="307" text-anchor="middle" font-size="13" fill="#333333">споживачі, ЗМІ,</text>
  <text x="622" y="327" text-anchor="middle" font-size="13" fill="#333333">громадськість</text>

  <!-- Column 4 -->
  <rect x="750" y="95" width="235" height="50" rx="8" fill="#2E75B6"/>
  <text x="867" y="127" text-anchor="middle" font-size="16"
        font-weight="bold" fill="#ffffff">За рівнем</text>
  <rect x="750" y="155" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="867" y="180" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Вертикальна</text>
  <text x="867" y="202" text-anchor="middle" font-size="13" fill="#333333">вгору / вниз</text>
  <text x="867" y="222" text-anchor="middle" font-size="13" fill="#333333">по ієрархії</text>
  <rect x="750" y="260" width="235" height="95" rx="6" fill="#DEEBF7"/>
  <text x="867" y="285" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Горизонтальна</text>
  <text x="867" y="307" text-anchor="middle" font-size="13" fill="#333333">з рівними</text>
  <text x="867" y="327" text-anchor="middle" font-size="13" fill="#333333">за статусом</text>

  <text x="500" y="420" text-anchor="middle" font-size="14" fill="#404040">
    Кожен вид комунікації обирається залежно від терміновості, доступності технологій,
    кваліфікації персоналу та тривалості проєкту.
  </text>
</svg>'''


SVG_WYSIWYG = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 460"
     font-family="Arial, Liberation Sans, sans-serif">
  <rect width="1000" height="460" fill="#f4f7fb"/>

  <rect x="300" y="15" width="400" height="55" rx="10" fill="#1F3864"/>
  <text x="500" y="50" text-anchor="middle" font-size="22"
        font-weight="bold" fill="#ffffff">Принцип WYSIWYG</text>

  <!-- Left: screen -->
  <rect x="40" y="100" width="400" height="290" rx="8" fill="#ffffff" stroke="#1F3864" stroke-width="3"/>
  <rect x="40" y="100" width="400" height="32" rx="8" fill="#1F3864"/>
  <text x="240" y="122" text-anchor="middle" font-size="14" fill="#ffffff">Екранний зразок</text>
  <rect x="60" y="150" width="360" height="20" rx="3" fill="#C00000"/>
  <text x="240" y="165" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">Заголовок документа</text>
  <rect x="60" y="185" width="360" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="60" y="207" width="340" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="60" y="229" width="360" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="60" y="251" width="310" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="60" y="285" width="360" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="60" y="307" width="350" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="60" y="329" width="280" height="15" rx="2" fill="#BFBFBF"/>

  <!-- Double arrow -->
  <line x1="470" y1="240" x2="530" y2="240" stroke="#2E75B6" stroke-width="3"/>
  <line x1="530" y1="240" x2="470" y2="240" stroke="#2E75B6" stroke-width="3"/>
  <text x="500" y="220" text-anchor="middle" font-size="16"
        font-weight="bold" fill="#2E75B6">WYSIWYG</text>
  <text x="500" y="270" text-anchor="middle" font-size="13" fill="#404040">=</text>

  <!-- Right: print -->
  <rect x="560" y="100" width="400" height="290" rx="8" fill="#ffffff" stroke="#1F3864" stroke-width="3"/>
  <rect x="560" y="100" width="400" height="32" rx="8" fill="#1F3864"/>
  <text x="760" y="122" text-anchor="middle" font-size="14" fill="#ffffff">Друкований вигляд</text>
  <rect x="580" y="150" width="360" height="20" rx="3" fill="#C00000"/>
  <text x="760" y="165" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">Заголовок документа</text>
  <rect x="580" y="185" width="360" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="580" y="207" width="340" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="580" y="229" width="360" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="580" y="251" width="310" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="580" y="285" width="360" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="580" y="307" width="350" height="15" rx="2" fill="#BFBFBF"/>
  <rect x="580" y="329" width="280" height="15" rx="2" fill="#BFBFBF"/>

  <text x="500" y="425" text-anchor="middle" font-size="14" fill="#404040">
    What You See Is What You Get — «що бачиш, те й маєш»
  </text>
</svg>'''


SVG_HIERARCHY = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560"
     font-family="Arial, Liberation Sans, sans-serif">
  <rect width="900" height="560" fill="#f4f7fb"/>

  <rect x="250" y="15" width="400" height="50" rx="10" fill="#1F3864"/>
  <text x="450" y="47" text-anchor="middle" font-size="20"
        font-weight="bold" fill="#ffffff">Ієрархія можливостей</text>

  <!-- outer -->
  <rect x="60" y="100" width="780" height="400" rx="20"
        fill="#E2EFDA" stroke="#548235" stroke-width="3"/>
  <text x="450" y="135" text-anchor="middle" font-size="17"
        font-weight="bold" fill="#375623">Видавничі системи</text>
  <text x="450" y="158" text-anchor="middle" font-size="13" fill="#375623">
    + верстка, поліграфія, робота з блоками
  </text>

  <!-- middle -->
  <rect x="130" y="185" width="640" height="290" rx="16"
        fill="#FFF2CC" stroke="#BF9000" stroke-width="3"/>
  <text x="450" y="218" text-anchor="middle" font-size="17"
        font-weight="bold" fill="#7F6000">Текстові процесори</text>
  <text x="450" y="241" text-anchor="middle" font-size="13" fill="#7F6000">
    + форматування, таблиці, формули, зображення
  </text>

  <!-- inner -->
  <rect x="200" y="270" width="500" height="180" rx="14"
        fill="#DEEBF7" stroke="#2E75B6" stroke-width="3"/>
  <text x="450" y="305" text-anchor="middle" font-size="17"
        font-weight="bold" fill="#1F3864">Текстові редактори</text>
  <text x="450" y="330" text-anchor="middle" font-size="13" fill="#1F3864">
    базові: введення, редагування, збереження
  </text>
  <text x="450" y="355" text-anchor="middle" font-size="13" fill="#1F3864">
    неформатований текст (.txt)
  </text>

  <text x="450" y="530" text-anchor="middle" font-size="14" fill="#404040">
    Кожен зовнішній рівень включає всі можливості внутрішнього
  </text>
</svg>'''


# ═══════════════════════════════════════════════════════════════════
#  2.  ЗБЕРЕЖЕННЯ SVG → PNG
# ═══════════════════════════════════════════════════════════════════

def save_svg(name: str, content: str) -> str:
    svg_path = os.path.join(IMAGES_DIR, name + ".svg")
    png_path = os.path.join(IMAGES_DIR, name + ".png")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2.5)
    return png_path


# ═══════════════════════════════════════════════════════════════════
#  3.  ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ═══════════════════════════════════════════════════════════════════

def set_normal_style(doc: Document) -> None:
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(14)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(attr), 'Times New Roman')
    pf = style.paragraph_format
    pf.line_spacing = 1.25
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_after = Pt(6)


def setup_page(doc: Document) -> None:
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)


def _apply_run_font(run, size=14, bold=False, italic=False, color=None, underline=False):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.underline = underline
    if color is not None:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(attr), 'Times New Roman')


def add_paragraph(doc, text, bold=False, italic=False, size=14,
                  color=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                  space_before=0, space_after=6, underline=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    _apply_run_font(run, size=size, bold=bold, italic=italic, color=color, underline=underline)
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = 1.25
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet' if level == 0 else 'List Bullet 2')
    run = p.add_run(text)
    _apply_run_font(run, size=14)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.line_spacing = 1.25
    pf.space_after = Pt(2)
    return p


def add_heading(doc, text, level=1):
    size = {1: 18, 2: 16, 3: 14}[level]
    align = WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
    p = doc.add_paragraph()
    run = p.add_run(text)
    _apply_run_font(run, size=size, bold=True)
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = 1.25
    pf.space_before = Pt(14 if level == 1 else 10)
    pf.space_after = Pt(8 if level == 1 else 4)
    return p


def add_image(doc, png_path, width_cm=15, caption=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run()
    run.add_picture(png_path, width=Cm(width_cm))
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run(caption)
        _apply_run_font(cr, size=12, italic=True, color=RGBColor(0x55, 0x55, 0x55))
        cp.paragraph_format.space_after = Pt(10)


def add_table(doc, headers, rows, widths_cm=None, header_fill="DEEBF7"):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        p = hdr[i].paragraphs[0]
        r = p.add_run(h)
        _apply_run_font(r, size=13, bold=True, color=RGBColor(0x1F, 0x38, 0x64))
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        # fill
        tcPr = hdr[i]._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), header_fill)
        tcPr.append(shd)

    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ''
            p = cells[i].paragraphs[0]
            r = p.add_run(str(val))
            _apply_run_font(r, size=12)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15

    if widths_cm:
        for i, w in enumerate(widths_cm):
            for row in table.rows:
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


# ═══════════════════════════════════════════════════════════════════
#  4.  НАПОВНЕННЯ ДОКУМЕНТА
# ═══════════════════════════════════════════════════════════════════

def build_title_block(doc):
    add_paragraph(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ",
                  bold=True, size=20, align=WD_ALIGN_PARAGRAPH.CENTER,
                  space_after=4)
    add_paragraph(doc,
                  "Програмні засоби обробки документів та інформації. "
                  "Види систем обробки текстів. Комунікаційні технології",
                  bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER,
                  space_after=12)

    info = [
        ("Спеціальність", "013 Початкова освіта. Вчитель інформатики початкової школи"),
        ("Дисципліна", "Інформаційно-комунікаційні технології"),
        ("Тривалість", "80 хв (практична частина — до 30 хв)"),
        ("Мета", "Ознайомити студентів із класифікацією систем обробки тексту, "
                 "їх призначенням та можливостями; сформувати уявлення про "
                 "комунікаційні технології; розвивати практичні навички роботи "
                 "з текстовими редакторами, процесорами та онлайн-сервісами."),
        ("Обладнання", "ПК з ОС Windows/Linux, Microsoft Word / LibreOffice Writer, "
                       "Блокнот (Notepad), Google Docs, проєктор, презентація, "
                       "доступ до мережі Інтернет."),
    ]
    table = doc.add_table(rows=0, cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for label, value in info:
        cells = table.add_row().cells
        cells[0].width = Cm(3.5)
        cells[1].width = Cm(13.5)
        r1 = cells[0].paragraphs[0].add_run(label)
        _apply_run_font(r1, size=13, bold=True)
        cells[0].paragraphs[0].paragraph_format.line_spacing = 1.15
        r2 = cells[1].paragraphs[0].add_run(value)
        _apply_run_font(r2, size=13)
        cells[1].paragraphs[0].paragraph_format.line_spacing = 1.15
        cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_paragraph(doc, "", space_after=0)


def build_theory(doc, img_classification, img_comms, img_wysiwyg, img_hierarchy):
    add_heading(doc, "І. Актуалізація опорних знань (5 хв)", level=1)
    add_paragraph(doc, "Бесіда за запитаннями:")
    for q in [
        "Які пристрої використовуються для введення та виведення тексту?",
        "У яких програмах ви вже працювали з текстом?",
        "Чим відрізняється звичайний текст від форматованого?",
        "Що таке шрифт, абзац, вирівнювання?",
    ]:
        add_bullet(doc, q)

    add_heading(doc, "ІІ. Теоретична частина (20 хв)", level=1)

    add_heading(doc, "2.1. Історична довідка", level=2)
    add_paragraph(doc,
        "Записування інформаційних повідомлень у вигляді тексту — один із "
        "найстаріших та найпоширеніших методів їх зберігання. У давнину люди "
        "записували тексти очеретяними паличками на табличках із сирої глини, "
        "писали на папірусі, гусячими перами — на пергаменті та папері. "
        "Копії з книжок робили вручну.")
    add_paragraph(doc,
        "З появою в XV столітті книгодрукування стало можливим виготовляти "
        "друковану продукцію масовими тиражами. Проте механічний засіб "
        "автоматизації ручного письма — друкарську машинку — було винайдено "
        "значно пізніше, у 1860-х роках. Відразу після цього виникла нова "
        "професія — машиністка.")
    add_paragraph(doc,
        "Сьогодні ж, коли в нашому розпорядженні є комп'ютери, програми для "
        "введення й редагування тексту та принтери, кожен без особливих зусиль "
        "може створювати тексти будь-якої складності, оформлювати їх за своїми "
        "уподобаннями й роздруковувати в багатьох примірниках.")

    add_heading(doc, "2.2. Класифікація систем обробки тексту", level=2)
    add_paragraph(doc,
        "Усі програми для роботи з текстом поділяють на три великі категорії. "
        "Розглянемо їх детальніше (рис. 1).")
    add_image(doc, img_classification, width_cm=15.5,
              caption="Рис. 1. Класифікація систем обробки тексту")

    add_heading(doc, "2.3. Текстові редактори", level=2)
    add_paragraph(doc,
        "Текстовий редактор — програма, призначена для введення, редагування "
        "і збереження у файлах неформатованого тексту, тобто тексту, всі "
        "символи якого мають однакові параметри відображення. Програми цієї "
        "категорії часто використовують для введення текстів програм і "
        "створення файлів, які містять конфігураційні параметри операційної "
        "системи.")
    add_paragraph(doc,
        "Текстові редактори включено до набору стандартних застосунків "
        "операційних систем — зокрема, до складу всіх версій Windows входить "
        "програма Блокнот (Notepad). Файли, створені за допомогою текстових "
        "редакторів, мають розширення імені .txt.")

    add_heading(doc, "2.4. Текстові процесори", level=2)
    add_paragraph(doc,
        "Програми, що дають змогу створювати, обробляти та зберігати "
        "форматований текст, називають текстовими процесорами. Такі файли "
        "можуть містити зображення, діаграми, таблиці, формули, звукові "
        "вставки, відеокліпи та інші об’єкти.")
    add_paragraph(doc,
        "Текстові процесори використовують у діловодстві — для створення "
        "бланків, договорів тощо, для підготовки різноманітних матеріалів. "
        "Особливої зручності додає те, що більшість текстових процесорів "
        "працює за принципом WYSIWYG (What You See Is What You Get — "
        "«що бачиш, те й маєш»), тобто екранний зразок сторінки відповідає "
        "її реальному, друкованому вигляду (рис. 2).")
    add_image(doc, img_wysiwyg, width_cm=15,
              caption="Рис. 2. Принцип WYSIWYG")
    add_paragraph(doc,
        "Серед текстових процесорів найвідомішим вважається Microsoft Word, "
        "що входить до складу пакета Microsoft Office. Альтернативою йому є "
        "Writer з пакета LibreOffice / OpenOffice.org, який за можливостями "
        "мало в чому поступається своєму конкурентові, однак є цілком "
        "безкоштовним. Сучасні онлайн-сервіси (Google Docs, Microsoft 365) "
        "дають змогу працювати з документами у «хмарі» та спільно "
        "редагувати їх.")

    add_heading(doc, "2.5. Видавничі системи", level=2)
    add_paragraph(doc,
        "Для розробки професійної поліграфічної продукції (газет, книжок, "
        "журналів, рекламних буклетів тощо) використовують видавничі системи. "
        "Вони мають зручні засоби для підготовки багатосторінкових складних "
        "видань і дають змогу отримати матеріали, що задовольняють вимогам "
        "типографії. Тексти для видавничих систем зазвичай готують за "
        "допомогою текстових процесорів; ілюстрації також створюють у "
        "спеціалізованих програмах.")

    add_heading(doc, "2.6. Порівняння можливостей", level=2)
    add_paragraph(doc,
        "Кожна наступна категорія програм включає всі можливості попередньої "
        "(рис. 3): видавничі системи виконують усі функції текстових "
        "процесорів, а текстові процесори — усі функції текстових редакторів.")
    add_image(doc, img_hierarchy, width_cm=13.5,
              caption="Рис. 3. Ієрархія можливостей систем обробки тексту")

    add_heading(doc, "2.7. Комунікаційні технології", level=2)
    add_paragraph(doc,
        "Вибір засобів і технологій комунікації визначається рядом факторів: "
        "терміновість отримання інформації, доступність технологій, персонал, "
        "задіяний у проєкті, тривалість проєкту, оточення проєкту. Основні "
        "види комунікацій подано на рис. 4.")
    add_image(doc, img_comms, width_cm=15.5,
              caption="Рис. 4. Види комунікацій")

    add_paragraph(doc, "Для офіційних комунікацій можна виділити такі способи:")
    add_bullet(doc, "Письмові звіти, листи, факси, електронна пошта.")
    add_bullet(doc, "Наради, телеконференції.")
    add_bullet(doc, "Інтернет-технології (Google Docs, Microsoft 365, «хмарні» сховища).")
    add_paragraph(doc,
        "Популярності набуває концепція BYOD (Bring Your Own Device — "
        "«принеси свій пристрій»), коли працівники отримують доступ до "
        "корпоративної інформації зі смартфонів, планшетів та інших "
        "особистих пристроїв у зручний час.")


def build_practical(doc):
    add_heading(doc, "ІІІ. Практична частина (до 30 хв)", level=1)
    add_paragraph(doc,
        "Завдання має три рівні складності. Студент самостійно обирає рівень, "
        "на якому він хоче працювати, або виконує їх послідовно. "
        "Орієнтовний час: рівень 1 — 8 хв, рівень 2 — 12 хв, рівень 3 — 10 хв.")

    # --- Level 1 ---
    add_heading(doc, "Рівень 1 (базовий, 8 хв). «Простий текст у Блокноті»", level=2)
    add_paragraph(doc, "Завдання:")
    steps1 = [
        "Запустіть програму Блокнот (Notepad).",
        "Наберіть текст із 5–6 речень про історію обробки текстів (скористайтеся матеріалом теоретичної частини).",
        "Збережіть файл у власній папці під назвою istoriya.txt.",
        "Закрийте та знову відкрийте файл. Переконайтеся, що текст відображається без форматування.",
        "Зробіть висновок: які можливості має текстовий редактор і чого він не вміє?",
    ]
    for i, s in enumerate(steps1, 1):
        add_paragraph(doc, f"{i}. {s}")

    # --- Level 2 ---
    add_heading(doc, "Рівень 2 (середній, 12 хв). «Форматування документа “Цікавинки”»", level=2)
    add_paragraph(doc,
        "Створіть у Microsoft Word (або Google Docs) документ «Цікавинки», "
        "що складається із заголовка та шести абзаців тексту. Застосуйте до "
        "кожного елемента форматування згідно з таблицею 1.")
    add_paragraph(doc, "Таблиця 1. Параметри форматування", bold=True,
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    fmt_rows = [
        ("Заголовок", "Напівжирний", "Червоний", "По центру"),
        ("Абзац 1", "Курсив", "Чорнильний (темно-синій)", "По ширині"),
        ("Абзац 2", "Підкреслений", "Зелений", "По лівому краю"),
        ("Абзац 3", "Курсив", "Блакитний", "По правому краю"),
        ("Абзац 4", "Підкреслений", "Синій", "По ширині"),
        ("Абзац 5", "Курсив", "Чорний", "По лівому краю"),
        ("Абзац 6", "Підкреслений", "Помаранчевий", "По правому краю"),
    ]
    add_table(doc, ["Абзац", "Шрифт", "Колір", "Вирівнювання"],
              fmt_rows, widths_cm=[3.0, 3.5, 5.0, 3.5])
    add_paragraph(doc,
        "Додатково: додайте нумерований список із 3 пунктів (наприклад, "
        "«Цікаві факти про текст») та збережіть файл як cikavynky.docx.")

    # --- Level 3 ---
    add_heading(doc, "Рівень 3 (високий, 10 хв). «Пам'ятка “Види комунікацій”»", level=2)
    add_paragraph(doc,
        "Створіть документ-пам'ятку для вчителя початкової школи за таким планом:")
    steps3 = [
        "Додайте заголовок «Види комунікацій у проєктній роботі» (стиль «Заголовок 1»).",
        "Вставте таблицю з 3 стовпців і 5 рядків (шапка + 4 види комунікацій) та заповніть її прикладами.",
        "Вставте зображення (схему з теоретичної частини) та додайте підпис до нього.",
        "Налаштуйте параметри сторінки: поля 2 см з усіх боків, орієнтація — книжкова.",
        "Збережіть файл як pamyatka.docx та надішліть його на перевірку.",
    ]
    for i, s in enumerate(steps3, 1):
        add_paragraph(doc, f"{i}. {s}")

    add_heading(doc, "Критерії оцінювання практичної частини", level=2)
    add_bullet(doc, "Рівень 1 — 6 балів: файл створено, текст набрано без помилок, зроблено висновок.")
    add_bullet(doc, "Рівень 2 — 8 балів: усі елементи відформатовано згідно з таблицею, додано список.")
    add_bullet(doc, "Рівень 3 — 10 балів: створено повноцінний документ-пам'ятку з таблицею та зображенням.")


def build_control_questions(doc):
    add_heading(doc, "ІV. Контрольні запитання (5 хв)", level=1)
    questions = [
        "Що таке текстовий редактор? Наведіть приклади.",
        "Що таке текстовий процесор? Чим він відрізняється від текстового редактора?",
        "Які файли мають розширення .txt і чому?",
        "Що означає принцип WYSIWYG?",
        "Які можливості мають видавничі системи? Наведіть приклади.",
        "Назвіть основні види комунікацій.",
        "Які фактори впливають на вибір засобів комунікації?",
        "У чому переваги використання «хмарних» технологій для спільної роботи з документами?",
        "Що таке концепція BYOD?",
        "Які переваги та недоліки письмових комунікацій порівняно з усними?",
        "Як обрати оптимальний засіб обробки тексту для конкретної навчальної задачі?",
        "Які санітарно-гігієнічні вимоги слід враховувати під час роботи учнів початкової школи з текстом на комп'ютері?",
    ]
    for i, q in enumerate(questions, 1):
        add_paragraph(doc, f"{i}. {q}")


def build_homework_and_summary(doc):
    add_heading(doc, "V. Підсумок заняття. Домашнє завдання (3 хв)", level=1)
    add_paragraph(doc, "Домашнє завдання:")
    add_bullet(doc, "Опрацювати конспект практичного заняття.")
    add_bullet(doc,
        "Створити порівняльну таблицю «Текстовий редактор — Текстовий процесор — "
        "Видавнича система» (не менше 5 критеріїв порівняння).")
    add_bullet(doc,
        "Підготувати коротке повідомлення (5–7 речень) про один із сучасних "
        "онлайн-сервісів для спільної роботи з документами (Google Docs, "
        "Microsoft 365, OnlyOffice тощо).")
    add_paragraph(doc,
        "Рефлексія: студенти по колу висловлюються одним реченням, "
        "що нового вони дізналися на занятті та що хотіли б опанувати глибше.")


# ═══════════════════════════════════════════════════════════════════
#  5.  ГОЛОВНА ФУНКЦІЯ
# ═══════════════════════════════════════════════════════════════════

def main():
    print("⏳ Генерація SVG-діаграм...")
    img_classification = save_svg("classification", SVG_CLASSIFICATION)
    img_comms         = save_svg("communications", SVG_COMMUNICATIONS)
    img_wysiwyg       = save_svg("wysiwyg", SVG_WYSIWYG)
    img_hierarchy     = save_svg("hierarchy", SVG_HIERARCHY)
    print(f"   ✓ Збережено у папці '{IMAGES_DIR}/' (SVG + PNG)")

    print("⏳ Формування DOCX...")
    doc = Document()
    set_normal_style(doc)
    setup_page(doc)

    build_title_block(doc)
    build_theory(doc, img_classification, img_comms, img_wysiwyg, img_hierarchy)
    build_practical(doc)
    build_control_questions(doc)
    build_homework_and_summary(doc)

    doc.save(OUTPUT_FILE)
    print(f"✅ Документ збережено: {OUTPUT_FILE}")
    print(f"📁 Зображення: {IMAGES_DIR}/")
    print("\nСтруктура папки images/:")
    for f in sorted(os.listdir(IMAGES_DIR)):
        size = os.path.getsize(os.path.join(IMAGES_DIR, f))
        print(f"   • {f:35s} {size/1024:6.1f} KB")


if __name__ == "__main__":
    main()