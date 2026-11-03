# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Віконний, графічний інтерфейс. Робота з вікнами
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
# СХЕМА 1. Структура вікна Windows
# ============================================================

def scheme_window_structure():
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.5, 8.1, "Структура вікна Windows",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Вікно
    wx, wy, ww, wh = 1.2, 1.0, 10.6, 6.5
    ax.add_patch(FancyBboxPatch((wx, wy), ww, wh,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="white", edgecolor="#404040",
                                linewidth=1.8))

    # Заголовок
    ax.add_patch(Rectangle((wx, wy + wh - 0.65), ww, 0.65,
                           facecolor="#1F4E79"))
    ax.text(wx + 0.4, wy + wh - 0.32, "📄 Безіменний — Блокнот",
            ha="left", va="center", fontsize=11, fontweight="bold",
            color="white")

    # Кнопки керування
    for i, symbol in enumerate(["—", "☐", "✕"]):
        bx = wx + ww - 0.5 - i * 0.65
        color = "#E81123" if symbol == "✕" else "#FFFFFF"
        ax.text(bx, wy + wh - 0.32, symbol, ha="center", va="center",
                fontsize=13, color=color, fontweight="bold")

    # Рядок меню
    ax.add_patch(Rectangle((wx, wy + wh - 1.05), ww, 0.4,
                           facecolor="#F5F5F7"))
    menu_items = ["Файл", "Редагування", "Вигляд", "Довідка"]
    for i, item in enumerate(menu_items):
        ax.text(wx + 0.4 + i * 1.5, wy + wh - 0.85, item,
                ha="left", va="center", fontsize=10.5,
                color=TEXT_DARK, fontweight="bold")

    # Робоча область
    ax.add_patch(Rectangle((wx + 0.15, wy + 0.15),
                           ww - 0.55, wh - 1.35,
                           facecolor="#FFFFFF", edgecolor="#BFBFBF",
                           linewidth=0.8))
    ax.text(wx + 0.5, wy + wh - 1.6, "Робоча область",
            ha="left", va="center", fontsize=10, style="italic",
            color=TEXT_GRAY)
    ax.text(wx + 0.5, wy + wh - 2.1, "Тут відображається вміст документа,",
            ha="left", va="center", fontsize=10, color=TEXT_DARK)
    ax.text(wx + 0.5, wy + wh - 2.5, "зображення або панелі програми.",
            ha="left", va="center", fontsize=10, color=TEXT_DARK)

    # Смуги прокрутки
    ax.add_patch(Rectangle((wx + ww - 0.4, wy + 0.15), 0.25, wh - 1.35,
                           facecolor="#E5E5EA", edgecolor="#BFBFBF",
                           linewidth=0.6))
    ax.add_patch(Rectangle((wx + 0.15, wy + 0.15), ww - 0.55, 0.25,
                           facecolor="#E5E5EA", edgecolor="#BFBFBF",
                           linewidth=0.6))

    # Виноски-стрілки
    notes = [
        (wx + 3.5, wy + wh - 0.32, "Заголовок вікна", 0.5, 7.9),
        (wx + ww - 0.5, wy + wh - 0.32, "Кнопки керування", 11.5, 7.9),
        (wx + 2.0, wy + wh - 0.85, "Рядок меню", 0.5, 1.2),
        (wx + ww - 0.3, wy + 3.0, "Смуга прокрутки", 12.3, 4.0),
    ]
    for x, y, label, tx, ty in notes:
        ax.annotate(label, xy=(x, y), xytext=(tx, ty),
                    ha="center", va="center", fontsize=10.5,
                    fontweight="bold", color=ACCENT_ORANGE,
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT_ORANGE,
                                    linewidth=1.5))

    return _save(fig, "scheme_window_structure")


# ============================================================
# СХЕМА 2. Елементи робочого столу та панелі задач
# ============================================================

