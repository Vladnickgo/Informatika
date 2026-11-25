import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ==============================================================================
# 1. НАЛАШТУВАННЯ ТА ГЕНЕРАЦІЯ СХЕМ (SVG + PNG у стилі Apple)
# ==============================================================================
os.makedirs("output", exist_ok=True)

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


def draw_rounded_card(ax, x, y, w, h, facecolor="#F5F5F7", edgecolor="#E5E5EA", lw=1.4, r=0.18, zorder=2):
    patch = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=zorder
    )
    ax.add_patch(patch)
    return patch


def generate_scheme_1_site_types():
    """Схема 1: Основні види вебсайтів за призначенням та функціоналом."""
    fig, ax = plt.subplots(figsize=(11, 5.4))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Заголовок схеми
    ax.text(
        5.5, 5.05, "Класифікація вебсайтів за цільовим призначенням",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color="#1D1D1F"
    )
    ax.text(
        5.5, 4.68, "Базові типи ресурсів у сучасному вебпросторі та освіті",
        ha="center", va="center", fontsize=11.5, color="#86868B"
    )

    cards_row1 = [
        {
            "title": "Сайт-візитка",
            "accent": "#0071E3",
            "desc": "1–5 сторінок\nПрезентація педагога,\nкласу чи закладу освіти",
            "x": 0.4
        },
        {
            "title": "Інтернет-магазин",
            "accent": "#248A3D",
            "desc": "Каталог, кошик, оплата\nОнлайн-продаж книг,\nрозвивальних ігор",
            "x": 3.9
        },
        {
            "title": "Блог / Медіа",
            "accent": "#C93400",
            "desc": "Хронологічні дописи\nМетодичні нотатки,\nпоради батькам учнів",
            "x": 7.4
        }
    ]

    cards_row2 = [
        {
            "title": "Вебпортал",
            "accent": "#6E30A8",
            "desc": "Багатосервісна система\nОсвітні платформи,\nбібліотеки, розклади",
            "x": 2.15
        },
        {
            "title": "Вебфорум / Спільнота",
            "accent": "#C4001D",
            "desc": "Гілки обговорень\nОбмін досвідом між\nвчителями та батьками",
            "x": 5.65
        }
    ]

    card_w = 3.2
    card_h = 1.85

    # Ряд 1
    for c in cards_row1:
        y = 2.45
        draw_rounded_card(ax, c["x"], y, card_w, card_h, r=0.18)
        # Кольорова акцентна смужка зверху
        draw_rounded_card(
            ax, c["x"] + 0.25, y + card_h - 0.14, card_w - 0.5, 0.07,
            facecolor=c["accent"], edgecolor="none", lw=0, r=0.03, zorder=3
        )
        ax.text(
            c["x"] + card_w / 2, y + 1.38, c["title"],
            ha="center", va="center", fontsize=13, fontweight="bold", color=c["accent"], zorder=4
        )
        ax.text(
            c["x"] + card_w / 2, y + 0.65, c["desc"],
            ha="center", va="center", fontsize=11, color="#1D1D1F", linespacing=1.35, zorder=4
        )

    # Ряд 2
    for c in cards_row2:
        y = 0.25
        draw_rounded_card(ax, c["x"], y, card_w, card_h, r=0.18)
        draw_rounded_card(
            ax, c["x"] + 0.25, y + card_h - 0.14, card_w - 0.5, 0.07,
            facecolor=c["accent"], edgecolor="none", lw=0, r=0.03, zorder=3
        )
        ax.text(
            c["x"] + card_w / 2, y + 1.38, c["title"],
            ha="center", va="center", fontsize=13, fontweight="bold", color=c["accent"], zorder=4
        )
        ax.text(
            c["x"] + card_w / 2, y + 0.65, c["desc"],
            ha="center", va="center", fontsize=11, color="#1D1D1F", linespacing=1.35, zorder=4
        )

    plt.savefig("output/scheme_1_site_types.png", dpi=220, bbox_inches="tight", pad_inches=0.15)
    plt.savefig("output/scheme_1_site_types.svg", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def generate_scheme_2_audience():
    """Схема 2: Сегментація цільової аудиторії (ЦА) освітнього вебсайту."""
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(
        5.5, 4.85, "Сегментація цільової аудиторії освітнього ресурсу",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color="#1D1D1F"
    )
    ax.text(
        5.5, 4.48, "Адаптація інтерфейсу, навігації та контенту під потреби користувачів",
        ha="center", va="center", fontsize=11.5, color="#86868B"
    )

    # Центральний верхній блок
    draw_rounded_card(ax, 3.3, 3.35, 4.4, 0.85, facecolor="#1D1D1F", edgecolor="none", r=0.18)
    ax.text(
        5.5, 3.77, "ЦІЛЬОВА АУДИТОРІЯ (ЦА)\nКритерії: вік, цифрові навички, мета візиту",
        ha="center", va="center", fontsize=11.5, fontweight="bold", color="#FFFFFF", linespacing=1.3
    )

    segments = [
        {
            "title": "Учні 1–4 класів",
            "accent": "#0071E3",
            "items": "• Великі кнопки та іконки\n• Мінімум суцільного тексту\n• Ігрові елементи, аудіо\n• Захист від реклами",
            "x": 0.35
        },
        {
            "title": "Батьки школярів",
            "accent": "#248A3D",
            "items": "• Швидкий доступ зі смартфона\n• Розклад, новини, оголошення\n• Чіткі інструкції та контакти\n• Прозорість та безпека даних",
            "x": 3.9
        },
        {
            "title": "Педагоги та методисти",
            "accent": "#6E30A8",
            "items": "• Зручний пошук та фільтри\n• Завантаження матеріалів\n• Обмін досвідом на форумі\n• Відповідність програмі НУШ",
            "x": 7.45
        }
    ]

    card_w = 3.2
    card_h = 2.45
    y_card = 0.3

    for seg in segments:
        cx = seg["x"] + card_w / 2
        # Стрілка від центрального блоку до сегмента
        ax.annotate(
            "", xy=(cx, y_card + card_h + 0.06), xytext=(5.5, 3.32),
            arrowprops=dict(arrowstyle="->", color="#86868B", lw=1.5, shrinkA=2, shrinkB=2),
            zorder=1
        )
        draw_rounded_card(ax, seg["x"], y_card, card_w, card_h, r=0.18)
        ax.text(
            cx, y_card + 2.08, seg["title"],
            ha="center", va="center", fontsize=12.5, fontweight="bold", color=seg["accent"]
        )
        ax.plot(
            [seg["x"] + 0.25, seg["x"] + card_w - 0.25],
            [y_card + 1.82, y_card + 1.82],
            color="#E5E5EA", lw=1.2
        )
        ax.text(
            seg["x"] + 0.22, y_card + 0.92, seg["items"],
            ha="left", va="center", fontsize=10.8, color="#1D1D1F", linespacing=1.42
        )

    plt.savefig("output/scheme_2_audience.png", dpi=220, bbox_inches="tight", pad_inches=0.15)
    plt.savefig("output/scheme_2_audience.svg", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def generate_scheme_3_workflow():
    """Схема 3: Етапи виконання самостійної роботи (флоу)."""
    fig, ax = plt.subplots(figsize=(11.5, 3.4))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 3.4)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(
        5.75, 3.05, "Алгоритм виконання самостійної роботи",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color="#1D1D1F"
    )

    steps = [
        {"num": "Етап 1", "title": "Теорія", "desc": "Опрацювання\nвидів сайтів\nі критеріїв ЦА", "color": "#0071E3"},
        {"num": "Етап 2", "title": "Відбір", "desc": "Пошук 5 сайтів\nрізних типів\nу браузері", "color": "#248A3D"},
        {"num": "Етап 3", "title": "Аналіз", "desc": "Оцінка UX,\nструктури та\nпортрета ЦА", "color": "#C93400"},
        {"num": "Етап 4", "title": "Таблиця", "desc": "Систематизація\nданих і перевірка\nетики дизайну", "color": "#6E30A8"},
        {"num": "Етап 5", "title": "Звіт", "desc": "Оформлення\nвисновків і\nзахист роботи", "color": "#C4001D"},
    ]

    w = 1.9
    h = 1.95
    gap = 0.35
    start_x = 0.3
    y = 0.45

    for idx, st in enumerate(steps):
        x = start_x + idx * (w + gap)
        draw_rounded_card(ax, x, y, w, h, r=0.18)
        # Бейдж номера етапу
        draw_rounded_card(
            ax, x + 0.35, y + h - 0.42, w - 0.7, 0.28,
            facecolor=st["color"], edgecolor="none", lw=0, r=0.1, zorder=3
        )
        ax.text(
            x + w / 2, y + h - 0.28, st["num"],
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#FFFFFF", zorder=4
        )
        ax.text(
            x + w / 2, y + 1.15, st["title"],
            ha="center", va="center", fontsize=12.5, fontweight="bold", color="#1D1D1F", zorder=4
        )
        ax.text(
            x + w / 2, y + 0.52, st["desc"],
            ha="center", va="center", fontsize=10.5, color="#86868B", linespacing=1.3, zorder=4
        )

        if idx < len(steps) - 1:
            ax.annotate(
                "",
                xy=(x + w + gap - 0.04, y + h / 2),
                xytext=(x + w + 0.04, y + h / 2),
                arrowprops=dict(arrowstyle="->", color="#86868B", lw=1.8),
                zorder=5
            )

    plt.savefig("output/scheme_3_workflow.png", dpi=220, bbox_inches="tight", pad_inches=0.15)
    plt.savefig("output/scheme_3_workflow.svg", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


generate_scheme_1_site_types()
generate_scheme_2_audience()
generate_scheme_3_workflow()

# ==============================================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ PYTHON-DOCX
# ==============================================================================
COLOR_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)    # #1F4E79 — основні заголовки
COLOR_SECONDARY = RGBColor(0x2E, 0x75, 0xB6)  # #2E75B6 — підзаголовки
COLOR_TEXT = RGBColor(0x00, 0x00, 0x00)       # Чорний основний текст
COLOR_CODE = RGBColor(0xC0, 0x39, 0x2B)       # #C0392B — моноширинні команди


def set_cell_shading(cell, color_hex):
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_callout_borders(cell, left_color_hex="1F4E79"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for border_name in ["top", "bottom", "right"]:
        border = OxmlElement(f"w:{border_name}")
        border.set(qn("w:val"), "none")
        tcBorders.append(border)
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "28")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), left_color_hex)
    tcBorders.append(left)
    tcPr.append(tcBorders)


