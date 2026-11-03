# -*- coding: utf-8 -*-
"""
Генерація методичного матеріалу:
Тематичний залік № 4. Контрольна робота.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs("output", exist_ok=True)

# ============================================================
#  НАЛАШТУВАННЯ СХЕМ (matplotlib) — стиль Apple
# ============================================================
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

C_BG = "#F5F5F7"
C_EDGE = "#E5E5EA"
T_DARK = "#1D1D1F"
T_GRAY = "#86868B"
A_BLUE = "#0071E3"
A_GREEN = "#248A3D"
A_ORANGE = "#C93400"
A_RED = "#C4001D"
A_PURPLE = "#6E30A8"


def _save(fig, name):
    png = os.path.join("output", f"{name}.png")
    svg = os.path.join("output", f"{name}.svg")
    fig.savefig(png, dpi=220, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(svg, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return png


def _card(ax, x, y, w, h, title, lines, accent, title_size=13.5, line_size=11.5):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0,rounding_size=2.0",
                         linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
    ax.add_patch(box)
    bar = FancyBboxPatch((x + 4, y + h - 5.0), w - 8, 1.1,
                         boxstyle="round,pad=0,rounding_size=0.55",
                         linewidth=0, facecolor=accent)
    ax.add_patch(bar)
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center",
            fontsize=title_size, fontweight="bold", color=T_DARK)
    if lines:
        ax.text(x + w / 2, y + h * 0.32, "\n".join(lines),
                ha="center", va="center", fontsize=line_size,
                color=T_GRAY, linespacing=1.45)


# -------- Схема 1: Загальна структура роботи (3 рівні + сума) --------
def schema_structure():
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 95, "Загальна структура тематичного заліку",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    levels = [
        ("Рівень 1\nТестові завдання", ["15 тестів + 1", "співставлення 5×5", "— 20 балів"], A_BLUE),
        ("Рівень 2\nПрактичні завдання", ["3 завдання", "з письмовою", "відповіддю — 12 балів"], A_GREEN),
        ("Рівень 3\nТворче завдання", ["1 комплексне", "завдання", "— 8 балів"], A_ORANGE),
    ]
    w, h, gap = 30, 52, 3
    x0 = (100 - 3 * w - 2 * gap) / 2
    y = 34
    for i, (title, lines, color) in enumerate(levels):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=2.0",
                             linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
        ax.add_patch(box)
        bar = FancyBboxPatch((x + 4, y + h - 5.0), w - 8, 1.1,
                             boxstyle="round,pad=0,rounding_size=0.55",
                             linewidth=0, facecolor=color)
        ax.add_patch(bar)
        ax.text(x + w / 2, y + h * 0.70, title, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=T_DARK, linespacing=1.35)
        ax.text(x + w / 2, y + h * 0.32, "\n".join(lines),
                ha="center", va="center", fontsize=11, color=T_GRAY, linespacing=1.5)

    # Підсумок
    total_box = FancyBboxPatch((15, 10), 70, 16,
                               boxstyle="round,pad=0,rounding_size=2.0",
                               linewidth=1.6, edgecolor="#0071E3",
                               facecolor="#EAF3FF")
    ax.add_patch(total_box)
    ax.text(50, 18, "РАЗОМ: 40 балів",
            ha="center", va="center", fontsize=16, fontweight="bold", color="#0071E3")
    return _save(fig, "tz1_structure")


# -------- Схема 2: Шкала переведення балів --------
def schema_scale():
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 95, "Шкала переведення балів у 12-бальну систему",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    rows = [
        ("36–40 балів", "Високий", "10–12", "#248A3D", "#E8F5EC"),
        ("30–35 балів", "Достатній", "7–9", "#0071E3", "#EAF3FF"),
        ("24–29 балів", "Середній", "4–6", "#C93400", "#FFF4E5"),
        ("0–23 бали",  "Початковий", "1–3", "#C4001D", "#FCE9EA"),
    ]
    x, w, y_start, h, gap = 8, 84, 72, 15, 3
    for i, (rng, level, grade, color, fill) in enumerate(rows):
        y = y_start - i * (h + gap)
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=1.8",
                             linewidth=1.4, edgecolor=C_EDGE, facecolor=fill)
        ax.add_patch(box)
        # кольоровий акцент зліва
        bar = FancyBboxPatch((x + 1.4, y + 1.4), 1.6, h - 2.8,
                             boxstyle="round,pad=0,rounding_size=0.65",
                             linewidth=0, facecolor=color)
        ax.add_patch(bar)
        ax.text(x + 6, y + h / 2, rng,
                ha="left", va="center", fontsize=13, fontweight="bold", color=T_DARK)
        ax.text(x + w * 0.52, y + h / 2, level,
                ha="center", va="center", fontsize=13, color=T_DARK)
        ax.text(x + w - 8, y + h / 2, grade,
                ha="center", va="center", fontsize=15, fontweight="bold", color=color)
    # Заголовки колонок
    ax.text(8 + 6, 90, "Бали",
            ha="left", va="center", fontsize=11.5, fontweight="bold", color=T_GRAY)
    ax.text(8 + 84 * 0.52, 90, "Рівень",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=T_GRAY)
    ax.text(8 + 84 - 8, 90, "Оцінка",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=T_GRAY)
    return _save(fig, "tz2_scale")


# -------- Схема 3: Розподіл часу (90 хв) --------
def schema_time():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(50, 92, "Орієнтовний розподіл часу (90 хв)",
            ha="center", va="center", fontsize=15, fontweight="bold", color=T_DARK)

    parts = [
        ("Рівень 1", "25 хв", A_BLUE, 25),
        ("Рівень 2", "30 хв", A_GREEN, 30),
        ("Рівень 3", "25 хв", A_ORANGE, 25),
        ("Самоперевірка", "10 хв", A_PURPLE, 10),
    ]
    total_w = 90
    x = 5
    y, h = 30, 40
    for label, time, color, width_share in parts:
        w = total_w * width_share / 90
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0,rounding_size=2.0",
                             linewidth=1.4, edgecolor=C_EDGE, facecolor=C_BG)
        ax.add_patch(box)
        bar = FancyBboxPatch((x + 2.4, y + 2.4), w - 4.8, 1.2,
                             boxstyle="round,pad=0,rounding_size=0.55",
                             linewidth=0, facecolor=color)
        ax.add_patch(bar)
        ax.text(x + w / 2, y + h * 0.62, label,
                ha="center", va="center", fontsize=11.5, fontweight="bold", color=T_DARK)
        ax.text(x + w / 2, y + h * 0.30, time,
                ha="center", va="center", fontsize=13, color=color, fontweight="bold")
        x += w
    return _save(fig, "tz3_time")


print("Генерація схем...")
p1 = schema_structure()
p2 = schema_scale()
p3 = schema_time()
print("Схеми збережено в output/")


# ============================================================
#  ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ============================================================
H_COLOR = RGBColor(0x1F, 0x4E, 0x79)
SH_COLOR = RGBColor(0x2E, 0x75, 0xB6)


def set_font(run, size=14, bold=False, italic=False, color=None):
    name = "Times New Roman"
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rfonts.set(qn(attr), name)


def set_default_style(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(14)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.space_after = Pt(4)
    rpr = st.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rfonts.set(qn(attr), "Times New Roman")


def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    set_font(p.add_run(text), size=14, bold=True, color=H_COLOR)


def add_topic(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    set_font(p.add_run(f"Тема: {text}"), size=14, bold=True)


def add_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(5)
    set_font(p.add_run(text), size=14, bold=True, color=H_COLOR)


def add_subheading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    set_font(p.add_run(text), size=14, bold=True, color=SH_COLOR)


def add_para(doc, text, indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if indent:
        p.paragraph_format.first_line_indent = Cm(1.0)
    set_font(p.add_run(text), size=14)


def add_numbered_manual(doc, items):
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_font(p.add_run(f"{i}. {text}"), size=14)


def add_numbered_paren(doc, items):
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_font(p.add_run(f"{i}) {text}"), size=14)


def add_list_number(doc, items):
    for text in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_font(p.add_run(text), size=14)


def add_picture_center(doc, path, width_cm=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(3)
    p.add_run().add_picture(path, width=Cm(width_cm))


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    set_font(run, size=12, italic=True)
    run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)


def shade_cell(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def set_col_width(cell, width_cm):
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn('w:tcW'))
    if tcW is None:
        tcW = OxmlElement('w:tcW')
        tcPr.append(tcW)
    tcW.set(qn('w:w'), str(int(width_cm * 567)))
    tcW.set(qn('w:type'), 'dxa')


def cell_text(cell, text, size=13, bold=False, color=None,
              align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    set_font(p.add_run(text), size=size, bold=bold, color=color)


def style_table(table, widths=None):
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    hdr = table.rows[0]
    set_repeat_header(hdr)
    for cell in hdr.cells:
        shade_cell(cell, "1F4E79")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    if widths:
        for row in table.rows:
            for cell, w in zip(row.cells, widths):
                set_col_width(cell, w)


def add_callout(doc, text, bg="FFF4E5", border="C93400"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_col_width(cell, 16.5)

    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), bg)
    tcPr.append(shd)

    borders = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:color"), border)
    borders.append(left)
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    set_font(p.add_run(text), size=14)
    doc.add_paragraph()


def add_page_number_footer(doc):
    section = doc.sections[0]
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = "PAGE"
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    set_font(run, size=12)


def add_test_question(doc, num, question, options):
    """Питання з вибором однієї правильної відповіді."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_font(p.add_run(f"{num}. {question}"), size=14)
    for letter, text in zip(("а", "б", "в", "г"), options):
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Cm(1.6)
        p2.paragraph_format.space_after = Pt(1)
        p2.paragraph_format.line_spacing = 1.15
        p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_font(p2.add_run(f"{letter}) {text}"), size=14)


