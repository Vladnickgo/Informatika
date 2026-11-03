# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: САМОСТІЙНА РОБОТА
Тема: Порівняння графічних інтерфейсів в операційних системах Windows і Linux
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
# СХЕМА 1. Два світи GUI
# ============================================================

def scheme_two_worlds():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.35, "Два світи графічних інтерфейсів",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # ---------- Windows ----------
    px, py, pw, ph = 0.4, 1.4, 6.0, 5.4
    _card(ax, px, py, pw, ph, fill="#E1F0FE", border=ACCENT_BLUE, radius=0.2)
    ax.text(px + pw / 2, py + ph - 0.5, "Windows",
            ha="center", va="center", fontsize=16, fontweight="bold",
            color=ACCENT_BLUE)
    ax.text(px + pw / 2, py + ph - 0.95,
            "оболонка — Explorer",
            ha="center", va="center", fontsize=12, style="italic",
            color=TEXT_DARK)

    # Міні-макет вікна Explorer
    wx, wy, ww, wh = px + 0.4, py + 1.0, pw - 0.8, 2.9
    ax.add_patch(FancyBboxPatch((wx, wy), ww, wh,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor="white", edgecolor="#404040",
                                linewidth=1.2))
    ax.add_patch(Rectangle((wx, wy + wh - 0.35), ww, 0.35,
                           facecolor=ACCENT_BLUE))
    ax.text(wx + ww / 2, wy + wh - 0.18, "Проводник — C:\\Навчання",
            ha="center", va="center", fontsize=9, color="white",
            fontweight="bold")

    # Ліва панель «дерево»
    ax.add_patch(Rectangle((wx, wy), 1.3, wh - 0.35,
                           facecolor="#F5F5F7", edgecolor="#BFBFBF",
                           linewidth=0.8))
    for i, line in enumerate(["📁 Робочий стіл", "💾 Диск C:", "  📁 Навчання"]):
        ax.text(wx + 0.1, wy + wh - 0.65 - i * 0.35, line,
                ha="left", va="center", fontsize=7.5, color=TEXT_DARK)

    # Права панель «вміст»
    for i, line in enumerate(["📁 Конспекти", "📄 план.docx"]):
        ax.text(wx + 1.5, wy + wh - 0.65 - i * 0.4, line,
                ha="left", va="center", fontsize=8, color=TEXT_DARK)

    ax.text(px + pw / 2, py + 0.55,
            "Панель завдань · меню «Пуск»\n"
            "єдина оболонка для всіх версій",
            ha="center", va="center", fontsize=10.5,
            color=TEXT_DARK, linespacing=1.6)

    # ---------- Linux ----------
    gx = 6.65
    _card(ax, gx, py, pw, ph, fill="#E8F8EC", border=ACCENT_GREEN, radius=0.2)
    ax.text(gx + pw / 2, py + ph - 0.5, "Linux",
            ha="center", va="center", fontsize=16, fontweight="bold",
            color=ACCENT_GREEN)
    ax.text(gx + pw / 2, py + ph - 0.95,
            "середовища — GNOME, KDE",
            ha="center", va="center", fontsize=12, style="italic",
            color=TEXT_DARK)

    # Дві невеликі картки GNOME / KDE
    sub_w, sub_h = 2.6, 2.9
    gap = 0.2
    sx0 = gx + (pw - (2 * sub_w + gap)) / 2
    sy = py + 1.0

    for i, (name, desc) in enumerate([
        ("GNOME", "мінімалізм,\nспрощений вигляд"),
        ("KDE Plasma", "гнучкість,\nбагато налаштувань"),
    ]):
        x = sx0 + i * (sub_w + gap)
        ax.add_patch(FancyBboxPatch((x, sy), sub_w, sub_h,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor="white", edgecolor="#404040",
                                    linewidth=1.2))
        ax.add_patch(Rectangle((x, sy + sub_h - 0.35), sub_w, 0.35,
                               facecolor=ACCENT_GREEN))
        ax.text(x + sub_w / 2, sy + sub_h - 0.18, name,
                ha="center", va="center", fontsize=9, color="white",
                fontweight="bold")
        ax.text(x + sub_w / 2, sy + 1.15, desc,
                ha="center", va="center", fontsize=9.5,
                color=TEXT_DARK, linespacing=1.6)

    ax.text(gx + pw / 2, py + 0.55,
            "Різні оболонки на вибір\n"
            "легко змінити без перевстановлення",
            ha="center", va="center", fontsize=10.5,
            color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_two_worlds")


# ============================================================
# СХЕМА 2. Спільні риси
# ============================================================

def scheme_common():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.4)
    ax.axis("off")

    ax.text(6.5, 6.0, "Спільні риси графічних інтерфейсів",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    items = [
        ("Робочий стіл", "Desktop",
         "головна область\nпісля входу", ACCENT_BLUE, "#E1F0FE"),
        ("Панель", "Panel / Taskbar",
         "запуск програм,\nперемикання вікон", ACCENT_GREEN, "#E8F8EC"),
        ("Файловий\nменеджер", "Explorer / Nautilus",
         "робота з файлами\nй папками", ACCENT_ORANGE, "#FFF4E5"),
        ("Вікна", "Windows",
         "прямокутні області\nпрограм", ACCENT_PURPLE, "#EFE6F7"),
        ("Сповіщення", "Notifications",
         "повідомлення\nсистеми", ACCENT_RED, "#FFEBEA"),
    ]

    card_w, card_h = 2.35, 4.0
    gap = 0.15
    x0 = (13 - (5 * card_w + 4 * gap)) / 2
    y0 = 1.0

    for i, (title, eng, desc, color, fill) in enumerate(items):
        x = x0 + i * (card_w + gap)
        cx = x + card_w / 2
        _card(ax, x, y0, card_w, card_h, fill=fill, border=color, radius=0.15)
        ax.text(cx, y0 + card_h - 0.6, title, ha="center", va="center",
                fontsize=12, fontweight="bold", color=color,
                linespacing=1.4)
        ax.text(cx, y0 + card_h - 1.45, eng, ha="center", va="center",
                fontsize=10, style="italic", color=TEXT_GRAY,
                linespacing=1.3)
        ax.text(cx, y0 + 1.3, desc, ha="center", va="center",
                fontsize=10.5, color=TEXT_DARK, linespacing=1.6)

    return _save(fig, "scheme_common")


# ============================================================
# СХЕМА 3. Ключові відмінності
# ============================================================

def scheme_differences():
    fig, ax = plt.subplots(figsize=(11, 7.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.0)
    ax.axis("off")

    ax.text(6.5, 8.55, "Ключові відмінності Windows і Linux",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # Заголовки колонок
    ax.text(3.4, 7.9, "WINDOWS", ha="center", va="center",
            fontsize=13, fontweight="bold", color=ACCENT_BLUE)
    ax.text(9.6, 7.9, "LINUX", ha="center", va="center",
            fontsize=13, fontweight="bold", color=ACCENT_GREEN)

    rows = [
        ("ОБОЛОНКА",
         "Одна на всі версії —\nExplorer",
         "Багато на вибір:\nGNOME, KDE, XFCE"),
        ("МЕНЮ «ПУСК»",
         "Фіксоване, однакове\nна всіх ПК",
         "Може бути відсутнім\n(залежить від оболонки)"),
        ("НАЛАШТУВАННЯ",
         "Єдині «Параметри»\nWindows",
         "Окремі для кожної\nоболонки"),
        ("ТЕМИ\nОФОРМЛЕННЯ",
         "Обмежені,\nздебільшого через\nMicrosoft Store",
         "Будь-які — від\nспільноти, часто\nбезкоштовні"),
        ("РОЗШИРЕННЯ",
         "Через Marketplace\nабо .exe-інсталятори",
         "Через пакетні\nменеджери (apt, dnf)"),
    ]

    label_w, left_x, right_x = 2.2, 4.55, 10.8
    card_w = 3.9
    card_h = 1.1
    gap_y = 0.18
    y_top = 7.4

    for i, (label, win, lin) in enumerate(rows):
        y = y_top - (i + 1) * (card_h + gap_y)
        # Етикетка
        _card(ax, 0.4, y, label_w, card_h, fill=CARD_BG,
              border=CARD_BORDER, radius=0.14)
        ax.text(0.4 + label_w / 2, y + card_h / 2, label,
                ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=TEXT_DARK, linespacing=1.4)

        # Windows
        _card(ax, left_x, y, card_w, card_h, fill="#E1F0FE",
              border=ACCENT_BLUE, radius=0.14)
        ax.text(left_x + card_w / 2, y + card_h / 2, win,
                ha="center", va="center", fontsize=10.5,
                color=TEXT_DARK, linespacing=1.5)

        # Linux
        _card(ax, right_x, y, card_w, card_h, fill="#E8F8EC",
              border=ACCENT_GREEN, radius=0.14)
        ax.text(right_x + card_w / 2, y + card_h / 2, lin,
                ha="center", va="center", fontsize=10.5,
                color=TEXT_DARK, linespacing=1.5)

    return _save(fig, "scheme_differences")


# ============================================================
# СХЕМА 4. Етапи роботи
# ============================================================

def scheme_steps():
    fig, ax = plt.subplots(figsize=(11, 8.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    ax.text(6.5, 9.1, "Етапи виконання самостійної роботи",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    steps = [
        "Опрацювати теоретичний матеріал і схеми 1–3",
        "Заповнити порівняльну таблицю (5 параметрів)",
        "Скласти список переваг і недоліків кожної ОС",
        "Підготувати відповіді на теоретичні питання",
        "Написати висновок про власний вибір GUI",
        "Оформити звіт і надіслати викладачу",
    ]

    card_w, card_h = 9.5, 0.85
    x0 = 2.0
    y_top = 8.3

    for i, step in enumerate(steps):
        y = y_top - i * 1.35
        cx = x0 + card_w / 2
        _card(ax, x0, y - card_h / 2, card_w, card_h,
              fill=CARD_BG, border=CARD_BORDER, radius=0.15)
        _badge(ax, 1.3, y, 0.6, 0.6, ACCENT_BLUE, str(i + 1),
               color="white", size=14, radius=0.3)
        ax.text(cx, y, step, ha="center", va="center",
                fontsize=11.5, color=TEXT_DARK)
        if i < len(steps) - 1:
            ax.annotate("", xy=(cx, y - card_h / 2 - 0.45),
                        xytext=(cx, y - card_h / 2 - 0.02),
                        arrowprops=dict(arrowstyle="-|>", color=TEXT_GRAY,
                                        linewidth=1.4, mutation_scale=12))

    return _save(fig, "scheme_steps")


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
    img1 = scheme_two_worlds()
    img2 = scheme_common()
    img3 = scheme_differences()
    img4 = scheme_steps()

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

    h1(doc, "Самостійна робота")
    theme_line(doc, "Порівняння графічних інтерфейсів в операційних "
                    "системах Windows і Linux")

    h2(doc, "Мета")
    body(doc, "дослідити спільні риси та відмінності між графічними "
              "середовищами Windows (Explorer) і Linux (GNOME, KDE); "
              "розвивати критичне мислення через самостійне виявлення "
              "переваг і недоліків різних GUI; виховувати толерантність "
              "до різних програмних рішень та повагу до різноманіття "
              "операційних систем.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11.",
        "Віртуальна машина з Linux (Ubuntu або Fedora) або доступ "
        "до справжньої системи Linux.",
        "Інструкційні картки із завданнями.",
        "Текстовий редактор для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Загорулько М. І., Сідоров О. М. Операційні системи: практикум. "
        "Київ : Наукова думка, 2019.",
        "Зайцев В. Г., Дробязко І. П. Операційні системи : навч. посіб. "
        "для студ. спец. 123 «Комп'ютерна інженерія». Київ : КПІ ім. "
        "Ігоря Сікорського, 2019.",
        "Іванов О. В., Петрова Н. М. Основи операційних систем : навч. "
        "посіб. Київ : Основи, 2020.",
    ]
    for s in sources:
        numbered(doc, s)

    # ---------- Завдання ----------
    h2(doc, "Завдання самостійної роботи")
    tasks = [
        "Опрацювати теоретичний матеріал і схеми 1–3.",
        "Заповнити порівняльну таблицю «Windows vs Linux» (не менше "
        "6 параметрів).",
        "Скласти список переваг і недоліків кожної ОС (по 3–4 пункти "
        "з кожного боку).",
        "Дати письмові відповіді на теоретичні питання (див. нижче).",
        "Сформулювати обґрунтований висновок про те, який GUI зручніший "
        "саме для вас і для вчителя початкової школи.",
        "Оформити звіт згідно з рекомендаціями та надіслати викладачу "
        "у визначений термін.",
    ]
    for t in tasks:
        numbered(doc, t)

    h2(doc, "Терміни виконання")
    body(doc, "Робота виконується протягом одного тижня після отримання "
              "завдання; готовий звіт подається на наступному "
              "практичному занятті або завантажується в електронний "
              "курс дисципліни до вказаної дати.")

    h2(doc, "Очікувані результати")
    results = [
        "знає назви оболонок графічного інтерфейсу Windows (Explorer) "
        "та Linux (GNOME, KDE, XFCE);",
        "розуміє базову концепцію WIMP та її реалізацію в обох ОС;",
        "називає щонайменше чотири спільні риси графічних інтерфейсів;",
        "характеризує щонайменше п'ять ключових відмінностей між "
        "Windows і Linux;",
        "формулює обґрунтовані переваги й недоліки кожної ОС;",
        "робить власний висновок і пояснює, який GUI доречніший у "
        "навчальному процесі початкової школи.",
    ]
    for r in results:
        bullet(doc, r)

    # ---------- Опрацьовувані питання ----------
    h2(doc, "Перелік опрацьовуваних питань")
    topics = [
        "Поняття графічного інтерфейсу користувача (GUI).",
        "Концепція WIMP та її реалізація в різних ОС.",
        "Графічна оболонка Windows Explorer: склад, призначення, "
        "ключові елементи.",
        "Графічні середовища Linux: GNOME, KDE Plasma, XFCE — "
        "призначення й особливості.",
        "Спільні риси інтерфейсів Windows і Linux.",
        "Ключові відмінності: оболонки, налаштування, теми, "
        "встановлення програм.",
        "Переваги й недоліки кожної ОС з погляду зручності "
        "користувача.",
        "Відкрите програмне забезпечення та його вплив на дизайн "
        "інтерфейсу.",
        "Вибір GUI для шкільного комп'ютерного класу.",
    ]
    for tp in topics:
        numbered(doc, tp)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості (стислий огляд)")

    h3(doc, "1. Два світи графічних інтерфейсів")
    body(doc, "Windows і Linux — дві найпоширеніші настільні "
              "операційні системи. Обидві мають графічний інтерфейс "
              "користувача, але побудовані за різними принципами. "
              "У Windows графічна оболонка одна на всі версії — "
              "Explorer. У Linux оболонок багато (GNOME, KDE Plasma, "
              "XFCE, Cinnamon та інші), і користувач може обрати ту, "
              "що йому до вподоби.")

    add_figure(doc, img1, 16.0)

    body(doc, "Розуміння цієї відмінності — ключ до подальшого "
              "порівняння. Windows дає користувачу єдиний, узгоджений "
              "досвід. Linux дає свободу вибору й можливість "
              "настроїти систему під себе. Обидва підходи мають "
              "свої переваги та недоліки.")

    h3(doc, "2. Спільні риси")
    body(doc, "Попри різницю в архітектурі, графічні інтерфейси "
              "Windows і Linux мають багато спільного. Це наслідок "
              "того, що обидві системи реалізують концепцію WIMP і "
              "орієнтуються на звички користувачів, сформовані "
              "десятиліттями.")

    add_figure(doc, img2, 16.0)

    body(doc, "Спільні елементи:")
    bullet(doc, "робочий стіл — головна область після входу в "
                "систему;")
    bullet(doc, "панель (taskbar у Windows, panel у Linux) — запуск "
                "програм і перемикання між вікнами;")
    bullet(doc, "файловий менеджер — Проводник (Windows) або "
                "Nautilus / Dolphin (Linux);")
    bullet(doc, "вікна програм із кнопками згортання, розгортання "
                "та закриття;")
    bullet(doc, "система сповіщень про події та помилки;")
    bullet(doc, "піктограми, меню, контекстне меню (права кнопка "
                "миші), гарячі клавіші (Ctrl + C, Ctrl + V).")

    h3(doc, "3. Ключові відмінності")
    body(doc, "Основна відмінність між Windows і Linux — ступінь "
              "свободи користувача. Розгляньмо це на конкретних "
              "параметрах порівняння.")

    add_figure(doc, img3, 16.0)

    add_table(
        doc,
        ["Параметр", "Windows", "Linux"],
        [
            ["Оболонка GUI",
             "Explorer — одна на всі версії",
             "GNOME, KDE, XFCE, Cinnamon — на вибір"],
            ["Меню «Пуск»",
             "Фіксоване, однакове",
             "Може бути відсутнім або налаштовуватися"],
            ["Налаштування системи",
             "Єдині «Параметри»",
             "Окремі для кожної оболонки"],
            ["Теми оформлення",
             "Обмежені, часто платні",
             "Будь-які, часто безкоштовні"],
            ["Встановлення програм",
             "Через Marketplace або .exe-інсталятори",
             "Через пакетні менеджери (apt, dnf, pacman)"],
            ["Відкритість коду",
             "Пропрієтарна (закритий код)",
             "Вільна (відкритий код)"],
            ["Ліцензія",
             "Платна (або OEM-версія з пристроєм)",
             "Безкоштовна"],
        ],
        widths=[3.6, 6.3, 6.6],
    )

    h3(doc, "4. Переваги й недоліки кожної ОС")
    body(doc, "Обидві системи мають сильні й слабкі сторони. "
              "Важливо не ставати на бік однієї з них, а розуміти, "
              "у яких умовах кожна з них доречніша.")

    add_table(
        doc,
        ["Windows: переваги", "Windows: недоліки"],
        [
            ["Узгоджений інтерфейс для всіх користувачів",
             "Обмежений вибір тем і налаштувань"],
            ["Величезна кількість програм і драйверів",
             "Платна ліцензія"],
            ["Звичність для більшості користувачів",
             "Закритий код (незалежний аудит ускладнений)"],
            ["Потужна підтримка ігор та офісних програм",
             "Періодичні примусові оновлення"],
        ],
        widths=[8.2, 8.3],
    )

    add_table(
        doc,
        ["Linux: переваги", "Linux: недоліки"],
        [
            ["Вибір графічних оболонок під свої потреби",
             "Потрібен час на опанування"],
            ["Безкоштовність і відкритий код",
             "Деякі програми Windows не запускаються напряму"],
            ["Високий рівень налаштування",
             "Фрагментованість: різні дистрибутиви поводяться "
             "по-різному"],
            ["Стабільність і безпека",
             "Менша кількість «звичних» програм для звичайного "
             "користувача"],
        ],
        widths=[8.2, 8.3],
    )

    callout(doc,
            "Порівнюючи ОС, важливо пам'ятати: не існує "
            "«найкращої» системи взагалі. Є система, найдоречніша "
            "для конкретних умов. Наприклад, для ігрового "
            "комп'ютера — Windows, для серверів — Linux, для "
            "навчального класу — залежить від бюджету, навичок "
            "адміністратора й потреб учнів.",
            fill="E1F0FE", accent="0071E3")

    h3(doc, "5. GUI у навчальному процесі")
    body(doc, "Для вчителя початкової школи вибір графічного "
              "середовища не є абстрактним питанням. Він впливає на "
              "те, наскільки швидко діти опановують комп'ютер, "
              "наскільки безпечно почуваються за ним і скільки часу "
              "витрачає вчитель на пояснення.")

    body(doc, "У навчальному класі важливі три речі:")
    bullet(doc, "узгодженість інтерфейсу — діти мають бачити "
                "однакові елементи в усіх програмах;")
    bullet(doc, "простота — мінімум зайвих кнопок і налаштувань;")
    bullet(doc, "стабільність — однакове середовище на всіх "
                "комп'ютерах класу.")

    body(doc, "Windows традиційно краще підходить для масового "
              "шкільного класу завдяки узгодженості та звичності. "
              "Linux із правильно підібраною оболонкою (наприклад, "
              "GNOME або XFCE) також може бути чудовим вибором — "
              "особливо якщо школа хоче заощадити на ліцензіях і "
              "використовувати вільне програмне забезпечення.")

    callout(doc,
            "У багатьох європейських школах успішно працюють "
            "комп'ютерні класи на Linux. Учні опановують LibreOffice, "
            "GIMP, Firefox та інші вільні програми — і не відчувають "
            "жодних незручностей. Головне — щоб інтерфейс був "
            "узгоджений і вчитель розумів, як ним користуватися.",
            fill="E8F8EC", accent="248A3D")

    # =====================================================
    # ЕТАПИ ВИКОНАННЯ
    # =====================================================
    h2(doc, "Етапи виконання самостійної роботи")
    body(doc, "Робота виконується послідовно за шість етапів. Кожен "
              "етап завершується певним результатом, який стане "
              "частиною звіту.")

    add_figure(doc, img4, 15.5)

    # ---------- Порівняльна таблиця ----------
    h2(doc, "Завдання на заповнення порівняльної таблиці")
    body(doc, "Заповніть таблицю, указавши характеристики кожного "
              "параметра для Windows і Linux. Спробуйте знайти не "
              "менше 6 параметрів для порівняння — від базових "
              "(назва оболонки) до складніших (модель встановлення "
              "програм, рівень свободи налаштувань).")

    add_table(
        doc,
        ["№", "Параметр", "Windows", "Linux"],
        [
            ["1", "Назва оболонки GUI", "", ""],
            ["2", "Наявність меню «Пуск»", "", ""],
            ["3", "Кількість доступних тем", "", ""],
            ["4", "Спосіб встановлення програм", "", ""],
            ["5", "Відкритість коду", "", ""],
            ["6", "Ліцензія", "", ""],
            ["7", "Складність для новачка", "", ""],
            ["8", "Гнучкість налаштувань", "", ""],
        ],
        widths=[1.0, 4.0, 5.7, 5.8],
    )

    # ---------- Список переваг ----------
    h2(doc, "Завдання на складання списку переваг і недоліків")
    body(doc, "Складіть список із 3–4 переваг і 3–4 недоліків для "
              "кожної ОС. Кожен пункт сформулюйте одним реченням і "
              "поясніть, для кого саме це є перевагою або недоліком.")
    body(doc, "Оформіть у вигляді чотирьох списків: «Windows — "
              "переваги», «Windows — недоліки», «Linux — переваги», "
              "«Linux — недоліки».")

    # =====================================================
    # ТЕОРЕТИЧНІ ПИТАННЯ
    # =====================================================
    h2(doc, "Теоретичні питання для самоперевірки")
    questions = [
        "Що таке графічний інтерфейс користувача? Чому він став "
        "важливим етапом розвитку ОС?",
        "Розшифруйте абревіатуру WIMP. Як кожен складник реалізовано "
        "в Windows і в Linux?",
        "Назвіть графічну оболонку Windows. Які її основні елементи?",
        "Які графічні середовища Linux ви знаєте? Чим GNOME "
        "відрізняється від KDE Plasma?",
        "Наведіть чотири спільні риси графічних інтерфейсів Windows "
        "і Linux.",
        "Назвіть п'ять ключових відмінностей між Windows і Linux.",
        "Чому в Linux існує багато оболонок, а в Windows — лише одна? "
        "Які переваги й недоліки кожного підходу?",
        "Які переваги дає відкритий код Linux для розвитку "
        "графічного інтерфейсу?",
        "Як вибір графічної оболонки впливає на роботу вчителя "
        "початкової школи з учнями?",
        "Який GUI ви обрали б для комп'ютерного класу початкової "
        "школи? Обґрунтуйте відповідь.",
    ]
    for q in questions:
        numbered(doc, q)

    # =====================================================
    # РЕКОМЕНДАЦІЇ ДО ОФОРМЛЕННЯ
    # =====================================================
    h2(doc, "Рекомендації до оформлення звіту")
    body(doc, "Звіт оформлюється у текстовому редакторі (MS Word / "
              "LibreOffice Writer) і повинен містити такі обов'язкові "
              "структурні елементи:")
    structure = [
        "Титульна сторінка: назва навчального закладу, тема, ПІБ "
        "студента, група, ПІБ викладача, рік.",
        "Мета та завдання роботи.",
        "Заповнена порівняльна таблиця (не менше 6 параметрів).",
        "Чотири списки переваг і недоліків (Windows / Linux).",
        "Відповіді на теоретичні питання (письмово, стисло).",
        "Висновок: 5–7 речень про те, який GUI зручніший для вас "
        "особисто і для вчителя початкової школи; обґрунтуйте "
        "відповідь.",
        "Список використаних джерел (оформлений за ДСТУ 8302:2015).",
    ]
    for s in structure:
        numbered(doc, s)

    body(doc, "Технічні параметри оформлення: шрифт Times New Roman, "
              "14 pt, міжрядковий інтервал 1,15, поля 2 см, абзацний "
              "відступ 1,25 см, вирівнювання за шириною. Обсяг "
              "звіту — 4–6 сторінок без урахування титульної "
              "сторінки та додатків. Ім'я файлу: "
              "«СР_GUI_Windows_Linux_ПІБ.docx».")

    # =====================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =====================================================
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Критерій", "Бали"],
        [
            ["Повнота й коректність теоретичної частини", "3"],
            ["Правильність заповнення порівняльної таблиці", "2"],
            ["Повнота списків переваг і недоліків кожної ОС", "2"],
            ["Відповіді на теоретичні питання", "2"],
            ["Обґрунтованість висновку про власний вибір GUI", "2"],
            ["Оформлення звіту згідно з рекомендаціями", "1"],
            ["Творчий підхід, власні приклади й спостереження", "1"],
        ],
        widths=[12.5, 4.0],
    )

    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (потребує доопрацювання).")

    doc.save("Самостійна_робота_GUI_Windows_Linux.docx")
    print("Готово: Самостійна_робота_GUI_Windows_Linux.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()