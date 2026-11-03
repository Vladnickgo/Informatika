# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Виконання операцій з файлами та папками в операційній системі
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

# Зберігаємо текст у SVG як <text>, а не криві — для редагування
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

OUT = "output"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# 1. ГЕНЕРАЦІЯ СХЕМ (matplotlib → PNG + SVG, мінімалістичний стиль)
# ============================================================

# Нейтральна палітра + акценти в стилі системних кольорів
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


def _badge(ax, cx, cy, w, h, fill, text, color="white", size=11, radius=None):
    r = radius if radius is not None else h / 2
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={r}",
                                facecolor=fill, edgecolor=fill, linewidth=0))
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=size, fontweight="bold", color=color)


def scheme_operations_map():
    """Схема 1. Основні операції над файлами та папками."""
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.4)
    ax.axis("off")

    ax.text(6.5, 6.95, "Основні операції над файлами та папками",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=TEXT_DARK)

    cards = [
        ("Копіювання", "Ctrl + C  →  Ctrl + V",
         "Створює другий примірник.\nОригінал залишається.", ACCENT_BLUE),
        ("Переміщення", "Ctrl + X  →  Ctrl + V",
         "Переносить об'єкт.\nУ початковій папці його немає.", ACCENT_ORANGE),
        ("Перейменування", "F2",
         "Змінює лише ім'я.\nВміст і місце залишаються.", ACCENT_GREEN),
        ("Видалення", "Delete / Shift + Delete",
         "Delete — у Кошик.\nShift + Delete — остаточно.", ACCENT_RED),
        ("Пошук", "Поле пошуку / Win + S",
         "Знаходить об'єкти\nза назвою або маскою.", ACCENT_PURPLE),
        ("Властивості", "Alt + Enter",
         "Перегляд і зміна\nатрибутів файлу.", ACCENT_ORANGE),
    ]

    card_w, card_h = 3.9, 2.6
    gap_x, gap_y = 0.25, 0.35
    x0 = 0.35
    y_top = 6.5

    for i, (title, shortcut, desc, color) in enumerate(cards):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h)
        ax.text(cx, y + card_h - 0.3, title, ha="center", va="top",
                fontsize=12, fontweight="bold", color=color)
        ax.text(cx, y + card_h - 0.85, shortcut, ha="center", va="top",
                fontsize=9.5, color=TEXT_GRAY, fontfamily="monospace")
        ax.text(cx, y + 1.0, desc, ha="center", va="top",
                fontsize=9.5, color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_operations_map")


def scheme_search_masks():
    """Схема 2. Пошук файлів за маскою."""
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    ax.text(6.5, 7.75, "Пошук файлів за маскою", ha="center", va="center",
            fontsize=14, fontweight="bold", color=TEXT_DARK)

    # Пояснення символів у двох картках
    _card(ax, 0.5, 6.3, 5.9, 1.0, fill="#E1F0FE", border=ACCENT_BLUE, radius=0.18)
    ax.text(1.0, 7.05, "*  —  будь-яка кількість символів",
            ha="left", va="center", fontsize=10.5, fontweight="bold",
            color=ACCENT_BLUE)
    ax.text(1.0, 6.6, "(у тому числі нуль)", ha="left", va="center",
            fontsize=9.5, color=TEXT_DARK, style="italic")

    _card(ax, 6.6, 6.3, 5.9, 1.0, fill="#E8F8EC", border=ACCENT_GREEN, radius=0.18)
    ax.text(7.1, 7.05, "?  —  рівно один символ",
            ha="left", va="center", fontsize=10.5, fontweight="bold",
            color=ACCENT_GREEN)
    ax.text(7.1, 6.6, "(будь-який, але лише один)", ha="left", va="center",
            fontsize=9.5, color=TEXT_DARK, style="italic")

    # Приклади
    examples = [
        ("*.docx", "Усі документи Word у папці"),
        ("Звіт*.docx", "Файли, назва яких починається зі «Звіт»"),
        ("????.txt", "Текстові файли з назвою рівно з 4 символів"),
        ("Фото_202?.jpg", "Фото за 2020–2029 роки"),
        ("*урок*", "Усі файли, у назві яких є слово «урок»"),
    ]

    y = 5.2
    for mask, meaning in examples:
        _badge(ax, 2.3, y, 3.6, 0.62, CARD_BG, mask, color=TEXT_DARK,
               size=10.5, radius=0.28)
        ax.annotate("", xy=(4.35, y), xytext=(4.15, y),
                    arrowprops=dict(arrowstyle="-|>", color=TEXT_GRAY,
                                    linewidth=1.4, mutation_scale=12))
        ax.text(4.65, y, meaning, ha="left", va="center",
                fontsize=10.5, color=TEXT_DARK)
        y -= 0.85

    return _save(fig, "scheme_search_masks")


def scheme_three_ways():
    """Схема 3. Три способи виконати одну операцію."""
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    ax.text(6.0, 5.75, "Три способи виконати одну операцію",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=TEXT_DARK)

    cards = [
        ("1", "Контекстне меню", "Права кнопка миші\n→ вибір команди", ACCENT_BLUE),
        ("2", "Гарячі клавіші", "Ctrl+C, Ctrl+X, Ctrl+V,\nF2, Delete, Alt+Enter",
         ACCENT_GREEN),
        ("3", "Перетягування", "Затиснути ліву кнопку\nта перемістити об'єкт",
         ACCENT_ORANGE),
    ]

    card_w, card_h = 3.6, 3.9
    gap = 0.3
    x0 = 0.3
    y0 = 0.9

    for i, (num, title, desc, color) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h)
        _badge(ax, cx, y0 + card_h - 0.8, 0.8, 0.8, color, num,
               size=15, radius=0.4)
        ax.text(cx, y0 + card_h - 1.75, title, ha="center", va="center",
                fontsize=12, fontweight="bold", color=TEXT_DARK)
        ax.text(cx, y0 + 1.3, desc, ha="center", va="center",
                fontsize=10, color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_three_ways")


def scheme_levels():
    """Схема 4. Три рівні практичних завдань."""
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.3, "Три рівні практичних завдань",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=TEXT_DARK)

    levels = [
        ("Рівень 1", "Репродуктивний",
         "Базові операції:\nкопіювати, перейменувати,\nвидалити, знайти",
         "≈ 7 хв", ACCENT_GREEN, "#E8F8EC"),
        ("Рівень 2", "Продуктивний",
         "Структура папок,\nпереміщення між папками,\nпошук за маскою",
         "≈ 10 хв", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Творчий",
         "Швидкісний ланцюжок\nоперацій + проєкт\nструктури для вчителя",
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
               size=11, radius=0.3)
        ax.text(cx, y0 + card_h - 1.55, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color=TEXT_DARK, style="italic")
        ax.text(cx, y0 + card_h - 3.0, desc, ha="center", va="center",
                fontsize=10, color=TEXT_DARK, linespacing=1.7)
        _badge(ax, cx, y0 + 0.75, 2.1, 0.55, fill, time_txt,
               color=color, size=10.5, radius=0.28)

    return _save(fig, "scheme_levels")


# ============================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ============================================================

FONT = "Times New Roman"
BLUE = RGBColor(0x1F, 0x4E, 0x79)


def _style_run(run, size=14, bold=False, italic=False, color=None):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rpr = run._r.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    for tag in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(tag), FONT)
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
    """Рядок «Тема: <назва>» — жирний, по центру, без верхнього регістру."""
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
    """Нумерований список у форматі 1), 2), 3)."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(1.0)
    _style_run(p.add_run(f"{idx}) "), bold=True)
    _style_run(p.add_run(text))
    return p


def callout(doc, text, fill="EAF2F8", accent="2E75B6", title=None):
    """Callout-блок без обов'язкового заголовка."""
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
        _style_run(p.add_run(htext), bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
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
# 3. ПОБУДОВА ДОКУМЕНТА
# ============================================================

def build_document():
    img1 = scheme_operations_map()
    img2 = scheme_search_masks()
    img3 = scheme_three_ways()
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

    # ---------- Заголовок + Тема ----------
    h1(doc, "Практичне заняття")
    theme_line(doc, "Виконання операцій з файлами та папками "
                    "в операційній системі")

    # ---------- Мета ----------
    h2(doc, "Мета")
    body(doc, "тренувати практичні навички виконання операцій копіювання, "
              "переміщення, видалення, перейменування та пошуку файлів і папок; "
              "розвивати швидкість реакції та впевненість під час роботи з "
              "графічним інтерфейсом файлового менеджера; виховувати культуру "
              "роботи з інформацією та дбайливе ставлення до логічної структури "
              "даних.")

    # ---------- Обладнання / ПЗ ----------
    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11 або Linux (графічне середовище).",
        "Файловий менеджер «Проводник» (Windows) / Nautilus (Linux).",
        "Інструкційні картки до рівнів 1–3 (додаються).",
        "Текстовий редактор (MS Word / LibreOffice Writer) для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці», Flameshot).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    # ---------- Література ----------
    h2(doc, "Література")
    sources = [
        "Таненбаум Е., Бос Г. Операційні системи: проектування та реалізація. "
        "Київ : Вильямс, 2015.",
        "Томпсон Д., Черніченко В. Операційні системи. Київ : Кондор, 2017.",
        "Загорулько М. І., Сідоров О. М. Операційні системи: практикум. "
        "Київ : Наукова думка, 2019.",
    ]
    for s in sources:
        numbered(doc, s)

    # =========================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =========================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Основні операції над файлами та папками")
    body(doc, "Операційна система надає користувачеві набір стандартних "
              "операцій над об'єктами файлової системи: копіювання, "
              "переміщення, перейменування, видалення, пошук, перегляд "
              "властивостей. Кожну з них можна виконати трьома способами: "
              "через контекстне меню, гарячими клавішами або перетягуванням "
              "мишею. Уміння швидко обирати потрібний спосіб формує "
              "впевненість під час роботи з графічним інтерфейсом.")

    add_figure(doc, img1, 16.0)

    body(doc, "Розрізняйте копіювання й переміщення: у першому випадку "
              "оригінал залишається на місці, у другому — об'єкт зникає з "
              "початкової папки. Під час переміщення між різними дисками "
              "система фактично виконує копіювання, а потім видаляє оригінал, "
              "тому операція триває довше.")

    add_table(
        doc,
        ["Операція", "Гарячі клавіші", "Результат"],
        [
            ["Копіювання", "Ctrl+C → Ctrl+V",
             "Створено другий примірник об'єкта"],
            ["Переміщення", "Ctrl+X → Ctrl+V",
             "Об'єкт переміщено в іншу папку"],
            ["Перейменування", "F2",
             "Змінено ім'я без зміни вмісту"],
            ["Видалення у Кошик", "Delete",
             "Об'єкт можна відновити"],
            ["Остаточне видалення", "Shift+Delete",
             "Відновлення ускладнене"],
            ["Властивості", "Alt+Enter",
             "Відкрито вікно атрибутів файлу"],
        ],
        widths=[4.4, 5.2, 6.9],
    )

    h3(doc, "2. Способи виконання операцій")
    body(doc, "У графічному середовищі одна й та сама операція виконується "
              "кількома способами. Початківцю зручно користуватися "
              "контекстним меню, досвідченому користувачеві — гарячими "
              "клавішами. Перетягування мишею (drag-and-drop) доречне, коли "
              "потрібно швидко перенести об'єкт у видиму папку.")

    add_figure(doc, img3, 15.5)

    body(doc, "Якщо ви не впевнені в результаті операції — користуйтеся "
              "контекстним меню: воно показує назву команди й дозволяє "
              "перевірити вибір. Гарячі клавіші доречні, коли дія вже "
              "відпрацьована до автоматизму.")

    h3(doc, "3. Пошук файлів і папок")
    body(doc, "Пошук дозволяє швидко знайти потрібний об'єкт, навіть якщо "
              "його місцезнаходження невідоме. У полі пошуку Проводника "
              "можна вводити точну назву або маску з символами «*» і «?». "
              "Символ «*» замінює будь-яку кількість символів, символ «?» — "
              "рівно один символ.")

    add_figure(doc, img2, 15.5)

    body(doc, "Додаткові можливості пошуку в Проводнику:")
    bullet(doc, "фільтр за типом файлу (документи, зображення, відео);")
    bullet(doc, "фільтр за датою змінення (сьогодні, цього тижня, цього місяця);")
    bullet(doc, "сортування результатів за назвою, датою або розміром;")
    bullet(doc, "пошук у межах вибраної папки або на всьому диску.")

    h3(doc, "4. Культура роботи з файловою системою")
    body(doc, "Акуратність під час роботи з файлами — складова інформаційної "
              "культури. Дотримуйтеся простих правил: давайте файлам змістовні "
              "назви; групуйте документи за темами в окремих папках; перед "
              "видаленням перевіряйте вибраний об'єкт; регулярно створюйте "
              "резервні копії важливих матеріалів.")

    callout(doc,
            "Копіювання — це «зробити ксерокопію малюнка», переміщення — "
            "«перекласти зошит зі столу до портфеля», видалення — «викинути "
            "чернетку в кошик». Такі аналогії допомагають дітям зрозуміти "
            "різницю між операціями.",
            fill="FFF4E5", accent="C55A11")

    # =========================================================
    # ПОКРОКОВИЙ АЛГОРИТМ РІЗНОРІВНЕВИХ ЗАВДАНЬ
    # =========================================================
    h2(doc, "Покроковий алгоритм виконання різнорівневих завдань")

    body(doc, "Практична частина заняття побудована за трирівневою системою "
              "(схема 4). Студент виконує завдання послідовно; орієнтовний "
              "час на кожен рівень — 7–10 хвилин, загальна тривалість "
              "практичної частини — 25–30 хвилин. Оцінка залежить від "
              "кількості успішно виконаних рівнів.")

    add_figure(doc, img4, 16.0)

    # -------- Рівень 1 --------
    h3(doc, "Рівень 1 — репродуктивний (≈ 7 хв)",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Мета: відпрацювати базові операції — копіювання, "
              "перейменування, видалення та пошук — на простих об'єктах.")

    add_table(
        doc,
        ["№", "Крок", "Дія"],
        [
            ["1", "Створіть робочу папку",
             "У дереві папок відкрийте диск C: або D:. Права кнопка → "
             "«Створити» → «Папку». Назвіть її «ПЗ_Операції_ПІБ»."],
            ["2", "Створіть файл",
             "Усередині папки створіть текстовий документ «проба.txt». "
             "Введіть у нього довільний текст і збережіть."],
            ["3", "Скопіюйте файл",
             "Виділіть «проба.txt» → Ctrl+C → у тій самій папці натисніть "
             "Ctrl+V. Має з'явитися «проба — копія.txt»."],
            ["4", "Перейменуйте копію",
             "Виділіть копію → F2 → введіть «звіт.txt» → Enter."],
            ["5", "Видаліть копію",
             "Виділіть «звіт.txt» → клавіша Delete. Перевірте, що файл "
             "зник з папки."],
            ["6", "Створіть ще три файли",
             "Створіть три текстові файли з назвами: «урок_1.txt», "
             "«урок_2.txt», «план.txt»."],
            ["7", "Знайдіть файли за маскою",
             "У полі пошуку введіть «урок*.txt» і натисніть Enter. "
             "Переконайтеся, що знайдено два файли."],
            ["8", "Перевірте результат",
             "Порахуйте файли у папці: їх має бути 4 (проба, урок_1, "
             "урок_2, план)."],
            ["9", "Зробіть скріншот",
             "Натисніть Print Screen; вставте у звіт із підписом."],
        ],
        widths=[1.0, 5.0, 10.5],
    )

    callout(doc,
            "Після виконання рівня 1 у папці «ПЗ_Операції_ПІБ» має бути "
            "рівно 4 файли: «проба.txt», «урок_1.txt», «урок_2.txt», "
            "«план.txt». Якщо кількість інша — перевірте, чи не залишилися "
            "копії.",
            fill="E8F8EC", accent="248A3D")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — продуктивний (≈ 10 хв)",
       color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Мета: побудувати ієрархічну структуру папок, виконати "
              "переміщення об'єктів і пошук за маскою у вкладеній структурі.")

    add_table(
        doc,
        ["№", "Крок", "Дія"],
        [
            ["1", "Побудуйте структуру папок",
             "Усередині «ПЗ_Операції_ПІБ» створіть папки «Уроки», "
             "«Матеріали», «Архів»."],
            ["2", "Створіть підпапки",
             "У папці «Уроки» створіть підпапки «1_клас» і «2_клас»."],
            ["3", "Перемістіть файли",
             "Перемістіть «урок_1.txt» у «Уроки\\1_клас», а «урок_2.txt» — "
             "у «Уроки\\2_клас» (Ctrl+X → Ctrl+V)."],
            ["4", "Перевірте результат",
             "Переконайтеся, що в корені «ПЗ_Операції_ПІБ» залишилися лише "
             "«проба.txt» і «план.txt», а також папки."],
            ["5", "Скопіюйте файл у дві папки",
             "Скопіюйте «план.txt» у «Матеріали» та в «Архів»."],
            ["6", "Знайдіть усі txt-файли",
             "У полі пошуку введіть «*.txt» і натисніть Enter. "
             "Перевірте, скільки файлів знайдено."],
            ["7", "Звузьте пошук",
             "У полі пошуку введіть «урок_?.txt». Переконайтеся, що "
             "знайдено лише файли з однією цифрою в назві."],
            ["8", "Перетягніть файл мишею",
             "Відкрийте «Матеріали» та «Архів» в окремих вікнах. "
             "Перетягніть «план.txt» з «Архіву» до «Матеріалів»."],
            ["9", "Зробіть скріншот",
             "Знімок дерева папок із розгорнутими вузлами."],
        ],
        widths=[1.0, 5.0, 10.5],
    )

    callout(doc,
            "У звіті має бути: скріншот структури папок, результати двох "
            "пошуків («*.txt» і «урок_?.txt») з підписами, коротке "
            "пояснення різниці між цими масками.",
            fill="FFF4E5", accent="C93400")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — творчий (≈ 10 хв)",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Мета: виконати швидкісний ланцюжок операцій без підказок і "
              "спроєктувати структуру папок для вчителя початкової школи.")

    body(doc, "Завдання А. Швидкісний ланцюжок. За один підхід виконайте "
              "послідовність дій, не користуючись інструкційною карткою. "
              "Кожен крок оцінюється окремо:")
    chain = [
        "створити папку «Швидкість»;",
        "створити в ній текстовий файл «тест.txt»;",
        "скопіювати файл у папку «Архів»;",
        "перейменувати оригінал у «тест_2.txt»;",
        "перемістити «тест_2.txt» до папки «Матеріали»;",
        "видалити копію з «Архіву»;",
        "знайти файл за маскою «тест*.txt»;",
        "змінити атрибут «тільки читання» для знайденого файлу.",
    ]
    for c in chain:
        numbered(doc, c)

    body(doc, "Завдання Б. Проєкт структури. Уявіть, що ви — вчитель "
              "початкової школи. Спроєктуйте структуру папок на робочому "
              "диску (не менше трьох рівнів вкладеності), яка дозволяла б "
              "швидко знаходити матеріали до уроків і зберігати зразки робіт "
              "учнів. Створіть цю структуру у файловому менеджері та "
              "продемонструйте на ній три операції: переміщення, "
              "копіювання, пошук за маскою.")

    body(doc, "У звіті до рівня 3 додайте:")
    numbered(doc, "скріншот структури папок з підписами рівнів;")
    numbered(doc, "перелік восьми кроків ланцюжка із зазначенням, які "
                  "кроки виконано без помилок;")
    numbered(doc, "коротке обґрунтування (5–7 речень) логіки структури;")
    numbered(doc, "одну пораду учням 3–4 класу щодо збереження файлів, "
                  "сформульовану доступною мовою.")

    callout(doc,
            "За бажанням (+1 бал). Запропонуйте власну маску пошуку, яка "
            "знаходить файли з назвами «урок_1», «урок_2», …, «урок_9», але "
            "НЕ знаходить файли з двозначними номерами. Поясніть, чому ваша "
            "маска працює саме так.",
            fill="FFEBEA", accent="C4001D")

    # =========================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =========================================================
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Рівень / критерій", "Показник", "Бали"],
        [
            ["Рівень 1",
             "Усі 9 кроків виконано правильно; у папці рівно 4 файли; "
             "є скріншот", "3"],
            ["Рівень 2",
             "Створено повну структуру; правильно виконано переміщення й "
             "копіювання; обидва пошуки за маскою коректні", "4"],
            ["Рівень 3",
             "Ланцюжок виконано без помилок (≥6 із 8 кроків); структура "
             "логічна, ≥3 рівні; є обґрунтування та порада для учнів", "4"],
            ["Якість звіту",
             "Оформлення за вимогами; підписи до всіх скріншотів; "
             "пояснення масок пошуку", "1"],
            ["Творчий підхід",
             "Виконано ускладнення або запропоновано оригінальну маску "
             "пошуку", "1"],
        ],
        widths=[3.6, 11.0, 2.0],
    )

    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 балів — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (потребує доопрацювання).")

    # =========================================================
    # ФОРМА ЗВІТНОСТІ
    # =========================================================
    h2(doc, "Форма звітності")
    body(doc, "Результати практичного заняття оформлюються у вигляді "
              "електронного звіту в текстовому редакторі. Звіт повинен "
              "містити такі обов'язкові частини:")
    report_parts = [
        "Титульна сторінка: навчальний заклад, тема, ПІБ студента, група, "
        "ПІБ викладача, дата.",
        "Короткі відповіді на контрольні питання кожного рівня (письмово).",
        "Скріншоти результатів: після рівня 1 (вміст папки), після рівня 2 "
        "(дерево папок + результати пошуку), після рівня 3 (спроєктована "
        "структура).",
        "Опис виконаних дій до кожного скріншота (1–2 речення).",
        "Структура папок для вчителя початкової школи та її обґрунтування "
        "(рівень 3).",
        "Висновок: що нового закріпили на практиці, які операції виконували "
        "впевнено, а які потребують додаткового тренування.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, шрифт "
              "Times New Roman 14 pt, інтервал 1,15, поля 2 см, обсяг — "
              "3–5 сторінок без титульної. Ім'я файлу: "
              "«Практика_Операції_з_файлами_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    doc.save("Практичне_заняття_Операції_з_файлами.docx")
    print("Готово: Практичне_заняття_Операції_з_файлами.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()