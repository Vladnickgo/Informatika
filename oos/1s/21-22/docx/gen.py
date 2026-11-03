# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Команди для роботи з текстовими файлами
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

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

OUT = "output"
os.makedirs(OUT, exist_ok=True)

TEXT_DARK = "#1D1D1F"
TEXT_GRAY = "#86868B"
CARD_BG = "#F5F5F7"
CARD_BORDER = "#E5E5EA"
ACCENT_BLUE = "#0071E3"
ACCENT_GREEN = "#248A3D"
ACCENT_ORANGE = "#C93400"
ACCENT_RED = "#C4001D"
ACCENT_PURPLE = "#6E30A8"
TERM_BG = "#1C1C1E"
TERM_TEXT = "#D1D1D6"
TERM_PROMPT = "#30D158"


def _save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220,
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(os.path.join(OUT, name + ".svg"),
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return os.path.join(OUT, name + ".png")


def _card(ax, x, y, w, h, fill=CARD_BG, border=CARD_BORDER, radius=0.22):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={radius}",
                                facecolor=fill, edgecolor=border, linewidth=1.4))


def _badge(ax, cx, cy, w, h, fill, text, color="white", size=12, radius=None):
    r = radius if radius is not None else h / 2
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={r}",
                                facecolor=fill, edgecolor=fill, linewidth=0))
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=size, fontweight="bold", color=color)


# ============================================================
# СХЕМА 1. Основні команди
# ============================================================

def scheme_commands():
    fig, ax = plt.subplots(figsize=(11, 7.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.0)
    ax.axis("off")

    ax.text(6.5, 8.55, "Основні команди для текстових файлів",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    commands = [
        ("type", "type <файл>",
         "Виводить увесь вміст\nфайлу на екран", ACCENT_BLUE, "#E1F0FE"),
        ("more", "more <файл>",
         "Посторінковий\nперегляд вмісту", ACCENT_GREEN, "#E8F8EC"),
        ("find", "find \"текст\" <файл>",
         "Шукає рядки зі\nвказаним текстом", ACCENT_PURPLE, "#EFE6F7"),
        ("copy con", "copy con <файл>",
         "Створює файл через\nвведення з клавіатури", ACCENT_ORANGE, "#FFF4E5"),
        ("findstr", "findstr \"текст\" <файл>",
         "Розширений пошук\nіз масками", ACCENT_PURPLE, "#EFE6F7"),
        ("echo", "echo текст > файл",
         "Швидке створення\nфайлу з одним рядком", ACCENT_RED, "#FFEBEA"),
    ]

    card_w, card_h = 3.9, 2.7
    gap_x, gap_y = 0.25, 0.3
    x0 = 0.4
    y_top = 7.9

    for i, (cmd, syntax, desc, color, fill) in enumerate(commands):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.18)
        _badge(ax, cx, y + card_h - 0.55, 2.1, 0.55, color, cmd,
               color="white", size=13.5, radius=0.28)
        ax.text(cx, y + card_h - 1.25, syntax, ha="center", va="center",
                fontsize=10, color=TEXT_GRAY, family="monospace")
        ax.text(cx, y + 0.85, desc, ha="center", va="center",
                fontsize=11, color=TEXT_DARK, linespacing=1.55)

    return _save(fig, "scheme_commands")


# ============================================================
# СХЕМА 2. Типи перегляду
# ============================================================

def scheme_view_types():
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.4)
    ax.axis("off")

    ax.text(6.5, 7.0, "Три способи перегляду вмісту файлу",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    panels = [
        ("type", "Увесь вміст\nодразу",
         "Коли файл невеликий.\nПісля виводу одразу\nповертає запрошення.",
         ACCENT_BLUE, "#E1F0FE"),
        ("more", "Посторінково",
         "Коли файл довгий.\nПоказує один екран,\nчекає натискання пробілу.",
         ACCENT_GREEN, "#E8F8EC"),
        ("find", "Тільки рядки,\nщо збігаються",
         "Коли потрібен пошук.\nПоказує рядки зі\nвказаним текстом.",
         ACCENT_PURPLE, "#EFE6F7"),
    ]

    card_w, card_h = 3.9, 4.7
    gap = 0.3
    x0 = 0.4
    y0 = 1.1

    for i, (cmd, subtitle, desc, color, fill) in enumerate(panels):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h, fill=fill, border=color, radius=0.18)
        _badge(ax, cx, y0 + card_h - 0.6, 2.0, 0.6, color, cmd,
               color="white", size=15, radius=0.3)
        ax.text(cx, y0 + card_h - 1.6, subtitle, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=TEXT_DARK,
                linespacing=1.4)
        ax.text(cx, y0 + 1.55, desc, ha="center", va="center",
                fontsize=11, color=TEXT_DARK, linespacing=1.7)

    return _save(fig, "scheme_view_types")


