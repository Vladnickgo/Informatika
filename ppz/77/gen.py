import os
import re
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
# 1. ГЕНЕРАЦІЯ СХЕМ (SVG + PNG у стилі Apple)
# ==============================================================================
os.makedirs("output", exist_ok=True)

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

BG_CARD = "#F5F5F7"
BORDER_CARD = "#E5E5EA"
TEXT_DARK = "#1D1D1F"
TEXT_GRAY = "#515154"
ACCENT_BLUE = "#0071E3"
ACCENT_GREEN = "#248A3D"
ACCENT_ORANGE = "#C93400"
ACCENT_PURPLE = "#6E30A8"
TERM_BG = "#1C1C1E"
TERM_PROMPT = "#30D158"
TERM_WHITE = "#FFFFFF"
TERM_GRAY = "#D1D1D6"


def save_diagram(fig, name):
    png_path = os.path.join("output", f"{name}.png")
    svg_path = os.path.join("output", f"{name}.svg")
    fig.savefig(png_path, dpi=220, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)
    return png_path


def draw_apple_card(ax, x, y, w, h, accent, badge_text, title, lines):
    card = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        facecolor=BG_CARD,
        edgecolor=BORDER_CARD,
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(card)

    badge_w = w - 0.5
    badge_h = 0.42
    badge_x = x + 0.25
    badge_y = y + h - 0.62
    badge = FancyBboxPatch(
        (badge_x, badge_y), badge_w, badge_h,
        boxstyle="round,pad=0.01,rounding_size=0.14",
        facecolor=accent,
        edgecolor="none",
        zorder=3
    )
    ax.add_patch(badge)
    ax.text(
        x + w / 2, badge_y + badge_h / 2, badge_text,
        ha="center", va="center", fontsize=11.0, fontweight="bold",
        color="white", zorder=4
    )

    ax.text(
        x + w / 2, badge_y - 0.36, title,
        ha="center", va="center", fontsize=12.5, fontweight="bold",
        color=TEXT_DARK, zorder=4
    )

    start_y = badge_y - 0.82
    step_y = 0.44
    for idx, line in enumerate(lines):
        ax.text(
            x + w / 2, start_y - idx * step_y, line,
            ha="center", va="center", fontsize=11.0,
            color=TEXT_GRAY, zorder=4
        )


