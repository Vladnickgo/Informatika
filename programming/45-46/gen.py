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
    # Верхня акцентна смужка
    bar = FancyBboxPatch(
        (x + 0.12, y + h - 0.22), w - 0.24, 0.10,
        boxstyle="round,pad=0.0,rounding_size=0.05",
        facecolor=accent, edgecolor="none"
    )
    ax.add_patch(bar)
    ax.text(
        x + w / 2, y + h - 0.52, title,
        ha="center", va="top", fontsize=title_fs, fontweight="bold", color=C_TEXT
    )
    ax.text(
        x + w / 2, y + h / 2 - 0.22, desc,
        ha="center", va="center", fontsize=desc_fs, color=C_SUBTEXT, linespacing=1.35
    )


def generate_scheme_1_interface():
    """Схема 1: Основні зони інтерфейсу редактора Scratch 3.0."""
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    ax.text(
        6.0, 4.92, "Основні зони робочого інтерфейсу Scratch 3.0",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    # Верхній ряд: 3 картки
    draw_card(
        ax, 0.3, 2.45, 3.55, 2.0,
        "1. Палітра блоків",
        "Категорії команд за кольором:\nРух, Вигляд, Звук, Події,\nКерування, Датчики",
        C_BLUE
    )
    draw_card(
        ax, 4.22, 2.45, 3.55, 2.0,
        "2. Область скриптів",
        "Робоче поле для складання\nалгоритмів із блоків\nметодом перетягування",
        C_PURPLE
    )
    draw_card(
        ax, 8.15, 2.45, 3.55, 2.0,
        "3. Сцена (Stage)",
        "Вікно виконання проєкту\nрозміром 480 × 360 пікселів,\nпрапорець запуску та Стоп",
        C_GREEN
    )

    # Нижній ряд: 2 ширші картки
    draw_card(
        ax, 1.2, 0.25, 4.5, 1.85,
        "4. Панель спрайтів і тла",
        "Керування персонажами, їхніми координатами X/Y,\nрозміром, напрямком та перемикання тла сцени",
        C_ORANGE
    )
    draw_card(
        ax, 6.3, 0.25, 4.5, 1.85,
        "5. Вкладки та меню файлу",
        "Перемикання «Код / Образи / Звуки»,\nменю «Файл» для збереження та завантаження .sb3",
        C_RED
    )

    return save_fig(fig, "scheme_1_interface")


def generate_scheme_2_libraries():
    """Схема 2: Бібліотеки ресурсів у Scratch 3.0."""
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    ax.text(
        6.0, 3.92, "Бібліотеки цифрових ресурсів проєкту Scratch",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    cards = [
        ("Спрайти", "Виконавці команд:\nтварини, люди,\nпредмети, літери", C_BLUE),
        ("Образи", "Зовнішній вигляд\nспрайта для анімації\nта зміни стану", C_PURPLE),
        ("Тло сцени", "Фон проєкту:\nкімната, космос,\nприрода, сітка XY", C_GREEN),
        ("Звуки", "Аудіоефекти,\nголоси, мелодії\nта власний запис", C_ORANGE),
    ]

    w = 2.65
    gap = 0.28
    start_x = 0.28
    for i, (title, desc, color) in enumerate(cards):
        x = start_x + i * (w + gap)
        draw_card(ax, x, 0.45, w, 2.95, title, desc, color, title_fs=13, desc_fs=11)

    return save_fig(fig, "scheme_2_libraries")


def generate_scheme_3_coordinates():
    """Схема 3: Координатна площина сцени Scratch (480 x 360)."""
    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    ax.set_xlim(-310, 310)
    ax.set_ylim(-235, 245)
    ax.axis("off")

    ax.text(
        0, 232, "Координатна площина сцени Scratch (480 × 360)",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    # Прямокутник сцени
    stage = FancyBboxPatch(
        (-240, -180), 480, 360,
        boxstyle="round,pad=0,rounding_size=12",
        facecolor=C_BG_CARD, edgecolor=C_BLUE, linewidth=2.0
    )
    ax.add_patch(stage)

    # Допоміжна сітка
    for gx in (-120, 120):
        ax.plot([gx, gx], [-180, 180], color=C_BORDER, linestyle="--", linewidth=1.1)
    for gy in (-90, 90):
        ax.plot([-240, 240], [gy, gy], color=C_BORDER, linestyle="--", linewidth=1.1)

    # Осі X та Y зі стрілками
    ax.annotate("", xy=(265, 0), xytext=(-265, 0),
                arrowprops=dict(arrowstyle="->", color=C_TEXT, lw=1.8))
    ax.annotate("", xy=(0, 200), xytext=(0, -200),
                arrowprops=dict(arrowstyle="->", color=C_TEXT, lw=1.8))

    # Підписи осей
    ax.text(275, 0, "X", ha="left", va="center", fontsize=13.5, fontweight="bold", color=C_BLUE)
    ax.text(0, 205, "Y", ha="center", va="bottom", fontsize=13.5, fontweight="bold", color=C_GREEN)

    # Точки та підписи
    points = [
        (0, 0, "(0; 0)", C_RED, (14, 14), "left", "bottom"),
        (240, 0, "(240; 0)", C_BLUE, (8, -18), "left", "top"),
        (-240, 0, "(-240; 0)", C_BLUE, (-8, -18), "right", "top"),
        (0, 180, "(0; 180)", C_GREEN, (12, 8), "left", "bottom"),
        (0, -180, "(0; -180)", C_GREEN, (12, -10), "left", "top"),
        (120, 90, "I чверть\n(+X; +Y)", C_PURPLE, (0, 0), "center", "center"),
        (-120, 90, "II чверть\n(-X; +Y)", C_ORANGE, (0, 0), "center", "center"),
        (-120, -90, "III чверть\n(-X; -Y)", C_ORANGE, (0, 0), "center", "center"),
        (120, -90, "IV чверть\n(+X; -Y)", C_PURPLE, (0, 0), "center", "center"),
    ]

    for px, py, label, color, (dx, dy), ha, va in points:
        if dx != 0 or dy != 0:
            ax.plot(px, py, "o", color=color, markersize=7.5, zorder=5)
            ax.text(px + dx, py + dy, label, ha=ha, va=va, fontsize=11.2, fontweight="bold", color=color)
        else:
            ax.text(px, py, label, ha=ha, va=va, fontsize=11.5, fontweight="bold", color=C_SUBTEXT)

    return save_fig(fig, "scheme_3_coordinates")


def generate_scheme_4_levels():
    """Схема 4: Трирівнева структура практичного завдання."""
    fig, ax = plt.subplots(figsize=(12, 3.9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.9)
    ax.axis("off")

    ax.text(
        6.0, 3.65, "Структура практичної роботи (загальна тривалість ≈ 27 хв)",
        ha="center", va="top", fontsize=14.5, fontweight="bold", color=C_TEXT
    )

    levels = [
        ("Рівень 1. Репродуктивний", "≈ 7 хв  |  до 4 балів\n\nНалаштування сцени,\nдодавання спрайта і тла,\nзбереження файлу .sb3", C_GREEN),
        ("Рівень 2. Продуктивний", "≈ 10 хв  |  до 5 балів\n\nТочне позиціонування\nза координатами X та Y,\nмаршрут по 4 точках", C_BLUE),
        ("Рівень 3. Творчий", "≈ 10 хв  |  до 4 балів\n\nВласна мінісцена:\n2 спрайти, тло, звук,\nдіалог і рух за координатами", C_PURPLE),
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

    return save_fig(fig, "scheme_4_levels")


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
    """
    parts: рядок або список кортежів (text, mode), де mode in ('normal', 'bold', 'italic', 'cmd')
    """
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
            set_run_font(run, font_name="Consolas", size_pt=13, bold=False, color=COLOR_CMD)
        else:
            set_run_font(run)
    return p


def numbered_paren(doc, items):
    """Нумерований список у форматі 1), 2), 3)... з відступом 1,0 см."""
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
    """Callout-блок без службових заголовків: таблиця 1x1 з лівою рамкою 28 sz."""
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

    # Повторення заголовка на кожній сторінці
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
    img_interface = generate_scheme_1_interface()
    img_libraries = generate_scheme_2_libraries()
    img_coords = generate_scheme_3_coordinates()
    img_levels = generate_scheme_4_levels()

    # 2. Створюємо DOCX
    doc = Document()
    configure_document(doc)

    # Верхній заголовок
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("ПРАКТИЧНЕ ЗАНЯТТЯ №10")
    set_run_font(r_title, size_pt=14, bold=True, color=COLOR_PRIMARY)

    # Тема
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_after = Pt(8)
    r_topic = p_topic.add_run(
        "Тема: Робота у середовищі: вивчення інтерфейсу редактора; створення, редагування та збереження проекту; "
        "користування бібліотекою спрайтів, звуків, тла; переміщення спрайтів з використанням координат."
    )
    set_run_font(r_topic, size_pt=14, bold=True, color=COLOR_TEXT)

    # Мета
    add_heading_1(doc, "Мета")
    add_body_p(
        doc,
        "Закріпити практичні навички роботи в Scratch: створення проекту, пошук і додавання ресурсів з бібліотек, "
        "точне позиціонування спрайтів за координатами. Розвивати вміння самостійно навчатися роботі з новим "
        "програмним забезпеченням. Розвивати проектне мислення. Виховувати старанність, акуратність у роботі "
        "з цифровими активами (збереження проектів, організація робочого простору)."
    )

    # Обладнання та програмне забезпечення
    add_heading_1(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "Інструкційні картки.",
        "Персональний комп'ютер або ноутбук із доступом до мережі Інтернет.",
        "Середовище візуального програмування Scratch 3.0 (онлайн-версія scratch.mit.edu або локальний додаток Scratch Desktop)."
    ])

    # Література
    add_heading_1(doc, "Література")
    add_list_items(doc, [
        "Морзе Н. В., Вембер В. П. Інформатика (рівень стандарт) : підруч. для 10 кл. закл. загал. серед. освіти. Київ : Оріон, 2024.",
        "Ривкінд Й. Я., Лисенко Т. І., Чернікова Л. А., Шакотько В. В. Інформатика (рівень стандарт) : підруч. для 10 кл. закл. загал. серед. освіти. Київ : Генеза, 2024.",
        "Руденко В. Д., Речич Н. В., Потієнко В. О. Інформатика (рівень стандарт) : підруч. для 10 кл. закл. загал. серед. освіти. Харків : Ранок, 2024."
    ], style_name="List Number")

    # =========================================================================
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # =========================================================================
    add_heading_1(doc, "Теоретичні відомості")

    # Підрозділ 1
    add_heading_2(doc, "1. Інтерфейс редактора Scratch 3.0")
    add_body_p(
        doc,
        "Середовище Scratch 3.0 побудоване за принципом конструктора: команди об'єднані у кольорові категорії, "
        "а алгоритм збирається шляхом з'єднання блоків між собою. Чітке розуміння розташування основних зон "
        "інтерфейсу дозволяє швидко знаходити потрібні інструменти та пояснювати будову вікна учням початкової школи."
    )
    add_scheme_image(doc, img_interface, "Рис. 1. Основні зони робочого інтерфейсу Scratch 3.0")

    # Підрозділ 2
    add_heading_2(doc, "2. Створення, редагування та збереження проєкту")
    add_body_p(doc, [
        ("Новий проєкт створюється командою ", "normal"),
        ("Файл -> Новий", "cmd"),
        (" (або ", "normal"),
        ("File -> New", "cmd"),
        ("). Для збереження результату на локальний диск використовують команду ", "normal"),
        ("Файл -> Вивантажити на ваш комп'ютер", "cmd"),
        (", після чого формується файл формату ", "normal"),
        (".sb3", "cmd"),
        (". Щоб продовжити роботу над збереженим проєктом, виконують ", "normal"),
        ("Файл -> Завантажити з вашого комп'ютера", "cmd"),
        (".", "normal")
    ])
    add_callout(doc, [
        ("Надавайте файлам зрозумілі імена без пробілів і випадкових символів, наприклад ", "normal"),
        ("PR10_Prizvyshche.sb3", "cmd"),
        (". Зберігайте проміжну версію проєкту після кожного завершеного етапу, щоб не втратити результати роботи.", "normal")
    ])

    # Підрозділ 3
    add_heading_2(doc, "3. Користування бібліотеками спрайтів, образів, тла та звуків")
    add_body_p(
        doc,
        "Scratch містить вбудовані бібліотеки готових мультимедійних ресурсів, згрупованих за тематичними "
        "категоріями (Тварини, Люди, Фантазія, Спорт, Музика тощо). Кожен об'єкт можна не лише обрати з бібліотеки, "
        "а й відредагувати у вбудованому графічному або аудіоредакторі, намалювати власноруч чи завантажити з комп'ютера."
    )
    add_scheme_image(doc, img_libraries, "Рис. 2. Основні бібліотеки ресурсів у Scratch 3.0")

    # Підрозділ 4
    add_heading_2(doc, "4. Координатна площина сцени та позиціонування спрайтів")
    add_body_p(doc, [
        ("Сцена Scratch має розмір ", "normal"),
        ("480 × 360", "bold"),
        (" умовних одиниць (пікселів). Її центр знаходиться в точці ", "normal"),
        ("(0; 0)", "cmd"),
        (". Горизонтальна вісь ", "normal"),
        ("X", "bold"),
        (" змінюється від ", "normal"),
        ("-240", "cmd"),
        (" (лівий край) до ", "normal"),
        ("240", "cmd"),
        (" (правий край), а вертикальна вісь ", "normal"),
        ("Y", "bold"),
        (" — від ", "normal"),
        ("-180", "cmd"),
        (" (нижній край) до ", "normal"),
        ("180", "cmd"),
        (" (верхній край). Для наочного тренування доречно тимчасово встановлювати бібліотечне тло ", "normal"),
        ("Xy-grid", "cmd"),
        (".", "normal")
    ])
    add_scheme_image(doc, img_coords, "Рис. 3. Координатна площина сцени Scratch", width_cm=15.5)

    # Підрозділ 5
    add_heading_2(doc, "5. Основні блоки переміщення за координатами")
    add_styled_table(
        doc,
        headers=["Блок команди", "Призначення", "Приклад використання"],
        rows=[
            [
                [("перемістити в x: 0 y: 0", "cmd")],
                "Миттєво встановлює спрайт у задану точку сцени",
                "Початкова позиція персонажа при старті проєкту"
            ],
            [
                [("ковзати 1 сек до x: 120 y: 90", "cmd")],
                "Плавно переміщує спрайт до вказаних координат за заданий час",
                "Плавний рух героя по маршруту без ривків"
            ],
            [
                [("змінити x на 50", "cmd")],
                "Зсуває спрайт горизонтально праворуч (+) або ліворуч (-)",
                "Кроковий рух по прямій лінії"
            ],
            [
                [("змінити y на -40", "cmd")],
                "Зсуває спрайт вертикально вгору (+) або вниз (-)",
                "Стрибок вгору або спуск вниз"
            ],
        ],
        col_widths_cm=[5.2, 6.0, 5.3]
    )

    # =========================================================================
    # ПОКРОКОВИЙ АЛГОРИТМ ВИКОНАННЯ РІЗНОРІВНЕВИХ ЗАВДАНЬ
    # =========================================================================
    add_heading_1(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    add_scheme_image(doc, img_levels, "Рис. 4. Розподіл завдань за рівнями складності")

    # Рівень 1
    add_heading_2(doc, "Рівень 1 — репродуктивний (≈ 7 хв)")
    add_body_p(
        doc,
        "Мета рівня: ознайомитися з інтерфейсом, підготувати робоче середовище, додати ресурси з бібліотек та зберегти базовий файл проєкту."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Дія студента", "Очікуваний результат"],
        rows=[
            [
                "1",
                [("Відкрийте середовище Scratch 3.0 та перевірте український інтерфейс (іконка глобуса -> ", "normal"), ("Українська", "cmd"), (").", "normal")],
                "Усі категорії блоків і меню відображаються українською мовою."
            ],
            [
                "2",
                "Видаліть стандартного спрайта (Рудого Кота) натисканням на значок кошика на панелі спрайтів.",
                "Сцена очищена від початкового персонажа."
            ],
            [
                "3",
                [("У бібліотеці тла оберіть координатну сітку ", "normal"), ("Xy-grid", "cmd"), (".", "normal")],
                "На сцені відображаються осі X, Y та координатні позначки."
            ],
            [
                "4",
                [("У бібліотеці спрайтів додайте будь-якого персонажа (наприклад, ", "normal"), ("Beetle", "cmd"), (" або ", "normal"), ("Cat Flying", "cmd"), (") та встановіть розмір ", "normal"), ("70", "cmd"), (".", "normal")],
                "Спрайт з'явився на сцені у зручному масштабі."
            ],
            [
                "5",
                [("Збережіть проєкт на комп'ютер під назвою ", "normal"), ("PR10_Prizvyshche.sb3", "cmd"), (".", "normal")],
                "Файл проєкту збережено у робочій папці."
            ],
        ],
        col_widths_cm=[1.5, 9.5, 5.5]
    )

    # Рівень 2
    add_heading_2(doc, "Рівень 2 — продуктивний (≈ 10 хв)")
    add_body_p(
        doc,
        "Мета рівня: створити алгоритм точного переміщення спрайта по чотирьох чвертях координатної площини з використанням блоків руху, подій та звуку."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Дія студента", "Блоки / параметри"],
        rows=[
            [
                "1",
                "Додайте точку старту алгоритму при натисканні на зелений прапорець і поверніть спрайт у центр сцени.",
                [("коли натиснуто зелений прапорець", "cmd"), ("\n", "normal"), ("перемістити в x: 0 y: 0", "cmd")]
            ],
            [
                "2",
                "Запрограмуйте плавний рух у I чверть, потім у II, III та IV чверті координатної площини.",
                [("ковзати 1 сек до x: 150 y: 100", "cmd"), ("\n", "normal"), ("ковзати 1 сек до x: -150 y: 100", "cmd"), ("\n", "normal"), ("ковзати 1 сек до x: -150 y: -100", "cmd"), ("\n", "normal"), ("ковзати 1 сек до x: 150 y: -100", "cmd")]
            ],
            [
                "3",
                "Поверніть спрайт у центр сцени та додайте коротку паузу між точками для наочності.",
                [("чекати 0.5 секунд", "cmd"), ("\n", "normal"), ("ковзати 1 сек до x: 0 y: 0", "cmd")]
            ],
            [
                "4",
                "Перейдіть на вкладку «Звуки», додайте звук із бібліотеки та відтворіть його після завершення маршруту.",
                [("відтворити звук Pop до кінця", "cmd")]
            ],
            [
                "5",
                "Запустіть скрипт, перевірте точність проходження вершин прямокутника та оновіть збережений файл.",
                [("Файл -> Вивантажити на ваш комп'ютер", "cmd")]
            ],
        ],
        col_widths_cm=[1.5, 7.8, 7.2]
    )

    # Рівень 3
    add_heading_2(doc, "Рівень 3 — творчий (≈ 10 хв)")
    add_body_p(
        doc,
        "Створіть власну інтерактивну мінісцену для уроку інформатики в початковій школі (наприклад, «Зустріч друзів у парку» "
        "або «Космічна подорож»), продемонструвавши охайну організацію робочого простору та точне позиціонування об'єктів."
    )
    add_styled_table(
        doc,
        headers=["Вимога до мінісцени", "Конкретний зміст виконання"],
        rows=[
            ["Тематичне тло", "Замініть координатну сітку на сюжетне тло з бібліотеки (або додайте перемикання тла)."],
            ["Два спрайти", "Додайте другого персонажа, задайте обом різні стартові координати (ліва та права частини сцени)."],
            ["Рух за координатами", "Організуйте плавне зближення спрайтів до заданих точок зустрічі без накладання один на одного."],
            ["Мультимедійний супровід", "Додайте короткі репліки (блок «говорити ... 2 сек») та щонайменше один звук із бібліотеки."],
            ["Акуратність проєкту", "Перейменуйте спрайти зрозумілими назвами, вирівняйте блоки в області скриптів, збережіть фінальний файл .sb3."],
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
            ["Рівень 1 (репродуктивний)", "Коректне налаштування інтерфейсу, додавання тла Xy-grid і спрайта, правильне збереження файлу .sb3.", "4"],
            ["Рівень 2 (продуктивний)", "Точне проходження всіх 4 координатних чвертей, повернення в центр (0; 0), коректне використання пауз і звуку.", "5"],
            ["Рівень 3 (творчий)", "Оригінальна мінісцена з 2 спрайтами, тематичним тлом, узгодженим рухом за координатами та звуковим супроводом.", "3"],
            ["Культура роботи з проєктом", "Охайна структура скриптів, зрозуміле іменування файлу та спрайтів, своєчасне оформлення звіту.", "1"],
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
        [("Файл виконаного проєкту у форматі ", "normal"), ("PR10_Prizvyshche.sb3", "cmd"), (".", "normal")],
        "Короткий електронний звіт (1–2 сторінки) зі скриншотом фінальної сцени та зібраних скриптів для кожного спрайта.",
        "Письмовий висновок (3–4 речення) про те, як наочність координатної сітки Scratch допомагає пояснювати поняття позиціонування учням початкової школи."
    ], style_name="List Bullet")

    output_docx = "Praktychne_zanyattya_10_Scratch.docx"
    doc.save(output_docx)
    print(f"Документ успішно створено: {output_docx}")
    print(f"Схеми (PNG + SVG) збережено у папці: {OUTPUT_DIR}/")


if __name__ == "__main__":
    build_document()