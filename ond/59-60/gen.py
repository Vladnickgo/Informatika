# -*- coding: utf-8 -*-
"""
Генерація методичного матеріалу:
Самостійна робота № 8. Цифрові інструменти та онлайн-сервіси
для збору й обробки дослідницьких даних.
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


# -------- Схема 1: Категорії цифрових інструментів (2×2) --------
def schema_categories():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 96, "Категорії цифрових інструментів для дослідження",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    items = [
        ("Збір даних", ["опитування,", "тестування, анкети"], A_BLUE),
        ("Обробка даних", ["таблиці, статистика,", "кодування"], A_GREEN),
        ("Візуалізація", ["діаграми,", "інфографіка"], A_ORANGE),
        ("Зберігання та обмін", ["хмарні диски,", "спільний доступ"], A_PURPLE),
    ]
    positions = [
        (6, 50, 41, 36), (53, 50, 41, 36),
        (6, 8, 41, 36),  (53, 8, 41, 36),
    ]
    for (title, lines, color), (x, y, w, h) in zip(items, positions):
        _card(ax, x, y, w, h, title, lines, accent=color, title_size=14, line_size=12)
    return _save(fig, "c1_categories")


# -------- Схема 2: Приклади сервісів за призначенням (2×2) --------
def schema_examples():
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 96, "Приклади цифрових сервісів",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    items = [
        ("Google Forms / MS Forms", ["онлайн-опитування,", "автозбір відповідей"], A_BLUE),
        ("Excel / Google Sheets", ["таблиці, формули,", "зведені таблиці"], A_GREEN),
        ("Canva / Infogram", ["схеми,", "інфографіка"], A_ORANGE),
        ("Google Drive / OneDrive", ["спільне зберігання", "й обмін файлами"], A_PURPLE),
    ]
    positions = [
        (6, 50, 41, 36), (53, 50, 41, 36),
        (6, 8, 41, 36),  (53, 8, 41, 36),
    ]
    for (title, lines, color), (x, y, w, h) in zip(items, positions):
        _card(ax, x, y, w, h, title, lines, accent=color, title_size=12.5, line_size=11.5)
    return _save(fig, "c2_examples")


# -------- Схема 3: Флоу роботи з даними (5 кроків) --------
def schema_flow():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 92, "Робота з дослідницькими даними: покроково",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    steps = [
        ("1", "Планування\nінструментів", A_BLUE),
        ("2", "Збір\nданих", A_GREEN),
        ("3", "Обробка\nй аналіз", A_ORANGE),
        ("4", "Візуалізація\nрезультатів", A_PURPLE),
        ("5", "Збереження\nта архівування", A_RED),
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
    return _save(fig, "c3_flow")


# -------- Схема 4: Етичні принципи цифрового дослідника (4 картки) --------
def schema_ethics():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 92, "Етичні принципи цифрового дослідника",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    items = [
        ("Добровільність", ["участь за", "згодою"], A_BLUE),
        ("Анонімність", ["без персональних", "даних"], A_GREEN),
        ("Захист даних", ["паролі, доступ", "лише для команди"], A_ORANGE),
        ("Прозорість", ["відкритий опис", "методів"], A_PURPLE),
    ]
    w, h, gap = 23.0, 58, 2.0
    total = 4 * w + 3 * gap
    x0 = (100 - total) / 2
    y = 14
    for i, (title, lines, color) in enumerate(items):
        x = x0 + i * (w + gap)
        _card(ax, x, y, w, h, title, lines, accent=color, title_size=13, line_size=11.5)
    return _save(fig, "c4_ethics")


print("Генерація схем...")
c1 = schema_categories()
c2 = schema_examples()
c3 = schema_flow()
c4 = schema_ethics()
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
add_title(doc, "САМОСТІЙНА РОБОТА № 8")
add_topic(
    doc,
    "Цифрові інструменти та онлайн-сервіси для збору й обробки "
    "дослідницьких даних."
)

# --- Мета ---
add_heading(doc, "Мета")
add_para(
    doc,
    "Ознайомити з цифровими інструментами та онлайн-сервісами для збору "
    "й обробки дослідницьких даних; розвивати цифрову компетентність "
    "у дослідницькій діяльності; виховувати відповідальне та етичне "
    "використання цифрових інструментів. Результат — підготовлене "
    "письмове повідомлення за обраною темою."
)

# --- Обладнання ---
add_heading(doc, "Обладнання та програмне забезпечення")
add_numbered_paren(doc, [
    "інструкційні картки (додаються);",
    "персональний комп'ютер або ноутбук із доступом до мережі Інтернет;",
    "обліковий запис Google або Microsoft (для роботи з онлайн-сервісами);",
    "текстовий редактор (Microsoft Word, Google Docs, LibreOffice Writer);",
    "табличний процесор (Microsoft Excel, Google Sheets, LibreOffice Calc).",
])

# --- Література ---
add_heading(doc, "Література")
add_list_number(doc, [
    "Кравець Н. П. Основи наукових досліджень : навчальний посібник. "
    "Київ : Вид-во НПУ імені М. П. Драгоманова, 2020. 74 с.",
    "Пріма Р. М. Сучасна наукова стаття: технологія творчості. "
    "Науковий вісник. 2020. № 4 (408). С. 99–103.",
    "Тушева В. В. Основи наукових досліджень. Харків : «Федорко», 2014. 408 с.",
])

# --- Завдання ---
add_heading(doc, "Завдання самостійної роботи")
add_numbered_manual(doc, [
    "Опрацювати джерела з питань використання цифрових інструментів "
    "у науково-педагогічному дослідженні.",
    "Підготувати письмове повідомлення (обсяг 3–4 сторінки) про один "
    "цифровий інструмент або групу сервісів для збору й обробки "
    "дослідницьких даних.",
    "Продемонструвати практичний приклад: створити коротке онлайн-"
    "опитування (Google Forms / Microsoft Forms) та подати скріншот "
    "зведених результатів.",
    "Сформулювати 3–5 етичних правил роботи з персональними даними "
    "учасників дослідження в цифровому середовищі.",
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
    "знання основних категорій цифрових інструментів для дослідження;",
    "уміння обирати сервіси відповідно до мети й типу дослідницьких даних;",
    "практичні навички створення онлайн-опитувань та обробки їх результатів;",
    "сформована цифрова компетентність майбутнього вчителя початкової школи;",
    "усвідомлення етичної відповідальності за захист персональних даних учасників.",
]:
    add_bullet(doc, item)

# --- Перелік питань ---
add_heading(doc, "Перелік опрацьовуваних питань")
add_numbered_manual(doc, [
    "Поняття цифрових інструментів та їх роль у науково-педагогічному дослідженні.",
    "Категорії цифрових інструментів: збір, обробка, візуалізація, зберігання даних.",
    "Огляд популярних онлайн-сервісів (Google Forms, Microsoft Forms, "
    "Google Sheets, Microsoft Excel, Canva, Infogram).",
    "Етичні та правові аспекти використання цифрових інструментів у дослідженні "
    "з дітьми (захист персональних даних, анонімність, згода батьків).",
])

# --- Теоретичні відомості ---
add_heading(doc, "Теоретичні відомості (стислий огляд)")

add_subheading(doc, "1. Роль цифрових інструментів у дослідженні")
add_para(
    doc,
    "Сучасне науково-педагогічне дослідження важко уявити без цифрових "
    "інструментів: вони дозволяють швидко збирати великі обсяги даних, "
    "автоматично їх обробляти, візуалізувати результати та зберігати "
    "матеріали в захищеному середовищі. Водночас використання цифрових "
    "сервісів вимагає від дослідника цифрової грамотності й етичної "
    "відповідальності за долю персональних даних учасників."
)

add_subheading(doc, "2. Категорії цифрових інструментів")
add_para(
    doc,
    "Умовно цифрові інструменти для дослідження поділяються на чотири "
    "категорії: для збору даних (онлайн-форми, анкети, тестові платформи), "
    "для обробки (табличні процесори, статистичні пакети), для візуалізації "
    "(сервіси діаграм та інфографіки) та для зберігання й обміну (хмарні "
    "диски, спільні папки). Ефективне дослідження зазвичай поєднує "
    "інструменти з усіх чотирьох категорій."
)
add_picture_center(doc, c1, width_cm=15.5)
add_caption(doc, "Рис. 1. Категорії цифрових інструментів для дослідження")

add_subheading(doc, "3. Огляд популярних онлайн-сервісів")
add_para(
    doc,
    "Серед найзручніших для початківця сервісів — Google Forms і "
    "Microsoft Forms (створення опитувань, автоматичний збір відповідей "
    "у таблицю), Google Sheets і Microsoft Excel (обробка даних, "
    "формули, зведені таблиці, діаграми), Canva та Infogram "
    "(візуалізація результатів, проста інфографіка), Google Drive "
    "та OneDrive (спільне зберігання й обмін матеріалами). Усі вони "
    "мають безкоштовні версії, достатні для навчального дослідження."
)
add_picture_center(doc, c2, width_cm=15.5)
add_caption(doc, "Рис. 2. Приклади цифрових сервісів для різних етапів роботи")

add_subheading(doc, "4. Етика роботи з даними в цифровому середовищі")
add_para(
    doc,
    "Використання цифрових інструментів у дослідженні з дітьми вимагає "
    "особливої обережності: персональні дані мають збиратися лише "
    "в мінімально необхідному обсязі, зберігатися захищено (паролі, "
    "двофакторна автентифікація), оброблятися анонімно (без прізвищ "
    "і точних дат народження) та не публікуватися у відкритому доступі."
)
add_picture_center(doc, c4, width_cm=16.0)
add_caption(doc, "Рис. 3. Етичні принципи цифрового дослідника")

add_callout(
    doc,
    "Персональні дані учнів — це чутлива інформація. Не збирайте зайвого: "
    "якщо для дослідження достатньо року народження й класу, не питайте "
    "точну дату народження, адресу чи телефон. Використовуйте псевдоніми "
    "або коди учасників. Згода батьків обов'язкова.",
    bg="FFF4E5", border="C93400",
)

add_subheading(doc, "5. Перевірка сервісу перед використанням")
add_para(
    doc,
    "Перед тим як обрати онлайн-сервіс для дослідження, перевірте його "
    "політику конфіденційності: де зберігаються дані, чи передаються вони "
    "третім сторонам, чи можна видалити власні дані повністю, чи сервіс "
    "використовує рекламу. Для дослідження з неповнолітніми надавайте "
    "перевагу сервісам з прозорою політикою та серверами в ЄС або Україні."
)

add_callout(
    doc,
    "Безкоштовний сервіс — не означає безпечний. Багато «безкоштовних» "
    "онлайн-форм збирають дані на користь рекламних мереж. "
    "Перед початком роботи перевірте: чи є в налаштуваннях опція "
    "«не передавати дані третім сторонам», чи можна експортувати "
    "відповіді у файл і видалити їх із сервера.",
    bg="E8F5EC", border="248A3D",
)

# --- Етапи виконання ---
add_heading(doc, "Етапи виконання самостійної роботи")
add_picture_center(doc, c3, width_cm=16.0)
add_caption(doc, "Рис. 4. Схема-флоу роботи з дослідницькими даними")
add_para(
    doc,
    "Кожен етап обов'язковий. Пропуск етапу планування інструментів "
    "призводить до того, що зібрані дані неможливо обробити; пропуск "
    "етапу збереження й архівування — до втрати матеріалів і неможливості "
    "повторного аналізу."
)

# --- Інструкційна картка ---
add_heading(doc, "Інструкційна картка практичного завдання")
add_para(
    doc,
    "Нижче наведено покроковий алгоритм виконання практичної частини "
    "самостійної роботи (створення опитування та обробка результатів). "
    "Орієнтовна тривалість — 80–90 хв."
)
inst_header = ["№", "Крок", "Зміст", "Час"]
inst_data = [
    ["1", "Вибір сервісу", "Обрати Google Forms або Microsoft Forms", "5 хв"],
    ["2", "Створення форми", "Додати 5–7 запитань (закриті й відкриті)", "15 хв"],
    ["3", "Налаштування", "Увімкнути анонімність, обмежити збір даних", "10 хв"],
    ["4", "Тестування", "Пройти форму самостійно або з 2–3 одногрупниками", "10 хв"],
    ["5", "Обробка відповідей", "Експорт у Google Sheets або Excel", "20 хв"],
    ["6", "Візуалізація", "Побудувати 2–3 діаграми, оформити висновок", "15 хв"],
    ["7", "Оформлення звіту", "Додати скріншоти, описати результат", "10 хв"],
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
    "Проаналізуйте запропоновані ситуації та заповніть таблицю: "
    "визначте, який цифровий інструмент доречно використати та які "
    "етичні норми слід врахувати."
)
fill_header = ["Ситуація", "Доречний інструмент", "Етичні норми"]
fill_data = [
    ["Провести анонімне опитування учнів 3 класу",
     "", ""],
    ["Обробити 100 відповідей анкети батьків",
     "", ""],
    ["Показати результати дослідження на слайді",
     "", ""],
    ["Зберегти матеріали дослідження для повторного аналізу",
     "", ""],
    ["Поділитися даними з науковим керівником",
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
    "Які категорії цифрових інструментів використовують у науково-педагогічному дослідженні?",
    "Які онлайн-сервіси доцільно застосовувати для збору даних і чому?",
    "Як забезпечити анонімність учасників під час онлайн-опитування?",
    "Які етичні норми слід враховувати, працюючи з персональними даними дітей?",
    "Наведіть приклад ситуації, коли використання цифрового інструменту може бути неетичним.",
])

# --- Рекомендації до оформлення ---
add_heading(doc, "Рекомендації до оформлення звіту")
for item in [
    "Обсяг — 3–4 сторінки друкованого тексту (Times New Roman, 14 pt, інтервал 1,15).",
    "Структура: титул, вступ (актуальність, мета), основна частина, "
    "практична частина зі скріншотами, висновки, список джерел.",
    "Поля: ліве — 3 см, праве — 1,5 см, верхнє й нижнє — 2 см.",
    "Нумерація сторінок — у правому нижньому куті.",
    "Список джерел — не менше 3 позицій, оформлених згідно з вимогами.",
    "Скріншоти форми та діаграм — обов'язкові; підписи під рисунками.",
    "У звіті обов'язково навести 3–5 власних етичних правил цифрового дослідника.",
]:
    add_bullet(doc, item)

# --- Критерії оцінювання ---
add_heading(doc, "Критерії оцінювання")
crit_header = ["Критерій", "Бали"]
crit_data = [
    ["Повнота розкриття теми", "0–3"],
    ["Практична частина (створена форма, обробка, візуалізація)", "0–3"],
    ["Дотримання етичних норм у роботі з даними", "0–2"],
    ["Власні етичні правила (3–5)", "0–2"],
    ["Оформлення звіту та якість скріншотів", "0–1"],
    ["Презентація та відповіді на питання", "0–1"],
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
last_row = t3.rows[-1]
for cell in last_row.cells:
    shade_cell(cell, "D9E2F3")
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.bold = True

# --- Збереження ---
OUT = "Samostiyna_robota_8_Tsyfrovi_instrumenty.docx"
doc.save(OUT)
print(f"Готово! Файл збережено: {OUT}")
print("Схеми збережено в папку: output/")