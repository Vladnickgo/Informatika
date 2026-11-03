# -*- coding: utf-8 -*-
"""
Генератор методичного матеріалу
Самостійна робота № 11. Створення макросів в текстовому редакторі Word
Запуск:  python selfwork_11_macros.py
Результат: Самостійна_робота_11_Макроси_Word.docx + папка output/ зі схемами (PNG + SVG)
"""

import os

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

# ----------------------------------------------------------------------------
# Загальні налаштування
# ----------------------------------------------------------------------------
OUT = "output"
DOCX_NAME = "Самостійна_робота_11_Макроси_Word.docx"

FONT = "Times New Roman"
DARK_BLUE = RGBColor(0x1F, 0x4E, 0x79)
MID_BLUE = RGBColor(0x2E, 0x75, 0xB6)
CODE_RED = RGBColor(0xC0, 0x39, 0x2B)
GRAY = RGBColor(0x59, 0x59, 0x59)

# палітра для схем (стиль Apple)
CARD_BG = "#F5F5F7"
CARD_EDGE = "#E5E5EA"
TEXT_DARK = "#1D1D1F"
TEXT_GRAY = "#86868B"
BLUE = "#0071E3"
GREEN = "#248A3D"
ORANGE = "#C93400"
RED = "#C4001D"
ARROW_GRAY = "#C7C7CC"

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


# ============================================================================
# 1. СХЕМИ (matplotlib -> PNG + SVG)
# ============================================================================
def _canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax


def _card(ax, x, y, w, h, lines, bg=CARD_BG, edge=CARD_EDGE, rs=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%s" % rs,
                                linewidth=1.4, edgecolor=edge,
                                facecolor=bg, zorder=2))
    if not lines:
        return
    n = len(lines)
    top = y + h - 0.2
    bottom = y + 0.2
    if n == 1:
        ys = [(top + bottom) / 2.0]
    else:
        step = (top - bottom) / (n - 1)
        ys = [top - i * step for i in range(n)]
    for (text, size, color, weight), yy in zip(lines, ys):
        ax.text(x + w / 2.0, yy, text, ha="center", va="center",
                fontsize=size, color=color, fontweight=weight,
                multialignment="center", zorder=3)


def _arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_GRAY, lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=12),
                zorder=1)