# ============================================================
# СХЕМА 3. Параметри find
# ============================================================

def scheme_find_params():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.0)
    ax.axis("off")

    ax.text(6.5, 7.6, "Параметри команди find",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Синтаксис
    _card(ax, 0.5, 6.35, 12.0, 0.7, fill="#F5F5F7",
          border=CARD_BORDER, radius=0.12)
    ax.text(6.5, 6.7, "find [/I] [/V] [/N] [/C] \"текст\" <файл>",
            ha="center", va="center", fontsize=12,
            color=TEXT_DARK, family="monospace", fontweight="bold")

    params = [
        ("/I", "Ігнорувати регістр",
         "Find і FIND вважаються однаковими",
         ACCENT_BLUE, "#E1F0FE"),
        ("/V", "Інверсія",
         "Показати рядки БЕЗ вказаного тексту",
         ACCENT_ORANGE, "#FFF4E5"),
        ("/N", "Номери рядків",
         "Додати номер рядка перед результатом",
         ACCENT_GREEN, "#E8F8EC"),
        ("/C", "Лічильник",
         "Показати лише кількість збігів",
         ACCENT_PURPLE, "#EFE6F7"),
    ]

    card_w, card_h = 6.0, 1.55
    gap_x, gap_y = 0.3, 0.2
    x0 = 0.35
    y_top = 5.85

    for i, (param, title, desc, color, fill) in enumerate(params):
        col, row = i % 2, i // 2
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)

        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.16)
        _badge(ax, x + 0.75, y + card_h / 2, 1.1, 0.7, color, param,
               color="white", size=14, radius=0.28)

        ax.text(x + 1.55, y + card_h - 0.55, title, ha="left", va="center",
                fontsize=12.5, fontweight="bold", color=color)
        ax.text(x + 1.55, y + 0.55, desc, ha="left", va="center",
                fontsize=11, color=TEXT_DARK)

    return _save(fig, "scheme_find_params")


# ============================================================
# СХЕМА 4. Три рівні
# ============================================================

def scheme_levels():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.3, "Три рівні практичних завдань",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    levels = [
        ("Рівень 1", "Перегляд\nі створення",
         "type, more,\necho, copy con —\nробота з одним файлом",
         "≈ 7 хв", ACCENT_GREEN, "#E8F8EC"),
        ("Рівень 2", "Пошук\nза шаблоном",
         "find із параметрами\n/I /V /N /C\nу кількох файлах",
         "≈ 10 хв", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Комплексний\nаналіз",
         "пошук у дереві\nфайлів і підготовка\nзвіту про знахідки",
         "≈ 10 хв", ACCENT_RED, "#FFEBEA"),
    ]

    card_w, card_h = 3.9, 5.0
    gap = 0.3
    x0 = 0.4
    y0 = 1.2

    for i, (level, name, desc, time_txt, color, fill) in enumerate(levels):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h)
        _badge(ax, cx, y0 + card_h - 0.7, 1.9, 0.6, color, level,
               size=13, radius=0.3)
        ax.text(cx, y0 + card_h - 1.6, name, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=TEXT_DARK,
                linespacing=1.4)
        ax.text(cx, y0 + card_h - 3.15, desc, ha="center", va="center",
                fontsize=12, color=TEXT_DARK, linespacing=1.7)
        _badge(ax, cx, y0 + 0.7, 2.1, 0.55, fill, time_txt,
               color=color, size=12.5, radius=0.28)

    return _save(fig, "scheme_levels")


