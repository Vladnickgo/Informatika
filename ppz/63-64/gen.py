# -*- coding: utf-8 -*-
"""
САМОСТІЙНА РОБОТА № 9
Тема: Роль статистики в педагогічних дослідженнях

Генерує:
  - Samostiyna_robota_9_Statystyka.docx
  - output/*.png та output/*.svg (5 схем у стилі Apple)
"""

import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOCX_NAME = "Samostiyna_robota_9_Statystyka.docx"
OUT_DIR = "output"

# ======================================================================
# 1. СХЕМИ (matplotlib, Apple-стиль)
# ======================================================================

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

C_CARD = "#F5F5F7"
C_LINE = "#E5E5EA"
C_TEXT = "#1D1D1F"
C_GRAY = "#86868B"
C_BLUE = "#0071E3"
C_GREEN = "#248A3D"
C_ORANGE = "#C93400"
C_RED = "#C4001D"
C_PURPLE = "#6E30A8"


def fig_new(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def fig_title(ax, w, h, text, fs=15):
    ax.text(w / 2.0, h - 0.10, text, ha="center", va="top",
            fontsize=fs, fontweight="bold", color=C_TEXT)


def draw_card(ax, x, y, w, h, title, sub=None, color=C_BLUE,
              title_fs=14.5, sub_fs=11.5):
    card = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0,rounding_size=0.18",
                          linewidth=1.4, edgecolor=C_LINE, facecolor=C_CARD)
    ax.add_patch(card)
    # тонка акцентна лінія зверху картки
    ax.plot([x + 0.28, x + w - 0.28], [y + h - 0.13, y + h - 0.13],
            color=color, lw=3.2, solid_capstyle="round")
    cx = x + w / 2.0
    ax.text(cx, y + h * 0.60, title, ha="center", va="center",
            fontsize=title_fs, fontweight="bold", color=C_TEXT)
    if sub:
        ax.text(cx, y + h * 0.26, sub, ha="center", va="center",
                fontsize=sub_fs, color=C_GRAY, linespacing=1.35)


def arrow_h(ax, x1, x2, y, color=C_GRAY):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7,
                                shrinkA=0, shrinkB=0, mutation_scale=15))


def arrow_v(ax, x, y1, y2, color=C_GRAY):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7,
                                shrinkA=0, shrinkB=0, mutation_scale=15))


