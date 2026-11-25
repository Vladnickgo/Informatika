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

# ==============================================================================
# 1. ГЕНЕРАЦІЯ СХЕМ (PNG + SVG У СТИЛІ APPLE)
# ==============================================================================
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

os.makedirs("output", exist_ok=True)

BG_CARD = "#F5F5F7"
BORDER_CARD = "#E5E5EA"
TEXT_DARK = "#1D1D1F"
TEXT_GRAY = "#86868B"
BLUE = "#0071E3"
GREEN = "#248A3D"
ORANGE = "#C93400"
RED = "#C4001D"
PURPLE = "#6E30A8"


def draw_card(ax, x, y, w, h, title, desc, accent_color=BLUE, title_size=13, desc_size=11):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        facecolor=BG_CARD, edgecolor=BORDER_CARD, linewidth=1.5
    )
    ax.add_patch(box)
    # Акцентна верхня смужка або індикатор
    badge = FancyBboxPatch(
        (x + 0.18, y + h - 0.16), w - 0.36, 0.06,
        boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor=accent_color, edgecolor="none"
    )
    ax.add_patch(badge)

    ax.text(
        x + w / 2, y + h - 0.45, title,
        fontsize=title_size, fontweight="bold", color=accent_color,
        ha="center", va="center"
    )
    ax.text(
        x + w / 2, y + (h - 0.55) / 2, desc,
        fontsize=desc_size, color=TEXT_DARK,
        ha="center", va="center", linespacing=1.35
    )


