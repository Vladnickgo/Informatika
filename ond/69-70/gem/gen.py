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
# 1. НАЛАШТУВАННЯ MATPLOTLIB ТА ГЕНЕРАЦІЯ СХЕМ (SVG + PNG)
# ==============================================================================
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_apple_card(ax, x, y, w, h, title, subtitle_lines, accent_color,
                    bg_color="#F5F5F7", border_color="#E5E5EA",
                    title_size=13.5, body_size=11.0, badge_text=None):
    """Малює картку в стилі Apple з верхньою акцентною смугою або бейджем."""
    card = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        facecolor=bg_color, edgecolor=border_color, linewidth=1.4, zorder=2
    )
    ax.add_patch(card)

    # Кольорова акцентна плашка зверху або бейдж
    if badge_text:
        badge_w = min(w * 0.45, 2.2)
        badge_h = 0.36
        badge = FancyBboxPatch(
            (x + 0.18, y + h - badge_h - 0.16), badge_w, badge_h,
            boxstyle="round,pad=0.01,rounding_size=0.14",
            facecolor=accent_color, edgecolor="none", zorder=3
        )
        ax.add_patch(badge)
        ax.text(
            x + 0.18 + badge_w / 2, y + h - badge_h / 2 - 0.16,
            badge_text, color="#FFFFFF", fontsize=10.5, fontweight="bold",
            ha="center", va="center", zorder=4
        )
        title_y = y + h - 0.72
    else:
        bar = FancyBboxPatch(
            (x + 0.18, y + h - 0.22), w - 0.36, 0.09,
            boxstyle="round,pad=0.005,rounding_size=0.04",
            facecolor=accent_color, edgecolor="none", zorder=3
        )
        ax.add_patch(bar)
        title_y = y + h - 0.48

    ax.text(
        x + 0.20, title_y, title,
        color="#1D1D1F", fontsize=title_size, fontweight="bold",
        ha="left", va="top", zorder=4
    )

    body_text = "\n".join(subtitle_lines)
    ax.text(
        x + 0.20, title_y - 0.38, body_text,
        color="#515154", fontsize=body_size, linespacing=1.38,
        ha="left", va="top", zorder=4
    )


def draw_arrow(ax, x1, y1, x2, y2, color="#86868B"):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>,head_length=7,head_width=4.5",
        color=color, linewidth=1.8, zorder=5
    )
    ax.add_patch(arrow)


