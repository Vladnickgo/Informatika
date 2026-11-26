# -*- coding: utf-8 -*-
"""
Лекція № 7. Огляд технологій Веб 2.0. Поняття веб-журналу й різновиди веб-журналів.
Генерація docx-документа + 4 схем (PNG/SVG) у стилі Apple.
Запуск:  python lekciya_7_web2.py
"""

import os
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

# ----------------------------------------------------------------------------
# КОНСТАНТИ
# ----------------------------------------------------------------------------
OUT_DIR = "output"
DOCX_NAME = "Lekciya_7_Tekhnolohiyi_Veb_2_0.docx"
os.makedirs(OUT_DIR, exist_ok=True)

FONT = "Times New Roman"
MONO = "Consolas"

NAVY = RGBColor(0x1F, 0x4E, 0x79)
BLUE = RGBColor(0x2E, 0x75, 0xB6)
CMD_COLOR = RGBColor(0xC0, 0x39, 0x2B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_TEXT = RGBColor(0x59, 0x59, 0x59)

CENTER = WD_ALIGN_PARAGRAPH.CENTER
JUSTIFY = WD_ALIGN_PARAGRAPH.JUSTIFY
LEFT = WD_ALIGN_PARAGRAPH.LEFT

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

C_CARD = "#F5F5F7"
C_EDGE = "#E5E5EA"
C_TEXT = "#1D1D1F"
C_GRAY = "#86868B"
C_BLUE = "#0071E3"
C_GREEN = "#248A3D"
C_ORANGE = "#C93400"
C_RED = "#C4001D"
C_PURPLE = "#6E30A8"


# ----------------------------------------------------------------------------
# ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ СХЕМ
# ----------------------------------------------------------------------------
def _wrap(text, max_chars):
    out = []
    for block in str(text).split("\n"):
        words = block.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out or [""]


def _fig(w_in, h_in, xr, yr):
    fig = plt.figure(figsize=(w_in, h_in))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, xr)
    ax.set_ylim(0, yr)
    ax.axis("off")
    return fig, ax


def card(ax, fig, x, y, w, h, title, sub=None, fs=12.5, accent=C_TEXT, fill=C_CARD):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=1.1",
                                linewidth=1.4, edgecolor=C_EDGE,
                                facecolor=fill, zorder=2))
    xr = ax.get_xlim()[1]
    yr = ax.get_xlim()[1]  # placeholder, перерахуємо нижче
    yr = ax.get_ylim()[1]
    ppu_x = fig.get_size_inches()[0] * 72.0 / xr
    ppu_y = fig.get_size_inches()[1] * 72.0 / yr
    inner_w = w * ppu_x - 16.0
    inner_h = h * ppu_y - 14.0

    size = float(fs)
    t_lines, s_lines = [""], []
    while size >= 8.0:
        sub_fs = size - 1.5
        t_lines = _wrap(title, max(6, int(inner_w / (0.56 * size))))
        s_lines = _wrap(sub, max(6, int(inner_w / (0.56 * sub_fs)))) if sub else []
        need = len(t_lines) * size * 1.35 + len(s_lines) * sub_fs * 1.35
        need += 4.0 if s_lines else 0.0
        if need <= inner_h:
            break
        size -= 0.5

    sub_fs = size - 1.5
    t_h = len(t_lines) * size * 1.35 / ppu_y
    s_h = len(s_lines) * sub_fs * 1.35 / ppu_y if s_lines else 0.0
    gap = 4.0 / ppu_y if s_lines else 0.0
    top = y + h / 2.0 + (t_h + gap + s_h) / 2.0
    cx = x + w / 2.0

    ax.text(cx, top - t_h / 2.0, "\n".join(t_lines), ha="center", va="center",
            fontsize=size, color=accent, fontweight="bold",
            linespacing=1.35, zorder=4)
    if s_lines:
        ax.text(cx, top - t_h - gap - s_h / 2.0, "\n".join(s_lines),
                ha="center", va="center", fontsize=sub_fs, color=C_GRAY,
                linespacing=1.35, zorder=4)


def arrow(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.8):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=1, shrinkB=1, mutation_scale=16),
                zorder=5)