def save_figure(fig, name):
    png_path = os.path.join("output", f"{name}.png")
    svg_path = os.path.join("output", f"{name}.svg")
    fig.savefig(png_path, dpi=220, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return png_path


def make_schema_1_structure():
    """Схема 1: Базова структура HTML-документа"""
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    ax.text(5.5, 4.85, "Анатомія HTML-сторінки (принцип матрьошки)",
            fontsize=15, fontweight="bold", color=TEXT_DARK, ha="center", va="center")

    # Зовнішній контейнер <html>
    outer = FancyBboxPatch(
        (0.4, 0.3), 10.2, 4.1,
        boxstyle="round,pad=0.02,rounding_size=0.22",
        facecolor="#FFFFFF", edgecolor=BLUE, linewidth=2.0
    )
    ax.add_patch(outer)
    ax.text(0.7, 4.12, "<html> ... </html>  — кореневий контейнер усієї вебсторінки",
            fontsize=12.5, fontweight="bold", color=BLUE, ha="left", va="center")

    # Ліва картка <head>
    draw_card(
        ax, 0.75, 0.65, 4.5, 3.1,
        "<head> ... </head>",
        "Службова інформація («паспорт»):\n"
        "• <meta charset=\"UTF-8\"> — кирилиця\n"
        "• <title>Назва</title> — текст на вкладці\n"
        "• Підключення стилів та іконок\n"
        "(не відображається у вікні сторінки)",
        accent_color=PURPLE, title_size=13.5, desc_size=11
    )

    # Права картка <body>
    draw_card(
        ax, 5.75, 0.65, 4.5, 3.1,
        "<body> ... </body>",
        "Видима частина («вітрина» сайту):\n"
        "• Заголовки <h1>–<h6> та абзаци <p>\n"
        "• Зображення <img> та таблиці <table>\n"
        "• Гіперпосилання <a>\n"
        "• Відео <video> та аудіо <audio>",
        accent_color=GREEN, title_size=13.5, desc_size=11
    )

    return save_figure(fig, "schema_1_html_structure")


def make_schema_2_tag_syntax():
    """Схема 2: Синтаксис парного тегу з атрибутами"""
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    ax.text(5.5, 3.85, "Будова HTML-тегу та його атрибутів",
            fontsize=15, fontweight="bold", color=TEXT_DARK, ha="center", va="center")

    # Темний блок коду (термінал-стиль)
    code_box = FancyBboxPatch(
        (0.6, 2.35), 9.8, 0.95,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        facecolor="#1C1C1E", edgecolor="#3A3A3C", linewidth=1.5
    )
    ax.add_patch(code_box)

    ax.text(1.75, 2.82, "<a", fontsize=14, fontweight="bold", color="#30D158", ha="center", va="center", family="monospace")
    ax.text(4.35, 2.82, "href=\"https://mon.gov.ua\"", fontsize=13.5, fontweight="bold", color="#64D2FF", ha="center", va="center", family="monospace")
    ax.text(6.35, 2.82, ">", fontsize=14, fontweight="bold", color="#30D158", ha="center", va="center", family="monospace")
    ax.text(7.65, 2.82, "Сайт МОН", fontsize=13.5, fontweight="bold", color="#FFFFFF", ha="center", va="center", family="monospace")
    ax.text(9.35, 2.82, "</a>", fontsize=14, fontweight="bold", color="#FF453A", ha="center", va="center", family="monospace")

    # Пояснювальні картки знизу
    draw_card(ax, 0.5, 0.35, 2.3, 1.55, "Відкриваючий тег", "Вказує браузеру,\nякий елемент\nпочинається", BLUE, 12, 10.5)
    draw_card(ax, 3.05, 0.35, 2.6, 1.55, "Атрибут = \"значення\"", "Уточнює властивість\nтегу (завжди у\nподвійних лапках)", ORANGE, 12, 10.5)
    draw_card(ax, 5.9, 0.35, 2.3, 1.55, "Вміст елемента", "Текст або інший\nтег, що бачить\nкористувач", GREEN, 12, 10.5)
    draw_card(ax, 8.45, 0.35, 2.1, 1.55, "Закриваючий тег", "Обов'язкова коса\nриска / перед\nіменем тегу", RED, 12, 10.5)

    # Стрілки
    for x_pos in [1.65, 4.35, 7.05, 9.45]:
        ax.annotate("", xy=(x_pos, 2.3), xytext=(x_pos, 1.95),
                    arrowprops=dict(arrowstyle="->", color=TEXT_GRAY, lw=1.6))

    return save_figure(fig, "schema_2_tag_syntax")


def make_schema_3_media_formats():
    """Схема 3: Графіка та мультимедіа у веб-розробці"""
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    ax.text(5.5, 4.25, "Вибір форматів графіки та мультимедіа для освітнього сайту",
            fontsize=15, fontweight="bold", color=TEXT_DARK, ha="center", va="center")

    draw_card(
        ax, 0.4, 0.4, 3.2, 3.35,
        "Растрова графіка",
        "JPG / JPEG — фотографії\nкласу, подій, портрети.\n\n"
        "PNG — скріншоти, кнопки,\nкартинки з прозорим фоном.\n\n"
        "WebP — сучасний легкий\nформат для швидкого\nзавантаження.",
        accent_color=BLUE, title_size=13, desc_size=10.8
    )

    draw_card(
        ax, 3.9, 0.4, 3.2, 3.35,
        "Векторна графіка",
        "SVG — логотипи школи,\nіконки, математичні фігури.\n\n"
        "Переваги:\n"
        "• Не втрачає чіткості\nпри будь-якому масштабі;\n"
        "• Має мінімальний розмір\nфайлу.",
        accent_color=PURPLE, title_size=13, desc_size=10.8
    )

    draw_card(
        ax, 7.4, 0.4, 3.2, 3.35,
        "Аудіо та відео",
        "MP3 / OGG (<audio>) —\nаудіоказки, диктанти,\nфонова музика.\n\n"
        "MP4 / WebM (<video>) —\nнавчальні відеоуроки.\n\n"
        "Обов'язковий атрибут:\ncontrols (панель керування).",
        accent_color=ORANGE, title_size=13, desc_size=10.8
    )

    return save_figure(fig, "schema_3_media_formats")


def make_schema_4_workflow():
    """Схема 4: Етапи виконання самостійної роботи (Flow)"""
    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.8)
    ax.axis("off")

    ax.text(5.5, 3.45, "Алгоритм виконання самостійної роботи",
            fontsize=15, fontweight="bold", color=TEXT_DARK, ha="center", va="center")

    steps = [
        ("1. Організація", "Створити папку\nпроєкту та\nпідпапку media/", BLUE),
        ("2. Каркас", "Описати теги\n<html>, <head>,\n<body>, UTF-8", PURPLE),
        ("3. Контент", "Додати текст,\nсписки, таблицю\nта посилання", GREEN),
        ("4. Медіа", "Вставити фото\n<img>, аудіо та\nвідеоролик", ORANGE),
        ("5. Перевірка", "Відкрити у\nбраузері, знайти\nй усунути баги", RED),
    ]

    w = 1.85
    gap = 0.28
    start_x = 0.32
    for i, (t, d, col) in enumerate(steps):
        x = start_x + i * (w + gap)
        draw_card(ax, x, 0.45, w, 2.45, t, d, accent_color=col, title_size=12, desc_size=10.5)
        if i < len(steps) - 1:
            ax.annotate(
                "", xy=(x + w + gap - 0.03, 1.65), xytext=(x + w + 0.03, 1.65),
                arrowprops=dict(arrowstyle="->", color=TEXT_GRAY, lw=2.0)
            )

    return save_figure(fig, "schema_4_workflow")


