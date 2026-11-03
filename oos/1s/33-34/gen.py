# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: САМОСТІЙНА РОБОТА
Тема: Робота з вікнами. Діалогове вікно та основні його елементи
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

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
# СХЕМА 1. Типи вікон
# ============================================================

def scheme_window_types():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.35, "Три типи вікон Windows",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    types = [
        ("Програмне", "Вікно програми",
         "Містить рядок меню,\nпанелі інструментів,\nробочу область.\n"
         "Можна змінювати розмір\nі переміщати.",
         "Блокнот\nПроводник\nPaint",
         ACCENT_BLUE, "#E1F0FE"),
        ("Діалогове", "Вікно запиту",
         "Використовується для\nвведення параметрів\nабо підтвердження дії.\n"
         "Часто НЕ можна змінити\nрозмір; чекає відповіді.",
         "Зберегти як\nПараметри\nПідтвердження",
         ACCENT_ORANGE, "#FFF4E5"),
        ("Документа", "Вікно файлу",
         "Відкривається усередині\nпрограмного вікна.\nМістить вміст\n"
         "конкретного документа.\nУ деяких програмах —\nокреме вікно.",
         "Текст у Блокноті\nТаблиця в Excel\nСлайд у PowerPoint",
         ACCENT_GREEN, "#E8F8EC"),
    ]

    card_w, card_h = 3.9, 6.4
    gap = 0.35
    x0 = 0.5
    y0 = 0.8

    for i, (title, subtitle, desc, examples, color, fill) in enumerate(types):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h, fill=fill, border=color, radius=0.18)
        _badge(ax, cx, y0 + card_h - 0.55, 2.6, 0.6, color, title,
               color="white", size=13, radius=0.3)
        ax.text(cx, y0 + card_h - 1.25, subtitle, ha="center", va="center",
                fontsize=11, style="italic", color=TEXT_DARK)
        ax.text(cx, y0 + card_h - 3.15, desc, ha="center", va="center",
                fontsize=10.5, color=TEXT_DARK, linespacing=1.7)
        ax.text(cx, y0 + 1.0, "Приклади:", ha="center", va="center",
                fontsize=10.5, fontweight="bold", color=color)
        ax.text(cx, y0 + 0.55, examples, ha="center", va="center",
                fontsize=9.5, color=TEXT_DARK, linespacing=1.5)

    return _save(fig, "scheme_window_types")


# ============================================================
# СХЕМА 2. Структура діалогового вікна (анотована)
# ============================================================