def scheme_desktop():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.35, "Робочий стіл і панель задач",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Робочий стіл
    dx, dy, dw, dh = 0.4, 1.4, 12.2, 5.5
    ax.add_patch(FancyBboxPatch((dx, dy), dw, dh,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#DEEAF6", edgecolor="#2E75B6",
                                linewidth=1.5))
    ax.text(dx + 0.3, dy + dh - 0.35, "Робочий стіл",
            ha="left", va="center", fontsize=11, fontweight="bold",
            color=ACCENT_BLUE)

    # Значки робочого столу
    icons = [
        ("🗑", "Кошик", 1.0),
        ("🖥", "Цей ПК", 2.7),
        ("📁", "Документи", 4.4),
    ]
    for icon, label, ix in icons:
        _card(ax, dx + ix, dy + dh - 2.1, 1.4, 1.4,
              fill="#FFFFFF", border=ACCENT_BLUE, radius=0.12)
        ax.text(dx + ix + 0.7, dy + dh - 1.1, icon,
                ha="center", va="center", fontsize=22)
        ax.text(dx + ix + 0.7, dy + dh - 1.7, label,
                ha="center", va="center", fontsize=9.5,
                color=TEXT_DARK, fontweight="bold")

    # Відкрите вікно на столі
    ax.add_patch(FancyBboxPatch((dx + 6.0, dy + 2.6), 5.4, 2.2,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor="white", edgecolor="#404040",
                                linewidth=1.3))
    ax.add_patch(Rectangle((dx + 6.0, dy + 4.45), 5.4, 0.35,
                           facecolor="#1F4E79"))
    ax.text(dx + 6.2, dy + 4.62, "📄 Відкрите вікно",
            ha="left", va="center", fontsize=9.5,
            color="white", fontweight="bold")
    ax.text(dx + 8.7, dy + 3.7, "Вікно програми знаходиться\n"
            "поверх робочого столу",
            ha="center", va="center", fontsize=10,
            color=TEXT_DARK, linespacing=1.5)

    # Панель задач
    tx, ty, tw, th = dx, dy - 0.9, dw, 0.75
    ax.add_patch(FancyBboxPatch((tx, ty), tw, th,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor="#1C1C1E", edgecolor="#1C1C1E",
                                linewidth=1.4))
    ax.text(tx + 0.3, ty + th / 2, "Панель задач",
            ha="left", va="center", fontsize=10.5,
            color="white", fontweight="bold")

    # Кнопки на панелі задач
    btn_labels = ["⊞", "📁", "🌐", "📄", "⚙"]
    for i, label in enumerate(btn_labels):
        bx = tx + 2.7 + i * 0.8
        ax.add_patch(FancyBboxPatch((bx, ty + 0.1), 0.6, 0.55,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor="#3A3A3C", edgecolor="#3A3A3C",
                                    linewidth=0))
        ax.text(bx + 0.3, ty + 0.38, label, ha="center", va="center",
                fontsize=13, color="white")

    # Системний лоток
    ax.text(tx + tw - 0.4, ty + th / 2, "14:32  🔊  📶",
            ha="right", va="center", fontsize=10,
            color="white")

    # Підписи-виноски
    ax.annotate("Кнопка «Пуск»", xy=(tx + 3.0, ty + th),
                xytext=(tx + 2.5, ty - 0.65),
                ha="center", fontsize=10, fontweight="bold",
                color=ACCENT_ORANGE,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT_ORANGE,
                                linewidth=1.3))
    ax.annotate("Системний лоток", xy=(tx + tw - 1.5, ty + th),
                xytext=(tx + tw - 2.0, ty - 0.65),
                ha="center", fontsize=10, fontweight="bold",
                color=ACCENT_ORANGE,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT_ORANGE,
                                linewidth=1.3))

    return _save(fig, "scheme_desktop")


# ============================================================
# СХЕМА 3. Буфер обміну
# ============================================================