def _save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=220,
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(os.path.join(OUT, name + ".svg"),
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


def scheme_idea():
    """Схема 1. Що таке макрос."""
    fig, ax = _canvas(6.3, 2.5)
    ax.text(0.85, 2.32, "Ваші дії", ha="center", va="center",
            fontsize=9.5, color=TEXT_GRAY)

    steps = ["Виділити текст", "Змінити шрифт", "Додати колір"]
    ys = [1.6, 0.85, 0.1]
    for text, yy in zip(steps, ys):
        _card(ax, 0.1, yy, 1.5, 0.5,
              [(text, 9.5, TEXT_DARK, "normal")], rs=0.1)

    _arrow(ax, 1.63, 1.1, 2.03, 1.1)

    _card(ax, 2.1, 0.35, 1.9, 1.5, [
        ("МАКРОС", 12.5, BLUE, "bold"),
        ("збережена", 9.5, TEXT_DARK, "normal"),
        ("послідовність дій", 9.5, TEXT_DARK, "normal"),
    ])

    _arrow(ax, 4.03, 1.1, 4.43, 1.1)

    _card(ax, 4.5, 0.5, 1.7, 1.2, [
        ("Один клік", 10.5, GREEN, "bold"),
        ("результат", 9.5, TEXT_DARK, "normal"),
        ("готовий", 9.5, TEXT_DARK, "normal"),
    ])
    _save(fig, "scheme_01_macro_idea")


def scheme_steps():
    """Схема 2. Етапи створення макросу (вертикальний степпер)."""
    fig, ax = _canvas(6.3, 3.0)
    items = [
        "Увімкнути вкладку «Розробник»",
        "Записати макрос і задати його ім'я",
        "Призначити кнопку або сполучення клавіш",
        "Перевірити роботу на різних фрагментах",
        "Зберегти документ у форматі .docm",
    ]
    y = 0.1
    for i, text in enumerate(items, 1):
        _card(ax, 0.1, y, 6.1, 0.46, [], rs=0.12)
        ax.text(0.42, y + 0.23, str(i), ha="center", va="center",
                fontsize=11.5, color=BLUE, fontweight="bold", zorder=3)
        ax.text(0.78, y + 0.23, text, ha="left", va="center",
                fontsize=10.5, color=TEXT_DARK, zorder=3)
        y += 0.56
    _save(fig, "scheme_02_macro_steps")


def scheme_security():
    """Схема 3. Рівні безпеки макросів."""
    fig, ax = _canvas(6.3, 1.9)
    items = [
        ("Вимкнути всі макроси", "максимальна безпека",
         "макроси не запускаються", RED),
        ("Сповіщення про макроси", "рекомендований режим",
         "запит на запуск", BLUE),
        ("Увімкнути всі макроси", "для перевірених файлів",
         "підвищений ризик", ORANGE),
    ]
    w, gap, y, h = 1.9, 0.2, 0.2, 1.5
    x = 0.15
    for title, s1, s2, accent in items:
        _card(ax, x, y, w, h, [
            (title, 10.5, accent, "bold"),
            (s1, 9, TEXT_GRAY, "normal"),
            (s2, 9, TEXT_DARK, "normal"),
        ])
        x += w + gap
    _save(fig, "scheme_03_security")


def scheme_vba():
    """Схема 4. Структура процедури VBA (термінал)."""
    fig, ax = _canvas(6.3, 2.9)
    ax.add_patch(FancyBboxPatch((0.15, 0.15), 6.0, 2.55,
                                boxstyle="round,pad=0,rounding_size=0.16",
                                linewidth=1.4, edgecolor="#3A3A3C",
                                facecolor="#1C1C1E", zorder=2))
    ax.text(0.4, 2.45, "Module1", fontsize=9, color="#86868B",
            family="monospace", ha="left", va="center", zorder=3)

    rows = [
        ("Sub FormatTitle()", "назва процедури"),
        ("    ' коментар до макросу", "коментар (апостроф)"),
        ("    Selection.Font.Bold = True", "властивість об'єкта"),
        ("    Selection.Font.Size = 16", "нове значення"),
        ("End Sub", "кінець процедури"),
    ]
    y = 2.05
    for code, note in rows:
        color = "#6E6E73" if code.strip().startswith("'") else "#FFFFFF"
        ax.text(0.4, y, code, fontsize=9.5, color=color, family="monospace",
                ha="left", va="center", zorder=3)
        ax.text(3.35, y, note, fontsize=9, color="#86868B",
                family="sans-serif", ha="left", va="center", zorder=3)
        y -= 0.4
    _save(fig, "scheme_04_vba")


def scheme_stages():
    """Схема 5. Етапи виконання самостійної роботи."""
    fig, ax = _canvas(6.3, 1.7)
    items = [("Опрацювати", "теорію"), ("Виконати", "практику"),
             ("Оформити", "звіт"), ("Подати", "на перевірку")]
    w, gap, y, h = 1.35, 0.25, 0.15, 1.25
    x = 0.1
    for i, (t1, t2) in enumerate(items):
        _card(ax, x, y, w, h, [
            (str(i + 1), 9.5, TEXT_GRAY, "normal"),
            (t1, 10.5, TEXT_DARK, "bold"),
            (t2, 9.5, TEXT_GRAY, "normal"),
        ], rs=0.1)
        if i < 3:
            _arrow(ax, x + w + 0.02, y + h / 2, x + w + gap - 0.02, y + h / 2)
        x += w + gap
    _save(fig, "scheme_05_stages")


def build_schemes():
    os.makedirs(OUT, exist_ok=True)
    scheme_idea()
    scheme_steps()
    scheme_security()
    scheme_vba()
    scheme_stages()


# ============================================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ DOCX
# ============================================================================
def set_run(run, size=14, bold=False, italic=False, color=None, name=FONT):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)
    rFonts.set(qn("w:eastAsia"), name)


def setup_styles(doc):
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(14)
    rPr = st.element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT)
    pf = st.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(0)
    pf.space_after = Pt(5)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def para(doc, text="", size=14, bold=False, italic=False, color=None,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5,
         left_indent=None, first_line=None, name=FONT):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    if left_indent is not None:
        pf.left_indent = left_indent
    if first_line is not None:
        pf.first_line_indent = first_line
    if text:
        r = p.add_run(text)
        set_run(r, size=size, bold=bold, italic=italic, color=color, name=name)
    return p