def generate_scheme_1_methods():
    """Схема 1: Основні емпіричні методи в початковій школі."""
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(
        5.75, 5.32, "ЕМПІРИЧНІ МЕТОДИ ДОСЛІДЖЕННЯ НА УРОКАХ ІНФОРМАТИКИ",
        fontsize=14.5, fontweight="bold", color="#1D1D1F", ha="center", va="center"
    )
    ax.text(
        5.75, 4.98, "Інструментарій збору даних про цифрові навички молодших школярів",
        fontsize=11.5, color="#86868B", ha="center", va="center"
    )

    cards = [
        {
            "x": 0.25, "y": 2.55, "w": 5.35, "h": 2.15,
            "title": "1. Педагогічне спостереження",
            "accent": "#0071E3",
            "lines": [
                "• Фіксація реальної поведінки учнів без втручання.",
                "• Об'єкт: посадка за ПК, робота з мишею, взаємодопомога.",
                "• Інструмент: карта спостереження з чіткими індикаторами."
            ]
        },
        {
            "x": 5.90, "y": 2.55, "w": 5.35, "h": 2.15,
            "title": "2. Педагогічне тестування",
            "accent": "#248A3D",
            "lines": [
                "• Об'єктивна перевірка знань і алгоритмічних умінь.",
                "• Формат: інтерактивні вправи, вибір 1 з 3–4 варіантів.",
                "• Тривалість у 1–4 класах: не більше 7–10 хвилин."
            ]
        },
        {
            "x": 0.25, "y": 0.20, "w": 5.35, "h": 2.15,
            "title": "3. Анкетування (опитування)",
            "accent": "#C93400",
            "lines": [
                "• Вивчення ставлення, інтересів та цифрових звичок.",
                "• Для 1–2 класів: графічні шкали («смайлики», зірочки).",
                "• Прості, однозначні формулювання без подвійних заперечень."
            ]
        },
        {
            "x": 5.90, "y": 0.20, "w": 5.35, "h": 2.15,
            "title": "4. Стандартизоване оцінювання",
            "accent": "#6E30A8",
            "lines": [
                "• Оцінювання за єдиними критеріями та ключами для всіх.",
                "• Переведення «сирих» балів у рівні сформованості.",
                "• Забезпечує порівнюваність результатів різних класів."
            ]
        }
    ]

    for c in cards:
        draw_apple_card(ax, c["x"], c["y"], c["w"], c["h"], c["title"], c["lines"], c["accent"])

    png_path = os.path.join(OUTPUT_DIR, "scheme_1_methods.png")
    svg_path = os.path.join(OUTPUT_DIR, "scheme_1_methods.svg")
    plt.savefig(png_path, dpi=220, bbox_inches="tight", pad_inches=0.15)
    plt.savefig(svg_path, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return png_path


def generate_scheme_2_formalization():
    """Схема 2: Алгоритм формалізації результатів дослідження."""
    fig, ax = plt.subplots(figsize=(12.0, 3.6))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 3.6)
    ax.axis("off")

    ax.text(
        6.0, 3.32, "КОНВЕЄР ФОРМАЛІЗАЦІЇ ЕМПІРИЧНИХ ДАНИХ",
        fontsize=14.5, fontweight="bold", color="#1D1D1F", ha="center", va="center"
    )

    steps = [
        {
            "x": 0.15, "w": 2.65, "accent": "#0071E3", "badge": "КРОК 1",
            "title": "Шифрування",
            "lines": ["Заміна ПІБ учнів", "на анонімні коди", "(У-01, У-02...)"]
        },
        {
            "x": 3.15, "w": 2.65, "accent": "#6E30A8", "badge": "КРОК 2",
            "title": "Кодування",
            "lines": ["Переведення відповідей", "у числа (Так = 1,", "Частково = 0,5, Ні = 0)"]
        },
        {
            "x": 6.15, "w": 2.65, "accent": "#C93400", "badge": "КРОК 3",
            "title": "Зведена матриця",
            "lines": ["Внесення даних", "у таблицю Excel /", "Google Таблиці"]
        },
        {
            "x": 9.15, "w": 2.70, "accent": "#248A3D", "badge": "КРОК 4",
            "title": "Аналіз і висновок",
            "lines": ["Підрахунок середніх,", "відсотків та побудова", "діаграм рівнів"]
        }
    ]

    for i, s in enumerate(steps):
        draw_apple_card(
            ax, s["x"], 0.25, s["w"], 2.70,
            s["title"], s["lines"], s["accent"],
            title_size=13.0, body_size=11.0, badge_text=s["badge"]
        )
        if i < len(steps) - 1:
            draw_arrow(ax, s["x"] + s["w"] + 0.05, 1.60, steps[i + 1]["x"] - 0.05, 1.60)

    png_path = os.path.join(OUTPUT_DIR, "scheme_2_formalization.png")
    svg_path = os.path.join(OUTPUT_DIR, "scheme_2_formalization.svg")
    plt.savefig(png_path, dpi=220, bbox_inches="tight", pad_inches=0.15)
    plt.savefig(svg_path, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return png_path


def generate_scheme_3_levels():
    """Схема 3: Структура трирівневих практичних завдань."""
    fig, ax = plt.subplots(figsize=(11.5, 3.7))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 3.7)
    ax.axis("off")

    ax.text(
        5.75, 3.42, "СТРУКТУРА РІЗНОРІВНЕВИХ ЗАВДАНЬ ПРАКТИКУМУ (27 ХВ)",
        fontsize=14.5, fontweight="bold", color="#1D1D1F", ha="center", va="center"
    )

    levels = [
        {
            "x": 0.20, "w": 3.45, "accent": "#248A3D", "badge": "РІВЕНЬ 1 • ≈ 7 ХВ",
            "title": "Репродуктивний",
            "lines": [
                "• Опрацювання готового",
                "  протоколу спостереження.",
                "• Шифрування та кодування",
                "  первинних індикаторів."
            ]
        },
        {
            "x": 4.02, "w": 3.45, "accent": "#0071E3", "badge": "РІВЕНЬ 2 • ≈ 10 ХВ",
            "title": "Продуктивний",
            "lines": [
                "• Формалізація результатів",
                "  тесту й анкети в Excel.",
                "• Обчислення формулами",
                "  SUM, AVERAGE, COUNTIF."
            ]
        },
        {
            "x": 7.85, "w": 3.45, "accent": "#C93400", "badge": "РІВЕНЬ 3 • ≈ 10 ХВ",
            "title": "Творчий",
            "lines": [
                "• Проєктування власної",
                "  мініанкети для 3 класу.",
                "• Розробка ключа оцінювання",
                "  та шкали рівнів."
            ]
        }
    ]

    for i, lv in enumerate(levels):
        draw_apple_card(
            ax, lv["x"], 0.22, lv["w"], 2.82,
            lv["title"], lv["lines"], lv["accent"],
            title_size=13.5, body_size=11.0, badge_text=lv["badge"]
        )
        if i < len(levels) - 1:
            draw_arrow(ax, lv["x"] + lv["w"] + 0.06, 1.63, levels[i + 1]["x"] - 0.06, 1.63)

    png_path = os.path.join(OUTPUT_DIR, "scheme_3_levels.png")
    svg_path = os.path.join(OUTPUT_DIR, "scheme_3_levels.svg")
    plt.savefig(png_path, dpi=220, bbox_inches="tight", pad_inches=0.15)
    plt.savefig(svg_path, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return png_path


# ==============================================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ ФОРМАТУВАННЯ DOCX
# ==============================================================================
COLOR_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)     # #1F4E79
COLOR_SECONDARY = RGBColor(0x2E, 0x75, 0xB6)   # #2E75B6
COLOR_CODE = RGBColor(0xC0, 0x39, 0x2B)        # #C0392B
COLOR_DARK = RGBColor(0x00, 0x00, 0x00)


