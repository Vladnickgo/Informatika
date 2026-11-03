# -*- coding: utf-8 -*-
"""
Генерація методичного матеріалу:
Практичне заняття № 11. Впровадження наукових розробок
в освітній процес початкової школи.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs("output", exist_ok=True)

# ============================================================
#  НАЛАШТУВАННЯ СХЕМ (matplotlib) — стиль Apple
# ============================================================
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

C_BG = "#F5F5F7"
C_EDGE = "#E5E5EA"
T_DARK = "#1D1D1F"
T_GRAY = "#86868B"
A_BLUE = "#0071E3"
A_GREEN = "#248A3D"
A_ORANGE = "#C93400"
A_RED = "#C4001D"
A_PURPLE = "#6E30A8"


def _save(fig, name):
    png = os.path.join("output", f"{name}.png")
    svg = os.path.join("output", f"{name}.svg")
    fig.savefig(png, dpi=220, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(svg, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return png


def _card(ax, x, y, w, h, title, lines, accent, title_size=13.5, line_size=11.5):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0,rounding_size=2.0",
                         linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
    ax.add_patch(box)
    bar = FancyBboxPatch((x + 4, y + h - 5.0), w - 8, 1.1,
                         boxstyle="round,pad=0,rounding_size=0.55",
                         linewidth=0, facecolor=accent)
    ax.add_patch(bar)
    ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center",
            fontsize=title_size, fontweight="bold", color=T_DARK)
    if lines:
        ax.text(x + w / 2, y + h * 0.32, "\n".join(lines),
                ha="center", va="center", fontsize=line_size,
                color=T_GRAY, linespacing=1.45)


# -------- Схема 1: Форми впровадження (4 картки) --------
def schema_forms():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 92, "Форми впровадження наукових розробок",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    items = [
        ("Урок", ["оновлені методи", "і прийоми"], A_BLUE),
        ("Позакласна робота", ["гуртки, проєкти,", "свята"], A_GREEN),
        ("Методичне об'єднання", ["обмін досвідом", "між учителями"], A_ORANGE),
        ("Пілотний майданчик", ["експериментальна", "перевірка"], A_PURPLE),
    ]
    w, h, gap = 23.0, 58, 2.0
    total = 4 * w + 3 * gap
    x0 = (100 - total) / 2
    y = 14
    for i, (title, lines, color) in enumerate(items):
        x = x0 + i * (w + gap)
        _card(ax, x, y, w, h, title, lines, accent=color, title_size=12.5, line_size=11.5)
    return _save(fig, "pr1_forms")


# -------- Схема 2: Принципи адаптації (2×2) --------
def schema_adaptation():
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 96, "Принципи адаптації наукової розробки до початкової школи",
            ha="center", va="center", fontsize=14.5, fontweight="bold", color=T_DARK)

    items = [
        ("Віковідповідність", ["урахування віку", "молодших школярів"], A_BLUE),
        ("Доступність", ["зрозумілі інструкції,", "прості приклади"], A_GREEN),
        ("Поступовість", ["від простого", "до складного"], A_ORANGE),
        ("Підтримка", ["допомога вчителя", "та колег"], A_PURPLE),
    ]
    positions = [
        (6, 50, 41, 36), (53, 50, 41, 36),
        (6, 8, 41, 36),  (53, 8, 41, 36),
    ]
    for (title, lines, color), (x, y, w, h) in zip(items, positions):
        _card(ax, x, y, w, h, title, lines, accent=color, title_size=13.5, line_size=12)
    return _save(fig, "pr2_adaptation")


# -------- Схема 3: Флоу циклу впровадження (5 кроків) --------
def schema_flow():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 92, "Цикл впровадження наукової розробки",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    steps = [
        ("1", "Аналіз\nрозробки", A_BLUE),
        ("2", "Адаптація\nдо умов", A_GREEN),
        ("3", "Пілотне\nвпровадження", A_ORANGE),
        ("4", "Оцінка\nрезультатів", A_PURPLE),
        ("5", "Коригування\nй поширення", A_RED),
    ]
    n = len(steps)
    w, h, gap = 16.5, 48, 3.5
    total_w = n * w + (n - 1) * gap
    x0 = (100 - total_w) / 2
    y = 18
    for i, (num, label, color) in enumerate(steps):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=2.0",
                             linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
        ax.add_patch(box)
        circ = Circle((x + w / 2, y + h - 9), 4.5, facecolor=color, edgecolor="none")
        ax.add_patch(circ)
        ax.text(x + w / 2, y + h - 9, num, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color="white")
        ax.text(x + w / 2, y + h / 2 - 6, label, ha="center", va="center",
                fontsize=11.5, color=T_DARK, linespacing=1.35)
        if i < n - 1:
            ax.annotate("", xy=(x + w + gap - 0.4, y + h / 2),
                        xytext=(x + w + 0.4, y + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=T_GRAY, lw=1.6))
    return _save(fig, "pr3_flow")


# -------- Схема 4: Структура звіту --------
def schema_report():
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 95, "Структура звіту про впровадження",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    items = [
        ("Опис розробки", "що впроваджується, звідки взято", A_BLUE),
        ("Адаптація", "як пристосовано до початкової школи", A_GREEN),
        ("Хід впровадження", "етапи, тривалість, учасники", A_ORANGE),
        ("Результати й спостереження", "що змінилося, як реагували діти", A_PURPLE),
        ("Висновки й рекомендації", "що варто поширити, що доопрацювати", A_RED),
    ]
    w, h, gap, x = 78, 11, 3.0, 11
    y_start = 74
    for i, (title, body, color) in enumerate(items):
        y = y_start - i * (h + gap)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=1.6",
                             linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
        ax.add_patch(box)
        bar = FancyBboxPatch((x + 1.4, y + 1.4), 1.4, h - 2.8,
                             boxstyle="round,pad=0,rounding_size=0.6",
                             linewidth=0, facecolor=color)
        ax.add_patch(bar)
        ax.text(x + 4.6, y + h * 0.62, title, ha="left", va="center",
                fontsize=13, fontweight="bold", color=T_DARK)
        ax.text(x + 4.6, y + h * 0.28, body, ha="left", va="center",
                fontsize=10.5, color=T_GRAY)
    return _save(fig, "pr4_report")


print("Генерація схем...")
p1 = schema_forms()
p2 = schema_adaptation()
p3 = schema_flow()
p4 = schema_report()
print("Схеми збережено в output/")


# ============================================================
#  ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ============================================================
H_COLOR = RGBColor(0x1F, 0x4E, 0x79)
SH_COLOR = RGBColor(0x2E, 0x75, 0xB6)


def set_font(run, size=14, bold=False, italic=False, color=None):
    name = "Times New Roman"
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rfonts.set(qn(attr), name)


def set_default_style(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(14)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.space_after = Pt(4)
    rpr = st.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rfonts.set(qn(attr), "Times New Roman")


def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    set_font(p.add_run(text), size=14, bold=True, color=H_COLOR)


def add_topic(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    set_font(p.add_run(f"Тема: {text}"), size=14, bold=True)


def add_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(5)
    set_font(p.add_run(text), size=14, bold=True, color=H_COLOR)


def add_subheading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    set_font(p.add_run(text), size=14, bold=True, color=SH_COLOR)


def add_para(doc, text, indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if indent:
        p.paragraph_format.first_line_indent = Cm(1.0)
    set_font(p.add_run(text), size=14)


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_font(p.add_run(text), size=14)


def add_numbered_manual(doc, items):
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_font(p.add_run(f"{i}. {text}"), size=14)


def add_numbered_paren(doc, items):
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_font(p.add_run(f"{i}) {text}"), size=14)


def add_list_number(doc, items):
    for text in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_font(p.add_run(text), size=14)


def add_picture_center(doc, path, width_cm=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(3)
    p.add_run().add_picture(path, width=Cm(width_cm))


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    set_font(run, size=12, italic=True)
    run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)


def shade_cell(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def set_col_width(cell, width_cm):
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn('w:tcW'))
    if tcW is None:
        tcW = OxmlElement('w:tcW')
        tcPr.append(tcW)
    tcW.set(qn('w:w'), str(int(width_cm * 567)))
    tcW.set(qn('w:type'), 'dxa')


def cell_text(cell, text, size=13, bold=False, color=None,
              align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    set_font(p.add_run(text), size=size, bold=bold, color=color)


def style_table(table, widths=None):
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    hdr = table.rows[0]
    set_repeat_header(hdr)
    for cell in hdr.cells:
        shade_cell(cell, "1F4E79")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    if widths:
        for row in table.rows:
            for cell, w in zip(row.cells, widths):
                set_col_width(cell, w)


def add_callout(doc, text, bg="FFF4E5", border="C93400"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_col_width(cell, 16.5)

    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), bg)
    tcPr.append(shd)

    borders = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:color"), border)
    borders.append(left)
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    set_font(p.add_run(text), size=14)
    doc.add_paragraph()


def add_page_number_footer(doc):
    section = doc.sections[0]
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = "PAGE"
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    set_font(run, size=12)


# ============================================================
#  ФОРМУВАННЯ ДОКУМЕНТА
# ============================================================
doc = Document()
set_default_style(doc)
add_page_number_footer(doc)

# --- Заголовок і тема ---
add_title(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 11")
add_topic(
    doc,
    "Впровадження наукових розробок в освітній процес "
    "початкової школи."
)

# --- Мета ---
add_heading(doc, "Мета")
add_para(
    doc,
    "Формувати вміння впроваджувати наукові розробки в освітній процес "
    "початкової школи; розвивати здатність адаптувати наукові розробки "
    "до реальних умов початкової школи; виховувати відповідальність "
    "за практичне впровадження наукових результатів. Результат — "
    "виконані тестові завдання та підготовлений звіт."
)

# --- Обладнання ---
add_heading(doc, "Обладнання та програмне забезпечення")
add_numbered_paren(doc, [
    "інструкційні картки (додаються);",
    "персональний комп'ютер або ноутбук;",
    "текстовий редактор (Microsoft Word, Google Docs, LibreOffice Writer);",
    "мультимедійний проєктор або екран для презентації;",
    "зошит для практичних робіт та ручка.",
])

# --- Література ---
add_heading(doc, "Література")
add_list_number(doc, [
    "Лаппо В. В. Основи педагогічних досліджень. Івано-Франківськ : "
    "НАІР, 2016. 284 с.",
    "Сисоєва С. О., Кристопчук Т. Є. Методологія науково-педагогічних "
    "досліджень. Рівне : Волинські обереги, 2013. 360 с.",
    "Тушева В. В. Основи наукових досліджень. Харків : «Федорко», 2014. 408 с.",
])

# --- Теоретичні відомості ---
add_heading(doc, "Теоретичні відомості")

add_subheading(doc, "1. Сутність упровадження наукових розробок")
add_para(
    doc,
    "Упровадження наукових розробок — це процес перенесення результатів "
    "наукового дослідження (методик, технологій, дидактичних матеріалів, "
    "програм) у реальну освітню практику. На відміну від теоретичного "
    "дослідження, упровадження завжди має практичний результат: зміни "
    "в діяльності вчителя, у поведінці та навчальних досягненнях учнів. "
    "Без упровадження наукові результати залишаються «на папері»."
)

add_subheading(doc, "2. Форми впровадження")
add_para(
    doc,
    "У початковій школі впровадження найчастіше відбувається через урок "
    "(оновлені методи й прийоми), позакласну роботу (гуртки, проєкти, "
    "свята), роботу методичного об'єднання вчителів (обмін досвідом, "
    "майстер-класи) та через пілотний майданчик (експериментальна "
    "перевірка на базі одного класу чи школи)."
)
add_picture_center(doc, p1, width_cm=16.0)
add_caption(doc, "Рис. 1. Форми впровадження наукових розробок у початковій школі")

add_subheading(doc, "3. Принципи адаптації розробки")
add_para(
    doc,
    "Перед упровадженням наукову розробку потрібно адаптувати до умов "
    "початкової школи: врахувати вікові особливості молодших школярів "
    "(віковідповідність), спростити інструкції й приклади (доступність), "
    "вибудувати поступове ускладнення (поступовість) та забезпечити "
    "підтримку з боку вчителя і колег. Адаптація — не «спрощення», "
    "а збереження суті розробки в доступній для дитини формі."
)
add_picture_center(doc, p2, width_cm=15.5)
add_caption(doc, "Рис. 2. Принципи адаптації наукової розробки до початкової школи")

add_subheading(doc, "4. Цикл упровадження")
add_para(
    doc,
    "Упровадження — це циклічний процес: аналіз розробки → адаптація "
    "до конкретних умов → пілотне впровадження (у невеликій групі) → "
    "оцінка результатів → коригування й поширення. Після поширення "
    "цикл може повторюватися вже в нових умовах (інша школа, інший клас)."
)
add_picture_center(doc, p3, width_cm=16.0)
add_caption(doc, "Рис. 3. Цикл упровадження наукової розробки")

add_callout(
    doc,
    "Впровадження — це відповідальність. Якщо наукова розробка адаптована "
    "некоректно, це може нашкодити дітям: знизити мотивацію, "
    "спричинити стрес, сформувати хибні уявлення. Тому перед "
    "упровадженням обов'язково проводиться пілотний етап у невеликій "
    "групі й консультація з науковим керівником або методистом.",
    bg="FFF4E5", border="C93400",
)

add_callout(
    doc,
    "Пілотний етап — не формальність. Саме на ньому виявляються "
    "«слабкі місця» розробки: занадто складні інструкції, "
    "недостатньо часу, незрозумілі дітям приклади. Після пілоту "
    "розробка обов'язково коригується, і лише потім її можна "
    "поширювати на інші класи.",
    bg="E8F5EC", border="248A3D",
)

# --- Покроковий алгоритм ---
add_heading(doc, "Покроковий алгоритм виконання різнорівневих завдань")
add_para(
    doc,
    "Загальна тривалість практичної частини — 25–30 хв. Завдання "
    "виконуються послідовно. Орієнтовний розподіл часу: рівень 1 "
    "(тестові завдання) — 7–8 хв, рівень 2 — 9–10 хв, рівень 3 — 10–12 хв."
)

add_subheading(doc, "Рівень 1. Тестові завдання (7–8 хв)")
add_para(doc, "Оберіть одну правильну відповідь для кожного запитання.")
tests = [
    "Що таке впровадження наукових розробок? "
    "а) підготовка наукової статті; "
    "б) перенесення результатів дослідження в освітню практику; "
    "в) захист дисертації; г) рецензування посібника.",
    "Яка з форм упровадження є найпоширенішою в початковій школі? "
    "а) урок; б) наукова конференція; в) симпозіум; г) захист проєкту.",
    "Що передує безпосередньому впровадженню розробки? "
    "а) публікація монографії; б) пілотне впровадження; "
    "в) захист кваліфікаційної роботи; г) звіт перед громадою.",
    "Який принцип адаптації передбачає врахування віку молодших школярів? "
    "а) поступовість; б) доступність; в) віковідповідність; г) підтримка.",
    "Що означає «поступовість» в адаптації розробки? "
    "а) спрощення всіх завдань; б) рух від простого до складного; "
    "в) виконання завдань у групі; г) швидке впровадження в усі класи.",
    "Хто є суб'єктом упровадження наукової розробки в школі? "
    "а) лише науковець; б) лише адміністрація школи; "
    "в) учитель, методист, адміністрація у співпраці; г) лише батьки.",
    "Що таке пілотне впровадження? "
    "а) масове впровадження в усі класи; б) експериментальна перевірка "
    "в невеликій групі; в) публікація статті; г) конкурсний захист.",
    "Чому важливо коригувати розробку після пілоту? "
    "а) щоб ускладнити завдання; б) щоб урахувати виявлені недоліки "
    "й адаптувати розробку до реальних умов; в) щоб скоротити обсяг; "
    "г) щоб формально виконати вимогу.",
]
add_numbered_manual(doc, tests)

add_subheading(doc, "Рівень 2. Практичні завдання (9–10 хв)")
add_numbered_manual(doc, [
    "Візьміть одну з відомих вам педагогічних технологій "
    "(наприклад, ігрові технології, проєктне навчання, "
    "технологію розвитку критичного мислення). Опишіть, "
    "як її можна адаптувати до учнів 2 класу (не менше 3 "
    "конкретних змін).",
    "Складіть короткий план пілотного впровадження цієї "
    "адаптованої розробки (3–5 кроків, із зазначенням "
    "тривалості).",
    "Визначте 2–3 показники, за якими ви будете оцінювати "
    "результати пілотного впровадження.",
])

add_subheading(doc, "Рівень 3. Творче завдання (10–12 хв)")
add_numbered_manual(doc, [
    "Уявіть, що ви впроваджуєте у своєму класі одну з наукових "
    "розробок (тема — за вашим вибором, узгоджена з викладачем). "
    "Підготуйте короткий усний виступ (1,5–2 хв) за структурою: "
    "що впроваджується — як адаптовано — очікувані результати — "
    "ризики й способи їх уникнути.",
    "Вислухайте виступ одногрупника та сформулюйте 1–2 "
    "уточнювальні запитання або одне конструктивне зауваження.",
    "Занотуйте у звіт 2–3 ризики, які ви будете враховувати "
    "під час реального впровадження.",
])

# --- Критерії оцінювання ---
add_heading(doc, "Критерії оцінювання")
crit_header = ["Критерій", "Бали"]
crit_data = [
    ["Виконання тестових завдань рівня 1", "0–2"],
    ["Виконання завдань рівня 2 (адаптація + план пілоту)", "0–4"],
    ["Виконання завдання рівня 3 (виступ + ризики)", "0–4"],
    ["Активна участь в обговоренні, конструктивні запитання", "0–2"],
    ["Разом", "0–12"],
]
t = doc.add_table(rows=1, cols=2)
for i, h in enumerate(crit_header):
    cell_text(t.rows[0].cells[i], h, size=13, bold=True,
              color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
for row in crit_data:
    cells = t.add_row().cells
    cell_text(cells[0], row[0], size=13)
    cell_text(cells[1], row[1], size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
style_table(t, widths=[13.0, 3.5])
last_row = t.rows[-1]
for cell in last_row.cells:
    shade_cell(cell, "D9E2F3")
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.bold = True
doc.add_paragraph()

# --- Форма звітності ---
add_heading(doc, "Форма звітності")
add_para(
    doc,
    "За результатами роботи студент готує письмовий звіт про впровадження "
    "адаптованої наукової розробки в освітній процес початкової школи. "
    "Звіт оформлюється в текстовому редакторі (docx або pdf) та подається "
    "викладачу в день заняття або на наступне заняття згідно з вимогами."
)
add_picture_center(doc, p4, width_cm=15.5)
add_caption(doc, "Рис. 4. Структура звіту про впровадження наукової розробки")

add_subheading(doc, "Вимоги до звіту")
for item in [
    "Обсяг — 2–3 сторінки друкованого тексту (Times New Roman, 14 pt, інтервал 1,15).",
    "Структура звіту — відповідно до рис. 4 (опис розробки, адаптація, "
    "хід упровадження, результати й спостереження, висновки).",
    "Обов'язковий елемент — короткий план пілотного впровадження (3–5 кроків).",
    "Обов'язковий елемент — 2–3 ризики впровадження та способи їх уникнення.",
    "Додатково — 2–3 слайди презентації виступу (за бажанням).",
    "Наприкінці — самооцінювальне резюме (2–3 речення): що вдалося, "
    "що потребує вдосконалення.",
]:
    add_bullet(doc, item)

# --- Збереження ---
OUT = "Praktychne_zanyattya_11_Vprovadzhennya_rozrobok.docx"
doc.save(OUT)
print(f"Готово! Файл збережено: {OUT}")
print("Схеми збережено в папку: output/")