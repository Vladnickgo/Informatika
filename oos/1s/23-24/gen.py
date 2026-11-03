# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ПРАКТИЧНЕ ЗАНЯТТЯ
Тема: Використання команд для роботи з мережею
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
TERM_BG = "#1C1C1E"
TERM_BODY = "#000000"
TERM_TEXT = "#D1D1D6"
TERM_PROMPT = "#30D158"


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
# СХЕМА 1. Основні мережеві команди
# ============================================================

def scheme_commands():
    fig, ax = plt.subplots(figsize=(11, 7.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.0)
    ax.axis("off")

    ax.text(6.5, 8.55, "Основні мережеві команди",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    commands = [
        ("ping", "ping <адреса>",
         "Перевірка доступності\nвузла за 4 пакети", ACCENT_BLUE, "#E1F0FE"),
        ("ipconfig", "ipconfig [/all]",
         "Показ власних\nIP-адрес, шлюзу, DNS", ACCENT_GREEN, "#E8F8EC"),
        ("tracert", "tracert <адреса>",
         "Маршрут до вузла —\nусі проміжні хопи", ACCENT_ORANGE, "#FFF4E5"),
        ("net", "net view | net use",
         "Перегляд мережевих\nресурсів і підключень", ACCENT_RED, "#FFEBEA"),
        ("nslookup", "nslookup <домен>",
         "Перевірка DNS:\nIP за доменним ім'ям", ACCENT_PURPLE, "#EFE6F7"),
        ("netstat", "netstat -an",
         "Активні з'єднання\nта відкриті порти", ACCENT_BLUE, "#E1F0FE"),
    ]

    card_w, card_h = 3.9, 2.7
    gap_x, gap_y = 0.25, 0.3
    x0 = 0.4
    y_top = 7.9

    for i, (cmd, syntax, desc, color, fill) in enumerate(commands):
        col, row = i % 3, i // 3
        x = x0 + col * (card_w + gap_x)
        y = y_top - card_h - row * (card_h + gap_y)
        cx = x + card_w / 2
        _card(ax, x, y, card_w, card_h, fill=fill, border=color, radius=0.18)
        _badge(ax, cx, y + card_h - 0.55, 2.1, 0.55, color, cmd,
               color="white", size=13.5, radius=0.28)
        ax.text(cx, y + card_h - 1.25, syntax, ha="center", va="center",
                fontsize=10, color=TEXT_GRAY, family="monospace")
        ax.text(cx, y + 0.85, desc, ha="center", va="center",
                fontsize=11, color=TEXT_DARK, linespacing=1.55)

    return _save(fig, "scheme_commands")


# ============================================================
# СХЕМА 2. Діагностика: ping і tracert
# ============================================================

def scheme_diagnostics():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.4)
    ax.axis("off")

    ax.text(6.5, 7.0, "Діагностика: ping і tracert",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    # ---------- Ліва панель: ping ----------
    px, py, pw, ph = 0.35, 2.0, 6.0, 4.5
    ax.add_patch(FancyBboxPatch((px, py), pw, ph,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=TERM_BG, edgecolor="#3A3A3C",
                                linewidth=1.6))
    ax.add_patch(Rectangle((px, py + ph - 0.55), pw, 0.55,
                           facecolor="#2C2C2E"))
    ax.text(px + 0.2, py + ph - 0.28, "ping 8.8.8.8",
            ha="left", va="center", fontsize=11, color=TERM_PROMPT,
            fontfamily="monospace", fontweight="bold")

    ping_lines = [
        "Обмін пакетами з 8.8.8.8:",
        "Відповідь від 8.8.8.8: байтів=32 час=15мс TTL=117",
        "Відповідь від 8.8.8.8: байтів=32 час=14мс TTL=117",
        "Відповідь від 8.8.8.8: байтів=32 час=15мс TTL=117",
        "Відповідь від 8.8.8.8: байтів=32 час=16мс TTL=117",
        "Статистика: відправлено=4, отримано=4, втрачено=0",
    ]
    yy = py + ph - 0.95
    for ln in ping_lines:
        ax.text(px + 0.2, yy, ln, ha="left", va="center",
                fontsize=9.5, color=TERM_TEXT, fontfamily="monospace")
        yy -= 0.42

    ax.text(3.35, 1.35, "Втрачено 0 — канал стабільний.\n"
                        "Втрачено 100% — вузол недоступний.",
            ha="center", va="center", fontsize=11, style="italic",
            color=TEXT_GRAY, linespacing=1.5)

    # ---------- Права панель: tracert ----------
    px2 = 6.65
    ax.add_patch(FancyBboxPatch((px2, py), pw, ph,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=TERM_BG, edgecolor="#3A3A3C",
                                linewidth=1.6))
    ax.add_patch(Rectangle((px2, py + ph - 0.55), pw, 0.55,
                           facecolor="#2C2C2E"))
    ax.text(px2 + 0.2, py + ph - 0.28, "tracert 8.8.8.8",
            ha="left", va="center", fontsize=11, color=TERM_PROMPT,
            fontfamily="monospace", fontweight="bold")

    tracert_lines = [
        "Трасування маршруту до 8.8.8.8:",
        "  1    <1 мс   192.168.1.1",
        "  2     3 мс   10.0.0.1",
        "  3    12 мс   203.0.113.5",
        "  4    15 мс   8.8.8.8",
        "Трасування завершено.",
    ]
    yy = py + ph - 0.95
    for ln in tracert_lines:
        ax.text(px2 + 0.2, yy, ln, ha="left", va="center",
                fontsize=9.5, color=TERM_TEXT, fontfamily="monospace")
        yy -= 0.42

    ax.text(9.65, 1.35, "Кожен рядок — окремий вузол.\n"
                        "«* * *» — вузол не відповідає.",
            ha="center", va="center", fontsize=11, style="italic",
            color=TEXT_GRAY, linespacing=1.5)

    return _save(fig, "scheme_diagnostics")


# ============================================================
# СХЕМА 3. Ланцюжок діагностики
# ============================================================

def scheme_network_chain():
    fig, ax = plt.subplots(figsize=(11, 6.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    ax.text(6.5, 6.6, "Ланцюжок діагностики мережі",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    nodes = [
        (1.6, "Комп'ютер", "ipconfig",
         "Чи є IP-адреса,\nмаска й шлюз?", ACCENT_BLUE, "#E1F0FE"),
        (4.9, "Маршрутизатор", "ping <шлюз>",
         "Чи відповідає\nвласний шлюз?", ACCENT_GREEN, "#E8F8EC"),
        (8.2, "Інтернет", "ping 8.8.8.8",
         "Чи виходить пакет\nза межі мережі?", ACCENT_ORANGE, "#FFF4E5"),
        (11.5, "Сервер", "ping / tracert",
         "Чи працює DNS\nі цільовий сайт?", ACCENT_RED, "#FFEBEA"),
    ]

    # З'єднувальні стрілки між вузлами (на рівні основного ряду)
    for i in range(len(nodes) - 1):
        x1 = nodes[i][0] + 1.2
        x2 = nodes[i + 1][0] - 1.2
        ax.annotate("", xy=(x2, 4.4), xytext=(x1, 4.4),
                    arrowprops=dict(arrowstyle="-|>", color=TEXT_GRAY,
                                    linewidth=1.8, mutation_scale=14))

    for x, title, cmd, desc, color, fill in nodes:
        # Основна картка
        w, h = 2.4, 1.15
        _card(ax, x - w / 2, 3.85, w, h, fill=fill, border=color, radius=0.18)
        ax.text(x, 4.42, title, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=TEXT_DARK)

        # Бейдж-команда над карткою
        _badge(ax, x, 5.6, 2.2, 0.55, color, cmd, color="white",
               size=10.5, radius=0.28)

        # Стрілка від бейджа до картки
        ax.annotate("", xy=(x, 5.05), xytext=(x, 5.3),
                    arrowprops=dict(arrowstyle="-|>", color=color,
                                    linewidth=1.4, mutation_scale=10))

        # Опис під карткою
        ax.text(x, 3.05, desc, ha="center", va="center",
                fontsize=11, color=TEXT_DARK, linespacing=1.6)

    ax.text(6.5, 1.55, "Порядок зліва направо — від найближчого вузла до "
                       "найдальшого.\nДіагностика зупиняється на тому "
                       "кроці, де з'являється помилка.",
            ha="center", va="center", fontsize=11, style="italic",
            color=TEXT_GRAY, linespacing=1.6)

    return _save(fig, "scheme_network_chain")


# ============================================================
# СХЕМА 4. Три рівні
# ============================================================

def scheme_levels():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    ax.text(6.5, 7.3, "Три рівні практичних завдань",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=TEXT_DARK)

    levels = [
        ("Рівень 1", "Базові команди",
         "ipconfig, ping —\nперевірка власної\nконфігурації",
         "≈ 7 хв", ACCENT_GREEN, "#E8F8EC"),
        ("Рівень 2", "Розширені\nпараметри",
         "tracert, ping -n -l,\nnslookup, netstat,\nnet view",
         "≈ 10 хв", ACCENT_ORANGE, "#FFF4E5"),
        ("Рівень 3", "Діагностика\nза сценарієм",
         "знайти, на якому\nкроці «ламається»\nмережа, скласти звіт",
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
               size=13, radius=0.3)
        ax.text(cx, y0 + card_h - 1.6, name, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=TEXT_DARK,
                linespacing=1.4)
        ax.text(cx, y0 + card_h - 3.15, desc, ha="center", va="center",
                fontsize=12, color=TEXT_DARK, linespacing=1.7)
        _badge(ax, cx, y0 + 0.7, 2.1, 0.55, fill, time_txt,
               color=color, size=12.5, radius=0.28)

    return _save(fig, "scheme_levels")


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


def code_line(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(1.0)
    _style_run(p.add_run(text), font_name="Consolas",
               color=RGBColor(0xC0, 0x39, 0x2B))
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
    img1 = scheme_commands()
    img2 = scheme_diagnostics()
    img3 = scheme_network_chain()
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

    h1(doc, "Практичне заняття")
    theme_line(doc, "Використання команд для роботи з мережею. "
                    "Навігація в мережевих ресурсах через командний рядок. "
                    "Перевірка стану мережі і взаємодія з іншими пристроями")

    h2(doc, "Мета")
    body(doc, "вивчати команди ping, ipconfig, net, tracert для "
              "діагностики мережі та доступу до мережевих ресурсів; "
              "розвивати системне мислення під час аналізу мережевих "
              "з'єднань і виявлення несправностей; виховувати культуру "
              "корпоративної роботи та дотримання мережевого етикету.")

    h2(doc, "Обладнання та програмне забезпечення")
    equipment = [
        "Персональний комп'ютер з ОС Windows 10/11, підключений до мережі.",
        "Командний рядок cmd або Windows Terminal.",
        "Інструкційні картки до рівнів 1–3.",
        "Текстовий редактор для оформлення звіту.",
        "Програма створення скріншотів (Print Screen, «Ножиці»).",
    ]
    for i, e in enumerate(equipment, 1):
        numbered_paren(doc, i, e)

    h2(doc, "Література")
    sources = [
        "Погребняк Б. І., Булаєнко М. В. Операційні системи : навч. посіб. "
        "Харків. нац. ун-т міськ. госп-ва ім. О. М. Бекетова. Харків : "
        "ХНУМГ ім. О. М. Бекетова, 2018.",
        "Сільвестр В., Гансен П. Основи операційних систем. Київ : "
        "Нова Книга, 2016.",
        "Таненбаум Е., Бос Г. Операційні системи: проектування та "
        "реалізація. Київ : Вильямс, 2015.",
    ]
    for s in sources:
        numbered(doc, s)

    # =====================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =====================================================
    h2(doc, "Теоретичні відомості")

    h3(doc, "1. Мережеві команди командного рядка")
    body(doc, "Командний рядок Windows має низку вбудованих команд для "
              "перевірки стану мережі, діагностики з'єднань і доступу до "
              "мережевих ресурсів. Вони працюють без графічного "
              "інтерфейсу, швидко виводять результат і дозволяють "
              "аналізувати мережу навіть на серверах без робочого столу.")

    add_figure(doc, img1, 16.0)

    add_table(
        doc,
        ["Команда", "Призначення", "Приклад"],
        [
            ["ping", "Перевірка доступності вузла",
             "ping 8.8.8.8"],
            ["ipconfig", "Показ власних налаштувань мережі",
             "ipconfig /all"],
            ["tracert", "Маршрут до вузла (усі проміжні хопи)",
             "tracert google.com"],
            ["net", "Робота з мережевими ресурсами",
             "net view \\\\Server"],
            ["nslookup", "Перевірка DNS-записів",
             "nslookup google.com"],
            ["netstat", "Активні з'єднання та відкриті порти",
             "netstat -an"],
        ],
        widths=[2.6, 7.4, 6.5],
        mono_cols=[0, 2],
    )

    h3(doc, "2. ipconfig — власна конфігурація")
    body(doc, "Команда ipconfig показує основні параметри мережевих "
              "адаптерів комп'ютера. Без параметрів вона виводить "
              "IP-адресу, маску підмережі та основний шлюз. З "
              "параметром /all — ще й MAC-адресу, DNS-сервери, ім'я "
              "хоста, час оренди адреси DHCP.")

    body(doc, "Ключові параметри:")
    bullet(doc, "/all — повна інформація про всі адаптери;")
    bullet(doc, "/release — відпустити поточну IP-адресу (DHCP);")
    bullet(doc, "/renew — отримати нову IP-адресу (DHCP);")
    bullet(doc, "/flushdns — очистити локальний DNS-кеш.")

    body(doc, "Приклади:")
    code_line(doc, "ipconfig")
    body(doc, "основні параметри всіх активних адаптерів.", space_after=2)
    code_line(doc, "ipconfig /all")
    body(doc, "детальна конфігурація кожного адаптера, зокрема DNS.",
         space_after=2)
    code_line(doc, "ipconfig /flushdns")
    body(doc, "очищення DNS-кешу, якщо сайти не відкриваються через "
              "застарілі записи.")

    callout(doc,
            "Якщо команда ipconfig показує адресу 169.254.x.x — це "
            "означає, що DHCP-сервер недоступний, і комп'ютер не отримав "
            "IP-адресу автоматично. У такому разі перевірте кабель або "
            "Wi-Fi, а потім виконайте ipconfig /renew.",
            fill="FFF4E5", accent="C93400")

    h3(doc, "3. ping — перевірка доступності")
    body(doc, "Команда ping надсилає ICMP-пакети до вузла та показує, "
              "скільки часу зайняла відповідь. Якщо відповідь є — "
              "вузол доступний. Якщо ні — можливі три причини: вузол "
              "вимкнений, мережа недоступна або ICMP заблокований "
              "брандмауером.")

    add_figure(doc, img2, 16.0)

    body(doc, "Ключові параметри:")
    bullet(doc, "-n <число> — кількість пакетів (за замовчуванням 4);")
    bullet(doc, "-l <розмір> — розмір пакета в байтах;")
    bullet(doc, "-t — надсилати пакети безперервно (зупинка — Ctrl + C);")
    bullet(doc, "-w <мс> — тайм-аут очікування відповіді.")

    body(doc, "Приклади:")
    code_line(doc, "ping 127.0.0.1")
    body(doc, "перевірка власного мережевого стека (має завжди "
              "відповідати).", space_after=2)
    code_line(doc, "ping 192.168.1.1")
    body(doc, "перевірка доступності власного шлюзу (маршрутизатора).",
         space_after=2)
    code_line(doc, "ping 8.8.8.8")
    body(doc, "перевірка виходу в Інтернет без DNS (Google DNS).",
         space_after=2)
    code_line(doc, "ping google.com")
    body(doc, "перевірка роботи DNS (ім'я має перетворитися на IP).")

    h3(doc, "4. tracert — маршрут до вузла")
    body(doc, "Команда tracert показує, через які проміжні "
              "маршрутизатори проходить пакет, доки не досягне цілі. "
              "Кожен рядок — окремий хоп. Якщо на певному хопі "
              "з'являється «* * *» — цей маршрутизатор не відповідає на "
              "службові пакети (не обов'язково помилка).")

    body(doc, "Приклади:")
    code_line(doc, "tracert 8.8.8.8")
    body(doc, "маршрут до сервера Google DNS за IP-адресою.", space_after=2)
    code_line(doc, "tracert -d google.com")
    body(doc, "те саме, але без зворотного розпізнавання імен "
              "(швидше).", space_after=2)
    code_line(doc, "tracert -h 5 8.8.8.8")
    body(doc, "обмежити кількість хопів до 5 (швидка перевірка перших "
              "вузлів).")

    h3(doc, "5. net, nslookup, netstat")
    body(doc, "Команда net — це набір підкоманд для роботи з "
              "мережевими ресурсами: перегляд доступних ресурсів "
              "локальної мережі, підключення до спільних папок, "
              "перегляд облікових записів.")
    bullet(doc, "net view — переглянути список комп'ютерів і ресурсів "
                "у локальній мережі;")
    bullet(doc, "net view \\\\Server — переглянути ресурси конкретного "
                "комп'ютера;")
    bullet(doc, "net use Z: \\\\Server\\Share — підключити спільну "
                "папку як диск Z:;")
    bullet(doc, "net user — перелік локальних облікових записів.")

    body(doc, "Команда nslookup перевіряє, чи правильно DNS "
              "перетворює доменне ім'я на IP-адресу. Команда netstat "
              "показує активні з'єднання та відкриті порти.")
    code_line(doc, "nslookup google.com")
    body(doc, "отримати IP-адресу домену google.com за версією DNS.",
         space_after=2)
    code_line(doc, "netstat -an")
    body(doc, "перелік усіх з'єднань і портів у числовому вигляді.")

    h3(doc, "6. Послідовність діагностики мережі")
    body(doc, "Під час реальної діагностики команди застосовують "
              "послідовно — від найближчого вузла до найдальшого. "
              "Це дозволяє швидко локалізувати проблему: якщо помилка "
              "виникає на першому кроці, решта вже не має сенсу.")

    add_figure(doc, img3, 16.0)

    body(doc, "Типова послідовність:")
    numbered(doc, "ipconfig — переконатися, що комп'ютер отримав "
                  "IP-адресу, маску та шлюз;")
    numbered(doc, "ping 127.0.0.1 — перевірити власний мережевий стек;")
    numbered(doc, "ping <шлюз> — перевірити зв'язок із маршрутизатором;")
    numbered(doc, "ping 8.8.8.8 — перевірити вихід в Інтернет без DNS;")
    numbered(doc, "ping <сайт> — перевірити роботу DNS;")
    numbered(doc, "tracert <сайт> — знайти, на якому хопі виникає "
                  "затримка або обрив.")

    h3(doc, "7. Мережевий етикет і безпека")
    body(doc, "Команди ping, tracert, netstat цілком безпечні, але "
              "їх потрібно застосовувати етично. Деякі правила:")
    bullet(doc, "не запускайте ping -t до чужого сервера «заради "
                "цікавості» — це створює зайве навантаження;")
    bullet(doc, "не використовуйте net view або net use для доступу "
                "до чужих ресурсів без дозволу адміністратора;")
    bullet(doc, "не публікуйте у звітах реальні IP-адреси та MAC-адреси "
                "без згоди власника мережі;")
    bullet(doc, "результати діагностики повідомляйте адміністратору "
                "у стислому вигляді: команда — результат — висновок.")

    callout(doc,
            "У навчальній мережі закладу діагностику потрібно "
            "проводити лише під керівництвом викладача. Не "
            "використовуйте команди проти серверів, які вам не "
            "належать. Сканування чужих портів без дозволу є "
            "порушенням правил мережевого етикету.",
            fill="FFEBEA", accent="C4001D")

    # =====================================================
    # РІВНІ ЗАВДАНЬ
    # =====================================================
    h2(doc, "Покроковий алгоритм виконання різнорівневих завдань")

    body(doc, "Практична частина заняття побудована за трирівневою "
              "системою. Студент виконує завдання послідовно; орієнтовний "
              "час на кожен рівень — 7–10 хвилин, загальна тривалість — "
              "25–30 хвилин. Оцінка залежить від кількості успішно "
              "виконаних рівнів.")

    add_figure(doc, img4, 16.0)

    # -------- Рівень 1 --------
    h3(doc, "Рівень 1 — базові команди (≈ 7 хв)",
       color=RGBColor(0x24, 0x8A, 0x3D))
    body(doc, "Мета: навчитися перевіряти власну конфігурацію командою "
              "ipconfig і доступність вузлів командою ping.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Відкрийте командний рядок", "Win + R → cmd → Enter"],
            ["2", "Перегляньте власну IP-конфігурацію", "ipconfig"],
            ["3", "Перегляньте детальну конфігурацію", "ipconfig /all"],
            ["4", "Запишіть у звіт: IP-адресу, маску, шлюз, DNS",
             "Скопіюйте з виводу вручну"],
            ["5", "Перевірте власний стек", "ping 127.0.0.1"],
            ["6", "Перевірте шлюз", "ping <адреса шлюзу з кроку 4>"],
            ["7", "Перевірте вихід в Інтернет", "ping 8.8.8.8"],
            ["8", "Перевірте DNS", "ping google.com"],
            ["9", "Порівняйте час відповіді", "Зверніть увагу на рядок "
             "«час=...мс»"],
            ["10", "Зробіть скріншот",
             "Print Screen; вставте у звіт із підписом"],
        ],
        widths=[1.0, 5.8, 9.7],
        mono_cols=[2],
    )

    callout(doc,
            "Після виконання рівня 1 у звіті має бути: IP-адреса, маска, "
            "шлюз і DNS вашого комп'ютера, а також результати трьох "
            "перевірок (127.0.0.1, шлюз, 8.8.8.8). Якщо ping 8.8.8.8 "
            "не відповідає — зафіксуйте це у звіті й перейдіть до "
            "рівня 2.",
            fill="E8F8EC", accent="248A3D")

    # -------- Рівень 2 --------
    h3(doc, "Рівень 2 — розширені параметри (≈ 10 хв)",
       color=RGBColor(0xC9, 0x34, 0x00))
    body(doc, "Мета: навчитися застосовувати параметри ping, "
              "використовувати tracert, nslookup і netstat для "
              "детальнішої діагностики.")

    add_table(
        doc,
        ["№", "Дія", "Команда / очікуваний результат"],
        [
            ["1", "Перевірте стабільність з'єднання",
             "ping -n 10 8.8.8.8"],
            ["2", "Перевірте передачу великого пакета",
             "ping -l 1000 8.8.8.8"],
            ["3", "Запустіть безперервний ping і зупиніть через 10–15 с",
             "ping -t 8.8.8.8   →  Ctrl + C"],
            ["4", "Запишіть статистику (відправлено / отримано / втрачено)",
             "З виводу кроку 3"],
            ["5", "Дізнайтеся маршрут до вузла",
             "tracert 8.8.8.8"],
            ["6", "Обмежте кількість хопів до 5", "tracert -h 5 8.8.8.8"],
            ["7", "Перевірте DNS для домену", "nslookup google.com"],
            ["8", "Порівняйте IP з nslookup і з ping",
             "ping google.com  →  перший рядок виводу"],
            ["9", "Перегляньте активні з'єднання", "netstat -an"],
            ["10", "Порахуйте кількість з'єднань у стані LISTENING",
             "netstat -an | find \"LISTENING\""],
            ["11", "Перегляньте ресурси локальної мережі", "net view"],
            ["12", "Зробіть скріншот",
             "Знімок вікна з результатом кроків 4 і 5"],
        ],
        widths=[1.0, 6.0, 9.5],
        mono_cols=[2],
    )

    callout(doc,
            "У звіті має бути: статистика ping -n 10 (відправлено / "
            "отримано / втрачено), кількість хопів із tracert, "
            "результат nslookup, кількість з'єднань LISTENING. "
            "Коротко поясніть, що показує кожен параметр.",
            fill="FFF4E5", accent="C93400")

    # -------- Рівень 3 --------
    h3(doc, "Рівень 3 — діагностика за сценарієм (≈ 10 хв)",
       color=RGBColor(0xC4, 0x00, 0x1D))
    body(doc, "Мета: навчитися знаходити місце несправності у мережі, "
              "послідовно застосовуючи команди від найближчого вузла до "
              "найдальшого, та оформлювати результат у вигляді звіту.")

    body(doc, "Завдання А. Сценарій «Інтернет не працює». Уявіть, що "
              "колега звернувся зі скаргою: «Сторінки не "
              "відкриваються». Виконайте діагностику за схемою 3 і "
              "заповніть таблицю.")

    add_table(
        doc,
        ["Крок", "Команда", "Що перевіряємо", "Результат (заповніть)"],
        [
            ["1", "ipconfig", "Чи є IP-адреса, шлюз, DNS", ""],
            ["2", "ping 127.0.0.1", "Чи працює стек", ""],
            ["3", "ping <шлюз>", "Чи доступний маршрутизатор", ""],
            ["4", "ping 8.8.8.8", "Чи є вихід в Інтернет", ""],
            ["5", "ping google.com", "Чи працює DNS", ""],
            ["6", "tracert 8.8.8.8", "Де саме виникає затримка", ""],
        ],
        widths=[1.4, 4.2, 5.8, 5.1],
        mono_cols=[1],
    )

    body(doc, "Завдання Б. Визначте, на якому кроці «ламається» мережа "
              "у вашому випадку (якщо ламається), і сформулюйте "
              "висновок у такому форматі:")

    code_line(doc, "«На кроці N команда <назва> показала <результат>.")
    code_line(doc, "Це означає, що <причина>.")
    code_line(doc, "Рекомендація: <що робити далі>».")

    body(doc, "Завдання В. Творче ускладнення (за бажанням, +1 бал). "
              "Придумайте власний сценарій несправності (наприклад, "
              "«сайти відкриваються, але дуже повільно» або «один "
              "сайт не відкривається, інші працюють») та опишіть "
              "послідовність із 4–5 команд, які допоможуть локалізувати "
              "проблему.")

    callout(doc,
            "Завдання Б оцінюється не за «правильну» відповідь, а за "
            "логічність висновку. Якщо мережа працює справно, "
            "зафіксуйте це й поясніть, як ви переконалися у "
            "справності кожного кроку.",
            fill="FFEBEA", accent="C4001D")

    # =====================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =====================================================
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Рівень / критерій", "Показник", "Бали"],
        [
            ["Рівень 1",
             "Усі 10 кроків виконано правильно; у звіті є IP, маска, "
             "шлюз, DNS, три перевірки ping; є скріншот", "3"],
            ["Рівень 2",
             "Виконано ping із параметрами -n, -l, -t; tracert; "
             "nslookup; netstat; net view; є скріншот і короткі "
             "пояснення", "4"],
            ["Рівень 3",
             "Заповнено таблицю діагностики (6 кроків); висновок "
             "сформульовано у заданому форматі; логіка послідовності "
             "дотримана", "4"],
            ["Якість звіту",
             "Оформлення за вимогами; підписи до скріншотів; наведено "
             "повну послідовність команд", "1"],
            ["Творчий підхід",
             "Виконано ускладнення (власний сценарій несправності)", "1"],
        ],
        widths=[3.6, 11.0, 2.0],
    )

    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (потребує доопрацювання).")

    # =====================================================
    # ФОРМА ЗВІТНОСТІ
    # =====================================================
    h2(doc, "Форма звітності")
    body(doc, "Результати практичного заняття оформлюються у вигляді "
              "електронного звіту в текстовому редакторі. Звіт повинен "
              "містити такі обов'язкові частини:")
    report_parts = [
        "Титульна сторінка: навчальний заклад, тема, ПІБ студента, "
        "група, ПІБ викладача, дата.",
        "Скріншот ipconfig /all із виділеними полями: IP-адреса, "
        "маска, шлюз, DNS.",
        "Скріншот результатів ping (127.0.0.1, шлюз, 8.8.8.8, "
        "google.com) після рівня 1.",
        "Скріншот tracert і статистики ping -n 10 після рівня 2.",
        "Заповнена таблиця діагностики (6 кроків) після рівня 3.",
        "Висновок у заданому форматі («На кроці N... Це означає... "
        "Рекомендація...»).",
        "Короткий підсумок: що нового засвоїли, які команди виявилися "
        "найзручнішими, які питання залишилися.",
    ]
    for r in report_parts:
        numbered(doc, r)

    body(doc, "Технічні вимоги до звіту: файл формату .docx або .pdf, "
              "шрифт Times New Roman 14 pt, інтервал 1,15, поля 2 см, "
              "обсяг — 3–5 сторінок без титульної. Ім'я файлу: "
              "«Практика_Мережеві_команди_ПІБ.docx». Звіт надсилається "
              "викладачу до наступного заняття через електронний курс.")

    doc.save("Практичне_заняття_Мережеві_команди.docx")
    print("Готово: Практичне_заняття_Мережеві_команди.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()