def set_run_font(run, font_name="Times New Roman", size_pt=14, bold=False, italic=False, color=COLOR_DARK):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), font_name)
    rFonts.set(qn("w:hAnsi"), font_name)
    rFonts.set(qn("w:cs"), font_name)


def format_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=5, space_before=0, line_spacing=1.15, left_indent_cm=0):
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    if left_indent_cm > 0:
        pf.left_indent = Cm(left_indent_cm)


def add_rich_text(p, text, base_size=14, base_bold=False, base_color=COLOR_DARK):
    """
    Підтримує inline-розмітку:
    **жирний текст**
    `моноширинна команда Consolas #C0392B`
    """
    tokens = []
    i = 0
    n = len(text)
    buf = ""
    while i < n:
        if text[i:i+2] == "**":
            if buf:
                tokens.append(("normal", buf))
                buf = ""
            end = text.find("**", i + 2)
            if end != -1:
                tokens.append(("bold", text[i+2:end]))
                i = end + 2
                continue
        elif text[i] == "`":
            if buf:
                tokens.append(("normal", buf))
                buf = ""
            end = text.find("`", i + 1)
            if end != -1:
                tokens.append(("code", text[i+1:end]))
                i = end + 1
                continue
        buf += text[i]
        i += 1
    if buf:
        tokens.append(("normal", buf))

    for kind, content in tokens:
        r = p.add_run(content)
        if kind == "bold":
            set_run_font(r, "Times New Roman", base_size, bold=True, color=base_color)
        elif kind == "code":
            set_run_font(r, "Consolas", base_size - 1, bold=True, color=COLOR_CODE)
        else:
            set_run_font(r, "Times New Roman", base_size, bold=base_bold, color=base_color)


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=5, line_spacing=1.15)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, "Times New Roman", 14, bold=True, color=COLOR_PRIMARY)
    return p


