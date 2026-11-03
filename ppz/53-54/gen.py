# -*- coding: utf-8 -*-
"""
Генератор методичного матеріалу
Практичне заняття № 15. Команда розгалуження.
Запуск:  python practice_15_branching.py
Результат: Практичне_заняття_15_Розгалуження.docx + output/ (схеми PNG + SVG)
"""

import os

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

# ----------------------------------------------------------------------------
OUT = "output"
DOCX_NAME = "Практичне_заняття_15_Розгалуження.docx"

FONT = "Times New Roman"
DARK_BLUE = RGBColor(0x1F, 0x4E, 0x79)
MID_BLUE = RGBColor(0x2E, 0x75, 0xB6)
CODE_RED = RGBColor(0xC0, 0x39, 0x2B)
CODE_DARK = RGBColor(0x1D, 0x1D, 0x1F)
GRAY = RGBColor(0x59, 0x59, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

CARD_BG = "#F5F5F7"
CARD_EDGE = "#E5E5EA"
TEXT_DARK = "#1D1D1F"
TEXT_GRAY = "#86868B"
BLUE = "#0071E3"
GREEN = "#248A3D"
ORANGE = "#C93400"
RED = "#C4001D"
ARROW_GRAY = "#C7C7CC"

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


# ============================================================================
# СХЕМИ
# ============================================================================
def _canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax


def _card(ax, x, y, w, h, lines, bg=CARD_BG, edge=CARD_EDGE, rs=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%s" % rs,
                                linewidth=1.4, edgecolor=edge,
                                facecolor=bg, zorder=2))
    if not lines:
        return
    n = len(lines)
    top = y + h - 0.15
    bottom = y + 0.15
    if n == 1:
        ys = [(top + bottom) / 2.0]
    else:
        step = (top - bottom) / (n - 1)
        ys = [top - i * step for i in range(n)]
    for (text, size, color, weight), yy in zip(lines, ys):
        ax.text(x + w / 2.0, yy, text, ha="center", va="center",
                fontsize=size, color=color, fontweight=weight,
                zorder=3)


def _arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_GRAY, lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=12),
                zorder=1)


def _diamond(ax, cx, cy, w, h, text, fs=10.5):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="#F5F5F7",
                         edgecolor=BLUE, linewidth=1.6, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color=TEXT_DARK, fontweight="bold", zorder=3)