def scheme_dialog_structure():
    fig, ax = plt.subplots(figsize=(11, 7.4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.6)
    ax.axis("off")

    ax.text(6.5, 8.2, "Структура діалогового вікна «Зберегти як»",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Діалогове вікно
    wx, wy, ww, wh = 1.5, 1.4, 10.0, 6.0
    ax.add_patch(FancyBboxPatch((wx, wy), ww, wh,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="white", edgecolor="#404040",
                                linewidth=1.8))

    # Заголовок
    ax.add_patch(Rectangle((wx, wy + wh - 0.55), ww, 0.55,
                           facecolor="#1F4E79"))
    ax.text(wx + 0.4, wy + wh - 0.28, "Зберегти як",
            ha="left", va="center", fontsize=11, fontweight="bold",
            color="white")
    ax.text(wx + ww - 0.3, wy + wh - 0.28, "✕",
            ha="center", va="center", fontsize=13, color="white",
            fontweight="bold")

    # Ліва панель навігації
    ax.add_patch(Rectangle((wx + 0.15, wy + 0.6), 2.2, wh - 1.3,
                           facecolor="#F5F5F7", edgecolor="#BFBFBF",
                           linewidth=0.8))
    for i, line in enumerate(["Робочий стіл", "Документи",
                              "Завантаження", "Диск C:"]):
        ax.text(wx + 0.3, wy + wh - 1.15 - i * 0.45, line,
                ha="left", va="center", fontsize=9.5, color=TEXT_DARK)

    # Поле введення імені файлу
    ax.text(wx + 2.6, wy + wh - 1.0, "Ім'я файлу:",
            ha="left", va="center", fontsize=10, fontweight="bold",
            color=TEXT_DARK)
    ax.add_patch(FancyBboxPatch((wx + 2.6, wy + wh - 1.55), ww - 2.9, 0.42,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor="white", edgecolor="#404040",
                                linewidth=1.0))
    ax.text(wx + 2.75, wy + wh - 1.34, "Звіт.txt",
            ha="left", va="center", fontsize=10, color=TEXT_DARK,
            family="monospace")

    # Поле типу файлу
    ax.text(wx + 2.6, wy + wh - 2.15, "Тип файлу:",
            ha="left", va="center", fontsize=10, fontweight="bold",
            color=TEXT_DARK)
    ax.add_patch(FancyBboxPatch((wx + 2.6, wy + wh - 2.65), ww - 2.9, 0.4,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor="white", edgecolor="#404040",
                                linewidth=1.0))
    ax.text(wx + 2.75, wy + wh - 2.45, "Текстові документи (*.txt)  ▼",
            ha="left", va="center", fontsize=9.5, color=TEXT_DARK)

    # Основна область (список файлів)
    ax.add_patch(Rectangle((wx + 2.6, wy + 1.1), ww - 2.9, wh - 4.05,
                           facecolor="white", edgecolor="#BFBFBF",
                           linewidth=0.8))
    for i, line in enumerate(["📄 звіт_1.txt", "📄 звіт_2.txt",
                              "📄 нотатки.txt"]):
        ax.text(wx + 2.8, wy + wh - 3.1 - i * 0.35, line,
                ha="left", va="center", fontsize=9.5, color=TEXT_DARK)

    # Кнопки
    btn_specs = [
        (wx + ww - 1.5, "Зберегти", "#0071E3"),
        (wx + ww - 2.8, "Скасувати", "#E5E5EA"),
    ]
    for bx, label, color in btn_specs:
        tc = "white" if color == "#0071E3" else TEXT_DARK
        ax.add_patch(FancyBboxPatch((bx, wy + 0.35), 1.2, 0.5,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=color, edgecolor="#404040",
                                    linewidth=0.8))
        ax.text(bx + 0.6, wy + 0.6, label, ha="center", va="center",
                fontsize=9.5, color=tc, fontweight="bold")

    # Виноски
    notes = [
        ("Заголовок", (wx + 3.0, wy + wh - 0.28), (6.5, 8.0), ACCENT_BLUE),
        ("Поле введення", (wx + 5.0, wy + wh - 1.34), (11.7, 7.4),
         ACCENT_ORANGE),
        ("Список вибору", (wx + 5.0, wy + wh - 2.45), (11.7, 6.4),
         ACCENT_ORANGE),
        ("Область вмісту", (wx + 5.0, wy + 2.6), (11.7, 2.0),
         ACCENT_GREEN),
        ("Кнопка дії", (wx + ww - 0.9, wy + 0.6), (9.5, 0.5),
         ACCENT_RED),
    ]
    for label, xy, xytext, color in notes:
        ax.annotate(label, xy=xy, xytext=xytext,
                    ha="center", va="center", fontsize=10.5,
                    fontweight="bold", color=color,
                    arrowprops=dict(arrowstyle="-|>", color=color,
                                    linewidth=1.5))

    return _save(fig, "scheme_dialog_structure")


# ============================================================
# СХЕМА 3. Основні елементи діалогових вікон
# ============================================================

def scheme_dialog_elements():
    fig, ax = plt.subplots(figsize=(11, 8.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    ax.text(6.5, 9.15, "Основні елементи діалогових вікон",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    elements = [
        ("Поле введення", "Однорядкове поле\nдля тексту чи числа",
         "☐ Звіт.txt", ACCENT_BLUE, "#E1F0FE"),
        ("Поле зі списком", "Розкривний список\nготових варіантів",
         "Тип файлу  ▼", ACCENT_GREEN, "#E8F8EC"),
        ("Перемикач (radio)", "Один варіант із кількох.\nЛише один активний",
         "◉ Так    ○ Ні", ACCENT_ORANGE, "#FFF4E5"),
        ("Прапорець (check)", "Так/ні для кожного\nпункту незалежно",
         "☑ Тільки читання\n☐ Прихований",
         ACCENT_PURPLE, "#EFE6F7"),
        ("Кнопка", "Виконує дію\nодразу після натискання",
         "[ Зберегти ]  [ Скасувати ]",
         ACCENT_BLUE, "#E1F0FE"),
        ("Вкладка", "Група налаштувань\nу межах одного вікна",
         "Загальні | Вигляд | Безпека",
         ACCENT_RED, "#FFEBEA"),
    ]

    card_w, card_h = 6.0, 2.7
    gap_x, gap_y = 0.35, 0.3
    x0 = 0.35
    y_top = 8.6

    for i, (title, desc, example, color, fill) in enumerate(elements):
        col, row = i % 2, i // 2
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)

        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.15)
        ax.text(x + 0.35, y + card_h - 0.5, title, ha="left", va="center",
                fontsize=12.5, fontweight="bold", color=color)
        ax.text(x + 0.35, y + 1.0, desc, ha="left", va="center",
                fontsize=10.5, color=TEXT_DARK, linespacing=1.55)

        # Приклад-прев'ю
        ax.add_patch(FancyBboxPatch((x + 3.0, y + 0.3), card_w - 3.3,
                                    card_h - 0.9,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor="white", edgecolor="#404040",
                                    linewidth=0.9))
        ax.text(x + 3.15, y + card_h / 2 - 0.1, example,
                ha="left", va="center", fontsize=10,
                color=TEXT_DARK, family="monospace", linespacing=1.6)

    return _save(fig, "scheme_dialog_elements")


# ============================================================
# СХЕМА 4. Етапи роботи
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
        "Опрацювати теоретичний матеріал і схеми 1–3",
        "Заповнити таблицю «Типи вікон» (3 типи × 3 параметри)",
        "Дослідити 2 діалогові вікна і записати їхні елементи",
        "Скласти схему власного діалогового вікна",
        "Дати відповіді на теоретичні питання",
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
    img1 = scheme_window_types()
    img2 = scheme_dialog_structure()
    img3 = scheme_dialog_elements()
    img4 = scheme_steps()

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
    theme_line(doc, "Робота з вікнами. Діалогове вікно та основні "
                    "його елементи")

    h2(doc, "Мета")
    body(doc, "систематизувати знання про типи вікон (програмні, "
              "діалогові, документа) та їхні основні елементи (поля, "
              "кнопки, перемикачі); розвивати навички самостійного "
              "аналізу структури будь-якого діалогового вікна для "
              "швидкого налаштування програми; виховувати уважність "
              "і послідовність під час заповнення форм та параметрів "
              "у діалогових вікнах.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Стандартні додатки Windows (Блокнот, Paint, Проводник).",
        "Інструкційні картки із завданнями.",
        "Текстовий редактор для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Іванов О. В., Петрова Н. М. Основи операційних систем : навч. "
        "посіб. Київ : Основи, 2020.",
        "Микитишин А. Г., Чихіра І. В. Операційні системи : консп. "
        "лекц. Тернопіль : ТНТУ імені Івана Пулюя, 2016.",
        "Погребняк Б. І., Булаєнко М. В. Операційні системи : навч. "
        "посіб. Харків. нац. ун-т міськ. госп-ва ім. О. М. Бекетова. "
        "Харків : ХНУМГ ім. О. М. Бекетова, 2018.",
    ]
    for s in sources:
        numbered(doc, s)

    # ---------- Завдання ----------
    h2(doc, "Завдання самостійної роботи")
    tasks = [
        "Опрацювати теоретичний матеріал і схеми 1–3.",
        "Заповнити порівняльну таблицю «Типи вікон» (3 типи × "
        "3 параметри).",
        "Дослідити два діалогові вікна у Windows і виписати їхні "
        "елементи.",
        "Скласти власну схему діалогового вікна (не менше 5 "
        "елементів різних типів).",
        "Дати письмові відповіді на теоретичні питання.",
        "Оформити звіт згідно з рекомендаціями та надіслати "
        "викладачу у визначений термін.",
    ]
    for t in tasks:
        numbered(doc, t)

    h2(doc, "Терміни виконання")
    body(doc, "Робота виконується протягом одного тижня після "
              "отримання завдання; готовий звіт подається на "
              "наступному практичному занятті або завантажується в "
              "електронний курс дисципліни до вказаної дати.")

    h2(doc, "Очікувані результати")
    results = [
        "називає три типи вікон Windows і пояснює різницю між ними;",
        "характеризує структуру діалогового вікна;",
        "розрізняє основні елементи діалогу: поле введення, поле "
        "зі списком, перемикач, прапорець, вкладку, кнопку;",
        "самостійно аналізує структуру незнайомого діалогового "
        "вікна;",
        "пояснює різницю між перемикачем (radio) і прапорцем "
        "(checkbox);",
        "складає власну схему діалогового вікна із заданими "
        "елементами.",
    ]
    for r in results:
        bullet(doc, r)

    # ---------- Опрацьовувані питання ----------
    h2(doc, "Перелік опрацьовуваних питань")
    topics = [
        "Поняття вікна та віконного інтерфейсу.",
        "Три типи вікон: програмне, діалогове, документа — "
        "призначення й особливості.",
        "Структура програмного вікна Windows.",
        "Призначення діалогових вікон: введення параметрів, "
        "підтвердження дії, попередження.",
        "Основні елементи діалогового вікна: поля введення, "
        "списки, перемикачі, прапорці, вкладки, кнопки.",
        "Різниця між перемикачем і прапорцем.",
        "Кнопки «ОК», «Скасувати», «Застосувати» — коли "
        "використовується кожна.",
        "Модальні та немодальні діалогові вікна.",
        "Правила заповнення діалогових форм.",
        "Типові помилки під час роботи з діалоговими вікнами.",
    ]
    for tp in topics:
        numbered(doc, tp)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості (стислий огляд)")

    h3(doc, "1. Три типи вікон Windows")
    body(doc, "У Windows усі вікна поділяють на три типи: програмні, "
              "діалогові та вікна документа. Кожен тип має своє "
              "призначення й характерні особливості.")

    add_figure(doc, img1, 16.0)

    body(doc, "Програмне вікно — це вікно програми, у якому вона "
              "працює. Воно містить заголовок, рядок меню, панелі "
              "інструментів і робочу область. Програмне вікно можна "
              "переміщати, змінювати його розмір, згортати, "
              "розгортати та закривати.")

    body(doc, "Діалогове вікно — це вікно для взаємодії з "
              "користувачем: воно запитує параметри, підтверджує "
              "дію або попереджає про наслідки. Діалогове вікно "
              "зазвичай НЕ можна змінити в розмірі; воно з'являється "
              "поверх програмного й чекає на відповідь. Саме тому "
              "його називають діалогом — система «розмовляє» з "
              "користувачем.")

    body(doc, "Вікно документа — це вікно всередині програмного, у "
              "якому відкрито конкретний файл. Наприклад, у Блокноті "
              "відкрито файл «Звіт.txt» — це і є вікно документа. У "
              "деяких програмах (Word, Excel) кожен документ "
              "відкривається в окремому вікні програми.")

    h3(doc, "2. Структура діалогового вікна")
    body(doc, "Діалогове вікно має типову структуру, яку корисно "
              "знати, щоб швидко орієнтуватися в будь-якому "
              "незнайомому діалозі.")

    add_figure(doc, img2, 16.0)

    body(doc, "Типові елементи діалогового вікна:")
    bullet(doc, "заголовок — назва діалогу (наприклад, «Зберегти "
                "як»);")
    bullet(doc, "область вмісту — основна частина з полями й "
                "перемикачами;")
    bullet(doc, "кнопки дії — «ОК», «Скасувати», «Застосувати»; "
                "розташовані внизу або справа;")
    bullet(doc, "область попереднього перегляду (у деяких "
                "діалогах) — показує, як виглядатиме результат.")

    h3(doc, "3. Основні елементи діалогових вікон")
    body(doc, "Діалогові вікна складаються з елементів керування. "
              "Кожен елемент має своє призначення й характерну "
              "поведінку. Уміння розпізнавати ці елементи — ключова "
              "навичка під час роботи з будь-якою програмою.")

    add_figure(doc, img3, 16.0)

    add_table(
        doc,
        ["Елемент", "Призначення", "Приклад"],
        [
            ["Поле введення", "Введення тексту або числа з клавіатури",
             "Поле «Ім'я файлу»"],
            ["Поле зі списком", "Вибір з готового переліку варіантів",
             "Список «Тип файлу»"],
            ["Перемикач (radio)", "Вибір ОДНОГО варіанта з кількох",
             "◉ Так    ○ Ні"],
            ["Прапорець (checkbox)", "Незалежне вмикання/вимикання "
                                     "кожного пункту",
             "☑ Тільки читання  ☐ Прихований"],
            ["Кнопка", "Виконання дії одразу після натискання",
             "[ Зберегти ]  [ Скасувати ]"],
            ["Вкладка", "Група налаштувань у межах одного діалогу",
             "Загальні | Вигляд | Безпека"],
            ["Повзунок", "Вибір значення з діапазону",
             "Гучність, яскравість"],
            ["Лічильник", "Збільшення/зменшення числа",
             "Кількість копій: [3] ▲▼"],
        ],
        widths=[3.6, 7.1, 5.8],
    )

    body(doc, "Розгляньмо детальніше ключові елементи.")

    h3(doc, "Поля введення та списки", color=RGBColor(0x00, 0x71, 0xE3))
    body(doc, "Поле введення — це прямокутна область, у яку "
              "користувач набирає текст або число з клавіатури. "
              "Коли поле активне, у ньому блимає курсор. Поле зі "
              "списком (випадаючий список) пропонує готові варіанти; "
              "користувач обирає один зі списку або може ввести "
              "своє значення, якщо список допускає введення.")

    h3(doc, "Перемикач і прапорець",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Перемикач (radio button) — це круглий елемент, який "
              "дозволяє обрати РІВНО ОДИН варіант із групи. Коли ви "
              "обираєте інший варіант, попередній автоматично "
              "знімається. Прапорець (checkbox) — це квадратний "
              "елемент, який працює незалежно: можна поставити "
              "кілька прапорців одночасно або не поставити жодного.")

    add_table(
        doc,
        ["Ознака", "Перемикач (radio)", "Прапорець (checkbox)"],
        [
            ["Форма", "Кругла", "Квадратна"],
            ["Скільки можна обрати", "Лише один зі групи",
             "Будь-яку кількість незалежно"],
            ["Приклад", "Стать: ◉ чоловіча ○ жіноча",
             "☑ Тільки читання  ☑ Прихований  ☐ Архівний"],
        ],
        widths=[4.2, 6.1, 6.2],
    )

    h3(doc, "Кнопки", color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Кнопки в діалогових вікнах мають різне призначення:")
    bullet(doc, "«ОК» — підтверджує зміни й закриває діалог;")
    bullet(doc, "«Скасувати» — закриває діалог БЕЗ збереження змін;")
    bullet(doc, "«Застосувати» — застосовує зміни, але не закриває "
                "діалог (можна продовжити налаштування);")
    bullet(doc, "додаткові кнопки («Огляд...», «Довідка», «За "
                "замовчуванням») виконують конкретні дії.")

    callout(doc,
            "Кнопка «Скасувати» або клавіша Esc закривають діалог "
            "без збереження змін. Клавіша Enter зазвичай натискає "
            "кнопку «ОК». Якщо ви випадково відкрили не той діалог "
            "— натисніть Esc, і жодні зміни не будуть застосовані.",
            fill="FFF4E5", accent="C93400")

    h3(doc, "Модальні та немодальні діалоги")
    body(doc, "Модальне діалогове вікно блокує роботу з рештою "
              "програми, доки користувач його не закриє. Наприклад, "
              "«Зберегти як» — модальне: не можна продовжити роботу "
              "з документом, поки не виберете ім'я файлу. "
              "Немодальне — не блокує програму: наприклад, вікно "
              "«Знайти й замінити» часто працює паралельно з "
              "редагуванням.")

    h3(doc, "4. Типові помилки під час роботи з діалогами")
    body(doc, "Навіть досвідчені користувачі припускаються помилок "
              "у діалогових вікнах. Найчастіші з них:")
    bullet(doc, "натиснути «ОК», не перевіривши всі параметри — "
                "діалог закриється, і зміни буде застосовано;")
    bullet(doc, "закрити діалог хрестиком у заголовку замість "
                "«Скасувати» — деякі програми сприймають це як "
                "«ОК» і зберігають зміни;")
    bullet(doc, "не звернути увагу на попередження (наприклад, "
                "«Файл уже існує. Перезаписати?»);")
    bullet(doc, "залишити поле обов'язковим, не заповнивши його — "
                "діалог не закриється або видасть помилку.")

    callout(doc,
            "Перед натисканням «ОК» пробігайте очима всі поля "
            "діалогу. Особливо важливо перевірити шлях збереження "
            "(у якій папці буде файл), ім'я файлу та формат. "
            "Помилка в цих трьох параметрах призводить до того, що "
            "потім довго шукаєш файл або отримуєш його в "
            "неправильному форматі.",
            fill="FFEBEA", accent="C4001D")

    # =====================================================
    # ЕТАПИ РОБОТИ
    # =====================================================
    h2(doc, "Етапи виконання самостійної роботи")
    body(doc, "Робота виконується послідовно за шість етапів. Кожен "
              "етап завершується певним результатом, який стане "
              "частиною звіту.")

    add_figure(doc, img4, 15.5)

    # ---------- Таблиця типів вікон ----------
    h2(doc, "Завдання на заповнення таблиці «Типи вікон»")
    body(doc, "Заповніть таблицю, указавши для кожного типу вікна "
              "його характеристики. Намагайтеся не переписувати "
              "теорію дослівно, а формулювати своїми словами.")

    add_table(
        doc,
        ["Параметр", "Програмне", "Діалогове", "Документа"],
        [
            ["Призначення", "", "", ""],
            ["Чи можна змінити розмір", "", "", ""],
            ["Чи блокує інші вікна", "", "", ""],
            ["Типові елементи", "", "", ""],
            ["Приклад", "", "", ""],
        ],
        widths=[4.2, 4.1, 4.1, 4.1],
    )

    # ---------- Дослідження діалогових вікон ----------
    h2(doc, "Завдання на дослідження діалогових вікон")
    body(doc, "Відкрийте два діалогові вікна у Windows (наприклад, "
              "«Зберегти як» у Блокноті та «Властивості» файлу) і "
              "для кожного заповніть таблицю.")

    add_table(
        doc,
        ["Параметр дослідження", "Вікно 1", "Вікно 2"],
        [
            ["Назва діалогу", "", ""],
            ["Програма, з якої відкрито", "", ""],
            ["Поля введення", "", ""],
            ["Поля зі списком", "", ""],
            ["Перемикачі", "", ""],
            ["Прапорці", "", ""],
            ["Кнопки дії", "", ""],
            ["Модальне чи ні", "", ""],
        ],
        widths=[5.2, 5.6, 5.7],
    )

    # ---------- Схема власного діалогу ----------
    h2(doc, "Завдання на складання власної схеми діалогу")
    body(doc, "Уявіть, що ви розробляєте діалогове вікно для "
              "програми «Мій щоденник». Вікно має дозволяти "
              "користувачу налаштувати основні параметри щоденника. "
              "Складіть схему цього вікна та опишіть його елементи.")

    body(doc, "Вимоги до схеми:")
    requirements = [
        "Не менше 5 елементів різних типів (наприклад, поле "
        "введення, поле зі списком, перемикач, прапорець, кнопка).",
        "Схема має бути візуальною (малюнок у Paint, Word або на "
        "папері з фотографією).",
        "Під схемою — перелік елементів із поясненням, для чого "
        "кожен із них.",
        "2–3 речення про те, що робитиме кнопка «ОК» у цьому "
        "діалозі.",
    ]
    for r in requirements:
        bullet(doc, r)

    # =====================================================
    # ТЕОРЕТИЧНІ ПИТАННЯ
    # =====================================================
    h2(doc, "Теоретичні питання для самоперевірки")
    questions = [
        "Що таке вікно? Які типи вікон ви знаєте?",
        "Чим програмне вікно відрізняється від діалогового? "
        "Наведіть приклад кожного.",
        "Що таке вікно документа? Чи завжди воно виглядає як "
        "окреме вікно програми?",
        "Назвіть основні елементи діалогового вікна.",
        "Чим перемикач (radio) відрізняється від прапорця "
        "(checkbox)? Наведіть приклад кожного.",
        "Для чого використовуються кнопки «ОК», «Скасувати» та "
        "«Застосувати»? Чим вони відрізняються?",
        "Що таке модальне діалогове вікно? Наведіть приклад.",
        "Як закрити діалогове вікно без збереження змін? Назвіть "
        "два способи.",
        "Чому діалогові вікна часто не можна змінити в розмірі?",
        "Які типові помилки найчастіше припускаються користувачі "
        "під час роботи з діалоговими вікнами?",
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
        "Заповнена порівняльна таблиця «Типи вікон».",
        "Заповнена таблиця дослідження двох діалогових вікон.",
        "Схема власного діалогового вікна «Мій щоденник» із "
        "переліком елементів.",
        "Відповіді на теоретичні питання (письмово, стисло).",
        "Висновок: що нового дізналися, які елементи діалогових "
        "вікон тепер розпізнаєте одразу.",
        "Список використаних джерел (оформлений за ДСТУ 8302:2015).",
    ]
    for s in structure:
        numbered(doc, s)

    body(doc, "Технічні параметри оформлення: шрифт Times New Roman, "
              "14 pt, міжрядковий інтервал 1,15, поля 2 см, абзацний "
              "відступ 1,25 см, вирівнювання за шириною. Обсяг "
              "звіту — 4–6 сторінок без урахування титульної "
              "сторінки та додатків. Ім'я файлу: "
              "«СР_Діалогові_вікна_ПІБ.docx».")

    # =====================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =====================================================
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Критерій", "Бали"],
        [
            ["Повнота й коректність заповнення таблиці «Типи вікон»",
             "2"],
            ["Якість дослідження двох діалогових вікон", "3"],
            ["Повнота схеми власного діалогового вікна", "3"],
            ["Відповіді на теоретичні питання", "2"],
            ["Обґрунтованість висновку", "1"],
            ["Оформлення звіту згідно з рекомендаціями", "1"],
            ["Творчий підхід, оригінальні елементи схеми", "1"],
        ],
        widths=[12.5, 4.0],
    )

    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (потребує доопрацювання).")

    doc.save("Самостійна_робота_Діалогові_вікна.docx")
    print("Готово: Самостійна_робота_Діалогові_вікна.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()