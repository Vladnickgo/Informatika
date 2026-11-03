# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ТЕМАТИЧНИЙ ЗАЛІК (контрольна робота)
Тема: Файлові системи та операції з файлами
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

# SVG: зберігаємо текст як <text> — для редагування
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

OUT = "output"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# Палітра в стилі системних кольорів (Apple)
# ============================================================
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
# СХЕМА 1. Структура тематичного заліку
# ============================================================

def scheme_structure():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.6)
    ax.axis("off")

    ax.text(6.5, 7.15, "Структура тематичного заліку",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    levels = [
        ("Рівень 1", "Тестові завдання",
         "15 запитань з вибором\nоднієї відповіді\n+ 1 завдання на співставлення",
         "8 балів", ACCENT_BLUE, "#E1F0FE"),
        ("Рівень 2", "Практичні завдання",
         "3 завдання на застосування\nзнань у знайомих\nситуаціях",
         "6 балів", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Творче завдання",
         "1 комплексне завдання\nна проєктування\nструктури даних",
         "6 балів", ACCENT_RED, "#FFEBEA"),
    ]

    card_w, card_h = 3.9, 4.5
    gap = 0.35
    x0 = 0.5
    y0 = 1.7

    for i, (level, name, desc, points, color, fill) in enumerate(levels):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h)
        _badge(ax, cx, y0 + card_h - 0.65, 1.9, 0.6, color, level,
               size=13, radius=0.3)
        ax.text(cx, y0 + card_h - 1.45, name, ha="center", va="center",
                fontsize=13, fontweight="bold", color=TEXT_DARK)
        ax.text(cx, y0 + card_h - 2.95, desc, ha="center", va="center",
                fontsize=12, color=TEXT_DARK, linespacing=1.7)
        _badge(ax, cx, y0 + 0.7, 2.1, 0.55, fill, points,
               color=color, size=12.5, radius=0.28)

    # Підсумок
    _badge(ax, 6.5, 0.75, 4.2, 0.7, TEXT_DARK,
           "Разом: 20 балів", color="white", size=14, radius=0.35)

    return _save(fig, "scheme_structure")


# ============================================================
# СХЕМА 2. Формат завдання на співставлення
# ============================================================

