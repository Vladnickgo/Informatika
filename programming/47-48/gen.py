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

# =============================================================================
# НАЛАШТУВАННЯ MATPLOTLIB (APPLE-ПОДІБНИЙ СТИЛЬ, РЕДАГОВАНИЙ SVG)
# =============================================================================
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Палітра
C_BG_CARD = "#F5F5F7"
C_BORDER = "#E5E5EA"
C_TEXT = "#1D1D1F"
C_SUBTEXT = "#86868B"
C_BLUE = "#0071E3"
C_GREEN = "#248A3D"
C_ORANGE = "#C93400"
C_RED = "#C4001D"
C_PURPLE = "#6E30A8"


def save_fig(fig, name):
    png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    svg_path = os.path.join(OUTPUT_DIR, f"{name}.svg")
    fig.savefig(png_path, dpi=220, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return png_path


def draw_card(ax, x, y, w, h, title, desc, accent, title_fs=12.5, desc_fs=10.8):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        facecolor=C_BG_CARD, edgecolor=C_BORDER, linewidth=1.4
    )
    ax.add_patch(box)
    bar = FancyBboxPatch(
        (x + 0.12, y + h - 0.22), w - 0.24, 0.10,
        boxstyle="round,pad=0.0,rounding_size=0.05",
        facecolor=accent, edgecolor="none"
    )
    ax.add_patch(bar)
    ax.text(
        x + w / 2, y + h - 0.48, title,
        ha="center", va="top", fontsize=title_fs, fontweight="bold", color=C_TEXT
    )
    ax.text(
        x + w / 2, y + h / 2 - 0.25, desc,
        ha="center", va="center", fontsize=desc_fs, color=C_SUBTEXT, linespacing=1.35
    )


