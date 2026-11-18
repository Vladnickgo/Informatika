#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лекція N. Системи управління електронними документами.
Технічні засоби обробки документів та інформації.
Класифікація офісної техніки.

Генерує:
  - Лекція_СЕД_офісна_техніка.docx
  - output/scheme_*.png (+ .svg) — 4 схеми у стилі Apple
"""

import os
import re

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

# ============================================================
# НАЛАШТУВАННЯ
# ============================================================
LECTURE_NUMBER = 1
OUTPUT_DIR = "output"
OUTPUT_DOCX = "Лекція_СЕД_офісна_техніка.docx"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Кольори Apple-стилю
C_BG      = "#F5F5F7"
C_EDGE    = "#E5E5EA"
C_TEXT    = "#1D1D1F"
C_GRAY    = "#86868B"
C_BLUE    = "#0071E3"
C_GREEN   = "#248A3D"
C_ORANGE  = "#C93400"
C_RED     = "#C4001D"
C_PURPLE  = "#6E30A8"

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


# ============================================================
# СХЕМИ
# ============================================================
def _wrap(text, width=20):
    if len(text) <= width:
        return text
    words = text.split()
    lines, line = [], ""
    for w in words:
        if len(line) + len(w) + (1 if line else 0) <= width:
            line = (line + " " + w).strip()
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return "\n".join(lines)


def draw_card(ax, cx, cy, w, h, text, bg=C_BG, edge=C_EDGE,
              text_color=C_TEXT, fontsize=13, bold=False, wrap_width=20):
    x, y = cx - w / 2, cy - h / 2
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.18",
        linewidth=1.4, edgecolor=edge, facecolor=bg,
    )
    ax.add_patch(box)
    ax.text(cx, cy, _wrap(text, wrap_width), ha="center", va="center",
            fontsize=fontsize, color=text_color,
            fontweight="bold" if bold else "normal", linespacing=1.3)


def draw_arrow(ax, x1, y1, x2, y2, color=C_GRAY):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4,
                                mutation_scale=14, shrinkA=0, shrinkB=0))


def _save(fig, name):
    fig.savefig(os.path.join(OUTPUT_DIR, f"{name}.png"),
                dpi=220, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(os.path.join(OUTPUT_DIR, f"{name}.svg"),
                bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


# --- Схема 1: Ринок DCT ---
def scheme_dct_market():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(5, 5.75,
            "Структура ринку DCT (Document and Content Technologies)",
            ha="center", va="center", fontsize=13, color=C_GRAY, fontweight="bold")

    draw_card(ax, 5, 4.55, 5.8, 1.0, "Програмне забезпечення DCT",
              bg="#EBF4FF", edge=C_BLUE, fontsize=14.5, bold=True, wrap_width=40)

    cards = [
        (1.7, "Системи електронного документообігу (СЕД)", "#EBF4FF", C_BLUE),
        (5.0, "Системи управління інформацією (IMS, портали)", "#E8F5EC", C_GREEN),
        (8.3, "Системи управління вмістом (CMS)", "#FFF4E5", C_ORANGE),
    ]
    for x, txt, bg, ed in cards:
        draw_card(ax, x, 2.0, 2.9, 2.2, txt, bg=bg, edge=ed,
                  fontsize=12.5, wrap_width=22)
        draw_arrow(ax, 5, 4.05, x, 3.1)

    _save(fig, "scheme_dct_market")


# --- Схема 2: Класифікація СЕД ---
def scheme_sed_classification():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(6, 5.75, "Класифікація систем електронного документообігу",
            ha="center", va="center", fontsize=13, color=C_GRAY, fontweight="bold")

    draw_card(ax, 6, 4.55, 2.4, 1.0, "СЕД",
              bg="#EBF4FF", edge=C_BLUE, fontsize=15, bold=True)

    titles = [
        "Бізнес-процеси",
        "Корпоративні СЕД",
        "Управління зображеннями",
        "Потоки робіт",
        "Управління виведенням",
    ]
    accents = [C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_RED]
    bgs = ["#EBF4FF", "#E8F5EC", "#FFF4E5", "#F2EBFA", "#FDE9EC"]

    xs = [1.1, 3.55, 6.0, 8.45, 10.9]
    for x, title, ac, bg in zip(xs, titles, accents, bgs):
        draw_card(ax, x, 2.05, 2.1, 2.4, title, bg=bg, edge=ac,
                  fontsize=11.5, wrap_width=13)
        draw_arrow(ax, 6, 4.05, x, 3.25)

    _save(fig, "scheme_sed_classification")


# --- Схема 3: Засоби обробки та зберігання ---
def scheme_processing_tools():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(5, 5.75, "Засоби обробки та зберігання документів",
            ha="center", va="center", fontsize=13, color=C_GRAY, fontweight="bold")

    draw_card(ax, 5, 4.65, 6.4, 0.95, "Засоби обробки та зберігання документів",
              bg="#EBF4FF", edge=C_BLUE, fontsize=13.5, bold=True, wrap_width=45)

    items = [
        ("Носії інформації", "папір, плівка, магнітні диски", C_BLUE, "#EBF4FF"),
        ("Ручні та друкарські засоби", "ручки, машинки, диктофони", C_GREEN, "#E8F5EC"),
        ("Комп'ютерна техніка", "ПК, принтери, сканери, МФУ", C_ORANGE, "#FFF4E5"),
        ("Офісне обладнання", "лотки, картотеки, шредери", C_PURPLE, "#F2EBFA"),
    ]
    xs = [1.25, 3.75, 6.25, 8.75]
    for x, (title, sub, ac, bg) in zip(xs, items):
        w, h, cy = 2.15, 2.3, 2.0
        box = FancyBboxPatch((x - w / 2, cy - h / 2), w, h,
                             boxstyle="round,pad=0,rounding_size=0.18",
                             linewidth=1.4, edgecolor=ac, facecolor=bg)
        ax.add_patch(box)
        ax.text(x, cy + 0.55, _wrap(title, 15), ha="center", va="center",
                fontsize=12, color=C_TEXT, fontweight="bold", linespacing=1.3)
        ax.text(x, cy - 0.55, _wrap(sub, 16), ha="center", va="center",
                fontsize=10, color=C_GRAY, linespacing=1.3)
        draw_arrow(ax, 5, 4.15, x, 3.15)

    _save(fig, "scheme_processing_tools")


# --- Схема 4: Класифікація офісної техніки ---
def scheme_office_tech():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(6, 5.75, "Класифікація офісної техніки",
            ha="center", va="center", fontsize=13, color=C_GRAY, fontweight="bold")

    draw_card(ax, 6, 4.55, 3.4, 1.0, "Офісна техніка",
              bg="#EBF4FF", edge=C_BLUE, fontsize=15, bold=True)

    titles = [
        "Складання документів",
        "Копіювання і розмножування",
        "Зберігання і транспортування",
        "Адміністративний зв'язок",
        "Репрографія та оздоблення",
    ]
    accents = [C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_RED]
    bgs = ["#EBF4FF", "#E8F5EC", "#FFF4E5", "#F2EBFA", "#FDE9EC"]

    xs = [1.1, 3.55, 6.0, 8.45, 10.9]
    for x, title, ac, bg in zip(xs, titles, accents, bgs):
        draw_card(ax, x, 2.05, 2.1, 2.4, title, bg=bg, edge=ac,
                  fontsize=11, wrap_width=13)
        draw_arrow(ax, 6, 4.05, x, 3.25)

    _save(fig, "scheme_office_tech")


# ============================================================
# ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ============================================================
def _insert_tcpr_element(tcPr, element, before_tags):
    for before in before_tags:
        existing = tcPr.find(qn(f"w:{before}"))
        if existing is not None:
            existing.addprevious(element)
            return
    tcPr.append(element)


def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    old = tcPr.find(qn("w:shd"))
    if old is not None:
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    _insert_tcpr_element(tcPr, shd,
                         ["noWrap", "tcMar", "textDirection",
                          "tcFitText", "vAlign", "hideMark"])


def set_cell_border(cell, side, color, sz=28):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        _insert_tcpr_element(tcPr, tcBorders,
                             ["shd", "noWrap", "tcMar", "textDirection",
                              "tcFitText", "vAlign", "hideMark"])
    el = tcBorders.find(qn(f"w:{side}"))
    if el is None:
        el = OxmlElement(f"w:{side}")
        tcBorders.append(el)
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:color"), color)


def set_cell_border_nil(cell, side):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        _insert_tcpr_element(tcPr, tcBorders,
                             ["shd", "noWrap", "tcMar", "textDirection",
                              "tcFitText", "vAlign", "hideMark"])
    el = tcBorders.find(qn(f"w:{side}"))
    if el is None:
        el = OxmlElement(f"w:{side}")
        tcBorders.append(el)
    el.set(qn("w:val"), "nil")


def repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    f1 = OxmlElement("w:fldChar")
    f1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    f2 = OxmlElement("w:fldChar")
    f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1)
    run._r.append(instr)
    run._r.append(f2)


def _style_run(run, *, name="Times New Roman", size=14, bold=False,
               italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def _add_runs_rich(p, text, size=14):
    """Підтримує **жирний** і `mono`."""
    tokens = re.split(r"(\*\*.*?\*\*|`[^`]*`)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            run = p.add_run(tok[2:-2])
            _style_run(run, size=size, bold=True,
                       color=RGBColor(0x1D, 0x1D, 0x1F))
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            run = p.add_run(tok[1:-1])
            _style_run(run, name="Consolas", size=size - 1,
                       color=RGBColor(0xC0, 0x39, 0x2B))
        else:
            run = p.add_run(tok)
            _style_run(run, size=size, color=RGBColor(0x1D, 0x1D, 0x1F))


def add_h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text.upper())
    _style_run(run, size=14, bold=True,
               color=RGBColor(0x1F, 0x4E, 0x79))
    return p


def add_h2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    _style_run(run, size=14, bold=True,
               color=RGBColor(0x2E, 0x75, 0xB6))
    return p


def add_topic(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(f"Тема: {text}")
    _style_run(run, size=14, bold=True,
               color=RGBColor(0x1F, 0x4E, 0x79))
    return p


def add_para(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(5)
    _add_runs_rich(p, text, size=14)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        _add_runs_rich(p, item, size=14)


def add_numbered_manual(doc, items, start=1):
    for i, item in enumerate(items, start=start):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(f"{i}. ")
        _style_run(run, size=14)
        _add_runs_rich(p, item, size=14)


def numbered_paren(doc, items):
    for i, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(f"{i}) ")
        _style_run(run, size=14)
        _add_runs_rich(p, item, size=14)


def add_literature(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        _add_runs_rich(p, item, size=14)


def add_callout(doc, text, bg="FFF4E5", border="C93400"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    set_cell_bg(cell, bg)
    set_cell_border(cell, "left", border, sz=28)
    for side in ("top", "bottom", "right"):
        set_cell_border_nil(cell, side)
    cell.width = Cm(16.5)
    table.columns[0].width = Cm(16.5)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    _add_runs_rich(p, text, size=13)

    doc.add_paragraph()


def add_image(doc, path, width_cm=16.0):
    doc.add_picture(path, width=Cm(width_cm))
    p = doc.paragraphs[-1]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)


def add_table(doc, headers, rows, widths_cm):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr_row = table.rows[0]
    repeat_table_header(hdr_row)
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        set_cell_bg(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(h)
        _style_run(run, size=13, bold=True,
                   color=RGBColor(0xFF, 0xFF, 0xFF))

    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            _add_runs_rich(p, val, size=12)

    for i, w in enumerate(widths_cm):
        table.columns[i].width = Cm(w)
        for cell in table.columns[i].cells:
            cell.width = Cm(w)

    doc.add_paragraph()
    return table


# ============================================================
# ДОКУМЕНТ
# ============================================================
def build_document():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(14)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    footer_p = doc.sections[0].footer.paragraphs[0]
    add_page_number(footer_p)

    # ---- ТИТУЛЬНА ЧАСТИНА ----
    add_h1(doc, f"ЛЕКЦІЯ {LECTURE_NUMBER}. Системи управління електронними документами")
    add_topic(doc, "Системи управління електронними документами. "
                   "Технічні засоби обробки документів та інформації. "
                   "Класифікація офісної техніки")

    # ---- МЕТА ----
    add_h2(doc, "Мета")
    add_para(doc, "**Навчальна:** розглянути системи управління електронними "
                  "документами; познайомитися з технічними засобами обробки "
                  "документів та інформації; вивчити класифікацію офісної техніки.")
    add_para(doc, "**Розвивальна:** розвивати логічне мислення, пам'ять; "
                  "формувати вміння узагальнювати матеріал.")
    add_para(doc, "**Виховна:** виховувати інформаційну культуру, бережливе "
                  "ставлення до обладнання комп'ютерного кабінету, уміння "
                  "працювати в групі; формувати позитивне ставлення до навчання.")

    # ---- ОБЛАДНАННЯ ----
    add_h2(doc, "Обладнання та наочність")
    numbered_paren(doc, [
        "Дошка.",
        "Комп'ютери з підключенням до мережі Інтернет.",
        "Роздаткові картки.",
        "Навчальна презентація.",
        "Браузер, офісні програми.",
    ])

    # ---- КЛЮЧОВІ ПОНЯТТЯ ----
    add_h2(doc, "Ключові поняття")
    add_para(doc, "Документообіг, система електронного документообігу (СЕД), EDM, "
                  "DCT, IMS, CMS, електронний документ, електронний підпис, "
                  "маршрутизація документів, офісна техніка, сканер, шредер, "
                  "ламінатор, репрографія, безпаперове діловодство.")

    # ---- ПЛАН ----
    add_h2(doc, "План лекції")
    add_numbered_manual(doc, [
        "Поняття системи електронного документообігу та її місце на ринку DCT.",
        "Основні принципи організації та функції СЕД.",
        "Класифікація СЕД і провідні системи на ринку України.",
        "Засоби обробки та зберігання документів.",
        "Технічні засоби обробки документів та інформації.",
        "Класифікація офісної техніки.",
    ])

    # ============ БЛОК 1 ============
    add_h2(doc, "1. Поняття СЕД та її місце на ринку DCT")
    add_para(doc, "**Документообіг** — це безперервний рух документів в організації "
                  "від моменту їх створення або одержання до завершення виконання "
                  "або відправлення. У паперовому світі документ долає безліч "
                  "кабінетів, полиць і папок, а кожен крок фіксується вручну. "
                  "Це нагадує гру в «зламаний телефон»: поки записка дійде до "
                  "адресата, вона може загубитися або змінитися.")
    add_para(doc, "**Система електронного документообігу (СЕД, Electronic Document "
                  "Management System, EDM)** — це програмне забезпечення, яке "
                  "автоматизує створення, зберігання, обробку, пошук і передачу "
                  "електронних документів між співробітниками організації.")
    add_para(doc, "Уявіть шкільний електронний щоденник: замість паперового "
                  "журналу, який може загубитися, кожен учень, батько та вчитель "
                  "бачить оцінки й зауваження у реальному часі. Так само СЕД "
                  "упорядковує документи в установі — від наказу про прийом на "
                  "роботу до фінансового звіту.")
    add_para(doc, "Потреба в ефективному управлінні електронними документами "
                  "привела до формування **ринку DCT** (Document and Content "
                  "Technologies) — технологій роботи з документами та вмістом. "
                  "СЕД є частиною цього ринку поряд із **IMS** (Information "
                  "Management Systems — портали для агрегації інформації) та "
                  "**CMS** (Content Management Systems — системи управління "
                  "вмістом на рівні об'єктів).")
    add_image(doc, os.path.join(OUTPUT_DIR, "scheme_dct_market.png"), 16.0)
    add_callout(doc, "Електронний документ набуває юридичної сили лише за "
                     "наявності кваліфікованого електронного підпису (КЕП), "
                     "який прирівнюється до власноручного підпису та печатки.")

    # ============ БЛОК 2 ============
    add_h2(doc, "2. Основні принципи організації та функції СЕД")
    add_para(doc, "Щоб система працювала ефективно, вона будується на кількох "
                  "базових принципах. Кожен із них породжує відповідну функцію.")
    add_bullets(doc, [
        "**Одноразова реєстрація документа** — документ вноситься в систему "
        "один раз і далі рухається без дублювання.",
        "**Паралельне виконання операцій** — кілька фахівців можуть "
        "опрацьовувати один документ одночасно, що скорочує час його руху.",
        "**Безперервність руху документа** — жодних «зупинок» на столах; "
        "система контролює кожен крок.",
        "**Єдина база документної інформації** — централізоване зберігання "
        "та виключення дублювання.",
        "**Ефективний пошук документа** — пошук за реквізитами, текстом, датою.",
        "**Розвинена система звітності** — контроль руху документа в процесі "
        "документообігу.",
    ])
    add_para(doc, "На цих принципах базуються основні функції СЕД — від "
                  "централізованого управління документами до інтеграції з "
                  "бухгалтерськими та виробничими системами.")
    add_table(doc,
        ["Принцип організації", "Відповідна функція СЕД"],
        [
            ["Одноразова реєстрація", "Централізоване управління документами, єдина база"],
            ["Паралельне виконання", "Колективна робота над документами"],
            ["Безперервність руху", "Підтримка життєвого циклу документа"],
            ["Єдина база", "Управління доступом, розмежування повноважень"],
            ["Ефективний пошук", "Швидкий пошук за реквізитами та вмістом"],
            ["Розвинена звітність", "Маршрутизація документів, контроль виконання"],
        ],
        [6.0, 10.0])
    add_callout(doc, "Принцип одноразової реєстрації означає, що кожен документ "
                     "має унікальний ідентифікатор, за яким його можна знайти "
                     "в системі. Це виключає появу «двійників» та полегшує аудит.")

    # ============ БЛОК 3 ============
    add_h2(doc, "3. Класифікація СЕД і провідні системи на ринку України")
    add_para(doc, "Системи електронного документообігу різняться за призначенням "
                  "і функціональністю. Залежно від кола завдань виділяють кілька "
                  "класів.")
    add_image(doc, os.path.join(OUTPUT_DIR, "scheme_sed_classification.png"), 16.0)
    add_para(doc, "**СЕД, орієнтовані на бізнес-процеси** — «важкі» системи, що "
                  "автоматизують складні маршрути та документопотоки великих "
                  "підприємств. **Корпоративні СЕД** охоплюють усі підрозділи "
                  "організації й підтримують єдині корпоративні стандарти. "
                  "**Системи управління зображеннями** працюють зі сканованими "
                  "копіями паперових документів. **Системи управління потоками "
                  "робіт (workflow)** формалізують типові процедури й автоматично "
                  "передають завдання між виконавцями. **Системи управління "
                  "виведенням** відповідають за формування, зберігання і доставку "
                  "вихідних документів.")
    add_para(doc, "На ринку України найбільш відомі такі системи:")
    add_table(doc,
        ["Система", "Розробник", "Основне призначення"],
        [
            ["Documentum", "Documentum Inc.",
             "Управління документами, знаннями і бізнес-процесами на великих "
             "підприємствах; платформа для розподілених архівів"],
            ["LanDocs", "Компанія «Ланіт»",
             "Діловодство й архівне зберігання документів; архітектура "
             "«клієнт/сервер» на Oracle або MS SQL Server"],
            ["Docs Fusion / Docs Open", "Hummingbird",
             "Електронні архіви для інтенсивного створення й редагування "
             "документів"],
            ["Optima Workflow", "Optima",
             "Формалізація типових процедур роботи з документами (потоків робіт)"],
        ],
        [3.5, 3.5, 9.5])
    add_callout(doc, "Вибір СЕД для організації визначається обсягом "
                     "документопотоку, кількістю користувачів, галузевими "
                     "вимогами та бюджетом. Універсальної «найкращої» системи "
                     "не існує — є оптимальна для конкретних умов.")

    # ============ БЛОК 4 ============
    add_h2(doc, "4. Засоби обробки та зберігання документів")
    add_para(doc, "Робота з великими масивами документованої інформації вимагає "
                  "різноманітних технічних засобів. Вони забезпечують створення, "
                  "збереження, передачу та використання документів.")
    add_para(doc, "До **носіїв інформації** належать папір, термопапір, "
                  "діазопапір, фотоплівка, калька, мікроносії, звуконосії, "
                  "відеоносії, магнітні диски, перфоносії. До **засобів "
                  "опрацювання** — ручки, олівці, друкарські машинки, диктофони, "
                  "принтери, графопобудовувачі, спеціалізовані програмні продукти.")
    add_para(doc, "Окрему групу становить **офісне обладнання**: фальцювальні, "
                  "бігувальні, перфоруючі та ріжучі машини (фольдери), "
                  "листовідбірні й сортувальні пристрої, скріплююче та склеююче "
                  "обладнання, брошурувальні машини, конвертовідкривачі, "
                  "ламінатори, адресувальні, штемпелювальні й франкірувальні "
                  "машини, шредери.")
    add_image(doc, os.path.join(OUTPUT_DIR, "scheme_processing_tools.png"), 16.0)
    add_table(doc,
        ["Група засобів", "Призначення", "Приклади"],
        [
            ["Носії інформації", "Фіксація та збереження відомостей",
             "Папір, плівка, магнітні диски"],
            ["Ручні та друкарські", "Створення тексту від руки чи друком",
             "Ручки, машинки, диктофони"],
            ["Комп'ютерна техніка", "Підготовка й опрацювання електронних документів",
             "ПК, сканер, принтер, МФУ"],
            ["Офісне обладнання", "Допоміжні операції з документами",
             "Фольдер, ламінатор, шредер"],
        ],
        [3.5, 6.0, 6.5])

    # ============ БЛОК 5 ============
    add_h2(doc, "5. Технічні засоби обробки документів та інформації")
    add_para(doc, "Сучасне діловодство все частіше спирається на **комп'ютерну "
                  "техніку**. Текстові та табличні процесори, комунікаційні "
                  "програми, планувальники об'єднуються в офісні пакети "
                  "(наприклад, `Microsoft Office`, `LibreOffice`) і полегшують "
                  "рутинну паперову роботу.")
    add_para(doc, "Для переведення паперових документів в електронну форму "
                  "використовують **сканери** та **МФУ**. Для оперативного "
                  "збереження документів на робочому місці — лотки, касети, "
                  "настільні картотеки, поворотні лотки на 2–4 полиці "
                  "(місткість 600–1200 аркушів А4), коробки з пластмаси, тумби "
                  "з вертикальним збереженням папок.")
    add_para(doc, "Для довгострокового зберігання магнітних матеріалів "
                  "(стрічок, дисків) створюють спеціальні служби, що ведуть "
                  "облік, зберігають машинограми, організовують пошукові системи "
                  "та видають документи користувачам.")
    add_callout(doc, "Сучасна тенденція — перехід до **безпаперового "
                     "діловодства**. Проте повна відмова від паперу поки "
                     "неможлива: значна частина документів має юридичні вимоги "
                     "до паперової форми або архівного зберігання.")

    # ============ БЛОК 6 ============
    add_h2(doc, "6. Класифікація офісної техніки")
    add_para(doc, "Офісна техніка — це сукупність технічних засобів, що "
                  "забезпечують діловодні, управлінські та інші операції в "
                  "установі. До її складу входять персональний комп'ютер із "
                  "периферією (принтер, сканер, колонки, модем, засоби "
                  "мультимедіа), телефонний і радіотелефонний апарати, міні-АТС, "
                  "переговорні пристрої, копіювальні апарати, проєкційна техніка.")
    add_para(doc, "За призначенням технічні засоби інформаційної діяльності "
                  "поділяють на кілька груп, які зручно подати у вигляді схеми.")
    add_image(doc, os.path.join(OUTPUT_DIR, "scheme_office_tech.png"), 16.0)
    add_para(doc, "Окремо виділяють **системи передавання даних**:")
    add_bullets(doc, [
        "**Недокументованих:** телефонний, радіопошуковий, радіотелеграфний, "
        "відеотелефонний зв'язок.",
        "**Документованих:** телеграфний, дейтофонний, факсимільний зв'язок.",
    ])
    add_table(doc,
        ["Клас офісної техніки", "Приклади пристроїв"],
        [
            ["Складання і виготовлення документів",
             "ПК, друкарська машинка, диктофон, принтер"],
            ["Копіювання і розмножування",
             "Копір, дуплікатор, цифровий друкарський апарат"],
            ["Зберігання і транспортування",
             "Лотки, касети, картотеки, коробки, шафи"],
            ["Адміністративний зв'язок",
             "Телефон, міні-АТС, переговорні пристрої"],
            ["Репрографія та оздоблення",
             "Сканер, ламінатор, брошурувальна машина, шредер"],
        ],
        [7.0, 9.0])

    # ---- КОНТРОЛЬНІ ПИТАННЯ ----
    add_h2(doc, "Контрольні питання")
    add_numbered_manual(doc, [
        "Що таке система електронного документообігу?",
        "Яке місце займають СЕД на ринку DCT?",
        "Назвіть основні принципи організації електронного документообігу.",
        "Які функції виконують системи електронного документообігу?",
        "Як класифікують СЕД?",
        "Які провідні СЕД представлені на ринку України?",
        "Чим корпоративні СЕД відрізняються від СЕД, орієнтованих на "
        "бізнес-процеси?",
        "Які засоби обробки та зберігання документів ви знаєте?",
        "Які технічні засоби використовують для обробки документів та інформації?",
        "Наведіть класифікацію офісної техніки.",
        "Які системи передавання документованих і недокументованих даних ви знаєте?",
        "Які переваги має безпаперове діловодство?",
    ])

    # ---- ЛІТЕРАТУРА ----
    add_h2(doc, "Рекомендовані джерела")
    add_literature(doc, [
        "Матвієнко О. В., Цивін М. Н. Основи організації електронного "
        "документообігу. Київ : ЦУЛ, 2017.",
        "Клименко О. Ф. Інформаційні системи і технології в обліку. "
        "Київ : КНЕУ, 2018.",
        "Зацеркляний М. М., Мельников О. В. Основи комп'ютерних технологій "
        "для економістів. Київ : ВД «Професіонал», 2019.",
    ])

    return doc


# ============================================================
# MAIN
# ============================================================
def main():
    print("→ Генерація схем...")
    scheme_dct_market()
    scheme_sed_classification()
    scheme_processing_tools()
    scheme_office_tech()
    print(f"  ✔ схеми збережено у {OUTPUT_DIR}/ (png + svg)")

    print("→ Побудова docx-документа...")
    doc = build_document()
    doc.save(OUTPUT_DOCX)
    print(f"✔ Готово: {OUTPUT_DOCX}")
    print(f"📁 Схеми: {OUTPUT_DIR}/*.png, {OUTPUT_DIR}/*.svg")


if __name__ == "__main__":
    main()