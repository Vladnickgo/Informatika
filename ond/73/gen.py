import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ==============================================================================
# 1. НАЛАШТУВАННЯ ТА ГЕНЕРАЦІЯ СХЕМ В APPLE-СТИЛІ (PNG + SVG)
# ==============================================================================

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

COLOR_BG = "#FFFFFF"
COLOR_CARD = "#F5F5F7"
COLOR_BORDER = "#E5E5EA"
COLOR_TEXT_DARK = "#1D1D1F"
COLOR_TEXT_GRAY = "#86868B"
COLOR_TEXT_BODY = "#424245"

ACCENT_BLUE = "#0071E3"
ACCENT_GREEN = "#248A3D"
ACCENT_ORANGE = "#C93400"
ACCENT_RED = "#C4001D"
ACCENT_PURPLE = "#6E30A8"


def draw_apple_card(ax, x, y, w, h, facecolor=COLOR_CARD, edgecolor=COLOR_BORDER,
                    linewidth=1.4, rounding=0.20):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={rounding}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=2
    )
    ax.add_patch(patch)
    return patch


def generate_diagrams(output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    paths = {}

    # --------------------------------------------------------------------------
    # Схема 1. Основні типи діаграм у педагогічному дослідженні (2x2)
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11.6, 5.8))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 5.8)
    ax.axis("off")

    ax.text(
        5.8, 5.45,
        "Основні види діаграм для візуалізації педагогічних даних",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=COLOR_TEXT_DARK
    )

    cards_fig1 = [
        {
            "x": 0.35, "y": 2.75, "w": 5.25, "h": 2.25,
            "accent": ACCENT_BLUE,
            "tag": "КАТЕГОРІАЛЬНІ ДАНІ • ПОРІВНЯННЯ",
            "title": "Стовпчаста діаграма (Bar / Column)",
            "desc": "Порівнює величини між окремими групами:\nконтрольним та експериментальним класами,\nрівнями досягнень НУШ (П, С, Д, В)."
        },
        {
            "x": 6.00, "y": 2.75, "w": 5.25, "h": 2.25,
            "accent": ACCENT_ORANGE,
            "tag": "НЕПЕРЕРВНІ ДАНІ • ЧАСТОТА ІНТЕРВАЛІВ",
            "title": "Гістограма розподілу (Histogram)",
            "desc": "Показує, скільки учнів потрапило у кожен\nчисловий інтервал (наприклад, час виконання\nтесту або розподіл балів від 0 до 100)."
        },
        {
            "x": 0.35, "y": 0.25, "w": 5.25, "h": 2.25,
            "accent": ACCENT_GREEN,
            "tag": "ЧАСТКИ ЦІЛОГО • ВІДСОТКОВА СТРУКТУРА",
            "title": "Кругова діаграма (Pie Chart)",
            "desc": "Відображає внесок кожної категорії у 100%\nвибірки (наприклад, частки відповідей учнів\nв анкеті при кількості категорій до 5)."
        },
        {
            "x": 6.00, "y": 0.25, "w": 5.25, "h": 2.25,
            "accent": ACCENT_PURPLE,
            "tag": "ПАРНІ ЗМІННІ • КОРЕЛЯЦІЙНИЙ ЗВ'ЯЗОК",
            "title": "Діаграма розсіювання (Scatter Plot)",
            "desc": "Виявляє залежність між двома показниками\nодного учня (наприклад, часом тренувань\nу Scratch та підсумковим балом за проєкт)."
        }
    ]

    for c in cards_fig1:
        draw_apple_card(ax, c["x"], c["y"], c["w"], c["h"], rounding=0.20)
        draw_apple_card(
            ax, c["x"] + 0.25, c["y"] + c["h"] - 0.14, 1.25, 0.06,
            facecolor=c["accent"], edgecolor="none", linewidth=0, rounding=0.03
        )
        ax.text(
            c["x"] + 0.25, c["y"] + c["h"] - 0.36,
            c["tag"], ha="left", va="center",
            fontsize=10.5, fontweight="bold", color=c["accent"]
        )
        ax.text(
            c["x"] + 0.25, c["y"] + c["h"] - 0.74,
            c["title"], ha="left", va="center",
            fontsize=13.5, fontweight="bold", color=COLOR_TEXT_DARK
        )
        ax.text(
            c["x"] + 0.25, c["y"] + 0.76,
            c["desc"], ha="left", va="center",
            fontsize=11.2, color=COLOR_TEXT_BODY, linespacing=1.38
        )

    fig1_png = os.path.join(output_dir, "fig1_chart_types.png")
    fig1_svg = os.path.join(output_dir, "fig1_chart_types.svg")
    fig.savefig(fig1_png, dpi=220, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(fig1_svg, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    paths["fig1"] = fig1_png

    # --------------------------------------------------------------------------
    # Схема 2. Алгоритм вибору виду діаграми за метою аналізу
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11.8, 3.8))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_xlim(0, 11.8)
    ax.set_ylim(0, 3.8)
    ax.axis("off")

    ax.text(
        5.9, 3.45,
        "Вибір типу графіка залежно від дослідницького завдання",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=COLOR_TEXT_DARK
    )

    steps_fig2 = [
        {
            "x": 0.25, "accent": ACCENT_BLUE,
            "step": "ЗАВДАННЯ 1",
            "title": "Порівняти групи",
            "desc": "Рівні знань у 3-А\nта 3-Б класах до і\nпісля експерименту.",
            "badge": "Стовпчаста"
        },
        {
            "x": 3.18, "accent": ACCENT_GREEN,
            "step": "ЗАВДАННЯ 2",
            "title": "Показати частки",
            "desc": "Відсотковий склад\nвідповідей «Так / Ні»\nв анкеті учнів.",
            "badge": "Кругова"
        },
        {
            "x": 6.11, "accent": ACCENT_ORANGE,
            "step": "ЗАВДАННЯ 3",
            "title": "Оцінити розподіл",
            "desc": "Щільність результатів\nтестування за баль-\nними інтервалами.",
            "badge": "Гістограма"
        },
        {
            "x": 9.04, "accent": ACCENT_PURPLE,
            "step": "ЗАВДАННЯ 4",
            "title": "Знайти зв’язок",
            "desc": "Вплив кількості спроб\nу тренажері на оцінку\nкожного учня.",
            "badge": "Розсіювання"
        }
    ]

    c_w = 2.51
    c_h = 2.65
    c_y = 0.30

    for i, s in enumerate(steps_fig2):
        draw_apple_card(ax, s["x"], c_y, c_w, c_h, rounding=0.20)
        ax.text(
            s["x"] + c_w / 2, c_y + c_h - 0.32,
            s["step"], ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=s["accent"]
        )
        ax.text(
            s["x"] + c_w / 2, c_y + c_h - 0.68,
            s["title"], ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=COLOR_TEXT_DARK
        )
        ax.text(
            s["x"] + c_w / 2, c_y + 1.18,
            s["desc"], ha="center", va="center",
            fontsize=11.0, color=COLOR_TEXT_BODY, linespacing=1.32
        )
        draw_apple_card(
            ax, s["x"] + 0.25, c_y + 0.18, c_w - 0.50, 0.38,
            facecolor="#FFFFFF", edgecolor=s["accent"], linewidth=1.2, rounding=0.10
        )
        ax.text(
            s["x"] + c_w / 2, c_y + 0.37,
            s["badge"], ha="center", va="center",
            fontsize=11.0, fontweight="bold", color=s["accent"]
        )

        if i < len(steps_fig2) - 1:
            x_s = s["x"] + c_w + 0.05
            x_e = steps_fig2[i + 1]["x"] - 0.05
            y_m = c_y + c_h / 2
            arrow = FancyArrowPatch(
                (x_s, y_m), (x_e, y_m),
                arrowstyle="-|>,head_length=6,head_width=4",
                color=COLOR_TEXT_GRAY, linewidth=1.6, zorder=3
            )
            ax.add_patch(arrow)

    fig2_png = os.path.join(output_dir, "fig2_chart_selection.png")
    fig2_svg = os.path.join(output_dir, "fig2_chart_selection.svg")
    fig.savefig(fig2_png, dpi=220, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(fig2_svg, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    paths["fig2"] = fig2_png

    # --------------------------------------------------------------------------
    # Схема 3. Принципи культури наукової візуалізації даних
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11.6, 3.6))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 3.6)
    ax.axis("off")

    ax.text(
        5.8, 3.25,
        "Три правила коректного оформлення наукових графіків",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=COLOR_TEXT_DARK
    )

    rules_fig3 = [
        {
            "x": 0.30, "accent": ACCENT_BLUE,
            "num": "ПРАВИЛО 1",
            "title": "Повнота атрибутів",
            "desc": "Кожен графік має змістовну\nназву, підписи обох осей,\nодиниці вимірювання (%, бали)\nта зрозумілу легенду."
        },
        {
            "x": 4.075, "accent": ACCENT_RED,
            "num": "ПРАВИЛО 2",
            "title": "Чесний масштаб осей",
            "desc": "Вісь значень у стовпчастих\nдіаграмах завжди починається\nз нуля, щоб не спотворювати\nрізницю між групами."
        },
        {
            "x": 7.85, "accent": ACCENT_GREEN,
            "num": "ПРАВИЛО 3",
            "title": "Візуальна стриманість",
            "desc": "У наукових роботах не\nзастосовують об’ємні 3D-ефекти,\nтіні та строкаті градієнти,\nякі ускладнюють читання."
        }
    ]

    r_w = 3.45
    r_h = 2.55
    r_y = 0.32

    for r_item in rules_fig3:
        draw_apple_card(ax, r_item["x"], r_y, r_w, r_h, rounding=0.20)
        ax.text(
            r_item["x"] + 0.24, r_y + r_h - 0.34,
            r_item["num"], ha="left", va="center",
            fontsize=10.5, fontweight="bold", color=r_item["accent"]
        )
        ax.text(
            r_item["x"] + 0.24, r_y + r_h - 0.72,
            r_item["title"], ha="left", va="center",
            fontsize=13.0, fontweight="bold", color=COLOR_TEXT_DARK
        )
        ax.text(
            r_item["x"] + 0.24, r_y + 0.86,
            r_item["desc"], ha="left", va="center",
            fontsize=11.0, color=COLOR_TEXT_BODY, linespacing=1.34
        )

    fig3_png = os.path.join(output_dir, "fig3_visualization_rules.png")
    fig3_svg = os.path.join(output_dir, "fig3_visualization_rules.svg")
    fig.savefig(fig3_png, dpi=220, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(fig3_svg, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    paths["fig3"] = fig3_png

    # --------------------------------------------------------------------------
    # Схема 4. Структура різнорівневих практичних завдань (27 хв)
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11.6, 4.1))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 4.1)
    ax.axis("off")

    ax.text(
        5.8, 3.75,
        "Структура різнорівневих завдань практичної роботи (загальний час — 27 хв)",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=COLOR_TEXT_DARK
    )

    levels_fig4 = [
        {
            "x": 0.30, "accent": ACCENT_BLUE,
            "badge": "РІВЕНЬ 1 • ≈ 7 ХВ",
            "title": "Репродуктивний",
            "desc": "Добір типу діаграми для\nпедагогічних задач, порівняння\nгістограми та стовпчастої,\nпошук помилок на графіку.",
            "score": "Оцінювання: до 3 балів"
        },
        {
            "x": 4.075, "accent": ACCENT_ORANGE,
            "badge": "РІВЕНЬ 2 • ≈ 10 ХВ",
            "title": "Продуктивний",
            "desc": "Побудова в табличному\nпроцесорі стовпчастої,\nгістограми та діаграми\nрозсіювання з лінією тренду.",
            "score": "Оцінювання: до 4 балів"
        },
        {
            "x": 7.85, "accent": ACCENT_GREEN,
            "badge": "РІВЕНЬ 3 • ≈ 10 ХВ",
            "title": "Творчий",
            "desc": "Візуалізація динаміки\nпедагогічного експерименту\nу 3-х класах та написання\nаналітичного висновку.",
            "score": "Оцінювання: до 4 балів"
        }
    ]

    lvl_w = 3.45
    lvl_h = 2.95
    lvl_y = 0.35

    for idx, lv in enumerate(levels_fig4):
        draw_apple_card(ax, lv["x"], lvl_y, lvl_w, lvl_h, rounding=0.20)
        ax.text(
            lv["x"] + 0.24, lvl_y + lvl_h - 0.35,
            lv["badge"], ha="left", va="center",
            fontsize=10.5, fontweight="bold", color=lv["accent"]
        )
        ax.text(
            lv["x"] + 0.24, lvl_y + lvl_h - 0.72,
            lv["title"], ha="left", va="center",
            fontsize=13.5, fontweight="bold", color=COLOR_TEXT_DARK
        )
        ax.text(
            lv["x"] + 0.24, lvl_y + 1.32,
            lv["desc"], ha="left", va="center",
            fontsize=11.0, color=COLOR_TEXT_BODY, linespacing=1.35
        )
        draw_apple_card(
            ax, lv["x"] + 0.22, lvl_y + 0.20, lvl_w - 0.44, 0.38,
            facecolor="#FFFFFF", edgecolor=COLOR_BORDER, linewidth=1.1, rounding=0.10
        )
        ax.text(
            lv["x"] + lvl_w / 2, lvl_y + 0.39,
            lv["score"], ha="center", va="center",
            fontsize=11.0, fontweight="bold", color=lv["accent"]
        )

        if idx < len(levels_fig4) - 1:
            x_s = lv["x"] + lvl_w + 0.05
            x_e = levels_fig4[idx + 1]["x"] - 0.05
            y_m = lvl_y + lvl_h / 2
            arrow = FancyArrowPatch(
                (x_s, y_m), (x_e, y_m),
                arrowstyle="-|>,head_length=6,head_width=4",
                color=COLOR_TEXT_GRAY, linewidth=1.6, zorder=3
            )
            ax.add_patch(arrow)

    fig4_png = os.path.join(output_dir, "fig4_task_levels.png")
    fig4_svg = os.path.join(output_dir, "fig4_task_levels.svg")
    fig.savefig(fig4_png, dpi=220, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(fig4_svg, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    paths["fig4"] = fig4_png

    return paths


# ==============================================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ОФОРМЛЕННЯ DOCX
# ==============================================================================

HEX_PRIMARY = "1F4E79"
HEX_SECONDARY = "2E75B6"
RGB_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)
RGB_SECONDARY = RGBColor(0x2E, 0x75, 0xB6)
RGB_DARK = RGBColor(0x1D, 0x1D, 0x1F)
RGB_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RGB_CODE = RGBColor(0xC0, 0x39, 0x2B)


def set_run_font(run, font_name="Times New Roman", size_pt=14, bold=False,
                 italic=False, color=RGB_DARK):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    run._element.rPr.rFonts.set(qn("w:cs"), font_name)
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_styled_paragraph(doc, segments, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                         space_before=0, space_after=5, line_spacing=1.15,
                         left_indent_cm=0.0, first_line_indent_cm=0.0):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    if left_indent_cm:
        pf.left_indent = Cm(left_indent_cm)
    if first_line_indent_cm:
        pf.first_line_indent = Cm(first_line_indent_cm)

    for text, flag in segments:
        r = p.add_run(text)
        if flag == "bold":
            set_run_font(r, bold=True)
        elif flag == "italic":
            set_run_font(r, italic=True)
        elif flag == "bold_italic":
            set_run_font(r, bold=True, italic=True)
        elif flag == "code":
            set_run_font(r, font_name="Consolas", size_pt=12.5, bold=False, color=RGB_CODE)
        elif flag == "primary":
            set_run_font(r, bold=True, color=RGB_PRIMARY)
        elif flag == "secondary":
            set_run_font(r, bold=True, color=RGB_SECONDARY)
        else:
            set_run_font(r)
    return p


def add_section_heading(doc, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(10)
    pf.space_after = Pt(5)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    r = p.add_run(title)
    set_run_font(r, size_pt=14, bold=True, color=RGB_PRIMARY)
    return p


def add_subheading(doc, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_before = Pt(7)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    r = p.add_run(title)
    set_run_font(r, size_pt=14, bold=True, color=RGB_SECONDARY)
    return p


def numbered_paren(doc, items):
    """Нумерований список у форматі 1), 2), 3)... з відступом 1,0 см."""
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        r_num = p.add_run(f"{idx}) ")
        set_run_font(r_num, bold=True)
        r_txt = p.add_run(item)
        set_run_font(r_txt)


def add_list_number(doc, items):
    """Нумерований список List Number з відступом 1,0 см."""
    for item in items:
        p = doc.add_paragraph(style="List Number")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        if isinstance(item, str):
            r = p.add_run(item)
            set_run_font(r)
        else:
            for text, flag in item:
                r = p.add_run(text)
                if flag == "bold":
                    set_run_font(r, bold=True)
                elif flag == "code":
                    set_run_font(r, font_name="Consolas", size_pt=12.5, color=RGB_CODE)
                else:
                    set_run_font(r)


def add_list_bullet(doc, items):
    """Маркований список List Bullet з відступом 1,0 см."""
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.left_indent = Cm(1.0)
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        if isinstance(item, str):
            r = p.add_run(item)
            set_run_font(r)
        else:
            for text, flag in item:
                r = p.add_run(text)
                if flag == "bold":
                    set_run_font(r, bold=True)
                elif flag == "code":
                    set_run_font(r, font_name="Consolas", size_pt=12.5, color=RGB_CODE)
                else:
                    set_run_font(r)


def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_row_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)


def set_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)


def add_callout_block(doc, segments, bg_hex="EDF4FB", border_hex="1F4E79"):
    """
    Callout-блок: таблиця з 1 осередком, пастельна заливка,
    ліва рамка 28 sz, без службових заголовків.
    """
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(16.5)

    set_cell_shading(cell, bg_hex)
    set_cell_margins(cell, top=130, bottom=130, left=200, right=180)

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")

    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), border_hex)
    tcBorders.append(left)

    for side in ("top", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), "D0E2F2")
        tcBorders.append(b)

    tcPr.append(tcBorders)
    set_row_cant_split(tbl.rows[0])

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.15

    for text, flag in segments:
        r = p.add_run(text)
        if flag == "bold":
            set_run_font(r, size_pt=13.5, bold=True, color=RGB_PRIMARY)
        elif flag == "code":
            set_run_font(r, font_name="Consolas", size_pt=12, color=RGB_CODE)
        else:
            set_run_font(r, size_pt=13.5, color=RGB_DARK)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)