# ============================================================
#  ФОРМУВАННЯ ДОКУМЕНТА
# ============================================================
doc = Document()
set_default_style(doc)
add_page_number_footer(doc)

# --- Заголовок і тема ---
add_title(doc, "ТЕМАТИЧНИЙ ЗАЛІК № 4")
add_topic(doc, "Тематичний залік. Контрольна робота.")

# --- Мета ---
add_heading(doc, "Мета")
add_para(
    doc,
    "Систематизувати та узагальнити знання з теми; розвивати здатність "
    "до самооцінювання й самоконтролю; виховувати відповідальне ставлення "
    "до навчальних досягнень. Форма контролю — підсумкове тестування "
    "(контрольна робота)."
)

# --- Обладнання ---
add_heading(doc, "Обладнання та програмне забезпечення")
add_numbered_paren(doc, [
    "інструкційні картки (додаються);",
    "бланк контрольної роботи або персональний комп'ютер із доступом "
    "до засобів тестування;",
    "текстовий редактор (Microsoft Word, Google Docs) для виконання "
    "практичних завдань;",
    "зошит для контрольних робіт та ручка;",
    "калькулятор (за потреби).",
])

# --- Література ---
add_heading(doc, "Література")
add_list_number(doc, [
    "Методичні рекомендації щодо написання та оформлення курсової роботи. "
    "Путивль : КЗСОР «Путивльський педагогічний фаховий коледж "
    "імені С. В. Руднєва», 2024. 14 с.",
    "Дубасенюк О. А. Методологія та методи науково-педагогічного "
    "дослідження. Житомир : Полісся, 2016. 256 с.",
    "Тушева В. В. Основи наукових досліджень. Харків : «Федорко», 2014. 408 с.",
])

