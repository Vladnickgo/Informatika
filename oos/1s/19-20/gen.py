# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Копіювання, переміщення і видалення файлів і каталогів.
      Перегляд інформації про файли та каталоги.
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
TERM_TITLE = "#2C2C2E"
TERM_TEXT = "#D1D1D6"
TERM_PROMPT = "#30D158"
TERM_CMD = "#FFFFFF"


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
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.5, 8.05, "Основні команди роботи з файлами",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    commands = [
        ("copy", "copy <звідки> <куди>",
         "Копіює один файл\nабо файли за маскою", ACCENT_BLUE),
        ("move", "move <звідки> <куди>",
         "Переносить файл;\nна відміну від copy — видаляє\nоригінал", ACCENT_ORANGE),
        ("del", "del <файл>",
         "Видаляє файл.\nПараметр /Q — без підтвердження", ACCENT_RED),
        ("ren", "ren <старе> <нове>",
         "Перейменовує файл\nу поточній папці", ACCENT_GREEN),
        ("attrib", "attrib [+/-R] [+/-H]\n[+/-S] [+/-A] <файл>",
         "Показує або змінює\nатрибути файлу", ACCENT_PURPLE),
        ("xcopy", "xcopy <звідки> <куди> /S",
         "Копіює папки\nразом зі вмістом", ACCENT_BLUE),
    ]

    card_w, card_h = 3.9, 2.55
    gap_x, gap_y = 0.25, 0.3
    x0 = 0.4
    y_top = 7.4

    for i, (cmd, syntax, desc, color) in enumerate(commands):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h)
        _badge(ax, cx, y + card_h - 0.55, 2.0, 0.55, color, cmd,
               color="white", size=14, radius=0.28)
        ax.text(cx, y + card_h - 1.2, syntax, ha="center", va="center",
                fontsize=10, color=TEXT_GRAY, family="monospace",
                linespacing=1.4)
        ax.text(cx, y + 0.72, desc, ha="center", va="center",
                fontsize=11, color=TEXT_DARK, linespacing=1.55)

    return _save(fig, "scheme_commands")


# ============================================================
# СХЕМА 2. Атрибути файлів
# ============================================================

