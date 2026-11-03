# -*- coding: utf-8 -*-
"""
Генерація DOCX для лекційного заняття № 11
Тема: Інтерпретація результатів. Пояснення отриманих даних,
      порівняння з існуючими теоріями
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

SVG_INTERPRETATION_STAGES = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 280" width="820" height="280">
  <rect width="820" height="280" fill="#ffffff"/>
  <text x="410" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Етапи інтерпретації результатів дослідження</text>

  <rect x="15" y="60" width="145" height="90" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="1.5"/>
  <text x="87" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e3a5f">1. Опис</text>
  <text x="87" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">що показали</text>
  <text x="87" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">дані</text>

  <polygon points="162,105 178,95 178,115" fill="#2980b9"/>

  <rect x="180" y="60" width="145" height="90" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="1.5"/>
  <text x="252" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#1e5a3f">2. Пояснення</text>
  <text x="252" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">чому саме так</text>
  <text x="252" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">(причини)</text>

  <polygon points="327,105 343,95 343,115" fill="#2980b9"/>

  <rect x="345" y="60" width="145" height="90" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="1.5"/>
  <text x="417" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7e5109">3. Порівняння</text>
  <text x="417" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">з теоріями,</text>
  <text x="417" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">дослідженнями</text>

  <polygon points="492,105 508,95 508,115" fill="#2980b9"/>

  <rect x="510" y="60" width="145" height="90" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="1.5"/>
  <text x="582" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#4a235a">4. Узагальнення</text>
  <text x="582" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">висновки,</text>
  <text x="582" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">закономірності</text>

  <polygon points="657,105 673,95 673,115" fill="#2980b9"/>

  <rect x="675" y="60" width="130" height="90" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="740" y="86" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="#7b241c">5. Висновки</text>
  <text x="740" y="106" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#c0392b">та</text>
  <text x="740" y="122" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#c0392b">рекомендації</text>

  <text x="410" y="200" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic" fill="#475569">Інтерпретація — це перехід від «що видно на графіку» до «що це означає</text>
  <text x="410" y="222" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic" fill="#475569">для теорії та практики початкової освіти»</text>
  <text x="410" y="252" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Кожен етап спирається на попередній: без опису неможливе пояснення, без порівняння — узагальнення</text>
</svg>
'''

SVG_COMPARISON_THEORY = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 380" width="760" height="380">
  <rect width="760" height="380" fill="#ffffff"/>
  <text x="380" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Три можливі результати порівняння з теорією</text>

  <rect x="30" y="55" width="220" height="260" rx="12" fill="#eafaf1" stroke="#27ae60" stroke-width="2"/>
  <text x="140" y="85" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e5a3f">ПІДТВЕРДЖЕННЯ</text>
  <text x="140" y="115" text-anchor="middle" font-family="Arial" font-size="11" fill="#27ae60">результати узгоджуються</text>
  <text x="140" y="132" text-anchor="middle" font-family="Arial" font-size="11" fill="#27ae60">з відомою теорією</text>
  <circle cx="140" cy="185" r="28" fill="#27ae60"/>
  <text x="140" y="194" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#ffffff">✓</text>
  <text x="140" y="245" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#1e5a3f">посилює надійність</text>
  <text x="140" y="262" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#1e5a3f">висновків дослідження</text>
  <text x="140" y="290" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#64748b">напр., гіпотеза</text>
  <text x="140" y="305" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#64748b">підтверджена</text>

  <rect x="270" y="55" width="220" height="260" rx="12" fill="#fef9e7" stroke="#e67e22" stroke-width="2"/>
  <text x="380" y="85" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#7e5109">УТОЧНЕННЯ</text>
  <text x="380" y="115" text-anchor="middle" font-family="Arial" font-size="11" fill="#e67e22">результати доповнюють</text>
  <text x="380" y="132" text-anchor="middle" font-family="Arial" font-size="11" fill="#e67e22">теорію новими умовами</text>
  <circle cx="380" cy="185" r="28" fill="#e67e22"/>
  <text x="380" y="194" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#ffffff">+</text>
  <text x="380" y="245" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#7e5109">поглиблює розуміння</text>
  <text x="380" y="262" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#7e5109">конкретних умов</text>
  <text x="380" y="290" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#64748b">напр., виявлено</text>
  <text x="380" y="305" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#64748b">нові чинники</text>

  <rect x="510" y="55" width="220" height="260" rx="12" fill="#fdedec" stroke="#c0392b" stroke-width="2"/>
  <text x="620" y="85" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#7b241c">СУПЕРЕЧНІСТЬ</text>
  <text x="620" y="115" text-anchor="middle" font-family="Arial" font-size="11" fill="#c0392b">результати не узгоджуються</text>
  <text x="620" y="132" text-anchor="middle" font-family="Arial" font-size="11" fill="#c0392b">з відомою теорією</text>
  <circle cx="620" cy="185" r="28" fill="#c0392b"/>
  <text x="620" y="194" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#ffffff">!</text>
  <text x="620" y="245" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#7b241c">потребує критичного</text>
  <text x="620" y="262" text-anchor="middle" font-family="Arial" font-size="11" font-style="italic" fill="#7b241c">аналізу й пояснення</text>
  <text x="620" y="290" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#64748b">напр., нові умови</text>
  <text x="620" y="305" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#64748b">дослідження</text>
</svg>
'''

SVG_ERRORS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 380" width="760" height="380">
  <rect width="760" height="380" fill="#ffffff"/>
  <text x="380" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Типові помилки інтерпретації результатів</text>

  <rect x="30" y="55" width="340" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="50" y="82" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">1. Підміна причини кореляцією</text>
  <text x="50" y="105" font-family="Arial" font-size="10.5" fill="#a93226">«Якщо два показники зростають одночасно,</text>
  <text x="50" y="122" font-family="Arial" font-size="10.5" fill="#a93226">це ще не означає, що один — причина іншого»</text>
  <text x="50" y="150" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Приклад: оцінки зросли разом із відвідуванням</text>
  <text x="50" y="167" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">гуртка — але це не доводить причинності</text>

  <rect x="390" y="55" width="340" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="410" y="82" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">2. Надмірне узагальнення</text>
  <text x="410" y="105" font-family="Arial" font-size="10.5" fill="#a93226">«Висновки за однією вибіркою поширюють</text>
  <text x="410" y="122" font-family="Arial" font-size="10.5" fill="#a93226">на всіх учнів початкової школи»</text>
  <text x="410" y="150" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Приклад: 20 учнів одного класу —</text>
  <text x="410" y="167" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">не вся генеральна сукупність</text>

  <rect x="30" y="200" width="340" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="50" y="227" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">3. Ігнорування статистичної значущості</text>
  <text x="50" y="250" font-family="Arial" font-size="10.5" fill="#a93226">«Різниця в 0,5 бала може бути</text>
  <text x="50" y="267" font-family="Arial" font-size="10.5" fill="#a93226">випадковою, а не закономірною»</text>
  <text x="50" y="295" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Потрібно перевіряти статистичну</text>
  <text x="50" y="312" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">значущість відмінностей</text>

  <rect x="390" y="200" width="340" height="130" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="1.5"/>
  <text x="410" y="227" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">4. Упереджене «підтвердження»</text>
  <text x="410" y="250" font-family="Arial" font-size="10.5" fill="#a93226">«Дослідник добирає лише ті дані,</text>
  <text x="410" y="267" font-family="Arial" font-size="10.5" fill="#a93226">що підтверджують його гіпотезу»</text>
  <text x="410" y="295" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">Порушує принцип наукової</text>
  <text x="410" y="312" font-family="Arial" font-size="10.5" font-style="italic" fill="#c0392b">об'єктивності</text>
</svg>
'''

SVG_CYCLE = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 380" width="700" height="380">
  <rect width="700" height="380" fill="#ffffff"/>
  <text x="350" y="26" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#1e3a5f">Цикл «результат → інтерпретація → теорія»</text>

  <circle cx="350" cy="205" r="130" fill="none" stroke="#e2e8f0" stroke-width="2" stroke-dasharray="6 4"/>

  <rect x="240" y="70" width="220" height="55" rx="10" fill="#eaf4fc" stroke="#2980b9" stroke-width="2"/>
  <text x="350" y="92" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e3a5f">РЕЗУЛЬТАТИ</text>
  <text x="350" y="112" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#2980b9">емпіричні дані дослідження</text>

  <rect x="490" y="180" width="190" height="55" rx="10" fill="#e8f6f3" stroke="#27ae60" stroke-width="2"/>
  <text x="585" y="202" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#1e5a3f">ІНТЕРПРЕТАЦІЯ</text>
  <text x="585" y="222" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#27ae60">пояснення, порівняння</text>

  <rect x="490" y="300" width="190" height="55" rx="10" fill="#fef9e7" stroke="#e67e22" stroke-width="2"/>
  <text x="585" y="322" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7e5109">ТЕОРІЯ</text>
  <text x="585" y="342" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#e67e22">існуючі концепції</text>

  <rect x="20" y="300" width="190" height="55" rx="10" fill="#f4ecf7" stroke="#8e44ad" stroke-width="2"/>
  <text x="115" y="322" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#4a235a">НОВЕ ЗНАННЯ</text>
  <text x="115" y="342" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#8e44ad">уточнення / доповнення</text>

  <rect x="20" y="180" width="190" height="55" rx="10" fill="#fdedec" stroke="#c0392b" stroke-width="2"/>
  <text x="115" y="202" text-anchor="middle" font-family="Arial" font-size="12.5" font-weight="bold" fill="#7b241c">НОВА ГІПОТЕЗА</text>
  <text x="115" y="222" text-anchor="middle" font-family="Arial" font-size="10.5" fill="#c0392b">для наступних досліджень</text>

  <defs>
    <marker id="arrLoop" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/>
    </marker>
  </defs>

  <path d="M462,102 Q580,110 585,178" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrLoop)"/>
  <path d="M585,237 L585,298" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrLoop)"/>
  <path d="M488,327 Q350,360 210,327" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrLoop)"/>
  <path d="M115,298 L115,237" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrLoop)"/>
  <path d="M210,207 Q280,140 240,100" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrLoop)"/>
</svg>
'''

SVG_EXAMPLE_CHART = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 380" width="760" height="380">
  <rect width="760" height="380" fill="#ffffff"/>
  <text x="380" y="24" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#1e3a5f">Приклад для інтерпретації: рівні сформованості до і після формувального етапу</text>

  <line x1="90" y1="60" x2="90" y2="300" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="90" y1="300" x2="700" y2="300" stroke="#94a3b8" stroke-width="1.5"/>

  <line x1="90" y1="240" x2="700" y2="240" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="90" y1="180" x2="700" y2="180" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="90" y1="120" x2="700" y2="120" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="90" y1="60" x2="700" y2="60" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>

  <text x="80" y="304" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">0%</text>
  <text x="80" y="244" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">25%</text>
  <text x="80" y="184" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">50%</text>
  <text x="80" y="124" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">75%</text>
  <text x="80" y="64" text-anchor="end" font-family="Arial" font-size="11" fill="#64748b">100%</text>

  <text x="200" y="322" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Високий</text>
  <text x="380" y="322" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Середній</text>
  <text x="560" y="322" text-anchor="middle" font-family="Arial" font-size="11.5" fill="#1e3a5f">Низький</text>

  <!-- До -->
  <rect x="150" y="252" width="35" height="48" fill="#c0392b"/>
  <text x="167" y="246" text-anchor="middle" font-family="Arial" font-size="10" fill="#c0392b" font-weight="bold">20%</text>

  <rect x="330" y="192" width="35" height="108" fill="#c0392b"/>
  <text x="347" y="186" text-anchor="middle" font-family="Arial" font-size="10" fill="#c0392b" font-weight="bold">45%</text>

  <rect x="510" y="216" width="35" height="84" fill="#c0392b"/>
  <text x="527" y="210" text-anchor="middle" font-family="Arial" font-size="10" fill="#c0392b" font-weight="bold">35%</text>

  <!-- Після -->
  <rect x="190" y="192" width="35" height="108" fill="#27ae60"/>
  <text x="207" y="186" text-anchor="middle" font-family="Arial" font-size="10" fill="#27ae60" font-weight="bold">45%</text>

  <rect x="370" y="204" width="35" height="96" fill="#27ae60"/>
  <text x="387" y="198" text-anchor="middle" font-family="Arial" font-size="10" fill="#27ae60" font-weight="bold">40%</text>

  <rect x="550" y="276" width="35" height="24" fill="#27ae60"/>
  <text x="567" y="270" text-anchor="middle" font-family="Arial" font-size="10" fill="#27ae60" font-weight="bold">15%</text>

  <rect x="620" y="85" width="14" height="14" rx="2" fill="#c0392b"/>
  <text x="640" y="97" font-family="Arial" font-size="10.5" fill="#1e3a5f">до</text>
  <rect x="670" y="85" width="14" height="14" rx="2" fill="#27ae60"/>
  <text x="690" y="97" font-family="Arial" font-size="10.5" fill="#1e3a5f">після</text>

  <text x="380" y="355" text-anchor="middle" font-family="Arial" font-size="11.5" font-style="italic" fill="#475569">Завдання для інтерпретації: що змінилося? Які причини? Як це співвідноситься з теорією?</text>
</svg>
'''


# ============================================================
# 4. ЗМІСТ ДОКУМЕНТА
# ============================================================

def build_document():
    doc = setup_document()

    # ---------- Титульна частина ----------
    add_title(doc, "ЛЕКЦІЙНЕ ЗАНЯТТЯ № 11", size=16, space_after=4)
    add_title(doc,
              "Інтерпретація результатів. Пояснення отриманих даних, "
              "порівняння з існуючими теоріями",
              size=15, space_after=10)
    add_title(doc, "Дисципліна: Основи науково-педагогічних досліджень",
              size=13, bold=False, space_after=2)
    add_title(doc, "Спеціальність: Початкова освіта", size=13, bold=False, space_after=12)

    # ---------- Мета ----------
    add_heading(doc, "Мета та завдання")
    add_paragraph(doc,
        "Мета: формувати вміння інтерпретувати результати педагогічного дослідження, "
        "пояснювати отримані дані та порівнювати їх з існуючими теоріями; розвивати "
        "аналітичне мислення та здатність співвідносити результати з теорією; "
        "виховувати наукову об'єктивність і критичність в інтерпретації результатів.")
    add_paragraph(doc,
        "Завдання: опанувати етапи інтерпретації результатів; навчитися розрізняти опис, "
        "пояснення та порівняння даних; виявляти типові помилки інтерпретації; "
        "формувати вміння співвідносити власні результати з теорією.")
    add_paragraph(doc, "Обладнання: інструкційні картки, мультимедійна презентація.")

    # ---------- Література ----------
    add_heading(doc, "Література")
    add_numbered(doc, "Сисоєва С. О., Кристопчук Т. Є. Методологія науково-педагогічних "
                      "досліджень. Рівне: Волинські обереги, 2013. 360 с.")
    add_numbered(doc, "Методичні рекомендації щодо написання та оформлення курсової роботи. "
                      "Путивль: КЗСОР «Путивльський педагогічний фаховий коледж "
                      "імені С. В. Руднєва», 2024. 14 с.")

    # ---------- 1. Сутність ----------
    add_heading(doc, "1. Сутність інтерпретації результатів")
    add_paragraph(doc,
        "Інтерпретація — це тлумачення результатів дослідження, розкриття їхнього "
        "змісту та значення. Якщо первинна обробка відповідає на питання «що отримано?», "
        "то інтерпретація відповідає на питання «що це означає і чому саме так?».")
    add_paragraph(doc,
        "Інтерпретація результатів є перехідною ланкою між емпіричною частиною "
        "дослідження та теоретичними висновками. Вона дає змогу не лише зафіксувати "
        "факти, а й пояснити їх, співвіднести з науковими теоріями та сформулювати "
        "практичні рекомендації.")
    add_svg_image(doc, SVG_INTERPRETATION_STAGES, width_cm=16,
                  caption="Рис. 1. Етапи інтерпретації результатів дослідження")

    add_paragraph(doc,
        "Інтерпретація має бути науково обґрунтованою, об'єктивною та критичною. "
        "Дослідник не повинен підганяти результати під власну гіпотезу — навпаки, "
        "він має чесно визнати, якщо результати її не підтверджують.")

    # ---------- 2. Етапи ----------
    add_heading(doc, "2. Основні етапи інтерпретації")
    add_table(doc,
        headers=["Етап", "Зміст", "Ключове питання"],
        rows=[
            ["Опис", "Фіксація того, що показали дані: числові показники, тенденції, "
                     "відмінності між групами", "Що отримано?"],
            ["Пояснення", "Встановлення причин отриманих результатів, механізмів "
                          "впливу, чинників", "Чому саме так?"],
            ["Порівняння", "Співвіднесення результатів з існуючими теоріями та "
                           "дослідженнями інших авторів", "Як це узгоджується з теорією?"],
            ["Узагальнення", "Формулювання закономірностей, висновків, "
                             "практичних рекомендацій", "Що це означає для практики?"],
            ["Висновки", "Підсумок дослідження, підтвердження або спростування гіпотези",
             "Чи досягнуто мету?"],
        ],
        col_widths=[3.0, 8.0, 5.5])
    add_paragraph(doc, "Таблиця 1. Етапи інтерпретації результатів", italic=True,
                  indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------- 3. Порівняння з теорією ----------
    add_heading(doc, "3. Порівняння результатів з існуючими теоріями")
    add_paragraph(doc,
        "Порівняння результатів з теорією — важливий етап інтерпретації. Воно дає змогу "
        "з'ясувати, чи узгоджуються результати з відомими науковими положеннями, "
        "чи доповнюють їх, чи суперечать їм.")
    add_svg_image(doc, SVG_COMPARISON_THEORY, width_cm=15,
                  caption="Рис. 2. Три можливі результати порівняння з теорією")

    add_heading(doc, "3.1. Алгоритм порівняння з теорією", level=2)
    add_numbered(doc, "Визначте ключові теоретичні положення, дотичні до вашого дослідження.")
    add_numbered(doc, "Співвіднесіть кожен отриманий результат із цими положеннями.")
    add_numbered(doc, "Зафіксуйте, що підтверджується, що уточнюється, а що суперечить.")
    add_numbered(doc, "Поясніть причини розбіжностей (вік, умови, вибірка, методики).")
    add_numbered(doc, "Сформулюйте внесок вашого дослідження в теорію та практику.")

    # ---------- 4. Типові помилки ----------
    add_heading(doc, "4. Типові помилки інтерпретації результатів")
    add_svg_image(doc, SVG_ERRORS, width_cm=16,
                  caption="Рис. 3. Типові помилки інтерпретації результатів")

    add_paragraph(doc,
        "Уникати цих помилок допомагає критичне ставлення до власних результатів, "
        "перевірка статистичної значущості, врахування обмежень вибірки та "
        "об'єктивне висвітлення всіх даних, а не лише тих, що підтверджують гіпотезу.")

    # ---------- 5. Цикл ----------
    add_heading(doc, "5. Цикл «результат → інтерпретація → теорія»")
    add_paragraph(doc,
        "Наукове пізнання — це циклічний процес. Отримані результати інтерпретуються "
        "в контексті теорії, внаслідок чого народжується нове знання або нова гіпотеза, "
        "яка знову потребує емпіричної перевірки.")
    add_svg_image(doc, SVG_CYCLE, width_cm=14,
                  caption="Рис. 4. Цикл «результат → інтерпретація → теорія»")

    # ---------- 6. Приклад ----------
    add_heading(doc, "6. Приклад інтерпретації результатів")
    add_paragraph(doc,
        "Розглянемо приклад. На констатувальному етапі високий рівень сформованості "
        "певного явища мали 20 % учнів, середній — 45 %, низький — 35 %. Після "
        "формувального етапу високий рівень зріс до 45 %, середній знизився до 40 %, "
        "низький — до 15 %.")
    add_svg_image(doc, SVG_EXAMPLE_CHART, width_cm=15,
                  caption="Рис. 5. Приклад для інтерпретації: рівні до і після формувального етапу")

    add_heading(doc, "6.1. Зразок інтерпретації", level=2)
    add_paragraph(doc, "Опис:", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Після формувального етапу високий рівень сформованості зріс із 20 % до 45 %, "
        "низький знизився з 35 % до 15 %.")
    add_paragraph(doc, "Пояснення:", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Зростання високого рівня можна пояснити систематичним використанням "
        "авторської методики, яка активізує пізнавальну діяльність учнів і "
        "враховує вікові особливості молодших школярів.")
    add_paragraph(doc, "Порівняння з теорією:", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Отримані результати узгоджуються з теорією розвивального навчання, згідно "
        "з якою активна діяльність учня є провідною умовою розвитку. Вони також "
        "доповнюють дослідження [автор], який наголошував на ролі мотивації.")
    add_paragraph(doc, "Висновок:", bold=True, indent=False, space_after=2)
    add_paragraph(doc,
        "Результати свідчать про ефективність запропонованої методики та "
        "підтверджують висунуту гіпотезу.")

    # ---------- Контрольні запитання ----------
    add_heading(doc, "Контрольні запитання")
    add_numbered(doc, "Що таке інтерпретація результатів дослідження і чим вона "
                      "відрізняється від первинної обробки даних?")
    add_numbered(doc, "Назвіть основні етапи інтерпретації результатів і схарактеризуйте "
                      "кожен із них.")
    add_numbered(doc, "Чому етап пояснення є ключовим для розуміння отриманих даних?")
    add_numbered(doc, "Які три можливі результати порівняння власних даних з існуючою теорією?")
    add_numbered(doc, "Наведіть алгоритм порівняння результатів дослідження з теоретичними "
                      "положеннями.")
    add_numbered(doc, "Назвіть типові помилки інтерпретації результатів. Як їх уникнути?")
    add_numbered(doc, "Чому не можна робити висновок про причинність лише на основі "
                      "кореляції показників?")
    add_numbered(doc, "У чому полягає небезпека надмірного узагальнення результатів "
                      "дослідження на одній вибірці?")
    add_numbered(doc, "Як цикл «результат → інтерпретація → теорія» відображає "
                      "наукове пізнання?")
    add_numbered(doc, "Сформулюйте вимоги до наукової об'єктивності в інтерпретації "
                      "результатів педагогічного дослідження.")

    # ---------- Файл ----------
    output = "Lecture11_Interpretatsiia.docx"
    doc.save(output)
    print(f"✅ Документ створено: {output}")


if __name__ == "__main__":
    build_document()