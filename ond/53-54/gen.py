# -*- coding: utf-8 -*-
"""
Генерація методичного матеріалу:
Самостійна робота № 7. Етика наукових досліджень.
Науково-педагогічне дослідження в контексті інклюзивної освіти.
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


# -------- Схема 1: Етичні принципи (2×2) --------
def schema_principles():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 96, "Етичні принципи науково-педагогічного дослідження",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    principles = [
        ("Честність", ["правдиве подання", "результатів і даних"], A_BLUE),
        ("Повага до особистості", ["добровільна участь,", "інформована згода"], A_GREEN),
        ("Прозорість", ["відкриті методи", "та процедури"], A_ORANGE),
        ("Відповідальність", ["за наслідки", "і вплив на дітей"], A_PURPLE),
    ]
    positions = [
        (6, 50, 41, 36), (53, 50, 41, 36),
        (6, 8, 41, 36),  (53, 8, 41, 36),
    ]
    for (title, lines, color), (x, y, w, h) in zip(principles, positions):
        _card(ax, x, y, w, h, title, lines, accent=color, title_size=14, line_size=12)
    return _save(fig, "s1_principles")


# -------- Схема 2: Тріада етики інклюзивного дослідження --------
def schema_triad():
    fig, ax = plt.subplots(figsize=(11, 5.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 92, "Етика інклюзивного дослідження: три виміри",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    items = [
        ("Доступність", ["матеріали й форми", "зрозумілі всім дітям"], A_BLUE),
        ("Повага до різноманіття", ["врахування особливих", "освітніх потреб"], A_GREEN),
        ("Конфіденційність", ["захист персональних", "даних учасників"], A_PURPLE),
    ]
    w, h, y = 30, 58, 14
    for i, (title, lines, color) in enumerate(items):
        x = 3 + i * 32
        _card(ax, x, y, w, h, title, lines, accent=color, title_size=14, line_size=12)
    return _save(fig, "s2_triad")


# -------- Схема 3: Етапи самостійної роботи (флоу) --------
def schema_steps():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 92, "Етапи виконання самостійної роботи",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    steps = [
        ("1", "Опрацювання\nджерел", A_BLUE),
        ("2", "Складання\nплану", A_GREEN),
        ("3", "Написання\nповідомлення", A_ORANGE),
        ("4", "Оформлення\nзвіту", A_PURPLE),
        ("5", "Презентація\nі захист", A_RED),
    ]
    n = len(steps)
    w, h, gap = 16.5, 48, 3.5
    total_w = n * w + (n - 1) * gap
    start_x = (100 - total_w) / 2
    y = 18

    for i, (num, label, color) in enumerate(steps):
        x = start_x + i * (w + gap)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=2.0",
                             linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
        ax.add_patch(box)
        circ = Circle((x + w / 2, y + h - 9), 4.5,
                      facecolor=color, edgecolor="none")
        ax.add_patch(circ)
        ax.text(x + w / 2, y + h - 9, num, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color="white")
        ax.text(x + w / 2, y + h / 2 - 6, label, ha="center", va="center",
                fontsize=11.5, color=T_DARK, linespacing=1.35)
        if i < n - 1:
            ax.annotate("", xy=(x + w + gap - 0.4, y + h / 2),
                        xytext=(x + w + 0.4, y + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=T_GRAY, lw=1.6))
    return _save(fig, "s3_steps")


# -------- Схема 4: Структура повідомлення --------
def schema_structure():
    fig, ax = plt.subplots(figsize=(10, 6.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 95, "Структура повідомлення",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    items = [
        ("Вступ", "актуальність теми, мета й завдання", A_BLUE),
        ("Теоретична частина", "етичні принципи, нормативна база", A_GREEN),
        ("Практичні приклади", "кейси з інклюзивної практики", A_ORANGE),
        ("Висновки та джерела", "узагальнення, список літератури", A_PURPLE),
    ]
    w, h, gap, x = 76, 14, 3.5, 12
    y_start = 72
    for i, (title, body, color) in enumerate(items):
        y = y_start - i * (h + gap)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=1.8",
                             linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
        ax.add_patch(box)
        bar = FancyBboxPatch((x + 1.6, y + 1.6), 1.6, h - 3.2,
                             boxstyle="round,pad=0,rounding_size=0.7",
                             linewidth=0, facecolor=color)
        ax.add_patch(bar)
        ax.text(x + 5.5, y + h * 0.62, title, ha="left", va="center",
                fontsize=13.5, fontweight="bold", color=T_DARK)
        ax.text(x + 5.5, y + h * 0.30, body, ha="left", va="center",
                fontsize=11.5, color=T_GRAY)
    return _save(fig, "s4_structure")


print("Генерація схем...")
p1 = schema_principles()
p2 = schema_triad()
p3 = schema_steps()
p4 = schema_structure()
print("Схеми збережено в output/")


# ============================================================
#  ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ============================================================
H_COLOR = RGBColor(0x1F, 0x4E, 0x79)
SH_COLOR = RGBColor(0x2E, 0x75, 0xB6)
MONO_COLOR = RGBColor(0xC0, 0x39, 0x2B)


def set_font(run, size=14, bold=False, italic=False, color=None, mono=False):
    name = "Consolas" if mono else "Times New Roman"
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if mono:
        run.font.color.rgb = MONO_COLOR
    elif color is not None:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:ascii'), name)
    rfonts.set(qn('w:hAnsi'), name)
    rfonts.set(qn('w:eastAsia'), name)
    rfonts.set(qn('w:cs'), name)


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
add_title(doc, "САМОСТІЙНА РОБОТА № 7")
add_topic(
    doc,
    "Етика наукових досліджень. Науково-педагогічне дослідження "
    "в контексті інклюзивної освіти."
)

# --- Мета ---
add_heading(doc, "Мета")
add_para(
    doc,
    "Сформувати знання про етику наукових досліджень та особливості "
    "дослідження в контексті інклюзивної освіти; розвивати етичну чутливість "
    "і здатність враховувати особливі освітні потреби учасників дослідження; "
    "виховувати толерантність, інклюзивну культуру та повагу до різноманіття. "
    "Результат — підготовлене письмове повідомлення за обраною темою."
)

# --- Обладнання ---
add_heading(doc, "Обладнання та програмне забезпечення")
add_numbered_paren(doc, [
    "інструкційні картки (додаються);",
    "персональний комп'ютер або ноутбук;",
    "текстовий редактор (Microsoft Word, Google Docs, LibreOffice Writer);",
    "зошит для самостійних робіт та ручка.",
])

# --- Література ---
add_heading(doc, "Література")
add_list_number(doc, [
    "Тушева В. В. Основи наукових досліджень. Харків : «Федорко», 2014. 408 с.",
    "Методичні рекомендації щодо написання та оформлення курсової роботи. "
    "Путивль : КЗСОР «Путивльський педагогічний фаховий коледж "
    "імені С. В. Руднєва», 2024. 14 с.",
    "Виховувати толерантність, інклюзивну культуру та повагу до різноманіття : "
    "методичні матеріали. [Б. м. : б. в.], [б. р.].",
])

# --- Завдання ---
add_heading(doc, "Завдання самостійної роботи")
add_numbered_manual(doc, [
    "Опрацювати джерела з питань етики наукових досліджень та особливостей "
    "дослідницької діяльності в умовах інклюзивної освіти.",
    "Підготувати письмове повідомлення (обсяг 3–4 сторінки) за однією "
    "з тем, запропонованих у переліку опрацьовуваних питань.",
    "Сформулювати 3–5 етичних правил, яких має дотримуватися дослідник "
    "під час роботи з дітьми з особливими освітніми потребами.",
    "Презентувати повідомлення на практичному занятті (5–7 хв) та взяти "
    "участь в обговоренні.",
])

# --- Терміни ---
add_heading(doc, "Терміни виконання")
add_para(
    doc,
    "Два тижні з дати видачі завдання. Захист повідомлення — на наступному "
    "практичному занятті згідно з розкладом. Роботи, подані з порушенням "
    "термінів без поважної причини, оцінюються зі зниженням балів."
)

# --- Очікувані результати ---
add_heading(doc, "Очікувані результати")
for item in [
    "знання основних етичних принципів науково-педагогічного дослідження;",
    "розуміння специфіки дослідницької діяльності в інклюзивному освітньому середовищі;",
    "уміння враховувати особливі освітні потреби учасників дослідження;",
    "сформована етична чутливість та інклюзивна культура майбутнього вчителя;",
    "навички оформлення та публічної презентації результатів самостійної роботи.",
]:
    add_bullet(doc, item)

# --- Перелік питань ---
add_heading(doc, "Перелік опрацьовуваних питань")
add_numbered_manual(doc, [
    "Сутність і значення етики наукових досліджень у педагогіці.",
    "Основні етичні принципи дослідника: чесність, повага, прозорість, "
    "відповідальність.",
    "Особливості проведення науково-педагогічного дослідження в умовах "
    "інклюзивної освіти.",
    "Етичні норми роботи з дітьми з особливими освітніми потребами "
    "та їхніми родинами.",
])

# --- Теоретичні відомості ---
add_heading(doc, "Теоретичні відомості (стислий огляд)")

add_subheading(doc, "1. Поняття етики наукових досліджень")
add_para(
    doc,
    "Етика наукових досліджень — це сукупність моральних норм і принципів, "
    "що регулюють діяльність дослідника на всіх етапах наукової роботи: "
    "від постановки проблеми до оприлюднення результатів. Дотримання цих "
    "норм забезпечує достовірність наукових даних та захищає права "
    "учасників дослідження."
)

add_subheading(doc, "2. Основні етичні принципи дослідника")
add_para(
    doc,
    "До базових принципів належать чесність і об'єктивність у поданні "
    "результатів, повага до особистості учасників та їхня добровільна "
    "участь, прозорість методів дослідження, конфіденційність отриманих "
    "даних і відповідальність за наслідки дослідницьких дій."
)
add_picture_center(doc, p1, width_cm=15.5)
add_caption(doc, "Рис. 1. Етичні принципи науково-педагогічного дослідження")

add_subheading(doc, "3. Особливості дослідження в інклюзивній освіті")
add_para(
    doc,
    "Дослідження в інклюзивному освітньому середовищі передбачає адаптацію "
    "інструментарію з урахуванням особливих освітніх потреб дітей, "
    "забезпечення доступності матеріалів (шрифт, формат, мова), дотримання "
    "поваги до різноманіття та уникнення дискримінаційних формулювань, "
    "отримання згоди батьків або законних представників неповнолітніх "
    "учасників, коректне формулювання висновків без «навішування ярликів»."
)
add_picture_center(doc, p2, width_cm=15.5)
add_caption(doc, "Рис. 2. Три виміри етики інклюзивного дослідження")

add_callout(
    doc,
    "Пам'ятайте: персональні дані дітей з особливими освітніми потребами "
    "є конфіденційною інформацією. У звіті використовуйте лише узагальнені "
    "дані або ініціали; не вказуйте діагнозів, назв закладів і конкретних "
    "класів, якщо це дозволяє ідентифікувати дитину.",
    bg="FFF4E5", border="C93400",
)

add_subheading(doc, "4. Етичні норми роботи з дітьми з ООП")
add_para(
    doc,
    "Дослідник має враховувати індивідуальні можливості та стан дитини, "
    "не створювати для неї стресових ситуацій, забезпечувати право "
    "відмовитися від участі на будь-якому етапі, зберігати анонімність "
    "та захищати персональні дані, узгоджувати дії з педагогами "
    "й фахівцями психолого-педагогічного супроводу."
)

add_callout(
    doc,
    "Будь-яка участь дитини в дослідженні можлива лише за умови "
    "інформованої згоди батьків або законних представників. Сама дитина "
    "також має право сказати «ні» — і це «ні» дослідник зобов'язаний "
    "поважати без пояснень і без тиску.",
    bg="E8F5EC", border="248A3D",
)

# --- Етапи виконання ---
add_heading(doc, "Етапи виконання самостійної роботи")
add_picture_center(doc, p3, width_cm=16.0)
add_caption(doc, "Рис. 3. Схема-флоу етапів виконання самостійної роботи")
add_para(
    doc,
    "Кожен етап є обов'язковим. Пропуск етапу складання плану призводить "
    "до хаотичного викладу матеріалу, а пропуск етапу оформлення звіту — "
    "до зниження оцінки за формальними критеріями."
)

# --- Інструкційна картка ---
add_heading(doc, "Інструкційна картка практичного завдання")
add_para(
    doc,
    "Нижче наведено покроковий алгоритм виконання самостійної роботи. "
    "Орієнтовна тривалість — 100 хв самостійної роботи вдома або "
    "в аудиторії під керівництвом викладача."
)
inst_header = ["№", "Крок", "Зміст", "Час"]
inst_data = [
    ["1", "Вибір теми", "Обрати одну з тем повідомлення, узгодити з викладачем", "5 хв"],
    ["2", "Добір джерел", "Опрацювати 3–5 джерел, зробити виписки", "20 хв"],
    ["3", "Складання плану", "Визначити структуру повідомлення (вступ, 2–3 розділи, висновки)", "10 хв"],
    ["4", "Написання тексту", "Розкрити зміст за планом, додати приклади", "40 хв"],
    ["5", "Формулювання правил", "Сформулювати 3–5 етичних правил дослідника", "10 хв"],
    ["6", "Оформлення звіту", "Оформити згідно з вимогами, перевірити список джерел", "15 хв"],
]
t = doc.add_table(rows=1, cols=4)
for i, h in enumerate(inst_header):
    cell_text(t.rows[0].cells[i], h, size=13, bold=True,
              color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
for row in inst_data:
    cells = t.add_row().cells
    cell_text(cells[0], row[0], size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    cell_text(cells[1], row[1], size=12)
    cell_text(cells[2], row[2], size=12)
    cell_text(cells[3], row[3], size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
style_table(t, widths=[1.2, 3.5, 9.3, 2.5])
doc.add_paragraph()

# --- Таблиця для заповнення ---
add_heading(doc, "Завдання на заповнення таблиці")
add_para(
    doc,
    "Проаналізуйте наведені ситуації та заповніть таблицю: назвіть етичну "
    "норму, яку порушує або захищає ситуація, і запропонуйте коректні дії "
    "дослідника."
)
fill_header = ["Ситуація", "Етична норма", "Дії дослідника"]
fill_data = [
    ["Дитина з ООП відмовляється від участі в опитуванні",
     "", ""],
    ["Дослідник отримав персональні дані учасників",
     "", ""],
    ["Потрібно опублікувати результати дослідження",
     "", ""],
    ["До дослідження залучають неповнолітніх учнів",
     "", ""],
    ["У звіті потрібно навести приклад із життя дитини",
     "", ""],
]
t2 = doc.add_table(rows=1, cols=3)
for i, h in enumerate(fill_header):
    cell_text(t2.rows[0].cells[i], h, size=13, bold=True,
              color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
for row in fill_data:
    cells = t2.add_row().cells
    cell_text(cells[0], row[0], size=12)
    cell_text(cells[1], " ", size=12)
    cell_text(cells[2], " ", size=12)
style_table(t2, widths=[7.0, 4.5, 5.0])
for row in t2.rows[1:]:
    row.height = Cm(1.0)
doc.add_paragraph()

# --- Питання для самоперевірки ---
add_heading(doc, "Теоретичні питання для самоперевірки")
add_numbered_manual(doc, [
    "Що таке етика наукових досліджень? Які її основні принципи?",
    "Чому дотримання етичних норм є особливо важливим у дослідженнях з дітьми?",
    "Які особливості має дослідження в умовах інклюзивної освіти?",
    "Як забезпечити конфіденційність даних учасників дослідження?",
    "Наведіть приклади етично коректних і некоректних формулювань у висновках дослідження.",
])

# --- Рекомендації до оформлення ---
add_heading(doc, "Рекомендації до оформлення звіту")
for item in [
    "Обсяг — 3–4 сторінки друкованого тексту (Times New Roman, 14 pt, інтервал 1,15).",
    "Структура: титульна сторінка, план, вступ, основна частина, висновки, список джерел.",
    "Поля: ліве — 3 см, праве — 1,5 см, верхнє й нижнє — 2 см.",
    "Нумерація сторінок — у правому нижньому куті.",
    "Список джерел — не менше 3 позицій, оформлених згідно з вимогами.",
    "У звіті обов'язково навести 3–5 власних етичних правил дослідника.",
]:
    add_bullet(doc, item)

# --- Критерії оцінювання ---
add_heading(doc, "Критерії оцінювання")
crit_header = ["Критерій", "Бали"]
crit_data = [
    ["Повнота розкриття теми", "0–3"],
    ["Дотримання етичних принципів викладу", "0–2"],
    ["Наявність прикладів з інклюзивної практики", "0–2"],
    ["Власні етичні правила (3–5)", "0–2"],
    ["Оформлення звіту", "0–1"],
    ["Презентація та відповіді на питання", "0–2"],
    ["Разом", "0–12"],
]
t3 = doc.add_table(rows=1, cols=2)
for i, h in enumerate(crit_header):
    cell_text(t3.rows[0].cells[i], h, size=13, bold=True,
              color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
for row in crit_data:
    cells = t3.add_row().cells
    cell_text(cells[0], row[0], size=13)
    cell_text(cells[1], row[1], size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
style_table(t3, widths=[13.0, 3.5])
# виділення рядка «Разом»
last_row = t3.rows[-1]
for cell in last_row.cells:
    shade_cell(cell, "D9E2F3")
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.bold = True

# --- Збереження ---
OUT = "Samostiyna_robota_7_Etyka_naukovykh_doslidzhen.docx"
doc.save(OUT)
print(f"Готово! Файл збережено: {OUT}")
print("Схеми збережено в папку: output/")