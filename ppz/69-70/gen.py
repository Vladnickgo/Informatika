# -*- coding: utf-8 -*-
"""
Практичне заняття № 20. Електронна пошта та її використання.
Генерація docx-документа + 4 схем (PNG/SVG) у стилі Apple.
Запуск:  python praktychne_20_poshta.py
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
DOCX_NAME = "Praktychne_zanyattya_20_Elektronna_poshta.docx"
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

# стиль схем
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
    """Переносить текст по словах, зберігаючи явні переходи рядка."""
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
    """Картка у стилі Apple з автоматичним підбором кеглю (без виходу тексту за межі)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=1.1",
                                linewidth=1.4, edgecolor=C_EDGE,
                                facecolor=fill, zorder=2))
    xr = ax.get_xlim()[1]
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
# СХЕМА 1. Шлях електронного листа
# ----------------------------------------------------------------------------
def scheme_email_flow():
    fig, ax = _fig(12.0, 3.9, 100, 32)
    ax.text(50, 29.3, "Шлях електронного листа", ha="center", va="center",
            fontsize=15, color=C_TEXT, fontweight="bold")

    items = [
        ("Відправник", "створює лист\nі натискає «Надіслати»", C_BLUE),
        ("Поштовий сервер\nвідправника", "приймає лист,\nпротокол SMTP", C_BLUE),
        ("Мережа Інтернет", "DNS знаходить\nсервер за доменом", C_GRAY),
        ("Поштовий сервер\nотримувача", "зберігає лист\nу скриньці", C_GREEN),
        ("Отримувач", "читає лист\nу вебпошті або IMAP", C_GREEN),
    ]
    w, h, y = 17.0, 15.0, 8.0
    xs = [2.0, 21.6, 41.2, 60.8, 80.4]
    for x, (t, s, col) in zip(xs, items):
        card(ax, fig, x, y, w, h, t, s, fs=12.5, accent=col)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + w + 0.5, y + h / 2.0, xs[i + 1] - 0.5, y + h / 2.0)
    return save_scheme(fig, "email_flow")


# ----------------------------------------------------------------------------
# СХЕМА 2. Анатомія ділового листа
# ----------------------------------------------------------------------------
def scheme_email_structure():
    fig, ax = _fig(12.0, 3.8, 100, 30)
    ax.text(50, 27.4, "Анатомія ділового електронного листа", ha="center",
            va="center", fontsize=15, color=C_TEXT, fontweight="bold")

    items = [
        ("Тема", "5–7 слів,\nбез «!!!»", C_BLUE),
        ("Звертання", "«Добрий день,\nпані Оксано!»", C_PURPLE),
        ("Основна частина", "факти й прохання,\nодне питання", C_TEXT),
        ("Підпис", "ім’я, посада,\nконтакти", C_GREEN),
        ("Вкладення", "файл до 20 МБ,\nназва без пробілів", C_ORANGE),
    ]
    w, h, y = 18.0, 16.0, 6.0
    xs = [1.0, 20.6, 40.2, 59.8, 79.4]
    for x, (t, s, col) in zip(xs, items):
        card(ax, fig, x, y, w, h, t, s, fs=12.5, accent=col)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + w + 0.4, y + h / 2.0, xs[i + 1] - 0.4, y + h / 2.0)
    return save_scheme(fig, "email_structure")


# ----------------------------------------------------------------------------
# СХЕМА 3. Антиспам-захист
# ----------------------------------------------------------------------------
def scheme_spam_defense():
    fig, ax = _fig(12.0, 4.9, 100, 40)
    ax.text(50, 37.4, "Антиспам-захист поштової скриньки", ha="center",
            va="center", fontsize=15, color=C_TEXT, fontweight="bold")

    items = [
        ("Перевірка адреси", "звіряйте домен,\nа не лише ім’я", C_BLUE),
        ("Фільтри й правила", "сортування за темою\nта адресою", C_GREEN),
        ("Чорний список", "блокування\nвідомих спамерів", C_ORANGE),
        ("Двофакторний вхід", "пароль + код\nіз телефона", C_PURPLE),
    ]
    w, h, y = 22.0, 14.5, 17.5
    xs = [1.8, 26.2, 50.6, 75.0]
    for x, (t, s, col) in zip(xs, items):
        card(ax, fig, x, y, w, h, t, s, fs=12.5, accent=col)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + w + 0.4, y + h / 2.0, xs[i + 1] - 0.4, y + h / 2.0)

    card(ax, fig, 1.8, 4.0, 95.2, 9.0,
         "Правило: спершу перевір адресу відправника — потім відкривай вкладення",
         None, fs=13, accent=C_RED, fill="#FDF1F2")
    return save_scheme(fig, "spam_defense")


