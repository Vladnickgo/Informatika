# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Файлова система. Файли та папки
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "output"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# 1. ГЕНЕРАЦІЯ СХЕМ (matplotlib → PNG + SVG)
# ============================================================

def _save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220,
                bbox_inches="tight", facecolor="white")
    fig.savefig(os.path.join(OUT, name + ".svg"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return os.path.join(OUT, name + ".png")


def scheme_explorer():
    """Схема 1: вікно «Проводника» та основні елементи навігації."""
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 15); ax.set_ylim(0, 9); ax.axis("off")

    # Вікно провідника
    ax.add_patch(FancyBboxPatch((0.5, 0.6), 14, 7.6,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#FFFFFF", edgecolor="#404040",
                                linewidth=2.0))

    # Заголовок вікна
    ax.add_patch(Rectangle((0.5, 7.4), 14, 0.8,
                           facecolor="#1F4E79", edgecolor="#1F4E79"))
    ax.text(0.8, 7.8, "Проводник  —  C:\\Навчання",
            ha="left", va="center", fontsize=11, fontweight="bold", color="white")

    # Адресний рядок
    ax.add_patch(Rectangle((0.5, 6.9), 14, 0.5,
                           facecolor="#F2F2F2", edgecolor="#BFBFBF"))
    ax.text(0.8, 7.15, "C:\\  ›  Навчання  ›",
            ha="left", va="center", fontsize=10, color="#404040")

    # Ліва панель (дерево)
    ax.add_patch(Rectangle((0.5, 0.6), 4.2, 6.3,
                           facecolor="#F7F9FC", edgecolor="#BFBFBF"))
    ax.text(0.75, 6.5, "ДЕРЕВО ПАПОК",
            ha="left", va="center", fontsize=10, fontweight="bold", color="#1F4E79")
    tree_lines = [
        ("📁 Робочий стіл", 0),
        ("📁 Документи", 0),
        ("📁 Завантаження", 0),
        ("💾 Диск C:", 0),
        ("   📁 Навчання", 1),
        ("      📁 Конспекти", 2),
        ("      📁 Звіти", 2),
        ("   📁 Фото", 1),
    ]
    for i, (line, lvl) in enumerate(tree_lines):
        ax.text(0.75 + lvl * 0.45, 5.9 - i * 0.5, line,
                ha="left", va="center", fontsize=9.5, color="#1a1a1a")

    # Права панель (вміст)
    ax.add_patch(Rectangle((4.9, 0.6), 9.6, 6.3,
                           facecolor="#FFFFFF", edgecolor="#BFBFBF"))
    ax.text(5.1, 6.5, "ВМІСТ ПАПКИ  «Навчання»",
            ha="left", va="center", fontsize=10, fontweight="bold", color="#1F4E79")

    content = [
        ("📁", "Конспекти", "Папка з файлами", 5.5),
        ("📁", "Звіти", "Папка з файлами", 4.5),
        ("📄", "план_уроку.docx", "Документ Word", 3.5),
        ("📊", "оцінки.xlsx", "Таблиця Excel", 2.5),
        ("🖼", "схема.png", "Зображення", 1.5),
    ]
    for icon, name, desc, y in content:
        ax.text(5.1, y, icon, fontsize=14, va="center")
        ax.text(5.7, y, name, fontsize=10, fontweight="bold",
                va="center", color="#1a1a1a")
        ax.text(9.2, y, desc, fontsize=9, va="center",
                color="#595959", style="italic")

    # Підписи-виноски
    ax.annotate("Дерево папок", xy=(2.6, 6.3), xytext=(2.6, 8.8),
                ha="center", fontsize=10, fontweight="bold", color="#C55A11",
                arrowprops=dict(arrowstyle="-|>", color="#C55A11", linewidth=1.5))
    ax.annotate("Вміст вибраної папки", xy=(9.7, 6.3), xytext=(10.5, 8.8),
                ha="center", fontsize=10, fontweight="bold", color="#C55A11",
                arrowprops=dict(arrowstyle="-|>", color="#C55A11", linewidth=1.5))

    return _save(fig, "scheme_explorer")


def scheme_paths():
    """Схема 2: абсолютний та відносний шляхи до файлу."""
    fig, ax = plt.subplots(figsize=(11.5, 5.5))
    ax.set_xlim(0, 15); ax.set_ylim(0, 7); ax.axis("off")

    ax.text(7.5, 6.4, "Схема 2. Абсолютний та відносний шляхи до файлу",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")

    # Абсолютний
    ax.add_patch(FancyBboxPatch((0.5, 3.6), 14, 2.1,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#DEEAF6", edgecolor="#2E75B6", linewidth=1.8))
    ax.text(1.0, 5.35, "АБСОЛЮТНИЙ ШЛЯХ (від кореня диска)",
            ha="left", va="center", fontsize=11, fontweight="bold", color="#1F4E79")
    ax.text(1.0, 4.55, "C:\\Навчання\\Конспекти\\лекція_1.docx",
            ha="left", va="center", fontsize=12, family="DejaVu Sans Mono",
            color="#1a1a1a")
    ax.text(1.0, 3.95, "завжди починається з імені диска та символу «\\» — "
                       "працює з будь-якого місця системи",
            ha="left", va="center", fontsize=10, style="italic", color="#595959")

    # Відносний
    ax.add_patch(FancyBboxPatch((0.5, 0.8), 14, 2.1,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#E2EFDA", edgecolor="#548235", linewidth=1.8))
    ax.text(1.0, 2.55, "ВІДНОСНИЙ ШЛЯХ (від поточної папки)",
            ha="left", va="center", fontsize=11, fontweight="bold", color="#375623")
    ax.text(1.0, 1.75, "Конспекти\\лекція_1.docx   або   .\\лекція_1.docx   або   ..\\Фото",
            ha="left", va="center", fontsize=12, family="DejaVu Sans Mono",
            color="#1a1a1a")
    ax.text(1.0, 1.15, "відраховується від папки, у якій зараз перебуває користувач; "
                       "«..» означає «на рівень вище»",
            ha="left", va="center", fontsize=10, style="italic", color="#595959")

    return _save(fig, "scheme_paths")


def scheme_attributes():
    """Схема 3: атрибути файлу (панель властивостей)."""
    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")

    ax.add_patch(FancyBboxPatch((1.0, 0.9), 10, 6.2,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#FFFFFF", edgecolor="#404040",
                                linewidth=1.8))
    ax.add_patch(Rectangle((1.0, 6.4), 10, 0.7,
                           facecolor="#1F4E79", edgecolor="#1F4E79"))
    ax.text(1.4, 6.75, "Властивості: лекція_1.docx",
            ha="left", va="center", fontsize=11, fontweight="bold", color="white")

    rows = [
        ("Тип файлу:", "Документ Microsoft Word (.docx)"),
        ("Розташування:", "C:\\Навчання\\Конспекти"),
        ("Розмір:", "184 КБ (188 416 байт)"),
        ("Створено:", "12.09.2024, 14:22"),
        ("Змінено:", "15.09.2024, 09:48"),
        ("Атрибути:", "☑ Тільки читання   ☐ Прихований   ☐ Архівний"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 5.8 - i * 0.78
        ax.text(1.4, y, k, ha="left", va="center", fontsize=10.5,
                fontweight="bold", color="#1F4E79")
        ax.text(3.7, y, v, ha="left", va="center", fontsize=10.5,
                color="#1a1a1a", family="DejaVu Sans")

    ax.text(6.0, 0.35,
            "Схема 3. Основні атрибути файлу у властивостях ОС Windows",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#1F4E79")
    return _save(fig, "scheme_attributes")


def scheme_levels():
    """Схема 4: три рівні практичних завдань."""
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")

    ax.text(8, 8.4, "Схема 4. Трирівнева система практичних завдань",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")

    cards = [
        ("РІВЕНЬ 1\nРепродуктивний",
         "Створити папку, файл,\nперейменувати,\nскопіювати, видалити",
         "#548235", "#E2EFDA", "≈ 5 хв"),
        ("РІВЕНЬ 2\nПродуктивний",
         "Побудувати ієрархію\nпапок, перемістити файли,\nзмінити атрибути",
         "#BF8F00", "#FFF2CC", "≈ 10 хв"),
        ("РІВЕНЬ 3\nТворчий",
         "Спроєктувати структуру\nпапок для вчителя\nпочаткової школи",
         "#C55A11", "#FBE5D6", "≈ 10 хв"),
    ]

    card_w, card_h = 4.6, 5.6
    gap = 0.6
    x0 = (16 - (3 * card_w + 2 * gap)) / 2
    y0 = 1.7

    for i, (title, body_txt, accent, fill, time) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        ax.add_patch(FancyBboxPatch((x, y0), card_w, card_h,
                                    boxstyle="round,pad=0.02,rounding_size=0.2",
                                    facecolor=fill, edgecolor=accent, linewidth=2.0))
        ax.add_patch(FancyBboxPatch((x, y0 + card_h - 1.5), card_w, 1.5,
                                    boxstyle="round,pad=0.02,rounding_size=0.2",
                                    facecolor=accent, edgecolor=accent,
                                    linewidth=2.0))
        ax.text(x + card_w / 2, y0 + card_h - 0.75, title,
                ha="center", va="center", fontsize=11, fontweight="bold",
                color="white", linespacing=1.4)
        ax.text(x + card_w / 2, y0 + card_h / 2 - 0.2, body_txt,
                ha="center", va="center", fontsize=10, color="#1a1a1a",
                linespacing=1.5)
        ax.text(x + card_w / 2, y0 + 0.35, "⏱ " + time,
                ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=accent)

    # Стрілка вгору
    ax.annotate("", xy=(14.9, 7.0), xytext=(14.9, 2.1),
                arrowprops=dict(arrowstyle="-|>", color="#404040",
                                linewidth=2.0, mutation_scale=18))
    ax.text(15.25, 4.55, "Складність ↑", ha="left", va="center",
            fontsize=10, fontweight="bold", color="#404040", rotation=90)

    ax.text(8, 0.5,
            "Студент виконує завдання послідовно; оцінка залежить від кількості "
            "успішно виконаних рівнів",
            ha="center", va="center", fontsize=10, style="italic", color="#595959")
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


def callout(doc, title, text, fill="EAF2F8", accent="2E75B6"):
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
    img1 = scheme_explorer()
    img2 = scheme_paths()
    img3 = scheme_attributes()
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

    # ---------- Заголовок ----------
    h1(doc, "Практичне заняття")
    h1(doc, "Файлова система. Файли та папки")

    body(doc, "«Основи операційних систем» · спеціальність 013 Початкова освіта "
              "(Вчитель інформатики початкової школи)", space_after=10)

    # ---------- Мета ----------
    h2(doc, "Мета")
    body(doc, "закріпити знання про логічну структуру файлової системи, атрибути "
              "файлів та організацію папок; розвивати вміння практично "
              "застосовувати навігацію файловою структурою у графічному "
              "середовищі; виховувати дисциплінованість під час роботи з "
              "файловою системою задля уникнення втрати даних.")

    # ---------- Обладнання / ПЗ ----------
    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11 або Linux (графічне середовище).",
        "Файловий менеджер «Проводник» (Windows) / Nautilus (Linux).",
        "Інструкційні картки до рівнів 1–3 (додаються).",
        "Текстовий редактор (MS Word / LibreOffice Writer) для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці», Flameshot тощо).",
    ]
    for e in equipment:
        bullet(doc, e)

    # ---------- Література ----------
    h2(doc, "Література")
    sources = [
        "Погребняк Б. І., Булаєнко М. В. Операційні системи : навч. посіб. — "
        "Харків : ХНУМГ ім. О. М. Бекетова, 2018.",
        "Сільвестр В., Гансен П. Основи операційних систем. — Київ : Нова Книга, 2016.",
        "Таненбаум Е., Бос Г. Операційні системи: проектування та реалізація. — "
        "Київ : Вильямс, 2015.",
    ]
    for s in sources:
        bullet(doc, s)

    # =========================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =========================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Файлова система та її логічна структура")
    body(doc, "Файлова система — це частина операційної системи, що забезпечує "
              "зберігання, пошук та впорядкування файлів і папок на носіях "
              "інформації. Логічно файлова система має ієрархічну (деревоподібну) "
              "будову: на найвищому рівні — диск (кореневий каталог), нижче — "
              "папки першого рівня, у них — папки другого рівня і т. д. "
              "На найнижчому рівні — файли. Така структура дозволяє швидко "
              "знаходити потрібні дані та уникнути безладу на диску.")

    add_figure(doc, img1, 16.0)

    body(doc, "Для навігації у файловій системі користувач використовує файловий "
              "менеджер — програму з графічним інтерфейсом, яка показує дерево "
              "папок і вміст вибраної папки (див. схему 1). Основні елементи "
              "навігації: адресний рядок, дерево папок, панель вмісту, кнопки "
              "«Назад», «Уперед», «Вгору».")

    h3(doc, "2. Файли, папки, ярлики")
    body(doc, "Файл — поіменована область на носії, що містить дані. Папка "
              "(каталог) — контейнер для групування файлів та інших папок. "
              "Ярлик — невеликий файл-посилання, який указує на інший об'єкт і "
              "не містить самих даних. Ярлики зручні для швидкого доступу до "
              "часто використовуваних програм чи папок.")

    h3(doc, "3. Шляхи до файлів")
    body(doc, "Шлях — це послідовність папок, яку треба пройти від початкової "
              "точки до файлу. Розрізняють абсолютний та відносний шляхи.")

    add_figure(doc, img2, 15.5)

    h3(doc, "4. Атрибути файлів")
    body(doc, "Кожен файл має набір характеристик, які називаються атрибутами. "
              "Вони визначають, як система й користувач можуть поводитися з "
              "файлом. Основні атрибути подано на схемі 3.")

    add_figure(doc, img3, 15.5)

    add_table(
        doc,
        ["Атрибут", "Що означає", "Практичний ефект"],
        [
            ["Ім'я", "Унікальна назва файлу разом з розширенням",
             "Використовується для пошуку й запуску"],
            ["Розмір", "Обсяг даних у байтах / кілобайтах",
             "Допомагає оцінити місце на диску"],
            ["Дата створення / змінення", "Час останньої зміни вмісту",
             "Дозволяє знайти останню версію роботи"],
            ["«Тільки читання»", "Заборона редагування", "Захищає важливі дані від випадкової зміни"],
            ["«Прихований»", "Файл не видно у звичайному режимі",
             "Використовується для системних файлів"],
            ["«Архівний»", "Файл потребує резервного копіювання",
             "Використовується програмами архівування"],
        ],
        widths=[4.4, 6.0, 6.1],
    )

    h3(doc, "5. Безпека роботи з файловою системою")
    body(doc, "Недбале поводження з файлами призводить до втрати даних. "
              "Дотримуйтеся трьох правил: перед видаленням перевіряйте, що "
              "об'єкт не потрібен; регулярно створюйте резервні копії важливих "
              "документів; не перейменовуйте й не переміщуйте системні файли.")

    callout(doc, "Методична підказка.",
            "Під час пояснення учням початкової школи доречно порівнювати файл "
            "із зошитом, папку — з полицею у шафі, а шлях — з адресою, за якою "
            "можна знайти цей зошит. Таке порівняння легко продемонструвати "
            "наочними предметами в класі.",
            fill="FFF4E5", accent="C55A11")

    # =========================================================
    # ХІД ЗАНЯТТЯ
    # =========================================================
    h2(doc, "Хід заняття")
    stages = [
        ("1. Організаційний момент (2 хв). ",
         "Перевірка присутності, готовності робочих місць, інструктаж з "
         "техніки безпеки під час роботи з комп'ютером."),
        ("2. Актуалізація опорних знань (5 хв). ",
         "Бесіда за питаннями: що таке файл, папка, ярлик; які атрибути "
         "файлу ви знаєте; для чого потрібен файловий менеджер."),
        ("3. Мотивація навчальної діяльності (3 хв). ",
         "Повідомлення теми, мети, завдань заняття. Постановка проблемного "
         "завдання: «Як організувати папки на робочому диску вчителя так, "
         "щоб швидко знаходити матеріали до уроку?»"),
        ("4. Вивчення теоретичних відомостей (10 хв). ",
         "Огляд будови файлової системи, шляхів до файлів, атрибутів. "
         "Робота зі схемами 1–3."),
        ("5. Виконання практичних завдань за рівнями (25 хв). ",
         "Рівень 1 — 5 хв, рівень 2 — 10 хв, рівень 3 — 10 хв. "
         "Студенти працюють за інструкційними картками."),
        ("6. Підбиття підсумків, рефлексія (5 хв). ",
         "Обговорення труднощів, самоперевірка, оголошення критеріїв "
         "оцінювання."),
    ]
    for lead, txt in stages:
        bullet(doc, txt, bold_lead=lead)

    # =========================================================
    # ПОКРОКОВИЙ АЛГОРИТМ РІЗНОРІВНЕВИХ ЗАВДАНЬ
    # =========================================================
    h2(doc, "Покроковий алгоритм виконання різнорівневих завдань")

    body(doc, "Практична частина заняття побудована за трирівневою системою "
              "(схема 4). Студент виконує завдання послідовно; час виконання "
              "кожного рівня — 5–10 хвилин, загальна тривалість практичної "
              "частини — до 25 хвилин. Оцінка залежить від кількості успішно "
              "виконаних рівнів.")

    add_figure(doc, img4, 16.0)

    # -------- Рівень 1 --------
    h3(doc, "Рівень 1 — репродуктивний (≈ 5 хв)",
       color=RGBColor(0x54, 0x82, 0x35))
    body(doc, "Мета: відпрацювати базові операції з файлами та папками у "
              "файловому менеджері.")

    add_table(
        doc,
        ["№", "Крок", "Дія"],
        [
            ["1", "Відкрийте Проводник",
             "Клацніть ярлик «Проводник» на панелі завдань або натисніть "
             "Win+E."],
            ["2", "Перейдіть на робочий диск",
             "У дереві папок оберіть диск C: або D: (за вказівкою викладача)."],
            ["3", "Створіть папку",
             "Права кнопка миші → «Створити» → «Папку». Введіть ім'я "
             "«Практика_ПІБ» (наприклад: Практика_Іваненко)."],
            ["4", "Відкрийте створену папку",
             "Двічі клацніть лівою кнопкою миші на папці."],
            ["5", "Створіть текстовий файл",
             "Права кнопка → «Створити» → «Текстовий документ». "
             "Назвіть його «Перший_файл.txt»."],
            ["6", "Перейменуйте файл",
             "Виділіть файл → права кнопка → «Перейменувати». "
             "Введіть ім'я «Звіт.txt»."],
            ["7", "Скопіюйте файл",
             "Виділіть файл → Ctrl+C → у папці «Практика_ПІБ» натисніть "
             "Ctrl+V. Переконайтеся, що копія має ім'я «Звіт — копія.txt»."],
            ["8", "Видаліть файл-копію",
             "Виділіть копію → клавіша Delete або Shift+Delete."],
            ["9", "Зробіть скріншот",
             "Натисніть Print Screen; вставте у звіт з поясненням дій."],
        ],
        widths=[1.0, 5.0, 10.5],
    )

    callout(doc, "Контроль.",
            "Після виконання рівня 1 у папці «Практика_ПІБ» має залишитися "
            "один файл «Звіт.txt». Якщо є зайві об'єкти — видаліть їх. "
            "Зробіть скріншот папки та підпишіть його.",
            fill="E2EFDA", accent="548235")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — продуктивний (≈ 10 хв)",
       color=RGBColor(0xBF, 0x8F, 0x00))
    body(doc, "Мета: навчитися будувати ієрархічну структуру папок, "
              "переміщувати файли та змінювати їхні атрибути.")

    add_table(
        doc,
        ["№", "Крок", "Дія"],
        [
            ["1", "Побудуйте структуру папок",
             "Усередині папки «Практика_ПІБ» створіть три папки: «Документи», "
             "«Фото», «Архів»."],
            ["2", "Створіть підпапки",
             "У папці «Документи» створіть підпапки «Звіти» та «Плани»."],
            ["3", "Створіть файли",
             "У «Документи\\Звіти» створіть файл «Тиждень_1.docx». "
             "У «Документи\\Плани» — файл «План_уроку.docx»."],
            ["4", "Перемістіть файл",
             "Виділіть «Тиждень_1.docx» → Ctrl+X → перейдіть до папки «Архів» "
             "→ Ctrl+V. Перевірте, що файл зник з початкової папки."],
            ["5", "Змініть атрибут",
             "Виділіть «План_уроку.docx» → права кнопка → «Властивості» → "
             "позначте «Тільки читання» → ОК. Спробуйте змінити вміст файлу — "
             "переконайтеся, що система попереджає."],
            ["6", "Поверніть атрибут",
             "Зніміть позначку «Тільки читання» у властивостях файлу."],
            ["7", "Скопіюйте шлях",
             "Виділіть файл → Shift + права кнопка → «Копіювати як шлях». "
             "Вставте шлях у звіт."],
            ["8", "Зробіть скріншот",
             "Знімок дерева папок у Проводнику з розгорнутими папками."],
        ],
        widths=[1.0, 5.0, 10.5],
    )

    callout(doc, "Контроль.",
            "У звіті має бути: структура папок (скріншот), абсолютний шлях до "
            "файлу «План_уроку.docx», коротке пояснення різниці між "
            "копіюванням і переміщенням.",
            fill="FFF2CC", accent="BF8F00")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — творчий (≈ 10 хв)",
       color=RGBColor(0xC5, 0x5A, 0x11))
    body(doc, "Мета: спроєктувати власну структуру папок для вчителя початкової "
              "школи та обґрунтувати її доцільність.")

    body(doc, "Завдання. Уявіть, що ви — вчитель початкової школи. Розробіть "
              "структуру папок на своєму робочому диску (не менше трьох рівнів "
              "вкладеності), яка дозволяла б швидко знаходити матеріали до "
              "уроків, зберігати зразки робіт учнів, фотографії зі свят та "
              "методичні матеріали. Створіть цю структуру у файловому менеджері.")

    body(doc, "Орієнтовні складники структури (можна доповнювати):")
    bullet(doc, "«1_Клас», «2_Клас», «3_Клас», «4_Клас» — матеріали за класами;")
    bullet(doc, "«Розробки_уроків» — плани-конспекти за темами;")
    bullet(doc, "«Роботи_учнів» — зразки виконаних завдань;")
    bullet(doc, "«Фотозвіти» — зображення з заходів;")
    bullet(doc, "«Методична_скарбничка» — ігри, вправи, дидактичні матеріали;")
    bullet(doc, "«Звітність» — документи для адміністрації.")

    body(doc, "Додатково в звіт додайте:")
    numbered(doc, "схему або скріншот розробленої структури папок (обов'язково "
                  "з підписами рівнів);")
    numbered(doc, "коротке обґрунтування (5–7 речень), чому саме така "
                  "структура є зручною для вчителя початкової школи;")
    numbered(doc, "одну пораду учням 3–4 класу щодо збереження файлів, "
                  "сформульовану доступною мовою.")

    callout(doc, "Творче ускладнення (за бажанням, +1 бал).",
            "Додайте до структури папку «Учні_з_особливими_потребами» та "
            "поясніть, як у її назві врахувати вимоги конфіденційності.",
            fill="FBE5D6", accent="C55A11")

    # =========================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =========================================================
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Рівень / критерій", "Показник", "Бали"],
        [
            ["Рівень 1", "Усі 9 кроків виконано правильно, є скріншот",
             "3"],
            ["Рівень 2", "Створено повну структуру, правильно виконано "
                         "переміщення, зміну атрибутів, скопійовано шлях",
             "4"],
            ["Рівень 3", "Структура логічна, містить ≥3 рівні, додано "
                         "обґрунтування та пораду для учнів",
             "4"],
            ["Якість звіту", "Оформлення за вимогами, наявність підписів до "
                             "скріншотів",
             "1"],
            ["Творчий підхід", "Додаткові елементи структури, оригінальна "
                               "порада, ускладнення",
             "1"],
        ],
        widths=[4.4, 10.1, 2.0],
    )

    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 балів — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (завдання потребує доопрацювання).")

    # =========================================================
    # ФОРМА ЗВІТНОСТІ
    # =========================================================
    h2(doc, "Форма звітності")
    body(doc, "Результати практичного заняття оформлюються у вигляді "
              "електронного звіту в текстовому редакторі. Звіт повинен містити "
              "такі обов'язкові частини:")
    report_parts = [
        "Титульна сторінка: навчальний заклад, тема, ПІБ студента, група, "
        "ПІБ викладача, дата.",
        "Короткі відповіді на контрольні питання кожного рівня (письмово).",
        "Скріншоти результатів: після рівня 1 (вміст папки), після рівня 2 "
        "(дерево папок + шлях до файлу), після рівня 3 (спроєктована "
        "структура).",
        "Опис виконаних дій до кожного скріншота (1–2 речення).",
        "Структура папок для вчителя початкової школи та її обґрунтування "
        "(рівень 3).",
        "Висновок: що нового закріпили на практиці, які труднощі виникли, "
        "як використаєте набуті вміння у роботі з учнями.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, шрифт "
              "Times New Roman 14 pt, інтервал 1,15, поля 2 см, обсяг — "
              "3–5 сторінок без титульної. Ім'я файлу: "
              "«Практика_Файлова_система_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    callout(doc, "Порада викладачу.",
            "На етапі перевірки звітів звертайте увагу не лише на технічну "
            "правильність дій, а й на те, чи вміє студент пояснити учням "
            "початкової школи поняття «файл», «папка», «шлях» доступною "
            "мовою. Найкращі приклади обговоріть на наступному занятті та "
            "включіть до методичної скарбнички групи.",
            fill="E2EFDA", accent="548235")

    doc.save("Практичне_заняття_Файлова_система.docx")
    print("Готово: Практичне_заняття_Файлова_система.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()