def create_scheme1():
    fig, ax = plt.subplots(figsize=(13.5, 4.5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    ax.text(
        8.0, 4.82,
        "Шлях публікації веб-сайту: від локального ПК до браузера учня",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=TEXT_DARK
    )

    cards = [
        (0.4, ACCENT_BLUE, "1. РОЗРОБКА", "Локальний ПК",
         ["HTML5, CSS3, JS", "Папка проєкту", "Головна index.html"]),
        (4.35, ACCENT_PURPLE, "2. ПЕРЕДАЧА", "Клієнт передачі",
         ["FileZilla (FTP/SFTP)", "Веб-менеджер файлів", "або Git-репозиторій"]),
        (8.3, ACCENT_GREEN, "3. ЗБЕРІГАННЯ", "Сервер хостингу",
         ["Каталог public_html", "Робота сервера 24/7", "Доменне ім’я (DNS)"]),
        (12.25, ACCENT_ORANGE, "4. ПЕРЕГЛЯД", "Браузер учня",
         ["Запит за URL-адресою", "Рендеринг сторінки", "ПК, планшет, смартфон"]),
    ]

    card_w = 3.35
    card_h = 3.55
    card_y = 0.55

    for idx, (cx, acc, bdg, ttl, lns) in enumerate(cards):
        draw_apple_card(ax, cx, card_y, card_w, card_h, acc, bdg, ttl, lns)
        if idx < len(cards) - 1:
            x_start = cx + card_w + 0.08
            x_end = cards[idx + 1][0] - 0.08
            y_mid = card_y + card_h / 2
            ax.annotate(
                "", xy=(x_end, y_mid), xytext=(x_start, y_mid),
                arrowprops=dict(arrowstyle="->,head_width=0.28,head_length=0.28",
                                color=ACCENT_BLUE, lw=2.0),
                zorder=5
            )

    return save_diagram(fig, "scheme1_web_hosting")


def create_scheme2():
    fig, ax = plt.subplots(figsize=(13.5, 5.2))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    ax.text(
        8.0, 5.82,
        "Взаємодія технологій HTML5, CSS3 та JavaScript в освітньому веб-проєкті",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=TEXT_DARK
    )

    cards = [
        (0.45, ACCENT_ORANGE, "HTML5 • СТРУКТУРА", "Каркас сторінки",
         ["Теги <header>, <main>, <footer>", "Заголовки, правила, списки", "Кнопки та ілюстрації для учнів"]),
        (5.7, ACCENT_BLUE, "CSS3 • ОФОРМЛЕННЯ", "Візуальний стиль",
         ["Кольорова палітра та контраст", "Великі читабельні шрифти", "Адаптивна сітка карток"]),
        (10.95, ACCENT_GREEN, "JS • ПОВЕДІНКА", "Інтерактивність",
         ["Перевірка відповідей у тесті", "Миттєвий підрахунок балів", "Зміна теми чи розміру тексту"]),
    ]

    card_w = 4.6
    card_h = 3.05
    card_y = 2.25

    for cx, acc, bdg, ttl, lns in cards:
        draw_apple_card(ax, cx, card_y, card_w, card_h, acc, bdg, ttl, lns)
        mid_x = cx + card_w / 2
        ax.annotate(
            "", xy=(mid_x, 1.65), xytext=(mid_x, card_y - 0.06),
            arrowprops=dict(arrowstyle="->,head_width=0.26,head_length=0.25",
                            color=acc, lw=2.0),
            zorder=5
        )

    term = FancyBboxPatch(
        (0.45, 0.35), 15.1, 1.22,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        facecolor=TERM_BG,
        edgecolor="#3A3A3C",
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(term)
    ax.text(
        0.85, 1.15, "~/edu-site $",
        ha="left", va="center", fontsize=12.0, fontweight="bold",
        family="monospace", color=TERM_PROMPT, zorder=4
    )
    ax.text(
        2.95, 1.15, "index.html  +  css/style.css  +  js/script.js",
        ha="left", va="center", fontsize=12.0, fontweight="bold",
        family="monospace", color=TERM_WHITE, zorder=4
    )
    ax.text(
        8.0, 0.65,
        "Єдина інтерактивна освітня веб-сторінка вчителя початкової школи",
        ha="center", va="center", fontsize=11.5, color=TERM_GRAY, zorder=4
    )

    return save_diagram(fig, "scheme2_html_css_js")


def create_scheme3():
    fig, ax = plt.subplots(figsize=(13.5, 5.1))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6.0)
    ax.axis("off")

    ax.text(
        8.0, 5.65,
        "Файлова структура проєкту та способи завантаження на сервер хостингу",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=TEXT_DARK
    )

    term = FancyBboxPatch(
        (0.45, 0.45), 6.85, 4.75,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        facecolor=TERM_BG,
        edgecolor="#3A3A3C",
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(term)

    ax.text(
        0.8, 4.82, "Корінь сайту: public_html/",
        ha="left", va="center", fontsize=12.5, fontweight="bold",
        family="monospace", color=TERM_PROMPT, zorder=4
    )

    tree_lines = [
        ("├── index.html", "  # Головна сторінка"),
        ("├── css/", ""),
        ("│   └── style.css", " # Таблиця стилів"),
        ("├── js/", ""),
        ("│   └── script.js", " # Логіка вікторини"),
        ("└── img/", ""),
        ("    └── hero.png", "  # Латиниця в іменах!"),
    ]
    y_pos = 4.22
    for left_part, comment_part in tree_lines:
        ax.text(
            0.85, y_pos, left_part,
            ha="left", va="center", fontsize=11.5, fontweight="bold",
            family="monospace", color=TERM_WHITE, zorder=4
        )
        if comment_part:
            ax.text(
                3.45, y_pos, comment_part,
                ha="left", va="center", fontsize=11.0,
                family="monospace", color=TERM_GRAY, zorder=4
            )
        y_pos -= 0.54

    ax.annotate(
        "", xy=(8.35, 2.82), xytext=(7.42, 2.82),
        arrowprops=dict(arrowstyle="->,head_width=0.30,head_length=0.28",
                        color=ACCENT_BLUE, lw=2.2),
        zorder=5
    )

    methods = [
        (3.85, ACCENT_BLUE, "1. FTP-клієнт (FileZilla)",
         "Введення Host, User, Password (порт 21) у FileZilla"),
        (2.15, ACCENT_PURPLE, "2. Веб-менеджер файлів хостингу",
         "Завантаження ZIP-архіву через панель у public_html"),
        (0.45, ACCENT_GREEN, "3. Статичний хостинг GitHub Pages",
         "Публікація репозиторію за адресою user.github.io"),
    ]

    for cy, acc, ttl, desc in methods:
        card = FancyBboxPatch(
            (8.5, cy), 7.05, 1.35,
            boxstyle="round,pad=0.02,rounding_size=0.18",
            facecolor=BG_CARD,
            edgecolor=BORDER_CARD,
            linewidth=1.4,
            zorder=2
        )
        ax.add_patch(card)
        bar = FancyBboxPatch(
            (8.68, cy + 0.22), 0.14, 0.91,
            boxstyle="round,pad=0.01,rounding_size=0.06",
            facecolor=acc,
            edgecolor="none",
            zorder=3
        )
        ax.add_patch(bar)
        ax.text(
            9.02, cy + 0.94, ttl,
            ha="left", va="center", fontsize=12.5, fontweight="bold",
            color=TEXT_DARK, zorder=4
        )
        ax.text(
            9.02, cy + 0.42, desc,
            ha="left", va="center", fontsize=10.8,
            color=TEXT_GRAY, zorder=4
        )

    return save_diagram(fig, "scheme3_ftp_deploy")


def create_scheme4():
    fig, ax = plt.subplots(figsize=(13.5, 4.8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(
        8.0, 5.22,
        "Алгоритм виконання різнорівневих завдань (загальний час — 27 хв)",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=TEXT_DARK
    )

    levels = [
        (0.45, ACCENT_GREEN, "РІВЕНЬ 1 • ≈ 7 ХВ", "Репродуктивний",
         ["Реєстрація на сервері хостингу", "Автогенерація базової сторінки", "Оцінювання: 1–5 балів"]),
        (5.7, ACCENT_BLUE, "РІВЕНЬ 2 • ≈ 10 ХВ", "Продуктивний",
         ["Верстка сторінки HTML5 + CSS3", "Завантаження на сервер через FTP", "Оцінювання: 6–9 балів"]),
        (10.95, ACCENT_ORANGE, "РІВЕНЬ 3 • ≈ 10 ХВ", "Творчий",
         ["Інтерактивний JS-модуль", "Налагодження в DevTools (F12)", "Оцінювання: 10–13 балів"]),
    ]

    card_w = 4.6
    card_h = 3.25
    card_y = 1.55

    for idx, (cx, acc, bdg, ttl, lns) in enumerate(levels):
        draw_apple_card(ax, cx, card_y, card_w, card_h, acc, bdg, ttl, lns)
        if idx < len(levels) - 1:
            x_start = cx + card_w + 0.08
            x_end = levels[idx + 1][0] - 0.08
            y_mid = card_y + card_h / 2
            ax.annotate(
                "", xy=(x_end, y_mid), xytext=(x_start, y_mid),
                arrowprops=dict(arrowstyle="->,head_width=0.28,head_length=0.26",
                                color=ACCENT_BLUE, lw=2.0),
                zorder=5
            )

    summary_box = FancyBboxPatch(
        (0.45, 0.35), 15.1, 0.85,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        facecolor=BG_CARD,
        edgecolor=ACCENT_BLUE,
        linewidth=1.4,
        zorder=2
    )
    ax.add_patch(summary_box)
    ax.text(
        8.0, 0.775,
        "Результат: опублікований освітній сайт за URL та звіт студента (до 13 балів)",
        ha="center", va="center", fontsize=11.8, fontweight="bold", color=TEXT_DARK, zorder=4
    )

    return save_diagram(fig, "scheme4_levels")


# ==============================================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ==============================================================================
COLOR_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)     # #1F4E79
COLOR_SECONDARY = RGBColor(0x2E, 0x75, 0xB6)   # #2E75B6
COLOR_CODE = RGBColor(0xC0, 0x39, 0x2B)        # #C0392B
COLOR_TEXT = RGBColor(0x00, 0x00, 0x00)        # Чорний основний текст
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_run_font(run, font_name="Times New Roman", size_pt=14, bold=False, italic=False, color=COLOR_TEXT):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), font_name)
    rFonts.set(qn("w:hAnsi"), font_name)
    rFonts.set(qn("w:cs"), font_name)


def add_rich_runs(paragraph, text, base_size=14, base_bold=False, base_italic=False, base_color=COLOR_TEXT):
    tokens = re.split(r"(\*\*.*?\*\*|`[^`]+`)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            r = paragraph.add_run(tok[2:-2])
            set_run_font(r, "Times New Roman", base_size, bold=True, italic=base_italic, color=base_color)
        elif tok.startswith("`") and tok.endswith("`"):
            r = paragraph.add_run(tok[1:-1])
            set_run_font(r, "Consolas", base_size - 1.5, bold=base_bold, italic=False, color=COLOR_CODE)
        else:
            r = paragraph.add_run(tok)
            set_run_font(r, "Times New Roman", base_size, bold=base_bold, italic=base_italic, color=base_color)


def add_body_p(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=5, space_before=0,
               first_line_indent=None, left_indent=None, bold=False, italic=False, color=COLOR_TEXT):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if first_line_indent is not None:
        pf.first_line_indent = Cm(first_line_indent)
    if left_indent is not None:
        pf.left_indent = Cm(left_indent)
    add_rich_runs(p, text, base_size=14, base_bold=bold, base_italic=italic, base_color=color)
    return p


def add_heading_h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(10)
    pf.space_after = Pt(5)
    pf.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, "Times New Roman", 14, bold=True, color=COLOR_PRIMARY)
    return p


def add_heading_h2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(8)
    pf.space_after = Pt(4)
    pf.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, "Times New Roman", 14, bold=True, color=COLOR_SECONDARY)
    return p


def numbered_paren(doc, items):
    for idx, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.line_spacing = 1.15
        pf.left_indent = Cm(1.0)
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        r_num = p.add_run(f"{idx}) ")
        set_run_font(r_num, "Times New Roman", 14, bold=True, color=COLOR_PRIMARY)
        add_rich_runs(p, item, base_size=14, base_color=COLOR_TEXT)


def add_list_number(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.line_spacing = 1.15
        pf.left_indent = Cm(1.0)
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        add_rich_runs(p, item, base_size=14, base_color=COLOR_TEXT)


def add_list_bullet(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.line_spacing = 1.15
        pf.left_indent = Cm(1.0)
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        add_rich_runs(p, item, base_size=14, base_color=COLOR_TEXT)


def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)


def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)


def add_callout(doc, text, fill_hex="EAF2F8", border_hex="2E75B6"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    cell = tbl.cell(0, 0)
    cell.width = Cm(16.8)
    set_cell_shading(cell, fill_hex)
    set_cell_margins(cell, top=130, bottom=130, left=200, right=180)
    prevent_row_split(tbl.rows[0])

    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")

    left_b = OxmlElement("w:left")
    left_b.set(qn("w:val"), "single")
    left_b.set(qn("w:sz"), "28")
    left_b.set(qn("w:space"), "0")
    left_b.set(qn("w:color"), border_hex)
    tcBorders.append(left_b)

    for side in ("top", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "none")
        tcBorders.append(b)

    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    add_rich_runs(p, text, base_size=14, base_color=COLOR_TEXT)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)


def add_styled_table(doc, headers, rows_data, col_widths_cm, center_cols=None):
    if center_cols is None:
        center_cols = set()

    tbl = doc.add_table(rows=1 + len(rows_data), cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    hdr_row = tbl.rows[0]
    set_table_header(hdr_row)
    prevent_row_split(hdr_row)
    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.width = Cm(col_widths_cm[c_idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, "1F4E79")
        set_cell_margins(cell, top=110, bottom=110, left=130, right=130)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.1
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        set_run_font(r, "Times New Roman", 13.5, bold=True, color=COLOR_WHITE)

    for r_idx, r_data in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        prevent_row_split(row)
        bg_hex = "F9FBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = Cm(col_widths_cm[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_shading(cell, bg_hex)
            set_cell_margins(cell, top=95, bottom=95, left=130, right=130)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            add_rich_runs(p, val, base_size=13.5, base_color=COLOR_TEXT)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)
    return tbl


def add_diagram_to_doc(doc, img_path, caption_text, width_cm=15.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Cm(width_cm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.line_spacing = 1.15
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(caption_text)
    set_run_font(r_cap, "Times New Roman", 12.5, italic=True, color=RGBColor(0x4A, 0x4A, 0x4A))


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    r1 = p.add_run()
    set_run_font(r1, "Times New Roman", 12, color=RGBColor(0x59, 0x59, 0x59))
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"

    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")

    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")

    r1._r.append(fldChar1)
    r1._r.append(instrText)
    r1._r.append(fldChar2)
    r1._r.append(fldChar3)


# ==============================================================================
# 3. ФОРМУВАННЯ ДОКУМЕНТА DOCX
# ==============================================================================
def build_docx():
    png1 = create_scheme1()
    png2 = create_scheme2()
    png3 = create_scheme3()
    png4 = create_scheme4()

    doc = Document()

    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    add_page_number_footer(section)

    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(14)
    normal_style.font.color.rgb = COLOR_TEXT
    rPr = normal_style.element.get_or_add_rPr()
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:cs"), "Times New Roman")
    rPr.insert(0, rFonts)

    # --------------------------------------------------------------------------
    # ЗАГОЛОВОК І ТЕМА
    # --------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.15
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("ПРАКТИЧНЕ ЗАНЯТТЯ № 22")
    set_run_font(r_title, "Times New Roman", 14, bold=True, color=COLOR_PRIMARY)

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.line_spacing = 1.15
    p_topic.paragraph_format.space_before = Pt(0)
    p_topic.paragraph_format.space_after = Pt(8)
    r_topic = p_topic.add_run(
        "Тема: Розробка й публікація веб-сайту. Реєстрація веб-сайту на сервері "
        "безкоштовного хостингу. Автоматизоване створення статичної веб-сторінки, "
        "вибір її типу й оформлення. Створення веб-сторінок засобами HTML/CSS/JS."
    )
    set_run_font(r_topic, "Times New Roman", 14, bold=True, color=COLOR_TEXT)

    # --------------------------------------------------------------------------
    # МЕТА, ОБЛАДНАННЯ, ЛІТЕРАТУРА
    # --------------------------------------------------------------------------
    add_body_p(
        doc,
        "**Мета:** опанувати процес публікації сайту на хостингу (FTP-клієнт або "
        "файловий менеджер), створювати сторінки з використанням HTML, CSS, базового JS; "
        "розвивати комплексні навички веб-розробника, уміння доводити проєкт до публікації, "
        "навички налагодження; виховувати відповідальність за опублікований контент, "
        "дотримання законів про авторське право, повагу до користувачів."
    )

    add_heading_h1(doc, "Обладнання та програмне забезпечення")
    numbered_paren(doc, [
        "Інструкційні картки до практичного заняття № 22.",
        "Персональний комп’ютер (ноутбук) зі стабільним підключенням до мережі Інтернет.",
        "Сучасний веббраузер із панеллю інструментів розробника DevTools (`Google Chrome`, `Mozilla Firefox` або `Microsoft Edge`).",
        "Редактор вихідного коду (`Visual Studio Code`, `Notepad++` або стандартний текстовий редактор із підтримкою кодування `UTF-8`).",
        "FTP-клієнт (`FileZilla Client`) та обліковий запис на сервері безкоштовного хостингу (`InfinityFree`, `000webhost` або статичний хостинг `GitHub Pages`)."
    ])

    add_heading_h1(doc, "Література")
    add_list_number(doc, [
        "Буров Є. В. Комп’ютерні мережі. Львів : Магнолія 2006, 2024. 256 с.",
        "Мирошниченко В. О. Використання сучасних інформаційних технологій: формування мультимедійної компетентності. Київ : Центр учбової літератури, 2022. 296 с.",
        "Потієнко В. О. Графічний дизайн : рівень стандарту (вибірковий модуль для 10–11 кл). Харків : Ранок, 2020. 160 с."
    ])

    # --------------------------------------------------------------------------
    # ХІД ЗАНЯТТЯ
    # --------------------------------------------------------------------------
    add_heading_h1(doc, "Хід заняття")
    add_styled_table(
        doc,
        headers=["№", "Етап заняття", "Зміст навчальної діяльності", "Час"],
        rows_data=[
            ["1", "Організаційний етап",
             "Перевірка готовності робочих місць, відкриття редактора коду, браузера та інструкційних карток.",
             "3 хв"],
            ["2", "Актуалізація знань та інструктаж із БЖД",
             "Повторення клієнт-серверної взаємодії, структури HTML/CSS/JS, правил безпечної роботи за ПК та захисту облікових даних.",
             "7 хв"],
            ["3", "Виконання практичних різнорівневих завдань",
             "Реєстрація хостингу, створення освітньої веб-сторінки (HTML5/CSS3/JS), публікація файлів через FTP/веб-менеджер, налагодження.",
             "27 хв"],
            ["4", "Перевірка робіт і підбиття підсумків",
             "Демонстрація опублікованих веб-сайтів за публічним URL-посиланням, оцінювання результатів, оформлення звіту.",
             "8 хв"],
        ],
        col_widths_cm=[1.2, 4.3, 9.3, 2.0],
        center_cols={0, 3}
    )

    # --------------------------------------------------------------------------
    # ТЕОРЕТИЧНІ ВІДОМОСТІ
    # --------------------------------------------------------------------------
    add_heading_h1(doc, "Теоретичні відомості")

    add_heading_h2(doc, "1. Архітектура веб-сайту та взаємодія клієнта із сервером")
    add_body_p(
        doc,
        "**Веб-сайт** — це сукупність логічно пов’язаних веб-сторінок, мультимедійних ресурсів "
        "і сценаріїв, об’єднаних спільною темою, дизайном та єдиною точкою входу (головною сторінкою "
        "`index.html`). Щоб створений на локальному комп’ютері освітній ресурс став доступним "
        "учням початкової школи та їхнім батькам, його необхідно розмістити на **веб-хостингу** — "
        "постійно підключеному до Інтернету сервері з виділеним дисковим простором і мережевою адресою."
    )
    add_body_p(
        doc,
        "Звернення до сайту відбувається за протоколами `HTTP` або захищеним `HTTPS` за допомогою "
        "**доменного імені** (наприклад, `teacher-it.infinityfreeapp.com`), яке система `DNS` "
        "перетворює на числовий IP-адрес сервера."
    )
    add_diagram_to_doc(
        doc, png1,
        "Рис. 1. Етапи життєвого циклу публікації веб-сайту на сервері хостингу"
    )

    add_heading_h2(doc, "2. Автоматизоване створення статичної веб-сторінки та її педагогічне оформлення")
    add_body_p(
        doc,
        "**Статична веб-сторінка** передається браузеру користувача саме в тому вигляді, в якому вона "
        "збережена на сервері (набір файлів `.html`, `.css`, `.js` та зображень), без звернення до "
        "серверних баз даних. Для швидкого старту застосовують засоби автоматизованого створення: "
        "вбудовані конструктори шаблонів хостинг-провайдерів (`Site.pro`), генератори стартової "
        "розмітки (`Emmet` у `VS Code`, команда `!` + `Tab`) або освітні шаблони."
    )
    add_body_p(
        doc,
        "Під час вибору типу та оформлення веб-сторінки для молодших школярів майбутній вчитель "
        "інформатики враховує психофізіологічні особливості дітей 6–10 років:"
    )
    add_list_bullet(doc, [
        "**Тип сторінки:** односторінковий освітній плакат (лендінг правила), інтерактивна пам’ятка з безпечного Інтернету або міні-тренажер із розгадування загадок.",
        "**Типографіка та контраст:** кегль основного тексту не менше `16px–18px`, чіткі шрифти без засічок (`Arial`, `Verdana`, `Segoe UI`), темний текст на світлому фоні.",
        "**Візуальна ієрархія:** мінімум текстового перевантаження, поділ інформації на короткі смислові картки, зрозумілі кнопки-підказки."
    ])

    add_heading_h2(doc, "3. Триєдина модель сучасної веб-розробки: HTML5, CSS3 та JavaScript")
    add_body_p(
        doc,
        "Якісна клієнтська частина (Frontend) будується на чіткому розподілі відповідальності між трьома "
        "базовими технологіями, що підключаються до головного документа `index.html`:"
    )
    add_styled_table(
        doc,
        headers=["Технологія", "Призначення на сторінці", "Ключові елементи та спосіб підключення"],
        rows_data=[
            ["**HTML5**",
             "Структура та смислова розмітка контенту (заголовки, абзаци, ілюстрації, кнопки).",
             "Теги `<!DOCTYPE html>`, `<header>`, `<main>`, `<section>`, `<footer>`, `<button>`."],
            ["**CSS3**",
             "Візуальне оформлення, кольори, шрифти, рамки, сітка розташування блоків.",
             "Зовнішній файл `css/style.css`, підключений тегом `<link rel=\"stylesheet\" href=\"css/style.css\">`."],
            ["**JavaScript**",
             "Інтерактивна поведінка, реакція на натискання кнопок, перевірка відповідей учня.",
             "Зовнішній файл `js/script.js`, підключений перед закриттям `</body>` тегом `<script src=\"js/script.js\"></script>`."],
        ],
        col_widths_cm=[3.2, 6.4, 7.2],
        center_cols={0}
    )
    add_diagram_to_doc(
        doc, png2,
        "Рис. 2. Взаємодія HTML5, CSS3 та JavaScript у структурі освітнього веб-проєкту"
    )

    add_heading_h2(doc, "4. Реєстрація безкоштовного хостингу та публікація через FTP / файловий менеджер")
    add_body_p(
        doc,
        "Безкоштовні хостинг-платформи (`InfinityFree`, `000webhost`, `GitHub Pages`) надають безкоштовний "
        "піддомен третього рівня та дисковий простір для навчальних проєктів. Після реєстрації облікового "
        "запису користувач отримує реквізити доступу: адресу сервера (`FTP Hostname`), логін (`Username`), "
        "пароль (`Password`) та стандартний порт підключення `21`."
    )
    add_body_p(
        doc,
        "Для перенесення локальної папки проєкту на сервер використовують спеціалізований **FTP-клієнт** "
        "(наприклад, `FileZilla`), який має двопанельний інтерфейс (зліва — локальні файли ПК, справа — "
        "каталог сервера), або вбудований **веб-менеджер файлів** (`Online File Manager`) у панелі керування."
    )
    add_diagram_to_doc(
        doc, png3,
        "Рис. 3. Організація кореневого каталогу сайту та способи завантаження файлів на сервер"
    )
    add_callout(
        doc,
        "Головна сторінка сайту обов’язково повинна називатися `index.html` (малими літерами) і міститися "
        "безпосередньо в кореневому каталозі `public_html/` (або `htdocs/`). Усі імена папок, стилів, "
        "скриптів та зображень слід записувати виключно латиницею без пробілів (`img/banner.png`), "
        "оскільки файлові системи веб-серверів (`Linux`) чутливі до регістру символів.",
        fill_hex="EAF2F8",
        border_hex="2E75B6"
    )

    add_heading_h2(doc, "5. Налагодження веб-сторінок, авторське право та цифрова відповідальність")
    add_body_p(
        doc,
        "Перед завершенням публікації веб-розробник здійснює **налагодження** (debugging): перевіряє "
        "відображення сторінки у браузері, відкриває панель розробника клавішею `F12` (вкладка `Console` "
        "для виявлення помилок JavaScript та вкладка `Network` для перевірки коду відповіді `200 OK` "
        "завантаження стилів і картинок)."
    )
    add_body_p(
        doc,
        "Публікуючи освітній сайт у відкритому доступі, вчитель несе правову й етичну відповідальність: "
        "необхідно використовувати лише власні ілюстрації або медіафайли з вільними ліцензіями "
        "(`Creative Commons CC0`, `Pixabay`, `Wikimedia Commons`), зазначати авторство використаних "
        "джерел і не розміщувати персональні дані чи фотографії учнів без письмової згоди батьків."
    )

    # --------------------------------------------------------------------------
    # ПОКРОКОВИЙ АЛГОРИТМ ВИКОНАННЯ РІЗНОРІВНЕВИХ ЗАВДАНЬ
    # --------------------------------------------------------------------------
    add_heading_h1(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    add_body_p(
        doc,
        "Практична частина заняття розрахована на **27 хвилин** і побудована за принципом "
        "поступового ускладнення навчальних дій від репродуктивного відтворення до творчої розробки."
    )
    add_diagram_to_doc(
        doc, png4,
        "Рис. 4. Структура та часовий розподіл різнорівневих завдань практичного заняття"
    )

    # --- РІВЕНЬ 1 ---
    add_heading_h2(doc, "Рівень 1 — репродуктивний (орієнтовний час — 7 хв)")
    add_body_p(
        doc,
        "**Завдання:** зареєструвати обліковий запис на сервері безкоштовного хостингу, створити "
        "піддомен освітнього проєкту, згенерувати базовий шаблон статичної веб-сторінки засобами "
        "редактора коду (`Emmet`) або конструктора хостингу та сформувати локальну структуру папок."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Зміст дії та команди / налаштування", "Очікуваний результат"],
        rows_data=[
            ["1.1",
             "Створіть на робочому столі папку проєкту `edu_site`, а всередині неї — три підкаталоги: `css`, `js`, `img`.",
             "Підготовлено коректну локальну файлову структуру проєкту."],
            ["1.2",
             "Відкрийте папку `edu_site` у редакторі коду (`VS Code`), створіть файл `index.html`, введіть символ `!` і натисніть `Tab` для автогенерації каркаса HTML5. Змініть `<html lang=\"uk\">` та `<title>Безпечний Інтернет — 2 клас</title>`.",
             "Автоматизовано сформовано валідну базову структуру статичної веб-сторінки."],
            ["1.3",
             "Зареєструйтеся на платформі безкоштовного хостингу (`InfinityFree` або `GitHub Pages`), створіть новий сайт із піддоменом `safe-web-class` та збережіть параметри підключення (`FTP Host`, `Username`, `Password`).",
             "Активовано обліковий запис і виділено місце на сервері хостингу."],
        ],
        col_widths_cm=[1.5, 9.5, 5.8],
        center_cols={0}
    )

    # --- РІВЕНЬ 2 ---
    add_heading_h2(doc, "Рівень 2 — продуктивний (орієнтовний час — 10 хв)")
    add_body_p(
        doc,
        "**Завдання:** наповнити освітню веб-сторінку для учнів початкової школи «3 золоті правила "
        "безпечного Інтернету» засобами HTML5, оформити її зовнішньою таблицею стилів `css/style.css` "
        "та виконати первинну публікацію файлів на сервер через FTP-клієнт або файловий менеджер."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Зміст дії та команди / налаштування", "Очікуваний результат"],
        rows_data=[
            ["2.1",
             "Усередині `<body>` файлу `index.html` додайте семантичні блоки: `<header>` із заголовком `<h1>3 правила юного дослідника Інтернету</h1>`, блок `<main>` із трьома картками `<section class=\"card\">` та `<footer>` із зазначенням авторства і ліцензії використаних ілюстрацій.",
             "Створено змістовну структуру освітньої веб-сторінки для молодших школярів."],
            ["2.2",
             "Створіть файл `css/style.css`, підключіть його в `<head>` через `<link rel=\"stylesheet\" href=\"css/style.css\">`. Задайте світлий фон (`#F5F7FA`), шрифт `Arial, sans-serif` розміром `18px`, заокруглені картки (`border-radius: 14px`) та контрастні заголовки (`#1F4E79`).",
             "Сторінка набула зручного для читання дітьми оформлення."],
            ["2.3",
             "Запустіть `FileZilla` (введіть `Host`, `Username`, `Password`, `Port: 21` -> `Швидке з’єднання`) або відкрийте `Online File Manager` у панелі хостингу. Скопіюйте файли `index.html`, папки `css/`, `js/`, `img/` у кореневий каталог `public_html/`.",
             "Усі файли веб-сайту успішно передано на віддалений сервер хостингу."],
        ],
        col_widths_cm=[1.5, 9.5, 5.8],
        center_cols={0}
    )

    # --- РІВЕНЬ 3 ---
    add_heading_h2(doc, "Рівень 3 — творчий (орієнтовний час — 10 хв)")
    add_body_p(
        doc,
        "**Завдання:** розробити інтерактивний елемент самоперевірки для учнів початкової школи "
        "засобами базового JavaScript (`js/script.js`), виконати налагодження коду в консолі розробника "
        "браузера (`F12`), оновити сайт на сервері хостингу та протестувати його роботу за публічною URL-адресою."
    )
    add_styled_table(
        doc,
        headers=["Крок", "Зміст дії та команди / налаштування", "Очікуваний результат"],
        rows_data=[
            ["3.1",
             "Додайте до `index.html` блок міні-вікторини з запитанням («Чи можна повідомляти пароль незнайомцям у грі?»), двома кнопками `<button onclick=\"checkAnswer(false)\">Так</button>` та `<button onclick=\"checkAnswer(true)\">Ні</button>` і абзацом результату `<p id=\"feedback\"></p>`.",
             "Підготовлено інтерфейсні елементи для інтерактивної взаємодії учня зі сторінкою."],
            ["3.2",
             "У файлі `js/script.js` опишіть функцію `checkAnswer(isCorrect)`, яка змінює текст (`textContent`) та колір (`style.color`) блока `#feedback` залежно від вибору учня, а також додайте кнопку перемикання збільшеного шрифту для учнів із порушенням зору. Підключіть `<script src=\"js/script.js\"></script>`.",
             "Реалізовано інтерактивний сценарій та елемент цифрової доступності."],
            ["3.3",
             "Перевірте роботу локально, натисніть `F12` (`Console`) та переконайтеся у відсутності помилок. Повторно завантажте оновлені `index.html` і `js/script.js` на хостинг, відкрийте сайт за публічним URL на ПК або смартфоні.",
             "Повноцінний інтерактивний освітній сайт опубліковано та перевірено в мережі Інтернет."],
        ],
        col_widths_cm=[1.5, 9.5, 5.8],
        center_cols={0}
    )

    add_callout(
        doc,
        "Якщо після оновлення стилів (`style.css`) або скриптів (`script.js`) на сервері хостингу "
        "браузер відображає попередню версію сторінки, виконайте жорстке оновлення кешу комбінацією "
        "клавіш `Ctrl + F5` (або `Cmd + Shift + R` на macOS).",
        fill_hex="EAFAF1",
        border_hex="248A3D"
    )

    # --------------------------------------------------------------------------
    # КРИТЕРІЇ ОЦІНЮВАННЯ
    # --------------------------------------------------------------------------
    add_heading_h1(doc, "Критерії оцінювання")
    add_styled_table(
        doc,
        headers=["Рівень досягнень", "Бали", "Критерії оцінювання результатів практичної роботи"],
        rows_data=[
            ["Початковий\n(фрагментарне виконання)",
             "1–3",
             "Зареєстровано обліковий запис на сервері безкоштовного хостингу, але структура локальних каталогів містить помилки або головну сторінку не опубліковано."],
            ["Середній\n(репродуктивний)",
             "4–6",
             "Створено базову статичну сторінку `index.html` засобами автогенерації, виконано публікацію на сервері, проте відсутнє власне CSS-оформлення або є помилки у шляхах до ресурсів."],
            ["Достатній\n(продуктивний)",
             "7–9",
             "Зверстано освітню веб-сторінку засобами HTML5 та зовнішнього CSS3 з урахуванням вікових особливостей молодших школярів, коректно завантажено файли через FTP або файловий менеджер."],
            ["Високий\n(творчий)",
             "10–13",
             "Створено та опубліковано повноцінний інтерактивний освітній веб-сайт (HTML5 + CSS3 + JS), виконано налагодження без помилок у консолі браузера, дотримано норм авторського права, вчасно подано оформлений звіт."],
        ],
        col_widths_cm=[4.2, 1.8, 10.8],
        center_cols={1}
    )

    # --------------------------------------------------------------------------
    # ФОРМА ЗВІТНОСТІ
    # --------------------------------------------------------------------------
    add_heading_h1(doc, "Форма звітності")
    add_body_p(
        doc,
        "За результатами виконання практичного заняття № 22 студент оформлює електронний звіт "
        "у форматі `.docx` або `.pdf` та подає його викладачу на перевірку. Звіт має містити:"
    )
    add_list_bullet(doc, [
        "Титульну інформацію (номер і тему практичного заняття, прізвище та групу студента).",
        "Активне гіперпосилання (URL) на опублікований у мережі Інтернет веб-сайт.",
        "Скріншоти: а) вікна панелі керування хостингом або FTP-клієнта `FileZilla` зі структурою каталогу `public_html/`; б) опублікованої веб-сторінки у вікні браузера; в) вкладки `Console` інструментів розробника (`F12`).",
        "Лістинг вихідного коду файлів `index.html`, `css/style.css` та `js/script.js`.",
        "Короткі висновки про опановані способи публікації веб-сайтів та забезпечення цифрової безпеки освітнього контенту."
    ])

    output_docx = "Практичне_заняття_22_Веб_сайт_Хостинг.docx"
    doc.save(output_docx)
    print(f"Документ успішно збережено: {output_docx}")
    print("Схеми збережено у папці: output/ (.png та .svg)")


if __name__ == "__main__":
    build_docx()