def save_scheme(fig, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    fig.savefig(os.path.join(OUT_DIR, name + ".png"), dpi=220,
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(os.path.join(OUT_DIR, name + ".svg"),
                bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


def scheme_roles():
    W, H = 8.6, 3.05
    fig, ax = fig_new(W, H)
    fig_title(ax, W, H, "Роль статистики в педагогічному дослідженні")
    data = [
        ("Опис", "Стисло подає\nрезультати", C_BLUE),
        ("Порівняння", "Зіставляє\nгрупи учнів", C_GREEN),
        ("Зв'язки", "Показує\nзалежності", C_ORANGE),
        ("Висновки", "Підтверджує\nгіпотези", C_PURPLE),
    ]
    w, h, gap, x, y = 1.85, 2.10, 0.30, 0.15, 0.25
    for t, s, c in data:
        draw_card(ax, x, y, w, h, t, s, c)
        x += w + gap
    save_scheme(fig, "stat_roles")


def scheme_measures():
    W, H = 8.6, 3.05
    fig, ax = fig_new(W, H)
    fig_title(ax, W, H, "Основні статистичні показники")
    data = [
        ("Середнє", "сума, поділена\nна кількість", C_BLUE),
        ("Медіана", "середина\nвпорядкованого ряду", C_GREEN),
        ("Мода", "найчастіше\nзначення", C_ORANGE),
        ("Розмах", "різниця\nmax і min", C_PURPLE),
    ]
    w, h, gap, x, y = 1.85, 2.10, 0.30, 0.15, 0.25
    for t, s, c in data:
        draw_card(ax, x, y, w, h, t, s, c, title_fs=14.0, sub_fs=11.0)
        x += w + gap
    save_scheme(fig, "stat_measures")


def scheme_methods():
    W, H = 8.6, 3.05
    fig, ax = fig_new(W, H)
    fig_title(ax, W, H, "Групи методів статистичного аналізу")
    data = [
        ("Описова", "середнє, медіана,\nмода, розмах", C_BLUE),
        ("Порівняльна", "порівняння двох\nгруп за ознакою", C_GREEN),
        ("Кореляційна", "зв'язок між\nпоказниками", C_ORANGE),
    ]
    w, h, gap, x, y = 2.45, 2.10, 0.45, 0.175, 0.25
    for t, s, c in data:
        draw_card(ax, x, y, w, h, t, s, c, title_fs=14.5, sub_fs=11.5)
        x += w + gap
    save_scheme(fig, "stat_methods")


def scheme_stages():
    W, H = 8.6, 3.05
    fig, ax = fig_new(W, H)
    fig_title(ax, W, H, "Етапи статистичного опрацювання даних")
    data = [
        ("Збір", "даних та\nоцінювання", C_BLUE),
        ("Упорядкування", "таблиці,\nранжування", C_GREEN),
        ("Обчислення", "середніх\nпоказників", C_ORANGE),
        ("Інтерпретація", "висновки\nй узагальнення", C_PURPLE),
    ]
    w, h, gap, x, y = 1.79, 2.10, 0.38, 0.15, 0.25
    for i, (t, s, c) in enumerate(data):
        draw_card(ax, x, y, w, h, t, s, c, title_fs=12.5, sub_fs=11.0)
        if i < len(data) - 1:
            arrow_h(ax, x + w + 0.04, x + w + gap - 0.04, y + h / 2)
        x += w + gap
    save_scheme(fig, "stat_stages")


def scheme_flow():
    W, H = 6.6, 6.3
    fig, ax = fig_new(W, H)
    fig_title(ax, W, H, "Етапи виконання самостійної роботи")
    steps = [
        ("Опрацювати джерела й інструкційну картку", C_BLUE),
        ("Обрати приклад із шкільної практики", C_GREEN),
        ("Обчислити статистичні показники", C_ORANGE),
        ("Оформити презентацію", C_PURPLE),
        ("Подати роботу на перевірку", C_RED),
    ]
    w, h, gap, x0, y = 5.6, 0.82, 0.33, 0.5, 0.30
    cx = W / 2.0
    for i, (t, c) in enumerate(steps):
        draw_card(ax, x0, y, w, h, t, None, c, title_fs=13.5)
        if i < len(steps) - 1:
            arrow_v(ax, cx, y + h + 0.03, y + h + gap - 0.03)
        y += h + gap
    save_scheme(fig, "stat_flow")


print("Генерація схем...")
scheme_roles()
scheme_measures()
scheme_methods()
scheme_stages()
scheme_flow()

# ======================================================================
# 2. ДОКУМЕНТ DOCX
# ======================================================================

doc = Document()

# ---- параметри сторінки ----
sec = doc.sections[0]
sec.left_margin = Cm(2.0)
sec.right_margin = Cm(2.0)
sec.top_margin = Cm(2.0)
sec.bottom_margin = Cm(2.0)

# ---- базовий стиль ----
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(14)
rpr = normal.element.get_or_add_rPr()
rfonts = rpr.find(qn("w:rFonts"))
if rfonts is None:
    rfonts = OxmlElement("w:rFonts")
    rpr.append(rfonts)
for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rfonts.set(qn(attr), "Times New Roman")
npf = normal.paragraph_format
npf.line_spacing = 1.15
npf.space_after = Pt(5)
npf.space_before = Pt(0)
npf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def set_run_font(run, size=14, bold=False, color=None,
                 name="Times New Roman", italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rp = run._element.get_or_add_rPr()
    rf = rp.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rp.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)


def add_runs(paragraph, text, size=14, bold=False, color=None):
    parts = re.split(r"(\[\[.+?\]\])", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("[[") and part.endswith("]]"):
            r = paragraph.add_run(part[2:-2])
            set_run_font(r, max(size - 1, 10), False, "C0392B", "Consolas")
        else:
            r = paragraph.add_run(part)
            set_run_font(r, size, bold, color)


def h1(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, 14, True, "1F4E79")
    return p


def h2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(10)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, 14, True, "2E75B6")
    return p


def body(text, size=14, space_after=5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
    add_runs(p, text, size)
    return p


def spacer(pts=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run("")
    set_run_font(r, pts)


# ---------- перезапуск нумерації List Number ----------
def _style_num_id(style_name):
    st = doc.styles[style_name]
    pPr = st.element.pPr
    if pPr is None or pPr.numPr is None or pPr.numPr.numId is None:
        return None
    return str(pPr.numPr.numId.val)


def _restart_num_id():
    try:
        numbering = doc.part.numbering_part.element
    except Exception:
        return None
    base = _style_num_id("List Number")
    abs_id = None
    for num in numbering.findall(qn("w:num")):
        if num.get(qn("w:numId")) == base:
            el = num.find(qn("w:abstractNumId"))
            if el is not None:
                abs_id = el.get(qn("w:val"))
            break
    if abs_id is None:
        return None
    existing = []
    for n in numbering.findall(qn("w:num")):
        v = n.get(qn("w:numId"))
        if v is not None and v.isdigit():
            existing.append(int(v))
    new_id = (max(existing) + 1) if existing else 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(new_id))
    a = OxmlElement("w:abstractNumId")
    a.set(qn("w:val"), abs_id)
    num.append(a)
    ov = OxmlElement("w:lvlOverride")
    ov.set(qn("w:ilvl"), "0")
    so = OxmlElement("w:startOverride")
    so.set(qn("w:val"), "1")
    ov.append(so)
    num.append(ov)
    numbering.append(num)
    return new_id


def numbered_list(items, size=14):
    nid = _restart_num_id()
    for text in items:
        p = doc.add_paragraph(style="List Number")
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-0.5)
        pf.line_spacing = 1.15
        pf.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if nid is not None:
            numPr = p._p.get_or_add_pPr().get_or_add_numPr()
            numPr.get_or_add_ilvl().val = 0
            numPr.get_or_add_numId().val = nid
        add_runs(p, text, size)


def bullet_list(items, size=14):
    for text in items:
        p = doc.add_paragraph(style="List Bullet")
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-0.5)
        pf.line_spacing = 1.15
        pf.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_runs(p, text, size)


def paren_list(items, size=14):
    for i, text in enumerate(items, start=1):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-0.6)
        pf.line_spacing = 1.15
        pf.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_runs(p, "%d) %s" % (i, text), size)


# ---------- службові елементи таблиць ----------
def _shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)