def repeat_header_row(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)


def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.color.rgb = COLOR_TEXT

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


def format_run(run, bold=False, italic=False, color=COLOR_TEXT, size=14, font_name="Times New Roman"):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def add_mixed_paragraph(container, segments, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=5, space_before=0, left_indent=0.0):
    """
    segments — список кортежів: (текст, стиль)
    стиль: 'normal', 'bold', 'italic', 'bold_italic', 'code'
    """
    p = container.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if left_indent:
        p.paragraph_format.left_indent = Cm(left_indent)

    for text, style in segments:
        run = p.add_run(text)
        if style == "bold":
            format_run(run, bold=True)
        elif style == "italic":
            format_run(run, italic=True)
        elif style == "bold_italic":
            format_run(run, bold=True, italic=True)
        elif style == "code":
            format_run(run, bold=False, color=COLOR_CODE, size=13, font_name="Consolas")
        else:
            format_run(run)
    return p


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    format_run(run, bold=True, color=COLOR_PRIMARY, size=14)
    return p


def add_subsection_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    format_run(run, bold=True, color=COLOR_SECONDARY, size=14)
    return p


def add_bullet_item(doc, segments):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(1.0)
    for text, style in segments:
        run = p.add_run(text)
        if style == "bold":
            format_run(run, bold=True)
        elif style == "italic":
            format_run(run, italic=True)
        elif style == "code":
            format_run(run, color=COLOR_CODE, size=13, font_name="Consolas")
        else:
            format_run(run)
    return p


