# -*- coding: utf-8 -*-
"""
Лекція 12. Основні поняття статистики: вибірка, популяція, параметр, статистика.
Генерує docx-документ + папку output/ зі схемами (PNG + SVG).
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
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ----------------------------------------------------------------------------
# КОНСТАНТИ
# ----------------------------------------------------------------------------
OUT = "output"
os.makedirs(OUT, exist_ok=True)

C_DARK = RGBColor(0x1F, 0x4E, 0x79)
C_MID = RGBColor(0x2E, 0x75, 0xB6)
C_RED = RGBColor(0xC0, 0x39, 0x2B)
C_GRAY = RGBColor(0x86, 0x86, 0x8B)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

S_TEXT = "1D1D1F"
S_GRAY = "86868B"
S_CARD = "F5F5F7"
S_EDGE = "E5E5EA"
S_BLUE = "0071E3"
S_GREEN = "248A3D"
S_ORANGE = "C93400"
S_PURPLE = "6E30A8"
S_RED = "C4001D"

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

ALIGN = {
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
}

# ----------------------------------------------------------------------------
# ГЕНЕРАЦІЯ СХЕМ
# ----------------------------------------------------------------------------
def _card(ax, x, y, w, h, face="#" + S_CARD, edge="#" + S_EDGE, radius=0.18, lw=1.4):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=%.2f" % radius,
        linewidth=lw, edgecolor=edge, facecolor=face, zorder=2,
    )
    ax.add_patch(patch)
    return patch


def _arrow(ax, x1, y1, x2, y2, color="#" + S_BLUE, lw=1.8, ms=16):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
        linewidth=lw, color=color, shrinkA=0, shrinkB=0, zorder=3,
    )
    ax.add_patch(arr)


def _save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220,
                bbox_inches="tight", pad_inches=0.15)
    fig.savefig(os.path.join(OUT, name + ".svg"),
                bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def scheme_population_sample():
    fig = plt.figure(figsize=(10, 4.3), dpi=220)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.3)
    ax.axis("off")

    ax.text(5.0, 4.02, "Генеральна сукупність і вибірка", ha="center", va="center",
            fontsize=15, fontweight="bold", color="#" + S_TEXT)

    # Ліва картка — популяція
    _card(ax, 0.35, 0.85, 3.85, 2.80)
    cx = 0.35 + 3.85 / 2.0
    ax.text(cx, 3.32, "ГЕНЕРАЛЬНА СУКУПНІСТЬ", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#" + S_BLUE)
    ax.text(cx, 2.93, "Популяція — усі об'єкти,", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(cx, 2.58, "що цікавлять дослідника", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(cx, 2.05, "Обсяг: N = 1240", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color="#" + S_BLUE)
    ax.text(cx, 1.55, "Приклад: усі учні 3-х", ha="center", va="center",
            fontsize=11.5, color="#" + S_GRAY)
    ax.text(cx, 1.22, "класів міста", ha="center", va="center",
            fontsize=11.5, color="#" + S_GRAY)

    # Права картка — вибірка
    _card(ax, 5.80, 0.85, 3.85, 2.80)
    cx2 = 5.80 + 3.85 / 2.0
    ax.text(cx2, 3.32, "ВИБІРКА", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#" + S_GREEN)
    ax.text(cx2, 2.93, "Частина популяції,", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(cx2, 2.58, "відібрана для вивчення", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(cx2, 2.05, "Обсяг: n = 120", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color="#" + S_GREEN)
    ax.text(cx2, 1.55, "Приклад: 120 учнів", ha="center", va="center",
            fontsize=11.5, color="#" + S_GRAY)
    ax.text(cx2, 1.22, "із 4 шкіл", ha="center", va="center",
            fontsize=11.5, color="#" + S_GRAY)

    _arrow(ax, 4.35, 2.20, 5.65, 2.20)
    ax.text(5.00, 2.55, "відбір", ha="center", va="center",
            fontsize=11, color="#" + S_GRAY)

    _save(fig, "scheme_01_population_sample")


def scheme_parameter_statistic():
    fig = plt.figure(figsize=(10, 4.5), dpi=220)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    ax.text(5.0, 4.20, "Параметр і статистика: дві мови статистики",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#" + S_TEXT)

    _card(ax, 0.40, 3.30, 4.20, 0.62, face="#E8F1FB", edge="#" + S_BLUE)
    ax.text(2.50, 3.61, "ГЕНЕРАЛЬНА СУКУПНІСТЬ (N)", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#" + S_BLUE)

    _card(ax, 5.40, 3.30, 4.20, 0.62, face="#EAF7EE", edge="#" + S_GREEN)
    ax.text(7.50, 3.61, "ВИБІРКА (n)", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#" + S_GREEN)

    _card(ax, 0.40, 0.55, 4.20, 2.50)
    ax.text(2.50, 2.72, "ПАРАМЕТР", ha="center", va="center",
            fontsize=13.5, fontweight="bold", color="#" + S_BLUE)
    ax.text(2.50, 2.28, "μ — середнє популяції", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(2.50, 1.93, "σ — стандартне відхилення", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(2.50, 1.58, "p — частка", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(2.50, 1.23, "ρ — коефіцієнт кореляції", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(2.50, 0.83, "Невідомий, але сталий", ha="center", va="center",
            fontsize=11.5, color="#" + S_GRAY)

    _card(ax, 5.40, 0.55, 4.20, 2.50)
    ax.text(7.50, 2.72, "СТАТИСТИКА", ha="center", va="center",
            fontsize=13.5, fontweight="bold", color="#" + S_GREEN)
    ax.text(7.50, 2.28, "x̄ — середнє вибірки", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(7.50, 1.93, "s — стандартне відхилення", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(7.50, 1.58, "p̂ — частка", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(7.50, 1.23, "r — коефіцієнт кореляції", ha="center", va="center",
            fontsize=12, color="#" + S_TEXT)
    ax.text(7.50, 0.83, "Обчислена за вибіркою", ha="center", va="center",
            fontsize=11.5, color="#" + S_GRAY)

    _arrow(ax, 4.68, 1.75, 5.32, 1.75, color="#" + S_PURPLE)
    ax.text(5.00, 2.07, "оцінює", ha="center", va="center",
            fontsize=10.5, color="#" + S_GRAY)

    _save(fig, "scheme_02_parameter_statistic")


def scheme_research_stages():
    fig = plt.figure(figsize=(10, 3.0), dpi=220)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.0)
    ax.axis("off")

    ax.text(5.0, 2.72, "Етапи статистичного дослідження", ha="center", va="center",
            fontsize=15, fontweight="bold", color="#" + S_TEXT)

    xs = [0.25, 2.75, 5.25, 7.75]
    w = 2.0
    h = 1.75
    y = 0.35
    titles = ["1. ЗБІР ДАНИХ", "2. ВПОРЯДКУВАННЯ", "3. АНАЛІЗ", "4. ВИСНОВОК"]
    colors = [S_BLUE, S_PURPLE, S_ORANGE, S_GREEN]
    descs = [
        ["спостереження,", "опитування"],
        ["групування,", "таблиці"],
        ["обчислення,", "показники"],
        ["тлумачення,", "рішення"],
    ]

    for i, x in enumerate(xs):
        _card(ax, x, y, w, h)
        ax.text(x + w / 2.0, 1.78, titles[i], ha="center", va="center",
                fontsize=12, fontweight="bold", color="#" + colors[i])
        ax.text(x + w / 2.0, 1.33, descs[i][0], ha="center", va="center",
                fontsize=11.5, color="#" + S_TEXT)
        ax.text(x + w / 2.0, 1.02, descs[i][1], ha="center", va="center",
                fontsize=11.5, color="#" + S_TEXT)
        if i < len(xs) - 1:
            _arrow(ax, x + w + 0.08, 1.22, x + w + 0.42, 1.22, ms=14)

    _save(fig, "scheme_03_research_stages")


def scheme_sample_requirements():
    fig = plt.figure(figsize=(10, 3.3), dpi=220)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.3)
    ax.axis("off")

    ax.text(5.0, 3.02, "Три умови репрезентативної вибірки",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#" + S_TEXT)

    xs = [0.20, 3.60, 7.00]
    w = 2.95
    h = 2.05
    y = 0.35
    titles = ["РЕПРЕЗЕНТАТИВНІСТЬ", "ВИПАДКОВІСТЬ", "ДОСТАТНІЙ ОБСЯГ"]
    colors = [S_BLUE, S_ORANGE, S_GREEN]
    descs = [
        ["склад вибірки", "повторює склад", "популяції"],
        ["кожен об'єкт має", "рівний шанс", "потрапити у вибірку"],
        ["чим більший n,", "тим менша", "похибка"],
    ]

    for i, x in enumerate(xs):
        _card(ax, x, y, w, h)
        ax.text(x + w / 2.0, 2.02, titles[i], ha="center", va="center",
                fontsize=12.5, fontweight="bold", color="#" + colors[i])
        ax.text(x + w / 2.0, 1.60, descs[i][0], ha="center", va="center",
                fontsize=11.5, color="#" + S_TEXT)
        ax.text(x + w / 2.0, 1.25, descs[i][1], ha="center", va="center",
                fontsize=11.5, color="#" + S_TEXT)
        ax.text(x + w / 2.0, 0.92, descs[i][2], ha="center", va="center",
                fontsize=11.5, color="#" + S_TEXT)

    _save(fig, "scheme_04_sample_requirements")


# ----------------------------------------------------------------------------
# ХЕЛПЕРИ DOCX
# ----------------------------------------------------------------------------
def set_run_font(run, name="Times New Roman", size=14, bold=False,
                 italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), name)


TOKEN_RE = re.compile(r"(\*\*.+?\*\*|`.+?`)")


def add_rich(p, text, size=14, color=None, bold=False, italic=False):
    for tok in TOKEN_RE.split(text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            r = p.add_run(tok[2:-2])
            set_run_font(r, size=size, bold=True, italic=italic, color=color)
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            r = p.add_run(tok[1:-1])
            set_run_font(r, name="Consolas", size=max(size - 1.5, 10),
                         bold=bold, color=C_RED)
        else:
            r = p.add_run(tok)
            set_run_font(r, size=size, bold=bold, italic=italic, color=color)


def para(doc, text="", size=14, bold=False, italic=False, color=None,
         align="justify", before=0, after=5, line=1.15,
         left=None, first=None, style=None):
    p = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.alignment = ALIGN[align]
    if left is not None:
        pf.left_indent = Cm(left)
    if first is not None:
        pf.first_line_indent = Cm(first)
    if text:
        add_rich(p, text, size=size, color=color, bold=bold, italic=italic)
    return p


def spacer(doc, pts=6):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(pts)
    pf.line_spacing = Pt(2)
    return p


def h1(doc, text, before=14, after=6):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.15
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size=14, bold=True, color=C_DARK)
    return p


def h2(doc, text, before=12, after=6):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.15
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size=14, bold=True, color=C_MID)
    return p


def bullet(doc, text, size=14, indent=1.0, after=3):
    p = doc.add_paragraph(style="List Bullet")
    pf = p.paragraph_format
    pf.left_indent = Cm(indent)
    pf.first_line_indent = Cm(-0.6)
    pf.space_before = Pt(0)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.15
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_rich(p, text, size=size)
    return p


def new_numbering(doc, indent_cm=1.0):
    numbering = doc.part.numbering_part.element

    abs_ids = [int(a.get(qn("w:abstractNumId")))
               for a in numbering.findall(qn("w:abstractNum"))]
    new_abs = (max(abs_ids) + 1) if abs_ids else 0

    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(new_abs))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)

    lvl = OxmlElement("w:lvl")
    lvl.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    lvl.append(start)
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), "decimal")
    lvl.append(num_fmt)
    lvl_text = OxmlElement("w:lvlText")
    lvl_text.set(qn("w:val"), "%1.")
    lvl.append(lvl_text)
    lvl_jc = OxmlElement("w:lvlJc")
    lvl_jc.set(qn("w:val"), "left")
    lvl.append(lvl_jc)

    pPr = OxmlElement("w:pPr")
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), str(int(indent_cm * 567)))
    ind.set(qn("w:hanging"), str(int(0.6 * 567)))
    pPr.append(ind)
    lvl.append(pPr)

    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), "Times New Roman")
    rPr.append(rFonts)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "28")
    rPr.append(sz)
    lvl.append(rPr)
    abstract.append(lvl)

    first_num = numbering.find(qn("w:num"))
    if first_num is not None:
        first_num.addprevious(abstract)
    else:
        numbering.append(abstract)

    num_ids = [int(n.get(qn("w:numId"))) for n in numbering.findall(qn("w:num"))]
    new_num = (max(num_ids) + 1) if num_ids else 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(new_num))
    abs_ref = OxmlElement("w:abstractNumId")
    abs_ref.set(qn("w:val"), str(new_abs))
    num.append(abs_ref)
    numbering.append(num)
    return new_num


def num_list(doc, items, size=14, indent=1.0):
    num_id = new_numbering(doc, indent_cm=indent)
    for item in items:
        p = doc.add_paragraph(style="List Number")
        pPr = p._p.get_or_add_pPr()
        numPr = OxmlElement("w:numPr")
        ilvl = OxmlElement("w:ilvl")
        ilvl.set(qn("w:val"), "0")
        nid = OxmlElement("w:numId")
        nid.set(qn("w:val"), str(num_id))
        numPr.append(ilvl)
        numPr.append(nid)
        pStyle = pPr.find(qn("w:pStyle"))
        if pStyle is not None:
            pStyle.addnext(numPr)
        else:
            pPr.insert(0, numPr)
        pf = p.paragraph_format
        pf.left_indent = Cm(indent)
        pf.first_line_indent = Cm(-0.6)
        pf.space_before = Pt(0)
        pf.space_after = Pt(3)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_rich(p, item, size=size)


def numbered_paren(doc, items, size=14, indent=1.0):
    """Обладнання: 1), 2), 3) ..."""
    for i, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(indent)
        pf.first_line_indent = Cm(-0.6)
        pf.space_before = Pt(0)
        pf.space_after = Pt(3)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run("%d) " % i)
        set_run_font(r, size=size, bold=False)
        add_rich(p, item, size=size)


def _insert_before(parent, el, successor_tags):
    for tag in successor_tags:
        found = parent.find(qn(tag))
        if found is not None:
            found.addprevious(el)
            return
    parent.append(el)


def set_cell_bg(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    old = tcPr.find(qn("w:shd"))
    if old is not None:
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    _insert_before(tcPr, shd, ["w:noWrap", "w:tcMar", "w:textDirection",
                               "w:tcFitText", "w:vAlign", "w:hideMark"])


def set_cell_borders(cell, borders):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement("w:" + edge)
        if edge in borders:
            sz, color = borders[edge]
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), color)
        else:
            el.set(qn("w:val"), "nil")
        tcBorders.append(el)
    _insert_before(tcPr, tcBorders, ["w:shd", "w:noWrap", "w:tcMar",
                                     "w:textDirection", "w:tcFitText",
                                     "w:vAlign", "w:hideMark"])


def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def callout(doc, text, fill="EAF2FB", edge=S_BLUE):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(16.5)
    set_cell_bg(cell, fill)
    set_cell_borders(cell, {"left": (28, edge)})
    p = cell.paragraphs[0]
    pf = p.paragraph_format
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.15
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_rich(p, text, size=13)
    spacer(doc, 6)


def make_table(doc, headers, rows, widths, size=12, header_size=12,
               header_fill="1F4E79"):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    hdr = tbl.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = Cm(widths[i])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_bg(cell, header_fill)
        p = cell.paragraphs[0]
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.space_before = Pt(3)
        pf.space_after = Pt(3)
        pf.line_spacing = 1.0
        add_rich(p, h, size=header_size, color=C_WHITE, bold=True)
    set_repeat_header(hdr)

    for row_data in rows:
        row = tbl.add_row()
        for i, val in enumerate(row_data):
            cell = row.cells[i]
            cell.width = Cm(widths[i])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            pf = p.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.space_before = Pt(2)
            pf.space_after = Pt(2)
            pf.line_spacing = 1.0
            add_rich(p, val, size=size)

    for i, w in enumerate(widths):
        tbl.columns[i].width = Cm(w)
    spacer(doc, 8)
    return tbl


def add_scheme(doc, path, number, caption, width=15.8):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(4)
    pf.space_after = Pt(2)
    pf.line_spacing = 1.0
    run = p.add_run()
    run.add_picture(path, width=Cm(width))
    para(doc, "Схема %d. %s" % (number, caption), size=11, italic=True,
         align="center", after=8, color=C_GRAY, line=1.0)


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run_font(run, size=12, color=C_GRAY)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)


# ----------------------------------------------------------------------------
# ЗБІРКА ДОКУМЕНТА
# ----------------------------------------------------------------------------
def build_document():
    doc = Document()

    section = doc.sections[0]
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(1.5)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    add_page_number_footer(section)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(14)
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), "Times New Roman")
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ---------------- Заголовок ----------------
    para(doc,
         "ЛЕКЦІЯ 12. ОСНОВНІ ПОНЯТТЯ СТАТИСТИКИ: ВИБІРКА, ПОПУЛЯЦІЯ, "
         "ПАРАМЕТР, СТАТИСТИКА",
         size=14, bold=True, color=C_DARK, align="center", after=4)

    para(doc,
         "Тема: Основні поняття статистики: вибірка, популяція, параметр, статистика",
         size=14, bold=True, align="center", after=8)

    para(doc,
         "**Мета:** формувати знання про основні поняття статистики — вибірку, "
         "популяцію, параметр, статистику; розвивати статистичне мислення та "
         "розуміння кількісних характеристик педагогічних явищ; виховувати "
         "точність і коректність у використанні статистичних понять.",
         after=4)

    para(doc, "**Обладнання:** інструкційні картки.", after=4)

    para(doc,
         "**Ключові поняття:** статистика, статистичні дані, генеральна "
         "сукупність (популяція), вибірка, обсяг вибірки, репрезентативність, "
         "випадковий відбір, параметр, статистика (вибіркова оцінка), вибіркова "
         "мінливість, похибка вибірки, середнє арифметичне, стандартне "
         "відхилення, частка.", after=6)

    # ---------------- План ----------------
    h1(doc, "План лекції")
    num_list(doc, [
        "Статистика як наука: предмет, завдання і місце в педагогічному дослідженні.",
        "Генеральна сукупність (популяція) і вибірка. Обсяг та способи формування вибірки.",
        "Параметр і статистика: відмінність, позначення, приклади.",
        "Репрезентативність вибірки, вибіркова мінливість і похибка вибірки.",
        "Наскрізний приклад: від популяції до коректного статистичного висновку.",
    ], size=14)

    # ---------------- Блок 1 ----------------
    h2(doc, "1. Статистика як наука: предмет, завдання і місце в педагогічному дослідженні")

    para(doc,
         "Слово «статистика» походить від латинського `status` — «стан». У "
         "сучасній науці воно має два значення. По-перше, це галузь знань про "
         "збирання, впорядкування, аналіз і тлумачення масових кількісних даних. "
         "По-друге, це самі дані, упорядковані за певними правилами. Для "
         "педагога-дослідника важливі обидва значення: він і збирає статистику "
         "(дані), і користується статистикою (методами).")

    para(doc,
         "Навіщо це вчителю початкової школи? Щоденна робота вчителя — це "
         "безперервний потік кількісних фактів: скільки учнів класу виконали "
         "завдання, який середній час витрачають третьокласники на одну вправу, "
         "як розподілилися оцінки за діагностичну роботу, чи справді інтерактивна "
         "гра підвищила результати. Без статистики ці факти залишаються "
         "розрізненими враженнями («здається, цей клас слабший»); зі статистикою "
         "вони перетворюються на перевірювані твердження.")

    para(doc,
         "Статистичне дослідження завжди проходить чотири етапи (схема 1). "
         "Зверніть увагу: обчислення — лише третій етап. Найбільше помилок у "
         "студентських роботах виникає не через арифметику, а через неякісний "
         "збір даних і поспішну інтерпретацію.")

    add_scheme(doc, os.path.join(OUT, "scheme_03_research_stages.png"), 1,
               "Етапи статистичного дослідження")

    para(doc,
         "Простий приклад. Учитель провів діагностичну роботу з інформатики у "
         "3-А класі (28 учнів). Отримано 28 чисел — це дані. Далі вчитель "
         "упорядкував їх, обчислив середній бал (8,4 з 12) і частку учнів, які "
         "виконали роботу на достатньому рівні (0,71). Тепер у нього є не 28 "
         "окремих результатів, а два показники, з якими можна працювати: "
         "порівнювати з паралельним класом, відстежувати динаміку, планувати "
         "корекційну роботу.")

    para(doc,
         "Пояснюючи учням суть статистики, доречно використати аналогію з "
         "колекцією намистин: спочатку намистини лежать у купі (дані), потім їх "
         "розкладають за кольором (упорядкування), рахують кожну групу (аналіз) і "
         "роблять висновок, яких намистин найбільше (інтерпретація). Така сама "
         "логіка лежить в основі будь-якого, навіть найскладнішого, статистичного "
         "дослідження.")

    callout(doc,
            "Дані — це ще не висновок. 28 оцінок у журналі перетворюються на "
            "знання лише тоді, коли їх упорядковано, узагальнено й пояснено. "
            "Пропущений етап упорядкування робить будь-які обчислення "
            "беззмістовними.")

    # ---------------- Блок 2 ----------------
    h2(doc, "2. Генеральна сукупність (популяція) і вибірка")

    para(doc,
         "**Генеральна сукупність (популяція)** — це вся множина об'єктів, щодо "
         "яких дослідник хоче зробити висновок. Приклади з педагогічної практики: "
         "усі учні третіх класів міста; усі вчителі початкової школи області; усі "
         "завдання з теми «Алгоритми» в підручнику; усі уроки інформатики за "
         "чверть в одній школі. Кількість об'єктів у популяції називають обсягом "
         "і позначають великою латинською літерою `N`.")

    para(doc,
         "**Вибірка** — це частина генеральної сукупності, відібрана для "
         "безпосереднього вивчення. Її обсяг позначають малою латинською літерою "
         "`n`. Вибірка виконує роль «представника» популяції в дослідженні: ми "
         "вивчаємо невелику частину, а висновок поширюємо на ціле.")

    para(doc,
         "Чому дослідник рідко вивчає всю популяцію? Причин три. "
         "**Недоступність** — усі вчителі країни фізично недосяжні для одного "
         "дослідника. **Вартість** — час, зусилля й кошти зростають пропорційно "
         "обсягу. **Руйнівність** — іноді повне обстеження змінює сам об'єкт "
         "(наприклад, тестування всіх учнів класу забирає урок, який планували "
         "на вивчення нового матеріалу). Водночас вибірка дає змогу дійти "
         "висновку про популяцію лише за однієї умови — репрезентативності.")

    add_scheme(doc, os.path.join(OUT, "scheme_01_population_sample.png"), 2,
               "Співвідношення генеральної сукупності та вибірки")

    para(doc,
         "Побутова аналогія, зрозуміла навіть молодшим школярам: щоб оцінити "
         "смак борщу, не потрібно з'їсти всю каструлю — достатньо ложки. Але "
         "ложку треба взяти після ретельного перемішування: якщо зачерпнути з "
         "поверхні, можна набрати самісінького жиру й зробити хибний висновок. "
         "Перемішування в статистиці — це випадковий відбір.")

    para(doc,
         "Спосіб формування вибірки визначає, наскільки їй можна довіряти. "
         "Розгляньмо чотири основні способи (таблиця 1).")

    make_table(
        doc,
        ["Спосіб формування", "Як діє дослідник", "Приклад у школі"],
        [
            ["Проста випадкова",
             "Кожен об'єкт має рівний шанс потрапити до вибірки; "
             "використовують жеребкування або генератор випадкових чисел",
             "Із 1240 учнів програма випадково обирає 120 номерів у списку"],
            ["Стратифікована",
             "Популяцію поділяють на групи (страти) і з кожної беруть "
             "пропорційну частку",
             "Окремо відбирають учнів міських і сільських шкіл у тій самій "
             "пропорції, що й у популяції"],
            ["Кластерна (гніздова)",
             "Одиниця відбору — не окремий учень, а цілий клас або школа",
             "Обирають 4 школи і тестують усіх третьокласників цих шкіл"],
            ["Систематична",
             "Відбирають кожен k-й елемент упорядкованого списку",
             "Кожного 10-го учня зі списку за журналом"],
        ],
        widths=[4.2, 7.0, 5.3],
        size=12,
    )

    callout(doc,
            "Вибірка «за зручністю» — лише свій клас, лише знайомі вчителі, лише "
            "ті, хто погодився, — майже завжди зміщена: вона відображає не "
            "популяцію, а той осередок, з якого її взято.",
            fill="FDECEA", edge=S_RED)

    # ---------------- Блок 3 ----------------
    h2(doc, "3. Параметр і статистика: відмінність, позначення, приклади")

    para(doc,
         "**Параметр** — це числова характеристика генеральної сукупності. "
         "Параметр описує популяцію повністю, тому є для дослідника істинним, але, "
         "як правило, невідомим значенням. Параметри позначають грецькими "
         "літерами: `μ` (мю) — середнє, `σ` (сигма) — стандартне відхилення, "
         "`p` — частка, `ρ` (ро) — коефіцієнт кореляції.")

    para(doc,
         "**Статистика** (вибіркова статистика, оцінка) — це числова "
         "характеристика, обчислена за даними вибірки. Її позначають латинськими "
         "літерами: `x̄` — вибіркове середнє, `s` — вибіркове стандартне "
         "відхилення, `p̂` — вибіркова частка, `r` — вибірковий коефіцієнт "
         "кореляції.")

    add_scheme(doc, os.path.join(OUT, "scheme_02_parameter_statistic.png"), 3,
               "Відповідність параметрів і вибіркових статистик")

    para(doc,
         "Ключова відмінність полягає в природі величини. Параметр — сталий "
         "(хоча й невідомий). Статистика — випадкова, бо залежить від того, які "
         "саме об'єкти потрапили до вибірки. Одна й та сама статистика, обчислена "
         "за різними вибірками з однієї популяції, дає різні числа. Це явище "
         "називають **вибірковою мінливістю**.")

    make_table(
        doc,
        ["Характеристика", "Параметр (популяція)", "Статистика (вибірка)"],
        [
            ["Середнє значення", "μ (мю)", "x̄ (ікс з рискою)"],
            ["Стандартне відхилення", "σ (сигма)", "s"],
            ["Частка", "p (пі)", "p̂"],
            ["Коефіцієнт кореляції", "ρ (ро)", "r"],
            ["Обсяг", "N", "n"],
            ["Алфавіт позначень", "грецькі літери", "латинські літери"],
        ],
        widths=[5.0, 5.75, 5.75],
        size=12,
    )

    para(doc,
         "Побутова аналогія: параметр — це «справжня температура тіла людини», "
         "яку ми ніколи не знаємо абсолютно точно; статистика — показник "
         "термометра, який щоразу може відрізнятися на кілька десятих. Ми "
         "користуємося показаннями термометра, але пам'ятаємо, що це оцінка, а не "
         "сама істина.")

    para(doc,
         "Саме тому коректне формулювання висновку звучить не «середній бал "
         "третьокласників міста становить 8,4», а «за даними вибірки середній бал "
         "оцінюється на рівні 8,4 з похибкою ±0,5». Перше твердження претендує на "
         "знання параметра, якого дослідник не має; друге чесно вказує на "
         "вибірковий характер оцінки.")

    callout(doc,
            "Статистика — не сам параметр, а його оцінка. Дві різні вибірки з "
            "однієї популяції дадуть різні значення x̄; це не помилка "
            "дослідника, а фундаментальна властивість вибіркового методу.",
            fill="FFF4E5", edge=S_ORANGE)

    # ---------------- Блок 4 ----------------
    h2(doc, "4. Репрезентативність вибірки, вибіркова мінливість і похибка вибірки")

    para(doc,
         "**Репрезентативність** — це властивість вибірки відтворювати основні "
         "характеристики генеральної сукупності в тих самих пропорціях. Образно "
         "кажучи, репрезентативна вибірка — це мініатюрна копія популяції. Якщо "
         "серед усіх третьокласників міста 40 % навчаються в сільських школах, то "
         "й у репрезентативній вибірці їх має бути приблизно 40 %.")

    add_scheme(doc, os.path.join(OUT, "scheme_04_sample_requirements.png"), 4,
               "Три умови, за яких вибірку можна вважати репрезентативною")

    para(doc,
         "Репрезентативність забезпечують три взаємопов'язані умови (схема 4). "
         "**Випадковість відбору** означає, що кожен об'єкт популяції має рівний "
         "шанс потрапити до вибірки; жоден учень не повинен відбиратися тому, що "
         "він «зручний» або «показовий». **Достатній обсяг** означає, що вибірка "
         "має бути настільки великою, щоб випадкові відхилення взаємно "
         "зрівноважувалися. **Повнота охоплення** означає, що до вибірки мають "
         "потрапити представники всіх груп популяції — хлопчики й дівчатка, "
         "міські й сільські учні, діти з різним рівнем підготовки.")

    para(doc,
         "**Похибка вибірки** (стандартна похибка) — це розбіжність між "
         "статистикою та параметром, зумовлена самим фактом відбору. Вона не є "
         "недбалістю дослідника; вона неминуча. Її величина орієнтовно обернено "
         "пропорційна кореню з обсягу вибірки: `похибка ≈ σ / √n`. Звідси "
         "практичний висновок: щоб зменшити похибку вдвічі, обсяг вибірки треба "
         "збільшити вчетверо.")

    para(doc,
         "Для студентських досліджень орієнтуються на такі практичні межі: "
         "`n ≥ 30` — мінімальний обсяг для застосування більшості статистичних "
         "методів; для порівняння двох груп — не менше 25–30 учнів у кожній; для "
         "кореляційного аналізу — не менше 30–50 спостережень. Ці межі не є "
         "догмою, але вони дисциплінують дослідника й захищають від надто "
         "сміливих висновків на п'яти спостереженнях.")

    callout(doc,
            "Правило орієнтовне: щоб зменшити похибку вибірки вдвічі, обсяг "
            "вибірки треба збільшити вчетверо. Тому збільшення n з 30 до 60 дає "
            "помітний виграш у точності, а з 300 до 330 — майже непомітний.",
            fill="EAF7EE", edge=S_GREEN)

    # ---------------- Блок 5 ----------------
    h2(doc, "5. Наскрізний приклад: від популяції до коректного статистичного висновку")

    para(doc,
         "Розгляньмо типову ситуацію з практики студентки-практикантки. Вона "
         "перевіряє гіпотезу: чи підвищує інтерактивний тренажер швидкість "
         "складання алгоритмів у третьокласників. **Генеральна сукупність** — усі "
         "96 учнів третіх класів школи (`N = 96`). **Вибірка** — 30 учнів 3-А і "
         "3-Б класів (`n = 30`), відібраних випадково зі списків.")

    para(doc,
         "Після проведення діагностичної роботи студентка отримала результати, "
         "подані в таблиці 3. Зверніть увагу на принципову різницю: ліворуч — те, "
         "що дослідниці насправді недоступне, праворуч — те, що вона реально "
         "обчислила.")

    make_table(
        doc,
        ["Показник", "Параметр (усі 96 учнів)", "Статистика (30 учнів)"],
        [
            ["Середній бал (з 12)", "μ — невідомий", "x̄ = 8,4"],
            ["Частка учнів, які виконали роботу", "p — невідома", "p̂ = 0,73"],
            ["Стандартне відхилення", "σ — невідоме", "s = 1,6"],
            ["Обсяг", "N = 96", "n = 30"],
        ],
        widths=[4.5, 6.0, 6.0],
        size=12,
    )

    para(doc,
         "Коректний висновок у звіті виглядає так: «За результатами вибіркового "
         "дослідження (`n = 30`) середній бал становить 8,4 (`s = 1,6`); частка "
         "учнів, які виконали роботу, — 0,73». Істинне значення параметра `μ`, "
         "найімовірніше, лежить у межах приблизно 8,4 ± 0,6. Твердження «середній "
         "бал усіх третьокласників школи дорівнює 8,4» було б статистично "
         "некоректним, адже воно приписує параметру точне значення, якого "
         "дослідниця не отримувала.")

    para(doc,
         "Що сталося б, якби студентка обмежилася п'ятьма учнями? Похибка "
         "зросла б більш ніж удвічі, а висновок про всю школу втратив би "
         "надійність. Саме тому в інструкційній картці до практичної роботи "
         "завжди зазначають мінімальний обсяг вибірки: це не формальність, а "
         "умова, за якої статистичний висновок узагалі має сенс.")

    # ---------------- Контрольні питання ----------------
    h1(doc, "Контрольні питання")
    num_list(doc, [
        "Що вивчає статистика? Наведіть приклад застосування статистики в початковій школі.",
        "Чим відрізняються сирі дані та статистичні показники? Наведіть приклад переходу від одного до іншого.",
        "Дайте означення генеральної сукупності. Наведіть два приклади популяцій з педагогічної практики.",
        "Що називають вибіркою? Якими літерами позначають обсяг популяції та обсяг вибірки?",
        "Назвіть три причини, чому дослідник рідко вивчає всю генеральну сукупність.",
        "Що таке репрезентативність вибірки? Які три умови її забезпечують?",
        "Охарактеризуйте просту випадкову, стратифіковану та кластерну вибірки. Наведіть шкільний приклад кожної.",
        "Що таке параметр? Якими літерами його позначають і чому саме ними?",
        "Що таке статистика (вибіркова оцінка)? Чому її позначають латинськими літерами?",
        "Поясніть різницю між μ і x̄, між σ і s, між p і p̂.",
        "Що таке похибка вибірки? Від чого вона залежить і як її можна зменшити?",
        "Чому статистика, обчислена за вибіркою, є випадковою величиною, а параметр — ні?",
    ], size=14)

    # ---------------- Джерела ----------------
    h1(doc, "Рекомендовані джерела")
    num_list(doc, [
        "Дубасенюк О. А. Методологія та методи науково-педагогічного дослідження. "
        "Житомир : Полісся, 2016. 256 с.",
        "Методичні рекомендації до виконання та захисту курсових робіт для "
        "здобувачів ОС «Бакалавр» спеціальності 012 «Дошкільна освіта» / уклад. "
        "Н. В. Лісневська, Л. П. Загородня, С. А. Тітаренко, І. Г. Данильченко, "
        "І. В. Корякіна, Н. М. Гордій. Глухів, 2023. 65 с.",
        "Руденко В. М. Математична статистика. Київ : Центр учбової літератури, "
        "2012. 304 с.",
    ], size=14)

    filename = "Лекція_12_Статистика_вибірка_популяція_параметр.docx"
    doc.save(filename)
    return filename


if __name__ == "__main__":
    scheme_population_sample()
    scheme_parameter_statistic()
    scheme_research_stages()
    scheme_sample_requirements()

    name = build_document()
    print("Готово!")
    print("Документ збережено:", os.path.abspath(name))
    print("Схеми (PNG + SVG) збережено в папці:", os.path.abspath(OUT))