def add_table(headers, rows, widths, font_size=12):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr = table.rows[0]
    _repeat_header(hdr)
    for i, htext in enumerate(headers):
        cell = hdr.cells[i]
        cell.width = Cm(widths[i])
        _shade(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(htext)
        set_run_font(r, font_size, True, "FFFFFF")

    for row_vals in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row_vals):
            cells[i].width = Cm(widths[i])
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_runs(p, val if val else " ", font_size)
    return table


def callout(text, fill="EAF3FB", border="0071E3", size=13):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    cell = t.cell(0, 0)
    cell.width = Cm(16.5)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), border)
    borders.append(left)
    for edge in ("top", "bottom", "right"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "nil")
        borders.append(e)
    tcPr.append(borders)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    pf.left_indent = Cm(0.3)
    pf.line_spacing = 1.15
    add_runs(p, text, size)
    return t


def add_scheme(name, width_cm=15.8):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run()
    run.add_picture(os.path.join(OUT_DIR, name + ".png"), width=Cm(width_cm))


# ---------- нумерація сторінок у футері ----------
def add_page_field(paragraph):
    run = paragraph.add_run()
    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    i = OxmlElement("w:instrText")
    i.set(qn("xml:space"), "preserve")
    i.text = " PAGE "
    s = OxmlElement("w:fldChar")
    s.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t")
    t.text = "1"
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    for el in (b, i, s, t, e):
        run._r.append(el)
    set_run_font(run, 12)


fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_page_field(fp)

# ======================================================================
# 3. ЗМІСТ ДОКУМЕНТА
# ======================================================================

# ---- заголовок ----
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(2)
r = p.add_run("САМОСТІЙНА РОБОТА № 9")
set_run_font(r, 14, True, "1F4E79")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(10)
r = p.add_run("Тема: Роль статистики в педагогічних дослідженнях")
set_run_font(r, 14, True, "1D1D1F")

# ---- мета ----
h1("Мета")
body("Створити презентацію про роль статистики в педагогічних дослідженнях; "
     "ознайомитися з призначенням і можливостями статистичних методів; "
     "розвивати вміння застосовувати статистичні підходи до аналізу педагогічних даних; "
     "виховувати наукову об'єктивність у кількісному аналізі результатів дослідження.")

# ---- обладнання ----
h1("Обладнання та програмне забезпечення")
paren_list([
    "інструкційні картки;",
    "персональний комп'ютер або ноутбук;",
    "табличний процесор (Microsoft Excel, LibreOffice Calc);",
    "програма для створення презентацій (Microsoft PowerPoint, LibreOffice Impress);",
    "доступ до мережі Інтернет для пошуку джерел.",
])

