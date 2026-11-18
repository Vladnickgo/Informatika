# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу: ЛЕКЦІЯ
Тема: Урок інформатики в початковій школі.
      Структура уроку інформатики в початкових класах
"""

import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------------------------------------------------------------------
# Константи
# ---------------------------------------------------------------------------
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

BG     = "#F5F5F7"
BORDER = "#E5E5EA"
TEXT   = "#1D1D1F"
GREY   = "#86868B"
BLUE   = "#0071E3"
GREEN  = "#248A3D"
ORANGE = "#C93400"
RED    = "#C4001D"
PURPLE = "#6E30A8"
YELLOW = "#C9A400"

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


# ---------------------------------------------------------------------------
# Базові елементи схем
# ---------------------------------------------------------------------------
def _new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def _save(fig, name):
    fig.savefig(f"{OUT_DIR}/{name}.png", dpi=220,
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(f"{OUT_DIR}/{name}.svg",
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return f"{OUT_DIR}/{name}.png"


def _card(ax, x, y, w, h, title, subtitle, accent, fs_title=14.5, fs_sub=11.5):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.18",
        linewidth=1.4, edgecolor=BORDER, facecolor=BG,
    )
    ax.add_patch(box)
    strip = FancyBboxPatch(
        (x + 0.06, y + h - 0.16), w - 0.12, 0.12,
        boxstyle="round,pad=0,rounding_size=0.06",
        linewidth=0, facecolor=accent,
    )
    ax.add_patch(strip)
    ax.text(x + w / 2, y + h - 0.55, title,
            ha="center", va="center", fontsize=fs_title,
            color=TEXT, fontweight="bold")
    if subtitle:
        ax.text(x + w / 2, y + h / 2 - 0.15, subtitle,
                ha="center", va="center", fontsize=fs_sub,
                color=GREY, linespacing=1.45)


def _arrow(ax, x1, y1, x2, y2, color=GREY):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=20,
        linewidth=1.6, color=color, shrinkA=0, shrinkB=0,
    )
    ax.add_patch(arr)


# ---------------------------------------------------------------------------
# Схема 1: типологія уроків інформатики
# ---------------------------------------------------------------------------
def schema_types():
    name = "lesson_types"
    fig, ax = _new_ax(11, 5.6)
    ax.text(5.5, 5.25, "Типи уроків інформатики в початкових класах",
            ha="center", va="center", fontsize=15,
            color=TEXT, fontweight="bold")

    items = [
        ("Засвоєння знань",     "пояснення + первинне\nзакріплення",        BLUE),
        ("Формування вмінь",    "практична робота\nза зразком",             GREEN),
        ("Узагальнення",        "систематизація,\nузагальнюючі таблиці",    PURPLE),
        ("Контроль і корекція", "самостійна робота,\nтестові завдання",     RED),
        ("Комбінований",        "поєднання кількох\nдидактичних цілей",     ORANGE),
        ("Нестандартний",       "урок-гра, урок-\nподорож, урок-казка",     YELLOW),
    ]
    cw, ch, gx, gy = 3.2, 1.7, 0.35, 0.35
    sx = (11 - (3 * cw + 2 * gx)) / 2

    for i, (t, s, c) in enumerate(items):
        col, row = i % 3, i // 3
        x = sx + col * (cw + gx)
        y = 3.30 - row * (ch + gy)
        _card(ax, x, y, cw, ch, t, s, c)

    return _save(fig, name)


# ---------------------------------------------------------------------------
# Схема 2: структура уроку (етапи)
# ---------------------------------------------------------------------------
def schema_stages():
    name = "lesson_stages"
    fig, ax = _new_ax(11, 5.4)
    ax.text(5.5, 5.05, "Структура уроку інформатики в початковій школі",
            ha="center", va="center", fontsize=15,
            color=TEXT, fontweight="bold")

    steps = [
        ("Етап 1", "Організаційний\nмомент",       BLUE),
        ("Етап 2", "Актуалізація\nопорних знань",  PURPLE),
        ("Етап 3", "Мотивація\nнавчальної діяльності", ORANGE),
        ("Етап 4", "Вивчення нового\nматеріалу",   GREEN),
        ("Етап 5", "Практична\nробота",            RED),
        ("Етап 6", "Підсумок\nі рефлексія",        YELLOW),
    ]
    cw, ch, gx = 3.0, 1.5, 0.4
    sx = 0.6
    y_top, y_bot = 3.0, 1.2

    pos = []
    for i in range(6):
        col = i if i < 3 else (5 - i)
        row = 0 if i < 3 else 1
        x = sx + col * (cw + gx)
        y = y_top if row == 0 else y_bot
        pos.append((x, y))

    for i, (num, text, color) in enumerate(steps):
        x, y = pos[i]
        _card(ax, x, y, cw, ch, num, text, color)

    # стрілки у верхньому ряду
    for i in (0, 1):
        x1 = pos[i][0] + cw + 0.04
        x2 = pos[i + 1][0] - 0.04
        _arrow(ax, x1, y_top + ch / 2, x2, y_top + ch / 2)

    # перехід між рядами
    x_down = pos[2][0] + cw / 2
    _arrow(ax, x_down, y_top - 0.04, x_down, y_bot + ch + 0.04)

    # стрілки в нижньому ряду (справа наліво)
    for i in (3, 4):
        x1 = pos[i][0] - 0.04
        x2 = pos[i + 1][0] + cw + 0.04
        _arrow(ax, x1, y_bot + ch / 2, x2, y_bot + ch / 2)

    return _save(fig, name)


# ---------------------------------------------------------------------------
# Схема 3: безпечна тривалість роботи за екраном
# ---------------------------------------------------------------------------
def schema_time():
    name = "screen_time"
    fig, ax = _new_ax(10, 4.4)
    ax.text(5, 4.05, "Безпечна тривалість безперервної роботи за екраном",
            ha="center", va="center", fontsize=14.5,
            color=TEXT, fontweight="bold")

    rows = [
        ("1 клас", 10, BLUE),
        ("2 клас", 12, GREEN),
        ("3 клас", 15, ORANGE),
        ("4 клас", 20, PURPLE),
    ]
    x0, scale, bh = 2.6, 0.30, 0.52

    for i, (label, minutes, color) in enumerate(rows):
        y = 0.85 + (3 - i) * 0.78
        ax.text(x0 - 0.25, y + bh / 2, label, ha="right", va="center",
                fontsize=12.5, color=TEXT)
        w = minutes * scale
        bar = FancyBboxPatch(
            (x0, y), w, bh,
            boxstyle="round,pad=0,rounding_size=0.16",
            linewidth=0, facecolor=color, alpha=0.88,
        )
        ax.add_patch(bar)
        ax.text(x0 + w + 0.18, y + bh / 2, f"{minutes} хв",
                ha="left", va="center", fontsize=12,
                color=TEXT, fontweight="bold")

    ax.text(5, 0.25, "для учнів 1 класу — не на кожному уроці",
            ha="center", va="center", fontsize=11, color=GREY)

    return _save(fig, name)


# ---------------------------------------------------------------------------
# Схема 4: форми організації навчальної діяльності
# ---------------------------------------------------------------------------
def schema_forms():
    name = "work_forms"
    fig, ax = _new_ax(11.5, 3.4)
    ax.text(5.75, 3.05, "Форми організації діяльності на уроці",
            ha="center", va="center", fontsize=15,
            color=TEXT, fontweight="bold")

    items = [
        ("Фронтальна",    "спільна робота\nвсього класу",     BLUE),
        ("Парна",         "робота в парах\nза інструкцією",   GREEN),
        ("Групова",       "проєктна робота\nу малих групах",  ORANGE),
        ("Індивідуальна", "власний темп\nі власний проєкт",   PURPLE),
    ]
    cw, ch, gap = 2.5, 1.7, 0.35
    total = 4 * cw + 3 * gap
    sx = (11.5 - total) / 2
    y = 0.95

    for i, (t, s, c) in enumerate(items):
        x = sx + i * (cw + gap)
        _card(ax, x, y, cw, ch, t, s, c)

    return _save(fig, name)


# ---------------------------------------------------------------------------
# Хелпери docx
# ---------------------------------------------------------------------------
def set_tnr(run, size=14, bold=False, color=None, italic=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color.lstrip("#").upper())
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Times New Roman")


def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def add_footer_page_number(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    run = p.add_run()
    set_tnr(run, size=12)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)


def add_heading(doc, text, color="#1F4E79", size=14,
                before=12, after=6, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    set_tnr(r, size=size, bold=True, color=color)
    return p


def add_par(doc, text, bold=False, italic=False, size=14,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=5):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    set_tnr(r, size=size, bold=bold, italic=italic)
    return p


def add_bullet(doc, text, indent_cm=1.0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(indent_cm)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    set_tnr(r)
    return p


# --- нумерація з коректним перезапуском -------------------------------------
_NUM_SEQ = [100]

_PPR_SUCCESSORS = (
    "w:suppressLineNumbers", "w:pBdr", "w:shd", "w:tabs",
    "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct",
    "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi",
    "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
    "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
    "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
    "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr",
    "w:pPrChange",
)


def new_numbered_list(doc):
    """Створює окреме визначення нумерації (кожен список починається з 1)."""
    nid = _NUM_SEQ[0]
    _NUM_SEQ[0] += 1

    numbering = doc.part.numbering_part.element

    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(nid))

    mlt = OxmlElement("w:multiLevelType")
    mlt.set(qn("w:val"), "singleLevel")
    abstract.append(mlt)

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
    ppr = OxmlElement("w:pPr")
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "567")
    ind.set(qn("w:hanging"), "284")
    ppr.append(ind)
    for el in (start, fmt, txt, jc, ppr):
        lvl.append(el)
    abstract.append(lvl)

    first_num = numbering.find(qn("w:num"))
    if first_num is not None:
        first_num.addprevious(abstract)
    else:
        numbering.append(abstract)

    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(nid))
    an = OxmlElement("w:abstractNumId")
    an.set(qn("w:val"), str(nid))
    num.append(an)
    numbering.append(num)
    return nid


def add_list_item(doc, text, num_id, indent_cm=1.0, size=14):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent = Cm(indent_cm)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    pPr = p._p.get_or_add_pPr()
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    numId = OxmlElement("w:numId")
    numId.set(qn("w:val"), str(num_id))
    numPr.append(ilvl)
    numPr.append(numId)
    pPr.insert_element_before(numPr, *_PPR_SUCCESSORS)

    add_runs_with_cmds(p, text, size=size)
    return p


def numbered_paren(doc, items, indent_cm=1.0):
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(indent_cm)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r1 = p.add_run(f"{i}) ")
        set_tnr(r1)
        r2 = p.add_run(text)
        set_tnr(r2)


def add_runs_with_cmds(p, text, size=13):
    parts = re.split(r"(`[^`]+`)", text)
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            r = p.add_run(part[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(size)
            r.font.color.rgb = RGBColor.from_string("C0392B")
            rpr = r._element.get_or_add_rPr()
            rfonts = rpr.find(qn("w:rFonts"))
            if rfonts is None:
                rfonts = OxmlElement("w:rFonts")
                rpr.append(rfonts)
            for attr in ("w:ascii", "w:hAnsi", "w:cs"):
                rfonts.set(qn(attr), "Consolas")
        else:
            r = p.add_run(part)
            set_tnr(r, size=size)


def add_callout(doc, text, fill="EEF4FB", border="0071E3"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        if side == "left":
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "28")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), border)
        else:
            el.set(qn("w:val"), "nil")
        tcBorders.append(el)
    tcPr.append(tcBorders)

    set_cell_bg(cell, fill)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    set_tnr(r, size=13)

    doc.add_paragraph()


def add_data_table(doc, headers, rows, widths_cm):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    for i, w in enumerate(widths_cm):
        tbl.columns[i].width = Cm(w)

    hdr = tbl.rows[0]
    set_repeat_header(hdr)
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = Cm(widths_cm[i])
        set_cell_bg(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        set_tnr(r, size=12, bold=True, color="FFFFFF")

    for row_data in rows:
        row = tbl.add_row()
        for i, val in enumerate(row_data):
            cell = row.cells[i]
            cell.width = Cm(widths_cm[i])
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            add_runs_with_cmds(p, val, size=12)

    doc.add_paragraph()
    return tbl


def add_image(doc, path, width_cm=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))


# ---------------------------------------------------------------------------
# Побудова документа
# ---------------------------------------------------------------------------
def build():
    img_types  = schema_types()
    img_stages = schema_stages()
    img_time   = schema_time()
    img_forms  = schema_forms()

    doc = Document()

    section = doc.sections[0]
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.0)
    add_footer_page_number(section)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(14)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(5)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Times New Roman")

    # ---------------- Заголовок ----------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("ЛЕКЦІЯ 3. УРОК ІНФОРМАТИКИ В ПОЧАТКОВІЙ ШКОЛІ")
    set_tnr(r, size=16, bold=True, color="1F4E79")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Тема: Урок інформатики в початковій школі. "
                  "Структура уроку інформатики в початкових класах")
    set_tnr(r, size=14, bold=True)

    # ---------------- Мета ----------------
    add_heading(doc, "Мета")
    add_par(doc,
            "сформувати у студентів цілісне уявлення про урок інформатики "
            "як основну форму організації навчання в початковій школі; "
            "розкрити типологію уроків, їхню структуру та хронометраж; "
            "ознайомити з дидактичними, методичними й санітарно-гігієнічними "
            "вимогами до організації уроку в 1–4 класах.")

    # ---------------- Ключові поняття ----------------
    add_heading(doc, "Ключові поняття")
    add_par(doc,
            "урок, структура уроку, тип уроку, дидактична мета, "
            "організаційний момент, актуалізація опорних знань, мотивація, "
            "первинне закріплення, практична робота, рефлексія, "
            "фізкультхвилинка, форми організації навчальної діяльності, "
            "санітарно-гігієнічні вимоги.")

    # ---------------- План лекції ----------------
    add_heading(doc, "План лекції")
    plan_id = new_numbered_list(doc)
    plan = [
        "Урок як основна форма навчання інформатики в початковій школі.",
        "Типологія уроків інформатики в початкових класах.",
        "Загальна структура уроку та характеристика його етапів.",
        "Структура комбінованого уроку інформатики: розподіл навчального часу.",
        "Санітарно-гігієнічні та психолого-педагогічні вимоги до уроку.",
        "Форми організації навчальної діяльності молодших школярів.",
    ]
    for item in plan:
        add_list_item(doc, item, plan_id)

    # =======================================================================
    # Блок 1
    # =======================================================================
    add_heading(doc, "1. Урок як основна форма навчання інформатики",
                color="2E75B6", before=12)
    add_par(doc,
            "У початковій школі урок залишається основною формою організації "
            "навчання. Його тривалість становить 35 хвилин у 1–2 класах і "
            "40 хвилин у 3–4 класах. Інформатика в початкових класах — "
            "пропедевтичний курс: його зміст не зводиться до засвоєння "
            "термінів, а передбачає набуття дитиною досвіду діяльності з "
            "інформаційними об’єктами.")
    add_par(doc,
            "Урок інформатики в початковій школі має подвійну мету: "
            "формування елементарної ІКТ-грамотності та розвиток мислення "
            "учнів — логічного, алгоритмічного, критичного. Провідною "
            "вимогою є діяльнісний характер навчання: не менше 60–70 % "
            "часу уроку учень має бути активним суб’єктом — спостерігати, "
            "пробувати, конструювати, обговорювати.")
    add_callout(doc,
                "Урок інформатики не є «уроком про комп’ютер». Комп’ютер — "
                "лише один із засобів, поряд з картками, роздатковим "
                "матеріалом, зошитом і дошкою. Якщо на уроці немає техніки, "
                "це не скасовує уроку інформатики, але змінює добір методів.")

    # =======================================================================
    # Блок 2
    # =======================================================================
    add_heading(doc, "2. Типологія уроків інформатики", color="2E75B6")
    add_par(doc,
            "Тип уроку визначається його провідною дидактичною метою. "
            "У початковій школі найчастіше використовують комбінований "
            "урок, оскільки він дає змогу поєднати повторення, пояснення та "
            "практичну роботу в межах одного заняття.")
    add_image(doc, img_types)
    add_data_table(
        doc,
        ["Тип уроку", "Провідна дидактична мета", "Частка"],
        [
            ["Урок засвоєння нових знань",
             "сформувати первинні уявлення про об’єкт або спосіб дії", "30 %"],
            ["Урок формування вмінь і навичок",
             "відпрацювати практичні дії за зразком та інструкцією", "35 %"],
            ["Урок узагальнення й систематизації",
             "упорядкувати знання, побудувати зв’язки між темами", "10 %"],
            ["Урок контролю й корекції",
             "перевірити рівень засвоєння, скоригувати типові помилки", "10 %"],
            ["Комбінований урок",
             "поєднати кілька дидактичних цілей в одному уроці", "15 %"],
        ],
        widths_cm=[4.6, 8.4, 2.2],
    )
    add_par(doc,
            "У 1–2 класах переважають уроки з ігровими та казковими "
            "сюжетами, у 3–4 класах зростає частка уроків із самостійною "
            "практичною роботою та елементами проєктної діяльності.")

    # =======================================================================
    # Блок 3
    # =======================================================================
    add_heading(doc, "3. Загальна структура уроку", color="2E75B6")
    add_par(doc,
            "Структура уроку — це впорядкована сукупність етапів, "
            "пов’язаних єдиною дидактичною метою. У методиці розрізняють "
            "три взаємопов’язані підструктури: дидактичну (навчання, "
            "розвиток, виховання), методичну (методи й прийоми на кожному "
            "етапі) та психологічну (увага, сприймання, запам’ятовування, "
            "емоційний стан).")
    add_image(doc, img_stages)
    add_par(doc,
            "Кожен етап виконує свою функцію. Організаційний момент "
            "налаштовує на роботу; актуалізація опорних знань відновлює "
            "потрібний досвід; мотивація створює потребу в новому знанні; "
            "вивчення нового матеріалу формує уявлення; практична робота "
            "переводить уявлення у вміння; підсумок і рефлексія "
            "усвідомлюють результат.")
    add_callout(doc,
                "Структура уроку не є жорстким шаблоном. Послідовність "
                "етапів зберігається, але їхня тривалість і наповнення "
                "змінюються залежно від теми, типу уроку та віку учнів. "
                "Механічне копіювання чужого конспекту без урахування "
                "конкретного класу — типова методична помилка.")

    # =======================================================================
    # Блок 4
    # =======================================================================
    add_heading(doc, "4. Розподіл навчального часу на уроці", color="2E75B6")
    add_par(doc,
            "Хронометраж уроку залежить від його тривалості. У 1–2 класах "
            "урок триває 35 хвилин, у 3–4 класах — 40 хвилин. Найбільш "
            "уразливим є етап практичної роботи за комп’ютером: його "
            "тривалість обмежена гігієнічними нормами, тому решту часу "
            "доцільно розподіляти на підготовку, обговорення та рефлексію.")
    add_data_table(
        doc,
        ["Етап уроку", "1–2 класи, хв", "3–4 класи, хв", "Зміст діяльності"],
        [
            ["Організаційний момент", "2", "2",
             "привітання, перевірка готовності робочих місць"],
            ["Актуалізація опорних знань", "5", "5",
             "коротке повторення попередньої теми"],
            ["Мотивація навчальної діяльності", "3", "3",
             "проблемне запитання, ігрова ситуація"],
            ["Вивчення нового матеріалу", "8", "9",
             "пояснення з демонстрацією на екрані"],
            ["Фізкультхвилинка", "2", "2",
             "вправи для очей і постави"],
            ["Практична робота за комп’ютером", "10", "15",
             "виконання завдань у середовищі"],
            ["Підсумок і рефлексія", "5", "4",
             "обговорення результату, самооцінка"],
        ],
        widths_cm=[5.2, 2.3, 2.3, 5.6],
    )
    add_callout(doc,
                "Фізкультхвилинка — обов’язковий елемент уроку інформатики, "
                "а не «додаток за наявності часу». Її доцільно проводити "
                "безпосередньо перед роботою за комп’ютером і повторно — "
                "після неї. Вправи для очей виконують кожні 10–15 хвилин "
                "роботи з екраном.")

    # =======================================================================
    # Блок 5
    # =======================================================================
    add_heading(doc, "5. Санітарно-гігієнічні та психолого-педагогічні вимоги",
                color="2E75B6")
    add_par(doc,
            "Урок інформатики в початковій школі підпорядковується "
            "санітарним нормам, що стосуються тривалості безперервної "
            "роботи за екраном, відстані до монітора, освітлення та "
            "організації робочого місця. Недотримання цих норм є найбільш "
            "поширеною причиною перевтоми молодших школярів.")
    add_image(doc, img_time)
    add_data_table(
        doc,
        ["Вимога", "1–2 класи", "3–4 класи"],
        [
            ["Безперервна робота за екраном", "до 10–12 хв", "до 15–20 хв"],
            ["Відстань до екрана", "не менше 50 см", "не менше 60 см"],
            ["Кількість фізкультхвилинок", "2", "1–2"],
            ["Вправи для очей", "кожні 10 хв", "кожні 15 хв"],
            ["Пауза після роботи за екраном", "обов’язкова, 5 хв",
             "обов’язкова, 5 хв"],
        ],
        widths_cm=[6.8, 4.4, 4.2],
    )
    add_par(doc,
            "До психолого-педагогічних вимог належать: урахування "
            "вікових можливостей уваги (для першокласника — до 7–10 хвилин "
            "зосередженої роботи), зміна видів діяльності протягом уроку, "
            "переважання наочності й практичних дій над словесним "
            "поясненням, позитивне емоційне підкріплення.")
    add_callout(doc,
                "Екран не замінює дошку, а доповнює її. Найефективнішим є "
                "поєднання: демонстрація на екрані — фіксація ключового "
                "кроку на дошці — повторення дії учнем за комп’ютером. "
                "Тривала демонстрація без участі дітей знижує засвоєння "
                "незалежно від якості матеріалу.")

    # =======================================================================
    # Блок 6
    # =======================================================================
    add_heading(doc, "6. Форми організації навчальної діяльності",
                color="2E75B6")
    add_par(doc,
            "На уроці інформатики в початкових класах доцільно поєднувати "
            "різні форми організації діяльності. Фронтальна робота "
            "забезпечує спільний старт і пояснення; парна — взаємоперевірку "
            "та взаємодопомогу; групова — розподіл ролей у спільному "
            "проєкті; індивідуальна — власний темп і самостійність.")
    add_image(doc, img_forms)
    add_par(doc,
            "Кількість учнів за одним комп’ютером не повинна "
            "перевищувати двох. Парна робота за одним робочим місцем "
            "потребує чіткого розподілу ролей: один виконує дію, інший "
            "контролює й коментує, потім вони міняються місцями. Без "
            "такого розподілу один учень працює, а другий лише "
            "спостерігає.")
    add_callout(doc,
                "Під час практичної роботи вчитель не сидить за власним "
                "комп’ютером, а переміщується між робочими місцями. "
                "Доцільний прийом — короткі цільові обходи: спочатку "
                "перевірити початок роботи в усіх, далі підходити до тих, "
                "хто зупинився або припустився типової помилки.")

    # ---------------- Контрольні питання ----------------
    add_heading(doc, "Контрольні питання")
    q_id = new_numbered_list(doc)
    questions = [
        "Чому урок вважають основною формою організації навчання "
        "інформатики в початковій школі?",
        "Яка тривалість уроку в 1–2 та 3–4 класах і чим вона зумовлена?",
        "Що таке тип уроку і яка ознака є визначальною для його "
        "виокремлення?",
        "Які типи уроків інформатики найчастіше використовують у "
        "початкових класах і чому?",
        "Назвіть основні етапи уроку інформатики та їхнє призначення.",
        "Які три підструктури уроку виокремлюють у методиці?",
        "Скільки часу доцільно відводити на практичну роботу за "
        "комп’ютером у 1–2 та 3–4 класах?",
        "Які санітарно-гігієнічні вимоги висувають до уроку інформатики "
        "в початковій школі?",
        "Чому фізкультхвилинка є обов’язковим елементом уроку "
        "інформатики?",
        "Які форми організації навчальної діяльності доцільно поєднувати "
        "на уроці інформатики?",
        "Як організувати парну роботу учнів за одним комп’ютером?",
        "Яких методичних помилок найчастіше припускаються, копіюючи "
        "готовий конспект уроку?",
    ]
    for q in questions:
        add_list_item(doc, q, q_id)

    # ---------------- Рекомендовані джерела ----------------
    add_heading(doc, "Рекомендовані джерела")
    src_id = new_numbered_list(doc)
    sources = [
        "Морзе Н. В., Барна О. В., Вембер В. П. Інформатика : підручник "
        "для 2 класу закладів загальної середньої освіти. Київ : УОВЦ "
        "«Оріон», 2019.",
        "Ривкінд Й. Я., Лисенко Т. І., Чернікова Л. А., Шакотько В. В. "
        "Інформатика : підручник для 3 класу закладів загальної середньої "
        "освіти. Київ : Генеза, 2020.",
        "Лапінський В. В., Проценко Г. О. Методика навчання інформатики "
        "в початковій школі. Київ : Видавничий дім «Освіта», 2018.",
    ]
    for s in sources:
        add_list_item(doc, s, src_id)

    # ---------------- Збереження ----------------
    filename = "Lektsiia_Urok_informatyky_pochatkova_shkola.docx"
    doc.save(filename)
    print(f"✔ Документ збережено: {filename}")
    print(f"✔ Схеми збережено в папці: {OUT_DIR}/ "
          f"(4 схеми × 2 формати = 8 файлів)")


if __name__ == "__main__":
    build()