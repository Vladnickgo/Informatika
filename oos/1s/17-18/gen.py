# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: САМОСТІЙНА РОБОТА
Тема: Робота з файлами і каталогами в командному рядку
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

# Палітра системних кольорів (Apple style)
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
# СХЕМА 1. Класифікація команд
# ============================================================

def scheme_commands_classification():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.5, 8.1, "Класифікація команд командного рядка",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    groups = [
        ("Навігація", "cd, dir, tree",
         "Переміщення деревом\nкаталогів та перегляд\nвмісту папок",
         ACCENT_BLUE, "#E1F0FE"),
        ("Керування каталогами", "mkdir, rmdir",
         "Створення\nта видалення папок",
         ACCENT_GREEN, "#E8F8EC"),
        ("Робота з файлами", "copy, move, del, ren, type",
         "Копіювання, видалення,\nперейменування, перегляд",
         ACCENT_ORANGE, "#FFF4E5"),
        ("Службові", "cls, help, exit",
         "Очищення екрана,\nдовідка, вихід",
         ACCENT_PURPLE, "#EFE6F7"),
    ]

    card_w, card_h = 6.0, 3.1
    gap_x, gap_y = 0.35, 0.3
    x0 = 0.3
    y_top = 7.6

    for i, (title, cmds, desc, color, fill) in enumerate(groups):
        col, row = i % 2, i // 2
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.18)
        ax.text(cx, y + card_h - 0.45, title, ha="center", va="center",
                fontsize=13, fontweight="bold", color=color)
        ax.text(cx, y + card_h - 1.55, cmds, ha="center", va="center",
                fontsize=12, fontweight="bold", color=TEXT_DARK,
                family="monospace")
        ax.text(cx, y + 0.75, desc, ha="center", va="center",
                fontsize=11.5, color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_commands_classification")


# ============================================================
# СХЕМА 2. Будова команди
# ============================================================

def scheme_syntax():
    fig, ax = plt.subplots(figsize=(11, 5.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    ax.text(6.5, 6.65, "Будова команди командного рядка",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Повний приклад команди
    _card(ax, 0.5, 5.4, 12.0, 0.85, fill="#F5F5F7", border=CARD_BORDER, radius=0.15)
    ax.text(6.5, 5.82, "dir     C:\\Users\\Student     /A",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=TEXT_DARK, family="monospace")

    # Розбір на три складові
    rows = [
        ("dir", "КОМАНДА",
         "ЩО зробити. Регістр не важливий: dir = DIR = Dir.",
         ACCENT_BLUE, "#E1F0FE"),
        ("C:\\Users\\Student", "ОБ'ЄКТ (ШЛЯХ)",
         "З ЧИМ працювати. Якщо пропущено — діє поточна папка.",
         ACCENT_GREEN, "#E8F8EC"),
        ("/A", "ПАРАМЕТР",
         "ЯК САМЕ. Додаткове налаштування; починається з «/».",
         ACCENT_ORANGE, "#FFF4E5"),
    ]

    y = 4.2
    for code, label, desc, color, fill in rows:
        # Чип із кодом
        chip_w = 3.0 if len(code) > 5 else 1.8
        ax.add_patch(FancyBboxPatch((0.5, y - 0.35), chip_w, 0.7,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=fill, edgecolor=color, linewidth=1.5))
        ax.text(0.5 + chip_w / 2, y, code, ha="center", va="center",
                fontsize=12, fontweight="bold", color=color,
                family="monospace")
        # Підпис і опис
        ax.text(0.5 + chip_w + 0.35, y + 0.14, label, ha="left", va="center",
                fontsize=11, fontweight="bold", color=color)
        ax.text(0.5 + chip_w + 0.35, y - 0.14, desc, ha="left", va="center",
                fontsize=10.5, color=TEXT_DARK)
        y -= 1.35

    return _save(fig, "scheme_syntax")


# ============================================================
# СХЕМА 3. Етапи самостійної роботи
# ============================================================

def scheme_steps():
    fig, ax = plt.subplots(figsize=(11, 8.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    ax.text(6.5, 9.1, "Етапи виконання самостійної роботи",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    steps = [
        "Опрацювати теоретичний матеріал і схеми 1–2",
        "Заповнити таблицю команд: синтаксис, призначення, приклад",
        "Скласти шпаргалку з 5 правил безпеки",
        "Виконати практичне завдання за інструкційною карткою",
        "Дати відповіді на теоретичні питання (письмово)",
        "Оформити звіт і надіслати викладачу",
    ]

    card_w, card_h = 9.5, 0.85
    x0 = 2.0
    y_top = 8.3

    for i, step in enumerate(steps):
        y = y_top - i * 1.35
        cx = x0 + card_w / 2
        _card(ax, x0, y - card_h / 2, card_w, card_h,
              fill=CARD_BG, border=CARD_BORDER, radius=0.15)
        _badge(ax, 1.3, y, 0.6, 0.6, ACCENT_BLUE, str(i + 1),
               color="white", size=14, radius=0.3)
        ax.text(cx, y, step, ha="center", va="center",
                fontsize=11.5, color=TEXT_DARK)
        if i < len(steps) - 1:
            ax.annotate("", xy=(cx, y - card_h / 2 - 0.45),
                        xytext=(cx, y - card_h / 2 - 0.02),
                        arrowprops=dict(arrowstyle="-|>", color=TEXT_GRAY,
                                        linewidth=1.4, mutation_scale=12))

    return _save(fig, "scheme_steps")


# ============================================================
# СХЕМА 4. Типові помилки
# ============================================================

def scheme_mistakes():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.5, 8.1, "Типові помилки початківців",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    mistakes = [
        ("Пробіли в назвах", "mkdir Моя папка",
         "Створить ДВІ папки: «Моя» і «папка».\n"
         "Правильно: mkdir Моя_папка",
         ACCENT_RED, "#FFEBEA"),
        ("Видалення непорожньої папки", "rmdir Навчання",
         "Помилка «The directory is not empty».\n"
         "Правильно: rmdir /S Навчання",
         ACCENT_ORANGE, "#FFF4E5"),
        ("Символи-джокери без перевірки", "del *.*",
         "Видалить УСІ файли у поточній папці.\n"
         "Спочатку перевірте: dir",
         ACCENT_RED, "#FFEBEA"),
        ("Забуті «..» у навігації", "cd Documents",
         "Спрацює лише, якщо Documents є\nу поточній папці. Перевірте: dir",
         ACCENT_BLUE, "#E1F0FE"),
    ]

    card_w, card_h = 6.0, 3.4
    gap_x, gap_y = 0.35, 0.35
    x0 = 0.3
    y_top = 7.6

    for i, (title, bad_cmd, desc, color, fill) in enumerate(mistakes):
        col, row = i % 2, i // 2
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2

        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.18)
        ax.text(cx, y + card_h - 0.45, title, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=color)

        # "Погана" команда в темному чипі
        ax.add_patch(FancyBboxPatch((x + 0.5, y + card_h - 1.6),
                                     card_w - 1.0, 0.65,
                                     boxstyle="round,pad=0.02,rounding_size=0.1",
                                     facecolor=TERM_BG, edgecolor="#3A3A3C",
                                     linewidth=1.2))
        ax.text(cx, y + card_h - 1.27, "✗  " + bad_cmd,
                ha="center", va="center", fontsize=11.5, fontweight="bold",
                color="#FF453A", family="monospace")

        ax.text(cx, y + 0.95, desc, ha="center", va="center",
                fontsize=10.5, color=TEXT_DARK, linespacing=1.55)

    return _save(fig, "scheme_mistakes")


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
    img1 = scheme_commands_classification()
    img2 = scheme_syntax()
    img3 = scheme_steps()
    img4 = scheme_mistakes()

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

    h1(doc, "Самостійна робота")
    theme_line(doc, "Робота з файлами і каталогами в командному рядку")

    # ---------- Мета ----------
    h2(doc, "Мета")
    body(doc, "поглибити знання про команди для створення, перегляду та "
              "зміни каталогів у командному рядку; розвивати самостійність "
              "у вирішенні практичних завдань без використання графічних "
              "інструментів; формувати наполегливість у подоланні труднощів "
              "під час вивчення командного рядка.")

    # ---------- Обладнання ----------
    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Командний рядок cmd або Windows Terminal.",
        "Інструкційні картки із завданнями.",
        "Текстовий редактор для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    # ---------- Література ----------
    h2(doc, "Література")
    sources = [
        "Зайцев В. Г., Дробязко І. П. Операційні системи : навч. посіб. для "
        "студ. спец. 123 «Комп'ютерна інженерія». Київ : КПІ ім. Ігоря "
        "Сікорського, 2019.",
        "Іванов О. В., Петрова Н. М. Основи операційних систем : навч. "
        "посіб. Київ : Основи, 2020.",
        "Микитишин А. Г., Чихіра І. В. Операційні системи : консп. лекц. "
        "Тернопіль : ТНТУ імені Івана Пулюя, 2016.",
    ]
    for s in sources:
        numbered(doc, s)

    # ---------- Завдання ----------
    h2(doc, "Завдання самостійної роботи")
    tasks = [
        "Опрацювати теоретичний матеріал за переліком опрацьовуваних питань.",
        "Заповнити таблицю команд: синтаксис, призначення, приклад "
        "використання (10 команд).",
        "Скласти шпаргалку з 5 правил безпечної роботи в командному рядку.",
        "Виконати практичне завдання за інструкційною карткою: побудувати "
        "структуру папок, наповнити її файлами, виконати операції "
        "копіювання, перейменування та видалення.",
        "Дати письмові відповіді на теоретичні питання.",
        "Оформити звіт згідно з рекомендаціями та надіслати викладачу "
        "у визначений термін.",
    ]
    for t in tasks:
        numbered(doc, t)

    # ---------- Терміни ----------
    h2(doc, "Терміни виконання")
    body(doc, "Робота виконується протягом одного тижня після отримання "
              "завдання; готовий звіт подається на наступному практичному "
              "занятті або завантажується в електронний курс дисципліни "
              "до вказаної дати.")

    # ---------- Очікувані результати ----------
    h2(doc, "Очікувані результати")
    results = [
        "знає синтаксис і призначення основних команд роботи з файлами "
        "та каталогами (dir, cd, mkdir, rmdir, copy, del, ren, tree);",
        "розуміє різницю між абсолютним і відносним шляхами у командному "
        "рядку;",
        "вміє самостійно створювати багаторівневу структуру папок без "
        "використання графічного інтерфейсу;",
        "правильно застосовує параметри команд (/S, /F, /Q) залежно від "
        "завдання;",
        "дотримується правил безпеки під час роботи з командами del і "
        "rmdir;",
        "пояснює типові помилки початківців і способи їх уникнення.",
    ]
    for r in results:
        bullet(doc, r)

    # ---------- Опрацьовувані питання ----------
    h2(doc, "Перелік опрацьовуваних питань")
    topics = [
        "Поняття командного рядка та його роль в операційній системі.",
        "Синтаксис команди: назва, об'єкт, параметр.",
        "Абсолютні та відносні шляхи у командному рядку.",
        "Спеціальні позначення: «..», «.», «\\».",
        "Команди перегляду вмісту каталогу (dir, tree).",
        "Команди навігації (cd) з різними формами аргументів.",
        "Команди створення та видалення каталогів (mkdir, rmdir).",
        "Команди роботи з файлами (copy, move, del, ren, type).",
        "Параметри команд /S, /F, /Q та їх призначення.",
        "Типові помилки під час роботи з командним рядком і способи їх "
        "уникнення.",
    ]
    for tp in topics:
        numbered(doc, tp)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості (стислий огляд)")

    h3(doc, "1. Командний рядок і його роль")
    body(doc, "Командний рядок — це текстовий інтерфейс операційної "
              "системи, у якому всі дії виконуються через введення команд "
              "з клавіатури. Користувач не бачить вікон, кнопок чи меню; "
              "система реагує на кожну команду текстовим виводом. У "
              "Windows командний рядок запускається програмою cmd.exe, "
              "у Linux — терміналом оболонки (bash, zsh).")

    body(doc, "Командний рядок дає змогу виконувати ті самі операції, що "
              "й графічний інтерфейс, але точніше, швидше та з можливістю "
              "автоматизації. Саме тому вміння працювати в командному "
              "рядку — базова навичка фахівця з ІТ.")

    h3(doc, "2. Класифікація команд")
    body(doc, "Усі команди командного рядка можна умовно поділити на "
              "чотири групи: навігація, керування каталогами, робота з "
              "файлами та службові команди. Кожна група має своє "
              "призначення, і разом вони утворюють повний набір "
              "інструментів для роботи з файловою системою.")

    add_figure(doc, img1, 16.0)

    h3(doc, "3. Будова команди")
    body(doc, "Кожна команда має три складові: назву (що зробити), "
              "об'єкт (з чим працювати) та параметр (як саме). Не всі "
              "складові є обов'язковими: об'єкт може бути пропущений "
              "(тоді діє поточна папка), а параметр — не потрібен для "
              "базових дій.")

    add_figure(doc, img2, 15.5)

    body(doc, "Приклади запису команд:")
    code_line(doc, "dir")
    body(doc, "переглянути вміст поточної папки.", space_after=2)
    code_line(doc, "dir D:\\Навчання")
    body(doc, "переглянути вміст конкретної папки за абсолютним шляхом.",
         space_after=2)
    code_line(doc, "mkdir Нова_папка")
    body(doc, "створити папку з назвою «Нова_папка» у поточному каталозі.",
         space_after=2)
    code_line(doc, "tree /F")
    body(doc, "вивести дерево каталогів разом із файлами.")

    h3(doc, "4. Особливості навігації")
    body(doc, "Команда cd розуміє як абсолютні, так і відносні шляхи. "
              "Символи «..» позначають батьківську папку, «\\» — корінь "
              "диска, «.» — поточну папку. Кілька «..» поспіль дозволяють "
              "піднятися на кілька рівнів угору.")

    bullet(doc, "cd — показати поточну папку (без аргументів);")
    bullet(doc, "cd Documents — перейти в підпапку Documents;")
    bullet(doc, "cd .. — перейти до батьківської папки;")
    bullet(doc, "cd ..\\.. — піднятися на два рівні вгору;")
    bullet(doc, "cd \\ — перейти до кореня диска;")
    bullet(doc, "cd /d D:\\Навчання — перейти на інший диск із "
                "зміною поточного каталогу.")

    callout(doc,
            "Команда cd без параметра /d не змінює поточний диск. Щоб "
            "перейти на інший диск разом зі зміною папки, використовуйте "
            "cd /d D:\\Шлях або спочатку введіть D: для зміни диска.",
            fill="E1F0FE", accent="0071E3")

    h3(doc, "5. Параметри команд")
    body(doc, "Параметри розширюють можливості базової команди. Вони "
              "завжди починаються з символу «/» у Windows і з «-» або «--» "
              "у Linux. Найуживаніші параметри:")
    bullet(doc, "/S — обробляти всі вкладені папки та файли;")
    bullet(doc, "/F — показувати файли разом із папками (для tree);")
    bullet(doc, "/Q — виконувати без підтвердження (для rmdir);")
    bullet(doc, "/A — показувати файли із заданими атрибутами (для dir).")

    h3(doc, "6. Безпека під час роботи з командним рядком")
    body(doc, "Командний рядок не має графічного підтвердження дій: "
              "виконана команда спрацьовує відразу. Тому варто "
              "дотримуватися п'яти правил:")
    safety = [
        "Перед командами del і rmdir перевірте поточну папку командою cd.",
        "Не використовуйте символи-джокери (del *.*) без попереднього "
        "перегляду вмісту (dir).",
        "Для видалення непорожніх папок застосовуйте rmdir /S (з "
        "підтвердженням) або rmdir /S /Q (без підтвердження).",
        "Використовуйте help <команда> або <команда> /? для перегляду "
        "довідки перед незнайомою командою.",
        "Не перейменовуйте та не переміщуйте системні папки Windows.",
    ]
    for s in safety:
        bullet(doc, s)

    callout(doc,
            "Якщо команду введено помилково — наслідки усуваються лише "
            "вручну або з резервної копії. У командному рядку немає "
            "звичного «Скасувати».",
            fill="FFEBEA", accent="C4001D")

    h3(doc, "7. Типові помилки початківців")
    body(doc, "Початківці найчастіше припускаються чотирьох помилок. "
              "Їх варто знати заздалегідь, щоб уникнути втрати даних або "
              "зайвих витрат часу.")

    add_figure(doc, img4, 16.0)

    # =====================================================
    # ЕТАПИ ВИКОНАННЯ
    # =====================================================
    h2(doc, "Етапи виконання самостійної роботи")
    body(doc, "Робота виконується послідовно за шість етапів. Кожен "
              "етап завершується певним результатом, який стане "
              "частиною звіту.")

    add_figure(doc, img3, 15.5)

    # =====================================================
    # ІНСТРУКЦІЙНА КАРТКА
    # =====================================================
    h2(doc, "Інструкційна картка практичного завдання")
    body(doc, "Виконайте всі кроки послідовно в командному рядку. "
              "Записуйте кожну команду та її результат у звіт. "
              "Для скріншотів достатньо трьох знімків: після кроку 20, "
              "після кроку 24 і після кроку 27.")

    steps = [
        ["1", "Відкрити командний рядок", "Win + R → cmd → Enter"],
        ["2", "Перейти на робочий диск", "D:  (або C:)"],
        ["3", "Створити робочу папку", "mkdir СР_Командний_ПІБ"],
        ["4", "Перейти до неї", "cd СР_Командний_ПІБ"],
        ["5", "Створити папку «Навчання»", "mkdir Навчання"],
        ["6", "Перейти до неї", "cd Навчання"],
        ["7", "Створити «1_Клас» і «2_Клас»", "mkdir 1_Клас && mkdir 2_Клас"],
        ["8", "Перейти в «1_Клас»", "cd 1_Клас"],
        ["9", "Створити «Уроки» і «Матеріали»", "mkdir Уроки && mkdir Матеріали"],
        ["10", "Перейти в «Уроки»", "cd Уроки"],
        ["11", "Створити файл із текстом",
         "echo План уроку для 1 класу > урок_1.txt"],
        ["12", "Перевірити вміст файлу", "type урок_1.txt"],
        ["13", "Піднятися на два рівні вгору", "cd ..\\.."],
        ["14", "Перейти в «2_Клас»", "cd 2_Клас"],
        ["15", "Створити «Уроки»", "mkdir Уроки"],
        ["16", "Перейти та створити файл",
         "cd Уроки && echo План уроку для 2 класу > урок_2.txt"],
        ["17", "Повернутися в «Навчання»", "cd ..\\.."],
        ["18", "Створити папку «Архів»", "mkdir Архів"],
        ["19", "Скопіювати файл в «Архів»",
         "copy 1_Клас\\Уроки\\урок_1.txt Архів"],
        ["20", "Вивести дерево каталогів", "tree /F"],
        ["21", "Перейти в «Архів»", "cd Архів"],
        ["22", "Перейменувати файл", "ren урок_1.txt старий_урок.txt"],
        ["23", "Повернутися в «Навчання»", "cd .."],
        ["24", "Перевірити вміст папки «Архів»", "dir Архів"],
        ["25", "Видалити «2_Клас» із файлами",
         "rmdir /S /Q 2_Клас"],
        ["26", "Перевірити дерево каталогів", "tree /F"],
        ["27", "Перевірити вміст кореневої папки", "dir"],
    ]

    add_table(
        doc,
        ["№", "Дія", "Команда"],
        steps,
        widths=[0.9, 6.5, 9.1],
        mono_cols=[2],
    )

    callout(doc,
            "У кінцевій структурі має залишитися: папка «Навчання» з "
            "папками «1_Клас» (містить «Уроки» і «Матеріали») та «Архів» "
            "(містить файл «старий_урок.txt»). Папка «2_Клас» має бути "
            "відсутня.",
            fill="E8F8EC", accent="248A3D")

    # ---------- Завдання на таблицю ----------
    h2(doc, "Завдання на заповнення таблиці команд")
    body(doc, "Заповніть таблицю, указавши для кожної команди її "
              "синтаксис, призначення та приклад використання. "
              "Приклади мають бути конкретними, а не загальними.")

    add_table(
        doc,
        ["Команда", "Синтаксис", "Призначення", "Приклад"],
        [
            ["dir", "", "", ""],
            ["cd", "", "", ""],
            ["mkdir / md", "", "", ""],
            ["rmdir / rd", "", "", ""],
            ["copy", "", "", ""],
            ["move", "", "", ""],
            ["del", "", "", ""],
            ["ren", "", "", ""],
            ["type", "", "", ""],
            ["tree", "", "", ""],
        ],
        widths=[3.0, 3.6, 5.0, 4.9],
        mono_cols=[0],
    )

    # ---------- Шпаргалка ----------
    h2(doc, "Завдання на складання шпаргалки")
    body(doc, "Складіть шпаргалку з 5 правил безпечної роботи в "
              "командному рядку. Кожне правило сформулюйте одним реченням "
              "і наведіть приклад команди, якої воно стосується. "
              "Оформіть у вигляді нумерованого списку.")

    # =====================================================
    # ТЕОРЕТИЧНІ ПИТАННЯ
    # =====================================================
    h2(doc, "Теоретичні питання для самоперевірки")
    questions = [
        "Що таке командний рядок і чим він відрізняється від графічного "
        "інтерфейсу?",
        "З яких трьох складових може складатися команда командного рядка? "
        "Наведіть приклад із усіма трьома складовими.",
        "Чим абсолютний шлях відрізняється від відносного? Наведіть по "
        "одному прикладу.",
        "Що означають символи «..», «.» і «\\» у командному рядку?",
        "Яка різниця між командами cd і cd /d? У яких випадках "
        "використовується кожна з них?",
        "Для чого призначений параметр /S у команді rmdir? Що станеться, "
        "якщо його не вказати для непорожньої папки?",
        "Як переглянути довідку про незнайому команду?",
        "Чому команда del *.* вважається небезпечною? Як убезпечити "
        "себе від випадкового видалення?",
        "Що станеться в результаті виконання команди "
        "mkdir Моя папка? Поясніть.",
        "Опишіть послідовність команд для створення структури: папка "
        "«Звіти» з підпапками «2023», «2024» та файлом «підсумок.txt» "
        "у папці «2024».",
    ]
    for q in questions:
        numbered(doc, q)

    # =====================================================
    # РЕКОМЕНДАЦІЇ ДО ОФОРМЛЕННЯ
    # =====================================================
    h2(doc, "Рекомендації до оформлення звіту")
    body(doc, "Звіт оформлюється у текстовому редакторі (MS Word / "
              "LibreOffice Writer) і повинен містити такі обов'язкові "
              "структурні елементи:")
    structure = [
        "Титульна сторінка: назва навчального закладу, тема, ПІБ "
        "студента, група, ПІБ викладача, рік.",
        "Мета та завдання роботи.",
        "Заповнена таблиця команд (синтаксис, призначення, приклад).",
        "Шпаргалка з 5 правил безпеки.",
        "Практична частина: послідовність виконаних команд із "
        "коментарями та трьома скріншотами (після кроків 20, 24, 27).",
        "Відповіді на теоретичні питання (письмово, стисло).",
        "Висновок: що нового засвоїли, які команди виконували впевнено, "
        "а які потребують додаткового тренування.",
        "Список використаних джерел (оформлений за ДСТУ 8302:2015).",
    ]
    for s in structure:
        numbered(doc, s)

    body(doc, "Технічні параметри оформлення: шрифт Times New Roman, "
              "14 pt, міжрядковий інтервал 1,15, поля 2 см, абзацний "
              "відступ 1,25 см, вирівнювання за шириною. Команди в "
              "тексті оформлюйте моноширинним шрифтом (Consolas) або "
              "виділяйте напівжирним. Обсяг звіту — 4–6 сторінок без "
              "урахування титульної сторінки та додатків. Ім'я файлу: "
              "«СР_Командний_рядок_ПІБ.docx».")

    # =====================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =====================================================
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Критерій", "Бали"],
        [
            ["Повнота й правильність заповнення таблиці команд", "3"],
            ["Якість шпаргалки з правил безпеки", "1"],
            ["Виконання практичного завдання за інструкційною карткою",
             "4"],
            ["Відповіді на теоретичні питання", "3"],
            ["Оформлення звіту згідно з рекомендаціями", "1"],
            ["Творчий підхід, власні приклади команд", "1"],
        ],
        widths=[12.5, 4.0],
    )

    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (потребує доопрацювання).")

    doc.save("Самостійна_робота_Командний_рядок.docx")
    print("Готово: Самостійна_робота_Командний_рядок.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()