# ============================================================
# ДОПОМІЖНІ ФУНКЦІЇ DOCX
# ============================================================

FONT = "Times New Roman"
BLUE = RGBColor(0x1F, 0x4E, 0x79)


def _style_run(run, size=14, bold=False, italic=False, color=None,
               font_name=None):
    name = font_name or FONT
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rpr = run._r.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    for tag in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(tag), name)
    return run


def shade_cell(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.insert_element_before(
        shd, "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText",
        "w:vAlign", "w:hideMark", "w:headers", "w:cellIns", "w:cellDel",
        "w:cellMerge", "w:tcPrChange")


def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.insert_element_before(
            tcBorders, "w:shd", "w:noWrap", "w:tcMar", "w:textDirection",
            "w:tcFitText", "w:vAlign", "w:hideMark", "w:headers",
            "w:cellIns", "w:cellDel", "w:cellMerge", "w:tcPrChange")
    for edge in ("top", "left", "bottom", "right"):
        if edge in kwargs:
            data = kwargs[edge]
            el = tcBorders.find(qn("w:" + edge))
            if el is None:
                el = OxmlElement("w:" + edge)
                tcBorders.append(el)
            for key in ("sz", "val", "color", "space"):
                if key in data:
                    el.set(qn("w:" + key), str(data[key]))


def h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    _style_run(p.add_run(text.upper()), size=14, bold=True, color=BLUE)
    return p


def theme_line(doc, topic):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(12)
    _style_run(p.add_run("Тема: "), size=14, bold=True, color=BLUE)
    _style_run(p.add_run(topic), size=14, bold=True, color=BLUE)
    return p


def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    _style_run(p.add_run(text), size=14, bold=True, color=BLUE)
    return p


def h3(doc, text, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    _style_run(p.add_run(text), size=14, bold=True,
               color=color or RGBColor(0x2E, 0x75, 0xB6))
    return p


def body(doc, text, bold_lead=None, space_after=4, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_lead:
        _style_run(p.add_run(bold_lead), bold=True)
    _style_run(p.add_run(text), italic=italic)
    return p


def bullet(doc, text, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(1.0)
    if bold_lead:
        _style_run(p.add_run(bold_lead), bold=True)
    _style_run(p.add_run(text))
    return p


def numbered(doc, text, bold_lead=None):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(1.0)
    if bold_lead:
        _style_run(p.add_run(bold_lead), bold=True)
    _style_run(p.add_run(text))
    return p


def numbered_paren(doc, idx, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(1.0)
    _style_run(p.add_run(f"{idx}) "), bold=True)
    _style_run(p.add_run(text))
    return p


def code_line(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(1.0)
    _style_run(p.add_run(text), font_name="Consolas",
               color=RGBColor(0xC0, 0x39, 0x2B))
    return p


def callout(doc, text, fill="EAF2F8", accent="2E75B6", title=None):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    cell = t.cell(0, 0)
    cell.width = Cm(16.5)
    set_cell_border(cell,
                    left={"sz": 28, "val": "single", "color": accent},
                    top={"sz": 4, "val": "single", "color": fill},
                    bottom={"sz": 4, "val": "single", "color": fill},
                    right={"sz": 4, "val": "single", "color": fill})
    shade_cell(cell, fill)
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    if title:
        _style_run(p.add_run(title + " "), bold=True,
                   color=RGBColor.from_string(accent))
    _style_run(p.add_run(text))
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.space_before = Pt(0)
    _style_run(spacer.add_run(""), size=6)


def add_table(doc, headers, rows, widths, mono_cols=None):
    mono_cols = mono_cols or []
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    hdr = table.rows[0].cells
    for i, htext in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        _style_run(p.add_run(htext), bold=True,
                   color=RGBColor(0xFF, 0xFF, 0xFF))
        shade_cell(hdr[i], "1F4E79")
    trPr = table.rows[0]._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    trPr.append(tbl_header)
    for r in rows:
        cells = table.add_row().cells
        for i, val in enumerate(r):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            if i in mono_cols:
                _style_run(p.add_run(val), font_name="Consolas",
                           color=RGBColor(0xC0, 0x39, 0x2B))
            else:
                _style_run(p.add_run(val))
    for row in table.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)
    _style_run(spacer.add_run(""), size=6)
    return table


def add_figure(doc, path, width_cm=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))


def add_page_numbers(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    _style_run(run, size=12)
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2)


# ============================================================
# ПОБУДОВА ДОКУМЕНТА
# ============================================================

def build_document():
    img1 = scheme_commands()
    img2 = scheme_view_types()
    img3 = scheme_find_params()
    img4 = scheme_levels()

    doc = Document()

    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(14)
    rpr = st.element.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    for tag in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(tag), FONT)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.space_after = Pt(4)

    sec = doc.sections[0]
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(1.5)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    add_page_numbers(sec)

    h1(doc, "Практичне заняття")
    theme_line(doc, "Команди для роботи з текстовими файлами. "
                    "Вивчення команд для перегляду, редагування та "
                    "створення текстових файлів. Використання команди "
                    "find для пошуку інформації у текстових файлах")

    h2(doc, "Мета")
    body(doc, "ознайомити з командами type, more, find, copy con, "
              "findstr для роботи з текстовими файлами в командному "
              "рядку; розвивати навички пошуку та фільтрації текстової "
              "інформації за допомогою команди find та шаблонів; "
              "виховувати інформаційну грамотність та вміння ефективно "
              "працювати з текстовими даними.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Командний рядок cmd або Windows Terminal.",
        "Інструкційні картки до рівнів 1–3.",
        "Текстовий редактор для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Микитишин А. Г., Чихіра І. В. Операційні системи : консп. лекц. "
        "Тернопіль : ТНТУ імені Івана Пулюя, 2016.",
        "Погребняк Б. І., Булаєнко М. В. Операційні системи : навч. посіб. "
        "Харків. нац. ун-т міськ. госп-ва ім. О. М. Бекетова. Харків : "
        "ХНУМГ ім. О. М. Бекетова, 2018.",
        "Сільвестр В., Гансен П. Основи операційних систем. Київ : "
        "Нова Книга, 2016.",
    ]
    for s in sources:
        numbered(doc, s)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Загальний огляд команд")
    body(doc, "Командний рядок Windows має кілька команд для роботи з "
              "текстовими файлами. Вони дозволяють переглядати вміст, "
              "створювати нові файли без графічного редактора, шукати "
              "рядки за шаблоном та фільтрувати інформацію.")

    add_figure(doc, img1, 16.0)

    add_table(
        doc,
        ["Команда", "Призначення", "Приклад"],
        [
            ["type", "Вивести весь вміст файлу на екран",
             "type звіт.txt"],
            ["more", "Посторінковий перегляд вмісту",
             "more звіт.txt"],
            ["find", "Пошук рядків зі вказаним текстом",
             "find \"урок\" звіт.txt"],
            ["findstr", "Розширений пошук із масками та шаблонами",
             "findstr /I \"урок*\" *.txt"],
            ["copy con", "Створити файл через введення з клавіатури",
             "copy con нотатка.txt"],
            ["echo", "Створити файл з одним рядком або дописати в кінець",
             "echo Привіт > нотатка.txt"],
        ],
        widths=[2.6, 7.2, 6.7],
        mono_cols=[0, 2],
    )

    h3(doc, "2. Перегляд вмісту: type та more")
    body(doc, "Команда type виводить увесь вміст файлу на екран одним "
              "потоком. Це зручно для невеликих файлів (до 25–30 рядків), "
              "бо довший вміст просто «проскочить» повз очі. Для великих "
              "файлів використовують more — він показує один екран і чекає "
              "натискання клавіші, щоб показати наступний.")

    add_figure(doc, img2, 16.0)

    body(doc, "Приклади:")
    code_line(doc, "type звіт.txt")
    body(doc, "вивести весь вміст файлу.", space_after=2)
    code_line(doc, "type звіт.txt | more")
    body(doc, "вивести вміст посторінково (символ | передає вивід type "
              "у more).", space_after=2)
    code_line(doc, "more < звіт.txt")
    body(doc, "альтернативний запис того ж самого через перенаправлення "
              "вводу.")

    h3(doc, "3. Створення текстових файлів: echo та copy con")
    body(doc, "У командному рядку можна створити текстовий файл без "
              "графічного редактора. Найпростіший спосіб — echo з "
              "перенаправленням виводу в файл:")
    code_line(doc, "echo Привіт, командний рядок! > вітання.txt")
    body(doc, "створює новий файл (або перезаписує існуючий) з одним "
              "рядком.", space_after=2)
    code_line(doc, "echo Другий рядок >> вітання.txt")
    body(doc, "дописує рядок у кінець файлу, не затираючи попередній "
              "вміст.", space_after=2)

    body(doc, "Якщо потрібно ввести кілька рядків одразу, "
              "використовують copy con. Після введення команди "
              "користувач набирає текст рядок за рядком, а завершує "
              "введення комбінацією Ctrl + Z і Enter:")
    code_line(doc, "copy con нотатка.txt")
    code_line(doc, "Перший рядок нотатки")
    code_line(doc, "Другий рядок нотатки")
    code_line(doc, "Додатковий рядок")
    code_line(doc, "^Z")
    body(doc, "після Ctrl + Z і Enter файл «нотатка.txt» буде створено "
              "з трьома рядками.")

    h3(doc, "4. Пошук за шаблоном: find")
    body(doc, "Команда find шукає у файлі рядки, що містять вказаний "
              "текст, і виводить лише ті, що збігаються. Це швидкий "
              "спосіб знайти потрібну інформацію у великому текстовому "
              "файлі без відкриття редактора.")

    add_figure(doc, img3, 16.0)

    body(doc, "Ключові параметри find:")
    bullet(doc, "/I — ігнорувати регістр (Find і FIND вважаються "
                "однаковими);")
    bullet(doc, "/V — інверсія: показати рядки БЕЗ вказаного тексту;")
    bullet(doc, "/N — додати номер рядка перед результатом;")
    bullet(doc, "/C — показати лише кількість рядків, що містять текст.")

    body(doc, "Приклади:")
    code_line(doc, "find \"урок\" план.txt")
    body(doc, "знайти всі рядки зі словом «урок» (з урахуванням "
              "регістру).", space_after=2)
    code_line(doc, "find /I \"урок\" план.txt")
    body(doc, "те саме, але без урахування регістру (знайде й «Урок»).",
         space_after=2)
    code_line(doc, "find /N /I \"завдання\" *.txt")
    body(doc, "знайти «завдання» в усіх txt-файлах поточної папки, "
              "виводячи номери рядків.", space_after=2)
    code_line(doc, "find /C \"урок\" план.txt")
    body(doc, "показати лише кількість рядків, що містять «урок».")

    body(doc, "Команда find розуміє простий шаблон — рядок у лапках. "
              "Якщо ж потрібні маски (зірочка, знак питання), "
              "використовують findstr:")
    code_line(doc, "findstr /I \"урок*\" *.txt")
    body(doc, "знайти всі рядки, що починаються зі слова «урок», у всіх "
              "txt-файлах поточної папки.")

    callout(doc,
            "find шукає підрядок, а findstr — за шаблоном. Якщо потрібно "
            "знайти точне слово «урок», а не «уроки» чи «уроками», "
            "скористайтеся findstr із параметром /C:\"урок\" або "
            "регулярним виразом findstr /R \"\\<урок\\>\".",
            fill="E1F0FE", accent="0071E3")

    h3(doc, "5. Редагування текстових файлів: edit та альтернативи")
    body(doc, "Історично у Windows існувала команда edit — текстовий "
              "редактор у командному рядку. Однак на сучасних 64-бітних "
              "версіях Windows (10/11) програма edit.exe не працює: це "
              "16-бітна програма, і система видає повідомлення про "
              "несумісність. Замість неї використовують:")
    bullet(doc, "notepad <файл> — запускає графічний «Блокнот» "
                "одразу з потрібним файлом;")
    bullet(doc, "echo текст >> файл — дописує рядок у кінець файлу;")
    bullet(doc, "copy con файл — створює новий файл через введення з "
                "клавіатури;")
    bullet(doc, "powershell -Command \"Add-Content файл 'текст'\" — "
                "додає рядок через PowerShell.")

    callout(doc,
            "Команда edit у сучасних версіях Windows не запускається. "
            "Якщо під час заняття студент спробує її виконати й побачить "
            "повідомлення про 16-бітну програму — це очікуваний "
            "результат, а не помилка. Використовуйте notepad або "
            "перенаправлення виводу.",
            fill="FFF4E5", accent="C93400")

    h3(doc, "6. Безпека під час роботи з текстовими файлами")
    body(doc, "Під час роботи з файлами через командний рядок варто "
              "пам'ятати кілька правил, щоб не втратити дані.")
    bullet(doc, "Оператор > перезаписує файл повністю. Якщо файл уже "
                "існує, попередній вміст буде втрачено — використовуйте "
                ">> для дописування.")
    bullet(doc, "Перед виконанням find у великій папці обмежте пошук "
                "маскою (*.txt), щоб не виводити зайву інформацію.")
    bullet(doc, "Не запускайте copy con без попереднього вибору імені "
                "файлу — інакше введений текст буде втрачено.")

    # =====================================================
    # РІВНІ ЗАВДАНЬ
    # =====================================================
    h2(doc, "Покроковий алгоритм виконання різнорівневих завдань")

    body(doc, "Практична частина заняття побудована за трирівневою "
              "системою. Студент виконує завдання послідовно; орієнтовний "
              "час на кожен рівень — 7–10 хвилин, загальна тривалість — "
              "25–30 хвилин. Оцінка залежить від кількості успішно "
              "виконаних рівнів.")

    add_figure(doc, img4, 16.0)

    # -------- Рівень 1 --------
    h3(doc, "Рівень 1 — перегляд і створення (≈ 7 хв)",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Мета: навчитися створювати текстовий файл командами echo "
              "і copy con, переглядати його вміст командами type та more.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Відкрийте командний рядок", "Win + R → cmd → Enter"],
            ["2", "Перейдіть на робочий диск", "D:  (або C:)"],
            ["3", "Створіть робочу папку", "mkdir ПЗ_Текст_ПІБ"],
            ["4", "Перейдіть до неї", "cd ПЗ_Текст_ПІБ"],
            ["5", "Створіть файл з одним рядком",
             "echo Перший рядок тексту > нотатка.txt"],
            ["6", "Допишіть ще два рядки",
             "echo Другий рядок >> нотатка.txt\n"
             "echo Третій рядок >> нотатка.txt"],
            ["7", "Перегляньте вміст через type", "type нотатка.txt"],
            ["8", "Перегляньте вміст через more", "more нотатка.txt"],
            ["9", "Створіть другий файл через copy con",
             "copy con план.txt\n"
             "Пункт 1\nПункт 2\nПункт 3\n^Z"],
            ["10", "Перевірте вміст другого файлу", "type план.txt"],
            ["11", "Зробіть скріншот", "Print Screen → у звіт із підписом"],
        ],
        widths=[1.0, 5.8, 9.7],
        mono_cols=[2],
    )

    callout(doc,
            "У папці «ПЗ_Текст_ПІБ» має бути два файли: «нотатка.txt» "
            "із трьома рядками та «план.txt» із трьома пунктами. "
            "Якщо один з них порожній — перевірте, чи натиснули ви "
            "Ctrl + Z і Enter під час copy con.",
            fill="E8F8EC", accent="248A3D")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — пошук за шаблоном (≈ 10 хв)",
       color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Мета: навчитися шукати інформацію у текстових файлах "
              "командою find із параметрами /I, /V, /N, /C та "
              "використовувати findstr для пошуку за маскою.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Створіть файл із кількома рядками",
             "echo Урок перший > уроки.txt\n"
             "echo Урок другий >> уроки.txt\n"
             "echo Урок третій >> уроки.txt"],
            ["2", "Знайдіть рядки зі словом «Урок» (з урахуванням регістру)",
             "find \"Урок\" уроки.txt"],
            ["3", "Знайдіть рядки зі словом «урок» (без урахування регістру)",
             "find /I \"урок\" уроки.txt"],
            ["4", "Додайте номери рядків",
             "find /N /I \"урок\" уроки.txt"],
            ["5", "Порахуйте кількість збігів",
             "find /C /I \"урок\" уроки.txt"],
            ["6", "Знайдіть рядки БЕЗ слова «Урок»",
             "find /V \"Урок\" уроки.txt"],
            ["7", "Знайдіть рядки за маскою (початок слова)",
             "findstr /I \"Урок*\" уроки.txt"],
            ["8", "Пошук у кількох файлах",
             "find /I \"рядок\" *.txt"],
            ["9", "Зробіть скріншот",
             "Знімок вікна з результатами кроків 4 і 6"],
        ],
        widths=[1.0, 6.2, 9.3],
        mono_cols=[2],
    )

    callout(doc,
            "У звіті має бути: скріншоти результатів кроків 4 і 6, "
            "коротке пояснення, чим відрізняються результати find і "
            "find /I, і чому команда find /V \"Урок\" показує порожній "
            "результат.",
            fill="FFF4E5", accent="C93400")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — комплексний аналіз (≈ 10 хв)",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Мета: створити структуру з кількох текстових файлів, "
              "виконати пошук у дереві каталогів та підготувати звіт про "
              "знахідки за допомогою перенаправлення виводу.")

    body(doc, "Завдання А. Створіть структуру файлів:")
    code_line(doc, "Аналіз\\")
    code_line(doc, "├── 1_Клас\\")
    code_line(doc, "│   ├── план_уроку.txt  (3 рядки)")
    code_line(doc, "│   └── завдання.txt    (3 рядки)")
    code_line(doc, "├── 2_Клас\\")
    code_line(doc, "│   └── план_уроку.txt  (3 рядки)")
    code_line(doc, "└── звіт_пошуку.txt  (поки порожній)")

    body(doc, "Завдання Б. Виконайте операції:")
    tasks_b = [
        "Створіть папки «Аналіз», «Аналіз\\1_Клас», «Аналіз\\2_Клас» "
        "командою mkdir.",
        "У кожній папці класу створіть файл «план_уроку.txt» із трьома "
        "рядками (деякі рядки мають містити слово «Урок»).",
        "У папці «1_Клас» створіть файл «завдання.txt» із трьома "
        "рядками.",
        "Знайдіть усі рядки зі словом «Урок» у дереві папок командою "
        "find /I \"урок\" /S *.txt — параметр /S означає «шукати "
        "рекурсивно».",
        "Перенаправте результат пошуку у файл «звіт_пошуку.txt» "
        "командою find /I \"урок\" /S *.txt > звіт_пошуку.txt.",
        "Перевірте, що у «звіт_пошуку.txt» є знайдені рядки (type "
        "звіт_пошуку.txt).",
        "Додайте до файлу ще й кількість збігів: find /C /I \"урок\" "
        "/S *.txt >> звіт_пошуку.txt.",
        "Перегляньте результат через more звіт_пошуку.txt.",
        "Зробіть скріншот кінцевої структури (tree /F) і вмісту "
        "звіту.",
    ]
    for t in tasks_b:
        numbered(doc, t)

    body(doc, "Завдання В. У звіті наведіть:")
    numbered(doc, "повну послідовність команд, які ви виконали;")
    numbered(doc, "пояснення, чому параметр /S у find відрізняється від "
                  "звичайного пошуку в одному файлі;")
    numbered(doc, "пояснення, чим оператори > і >> відрізняються;")
    numbered(doc, "короткий висновок (3–4 речення) про те, які команди "
                  "виявилися найзручнішими для роботи з текстовими "
                  "файлами.")

    callout(doc,
            "За бажанням (+1 бал). Запропонуйте, як однією командою "
            "findstr знайти у файлі «звіт_пошуку.txt» усі рядки, що "
            "починаються з номера рядка (наприклад, «3:») — тобто "
            "результати find /N. Поясніть, який параметр findstr для "
            "цього використовується.",
            fill="FFEBEA", accent="C4001D")

    # =====================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =====================================================
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Рівень / критерій", "Показник", "Бали"],
        [
            ["Рівень 1",
             "Створено два файли з правильним вмістом; переглянуто "
             "через type і more; є скріншот", "3"],
            ["Рівень 2",
             "Усі параметри find (/I, /V, /N, /C) виконано правильно; "
             "findstr із маскою працює; є скріншоти", "4"],
            ["Рівень 3",
             "Створено структуру; пошук /S виконано; результат "
             "перенаправлено у файл; є скріншот і пояснення", "4"],
            ["Якість звіту",
             "Оформлення за вимогами; підписи до скріншотів; наведено "
             "повну послідовність команд", "1"],
            ["Творчий підхід",
             "Виконано ускладнення з findstr або запропоновано "
             "власний спосіб", "1"],
        ],
        widths=[3.6, 11.0, 2.0],
    )

    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (потребує доопрацювання).")

    # =====================================================
    # ФОРМА ЗВІТНОСТІ
    # =====================================================
    h2(doc, "Форма звітності")
    body(doc, "Результати практичного заняття оформлюються у вигляді "
              "електронного звіту в текстовому редакторі. Звіт повинен "
              "містити такі обов'язкові частини:")
    report_parts = [
        "Титульна сторінка: навчальний заклад, тема, ПІБ студента, "
        "група, ПІБ викладача, дата.",
        "Скріншот папки з двома файлами після рівня 1.",
        "Скріншоти результатів find /N і find /V після рівня 2.",
        "Скріншот дерева (tree /F) і вмісту «звіт_пошуку.txt» після "
        "рівня 3.",
        "Повна послідовність команд кожного рівня (моноширинним "
        "шрифтом).",
        "Відповіді на питання: чим find відрізняється від findstr; що "
        "робить параметр /S; чим оператори > і >> відрізняються.",
        "Висновок: що нового засвоїли, які команди виконували "
        "впевнено, а які потребують додаткового тренування.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, "
              "шрифт Times New Roman 14 pt, інтервал 1,15, поля 2 см, "
              "обсяг — 3–5 сторінок без титульної. Ім'я файлу: "
              "«Практика_Текстові_файли_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    doc.save("Практичне_заняття_Текстові_файли.docx")
    print("Готово: Практичне_заняття_Текстові_файли.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()