def generate_scheme_1_operators():
    """Схема 1: Класифікація блоків категорії 'Оператори' у Scratch 3.0."""
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    ax.text(
        6.0, 4.12, "Категорія «Оператори» у Scratch 3.0: чотири групи блоків",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    cards = [
        ("Математичні", "Овальні блоки (число):\n+ , − , * , /\nвипадкове, остача,\nокруглити, модуль", C_GREEN),
        ("Порівняння", "Шестикутні (так/ні):\n> , < , =\nперевірка рівності\nта нерівностей", C_BLUE),
        ("Логічні", "Шестикутні (так/ні):\nІ , АБО , НЕ\nоб'єднання кількох\nумов в одну", C_PURPLE),
        ("Текстові", "Овальні та шестикутні:\nз'єднати, літера №,\nдовжина рядка,\nмістить підрядок", C_ORANGE),
    ]

    w = 2.65
    gap = 0.28
    start_x = 0.28
    for i, (title, desc, color) in enumerate(cards):
        x = start_x + i * (w + gap)
        draw_card(ax, x, 0.35, w, 3.25, title, desc, color, title_fs=12.8, desc_fs=10.8)

    return save_fig(fig, "scheme_1_operators")


def generate_scheme_2_logic():
    """Схема 2: Логічні операції І, АБО, НЕ у Scratch."""
    fig, ax = plt.subplots(figsize=(12, 4.3))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.3)
    ax.axis("off")

    ax.text(
        6.0, 4.02, "Логічні операції для побудови складних умов",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    cards = [
        ("Операція «І» (AND)", "Істина, коли ОБИДВІ\nумови виконуються.\n\nПриклад:\nвік > 6  І  вік < 11", C_BLUE),
        ("Операція «АБО» (OR)", "Істина, коли виконується\nХОЧА Б ОДНА умова.\n\nПриклад:\nдень = Сб  АБО  день = Нд", C_GREEN),
        ("Операція «НЕ» (NOT)", "Змінює результат умови\nна протилежний.\n\nПриклад:\nНЕ (пароль = 1234)", C_RED),
    ]

    w = 3.55
    gap = 0.40
    start_x = 0.27
    for i, (title, desc, color) in enumerate(cards):
        x = start_x + i * (w + gap)
        draw_card(ax, x, 0.32, w, 3.20, title, desc, color, title_fs=12.8, desc_fs=10.8)

    return save_fig(fig, "scheme_2_logic")


def generate_scheme_3_strings():
    """Схема 3: Візуалізація дій із текстовими виразами на прикладі слова 'ШКОЛА'."""
    fig, ax = plt.subplots(figsize=(12, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    ax.text(
        6.0, 4.35, "Робота з текстовими виразами на прикладі рядка «ШКОЛА»",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    # Візуалізація символів та індексів (у Scratch нумерація з 1)
    letters = ["Ш", "К", "О", "Л", "А"]
    cell_w = 1.15
    gap = 0.18
    total_w = len(letters) * cell_w + (len(letters) - 1) * gap
    start_x = (12.0 - total_w) / 2

    for idx, ch in enumerate(letters, start=1):
        cx = start_x + (idx - 1) * (cell_w + gap)
        box = FancyBboxPatch(
            (cx, 2.75), cell_w, 0.95,
            boxstyle="round,pad=0.02,rounding_size=0.16",
            facecolor=C_BG_CARD, edgecolor=C_BLUE, linewidth=1.6
        )
        ax.add_patch(box)
        ax.text(cx + cell_w / 2, 3.25, ch, ha="center", va="center",
                fontsize=15, fontweight="bold", color=C_TEXT)
        ax.text(cx + cell_w / 2, 2.50, f"індекс {idx}", ha="center", va="top",
                fontsize=10.5, color=C_SUBTEXT)

    # Нижній ряд: 3 картки з результатами операцій
    ops = [
        ("довжина «ШКОЛА»", "Результат: 5\n(кількість символів)", C_GREEN),
        ("літера 3 у «ШКОЛА»", "Результат: «О»\n(нумерація з 1)", C_PURPLE),
        ("з'єднати «Привіт, » і ім'я", "Результат: «Привіт, Оля»\n(склеювання рядків)", C_ORANGE),
    ]
    w = 3.55
    g = 0.40
    sx = 0.27
    for i, (title, desc, color) in enumerate(ops):
        x = sx + i * (w + g)
        draw_card(ax, x, 0.25, w, 1.85, title, desc, color, title_fs=11.8, desc_fs=10.5)

    return save_fig(fig, "scheme_3_strings")


def generate_scheme_4_levels():
    """Схема 4: Трирівнева структура практичної роботи №11."""
    fig, ax = plt.subplots(figsize=(12, 3.9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.9)
    ax.axis("off")

    ax.text(
        6.0, 3.65, "Структура практичної роботи (загальна тривалість ≈ 27 хв)",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    levels = [
        ("Рівень 1. Репродуктивний", "≈ 7 хв  |  до 4 балів\n\nПрограма-калькулятор:\nвведення двох чисел,\nсума та добуток у тексті", C_GREEN),
        ("Рівень 2. Продуктивний", "≈ 10 хв  |  до 5 балів\n\nПеревірка оцінки (1–12)\nз логічними умовами\n«І» та «АБО»", C_BLUE),
        ("Рівень 3. Творчий", "≈ 10 хв  |  до 4 балів\n\nМінівікторина для учнів:\nвипадкові приклади,\nаналіз текстової відповіді", C_PURPLE),
    ]

    w = 3.45
    gap = 0.55
    start_x = 0.27
    for i, (title, desc, color) in enumerate(levels):
        x = start_x + i * (w + gap)
        draw_card(ax, x, 0.3, w, 2.85, title, desc, color, title_fs=12.5, desc_fs=10.8)
        if i < 2:
            ax.annotate(
                "", xy=(x + w + gap - 0.08, 1.72), xytext=(x + w + 0.08, 1.72),
                arrowprops=dict(arrowstyle="->", color=C_SUBTEXT, lw=2.0)
            )

    return save_fig(fig, "scheme_4_levels_pr11")


# =============================================================================
# ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ PYTHON-DOCX
# =============================================================================
COLOR_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)
COLOR_SUB = RGBColor(0x2E, 0x75, 0xB6)
COLOR_CMD = RGBColor(0xC0, 0x39, 0x2B)
COLOR_TEXT = RGBColor(0x00, 0x00, 0x00)


def set_run_font(run, font_name="Times New Roman", size_pt=14, bold=False, italic=False, color=COLOR_TEXT):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), font_name)
    rFonts.set(qn("w:hAnsi"), font_name)
    rFonts.set(qn("w:cs"), font_name)
    rFonts.set(qn("w:eastAsia"), font_name)


def configure_document(doc):
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)
        add_page_number_footer(section)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(14)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)

    run = p.add_run()
    set_run_font(run, size_pt=12)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(fld_end)


def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    set_run_font(run, size_pt=14, bold=True, color=COLOR_PRIMARY)
    return p


def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    set_run_font(run, size_pt=14, bold=True, color=COLOR_SUB)
    return p


def add_body_p(doc, parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=5):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)

    if isinstance(parts, str):
        run = p.add_run(parts)
        set_run_font(run)
        return p

    for text, mode in parts:
        run = p.add_run(text)
        if mode == "bold":
            set_run_font(run, bold=True)
        elif mode == "italic":
            set_run_font(run, italic=True)
        elif mode == "cmd":
            set_run_font(run, font_name="Consolas", size_pt=13, color=COLOR_CMD)
        else:
            set_run_font(run)
    return p