img_1 = make_schema_1_structure()
img_2 = make_schema_2_tag_syntax()
img_3 = make_schema_3_media_formats()
img_4 = make_schema_4_workflow()

# ==============================================================================
# 2. НАЛАШТУВАННЯ ДОКУМЕНТА DOCX
# ==============================================================================
doc = Document()

# Поля сторінки (стандартні 2 см з усіх боків)
for section in doc.sections:
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

# Базовий стиль Normal
style_normal = doc.styles["Normal"]
style_normal.font.name = "Times New Roman"
style_normal.font.size = Pt(14)
style_normal.font.color.rgb = RGBColor(0x1D, 0x1D, 0x1F)
style_normal.paragraph_format.line_spacing = 1.15
style_normal.paragraph_format.space_after = Pt(5)
style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# Стилі списків
for list_style_name in ["List Bullet", "List Number"]:
    st = doc.styles[list_style_name]
    st.font.name = "Times New Roman"
    st.font.size = Pt(14)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.left_indent = Cm(1.0)

COLOR_H1 = RGBColor(0x1F, 0x4E, 0x79)
COLOR_H2 = RGBColor(0x2E, 0x75, 0xB6)
COLOR_CODE = RGBColor(0xC0, 0x39, 0x2B)
COLOR_DARK = RGBColor(0x1D, 0x1D, 0x1F)


def add_page_number_footer(section):
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


add_page_number_footer(doc.sections[0])


def add_main_title(title_text, theme_text):
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run(title_text.upper())
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_H1

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_after = Pt(10)
    r2 = p2.add_run(f"Тема: {theme_text}")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_DARK


def add_section_header(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_H1
    return p


def add_sub_header(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_H2
    return p


def add_rich_paragraph(segments, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=5, left_indent=None):
    """
    segments: список кортежів (текст, стиль), де стиль може бути:
    'normal', 'bold', 'italic', 'code'
    """
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(space_after)
    if left_indent is not None:
        p.paragraph_format.left_indent = Cm(left_indent)
    for text, kind in segments:
        r = p.add_run(text)
        if kind == "code":
            r.font.name = "Consolas"
            r.font.size = Pt(12.5)
            r.font.color.rgb = COLOR_CODE
        else:
            r.font.name = "Times New Roman"
            r.font.size = Pt(14)
            r.font.color.rgb = COLOR_DARK
            if kind == "bold":
                r.font.bold = True
            elif kind == "italic":
                r.font.italic = True
    return p


def numbered_paren(items):
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.space_after = Pt(3)
        r_num = p.add_run(f"{idx}) ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(14)
        r_num.font.bold = True
        r_txt = p.add_run(item)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(14)


def add_callout(segments, bg_hex="EDF4FB", border_hex="1F4E79"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.0)

    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), bg_hex)
    tcPr.append(shd)

    tcBorders = OxmlElement("w:tcBorders")
    for side in ["top", "right", "bottom"]:
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

    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", "120"), ("bottom", "120"), ("left", "180"), ("right", "150")]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), val)
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(0)
    for text, kind in segments:
        r = p.add_run(text)
        if kind == "code":
            r.font.name = "Consolas"
            r.font.size = Pt(12.5)
            r.font.color.rgb = COLOR_CODE
        else:
            r.font.name = "Times New Roman"
            r.font.size = Pt(14)
            r.font.color.rgb = COLOR_DARK
            if kind == "bold":
                r.font.bold = True

    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(4)


def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)


