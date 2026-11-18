# -*- coding: utf-8 -*-
"""
Лекція 13. Збирання та організація даних:
методи збору даних, табличне представлення даних.
Генерує docx-документ + схеми (PNG + SVG) у папці output/.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ----------------------------------------------------------------------------
# КОНСТАНТИ ОФОРМЛЕННЯ
# ----------------------------------------------------------------------------
OUT = "output"
os.makedirs(OUT, exist_ok=True)

C_CARD = "#F5F5F7"
C_BORDER = "#E5E5EA"
C_TEXT = "#1D1D1F"
C_GRAY = "#86868B"
C_BLUE = "#0071E3"
C_GREEN = "#248A3D"
C_ORANGE = "#C93400"
C_RED = "#C4001D"
C_PURPLE = "#6E30A8"

DARK_HEAD = RGBColor(0x1F, 0x4E, 0x79)
SUB_HEAD = RGBColor(0x2E, 0x75, 0xB6)
MONO_COLOR = RGBColor(0xC0, 0x39, 0x2B)

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


# ============================================================================
# 1. СХЕМИ (matplotlib)
# ============================================================================
def _save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220,
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(os.path.join(OUT, name + ".svg"),
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


def _card(ax, x, y, w, h, title, sub=None, accent=C_BLUE,
          fs_title=13.0, fs_sub=11.5):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0,rounding_size=0.18",
                         linewidth=1.4, edgecolor=C_BORDER,
                         facecolor=C_CARD, zorder=2)
    ax.add_patch(box)
    bar = FancyBboxPatch((x + 0.14, y + h - 0.17), w - 0.28, 0.09,
                         boxstyle="round,pad=0,rounding_size=0.045",
                         linewidth=0, facecolor=accent, zorder=3)
    ax.add_patch(bar)
    if sub:
        ax.text(x + w / 2, y + h / 2 + 0.14, title, ha="center", va="center",
                fontsize=fs_title, color=C_TEXT, fontweight="bold", zorder=4)
        ax.text(x + w / 2, y + h / 2 - 0.24, sub, ha="center", va="center",
                fontsize=fs_sub, color=C_GRAY, zorder=4)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=fs_title, color=C_TEXT, fontweight="bold", zorder=4)


# --- Схема 1. Методи збору даних -------------------------------------------
def scheme_methods():
    fig, ax = plt.subplots(figsize=(12.6, 3.9))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    ax.text(0.35, 4.55, "Методи збору даних", fontsize=15, fontweight="bold",
            color=C_TEXT, ha="left", va="center")

    items = [
        ("Спостереження", "бачу і фіксую", C_BLUE),
        ("Опитування", "питаю і слухаю", C_GREEN),
        ("Аналіз документів", "читаю і виписую", C_ORANGE),
        ("Експеримент", "перевіряю дослідом", C_PURPLE),
    ]
    w, h, gap = 3.55, 2.55, 0.45
    x, y = 0.35, 0.95
    for title, sub, accent in items:
        _card(ax, x, y, w, h, title, sub, accent=accent, fs_title=13.0, fs_sub=11.5)
        x += w + gap

    _save(fig, "01_metody_zboru_danyh")


# --- Схема 2. Шлях від ідеї до таблиці --------------------------------------
def scheme_flow():
    fig, ax = plt.subplots(figsize=(12.6, 3.6))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    ax.text(0.35, 4.15, "Шлях від ідеї до таблиці", fontsize=15,
            fontweight="bold", color=C_TEXT, ha="left", va="center")

    steps = [
        ("1. Мета", "що досліджую", C_BLUE),
        ("2. Метод", "як збираю", C_BLUE),
        ("3. Збір", "фіксую факти", C_BLUE),
        ("4. Групування", "упорядковую", C_BLUE),
        ("5. Таблиця", "подаю результат", C_GREEN),
    ]
    w, h, gap = 2.75, 2.35, 0.42
    x, y = 0.35, 0.85
    for i, (title, sub, accent) in enumerate(steps):
        _card(ax, x, y, w, h, title, sub, accent=accent, fs_title=12.0, fs_sub=11.0)
        if i < len(steps) - 1:
            ax.annotate("",
                        xy=(x + w + gap - 0.06, y + h / 2),
                        xytext=(x + w + 0.06, y + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.4))
        x += w + gap

    _save(fig, "02_alhorytm_uporyadkuvannya")


# --- Схема 3. Будова таблиці ------------------------------------------------
def scheme_table_structure():
    fig, ax = plt.subplots(figsize=(12.6, 5.6))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 9.4)
    ax.axis("off")

    ax.text(0.35, 8.9, "Будова таблиці", fontsize=15, fontweight="bold",
            color=C_TEXT, ha="left", va="center")

    x0, y_top = 0.6, 7.6
    col_w = [3.1, 1.75, 1.75, 1.75]
    row_h = [0.95, 0.85, 0.85, 0.85]
    headers = ["Клас", "Учнів", "Високий", "Середній"]
    body = [["1-А", "25", "7", "12"],
            ["2-Б", "27", "9", "11"],
            ["3-В", "24", "6", "10"]]

    # головка
    x = x0
    y = y_top - row_h[0]
    for j, head in enumerate(headers):
        ax.add_patch(Rectangle((x, y), col_w[j], row_h[0],
                               facecolor="#DCEBFB", edgecolor=C_BORDER, linewidth=1.2))
        ax.text(x + col_w[j] / 2, y + row_h[0] / 2, head, ha="center",
                va="center", fontsize=10.5, color="#1F4E79", fontweight="bold")
        x += col_w[j]

    # тіло
    yy = y
    for i, row in enumerate(body):
        yy -= row_h[i + 1]
        x = x0
        for j, val in enumerate(row):
            if j == 0:
                fill, tcol = "#DFF2E3", C_TEXT
            elif i == 1 and j == 2:
                fill, tcol = "#FDE7D8", C_ORANGE
            else:
                fill, tcol = "#FFFFFF", C_TEXT
            ax.add_patch(Rectangle((x, yy), col_w[j], row_h[i + 1],
                                   facecolor=fill, edgecolor=C_BORDER, linewidth=1.2))
            ax.text(x + col_w[j] / 2, yy + row_h[i + 1] / 2, val,
                    ha="center", va="center", fontsize=11, color=tcol)
            x += col_w[j]

    # легенда
    legend = [
        ("#DCEBFB", "#1F4E79", "Головка", "назви стовпців — ознаки"),
        ("#DFF2E3", C_GREEN, "Боковик", "назви рядків — об’єкти"),
        ("#FDE7D8", C_ORANGE, "Комірка", "одне значення на перетині"),
    ]
    lx, ly = 9.9, 7.1
    for fill, stroke, title, sub in legend:
        ax.add_patch(Rectangle((lx, ly), 0.55, 0.55, facecolor=fill,
                               edgecolor=stroke, linewidth=1.3))
        ax.text(lx + 0.85, ly + 0.38, title, ha="left", va="center",
                fontsize=12.5, fontweight="bold", color=C_TEXT)
        ax.text(lx + 0.85, ly + 0.05, sub, ha="left", va="center",
                fontsize=11, color=C_GRAY)
        ly -= 1.05

    ax.text(0.6, 3.35,
            "Таблиця = рядки × стовпці: кожне значення має свою адресу — рядок і стовпець.",
            fontsize=11.5, color=C_GRAY, ha="left", va="center")

    _save(fig, "03_budova_tablytsi")


# --- Схема 4. Види таблиць ---------------------------------------------------
def scheme_table_types():
    fig, ax = plt.subplots(figsize=(12.6, 3.9))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    ax.text(0.35, 4.55, "Види таблиць", fontsize=15, fontweight="bold",
            color=C_TEXT, ha="left", va="center")

    items = [
        ("Проста", "одна ознака", C_BLUE),
        ("Групова", "групи за однією ознакою", C_GREEN),
        ("Комбінаційна", "дві і більше ознак", C_PURPLE),
    ]
    w, h, gap = 4.6, 2.6, 0.6
    x, y = 0.6, 0.95
    for title, sub, accent in items:
        _card(ax, x, y, w, h, title, sub, accent=accent, fs_title=14.0, fs_sub=11.5)
        x += w + gap

    _save(fig, "04_vydy_tablyts")


# ============================================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ DOCX
# ============================================================================
def set_normal_style(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(14)
    rpr = st.element.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(attr), "Times New Roman")
    pf = st.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(5)
    pf.space_before = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def add_page_numbers(section):
    par = section.footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    f1 = OxmlElement("w:fldChar")
    f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = "PAGE"
    f2 = OxmlElement("w:fldChar")
    f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1)
    run._r.append(it)
    run._r.append(f2)


def _runs(par, parts, size=14):
    if isinstance(parts, str):
        parts = [(parts, "n")]
    for item in parts:
        if isinstance(item, str):
            text, kind = item, "n"
        else:
            text, kind = item
        r = par.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(size)
        if kind == "b":
            r.bold = True
        elif kind == "i":
            r.italic = True
        elif kind == "m":
            r.font.name = "Consolas"
            r.font.size = Pt(size - 1)
            r.font.color.rgb = MONO_COLOR

def add_para(doc, parts, size=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
             space_after=5, space_before=0):
    par = doc.add_paragraph()
    par.alignment = align
    par.paragraph_format.space_after = Pt(space_after)
    par.paragraph_format.space_before = Pt(space_before)
    par.paragraph_format.line_spacing = 1.15
    _runs(par, parts, size)
    return par


def h_main(doc, text):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_after = Pt(4)
    r = par.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.color.rgb = DARK_HEAD


def h_sub(doc, text, color=SUB_HEAD):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.LEFT
    par.paragraph_format.space_before = Pt(10)
    par.paragraph_format.space_after = Pt(4)
    r = par.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.color.rgb = color


def bullet(doc, parts, size=14):
    par = doc.add_paragraph(style="List Bullet")
    par.paragraph_format.left_indent = Cm(1.0)
    par.paragraph_format.space_after = Pt(3)
    par.paragraph_format.line_spacing = 1.15
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    _runs(par, parts, size)
    return par


def _set_num(par, num_id):
    pPr = par._p.get_or_add_pPr()
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    numId = OxmlElement("w:numId")
    numId.set(qn("w:val"), str(num_id))
    numPr.append(ilvl)
    numPr.append(numId)
    successors = (
        "w:suppressLineNumbers", "w:pBdr", "w:shd", "w:tabs",
        "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
        "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE",
        "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid",
        "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
        "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
        "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle",
        "w:rPr", "w:sectPr", "w:pPrChange",
    )
    pPr.insert_element_before(numPr, *successors)


def create_num(doc):
    numbering = doc.part.numbering_part.element
    abs_ids = [int(a.get(qn("w:abstractNumId")))
               for a in numbering.findall(qn("w:abstractNum"))]
    new_abs = (max(abs_ids) + 1) if abs_ids else 0

    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(new_abs))
    lvl = OxmlElement("w:lvl")
    lvl.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    fmt = OxmlElement("w:numFmt")
    fmt.set(qn("w:val"), "decimal")
    txt = OxmlElement("w:lvlText")
    txt.set(qn("w:val"), "%1.")
    jc = OxmlElement("w:lvlJc")
    jc.set(qn("w:val"), "left")
    pPr = OxmlElement("w:pPr")
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "567")
    ind.set(qn("w:hanging"), "284")
    pPr.append(ind)
    for el in (start, fmt, txt, jc, pPr):
        lvl.append(el)
    abstract.append(lvl)

    first_num = numbering.find(qn("w:num"))
    if first_num is not None:
        first_num.addprevious(abstract)
    else:
        numbering.append(abstract)

    num_ids = [int(n.get(qn("w:numId")))
               for n in numbering.findall(qn("w:num"))]
    new_num = (max(num_ids) + 1) if num_ids else 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(new_num))
    ref = OxmlElement("w:abstractNumId")
    ref.set(qn("w:val"), str(new_abs))
    num.append(ref)
    numbering.append(num)
    return new_num


def num_item(doc, parts, num_id, size=14):
    par = doc.add_paragraph()
    _set_num(par, num_id)
    par.paragraph_format.left_indent = Cm(1.0)
    par.paragraph_format.space_after = Pt(3)
    par.paragraph_format.line_spacing = 1.15
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    _runs(par, parts, size)
    return par


def numbered_paren(doc, items, size=14):
    for i, item in enumerate(items, 1):
        par = doc.add_paragraph()
        par.paragraph_format.left_indent = Cm(1.0)
        par.paragraph_format.first_line_indent = Cm(-0.6)
        par.paragraph_format.space_after = Pt(3)
        par.paragraph_format.line_spacing = 1.15
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = par.add_run("%d) " % i)
        r.font.name = "Times New Roman"
        r.font.size = Pt(size)
        if isinstance(item, str):
            item = [(item, "n")]
        _runs(par, item, size)


def _shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def add_table(doc, headers, rows, widths, font_size=12):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    for i, w in enumerate(widths):
        table.columns[i].width = Cm(w)

    hdr = table.rows[0]
    for i, head in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = Cm(widths[i])
        _shade(cell, "1F4E79")
        par = cell.paragraphs[0]
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_before = Pt(3)
        par.paragraph_format.space_after = Pt(3)
        par.paragraph_format.line_spacing = 1.0
        r = par.add_run(head)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    trPr = hdr._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    trPr.append(tbl_header)

    for row_data in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row_data):
            cell = cells[i]
            cell.width = Cm(widths[i])
            par = cell.paragraphs[0]
            par.alignment = WD_ALIGN_PARAGRAPH.LEFT
            par.paragraph_format.space_before = Pt(3)
            par.paragraph_format.space_after = Pt(3)
            par.paragraph_format.line_spacing = 1.0
            if isinstance(val, str):
                val = [(val, "n")]
            _runs(par, val, font_size)

    add_para(doc, "", space_after=2)
    return table


def callout(doc, parts, fill="EAF3FB", accent="0071E3"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Cm(16.0)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for side, sz, color in (("top", "4", "D6E4F0"),
                            ("left", "28", accent),
                            ("bottom", "4", "D6E4F0"),
                            ("right", "4", "D6E4F0")):
        el = OxmlElement("w:" + side)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tcPr.append(borders)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

    par = cell.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.line_spacing = 1.15
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.space_after = Pt(6)
    par.paragraph_format.left_indent = Cm(0.2)
    par.paragraph_format.right_indent = Cm(0.2)
    _runs(par, parts, 13)

    add_para(doc, "", space_after=2)


def add_figure(doc, path, caption, width=15.5):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.space_after = Pt(2)
    par.add_run().add_picture(path, width=Cm(width))

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    r = cap.add_run(caption)
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)


# ============================================================================
# 3. ГЕНЕРАЦІЯ СХЕМ
# ============================================================================
scheme_methods()
scheme_flow()
scheme_table_structure()
scheme_table_types()

# ============================================================================
# 4. ДОКУМЕНТ
# ============================================================================
doc = Document()
set_normal_style(doc)

section = doc.sections[0]
section.left_margin = Cm(2.0)
section.right_margin = Cm(1.5)
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)
add_page_numbers(section)

# --- Заголовок і тема -------------------------------------------------------
h_main(doc, "ЛЕКЦІЯ 13. ЗБИРАННЯ ТА ОРГАНІЗАЦІЯ ДАНИХ")

add_para(doc,
         [("Тема: Збирання та організація даних: методи збору даних, "
           "табличне представлення даних.", "b")],
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

# --- Мета -------------------------------------------------------------------
h_sub(doc, "Мета")
add_para(doc,
         "Формувати вміння збирати та організовувати дані, подавати їх у "
         "таблицях; розвивати вміння систематизувати та впорядковувати "
         "дослідницькі дані; виховувати точність і акуратність в організації "
         "даних.")

# --- Обладнання -------------------------------------------------------------
h_sub(doc, "Обладнання")
numbered_paren(doc, ["інструкційні картки"])

# --- Ключові поняття --------------------------------------------------------
h_sub(doc, "Ключові поняття")
add_para(doc,
         "дані; збирання даних; метод; вибірка; генеральна сукупність; "
         "спостереження; опитування; анкета; інтерв’ю; аналіз документів; "
         "експеримент; таблиця; головка; боковик; комірка; групування; "
         "систематизація.")

# --- План лекції ------------------------------------------------------------
h_sub(doc, "План лекції")
num_plan = create_num(doc)
plan = [
    "Дані та інформація: чому без упорядкування факти не мають цінності.",
    "Методи збору даних у педагогічному дослідженні.",
    "Вимоги до якості зібраних даних і поняття вибірки.",
    "Табличне представлення даних: будова таблиці.",
    "Види таблиць та правила їх побудови.",
    "Алгоритм упорядкування даних і типові помилки.",
]
for item in plan:
    num_item(doc, item, num_plan)

# ============================================================================
# ТЕОРЕТИЧНИЙ МАТЕРІАЛ
# ============================================================================

# --- Блок 1 -----------------------------------------------------------------
h_sub(doc, "1. Дані як «сировина» дослідження")
add_para(doc,
         "Кожне наукове дослідження починається з фактів. Дані — це окремі "
         "зафіксовані факти, значення, відповіді, результати вимірювань, які "
         "дослідник зібрав у ході роботи. Самі по собі вони ще не є висновком: "
         "це лише матеріал, з якого цей висновок буде зроблено.")
add_para(doc,
         "Уявіть коробку з деталями конструктора. Поки деталі лежать у "
         "коробці, це просто купа — з неї нічого не можна зрозуміти. Але щойно "
         "деталі розклали за формою, кольором і розміром, з’являється "
         "можливість зібрати модель. Так само і з даними: спочатку їх збирають, "
         "потім упорядковують — і лише після цього вони перетворюються на "
         "інформацію, з якої можна робити висновки.")
add_para(doc,
         [("Дані", "b"), " — це зафіксовані факти. ",
          ("Інформація", "b"), " — це дані, упорядковані так, що вони набувають "
          "змісту й дають відповідь на поставлене запитання."])
add_para(doc,
         "Для майбутнього вчителя інформатики це особливо важливо: саме "
         "таблиця є першою моделлю бази даних, з якою учні початкової школи "
         "знайомляться на уроках. Тому вміння збирати й упорядковувати дані — "
         "це не лише дослідницька, а й професійна компетентність.")

callout(doc,
        "Зібрані, але не впорядковані дані майже не мають цінності: за ними "
        "неможливо побачити ні тенденції, ні закономірності. Упорядкування — "
        "не завершальний, а обов’язковий етап збору даних.")

# --- Блок 2 -----------------------------------------------------------------
h_sub(doc, "2. Методи збору даних")
add_para(doc,
         "Усі методи збору даних у педагогічному дослідженні можна об’єднати "
         "в чотири групи — від найпростішого спостереження за реальним "
         "перебігом подій до спеціально організованого експерименту.")

add_figure(doc, os.path.join(OUT, "01_metody_zboru_danyh.png"),
           "Рис. 1. Методи збору даних")

add_para(doc, [("Спостереження", "b"),
               " — цілеспрямоване, планомірне й обов’язково зафіксоване "
               "сприймання педагогічного процесу. Дослідник не втручається в "
               "події, а лише фіксує те, що відбувається. Приклад: на уроці "
               "інформатики у 2 класі фіксуємо, скільки учнів піднімають руку, "
               "коли вчитель ставить запитання."])
add_para(doc, [("Опитування", "b"),
               " — метод, за якого інформацію отримують безпосередньо від "
               "учасників освітнього процесу. Його різновиди: бесіда, анкета, "
               "інтерв’ю. Приклад: анкета «Що ти робиш на перерві?», яку "
               "заповнюють учні 3 класу."])
add_para(doc, [("Аналіз документів", "b"),
               " — вивчення вже наявних матеріалів: класних журналів, "
               "щоденників, результатів контрольних робіт, портфоліо учня, "
               "календарно-тематичного планування вчителя."])
add_para(doc, [("Експеримент", "b"),
               " — спеціально організована перевірка гіпотези в контрольованих "
               "умовах. Констатувальний експеримент фіксує наявний стан, "
               "формувальний — перевіряє, чи справді певний засіб дає "
               "очікуваний результат."])

add_table(doc,
          ["Метод", "Що дає досліднику", "Приклад зі школи"],
          [["Спостереження",
            "бачу і фіксую те, що відбувається насправді",
            "скільки учнів 2 класу піднімають руку на уроці інформатики"],
           ["Опитування",
            "отримую думки й відповіді самих учасників",
            "анкета «Що ти робиш на перерві?» для учнів 3 класу"],
           ["Аналіз документів",
            "працюю з уже зафіксованою інформацією",
            "оцінки з класного журналу за семестр"],
           ["Експеримент",
            "перевіряю, чи справді діє певний засіб",
            "порівняння результатів уроків з навчальною грою та без неї"]],
          widths=[3.8, 6.0, 6.0])

# --- Блок 3 -----------------------------------------------------------------
h_sub(doc, "3. Вимоги до якості зібраних даних")
add_para(doc,
         "Зібрати дані — це лише половина справи. Щоб на їх основі можна було "
         "зробити коректний висновок, дані мають відповідати низці вимог.")
bullet(doc, [("точність", "b"),
             " — записано саме те, що реально було, без «округлення на користь "
             "гіпотези»;"])
bullet(doc, [("повнота", "b"),
             " — зібрано значення за всіма запланованими ознаками, без "
             "пропусків;"])
bullet(doc, [("надійність", "b"),
             " — повторний збір у схожих умовах дає близький результат;"])
bullet(doc, [("своєчасність", "b"),
             " — дані зафіксовано тоді, коли подія відбулася, а не «по пам’яті» "
             "через тиждень;"])
bullet(doc, [("однозначність", "b"),
             " — різні дослідники розуміють і тлумачать запис однаково;"])
bullet(doc, [("репрезентативність", "b"),
             " — вибірка представляє всю генеральну сукупність."])

add_para(doc,
         "Остання вимога найчастіше порушується. Якщо анкету в класі, де "
         "28 учнів, заповнили лише 5 осіб, робити висновок про весь клас не "
         "можна: така вибірка не є репрезентативною. Висновок стосуватиметься "
         "лише тих п’ятьох, хто відповідав.")

callout(doc,
        "Фіксуйте дані одразу й за єдиним зразком: польовий щоденник, "
        "однаковий формат запису, дата й умови спостереження. Запис, "
        "зроблений через кілька днів «по пам’яті», втрачає точність і "
        "перетворюється на припущення.",
        fill="FFF4E8", accent="C93400")

# --- Блок 4 -----------------------------------------------------------------
h_sub(doc, "4. Табличне представлення даних")
add_para(doc,
         "Найзручніша форма впорядкування даних — таблиця. Це форма подання "
         "даних, у якій значення розміщуються на перетині рядків і стовпців. "
         "Завдяки цьому кожне значення має свою «адресу»: воно належить "
         "конкретному об’єкту (рядок) і конкретній ознаці (стовпець).")

add_figure(doc, os.path.join(OUT, "03_budova_tablytsi.png"),
           "Рис. 2. Будова таблиці")

add_para(doc,
         "У таблиці розрізняють головку (шапку) — рядок із назвами стовпців, "
         "боковик — стовпець із назвами рядків, і комірки — місця перетину "
         "рядка та стовпця. Крім того, виділяють підмет таблиці (те, про що "
         "йдеться, — об’єкти в рядках чи стовпцях) і присудок (те, що про них "
         "сказано, — числові значення).")

add_table(doc,
          ["Елемент таблиці", "Що в ньому розміщують", "Приклад"],
          [["Головка (шапка)", "назви стовпців — ознаки",
            "Клас, Учнів, Високий рівень"],
           ["Боковик", "назви рядків — об’єкти",
            "1-А, 2-Б, 3-В"],
           ["Комірка", "одне значення на перетині рядка і стовпця",
            "25, 7, 12"],
           ["Підсумковий рядок", "узагальнені результати за стовпцем",
            "Разом, Середнє"]],
          widths=[4.0, 6.5, 5.3])

add_para(doc, "Під час побудови таблиці дотримуйтеся таких правил:")
bullet(doc, "заголовки стовпців — короткі й зрозумілі, без крапки в кінці;")
bullet(doc, "одиниці вимірювання вказують у головці, наприклад «Кількість "
            "учнів, осіб»;")
bullet(doc, "порожніх клітинок не залишають: ставлять «0» або «–»;")
bullet(doc, "в межах одного стовпця — однакова точність округлення;")
bullet(doc, "підсумковий рядок або стовпець — обов’язковий;")
bullet(doc, "усередині таблиці даних не використовують об’єднаних комірок.")

# --- Блок 5 -----------------------------------------------------------------
h_sub(doc, "5. Види таблиць")
add_para(doc,
         "Залежно від кількості ознак, за якими впорядковано дані, таблиці "
         "поділяють на прості, групові та комбінаційні.")

add_figure(doc, os.path.join(OUT, "04_vydy_tablyts.png"),
           "Рис. 3. Види таблиць")

add_table(doc,
          ["Вид таблиці", "Скільки ознак", "Приклад"],
          [["Проста", "одна ознака, один об’єкт",
            "оцінки одного учня з інформатики за чвертями"],
           ["Групова", "об’єкти згруповані за однією ознакою",
            "середній бал учнів 1-А, 2-Б, 3-В"],
           ["Комбінаційна", "дві й більше ознак одночасно",
            "клас × предмет × семестр"]],
          widths=[4.0, 5.5, 6.3])

add_para(doc,
         "Для дослідницької роботи найчастіше використовують групові таблиці: "
         "вони дають змогу порівняти між собою окремі класи, паралелі або "
         "групи учнів за однією важливою ознакою.")

# --- Блок 6 -----------------------------------------------------------------
h_sub(doc, "6. Алгоритм упорядкування даних")
add_para(doc,
         "Щоб перетворити зібрані факти на таблицю, достатньо пройти шість "
         "послідовних кроків. Кожен наступний крок спирається на попередній, "
         "тому пропускати їх не можна.")

add_figure(doc, os.path.join(OUT, "02_alhorytm_uporyadkuvannya.png"),
           "Рис. 4. Шлях від ідеї до таблиці")

num_steps = create_num(doc)
steps = [
    "Сформулювати мету: що саме хочемо з’ясувати.",
    "Визначити ознаки, значення яких фіксуватимемо.",
    "Обрати метод збору даних (або кілька методів).",
    "Зібрати дані та зафіксувати їх в єдиному форматі.",
    "Упорядкувати: згрупувати, відсортувати, порахувати підсумки.",
    "Побудувати таблицю й перевірити її на відповідність правилам.",
]
for step in steps:
    num_item(doc, step, num_steps)

add_para(doc,
         [("Готову таблицю зручно будувати в ", "n"),
          ("Microsoft Excel", "m"), (" або ", "n"),
          ("Google Таблиці", "m"),
          (": програма автоматично рахує суми й середні значення та дає змогу "
           "відсортувати рядки за обраною ознакою.", "n")])

callout(doc,
        "Типові помилки під час побудови таблиць: різні одиниці вимірювання в "
        "одному стовпці; кілька значень в одній комірці; об’єднані комірки "
        "всередині таблиці даних; відсутність підсумкового рядка; різні назви "
        "того самого об’єкта в різних рядках (наприклад, «2-Б» і «2 Б»).",
        fill="FDECEC", accent="C4001D")

# ============================================================================
# КОНТРОЛЬНІ ПИТАННЯ
# ============================================================================
h_sub(doc, "Контрольні питання")
num_q = create_num(doc)
questions = [
    "Що таке дані? Чим дані відрізняються від інформації?",
    "Чому зібрані, але не впорядковані дані майже не мають цінності?",
    "Назвіть основні методи збору даних у педагогічному дослідженні.",
    "У чому особливість спостереження як методу збору даних?",
    "Які різновиди опитування ви знаєте? Наведіть приклад анкети для "
    "молодших школярів.",
    "Що може бути джерелом даних під час аналізу документів?",
    "Чим констатувальний експеримент відрізняється від формувального?",
    "Які вимоги висувають до якості зібраних даних?",
    "Що таке репрезентативність вибірки? Наведіть приклад нерепрезентативної "
    "вибірки.",
    "Назвіть і охарактеризуйте основні елементи таблиці.",
    "Які види таблиць розрізняють? Наведіть приклад для кожного виду.",
    "Яких помилок слід уникати під час побудови таблиці даних?",
]
for q in questions:
    num_item(doc, q, num_q)

# ============================================================================
# РЕКОМЕНДОВАНІ ДЖЕРЕЛА
# ============================================================================
h_sub(doc, "Рекомендовані джерела")
num_src = create_num(doc)
sources = [
    "Лаппо В. В. Основи педагогічних досліджень. Івано-Франківськ : НАІР, "
    "2016. 284 с.",
    "Оліяр М. П., Русин Г. А., Червінька І. Б. Основи науково-педагогічних "
    "досліджень (модульно-рейтинговий підхід). Івано-Франківськ : Наїр, "
    "2013. 214 с.",
]
for s in sources:
    num_item(doc, s, num_src)

# ============================================================================
# ЗБЕРЕЖЕННЯ
# ============================================================================
FILE_NAME = "Lektsiia_13_Zbyrannia_ta_orhanizatsiia_danykh.docx"
doc.save(FILE_NAME)
print("Готово! Створено файл:", FILE_NAME)
print("Схеми збережено в папці:", os.path.abspath(OUT))
print("Файли схем:", ", ".join(sorted(os.listdir(OUT))))