# ---- література ----
h1("Література")
numbered_list([
    "Гончаренко С. У. Педагогічні дослідження : методологічні поради молодим науковцям. "
    "Київ ; Вінниця : ДОВ «Вінниця», 2008. 278 с.",
    "Кравець Н. П. Основи наукових досліджень : навчальний посібник. "
    "Київ : Вид-во НПУ імені М. П. Драгоманова, 2020. 74 с.",
    "Методичні рекомендації щодо написання та оформлення курсової роботи. "
    "Путивль : КЗСОР «Путивльський педагогічний фаховий коледж імені С. В. Руднєва», 2024. 14 с.",
])

# ---- завдання ----
h1("Завдання самостійної роботи")
numbered_list([
    "Опрацювати теоретичні відомості про роль статистики в педагогічному дослідженні.",
    "З'ясувати, які статистичні показники застосовують для опису результатів навчання, "
    "та в яких випадках кожен із них доречний.",
    "Підібрати приклад із шкільної практики (наприклад, результати тесту з інформатики "
    "у 20 учнів початкової школи) і підготувати числові дані для аналізу.",
    "Обчислити середнє арифметичне, медіану, моду та розмах за власними даними, "
    "побудувати стовпчикову діаграму розподілу балів.",
    "Створити презентацію обсягом 8–12 слайдів, у якій розкрити роль статистики "
    "та подати результати власних обчислень.",
    "Сформулювати висновок про те, як статистичні дані підвищують обґрунтованість "
    "педагогічного дослідження.",
])

# ---- терміни ----
h1("Терміни виконання")
body("Робота виконується протягом двох тижнів від дати видачі завдання. "
     "Проміжний контроль (перевірка підготовлених даних і таблиці показників) — "
     "на наступному практичному занятті. Остаточний варіант презентації та звіт "
     "подаються до початку консультації; захист роботи відбувається на консультації "
     "у формі короткої доповіді на 3–4 хвилини.")

# ---- очікувані результати ----
h1("Очікувані результати")
bullet_list([
    "пояснює, чому статистика є обов'язковим складником педагогічного дослідження;",
    "розрізняє описову, порівняльну та кореляційну статистику;",
    "правильно обчислює середнє арифметичне, медіану, моду та розмах;",
    "добирає доречний показник відповідно до мети дослідження;",
    "подає результати у вигляді таблиць і діаграм з підписами;",
    "формулює висновки з опорою на кількісні дані, а не на власні враження;",
    "створює і захищає презентацію за результатами власного мінідослідження.",
])

# ---- перелік питань ----
h1("Перелік опрацьовуваних питань")
numbered_list([
    "Поняття статистики та її місце в педагогічному дослідженні.",
    "Генеральна сукупність і вибірка, вимоги до обсягу вибірки.",
    "Вимірювання педагогічних явищ: номінальна, порядкова, інтервальна шкали.",
    "Міри центральної тенденції: середнє арифметичне, медіана, мода.",
    "Міри розсіювання: розмах, дисперсія, стандартне відхилення.",
    "Описова статистика та її роль у поданні результатів.",
    "Порівняльний аналіз груп (t-критерій Стьюдента, критерій χ²).",
    "Кореляційний аналіз і коефіцієнт кореляції Пірсона.",
    "Візуалізація даних: таблиці, стовпчикові та лінійні діаграми.",
    "Інтерпретація результатів і формулювання висновків дослідження.",
])

# ---- теоретичні відомості ----
h1("Теоретичні відомості (стислий огляд)")

h2("1. Статистика як інструмент педагогічного дослідження")
body("Педагогіка досліджує масові явища: успішність класу, ставлення учнів до предмета, "
     "ефективність окремої методики. Одиничне спостереження ще не є доказом, адже один учень "
     "може випадково показати високий або низький результат. Статистика дає змогу перейти від "
     "суб'єктивного «здається» до обґрунтованого «доведено»: зібрати дані, упорядкувати їх, "
     "обчислити показники та зробити висновки, що поширюються на всю досліджувану групу.")
add_scheme("stat_roles")
body("Кожна з чотирьох ролей відповідає на своє питання: що відбувається (опис), "
     "чи відрізняються групи (порівняння), чи пов'язані показники між собою (зв'язки), "
     "чи можна підтвердити гіпотезу (висновки).")
callout("Обсяг вибірки впливає на надійність висновків. Для студентського дослідження "
        "зазвичай достатньо 20–30 спостережень, однак і тоді висновки формулюють обережно: "
        "«у досліджуваній групі простежується тенденція», а не «встановлено закономірність».")