def para_rich(doc, parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
              space_before=0, space_after=5):
    """parts: список кортежів (текст, "text" | "code")."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    for text, kind in parts:
        r = p.add_run(text)
        if kind == "code":
            set_run(r, size=13, name="Consolas", color=CODE_RED)
        else:
            set_run(r, size=14)
    return p


def heading(doc, text, color=DARK_BLUE, size=14, space_before=12,
            space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT):
    return para(doc, text, size=size, bold=True, color=color, align=align,
                space_before=space_before, space_after=space_after)


def subheading(doc, text):
    return para(doc, text, size=14, bold=True, color=MID_BLUE,
                align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=4)


def numbered_paren(doc, items):
    for i, item in enumerate(items, 1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-0.6)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run("%d) " % i), size=14)
        set_run(p.add_run(item), size=14)


def num_list(doc, items, start=1):
    for i, item in enumerate(items, start):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-0.6)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run("%d. " % i), size=14)
        set_run(p.add_run(item), size=14)


def literature_list(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run(item), size=14)


def bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_run(p.add_run(item), size=14)


def set_cell_bg(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def callout(doc, text, fill="EAF2FB", accent="0071E3"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.0)
    tcPr = cell._tc.get_or_add_tcPr()

    borders = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), accent)
    borders.append(left)
    for edge in ("top", "bottom", "right"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "nil")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tcPr.append(borders)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

    p = cell.paragraphs[0]
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing = 1.15
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    set_run(p.add_run(text), size=13.5)
    return tbl


def styled_table(doc, headers, rows, widths, font_size=12,
                 code_cols=(), center_cols=(0,)):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    tblPr = tbl._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.insert_element_before(layout, "w:tblCellMar", "w:tblLook",
                                "w:tblCaption", "w:tblDescription")

    hdr = tbl.rows[0]
    trPr = hdr._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)

    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = Cm(widths[i])
        set_cell_bg(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        set_run(p.add_run(h), size=font_size, bold=True,
                color=RGBColor(0xFF, 0xFF, 0xFF))

    for row in rows:
        cells = tbl.add_row().cells
        for i, val in enumerate(row):
            cells[i].width = Cm(widths[i])
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            if i in center_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if not val:
                continue
            if i in code_cols:
                set_run(p.add_run(val), size=font_size - 1, name="Consolas",
                        color=CODE_RED)
            else:
                set_run(p.add_run(val), size=font_size)
    return tbl


def add_page_numbers(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run(run, size=12, color=GRAY)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)


def add_scheme(doc, filename, caption, width_cm=16.0):
    path = os.path.join(OUT, filename)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    set_run(cap.add_run(caption), size=12, italic=True, color=GRAY)


# ============================================================================
# 3. ЗБІРКА ДОКУМЕНТА
# ============================================================================
def build_document():
    doc = Document()
    setup_styles(doc)

    sec = doc.sections[0]
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(1.5)
    add_page_numbers(sec)

    # --- Заголовок -----------------------------------------------------------
    heading(doc, "САМОСТІЙНА РОБОТА № 11",
            align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4)
    para(doc, "Тема: Створення макросів в текстовому редакторі Word",
         bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    # --- Мета ----------------------------------------------------------------
    heading(doc, "Мета")
    para(doc, "Формувати навички запису та виконання макросів у Word, "
              "призначати макроси на кнопки або клавіші. Розвивати вміння "
              "оптимізувати повторювані дії, логічне мислення. Виховувати "
              "прагнення до підвищення продуктивності праці, раціонального "
              "використання часу.")

    # --- Обладнання ----------------------------------------------------------
    heading(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "персональний комп'ютер або ноутбук;",
        "текстовий редактор Microsoft Word 2016 / 2019 / 2021 або Microsoft 365;",
        "інструкційні картки до заняття;",
        "файл-заготовка «Зразок_тексту.docx» із трьома фрагментами тексту;",
        "доступ до мережі Інтернет (довідкова система Microsoft, навчальні відео).",
    ])

    # --- Література ----------------------------------------------------------
    heading(doc, "Література")
    literature_list(doc, [
        "Шумілова І. Ф. Новітні технології викладання освітніх галузей "
        "у початковій школі : навч. посіб. Київ : Олді, 2023. 248 с.",
        "Юнчик В. Л. Системне, прикладне програмне забезпечення та хмарні "
        "технології в освіті : конспект лекцій для студентів спеціальності "
        "014.09 Середня освіта (Інформатика) першого (бакалаврського) рівня. "
        "Волин. нац. ун-т ім. Лесі Українки. Луцьк : ВНУ імені Лесі Українки, "
        "2024. 162 с.",
        "Анісімов А. В., Кулябко П. П. Інформаційні системи та бази даних : "
        "навч. посіб. для студ. ф-ту комп'ютер. наук та кібернетики. Київ, "
        "2017. 110 с.",
    ])

    # --- Завдання самостійної роботи -----------------------------------------
    heading(doc, "Завдання самостійної роботи")
    num_list(doc, [
        "Опрацювати теоретичні відомості щодо призначення макросів та "
        "середовища VBA у текстовому редакторі Word.",
        "Увімкнути вкладку «Розробник» і встановити рівень безпеки макросів "
        "«Сповіщення про макроси».",
        "Записати макрос FormatTitle, який робить виділений текст "
        "напівжирним, установлює розмір шрифту 16 pt, змінює колір на "
        "темно-синій та додає відступ 6 pt перед абзацом.",
        "Призначити записаний макрос на кнопку панелі швидкого доступу та на "
        "сполучення клавіш Ctrl+Shift+T; перевірити його роботу.",
        "Записати макрос NumberList із відносним посиланням, який перетворює "
        "поточний абзац на нумерований список, і виконати його для трьох "
        "різних фрагментів документа.",
        "Відкрити макрос у редакторі VBA, доповнити код коментарями, змінити "
        "розмір шрифту, зберегти документ у форматі .docm та оформити звіт.",
    ])

    # --- Терміни виконання ---------------------------------------------------
    heading(doc, "Терміни виконання")
    para(doc, "Робота виконується протягом тижня після практичного заняття. "
              "Звіт (документ із записаними макросами у форматі .docm та "
              "текстовий звіт у форматі .docx або .pdf) подається на "
              "наступному занятті до початку аудиторної роботи. Максимальна "
              "кількість балів за роботу — 13.")

    # --- Очікувані результати ------------------------------------------------
    heading(doc, "Очікувані результати")
    bullets(doc, [
        "налаштовувати стрічку Word та рівень безпеки макросів;",
        "записувати макроси з абсолютними та відносними посиланнями;",
        "призначати макроси на кнопку панелі швидкого доступу та на "
        "сполучення клавіш;",
        "читати й редагувати процедури VBA, додавати коментарі;",
        "обирати правильний формат збереження документа (.docx або .docm);",
        "оцінювати ефект автоматизації повторюваних дій та оформлювати звіт.",
    ])

    # --- Перелік опрацьовуваних питань --------------------------------------
    heading(doc, "Перелік опрацьовуваних питань")
    num_list(doc, [
        "Поняття макросу та його роль в автоматизації роботи з документами.",
        "Історія появи макросів; мова програмування VBA.",
        "Вкладка «Розробник»: інструменти та їх призначення.",
        "Рівні безпеки макросів і правила роботи з файлами з Інтернету.",
        "Порядок запису макросу: ім'я, місце збереження, опис дій.",
        "Абсолютні та відносні посилання під час запису макросу.",
        "Призначення макросу на кнопку панелі швидкого доступу.",
        "Призначення макросу на сполучення клавіш.",
        "Редактор VBA: структура процедури Sub … End Sub, коментарі, змінні.",
        "Формати збереження документів із макросами та типові помилки "
        "початківців.",
    ])

    # --- Теоретичні відомості ------------------------------------------------
    heading(doc, "Теоретичні відомості (стислий огляд)")

    subheading(doc, "1.1. Поняття макросу")
    para(doc, "Макрос — це збережена послідовність команд і дій користувача, "
              "яку текстовий редактор виконує автоматично за однією командою. "
              "Замість того щоб щоразу вручну виділяти заголовок, змінювати "
              "шрифт, колір і відступ, достатньо один раз записати ці дії — і "
              "надалі вони повторюватимуться за один клік або натискання "
              "сполучення клавіш.")
    para(doc, "У шкільній практиці макроси доречні там, де є повторювані "
              "однотипні операції: оформлення карток завдань, створення "
              "однакових заголовків у роздаткових матеріалах, нумерація "
              "списків, вставлення шаблонних рамок і таблиць. Уявіть, що "
              "вчитель готує 30 карток із завданнями й кожну треба "
              "відформатувати однаково: запис дій у макрос перетворює "
              "тридцять повторень на одну команду.")
    add_scheme(doc, "scheme_01_macro_idea.png",
               "Схема 1. Що таке макрос")
    callout(doc, "Макрос не «розуміє» змісту документа — він лише точно "
                 "повторює записану послідовність команд. Тому перед запуском "
                 "макросу важливо поставити курсор у потрібне місце й "
                 "перевірити, який фрагмент виділено.",
            fill="EAF2FB", accent="0071E3")

    subheading(doc, "1.2. Запис макросу: покроковий алгоритм")
    para_rich(doc, [
        ("Запис макросу — це режим, у якому Word фіксує кожну дію "
         "користувача й перетворює її на команди мови VBA. Робота "
         "складається з п'яти послідовних кроків (схема 2). Перед початком "
         "запису слід увімкнути вкладку «Розробник» (", "text"),
        ("Файл → Параметри → Настроювання стрічки", "code"),
        ("), налаштувати рівень безпеки та зберегти документ у форматі ", "text"),
        (".docm", "code"),
        (", оскільки формат ", "text"),
        (".docx", "code"),
        (" макроси не зберігає.", "text"),
    ])
    add_scheme(doc, "scheme_02_macro_steps.png",
               "Схема 2. Етапи створення макросу")
    para(doc, "Під час запису важливо правильно обрати тип посилання — від "
              "цього залежить, чи працюватиме макрос лише в одному місці "
              "документа, чи для довільної кількості фрагментів (таблиця 1).")
    styled_table(
        doc,
        ["Тип посилання", "Як поводиться макрос", "Коли використовувати"],
        [
            ["Абсолютне (за замовчуванням)",
             "Завжди працює з тим самим місцем документа, яке було виділено "
             "під час запису",
             "Однотипне оформлення фіксованих елементів: заголовок, шапка "
             "таблиці, титульна сторінка"],
            ["Відносне (кнопка «Відносне посилання»)",
             "Починає роботу від поточного положення курсора й не прив'язаний "
             "до конкретного місця",
             "Обробка довільної кількості фрагментів тексту поспіль: "
             "нумерація списків, форматування карток"],
        ],
        widths=[4.0, 6.5, 6.5],
        font_size=12,
        center_cols=(),
    )
    para(doc, "Таблиця 1. Абсолютні та відносні посилання під час запису "
              "макросу", size=12, italic=True, color=GRAY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)
    callout(doc, "Перед записом макросу з відносним посиланням обов'язково "
                 "натисніть кнопку «Відносне посилання» на вкладці "
                 "«Розробник». Інакше Word запам'ятає конкретне місце "
                 "документа, і макрос спрацює лише там.",
            fill="FFF4E5", accent="C93400")

    subheading(doc, "1.3. Безпека макросів")
    para(doc, "Оскільки макрос — це фактично програма, він може виконувати не "
              "лише корисні дії. Саме тому Word має три режими безпеки, і "
              "вибір режиму визначає, чи запускатимуться макроси автоматично, "
              "чи з дозволу користувача (схема 3). Для навчальної роботи "
              "доцільно використовувати режим «Сповіщення про макроси»: "
              "редактор щоразу запитуватиме підтвердження, і студент "
              "контролюватиме запуск коду.")
    add_scheme(doc, "scheme_03_security.png",
               "Схема 3. Рівні безпеки макросів")
    callout(doc, "Файли, завантажені з Інтернету, відкриваються в режимі "
                 "захищеного перегляду. Перш ніж увімкнути макроси, "
                 "переконайтеся, що джерело файлу надійне, а сам код "
                 "зрозумілий.",
            fill="FDECEA", accent="C4001D")

    subheading(doc, "1.4. Основи VBA: структура процедури")
    para_rich(doc, [
        ("Кожен записаний макрос Word зберігає як процедуру мови VBA. "
         "Процедура починається словом ", "text"),
        ("Sub", "code"),
        (" та завершується ", "text"),
        ("End Sub", "code"),
        ("; усе, що міститься між ними, виконується послідовно. Коментарі "
         "починаються з апострофа й не впливають на роботу програми, але "
         "роблять код зрозумілим для інших (схема 4).", "text"),
    ])
    add_scheme(doc, "scheme_04_vba.png",
               "Схема 4. Структура процедури VBA", width_cm=14.0)
    para_rich(doc, [
        ("Редактор VBA відкривається командою ", "text"),
        ("Розробник → Visual Basic", "code"),
        (". Змінювати записаний код слід обережно: достатньо змінити число "
         "у рядку ", "text"),
        ("Selection.Font.Size = 16", "code"),
        (", щоб макрос почав застосовувати інший розмір шрифту.", "text"),
    ])

    # --- Етапи виконання -----------------------------------------------------
    heading(doc, "Етапи виконання самостійної роботи")
    para(doc, "Робота виконується у чотири послідовні етапи (схема 5). Кожен "
              "етап завершується проміжним результатом, який фіксується в "
              "звіті: опрацьовані питання, записані макроси, скріншоти та "
              "висновки.")
    add_scheme(doc, "scheme_05_stages.png",
               "Схема 5. Етапи виконання самостійної роботи", width_cm=15.5)
    para(doc, "На першому етапі студент працює з теоретичними відомостями та "
              "питаннями для самоперевірки. На другому — виконує практичні "
              "завдання за інструкційною карткою. На третьому — оформлює "
              "звіт зі скріншотами й кодом процедур. На четвертому — подає "
              "файли на перевірку та відповідає на запитання викладача.")

    # --- Інструкційна картка -------------------------------------------------
    heading(doc, "Інструкційна картка практичного завдання")
    para(doc, "Виконуйте команди послідовно, фіксуючи результати кожного "
              "кроку в звіті (таблиця 2).")
    styled_table(
        doc,
        ["№", "Дія", "Команда / шлях", "Результат"],
        [
            ["1", "Увімкнути вкладку «Розробник»",
             "Файл → Параметри → Настроювання стрічки → прапорець «Розробник»",
             "На стрічці з'явилася вкладка «Розробник»"],
            ["2", "Налаштувати безпеку макросів",
             "Розробник → Безпека макросів → Сповіщення про макроси",
             "Word запитуватиме дозвіл на запуск макросів"],
            ["3", "Створити файл-заготовку",
             "Файл → Створити → Новий документ; зберегти як Практика_11.docm",
             "Документ у форматі з підтримкою макросів"],
            ["4", "Почати запис макросу",
             "Розробник → Макроси → Записати макрос…; ім'я FormatTitle",
             "Увімкнено режим запису дій"],
            ["5", "Виконати дії для запису",
             "Ctrl+B; розмір шрифту 16 pt; колір тексту — темно-синій; "
             "інтервал перед абзацом 6 pt",
             "Дії зафіксовано в макросі"],
            ["6", "Зупинити запис",
             "Розробник → Макроси → Зупинити запис",
             "Макрос збережено в документі"],
            ["7", "Призначити макрос на кнопку",
             "Файл → Параметри → Панель швидкого доступу → Макроси → "
             "FormatTitle → Додати",
             "Кнопка макросу на панелі швидкого доступу"],
            ["8", "Призначити сполучення клавіш",
             "Розробник → Макроси → FormatTitle → Клавіші → Ctrl+Shift+T → "
             "Призначити",
             "Макрос запускається з клавіатури"],
            ["9", "Записати макрос із відносним посиланням",
             "Розробник → Відносне посилання → Записати макрос…; ім'я "
             "NumberList",
             "Макрос працює від поточного курсора"],
            ["10", "Відредагувати код VBA",
             "Розробник → Visual Basic → Module1",
             "Відкрито редактор VBA з кодом процедури"],
            ["11", "Зберегти результат",
             "Файл → Зберегти як → Практика_11.docm",
             "Файл із макросами збережено"],
        ],
        widths=[1.0, 4.3, 6.4, 5.3],
        font_size=11,
        code_cols=(2,),
    )
    para(doc, "Таблиця 2. Покроковий алгоритм виконання практичного завдання",
         size=12, italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)
    callout(doc, "Якщо після збереження документа кнопка макросу не реагує на "
                 "натискання, перевірте формат файлу: у .docx макроси не "
                 "зберігаються й не виконуються.",
            fill="EAF7EE", accent="248A3D")

    # --- Завдання на заповнення таблиці --------------------------------------
    heading(doc, "Завдання на заповнення таблиці")
    para(doc, "Заповніть таблицю 3 під час виконання роботи: укажіть "
              "призначення кожного інструмента та команду, якою він "
              "викликається.")
    styled_table(
        doc,
        ["Інструмент", "Призначення", "Команда виклику"],
        [
            ["Записати макрос", "", ""],
            ["Відносне посилання", "", ""],
            ["Зупинити запис", "", ""],
            ["Безпека макросів", "", ""],
            ["Редактор Visual Basic", "", ""],
            ["Панель швидкого доступу", "", ""],
        ],
        widths=[5.5, 6.0, 5.5],
        font_size=12,
        center_cols=(),
    )
    para(doc, "Таблиця 3. Інструменти роботи з макросами", size=12,
         italic=True, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=2, space_after=6)

    # --- Питання для самоперевірки -------------------------------------------
    heading(doc, "Теоретичні питання для самоперевірки")
    num_list(doc, [
        "Що таке макрос? Які задачі він допомагає розв'язувати?",
        "Які переваги й обмеження мають макроси порівняно з ручним "
        "форматуванням?",
        "Як увімкнути вкладку «Розробник» у текстовому редакторі Word?",
        "Які рівні безпеки макросів існують? Який режим рекомендовано для "
        "навчальної роботи?",
        "Чому документ із макросами потрібно зберігати у форматі .docm?",
        "Яка різниця між абсолютним і відносним посиланнями під час запису "
        "макросу?",
        "Як призначити макрос на кнопку панелі швидкого доступу?",
        "Як призначити макрос на сполучення клавіш і яких комбінацій краще "
        "уникати?",
        "Що таке VBA? Опишіть структуру процедури Sub … End Sub.",
        "Як додати коментар у код VBA і навіщо це робити?",
    ])

    # --- Рекомендації до звіту -----------------------------------------------
    heading(doc, "Рекомендації до оформлення звіту")
    bullets(doc, [
        "Звіт оформлюється в текстовому редакторі Word: шрифт Times New "
        "Roman, 14 pt, міжрядковий інтервал 1,15.",
        "Структура звіту: тема, мета, короткі теоретичні відомості, хід "
        "виконання зі скріншотами, результати роботи макросів, висновки.",
        "До звіту додається файл із макросами (.docm), у якому записані "
        "макроси FormatTitle і NumberList.",
        "Скріншоти мають бути чіткими й підписаними та відображати вікна "
        "«Макроси», «Visual Basic» і результат роботи макросу.",
        "Код процедур VBA наводиться повністю, з коментарями.",
        "Висновки — 4–6 речень: що вдалося, які труднощі виникли, де можна "
        "застосувати макроси в роботі вчителя.",
        "Назва файлу звіту: СР11_Прізвище_Ім'я.docx.",
    ])

    # --- Критерії оцінювання -------------------------------------------------
    heading(doc, "Критерії оцінювання")
    styled_table(
        doc,
        ["№", "Критерій", "Бали"],
        [
            ["1", "Опрацювання теоретичних відомостей, відповіді на питання "
                  "самоперевірки", "2"],
            ["2", "Налаштування вкладки «Розробник» і рівня безпеки макросів",
             "1"],
            ["3", "Запис макросу з абсолютними посиланнями (FormatTitle)", "2"],
            ["4", "Запис макросу з відносним посиланням (NumberList)", "2"],
            ["5", "Призначення макросів на кнопку та сполучення клавіш", "2"],
            ["6", "Редагування коду VBA, наявність коментарів", "2"],
            ["7", "Оформлення звіту та наявність підписаних скріншотів", "1"],
            ["8", "Захист роботи (відповіді на запитання)", "1"],
            ["", "Разом", "13"],
        ],
        widths=[1.0, 13.5, 2.5],
        font_size=12,
    )
    para(doc, "Таблиця 4. Критерії та бали", size=12, italic=True, color=GRAY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)

    para(doc, "Після завершення роботи надішліть файл із макросами та звіт на "
              "перевірку й підготуйтеся до усного захисту результатів.")

    doc.save(DOCX_NAME)
    print("Готово: створено файл '%s'." % DOCX_NAME)
    print("Схеми збережено у папці '%s' (PNG + SVG)." % OUT)


# ============================================================================
# 4. ЗАПУСК
# ============================================================================
if __name__ == "__main__":
    build_schemes()
    build_document()