def add_styled_table(headers, rows_data, col_widths):
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Заголовок таблиці
    hdr_row = tbl.rows[0]
    set_repeat_table_header(hdr_row)
    for idx, text in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.width = Cm(col_widths[idx])
        set_cell_shading(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Рядки даних
    for r_idx, row_items in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        for c_idx, cell_content in enumerate(row_items):
            cell = row.cells[c_idx]
            cell.width = Cm(col_widths[c_idx])
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            # cell_content може бути рядком або списком сегментів (текст, тип)
            if isinstance(cell_content, str):
                r = p.add_run(cell_content)
                r.font.name = "Times New Roman"
                r.font.size = Pt(13)
                r.font.color.rgb = COLOR_DARK
            else:
                for txt, kind in cell_content:
                    r = p.add_run(txt)
                    if kind == "code":
                        r.font.name = "Consolas"
                        r.font.size = Pt(12)
                        r.font.color.rgb = COLOR_CODE
                    else:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(13)
                        r.font.color.rgb = COLOR_DARK
                        if kind == "bold":
                            r.font.bold = True

    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(4)
    return tbl


def add_schema_image(img_path, caption_text):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Cm(16.0))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(12)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


# ==============================================================================
# 3. НАПОВНЕННЯ ЗМІСТУ САМОСТІЙНОЇ РОБОТИ № 15
# ==============================================================================
add_main_title(
    "САМОСТІЙНА РОБОТА № 15",
    "Основні теги і атрибути. Встановлення параметрів сторінки сайту, введення й форматування елементів сторінки: тексту, гіперпосилань, зображень. Графіка та мультимедійна інформація."
)

# Мета
add_rich_paragraph([
    ("Мета: ", "bold"),
    ("навчитися використовувати основні теги мови розмітки HTML (", "normal"),
    ("<html>, <head>, <body>, <h1>, <p>, <a>, <img>, <table>, <audio>, <video>", "code"),
    ("), налаштовувати параметри вебсторінки, вставляти графіку, гіперпосилання та мультимедіа; розвивати дрібну моторику під час набору коду, уважність до синтаксису та візуальне мислення; виховувати терпіння, акуратність і прагнення до семантичної коректності коду в контексті майбутньої педагогічної діяльності.", "normal")
])

# Обладнання
add_section_header("Обладнання та програмне забезпечення")
numbered_paren([
    "Персональний комп’ютер або ноутбук із доступом до мережі Інтернет.",
    "Текстовий редактор із підсвічуванням синтаксису (Notepad++, Visual Studio Code або стандартний Блокнот).",
    "Сучасний веббраузер (Google Chrome, Mozilla Firefox або Microsoft Edge).",
    "Інструкційні картки та набір навчальних медіафайлів (зображення, аудіо- та відеофрагменти для початкової школи)."
])

# Література
add_section_header("Література")
lit_items = [
    "Буйницька О. П. Інформаційні технології та технічні засоби навчання : навч. посіб. Київ : Центр навчальної літератури, 2019. 240 с.",
    "Буров Є. В. Комп’ютерні мережі. Львів : Магнолія 2006, 2024. 256 с.",
    "Мирошниченко В. О. Використання сучасних інформаційних технологій: формування мультимедійної компетентності. Київ : Центр учбової літератури, 2022. 296 с."
]
for item in lit_items:
    p = doc.add_paragraph(style="List Number")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(item)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

# Завдання самостійної роботи
add_section_header("Завдання самостійної роботи")
tasks_sr = [
    "Опрацювати теоретичні відомості щодо базової структури HTML-документа, синтаксису парних і одинарних тегів, а також правил запису атрибутів.",
    "Дослідити способи встановлення параметрів вебсторінки (кодування символів, заголовок вкладки браузера, фонове оформлення).",
    "Систематизувати основні формати растрової, векторної графіки та мультимедійних файлів, придатних для створення освітніх вебресурсів для учнів 1–4 класів.",
    "Виконати практичне завдання згідно з інструкційною карткою: створити тематичну освітню вебсторінку «Інформатика для молодших школярів» (або «Візитівка нашого класу») із використанням заголовків, форматованого тексту, списків, таблиці, гіперпосилань, зображень та медіаплеєрів.",
    "Заповнити узагальнюючу таблицю основних HTML-тегів та їхніх атрибутів.",
    "Підготувати відповіді на теоретичні питання для самоперевірки та оформити звіт про виконання роботи."
]
for t in tasks_sr:
    p = doc.add_paragraph(style="List Number")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(t)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