def scheme_attributes():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.0)
    ax.axis("off")

    ax.text(6.5, 7.6, "Атрибути файлів у командному рядку",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    attrs = [
        ("R", "Read-only", "Тільки читання",
         "Захищає від редагування\nй випадкового видалення",
         ACCENT_RED, "#FFEBEA"),
        ("H", "Hidden", "Прихований",
         "Не видно у звичайному\nперегляді командою dir",
         ACCENT_ORANGE, "#FFF4E5"),
        ("S", "System", "Системний",
         "Позначає системні файли\nWindows. Не змінюйте!",
         ACCENT_PURPLE, "#EFE6F7"),
        ("A", "Archive", "Архівний",
         "Позначає файли, що\nпотребують резервного копіювання",
         ACCENT_BLUE, "#E1F0FE"),
    ]

    card_w, card_h = 6.0, 2.7
    gap_x, gap_y = 0.35, 0.3
    x0 = 0.35
    y_top = 7.15

    for i, (letter, eng, ukr, desc, color, fill) in enumerate(attrs):
        col, row = i % 2, i // 2
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)

        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.18)
        _badge(ax, x + 0.85, y + card_h - 0.85, 0.9, 0.9, color, letter,
               color="white", size=18, radius=0.2)

        ax.text(x + 1.6, y + card_h - 0.55, eng, ha="left", va="center",
                fontsize=13, fontweight="bold", color=color)
        ax.text(x + 1.6, y + card_h - 1.05, ukr, ha="left", va="center",
                fontsize=12, color=TEXT_DARK, style="italic")
        ax.text(x + 0.5, y + 0.85, desc, ha="left", va="center",
                fontsize=11, color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_attributes")


# ============================================================
# СХЕМА 3. copy vs xcopy
# ============================================================

def scheme_copy_vs_xcopy():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.5)
    ax.axis("off")

    ax.text(6.5, 7.1, "copy та xcopy: у чому різниця",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    panels = [
        ("copy", "Для ОДНОГО файлу",
         ["Копіює файл або групу файлів за маскою",
          "НЕ копіює каталоги",
          "Синтаксис: copy <звідки> <куди>",
          "Приклад: copy звіт.txt D:\\Архів"],
         ACCENT_BLUE, "#E1F0FE"),
        ("xcopy", "Для КАТАЛОГІВ",
         ["Копіює каталоги зі всім вмістом",
          "Параметр /S — з підкаталогами",
          "Параметр /E — і порожні каталоги",
          "Приклад: xcopy Навчання D:\\Бекап /S /E"],
         ACCENT_GREEN, "#E8F8EC"),
    ]

    card_w, card_h = 6.1, 4.9
    gap = 0.3
    x0 = 0.3
    y0 = 1.0

    for i, (title, subtitle, lines, color, fill) in enumerate(panels):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2

        _card(ax, x, y0, card_w, card_h, fill=fill, border=color, radius=0.18)

        # Заголовок-бейдж
        _badge(ax, cx, y0 + card_h - 0.55, 2.4, 0.65, color, title,
               color="white", size=15, radius=0.32)

        ax.text(cx, y0 + card_h - 1.35, subtitle, ha="center", va="center",
                fontsize=13, fontweight="bold", color=color)

        # Рядки
        yy = y0 + card_h - 2.15
        for line in lines:
            ax.text(x + 0.4, yy, "•  " + line, ha="left", va="center",
                    fontsize=11, color=TEXT_DARK)
            yy -= 0.55

    return _save(fig, "scheme_copy_vs_xcopy")


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
        ("Рівень 1", "Базові операції",
         "copy, ren, del,\nattrib — з одним\nфайлом",
         "≈ 7 хв", ACCENT_GREEN, "#E8F8EC"),
        ("Рівень 2", "Маски й атрибути",
         "move, del за маскою,\nгрупові атрибути,\ndir /A",
         "≈ 10 хв", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Комплексний\nпроєкт",
         "xcopy каталогів,\nattrib +H /S /D,\nзвіт про результати",
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
        ax.text(cx, y0 + card_h - 1.55, name, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=TEXT_DARK,
                linespacing=1.4)
        ax.text(cx, y0 + card_h - 3.1, desc, ha="center", va="center",
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
    img2 = scheme_attributes()
    img3 = scheme_copy_vs_xcopy()
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
    theme_line(doc, "Копіювання, переміщення і видалення файлів і каталогів. "
                    "Перегляд інформації про файли та каталоги")

    h2(doc, "Мета")
    body(doc, "відпрацьовувати використання команд copy, move, del, ren, "
              "attrib для керування файлами та каталогами в командному "
              "рядку; розвивати алгоритмічне мислення через складання "
              "послідовностей команд для виконання типових завдань; "
              "виховувати уважність до синтаксису команд та "
              "відповідальність за результати їх виконання.")

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
        "Іванов О. В., Петрова Н. М. Основи операційних систем : навч. "
        "посіб. Київ : Основи, 2020.",
        "Микитишин А. Г., Чихіра І. В. Операційні системи : консп. лекц. "
        "Тернопіль : ТНТУ імені Івана Пулюя, 2016.",
        "Погребняк Б. І., Булаєнко М. В. Операційні системи : навч. посіб. "
        "Харків. нац. ун-т міськ. госп-ва ім. О. М. Бекетова. Харків : "
        "ХНУМГ ім. О. М. Бекетова, 2018.",
    ]
    for s in sources:
        numbered(doc, s)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Основні команди керування файлами")
    body(doc, "Командний рядок надає повний набір команд для копіювання, "
              "переміщення, видалення та перейменування файлів і "
              "каталогів. Кожна команда має власний синтаксис, який "
              "потрібно точно дотримуватися: помилка в одному символі "
              "може призвести до непередбачуваного результату.")

    add_figure(doc, img1, 16.0)

    add_table(
        doc,
        ["Команда", "Призначення", "Приклад"],
        [
            ["copy", "Копіювання файлу або групи файлів",
             "copy звіт.txt D:\\Архів"],
            ["move", "Переміщення файлу (оригінал зникає)",
             "move звіт.txt D:\\Архів"],
            ["del", "Видалення файлу",
             "del звіт.txt"],
            ["ren", "Перейменування файлу",
             "ren звіт.txt підсумок.txt"],
            ["attrib", "Перегляд і зміна атрибутів",
             "attrib +r звіт.txt"],
            ["xcopy", "Копіювання каталогів із вмістом",
             "xcopy Навчання D:\\Бекап /S /E"],
        ],
        widths=[2.8, 7.0, 6.7],
        mono_cols=[0, 2],
    )

    body(doc, "Ключова відмінність між copy і move: copy залишає оригінал "
              "на місці й створює його копію, а move переносить файл — у "
              "початковій папці його вже не буде. Обидві команди "
              "приймають як абсолютні, так і відносні шляхи.")

    h3(doc, "2. Копіювання каталогів: xcopy")
    body(doc, "Команда copy не призначена для каталогів: якщо вказати "
              "папку, система видасть повідомлення «The system cannot "
              "find the file specified» або «Invalid number of "
              "parameters». Для копіювання каталогів у Windows "
              "використовують xcopy (або сучаснішу robocopy).")

    add_figure(doc, img3, 16.0)

    bullet(doc, "/S — копіювати всі підкаталоги, крім порожніх;")
    bullet(doc, "/E — копіювати всі підкаталоги, у тому числі порожні;")
    bullet(doc, "/I — якщо кінцевий об'єкт не існує, вважати його "
                "каталогом (не запитувати підтвердження);")
    bullet(doc, "/Y — не запитувати підтвердження перезапису файлів.")

    h3(doc, "3. Перегляд інформації про файли та каталоги")
    body(doc, "Для перегляду інформації використовують команду dir із "
              "параметрами та команду attrib. Вони дозволяють побачити "
              "не лише назви, а й розміри, дати, атрибути та приховані "
              "файли.")

    add_table(
        doc,
        ["Команда", "Що показує"],
        [
            ["dir", "Список файлів і папок у поточному каталозі"],
            ["dir /A", "Усі файли, включаючи приховані та системні"],
            ["dir /A:H", "Тільки приховані файли"],
            ["dir /A:R", "Тільки файли з атрибутом «тільки читання»"],
            ["dir /S", "Рекурсивно: файли з усіх підкаталогів"],
            ["dir /O:N", "Сортувати за назвою"],
            ["dir /O:D", "Сортувати за датою змінення"],
            ["dir /T:W", "Показати дату й час змінення файлів"],
            ["attrib", "Атрибути файлів у поточній папці"],
            ["attrib /S /D", "Атрибути файлів і каталогів рекурсивно"],
        ],
        widths=[4.5, 12.0],
        mono_cols=[0],
    )

    h3(doc, "4. Атрибути файлів і команда attrib")
    body(doc, "Кожен файл має чотири основні атрибути, які можна "
              "переглянути й змінити командою attrib. Синтаксис: "
              "«attrib [+/-R] [+/-H] [+/-S] [+/-A] <файл>». Знак «+» "
              "встановлює атрибут, знак «-» — знімає.")

    add_figure(doc, img2, 16.0)

    body(doc, "Приклади використання:")
    code_line(doc, "attrib")
    body(doc, "показати атрибути всіх файлів у поточній папці.",
         space_after=2)
    code_line(doc, "attrib +r звіт.txt")
    body(doc, "встановити атрибут «тільки читання».", space_after=2)
    code_line(doc, "attrib -r -h звіт.txt")
    body(doc, "зняти атрибути «тільки читання» та «прихований».",
         space_after=2)
    code_line(doc, "attrib +h /S /D Приватне")
    body(doc, "приховати папку «Приватне» разом з усім вмістом "
              "(параметр /S — рекурсивно, /D — застосувати до папок).",
         space_after=2)
    code_line(doc, "dir /A:H")
    body(doc, "переглянути список прихованих файлів (переконатися, що "
              "атрибут справді встановлено).")

    callout(doc,
            "Приховати файл атрибутом H — це не захист, а лише зручність "
            "перегляду. Будь-хто, хто знає команду dir /A, побачить "
            "приховані файли. Для справжнього захисту даних "
            "використовують шифрування (BitLocker, EFS) або архівування "
            "з паролем.",
            fill="E1F0FE", accent="0071E3")

    h3(doc, "5. Безпека під час видалення та переміщення")
    body(doc, "Команди del, move та xcopy виконуються без підтвердження "
              "й без можливості «Скасувати». Тому важливо пам'ятати "
              "такі правила.")
    bullet(doc, "Перед del і move перевірте поточну папку командою cd і "
                "вміст папки командою dir.")
    bullet(doc, "Не використовуйте del *.* без попереднього перегляду "
                "вмісту: команда видалить усі файли у поточній папці.")
    bullet(doc, "Переміщення на інший диск (move) виконується як "
                "копіювання + видалення. Якщо копіювання не вдалося, "
                "оригінал може залишитися на місці або, навпаки, бути "
                "вже видаленим — перевіряйте результат.")
    bullet(doc, "Файл з атрибутом R (тільки читання) не видаляється "
                "командою del без попереднього зняття атрибута — це "
                "додатковий захист.")

    callout(doc,
            "Якщо команда видалила щось зайве, відновити вміст можна з "
            "резервної копії або з «Кошика» (якщо видалення виконувалося "
            "через графічний інтерфейс). Команда del у командному рядку "
            "видаляє файли остаточно, минаючи Кошик.",
            fill="FFEBEA", accent="C4001D")

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
    h3(doc, "Рівень 1 — базові операції (≈ 7 хв)",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Мета: відпрацювати copy, ren, del, attrib на одному файлі.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Відкрийте командний рядок",
             "Win + R → cmd → Enter"],
            ["2", "Перейдіть на робочий диск", "D:  (або C:)"],
            ["3", "Створіть робочу папку", "mkdir ПЗ_Файли_ПІБ"],
            ["4", "Перейдіть до неї", "cd ПЗ_Файли_ПІБ"],
            ["5", "Створіть файл зі змістом",
             "echo Тестовий вміст > джерело.txt"],
            ["6", "Скопіюйте файл",
             "copy джерело.txt копія.txt"],
            ["7", "Перевірте наявність двох файлів", "dir"],
            ["8", "Перейменуйте копію",
             "ren копія.txt звіт.txt"],
            ["9", "Перегляньте атрибути обох файлів", "attrib"],
            ["10", "Встановіть атрибут «тільки читання»",
             "attrib +r звіт.txt"],
            ["11", "Спробуйте видалити захищений файл",
             "del звіт.txt  (має з'явитися запит на підтвердження "
             "або відмова)"],
            ["12", "Зніміть атрибут і видаліть файл",
             "attrib -r звіт.txt\ndel звіт.txt"],
            ["13", "Зробіть скріншот",
             "Print Screen; вставте у звіт із підписом"],
        ],
        widths=[1.0, 5.8, 9.7],
        mono_cols=[2],
    )

    callout(doc,
            "Після виконання рівня 1 у папці «ПЗ_Файли_ПІБ» має "
            "залишитися один файл — «джерело.txt». Файл «звіт.txt» "
            "має бути видалений.",
            fill="E8F8EC", accent="248A3D")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — маски й атрибути (≈ 10 хв)",
       color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Мета: навчитися працювати з масками (зірочка, знак "
              "питання), застосовувати move для переміщення між папками "
              "та змінювати атрибути групи файлів.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Створіть три файли",
             "echo 1 > урок_1.txt\necho 2 > урок_2.txt\n"
             "echo 3 > урок_3.txt"],
            ["2", "Створіть папку «Архів»", "mkdir Архів"],
            ["3", "Скопіюйте групу файлів за маскою",
             "copy урок_*.txt Архів"],
            ["4", "Перевірте вміст папки «Архів»", "dir Архів"],
            ["5", "Перемістіть один файл із кореня в «Архів»",
             "move урок_2.txt Архів"],
            ["6", "Перевірте, що урок_2.txt зник із кореня", "dir"],
            ["7", "Встановіть атрибут R для всіх txt у «Архіві»",
             "attrib +r Архів\\*.txt"],
            ["8", "Перегляньте атрибути в «Архіві»", "attrib Архів\\*.txt"],
            ["9", "Перевірте пошук за атрибутом",
             "dir /A:R Архів"],
            ["10", "Приховайте папку «Архів» разом зі вмістом",
             "attrib +h Архів"],
            ["11", "Перевірте, що папки не видно у звичайному списку",
             "dir  →  Архів відсутній"],
            ["12", "Перегляньте приховані об'єкти",
             "dir /A:H"],
            ["13", "Зніміть атрибут H із папки",
             "attrib -h Архів"],
            ["14", "Зробіть скріншот",
             "Знімок вікна з результатом кроків 8 і 12"],
        ],
        widths=[1.0, 5.8, 9.7],
        mono_cols=[2],
    )

    callout(doc,
            "У звіті має бути: скріншот атрибутів файлів папки «Архів» "
            "(усі txt мають позначку R), скріншот прихованих об'єктів "
            "командою dir /A:H і коротке пояснення, чим відрізняються "
            "результати команд dir і dir /A:H.",
            fill="FFF4E5", accent="C93400")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — комплексний проєкт (≈ 10 хв)",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Мета: створити багаторівневу структуру, наповнити її "
              "файлами, виконати копіювання каталогів командою xcopy та "
              "перевірити атрибути.")

    body(doc, "Завдання А. Створіть структуру папок:")
    code_line(doc, "Проєкт\\")
    code_line(doc, "├── Джерело\\")
    code_line(doc, "│   ├── урок_1.txt")
    code_line(doc, "│   ├── урок_2.txt")
    code_line(doc, "│   └── Матеріали\\")
    code_line(doc, "│       └── схема.txt")
    code_line(doc, "└── Бекап\\   (поки порожня)")

    body(doc, "Завдання Б. Виконайте операції:")
    tasks_b = [
        "Створіть папки «Проєкт\\Джерело» та «Проєкт\\Бекап».",
        "У папці «Джерело» створіть файли «урок_1.txt», «урок_2.txt» "
        "та підпапку «Матеріали» з файлом «схема.txt».",
        "Скопіюйте каталог «Джерело» у «Бекап» командою "
        "xcopy Джерело Бекап\\Джерело /S /E /I.",
        "Перевірте, що в «Бекап\\Джерело» є всі файли та підпапки "
        "командою tree /F.",
        "Встановіть атрибут R для всіх txt-файлів у «Бекап\\Джерело».",
        "Перегляньте атрибути рекурсивно командою attrib /S.",
        "Спробуйте змінити вміст файлу з атрибутом R командою "
        "echo Зміна >> Бекап\\Джерело\\урок_1.txt — система має "
        "відмовити.",
        "Зніміть атрибут R і повторіть зміну — тепер успішно.",
        "Видаліть папку «Бекап» разом з усім вмістом командою "
        "rmdir /S /Q Бекап.",
        "Зробіть скріншот кінцевого дерева «Проєкт» командою tree /F.",
    ]
    for t in tasks_b:
        numbered(doc, t)

    body(doc, "Завдання В. У звіті наведіть:")
    numbered(doc, "повну послідовність команд, які ви виконали;")
    numbered(doc, "пояснення, чому параметр /S у xcopy не копіює "
                  "порожні каталоги, а /E — копіює;")
    numbered(doc, "пояснення, чому атрибут R заважає зміні файлу;")
    numbered(doc, "короткий висновок (3–4 речення) про те, які команди "
                  "виявилися найзручнішими для роботи з групами файлів.")

    callout(doc,
            "За бажанням (+1 бал). Запропонуйте, як однією командою "
            "xcopy зробити резервну копію папки «Джерело» у папку "
            "«Бекап\\Копія_2024», щоб у ній не було файлів із "
            "розширенням .tmp. Поясніть, який параметр xcopy для цього "
            "використовується.",
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
             "Усі 13 кроків виконано правильно; у папці рівно один "
             "файл; є скріншот", "3"],
            ["Рівень 2",
             "Файли створено й переміщено; copy за маскою та move "
             "працюють коректно; атрибути змінено й перевірено; "
             "є скріншот", "4"],
            ["Рівень 3",
             "Створено структуру; xcopy /S /E /I виконано правильно; "
             "атрибути перевірено; rmdir /S /Q виконано; є скріншот "
             "і пояснення", "4"],
            ["Якість звіту",
             "Оформлення за вимогами; підписи до скріншотів; "
             "наведено повну послідовність команд", "1"],
            ["Творчий підхід",
             "Виконано ускладнення з xcopy /EXCLUDE або запропоновано "
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
        "Скріншот папки після рівня 1 з підписом.",
        "Скріншот атрибутів (attrib Архів\\*.txt) і прихованих "
        "об'єктів (dir /A:H) після рівня 2.",
        "Скріншот дерева (tree /F) після рівня 3.",
        "Повна послідовність команд кожного рівня (моноширинним "
        "шрифтом).",
        "Відповіді на питання: чим copy відрізняється від xcopy; що "
        "робить параметр /S у xcopy; чому атрибут R заважає зміні.",
        "Висновок: що нового засвоїли, які команди виконували "
        "впевнено, а які потребують додаткового тренування.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, "
              "шрифт Times New Roman 14 pt, інтервал 1,15, поля 2 см, "
              "обсяг — 3–5 сторінок без титульної. Ім'я файлу: "
              "«Практика_Операції_cmd_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    doc.save("Практичне_заняття_Копіювання_Переміщення_Видалення.docx")
    print("Готово: Практичне_заняття_Копіювання_Переміщення_Видалення.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()