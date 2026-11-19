import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ==============================================================================
# 1. НАЛАШТУВАННЯ ПАЛІТРИ ТА ШРИФТІВ ДЛЯ СХЕМ (APPLE-ПОДІБНИЙ СТИЛЬ)
# ==============================================================================
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

COLORS = {
    "bg_card": "#F5F5F7",
    "border": "#E5E5EA",
    "text_dark": "#1D1D1F",
    "text_muted": "#86868B",
    "blue": "#0071E3",
    "green": "#248A3D",
    "orange": "#C93400",
    "red": "#C4001D",
    "purple": "#6E30A8",
    "white": "#FFFFFF",
}

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_figure(fig, name: str) -> str:
    png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    svg_path = os.path.join(OUTPUT_DIR, f"{name}.svg")
    fig.savefig(png_path, dpi=220, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return png_path


def draw_card(ax, x, y, w, h, title, lines, accent_color, badge=None, title_size=13.0, body_size=11.0):
    card = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        facecolor=COLORS["bg_card"],
        edgecolor=COLORS["border"],
        linewidth=1.4,
        zorder=2,
    )
    ax.add_patch(card)

    # Кольорова верхня акцентна смужка
    bar_h = 0.14
    accent_bar = FancyBboxPatch(
        (x + 0.18, y + h - bar_h - 0.14), w - 0.36, bar_h,
        boxstyle="round,pad=0.01,rounding_size=0.07",
        facecolor=accent_color,
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(accent_bar)

    cur_y = y + h - 0.48
    if badge:
        ax.text(
            x + 0.22, cur_y, badge,
            fontsize=10.5, fontweight="bold", color=accent_color,
            va="top", ha="left", zorder=4
        )
        cur_y -= 0.34

    ax.text(
        x + 0.22, cur_y, title,
        fontsize=title_size, fontweight="bold", color=COLORS["text_dark"],
        va="top", ha="left", zorder=4
    )
    cur_y -= 0.42

    for line in lines:
        ax.text(
            x + 0.22, cur_y, line,
            fontsize=body_size, color=COLORS["text_muted"] if line.startswith("Приклад:") else COLORS["text_dark"],
            va="top", ha="left", zorder=4
        )
        cur_y -= 0.33


def generate_all_diagrams() -> dict:
    paths = {}

    # --------------------------------------------------------------------------
    # СХЕМА 1. Вибір типу діаграми за завданням дослідження
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12.4, 5.8))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 5.8)
    ax.axis("off")

    ax.text(
        6.2, 5.45, "Вибір типу діаграми відповідно до мети аналізу даних",
        fontsize=14.5, fontweight="bold", color=COLORS["text_dark"], ha="center", va="center"
    )

    cards_1 = [
        (
            0.25, 2.85, 5.75, 2.20,
            "Стовпчаста гістограма (Порівняння)",
            [
                "• Порівняння показників груп або класів",
                "• Відображення частот рівнів навченості",
                "Приклад: результати 3-А та 3-Б класів"
            ],
            COLORS["blue"], "ПОРІВНЯННЯ"
        ),
        (
            6.40, 2.85, 5.75, 2.20,
            "Лінійний графік (Динаміка змін)",
            [
                "• Відстеження змін у часі чи за етапами",
                "• Візуалізація прогресу формувального етапу",
                "Приклад: темп виконання тестів за 4 тижні"
            ],
            COLORS["green"], "ДИНАМІКА"
        ),
        (
            0.25, 0.30, 5.75, 2.20,
            "Секторна діаграма (Структура цілого)",
            [
                "• Частки складових у межах 100 % вибірки",
                "• Оптимальна кількість секторів: від 2 до 5",
                "Приклад: частка учнів із високим рівнем ІКТ"
            ],
            COLORS["orange"], "СТРУКТУРА"
        ),
        (
            6.40, 0.30, 5.75, 2.20,
            "Точкова діаграма (Зв'язок ознак)",
            [
                "• Пошук залежності між двома змінними",
                "• Виявлення аномальних значень (викидів)",
                "Приклад: час за тренажером і бал за тест"
            ],
            COLORS["purple"], "КОРЕЛЯЦІЯ"
        ),
    ]

    for x, y, w, h, title, lines, col, badge in cards_1:
        draw_card(ax, x, y, w, h, title, lines, col, badge=badge, title_size=12.8, body_size=11.0)

    paths["fig1"] = save_figure(fig, "fig1_chart_types")

    # --------------------------------------------------------------------------
    # СХЕМА 2. Обов'язкові елементи наукової діаграми у звіті
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12.4, 4.3))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 4.3)
    ax.axis("off")

    ax.text(
        6.2, 3.92, "Обов'язкові структурні елементи наукової діаграми",
        fontsize=14.5, fontweight="bold", color=COLORS["text_dark"], ha="center", va="center"
    )

    steps_2 = [
        ("1. Назва та номер", ["Підпис під рисунком:", "Рис. 1. Розподіл учнів...", "Без повтору в полі графіка"], COLORS["blue"]),
        ("2. Осі та шкала", ["Підписи осей X та Y", "Одиниці виміру (%, бали)", "Початок осі Y з нуля"], COLORS["green"]),
        ("3. Ряди та легенда", ["Чіткий контраст кольорів", "Легенда для 2+ рядів", "Підписи значень даних"], COLORS["orange"]),
        ("4. Посилання в тексті", ["Згадка у тексті звіту", "Аналітичний висновок", "Пояснення тенденцій"], COLORS["purple"]),
    ]

    card_w = 2.72
    gap = 0.34
    start_x = 0.25
    for idx, (title, lines, col) in enumerate(steps_2):
        cx = start_x + idx * (card_w + gap)
        draw_card(ax, cx, 0.45, card_w, 2.95, title, lines, col, title_size=12.5, body_size=10.8)
        if idx < len(steps_2) - 1:
            ax.annotate(
                "", xy=(cx + card_w + gap - 0.05, 1.92), xytext=(cx + card_w + 0.05, 1.92),
                arrowprops=dict(arrowstyle="->", color=COLORS["text_muted"], lw=2.0),
                zorder=5
            )

    paths["fig2"] = save_figure(fig, "fig2_chart_elements")

    # --------------------------------------------------------------------------
    # СХЕМА 3. Типові помилки візуалізації та правила їх уникнення
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12.4, 4.5))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    ax.text(
        6.2, 4.12, "Контроль якості графічного матеріалу: уникаємо спотворень",
        fontsize=14.5, fontweight="bold", color=COLORS["text_dark"], ha="center", va="center"
    )

    draw_card(
        ax, 0.30, 0.45, 5.70, 3.15,
        "Неприпустимо у науковому звіті",
        [
            "✕ Об'ємні 3D-діаграми, що викривляють пропорції",
            "✕ Обрізана вісь значень (штучне збільшення різниці)",
            "✕ Понад 6 секторів у круговій діаграмі",
            "✕ Строкаті фони, тіні та кислотні відтінки"
        ],
        COLORS["red"], badge="ПОМИЛКИ ВІЗУАЛІЗАЦІЇ", title_size=13.0, body_size=11.0
    )

    draw_card(
        ax, 6.40, 0.45, 5.70, 3.15,
        "Академічний стандарт оформлення",
        [
            "✓ Плоска (2D) геометрія з точними пропорціями",
            "✓ Нульова базова лінія для порівняння величин",
            "✓ Єдина спокійна колірна гама (2–4 відтінки)",
            "✓ Читабельний шрифт підписів не менше 10–12 pt"
        ],
        COLORS["green"], badge="ПРАВИЛЬНИЙ ПІДХІД", title_size=13.0, body_size=11.0
    )

    paths["fig3"] = save_figure(fig, "fig3_visual_errors")

    # --------------------------------------------------------------------------
    # СХЕМА 4. Трирівнева структура практичної роботи
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12.4, 4.3))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 4.3)
    ax.axis("off")

    ax.text(
        6.2, 3.92, "Алгоритм виконання різнорівневих практичних завдань (27 хв)",
        fontsize=14.5, fontweight="bold", color=COLORS["text_dark"], ha="center", va="center"
    )

    levels = [
        (
            "Рівень 1. Репродуктивний",
            ["Тривалість: ≈ 7 хв", "• Введення вибірки у таблицю", "• Побудова стовпчастої діаграми", "• Оформлення осей і заголовка"],
            COLORS["blue"], "БАЗОВИЙ (до 5 балів)"
        ),
        (
            "Рівень 2. Продуктивний",
            ["Тривалість: ≈ 10 хв", "• Обчислення частот і часток (%)", "• Комбінована діаграма динаміки", "• Порівняння двох груп учнів"],
            COLORS["orange"], "СЕРЕДНІЙ (до 9 балів)"
        ),
        (
            "Рівень 3. Творчий",
            ["Тривалість: ≈ 10 хв", "• Добір оптимальної моделі графіка", "• Візуалізація власного мінідослідження", "• Формулювання наукових висновків"],
            COLORS["green"], "ВИСОКИЙ (до 13 балів)"
        ),
    ]

    lw = 3.72
    lgap = 0.37
    lx0 = 0.25
    for idx, (title, lines, col, badge) in enumerate(levels):
        cx = lx0 + idx * (lw + lgap)
        draw_card(ax, cx, 0.45, lw, 2.95, title, lines, col, badge=badge, title_size=12.8, body_size=11.0)
        if idx < len(levels) - 1:
            ax.annotate(
                "", xy=(cx + lw + lgap - 0.05, 1.92), xytext=(cx + lw + 0.05, 1.92),
                arrowprops=dict(arrowstyle="->", color=COLORS["text_muted"], lw=2.2),
                zorder=5
            )

    paths["fig4"] = save_figure(fig, "fig4_task_levels")

    return paths