# Терміни виконання
add_rich_paragraph([
    ("Терміни виконання: ", "bold"),
    ("робота виконується в позааудиторний час протягом 1 тижня (2 академічні години) та подається на перевірку викладачеві до початку наступного практичного заняття.", "normal")
])

# Очікувані результати
add_section_header("Очікувані результати")
outcomes = [
    "Студент пояснює призначення мови HTML та структуру вебсторінки на рівні, доступному для розуміння учнями початкових класів.",
    "Грамотно застосовує парні й одинарні теги, дотримується правил вкладеності та синтаксису атрибутів.",
    "Уміє налаштовувати кодування UTF-8 для коректного відображення українського алфавіту та задавати заголовок сторінки.",
    "Вставляє на сторінку зображення з альтернативним текстом, створює внутрішні та зовнішні гіперпосилання, вбудовує аудіо- й відеоматеріали.",
    "Структурує навчальну інформацію за допомогою списків і таблиць для підвищення наочності дидактичних матеріалів."
]
for out in outcomes:
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(out)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

# Перелік опрацьовуваних питань
add_section_header("Перелік опрацьовуваних питань")
questions_list = [
    "Поняття мови гіпертекстової розмітки HTML. Відмінність між мовою розмітки та мовою програмування.",
    "Обов’язкова структура HTML5-документа: призначення інструкції <!DOCTYPE html> та контейнерів <html>, <head>, <body>.",
    "Встановлення параметрів сторінки у секції <head>: кодування символів <meta charset=\"UTF-8\"> та заголовок вкладки <title>.",
    "Поняття тегу та атрибута. Відмінність між парними (контейнерними) та одинарними (порожніми) тегами.",
    "Теги структурування та форматування тексту: заголовки шести рівнів <h1>–<h6>, абзаци <p>, перенесення рядка <br>, логічне виділення <strong> та <em>.",
    "Організація списків на вебсторінці: маркований <ul>, нумерований <ol> та елементи списку <li>.",
    "Створення гіперпосилань за допомогою тегу <a>. Атрибути href та target=\"_blank\". Відносні й абсолютні шляхи.",
    "Додавання зображень тегом <img>. Обов’язкові атрибути src та alt, налаштування розмірів width і height.",
    "Табличне подання даних: теги <table>, <tr>, <th>, <td> та базові атрибути меж і відступів.",
    "Інтеграція мультимедійного контенту (аудіозаписів та навчальних відеороликів) засобами HTML5 (<audio>, <video>)."
]
for q in questions_list:
    p = doc.add_paragraph(style="List Number")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(q)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

# Теоретичні відомості
add_section_header("Теоретичні відомості (стислий огляд)")

add_sub_header("1. Базова структура HTML-документа та параметри сторінки")
add_rich_paragraph([
    ("HTML (HyperText Markup Language) — це стандартна мова розмітки, за допомогою якої браузер розуміє, як саме розмістити текст, картинки й кнопки на екрані. Для учнів 3–4 класів створення вебсторінки найзручніше пояснити через аналогію ", "normal"),
    ("будівництва казкового будиночка", "bold"),
    (": HTML — це цеглинки та стіни (каркас), CSS — фарба й шпалери (оформлення), а JavaScript — електрика та дзвінок на дверях (інтерактивність).", "normal")
])
add_rich_paragraph([
    ("Будь-який сучасний вебдокумент починається з оголошення типу документа ", "normal"),
    ("<!DOCTYPE html>", "code"),
    (" і складається з головного контейнера ", "normal"),
    ("<html>", "code"),
    (", поділеного на дві частини: службову «шапку» ", "normal"),
    ("<head>", "code"),
    (" («паспорт» сторінки) та видиме «тіло» ", "normal"),
    ("<body>", "code"),
    (" («вітрину», яку бачить користувач). Щоб українські літери «і», «ї», «є», «ґ» не перетворювалися на незрозумілі символи, у ", "normal"),
    ("<head>", "code"),
    (" обов’язково вказують кодування ", "normal"),
    ("<meta charset=\"UTF-8\">", "code"),
    (", а назву вкладки браузера задають тегом ", "normal"),
    ("<title>", "code"),
    (".", "normal")
])