def add_numbered_item(doc, segments):
    p = doc.add_paragraph(style="List Number")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(1.0)
    for text, style in segments:
        run = p.add_run(text)
        if style == "bold":
            format_run(run, bold=True)
        elif style == "italic":
            format_run(run, italic=True)
        elif style == "code":
            format_run(run, color=COLOR_CODE, size=13, font_name="Consolas")
        else:
            format_run(run)
    return p


def numbered_paren(doc, index, segments):
    """Нумерований список у форматі 1), 2), 3)... з відступом 1,0 см."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-0.5)

    r_num = p.add_run(f"{index}) ")
    format_run(r_num, bold=True)

    for text, style in segments:
        run = p.add_run(text)
        if style == "bold":
            format_run(run, bold=True)
        elif style == "italic":
            format_run(run, italic=True)
        elif style == "code":
            format_run(run, color=COLOR_CODE, size=13, font_name="Consolas")
        else:
            format_run(run)
    return p


def add_callout(doc, segments, bg_hex="EDF4FB", border_hex="1F4E79"):
    """Callout-блок без службових заголовків — лише змістовний текст."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Cm(16.5)

    cell = table.cell(0, 0)
    cell.width = Cm(16.5)
    set_cell_shading(cell, bg_hex)
    set_callout_borders(cell, border_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=160)
    prevent_row_split(table.rows[0])

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    for text, style in segments:
        run = p.add_run(text)
        if style == "bold":
            format_run(run, bold=True)
        elif style == "italic":
            format_run(run, italic=True)
        elif style == "code":
            format_run(run, color=COLOR_CODE, size=13, font_name="Consolas")
        else:
            format_run(run)

    # Невеликий відступ після таблиці
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)
    spacer.paragraph_format.line_spacing = 1.0