# --- Схема загальної структури ---
add_heading(doc, "Загальна структура роботи")
add_para(
    doc,
    "Залік складається з трьох рівнів. Максимальна сума — 40 балів, "
    "які переводяться у 12-бальну шкалу. Час виконання — 90 хв."
)
add_picture_center(doc, p1, width_cm=16.0)
add_caption(doc, "Рис. 1. Загальна структура тематичного заліку (3 рівні + сума балів)")

add_picture_center(doc, p3, width_cm=16.0)
add_caption(doc, "Рис. 2. Орієнтовний розподіл часу виконання")

# ============================================================
#  РІВЕНЬ 1
# ============================================================
add_heading(doc, "Рівень 1. Тестові завдання (20 балів)")

add_subheading(doc, "Частина А. Вибір однієї правильної відповіді (15 × 1 бал)")
add_para(
    doc,
    "У кожному завданні оберіть одну правильну відповідь із чотирьох "
    "запропонованих. За кожну правильну відповідь — 1 бал."
)

test_data = [
    ("Що є предметом дисципліни «Основи науково-педагогічних досліджень»?",
     ["технологія виготовлення підручників",
      "закономірності науково-педагогічного пізнання та методи дослідження",
      "організація дозвілля школярів",
      "методика викладання математики"]),
    ("Який метод дослідження належить до теоретичних?",
     ["спостереження", "анкетування",
      "аналіз наукової літератури", "педагогічний експеримент"]),
    ("Що таке гіпотеза дослідження?",
     ["остаточний висновок дослідження",
      "наукове припущення, яке потребує перевірки",
      "список літератури", "тема дослідження"]),
    ("У якій частині наукової роботи обґрунтовується актуальність теми?",
     ["у висновках", "у вступі", "у списку джерел", "у додатках"]),
    ("Що таке апробація результатів дослідження?",
     ["публічне представлення та перевірка результатів фаховою спільнотою",
      "остаточне оформлення роботи",
      "знищення чорнових матеріалів",
      "переклад роботи іноземною мовою"]),
    ("Який етичний принцип вимагає добровільної участі респондентів?",
     ["прозорість", "чесність",
      "повага до особистості", "об'єктивність"]),
    ("Що таке інклюзивна освіта?",
     ["освіта лише для обдарованих дітей",
      "освіта, що забезпечує рівний доступ до навчання всіх дітей "
      "з урахуванням їхніх потреб",
      "виключно дистанційне навчання",
      "домашня форма навчання"]),
    ("Який цифровий інструмент доцільно використати для збору даних опитування?",
     ["Microsoft Word", "Google Forms",
      "Microsoft Paint", "калькулятор"]),
    ("Що таке впровадження наукових розробок?",
     ["перенесення результатів дослідження в освітню практику",
      "захист дисертації", "написання статті", "рецензування"]),
    ("Яка форма апробації є публічною?",
     ["читання вдома",
      "доповідь на науковій конференції",
      "особистий щоденник", "чорновий запис"]),
    ("Що таке пілотне впровадження?",
     ["масове впровадження в усі школи",
      "експериментальна перевірка розробки в невеликій групі",
      "публікація монографії", "конкурсний відбір"]),
    ("Що таке плагіат?",
     ["коректне цитування",
      "привласнення чужих ідей і тексту без посилання на автора",
      "самостійне написання роботи", "рецензування"]),
    ("Який вид експерименту передбачає активне втручання дослідника "
     "в освітній процес?",
     ["констатувальний", "формувальний", "спостереження", "анкетування"]),
    ("Що таке наукова новизна?",
     ["нова тема дослідження",
      "нові, раніше не відомі науці факти, закономірності чи методи",
      "нова назва роботи", "новий список літератури"]),
    ("Яка вимога до оформлення списку джерел?",
     ["довільний порядок", "лише іноземні джерела",
      "оформлення згідно з чинними вимогами (ДСТУ)",
      "лише електронні ресурси"]),
]
for i, (q, opts) in enumerate(test_data, 1):
    add_test_question(doc, i, q, opts)

