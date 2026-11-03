# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ЛЕКЦІЯ
Тема: Основи графічного інтерфейсу користувача (GUI)
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
# СХЕМА 1. CLI vs GUI
# ============================================================

def scheme_cli_vs_gui():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.35, "Текстовий інтерфейс (CLI) та графічний (GUI)",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # ---------- CLI панель ----------
    px, py, pw, ph = 0.4, 2.0, 6.0, 4.7
    ax.add_patch(FancyBboxPatch((px, py), pw, ph,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#1C1C1E", edgecolor="#3A3A3C",
                                linewidth=1.6))
    ax.text(px + pw / 2, py + ph - 0.4, "CLI — командний рядок",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="white")

    cli_lines = [
        ("C:\\Users\\Student>", "dir", "#30D158", "white"),
        ("", " Документи",     None,     "#D1D1D6"),
        ("", " Завантаження",  None,     "#D1D1D6"),
        ("", " звіт.docx",     None,     "#D1D1D6"),
        ("C:\\Users\\Student>", "copy звіт.docx D:\\Архів", "#30D158", "white"),
        ("", " 1 файл скопійовано.", None, "#D1D1D6"),
    ]
    yy = py + ph - 1.1
    for prompt, cmd, pc, cc in cli_lines:
        if prompt:
            ax.text(px + 0.25, yy, prompt, ha="left", va="center",
                    fontsize=9.5, color=pc, family="monospace",
                    fontweight="bold")
            ax.text(px + 2.4, yy, cmd, ha="left", va="center",
                    fontsize=9.5, color=cc, family="monospace")
        else:
            ax.text(px + 0.25, yy, cmd, ha="left", va="center",
                    fontsize=9.5, color=cc, family="monospace")
        yy -= 0.42

    ax.text(px + pw / 2, py + 0.4, "Клавіатура · тексти · команди",
            ha="center", va="center", fontsize=10.5, style="italic",
            color="#A1A1A6")

    # ---------- GUI панель ----------
    gx = 6.65
    ax.add_patch(FancyBboxPatch((gx, py), pw, ph,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#FFFFFF", edgecolor="#404040",
                                linewidth=1.6))
    ax.add_patch(Rectangle((gx, py + ph - 0.55), pw, 0.55,
                           facecolor="#1F4E79"))
    ax.text(gx + pw / 2, py + ph - 0.28, "GUI — робочий стіл",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="white")

    # Іконки-плитки на «робочому столі»
    icons = [
        ("📁", "Документи", ACCENT_BLUE),
        ("📁", "Завантаження", ACCENT_GREEN),
        ("📄", "звіт.docx", ACCENT_ORANGE),
        ("🖼", "фото.png", ACCENT_PURPLE),
    ]
    tile_w, tile_h = 2.4, 1.4
    gap_x, gap_y = 0.35, 0.35
    start_x = gx + 0.35
    start_y = py + ph - 2.15

    for i, (icon, label, color) in enumerate(icons):
        col, row = i % 2, i // 2
        tx = start_x + col * (tile_w + gap_x)
        ty = start_y - row * (tile_h + gap_y)
        _card(ax, tx, ty, tile_w, tile_h, fill="#F5F5F7",
              border=color, radius=0.14)
        ax.text(tx + tile_w / 2, ty + tile_h - 0.4, icon,
                ha="center", va="center", fontsize=18)
        ax.text(tx + tile_w / 2, ty + 0.35, label,
                ha="center", va="center", fontsize=10,
                color=TEXT_DARK)

    ax.text(gx + pw / 2, py + 0.4,
            "Миша · значки · меню · вікна",
            ha="center", va="center", fontsize=10.5, style="italic",
            color=TEXT_GRAY)

    return _save(fig, "scheme_cli_vs_gui")


# ============================================================
# СХЕМА 2. WIMP
# ============================================================