def save_scheme(fig, name):
    png = os.path.join(OUT_DIR, name + ".png")
    svg = os.path.join(OUT_DIR, name + ".svg")
    fig.savefig(png, dpi=220, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(svg, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return png, svg


# ----------------------------------------------------------------------------
# СХЕМА 1. Веб 1.0 vs Веб 2.0
# ----------------------------------------------------------------------------
def scheme_web2_vs_web1():
    fig, ax = _fig(12.0, 3.9, 100, 32)
    ax.text(50, 29.3, "Від Веб 1.0 до Веб 2.0: зміна ролі користувача", ha="center",
            va="center", fontsize=15, color=C_TEXT, fontweight="bold")

    card(ax, fig, 2.0, 5.0, 46.0, 20.0,
         "Веб 1.0\n«читання»",
         "статичні сторінки,\nконтент створює редактор,\nкористувач лише читає",
         fs=13.5, accent=C_GRAY)
    card(ax, fig, 52.0, 5.0, 46.0, 20.0,
         "Веб 2.0\n«читання й письмо»",
         "динамічні сервіси,\nконтент створюють користувачі,\nспівпраця й обмін",
         fs=13.5, accent=C_BLUE)
    arrow(ax, 48.2, 15.0, 51.8, 15.0, color=C_BLUE, lw=2.0)
    return save_scheme(fig, "web2_vs_web1")


# ----------------------------------------------------------------------------
# СХЕМА 2. Види веб-журналів
# ----------------------------------------------------------------------------
def scheme_blog_types():
    fig, ax = _fig(12.0, 3.9, 100, 32)
    ax.text(50, 29.3, "Різновиди веб-журналів (блогів)", ha="center",
            va="center", fontsize=15, color=C_TEXT, fontweight="bold")

    items = [
        ("Особистий", "щоденник,\nдумки автора", C_BLUE),
        ("Тематичний", "один предмет\nчи навичка", C_PURPLE),
        ("Блог учителя", "новини класу,\nзавдання", C_GREEN),
        ("Блог класу", "спільні\nпроєкти", C_ORANGE),
        ("Мікроблог", "короткі\nзаписи", C_RED),
    ]
    w, h, y = 17.0, 15.0, 8.0
    xs = [2.0, 21.6, 41.2, 60.8, 80.4]
    for x, (t, s, col) in zip(xs, items):
        card(ax, fig, x, y, w, h, t, s, fs=12.5, accent=col)
    return save_scheme(fig, "blog_types")


# ----------------------------------------------------------------------------
# СХЕМА 3. Етапи створення веб-журналу
# ----------------------------------------------------------------------------
def scheme_blog_creation():
    fig, ax = _fig(12.0, 4.0, 100, 32)
    ax.text(50, 29.3, "Етапи створення веб-журналу", ha="center",
            va="center", fontsize=15, color=C_TEXT, fontweight="bold")

    items = [
        ("Вибір\nплатформи", "Blogger,\nWordPress", C_BLUE),
        ("Реєстрація", "обліковий\nзапис Google", C_BLUE),
        ("Вибір\nшаблону", "тема й\nкольори", C_PURPLE),
        ("Налаштування", "назва, адреса,\nприватність", C_ORANGE),
        ("Перший\nдопис", "текст,\nзображення", C_GREEN),
        ("Публікація", "перевірка →\nопублікувати", C_GREEN),
    ]
    w, h, y = 14.5, 15.0, 8.0
    xs = [1.5, 18.0, 34.5, 51.0, 67.5, 84.0]
    for x, (t, s, col) in zip(xs, items):
        card(ax, fig, x, y, w, h, t, s, fs=12.0, accent=col)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + w + 0.2, y + h / 2.0, xs[i + 1] - 0.2, y + h / 2.0)
    return save_scheme(fig, "blog_creation")


# ----------------------------------------------------------------------------
# СХЕМА 4. Параметри налаштування блогу
# ----------------------------------------------------------------------------
def scheme_blog_settings():
    fig, ax = _fig(12.0, 3.9, 100, 32)
    ax.text(50, 29.3, "Основні параметри налаштування веб-журналу", ha="center",
            va="center", fontsize=15, color=C_TEXT, fontweight="bold")

    items = [
        ("Назва й адреса", "унікальна адреса\nблогу", C_BLUE),
        ("Дизайн і шаблон", "тема, кольори,\nшрифти", C_PURPLE),
        ("Приватність", "хто бачить\nдописи", C_ORANGE),
        ("Коментарі", "модерація,\nхто пише", C_GREEN),
        ("Резервні копії", "експорт\nдописів", C_RED),
    ]
    w, h, y = 17.0, 15.0, 8.0
    xs = [2.0, 21.6, 41.2, 60.8, 80.4]
    for x, (t, s, col) in zip(xs, items):
        card(ax, fig, x, y, w, h, t, s, fs=12.5, accent=col)
    return save_scheme(fig, "blog_settings")


# ----------------------------------------------------------------------------
# ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ----------------------------------------------------------------------------
def set_run_font(run, size=14, bold=False, color=None, name=FONT):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:eastAsia"), name)
    rFonts.set(qn("w:cs"), name)


def add_rich_text(p, text, size=14, bold=False, color=None):
    parts = str(text).split("`")
    for i, part in enumerate(parts):
        if part == "":
            continue
        if i % 2 == 1:
            r = p.add_run(part)
            set_run_font(r, size=size - 1, bold=bold, color=CMD_COLOR, name=MONO)
        else:
            r = p.add_run(part)
            set_run_font(r, size=size, bold=bold, color=color, name=FONT)


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def set_cell_borders(cell, left_color=None, sz=28):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement("w:" + edge)
        if edge == "left" and left_color:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), left_color)
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)
    tcPr.append(borders)