h2("2. Основні статистичні показники")
body("Щоб описати групу чисел, недостатньо назвати одне значення. Потрібні показники, "
     "які характеризують типовий рівень і розкид даних. Найуживаніші з них подано на схемі.")
add_scheme("stat_measures")
body("Порівняймо показники на прикладі балів п'яти учнів: 3, 4, 4, 5, 4.")
spacer(4)
add_table(
    ["Показник", "Що характеризує", "Значення для ряду 3, 4, 4, 5, 4"],
    [
        ["Середнє арифметичне", "узагальнений рівень групи", "4,0"],
        ["Медіана", "середину впорядкованого ряду", "4"],
        ["Мода", "найчастіше значення", "4"],
        ["Розмах", "ширину розкиду даних", "2"],
    ],
    widths=[4.5, 7.0, 5.0],
    font_size=12,
)
spacer(6)
callout("Округлюйте проміжні результати до двох знаків після коми, а підсумковий подавайте "
        "з тією самою точністю, що й вихідні дані. Різниця між «4» і «4,0» у звіті — це різниця "
        "між недбалістю та науковою культурою.", fill="FFF4E8", border="C93400")

h2("3. Методи статистичного аналізу")
body("Залежно від мети дослідження застосовують різні групи методів. Вибір методу визначає "
     "не складність обчислень, а тип запитання, на яке дослідник шукає відповідь.")
add_scheme("stat_methods")
bullet_list([
    "Описова статистика відповідає на питання «як виглядають дані» і не потребує складних обчислень.",
    "Порівняльна статистика перевіряє, чи є різниця між групами статистично значущою "
    "(t-критерій Стьюдента для середніх, критерій χ² для частот).",
    "Кореляційна статистика встановлює силу й напрям зв'язку між показниками "
    "(коефіцієнт кореляції Пірсона набуває значень від –1 до +1).",
])
callout("Кореляція не доводить причинності. Якщо учні з вищою мотивацією мають вищі бали, "
        "це не означає, що мотивація є єдиною причиною успішності: можливі й інші чинники — "
        "рівень підготовки, умови навчання, тривалість виконання завдань.",
        fill="EDF7EE", border="248A3D")

h2("4. Етапи статистичного опрацювання даних")
body("Статистичне опрацювання — це послідовність із чотирьох кроків. Пропуск будь-якого з них "
     "робить результат ненадійним: без якісного збору даних неможливі коректні обчислення, "
     "а без інтерпретації числа залишаються лише числами.")
add_scheme("stat_stages")
numbered_list([
    "Збір даних: фіксація результатів за єдиною шкалою та в єдиних умовах.",
    "Упорядкування: перенесення даних у таблицю, перевірка на пропуски й помилки, ранжування.",
    "Обчислення: визначення показників і побудова діаграм у табличному процесорі.",
    "Інтерпретація: пояснення значень, співвіднесення з гіпотезою, формулювання висновків.",
])

h2("5. Подання результатів у презентації")
body("Результати дослідження сприймаються лише тоді, коли їх видно. Презентація не повинна "
     "дублювати звіт: на слайд виносять головне — таблицю показників, одну-дві діаграми "
     "та короткий висновок.")
bullet_list([
    "одна думка — один слайд;",
    "таблиця на слайді містить не більше 7 рядків;",
    "діаграма має підписані осі та заголовок «Рис. 1. Розподіл балів …»;",
    "не більше двох шрифтів і трьох кольорів на слайді;",
    "список джерел — на останньому слайді.",
])

# ---- етапи виконання ----
h1("Етапи виконання самостійної роботи")
body("Послідовність роботи подано на схемі. Кожен етап завершується конкретним результатом, "
     "який можна перевірити самостійно.")
add_scheme("stat_flow", width_cm=12.5)

