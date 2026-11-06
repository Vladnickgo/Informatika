# -*- coding: utf-8 -*-
"""
Генератор методичного матеріалу
Практичне заняття № 17. Запуск макросів. MsgBox та InputBox
Запуск:  python practice_17_dialogs.py
Результат: Практичне_заняття_17_Діалоги.docx + output/ (5 схем, PNG + SVG)
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
from matplotlib.patches import FancyBboxPatch

# ----------------------------------------------------------------------------
OUT = "output"
DOCX_NAME = "Практичне_заняття_17_Діалоги.docx"

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
                fontsize=size, color=color, fontweight=weight, zorder=3)


def _arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_GRAY, lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=12),
                zorder=1)


def _save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220,
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(os.path.join(OUT, name + ".svg"),
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


def scheme_launch():
    fig, ax = _canvas(6.3, 2.2)
    items = [
        ("Гаряча клавіша", "Ctrl+Shift+…", BLUE),
        ("Вікно макросів", "Alt+F8", GREEN),
        ("Кнопка аркуша", "Розробник", ORANGE),
        ("Панель доступу", "часто вживані", BLUE),
        ("Подія Excel", "Workbook_Open", GREEN),
        ("F5 у редакторі", "налагодження", ORANGE),
    ]
    w, gap, h = 2.0, 0.1, 0.85
    x0 = 0.05
    for i, (t, s, accent) in enumerate(items[:3]):
        x = x0 + i * (w + gap)
        _card(ax, x, 1.15, w, h, [
            (t, 8.5, accent, "bold"),
            (s, 8, TEXT_GRAY, "normal"),
        ], rs=0.1)
    for i, (t, s, accent) in enumerate(items[3:]):
        x = x0 + i * (w + gap)
        _card(ax, x, 0.1, w, h, [
            (t, 8.5, accent, "bold"),
            (s, 8, TEXT_GRAY, "normal"),
        ], rs=0.1)
    _save(fig, "scheme_01_launch")


def scheme_msgbox():
    fig, ax = _canvas(6.3, 2.3)
    params = [
        [("Промпт", 11, BLUE, "bold"),
         ("обов'язковий", 9, TEXT_GRAY, "normal"),
         ("текст", 9, TEXT_DARK, "normal"),
         ("повідомлення", 9, TEXT_DARK, "normal")],
        [("Кнопки", 11, GREEN, "bold"),
         ("опційно", 9, TEXT_GRAY, "normal"),
         ("vbYesNo +", 9, TEXT_DARK, "normal"),
         ("vbQuestion", 9, TEXT_DARK, "normal")],
        [("Заголовок", 11, ORANGE, "bold"),
         ("опційно", 9, TEXT_GRAY, "normal"),
         ("назва", 9, TEXT_DARK, "normal"),
         ("вікна", 9, TEXT_DARK, "normal")],
    ]
    w, gap, h = 1.95, 0.15, 1.0
    x0 = 0.12
    for i, lines in enumerate(params):
        x = x0 + i * (w + gap)
        _card(ax, x, 1.3, w, h, lines, rs=0.1)
    _arrow(ax, 3.15, 1.25, 3.15, 0.95)
    _card(ax, 0.9, 0.15, 4.5, 0.75, [
        ("Повертає код натиснутої кнопки", 9.5, BLUE, "bold"),
        ("vbYes = 6 · vbNo = 7 · vbCancel = 2", 9, TEXT_DARK, "normal"),
    ], rs=0.1)
    _save(fig, "scheme_02_msgbox")


def scheme_inputbox():
    fig, ax = _canvas(6.3, 2.6)
    params = [
        [("Промпт", 11, BLUE, "bold"),
         ("обов'язковий", 9, TEXT_GRAY, "normal"),
         ("що ввести", 9, TEXT_DARK, "normal")],
        [("Заголовок", 11, GREEN, "bold"),
         ("опційно", 9, TEXT_GRAY, "normal"),
         ("назва вікна", 9, TEXT_DARK, "normal")],
        [("Значення", 11, ORANGE, "bold"),
         ("за замовч.", 9, TEXT_GRAY, "normal"),
         ("підказка-число", 8.5, TEXT_DARK, "normal")],
    ]
    w, gap, h = 1.95, 0.15, 0.85
    x0 = 0.12
    for i, lines in enumerate(params):
        x = x0 + i * (w + gap)
        _card(ax, x, 1.6, w, h, lines, rs=0.1)
    _arrow(ax, 3.15, 1.55, 3.15, 1.3)
    _card(ax, 0.9, 0.65, 4.5, 0.55, [
        ("Повертає рядок — введений текст", 10.5, BLUE, "bold"),
    ], rs=0.1)
    _arrow(ax, 3.15, 0.6, 3.15, 0.42)
    _card(ax, 0.9, 0.05, 4.5, 0.32, [
        ('If текст = "" → Exit Sub', 9.5, ORANGE, "bold"),
    ], rs=0.08)
    _save(fig, "scheme_03_inputbox")


def scheme_levels():
    fig, ax = _canvas(6.3, 1.5)
    items = [
        ("Рівень 1", "Репродуктивний", "готовий код", BLUE),
        ("Рівень 2", "Продуктивний", "код + валідація", GREEN),
        ("Рівень 3", "Творчий", "повна програма", ORANGE),
    ]
    w, gap, h = 1.9, 0.15, 0.95
    x0 = 0.1
    for i, (t1, t2, t3, accent) in enumerate(items):
        x = x0 + i * (w + gap)
        _card(ax, x, 0.3, w, h, [
            (t1, 11, accent, "bold"),
            (t2, 8, TEXT_DARK, "normal"),
            (t3, 8, TEXT_GRAY, "normal"),
        ], rs=0.1)
    _save(fig, "scheme_04_levels")


def scheme_dialog_flow():
    fig, ax = _canvas(6.3, 2.6)
    items = [
        ("InputBox", "введення даних від користувача", BLUE),
        ('Перевірка ""', "чи не скасовано?", ORANGE),
        ("MsgBox vbYesNo", "підтвердження дії", GREEN),
        ("Дія", "запис або вихід", RED),
    ]
    for i, (t, s, accent) in enumerate(items):
        y = 2.0 - i * 0.55
        _card(ax, 1.15, y, 4.0, 0.45, [
            (t, 10.5, accent, "bold"),
            (s, 8.5, TEXT_GRAY, "normal"),
        ], rs=0.1)
        if i < 3:
            _arrow(ax, 3.15, y - 0.02, 3.15, y - 0.13)
    _save(fig, "scheme_05_dialog_flow")


def build_schemes():
    os.makedirs(OUT, exist_ok=True)
    scheme_launch()
    scheme_msgbox()
    scheme_inputbox()
    scheme_levels()
    scheme_dialog_flow()


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
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    if text:
        set_run(p.add_run(text), size=size, bold=bold, italic=italic, color=color)
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


def code_block(doc, lines, size=10.5):
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

    first = True
    for line in lines:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_before = Pt(2 if line is lines[0] else 0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_run(p.add_run(line), size=size, name="Consolas", color=CODE_DARK)

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
            p.alignment = (WD_ALIGN_PARAGRAPH.CENTER if i in center_cols
                           else WD_ALIGN_PARAGRAPH.LEFT)
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

    # Заголовок
    heading(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 17",
            align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4)
    para(doc, "Тема: Запуск макросів на виконання. Використання MsgBox та InputBox",
         bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    # Мета
    heading(doc, "Мета")
    para(doc, "Навчати запускати макроси різними способами, застосовувати "
              "діалогові вікна MsgBox (виведення повідомлень) та InputBox "
              "(введення даних). Розвивати навички створення інтерактивних "
              "програм, уміння проектувати діалог з користувачем. Виховувати "
              "орієнтацію на користувача, прагнення робити програми зручними "
              "та зрозумілими.")

    # Обладнання
    heading(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "персональний комп'ютер або ноутбук;",
        "табличний редактор Microsoft Excel 2016 / 2019 / 2021 або Microsoft 365;",
        "вбудований редактор VBA (Visual Basic for Applications);",
        "інструкційні картки до заняття;",
        "файл-заготовка «Практика_17.xlsm».",
    ])

    # Література
    heading(doc, "Література")
    literature_list(doc, [
        "Мирошниченко В. О. Використання сучасних інформаційних технологій: "
        "формування мультимедійної компетентності. Київ : Центр учбової "
        "літератури, 2022. 296 с.",
        "Потієнко В. О. Графічний дизайн : рівень стандарту (вибірковий "
        "модуль для 10–11 кл). Харків : Ранок, 2020. 160 с.",
        "Речич Н. В. Вебтехнології : рівень стандарту (вибірковий модуль "
        "для 10–11 кл.). Харків : Ранок, 2020. 160 с.",
    ])

    # ------------------------------------------------------------------
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # ------------------------------------------------------------------
    heading(doc, "Теоретичні відомості")

    subheading(doc, "1.1. Способи запуску макросів")
    para(doc, "Макрос можна запустити шістьма способами (схема 1). Вибір "
              "способу залежить від того, хто ним користуватиметься: "
              "розробник під час налагодження натискає F5 у редакторі VBA, "
              "а кінцевий користувач — кнопку на аркуші або сполучення "
              "клавіш. Для програм із повторюваним використанням зручно "
              "закріпити макрос на панелі швидкого доступу або запускати "
              "його автоматично через подію Excel.")
    add_scheme(doc, "scheme_01_launch.png",
               "Схема 1. Способи запуску макросів")

    subheading(doc, "1.2. Функція MsgBox")
    para(doc, "MsgBox — функція для виведення діалогового вікна з "
              "повідомленням. Вона має три основні параметри: промпт "
              "(обов'язковий текст повідомлення), кнопки (тип кнопок та "
              "іконки) і заголовок (назва вікна). Функція повертає код "
              "натиснутої користувачем кнопки, тому MsgBox часто "
              "використовують не лише для інформування, а й для отримання "
              "відповіді (схема 2).")
    add_scheme(doc, "scheme_02_msgbox.png",
               "Схема 2. Структура функції MsgBox")
    para(doc, "Основні константи кнопок та іконок наведено в таблицях 1 і 2.")
    styled_table(
        doc,
        ["Константа", "Значення", "Кнопки"],
        [
            ["vbOKOnly", "0", "OK"],
            ["vbOKCancel", "1", "OK, Скасувати"],
            ["vbYesNo", "4", "Так, Ні"],
            ["vbYesNoCancel", "3", "Так, Ні, Скасувати"],
            ["vbRetryCancel", "5", "Повторити, Скасувати"],
        ],
        widths=[4.5, 3.0, 9.5],
        font_size=12,
        code_cols=(0,),
        center_cols=(0, 1),
    )
    para(doc, "Таблиця 1. Типи кнопок MsgBox", size=12, italic=True,
         color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)
    styled_table(
        doc,
        ["Константа", "Значення", "Призначення"],
        [
            ["vbInformation", "64", "Синій знак «і» — інформація"],
            ["vbQuestion", "32", "Знак питання — уточнення"],
            ["vbExclamation", "48", "Жовтий трикутник — попередження"],
            ["vbCritical", "16", "Червоний хрест — помилка"],
        ],
        widths=[4.5, 3.0, 9.5],
        font_size=12,
        code_cols=(0,),
        center_cols=(0, 1),
    )
    para(doc, "Таблиця 2. Іконки MsgBox", size=12, italic=True, color=GRAY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)

    subheading(doc, "1.3. Функція InputBox")
    para(doc, "InputBox — функція для введення даних через діалогове вікно. "
              "Вона має промпт (запит до користувача), заголовок вікна та "
              "значення за замовчуванням (те, що вже стоїть у полі "
              "введення). Функція повертає рядок — введений користувачем "
              "текст або порожній рядок, якщо вікно закрито кнопкою "
              "«Скасувати» (схема 3).")
    add_scheme(doc, "scheme_03_inputbox.png",
               "Схема 3. Структура функції InputBox")
    para_rich(doc, [
        ("Найважливіша перевірка після виклику InputBox — порівняння "
         "результату з порожнім рядком. Якщо користувач натиснув "
         "«Скасувати», подальша робота програми втрачає сенс, тому "
         "виконують достроковий вихід із процедури: ", "text"),
        ('If текст = "" Then Exit Sub', "code"),
        (".", "text"),
    ])
    callout(doc, "Значення, яке повертає InputBox, має тип String. Перш ніж "
                 "використовувати його як число (наприклад, оцінку), "
                 "перевірте, чи можна його перетворити: якщо користувач "
                 "ввів літери замість цифр, подальші обчислення дадуть "
                 "помилку.",
            fill="FFF4E5", accent="C93400")

    subheading(doc, "1.4. Комбінування MsgBox та InputBox")
    para(doc, "У реальній програмі ці дві функції працюють разом: InputBox "
              "збирає дані, перевірки відсіюють некоректні значення, а "
              "MsgBox повідомляє результат і запитує підтвердження перед "
              "незворотною дією (схема 5). Такий ланцюжок забезпечує "
              "зрозумілий діалог із користувачем.")
    add_scheme(doc, "scheme_05_dialog_flow.png",
               "Схема 5. Потік діалогу «введення → перевірка → "
               "підтвердження → дія»", width_cm=15.5)

    subheading(doc, "1.5. Автоматичний запуск через подію Workbook_Open")
    para_rich(doc, [
        ("Окремий спосіб запуску — прив'язка макросу до події. Процедура з "
         "ім'ям ", "text"),
        ("Workbook_Open", "code"),
        (" автоматично виконується під час відкриття книги. Вона "
         "розміщується не в модулі, а в об'єкті ", "text"),
        ("ThisWorkbook", "code"),
        (" у редакторі VBA. Такий прийом зручний для вітального "
         "повідомлення або автоматичного оновлення даних.", "text"),
    ])

    # ------------------------------------------------------------------
    # РІВНІ
    # ------------------------------------------------------------------
    heading(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    para(doc, "Практична частина складається з трьох рівнів. Рівень 1 — "
              "відпрацювання базових функцій, рівень 2 — об'єднання "
              "введення й перевірки, рівень 3 — створення повноцінної "
              "інтерактивної програми з меню.")
    add_scheme(doc, "scheme_04_levels.png",
               "Схема 4. Три рівні практичної частини", width_cm=15.5)

    # ---------- Рівень 1 ----------
    subheading(doc, "Рівень 1. Репродуктивний")
    para(doc, "Завдання. Створити два простих макроси: вітальне "
              "повідомлення та запит оцінки з перевіркою на скасування.")
    para_rich(doc, [("Макрос 1.1. ", "b"), ("Привітання", "code"),
                    (" — виводить MsgBox із заголовком «Вітання» та іконкою "
                     "vbInformation.", "text")])
    code_block(doc, [
        "Sub Привітання()",
        '    MsgBox "Ласкаво просимо до програми обліку оцінок!", _',
        '           vbInformation, "Вітання"',
        "End Sub",
    ])
    para_rich(doc, [("Макрос 1.2. ", "b"), ("ВвестиОцінку", "code"),
                    (" — запитує оцінку через InputBox зі значенням за "
                     "замовчуванням 10 і повідомляє про скасування, якщо "
                     "користувач закрив вікно.", "text")])
    code_block(doc, [
        "Sub ВвестиОцінку()",
        "    Dim оцінка As String",
        '    оцінка = InputBox("Введіть оцінку (1-12):", _',
        '                      "Оцінювання", 10)',
        "",
        '    If оцінка = "" Then',
        '        MsgBox "Операцію скасовано!", _',
        '               vbExclamation, "Скасування"',
        "        Exit Sub",
        "    End If",
        "",
        '    MsgBox "Ви ввели: " & оцінка, vbInformation, "Результат"',
        "End Sub",
    ])
    para(doc, "Кроки виконання наведено в таблиці 3.")
    styled_table(
        doc,
        ["№", "Дія", "Команда / шлях", "Результат"],
        [
            ["1", "Створити книгу Excel", "Файл → Створити", "Нова книга"],
            ["2", "Зберегти у форматі .xlsm",
             "Файл → Зберегти як → Прізвище_ПЗ17_діалоги.xlsm",
             "Книга з підтримкою макросів"],
            ["3", "Створити таблицю",
             "A1:D1 — «№, Прізвище, Оцінка, Коментар»",
             "Таблиця готова до заповнення"],
            ["4", "Відкрити редактор VBA", "Alt+F11",
             "Вікно Microsoft Visual Basic"],
            ["5", "Додати модуль", "Insert → Module",
             "У проєкті з'явився Module1"],
            ["6", "Ввести код Привітання та ВвестиОцінку",
             "код процедур (див. вище)", "Код набрано"],
            ["7", "Запустити Привітання", "F5 із курсором у процедурі",
             "З'явилося вікно з вітанням"],
            ["8", "Запустити ВвестиОцінку",
             "F5 → 8 → OK; повторити → Скасувати",
             "Два різні повідомлення"],
            ["9", "Зберегти книгу", "Ctrl+S", "Зміни збережено"],
        ],
        widths=[1.0, 4.0, 6.0, 5.5],
        font_size=11,
        code_cols=(2,),
    )
    para(doc, "Таблиця 3. Кроки виконання рівня 1", size=12, italic=True,
         color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)

    # ---------- Рівень 2 ----------
    subheading(doc, "Рівень 2. Продуктивний")
    para_rich(doc, [
        ("Завдання. Створити макрос ", "b"),
        ("ДодатиУчня", "code"),
        (", який послідовно запитує прізвище та оцінку, перевіряє "
         "коректність уведених даних, запитує підтвердження через MsgBox "
         "vbYesNo і лише після цього записує рядок у таблицю.", "b"),
    ])
    para(doc, "Орієнтовний каркас коду:")
    code_block(doc, [
        "Sub ДодатиУчня()",
        "    Dim прізвище As String",
        "    Dim оцінка As Variant",
        "    Dim рядок As Long",
        "    Dim відповідь As Integer",
        "",
        '    прізвище = InputBox("Введіть прізвище учня:", "Новий учень")',
        '    If прізвище = "" Then',
        '        MsgBox "Операцію скасовано!", vbExclamation',
        "        Exit Sub",
        "    End If",
        "",
        '    оцінка = InputBox("Введіть оцінку (1-12):", _',
        '                      "Новий учень", 10)',
        '    If оцінка = "" Then Exit Sub',
        "",
        "    If Not IsNumeric(оцінка) Then",
        '        MsgBox "Оцінка має бути числом!", vbCritical',
        "        Exit Sub",
        "    End If",
        "    If оцінка < 1 Or оцінка > 12 Then",
        '        MsgBox "Оцінка має бути від 1 до 12!", vbCritical',
        "        Exit Sub",
        "    End If",
        "",
        '    відповідь = MsgBox("Прізвище: " & прізвище & vbCrLf & _',
        '                       "Оцінка: " & оцінка & vbCrLf & _',
        '                       "Додати запис?", _',
        '                       vbYesNo + vbQuestion, "Перевірка")',
        "    If відповідь <> vbYes Then Exit Sub",
        "",
        "    рядок = Cells(Rows.Count, 2).End(xlUp).Row + 1",
        "    Cells(рядок, 1).Value = рядок - 1",
        "    Cells(рядок, 2).Value = прізвище",
        "    Cells(рядок, 3).Value = оцінка",
        '    MsgBox "Учня " & прізвище & " додано!", vbInformation',
        "End Sub",
    ])
    para(doc, "Що саме перевіряє макрос — у таблиці 4.")
    styled_table(
        doc,
        ["Перевірка", "Умова", "Реакція макросу"],
        [
            ["Скасування введення прізвища", 'прізвище = ""',
             "MsgBox vbExclamation + Exit Sub"],
            ["Скасування введення оцінки", 'оцінка = ""',
             "Тихий вихід (без повідомлення)"],
            ["Нечислове значення", "Not IsNumeric(оцінка)",
             "MsgBox vbCritical + Exit Sub"],
            ["Вихід за діапазон", "оцінка < 1 Or оцінка > 12",
             "MsgBox vbCritical + Exit Sub"],
            ["Підтвердження запису", "MsgBox vbYesNo",
             "vbNo → тихий вихід, vbYes → запис у таблицю"],
        ],
        widths=[5.0, 5.5, 6.5],
        font_size=12,
        code_cols=(1,),
        center_cols=(),
    )
    para(doc, "Таблиця 4. Перевірки у макросі ДодатиУчня", size=12,
         italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)
    callout(doc, "Функція IsNumeric повертає True, якщо значення можна "
                 "перетворити на число. Без цієї перевірки введення літер "
                 "під час порівняння оцінка < 1 спричинить помилку "
                 "виконання та зупинку макросу.",
            fill="EAF2FB", accent="0071E3")

    # ---------- Рівень 3 ----------
    subheading(doc, "Рівень 3. Творчий")
    para(doc, "Завдання. Побудувати повноцінну інтерактивну програму обліку "
              "оцінок із меню, видаленням записів, пошуком і вітальним "
              "повідомленням під час відкриття книги.")
    para(doc, "Склад програми:")
    num_list(doc, [
        "Головне меню — MsgBox vbYesNoCancel; «Так» → додати учня, "
        "«Ні» → видалити, «Скасувати» → вихід.",
        "Видалення учня — перевірка активної комірки, MsgBox vbYesNo "
        "для підтвердження, видалення рядка та перенумерація.",
        "Пошук учня — InputBox для прізвища, цикл по таблиці, "
        "MsgBox із результатом.",
        "Подія Workbook_Open — вітальне повідомлення під час відкриття "
        "книги (розміщується в об'єкті ThisWorkbook).",
        "Кнопка на аркуші — прив'язати до макросу «ГоловнеМеню».",
    ])
    para(doc, "Макрос ГоловнеМеню:")
    code_block(doc, [
        "Sub ГоловнеМеню()",
        "    Dim вибір As Integer",
        "    Do",
        '        вибір = MsgBox("Виберіть дію:" & vbCrLf & _',
        '                       "Так — Додати учня" & vbCrLf & _',
        '                       "Ні — Видалити учня" & vbCrLf & _',
        '                       "Скасувати — Вихід", _',
        "                       vbYesNoCancel + vbInformation, _",
        '                       "Головне меню")',
        "        Select Case вибір",
        "            Case vbYes: Call ДодатиУчня",
        "            Case vbNo:  Call ВидалитиУчня",
        "            Case vbCancel",
        '                MsgBox "До побачення!", vbInformation',
        "                Exit Sub",
        "        End Select",
        "    Loop",
        "End Sub",
    ])
    para(doc, "Макрос ВидалитиУчня:")
    code_block(doc, [
        "Sub ВидалитиУчня()",
        "    Dim р As Long, і As Long",
        "    Dim прізвище As String",
        "    р = ActiveCell.Row",
        '    If р < 2 Or Cells(р, 2).Value = "" Then',
        '        MsgBox "Виділіть рядок учня!", vbExclamation',
        "        Exit Sub",
        "    End If",
        "    прізвище = Cells(р, 2).Value",
        '    If MsgBox("Видалити " & прізвище & "?", _',
        "              vbYesNo + vbQuestion) <> vbYes Then Exit Sub",
        "    Rows(р).Delete Shift:=xlUp",
        "    For і = 2 To Cells(Rows.Count, 2).End(xlUp).Row",
        "        Cells(і, 1).Value = і - 1",
        "    Next і",
        '    MsgBox "Учня " & прізвище & " видалено!", vbInformation',
        "End Sub",
    ])
    para(doc, "Макрос ПошукУчня:")
    code_block(doc, [
        "Sub ПошукУчня()",
        "    Dim пошук As String, і As Long",
        '    пошук = InputBox("Прізвище для пошуку:", "Пошук")',
        '    If пошук = "" Then Exit Sub',
        "    For і = 2 To Cells(Rows.Count, 2).End(xlUp).Row",
        '        If LCase(Cells(і, 2)) Like LCase("*" & пошук & "*") Then',
        "            Cells(і, 2).Select",
        '            MsgBox "Знайдено: " & Cells(і, 2) & _',
        '                   vbCrLf & "Оцінка: " & Cells(і, 3), _',
        "                   vbInformation",
        "            Exit Sub",
        "        End If",
        "    Next і",
        '    MsgBox "Учня не знайдено!", vbExclamation',
        "End Sub",
    ])
    para_rich(doc, [
        ("Подія ", "text"), ("Workbook_Open", "code"),
        (" розміщується в об'єкті ", "text"), ("ThisWorkbook", "code"),
        (" (а не в модулі):", "text"),
    ])
    code_block(doc, [
        "Private Sub Workbook_Open()",
        '    MsgBox "Вітаємо у програмі обліку оцінок!" & vbCrLf & _',
        '           "Для роботи натисніть кнопку «Головне меню»", _',
        "           vbInformation",
        "End Sub",
    ])
    para(doc, "Вимоги до програми — у таблиці 5.")
    styled_table(
        doc,
        ["Елемент", "Вимога", "Перевірка"],
        [
            ["Головне меню", "Цикл Do із MsgBox vbYesNoCancel",
             "Кнопка «Скасувати» завершує програму"],
            ["Видалення", "Перевірка активної комірки, MsgBox vbYesNo",
             "Натискання «Ні» не змінює таблицю"],
            ["Пошук", "InputBox, LCase + Like, повідомлення про "
                      "результат", "Пошук за частиною прізвища знаходить "
                      "запис"],
            ["Вітання", "Подія Workbook_Open у ThisWorkbook",
             "Повідомлення з'являється під час відкриття книги"],
            ["Інтерфейс", "Кнопка на аркуші з прив'язкою до ГоловнеМеню",
             "Клік по кнопці відкриває меню"],
        ],
        widths=[3.5, 7.5, 6.0],
        font_size=11.5,
        center_cols=(),
    )
    para(doc, "Таблиця 5. Вимоги до творчого завдання", size=12,
         italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)
    callout(doc, "Перед видаленням рядка обов'язково запитуйте "
                 "підтвердження. Видалення — незворотна дія, і випадкове "
                 "натискання кнопки не повинно призводити до втрати даних.",
            fill="FDECEA", accent="C4001D")

    # ------------------------------------------------------------------
    # КРИТЕРІЇ
    # ------------------------------------------------------------------
    heading(doc, "Критерії оцінювання")
    styled_table(
        doc,
        ["№", "Критерій", "Бали"],
        [
            ["1", "Книгу збережено у форматі .xlsm з правильною назвою", "1"],
            ["2", "Таблицю з даними створено", "1"],
            ["3", "Макрос Привітання (MsgBox з іконкою) працює", "2"],
            ["4", "Макрос ВвестиОцінку (InputBox + перевірка на скасування) "
                  "працює", "2"],
            ["5", "Макрос ДодатиУчня (два InputBox + валідація діапазону) "
                  "працює", "4"],
            ["6", "Макрос ВидалитиУчня (MsgBox vbYesNo + перенумерація) "
                  "працює", "3"],
            ["7", "Макрос ПошукУчня працює", "2"],
            ["8", "Макрос ГоловнеМеню (vbYesNoCancel + Select Case) працює",
             "3"],
            ["9", "Подія Workbook_Open реалізована", "1"],
            ["10", "Оформлення, скріншоти, висновки у звіті", "1"],
            ["", "Разом", "20"],
        ],
        widths=[1.0, 13.5, 2.5],
        font_size=12,
    )
    para(doc, "Таблиця 6. Критерії та бали", size=12, italic=True, color=GRAY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)

    # ------------------------------------------------------------------
    # ФОРМА ЗВІТНОСТІ
    # ------------------------------------------------------------------
    heading(doc, "Форма звітності")
    para(doc, "За результатами заняття студент подає два файли:")
    bullets(doc, [
        "книгу Excel — Прізвище_ПЗ17_діалоги.xlsm з усіма макросами та "
        "кнопкою на аркуші;",
        "звіт — ПЗ17_Прізвище.docx, оформлений у текстовому редакторі Word "
        "(Times New Roman, 14 pt, інтервал 1,15).",
    ])
    para(doc, "Структура звіту:")
    num_list(doc, [
        "тема та мета роботи;",
        "коротке пояснення ролі MsgBox та InputBox (3–5 речень);",
        "код кожної процедури з коментарями;",
        "скріншоти вікон MsgBox та InputBox для кожного рівня "
        "(не менше ніж 5);",
        "опис виявлених труднощів та способів їх подолання;",
        "висновки (4–6 речень): де в роботі вчителя початкової школи "
        "доречно застосовувати інтерактивні діалоги.",
    ])

    doc.save(DOCX_NAME)
    print("Готово: створено файл '%s'." % DOCX_NAME)
    print("Схеми збережено у папці '%s' (PNG + SVG)." % OUT)


if __name__ == "__main__":
    build_schemes()
    build_document()