# ==============================================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ФОРМАТУВАННЯ DOCX
# ==============================================================================
COLOR_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)    # #1F4E79 темно-синій
COLOR_SECONDARY = RGBColor(0x2E, 0x75, 0xB6)  # #2E75B6 акцентний синій
COLOR_CODE = RGBColor(0xC0, 0x39, 0x2B)       # #C0392B моноширинний червоний
COLOR_TEXT = RGBColor(0x00, 0x00, 0x00)
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def configure_base_styles(doc: Document):
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(14)
    normal.font.color.rgb = COLOR_TEXT
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.space_before = Pt(0)

    for style_name in ["List Bullet", "List Number"]:
        if style_name in doc.styles:
            st = doc.styles[style_name]
            st.font.name = "Times New Roman"
            st._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
            st.font.size = Pt(14)
            st.font.color.rgb = COLOR_TEXT
            st.paragraph_format.line_spacing = 1.15
            st.paragraph_format.space_after = Pt(4)
            st.paragraph_format.left_indent = Cm(1.0)


def add_page_number_footer(doc: Document):
    section = doc.sections[0]
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")

    r = run._r
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)


def add_formatted_runs(p, segments):
    """
    segments: список кортежів (текст, стиль), де стиль у наборі:
    'normal', 'bold', 'italic', 'code'
    """
    for text, kind in segments:
        r = p.add_run(text)
        if kind == "code":
            r.font.name = "Consolas"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
            r.font.size = Pt(12.5)
            r.font.color.rgb = COLOR_CODE
            r.bold = True
        else:
            r.font.name = "Times New Roman"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
            r.font.size = Pt(14)
            r.font.color.rgb = COLOR_TEXT
            if kind == "bold":
                r.bold = True
            elif kind == "italic":
                r.italic = True