def scheme_wimp():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.35, "WIMP: чотири опори графічного інтерфейсу",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    items = [
        ("W", "Windows", "Вікна",
         "Прямокутні області,\nу яких відкрито програми\nчи документи",
         ACCENT_BLUE, "#E1F0FE"),
        ("I", "Icons", "Значки (піктограми)",
         "Маленькі зображення,\nщо позначають об'єкти:\nфайли, папки, програми",
         ACCENT_GREEN, "#E8F8EC"),
        ("M", "Menus", "Меню",
         "Списки команд, з яких\nкористувач обирає\nпотрібну дію",
         ACCENT_ORANGE, "#FFF4E5"),
        ("P", "Pointers", "Вказівники",
         "Курсор миші, що вказує\nна об'єкти та запускає дії\nклацанням",
         ACCENT_PURPLE, "#EFE6F7"),
    ]

    card_w, card_h = 2.95, 5.6
    gap = 0.2
    x0 = (13 - (4 * card_w + 3 * gap)) / 2
    y0 = 1.0

    for i, (letter, eng, ukr, desc, color, fill) in enumerate(items):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h, fill=fill, border=color, radius=0.18)
        _badge(ax, cx, y0 + card_h - 0.7, 1.1, 1.1, color, letter,
               color="white", size=22, radius=0.28)
        ax.text(cx, y0 + card_h - 1.75, eng, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=color)
        ax.text(cx, y0 + card_h - 2.15, ukr, ha="center", va="center",
                fontsize=11, style="italic", color=TEXT_DARK)
        ax.text(cx, y0 + 1.6, desc, ha="center", va="center",
                fontsize=10.5, color=TEXT_DARK, linespacing=1.7)

    return _save(fig, "scheme_wimp")


# ============================================================
# СХЕМА 3. Принципи GUI
# ============================================================