def add_styled_table(doc, headers, rows_data, col_widths_cm):
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Заголовковий рядок
    hdr_row = table.rows[0]
    repeat_header_row(hdr_row)
    prevent_row_split(hdr_row)

    for j, h_text in enumerate(headers):
        cell = hdr_row.cells[j]
        cell.width = Cm(col_widths_cm[j])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, "1F4E79")
        set_cell_margins(cell, top=100, bottom=100, left=110, right=110)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h_text)
        format_run(run, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), size=13)

    # Рядки даних
    for i, r_data in enumerate(rows_data):
        row = table.rows[i + 1]
        prevent_row_split(row)
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"

        for j, cell_content in enumerate(r_data):
            cell = row.cells[j]
            cell.width = Cm(col_widths_cm[j])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=85, bottom=85, left=110, right=110)

            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (j == 0 and len(str(cell_content)) <= 6) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)

            if isinstance(cell_content, list):
                for text, style in cell_content:
                    run = p.add_run(text)
                    if style == "bold":
                        format_run(run, bold=True, size=13)
                    elif style == "italic":
                        format_run(run, italic=True, size=13)
                    elif style == "code":
                        format_run(run, color=COLOR_CODE, size=12, font_name="Consolas")
                    else:
                        format_run(run, size=13)
            else:
                run = p.add_run(str(cell_content))
                format_run(run, size=13)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)
    spacer.paragraph_format.line_spacing = 1.0
    return table