def add_body_p(doc: Document, segments, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=5):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    if isinstance(segments, str):
        add_formatted_runs(p, [(segments, "normal")])
    else:
        add_formatted_runs(p, segments)
    return p


def add_heading_1(doc: Document, text: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    return p


def add_heading_2(doc: Document, text: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    return p


def numbered_paren(doc: Document, items: list):
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        add_formatted_runs(p, [(f"{idx}) ", "bold"), (item, "normal")])


def add_bullet_list(doc: Document, items: list):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        if isinstance(item, str):
            add_formatted_runs(p, [(item, "normal")])
        else:
            add_formatted_runs(p, item)


def add_number_list(doc: Document, items: list):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        if isinstance(item, str):
            add_formatted_runs(p, [(item, "normal")])
        else:
            add_formatted_runs(p, item)


def set_cell_shading(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def add_callout(doc: Document, segments, fill_hex="EEF4FB", border_hex="2E75B6"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.0)
    set_cell_shading(cell, fill_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=160)

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in ["top", "right", "bottom"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "none")
        tcBorders.append(el)
    left_el = OxmlElement("w:left")
    left_el.set(qn("w:val"), "single")
    left_el.set(qn("w:sz"), "28")
    left_el.set(qn("w:space"), "0")
    left_el.set(qn("w:color"), border_hex)
    tcBorders.append(left_el)
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(0)
    if isinstance(segments, str):
        add_formatted_runs(p, [(segments, "normal")])
    else:
        add_formatted_runs(p, segments)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)
    spacer.paragraph_format.space_before = Pt(0)


def add_styled_table(doc: Document, headers: list, rows: list, col_widths_cm: list):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Заголовок таблиці
    hdr_row = tbl.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)

    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.width = Cm(col_widths_cm[c_idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, "1F4E79")
        set_cell_margins(cell, top=100, bottom=100, left=110, right=110)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.1
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.bold = True
        r.font.color.rgb = COLOR_WHITE

    # Рядки даних
    for r_idx, row_data in enumerate(rows):
        row = tbl.rows[r_idx + 1]
        r_trPr = row._tr.get_or_add_trPr()
        r_cant = OxmlElement("w:cantSplit")
        r_trPr.append(r_cant)
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"

        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Cm(col_widths_cm[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=85, bottom=85, left=110, right=110)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.12
            p.paragraph_format.space_after = Pt(0)
            if isinstance(val, str):
                add_formatted_runs(p, [(val, "normal")])
            else:
                add_formatted_runs(p, val)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)
    spacer.paragraph_format.space_before = Pt(0)
    return tbl


def add_diagram(doc: Document, img_path: str, caption: str, width_cm: float = 15.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    run = p_img.add_run()
    run.add_picture(img_path, width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(12)
    r_cap.italic = True
    r_cap.font.color.rgb = COLOR_PRIMARY


# ==============================================================================
# 3. ФОРМУВАННЯ ЗМІСТУ ДОКУМЕНТА
# ==============================================================================
def build_document():
    diagrams = generate_all_diagrams()
    doc = Document()
    configure_base_styles(doc)
    add_page_number_footer(doc)

    # --- ЗАГОЛОВОК ТА ТЕМА ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("ПРАКТИЧНЕ ЗАНЯТТЯ № 13")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(14)
    r_title.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_after = Pt(8)
    r_topic = p_topic.add_run("Тема: Графічне представлення даних.")
    r_topic.font.name = "Times New Roman"
    r_topic.font.size = Pt(14)
    r_topic.bold = True
    r_topic.font.color.rgb = COLOR_TEXT

    # --- МЕТА ---
    add_heading_1(doc, "Мета")
    add_body_p(
        doc,
        "Формувати вміння графічно представляти емпіричні дані педагогічного дослідження; "
        "розвивати візуальне мислення та навички обґрунтованого добору графічних форм подання "
        "результатів під час підготовки наукового звіту; виховувати прагнення до наочності, "
        "логічності та точності у представленні результатів роботи майбутнього вчителя інформатики "
        "початкової школи."
    )

    # --- ОБЛАДНАННЯ ---
    add_heading_1(doc, "Обладнання та програмне забезпечення")
    numbered_paren(
        doc,
        [
            "інструкційні картки до практичного заняття;",
            "персональний комп’ютер або ноутбук із встановленим табличним процесором (MS Excel або LibreOffice Calc);",
            "набір емпіричних даних педагогічної діагностики учнів початкової школи (файл або таблиця завдання)."
        ]
    )

    # --- ЛІТЕРАТУРА ---
    add_heading_1(doc, "Література")
    add_number_list(
        doc,
        [
            "Лісневська Н. В., Загородня Л. П., Тітаренко С. А., Данильченко І. Г., Корякіна І. В., Гордій Н. М. Методичні рекомендації до виконання та захисту курсових робіт для здобувачів ОС «Бакалавр» спеціальності 012 «Дошкільна освіта». Глухів : ГНПУ ім. О. Довженка, 2023. 65 с.",
            "Пріма Р. М. Сучасна наукова стаття: технологія творчості. Науковий вісник. 2020. № 4 (408). С. 99–103.",
            "Шейко В. М., Кушнаренко Н. М. Організація та методика науково-дослідницької діяльності : підручник. Київ : Знання, 2018. 310 с."
        ]
    )

    # --- ТЕОРЕТИЧНІ ВІДОМОСТІ ---
    add_heading_1(doc, "Теоретичні відомості")

    add_heading_2(doc, "1. Сутність і роль графічного методу в педагогічному дослідженні")
    add_body_p(
        doc,
        [
            ("Графічне представлення даних — це спосіб наочного відображення кількісних і якісних "
             "показників дослідження за допомогою геометричних образів (стовпчиків, ліній, секторів, точок). "
             "У роботі вчителя інформатики початкової школи діаграми дають змогу швидко оцінити рівень "
             "сформованості алгоритмічного мислення учнів, порівняти успішність контрольного та експериментального "
             "класів і переконливо обґрунтувати ефективність обраної методики у звіті чи курсовій роботі.", "normal")
        ]
    )

    add_heading_2(doc, "2. Класифікація діаграм за характером досліджуваних даних")
    add_body_p(
        doc,
        "Вибір типу діаграми визначається не естетичними вподобаннями автора, а логікою запитання, "
        "на яке відповідає рисунок. Невідповідність типу графіка природі даних ускладнює сприйняття "
        "висновків дослідження."
    )
    add_diagram(
        doc,
        diagrams["fig1"],
        "Рис. 1. Відповідність типів діаграм завданням аналізу педагогічних даних"
    )

    add_styled_table(
        doc,
        ["Тип діаграми", "Аналітичне завдання", "Приклад у початковій школі"],
        [
            [
                [("Стовпчаста (гістограма)", "bold")],
                "Порівняння абсолютних або відносних значень між групами",
                "Порівняння середнього балу учнів 3-А і 3-Б класів за підсумками тесту з безпеки в інтернеті"
            ],
            [
                [("Лінійний графік", "bold")],
                "Відображення динаміки показника у часі чи за етапами експерименту",
                "Зміна швидкості набору тексту молодшими школярами протягом 5 тижнів тренувань"
            ],
            [
                [("Секторна (кругова)", "bold")],
                "Демонстрація частки кожної категорії у загальній сукупності (100 %)",
                "Структура вибірки за рівнями володіння блоковим середовищем Scratch (початковий, середній, достатній, високий)"
            ],
            [
                [("Точкова діаграма", "bold")],
                "Виявлення кореляції (взаємозв’язку) між двома кількісними ознаками",
                "Залежність між часом роботи з інтерактивним тренажером і кількістю правильних відповідей"
            ],
        ],
        [4.2, 6.0, 6.8]
    )

    add_heading_2(doc, "3. Попередня обробка первинних даних у табличному процесорі")
    add_body_p(
        doc,
        [
            ("Перед побудовою діаграми первинні протоколи спостережень чи тестування зводять у таблицю. "
             "Для автоматичного підрахунку показників у табличному процесорі застосовують базові функції: ", "normal"),
            ("=AVERAGE(B2:B26)", "code"),
            (" — обчислення середнього арифметичного вибірки; ", "normal"),
            ("=COUNTIF(C2:C26; \"Високий\")", "code"),
            (" — підрахунок кількості учнів, які досягли певного рівня; ", "normal"),
            ("=F2/$F$6*100", "code"),
            (" — переведення абсолютних частот у відсоткові частки.", "normal")
        ]
    )

    add_heading_2(doc, "4. Вимоги до оформлення діаграм у науковому звіті")
    add_body_p(
        doc,
        "Діаграма у звіті є самостійним носієм інформації, тому читач має зрозуміти її зміст без "
        "додаткових усних пояснень автора. Кожен рисунок обов’язково містить номер, змістовний підпис під ним, "
        "позначення осей, одиниці виміру та легенду."
    )
    add_diagram(
        doc,
        diagrams["fig2"],
        "Рис. 2. Обов’язкові елементи наукової діаграми в академічному звіті"
    )

    add_callout(
        doc,
        [
            ("У наукових звітах і статтях не дублюйте заголовок діаграми всередині її графічної області, "
             "якщо під рисунком уже розміщено підпис формату ", "normal"),
            ("Рис. 1. Розподіл учнів 4-х класів за рівнями цифрової грамотності", "code"),
            (". У тексті звіту перед рисунком або одразу після нього обов’язково наводьте посилання ", "normal"),
            ("(рис. 1)", "code"),
            (" та стислий аналітичний коментар виявлених закономірностей.", "normal")
        ]
    )

    add_heading_2(doc, "5. Типові помилки візуалізації та контроль точності")
    add_body_p(
        doc,
        "Надмірне декоративне оформлення (об’ємні фігури, тіні, градієнти) або неправильно обраний масштаб "
        "осі здатні викривити реальну картину педагогічного експерименту й знизити довіру до результатів."
    )
    add_diagram(
        doc,
        diagrams["fig3"],
        "Рис. 3. Порівняння некоректних прийомів візуалізації та академічного стандарту"
    )

    # --- ПОКРОКОВИЙ АЛГОРИТМ ВИКОНАННЯ ЗАВДАНЬ ---
    add_heading_1(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    add_body_p(
        doc,
        "Практична частина заняття розрахована на 27 хвилин і складається з трьох послідовних рівнів "
        "складності. Виконання кожного наступного рівня підвищує підсумковий бал за заняття."
    )
    add_diagram(
        doc,
        diagrams["fig4"],
        "Рис. 4. Структура та часовий регламент різнорівневої практичної роботи"
    )

    # Рівень 1
    add_heading_2(doc, "Рівень 1 — репродуктивний (орієнтовний час: 7 хв)")
    add_body_p(
        doc,
        [
            ("Завдання: ", "bold"),
            ("створіть у табличному процесорі аркуш ", "normal"),
            ("Рівень_1", "code"),
            (", внесіть зведені результати діагностики навичок роботи з графічним редактором в учнів 2-А класу "
             "(високий рівень — 6 учнів, достатній — 11 учнів, середній — 7 учнів, початковий — 2 учні) та побудуйте "
             "стовпчасту діаграму.", "normal")
        ]
    )
    add_styled_table(
        doc,
        ["Крок", "Зміст дії", "Інструмент / команда"],
        [
            [
                "1",
                "Створити таблицю з двома стовпцями: «Рівень досягнень» та «Кількість учнів (осіб)»",
                [("Діапазон ", "normal"), ("A1:B5", "code")]
            ],
            [
                "2",
                "Виділити діапазон даних разом із заголовками стовпців і вставити плоску стовпчасту діаграму",
                [("Вставка → Діаграми → Гістограма 2D", "code")]
            ],
            [
                "3",
                "Додати підписи даних над стовпчиками та вказати одиниці виміру на вертикальній осі",
                [("Елементи діаграми → Підписи даних", "code")]
            ],
            [
                "4",
                "Прибрати декоративні ефекти, перевірити старт осі Y з нуля та зберегти діаграму",
                [("Формат осі → Мінімум: 0.0", "code")]
            ],
        ],
        [1.8, 9.2, 6.0]
    )

    # Рівень 2
    add_heading_2(doc, "Рівень 2 — продуктивний (орієнтовний час: 10 хв)")
    add_body_p(
        doc,
        [
            ("Завдання: ", "bold"),
            ("на аркуші ", "normal"),
            ("Рівень_2", "code"),
            (" проведіть порівняльний аналіз результатів експериментального (3-А, 25 учнів) та контрольного "
             "(3-Б, 24 учні) класів після впровадження ігрових вправ з алгоритмізації. Переведіть абсолютні "
             "показники у відсотки та побудуйте порівняльну діаграму з двома рядами даних.", "normal")
        ]
    )
    add_styled_table(
        doc,
        ["Крок", "Зміст дії", "Інструмент / команда"],
        [
            [
                "1",
                "Ввести дані для 3-А (високий — 9, достатній — 10, середній — 5, початковий — 1) та 3-Б (високий — 4, достатній — 9, середній — 8, початковий — 3)",
                [("Діапазон ", "normal"), ("A1:C5", "code")]
            ],
            [
                "2",
                "У сусідніх стовпцях розрахувати відсоткову частку кожного рівня для обох класів",
                [("=B2/SUM($B$2:$B$5)*100", "code")]
            ],
            [
                "3",
                "Побудувати групову стовпчасту діаграму за відсотковими показниками двох класів",
                [("Гістограма з групуванням", "code")]
            ],
            [
                "4",
                "Налаштувати контрастну двоколірну палітру, легенду внизу та підписи значень із точністю до 1 знака",
                [("Формат підписів → Число: 0,0%", "code")]
            ],
        ],
        [1.8, 9.2, 6.0]
    )

    # Рівень 3
    add_heading_2(doc, "Рівень 3 — творчий (орієнтовний час: 10 хв)")
    add_body_p(
        doc,
        [
            ("Завдання: ", "bold"),
            ("на аркуші ", "normal"),
            ("Рівень_3", "code"),
            (" змоделюйте результати власного мінідослідження з методики навчання інформатики в початковій школі "
             "(наприклад, динаміка успішності за 4 контрольні зрізи або зв’язок між кількістю виконаних інтерактивних "
             "вправ і підсумковою оцінкою). Самостійно оберіть оптимальний тип діаграми, оформте її за науковими "
             "вимогами та напишіть аналітичний висновок обсягом 4–5 речень для розділу звіту.", "normal")
        ]
    )
    add_styled_table(
        doc,
        ["Етап", "Вимоги до виконання творчого завдання", "Результат у файлі та звіті"],
        [
            [
                "1",
                "Сформулювати тему мінідослідження та згенерувати коректний масив даних (не менше 8–10 значень або 4 часових етапів)",
                "Таблиця вихідних даних із підписами одиниць виміру"
            ],
            [
                "2",
                "Обґрунтувати вибір типу діаграми (лінійний графік або точкова діаграма з лінією тренду)",
                "Акуратна 2D-діаграма без візуального шуму"
            ],
            [
                "3",
                "Експортувати діаграму у звіт, оформити підпис рисунка та сформулювати науковий висновок",
                "Фрагмент тексту звіту з посиланням на рисунок"
            ],
        ],
        [1.8, 9.4, 5.8]
    )

    # --- КРИТЕРІЇ ОЦІНЮВАННЯ ---
    add_heading_1(doc, "Критерії оцінювання")
    add_styled_table(
        doc,
        ["Рівень / компонент роботи", "Показники якості виконання", "Макс. бал"],
        [
            [
                "Рівень 1 (репродуктивний)",
                "Правильно внесено дані, побудовано плоску стовпчасту діаграму, коректно відображено осі та підписи значень",
                "4 бали"
            ],
            [
                "Рівень 2 (продуктивний)",
                "Безпомилково обчислено відсоткові частки за допомогою формул, побудовано групову діаграму порівняння двох класів, налаштовано легенду",
                "4 бали"
            ],
            [
                "Рівень 3 (творчий)",
                "Доцільно обрано тип діаграми відповідно до педагогічної задачі, відсутні візуальні спотворення, сформульовано логічний аналітичний висновок",
                "3 бали"
            ],
            [
                "Оформлення звіту",
                "Дотримано вимог до оформлення рисунків, підписів, посилань у тексті та охайності подання матеріалів",
                "2 бали"
            ],
            [
                [("Разом", "bold")],
                [("Максимальна сума балів за практичне заняття", "bold")],
                [("13 балів", "bold")]
            ],
        ],
        [4.5, 9.7, 2.8]
    )

    # --- ФОРМА ЗВІТНОСТІ ---
    add_heading_1(doc, "Форма звітності")
    add_body_p(
        doc,
        "За результатами заняття студент подає викладачеві два файли:"
    )
    add_bullet_list(
        doc,
        [
            [
                ("файл електронної таблиці ", "normal"),
                ("Prizvyshche_PZ13.xlsx", "code"),
                (" (або ", "normal"),
                (".ods", "code"),
                ("), що містить три окремі аркуші (", "normal"),
                ("Рівень_1", "code"),
                (", ", "normal"),
                ("Рівень_2", "code"),
                (", ", "normal"),
                ("Рівень_3", "code"),
                (") зі збереженими формулами та побудованими діаграмами;", "normal")
            ],
            [
                ("текстовий звіт ", "normal"),
                ("Prizvyshche_Zvit_PZ13.docx", "code"),
                (", оформлений за вимогами академічної доброчесності (шрифт Times New Roman, кегль 14 pt, "
                 "міжрядковий інтервал 1,15), який містить мету роботи, вставлені зображення всіх трьох діаграм "
                 "із належними підписами під кожним рисунком, текстові посилання на них та підсумковий висновок "
                 "щодо доцільності різних способів графічного представлення даних у педагогічному дослідженні.", "normal")
            ]
        ]
    )

    output_docx = "Praktychne_13_Grafichne_predstavlennia_danykh.docx"
    doc.save(output_docx)
    print(f"Документ успішно створено: {output_docx}")
    print(f"Схеми (PNG та SVG) збережено у папці: {OUTPUT_DIR}/")


if __name__ == "__main__":
    build_document()