def numbered_paren(doc, items):
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        r_num = p.add_run(f"{idx}) ")
        set_run_font(r_num, bold=True)
        r_txt = p.add_run(item)
        set_run_font(r_txt)


def add_list_items(doc, items, style_name="List Number"):
    for item in items:
        p = doc.add_paragraph(style=style_name)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        if isinstance(item, str):
            r = p.add_run(item)
            set_run_font(r)
        else:
            for text, mode in item:
                r = p.add_run(text)
                if mode == "bold":
                    set_run_font(r, bold=True)
                elif mode == "cmd":
                    set_run_font(r, font_name="Consolas", size_pt=13, color=COLOR_CMD)
                else:
                    set_run_font(r)


def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def add_callout(doc, parts, fill_hex="EEF4FA", border_hex="0071E3"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(16.5)
    set_cell_shading(cell, fill_hex)
    set_cell_margins(cell, top=100, bottom=100, left=180, right=140)

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in ("top", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "none")
        tcBorders.append(b)
    left_b = OxmlElement("w:left")
    left_b.set(qn("w:val"), "single")
    left_b.set(qn("w:sz"), "28")
    left_b.set(qn("w:space"), "0")
    left_b.set(qn("w:color"), border_hex)
    tcBorders.append(left_b)
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(0)
    if isinstance(parts, str):
        r = p.add_run(parts)
        set_run_font(r)
    else:
        for text, mode in parts:
            r = p.add_run(text)
            if mode == "bold":
                set_run_font(r, bold=True)
            elif mode == "cmd":
                set_run_font(r, font_name="Consolas", size_pt=13, color=COLOR_CMD)
            else:
                set_run_font(r)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)


def add_styled_table(doc, headers, rows, col_widths_cm):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))

    for col_idx, h_text in enumerate(headers):
        cell = tbl.rows[0].cells[col_idx]
        cell.width = Cm(col_widths_cm[col_idx])
        set_cell_shading(cell, "1F4E79")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(h_text)
        set_run_font(r, size_pt=13, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))

    for row_idx, row_data in enumerate(rows, start=1):
        for col_idx, cell_val in enumerate(row_data):
            cell = tbl.rows[row_idx].cells[col_idx]
            cell.width = Cm(col_widths_cm[col_idx])
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            if isinstance(cell_val, str):
                r = p.add_run(cell_val)
                set_run_font(r, size_pt=13)
            else:
                for text, mode in cell_val:
                    r = p.add_run(text)
                    if mode == "bold":
                        set_run_font(r, size_pt=13, bold=True)
                    elif mode == "cmd":
                        set_run_font(r, font_name="Consolas", size_pt=12, color=COLOR_CMD)
                    else:
                        set_run_font(r, size_pt=13)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)
    return tbl