add_schema_image(img_1, "Рис. 1. Анатомія базового HTML-документа")

add_sub_header("2. Теги, атрибути та правила форматування тексту")
add_rich_paragraph([
    ("Команда розмітки називається ", "normal"),
    ("тегом", "bold"),
    (" і завжди береться у кутові дужки ", "normal"),
    ("< >", "code"),
    (". Більшість тегів є ", "normal"),
    ("парними", "bold"),
    (" (мають відкриваючий тег, наприклад ", "normal"),
    ("<p>", "code"),
    (", і закриваючий зі скісною рискою ", "normal"),
    ("</p>", "code"),
    ("). Проте існують і ", "normal"),
    ("одинарні теги", "bold"),
    (", які не потребують закриття: ", "normal"),
    ("<br>", "code"),
    (" (перенесення рядка), ", "normal"),
    ("<hr>", "code"),
    (" (горизонтальна лінія-розділювач) та ", "normal"),
    ("<img>", "code"),
    (" (зображення). Додаткові налаштування записуються всередині відкриваючого тегу у вигляді ", "normal"),
    ("атрибутів", "bold"),
    (" за схемою ", "normal"),
    ("назва=\"значення\"", "code"),
    (".", "normal")
])

add_schema_image(img_2, "Рис. 2. Синтаксична будова парного тегу з атрибутом")

add_callout([
    ("Важливе правило синтаксису: ", "bold"),
    ("теги не можна закривати «навхрест». Якщо ви відкрили абзац, а всередині виділили слово жирним шрифтом, то спочатку закривається внутрішній тег, а потім зовнішній: ", "normal"),
    ("<p>Увага! <strong>Виконайте вправу.</strong></p>", "code"),
    (". Порушення цього порядку призводить до збою відображення сторінки.", "normal")
], bg_hex="FFF4E5", border_hex="C93400")

add_sub_header("3. Гіперпосилання, списки та таблиці")
add_rich_paragraph([
    ("Головна особливість Інтернету — можливість миттєво переходити з однієї сторінки на іншу за допомогою ", "normal"),
    ("гіперпосилань", "bold"),
    (". Для їх створення використовують парний тег ", "normal"),
    ("<a>", "code"),
    (" (від англ. ", "normal"),
    ("anchor", "italic"),
    (" — якір). Адресу призначення вказують в атрибуті ", "normal"),
    ("href", "code"),
    (". Якщо додати атрибут ", "normal"),
    ("target=\"_blank\"", "code"),
    (", посилання відкриється у новій вкладці браузера — це дуже зручно на уроці, щоб учень не втратив основну сторінку із завданням.", "normal")
])
add_rich_paragraph([
    ("Для впорядкування дидактичного матеріалу використовують марковані (", "normal"),
    ("<ul>", "code"),
    (") та нумеровані (", "normal"),
    ("<ol>", "code"),
    (") списки, де кожен пункт обгортається у тег ", "normal"),
    ("<li>", "code"),
    (". Розклад уроків, порівняльні характеристики або кросворди зручно оформлювати у вигляді таблиці ", "normal"),
    ("<table>", "code"),
    (", яка складається з рядків ", "normal"),
    ("<tr>", "code"),
    (", заголовкових комірок ", "normal"),
    ("<th>", "code"),
    (" та звичайних комірок даних ", "normal"),
    ("<td>", "code"),
    (".", "normal")
])

add_sub_header("4. Графіка та мультимедіа на освітньому вебсайті")
add_rich_paragraph([
    ("Для молодших школярів візуалізація є критично важливою, оскільки в 6–10 років переважає наочно-образне мислення. Зображення вставляють одинарним тегом ", "normal"),
    ("<img>", "code"),
    (" із двома обов’язковими атрибутами: ", "normal"),
    ("src", "code"),
    (" (шлях до файлу зображення) та ", "normal"),
    ("alt", "code"),
    (" (альтернативний текстовий опис, який з’явиться, якщо картинка не завантажиться, або буде озвучений програмою екранного доступу для дітей із порушеннями зору).", "normal")
])
add_rich_paragraph([
    ("Стандарт HTML5 дозволяє додавати звук і відео без сторонніх плагінів. Для відтворення аудіоказок чи словникових диктантів застосовують тег ", "normal"),
    ("<audio src=\"kazka.mp3\" controls></audio>", "code"),
    (", а для навчальних мультфільмів чи відеоінструкцій — тег ", "normal"),
    ("<video src=\"urok.mp4\" width=\"480\" controls></video>", "code"),
    (". Атрибут ", "normal"),
    ("controls", "code"),
    (" обов’язковий, інакше на екрані не з’являться кнопки відтворення, паузи та гучності.", "normal")
])