def add_page_number_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = CENTER
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    set_run_font(run, size=12, color=GRAY_TEXT)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    fld_txt = OxmlElement("w:t")
    fld_txt.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    for el in (fld_begin, instr, fld_sep, fld_txt, fld_end):
        run._r.append(el)


def setup_document():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(14)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)

    pf = style.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(5)
    pf.space_before = Pt(0)
    pf.alignment = JUSTIFY

    sec = doc.sections[0]
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(1.5)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    add_page_number_footer(sec)
    return doc


def heading(doc, text, color=NAVY, size=14, space_before=10, space_after=5, align=LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    add_rich_text(p, text, size=size, bold=True, color=color)
    return p


def body(doc, text, space_after=5, align=JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    add_rich_text(p, text, size=14)
    return p


def bullet(doc, items, indent=1.0):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = JUSTIFY
        add_rich_text(p, it, size=14)


def list_number(doc, items, indent=1.0):
    for it in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = JUSTIFY
        add_rich_text(p, it, size=14)


def numbered_paren(doc, items, indent=1.0):
    for i, it in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = JUSTIFY
        add_rich_text(p, "{}) ".format(i), size=14)
        add_rich_text(p, it, size=14)


def add_table(doc, headers, rows, widths):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False

    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)

    hdr = t.rows[0]
    for i, htext in enumerate(headers):
        c = hdr.cells[i]
        c.text = ""
        p = c.paragraphs[0]
        p.alignment = CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        add_rich_text(p, htext, size=12, bold=True, color=WHITE)
        shade(c, "1F4E79")

    trPr = hdr._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)

    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = CENTER if i == 0 else LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            add_rich_text(p, val, size=12)

    for row in t.rows:
        for i, wcm in enumerate(widths):
            row.cells[i].width = Cm(wcm)
    for i, wcm in enumerate(widths):
        t.columns[i].width = Cm(wcm)
    return t


def callout(doc, text, accent="#0071E3", fill="EAF1F8"):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    cell = t.cell(0, 0)
    cell.width = Cm(16.0)
    set_cell_borders(cell, left_color=accent, sz=28)
    shade(cell, fill)
    p = cell.paragraphs[0]
    p.alignment = JUSTIFY
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    add_rich_text(p, text, size=13)
    gap = doc.add_paragraph()
    gap.paragraph_format.space_after = Pt(0)
    gap.paragraph_format.line_spacing = 1.0
    for r in gap.runs:
        r.font.size = Pt(4)


def figure(doc, path, caption, width_cm=16.0):
    p = doc.add_paragraph()
    p.alignment = CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))
    cap = doc.add_paragraph()
    cap.alignment = CENTER
    cap.paragraph_format.space_after = Pt(6)
    add_rich_text(cap, caption, size=12, color=GRAY_TEXT)


