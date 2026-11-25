# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Календарно-тематичне планування, схема календарного плану
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


def _card_single(ax, x, y, w, h, text, accent, fs=13):
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
    ax.text(x + w / 2, y + h / 2 - 0.04, text,
            ha="center", va="center", fontsize=fs,
            color=TEXT, fontweight="bold")


def _arrow(ax, x1, y1, x2, y2, color=GREY):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=20,
        linewidth=1.6, color=color, shrinkA=0, shrinkB=0,
    )
    ax.add_patch(arr)


# ---------------------------------------------------------------------------
# Схема 1: ієрархія нормативних документів
# ---------------------------------------------------------------------------
def schema_hierarchy():
    name = "normative_hierarchy"
    fig, ax = _new_ax(10, 6.4)
    ax.text(5, 6.05, "Від нормативного документа — до плану уроку",
            ha="center", va="center", fontsize=14.5,
            color=TEXT, fontweight="bold")

    steps = [
        ("Базовий навчальний план", BLUE),
        ("Типова освітня програма", PURPLE),
        ("Навчальна програма з інформатики", GREEN),
        ("Календарно-тематичний план", ORANGE),
        ("План (конспект) уроку", RED),
    ]
    cw, ch, dx, dy, x0, y0 = 5.6, 0.88, 0.60, 1.05, 0.50, 4.90

    pos = []
    for i, (label, color) in enumerate(steps):
        x = x0 + dx * i
        y = y0 - dy * i
        _card_single(ax, x, y, cw, ch, label, color)
        pos.append((x, y))

    for i in range(4):
        x1 = pos[i][0] + cw / 2
        y1 = pos[i][1] - 0.02
        x2 = pos[i + 1][0] + cw / 2
        y2 = pos[i + 1][1] + ch + 0.02
        _arrow(ax, x1, y1, x2, y2)

    return _save(fig, name)


# ---------------------------------------------------------------------------
# Схема 2: графи календарно-тематичного плану
# ---------------------------------------------------------------------------
def schema_plan_fields():
    name = "plan_fields"
    fig, ax = _new_ax(11, 5.8)
    ax.text(5.5, 5.45, "Схема календарно-тематичного плану: обов’язкові графи",
            ha="center", va="center", fontsize=14.5,
            color=TEXT, fontweight="bold")

    items = [
        ("Номер уроку",         "порядковий номер\nу межах року",         BLUE),
        ("Дата",                "дата проведення\nабо номер тижня",        PURPLE),
        ("Тема уроку",          "формулювання\nз навчальної програми",     GREEN),
        ("Очікувані результати", "державні вимоги\nдо засвоєння",          ORANGE),
        ("Зміст матеріалу",     "ключові поняття,\nщо вивчаються",         YELLOW),
        ("Діяльність учнів",    "практичні роботи,\nвправи, проєкти",      RED),
    ]
    cw, ch, gx, gy = 3.3, 1.55, 0.35, 0.40
    sx = (11 - (3 * cw + 2 * gx)) / 2

    for i, (t, s, c) in enumerate(items):
        col, row = i % 3, i // 3
        x = sx + col * (cw + gx)
        y = 3.40 - row * (ch + gy)
        _card(ax, x, y, cw, ch, t, s, c, fs_title=13, fs_sub=11)

    return _save(fig, name)


# ---------------------------------------------------------------------------
# Схема 3: алгоритм укладання календарно-тематичного плану
# ---------------------------------------------------------------------------
def schema_algorithm():
    name = "plan_algorithm"
    fig, ax = _new_ax(9.5, 6.8)
    ax.text(4.75, 6.45, "Алгоритм укладання календарно-тематичного плану",
            ha="center", va="center", fontsize=14.5,
            color=TEXT, fontweight="bold")

    steps = [
        ("1. Опрацювати навчальну програму", BLUE),
        ("2. Визначити кількість годин", PURPLE),
        ("3. Розподілити теми за уроками", GREEN),
        ("4. Заповнити таблицю плану", ORANGE),
        ("5. Узгодити й затвердити", RED),
    ]
    cw, ch, gap = 6.6, 1.0, 0.32
    sx = (9.5 - cw) / 2
    y_start = 5.45

    pos = []
    for i, (label, color) in enumerate(steps):
        y = y_start - i * (ch + gap)
        _card_single(ax, sx, y, cw, ch, label, color, fs=13)
        pos.append(y)

    for i in range(4):
        y1 = pos[i] - 0.02
        y2 = pos[i + 1] + ch + 0.02
        _arrow(ax, sx + cw / 2, y1, sx + cw / 2, y2)

    return _save(fig, name)