add_schema_image(img_3, "Рис. 3. Класифікація графічних та мультимедійних форматів для вебсторінок")

# Етапи виконання
add_section_header("Етапи виконання самостійної роботи")
add_schema_image(img_4, "Рис. 4. Послідовність виконання завдань самостійної роботи")

# Інструкційна картка
add_section_header("Інструкційна картка практичного завдання")
add_rich_paragraph([
    ("Завдання: ", "bold"),
    ("розробити односторінковий навчальний вебресурс ", "normal"),
    ("«Цікава інформатика для 3 класу»", "bold"),
    (", зберігши його у файлі ", "normal"),
    ("index.html", "code"),
    (" всередині окремої робочої папки ", "normal"),
    ("SR15_Prizvyshche", "code"),
    (".", "normal")
])

instr_headers = ["№ кроку", "Зміст дії студента", "Зразок HTML-коду / команди"]
instr_rows = [
    [
        "1",
        "Створіть папку проєкту та підпапку media для картинок, звуку й відео. Створіть текстовий файл index.html у кодуванні UTF-8.",
        [("mkdir SR15_Prizvyshche\nmkdir SR15_Prizvyshche\\media", "code")]
    ],
    [
        "2",
        "Сформуйте базовий каркас сторінки, задайте українське кодування, заголовок вкладки та світло-блакитний фон сторінки.",
        [("<!DOCTYPE html>\n<html lang=\"uk\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Цікава інформатика</title>\n</head>\n<body bgcolor=\"#F0F8FF\">", "code")]
    ],
    [
        "3",
        "Додайте головний заголовок по центру та вступний абзац із виділенням ключових слів.",
        [("<h1 align=\"center\">Ласкаво просимо на урок!</h1>\n<p>Сьогодні ми вивчаємо <strong>безпечний Інтернет</strong> та <em>комп'ютерну графіку</em>.</p>", "code")]
    ],
    [
        "4",
        "Вставте тематичне зображення із папки media, задавши ширину 350 пікселів та альтернативний опис.",
        [("<img src=\"media/robot.png\" alt=\"Веселий робот-помічник\" width=\"350\">", "code")]
    ],
    [
        "5",
        "Оформіть нумерований список із 3 правил безпечної роботи за комп'ютером та додайте корисне посилання на освітній портал.",
        [("<ol>\n  <li>Тримай спину рівно.</li>\n  <li>Роби гімнастику для очей.</li>\n</ol>\n<a href=\"https://mon.gov.ua\" target=\"_blank\">Портал МОН</a>", "code")]
    ],
    [
        "6",
        "Створіть таблицю на 2 стовпці та 3 рядки з розкладом гуртка юних інформатиків.",
        [("<table border=\"1\" cellpadding=\"6\">\n  <tr><th>День тижня</th><th>Тема заняття</th></tr>\n  <tr><td>Вівторок</td><td>Малюємо у графічному редакторі</td></tr>\n</table>", "code")]
    ],
    [
        "7",
        "Вбудуйте аудіо- або відеофрагмент із панеллю керування та коректно закрийте теги </body> і </html>.",
        [("<video src=\"media/lesson.mp4\" width=\"420\" controls></video>\n</body>\n</html>", "code")]
    ]
]
add_styled_table(instr_headers, instr_rows, [2.0, 6.5, 8.5])

# Завдання на заповнення таблиці
add_section_header("Завдання на заповнення таблиці")
add_rich_paragraph([
    ("У звіті заповніть порожні комірки таблиці, систематизувавши призначення та ключові атрибути вивчених HTML-тегів:", "normal")
])