# ----------------------------------------------------------------------------
# СХЕМА 4. Різнорівневі завдання
# ----------------------------------------------------------------------------
def scheme_levels():
    fig, ax = _fig(12.0, 4.2, 100, 35)
    ax.text(50, 32.4, "Різнорівневі завдання: 25–30 хв, 13 балів", ha="center",
            va="center", fontsize=15, color=C_TEXT, fontweight="bold")

    items = [
        ("Рівень 1\nРепродуктивний", "7 хв · 3 бали\nреєстрація скриньки,\nпростий лист", C_BLUE),
        ("Рівень 2\nПродуктивний", "10 хв · 4 бали\nвкладення, підпис,\nфільтри", C_ORANGE),
        ("Рівень 3\nТворчий", "10 хв · 5 балів\nлист-пам’ятка\nдля батьків", C_GREEN),
    ]
    w, h, y = 29.0, 19.5, 7.0
    xs = [1.0, 35.5, 70.0]
    for x, (t, s, col) in zip(xs, items):
        card(ax, fig, x, y, w, h, t, s, fs=13, accent=col)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + w + 0.5, y + h / 2.0, xs[i + 1] - 0.5, y + h / 2.0)
    return save_scheme(fig, "levels")


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
    """Текст із підтримкою `команд` — Consolas, червоний."""
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

    heading(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 20", color=NAVY,
            align=CENTER, space_before=0, space_after=4)

    tp = doc.add_paragraph()
    tp.alignment = CENTER
    tp.paragraph_format.space_after = Pt(8)
    add_rich_text(
        tp,
        "Тема: Електронна пошта та її використання. Основи роботи "
        "з електронною поштою. Безпека електронної пошти та антиспам-заходи.",
        size=14, bold=True)

    heading(doc, "Мета", color=BLUE, space_before=4)
    body(doc, "Опанувати реєстрацію поштової скриньки, надсилання й отримання "
              "листів, роботу з вкладеннями, налаштування фільтрів та захист від "
              "спаму. Розвивати навички ділової комунікації, уміння структурувати "
              "лист і захищати обліковий запис. Виховувати етикет електронного "
              "листування, відповідальність за безпеку паролів і повагу до чужого часу.")

    heading(doc, "Обладнання та програмне забезпечення", color=BLUE)
    numbered_paren(doc, [
        "персональний комп’ютер з доступом до мережі Інтернет;",
        "браузер `Google Chrome` або `Mozilla Firefox`;",
        "поштовий сервіс `Gmail` або `Ukr.net` (веб-інтерфейс);",
        "інструкційні картки практичного заняття;",
        "файли-заготовки для вкладення: `zvit.docx`, `pamyatka.docx`.",
    ])

    heading(doc, "Література", color=BLUE)
    list_number(doc, [
        "Шумілова І. Ф. Новітні технології викладання освітніх галузей "
        "у початковій школі : навч. посіб. Київ : Олді, 2023. 248 с.",
        "Юнчик В. Л. Системне, прикладне програмне забезпечення та хмарні "
        "технології в освіті : конспект лекцій для студентів спеціальності "
        "014.09 Середня освіта (Інформатика) першого (бакалаврського) рівня. "
        "Луцьк : ВНУ імені Лесі Українки, 2024. 162 с.",
        "Анісімов А. В., Кулябко П. П. Інформаційні системи та бази даних : "
        "навч. посіб. для студ. ф-ту комп’ютер. наук та кібернетики. Київ, 2017. 110 с.",
    ])

    # ------------------------------------------------------------------
    heading(doc, "Теоретичні відомості", color=NAVY, space_before=12)

    # 1
    heading(doc, "1. Електронна пошта: призначення та адресація", color=BLUE)
    body(doc, "Електронна пошта — це служба передавання повідомлень між "
              "користувачами комп’ютерної мережі. Кожна скринька має адресу виду "
              "`name@domain`, де ліва частина — унікальне ім’я користувача, "
              "а права — домен поштового сервера. Для молодших школярів зручна "
              "аналогія з конвертом: `name` — це «квартира», а `domain` — «будинок», "
              "у якому працює поштове відділення.")
    body(doc, "Працювати з поштою можна двома способами: через веб-інтерфейс "
              "(браузер) і через поштовий клієнт (програму на пристрої). Учителю "
              "початкової школи зручніший веб-інтерфейс: він не потребує налаштувань "
              "і доступний з будь-якого комп’ютера класу.")
    figure(doc, schemes["flow"], "Рис. 1. Шлях електронного листа від відправника до отримувача")

    # 2
    heading(doc, "2. Структура та етикет ділового листа", color=BLUE)
    body(doc, "Діловий лист будується за сталою схемою: тема → звертання → "
              "коротке пояснення мети → суть → конкретне прохання → підпис. "
              "Один лист має містити одне питання: так адресат швидше відповість "
              "і не загубить важливу інформацію серед інших повідомлень.")
    figure(doc, schemes["structure"], "Рис. 2. Анатомія ділового електронного листа")
    add_table(doc,
              ["Елемент листа", "Призначення", "Практична порада"],
              [
                  ["Поле «Кому»", "Основна адреса отримувача",
                   "Перевіряйте адресу після автопідказки"],
                  ["Поле «Копія»", "Отримувачі, які мають бачити лист",
                   "Не перевантажуйте копію зайвими адресами"],
                  ["Поле «Прихована копія»", "Приховані отримувачі листа",
                   "Для розсилки батькам — лише `Bcc`"],
                  ["Поле «Тема»", "Короткий зміст листа",
                   "5–7 слів, без «ТЕРМІНОВО!!!»"],
                  ["Тіло листа", "Суть, розбита на абзаци",
                   "Один лист — одне питання"],
                  ["Вкладення", "Файли, що передаються з листом",
                   "До 20–25 МБ, назва без пробілів"],
              ],
              [4.6, 6.2, 5.2])
    callout(doc, "Якщо лист адресовано батькам усього класу, ставте адреси "
                 "в поле «Прихована копія» (`Bcc`). Так кожен отримувач бачить "
                 "лише своє ім’я і не бачить адрес інших родин — це вимога етикету "
                 "й захисту персональних даних.",
            accent="#0071E3", fill="EAF1F8")

    # 3
    heading(doc, "3. Робота з вкладеннями", color=BLUE)
    body(doc, "Вкладення — це файл, що передається разом із листом. Більшість "
              "сервісів обмежують розмір листа 20–25 МБ, тому великі матеріали "
              "(відео, презентації з ілюстраціями) краще надсилати посиланням "
              "на хмарну теку.")
    bullet(doc, [
        "називайте файли латиницею без пробілів: `homework_2class.docx`;",
        "використовуйте формати `docx`, `pdf`, `jpg`, `png`, `zip`;",
        "не відкривайте вкладення `.exe`, `.scr`, `.js` навіть від знайомих;",
        "після надсилання перевірте, чи файл справді прикріпився, а не лише згаданий у тексті.",
    ])

    # 4
    heading(doc, "4. Безпека поштової скриньки", color=BLUE)
    body(doc, "Поштова скринька — це ключ до багатьох інших сервісів, тому пароль "
              "має бути довгим (12 і більше символів), унікальним і не повторюватися "
              "на інших сайтах. Двофакторна автентифікація додає другий крок входу — "
              "код із телефона, який неможливо вгадати.")
    callout(doc, "Правило двох кроків: пароль зберігайте лише в менеджері паролів, "
                 "а код підтвердження нікому не повідомляйте — навіть людині, "
                 "яка представляється адміністратором школи.",
            accent="#248A3D", fill="EAF6EC")
    add_table(doc,
              ["Ознака підозрілого листа", "Що робити"],
              [
                  ["Невідомий або спотворений домен", "Не відкривати лист, позначити як спам"],
                  ["Прохання «негайно підтвердити пароль»", "Не переходити за посиланням, зайти на сайт вручну"],
                  ["Посилання веде на сторонній сайт", "Навести курсор і перевірити адресу"],
                  ["Вкладення `.exe`, `.scr`, `.js`", "Не завантажувати й не відкривати"],
                  ["Помилки в тексті, звертання «Шановний клієнте!»", "Видалити лист, повідомити адміністратора"],
              ],
              [8.0, 8.0])
    body(doc, "Фішинг — це лист, що імітує повідомлення від відомої установи, аби "
              "змусити вас ввести пароль на підробленій сторінці. Надійна звичка: "
              "заходити на сайт сервісу вручну, а не за посиланням із листа.")

    # 5
    heading(doc, "5. Спам і антиспам-заходи", color=BLUE)
    body(doc, "Спам — це масова небажана розсилка реклами чи шахрайських "
              "повідомлень. Ознаки спаму: невідомий відправник, гучна обіцянка "
              "виграшу, вимога термінової дії, багато посилань і картинок. "
              "Основні засоби захисту — фільтри, чорний список, перевірка адреси "
              "та двофакторний вхід.")
    figure(doc, schemes["spam"], "Рис. 3. Антиспам-захист поштової скриньки")
    callout(doc, "Ніколи не відповідайте на спам і не натискайте «Відписатися» "
                 "в підозрілому листі: так ви підтверджуєте, що адреса активна. "
                 "Позначайте такий лист як спам — фільтр поступово навчиться "
                 "його розпізнавати.",
            accent="#C93400", fill="FDF0E8")

    # 6
    heading(doc, "6. Пошта в роботі вчителя початкової школи", color=BLUE)
    body(doc, "У шкільній практиці пошта замінює частину паперового обігу: "
              "повідомлення батькам, збір дитячих робіт, обмін методичними "
              "матеріалами з колегами. Акуратність листування формує довіру "
              "батьків і економить час усім учасникам.")
    bullet(doc, [
        "розсилка батькам — лише через `Bcc`, тема з класом і датою;",
        "збір робіт учнів — окрема папка `Роботи_2_клас` і фільтр за темою;",
        "шаблони відповідей на типові запитання батьків;",
        "архівування листів наприкінці семестру;",
        "окремі папки для кожного класу й для методичних матеріалів.",
    ])

    # ------------------------------------------------------------------
    heading(doc, "Покроковий алгоритм виконання різнорівневих завдань",
            color=NAVY, space_before=12)
    body(doc, "Практична частина триває 25–30 хв і складається з трьох рівнів: "
              "репродуктивного (7 хв), продуктивного (10 хв) і творчого (10 хв). "
              "Кожен наступний рівень спирається на результат попереднього.")
    figure(doc, schemes["levels"], "Рис. 4. Структура різнорівневих завдань практичного заняття")

    heading(doc, "Рівень 1. Репродуктивний (≈ 7 хв, 3 бали)", color=BLUE)
    add_table(doc,
              ["Крок", "Дія", "Де виконується / команда", "Результат"],
              [
                  ["1", "Відкрийте браузер і перейдіть на поштовий сервіс",
                   "Адресний рядок: `mail.google.com`", "Відкрито сторінку входу"],
                  ["2", "Натисніть `Створити обліковий запис`",
                   "Кнопка на сторінці входу", "Відкрито форму реєстрації"],
                  ["3", "Заповніть ім’я, прізвище, ім’я користувача, пароль",
                   "Поля форми", "Дані введено"],
                  ["4", "Підтвердьте номер телефону кодом із SMS",
                   "Вікно підтвердження", "Скриньку створено"],
                  ["5", "Натисніть `Написати`, вкажіть адресу викладача й тему",
                   "Кнопка `Написати`", "Лист готовий до надсилання"],
                  ["6", "Додайте текст-вітання і натисніть `Надіслати`",
                   "Кнопка `Надіслати`", "Лист у папці «Надіслані»"],
                  ["7", "Відкрийте папку `Вхідні` і прочитайте лист-відповідь",
                   "Папки пошти", "Лист прочитано"],
              ],
              [1.3, 5.6, 5.3, 3.8])

    heading(doc, "Рівень 2. Продуктивний (≈ 10 хв, 4 бали)", color=BLUE)
    add_table(doc,
              ["Крок", "Дія", "Налаштування / команда", "Результат"],
              [
                  ["1", "Створіть файл `zvit.docx` з прізвищем, групою і датою",
                   "Текстовий процесор", "Файл створено"],
                  ["2", "У вікні листа натисніть `Прикріпити файл` (скріпка)",
                   "Панель інструментів листа", "Відкрито діалог вибору файлу"],
                  ["3", "Виберіть `zvit.docx` і дочекайтеся завантаження",
                   "Діалог файлів", "Вкладення додано"],
                  ["4", "Перевірте назву й розмір вкладення (до 20–25 МБ)",
                   "Вікно листа", "Вкладення коректне"],
                  ["5", "Налаштуйте підпис: `Налаштування` → `Загальні` → `Підпис`",
                   "Меню налаштувань", "Підпис збережено"],
                  ["6", "Створіть фільтр: `Налаштування` → `Фільтри` → `Створити фільтр`",
                   "Меню фільтрів", "Правило створено"],
                  ["7", "Перевірте дію фільтра на тестовому листі",
                   "Папки пошти", "Лист відсортовано автоматично"],
              ],
              [1.3, 5.6, 5.3, 3.8])

    heading(doc, "Рівень 3. Творчий (≈ 10 хв, 5 балів)", color=BLUE)
    body(doc, "Завдання: підготуйте лист-пам’ятку для батьків учнів 2 класу про "
              "домашнє завдання з інформатики. Лист має містити вкладення "
              "`pamyatka.docx`, адреси батьків — у полі «Прихована копія», "
              "а відповіді батьків мають автоматично потрапляти в папку «Батьки».")
    add_table(doc,
              ["Етап", "Зміст роботи", "Результат"],
              [
                  ["1", "Скласти текст за схемою: тема → звертання → суть → "
                        "прохання → підпис (5–7 речень)", "Готовий текст листа"],
                  ["2", "Додати вкладення `pamyatka.docx`, перевірити назву файлу",
                   "Вкладення прикріплено"],
                  ["3", "Розмістити адреси батьків у полі `Bcc`, перевірити поле «Кому»",
                   "Розсилку налаштовано"],
                  ["4", "Створити фільтр «відповіді батьків» → папка `Батьки`",
                   "Фільтр працює"],
                  ["5", "Зробити 2–3 скріншоти та зберегти їх для звіту",
                   "Скріншоти готові"],
              ],
              [1.2, 10.3, 4.5])

    # ------------------------------------------------------------------
    heading(doc, "Критерії оцінювання", color=NAVY, space_before=12)
    add_table(doc,
              ["Вид роботи", "Показник", "Бали"],
              [
                  ["Рівень 1", "Скриньку створено, лист надіслано й прочитано", "3"],
                  ["Рівень 2", "Вкладення, підпис і фільтр налаштовано коректно", "4"],
                  ["Рівень 3", "Лист-пам’ятка повний, `Bcc` і фільтр використано", "5"],
                  ["Звіт", "Звіт оформлено, скріншоти наявні", "1"],
                  ["Разом", "Максимальна кількість балів за заняття", "13"],
              ],
              [4.0, 10.0, 2.0])

    heading(doc, "Форма звітності", color=BLUE)
    bullet(doc, [
        "звіт у файлі `zvit.docx`, назва якого містить прізвище студента;",
        "адреса створеної поштової скриньки;",
        "3–4 скріншоти: реєстрація, лист із вкладенням, налаштований фільтр, лист-пам’ятка;",
        "короткий опис створеного фільтра (умова → дія);",
        "висновок: 2–3 речення про те, які заходи захисту скриньки ви вважаєте обов’язковими.",
    ])

    doc.save(DOCX_NAME)
    return DOCX_NAME


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    p1 = scheme_email_flow()
    p2 = scheme_email_structure()
    p3 = scheme_spam_defense()
    p4 = scheme_levels()

    schemes = {
        "flow": p1[0],
        "structure": p2[0],
        "spam": p3[0],
        "levels": p4[0],
    }
    name = build_document(schemes)
    print("Готово!")
    print("Документ:", os.path.abspath(name))
    print("Схеми PNG/SVG:", os.path.abspath(OUT_DIR))
    for item in (p1, p2, p3, p4):
        print("  -", os.path.basename(item[0]), "+", os.path.basename(item[1]))