def add_sub_heading(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=4, line_spacing=1.15)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, "Times New Roman", 14, bold=True, color=COLOR_SECONDARY)
    return p


def add_body_p(doc, text, space_after=5, left_indent_cm=0):
    p = doc.add_paragraph()
    format_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=space_after, left_indent_cm=left_indent_cm)
    add_rich_text(p, text)
    return p


def add_bullet_item(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    format_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, left_indent_cm=1.0)
    add_rich_text(p, text)
    return p


def add_numbered_item(doc, text):
    p = doc.add_paragraph(style="List Number")
    format_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, left_indent_cm=1.0)
    add_rich_text(p, text)
    return p


def numbered_paren(doc, items):
    """Нумерований список у форматі 1), 2), 3)... з відступом 1,0 см."""
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        format_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, left_indent_cm=1.0)
        add_rich_text(p, f"{idx}) {item}")


def add_callout(doc, text, fill_hex="EEF5FC", border_hex="1F4E79"):
    """Callout-блок: таблиця з 1 осередком, пастельна заливка, ліва рамка 28 sz, без заголовків."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(16.5)

    tcPr = cell._tc.get_or_add_tcPr()

    # Заливка
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)

    # Рамки: тільки ліва 28 sz
    tcBorders = OxmlElement("w:tcBorders")
    for side in ["top", "bottom", "right"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "none")
        tcBorders.append(el)
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), border_hex)
    tcBorders.append(left)
    tcPr.append(tcBorders)

    # Внутрішні відступи
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", "110"), ("bottom", "110"), ("left", "180"), ("right", "150")]:
        m = OxmlElement(f"w:{side}")
        m.set(qn("w:w"), val)
        m.set(qn("w:type"), "dxa")
        tcMar.append(m)
    tcPr.append(tcMar)

    p = cell.paragraphs[0]
    format_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, space_before=0, line_spacing=1.15)
    add_rich_text(p, text, base_size=14)

    sp = doc.add_paragraph()
    format_paragraph(sp, space_after=4, space_before=0)


def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", str(top)), ("bottom", str(bottom)), ("left", str(left)), ("right", str(right))]:
        m = OxmlElement(f"w:{side}")
        m.set(qn("w:w"), val)
        m.set(qn("w:type"), "dxa")
        tcMar.append(m)
    tcPr.append(tcMar)


def add_styled_table(doc, headers, rows, col_widths_cm, center_cols=None):
    """Створює таблицю Table Grid із повторюваним заголовком #1F4E79."""
    if center_cols is None:
        center_cols = []
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header row
    hdr_row = tbl.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)

    for j, h_text in enumerate(headers):
        cell = hdr_row.cells[j]
        cell.width = Cm(col_widths_cm[j])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, "1F4E79")
        set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
        p = cell.paragraphs[0]
        format_paragraph(p, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0, space_before=0, line_spacing=1.1)
        r = p.add_run(h_text)
        set_run_font(r, "Times New Roman", 13.5, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))

    # Data rows
    for i, row_data in enumerate(rows):
        row = tbl.rows[i + 1]
        r_trPr = row._tr.get_or_add_trPr()
        r_trPr.append(OxmlElement("w:cantSplit"))
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = Cm(col_widths_cm[j])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=75, bottom=75, left=100, right=100)
            p = cell.paragraphs[0]
            align = WD_ALIGN_PARAGRAPH.CENTER if j in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, align=align, space_after=0, space_before=0, line_spacing=1.12)
            add_rich_text(p, val, base_size=13.5)

    sp = doc.add_paragraph()
    format_paragraph(sp, space_after=4, space_before=0)
    return tbl