def _save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220,
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(os.path.join(OUT, name + ".svg"),
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


def scheme_branch_idea():
    fig, ax = _canvas(6.3, 2.0)
    _card(ax, 0.15, 0.6, 1.9, 0.8, [
        ("УМОВА", 11, BLUE, "bold"),
        ("оцінка ≥ 60 ?", 9.5, TEXT_DARK, "normal"),
    ])
    _card(ax, 3.6, 1.15, 2.55, 0.6, [
        ("ТАК → «Зараховано»", 10, GREEN, "bold"),
    ])
    _card(ax, 3.6, 0.2, 2.55, 0.6, [
        ("НІ → «Не зараховано»", 10, RED, "bold"),
    ])
    _arrow(ax, 2.08, 1.1, 3.55, 1.45)
    _arrow(ax, 2.08, 0.9, 3.55, 0.5)
    _save(fig, "scheme_01_branch_idea")


def scheme_if_forms():
    fig, ax = _canvas(6.3, 2.3)
    items = [
        ("Скорочена", ["If умова Then", "  дія"], BLUE),
        ("Повна", ["If умова Then", "  дія 1", "Else", "  дія 2"], GREEN),
        ("Багатоваріантна",
         ["If умова 1 Then", "ElseIf умова 2 Then", "Else"], ORANGE),
    ]
    w, gap, y, h = 1.9, 0.2, 0.15, 2.0
    x = 0.1
    for title, code_lines, accent in items:
        content = [(title, 11, accent, "bold")]
        for ln in code_lines:
            content.append((ln, 9, TEXT_DARK, "normal"))
        _card(ax, x, y, w, h, content)
        x += w + gap
    _save(fig, "scheme_02_if_forms")


def scheme_flowchart():
    fig, ax = _canvas(6.3, 2.8)
    _card(ax, 1.65, 2.3, 3.0, 0.42, [
        ("Ввести число N", 10.5, TEXT_DARK, "normal"),
    ])
    _diamond(ax, 3.15, 1.35, 2.2, 0.9, "N > 0 ?", 11)
    _arrow(ax, 3.15, 2.28, 3.15, 1.82)
    _card(ax, 0.15, 0.55, 2.0, 0.5, [
        ("ТАК: Додатне", 10.5, GREEN, "bold"),
    ])
    _arrow(ax, 2.03, 1.18, 1.15, 1.06)
    _card(ax, 4.15, 0.55, 2.0, 0.5, [
        ("НІ: Від'ємне або 0", 10.5, RED, "bold"),
    ])
    _arrow(ax, 4.27, 1.18, 5.15, 1.06)
    _save(fig, "scheme_03_flowchart")


def scheme_levels():
    fig, ax = _canvas(6.3, 1.7)
    items = [
        ("Рівень 1", "Репродуктивний", "≈ 7 хв", BLUE),
        ("Рівень 2", "Продуктивний", "≈ 10 хв", GREEN),
        ("Рівень 3", "Творчий", "≈ 10 хв", ORANGE),
    ]
    w, gap, y, h = 1.9, 0.2, 0.55, 1.0
    x = 0.1
    for t1, t2, t3, accent in items:
        _card(ax, x, y, w, h, [
            (t1, 11, accent, "bold"),
            (t2, 9, TEXT_DARK, "normal"),
            (t3, 9.5, TEXT_GRAY, "normal"),
        ])
        x += w + gap
    ax.text(3.15, 0.25, "Разом: 25–30 хв", ha="center", va="center",
            fontsize=10.5, color=TEXT_DARK, fontweight="bold")
    _save(fig, "scheme_04_levels")


def build_schemes():
    os.makedirs(OUT, exist_ok=True)
    scheme_branch_idea()
    scheme_if_forms()
    scheme_flowchart()
    scheme_levels()


# ============================================================================
# ДОПОМІЖНІ ФУНКЦІЇ DOCX
# ============================================================================
def set_run(run, size=14, bold=False, italic=False, color=None, name=FONT):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), name)


def setup_styles(doc):
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(14)
    rPr = st.element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT)
    pf = st.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(0)
    pf.space_after = Pt(5)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def para(doc, text="", size=14, bold=False, italic=False, color=None,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5,
         left_indent=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    if left_indent is not None:
        pf.left_indent = left_indent
    if text:
        r = p.add_run(text)
        set_run(r, size=size, bold=bold, italic=italic, color=color)
    return p


def para_rich(doc, parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
              space_before=0, space_after=5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    for text, kind in parts:
        r = p.add_run(text)
        if kind == "code":
            set_run(r, size=13, name="Consolas", color=CODE_RED)
        elif kind == "code_dark":
            set_run(r, size=13, name="Consolas", color=CODE_DARK)
        elif kind == "b":
            set_run(r, size=14, bold=True)
        else:
            set_run(r, size=14)
    return p


def heading(doc, text, color=DARK_BLUE, size=14, space_before=12,
            space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT):
    return para(doc, text, size=size, bold=True, color=color, align=align,
                space_before=space_before, space_after=space_after)


def subheading(doc, text):
    return para(doc, text, size=14, bold=True, color=MID_BLUE,
                align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=4)


def numbered_paren(doc, items):
    for i, item in enumerate(items, 1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-0.6)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run("%d) " % i), size=14)
        set_run(p.add_run(item), size=14)


def num_list(doc, items, start=1):
    for i, item in enumerate(items, start):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-0.6)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run("%d. " % i), size=14)
        set_run(p.add_run(item), size=14)


def literature_list(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run(item), size=14)


def bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run(item), size=14)


def set_cell_bg(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def callout(doc, text, fill="EAF2FB", accent="0071E3"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.0)
    tcPr = cell._tc.get_or_add_tcPr()

    borders = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), accent)
    borders.append(left)
    for edge in ("top", "bottom", "right"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "nil")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tcPr.append(borders)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

    p = cell.paragraphs[0]
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing = 1.15
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    set_run(p.add_run(text), size=13.5)
    return tbl


