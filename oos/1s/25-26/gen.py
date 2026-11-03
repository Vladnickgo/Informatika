# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Основи автоматизації завдань в командному рядку
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
TERM_KEYWORD = "#FF9500"
TERM_STRING = "#FF453A"


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
# СХЕМА 1. Основні команди пакетних файлів
# ============================================================

def scheme_commands():
    fig, ax = plt.subplots(figsize=(11, 7.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.0)
    ax.axis("off")

    ax.text(6.5, 8.55, "Основні команди пакетних файлів",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    commands = [
        ("@echo off", "Вимикає показ команд\nна екрані під час виконання",
         ACCENT_BLUE, "#E1F0FE"),
        ("echo", "Виводить текст\nна екран або у файл",
         ACCENT_GREEN, "#E8F8EC"),
        ("set", "Створює змінну.\nset /p — запитує у користувача",
         ACCENT_ORANGE, "#FFF4E5"),
        ("if", "Перевіряє умову\nй виконує дію залежно від неї",
         ACCENT_PURPLE, "#EFE6F7"),
        ("goto", "Переходить до мітки\n(організація циклів)",
         ACCENT_RED, "#FFEBEA"),
        ("pause", "Зупиняє виконання,\nчекає натискання клавіші",
         ACCENT_BLUE, "#E1F0FE"),
    ]

    card_w, card_h = 3.9, 2.7
    gap_x, gap_y = 0.25, 0.3
    x0 = 0.4
    y_top = 7.9

    for i, (cmd, desc, color, fill) in enumerate(commands):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.18)
        _badge(ax, cx, y + card_h - 0.55, 2.4, 0.55, color, cmd,
               color="white", size=13, radius=0.28)
        ax.text(cx, y + 0.9, desc, ha="center", va="center",
                fontsize=11.5, color=TEXT_DARK, linespacing=1.55)

    return _save(fig, "scheme_commands")


# ============================================================
# СХЕМА 2. Будова .bat файлу
# ============================================================

def scheme_bat_structure():
    fig, ax = plt.subplots(figsize=(11, 8.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    ax.text(6.5, 9.15, "Будова пакетного файлу .bat",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Темне вікно з кодом
    px, py, pw, ph = 0.4, 3.8, 12.2, 5.0
    ax.add_patch(FancyBboxPatch((px, py), pw, ph,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=TERM_BG, edgecolor="#3A3A3C",
                                linewidth=1.6))
    ax.add_patch(Rectangle((px, py + ph - 0.5), pw, 0.5,
                           facecolor=TERM_TITLE))
    ax.text(px + 0.3, py + ph - 0.25, "hello.bat",
            ha="left", va="center", fontsize=11, color="#A1A1A6",
            family="monospace")

    code_lines = [
        ("1", "@echo off",                            TERM_KEYWORD),
        ("2", "title Мій перший скрипт",              TERM_TEXT),
        ("3", "set /p name=Введіть ім'я: ",           TERM_TEXT),
        ("4", "echo Привіт, %name%!",                 TERM_TEXT),
        ("5", "echo Сьогодні %date%",                 TERM_TEXT),
        ("6", "mkdir Zvit_%name%",                    TERM_TEXT),
        ("7", "echo Файл створено >> Zvit_%name%\\info.txt", TERM_TEXT),
        ("8", "pause",                                TERM_KEYWORD),
        ("9", "exit",                                 TERM_KEYWORD),
    ]

    yy = py + ph - 0.95
    for num, line, color in code_lines:
        ax.text(px + 0.35, yy, num, ha="left", va="center",
                fontsize=10, color="#636366", family="monospace")
        ax.text(px + 0.85, yy, line, ha="left", va="center",
                fontsize=11.5, color=color, family="monospace")
        yy -= 0.42

    # Картки-пояснення під кодом
    notes = [
        ("@echo off", "вимикає показ команд", ACCENT_BLUE, "#E1F0FE"),
        ("set /p", "запитує дані у користувача", ACCENT_GREEN, "#E8F8EC"),
        ("%name%", "підставляє значення змінної", ACCENT_ORANGE, "#FFF4E5"),
        ("pause", "тримає вікно відкритим", ACCENT_RED, "#FFEBEA"),
    ]

    cw, ch = 2.95, 1.9
    gap = 0.12
    x0 = 0.4
    y0 = 1.3

    for i, (title, desc, color, fill) in enumerate(notes):
        x = x0 + i * (cw + gap)
        cx = x + cw / 2
        _card(ax, x, y0, cw, ch, fill=fill, border=color, radius=0.15)
        ax.text(cx, y0 + ch - 0.45, title, ha="center", va="center",
                fontsize=11.5, fontweight="bold", color=color,
                family="monospace")
        ax.text(cx, y0 + 0.7, desc, ha="center", va="center",
                fontsize=10.5, color=TEXT_DARK, linespacing=1.5)

    ax.text(6.5, 0.55, "Зберегти файл можна у Блокноті: ім'я — hello.bat, "
                       "тип — «Усі файли»",
            ha="center", va="center", fontsize=10.5, style="italic",
            color=TEXT_GRAY)

    return _save(fig, "scheme_bat_structure")


# ============================================================
# СХЕМА 3. Планувальник завдань
# ============================================================

def scheme_scheduler():
    fig, ax = plt.subplots(figsize=(11, 7.4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.5, 8.1, "Планувальник завдань: що налаштовуємо",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Верхній банер: три кроки запуску
    steps = [
        ("Крок 1", "Win + R", ACCENT_BLUE),
        ("Крок 2", "taskschd.msc", ACCENT_GREEN),
        ("Крок 3", "Створити завдання", ACCENT_ORANGE),
    ]
    step_w, step_h = 3.6, 1.0
    step_gap = 0.35
    total_w = 3 * step_w + 2 * step_gap
    sx0 = (13 - total_w) / 2
    sy = 6.5

    for i, (label, cmd, color) in enumerate(steps):
        x = sx0 + i * (step_w + step_gap)
        cx = x + step_w / 2
        _card(ax, x, sy, step_w, step_h, fill="#F5F5F7",
              border=color, radius=0.16)
        ax.text(cx, sy + step_h - 0.32, label, ha="center", va="center",
                fontsize=10.5, color=color, fontweight="bold")
        ax.text(cx, sy + 0.32, cmd, ha="center", va="center",
                fontsize=12, color=TEXT_DARK, fontweight="bold",
                family="monospace")
        if i < 2:
            ax.annotate("", xy=(x + step_w + 0.3, sy + step_h / 2),
                        xytext=(x + step_w + 0.05, sy + step_h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=TEXT_GRAY,
                                        linewidth=1.6, mutation_scale=12))

    # Нижче — 4 картки пояснення
    params = [
        ("ТРИГЕР", "КОЛИ запускати:\nодин раз, щодня,\nпри вході в систему",
         ACCENT_BLUE, "#E1F0FE"),
        ("ДІЯ", "ЩО запускати:\nсам .bat-файл або\ncmd.exe з аргументом /c",
         ACCENT_GREEN, "#E8F8EC"),
        ("УМОВИ", "ЗА ЯКИХ УМОВ:\nлише від мережі,\nрозбудити комп'ютер",
         ACCENT_ORANGE, "#FFF4E5"),
        ("ОБЛІКОВИЙ ЗАПИС", "ВІД ЧИЙОГО ІМЕНІ:\nвід вашого або\nсистемного",
         ACCENT_PURPLE, "#EFE6F7"),
    ]

    cw, ch = 3.0, 3.6
    gap_x, gap_y = 0.12, 0.2
    x0 = (13 - (4 * cw + 3 * gap_x)) / 2
    y0 = 1.2

    for i, (title, desc, color, fill) in enumerate(params):
        x = x0 + i * (cw + gap_x)
        cx = x + cw / 2
        _card(ax, x, y0, cw, ch, fill=fill, border=color, radius=0.15)
        _badge(ax, cx, y0 + ch - 0.5, 2.6, 0.55, color, title,
               color="white", size=11, radius=0.28)
        ax.text(cx, y0 + 1.35, desc, ha="center", va="center",
                fontsize=10.5, color=TEXT_DARK, linespacing=1.7)

    return _save(fig, "scheme_scheduler")


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
        ("Рівень 1", "Простий скрипт",
         "echo, pause,\n@echo off —\nвиведення тексту",
         "≈ 7 хв", ACCENT_GREEN, "#E8F8EC"),
        ("Рівень 2", "Скрипт зі\nзмінними",
         "set /p, if, goto,\nстворення папок\nі файлів",
         "≈ 10 хв", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Автоматизація\nза розкладом",
         ".bat + Планувальник\nзавдань — запуск\nбез участі людини",
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
    img2 = scheme_bat_structure()
    img3 = scheme_scheduler()
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
    theme_line(doc, "Основи автоматизації завдань в командному рядку. "
                    "Створення простих скриптів та пакетних файлів для "
                    "автоматизації завдань. Використання планувальника "
                    "завдань для автоматичного виконання команд")

    h2(doc, "Мета")
    body(doc, "формувати навички створення пакетних файлів (.bat) та "
              "налаштування планувальника завдань Windows; розвивати "
              "здатність до алгоритмізації повторюваних дій та "
              "оптимізації робочих процесів; виховувати раціональне "
              "ставлення до часу та трудових ресурсів через "
              "автоматизацію рутинних операцій.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Командний рядок cmd або Windows Terminal.",
        "Програма «Блокнот» для створення .bat-файлів.",
        "Планувальник завдань (taskschd.msc).",
        "Інструкційні картки до рівнів 1–3.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Сільвестр В., Гансен П. Основи операційних систем. Київ : "
        "Нова Книга, 2016.",
        "Таненбаум Е., Бос Г. Операційні системи: проектування та "
        "реалізація. Київ : Вильямс, 2015.",
        "Томпсон Д., Черніченко В. Операційні системи. Київ : Кондор, "
        "2017.",
    ]
    for s in sources:
        numbered(doc, s)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Що таке автоматизація та пакетні файли")
    body(doc, "Автоматизація — це заміна ручної праці роботою програми. "
              "У командному рядку Windows інструментом автоматизації є "
              "пакетні файли — текстові файли з розширенням .bat або "
              ".cmd, у яких записано послідовність команд. Коли такий "
              "файл запускається, командна оболонка (cmd.exe) виконує "
              "всі рядки один за одним так, ніби ви вводите їх вручну.")

    body(doc, "Пакетні файли дозволяють:")
    bullet(doc, "виконувати багато команд однією дією;")
    bullet(doc, "використовувати змінні та умовні переходи;")
    bullet(doc, "запускати скрипти за розкладом через планувальник "
                "завдань;")
    bullet(doc, "створювати резервні копії, очищати тимчасові файли, "
                "запускати послідовність програм.")

    h3(doc, "2. Основні команди пакетних файлів")
    body(doc, "Пакетні файли використовують ті самі команди, що й "
              "командний рядок, плюс кілька спеціальних — для керування "
              "виконанням, змінних і виводу.")

    add_figure(doc, img1, 16.0)

    add_table(
        doc,
        ["Команда", "Призначення", "Приклад"],
        [
            ["@echo off", "Вимикає показ команд у вікні",
             "@echo off"],
            ["echo", "Виводить текст або створює файл",
             "echo Привіт"],
            ["set", "Створює або змінює змінну",
             "set name=Іван"],
            ["set /p", "Запитує значення у користувача",
             "set /p name=Ім'я: "],
            ["if", "Перевіряє умову",
             "if exist файл.txt echo Є!"],
            ["goto", "Переходить до мітки :label",
             "goto end"],
            ["pause", "Зупиняє виконання до натискання клавіші",
             "pause"],
            ["exit", "Завершує роботу скрипта", "exit"],
            [":: або rem", "Коментар (не виконується)",
             ":: це коментар"],
        ],
        widths=[2.6, 7.2, 6.7],
        mono_cols=[0, 2],
    )

    h3(doc, "3. Будова пакетного файлу")
    body(doc, "Мінімальний пакетний файл містить кілька рядків: "
              "вимкнення показу команд, безпосередньо команди та "
              "завершення. Розгляньмо типовий приклад — скрипт, який "
              "запитує ім'я користувача і створює для нього папку.")

    add_figure(doc, img2, 16.0)

    body(doc, "Ключові особливості синтаксису:")
    bullet(doc, "@echo off — на самому початку, щоб команди не "
                "дублювалися на екрані;")
    bullet(doc, "змінні записуються без пробілів навколо «=»: "
                "set name=Іван (не set name = Іван);")
    bullet(doc, "значення змінної підставляється через %ім'я% — "
                "наприклад, %name%;")
    bullet(doc, "коментарі починаються з :: або rem;")
    bullet(doc, "pause у кінці дозволяє побачити результат перед "
                "закриттям вікна.")

    callout(doc,
            "Файл потрібно зберігати з розширенням .bat або .cmd. "
            "У Блокноті виберіть «Файл → Зберегти як», тип файлу — "
            "«Усі файли», ім'я — hello.bat (саме з крапкою). Якщо "
            "зберегти як hello.bat.txt, скрипт не запуститься: "
            "розширення .txt перетворить його на звичайний текст.",
            fill="FFF4E5", accent="C93400")

    h3(doc, "4. Планувальник завдань Windows")
    body(doc, "Планувальник завдань (Task Scheduler) — це системна "
              "програма Windows, яка запускає програми або скрипти за "
              "розкладом чи за певних подій. Він не потребує, щоб "
              "користувач сидів за комп'ютером: завдання виконується "
              "автоматично у визначений момент.")

    add_figure(doc, img3, 16.0)

    body(doc, "Під час створення завдання налаштовують чотири речі:")
    numbered(doc, "Тригер — коли запускати (один раз, щодня, при "
                  "вході в систему, за подією).")
    numbered(doc, "Дія — що запускати (програму, .bat-файл, "
                  "PowerShell-скрипт).")
    numbered(doc, "Умови — за яких умов (лише від мережі, розбудити "
                  "комп'ютер, запускати лише при простої).")
    numbered(doc, "Обліковий запис — від чийого імені виконувати "
                  "(ваш або системний, з правами адміністратора чи без).")

    body(doc, "Типова послідовність запуску:")
    code_line(doc, "Win + R  →  taskschd.msc  →  Enter")
    body(doc, "відкривається вікно Планувальника. Далі — «Створити "
              "завдання» (Create Task), заповнюємо вкладки «Загальні», "
              "«Тригери», «Дії», «Умови» та зберігаємо.")

    callout(doc,
            "У полі «Програма або сценарій» для .bat-файлу краще "
            "вказувати cmd.exe, а в полі «Додаткові аргументи» — "
            "/c \"C:\\Scripts\\hello.bat\". Це надійніше, ніж вказувати "
            "сам .bat-файл: Windows гарантовано запустить його через "
            "командну оболонку, навіть якщо асоціація .bat пошкоджена.",
            fill="E1F0FE", accent="0071E3")

    h3(doc, "5. Безпека під час запуску скриптів")
    body(doc, "Пакетний файл — це програма, яка має ті самі права, що "
              "й користувач, який її запускає. Тому скрипт із чужого "
              "джерела може бути небезпечним: видалити файли, "
              "завантажити шкідливу програму, змінити налаштування "
              "системи. Дотримуйтеся таких правил:")
    bullet(doc, "не запускайте .bat-файли, отримані від невідомих осіб;")
    bullet(doc, "перед запуском відкрийте файл у Блокноті й прочитайте, "
                "що він робить;")
    bullet(doc, "тестуйте нові скрипти у безпечній папці, а не в "
                "корені системного диска;")
    bullet(doc, "не запускайте скрипти від імені адміністратора без "
                "нагальної потреби;")
    bullet(doc, "завдання у планувальнику перевіряйте одразу після "
                "створення (правий клік → «Виконати»).")

    callout(doc,
            "Завдання в планувальнику можуть запускатися непомітно для "
            "користувача. Тому після створення завдання обов'язково "
            "перевірте вкладку «Історія» (History) — там видно, чи "
            "запускалося завдання, з яким результатом і коли. "
            "Якщо щось пішло не так — завдання можна видалити одним "
            "кліком.",
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
    h3(doc, "Рівень 1 — простий скрипт (≈ 7 хв)",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Мета: навчитися створювати пакетний файл, який виводить "
              "текст на екран і коректно завершується.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Відкрийте «Блокнот»",
             "Win + R → notepad → Enter"],
            ["2", "Створіть папку для скриптів",
             "mkdir D:\\Scripts   (у cmd)"],
            ["3", "Введіть у Блокноті перший рядок",
             "@echo off"],
            ["4", "Додайте заголовок вікна",
             "title Мій перший скрипт"],
            ["5", "Додайте вивід тексту",
             "echo Привіт, командний рядок!"],
            ["6", "Додайте вивід дати",
             "echo Сьогодні: %date%"],
            ["7", "Додайте паузу", "pause"],
            ["8", "Збережіть файл",
             "Файл → Зберегти як → тип «Усі файли» → "
             "D:\\Scripts\\hello.bat"],
            ["9", "Запустіть скрипт",
             "Двічі клацніть hello.bat  →  вікно cmd показує ваш текст"],
            ["10", "Перевірте, що скрипт можна запустити з cmd",
             "cd /d D:\\Scripts  →  hello.bat"],
            ["11", "Зробіть скріншот",
             "Знімок вікна cmd із результатом скрипта"],
        ],
        widths=[1.0, 5.8, 9.7],
        mono_cols=[2],
    )

    callout(doc,
            "Після запуску вікно має показати два рядки тексту й "
            "запропонувати «Для продовження натисніть будь-яку "
            "клавішу...». Якщо вікно відкрилося й одразу закрилося — "
            "ви забули pause. Якщо файл відкривається в Блокноті — "
            "перевірте розширення: воно має бути .bat, а не .bat.txt.",
            fill="E8F8EC", accent="248A3D")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — скрипт зі змінними (≈ 10 хв)",
       color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Мета: навчитися використовувати змінні, введення "
              "користувача, умовні переходи та створення папок у "
              "скрипті.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Створіть новий файл",
             "notepad D:\\Scripts\\folder.bat"],
            ["2", "Заголовок і вимкнення показу команд",
             "@echo off\ntitle Створення папки"],
            ["3", "Запитайте ім'я папки",
             "set /p name=Введіть назву папки: "],
            ["4", "Перевірте, чи ім'я не порожнє",
             "if \"%name%\"==\"\" goto empty"],
            ["5", "Створіть папку та файл у ній",
             "mkdir \"%name%\"\n"
             "echo Створено %date% >> \"%name%\\info.txt\""],
            ["6", "Виведіть повідомлення та перейдіть у кінець",
             "echo Папку «%name%» створено.\ngoto end"],
            ["7", "Додайте мітку для помилки",
             ":empty\necho Ви не ввели назву!"],
            ["8", "Додайте мітку завершення",
             ":end\npause\nexit"],
            ["9", "Запустіть скрипт двічі",
             "folder.bat → введіть назву\n"
             "folder.bat → натисніть Enter без назви"],
            ["10", "Перевірте результат",
             "dir  →  нова папка з info.txt"],
            ["11", "Зробіть скріншот",
             "Знімок обох запусків: успіху та помилки"],
        ],
        widths=[1.0, 5.5, 10.0],
        mono_cols=[2],
    )

    callout(doc,
            "У звіті має бути: код скрипта folder.bat повністю, "
            "скріншоти двох запусків (з ім'ям і без імені) та коротке "
            "пояснення, для чого в скрипті використовується goto end і "
            "goto empty. Порівняйте, що сталося б, якби goto у скрипті "
            "не було.",
            fill="FFF4E5", accent="C93400")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — автоматизація за розкладом (≈ 10 хв)",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Мета: створити скрипт, який робить резервну копію "
              "папки, і налаштувати його автоматичний запуск через "
              "Планувальник завдань Windows.")

    body(doc, "Завдання А. Створіть скрипт backup.bat:")
    code_line(doc, "@echo off")
    code_line(doc, "title Резервне копіювання")
    code_line(doc, "set src=D:\\Zvit")
    code_line(doc, "set dst=D:\\Backup\\Zvit_%date:~-4%-%date:~3,2%")
    code_line(doc, "if not exist \"%dst%\" mkdir \"%dst%\"")
    code_line(doc, "xcopy \"%src%\" \"%dst%\" /S /E /Y")
    code_line(doc, "echo Копіювання завершено %date% %time% >> "
                   "\"%dst%\\backup_log.txt\"")
    code_line(doc, "exit")

    body(doc, "Завдання Б. Перевірте скрипт вручну:")
    tasks_b = [
        "Створіть папку «D:\\Zvit» і покладіть у неї 2–3 довільні "
        "текстові файли.",
        "Запустіть backup.bat подвійним клацанням.",
        "Переконайтеся, що у «D:\\Backup» з'явилася папка "
        "«Zvit_<рік>-<місяць>» з копією файлів.",
        "Перевірте, що у цій папці є файл «backup_log.txt» із датою "
        "та часом.",
    ]
    for t in tasks_b:
        numbered(doc, t)

    body(doc, "Завдання В. Налаштуйте автоматичний запуск:")
    code_line(doc, "Win + R  →  taskschd.msc  →  Enter")
    tasks_v = [
        "У Планувальнику завдань виберіть «Створити завдання».",
        "На вкладці «Загальні» введіть ім'я «Резервна копія Zvit», "
        "поставте позначку «Виконувати з найвищими правами».",
        "На вкладці «Тригери» натисніть «Створити», виберіть "
        "«Щодня», час — довільний (наприклад, 15:00).",
        "На вкладці «Дії» натисніть «Створити»:",
        "У полі «Програма або сценарій» введіть: cmd.exe",
        "У полі «Додати аргументи» введіть: /c \"D:\\Scripts\\backup.bat\"",
        "Натисніть «ОК» і збережіть завдання.",
        "Знайдіть завдання в бібліотеці, правий клік → «Виконати» — "
        "перевірте, що воно запускається негайно.",
        "Перегляньте вкладку «Історія» — там має бути запис про "
        "успішний запуск.",
        "Зробіть скріншоти: вікно завдання (вкладка «Дії») і вкладка "
        "«Історія».",
    ]
    for t in tasks_v:
        numbered(doc, t)

    body(doc, "Завдання Г. У звіті наведіть:")
    numbered(doc, "повний код backup.bat;")
    numbered(doc, "скріншоти вікна завдання і вкладки «Історія»;")
    numbered(doc, "пояснення, що роблять конструкції "
                  "%date:~-4% та %date:~3,2% у скрипті;")
    numbered(doc, "пояснення, чому у полі «Програма» вказано cmd.exe, "
                  "а не сам .bat-файл;")
    numbered(doc, "висновок (3–4 речення) про те, які рутинні дії "
                  "можна автоматизувати у вашій навчальній або "
                  "майбутній роботі.")

    callout(doc,
            "За бажанням (+1 бал). Додайте у скрипт перевірку: якщо "
            "папки «D:\\Zvit» не існує — вивести повідомлення про "
            "помилку і не виконувати копіювання. Скористайтеся "
            "конструкцією if not exist. Поясніть, чому така перевірка "
            "робить скрипт надійнішим.",
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
             "Скрипт hello.bat створено й успішно запущено; є "
             "скріншот; вікно не закривається одразу", "3"],
            ["Рівень 2",
             "Скрипт folder.bat містить set /p, if, goto; обидва "
             "сценарії (з ім'ям і без) працюють коректно; є "
             "скріншоти", "4"],
            ["Рівень 3",
             "backup.bat виконує копіювання; завдання у "
             "Планувальнику створено й успішно виконано вручну; "
             "є скріншоти вікна та історії", "4"],
            ["Якість звіту",
             "Оформлення за вимогами; наведено код усіх скриптів; "
             "підписи до скріншотів", "1"],
            ["Творчий підхід",
             "Виконано ускладнення (перевірка наявності папки) або "
             "запропоновано власну ідею автоматизації", "1"],
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
        "Код скрипта hello.bat + скріншот вікна з результатом "
        "(рівень 1).",
        "Код скрипта folder.bat + скріншоти двох запусків (рівень 2).",
        "Код скрипта backup.bat + скріншоти вікна завдання і вкладки "
        "«Історія» (рівень 3).",
        "Пояснення конструкцій %date:~-4% і %date:~3,2%, а також "
        "причини використання cmd.exe у полі «Програма».",
        "Висновок: що нового засвоїли, які рутинні дії плануєте "
        "автоматизувати у своїй роботі.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, "
              "шрифт Times New Roman 14 pt, інтервал 1,15, поля 2 см, "
              "обсяг — 3–5 сторінок без титульної. Код скриптів — "
              "моноширинним шрифтом (Consolas). Ім'я файлу: "
              "«Практика_Автоматизація_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    doc.save("Практичне_заняття_Автоматизація.docx")
    print("Готово: Практичне_заняття_Автоматизація.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()