def scheme_principles():
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.5, 8.05, "Ключові принципи графічного інтерфейсу",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    principles = [
        ("Наочність",
         "Об'єкти видно одразу,\nдію можна передбачити",
         ACCENT_BLUE, "#E1F0FE"),
        ("Послідовність",
         "Однакові дії виконуються\nоднаково в усіх програмах",
         ACCENT_GREEN, "#E8F8EC"),
        ("Зворотний зв'язок",
         "Система показує результат\nкожної дії користувача",
         ACCENT_ORANGE, "#FFF4E5"),
        ("Толерантність до помилок",
         "Хибну дію можна скасувати\n(Ctrl + Z) або виправити",
         ACCENT_RED, "#FFEBEA"),
        ("Простота",
         "Мінімум дій для типової\nоперації",
         ACCENT_PURPLE, "#EFE6F7"),
        ("Естетика",
         "Охайне оформлення\nне відволікає від роботи",
         ACCENT_BLUE, "#E1F0FE"),
    ]

    card_w, card_h = 3.9, 2.55
    gap_x, gap_y = 0.25, 0.3
    x0 = 0.4
    y_top = 7.6

    for i, (title, desc, color, fill) in enumerate(principles):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.18)
        ax.text(cx, y + card_h - 0.45, title, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=color)
        ax.text(cx, y + 0.9, desc, ha="center", va="center",
                fontsize=11, color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_principles")


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
    img1 = scheme_cli_vs_gui()
    img2 = scheme_wimp()
    img3 = scheme_principles()

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

    h1(doc, "Лекція")
    theme_line(doc, "Основи графічного інтерфейсу користувача (GUI). "
                    "Визначення та основні принципи GUI")

    h2(doc, "Мета")
    body(doc, "визначити поняття графічного інтерфейсу, його ключові "
              "принципи (WIMP — вікна, піктограми, меню, вказівник); "
              "розвивати аналітичне мислення через порівняння "
              "текстового та графічного способів взаємодії з ОС; "
              "виховувати естетичне сприйняття інформаційних технологій "
              "і розуміння важливості юзабіліті.")

    h2(doc, "Обладнання")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Проєктор або великий екран для демонстрації схем.",
        "Інструкційні картки (для нотаток студентів).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Ключові поняття")
    body(doc, "графічний інтерфейс користувача (GUI), WIMP, вікно, "
              "піктограма, меню, вказівник, курсор, робочий стіл, "
              "текстовий інтерфейс (CLI), юзабіліті, "
              "людино-орієнтований дизайн.")

    h2(doc, "План лекції")
    plan = [
        "Поняття графічного інтерфейсу користувача.",
        "Коротка історія: від CLI до GUI.",
        "Ключова концепція WIMP: вікна, піктограми, меню, вказівник.",
        "Основні принципи ефективного GUI.",
        "Юзабіліті та людино-орієнтований дизайн.",
        "Значення GUI для вчителя початкової школи.",
    ]
    for item in plan:
        numbered(doc, item)

    # =====================================================
    # БЛОК 1. Поняття GUI
    # =====================================================
    h2(doc, "1. Поняття графічного інтерфейсу користувача")

    body(doc, "Інтерфейс користувача — це спосіб, у який людина "
              "взаємодіє з комп'ютером: віддає команди, отримує "
              "результати й бачить реакцію системи. Інтерфейс може бути "
              "текстовим (командний рядок) або графічним.")

    body(doc, "Графічний інтерфейс користувача (GUI, Graphical User "
              "Interface) — це спосіб взаємодії з комп'ютером, у якому "
              "об'єкти файлової системи та команди подано у вигляді "
              "зображень (піктограм, вікон, кнопок, меню), а керування "
              "виконується за допомогою миші, клавіатури або дотику, "
              "без потреби пам'ятати текстові команди.")

    add_figure(doc, img1, 16.0)

    body(doc, "Порівняймо два способи. У CLI користувач пише команду "
              "й отримує текстовий результат. У GUI користувач бачить "
              "зображення об'єктів і виконує дії через наочні елементи. "
              "Це принципово інший підхід: замість того, щоб "
              "запам'ятовувати команду, користувач упізнає образ і "
              "обирає дію.")

    body(doc, "Графічний інтерфейс уперше з'явився у 1970-х роках у "
              "дослідженнях Xerox PARC, а масового поширення набув "
              "завдяки комп'ютерам Apple Macintosh (1984) і згодом — "
              "Windows. Саме перехід до графічного інтерфейсу зробив "
              "комп'ютери доступними для мільйонів звичайних "
              "користувачів, а не лише для програмістів.")

    callout(doc,
            "Уявіть, що ви хочете скопіювати файл. У CLI ви пишете: "
            "copy звіт.docx D:\\Архів. У GUI ви бачите значок файлу, "
            "виділяєте його клацанням, натискаєте Ctrl + C, "
            "переходите в іншу папку й натискаєте Ctrl + V. Результат "
            "той самий, але спосіб — наочніший.",
            fill="E1F0FE", accent="0071E3")

    # =====================================================
    # БЛОК 2. WIMP
    # =====================================================
    h2(doc, "2. Ключова концепція WIMP")

    body(doc, "Більшість графічних інтерфейсів побудовані за "
              "концепцією WIMP. Абревіатура розшифровується як "
              "Windows, Icons, Menus, Pointers — вікна, піктограми, "
              "меню, вказівники. Ці чотири елементи утворюють основу "
              "взаємодії користувача з комп'ютером.")

    add_figure(doc, img2, 16.0)

    add_table(
        doc,
        ["Елемент", "Що це", "Приклад у Windows"],
        [
            ["Windows (вікна)",
             "Прямокутні області, у яких відкриваються програми, "
             "документи або діалоги",
             "Вікно «Проводник», вікно браузера, діалог збереження"],
            ["Icons (піктограми)",
             "Невеликі зображення, що позначають об'єкти файлової "
             "системи або програми",
             "Значок папки, документ .docx, ярлик браузера"],
            ["Menus (меню)",
             "Списки команд, об'єднані за тематикою",
             "Головне меню «Пуск», контекстне меню (права кнопка), "
             "рядок меню у програмі"],
            ["Pointers (вказівники)",
             "Курсор миші або дотику, яким користувач указує на "
             "об'єкти та активує їх",
             "Стрілка, рука, пісочний годинник, курсор у вигляді I"],
        ],
        widths=[3.4, 6.5, 6.6],
    )

    body(doc, "Розгляньмо кожен елемент докладніше.")

    h3(doc, "Вікна", color=RGBColor(0x00, 0x71, 0xE3))
    body(doc, "Вікно — це прямокутна область на екрані, у якій "
              "відображається вміст програми або документа. Вікна "
              "можна переміщувати, згортати, розгортати, змінювати "
              "їхній розмір, розташовувати поруч або одне над одним. "
              "Саме можливість відкрити кілька вікон одночасно дала "
              "назву концепції багатозадачності.")

    bullet(doc, "заголовок вікна — показує назву програми й документа;")
    bullet(doc, "кнопки керування — згорнути, розгорнути, закрити;")
    bullet(doc, "рядок меню — команди, згруповані за категоріями;")
    bullet(doc, "робоча область — безпосередньо вміст;")
    bullet(doc, "смуги прокручування — для переміщення вмісту.")

    h3(doc, "Піктограми", color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Піктограма (значок, іконка) — це маленьке зображення, "
              "яке позначає об'єкт. Піктограми допомагають упізнати "
              "об'єкт без читання його назви. Наприклад, значок папки "
              "виглядає як канцелярська папка, значок документа — як "
              "аркуш паперу, значок програми — як логотип цієї "
              "програми.")

    body(doc, "Хороша піктограма відповідає трьом вимогам: "
              "впізнавана (одразу зрозуміло, що вона позначає), "
              "проста (без зайвих деталей) і послідовна (усі піктограми "
              "одного набору витримані в єдиному стилі).")

    h3(doc, "Меню", color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Меню — це список команд, з яких користувач обирає "
              "потрібну. Меню бувають кількох видів: головне меню "
              "«Пуск», рядок меню у програмі (Файл, Редагування, "
              "Вигляд), контекстне меню (з'являється після натискання "
              "правої кнопки миші на об'єкті).")

    body(doc, "Головна перевага меню — команди не треба пам'ятати: "
              "їх видно у списку, і користувач обирає потрібну. "
              "Головний недолік — глибока вкладеність (меню в меню) "
              "ускладнює пошук. Тому сучасні інтерфейси часто "
              "замінюють меню на панелі інструментів або стрічку "
              "(Ribbon).")

    h3(doc, "Вказівники", color=RGBColor(0x6E, 0x30, 0xA8))
    body(doc, "Вказівник — це курсор, яким користувач керує "
              "мишею, тачпадом або пальцем на сенсорному екрані. "
              "Вигляд курсора залежить від контексту: стрілка — "
              "звичайне положення, рука — на гіперпосиланні, "
              "пісочний годинник — система виконує дію, вертикальна "
              "риска — введення тексту.")

    body(doc, "Крім миші, вказівником може бути палець (на планшеті "
              "чи смартфоні), стилус, а в голосових інтерфейсах — "
              "голос. Але концепція залишається: користувач указує "
              "на об'єкт і виконує дію.")

    # =====================================================
    # БЛОК 3. Принципи
    # =====================================================
    h2(doc, "3. Основні принципи ефективного GUI")

    body(doc, "Графічний інтерфейс може бути зручним або "
              "невдалим — залежно від того, чи дотримано базових "
              "принципів. Існує шість принципів, які визначають "
              "якість графічного інтерфейсу.")

    add_figure(doc, img3, 16.0)

    h3(doc, "Наочність", color=RGBColor(0x00, 0x71, 0xE3))
    body(doc, "Кожен об'єкт має бути видимим, а його призначення — "
              "зрозумілим. Користувач не повинен вгадувати, що буде, "
              "якщо натиснути кнопку. Наприклад, кнопка з написом "
              "«Зберегти» і значком дискети одразу показує свою дію.")

    h3(doc, "Послідовність", color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Однакові дії в різних програмах мають виконуватися "
              "однаково. Якщо в одній програмі Ctrl + S зберігає "
              "файл, то й в інших — теж. Якщо кнопка «ОК» розташована "
              "справа, то й у всіх діалогах — справа. Це створює "
              "відчуття передбачуваності.")

    h3(doc, "Зворотний зв'язок", color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Система повинна показувати результат кожної дії. "
              "Коли файл копіюється, з'являється індикатор прогресу. "
              "Коли команда виконана — коротке повідомлення. Коли "
              "виникає помилка — зрозуміле пояснення. Без зворотного "
              "зв'язку користувач почувається наче в темряві.")

    h3(doc, "Толерантність до помилок",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Люди помиляються. Добрий інтерфейс дозволяє виправити "
              "помилку: Ctrl + Z скасовує останню дію, кошик дозволяє "
              "відновити видалений файл, а система попереджає перед "
              "небезпечною дією. Мета — не покарати за помилку, "
              "а допомогти її виправити.")

    h3(doc, "Простота", color=RGBColor(0x6E, 0x30, 0xA8))
    body(doc, "Типова операція виконується за мінімум дій. Якщо "
              "для звичайного збереження документа потрібно п'ять "
              "кліків — інтерфейс поганий. Один клік або гаряча "
              "клавіша — добре. Простота економить час користувача.")

    h3(doc, "Естетика", color=RGBColor(0x00, 0x71, 0xE3))
    body(doc, "Оформлення не повинно відволікати від роботи. "
              "Гармонійні кольори, виразні шрифти, виважене "
              "розташування елементів — усе це створює відчуття "
              "порядку й комфорту. Навпаки, строкаті кольори, "
              "мерехтіння й хаотичні елементи втомлюють очі.")

    callout(doc,
            "У 2012 році Apple представила новий дизайн iOS 7, у "
            "якому відмовилася від об'ємних елементів на користь "
            "плоских. Це викликало суперечки, але згодом стало "
            "стандартом для всієї індустрії. Причина — саме естетика "
            "й простота: плоскі елементи краще читаються на екранах "
            "різних розмірів і не відволікають від змісту.",
            fill="E1F0FE", accent="0071E3")

    # =====================================================
    # БЛОК 4. Юзабіліті
    # =====================================================
    h2(doc, "4. Юзабіліті та людино-орієнтований дизайн")

    body(doc, "Юзабіліті (usability, зручність використання) — це "
              "ступінь, до якого інтерфейс дозволяє користувачеві "
              "досягти своєї мети швидко, легко й без зайвих "
              "зусиль. Високе юзабіліті означає: користувач інтуїтивно "
              "розуміє, що робити, і не витрачає час на боротьбу з "
              "інтерфейсом.")

    body(doc, "Юзабіліті визначають п'ять складників:")
    bullet(doc, "Легкість навчання — наскільки швидко новачок "
                "опановує основні дії;")
    bullet(doc, "Ефективність — скільки часу й кроків займає типова "
                "операція;")
    bullet(doc, "Запам'ятовуваність — наскільки легко повернутися "
                "до інтерфейсу після перерви;")
    bullet(doc, "Стійкість до помилок — наскільки легко помилитися "
                "й наскільки легко виправити;")
    bullet(doc, "Задоволення — наскільки комфортно працювати.")

    body(doc, "Людино-орієнтований дизайн (user-centered design) — "
              "це підхід, у якому інтерфейс проєктують, відштовхуючись "
              "від потреб реальних користувачів. Перед створенням "
              "програми розробники досліджують, як люди виконують "
              "свої задачі, які труднощі відчувають і що їм "
              "допомогло б найбільше. Інтерфейс перевіряють на "
              "реальних користувачах і вдосконалюють за "
              "результатами тестів.")

    add_table(
        doc,
        ["Принцип", "Як виявляється", "Приклад з інтерфейсу Windows"],
        [
            ["Наочність", "Об'єкти видно, дію можна передбачити",
             "Значок папки показує, що всередині — файли"],
            ["Послідовність", "Однакові дії — однаково",
             "Ctrl + C, Ctrl + V у всіх програмах"],
            ["Зворотний зв'язок", "Результат дії видно",
             "Індикатор копіювання файлів"],
            ["Толерантність", "Помилку можна виправити",
             "Кошик, Ctrl + Z, попередження перед видаленням"],
            ["Простота", "Мінімум кроків",
             "Один клік на значок запускає програму"],
            ["Естетика", "Оформлення не заважає",
             "Єдиний стиль вікон і піктограм"],
        ],
        widths=[3.6, 6.0, 6.9],
    )

    # =====================================================
    # БЛОК 5. GUI для вчителя
    # =====================================================
    h2(doc, "5. Значення GUI для вчителя початкової школи")

    body(doc, "Для вчителя початкової школи розуміння принципів GUI — "
              "не абстрактна теорія, а щоденний інструмент. Молодші "
              "школярі опановують комп'ютер саме через графічний "
              "інтерфейс: вони бачать значки, натискають кнопки, "
              "відкривають вікна. Якщо вчитель розуміє, чому "
              "інтерфейс працює саме так, він може пояснити це "
              "дітям доступно й послідовно.")

    body(doc, "Кілька практичних висновків для педагога:")
    bullet(doc, "використовуйте наочність: показуйте не текст "
                "команди, а значок або вікно, про яке йдеться;")
    bullet(doc, "дотримуйтеся послідовності: у роботі з дітьми "
                "однакові дії завжди виконуйте однаково (наприклад, "
                "збереження через Ctrl + S);")
    bullet(doc, "давайте зворотний зв'язок: після кожної дії "
                "дитини показуйте, що сталося (файл з'явився, "
                "папка створилася);")
    bullet(doc, "вчіть виправляти помилки: пояснюйте, що Ctrl + Z, "
                "кошик і повторна спроба — нормальна частина роботи;")
    bullet(doc, "не перевантажуйте інтерфейс: учень 1–2 класу "
                "має бачити лише ті елементи, які йому потрібні "
                "для конкретного завдання.")

    callout(doc,
            "Коли учень уперше бачить комп'ютер, він не думає про "
            "WIMP-концепцію. Він бачить значки, натискає на них і "
            "спостерігає, що відбувається. Завдання вчителя — "
            "зробити цей досвід позитивним, послідовним і "
            "безпечним. Саме тому розуміння принципів GUI — "
            "професійна необхідність для вчителя інформатики.",
            fill="E8F8EC", accent="248A3D")

    # =====================================================
    # КОНТРОЛЬНІ ПИТАННЯ
    # =====================================================
    h2(doc, "Контрольні питання")
    questions = [
        "Дайте визначення графічного інтерфейсу користувача (GUI).",
        "Чим GUI відрізняється від CLI? Наведіть приклад однієї дії, "
        "виконаної обома способами.",
        "Розшифруйте абревіатуру WIMP і поясніть кожен складник.",
        "Що таке вікно? Які елементи воно має?",
        "Які вимоги висувають до якісної піктограми?",
        "Які види меню ви знаєте? Наведіть приклади.",
        "Чому вигляд курсора миші змінюється залежно від контексту?",
        "Назвіть і поясніть шість основних принципів ефективного "
        "GUI.",
        "Що таке юзабіліті? Які п'ять складників його визначають?",
        "Навіщо розробники застосовують людино-орієнтований дизайн?",
        "Як знання принципів GUI допомагає вчителю початкової школи "
        "в роботі з учнями 1–4 класів?",
    ]
    for q in questions:
        numbered(doc, q)

    h2(doc, "Рекомендовані джерела")
    sources = [
        "Томпсон Д., Черніченко В. Операційні системи. Київ : "
        "Кондор, 2017.",
        "Загорулько М. І., Сідоров О. М. Операційні системи: "
        "практикум. Київ : Наукова думка, 2019.",
        "Зайцев В. Г., Дробязко І. П. Операційні системи : навч. "
        "посіб. для студ. спец. 123 «Комп'ютерна інженерія». Київ : "
        "КПІ ім. Ігоря Сікорського, 2019.",
    ]
    for s in sources:
        numbered(doc, s)

    doc.save("Лекція_Основи_GUI.docx")
    print("Готово: Лекція_Основи_GUI.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()