fill_headers = ["HTML-тег", "Тип (парний / одинарний)", "Основне призначення на сторінці", "Ключові атрибути"]
fill_rows = [
    [[("<title>", "code")], "Парний", "Задає назву сторінки на вкладці браузера", "Немає"],
    [[("<h1> ... <h6>", "code")], "...", "...", [("align", "code")]],
    [[("<a>", "code")], "...", "Створює гіперпосилання на іншу сторінку або файл", "..."],
    [[("<img>", "code")], "Одинарний", "...", [("src, alt, width, height", "code")]],
    [[("<table>", "code")], "...", "...", [("border, cellpadding", "code")]],
    [[("<video>", "code")], "Парний", "...", "..."]
]
add_styled_table(fill_headers, fill_rows, [3.2, 3.8, 5.5, 4.5])

# Теоретичні питання для самоперевірки
add_section_header("Теоретичні питання для самоперевірки")
self_check_q = [
    "Що таке HTML і чому його називають мовою розмітки гіпертексту, а не мовою програмування?",
    "Яку роль виконує інструкція <!DOCTYPE html> на початку кожного вебдокумента?",
    "Чим відрізняється вміст контейнера <head> від вмісту контейнера <body>?",
    "Для чого в розділі <head> прописують тег <meta charset=\"UTF-8\">? Що станеться, якщо його пропустити?",
    "Наведіть по 3 приклади парних і одинарних тегів HTML.",
    "Що таке атрибут тегу та за якими синтаксичними правилами він записується?",
    "Чому атрибут alt у тегу <img> вважається обов’язковим з погляду доступності освіти?",
    "Як зробити так, щоб гіперпосилання відкривалося у новій вкладці браузера?",
    "У чому полягає відмінність між тегами <ul>, <ol> та <li>?",
    "Які атрибути необхідно вказати в тегах <audio> та <video>, щоб користувач міг керувати відтворенням медіафайлу?"
]
for q in self_check_q:
    p = doc.add_paragraph(style="List Number")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(q)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

# Рекомендації до оформлення звіту
add_section_header("Рекомендації до оформлення звіту")
add_rich_paragraph([
    ("Звіт про виконання самостійної роботи подається в електронному або друкованому вигляді та повинен містити:", "normal")
])
report_reqs = [
    "Титульну сторінку із зазначенням номера й теми самостійної роботи, прізвища, імені та групи студента.",
    "Мету роботи та перелік використаного програмного забезпечення.",
    "Лістинг (повний вихідний код) створеного файлу index.html із відступами для наочності вкладеності тегів.",
    "Скріншот вікна браузера, що демонструє коректне відображення всіх елементів розробленої вебсторінки (тексту, списків, таблиці, зображення, посилання та медіаплеєра).",
    "Заповнену узагальнюючу таблицю HTML-тегів та короткі письмові відповіді на 10 питань для самоперевірки.",
    "Висновок щодо методичної доцільності використання вебтехнологій у роботі вчителя інформатики початкової школи."
]
for req in report_reqs:
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(req)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

# Критерії оцінювання
add_section_header("Критерії оцінювання")
crit_headers = ["Критерій оцінювання", "Показники виконання", "Макс. бал"]
crit_rows = [
    [
        "1. Семантична та синтаксична коректність HTML-коду",
        "Наявність <!DOCTYPE html>, <html>, <head>, <body>, кодування UTF-8, правильне закриття всіх парних тегів.",
        "3"
    ],
    [
        "2. Форматування тексту, списків і таблиць",
        "Використано заголовки різних рівнів, абзаци, логічне виділення тексту, списки та структуровану таблицю.",
        "3"
    ],
    [
        "3. Інтеграція гіперпосилань, графіки та мультимедіа",
        "Коректно працюють гіперпосилання (href, target), відображається зображення з атрибутом alt, додано робочий елемент <audio> або <video> з controls.",
        "3"
    ],
    [
        "4. Якість звіту та повнота теоретичних відповідей",
        "Заповнено узагальнюючу таблицю тегів, надано змістовні відповіді на питання самоперевірки, додано скріншот результату.",
        "3"
    ],
    [
        [("Усього за самостійну роботу", "bold")],
        [("Максимальна сума балів за виконання всіх етапів роботи", "bold")],
        [("12", "bold")]
    ]
]
add_styled_table(crit_headers, crit_rows, [5.0, 9.5, 2.5])

output_docx = "Samostiyna_robota_15_HTML_Multimedia.docx"
doc.save(output_docx)
print(f"Документ успішно згенеровано: {output_docx}")
print("Схеми збережено у папці output/ у форматах PNG та SVG.")