# ----------------------------------------------------------------------------
# ДОКУМЕНТ
# ----------------------------------------------------------------------------
def build_document(schemes):
    doc = setup_document()

    heading(doc, "ЛЕКЦІЯ 7. Огляд технологій Веб 2.0", color=NAVY,
            align=CENTER, space_before=0, space_after=4)

    tp = doc.add_paragraph()
    tp.alignment = CENTER
    tp.paragraph_format.space_after = Pt(8)
    add_rich_text(
        tp,
        "Тема: Огляд технологій Веб 2. Поняття веб-журналу й різновиди "
        "веб-журналів. Створення й оформлення веб-журналу, публікація "
        "повідомлень у веб-журналі та настроювання його параметрів.",
        size=14, bold=True)

    heading(doc, "Мета", color=BLUE, space_before=4)
    body(doc, "Ознайомити з технологіями Веб 2.0 (соціальні мережі, блоги, вікі), "
              "поняттям веб-журналу (блогу), його видами, основами створення та "
              "ведення. Розвивати навички роботи з соціальними медіа, уміння "
              "створювати контент і налаштовувати параметри публікації. Виховувати "
              "культуру ведення блогу, відповідальність за оприлюднену інформацію "
              "та повагу до читачів.")

    heading(doc, "Ключові поняття", color=BLUE)
    bullet(doc, [
        "Веб 2.0 — друге покоління веб-сервісів, де користувач є не лише читачем, а й автором контенту;",
        "соціальні сервіси — мережі, блоги, вікі, закладки, медіасховища;",
        "веб-журнал (блог) — сайт із регулярно оновлюваними дописами у зворотному хронологічному порядку;",
        "допис (пост) — окрема публікація в блозі з текстом, зображеннями, тегами;",
        "шаблон (тема) — набір налаштувань зовнішнього вигляду блогу;",
        "тег — ключове слово для сортування дописів;",
        "RSS — формат автоматичного отримання нових дописів блогу;",
        "модерація коментарів — перевірка повідомлень читачів перед публікацією.",
    ])

    heading(doc, "План лекції", color=BLUE)
    list_number(doc, [
        "Поняття Веб 2.0 та його ключові ознаки.",
        "Соціальні сервіси Веб 2.0: мережі, блоги, вікі, медіасховища.",
        "Веб-журнал (блог): визначення та різновиди.",
        "Створення й оформлення веб-журналу.",
        "Публікація повідомлень і налаштування параметрів блогу.",
        "Культура ведення блогу та відповідальність автора.",
    ])

    # ------------------------------------------------------------------
    heading(doc, "Теоретичний матеріал", color=NAVY, space_before=12)

    # 1
    heading(doc, "1. Поняття Веб 2.0 та його ключові ознаки", color=BLUE)
    body(doc, "Термін «Веб 2.0» з’явився на початку 2000-х і позначає друге "
              "покоління веб-сервісів, у яких користувач стає не лише споживачем, "
              "а й творцем контенту. У Веб 1.0 сторінки створювали редактори, "
              "а відвідувач лише читав. У Веб 2.0 будь-який користувач може "
              "публікувати тексти, фото, відео, коментувати й ділитися "
              "матеріалами. Для вчителя початкової школи це означає: клас може "
              "вести власний блог, а учень — долучатися до створення контенту "
              "під керівництвом дорослого.")
    figure(doc, schemes["web2"], "Рис. 1. Від Веб 1.0 до Веб 2.0: зміна ролі користувача")
    body(doc, "Ключові ознаки Веб 2.0: користувацький контент, колективна "
              "співпраця, простота публікації, безкоштовні хмарні сервіси, "
              "зворотний зв’язок через коментарі, теги й посилання. Завдяки "
              "цим ознакам школа отримує інструменти для проєктної діяльності "
              "та комунікації з батьками.")
    callout(doc, "Технології Веб 2.0 не потребують знання програмування. "
                 "Учень 3–4 класу разом з учителем може створити блог класу "
                 "за 15–20 хвилин і вести його протягом навчального року.",
            accent="#0071E3", fill="EAF1F8")

    # 2
    heading(doc, "2. Соціальні сервіси Веб 2.0", color=BLUE)
    body(doc, "До соціальних сервісів належать платформи, де користувачі "
              "взаємодіють і обмінюються контентом. У шкільній практиці "
              "найуживаніші блоги, вікі-сайти для спільного редагування "
              "текстів, медіасховища для фото й відео та соціальні мережі "
              "для швидких оголошень.")
    add_table(doc,
              ["Сервіс", "Приклади", "Освітнє застосування"],
              [
                  ["Блоги", "`Blogger`, `WordPress`",
                   "Блог класу, щоденник проєкту"],
                  ["Вікі", "`Wikipedia`, `Wiki site`",
                   "Спільне створення словника термінів"],
                  ["Медіасховища", "`YouTube`, `Google Photos`",
                   "Відеозвіт про екскурсію, фотоальбом"],
                  ["Хмарні документи", "`Google Docs`",
                   "Спільна робота над текстом"],
                  ["Соціальні мережі", "`Facebook`, `Instagram`",
                   "Оголошення для батьків"],
              ],
              [4.0, 5.5, 6.5])

    # 3
    heading(doc, "3. Веб-журнал (блог) та його різновиди", color=BLUE)
    body(doc, "Веб-журнал (блог, від англ. web log) — це сайт із регулярно "
              "оновлюваними дописами, розміщеними у зворотному хронологічному "
              "порядку: найновіше — вгорі. Автор блогу називається блогером, "
              "а читачі можуть залишати коментарі під дописами. Для школи блог "
              "зручний тим, що поєднує новини, завдання, фото та зворотний "
              "зв’язок в одному місці.")
    figure(doc, schemes["types"], "Рис. 2. Різновиди веб-журналів (блогів)")
    body(doc, "За змістом розрізняють: особистий щоденник, тематичний блог "
              "(присвячений одному предмету), блог учителя (новини й завдання "
              "класу), блог класу (спільні проєкти), мікроблог (короткі записи "
              "на кшталт `Twitter`). За доступом — публічний, для обраного кола "
              "читачів або приватний. За форматом — текстовий, фотоблог, "
              "відеоблог (влог), подкаст.")
    callout(doc, "Для початкової школи найзручніший блог учителя: він веде "
                 "його самостійно, публікує завдання й новини, а батьки "
                 "отримують оновлення через `RSS` або email-розсилку.",
            accent="#6E30A8", fill="F1EAF9")

    # 4
    heading(doc, "4. Створення й оформлення веб-журналу", color=BLUE)
    body(doc, "Створення блогу складається з шести послідовних кроків. "
              "Найпопулярніші безкоштовні платформи — `Blogger` (вхід через "
              "обліковий запис `Google`) та `WordPress.com`. Обидві не "
              "потребують програмування і дають змогу редагувати вигляд "
              "блогу в кілька кліків.")
    figure(doc, schemes["creation"], "Рис. 3. Етапи створення веб-журналу")
    body(doc, "Оформлення блогу — це передусім шаблон (тема). Обирайте "
              "світлий, стриманий шаблон з великим шрифтом: він зручний "
              "для читання на смартфонах, з яких більшість батьків "
              "переглядає блог. Додайте логотип класу, єдиний стиль "
              "заголовків і зрозумілі рубрики.")
    bullet(doc, [
        "назва блогу — коротка й упізнавана: `nash_2v_klas`;",
        "адреса — латиницею без пробілів;",
        "шаблон — світлий, шрифт не менше 14 pt;",
        "меню — не більше 5 рубрик;",
        "кольори — 2–3 основні, без різнобарв’я.",
    ])

    # 5
    heading(doc, "5. Публікація повідомлень і налаштування параметрів", color=BLUE)
    body(doc, "Публікація допису відкривається кнопкою `Створити` "
              "(`Новий допис`). Допис містить заголовок, тіло, зображення, "
              "теги й налаштування доступу. Перед публікацією зручно "
              "натиснути `Попередній перегляд` — так ви побачите, як "
              "допис виглядатиме на екрані читача.")
    figure(doc, schemes["settings"], "Рис. 4. Основні параметри налаштування веб-журналу")
    add_table(doc,
              ["Параметр", "Що регулює", "Порада для вчителя"],
              [
                  ["Назва й адреса", "Заголовок блогу й унікальну адресу",
                   "Адреса латиницею без пробілів"],
                  ["Дизайн і шаблон", "Тему, кольори, шрифти",
                   "Світлий шаблон, шрифт ≥ 14 pt"],
                  ["Приватність", "Хто бачить блог — усі чи лише запрошені",
                   "Для закритого класу — «лише за запрошенням»"],
                  ["Коментарі", "Хто може писати й чи потрібна модерація",
                   "Увімкніть модерацію перед публікацією"],
                  ["Резервні копії", "Експорт дописів і налаштувань",
                   "Робіть копію щомісяця"],
                  ["Авторство", "Хто може публікувати дописи",
                   "Додавайте учнів як авторів лише за потреби"],
              ],
              [3.8, 6.4, 5.8])
    callout(doc, "Увімкніть модерацію коментарів до публікації. Це захищає "
                 "блог від небажаних повідомлень і дає вчителю змогу "
                 "перевірити кожен коментар перед оприлюдненням.",
            accent="#C93400", fill="FDF0E8")

    # 6
    heading(doc, "6. Культура ведення блогу та відповідальність автора", color=BLUE)
    body(doc, "Оприлюднена інформація залишається в мережі надовго й може "
              "бути скопійована. Тому автор блогу має керуватися простими "
              "правилами: поважати приватність (не публікувати фото дітей "
              "без згоди батьків), перевіряти факти, зазначати джерела, "
              "не використовувати чужі матеріали без дозволу. Ввічливість "
              "у коментарях і відповідях — частина професійної культури "
              "вчителя.")
    bullet(doc, [
        "не публікуйте персональні дані дітей (адреси, телефони, розклад гуртків);",
        "для фото дітей отримайте письмову згоду батьків;",
        "посилайтеся на джерела запозичених матеріалів;",
        "дотримуйтеся авторських прав на зображення й музику;",
        "відповідайте на коментарі ввічливо й у межах робочого часу.",
    ])

    # ------------------------------------------------------------------
    heading(doc, "Контрольні питання", color=NAVY, space_before=12)
    list_number(doc, [
        "Що таке Веб 2.0 і чим він відрізняється від Веб 1.0?",
        "Назвіть три ключові ознаки технологій Веб 2.0.",
        "Які соціальні сервіси Веб 2.0 ви знаєте? Наведіть приклади.",
        "Що таке вікі-сайт і в чому його відмінність від блогу?",
        "Дайте визначення веб-журналу (блогу).",
        "Які різновиди веб-журналів виділяють за змістом?",
        "Які безкоштовні платформи для створення блогу ви знаєте?",
        "Назвіть основні етапи створення веб-журналу.",
        "Що таке шаблон блогу і які його основні елементи?",
        "Які параметри блогу слід налаштувати перед публікацією першого допису?",
        "Для чого в блозі використовують теги й рубрики?",
        "Яких правил безпеки та етикету слід дотримуватися під час ведення блогу?",
    ])

    heading(doc, "Рекомендовані джерела", color=NAVY, space_before=10)
    list_number(doc, [
        "Потієнко В. О. Графічний дизайн : рівень стандарту (вибірковий модуль "
        "для 10–11 кл.). Харків : Ранок, 2020. 160 с.",
        "Речич Н. В. Вебтехнології : рівень стандарту (вибірковий модуль "
        "для 10–11 кл.). Харків : Ранок, 2020. 160 с.",
        "Офісні технології : навч. посіб. / Трофименко О. Г., Прокоп Ю. В., "
        "Логінова Н. І., Чанишев Р. І. Одеса : Фенікс, 2019. 207 с.",
    ])

    doc.save(DOCX_NAME)
    return DOCX_NAME


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    p1 = scheme_web2_vs_web1()
    p2 = scheme_blog_types()
    p3 = scheme_blog_creation()
    p4 = scheme_blog_settings()

    schemes = {
        "web2": p1[0],
        "types": p2[0],
        "creation": p3[0],
        "settings": p4[0],
    }
    name = build_document(schemes)
    print("Готово!")
    print("Документ:", os.path.abspath(name))
    print("Схеми PNG/SVG:", os.path.abspath(OUT_DIR))
    for item in (p1, p2, p3, p4):
        print("  -", os.path.basename(item[0]), "+", os.path.basename(item[1]))