def scheme_clipboard():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    ax.text(6.5, 6.8, "Буфер обміну: три кроки",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Крок 1
    _card(ax, 0.4, 1.5, 3.9, 4.6, fill="#E1F0FE",
          border=ACCENT_BLUE, radius=0.18)
    _badge(ax, 2.35, 5.5, 0.7, 0.7, ACCENT_BLUE, "1",
           color="white", size=16, radius=0.35)
    ax.text(2.35, 4.85, "ВИДІЛИТИ", ha="center", va="center",
            fontsize=13, fontweight="bold", color=ACCENT_BLUE)
    ax.text(2.35, 4.45, "об'єкт і натиснути\nCtrl + C",
            ha="center", va="center", fontsize=11,
            color=TEXT_DARK, linespacing=1.6)
    ax.text(2.35, 2.6, "📄→📋", ha="center", va="center", fontsize=24)
    ax.text(2.35, 1.9, "об'єкт копіюється\nу буфер", ha="center", va="center",
            fontsize=10.5, style="italic", color=TEXT_GRAY,
            linespacing=1.5)

    # Стрілка
    ax.annotate("", xy=(5.0, 3.8), xytext=(4.5, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=TEXT_GRAY,
                                linewidth=2.0, mutation_scale=18))

    # Крок 2 (буфер посередині)
    _card(ax, 5.2, 1.5, 2.6, 4.6, fill="#F5F5F7",
          border=TEXT_GRAY, radius=0.18)
    ax.text(6.5, 5.5, "БУФЕР", ha="center", va="center",
            fontsize=12, fontweight="bold", color=TEXT_DARK)
    ax.text(6.5, 5.05, "обміну", ha="center", va="center",
            fontsize=11, style="italic", color=TEXT_GRAY)
    ax.text(6.5, 3.4, "📋", ha="center", va="center", fontsize=40)
    ax.text(6.5, 2.2, "тимчасово\nзберігає один\nоб'єкт (або кілька)",
            ha="center", va="center", fontsize=10,
            color=TEXT_DARK, linespacing=1.6)

    # Стрілка
    ax.annotate("", xy=(10.2, 3.8), xytext=(8.1, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=TEXT_GRAY,
                                linewidth=2.0, mutation_scale=18))

    # Крок 3
    _card(ax, 8.7, 1.5, 3.9, 4.6, fill="#E8F8EC",
          border=ACCENT_GREEN, radius=0.18)
    _badge(ax, 10.65, 5.5, 0.7, 0.7, ACCENT_GREEN, "3",
           color="white", size=16, radius=0.35)
    ax.text(10.65, 4.85, "ВСТАВИТИ", ha="center", va="center",
            fontsize=13, fontweight="bold", color=ACCENT_GREEN)
    ax.text(10.65, 4.45, "у потрібному місці\nнатиснути Ctrl + V",
            ha="center", va="center", fontsize=11,
            color=TEXT_DARK, linespacing=1.6)
    ax.text(10.65, 2.6, "📋→📄", ha="center", va="center", fontsize=24)
    ax.text(10.65, 1.9, "об'єкт з'являється\nу новому місці",
            ha="center", va="center", fontsize=10.5, style="italic",
            color=TEXT_GRAY, linespacing=1.5)

    return _save(fig, "scheme_clipboard")


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
        ("Рівень 1", "Робота з вікнами",
         "відкрити, згорнути,\nрозгорнути, перемістити,\nзмінити розмір",
         "≈ 7 хв", ACCENT_GREEN, "#E8F8EC"),
        ("Рівень 2", "Буфер обміну\nта панель задач",
         "Ctrl+C / Ctrl+V,\nзакріплення програм,\nконтекстне меню",
         "≈ 10 хв", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Стандартні\nдодатки",
         "Блокнот, Калькулятор,\nPaint — створення\nі збереження файлів",
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
    img1 = scheme_window_structure()
    img2 = scheme_desktop()
    img3 = scheme_clipboard()
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
    theme_line(doc, "Віконний, графічний інтерфейс. Робота з вікнами. "
                    "Структура вікон Windows. Робочий стіл. Панель "
                    "задач. Технологічні механізми Windows. Буфер "
                    "обміну. Система меню. Стандартні додатки Windows")

    h2(doc, "Мета")
    body(doc, "оволодівати практичними прийомами роботи з вікнами, "
              "панеллю задач, робочим столом, буфером обміну та "
              "стандартними додатками Windows; розвивати дрібну "
              "моторику та координацію «рука–око» під час виконання "
              "операцій з графічними об'єктами; виховувати дбайливе "
              "ставлення до інтерфейсу системи та організованість "
              "на робочому столі.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Маніпулятор «миша» та клавіатура.",
        "Інструкційні картки до рівнів 1–3.",
        "Стандартні додатки Windows: Блокнот, Калькулятор, Paint.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Зайцев В. Г., Дробязко І. П. Операційні системи : навч. посіб. "
        "для студ. спец. 123 «Комп'ютерна інженерія». Київ : КПІ ім. "
        "Ігоря Сікорського, 2019.",
        "Іванов О. В., Петрова Н. М. Основи операційних систем : навч. "
        "посіб. Київ : Основи, 2020.",
        "Микитишин А. Г., Чихіра І. В. Операційні системи : консп. "
        "лекц. Тернопіль : ТНТУ імені Івана Пулюя, 2016.",
    ]
    for s in sources:
        numbered(doc, s)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Віконний графічний інтерфейс")
    body(doc, "Віконний інтерфейс — це спосіб взаємодії з комп'ютером, "
              "у якому кожна програма відкривається в окремому "
              "прямокутному вікні. Користувач бачить не текстові "
              "команди, а графічні об'єкти — вікна, значки, меню, "
              "кнопки — та керує ними за допомогою миші й клавіатури. "
              "Саме віконний інтерфейс зробив комп'ютер зрозумілим "
              "для мільйонів людей без спеціальної підготовки.")

    body(doc, "У Windows віконний інтерфейс реалізований через "
              "оболонку Explorer. Вона забезпечує робочий стіл, "
              "панель задач, меню «Пуск» і файловий менеджер, "
              "який теж називається Проводник.")

    h3(doc, "2. Структура вікна Windows")
    body(doc, "Будь-яке вікно Windows має однакову структуру. "
              "Це один із принципів послідовності інтерфейсу: "
              "елементи керування розташовані там, де користувач "
              "очікує їх побачити.")

    add_figure(doc, img1, 16.0)

    body(doc, "Основні елементи вікна:")
    bullet(doc, "Заголовок вікна — назва програми або документа; "
                "за нього вікно можна перетягувати мишею;")
    bullet(doc, "кнопки керування — «Згорнути», «Розгорнути / "
                "Відновити», «Закрити»; розташовані у правому "
                "верхньому куті;")
    bullet(doc, "рядок меню — команди, згруповані за категоріями "
                "(Файл, Редагування, Вигляд, Довідка);")
    bullet(doc, "робоча область — безпосередньо вміст програми;")
    bullet(doc, "смуги прокручування — вертикальна та горизонтальна; "
                "з'являються, коли вміст не вміщується повністю;")
    bullet(doc, "рядок стану (у деяких програмах) — додаткова "
                "інформація внизу вікна.")

    body(doc, "Дії з вікнами виконуються двома способами: "
              "перетягуванням мишею та подвійним клацанням на "
              "заголовку (розгортання / відновлення). Розмір вікна "
              "можна змінити, потягнувши за будь-який кут або край.")

    h3(doc, "3. Робочий стіл і панель задач")
    body(doc, "Робочий стіл — це головна область екрана, яка "
              "з'являється після входу в систему. На ньому "
              "розташовані значки (ярлики, папки, файли) та "
              "відкриваються вікна програм. Робочий стіл можна "
              "порівняти з поверхнею стола, на якому лежать "
              "потрібні інструменти.")

    add_figure(doc, img2, 16.0)

    body(doc, "Панель задач — горизонтальна смуга внизу екрана. "
              "Вона містить:")
    bullet(doc, "кнопку «Пуск» — відкриває головне меню системи;")
    bullet(doc, "значки закріплених і відкритих програм;")
    bullet(doc, "область сповіщень (системний лоток) — годинник, "
                "гучність, мережа, індикатори безпеки;")
    bullet(doc, "кнопку «Показати робочий стіл» — згортає всі "
                "вікна одним клацанням.")

    body(doc, "На панелі задач можна закріплювати потрібні програми "
              "(права кнопка → «Закріпити на панелі завдань»), щоб "
              "запускати їх одним клацанням. Це зручно для часто "
              "використовуваних додатків.")

    h3(doc, "4. Буфер обміну")
    body(doc, "Буфер обміну — це тимчасова область пам'яті, у яку "
              "система поміщає скопійований або вирізаний об'єкт. "
              "Звідти цей об'єкт можна вставити в інше місце — "
              "в іншу програму, документ або папку.")

    add_figure(doc, img3, 16.0)

    body(doc, "Три базові операції з буфером обміну:")
    bullet(doc, "Ctrl + C — копіювати виділений об'єкт (оригінал "
                "залишається на місці);")
    bullet(doc, "Ctrl + X — вирізати об'єкт (він зникає з місця "
                "і поміщається в буфер);")
    bullet(doc, "Ctrl + V — вставити об'єкт з буфера в потрібне "
                "місце.")

    body(doc, "Буфер обміну зберігає лише один об'єкт (або один "
              "набір об'єктів) одночасно: коли ви копіюєте щось "
              "нове, попередній вміст буфера замінюється. У "
              "Windows 10/11 є розширений буфер обміну (Win + V), "
              "який зберігає історію останніх копіювань.")

    callout(doc,
            "Буфер обміну працює між різними програмами. "
            "Наприклад, можна скопіювати текст із Блокнота "
            "(Ctrl + C) і вставити його у Paint як напис або в "
            "адресний рядок браузера (Ctrl + V). Саме завдяки "
            "буферу обміну вдається швидко переносити дані з "
            "однієї програми в іншу.",
            fill="E1F0FE", accent="0071E3")

    h3(doc, "5. Система меню")
    body(doc, "Меню — це список команд, з яких користувач обирає "
              "потрібну. У Windows використовують кілька видів меню:")
    bullet(doc, "головне меню «Пуск» — запуск програм, налаштування, "
                "вимкнення;")
    bullet(doc, "рядок меню у вікні програми (Файл, Редагування, "
                "Вигляд, Довідка);")
    bullet(doc, "контекстне меню — з'являється після натискання "
                "правої кнопки миші на об'єкті; містить команди, "
                "доречні саме для цього об'єкта.")

    body(doc, "Контекстне меню — найшвидший спосіб виконати типову "
              "дію (копіювати, перейменувати, видалити, відкрити "
              "властивості), не шукаючи відповідну команду в "
              "рядку меню.")

    h3(doc, "6. Стандартні додатки Windows")
    body(doc, "Windows постачається з набором простих програм, "
              "достатніх для типових завдань користувача. Їх "
              "називають стандартними додатками.")

    add_table(
        doc,
        ["Додаток", "Призначення", "Типове використання"],
        [
            ["Блокнот", "Простий текстовий редактор",
             "Швидкі нотатки, чернетки, перегляд .txt"],
            ["Калькулятор", "Обчислення",
             "Арифметичні дії, інженерні розрахунки"],
            ["Paint", "Растовий графічний редактор",
             "Малюнки, обрізання скріншотів, схеми"],
            ["Ножиці / Фрагмент", "Створення скріншотів",
             "Знімок екрана або окремої області"],
            ["Проводник", "Файловий менеджер",
             "Робота з файлами й папками"],
            ["WordPad", "Розширений текстовий редактор",
             "Документи з форматуванням (у старих версіях)"],
        ],
        widths=[3.6, 6.2, 6.7],
    )

    body(doc, "Стандартні додатки запускаються через меню «Пуск» "
              "(поле пошуку) або через команду в діалозі "
              "«Виконати» (Win + R): notepad, calc, mspaint.")

    h3(doc, "7. Організованість робочого столу")
    body(doc, "Дбайливе ставлення до інтерфейсу системи — це не "
              "лише естетика, а й практична зручність. Коли "
              "робочий стіл організований, легше знайти потрібне "
              "й швидше виконати роботу.")
    bullet(doc, "тримайте на робочому столі лише ті ярлики, якими "
                "регулярно користуєтеся;")
    bullet(doc, "сортуйте файли за темами в окремих папках, а не "
                "зберігайте все на робочому столі;")
    bullet(doc, "використовуйте змістовні назви для файлів і "
                "ярликів;")
    bullet(doc, "періодично очищуйте Кошик і тимчасові файли;")
    bullet(doc, "не захаращуйте панель задач знайомими програмами, "
                "якими користуєтеся раз на місяць.")

    callout(doc,
            "Захоплення усього екрана скріншотом (Print Screen) "
            "копіює зображення в буфер обміну. Далі його можна "
            "вставити в Paint (Ctrl + V), обрізати й зберегти як "
            "файл. Комбінація Win + Shift + S запускає «Ножиці» — "
            "зручніший спосіб зробити знімок лише потрібної "
            "області екрана.",
            fill="FFF4E5", accent="C93400")

    # =====================================================
    # РІВНІ ЗАВДАНЬ
    # =====================================================
    h2(doc, "Покроковий алгоритм виконання різнорівневих завдань")

    body(doc, "Практична частина заняття побудована за трирівневою "
              "системою. Студент виконує завдання послідовно; "
              "орієнтовний час на кожен рівень — 7–10 хвилин, "
              "загальна тривалість — 25–30 хвилин. Оцінка залежить "
              "від кількості успішно виконаних рівнів.")

    add_figure(doc, img4, 16.0)

    # -------- Рівень 1 --------
    h3(doc, "Рівень 1 — робота з вікнами (≈ 7 хв)",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Мета: навчитися відкривати вікна, керувати їхнім "
              "розміром і положенням, перемикатися між кількома "
              "вікнами.")

    add_table(
        doc,
        ["№", "Дія", "Як виконати"],
        [
            ["1", "Відкрийте Блокнот",
             "Пуск → пошук → notepad → Enter"],
            ["2", "Відкрийте Калькулятор",
             "Пуск → пошук → calc → Enter"],
            ["3", "Відкрийте Paint",
             "Пуск → пошук → mspaint → Enter"],
            ["4", "Перемкніться між вікнами",
             "Alt + Tab  або клацанням на панелі задач"],
            ["5", "Згорніть усі вікна",
             "Кнопка «—» у заголовку або Win + D"],
            ["6", "Розгорніть одне вікно на весь екран",
             "Подвійне клацання на заголовку або кнопка «☐»"],
            ["7", "Відновіть попередній розмір",
             "Повторне подвійне клацання на заголовку"],
            ["8", "Змініть розмір вікна",
             "Потягніть за будь-який кут чи край"],
            ["9", "Перемістіть вікно",
             "Потягніть за заголовок"],
            ["10", "Розташуйте два вікна поруч",
             "Перетягніть вікно до лівого або правого краю екрана"],
            ["11", "Зробіть скріншот",
             "Print Screen → вставте у звіт із підписом"],
        ],
        widths=[1.0, 6.0, 9.5],
    )

    callout(doc,
            "Після виконання рівня 1 у звіті має бути один скріншот, "
            "на якому видно два вікна поруч (наприклад, Блокнот і "
            "Калькулятор). Якщо вікна не розташовуються поруч — "
            "перевірте, чи не увімкнено режим планшета.",
            fill="E8F8EC", accent="248A3D")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — буфер обміну та панель задач (≈ 10 хв)",
       color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Мета: навчитися копіювати й вставляти об'єкти між "
              "програмами, працювати з контекстним меню та "
              "закріплювати програми на панелі задач.")

    add_table(
        doc,
        ["№", "Дія", "Як виконати"],
        [
            ["1", "Скопіюйте текст у Блокноті",
             "Виділіть текст → Ctrl + C"],
            ["2", "Вставте текст у Блокнот",
             "Клацніть у полі → Ctrl + V"],
            ["3", "Скопіюйте число з Калькулятора",
             "Обчисліть 15 × 24 → Ctrl + C (результат)"],
            ["4", "Вставте результат у Блокнот",
             "Перемкніться у Блокнот → Ctrl + V"],
            ["5", "Виріжте рядок із Блокнота",
             "Виділіть рядок → Ctrl + X"],
            ["6", "Вставте рядок в інше місце",
             "Клацніть у кінці тексту → Ctrl + V"],
            ["7", "Скопіюйте фрагмент малюнка у Paint",
             "Виділіть область → Ctrl + C"],
            ["8", "Вставте фрагмент у Paint",
             "Ctrl + V — з'явиться копія"],
            ["9", "Створіть ярлик на робочому столі",
             "Права кнопка на робочому столі → Створити → Ярлик"],
            ["10", "Закріпіть Блокнот на панелі задач",
             "Права кнопка на значку в панелі задач → "
             "«Закріпити на панелі завдань»"],
            ["11", "Відкрийте контекстне меню на файлі",
             "Права кнопка на будь-якому ярлику"],
            ["12", "Зробіть скріншот",
             "Знімок вікна Блокнота з трьома рядками: "
             "текст, число, вирізаний рядок"],
        ],
        widths=[1.0, 6.0, 9.5],
    )

    callout(doc,
            "У звіті має бути: скріншот Блокнота з трьома рядками "
            "тексту (оригінал, число з Калькулятора, вирізаний "
            "рядок), скріншот закріпленого Блокнота на панелі "
            "задач і коротке пояснення різниці між Ctrl + C і "
            "Ctrl + X.",
            fill="FFF4E5", accent="C93400")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — стандартні додатки (≈ 10 хв)",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Мета: створити й зберегти файл у стандартному "
              "додатку, використовуючи навички роботи з вікнами, "
              "меню та буфером обміну.")

    body(doc, "Завдання А. Створіть зображення в Paint:")
    tasks_a = [
        "Відкрийте Paint (mspaint).",
        "Намалюйте просту схему: прямокутник із написом "
        "«Практика» та стрілку до другого прямокутника з "
        "написом «ПІБ».",
        "Скопіюйте фрагмент малюнка (Ctrl + C) і вставте його "
        "в інше місце (Ctrl + V).",
        "Збережіть файл: Файл → Зберегти як → "
        "«Практика_ПІБ.png» на робочому столі.",
    ]
    for t in tasks_a:
        numbered(doc, t)

    body(doc, "Завдання Б. Створіть текстовий файл у Блокноті:")
    tasks_b = [
        "Відкрийте Блокнот.",
        "Введіть три рядки: своє прізвище, дату й коротке "
        "речення про те, що сьогодні вивчили.",
        "Скопіюйте перший рядок і вставте його ще раз у кінці.",
        "Збережіть файл: Файл → Зберегти як → "
        "«Нотатка_ПІБ.txt» на робочому столі.",
    ]
    for t in tasks_b:
        numbered(doc, t)

    body(doc, "Завдання В. Обчислення в Калькуляторі:")
    tasks_v = [
        "Відкрийте Калькулятор у режимі «Звичайний».",
        "Обчисліть: 128 × 17 + 256 ÷ 4.",
        "Скопіюйте результат (Ctrl + C).",
        "Вставте результат у текстовий файл «Нотатка_ПІБ.txt» "
        "(Ctrl + V) і збережіть зміни.",
    ]
    for t in tasks_v:
        numbered(doc, t)

    body(doc, "Завдання Г. У звіті наведіть:")
    numbered(doc, "скріншот малюнка з Paint (два прямокутники "
                  "й стрілка);")
    numbered(doc, "скріншот текстового файлу в Блокноті з "
                  "результатом обчислення;")
    numbered(doc, "пояснення, у яких випадках зручніше "
                  "використовувати Ctrl + C, а коли — Ctrl + X;")
    numbered(doc, "короткий висновок (3–4 речення) про те, які "
                  "навички сьогодні виявилися найпотрібнішими.")

    callout(doc,
            "За бажанням (+1 бал). Створіть скріншот лише області "
            "малюнка через «Ножиці» (Win + Shift + S) і збережіть "
            "його окремим файлом «Скріншот_ПІБ.png». Поясніть, "
            "чим цей спосіб зручніший за звичайний Print Screen.",
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
             "Усі дії з вікнами виконано правильно; є скріншот із "
             "двома вікнами поруч", "3"],
            ["Рівень 2",
             "Копіювання й вирізання працюють; ярлик створено; "
             "Блокнот закріплено на панелі задач; є скріншоти",
             "4"],
            ["Рівень 3",
             "Малюнок у Paint і файл .txt створено й збережено; "
             "результат обчислення вставлено; є скріншоти й "
             "висновок", "4"],
            ["Якість звіту",
             "Оформлення за вимогами; підписи до скріншотів; "
             "пояснення різниці між Ctrl + C і Ctrl + X", "1"],
            ["Творчий підхід",
             "Виконано ускладнення зі «Ножицями» або "
             "запропоновано власну ідею", "1"],
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
        "Скріншот двох вікон поруч після рівня 1 (наприклад, "
        "Блокнот і Калькулятор).",
        "Скріншот Блокнота з трьома рядками тексту, числа та "
        "вирізаного рядка після рівня 2.",
        "Скріншот закріпленого Блокнота на панелі задач.",
        "Скріншот малюнка в Paint після рівня 3 (два "
        "прямокутники й стрілка).",
        "Скріншот текстового файлу «Нотатка_ПІБ.txt» із "
        "результатом обчислення.",
        "Відповіді на питання: чим Ctrl + C відрізняється від "
        "Ctrl + X; які елементи має будь-яке вікно Windows; "
        "що таке контекстне меню і коли воно зручніше за "
        "рядок меню.",
        "Висновок: що нового засвоїли, які навички виявилися "
        "найпотрібнішими.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, "
              "шрифт Times New Roman 14 pt, інтервал 1,15, поля 2 см, "
              "обсяг — 3–5 сторінок без титульної. Ім'я файлу: "
              "«Практика_Вікна_Windows_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    doc.save("Практичне_заняття_Вікна_Windows.docx")
    print("Готово: Практичне_заняття_Вікна_Windows.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()