# --- Співставлення 5×5 ---
add_subheading(doc, "Частина Б. Завдання на співставлення 5 × 5 (5 балів)")
add_para(
    doc,
    "Установіть відповідність між методом дослідження (1–5) та його "
    "характеристикою (А–Д). За кожну правильну пару — 1 бал. "
    "Відповіді запишіть у таблицю нижче."
)

add_para(doc, "Методи дослідження:", indent=False)
add_numbered_manual(doc, [
    "Спостереження",
    "Анкетування",
    "Педагогічний експеримент",
    "Бесіда",
    "Аналіз документів",
])

add_para(doc, "Характеристики:", indent=False)
for letter, text in [
    ("А", "Активне втручання дослідника у педагогічний процес з метою "
          "перевірки гіпотези"),
    ("Б", "Цілеспрямоване, планомірне сприйняття педагогічних явищ "
          "без втручання в їхній перебіг"),
    ("В", "Опрацювання навчальних програм, зошитів, щоденників, "
          "нормативних актів"),
    ("Г", "Усне опитування в процесі живого спілкування з респондентом"),
    ("Д", "Письмове опитування за стандартизованою формою, "
          "що передбачає самостійне заповнення"),
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_font(p.add_run(f"{letter}) {text}"), size=14)

# Таблиця відповідей
add_para(doc, "Таблиця для запису відповідей:", indent=False)
match_header = ["Метод", "1", "2", "3", "4", "5"]
t = doc.add_table(rows=1, cols=6)
for i, h in enumerate(match_header):
    cell_text(t.rows[0].cells[i], h, size=13, bold=True,
              color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
cells = t.add_row().cells
cell_text(cells[0], "Літера", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
for c in cells[1:]:
    cell_text(c, " ", size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
style_table(t, widths=[3.0, 2.6, 2.6, 2.6, 2.6, 2.6])
doc.add_paragraph()

# ============================================================
#  РІВЕНЬ 2
# ============================================================
add_heading(doc, "Рівень 2. Практичні завдання (12 балів)")
add_para(
    doc,
    "Виконайте три завдання з розгорнутою письмовою відповіддю. "
    "Кожне завдання оцінюється від 0 до 4 балів. Відповіді подавайте "
    "стисло, по суті, з конкретними прикладами зі шкільної практики."
)

add_subheading(doc, "Завдання 1 (4 бали)")
add_para(
    doc,
    "Сформулюйте тему, мету й гіпотезу власного мікродослідження "
    "за обраною проблемою початкової школи (наприклад: "
    "«Використання дидактичної гри на уроках математики в 1 класі»). "
    "Обґрунтуйте актуальність теми (2–3 речення)."
)
add_subheading(doc, "Завдання 2 (4 бали)")
add_para(
    doc,
    "Розробіть план пілотного впровадження обраної наукової розробки "
    "у своєму класі: 4–5 послідовних кроків із зазначенням тривалості "
    "та очікуваного результату. Назвіть 2–3 показники, за якими ви "
    "будете оцінювати результати впровадження."
)
add_subheading(doc, "Завдання 3 (4 бали)")
add_para(
    doc,
    "Опишіть 3–4 етичні норми дослідження з дітьми з особливими "
    "освітніми потребами. Наведіть конкретний приклад ситуації "
    "зі шкільної практики, у якій ці норми мають бути дотримані."
)

# ============================================================
#  РІВЕНЬ 3
# ============================================================
add_heading(doc, "Рівень 3. Творче завдання (8 балів)")
add_para(
    doc,
    "Розробіть мініпроєкт упровадження наукової розробки в освітній "
    "процес початкової школи. Проєкт має містити всі обов'язкові "
    "складові (див. нижче) та бути оформленим у вигляді тексту "
    "обсягом 1–1,5 сторінки."
)
add_numbered_manual(doc, [
    "Тема та короткий опис наукової розробки, яку впроваджуєте.",
    "Мета й завдання впровадження.",
    "Адаптація розробки до умов вашого класу (3–5 конкретних змін).",
    "План пілотного впровадження (4–5 кроків із тривалістю).",
    "Показники оцінювання результатів (2–3 показники).",
    "Ризики впровадження та способи їх уникнення (2–3 ризики).",
    "Форми апробації результатів (2–3 форми).",
])
add_para(
    doc,
    "Додатково (за бажанням, не впливає на бали, але враховується "
    "як якісне оформлення): підготуйте 3–5 слайдів презентації "
    "вашого мініпроєкту."
)

# ============================================================
#  КРИТЕРІЇ ОЦІНЮВАННЯ
# ============================================================
add_heading(doc, "Критерії оцінювання")
crit_header = ["Рівень / критерій", "Максимум балів"]
crit_data = [
    ["Рівень 1. Тестові завдання (15 тестів × 1 бал)", "15"],
    ["Рівень 1. Співставлення 5 × 5 (5 пар × 1 бал)", "5"],
    ["Рівень 2. Практичне завдання 1", "4"],
    ["Рівень 2. Практичне завдання 2", "4"],
    ["Рівень 2. Практичне завдання 3", "4"],
    ["Рівень 3. Творче завдання (мініпроєкт)", "8"],
    ["Разом", "40"],
]
t2 = doc.add_table(rows=1, cols=2)
for i, h in enumerate(crit_header):
    cell_text(t2.rows[0].cells[i], h, size=13, bold=True,
              color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
for row in crit_data:
    cells = t2.add_row().cells
    cell_text(cells[0], row[0], size=13)
    cell_text(cells[1], row[1], size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
style_table(t2, widths=[13.0, 3.5])
last_row = t2.rows[-1]
for cell in last_row.cells:
    shade_cell(cell, "D9E2F3")
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.bold = True
doc.add_paragraph()

# --- Шкала переведення ---
add_subheading(doc, "Шкала переведення балів у 12-бальну систему")
add_picture_center(doc, p2, width_cm=15.5)
add_caption(doc, "Рис. 3. Шкала переведення балів у 12-бальну систему")

# ============================================================
#  ПРАВИЛЬНІ ВІДПОВІДІ (callout у кінці)
# ============================================================
add_heading(doc, "Правильні відповіді на співставлення")
add_callout(
    doc,
    "Завдання на співставлення 5 × 5: "
    "1 — Б, 2 — Д, 3 — А, 4 — Г, 5 — В.",
    bg="E8F5EC", border="248A3D",
)

# --- Збереження ---
OUT = "Tematychnyi_zalik_4_Kontrolna_robota.docx"
doc.save(OUT)
print(f"Готово! Файл збережено: {OUT}")
print("Схеми збережено в папку: output/")