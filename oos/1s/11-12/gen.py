# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: САМОСТІЙНА РОБОТА
Тема: Операції з файлами. Копіювання та переміщення файлів.
      Видалення файлів і папок. Навігація файловою структурою.
      Управління атрибутами файлів.
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


def _folder(ax, x, y, w=1.8, h=1.2, fc="#DEEAF6", ec="#2E75B6", label=""):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=fc, edgecolor=ec, linewidth=1.6))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=10, fontweight="bold", color="#1F4E79")


def _file(ax, x, y, w=1.4, h=0.9, fc="#FFF2CC", ec="#BF8F00", label="файл"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=fc, edgecolor=ec, linewidth=1.4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=9, fontweight="bold", color="#7F6000")


def scheme_copy_vs_move():
    """Схема 1: копіювання vs переміщення."""
    fig, ax = plt.subplots(figsize=(12, 6.2))
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")

    # ---------- Лівий блок: копіювання ----------
    ax.add_patch(Rectangle((0.3, 0.4), 7.4, 7.6,
                           facecolor="#F7F9FC", edgecolor="#BFBFBF", linewidth=1.5))
    ax.text(4.0, 7.5, "КОПІЮВАННЯ  (Ctrl+C → Ctrl+V)",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")

    _folder(ax, 0.8, 5.0, label="Папка А")
    _folder(ax, 0.8, 2.0, label="Папка Б")
    _file(ax, 1.0, 5.3, label="звіт.docx")
    _file(ax, 1.0, 2.3, label="звіт.docx")
    ax.annotate("", xy=(1.7, 2.05), xytext=(1.7, 5.25),
                arrowprops=dict(arrowstyle="-|>", color="#548235",
                                linewidth=2.4, mutation_scale=20))
    ax.text(2.6, 4.4, "копія", fontsize=10, fontweight="bold",
            color="#548235", style="italic")

    ax.text(4.0, 1.2, "Результат: файл існує у ДВОХ папках;\n"
                      "вміст папки А не змінюється",
            ha="center", va="center", fontsize=10, color="#375623", linespacing=1.4)
    ax.add_patch(Rectangle((4.5, 4.6), 2.8, 0.9,
                           facecolor="#E2EFDA", edgecolor="#548235", linewidth=1.4))
    ax.text(5.9, 5.05, "оригінал залишається",
            ha="center", va="center", fontsize=9, fontweight="bold", color="#375623")

    # ---------- Правий блок: переміщення ----------
    ax.add_patch(Rectangle((8.3, 0.4), 7.4, 7.6,
                           facecolor="#F7F9FC", edgecolor="#BFBFBF", linewidth=1.5))
    ax.text(12.0, 7.5, "ПЕРЕМІЩЕННЯ  (Ctrl+X → Ctrl+V)",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#C55A11")

    _folder(ax, 8.8, 5.0, label="Папка А")
    _folder(ax, 8.8, 2.0, label="Папка Б")
    _file(ax, 9.0, 2.3, label="звіт.docx")
    ax.annotate("", xy=(9.7, 2.05), xytext=(9.7, 5.25),
                arrowprops=dict(arrowstyle="-|>", color="#C55A11",
                                linewidth=2.4, mutation_scale=20))
    ax.text(10.6, 4.4, "файл", fontsize=10, fontweight="bold",
            color="#C55A11", style="italic")

    ax.text(12.0, 1.2, "Результат: файл існує лише у папці Б;\n"
                       "у папці А його вже НЕМАЄ",
            ha="center", va="center", fontsize=10, color="#843C0C", linespacing=1.4)
    ax.add_patch(Rectangle((12.5, 4.6), 2.9, 0.9,
                           facecolor="#FBE5D6", edgecolor="#C55A11", linewidth=1.4))
    ax.text(13.95, 5.05, "оригінал зникає з А",
            ha="center", va="center", fontsize=9, fontweight="bold", color="#843C0C")

    ax.text(8.0, 8.6,
            "Схема 1. Копіювання та переміщення: у чому різниця",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")
    return _save(fig, "scheme_copy_vs_move")


def scheme_delete_flow():
    """Схема 2: шляхи видалення файлів."""
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 16); ax.set_ylim(0, 8); ax.axis("off")

    ax.text(8.0, 7.4, "Схема 2. Видалення файлів: Кошик чи остаточне",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")

    # Стартовий файл
    ax.add_patch(FancyBboxPatch((0.8, 3.6), 2.2, 1.4,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#FFF2CC", edgecolor="#BF8F00", linewidth=1.6))
    ax.text(1.9, 4.3, "файл", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#7F6000")

    # Розгалуження
    # Верхній шлях — звичайне видалення
    ax.annotate("", xy=(4.4, 5.3), xytext=(3.05, 4.55),
                arrowprops=dict(arrowstyle="-|>", color="#2E75B6",
                                linewidth=2.0, mutation_scale=18))
    ax.text(3.5, 5.15, "Delete", fontsize=9, fontweight="bold",
            color="#2E75B6", style="italic")

    ax.add_patch(FancyBboxPatch((4.4, 4.6), 3.2, 1.4,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#DEEAF6", edgecolor="#2E75B6", linewidth=1.6))
    ax.text(6.0, 5.3, "Кошик", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#1F4E79")
    ax.text(6.0, 4.85, "(тимчасове зберігання)",
            ha="center", va="center", fontsize=9, style="italic", color="#595959")

    ax.annotate("", xy=(10.0, 5.3), xytext=(7.65, 5.3),
                arrowprops=dict(arrowstyle="-|>", color="#2E75B6",
                                linewidth=2.0, mutation_scale=18))
    ax.text(8.8, 5.55, "відновити", fontsize=9, fontweight="bold",
            color="#2E75B6", style="italic")

    ax.add_patch(FancyBboxPatch((10.0, 4.6), 3.6, 1.4,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#E2EFDA", edgecolor="#548235", linewidth=1.6))
    ax.text(11.8, 5.3, "Файл відновлено", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#375623")
    ax.text(11.8, 4.85, "можна продовжити роботу",
            ha="center", va="center", fontsize=9, style="italic", color="#595959")

    # Нижній шлях — остаточне видалення
    ax.annotate("", xy=(4.4, 2.3), xytext=(3.05, 3.85),
                arrowprops=dict(arrowstyle="-|>", color="#C55A11",
                                linewidth=2.0, mutation_scale=18))
    ax.text(3.2, 3.0, "Shift+Delete\nабо\nочистити Кошик",
            fontsize=9, fontweight="bold", color="#C55A11",
            ha="left", va="center", linespacing=1.2)

    ax.add_patch(FancyBboxPatch((4.4, 1.6), 3.2, 1.4,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#FBE5D6", edgecolor="#C55A11", linewidth=1.6))
    ax.text(6.0, 2.3, "Остаточне видалення",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#843C0C")

    ax.annotate("", xy=(10.0, 2.3), xytext=(7.65, 2.3),
                arrowprops=dict(arrowstyle="-|>", color="#C55A11",
                                linewidth=2.0, mutation_scale=18))
    ax.text(8.8, 2.55, "безповоротно", fontsize=9, fontweight="bold",
            color="#C55A11", style="italic")

    ax.add_patch(FancyBboxPatch((10.0, 1.6), 3.6, 1.4,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#FFC7CE", edgecolor="#C00000", linewidth=1.6))
    ax.text(11.8, 2.3, "Дані втрачено", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#9C0006")
    ax.text(11.8, 1.85, "відновлення ускладнене",
            ha="center", va="center", fontsize=9, style="italic", color="#595959")

    ax.text(8.0, 0.4,
            "Правило безпеки: перед видаленням переконайтеся, що обрано САМЕ той об'єкт",
            ha="center", va="center", fontsize=10, style="italic", color="#595959")
    return _save(fig, "scheme_delete_flow")


def scheme_navigation():
    """Схема 3: способи навігації файловою структурою."""
    fig, ax = plt.subplots(figsize=(12, 6.0))
    ax.set_xlim(0, 16); ax.set_ylim(0, 8); ax.axis("off")

    ax.text(8.0, 7.4, "Схема 3. Способи навігації файловою структурою",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")

    cards = [
        ("Дерево папок\nу Проводнику",
         "Клік по імені папки\nу лівій панелі\n→ відкривається вміст",
         "#2E75B6", "#DEEAF6"),
        ("Адресний рядок",
         "Ввести шлях вручну:\nC:\\Навчання\\Конспекти\nта натиснути Enter",
         "#548235", "#E2EFDA"),
        ("Гарячі клавіші\nта кнопки",
         "Alt+←  назад\nAlt+→  уперед\nAlt+↑  на рівень вище",
         "#C55A11", "#FBE5D6"),
    ]

    card_w, card_h = 4.6, 4.6
    gap = 0.6
    x0 = (16 - (3 * card_w + 2 * gap)) / 2
    y0 = 1.4

    for i, (title, txt, accent, fill) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        ax.add_patch(FancyBboxPatch((x, y0), card_w, card_h,
                                    boxstyle="round,pad=0.02,rounding_size=0.2",
                                    facecolor=fill, edgecolor=accent, linewidth=2.0))
        ax.add_patch(FancyBboxPatch((x, y0 + card_h - 1.3), card_w, 1.3,
                                    boxstyle="round,pad=0.02,rounding_size=0.2",
                                    facecolor=accent, edgecolor=accent,
                                    linewidth=2.0))
        ax.text(x + card_w / 2, y0 + card_h - 0.65, title,
                ha="center", va="center", fontsize=11, fontweight="bold",
                color="white", linespacing=1.4)
        ax.text(x + card_w / 2, y0 + card_h / 2 - 0.4, txt,
                ha="center", va="center", fontsize=10, color="#1a1a1a",
                linespacing=1.6)

    ax.text(8.0, 0.5,
            "Різні способи навігації доповнюють один одного: щоразу обирайте найшвидший",
            ha="center", va="center", fontsize=10, style="italic", color="#595959")
    return _save(fig, "scheme_navigation")


def scheme_attributes():
    """Схема 4: основні атрибути файлу."""
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis("off")

    ax.add_patch(FancyBboxPatch((0.8, 0.7), 11.4, 6.4,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor="#FFFFFF", edgecolor="#404040",
                                linewidth=1.8))
    ax.add_patch(Rectangle((0.8, 6.4), 11.4, 0.7,
                           facecolor="#1F4E79", edgecolor="#1F4E79"))
    ax.text(1.2, 6.75, "Властивості: план_уроку.docx",
            ha="left", va="center", fontsize=11, fontweight="bold", color="white")

    rows = [
        ("☑ Тільки читання",
         "Забороняє редагування та видалення;\n"
         "захищає важливі файли від випадкової зміни",
         "#548235", "#E2EFDA"),
        ("☐ Прихований",
         "Ховає файл зі звичайного перегляду;\n"
         "використовується для системних файлів",
         "#BF8F00", "#FFF2CC"),
        ("☐ Архівний",
         "Позначає файл як такий, що потребує\n"
         "резервного копіювання; вмикається автоматично",
         "#2E75B6", "#DEEAF6"),
    ]

    for i, (label, txt, accent, fill) in enumerate(rows):
        y = 5.3 - i * 1.7
        ax.add_patch(FancyBboxPatch((1.1, y - 0.35), 10.8, 1.4,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=fill, edgecolor=accent, linewidth=1.5))
        ax.text(1.4, y + 0.55, label, ha="left", va="center",
                fontsize=11, fontweight="bold", color=accent)
        ax.text(1.4, y - 0.05, txt, ha="left", va="center",
                fontsize=10, color="#1a1a1a", linespacing=1.5)

    ax.text(6.5, 0.35,
            "Схема 4. Основні атрибути файлу в ОС Windows",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#1F4E79")
    return _save(fig, "scheme_attributes")


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
    img1 = scheme_copy_vs_move()
    img2 = scheme_delete_flow()
    img3 = scheme_navigation()
    img4 = scheme_attributes()

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
    h1(doc, "Самостійна робота")
    h1(doc, "Операції з файлами. Копіювання та переміщення файлів. "
           "Видалення файлів і папок. Навігація файловою структурою. "
           "Управління атрибутами файлів")

    body(doc, "«Основи операційних систем» · спеціальність 013 Початкова освіта "
              "(Вчитель інформатики початкової школи)", space_after=10)

    # ---------- Мета ----------
    h2(doc, "Мета")
    body(doc, "опрацювати способи виконання основних операцій з файлами та "
              "папками, включаючи зміну атрибутів; розвивати операційне "
              "мислення через планування послідовності дій під час роботи з "
              "об'єктами файлової системи; виховувати відповідальність за "
              "збереження чужих та власних даних під час виконання операцій "
              "видалення чи переміщення.")

    # ---------- Обладнання ----------
    h2(doc, "Обладнання")
    body(doc, "інструкційні картки; персональний комп'ютер з ОС Windows 10/11 "
              "або Linux (графічне середовище); файловий менеджер "
              "(Проводник / Nautilus); текстовий редактор для оформлення звіту; "
              "програма створення скріншотів.")

    # ---------- Завдання ----------
    h2(doc, "Завдання самостійної роботи")
    tasks = [
        "Опрацювати теоретичний матеріал за переліком опрацьовуваних питань.",
        "Скласти порівняльну таблицю операцій копіювання, переміщення та "
        "видалення (не менше трьох параметрів порівняння: вплив на оригінал, "
        "можливість скасування, гарячі клавіші).",
        "Виконати практичне завдання за інструкційною карткою (див. нижче): "
        "створити структуру папок, виконати операції копіювання, переміщення, "
        "видалення та зміни атрибутів.",
        "Скласти пам'ятку «Безпечне видалення файлів» (7–10 пунктів) для "
        "молодших школярів і для вчителя.",
        "Дати письмові відповіді на теоретичні питання (див. нижче).",
        "Оформити звіт згідно з рекомендаціями та надіслати викладачу у "
        "визначений термін.",
    ]
    for t in tasks:
        numbered(doc, t)

    # ---------- Терміни ----------
    h2(doc, "Терміни виконання")
    body(doc, "Робота виконується протягом одного тижня після отримання "
              "завдання; готовий звіт подається на наступному практичному "
              "занятті або завантажується в електронний курс дисципліни до "
              "вказаної дати.")

    # ---------- Очікувані результати ----------
    h2(doc, "Очікувані результати")
    results = [
        "знає відмінності між копіюванням, переміщенням та видаленням "
        "об'єктів файлової системи;",
        "розуміє механізм роботи «Кошика» та наслідки остаточного видалення;",
        "володіє способами навігації файловою структурою (дерево, адресний "
        "рядок, гарячі клавіші);",
        "вміє змінювати атрибути файлу («тільки читання», «прихований», "
        "«архівний») та пояснювати їхнє практичне значення;",
        "планує послідовність дій перед виконанням операцій, що можуть "
        "призвести до втрати даних;",
        "добирає доступні молодшим школярам пояснення та формулює правила "
        "безпечної роботи з файлами.",
    ]
    for r in results:
        bullet(doc, r)

    # ---------- Джерела ----------
    h2(doc, "Рекомендовані джерела")
    sources = [
        "Сільвестр В., Гансен П. Основи операційних систем. — Київ : Нова Книга, 2016.",
        "Таненбаум Е., Бос Г. Операційні системи: проектування та реалізація. — "
        "Київ : Вильямс, 2015.",
        "Томпсон Д., Черніченко В. Операційні системи. — Київ : Кондор, 2017.",
    ]
    for s in sources:
        bullet(doc, s)

    # ---------- Опрацьовувані питання ----------
    h2(doc, "Перелік опрацьовуваних питань")
    topics = [
        "Поняття операції над файлами та папками.",
        "Копіювання об'єктів: способи запуску, вплив на оригінал.",
        "Переміщення об'єктів: відмінність від копіювання, особливості "
        "переміщення між різними дисками.",
        "Видалення файлів і папок: «Кошик», остаточне видалення, наслідки.",
        "Відновлення об'єктів із «Кошика».",
        "Навігація файловою структурою: дерево папок, адресний рядок, "
        "гарячі клавіші.",
        "Атрибути файлу («тільки читання», «прихований», «архівний»): "
        "призначення та способи зміни.",
        "Правила безпечної роботи з файловою системою задля уникнення "
        "втрати даних.",
    ]
    for tp in topics:
        numbered(doc, tp)

    # =========================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =========================================================
    h2(doc, "Теоретичні відомості (стислий огляд)")

    h3(doc, "1. Копіювання та переміщення файлів")
    body(doc, "Копіювання — це створення точної копії об'єкта в іншому місці. "
              "Оригінал залишається на попередньому місці, тож після операції "
              "файл існує у двох примірниках. Копіювання використовують для "
              "резервного збереження даних і для поширення файлів між папками "
              "чи носіями.")

    body(doc, "Переміщення — це перенесення об'єкта з одного місця в інше. "
              "Після операції файл існує лише у кінцевій папці, а в "
              "початковій його вже немає. Переміщення зручне для наведення "
              "порядку у файловій структурі. Під час переміщення між різними "
              "дисками операційна система фактично виконує копіювання, а потім "
              "видаляє оригінал — для користувача результат той самий, але "
              "операція триває довше.")

    add_figure(doc, img1, 16.0)

    add_table(
        doc,
        ["Параметр", "Копіювання", "Переміщення", "Видалення"],
        [
            ["Вплив на оригінал", "залишається", "зникає", "зникає"],
            ["Гарячі клавіші", "Ctrl+C → Ctrl+V", "Ctrl+X → Ctrl+V",
             "Delete / Shift+Delete"],
            ["Можливість скасування", "так (Ctrl+Z)",
             "так (Ctrl+Z)", "так (Ctrl+Z, до очищення Кошика)"],
            ["Основне призначення", "резервна копія, поширення",
             "наведення порядку", "звільнення місця"],
        ],
        widths=[4.0, 4.2, 4.1, 4.2],
    )

    h3(doc, "2. Видалення файлів і папок")
    body(doc, "У сучасних операційних системах видалення зазвичай відбувається "
              "у два кроки: об'єкт спершу потрапляє до «Кошика» — тимчасового "
              "сховища, з якого його можна відновити, — і лише після очищення "
              "Кошика видаляється остаточно. Остаточне видалення виконується "
              "комбінацією Shift+Delete або через контекстне меню «Видалити "
              "безповоротно».")

    add_figure(doc, img2, 15.5)

    callout(doc, "Правило безпеки.",
            "Перед видаленням перевірте, що вибрано САМЕ той об'єкт, який "
            "потрібно видалити. Після остаточного видалення відновлення "
            "можливе лише спеціальними програмами й не завжди успішне. "
            "Для папок, що містять багато файлів, спершу перегляньте їхній "
            "вміст, а не видаляйте навмання.",
            fill="FFC7CE", accent="C00000")

    h3(doc, "3. Навігація файловою структурою")
    body(doc, "Навігація — це переміщення між папками для пошуку потрібних "
              "об'єктів. Основні способи навігації у графічному середовищі "
              "подано на схемі 3.")

    add_figure(doc, img3, 15.5)

    body(doc, "Додаткові корисні прийоми під час роботи з файловою системою:")
    bullet(doc, "пошук файлу за назвою чи розширенням у полі пошуку "
                "Проводника;")
    bullet(doc, "сортування вмісту папки за датою, розміром, типом;")
    bullet(doc, "перегляд прихованих файлів через меню «Вигляд» "
                "(обережно: не змінюйте системні файли);")
    bullet(doc, "закріплення часто використовуваних папок у «Швидкому доступі».")

    h3(doc, "4. Управління атрибутами файлів")
    body(doc, "Атрибути — це характеристики файлу, які визначають, як система "
              "і користувач можуть поводитися з ним. Зміна атрибутів "
              "виконується через контекстне меню «Властивості» (права кнопка "
              "миші на файлі). Найуживаніші атрибути подано на схемі 4.")

    add_figure(doc, img4, 15.0)

    body(doc, "Приклади практичного застосування атрибутів учителем:")
    bullet(doc, "позначити «тільки читання» файли з підсумковими оцінками, "
                "щоб уникнути випадкової зміни;")
    bullet(doc, "приховати папку з персональними даними учнів;")
    bullet(doc, "перевірити атрибут «архівний» перед резервним копіюванням, "
                "щоб не копіювати зайвий раз незмінені файли.")

    callout(doc, "Методична підказка.",
            "У роботі з молодшими школярами варто ілюструвати операції з "
            "файлами предметними діями: копіювання — як «зробити ксерокопію "
            "малюнка», переміщення — як «перекласти зошит зі столу до "
            "портфеля», видалення — як «викинути чернетку в кошик для "
            "сміття». Такі аналогії допомагають дітям зрозуміти різницю між "
            "операціями.",
            fill="FFF4E5", accent="C55A11")

    # =========================================================
    # ПРАКТИЧНЕ ЗАВДАННЯ (ІНСТРУКЦІЙНА КАРТКА)
    # =========================================================
    h2(doc, "Практичне завдання за інструкційною карткою")
    body(doc, "Створіть на робочому диску папку «СР_Операції_ПІБ» і виконайте "
              "у ній таку послідовність дій:")

    add_table(
        doc,
        ["№", "Дія", "Очікуваний результат"],
        [
            ["1", "Створіть папки «Джерело» та «Приймач»",
             "У папці «СР_Операції_ПІБ» з'явилися дві підпапки"],
            ["2", "У папці «Джерело» створіть текстовий файл «зразок.txt» "
                  "із довільним текстом",
             "Файл створено, у ньому є текст"],
            ["3", "Скопіюйте файл «зразок.txt» у папку «Приймач» (Ctrl+C → Ctrl+V)",
             "Файл існує у ДВОХ папках"],
            ["4", "Перейменуйте копію в «копія.txt»",
             "У папці «Приймач» файл має нове ім'я"],
            ["5", "Перемістіть файл «зразок.txt» із «Джерело» до «Приймач» "
                  "(Ctrl+X → Ctrl+V)",
             "У папці «Джерело» файлу немає; у «Приймач» — два файли"],
            ["6", "Видаліть файл «копія.txt» клавішею Delete",
             "Файл зник з папки та потрапив до Кошика"],
            ["7", "Відновіть «копія.txt» з Кошика",
             "Файл повернувся у «Приймач»"],
            ["8", "Встановіть для «зразок.txt» атрибут «Тільки читання»",
             "У властивостях файлу встановлено прапорець; спроба редагування "
             "викликає попередження"],
            ["9", "Зніміть атрибут «Тільки читання» і встановіть «Прихований»",
             "Файл зникає зі звичайного перегляду; перегляд прихованих "
             "файлів через «Вигляд» показує його"],
            ["10", "Поверніть звичайні атрибути файлу та зробіть скріншот "
                   "кінцевої структури",
             "Готовий скріншот для звіту"],
        ],
        widths=[1.0, 7.5, 8.0],
    )

    callout(doc, "Самоперевірка.",
            "Після виконання всіх кроків у папці «СР_Операції_ПІБ» має бути "
            "дві папки: «Джерело» (порожня) та «Приймач» (містить два файли: "
            "«зразок.txt» і «копія.txt» зі звичайними атрибутами).",
            fill="E2EFDA", accent="548235")

    # =========================================================
    # ТЕОРЕТИЧНІ ПИТАННЯ
    # =========================================================
    h2(doc, "Теоретичні питання для самоперевірки")
    questions = [
        "Чим копіювання файлу відрізняється від переміщення? Наведіть "
        "приклад ситуації, коли доцільно використати кожну з операцій.",
        "Чому під час переміщення між різними дисками операція триває "
        "довше, ніж у межах одного диска?",
        "Що таке «Кошик»? Які переваги й обмеження він має?",
        "У яких випадках файл видаляється остаточно, минаючи Кошик?",
        "Опишіть алгоритм відновлення файлу з «Кошика».",
        "Назвіть не менше трьох способів навігації файловою структурою та "
        "поясніть, коли кожен із них зручніший.",
        "Які атрибути файлу ви знаєте? Для чого кожен із них "
        "використовується?",
        "Як атрибут «тільки читання» допомагає вчителю під час роботи з "
        "важливими документами?",
        "Сформулюйте три правила безпечного видалення файлів для "
        "молодшого школяра.",
        "Запропонуйте структуру папок для зберігання матеріалів учителя "
        "початкової школи, у якій операції переміщення були б мінімальними.",
    ]
    for q in questions:
        numbered(doc, q)

    # =========================================================
    # РЕКОМЕНДАЦІЇ ДО ОФОРМЛЕННЯ
    # =========================================================
    h2(doc, "Рекомендації до оформлення звіту")
    body(doc, "Звіт оформлюється у текстовому редакторі (MS Word / LibreOffice "
              "Writer) і повинен містити такі обов'язкові структурні елементи:")
    structure = [
        "Титульна сторінка: назва навчального закладу, тема, ПІБ студента, "
        "група, ПІБ викладача, рік.",
        "Мета та завдання роботи.",
        "Порівняльна таблиця операцій копіювання, переміщення та видалення "
        "(не менше трьох параметрів).",
        "Пам'ятка «Безпечне видалення файлів» — окремо для молодшого "
        "школяра та для вчителя.",
        "Практична частина: скріншоти виконання інструкційної картки "
        "(не менше 3 зображень) з короткими коментарями.",
        "Відповіді на теоретичні питання (письмово, стисло).",
        "Висновок: 4–6 речень про те, що нового дізналися, як "
        "використовуватимете ці знання у роботі з молодшими школярами.",
        "Список використаних джерел (оформлений за ДСТУ 8302:2015).",
    ]
    for s in structure:
        numbered(doc, s)

    body(doc, "Технічні параметри оформлення: шрифт Times New Roman, 14 pt, "
              "міжрядковий інтервал 1,15, поля 2 см, абзацний відступ 1,25 см, "
              "вирівнювання за шириною. Обсяг звіту — 5–7 сторінок без "
              "урахування титульної сторінки та додатків. Ім'я файлу: "
              "«СР_Операції_з_файлами_ПІБ.docx».")

    # ---------- Критерії оцінювання ----------
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Критерій", "Бали"],
        [
            ["Повнота й коректність теоретичної частини", "3"],
            ["Правильність заповнення порівняльної таблиці", "2"],
            ["Виконання практичного завдання за інструкційною карткою", "3"],
            ["Якість пам'ятки «Безпечне видалення файлів»", "1"],
            ["Відповіді на теоретичні питання", "2"],
            ["Оформлення звіту згідно з рекомендаціями", "1"],
            ["Творчий підхід, власні приклади й аналогії для початкової школи",
             "1"],
        ],
        widths=[11.5, 5.0],
    )
    body(doc, "Максимальна кількість балів — 13. Шкала переведення: "
              "12–13 балів — «відмінно», 9–11 — «добре», 6–8 — «задовільно», "
              "менше 6 — «незадовільно» (потребує доопрацювання).")

    callout(doc, "Порада викладачу.",
            "На етапі перевірки звітів звертайте увагу не лише на технічну "
            "правильність дій, а й на те, чи вміє студент пояснити молодшим "
            "школярам правила безпечної роботи з файлами доступною мовою. "
            "Найкращі пам'ятки та аналогії обговоріть на наступному занятті "
            "та включіть до методичної скарбнички групи.",
            fill="E2EFDA", accent="548235")

    doc.save("Самостійна_робота_Операції_з_файлами.docx")
    print("Готово: Самостійна_робота_Операції_з_файлами.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()