def add_scheme_image(doc, img_path, caption_text, width_cm=15.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    run = p_img.add_run()
    run.add_picture(img_path, width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(caption_text)
    set_run_font(r_cap, size_pt=12, italic=True, color=RGBColor(0x55, 0x55, 0x55))


# =============================================================================
# ГЕНЕРАЦІЯ ДОКУМЕНТА
# =============================================================================
def build_document():
    # 1. Генеруємо схеми
    img_operators = generate_scheme_1_operators()
    img_logic = generate_scheme_2_logic()
    img_strings = generate_scheme_3_strings()
    img_levels = generate_scheme_4_levels()

    # 2. Створюємо DOCX
    doc = Document()
    configure_document(doc)

    # Верхній заголовок
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("ПРАКТИЧНЕ ЗАНЯТТЯ №11")
    set_run_font(r_title, size_pt=14, bold=True, color=COLOR_PRIMARY)

    # Тема
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_after = Pt(8)
    r_topic = p_topic.add_run("Тема: Логічні вирази, математичні дії, дії з текстовими виразами.")
    set_run_font(r_topic, size_pt=14, bold=True, color=COLOR_TEXT)

    # Мета
    add_heading_1(doc, "Мета")
    add_body_p(
        doc,
        "Навчитися використовувати блоки математичних та логічних операцій, роботи з рядками у Scratch "
        "для створення складніших програм. Розвивати логіко-математичне мислення, вміння будувати складні "
        "умови для розгалужень і циклів. Розвивати навички формалізації. Виховувати розуміння потужності "
        "інструментів програмування, здатних оперувати не лише графікою, а й даними."
    )

    # Обладнання та програмне забезпечення
    add_heading_1(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "Інструкційні картки.",
        "Персональний комп'ютер або ноутбук із доступом до мережі Інтернет.",
        "Середовище візуального програмування Scratch 3.0 (scratch.mit.edu або Scratch Desktop)."
    ])

    # Література
    add_heading_1(doc, "Література")
    add_list_items(doc, [
        "Єжова Л. Ф. Алгоритмізація і програмування процедур обробки інформації : навч.-метод. посібник. Київ : КНЕУ, 2019. 60 с.",
        "Васильєв О. Алгоритми. Київ : Навчальна книга – Богдан, 2022. 424 с.",
        "Васильєв О. Програмування мовою Java. Київ : Навчальна книга – Богдан, 2020. 696 с."
    ], style_name="List Number")

    # =========================================================================
    # ХІД ЗАНЯТТЯ (за запитом користувача)
    # =========================================================================
    add_heading_1(doc, "Хід заняття")
    add_styled_table(
        doc,
        headers=["Етап заняття", "Зміст діяльності", "Орієнтовний час"],
        rows=[
            ["1. Організаційний етап", "Перевірка готовності робочих місць, запуск Scratch 3.0, ознайомлення з темою та метою заняття.", "3 хв"],
            ["2. Теоретичний інструктаж", "Повторення категорії «Оператори»: форми блоків (овальні й шестикутні), приклади обчислень і логічних умов.", "7 хв"],
            ["3. Практична робота", "Послідовне виконання завдань репродуктивного (7 хв), продуктивного (10 хв) та творчого (10 хв) рівнів.", "27 хв"],
            ["4. Підбиття підсумків", "Демонстрація створених проєктів, самоперевірка за критеріями оцінювання, збереження файлів та оформлення звіту.", "8 хв"],
        ],
        col_widths_cm=[4.5, 9.5, 2.5]
    )

    # =========================================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =========================================================================
    add_heading_1(doc, "Теоретичні відомості")

    # Підрозділ 1
    add_heading_2(doc, "1. Огляд категорії «Оператори» у Scratch 3.0")
    add_body_p(
        doc,
        "Усі блоки для обчислень, перевірки умов та обробки тексту зібрані в зеленій категорії «Оператори». "
        "Форма кожного блока підказує, який тип результату він повертає: овальні блоки повертають число або текст "
        "і вставляються у поля введення інших команд, а шестикутні повертають логічне значення («істина» або «хиба») "
        "і використовуються всередині умовних конструкцій та циклів."
    )
    add_scheme_image(doc, img_operators, "Рис. 1. Чотири групи блоків у категорії «Оператори»")

    # Підрозділ 2
    add_heading_2(doc, "2. Математичні операції та генерація випадкових чисел")
    add_body_p(doc, [
        ("Scratch підтримує базові арифметичні дії (", "normal"),
        ("+", "cmd"), (", ", "normal"), ("-", "cmd"), (", ", "normal"),
        ("*", "cmd"), (", ", "normal"), ("/", "cmd"),
        ("), обчислення остачі від ділення (", "normal"),
        ("остача від ділення", "cmd"),
        ("), округлення (", "normal"),
        ("округлити", "cmd"),
        (") та математичні функції (", "normal"),
        ("модуль", "cmd"), (", ", "normal"), ("корінь", "cmd"),
        ("). Для створення тренажерів і вікторин у початковій школі особливо корисний блок ", "normal"),
        ("випадкове від 1 до 10", "cmd"),
        (", який щоразу формує нове число у заданому діапазоні.", "normal")
    ])
    add_callout(doc, [
        ("Порядок виконання дій у Scratch визначається вкладеністю блоків: спочатку обчислюється внутрішній блок, "
         "а його результат передається зовнішньому. Це природно замінює математичні дужки.", "normal")
    ])

    # Підрозділ 3
    add_heading_2(doc, "3. Операції порівняння та логічні вирази")
    add_body_p(
        doc,
        "Прості умови будуються за допомогою блоків порівняння («більше», «менше», «дорівнює»). "
        "Коли потрібно перевірити одночасно дві або більше ознак, застосовують логічні операції «І», «АБО» та «НЕ»."
    )
    add_scheme_image(doc, img_logic, "Рис. 2. Логічні операції І, АБО, НЕ та приклади умов")

    # Підрозділ 4
    add_heading_2(doc, "4. Дії з текстовими виразами (рядками)")
    add_body_p(doc, [
        ("Текстові операції дозволяють формувати зрозумілі повідомлення для користувача та аналізувати введені відповіді. "
         "Блок ", "normal"),
        ("з'єднати [яблуко] [банан]", "cmd"),
        (" склеює два рядки (не забувайте додавати пробіл у кінці першого слова). Блок ", "normal"),
        ("довжина [яблуко]", "cmd"),
        (" повертає кількість символів, а ", "normal"),
        ("літера 1 у [яблуко]", "cmd"),
        (" — символ за його порядковим номером.", "normal")
    ])
    add_scheme_image(doc, img_strings, "Рис. 3. Основні операції над текстовими рядками у Scratch")

    # =========================================================================
    # ПОКРОКОВИЙ АЛГОРИТМ ВИКОНАННЯ РІЗНОРІВНЕВИХ ЗАВДАНЬ
    # =========================================================================
    add_heading_1(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    add_scheme_image(doc, img_levels, "Рис. 4. Трирівнева структура практичної роботи №11")

    # Рівень 1
    add_heading_2(doc, "Рівень 1 — репродуктивний (≈ 7 хв)")
    add_body_p(
        doc,
        "Мета рівня: навчитися поєднувати змінні, математичні блоки та склеювання тексту в одному алгоритмі «Калькулятор»."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Дія студента", "Блоки / параметри"],
        rows=[
            [
                "1",
                "Створіть новий проєкт у Scratch та додайте у категорії «Змінні» дві змінні: a і b.",
                [("Створити змінну: a, b", "cmd")]
            ],
            [
                "2",
                "Організуйте запит першого числа від користувача та збережіть відповідь у змінній a.",
                [("запитати [Введіть перше число:] і чекати", "cmd"), ("\n", "normal"), ("надати a значення (відповідь)", "cmd")]
            ],
            [
                "3",
                "Аналогічно запитайте друге число та збережіть його у змінній b.",
                [("запитати [Введіть друге число:] і чекати", "cmd"), ("\n", "normal"), ("надати b значення (відповідь)", "cmd")]
            ],
            [
                "4",
                "Виведіть результат додавання у вигляді повноцінного речення за допомогою блоку склеювання тексту.",
                [("говорити (з'єднати [Сума = ] (a + b)) 2 сек", "cmd")]
            ],
            [
                "5",
                "Додайте ще один блок виведення для добутку чисел та збережіть проєкт під назвою PR11_Prizvyshche.sb3.",
                [("говорити (з'єднати [Добуток = ] (a * b)) 2 сек", "cmd")]
            ],
        ],
        col_widths_cm=[1.5, 7.6, 7.4]
    )

    # Рівень 2
    add_heading_2(doc, "Рівень 2 — продуктивний (≈ 10 хв)")
    add_body_p(
        doc,
        "Мета рівня: реалізувати перевірку шкільної оцінки за 12-бальною шкалою з використанням складених логічних умов."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Дія студента", "Блоки / параметри"],
        rows=[
            [
                "1",
                "Додайте нового спрайта (або окремий скрипт на клавішу Пропуск) та змінну оцінка.",
                [("коли клавішу пропуск натиснуто", "cmd"), ("\n", "normal"), ("запитати [Введіть оцінку (1-12):] і чекати", "cmd")]
            ],
            [
                "2",
                "Перевірте коректність діапазону: якщо число менше 1 АБО більше 12 — повідомте про помилку.",
                [("якщо (оцінка < 1) або (оцінка > 12) то", "cmd"), ("\n", "normal"), ("говорити [Некоректна оцінка!] 2 сек", "cmd")]
            ],
            [
                "3",
                "Додайте перевірку високого рівня навчальних досягнень (від 10 до 12 включно) через логічне «І».",
                [("якщо (оцінка > 9) і (оцінка < 13) то", "cmd"), ("\n", "normal"), ("говорити [Високий рівень!] 2 сек", "cmd")]
            ],
            [
                "4",
                "Додайте перевірку достатнього рівня (7–9 балів) та виведення відповідного коментаря.",
                [("якщо (оцінка > 6) і (оцінка < 10) то", "cmd"), ("\n", "normal"), ("говорити [Достатній рівень!] 2 сек", "cmd")]
            ],
            [
                "5",
                "Протестуйте скрипт на граничних значеннях: 0, 1, 7, 10, 12, 15 та оновіть збережений файл.",
                [("Тест: 0, 1, 7, 10, 12, 15", "cmd")]
            ],
        ],
        col_widths_cm=[1.5, 7.6, 7.4]
    )

    # Рівень 3
    add_heading_2(doc, "Рівень 3 — творчий (≈ 10 хв)")
    add_body_p(
        doc,
        "Розробіть інтерактивний мінітренажер для учнів початкової школи «Розумний помічник», який поєднує "
        "математичні обчислення, логічну перевірку та обробку текстових даних."
    )
    add_styled_table(
        doc,
        headers=["Вимога до тренажера", "Конкретний зміст виконання"],
        rows=[
            ["Персоналізація (текст)", "На старті програма запитує ім'я учня, вітається через блок «з'єднати» та повідомляє кількість літер у його імені."],
            ["Генерація завдання", "Програма створює два випадкових числа від 2 до 9 та пропонує учневі обчислити їхній добуток."],
            ["Логічна перевірка", "Використовується розгалуження «якщо ... то ... інакше»: при правильній відповіді нараховується бал, при помилці — виводиться підказка з правильним результатом."],
            ["Повторення", "Тренажер ставить щонайменше 3 приклади поспіль (цикл «повторити 3») і в кінці оголошує підсумковий рахунок."],
        ],
        col_widths_cm=[5.0, 11.5]
    )

    # =========================================================================
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # =========================================================================
    add_heading_1(doc, "Критерії оцінювання")
    add_styled_table(
        doc,
        headers=["Компонент оцінювання", "Показники якості виконання", "Макс. балів"],
        rows=[
            ["Рівень 1 (репродуктивний)", "Коректне введення двох чисел, обчислення суми й добутку, форматований вивід через блок «з'єднати».", "4"],
            ["Рівень 2 (продуктивний)", "Правильна побудова складених умов із «І» та «АБО», коректна обробка граничних і помилкових значень.", "5"],
            ["Рівень 3 (творчий)", "Повноцінний мінітренажер із персоналізацією імені, випадковими прикладами, підрахунком балів та циклом.", "3"],
            ["Культура коду та звітності", "Зрозумілі назви змінних, охайне розташування скриптів, своєчасне збереження .sb3 та оформлення звіту.", "1"],
            [
                [("Разом", "bold")],
                [("Максимальна сума балів за практичне заняття", "bold")],
                [("13", "bold")]
            ],
        ],
        col_widths_cm=[4.8, 9.2, 2.5]
    )

    # =========================================================================
    # ФОРМА ЗВІТНОСТІ
    # =========================================================================
    add_heading_1(doc, "Форма звітності")
    add_body_p(doc, "Для зарахування практичного заняття студент подає викладачеві:")
    add_list_items(doc, [
        [("Файл виконаного проєкту у форматі ", "normal"), ("PR11_Prizvyshche.sb3", "cmd"), (".", "normal")],
        "Скриншоти зібраних скриптів для кожного з трьох рівнів та приклади роботи програми на сцені.",
        "Короткий висновок (3–4 речення) про те, як поєднання математичних, логічних і текстових блоків дозволяє створювати навчальні тренажери для початкової школи."
    ], style_name="List Bullet")

    output_docx = "Praktychne_zanyattya_11_Operatory_Scratch.docx"
    doc.save(output_docx)
    print(f"Документ успішно створено: {output_docx}")
    print(f"Схеми (PNG + SVG) збережено у папці: {OUTPUT_DIR}/")


if __name__ == "__main__":
    build_document()