def add_picture_block(doc, img_path, caption_text, width_cm=15.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(6)
    p_cap.paragraph_format.line_spacing = 1.15
    run_cap = p_cap.add_run(caption_text)
    format_run(run_cap, italic=True, size=12, color=RGBColor(0x4A, 0x55, 0x68))


# ==============================================================================
# 3. ФОРМУВАННЯ DOCX-ДОКУМЕНТА
# ==============================================================================
doc = Document()

# Налаштування полів сторінки (A4: 21.0 x 29.7 см -> робоча ширина 16.5 см)
section = doc.sections[0]
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
normal_style.font.color.rgb = COLOR_TEXT

# --- ЗАГОЛОВОК ТА ТЕМА ---
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.line_spacing = 1.15
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
r_title = p_title.add_run("САМОСТІЙНА РОБОТА № 14")
format_run(r_title, bold=True, color=COLOR_PRIMARY, size=14)

p_topic = doc.add_paragraph()
p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_topic.paragraph_format.line_spacing = 1.15
p_topic.paragraph_format.space_before = Pt(0)
p_topic.paragraph_format.space_after = Pt(8)
r_topic = p_topic.add_run("Тема: Види сайтів та цільова аудиторія")
format_run(r_topic, bold=True, color=COLOR_TEXT, size=14)

# --- МЕТА ---
add_mixed_paragraph(doc, [
    ("Мета: ", "bold"),
    ("формувати знання про основні види сайтів (сайт-візитка, інтернет-магазин, блог, вебпортал, форум), навчитися визначати та аналізувати цільову аудиторію вебресурсу; розвивати маркетингове мислення, уміння сегментувати аудиторію, навички критичного аналізу освітніх та комерційних сайтів; виховувати усвідомлення відповідальності розробника та педагога перед користувачами, дотримання принципів етичності й безпеки вебдизайну.", "normal")
])

# --- ОБЛАДНАННЯ ---
add_section_heading(doc, "Обладнання та програмне забезпечення")
numbered_paren(doc, 1, [("Персональний комп’ютер або ноутбук із підключенням до мережі Інтернет.", "normal")])
numbered_paren(doc, 2, [("Веббраузер (Google Chrome, Mozilla Firefox або Microsoft Edge) з інструментами розробника (", "normal"), ("DevTools", "code"), (").", "normal")])
numbered_paren(doc, 3, [("Текстовий процесор (Microsoft Word, LibreOffice Writer або Google Документи) для оформлення звіту.", "normal")])
numbered_paren(doc, 4, [("Інструкційні картки до самостійної роботи № 14.", "normal")])

# --- ЛІТЕРАТУРА ---
add_section_heading(doc, "Література")
add_numbered_item(doc, [("Юнчик В. Л. Системне, прикладне програмне забезпечення та хмарні технології в освіті : конспект лекцій для студентів спеціальності 014.09 Середня освіта (Інформатика) першого (бакалаврського) рівня. Волин. нац. ун-т ім. Лесі Українки. Луцьк : ВНУ імені Лесі Українки, 2024. 162 с.", "normal")])
add_numbered_item(doc, [("Анісімов А. В., Кулябко П. П. Інформаційні системи та бази даних : навч. посіб. для студ. ф-ту комп’ютер. наук та кібернетики. Київ, 2017. 110 с.", "normal")])
add_numbered_item(doc, [("Буйницька О. П. Інформаційні технології та технічні засоби навчання : навч. посіб. Київ : Центр навчальної літератури, 2019. 240 с.", "normal")])

# --- ЗАВДАННЯ САМОСТІЙНОЇ РОБОТИ ---
add_section_heading(doc, "Завдання самостійної роботи")
add_numbered_item(doc, [("Опрацювати теоретичний матеріал щодо класифікації вебсайтів за призначенням, функціональними можливостями та структурою.", "normal")])
add_numbered_item(doc, [("Засвоїти методику визначення та сегментації цільової аудиторії (ЦА) за демографічними, поведінковими та освітніми критеріями.", "normal")])
add_numbered_item(doc, [("Дібрати 5 діючих вебресурсів різних типів (у тому числі освітнього спрямування для початкової школи) та провести їхній порівняльний аналіз за інструкційною карткою.", "normal")])
add_numbered_item(doc, [("Скласти узагальнений портрет цільової аудиторії (персону користувача) для персонального блогу або сайту-візитки вчителя початкових класів.", "normal")])
add_numbered_item(doc, [("Оцінити обрані ресурси з погляду етичності вебдизайну, цифрової безпеки дітей та інклюзивності інтерфейсу.", "normal")])
add_numbered_item(doc, [("Оформити результати дослідження у вигляді структурованого електронного звіту та дати письмові відповіді на питання для самоперевірки.", "normal")])

# --- ТЕРМІНИ ВИКОНАННЯ ---
add_section_heading(doc, "Терміни виконання")
add_mixed_paragraph(doc, [
    ("Робота виконується в позааудиторний час відповідно до графіка навчального процесу. Оформлений звіт подається викладачу в електронному або друкованому вигляді до початку наступного практичного заняття за розкладом.", "normal")
])

# --- ОЧІКУВАНІ РЕЗУЛЬТАТИ ---
add_section_heading(doc, "Очікувані результати")
add_bullet_item(doc, [("розрізняє основні типи вебсайтів за їхньою структурою, навігацією та ключовими завданнями;", "normal")])
add_bullet_item(doc, [("визначає ядро та непрямі сегменти цільової аудиторії конкретного вебресурсу;", "normal")])
add_bullet_item(doc, [("обґрунтовує вибір кольорової гами, шрифтів та архітектури сайту відповідно до вікових особливостей учнів початкової школи та їхніх батьків;", "normal")])
add_bullet_item(doc, [("виявляє маніпулятивні елементи інтерфейсу (темні патерни) та оцінює дотримання етичних норм у вебпросторі.", "normal")])

# --- ПЕРЕЛІК ОПРАЦЬОВУВАНИХ ПИТАНЬ ---
add_section_heading(doc, "Перелік опрацьовуваних питань")
add_numbered_item(doc, [("Поняття вебсайту як інформаційної системи; відмінність між вебсторінкою, вебсайтом та вебзастосунком.", "normal")])
add_numbered_item(doc, [("Класифікація вебсайтів за призначенням: сайт-візитка, лендінг, корпоративний сайт, інтернет-магазин.", "normal")])
add_numbered_item(doc, [("Інформаційно-комунікаційні ресурси: тематичний блог, новинне медіа, освітній вебпортал, вебфорум.", "normal")])
add_numbered_item(doc, [("Поняття цільової аудиторії (ЦА) та її роль у проєктуванні інтерфейсу користувача (UI/UX).", "normal")])
add_numbered_item(doc, [("Критерії сегментації цільової аудиторії: географічні, соціально-демографічні, психографічні та поведінкові.", "normal")])
add_numbered_item(doc, [("Методика створення «персони користувача» (User Persona) для освітнього вебресурсу.", "normal")])
add_numbered_item(doc, [("Особливості сприйняття вебінтерфейсу дітьми молодшого шкільного віку (6–10 років).", "normal")])
add_numbered_item(doc, [("Етичність вебдизайну: цифрова доступність (інклюзивність), захист персональних даних та відмова від маніпулятивних патернів.", "normal")])

# --- ТЕОРЕТИЧНІ ВІДОМОСТІ ---
add_section_heading(doc, "Теоретичні відомості (стислий огляд)")

add_subsection_heading(doc, "1. Сайт як цільовий інструмент комунікації")
add_mixed_paragraph(doc, [
    ("Вебсайт — це сукупність логічно пов’язаних між собою вебсторінок, об’єднаних спільним доменним ім’ям, дизайном та цільовим призначенням. У педагогічній практиці сайт можна порівняти зі шкільним інформаційним стендом або кабінетом: якщо стенд у коридорі містить лише розклад і контакти (сайт-візитка), то шкільна бібліотека з каталогом, читальним залом та гуртками нагадує повноцінний освітній портал. Ефективність будь-якого ресурсу визначається тим, наскільки точно його структура відповідає завданням власника та очікуванням відвідувачів.", "normal")
])

add_subsection_heading(doc, "2. Основні види вебсайтів та їхні характерні ознаки")
add_mixed_paragraph(doc, [
    ("Залежно від функціоналу, обсягу контенту та способу взаємодії з користувачем виділяють п’ять базових типів сайтів, найпоширеніших у повсякденній та освітній діяльності:", "normal")
])

add_bullet_item(doc, [("Сайт-візитка — компактний ресурс (зазвичай 1–5 сторінок), що містить ключові відомості про особу, проєкт або заклад: напрями діяльності, портфоліо, досягнення та форму зворотного зв’язку. Приклад у школі: персональна сторінка вчителя початкових класів або сайт класної спільноти.", "normal")])
add_bullet_item(doc, [("Інтернет-магазин — комерційна платформа для дистанційного продажу товарів чи послуг. Обов’язкові елементи: структурований каталог із фільтрами, картки товарів, кошик, модуль онлайн-оплати та вибору доставки. У шкільному контексті це ресурси для замовлення друкованих робочих зошитів, конструкторів або дидактичних ігор.", "normal")])
add_bullet_item(doc, [("Блог — вебресурс, основою якого є регулярно оновлювані записи (пости), розташовані у зворотному хронологічному порядку. Блог передбачає авторський стиль викладу, рубрикатор за темами та можливість коментування. Учителі використовують блоги для публікації сценаріїв уроків, лайфхаків для батьків першокласників і фотозвітів.", "normal")])
add_bullet_item(doc, [("Вебпортал — масштабний багатосервісний ресурс, який об’єднує великий обсяг різнопланової інформації та інтерактивних сервісів в єдиній точці входу (особистий кабінет, електронний щоденник, бібліотека мультимедійних вправ, тестування). Прикладом є державні освітні платформи («Всеукраїнська школа онлайн», «Нова українська школа»).", "normal")])
add_bullet_item(doc, [("Вебфорум — платформа для тематичного спілкування користувачів, побудована за ієрархією «розділ → тема → гілка повідомлень». На відміну від блогу, контент на форумі створюють самі учасники спільноти, обмінюючись методичними порадами чи обговорюючи навчальні програми.", "normal")])

add_picture_block(
    doc,
    "output/scheme_1_site_types.png",
    "Рис. 1. Класифікація основних видів вебсайтів за цільовим призначенням та освітнім застосуванням"
)

# Зведена таблиця типів сайтів
add_styled_table(
    doc,
    ["Тип сайту", "Обсяг і структура", "Ключовий функціонал", "Освітній приклад"],
    [
        [
            [("Сайт-візитка", "bold")],
            "1–5 сторінок, лінійна навігація",
            "Презентація, контакти, портфоліо",
            "Сайт-портфоліо вчителя початкових класів"
        ],
        [
            [("Інтернет-магазин", "bold")],
            "Багаторівневий каталог товарів",
            "Пошук, фільтри, кошик, еквайринг",
            "Магазин дидактичних матеріалів НУШ"
        ],
        [
            [("Блог", "bold")],
            "Стрічка дописів, теги, архів",
            "Публікація статей, коментарі, підписка",
            "Методичний блог класовода для батьків"
        ],
        [
            [("Вебпортал", "bold")],
            "Розгалужена екосистема сервісів",
            "Авторизація, бази даних, інтерактив",
            "Освітній портал «На Урок» або «Освіта.ua»"
        ],
        [
            [("Вебфорум", "bold")],
            "Категорії та гілки обговорень",
            "Реєстрація, створення тем, модерація",
            "Професійна спільнота педагогів України"
        ]
    ],
    [3.5, 4.0, 4.5, 4.5]
)

add_subsection_heading(doc, "3. Цільова аудиторія та її сегментація")
add_mixed_paragraph(doc, [
    ("Цільова аудиторія (ЦА) — це група реальних або потенційних користувачів, на задоволення інформаційних, освітніх чи споживчих потреб яких орієнтований вебсайт. Спроба створити «сайт для всіх» зазвичай призводить до того, що ресурс стає незручним для кожного: першокласник губиться у складних меню, а методист не знаходить потрібних документів за яскравою анімацією.", "normal")
])
add_mixed_paragraph(doc, [
    ("Для точного проєктування застосовують сегментацію ЦА — поділ усіх відвідувачів на однорідні групи за чотирма ознаками: географічною (регіон, мова спілкування), соціально-демографічною (вік, роль — учень, батько/мати, учитель), поведінковою (частота візитів, тип пристрою — смартфон чи ПК) та психографічною (інтереси, рівень цифрової грамотності, мотивація).", "normal")
])

add_picture_block(
    doc,
    "output/scheme_2_audience.png",
    "Рис. 2. Сегментація цільової аудиторії освітнього вебресурсу та вимоги до інтерфейсу"
)

add_subsection_heading(doc, "4. Етичність вебдизайну та відповідальність перед аудиторією")
add_mixed_paragraph(doc, [
    ("Проєктування сайтів, особливо тих, якими користуються діти молодшого шкільного віку, вимагає суворого дотримання професійної етики. Неприпустимим є використання «темних патернів» (Dark Patterns) — елементів інтерфейсу, що змушують користувача виконати небажану дію (приховані підписки, замаскована реклама під кнопку «Завантажити», нав’язливі спливаючі вікна).", "normal")
])

add_callout(doc, [
    ("Етичний вебдизайн для дитячої та освітньої аудиторії базується на трьох принципах: ", "bold"),
    ("1) інклюзивність (контрастність тексту, зрозумілі підписи до кнопок, коректна робота з клавіатури та скрінрідерами); 2) цифрова гігієна (відсутність агресивної банерної реклами та збору надлишкових персональних даних неповнолітніх); 3) когнітивна доступність (структуровані короткі абзаци, візуальні підказки та передбачувана навігація).", "normal")
])

# --- ЕТАПИ ВИКОНАННЯ САМОСТІЙНОЇ РОБОТИ ---
add_section_heading(doc, "Етапи виконання самостійної роботи")
add_mixed_paragraph(doc, [
    ("Для раціонального розподілу часу дотримуйтеся наведеної послідовності дій під час виконання завдання:", "normal")
])

add_picture_block(
    doc,
    "output/scheme_3_workflow.png",
    "Рис. 3. Послідовність етапів виконання самостійної роботи № 14"
)

# --- ІНСТРУКЦІЙНА КАРТКА ПРАКТИЧНОГО ЗАВДАННЯ ---
add_section_heading(doc, "Інструкційна картка практичного завдання")
add_mixed_paragraph(doc, [
    ("Виконайте покроковий аналіз вебресурсів у браузері та зафіксуйте результати у робочому звіті.", "normal")
])

add_styled_table(
    doc,
    ["Крок", "Дія студента", "Інструмент / Команда", "Результат виконання"],
    [
        [
            "1",
            "Відкрийте веббраузер та оберіть по 1 реальному сайту кожного з 5 типів (візитка, інтернет-магазин, блог, портал, форум), надаючи перевагу освітній або дитячій тематиці.",
            [("Браузер, адресний рядок ", "normal"), ("Ctrl + L", "code")],
            "Сформовано список із 5 активних URL-адрес для дослідження."
        ],
        [
            "2",
            "Дослідіть структуру головної сторінки, навігаційне меню, наявність пошуку, форм реєстрації та інтерактивних модулів кожного сайту.",
            [("Перегляд коду / інспектор ", "normal"), ("Ctrl + Shift + I", "code")],
            "Визначено типові функціональні блоки, що підтверджують вид сайту."
        ],
        [
            "3",
            "Перевірте адаптивність інтерфейсу для мобільних пристроїв (режим емуляції смартфона в інструментах розробника).",
            [("DevTools → ", "normal"), ("Ctrl + Shift + M", "code")],
            "Оцінено зручність перегляду ресурсу батьками та учнями зі смартфона."
        ],
        [
            "4",
            "Визначте ядро цільової аудиторії кожного сайту: вік, соціальну роль, рівень цифрових навичок та головну мету відвідування.",
            "Аналітична таблиця звіту",
            "Заповнено графи щодо сегментації ЦА для всіх 5 ресурсів."
        ],
        [
            "5",
            "Проведіть аудит етичності: перевірте наявність нав’язливої реклами, спливаючих вікон, політики конфіденційності та зручності читання шрифтів.",
            "Візуальний огляд інтерфейсу",
            "Сформульовано висновок про етичність і безпечність кожного сайту."
        ],
        [
            "6",
            "Складіть мініпортрет (User Persona) для уявного блогу вчителя 2-го класу: опишіть 2 сегменти (батьки та учні) і запропонуйте 4 вимоги до дизайну.",
            "Текстовий процесор",
            "Розроблено текстову модель структури та оформлення педагогічного блогу."
        ]
    ],
    [1.3, 6.2, 4.2, 4.8]
)

# --- ЗАВДАННЯ НА ЗАПОВНЕННЯ ТАБЛИЦІ ---
add_section_heading(doc, "Завдання на заповнення порівняльної таблиці")
add_mixed_paragraph(doc, [
    ("Перенесіть наведену нижче таблицю у звіт та заповніть її на основі аналізу 5 обраних вебресурсів (перший рядок наведено як зразок оформлення):", "normal")
])

add_styled_table(
    doc,
    ["Вид сайту та назва (URL)", "Ключові елементи функціоналу", "Ядро цільової аудиторії (вік, роль, мета)", "Оцінка етичності та зручності (UX)"],
    [
        [
            [("Освітній портал\n", "bold"), ("«Нова українська школа» (nus.org.ua)", "italic")],
            "Рубрикатор статей, нормативна база, медіатека, пошук за тегами, підписка на дайджест",
            "Вчителі початкової школи, керівники ЗЗСО, батьки (25–55 років); мета — методична підтримка та новини реформи",
            "Висока читабельність, відсутня агресивна реклама, чітка ієрархія заголовків"
        ],
        [
            "1. Сайт-візитка:\n...",
            "...",
            "...",
            "..."
        ],
        [
            "2. Інтернет-магазин:\n...",
            "...",
            "...",
            "..."
        ],
        [
            "3. Тематичний блог:\n...",
            "...",
            "...",
            "..."
        ],
        [
            "4. Освітній портал:\n...",
            "...",
            "...",
            "..."
        ],
        [
            "5. Вебфорум:\n...",
            "...",
            "...",
            "..."
        ]
    ],
    [3.8, 4.2, 4.5, 4.0]
)

# --- ТЕОРЕТИЧНІ ПИТАННЯ ДЛЯ САМОПЕРЕВІРКИ ---
add_section_heading(doc, "Теоретичні питання для самоперевірки")
add_numbered_item(doc, [("У чому полягає принципова різниця між сайтом-візиткою та вебпорталом за структурою та призначенням?", "normal")])
add_numbered_item(doc, [("Які обов’язкові функціональні модулі відрізняють інтернет-магазин від інформаційного каталогу?", "normal")])
add_numbered_item(doc, [("Чому зворотний хронологічний порядок публікацій є характерною ознакою блогу?", "normal")])
add_numbered_item(doc, [("Яким чином організована взаємодія користувачів на вебфорумі та яка роль модератора?", "normal")])
add_numbered_item(doc, [("Що таке цільова аудиторія вебсайту і чому її потрібно визначати до початку розробки дизайну?", "normal")])
add_numbered_item(doc, [("Назвіть чотири основні групи критеріїв сегментації цільової аудиторії та наведіть приклади для шкільного сайту.", "normal")])
add_numbered_item(doc, [("Як вікові особливості учнів 1–4 класів впливають на вибір розміру шрифту, навігації та ілюстрацій на сайті?", "normal")])
add_numbered_item(doc, [("Що означає поняття «персона користувача» (User Persona) у вебпроєктуванні?", "normal")])
add_numbered_item(doc, [("Наведіть 2–3 приклади «темних патернів» у вебдизайні та поясніть, чому вони є неетичними.", "normal")])
add_numbered_item(doc, [("Яких вимог цифрової безпеки та інклюзивності має дотримуватися вчитель, створюючи власний освітній вебресурс?", "normal")])

# --- РЕКОМЕНДАЦІЇ ДО ОФОРМЛЕННЯ ЗВІТУ ---
add_section_heading(doc, "Рекомендації до оформлення звіту")
add_bullet_item(doc, [("Формат документа: файл ", "normal"), (".docx", "code"), (" або ", "normal"), (".pdf", "code"), (", назва файлу — ", "normal"), ("SR14_Prizvyshche_Imya.docx", "code"), (".", "normal")])
add_bullet_item(doc, [("Параметри сторінки: формат А4, шрифт Times New Roman, кегль 14 pt, міжрядковий інтервал 1,15, вирівнювання основного тексту за шириною.", "normal")])
add_bullet_item(doc, [("Обов’язкові структурні елементи звіту: титульна сторінка (або шапка роботи), заповнена порівняльна таблиця 5 вебресурсів, опис портрета цільової аудиторії блогу вчителя, стислі письмові відповіді на 10 питань для самоперевірки та загальний висновок.", "normal")])
add_bullet_item(doc, [("Для підтвердження аналізу бажано додати 2–3 скріншоти досліджених сайтів із власними поясненнями елементів інтерфейсу.", "normal")])

# --- КРИТЕРІЇ ОЦІНЮВАННЯ ---
add_section_heading(doc, "Критерії оцінювання")
add_styled_table(
    doc,
    ["Показник оцінювання", "Критерії нарахування балів", "Макс. бал"],
    [
        [
            "Теоретична підготовка та відповіді на питання для самоперевірки",
            "Повні, термінологічно грамотні відповіді на всі 10 питань з наведенням власних прикладів — 3 б.; часткові відповіді або неточності — 1–2 б.",
            "3"
        ],
        [
            "Добір та порівняльний аналіз 5 видів вебсайтів",
            "Коректно дібрано всі 5 типів сайтів, аргументовано описано їхній функціонал і сегменти ЦА в таблиці — 4 б.; проаналізовано 3–4 сайти або поверхнево — 2–3 б.",
            "4"
        ],
        [
            "Розробка моделі цільової аудиторії для освітнього блогу",
            "Детально описано сегменти (учні, батьки), обґрунтовано вимоги до UX/UI та структури контенту — 3 б.; загальний опис без урахування вікових особливостей — 1–2 б.",
            "3"
        ],
        [
            "Аудит етичності дизайну, культура оформлення звіту та своєчасність",
            "Здійснено перевірку ресурсів на етичність та інклюзивність, звіт оформлено охайно згідно з вимогами і подано вчасно — 2 б.; наявні огріхи оформлення — 1 б.",
            "2"
        ],
        [
            [("Разом за самостійну роботу", "bold")],
            [("Максимальна сума балів за 12-бальною шкалою оцінювання", "bold")],
            [("12", "bold")]
        ]
    ],
    [4.8, 9.2, 2.5]
)

output_filename = "Samostiyna_robota_14_Vydy_saytiv_ta_CA.docx"
doc.save(output_filename)
print(f"Документ успішно створено: {output_filename}")
print("Згенеровані схеми (PNG + SVG) збережено у папці: output/")