def add_styled_table(doc, headers, rows_data, col_widths_cm, font_size_pt=13):
    """
    Таблиця Table Grid із шапкою #1F4E79, білим жирним текстом,
    повторенням шапки tblHeader та фіксованими ширинами стовпців у см.
    """
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    hdr_row = tbl.rows[0]
    set_row_repeat_header(hdr_row)
    set_row_cant_split(hdr_row)
    for col_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[col_idx]
        cell.width = Cm(col_widths_cm[col_idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=100, bottom=100, left=110, right=110)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.1
        r = p.add_run(h_text)
        set_run_font(r, size_pt=font_size_pt, bold=True, color=RGB_WHITE)

    for r_idx, row_items in enumerate(rows_data, start=1):
        row = tbl.rows[r_idx]
        set_row_cant_split(row)
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, cell_val in enumerate(row_items):
            cell = row.cells[c_idx]
            cell.width = Cm(col_widths_cm[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=85, bottom=85, left=110, right=110)

            p = cell.paragraphs[0]
            if isinstance(cell_val, str) and len(cell_val) <= 10:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf = p.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.line_spacing = 1.12

            if isinstance(cell_val, str):
                r = p.add_run(cell_val)
                set_run_font(r, size_pt=font_size_pt, bold=(c_idx == 0 and len(cell_val) <= 6))
            else:
                for seg_text, seg_flag in cell_val:
                    r = p.add_run(seg_text)
                    if seg_flag == "bold":
                        set_run_font(r, size_pt=font_size_pt, bold=True)
                    elif seg_flag == "code":
                        set_run_font(r, font_name="Consolas", size_pt=font_size_pt - 1, color=RGB_CODE)
                    else:
                        set_run_font(r, size_pt=font_size_pt)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)
    return tbl


def add_figure(doc, img_path, caption_text, width_cm=15.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p_img.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after = Pt(3)
    pf.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf_c = p_cap.paragraph_format
    pf_c.space_before = Pt(0)
    pf_c.space_after = Pt(6)
    r_cap = p_cap.add_run(caption_text)
    set_run_font(r_cap, size_pt=12.5, italic=True, color=RGBColor(0x55, 0x55, 0x55))


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"

    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")

    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")

    r_page = p.add_run()
    set_run_font(r_page, size_pt=12, color=RGB_DARK)
    r_page._r.append(fldChar1)
    r_page._r.append(instrText)
    r_page._r.append(fldChar2)
    r_page._r.append(fldChar3)


# ==============================================================================
# 3. ФОРМУВАННЯ НАВЧАЛЬНОГО ДОКУМЕНТА DOCX
# ==============================================================================

def build_practical_work_docx(diagram_paths, filename="Praktychne_zanyattya_14.docx"):
    doc = Document()

    # Параметри сторінки A4 (ширина робочого поля = 21.0 - 2.25 - 2.25 = 16.5 см)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.25)
    section.right_margin = Cm(2.25)

    # Базовий стиль Normal
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal_style.font.size = Pt(14)
    normal_style.font.color.rgb = RGB_DARK

    add_page_number_footer(section)

    # --------------------------------------------------------------------------
    # ВСТУПНІ РЕКВІЗИТИ ЗАНЯТТЯ
    # --------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("ПРАКТИЧНЕ ЗАНЯТТЯ № 14")
    set_run_font(r_title, size_pt=14, bold=True, color=RGB_PRIMARY)

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(0)
    p_topic.paragraph_format.space_after = Pt(8)
    p_topic.paragraph_format.line_spacing = 1.15
    r_topic = p_topic.add_run(
        "Тема: Графічне представлення даних: гістограми, діаграми розсіювання тощо."
    )
    set_run_font(r_topic, size_pt=14, bold=True, color=RGB_DARK)

    add_styled_paragraph(doc, [
        ("Мета: ", "primary"),
        ("формувати вміння будувати гістограми, діаграми розсіювання, стовпчасті та кругові "
         "діаграми засобами табличного процесора; розвивати вміння обирати доцільні види графіків "
         "для різних типів педагогічних даних та готувати підсумковий звіт; виховувати культуру "
         "наочного подання наукової інформації і відповідальність за точність її візуалізації.", "normal")
    ], space_after=6)

    add_styled_paragraph(doc, [
        ("Обладнання та програмне забезпечення:", "primary")
    ], align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=3)

    numbered_paren(doc, [
        "інструкційні картки до практичного заняття;",
        "персональні комп’ютери (ноутбуки) з доступом до мережі Інтернет;",
        "табличний процесор (Microsoft Excel або Google Таблиці) для обробки та візуалізації даних."
    ])

    add_styled_paragraph(doc, [
        ("Література:", "primary")
    ], align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=3)

    add_list_number(doc, [
        "Гончаренко С. У. Педагогічні дослідження : методологічні поради молодим науковцям. Київ ; Вінниця : ДОВ «Вінниця», 2008. 278 с.",
        "Методичні рекомендації щодо написання та оформлення курсової роботи. Путивль : КЗСОР «Путивльський педагогічний фаховий коледж імені С. В. Руднєва», 2024. 14 с.",
        "Сисоєва С. О., Кристопчук Т. Є. Методологія науково-педагогічних досліджень. Рівне : Волинські обереги, 2013. 360 с."
    ])

    add_styled_paragraph(doc, [
        ("Хід заняття:", "primary")
    ], align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=3)

    add_list_number(doc, [
        "Організаційний етап та повторення правил безпечної роботи за комп’ютером.",
        "Опрацювання теоретичних відомостей щодо класифікації та вибору діаграм у педагогічному дослідженні.",
        "Виконання комплексу різнорівневих практичних завдань у табличному процесорі за інструкційною карткою.",
        "Оформлення індивідуального звіту, самооцінювання результатів та підбиття підсумків заняття."
    ])

    # --------------------------------------------------------------------------
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Теоретичні відомості")

    add_subheading(doc, "1. Роль графічного представлення даних у педагогічному дослідженні")
    add_styled_paragraph(doc, [
        ("Після збору та формалізації емпіричних показників дослідник отримує зведені числові "
         "таблиці. Проте сприймати закономірності, порівнювати успішність двох класів або "
         "відстежувати динаміку формування алгоритмічних умінь молодших школярів значно швидше "
         "за допомогою ", "normal"),
        ("графічної візуалізації", "bold"),
        (". У курсових і кваліфікаційних роботах майбутнього вчителя інформатики діаграми не "
         "дублюють таблиці механічно, а наочно підкреслюють головні висновки педагогічного "
         "експерименту.", "normal")
    ])

    add_subheading(doc, "2. Класифікація основних видів діаграм")
    add_styled_paragraph(doc, [
        ("Залежно від природи педагогічних вимірювань у наукових дослідженнях використовують "
         "чотири базові типи діаграм (рис. 1): ", "normal"),
        ("стовпчасті (гістограми порівняння категорій), частотні гістограми, кругові діаграми "
         "та діаграми розсіювання", "bold"),
        (". Для відображення змін показників у часі (наприклад, результатів чотирьох "
         "тематичних контрольних робіт протягом навчального року) додатково застосовують ", "normal"),
        ("лінійні графіки (графіки трендів)", "bold"),
        (".", "normal")
    ])

    add_figure(
        doc,
        diagram_paths["fig1"],
        "Рис. 1. Класифікація основних видів діаграм у педагогічних дослідженнях"
    )

    add_subheading(doc, "3. Вибір типу діаграми відповідно до шкали та мети аналізу")
    add_styled_paragraph(doc, [
        ("Помилковий вибір діаграми спотворює зміст експерименту. Наприклад, кругова діаграма "
         "непридатна для порівняння середніх балів різних класів, оскільки їхня сума не утворює "
         "єдиного цілого (100 %). Так само не варто плутати ", "normal"),
        ("звичайну стовпчасту діаграму", "bold"),
        (" (де стовпці розділені проміжками й позначають окремі категорії, як-от «3-А клас» і «3-Б клас») "
         "із ", "normal"),
        ("частотною гістограмою", "bold"),
        (" (де стовпці прилягають один до одного без проміжків, відображаючи неперервні інтервали "
         "значень, наприклад 0–20, 21–40, 41–60 балів).", "normal")
    ])

    add_figure(
        doc,
        diagram_paths["fig2"],
        "Рис. 2. Алгоритм вибору виду діаграми залежно від дослідницького завдання"
    )

    add_styled_table(
        doc,
        headers=[
            "Дослідницьке завдання в початковій школі",
            "Тип даних",
            "Доцільний вид графіка",
            "Що відкладається по осях"
        ],
        rows_data=[
            [
                "Порівняти розподіл учнів 3-А та 3-Б класів за 4 рівнями навчальних досягнень НУШ",
                "Категоріальні (рангові)",
                [("Стовпчаста діаграма з групуванням", "bold")],
                "Вісь X — рівні (П, С, Д, В); вісь Y — кількість або відсоток учнів"
            ],
            [
                "Показати структуру відповідей 4-го класу на анкету «Улюблений блок у Scratch»",
                "Номінальні (частки цілого)",
                [("Кругова діаграма", "bold")],
                "Сектори кола — варіанти відповідей (у відсотках, сума = 100 %)"
            ],
            [
                "Дослідити частоту розподілу балів за діагностичний тест (від 0 до 12 балів)",
                "Кількісні інтервальні",
                [("Частотна гістограма", "bold")],
                "Вісь X — інтервали балів; вісь Y — частота (кількість учнів)"
            ],
            [
                "Перевірити, чи впливає час виконання вправ у тренажері на оцінку за тест",
                "Парні кількісні змінні",
                [("Діаграма розсіювання", "bold")],
                "Вісь X — час тренування (хв); вісь Y — тестовий бал учня"
            ]
        ],
        col_widths_cm=[4.8, 3.3, 3.8, 4.6],
        font_size_pt=12.5
    )

    add_subheading(doc, "4. Технологія побудови гістограми та діаграми розсіювання у табличному процесорі")
    add_styled_paragraph(doc, [
        ("У програмах Microsoft Excel або Google Таблиці побудова графіка починається з виділення "
         "діапазону числових даних разом із заголовками стовпців та переходу до меню ", "normal"),
        ("Вставлення → Діаграма", "code"),
        (". Для побудови ", "normal"),
        ("діаграми розсіювання", "bold"),
        (" виділяють два суміжні числові стовпці (незалежну змінну X та залежну Y) і обирають тип ", "normal"),
        ("Точкова (Scatter)", "code"),
        (". Щоб оцінити силу зв’язку, на діаграму додають ", "normal"),
        ("лінію тренду", "bold"),
        (" та обчислюють коефіцієнт лінійної кореляції Пірсона за допомогою функції ", "normal"),
        ("=CORREL(B2:B11; C2:C11)", "code"),
        (".", "normal")
    ])

    add_subheading(doc, "5. Культура наукової візуалізації та вимоги до оформлення у курсовій роботі")
    add_styled_paragraph(doc, [
        ("Згідно з вимогами до оформлення курсових робіт педагогічного коледжу, кожен рисунок "
         "(діаграма) розміщується по центру сторінки одразу після першого посилання на нього в тексті "
         "та супроводжується підписом під зображенням у форматі: ", "normal"),
        ("Рис. 2.1. Порівняння рівнів сформованості алгоритмічних умінь учнів 3-х класів", "italic"),
        (". Дотримання трьох базових правил (рис. 3) захищає дослідження від візуальних викривлень.", "normal")
    ])

    add_figure(
        doc,
        diagram_paths["fig3"],
        "Рис. 3. Базові вимоги культури наукового представлення графічних даних"
    )

    # Callout-блок без службового заголовка
    add_callout_block(doc, [
        ("Під час оформлення графіків у науковій роботі не використовуйте об’ємні 3D-діаграми та "
         "обрізану вісь значень (наприклад, початок осі Y зі значення 60 % замість 0 %). Такі прийоми "
         "візуально перебільшують незначну різницю між результатами контрольного й експериментального "
         "класів і порушують принцип наукової об’єктивності. Усі текстові елементи на діаграмі повинні "
         "бути виконані українською мовою без скорочень на кшталт ", "normal"),
        ("Series1", "code"),
        (" або ", "normal"),
        ("Chart Title", "code"),
        (".", "normal")
    ])

    # --------------------------------------------------------------------------
    # ПОКРОКОВИЙ АЛГОРИТМ ВИКОНАННЯ РІЗНОРІВНЕВИХ ЗАВДАНЬ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Покроковий алгоритм виконання різнорівневих завдань")

    add_styled_paragraph(doc, [
        ("Практична частина заняття розрахована на ", "normal"),
        ("27 хвилин", "bold"),
        (" і складається з трьох послідовних рівнів складності (рис. 4). Усі розрахунки та "
         "побудову діаграм виконують у новому файлі табличного процесора ", "normal"),
        ("pr14_visualization.xlsx", "code"),
        (" (кожен рівень завдань оформлюється на окремому аркуші книги).", "normal")
    ])

    add_figure(
        doc,
        diagram_paths["fig4"],
        "Рис. 4. Структура та регламент виконання різнорівневих завдань практичної роботи"
    )

    # Рівень 1
    add_subheading(doc, "Рівень 1 — репродуктивний (орієнтовний час виконання: 7 хв)")
    add_styled_paragraph(doc, [
        ("Завдання 1. ", "bold"),
        ("Опрацюйте наведені нижче педагогічні кейси з досвіду вчителя інформатики початкової "
         "школи, визначте оптимальний вид діаграми для кожного випадку та проаналізуйте помилки "
         "візуалізації.", "normal")
    ])

    add_styled_table(
        doc,
        headers=["Крок", "Зміст практичної дії студента", "Очікуваний проміжний результат"],
        rows_data=[
            [
                "1",
                "Для кожної із 4 педагогічних ситуацій оберіть доцільний вид діаграми та "
                "обґрунтуйте вибір у 1–2 реченнях: а) розподіл 28 учнів 2-го класу за трьома "
                "варіантами відповіді анкети; б) порівняння середнього бала 4-А і 4-Б класів за "
                "4 темами; в) інтервальний розподіл швидкості набору тексту (симв./хв) у 4-му класі; "
                "г) залежність між кількістю виконаних домашніх завдань і підсумковою оцінкою.",
                "Заповнена таблиця обґрунтування вибору графіків у звіті."
            ],
            [
                "2",
                "Поясніть у письмовій формі дві ключові відмінності між стовпчастою діаграмою "
                "та частотною гістограмою (за типом даних по осі X та способом зображення стовпців).",
                "Сформульовано чітке порівняння обох видів діаграм."
            ],
            [
                "3",
                "Виявіть 3 помилки оформлення діаграми: «На діаграмі порівняння успішності 3-А "
                "(72 %) і 3-Б (76 %) класів застосовано 3D-стовпці, вісь Y починається зі значення "
                "70 %, а підпис графіка має вигляд “Діаграма 1”».",
                "Перелічено 3 порушення правил наукової візуалізації та запропоновано виправлення."
            ]
        ],
        col_widths_cm=[1.5, 9.2, 5.8],
        font_size_pt=12.5
    )

    # Рівень 2
    add_subheading(doc, "Рівень 2 — продуктивний (орієнтовний час виконання: 10 хв)")
    add_styled_paragraph(doc, [
        ("Завдання 2. ", "bold"),
        ("У табличному процесорі на аркуші ", "normal"),
        ("Рівень_2", "code"),
        (" введіть емпіричні дані вибірки з 10 учнів 4-го класу (час виконання тренувальних "
         "вправ у середовищі Scratch у хвилинах та отриманий тестовий бал за 12-бальною шкалою) "
         "і побудуйте два типи графіків.", "normal")
    ])

    add_styled_table(
        doc,
        headers=[
            "Код учня",
            "Учень_01",
            "Учень_02",
            "Учень_03",
            "Учень_04",
            "Учень_05",
            "Учень_06",
            "Учень_07",
            "Учень_08",
            "Учень_09",
            "Учень_10"
        ],
        rows_data=[
            [
                [("Час тренувань, хв (X)", "bold")],
                "12", "18", "25", "15", "32", "28", "10", "35", "22", "30"
            ],
            [
                [("Тестовий бал (Y)", "bold")],
                "5", "7", "9", "6", "11", "10", "4", "12", "8", "10"
            ]
        ],
        col_widths_cm=[3.5, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3],
        font_size_pt=11.5
    )

    add_styled_table(
        doc,
        headers=["Крок", "Зміст практичної дії студента", "Очікуваний проміжний результат"],
        rows_data=[
            [
                "1",
                [
                    ("Перенесіть таблицю вихідних даних у вертикальний діапазон ", "normal"),
                    ("A1:C11", "code"),
                    (" (стовпець A — код учня, B — час тренувань, C — тестовий бал) та побудуйте ", "normal"),
                    ("частотну гістограму", "bold"),
                    (" розподілу тестових балів учнів (із шириною інтервалу 3 бали).", "normal")
                ],
                "Побудовано частотну гістограму з підписаними осями й заголовком."
            ],
            [
                "2",
                [
                    ("Виділіть числові стовпці ", "normal"),
                    ("B1:C11", "code"),
                    (" та побудуйте ", "normal"),
                    ("діаграму розсіювання", "bold"),
                    (" (Точкову діаграму). Додайте на графік лінійну лінію тренду та підпишіть "
                     "осі: X — «Час тренувань у Scratch, хв», Y — «Тестовий бал».", "normal")
                ],
                "Оформлено діаграму розсіювання з лінією тренду."
            ],
            [
                "3",
                [
                    ("В окремій клітинці обчисліть коефіцієнт кореляції Пірсона формулою ", "normal"),
                    ("=CORREL(B2:B11; C2:C11)", "code"),
                    (" та сформулюйте висновок про характер зв’язку між часом тренувань і "
                     "результатом тестування.", "normal")
                ],
                "Отримано значення коефіцієнта кореляції (≈ 0,98) та записано висновок."
            ]
        ],
        col_widths_cm=[1.5, 9.2, 5.8],
        font_size_pt=12.5
    )

    # Рівень 3
    add_subheading(doc, "Рівень 3 — творчий (орієнтовний час виконання: 10 хв)")
    add_styled_paragraph(doc, [
        ("Завдання 3. ", "bold"),
        ("У межах курсової роботи проведено формувальний експеримент із розвитку алгоритмічного "
         "мислення учнів 3-х класів. За наведеними зведеними даними контрольного (3-А, 25 учнів) "
         "та експериментального (3-Б, 25 учнів) класів на аркуші ", "normal"),
        ("Рівень_3", "code"),
        (" виконайте комплексну візуалізацію та наукову інтерпретацію результатів.", "normal")
    ])

    add_styled_table(
        doc,
        headers=[
            "Рівень навчальних досягнень НУШ",
            "3-А (контрольний), до експерименту, %",
            "3-А (контрольний), після експерименту, %",
            "3-Б (експериментальний), до експерименту, %",
            "3-Б (експериментальний), після експерименту, %"
        ],
        rows_data=[
            ["Початковий (1–3 бали)", "24", "20", "24", "8"],
            ["Середній (4–6 балів)", "40", "40", "44", "24"],
            ["Достатній (7–9 балів)", "28", "32", "24", "44"],
            ["Високий (10–12 балів)", "8", "8", "8", "24"]
        ],
        col_widths_cm=[4.5, 3.0, 3.0, 3.0, 3.0],
        font_size_pt=12.0
    )

    add_styled_paragraph(doc, [
        ("Вимоги до виконання творчого завдання:", "bold")
    ], align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=3)

    add_list_bullet(doc, [
        "побудувати групову стовпчасту діаграму порівняння результатів контрольного та експериментального класів на контрольному етапі експерименту (після експерименту) у відсотках;",
        "додатково побудувати кругову діаграму структури рівнів досягнень учнів 3-Б класу після впровадження авторської методики із відображенням підписів даних (%);",
        "оформити обидва графіки відповідно до вимог методичних рекомендацій коледжу (змістовна назва, єдина колірна палітра, вимкнені 3D-ефекти, вісь Y від 0 % до 50 %);",
        "написати науковий висновок до діаграм (4–5 речень) для розділу курсової роботи про ефективність проведеного педагогічного експерименту."
    ])

    # --------------------------------------------------------------------------
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Критерії оцінювання")

    add_styled_paragraph(doc, [
        ("Максимальна оцінка за виконання практичного заняття становить ", "normal"),
        ("13 балів", "bold"),
        (" і складається з балів за три рівні практичних завдань та якість оформлення звіту:", "normal")
    ])

    add_styled_table(
        doc,
        headers=[
            "Компонент оцінювання",
            "Показники сформованості вмінь",
            "Максимальний бал"
        ],
        rows_data=[
            [
                "Рівень 1 (репродуктивний)",
                "Безпомилково підібрано типи діаграм для всіх 4 педагогічних кейсів; "
                "чітко розмежовано стовпчасту діаграму та гістограму; виявлено всі дефекти графіка.",
                "3 бали"
            ],
            [
                "Рівень 2 (продуктивний)",
                "Коректно побудовано частотну гістограму та діаграму розсіювання у табличному "
                "процесорі; додано лінію тренду, обчислено кореляцію та пояснено її зміст.",
                "4 бали"
            ],
            [
                "Рівень 3 (творчий)",
                "Грамотно візуалізовано порівняльні результати педагогічного експерименту; "
                "дотримано стандартів оформлення графіків у курсовій роботі; висновок аргументований.",
                "4 бали"
            ],
            [
                "Оформлення та захист звіту",
                "Електронний звіт і табличний файл містять усі обов’язкові компоненти, охайно "
                "структуровані; студент впевнено пояснює вибір кожного типу діаграми.",
                "2 бали"
            ],
            [
                [("Разом", "bold")],
                [("Сумарний бал за практичне заняття № 14", "bold")],
                [("13 балів", "bold")]
            ]
        ],
        col_widths_cm=[4.2, 9.5, 2.8],
        font_size_pt=12.5
    )

    # --------------------------------------------------------------------------
    # ФОРМА ЗВІТНОСТІ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Форма звітності")

    add_styled_paragraph(doc, [
        ("За підсумками заняття студент подає викладачеві два електронні файли (або роздрукований "
         "звіт із електронним додатком): текстовий документ звіту та файл табличного процесора ", "normal"),
        ("pr14_visualization.xlsx", "code"),
        (". Звіт повинен містити:", "normal")
    ], space_after=4)

    add_list_number(doc, [
        "Титульну шапку із зазначенням номера і теми практичного заняття, прізвища, імені та групи студента.",
        "Письмові відповіді та таблицю відповідності типів діаграм до педагогічних ситуацій (Рівень 1).",
        "Вставлені знімки (або експортовані зображення) частотної гістограми, діаграми розсіювання з лінією тренду, формулу розрахунку кореляції та висновок (Рівень 2).",
        "Порівняльну стовпчасту та кругову діаграми результатів педагогічного експерименту з підписами за вимогами до курсової роботи та аналітичним висновком (Рівень 3)."
    ])

    doc.save(filename)
    print(f"Документ успішно збережено: {filename}")
    print("Згенеровані схеми (PNG + SVG) збережено у папці: output/")


if __name__ == "__main__":
    diagrams = generate_diagrams(output_dir="output")
    build_practical_work_docx(
        diagram_paths=diagrams,
        filename="Praktychne_zanyattya_14_Grafichne_predstavlennya_danykh.docx"
    )