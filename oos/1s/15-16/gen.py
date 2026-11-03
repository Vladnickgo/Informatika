# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Основи роботи з командним рядком Windows
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

# Палітра в стилі системних кольорів
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
# СХЕМА 1. Вікно командного рядка
# ============================================================

def scheme_cmd_window():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    ax.text(6.5, 7.75, "Вікно командного рядка",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Вікно термінала
    ax.add_patch(FancyBboxPatch((0.4, 2.4), 12.2, 5.0,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=TERM_BG, edgecolor="#3A3A3C",
                                linewidth=1.6))
    # Заголовок вікна
    ax.add_patch(Rectangle((0.4, 7.0), 12.2, 0.4, facecolor=TERM_TITLE))
    ax.text(0.7, 7.2, "C:\\WINDOWS\\system32\\cmd.exe",
            ha="left", va="center", fontsize=10,
            color="#A1A1A6", family="monospace")

    # Запрошення + команда
    ax.text(0.7, 6.55, "C:\\Users\\Student>", ha="left", va="center",
            fontsize=11, color=TERM_PROMPT, fontweight="bold",
            family="monospace")
    ax.text(3.9, 6.55, " dir", ha="left", va="center",
            fontsize=11, color=TERM_CMD, fontweight="bold",
            family="monospace")

    # Вивід
    outputs = [
        (5.95, " Том у пристрої C не має мітки."),
        (5.40, " Серійний номер тому: 1234-ABCD"),
        (4.85, ""),
        (4.30, " Каталог: C:\\Users\\Student"),
        (3.75, ""),
        (3.20, " <DIR>          Documents"),
        (2.65, " <DIR>          Downloads"),
    ]
    for y, line in outputs:
        ax.text(0.7, y, line, ha="left", va="center",
                fontsize=10.5, color=TERM_TEXT, family="monospace")

    # Легенда під терміналом
    legend = [
        ("Запрошення", "запрошення до введення", TERM_PROMPT),
        ("Команда", "те, що ви набрали", TERM_CMD),
        ("Результат", "вивід системи", TERM_TEXT),
    ]
    cw, ch = 4.0, 1.4
    gap = 0.15
    x0 = 0.4
    y0 = 0.5
    for i, (title, desc, color) in enumerate(legend):
        x = x0 + i * (cw + gap)
        _card(ax, x, y0, cw, ch, fill=CARD_BG, border=CARD_BORDER, radius=0.18)
        border = "#3A3A3C" if color == TERM_CMD else color
        ax.add_patch(FancyBboxPatch((x + 0.2, y0 + ch - 0.55), 0.28, 0.32,
                                    boxstyle="round,pad=0.02,rounding_size=0.05",
                                    facecolor=color, edgecolor=border,
                                    linewidth=1.0))
        ax.text(x + 0.65, y0 + ch - 0.38, title, ha="left", va="center",
                fontsize=12, fontweight="bold", color=TEXT_DARK)
        ax.text(x + 0.2, y0 + 0.45, desc, ha="left", va="center",
                fontsize=10.5, color=TEXT_GRAY)

    return _save(fig, "scheme_cmd_window")


# ============================================================
# СХЕМА 2. Основні команди
# ============================================================

def scheme_commands_map():
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.5, 8.05, "Основні команди командного рядка",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    commands = [
        ("dir", "Перегляд вмісту\nпоточної папки", ACCENT_BLUE),
        ("cd", "Перехід до іншої\nпапки", ACCENT_GREEN),
        ("mkdir", "Створення\nнової папки", ACCENT_ORANGE),
        ("rmdir", "Видалення\nпорожньої папки", ACCENT_ORANGE),
        ("del", "Видалення\nфайлу", ACCENT_RED),
        ("copy", "Копіювання\nфайлу", ACCENT_BLUE),
        ("cls", "Очищення\nекрана", ACCENT_PURPLE),
        ("tree", "Дерево\nкаталогів", ACCENT_GREEN),
        ("exit", "Закриття\nвікна", ACCENT_RED),
    ]

    card_w, card_h = 3.9, 2.15
    gap_x, gap_y = 0.25, 0.25
    x0 = (13 - (3 * card_w + 2 * gap_x)) / 2
    y_top = 7.4

    for i, (cmd, desc, color) in enumerate(commands):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h)
        _badge(ax, cx, y + card_h - 0.55, 2.2, 0.55, color, cmd,
               color="white", size=13.5, radius=0.28)
        ax.text(cx, y + 0.85, desc, ha="center", va="center",
                fontsize=11.5, color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_commands_map")


# ============================================================
# СХЕМА 3. Навігація дерева каталогів
# ============================================================

def scheme_navigation():
    fig, ax = plt.subplots(figsize=(11, 7.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    ax.text(6.5, 7.75, "Навігація дерева каталогів",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    def node(cx, cy, label, current=False):
        w, h = 1.9, 0.55
        fc = ACCENT_BLUE if current else "#E1F0FE"
        tc = "white" if current else TEXT_DARK
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=fc, edgecolor=ACCENT_BLUE,
                                    linewidth=1.4))
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=11, fontweight="bold", color=tc)

    def link(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color=TEXT_GRAY, linewidth=1.6)

    # Дерево
    node(2.5, 6.3, "C:\\")
    node(2.5, 5.4, "Users\\")
    node(2.5, 4.5, "Student\\")
    node(1.3, 3.6, "Documents\\", current=True)
    node(3.7, 3.6, "Public\\")
    node(1.3, 2.7, "report.docx")

    link(2.5, 6.03, 2.5, 5.68)
    link(2.5, 5.13, 2.5, 4.78)
    link(2.5, 4.23, 1.3, 3.88)
    link(2.5, 4.23, 3.7, 3.88)
    link(1.3, 3.33, 1.3, 2.98)

    # Нотатка під деревом
    ax.text(2.5, 1.5, "Синя папка — поточна",
            ha="center", va="center", fontsize=11, style="italic",
            color=ACCENT_BLUE)

    # Команди навігації праворуч
    cmds = [
        ("cd Documents", "вниз, у підпапку", ACCENT_GREEN),
        ("cd ..", "вгору, до батьківської", ACCENT_ORANGE),
        ("cd \\", "до кореня диска", ACCENT_BLUE),
        ("cd ..\\..", "на два рівні вгору", ACCENT_RED),
    ]

    cw, ch = 7.0, 1.15
    cx = 9.0
    y = 6.35

    for cmd, desc, color in cmds:
        x = cx - cw / 2
        _card(ax, x, y, cw, ch, fill=CARD_BG, border=CARD_BORDER, radius=0.15)
        _badge(ax, x + 1.45, y + ch / 2, 2.5, 0.6, color, cmd,
               color="white", size=12, radius=0.3)
        ax.text(x + 3.0, y + ch / 2, desc, ha="left", va="center",
                fontsize=11.5, color=TEXT_DARK)
        y -= 1.45

    return _save(fig, "scheme_navigation")


# ============================================================
# СХЕМА 4. Три рівні завдань
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
        ("Рівень 1", "Базові команди",
         "dir, cd, mkdir,\ncls — окремі\nпрості команди",
         "≈ 7 хв", ACCENT_GREEN, "#E8F8EC"),
        ("Рівень 2", "Навігація\nта файли",
         "переміщення деревом,\ncopy, ren, del,\ntree — зв'язки",
         "≈ 10 хв", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Комплексний\nпроєкт",
         "структура папок\nі наповнення файлами\nлише через cmd",
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
    """Рядок із моноширинним шрифтом — для команд cmd."""
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


def add_table(doc, headers, rows, widths):
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
    img1 = scheme_cmd_window()
    img2 = scheme_commands_map()
    img3 = scheme_navigation()
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
    theme_line(doc, "Основи роботи з командним рядком Windows. "
                    "Використання основних команд: cd, dir, mkdir, rmdir тощо")

    h2(doc, "Мета")
    body(doc, "навчати студентів основам роботи в командному рядку Windows, "
              "введенню базових команд навігації та керування каталогами; "
              "розвивати абстрактно-логічне мислення через роботу без "
              "графічного інтерфейсу, текстовим способом; виховувати терпіння "
              "та посидючість під час освоєння текстового інтерфейсу як "
              "невід'ємної частини ІТ-професії.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Командний рядок cmd (Windows) або термінал Windows Terminal.",
        "Інструкційні картки до рівнів 1–3.",
        "Текстовий редактор для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Загорулько М. І., Сідоров О. М. Операційні системи: практикум. "
        "Київ : Наукова думка, 2019.",
        "Зайцев В. Г., Дробязко І. П. Операційні системи : навч. посіб. для "
        "студ. спец. 123 «Комп'ютерна інженерія». Київ : КПІ ім. Ігоря "
        "Сікорського, 2019.",
        "Іванов О. В., Петрова Н. М. Основи операційних систем : навч. "
        "посіб. Київ : Основи, 2020.",
    ]
    for s in sources:
        numbered(doc, s)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Що таке командний рядок")
    body(doc, "Командний рядок — це текстовий інтерфейс операційної системи, "
              "у якому користувач вводить команди вручну, а система виконує "
              "їх і виводить результат у вигляді тексту. На відміну від "
              "графічного інтерфейсу, тут немає вікон, кнопок і миші — усе "
              "керується з клавіатури. У Windows командний рядок запускається "
              "програмою cmd.exe (скорочено — cmd).")

    add_figure(doc, img1, 16.0)

    body(doc, "Вікно командного рядка складається з трьох частин: "
              "запрошення (prompt), у якому видно поточну папку; власне "
              "команди, яку ви набрали; результату — тексту, що виводить "
              "система. Після виконання команди знову з'являється запрошення "
              "— і цикл повторюється.")

    callout(doc,
            "Відкрити командний рядок можна так: натиснути Win + R, ввести "
            "cmd і натиснути Enter. Або скористатися пошуком у меню "
            "«Пуск». Для запуску від імені адміністратора — права кнопка "
            "миші на «Командний рядок» → «Запуск від імені адміністратора».",
            fill="E1F0FE", accent="0071E3")

    h3(doc, "2. Синтаксис команд")
    body(doc, "Загальний вигляд команди такий:")
    code_line(doc, "назва_команди [параметри] [об'єкт]")
    body(doc, "де «назва_команди» — сама команда (наприклад, dir), "
              "«параметри» — додаткові налаштування (наприклад, /F для "
              "tree), «об'єкт» — файл, папка або шлях, до якого "
              "застосовується команда. Усі складові розділяються пробілами. "
              "Регістр літер значення не має: dir, DIR і Dir — те саме.")

    h3(doc, "3. Основні команди")
    body(doc, "Нижче наведено команди, які найчастіше використовуються під "
              "час роботи з файловою системою.")

    add_figure(doc, img2, 16.0)

    add_table(
        doc,
        ["Команда", "Синтаксис", "Призначення"],
        [
            ["dir", "dir [шлях]", "Перегляд вмісту каталогу"],
            ["cd", "cd [шлях]", "Зміна поточного каталогу"],
            ["cd ..", "cd ..", "Перехід до батьківської папки"],
            ["cd \\", "cd \\", "Перехід до кореня диска"],
            ["mkdir / md", "mkdir <ім'я>", "Створення каталогу"],
            ["rmdir / rd", "rmdir <ім'я>", "Видалення порожнього каталогу"],
            ["del", "del <файл>", "Видалення файлу"],
            ["copy", "copy <звідки> <куди>", "Копіювання файлу"],
            ["move", "move <звідки> <куди>", "Переміщення файлу"],
            ["ren", "ren <старе> <нове>", "Перейменування файлу"],
            ["type", "type <файл>", "Виведення вмісту файлу"],
            ["echo", "echo <текст>", "Виведення тексту на екран"],
            ["cls", "cls", "Очищення екрана"],
            ["tree", "tree [/F]", "Дерево каталогів (з /F — із файлами)"],
            ["exit", "exit", "Закриття вікна командного рядка"],
        ],
        widths=[3.2, 5.4, 7.9],
    )

    h3(doc, "4. Навігація деревом каталогів")
    body(doc, "Команда cd — головний інструмент переміщення файловою "
              "структурою. Вона розуміє як абсолютні, так і відносні шляхи. "
              "Символи «..» позначають батьківську папку, «\\» — корінь "
              "диска, «.» — поточну папку. Кілька «..» поспіль дозволяють "
              "піднятися на кілька рівнів угору.")

    add_figure(doc, img3, 16.0)

    body(doc, "Приклади переходів від папки C:\\Users\\Student:")
    bullet(doc, "cd Documents — перехід у підпапку Documents;")
    bullet(doc, "cd .. — перехід до C:\\Users;")
    bullet(doc, "cd ..\\.. — перехід до C:\\;")
    bullet(doc, "cd \\Users\\Public — перехід до C:\\Users\\Public "
                "за абсолютним шляхом.")

    h3(doc, "5. Безпека під час роботи з командним рядком")
    body(doc, "Командний рядок не має графічного підтвердження дій: "
              "виконана команда спрацьовує відразу. Тому важливо бути "
              "уважним і пам'ятати кілька правил.")

    bullet(doc, "Перед виконанням команди del або rmdir перевірте поточну "
                "папку командою cd.")
    bullet(doc, "Команда rmdir без параметра /S не видаляє непорожні "
                "каталоги — це запобіжник від випадкової втрати даних.")
    bullet(doc, "Не використовуйте символи-джокери (наприклад, del *.*) "
                "без попереднього перегляду вмісту папки командою dir.")
    bullet(doc, "Для перегляду довідки про будь-яку команду введіть "
                "help <назва> або <назва> /?.")

    callout(doc,
            "Командний рядок виконує команду відразу після натискання "
            "Enter і не має звичного «Скасувати». Якщо команду введено "
            "помилково — наслідки усуваються лише вручну або з резервної "
            "копії.",
            fill="FFEBEA", accent="C4001D")

    # =====================================================
    # РІВНІ ПРАКТИЧНИХ ЗАВДАНЬ
    # =====================================================
    h2(doc, "Покроковий алгоритм виконання різнорівневих завдань")

    body(doc, "Практична частина заняття побудована за трирівневою "
              "системою. Студент виконує завдання послідовно; орієнтовний "
              "час на кожен рівень — 7–10 хвилин, загальна тривалість — "
              "25–30 хвилин. Оцінка залежить від кількості успішно "
              "виконаних рівнів.")

    add_figure(doc, img4, 16.0)

    # -------- Рівень 1 --------
    h3(doc, "Рівень 1 — базові команди (≈ 7 хв)",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Мета: навчитися запускати командний рядок, орієнтуватися в "
              "поточній папці та виконувати прості команди dir, cd, mkdir, "
              "cls.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Відкрийте командний рядок",
             "Win + R → введіть cmd → Enter"],
            ["2", "Перегляньте поточну папку",
             "cd  (без аргументів)"],
            ["3", "Перегляньте вміст поточної папки",
             "dir"],
            ["4", "Очистіть екран",
             "cls"],
            ["5", "Перейдіть на диск D:",
             "D:  (якщо диска D: немає — залишайтеся на C:)"],
            ["6", "Створіть робочу папку",
             "mkdir Практика_ПІБ  (наприклад, mkdir Практика_Іваненко)"],
            ["7", "Перейдіть у створену папку",
             "cd Практика_ПІБ"],
            ["8", "Перевірте нову поточну папку",
             "cd  — запрошення має показати новий шлях"],
            ["9", "Зробіть скріншот",
             "Print Screen; вставте у звіт із підписом"],
        ],
        widths=[1.0, 5.6, 9.9],
    )

    callout(doc,
            "Після виконання рівня 1 запрошення командного рядка має "
            "виглядати приблизно так: D:\\Практика_Іваненко> (або "
            "C:\\Users\\Student\\Практика_Іваненко>). Якщо це не так — "
            "перевірте, чи правильно ви виконали перехід.",
            fill="E8F8EC", accent="248A3D")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — навігація та файли (≈ 10 хв)",
       color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Мета: навчитися переміщуватися деревом каталогів, "
              "створювати, копіювати, перейменовувати та видаляти файли "
              "командами copy, ren, del, tree.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Створіть три підпапки",
             "mkdir Документи\nmkdir Фото\nmkdir Архів"],
            ["2", "Перейдіть у папку Документи",
             "cd Документи"],
            ["3", "Створіть файл зі змістом",
             "echo Привіт, командний рядок! > звіт.txt"],
            ["4", "Перевірте вміст файлу",
             "type звіт.txt"],
            ["5", "Перегляньте вміст папки",
             "dir"],
            ["6", "Перейдіть до батьківської папки",
             "cd .."],
            ["7", "Перейдіть у папку Архів",
             "cd Архів"],
            ["8", "Скопіюйте файл із Документів",
             "copy ..\\Документи\\звіт.txt ."],
            ["9", "Перейменуйте файл",
             "ren звіт.txt архів.txt"],
            ["10", "Виведіть дерево каталогів",
             "cd ..\ntree /F"],
            ["11", "Зробіть скріншот",
             "Знімок вікна з результатом tree /F"],
        ],
        widths=[1.0, 5.6, 9.9],
    )

    callout(doc,
            "У звіті має бути: скріншот дерева tree /F, коротке пояснення, "
            "чим команда copy відрізняється від move, і чому ren не може "
            "перенести файл до іншої папки.",
            fill="FFF4E5", accent="C93400")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — комплексний проєкт (≈ 10 хв)",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Мета: створити багаторівневу структуру папок і наповнити її "
              "файлами, користуючись ЛИШЕ командним рядком. Усі дії "
              "виконуються послідовно, без графічного інтерфейсу.")

    body(doc, "Завдання А. Створіть у папці «Практика_ПІБ» таку структуру:")
    code_line(doc, "Student\\")
    code_line(doc, "├── 1_Клас\\")
    code_line(doc, "│   ├── Уроки\\")
    code_line(doc, "│   └── Матеріали\\")
    code_line(doc, "├── 2_Клас\\")
    code_line(doc, "│   └── Уроки\\")
    code_line(doc, "└── Архів\\")

    body(doc, "Завдання Б. Наповніть структуру файлами (лише через cmd):")
    tasks_b = [
        "У папці Student\\1_Клас\\Уроки створіть файл «урок_1.txt» "
        "із довільним текстом.",
        "У папці Student\\2_Клас\\Уроки створіть файл «урок_2.txt» "
        "із довільним текстом.",
        "Скопіюйте «урок_1.txt» у папку Архів.",
        "Перейменуйте копію у «архів_уроку.txt».",
        "Виведіть повне дерево командою tree /F.",
        "Зробіть скріншот кінцевого дерева.",
    ]
    for t in tasks_b:
        numbered(doc, t)

    body(doc, "Завдання В. Складіть у звіті послідовність команд, які ви "
              "використали для кожного кроку. Поясніть, чому команда "
              "rmdir не спрацює для видалення папки з файлами, і який "
              "параметр потрібно додати, щоб видалити непорожню папку.")

    callout(doc,
            "За бажанням (+1 бал). Запишіть однорядковий ланцюжок команд "
            "для створення всіх папок структури однією командою, "
            "використовуючи оператор && (наприклад: mkdir A && "
            "cd A && mkdir B). Поясніть, що робить цей оператор.",
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
             "Усі 9 кроків виконано правильно; поточна папка відповідає "
             "очікуваній; є скріншот", "3"],
            ["Рівень 2",
             "Створено три підпапки; файли створено й перевірено; "
             "виконано copy та ren; дерево tree /F відображає структуру",
             "4"],
            ["Рівень 3",
             "Створено повну структуру (7 папок); файли розміщено; "
             "виконано копіювання та перейменування; є скріншот і "
             "пояснення", "4"],
            ["Якість звіту",
             "Оформлення за вимогами; підписи до скріншотів; наведені "
             "послідовності команд", "1"],
            ["Творчий підхід",
             "Виконано ускладнення з ланцюжком && або запропоновано "
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
        "Титульна сторінка: навчальний заклад, тема, ПІБ студента, група, "
        "ПІБ викладача, дата.",
        "Скріншот вікна командного рядка після рівня 1 з підписом "
        "(видно поточну папку).",
        "Скріншот дерева tree /F після рівня 2 з коротким коментарем.",
        "Скріншот кінцевої структури папок після рівня 3.",
        "Послідовності команд для кожного кроку рівня 3 (у вигляді "
        "моноширинного списку).",
        "Відповіді на питання: чим copy відрізняється від move; чому "
        "ren не може перенести файл; що робить параметр /S у rmdir.",
        "Висновок: що нового засвоїли, які команди виконували впевнено, "
        "а які потребують додаткового тренування.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, "
              "шрифт Times New Roman 14 pt, інтервал 1,15, поля 2 см, "
              "обсяг — 3–5 сторінок без титульної. Ім'я файлу: "
              "«Практика_Командний_рядок_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    doc.save("Практичне_заняття_Командний_рядок.docx")
    print("Готово: Практичне_заняття_Командний_рядок.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()