# ---------------------------------------------------------------------------
# Схема 4: три рівні практичної роботи
# ---------------------------------------------------------------------------
def schema_levels():
    name = "task_levels"
    fig, ax = _new_ax(10, 4.8)
    ax.text(5, 4.45, "Три рівні практичної роботи",
            ha="center", va="center", fontsize=14.5,
            color=TEXT, fontweight="bold")

    levels = [
        ("Рівень 1", "репродуктивний\n≈ 7 хв\n3 бали",  BLUE),
        ("Рівень 2", "продуктивний\n≈ 10 хв\n4 бали",   GREEN),
        ("Рівень 3", "творчий\n≈ 10 хв\n4 бали",        ORANGE),
    ]
    cw, ch, gap = 2.9, 1.9, 0.35
    total = 3 * cw + 2 * gap
    sx = (10 - total) / 2
    y = 1.5

    for i, (t, s, c) in enumerate(levels):
        x = sx + i * (cw + gap)
        _card(ax, x, y, cw, ch, t, s, c, fs_title=13.5, fs_sub=11.5)

    sw, sh = 5.0, 1.0
    sum_x, sum_y = (10 - sw) / 2, 0.22
    box = FancyBboxPatch(
        (sum_x, sum_y), sw, sh,
        boxstyle="round,pad=0,rounding_size=0.18",
        linewidth=1.4, edgecolor=BORDER, facecolor="#EEF4FB",
    )
    ax.add_patch(box)
    ax.text(sum_x + sw / 2, sum_y + sh / 2, "≈ 27 хв  •  13 балів",
            ha="center", va="center", fontsize=13, color=TEXT)

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
_NUM_SEQ = [200]

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
    img_hierarchy = schema_hierarchy()
    img_fields    = schema_plan_fields()
    img_algorithm = schema_algorithm()
    img_levels    = schema_levels()

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
    r = p.add_run("ПРАКТИЧНЕ ЗАНЯТТЯ")
    set_tnr(r, size=16, bold=True, color="1F4E79")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Тема: Календарно-тематичне планування, "
                  "схема календарного плану")
    set_tnr(r, size=14, bold=True)

    # ---------------- Мета ----------------
    add_heading(doc, "Мета")
    add_par(doc,
            "формувати вміння складати календарно-тематичний план з "
            "урахуванням вимог навчальної програми та Базового навчального "
            "плану; розвивати навички прогнозування та раціонального "
            "розподілу навчального матеріалу в часі; виховувати "
            "акуратність, дисциплінованість, відповідальне ставлення до "
            "нормативних документів.")

    # ---------------- Обладнання ----------------
    add_heading(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "Інструкційні картки А, Б, В із зразками календарно-тематичного "
        "плану.",
        "Навчальна програма з інформатики для 1–4 класів (роздруківка).",
        "Витяг з Базового навчального плану початкової школи.",
        "Персональний комп’ютер або ноутбук із текстовим редактором.",
        "Мультимедійний проєктор і екран.",
        "Зошит для практичних робіт і лінійка.",
    ])

    # ---------------- Література ----------------
    add_heading(doc, "Література")
    lit_id = new_numbered_list(doc)
    literature = [
        "Єрьоміна О. В., Єфремова Н. І., Бондаренко О. О. Методика "
        "викладання інформатики в початковій школі : "
        "навчально-методичний посібник. Київ : Генеза, 2015.",
        "Антонова О. Нова українська школа: використання "
        "інформаційно-комунікаційних технологій у 1–2 класах загальної "
        "середньої освіти : навч.-метод. посіб. Київ : Ґенеза, 2019. 96 с.",
        "Ляховська Т. В., Біліченко О. М., Сікорська Л. І. Методика "
        "викладання інформатики в початкових класах : "
        "навчально-методичний посібник. Київ : Видавничий дім «Освіта», "
        "2018.",
    ]
    for item in literature:
        add_list_item(doc, item, lit_id)

    # =======================================================================
    # Теоретичні відомості
    # =======================================================================
    add_heading(doc, "Теоретичні відомості")

    add_heading(doc, "1. Нормативна основа календарного планування",
                color="2E75B6", before=6)
    add_par(doc,
            "Календарно-тематичний план не створюється «з нуля»: він "
            "випливає з документів вищого рівня. Базовий навчальний план "
            "визначає граничну кількість годин на інформатичну освітню "
            "галузь; типова освітня програма встановлює розподіл за "
            "циклами; навчальна програма з інформатики фіксує теми, "
            "очікувані результати та види діяльності. Учитель перетворює "
            "ці вимоги на власний робочий документ — календарно-"
            "тематичний план.")
    add_image(doc, img_hierarchy)
    add_callout(doc,
                "Змінювати формулювання тем навчальної програми в "
                "календарному плані не можна: план має бути впізнаваний "
                "під час перевірки. Уточнювати й конкретизувати "
                "формулювання — можна, скорочувати або переставляти "
                "теми — ні.")

    add_heading(doc, "2. Сутність і функції календарно-тематичного плану",
                color="2E75B6")
    add_par(doc,
            "Календарно-тематичний план — це документ учителя, який "
            "розподіляє зміст навчальної програми за конкретними уроками "
            "на певний період (рік, семестр, чверть). Він виконує чотири "
            "основні функції: планувальну (визначає послідовність "
            "матеріалу), організаційну (узгоджує теми з календарем і "
            "канікулами), контрольно-діагностичну (дає змогу побачити "
            "місце контрольних і практичних робіт) та нормативну "
            "(засвідчує виконання програми).")
    add_par(doc,
            "План складають на навчальний рік, але обов’язково "
            "перевіряють і коригують поквартально. Розбіжність між "
            "запланованою та фактичною кількістю уроків (карантин, "
            "святкові дні, перенесення занять) фіксують у графі "
            "«Примітки» або окремим аркушем коригування.")

    add_heading(doc, "3. Схема календарно-тематичного плану",
                color="2E75B6")
    add_par(doc,
            "Обов’язковий мінімум граф календарно-тематичного плану "
            "визначений нормативними вимогами. Школи можуть доповнювати "
            "схему власними графами (наприклад, «Обладнання», "
            "«Міжпредметні зв’язки»), але не можуть вилучати "
            "обов’язкові.")
    add_image(doc, img_fields)
    add_data_table(
        doc,
        ["Графа", "Що фіксується", "Приклад запису"],
        [
            ["Номер уроку",
             "наскрізна нумерація в межах навчального року",
             "5"],
            ["Дата",
             "дата проведення або номер тижня",
             "12.09 або 3-й тиждень"],
            ["Тема уроку",
             "формулювання з навчальної програми",
             "«Інформація навколо нас»"],
            ["Очікувані результати",
             "державні вимоги до засвоєння теми",
             "розпізнає джерела інформації"],
            ["Зміст матеріалу",
             "ключові поняття, які вивчаються на уроці",
             "інформація, носій інформації"],
            ["Діяльність учнів",
             "практичні роботи, вправи, проєкти, екскурсії",
             "практична робота № 2"],
        ],
        widths_cm=[4.0, 6.0, 6.0],
    )

    add_heading(doc, "4. Алгоритм укладання плану", color="2E75B6")
    add_par(doc,
            "Укладання плану доцільно виконувати за сталою "
            "послідовністю дій. Порушення порядку (наприклад, спроба "
            "відразу заповнювати таблицю без підрахунку годин) майже "
            "завжди призводить до розбіжності між сумою запланованих "
            "уроків і кількістю тижнів у чверті.")
    add_image(doc, img_algorithm)
    add_callout(doc,
                "Кількість уроків у чверті визначають не «на око», а за "
                "календарем: кількість навчальних тижнів у чверті "
                "множать на тижневе навантаження. Якщо на тиждень "
                "відведено одну годину, а в чверті вісім навчальних "
                "тижнів — у плані буде рівно вісім уроків, незалежно від "
                "кількості тем у програмі.")

    add_heading(doc, "5. Розподіл навчального матеріалу в часі",
                color="2E75B6")
    add_par(doc,
            "Розподіляючи матеріал, ураховують логіку теми, вікові "
            "можливості учнів і гігієнічні норми роботи за комп’ютером. "
            "Практичні роботи доцільно ставити не на перший урок теми, а "
            "після засвоєння базових понять. Контрольну роботу планують "
            "на останній тиждень чверті, залишаючи один урок на "
            "корекцію.")
    add_data_table(
        doc,
        ["Чверть", "Годин", "Провідна тема", "Практична складова"],
        [
            ["I", "8", "Інформація навколо нас", "2 практичні роботи"],
            ["II", "8", "Комп’ютер і його складові", "3 практичні роботи"],
            ["III", "10", "Алгоритми і виконавці", "4 практичні роботи"],
            ["IV", "9", "Проєкти та узагальнення",
             "2 практичні, 1 контрольна"],
        ],
        widths_cm=[2.6, 3.0, 6.4, 4.0],
    )
    add_callout(doc,
                "Резерв часу — не «вільні уроки», а спланований запас на "
                "повторення, корекцію та непередбачені пропуски. "
                "Оптимально залишати один-два уроки резерву на чверть і "
                "позначати їх у плані окремим рядком, а не розподіляти "
                "«подрібно» між темами.")

    # =======================================================================
    # Покроковий алгоритм різнорівневих завдань
    # =======================================================================
    add_heading(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    add_par(doc,
            "Практична частина заняття складається з трьох рівнів. "
            "Загальна тривалість — близько 27 хв. Кожен наступний рівень "
            "спирається на результат попереднього.")
    add_image(doc, img_levels)

    # ---- Рівень 1 ----
    add_heading(doc, "Рівень 1 — репродуктивний (≈ 7 хв)",
                color="2E75B6", before=6)
    add_par(doc,
            "Завдання: за інструкційною карткою А заповніть шапку та "
            "перші три рядки календарно-тематичного плану для 1 класу, "
            "дотримуючись зразка.")
    add_data_table(
        doc,
        ["№", "Крок", "Дія", "Результат"],
        [
            ["1", "Отримати картку", "Взяти інструкційну картку А зі зразком",
             "Шаблон плану перед очима"],
            ["2", "Знайти розділ програми",
             "Відкрити навчальну програму, розділ для 1 класу",
             "Перелік тем I чверті"],
            ["3", "Перенести нумерацію",
             "Записати в графу «Номер уроку» числа 1, 2, 3",
             "Три рядки з номерами"],
            ["4", "Вписати теми",
             "Перенести формулювання тем дослівно з програми",
             "Графа «Тема уроку» заповнена"],
            ["5", "Заповнити результати",
             "Скопіювати очікувані результати з програми",
             "Графа «Очікувані результати» заповнена"],
            ["6", "Перевірити",
             "Звірити кількість рядків із кількістю уроків у чверті",
             "Розбіжностей немає"],
        ],
        widths_cm=[1.0, 3.6, 6.6, 4.4],
    )

    # ---- Рівень 2 ----
    add_heading(doc, "Рівень 2 — продуктивний (≈ 10 хв)",
                color="2E75B6", before=6)
    add_par(doc,
            "Завдання: за інструкційною карткою Б самостійно складіть "
            "фрагмент календарно-тематичного плану для 2 класу на "
            "I чверть (8 уроків), розподіливши теми програми за уроками.")
    add_data_table(
        doc,
        ["№", "Крок", "Дія", "Результат"],
        [
            ["1", "Визначити навантаження",
             "Знайти в Базовому навчальному плані кількість годин на "
             "тиждень для 2 класу",
             "1 год на тиждень"],
            ["2", "Порахувати уроки",
             "Помножити кількість навчальних тижнів на тижневе "
             "навантаження",
             "8 уроків у I чверті"],
            ["3", "Виписати теми",
             "Виписати теми I чверті з навчальної програми",
             "Перелік тем для розподілу"],
            ["4", "Розподілити теми",
             "Розподілити теми за 8 уроками з урахуванням логіки",
             "Тема на кожен урок"],
            ["5", "Позначити практичні",
             "Визначити 2 уроки з практичною роботою за комп’ютером",
             "Графа «Діяльність учнів» заповнена"],
            ["6", "Перевірити суму",
             "Порівняти кількість рядків із підрахунком уроків",
             "Сума збігається"],
        ],
        widths_cm=[1.0, 3.6, 6.6, 4.4],
    )

    # ---- Рівень 3 ----
    add_heading(doc, "Рівень 3 — творчий (≈ 10 хв)",
                color="2E75B6", before=6)
    add_par(doc,
            "Завдання: за інструкційною карткою В складіть "
            "календарно-тематичний план для 3 класу на II чверть "
            "(16 уроків) і підготуйте коротке обґрунтування розподілу "
            "годин (1–2 хв усної презентації).")
    add_par(doc, "Вимоги до творчого рівня:", bold=True, after=3)
    add_bullet(doc, "Ураховано тижневе навантаження та кількість "
                    "навчальних тижнів у чверті.")
    add_bullet(doc, "Передбачено 4 практичні роботи за комп’ютером.")
    add_bullet(doc, "Передбачено 1 контрольну роботу та 1 урок корекції.")
    add_bullet(doc, "Залишено 1 урок резерву з окремим позначенням.")
    add_bullet(doc, "Теми сформульовано відповідно до навчальної програми.")
    add_data_table(
        doc,
        ["№", "Крок", "Дія", "Результат"],
        [
            ["1", "Підготувати основу",
             "Накреслити таблицю плану з шістьма графами",
             "Порожня таблиця на 16 рядків"],
            ["2", "Заповнити теми",
             "Розподілити теми II чверті за уроками",
             "16 рядків із темами"],
            ["3", "Розставити практичні",
             "Позначити 4 уроки з практичними роботами",
             "Практичні на місцях"],
            ["4", "Додати контроль",
             "Визначити урок контрольної та урок корекції",
             "Контроль і корекція позначені"],
            ["5", "Обґрунтувати",
             "Сформулювати 3–4 речення про логіку розподілу",
             "Готове усне обґрунтування"],
        ],
        widths_cm=[1.0, 4.2, 6.0, 4.6],
    )

    # ---------------- Критерії оцінювання ----------------
    add_heading(doc, "Критерії оцінювання")
    add_data_table(
        doc,
        ["№", "Критерій", "Бал"],
        [
            ["1", "Рівень 1: шапку і три рядки плану заповнено за зразком",
             "3"],
            ["2", "Рівень 2: фрагмент плану на 8 уроків складено коректно",
             "4"],
            ["3", "Рівень 3: план на 16 уроків відповідає програмі", "3"],
            ["4", "Рівень 3: передбачено практичні, контрольну й резерв", "1"],
            ["5", "Оформлення звіту відповідно до вимог", "2"],
            ["", "Разом", "13"],
        ],
        widths_cm=[0.9, 11.6, 3.0],
    )

    # ---------------- Форма звітності ----------------
    add_heading(doc, "Форма звітності")
    add_par(doc, "Письмовий звіт студента має містити:", after=3)
    add_bullet(doc, "Титульну сторінку (ПІБ, група, тема, дата).")
    add_bullet(doc, "Сформульовану мету роботи.")
    add_bullet(doc, "Заповнену таблицю рівня 1 (3 рядки).")
    add_bullet(doc, "Фрагмент плану для 2 класу на I чверть (8 уроків).")
    add_bullet(doc, "План для 3 класу на II чверть (16 уроків).")
    add_bullet(doc, "Обґрунтування розподілу годин (3–5 речень).")
    add_bullet(doc, "Висновок обсягом 5–7 речень із самооцінкою.")

    # ---------------- Збереження ----------------
    filename = "Praktychne_KTP_kalendarnyi_plan.docx"
    doc.save(filename)
    print(f"✔ Документ збережено: {filename}")
    print(f"✔ Схеми збережено в папці: {OUT_DIR}/ "
          f"(4 схеми × 2 формати = 8 файлів)")


if __name__ == "__main__":
    build()