# ---- інструкційна картка ----
h1("Інструкційна картка практичного завдання")
spacer(4)
add_table(
    ["№", "Крок", "Дія", "Команда / результат"],
    [
        ["1", "Створити файл таблиці", "Відкрити табличний процесор",
         "[[Файл → Створити → Електронна таблиця]]"],
        ["2", "Внести дані", "Стовпець A — номер учня, стовпець B — бал",
         "[[A2:B21]]"],
        ["3", "Обчислити середнє", "Клітинка D2",
         "[[=СРЗНАЧ(B2:B21)]]"],
        ["4", "Обчислити медіану", "Клітинка D3",
         "[[=МЕДИАНА(B2:B21)]]"],
        ["5", "Обчислити моду", "Клітинка D4",
         "[[=МОДА(B2:B21)]]"],
        ["6", "Обчислити розмах", "Клітинка D5",
         "[[=МАКС(B2:B21)-МИН(B2:B21)]]"],
        ["7", "Побудувати діаграму", "Виділити діапазон A1:B21",
         "[[Вставка → Діаграма → Стовпчикова]]"],
        ["8", "Перенести на слайд", "Скопіювати таблицю та діаграму",
         "[[Ctrl + C]] → [[Ctrl + V]]"],
    ],
    widths=[1.2, 3.6, 6.4, 5.3],
    font_size=12,
)
spacer(6)
callout("У LibreOffice Calc назви функцій записують англійською: "
        "[[=AVERAGE(B2:B21)]], [[=MEDIAN(B2:B21)]], [[=MODE(B2:B21)]]. "
        "Якщо програма не розпізнає команду, перевірте, чи правильно вказано діапазон "
        "і чи не стоїть перед числом апостроф.", fill="F2EEF9", border="6E30A8")

# ---- таблиця для заповнення ----
h1("Завдання на заповнення таблиці")
body("Заповніть таблицю за результатами власних обчислень. У останньому стовпці "
     "запишіть формулу або спосіб, яким отримано значення.")
spacer(4)
add_table(
    ["Показник", "Позначення", "Значення для моєї вибірки", "Як обчислено"],
    [
        ["Середнє арифметичне", "x\u0304", "", ""],
        ["Медіана", "Me", "", ""],
        ["Мода", "Mo", "", ""],
        ["Розмах", "R", "", ""],
        ["Стандартне відхилення", "σ", "", ""],
    ],
    widths=[5.0, 2.5, 5.0, 4.0],
    font_size=12,
)
spacer(6)

# ---- питання для самоперевірки ----
h1("Теоретичні питання для самоперевірки")
numbered_list([
    "Чому одиничне спостереження не є достатнім для педагогічного висновку?",
    "Які чотири основні ролі виконує статистика в педагогічному дослідженні?",
    "Що таке генеральна сукупність і вибірка?",
    "Які вимоги висувають до обсягу та складу вибірки?",
    "Чим відрізняються середнє арифметичне та медіана?",
    "У яких випадках моду доцільніше використовувати, ніж середнє?",
    "Що показує розмах і чим він поступається стандартному відхиленню?",
    "Для чого застосовують t-критерій Стьюдента?",
    "Що означає коефіцієнт кореляції, який дорівнює 0,85?",
    "Чому з кореляції не випливає причинно-наслідковий зв'язок?",
])

# ---- рекомендації до звіту ----
h1("Рекомендації до оформлення звіту")
bullet_list([
    "обсяг презентації — 8–12 слайдів плюс титульний;",
    "титульний слайд містить тему, прізвище та ім'я студента, групу, рік;",
    "розмір шрифту на слайді — не менше 20 pt;",
    "таблиці та діаграми супроводжуються підписами й нумерацією;",
    "висновки подаються окремим слайдом і містять не більше 4 тез;",
    "файл назвати за зразком «Прізвище_СР9.pptx» і подати разом зі звітом.",
])

# ---- критерії оцінювання ----
h1("Критерії оцінювання")
spacer(4)
add_table(
    ["Критерій", "Показники", "Бали"],
    [
        ["Теоретичний огляд", "повнота, точність понять, опора на джерела", "3"],
        ["Статистичні обчислення", "правильність показників, наявність перевірки", "3"],
        ["Презентація", "структура, візуалізація, читабельність", "3"],
        ["Висновки", "обґрунтованість, опора на кількісні дані", "2"],
        ["Оформлення і терміни", "відповідність вимогам, вчасність подання", "2"],
        ["Разом", "", "13"],
    ],
    widths=[5.0, 9.5, 2.0],
    font_size=12,
)
spacer(6)
body("Шкала переведення балів: 12–13 — відмінно; 9–11 — добре; 6–8 — задовільно; "
     "0–5 — незадовільно.")

# ======================================================================
# 4. ЗБЕРЕЖЕННЯ
# ======================================================================
doc.save(DOCX_NAME)

print("Готово!")
print("Створено документ:", DOCX_NAME)
print("Схеми збережено у папці:", OUT_DIR)
for f in sorted(os.listdir(OUT_DIR)):
    print("   -", f)