def code_block(doc, lines, indent="", size=11.5):
    """Блок коду: Consolas, світло-сірий фон, тонка рамка."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(16.5)
    tcPr = cell._tc.get_or_add_tcPr()

    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "E5E5EA")
        borders.append(el)
    tcPr.append(borders)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F5F5F7")
    tcPr.append(shd)

    def _fill(p, text):
        p.paragraph_format.space_before = Pt(2 if text is lines[0] else 0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_run(p.add_run(indent + text), size=size, name="Consolas",
                color=CODE_DARK)

    _fill(cell.paragraphs[0], lines[0])
    for line in lines[1:]:
        p = cell.add_paragraph()
        _fill(p, line)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)
    spacer.paragraph_format.space_before = Pt(0)
    return tbl


def styled_table(doc, headers, rows, widths, font_size=12,
                 code_cols=(), center_cols=(0,)):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    tblPr = tbl._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.insert_element_before(layout, "w:tblCellMar", "w:tblLook",
                                "w:tblCaption", "w:tblDescription")

    hdr = tbl.rows[0]
    trPr = hdr._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)

    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = Cm(widths[i])
        set_cell_bg(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        set_run(p.add_run(h), size=font_size, bold=True, color=WHITE)

    for row in rows:
        cells = tbl.add_row().cells
        for i, val in enumerate(row):
            cells[i].width = Cm(widths[i])
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            if i in center_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if not val:
                continue
            if i in code_cols:
                set_run(p.add_run(val), size=font_size - 1, name="Consolas",
                        color=CODE_RED)
            else:
                set_run(p.add_run(val), size=font_size)
    return tbl


def add_page_numbers(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run(run, size=12, color=GRAY)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)


def add_scheme(doc, filename, caption, width_cm=16.0):
    path = os.path.join(OUT, filename)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    set_run(cap.add_run(caption), size=12, italic=True, color=GRAY)


# ============================================================================
# ЗБІРКА ДОКУМЕНТА
# ============================================================================
def build_document():
    doc = Document()
    setup_styles(doc)

    sec = doc.sections[0]
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(1.5)
    add_page_numbers(sec)

    # --- Заголовок -----------------------------------------------------------
    heading(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 15",
            align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4)
    para(doc, "Тема: Команда розгалуження.",
         bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    # --- Мета ----------------------------------------------------------------
    heading(doc, "Мета")
    para(doc, "Навчати використовувати умовний оператор (If…Then…Else) для "
              "створення розгалужених алгоритмів у VBA. Розвивати логічне "
              "мислення, вміння аналізувати умови та приймати рішення в коді. "
              "Виховувати системність, вміння передбачати різні варіанти "
              "розвитку подій.")

    # --- Обладнання ----------------------------------------------------------
    heading(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "персональний комп'ютер або ноутбук;",
        "текстовий редактор Microsoft Word 2016 / 2019 / 2021 або Microsoft 365;",
        "вбудований редактор VBA (Visual Basic for Applications);",
        "інструкційні картки до заняття;",
        "файл-заготовка «Практика_15.docm».",
    ])

    # --- Література ----------------------------------------------------------
    heading(doc, "Література")
    literature_list(doc, [
        "Юнчик В. Л. Системне, прикладне програмне забезпечення та хмарні "
        "технології в освіті : конспект лекцій для студентів спеціальності "
        "014.09 Середня освіта (Інформатика) першого (бакалаврського) рівня. "
        "Волин. нац. ун-т ім. Лесі Українки. Луцьк : ВНУ імені Лесі Українки, "
        "2024. 162 с.",
        "Анісімов А. В., Кулябко П. П. Інформаційні системи та бази даних : "
        "навч. посіб. для студ. ф-ту комп'ютер. наук та кібернетики. Київ, "
        "2017. 110 с.",
        "Буйницька О. П. Інформаційні технології та технічні засоби навчання : "
        "навч. посіб. Київ : Центр навчальної літератури, 2019. 240 с.",
    ])

    # --- Теоретичні відомості ------------------------------------------------
    heading(doc, "Теоретичні відомості")

    subheading(doc, "1.1. Поняття розгалуження в алгоритмах")
    para(doc, "Розгалуження — це алгоритмічна структура, у якій виконання "
              "команд залежить від істинності певної умови. Якщо умова "
              "виконується, програма виконує одні дії, якщо ні — інші. У "
              "повсякденному житті ми щохвилини приймаємо подібні рішення: "
              "«Якщо надворі дощ — беру парасольку, інакше — не беру»; «Якщо "
              "оцінка за тест не менша за 60 балів — студент зарахований, "
              "інакше — ні». Саме такі конструкції реалізує команда "
              "розгалуження в коді (схема 1).")
    add_scheme(doc, "scheme_01_branch_idea.png",
               "Схема 1. Загальна ідея розгалуження")
    callout(doc, "Умова в розгалуженні завжди має один із двох результатів — "
                 "True (істина) або False (хибність). Жодного третього "
                 "варіанту немає, тому й гілок у найпростішому розгалуженні "
                 "лише дві.",
            fill="EAF2FB", accent="0071E3")

    subheading(doc, "1.2. Скорочена форма: If…Then")
    para_rich(doc, [
        ("Якщо дію потрібно виконати лише за істинної умови, застосовують "
         "скорочену форму. Вона записується в один рядок і має вигляд ", "text"),
        ("If умова Then дія", "code"),
        (". Наприклад, повідомлення про успішне складання іспиту:", "text"),
    ])
    code_block(doc, [
        'If score >= 60 Then MsgBox "Зараховано"',
    ])
    para_rich(doc, [
        ("Якщо умова хибна, жодна дія не виконується, і програма переходить "
         "до наступного рядка. Скорочена форма зручна, коли потрібно лише "
         "«відреагувати» на виконання умови, а в іншому разі — нічого не "
         "робити.", "text"),
    ])

    subheading(doc, "1.3. Повна форма: If…Then…Else")
    para(doc, "Коли дій дві й вони взаємовиключні, використовують повну форму "
              "з ключовим словом Else («інакше»). Кожна дія розміщується на "
              "окремому рядку, а весь блок закривається словом End If. "
              "Порівняйте три форми запису оператора (схема 2):")
    add_scheme(doc, "scheme_02_if_forms.png",
               "Схема 2. Форми запису оператора If")
    para(doc, "Приклад повної форми — визначення, чи є число додатним:")
    code_block(doc, [
        "If N > 0 Then",
        '    MsgBox "Число додатне"',
        "Else",
        '    MsgBox "Число від\'ємне або дорівнює нулю"',
        "End If",
    ])
    callout(doc, "Кожен If, записаний у блоковій формі, обов'язково "
                 "закривається End If. Пропущене End If — найпоширеніша "
                 "синтаксична помилка початківців.",
            fill="FFF4E5", accent="C93400")

    subheading(doc, "1.4. Оператори порівняння та логічні оператори")
    para(doc, "Умова в If будується з операторів порівняння (таблиця 1) та "
              "логічних операторів (таблиця 2). Оператори порівняння "
              "повертають True або False, а логічні — дозволяють об'єднувати "
              "кілька умов в одну.")
    styled_table(
        doc,
        ["Оператор", "Значення", "Приклад"],
        [
            ["=", "дорівнює", "x = 10"],
            ["<>", "не дорівнює", "x <> 10"],
            [">", "більше", "x > 10"],
            ["<", "менше", "x < 10"],
            [">=", "більше або дорівнює", "x >= 10"],
            ["<=", "менше або дорівнює", "x <= 10"],
        ],
        widths=[3.0, 6.0, 7.5],
        font_size=12,
        code_cols=(0, 2),
    )
    para(doc, "Таблиця 1. Оператори порівняння", size=12, italic=True,
         color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)
    styled_table(
        doc,
        ["Оператор", "Значення", "Приклад"],
        [
            ["And", "І (обидві умови істинні)", "x > 0 And x < 10"],
            ["Or", "АБО (хоча б одна істинна)", "x < 0 Or x > 100"],
            ["Not", "НЕ (заперечення)", "Not (x = 5)"],
        ],
        widths=[3.0, 6.0, 7.5],
        font_size=12,
        code_cols=(0, 2),
    )
    para(doc, "Таблиця 2. Логічні оператори", size=12, italic=True, color=GRAY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)
    para_rich(doc, [
        ("Приклад: перевірити, чи належить оцінка діапазону від 60 до 100 "
         "балів. Умова матиме вигляд ", "text"),
        ("score >= 60 And score <= 100", "code"),
        (".", "text"),
    ])

    subheading(doc, "1.5. Конструкція ElseIf та вкладені умови")
    para_rich(doc, [
        ("Якщо варіантів розвитку подій більше ніж два, вкладені оператори "
         "If стають громіздкими. Натомість використовують конструкцію ", "text"),
        ("ElseIf", "code"),
        (", яка дозволяє послідовно перевіряти кілька умов. Слово ", "text"),
        ("Else", "code"),
        (" в такій конструкції спрацьовує тоді, коли жодна з попередніх "
         "умов не виконалася (схема 3).", "text"),
    ])
    code_block(doc, [
        "If score >= 90 Then",
        '    MsgBox "Відмінно"',
        "ElseIf score >= 75 Then",
        '    MsgBox "Добре"',
        "ElseIf score >= 60 Then",
        '    MsgBox "Задовільно"',
        "Else",
        '    MsgBox "Незадовільно"',
        "End If",
    ])
    add_scheme(doc, "scheme_03_flowchart.png",
               "Схема 3. Блок-схема розгалуження з двома гілками",
               width_cm=15.0)
    callout(doc, "Порядок перевірки умов ElseIf має значення: VBA перевіряє їх "
                 "згори вниз і зупиняється на першій істинній. Тому умови "
                 "записують від найсильнішої до найслабшої.",
            fill="EAF7EE", accent="248A3D")

    # --- Різнорівневі завдання -----------------------------------------------
    heading(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    para(doc, "Практична частина складається з трьох рівнів, які виконуються "
              "послідовно (схема 4). Кожен наступний рівень спирається на "
              "попередній, тому важливо не пропускати кроків.")
    add_scheme(doc, "scheme_04_levels.png",
               "Схема 4. Три рівні практичної частини", width_cm=15.5)

    # --- Рівень 1 ------------------------------------------------------------
    subheading(doc, "Рівень 1. Репродуктивний (≈ 7 хв)")
    para_rich(doc, [
        ("Завдання. ", "b"),
        ("Записати макрос ", "text"),
        ("CheckGrade", "code"),
        (", який за введеним числом балів (0–100) виводить повідомлення "
         "«Зараховано», якщо балів не менше ніж 60, і «Не зараховано» в "
         "іншому разі. Використати скорочену та повну форму оператора "
         "If.", "text"),
    ])
    para(doc, "Орієнтовний шаблон коду для доопрацювання:")
    code_block(doc, [
        "Sub CheckGrade()",
        "    Dim score As Integer",
        "    score = InputBox(\"Введіть кількість балів (0-100)\")",
        "",
        "    If score >= 60 Then",
        "        MsgBox \"Зараховано\", vbInformation",
        "    Else",
        "        MsgBox \"Не зараховано\", vbCritical",
        "    End If",
        "End Sub",
    ])
    para(doc, "Послідовність виконання наведено в таблиці 3.")
    styled_table(
        doc,
        ["№", "Дія", "Команда / шлях", "Результат"],
        [
            ["1", "Відкрити файл-заготовку",
             "Практика_15.docm", "Документ Word із підтримкою макросів"],
            ["2", "Відкрити редактор VBA", "Alt+F11", "Вікно Microsoft Visual Basic"],
            ["3", "Додати модуль",
             "Insert → Module", "У проєкті з'явився Module1"],
            ["4", "Ввести код процедури",
             "код CheckGrade (див. вище)", "Код набрано в редакторі"],
            ["5", "Запустити макрос", "F5 або Run → Run Sub",
             "З'явиться діалог InputBox"],
            ["6", "Перевірити роботу",
             "ввести 75, потім 40", "Отримано два різні повідомлення"],
            ["7", "Зберегти файл",
             "Ctrl+S", "Макрос збережено в .docm"],
        ],
        widths=[1.0, 3.6, 5.9, 6.5],
        font_size=11,
        code_cols=(2,),
    )
    para(doc, "Таблиця 3. Кроки виконання завдання рівня 1", size=12,
         italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)

    # --- Рівень 2 ------------------------------------------------------------
    subheading(doc, "Рівень 2. Продуктивний (≈ 10 хв)")
    para_rich(doc, [
        ("Завдання. ", "b"),
        ("Записати макрос ", "text"),
        ("AgeGroup", "code"),
        (", який за номером класу початкової школи (1–4) визначає вікову "
         "групу учня. Використати конструкцію ", "text"),
        ("ElseIf", "code"),
        (". Передбачити перевірку на некоректно введене число (менше за 1 "
         "або більше за 4).", "text"),
    ])
    para(doc, "Орієнтовний шаблон коду для доопрацювання:")
    code_block(doc, [
        "Sub AgeGroup()",
        "    Dim k As Integer",
        "    k = InputBox(\"Введіть номер класу (1-4)\")",
        "",
        "    If k = 1 Then",
        '        MsgBox "Вік: 6-7 років"',
        "    ElseIf k = 2 Then",
        '        MsgBox "Вік: 7-8 років"',
        "    ElseIf k = 3 Then",
        '        MsgBox "Вік: 8-9 років"',
        "    ElseIf k = 4 Then",
        '        MsgBox "Вік: 9-10 років"',
        "    Else",
        '        MsgBox "Некоректний номер класу", vbExclamation',
        "    End If",
        "End Sub",
    ])
    para(doc, "Кроки виконання — у таблиці 4.")
    styled_table(
        doc,
        ["№", "Дія", "Команда / шлях", "Результат"],
        [
            ["1", "Додати новий модуль",
             "Insert → Module", "Створено Module2"],
            ["2", "Ввести код AgeGroup",
             "код процедури (див. вище)", "Код набрано в редакторі"],
            ["3", "Запустити макрос", "F5",
             "З'явиться діалог введення номера класу"],
            ["4", "Перевірити всі гілки",
             "по черзі ввести 1, 2, 3, 4", "Отримано чотири різні повідомлення"],
            ["5", "Перевірити Else-гілку",
             "ввести 0, а потім 7", "Повідомлення про некоректний номер"],
            ["6", "Зберегти файл", "Ctrl+S", "Зміни збережено"],
        ],
        widths=[1.0, 3.6, 5.9, 6.5],
        font_size=11,
        code_cols=(2,),
    )
    para(doc, "Таблиця 4. Кроки виконання завдання рівня 2", size=12,
         italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)
    callout(doc, "Перевіряйте макрос не лише на «правильних», а й на "
                 "граничних та некоректних значеннях. Це виявляє помилки "
                 "логіки, які не видні на типових прикладах.",
            fill="EAF2FB", accent="0071E3")

    # --- Рівень 3 ------------------------------------------------------------
    subheading(doc, "Рівень 3. Творчий (≈ 10 хв)")
    para_rich(doc, [
        ("Завдання. ", "b"),
        ("Розробити макрос ", "text"),
        ("GradeByScore", "code"),
        (", який за 100-бальною шкалою визначає рівень навчальних досягнень "
         "учня й повертає відповідне повідомлення. Передбачити:", "text"),
    ])
    num_list(doc, [
        "перевірку діапазону введення (від 0 до 100) — інакше виводити "
        "попередження;",
        "п'ять рівнів: A (90–100), B (80–89), C (70–79), D (60–69), "
        "E (50–59), F (менше ніж 50);",
        "використання MsgBox із різними іконками (vbInformation, "
        "vbExclamation, vbCritical) залежно від результату;",
        "коментарі до кожного логічного блоку.",
    ])
    para(doc, "Орієнтовний каркас:")
    code_block(doc, [
        "Sub GradeByScore()",
        "    Dim s As Integer",
        "    s = InputBox(\"Введіть бал (0-100)\")",
        "",
        "    ' Перевірка діапазону",
        "    If s < 0 Or s > 100 Then",
        '        MsgBox "Некоректне значення!", vbCritical',
        "        Exit Sub",
        "    End If",
        "",
        "    If s >= 90 Then",
        '        MsgBox "Рівень A", vbInformation',
        "    ElseIf s >= 80 Then",
        '        MsgBox "Рівень B", vbInformation',
        "    ElseIf s >= 70 Then",
        '        MsgBox "Рівень C"',
        "    ElseIf s >= 60 Then",
        '        MsgBox "Рівень D"',
        "    ElseIf s >= 50 Then",
        '        MsgBox "Рівень E", vbExclamation',
        "    Else",
        '        MsgBox "Рівень F", vbCritical',
        "    End If",
        "End Sub",
    ])
    para(doc, "Вимоги до результату роботи наведено в таблиці 5.")
    styled_table(
        doc,
        ["Критерій перевірки", "Очікуваний результат"],
        [
            ["Введено 95", "Повідомлення «Рівень A» з іконкою Information"],
            ["Введено 65", "Повідомлення «Рівень D»"],
            ["Введено 49", "Повідомлення «Рівень F» з іконкою Critical"],
            ["Введено -5 або 200", "Повідомлення «Некоректне значення!»"],
            ["Порожнє введення", "Макрос завершується без помилки"],
            ["Читабельність коду",
             "Наявні коментарі до кожного логічного блоку"],
        ],
        widths=[6.0, 11.0],
        font_size=12,
        center_cols=(),
    )
    para(doc, "Таблиця 5. Критерії перевірки творчого завдання", size=12,
         italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)
    callout(doc, "Оператор Exit Sub достроково завершує виконання процедури. "
                 "Він корисний, коли вхідні дані некоректні й подальші "
                 "перевірки втрачають сенс.",
            fill="FFF4E5", accent="C93400")

    # --- Критерії оцінювання -------------------------------------------------
    heading(doc, "Критерії оцінювання")
    styled_table(
        doc,
        ["№", "Критерій", "Бали"],
        [
            ["1", "Рівень 1: макрос CheckGrade із повною формою If…Then…Else",
             "3"],
            ["2", "Рівень 2: макрос AgeGroup із конструкцією ElseIf та "
                  "перевіркою Else", "4"],
            ["3", "Рівень 3: макрос GradeByScore з валідацією діапазону, "
                  "іконками MsgBox і коментарями", "4"],
            ["4", "Оформлення звіту, наявність скріншотів, сформульовані "
                  "висновки", "2"],
            ["", "Разом", "13"],
        ],
        widths=[1.0, 13.5, 2.5],
        font_size=12,
    )
    para(doc, "Таблиця 6. Критерії та бали", size=12, italic=True, color=GRAY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)

    # --- Форма звітності -----------------------------------------------------
    heading(doc, "Форма звітності")
    para(doc, "За результатами заняття студент подає два файли:")
    bullets(doc, [
        "файл із макросами — Практика_15_Прізвище.docm (містить усі три "
        "процедури: CheckGrade, AgeGroup, GradeByScore);",
        "звіт — ПЗ15_Прізвище.docx, оформлений у текстовому редакторі Word "
        "(Times New Roman, 14 pt, інтервал 1,15).",
    ])
    para(doc, "Структура звіту:")
    num_list(doc, [
        "тема та мета роботи;",
        "коротке пояснення призначення конструкцій If…Then, "
        "If…Then…Else, ElseIf (3–5 речень);",
        "код кожної з трьох процедур із коментарями;",
        "скріншоти вікон MsgBox для кожного рівня (не менше ніж 4);",
        "опис виявлених труднощів та способів їх подолання;",
        "висновки (4–6 речень): де в роботі вчителя початкової школи "
        "доречно застосовувати розгалуження.",
    ])

    doc.save(DOCX_NAME)
    print("Готово: створено файл '%s'." % DOCX_NAME)
    print("Схеми збережено у папці '%s' (PNG + SVG)." % OUT)


# ============================================================================
if __name__ == "__main__":
    build_schemes()
    build_document()