def scheme_matching_format():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    ax.text(6.5, 7.7, "Формат завдання на співставлення",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    ax.text(2.8, 6.95, "ОПЕРАЦІЇ", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=ACCENT_BLUE)
    ax.text(10.2, 6.95, "РЕЗУЛЬТАТИ", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=ACCENT_GREEN)

    operations = [
        "1.  Ctrl+C → Ctrl+V",
        "2.  Ctrl+X → Ctrl+V",
        "3.  F2",
        "4.  Delete",
        "5.  Shift+Delete",
    ]
    results = [
        "А.  Об'єкт видалено остаточно",
        "Б.  Створено копію об'єкта",
        "В.  Об'єкт видалено у Кошик",
        "Г.  Змінено ім'я об'єкта",
        "Д.  Об'єкт переміщено",
    ]

    y = 5.9
    for op, res in zip(operations, results):
        _card(ax, 0.5, y - 0.42, 4.7, 0.78,
              fill="#E1F0FE", border=ACCENT_BLUE, radius=0.12)
        ax.text(0.75, y, op, ha="left", va="center",
                fontsize=12, color=TEXT_DARK)

        _card(ax, 7.8, y - 0.42, 5.0, 0.78,
              fill="#E8F8EC", border=ACCENT_GREEN, radius=0.12)
        ax.text(8.05, y, res, ha="left", va="center",
                fontsize=12, color=TEXT_DARK)

        ax.text(6.5, y, "?", ha="center", va="center",
                fontsize=15, fontweight="bold", color=TEXT_GRAY)

        y -= 0.85

    ax.text(6.5, 0.4, "Запишіть відповідність: 1 – ?,  2 – ?,  3 – ?,  4 – ?,  5 – ?",
            ha="center", va="center", fontsize=11.5, style="italic",
            color=TEXT_GRAY)

    return _save(fig, "scheme_matching_format")


# ============================================================
# СХЕМА 3. Шкала оцінювання
# ============================================================

def scheme_grading_scale():
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    ax.text(6.5, 4.75, "Шкала оцінювання",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    grades = [
        ("18–20", "Відмінно", ACCENT_GREEN, "#E8F8EC"),
        ("14–17", "Добре", ACCENT_BLUE, "#E1F0FE"),
        ("10–13", "Задовільно", ACCENT_ORANGE, "#FFF4E5"),
        ("1–9", "Незадовільно", ACCENT_RED, "#FFEBEA"),
    ]

    card_w, card_h = 2.9, 3.3
    gap = 0.3
    x0 = (13 - (4 * card_w + 3 * gap)) / 2
    y0 = 0.7

    for i, (score, label, color, fill) in enumerate(grades):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h, fill=fill, border=color, radius=0.2)
        ax.text(cx, y0 + card_h - 0.9, score, ha="center", va="center",
                fontsize=22, fontweight="bold", color=color)
        ax.text(cx, y0 + card_h - 1.55, "балів", ha="center", va="center",
                fontsize=11, color=TEXT_GRAY, style="italic")
        ax.text(cx, y0 + 0.9, label, ha="center", va="center",
                fontsize=13, fontweight="bold", color=TEXT_DARK)

    return _save(fig, "scheme_grading_scale")


# ============================================================
# ДОПОМІЖНІ ФУНКЦІЇ DOCX
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


def test_question(doc, num, question, options):
    """Одне тестове запитання з 4 варіантами відповіді."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    _style_run(p.add_run(f"{num}. "), bold=True)
    _style_run(p.add_run(question))
    for letter, opt in zip(["а", "б", "в", "г"], options):
        op = doc.add_paragraph()
        op.paragraph_format.left_indent = Cm(1.0)
        op.paragraph_format.space_after = Pt(1)
        op.paragraph_format.line_spacing = 1.15
        _style_run(op.add_run(f"{letter}) "), bold=True)
        _style_run(op.add_run(opt))


# ============================================================
# ПОБУДОВА ДОКУМЕНТА
# ============================================================

def build_document():
    img1 = scheme_structure()
    img2 = scheme_matching_format()
    img3 = scheme_grading_scale()

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

    # Заголовок + Тема
    h1(doc, "Тематичний залік")
    theme_line(doc, "Тематичний залік. Контрольна робота "
                    "з розділу «Файлові системи та операції з файлами»")

    h2(doc, "Мета")
    body(doc, "узагальнити та проконтролювати засвоєння знань з розділу "
              "«Файлові системи та операції з файлами»; розвивати здатність "
              "до самооцінки та рефлексії під час виконання контрольних "
              "завдань; виховувати чесність, принциповість та самостійність "
              "під час підсумкового оцінювання.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11 або Linux.",
        "Файловий менеджер «Проводник» (Windows) / Nautilus (Linux).",
        "Інструкційні картки із завданнями рівнів 1–3.",
        "Аркуші для письмових відповідей або електронний бланк.",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Томпсон Д., Черніченко В. Операційні системи. Київ : Кондор, 2017.",
        "Загорулько М. І., Сідоров О. М. Операційні системи: практикум. "
        "Київ : Наукова думка, 2019.",
        "Зайцев В. Г., Дробязко І. П. Операційні системи : навч. посіб. для "
        "студ. спец. 123 «Комп'ютерна інженерія». Київ : КПІ ім. Ігоря "
        "Сікорського, 2019.",
    ]
    for s in sources:
        numbered(doc, s)

    h2(doc, "Загальна структура роботи")
    body(doc, "Залікова робота складається з трьох рівнів. Кожен наступний "
              "рівень ускладнюється та оцінюється окремо. Максимальна "
              "кількість балів за всю роботу — 20.")
    add_figure(doc, img1, 16.0)

    # =====================================================
    # РІВЕНЬ 1
    # =====================================================
    h2(doc, "Рівень 1. Тестові завдання (8 балів)")
    body(doc, "Оберіть одну правильну відповідь у кожному запитанні. "
              "Правильна відповідь на кожне з 15 запитань оцінюється "
              "0,4 бала; завдання на співставлення — 2 бали.")

    questions = [
        ("Що таке файлова система?",
         ["програма для створення файлів",
          "частина операційної системи, що забезпечує зберігання та "
          "впорядкування даних на носіях",
          "пристрій для зберігання інформації",
          "програма для перегляду зображень"]),
        ("Яке розширення має текстовий документ Microsoft Word?",
         [".txt", ".docx", ".xlsx", ".pdf"]),
        ("Яка комбінація клавіш використовується для копіювання об'єкта?",
         ["Ctrl + X", "Ctrl + C", "Ctrl + V", "Ctrl + Z"]),
        ("Що відбувається з файлом під час переміщення?",
         ["створюється копія, оригінал залишається на місці",
          "файл зникає з початкової папки та з'являється в кінцевій",
          "файл видаляється назавжди",
          "вміст файлу змінюється"]),
        ("Яка клавіша переміщує об'єкт у Кошик?",
         ["Backspace", "Delete", "Esc", "Enter"]),
        ("Яка комбінація клавіш видаляє об'єкт остаточно, минаючи Кошик?",
         ["Ctrl + Delete", "Alt + Delete", "Shift + Delete", "Fn + Delete"]),
        ("Який символ у масці пошуку замінює будь-яку кількість символів?",
         ["?", "*", "#", "%"]),
        ("Яка файлова система є стандартною для ОС Windows?",
         ["FAT32", "NTFS", "ext4", "HFS+"]),
        ("Яка максимальна довжина імені файлу в ОС Windows (у символах)?",
         ["32", "128", "255", "512"]),
        ("Що таке ярлик?",
         ["файл із копією вмісту іншого файлу",
          "файл-посилання на інший об'єкт",
          "папка зі швидким доступом",
          "архів із програмами"]),
        ("Який атрибут забороняє редагування файлу?",
         ["«Прихований»", "«Архівний»", "«Тільки читання»", "«Системний»"]),
        ("Що таке абсолютний шлях?",
         ["шлях від поточної папки",
          "шлях від кореня диска",
          "шлях до Кошика",
          "шлях до робочого столу"]),
        ("Яке розширення має презентація Microsoft PowerPoint?",
         [".docx", ".xlsx", ".pptx", ".pdf"]),
        ("Яка гаряча клавіша перейменовує файл?",
         ["F1", "F2", "F5", "F12"]),
        ("Яка дія НЕ призводить до втрати даних?",
         ["Shift + Delete",
          "очищення Кошика",
          "копіювання файлу",
          "форматування диска"]),
    ]

    for i, (q, opts) in enumerate(questions, 1):
        test_question(doc, i, q, opts)

    # Завдання на співставлення
    h3(doc, "Завдання 16. Співставлення (2 бали)",
       color=RGBColor(0x00, 0x71, 0xE3))
    body(doc, "Установіть відповідність між операціями (1–5) та їхніми "
              "результатами (А–Д). Запишіть відповідь у вигляді рядка: "
              "1 – ?, 2 – ?, 3 – ?, 4 – ?, 5 – ?.")
    add_figure(doc, img2, 16.0)

    add_table(
        doc,
        ["№", "Операція", "Результат"],
        [
            ["1", "Ctrl + C → Ctrl + V", "А. Об'єкт видалено остаточно"],
            ["2", "Ctrl + X → Ctrl + V", "Б. Створено копію об'єкта"],
            ["3", "F2", "В. Об'єкт видалено у Кошик"],
            ["4", "Delete", "Г. Змінено ім'я об'єкта"],
            ["5", "Shift + Delete", "Д. Об'єкт переміщено в іншу папку"],
        ],
        widths=[1.0, 6.0, 9.5],
    )

    # =====================================================
    # РІВЕНЬ 2
    # =====================================================
    h2(doc, "Рівень 2. Практичні завдання (6 балів)")
    body(doc, "Завдання 1–3 виконуються письмово. Кожне завдання "
              "оцінюється у 2 бали.")

    h3(doc, "Завдання 1. Порівняльна таблиця (2 бали)")
    body(doc, "Заповніть таблицю, указавши характеристики кожної операції.")
    add_table(
        doc,
        ["Параметр", "Копіювання", "Переміщення", "Видалення"],
        [
            ["Вплив на оригінал", "", "", ""],
            ["Гарячі клавіші", "", "", ""],
            ["Основне призначення", "", "", ""],
            ["Можливість скасування", "", "", ""],
        ],
        widths=[4.2, 4.1, 4.1, 4.1],
    )

    h3(doc, "Завдання 2. Алгоритм (2 бали)")
    body(doc, "Опишіть алгоритм створення папки «Мої_документи» на диску D: "
              "та текстового файлу «нотатка.txt» усередині цієї папки. "
              "Подайте алгоритм у вигляді послідовності 5–7 кроків.")
    for i in range(1, 8):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        _style_run(p.add_run(f"{i}. "), bold=True)
        _style_run(p.add_run("_" * 70), color=RGBColor(0xBF, 0xBF, 0xBF))

    h3(doc, "Завдання 3. Абсолютний та відносний шляхи (2 бали)")
    body(doc, "Поясніть різницю між абсолютним та відносним шляхами до "
              "файлу. Наведіть по одному прикладу кожного для файлу "
              "«урок_1.docx», що міститься у папці "
              "«C:\\Навчання\\3_клас\\Уроки».")

    # =====================================================
    # РІВЕНЬ 3
    # =====================================================
    h2(doc, "Рівень 3. Творче завдання (6 балів)")
    body(doc, "Завдання 4 виконується письмово та передбачає комплексне "
              "застосування знань з розділу.")

    h3(doc, "Завдання 4. Проєкт структури файлової системи (6 балів)")
    body(doc, "Уявіть, що ви — вчитель початкової школи. На робочому диску "
              "комп'ютера потрібно організувати матеріали для навчання "
              "учнів 1–4 класів так, щоб швидко знаходити потрібні "
              "документи та уникнути втрати даних.")

    body(doc, "Виконайте такі кроки:")
    steps = [
        "Спроєктуйте структуру папок (не менше трьох рівнів вкладеності) "
        "та зобразіть її у вигляді схеми або переліку.",
        "Сформулюйте 5 правил іменування файлів і папок, яких ви будете "
        "дотримуватися в цій структурі.",
        "Запропонуйте по дві маски пошуку для швидкого знаходження: "
        "(а) усіх планів уроків з певного предмета; (б) усіх фото з "
        "конкретного заходу.",
        "Опишіть, як ваша структура допоможе уникнути випадкової втрати "
        "даних (2–3 речення).",
        "Наведіть 1 приклад абсолютного та 1 приклад відносного шляху "
        "до будь-якого файлу з вашої структури.",
    ]
    for s in steps:
        numbered(doc, s)

    callout(doc,
            "Оцінюється: логічність структури (2 бали), коректність правил "
            "іменування (1 бал), доречність масок пошуку (1 бал), "
            "обґрунтування захисту даних (1 бал), правильність прикладів "
            "шляхів (1 бал).",
            fill="E1F0FE", accent="0071E3")

    # =====================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =====================================================
    h2(doc, "Критерії оцінювання")
    add_figure(doc, img3, 15.0)

    add_table(
        doc,
        ["Рівень", "Що оцінюється", "Максимум балів"],
        [
            ["Рівень 1",
             "15 тестових запитань по 0,4 бала + завдання на співставлення "
             "(2 бали)", "8"],
            ["Рівень 2",
             "Завдання 1–3, по 2 бали кожне: заповнення таблиці, алгоритм, "
             "пояснення шляхів", "6"],
            ["Рівень 3",
             "Завдання 4: логічність структури (2), правила іменування (1), "
             "маски пошуку (1), захист даних (1), приклади шляхів (1)", "6"],
            ["Разом", "Сума балів за три рівні", "20"],
        ],
        widths=[2.8, 11.3, 2.4],
    )

    body(doc, "Шкала переведення у підсумкову оцінку: 18–20 балів — "
              "«відмінно»; 14–17 — «добре»; 10–13 — «задовільно»; "
              "менше 10 — «незадовільно».")

    callout(doc,
            "Відповіді на завдання 16 (співставлення): 1 – Б, 2 – Д, "
            "3 – Г, 4 – В, 5 – А. Ця інформація призначена для перевірки "
            "викладачем — не використовуйте її під час виконання роботи.",
            fill="E8F8EC", accent="248A3D")

    doc.save("Тематичний_залік_Файлові_системи.docx")
    print("Готово: Тематичний_залік_Файлові_системи.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()