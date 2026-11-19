# -*- coding: utf-8 -*-
"""
Практичне заняття 12.
Спостереження, тестування, анкетування, стандартизоване оцінювання
та формалізація їхніх результатів.
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
# 1. СХЕМИ
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


# --- Схема 1. Чотири емпіричні методи ---------------------------------------
def scheme_methods():
    fig, ax = plt.subplots(figsize=(12.6, 3.9))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    ax.text(0.35, 4.55, "Емпіричні методи дослідження",
            fontsize=15, fontweight="bold",
            color=C_TEXT, ha="left", va="center")

    items = [
        ("Спостереження", "бачу і протоколюю", C_BLUE),
        ("Тестування", "вимірюю завданнями", C_GREEN),
        ("Анкетування", "питаю письмово", C_ORANGE),
        ("Стандарт. оцінювання", "порівнюю зі шкалою", C_PURPLE),
    ]
    w, h, gap = 3.55, 2.55, 0.45
    x, y = 0.35, 0.95
    for title, sub, accent in items:
        _card(ax, x, y, w, h, title, sub, accent=accent,
              fs_title=12.5, fs_sub=11.0)
        x += w + gap

    _save(fig, "01_metody_empirychni")


# --- Схема 2. Шлях формалізації ---------------------------------------------
def scheme_formalization():
    fig, ax = plt.subplots(figsize=(12.6, 3.6))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    ax.text(0.35, 4.15, "Формалізація результатів",
            fontsize=15, fontweight="bold",
            color=C_TEXT, ha="left", va="center")

    steps = [
        ("1. Фіксація", "протокол / бланк", C_BLUE),
        ("2. Кодування", "єдині позначення", C_BLUE),
        ("3. Таблиця", "рядки й стовпці", C_BLUE),
        ("4. Обробка", "суми, середні", C_BLUE),
        ("5. Висновок", "узагальнення", C_GREEN),
    ]
    w, h, gap = 2.75, 2.35, 0.42
    x, y = 0.35, 0.85
    for i, (title, sub, accent) in enumerate(steps):
        _card(ax, x, y, w, h, title, sub, accent=accent,
              fs_title=12.0, fs_sub=11.0)
        if i < len(steps) - 1:
            ax.annotate("",
                        xy=(x + w + gap - 0.06, y + h / 2),
                        xytext=(x + w + 0.06, y + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.4))
        x += w + gap

    _save(fig, "02_formalizatsiia")


# --- Схема 3. Три рівні завдань ---------------------------------------------
def scheme_levels():
    fig, ax = plt.subplots(figsize=(12.6, 4.4))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(0.35, 5.15, "Різнорівневі завдання",
            fontsize=15, fontweight="bold",
            color=C_TEXT, ha="left", va="center")
    ax.text(15.85, 5.15, "Разом: 25–30 хв",
            fontsize=12, color=C_GRAY, ha="right", va="center")

    items = [
        ("Рівень 1 · Репродуктивний", "≈ 7 хв", "повторюю зразок", C_BLUE),
        ("Рівень 2 · Продуктивний", "≈ 10 хв", "переношу в нову ситуацію", C_GREEN),
        ("Рівень 3 · Творчий", "≈ 10 хв", "створюю власний інструмент", C_PURPLE),
    ]
    w, h, gap = 4.9, 3.2, 0.55
    x, y = 0.4, 0.65
    for title, tm, sub, accent in items:
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=0.2",
                             linewidth=1.4, edgecolor=C_BORDER,
                             facecolor=C_CARD, zorder=2)
        ax.add_patch(box)
        bar = FancyBboxPatch((x + 0.18, y + h - 0.2), w - 0.36, 0.1,
                             boxstyle="round,pad=0,rounding_size=0.05",
                             linewidth=0, facecolor=accent, zorder=3)
        ax.add_patch(bar)
        ax.text(x + w / 2, y + h - 0.75, title, ha="center", va="center",
                fontsize=13.5, fontweight="bold", color=C_TEXT, zorder=4)
        ax.text(x + w / 2, y + h - 1.55, tm, ha="center", va="center",
                fontsize=15, fontweight="bold", color=accent, zorder=4)
        ax.text(x + w / 2, y + 0.75, sub, ha="center", va="center",
                fontsize=12, color=C_GRAY, zorder=4)
        x += w + gap

    _save(fig, "03_rivni_zavdan")


# --- Схема 4. Етика збору даних ---------------------------------------------
def scheme_ethics():
    fig, ax = plt.subplots(figsize=(12.6, 3.9))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    ax.text(0.35, 4.55, "Етика збору даних",
            fontsize=15, fontweight="bold",
            color=C_TEXT, ha="left", va="center")

    items = [
        ("Добровільність", "без примусу й тиску", C_BLUE),
        ("Анонімність", "без прізвищ у звіті", C_GREEN),
        ("Конфіденційність", "дані не для третіх осіб", C_ORANGE),
        ("Достовірність", "факти без вигадок", C_RED),
    ]
    w, h, gap = 3.55, 2.55, 0.45
    x, y = 0.35, 0.95
    for title, sub, accent in items:
        _card(ax, x, y, w, h, title, sub, accent=accent,
              fs_title=12.5, fs_sub=11.0)
        x += w + gap

    _save(fig, "04_etyka_zboru")


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
scheme_formalization()
scheme_levels()
scheme_ethics()

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
h_main(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ 12")

add_para(doc,
         [("Тема: Спостереження, тестування, анкетування, стандартизоване "
           "оцінювання та формалізація їхніх результатів.", "b")],
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

# --- Мета -------------------------------------------------------------------
h_sub(doc, "Мета")
add_para(doc,
         "Формувати вміння проводити спостереження, тестування, анкетування, "
         "стандартизоване оцінювання та формалізувати їхні результати; "
         "розвивати практичні навички збору емпіричних даних; виховувати "
         "відповідальність за достовірність і етичність збору даних.")

# --- Обладнання та програмне забезпечення -----------------------------------
h_sub(doc, "Обладнання та програмне забезпечення")
numbered_paren(doc, [
    "інструкційні картки до практичного заняття;",
    "зошит для практичних робіт, ручка, олівець, лінійка;",
    "персональний комп’ютер із текстовим редактором "
    "Microsoft Word або Google Документи;",
    "табличний процесор Microsoft Excel або Google Таблиці;",
    "бланки протоколу спостереження, анкети й тесту (додаються).",
])

# --- Література -------------------------------------------------------------
h_sub(doc, "Література")
num_src = create_num(doc)
sources = [
    "Лимар Ю. М. Основи науково-педагогічних досліджень. Чернігів : "
    "Чернігівський національний педагогічний університет імені Т. Г. Шевченка, "
    "2011. 56 с.",
    "Сисоєва С. О., Кристопчук Т. Є. Методологія науково-педагогічних "
    "досліджень. Рівне : Волинські обереги, 2013. 360 с.",
]
for s in sources:
    num_item(doc, s, num_src)

# ============================================================================
# ТЕОРЕТИЧНІ ВІДОМОСТІ
# ============================================================================
h_sub(doc, "Теоретичні відомості")

# --- 1. Огляд методів -------------------------------------------------------
h_sub(doc, "1. Емпіричні методи в педагогічному дослідженні", SUB_HEAD)
add_para(doc,
         "Емпіричні методи дають досліднику первинний фактичний матеріал. "
         "До основних з них належать спостереження, тестування, анкетування "
         "та стандартизоване оцінювання. Кожен метод має свою мету, "
         "інструмент і форму фіксації результатів, тому в реальному "
         "дослідженні їх зазвичай поєднують.")

add_figure(doc, os.path.join(OUT, "01_metody_empirychni.png"),
           "Рис. 1. Емпіричні методи дослідження")

add_table(doc,
          ["Метод", "Що дає", "Інструмент", "Форма фіксації"],
          [["Спостереження", "опис реального перебігу подій",
            "протокол, щоденник", "записи за схемою"],
           ["Тестування", "числовий показник підготовки",
            "тест із ключем", "бланк відповідей, бали"],
           ["Анкетування", "думки, ставлення, самооцінку",
            "анкета", "зведена таблиця відповідей"],
           ["Стандарт. оцінювання", "порівняння зі шкалою",
            "оцінний лист, рубрика", "рівень за шкалою"]],
          widths=[3.8, 4.4, 3.4, 4.2])

callout(doc,
        "Інструмент обирають під мету, а не навпаки: якщо треба з’ясувати, "
        "як учень діє на уроці, — це спостереження; якщо треба порівняти "
        "рівень засвоєння теми в кількох класах — це тест або "
        "стандартизоване оцінювання.")

# --- 2. Спостереження -------------------------------------------------------
h_sub(doc, "2. Спостереження та протокол спостереження", SUB_HEAD)
add_para(doc,
         "Спостереження — це цілеспрямоване й планомірне сприймання "
         "педагогічного процесу з обов’язковою фіксацією побаченого. "
         "Результати заносять у протокол — таблицю, у якій заздалегідь "
         "визначено, що саме й у якій формі записувати.")
add_para(doc, "Основні вимоги до протоколу:")
bullet(doc, "фіксують факт, а не оцінку («підняв руку», а не «був активний»);")
bullet(doc, "записують час і тривалість кожної події;")
bullet(doc, "використовують однакові умовні позначки впродовж усього "
            "спостереження;")
bullet(doc, "запис роблять безпосередньо під час події, а не «по пам’яті».")

# --- 3. Тестування і стандартизоване оцінювання -----------------------------
h_sub(doc, "3. Тестування і стандартизоване оцінювання", SUB_HEAD)
add_para(doc,
         "Тест — це система коротких завдань однакової структури з "
         "наперед визначеним ключем і правилами оцінювання. За формою "
         "завдань розрізняють тести закриті (вибір однієї відповіді з "
         "кількох), відкриті (коротка чи розгорнута відповідь) та на "
         "встановлення відповідності.")
add_para(doc,
         "Стандартизоване оцінювання передбачає єдину шкалу для всіх "
         "учасників. Наприклад, рівні навчальних досягнень учнів початкової "
         "школи: початковий, середній, достатній, високий. Головна вимога — "
         "однакові критерії застосовувати до всіх без винятку.")
add_para(doc, "Обов’язкові елементи тесту та оцінного листа:")
bullet(doc, "інструкція для учасника;")
bullet(doc, "чітко сформульовані завдання;")
bullet(doc, "ключ або критерії оцінювання;")
bullet(doc, "шкала переведення балів у рівень.")

# --- 4. Анкетування ---------------------------------------------------------
h_sub(doc, "4. Анкетування: види запитань і вимоги", SUB_HEAD)
add_para(doc,
         "Анкета — це набір запитань, на які учасник відповідає письмово. "
         "За формою запитання бувають закриті (з готовими варіантами "
         "відповіді), напівзакриті (з варіантами та можливістю дописати "
         "своє) і відкриті (вільна відповідь).")
add_para(doc, "Вимоги до анкети:")
bullet(doc, "на початку — коротка інструкція й гарантія анонімності;")
bullet(doc, "одне запитання — одна думка, без подвійних формулювань;")
bullet(doc, "уникати навіювальних і оцінних слів («чи не здається вам, "
            "що…»);")
bullet(doc, "для молодших школярів — не більше 5–7 простих запитань;")
bullet(doc, "наприкінці — подяка за участь.")

# --- 5. Формалізація результатів --------------------------------------------
h_sub(doc, "5. Формалізація результатів дослідження", SUB_HEAD)
add_para(doc,
         "Формалізація — це перетворення «сирих» записів на впорядковані "
         "числові й табличні дані, придатні для порівняння та висновків. "
         "Вона включає п’ять послідовних кроків.")

add_figure(doc, os.path.join(OUT, "02_formalizatsiia.png"),
           "Рис. 2. Шлях формалізації результатів")

add_para(doc,
         "На першому кроці заповнюють протокол або бланк. На другому — "
         "вводять єдині позначки для повторюваних значень (наприклад, "
         "«+» — завдання виконано, «–» — не виконано). На третьому — "
         "переносять дані в таблицю. На четвертому — рахують суми, "
         "середні, відсотки. На п’ятому — формулюють висновок за метою "
         "дослідження.")

# --- 6. Етика ---------------------------------------------------------------
h_sub(doc, "6. Етика збору даних", SUB_HEAD)
add_para(doc,
         "Дослідник працює з людьми, тому достовірність даних — це не лише "
         "наукова, а й етична вимога. Порушення етики знецінює результати "
         "всієї роботи.")

add_figure(doc, os.path.join(OUT, "04_etyka_zboru.png"),
           "Рис. 3. Принципи етики збору даних")

callout(doc,
        "Якщо учасник відмовився відповідати або просить вилучити свої "
        "дані — його бажання виконують без обговорення. У звіті прізвища "
        "учасників не вказують: використовують коди на зразок «Уч. 1», "
        "«Уч. 2».",
        fill="FDECEC", accent="C4001D")

# ============================================================================
# ПОКРОКОВИЙ АЛГОРИТМ
# ============================================================================
h_sub(doc, "Покроковий алгоритм виконання різнорівневих завдань")
add_para(doc,
         "Практична частина складається з трьох рівнів і виконується "
         "послідовно. Загальна тривалість — 25–30 хвилин.")

add_figure(doc, os.path.join(OUT, "03_rivni_zavdan.png"),
           "Рис. 4. Рівні завдань і розподіл часу")

# --- Рівень 1 ---------------------------------------------------------------
h_sub(doc, "Рівень 1. Репродуктивний (≈ 7 хв)")
add_para(doc,
         [("Завдання. ", "b"),
          ("За поданим зразком заповнити протокол спостереження за уроком "
           "інформатики у 2 класі (фрагмент — 10 хвилин). Зразок протоколу "
           "видає викладач на інструкційній картці.", "n")])

add_table(doc,
          ["Крок", "Дія", "Результат"],
          [["1", "Ознайомтеся зі схемою протоколу на інструкційній картці",
            "розумієте, які стовпці заповнювати"],
           ["2", "Перегляньте відеофрагмент уроку (або заслухайте опис)",
            "маєте факти для запису"],
           ["3", "Заповніть стовпці «Час», «Подія», «Умовна позначка»",
            "заповнений протокол"],
           ["4", "Порахуйте кількість позначок кожного виду",
            "підсумковий рядок протоколу"],
           ["5", "Перевірте, чи не порушено правила фіксації",
            "виправлений протокол"]],
          widths=[1.4, 8.4, 6.0])

# --- Рівень 2 ---------------------------------------------------------------
h_sub(doc, "Рівень 2. Продуктивний (≈ 10 хв)")
add_para(doc,
         [("Завдання. ", "b"),
          ("За результатами заповненого протоколу побудувати зведену "
           "таблицю «Показники активності учнів 2 класу на уроці "
           "інформатики», обчислити відсотки й сформулювати один "
           "висновок.", "n")])

add_table(doc,
          ["Крок", "Дія", "Результат"],
          [["1", "Визначте, які показники будете зводити (підняв руку, "
                 "відповів, поставив запитання)", "перелік стовпців"],
           ["2", "Перенесіть підсумки протоколу в таблицю Excel / Google "
                 "Таблиці", "таблиця з числовими даними"],
           ["3", "Обчисліть відсоток кожного показника від загальної "
                 "кількості учнів", "стовпець «%»"],
           ["4", "Додайте підсумковий рядок із середнім значенням",
            "завершена таблиця"],
           ["5", "Сформулюйте висновок одним-двома реченнями",
            "текст висновку під таблицею"]],
          widths=[1.4, 8.4, 6.0])

callout(doc,
        "У таблиці мають бути однакові одиниці вимірювання в межах одного "
        "стовпця й обов’язковий підсумковий рядок. Порожніх клітинок не "
        "залишайте: ставте «0» або «–».",
        fill="FFF4E8", accent="C93400")

# --- Рівень 3 ---------------------------------------------------------------
h_sub(doc, "Рівень 3. Творчий (≈ 10 хв)")
add_para(doc,
         [("Завдання. ", "b"),
          ("Скласти власну анкету з 5 запитань для учнів 3 класу за темою "
           "«Що мені подобається на уроках інформатики?». Передбачити "
           "інструкцію, різні типи запитань, форму подання результатів у "
           "звіті.", "n")])

add_table(doc,
          ["Етап", "Що зробити", "Орієнтир"],
          [["Інструкція", "1–2 речення: мета й гарантія анонімності",
            "«Обери один варіант…»"],
           ["Запитання 1", "закрите — вибір одного варіанта з чотирьох",
            "«Що тобі найбільше подобається?»"],
           ["Запитання 2", "закрите — вибір кількох варіантів",
            "«Познач усе, що подобається»"],
           ["Запитання 3", "напівзакрите — варіанти + «свій варіант»",
            "«Інше: ______»"],
           ["Запитання 4", "відкрите — коротка вільна відповідь",
            "«Що б ти змінив?»"],
           ["Запитання 5", "шкала (від 1 до 5)",
            "«Наскільки цікаво?»"],
           ["Форма результату", "таблиця «№ запитання — кількість "
                                "відповідей — %»", "готова до обробки"]],
          widths=[3.4, 7.4, 5.0])

# ============================================================================
# КРИТЕРІЇ ОЦІНЮВАННЯ
# ============================================================================
h_sub(doc, "Критерії оцінювання")

add_table(doc,
          ["Вид роботи", "Що оцінюють", "Максимум балів"],
          [["Рівень 1. Репродуктивний (≈ 7 хв)",
            "повнота й точність протоколу, дотримання правил фіксації", "3"],
           ["Рівень 2. Продуктивний (≈ 10 хв)",
            "правильність обчислень, охайність таблиці, "
            "обґрунтованість висновку", "5"],
           ["Рівень 3. Творчий (≈ 10 хв)",
            "структура анкети, доречність типів запитань, "
            "етичність формулювань", "3"],
           ["Оформлення звіту", "акуратність, єдиний стиль, "
            "вчасне подання", "2"],
           ["Разом", "—", "13"]],
          widths=[6.5, 7.3, 2.2])

add_para(doc,
         [("Шкала переведення балів: ", "b"),
          ("11–13 балів — «відмінно»; 8–10 — «добре»; 5–7 — "
           "«задовільно»; 0–4 — «незадовільно».", "n")])

# ============================================================================
# ФОРМА ЗВІТНОСТІ
# ============================================================================
h_sub(doc, "Форма звітності")
add_para(doc,
         "За результатами практичного заняття студент готує письмовий звіт "
         "обсягом 2–3 сторінки в електронному вигляді (файл "
         "Microsoft Word або Google Документ).")
add_para(doc, "Структура звіту:")
numbered_paren(doc, [
    "тема, мета й обладнання заняття;",
    "заповнений протокол спостереження (рівень 1);",
    "зведена таблиця показників із підсумковим рядком і висновком "
    "(рівень 2);",
    "власна анкета з 5 запитань та опис форми обробки її результатів "
    "(рівень 3);",
    "короткий підсумок (3–5 речень): що вдалося, які труднощі виникли, "
    "що будете враховувати в майбутній професійній діяльності.",
])

callout(doc,
        "У звіті не вказуйте прізвищ учнів — лише коди («Уч. 1», «Уч. 2»). "
        "Усі таблиці оформлюйте в єдиному стилі, із заголовками стовпців і "
        "підсумковим рядком.")

# ============================================================================
# ЗБЕРЕЖЕННЯ
# ============================================================================
FILE_NAME = "Praktychne_12_Empirychni_metody.docx"
doc.save(FILE_NAME)
print("Готово! Створено файл:", FILE_NAME)
print("Схеми збережено в папці:", os.path.abspath(OUT))
print("Файли схем:", ", ".join(sorted(os.listdir(OUT))))