def add_scheme_picture(doc, img_path, caption_text, width_cm=16.0):
    p_img = doc.add_paragraph()
    format_paragraph(p_img, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    format_paragraph(p_cap, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    r_cap = p_cap.add_run(caption_text)
    set_run_font(r_cap, "Times New Roman", 12.5, italic=True, color=RGBColor(0x55, 0x55, 0x55))


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run()
    set_run_font(r, "Times New Roman", 12, color=RGBColor(0x55, 0x55, 0x55))
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    r._r.append(fldChar1)
    r._r.append(instrText)
    r._r.append(fldChar2)
    r._r.append(fldChar3)


# ==============================================================================
# 3. ФОРМУВАННЯ ДОКУМЕНТА DOCX
# ==============================================================================
def build_document():
    scheme_1 = generate_scheme_1_methods()
    scheme_2 = generate_scheme_2_formalization()
    scheme_3 = generate_scheme_3_levels()

    doc = Document()

    # Налаштування полів сторінки (A4)
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.0)
        add_page_number_footer(section)

    # Базовий стиль Normal
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(14)

    # --------------------------------------------------------------------------
    # ЗАГОЛОВОК ТА ВХІДНІ ПАРАМЕТРИ
    # --------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    format_paragraph(p_title, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4)
    r_title = p_title.add_run("ПРАКТИЧНЕ ЗАНЯТТЯ 12")
    set_run_font(r_title, "Times New Roman", 14, bold=True, color=COLOR_PRIMARY)

    p_theme = doc.add_paragraph()
    format_paragraph(p_theme, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8)
    r_theme = p_theme.add_run(
        "Тема: Спостереження, тестування, анкетування, стандартизоване оцінювання та формалізація їхніх результатів."
    )
    set_run_font(r_theme, "Times New Roman", 14, bold=True, color=COLOR_DARK)

    add_section_heading(doc, "Мета")
    add_body_p(
        doc,
        "Формувати вміння проводити спостереження, тестування, анкетування, стандартизоване оцінювання та формалізувати їхні результати; розвивати практичні навички збору емпіричних даних; виховувати відповідальність за достовірність і етичність збору даних."
    )

    add_section_heading(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "інструкційні картки до практичного заняття;",
        "зошит для практичних робіт, ручка, олівець, лінійка;",
        "персональний комп’ютер із текстовим редактором Microsoft Word або Google Документи;",
        "табличний процесор Microsoft Excel або Google Таблиці;",
        "бланки протоколу спостереження, анкети й тесту (додаються)."
    ])

    add_section_heading(doc, "Література")
    add_numbered_item(
        doc,
        "Лимар Ю. М. Основи науково-педагогічних досліджень. Чернігів : Чернігівський національний педагогічний університет імені Т. Г. Шевченка, 2011. 56 с."
    )
    add_numbered_item(
        doc,
        "Сисоєва С. О., Кристопчук Т. Є. Методологія науково-педагогічних досліджень. Рівне : Волинські обереги, 2013. 360 с."
    )

    # --------------------------------------------------------------------------
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Теоретичні відомості")

    add_sub_heading(doc, "1. Специфіка емпіричних методів у педагогічному дослідженні")
    add_body_p(
        doc,
        "**Емпіричні методи дослідження** — це способи безпосереднього вивчення педагогічних явищ, процесів і результатів навчання на основі чуттєвого сприйняття, вимірювання та фіксації фактів. Для вчителя інформатики початкової школи (1–4 класи) вибір інструментарію ускладнюється віковими особливостями учнів: швидкою втомлюваністю, нестійкою увагою та обмеженими навичками читання у першокласників."
    )
    add_scheme_picture(
        doc, scheme_1,
        "Рис. 1. Емпіричні методи дослідження на уроках інформатики в початковій школі"
    )

    add_sub_heading(doc, "2. Педагогічне спостереження та протоколювання")
    add_body_p(
        doc,
        "**Педагогічне спостереження** — це цілеспрямоване, систематичне сприйняття та фіксація проявів навчальної діяльності учнів у природних умовах уроку. Щоб спостереження мало наукову цінність, воно повинно бути **стандартизованим** (структурованим): дослідник заздалегідь визначає конкретні поведінкові індикатори (наприклад: «самостійно запускає середовище ScratchJr», «дотримується правил безпечної роботи за комп’ютером», «звертається по допомогу до вчителя») і заносить їх до **карти (протоколу) спостереження**."
    )

    add_sub_heading(doc, "3. Тестування та анкетування молодших школярів")
    add_body_p(
        doc,
        "**Педагогічне тестування** використовують для об’єктивного вимірювання рівня сформованості знань і способів дій за допомогою системи стандартизованих завдань. У початковій школі доцільно поєднувати завдання з вибором однієї правильної відповіді та візуальні вправи (встановлення послідовності команд виконавця). **Анкетування** (письмове опитування) спрямоване на виявлення мотивації, пізнавального інтересу та цифрових звичок дитини. Для учнів 1–2 класів текстові варіанти відповідей замінюють **графічними шкалами** (смайлики, зірочки, світлофор)."
    )

    add_sub_heading(doc, "4. Стандартизоване оцінювання та критеріальні шкали")
    add_body_p(
        doc,
        "**Стандартизоване оцінювання** передбачає єдину процедуру проведення діагностики, однакові інструкції, фіксований час і чіткі ключі перевірки для всіх респондентів. Первинні («сирі») бали переводять у відсотки успішності та співвідносять із **рівнями сформованості** досліджуваної якості: початковим (низьким), середнім, достатнім або високим."
    )

    add_sub_heading(doc, "5. Формалізація результатів емпіричного дослідження")
    add_body_p(
        doc,
        "**Формалізація результатів** — це переведення якісних описів, відповідей анкет і позначок у протоколах у стандартизовану числову або табличну форму, придатну для математико-статистичного опрацювання. Процес охоплює чотири обов’язкові етапи: шифрування персональних даних, присвоєння числових кодів індикаторам, побудову зведеної матриці даних та обчислення узагальнених показників."
    )
    add_scheme_picture(
        doc, scheme_2,
        "Рис. 2. Послідовність формалізації результатів педагогічної діагностики"
    )

    add_callout(
        doc,
        "Під час збору та формалізації даних у школі обов’язково дотримуйтеся принципу конфіденційності: у зведені таблиці та звіти заборонено вносити прізвища й імена учнів — використовуйте лише знеособлені шифри (наприклад, `У-01`, `У-02`), а опитування проводьте лише за згодою батьків та адміністрації закладу.",
        fill_hex="EEF5FC", border_hex="1F4E79"
    )

    # --------------------------------------------------------------------------
    # ПОКРОКОВИЙ АЛГОРИТМ ВИКОНАННЯ РІЗНОРІВНЕВИХ ЗАВДАНЬ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    add_body_p(
        doc,
        "Практична частина заняття розрахована на **27 хвилин** і складається з трьох послідовних рівнів складності, що моделюють реальну роботу вчителя-дослідника."
    )
    add_scheme_picture(
        doc, scheme_3,
        "Рис. 3. Розподіл часу та змісту практичної частини заняття"
    )

    # --- Рівень 1 ---
    add_sub_heading(doc, "Рівень 1 — репродуктивний (≈ 7 хв)")
    add_body_p(
        doc,
        "**Мета рівня:** навчитися знеособлювати вибірку та кодувати первинні якісні дані карти педагогічного спостереження."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Зміст дії студента", "Очікуваний результат / формат фіксації"],
        rows=[
            [
                "1",
                "Ознайомтеся з фрагментом протоколу спостереження за 6 учнями 2 класу під час роботи в графічному редакторі (індикатори: І1 — правильна посадка; І2 — точне керування мишею; І3 — збереження файлу).",
                "Визначено 3 індикатори та 6 об’єктів спостереження у робочому зошиті або текстовому документі."
            ],
            [
                "2",
                "Виконайте шифрування списку учнів: замініть прізвища та імена на стандартизовані коди від `У-01` до `У-06`.",
                "Сформовано стовпець анонімних шифрів респондентів без розкриття персональних даних."
            ],
            [
                "3",
                "Закодуйте якісні позначки спостереження в числову шкалу: «проявляється стабільно (+)» = `2`, «проявляється епізодично (±)» = `1`, «не проявляється (–)» = `0`.",
                "Кожен індикатор кожного учня подано у вигляді цілого числа (`0`, `1` або `2`)."
            ],
            [
                "4",
                "Підрахуйте індивідуальну суму балів кожного учня (максимум — 6 балів) та зафіксуйте її у зведеній таблиці.",
                "Заповнено числовий протокол спостереження за вибіркою з 6 учнів."
            ]
        ],
        col_widths_cm=[1.5, 8.8, 6.2],
        center_cols=[0]
    )

    # --- Рівень 2 ---
    add_sub_heading(doc, "Рівень 2 — продуктивний (≈ 10 хв)")
    add_body_p(
        doc,
        "**Мета рівня:** формалізувати результати стандартизованого тесту й анкети в табличному процесорі та автоматизувати їхнє статистичне опрацювання."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Зміст дії студента", "Інструмент / формула опрацювання"],
        rows=[
            [
                "1",
                "Створіть у табличному процесорі книгу `Lab12_Прізвище.xlsx` із двома аркушами: `Тестування` та `Анкетування`.",
                "Файл `Lab12_Прізвище.xlsx` зі структурованими шапками таблиць."
            ],
            [
                "2",
                "На аркуші `Тестування` внесіть результати виконання 5 тестових завдань учнями `У-01`…`У-06` (правильна відповідь = `1`, неправильна = `0`).",
                "Матриця розміром 6 рядків × 5 стовпців завдань (`B2:F7`)."
            ],
            [
                "3",
                "Обчисліть для кожного учня загальний бал, відсоток успішності та середній бал по класу.",
                "Формули `=SUM(B2:F2)`, `=G2/5*100`, `=AVERAGE(G2:G7)`."
            ],
            [
                "4",
                "На аркуші `Анкетування` закодуйте відповіді на запитання «Чи подобається тобі складати алгоритми?» (Так = `3`, Важко сказати = `2`, Ні = `1`) та підрахуйте кількість кожного варіанту.",
                "Функція `=COUNTIF(B2:B7; 3)` (аналогічно для значень `2` та `1`)."
            ],
            [
                "5",
                "Співвіднесіть відсоток успішності тесту з рівнями сформованості: низький (менше 40 %), середній (40–69 %), достатній (70–89 %), високий (90–100 %).",
                "Автоматичне або критеріальне визначення рівня для кожного шифру."
            ]
        ],
        col_widths_cm=[1.5, 8.8, 6.2],
        center_cols=[0]
    )

    # --- Рівень 3 ---
    add_sub_heading(doc, "Рівень 3 — творчий (≈ 10 хв)")
    add_body_p(
        doc,
        "**Мета рівня:** розробити власний валідний діагностичний мініінструментарій для уроку інформатики в початковій школі та ключ його формалізації."
    )
    add_body_p(
        doc,
        "**Завдання:** оберіть одну з тем курсу «Я досліджую світ» (інформатична освітня галузь) для 3 класу — *«Безпечна поведінка в інтернеті»* або *«Алгоритми з розгалуженням у середовищі Scratch»*. Спроєктуйте комплект із трьох взаємопов’язаних елементів та зафіксуйте його у вигляді таблиці-паспорта інструментарію:"
    )
    add_bullet_item(
        doc,
        "**3 індикатори спостереження** за практичною роботою учня за комп’ютером із трирівневою шкалою оцінювання (`0`, `1`, `2` бали)."
    )
    add_bullet_item(
        doc,
        "**3 тестові запитання** з вибором однієї правильної відповіді з трьох варіантів (адаптовані за лексикою до віку 8–9 років) із зазначенням ключа правильних відповідей."
    )
    add_bullet_item(
        doc,
        "**2 анкетні запитання** для виявлення самооцінки та емоційного ставлення учня до теми із зазначенням правил кодування відповідей у числа."
    )

    add_styled_table(
        doc,
        headers=["Компонент інструментарію", "Зміст завдання / індикатора", "Правило кодування та макс. бал"],
        rows=[
            [
                "Спостереження (3 індикатори)",
                "Навести 3 конкретні дії учня, які можна візуально зафіксувати на уроці.",
                "0 — не виконує; 1 — з підказкою; 2 — самостійно (макс. 6 балів)."
            ],
            [
                "Тестування (3 завдання)",
                "Сформулювати 3 короткі запитання + 3 варіанти відповіді до кожного + ключ.",
                "0 — помилка; 1 — правильна відповідь за ключем (макс. 3 бали)."
            ],
            [
                "Анкетування (2 запитання)",
                "Сформулювати 2 закриті запитання зі шкалою оцінювання для 3 класу.",
                "Числовий код варіанту відповіді (наприклад, 1–3 бали; макс. 6 балів)."
            ]
        ],
        col_widths_cm=[4.5, 6.8, 5.2],
        center_cols=[]
    )

    # --------------------------------------------------------------------------
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Критерії оцінювання")
    add_styled_table(
        doc,
        headers=["Рівень / показник оцінювання", "Критерії зарахування балів", "Макс. бал"],
        rows=[
            [
                "Рівень 1 (репродуктивний)",
                "Коректно виконано знеособлення вибірки (шифри У-01…У-06), безпомилково закодовано всі індикатори протоколу спостереження та обчислено суми.",
                "3"
            ],
            [
                "Рівень 2 (продуктивний)",
                "Правильно сформовано зведені матриці в табличному процесорі, застосовано формули `SUM`, `AVERAGE`, `COUNTIF`, коректно визначено рівні сформованості.",
                "4"
            ],
            [
                "Рівень 3 (творчий)",
                "Розроблений інструментарій відповідає віковим особливостям учнів 3 класу, містить чіткі індикатори, валідні тестові завдання з ключами та шкалу кодування анкети.",
                "4"
            ],
            [
                "Культура оформлення та етичність",
                "Дотримано вимог до оформлення звіту, таблиць і діаграм; забезпечено анонімність даних; сформульовано аргументований висновок.",
                "2"
            ],
            [
                "Разом за практичне заняття",
                "Сумарна оцінка за виконання всіх етапів роботи",
                "13"
            ]
        ],
        col_widths_cm=[4.5, 9.5, 2.5],
        center_cols=[2]
    )

    # --------------------------------------------------------------------------
    # ФОРМА ЗВІТНОСТІ
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Форма звітності")
    add_body_p(
        doc,
        "Після завершення практичного заняття студент подає викладачеві у паперовому або електронному вигляді комплект матеріалів:"
    )
    add_numbered_item(
        doc,
        "**Звіт про виконання практичного заняття № 12** у форматі `.docx` або запис у робочому зошиті, що містить: тему й мету роботи, закодовану таблицю спостереження (Рівень 1), таблицю-паспорт власного діагностичного інструментарію (Рівень 3) та загальний висновок (3–5 речень) про значення формалізації даних у роботі вчителя інформатики."
    )
    add_numbered_item(
        doc,
        "**Файл електронної таблиці** `Lab12_Прізвище.xlsx` (або посилання на Google Таблицю з правами перегляду), що містить заповнені й обраховані формулами аркуші `Тестування` та `Анкетування` (Рівень 2)."
    )

    output_docx = "Практичне_заняття_12_Спостереження_тестування_анкетування.docx"
    doc.save(output_docx)
    print(f"Документ успішно створено: {output_docx}")
    print(f"Схеми (PNG та SVG) збережено у директорії: {OUTPUT_DIR}/")


if __name__ == "__main__":
    build_document()