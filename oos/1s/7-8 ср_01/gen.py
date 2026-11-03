# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: САМОСТІЙНА РОБОТА
Тема: Організація файлової системи. Створення та іменування файлів і папок
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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


def scheme_filename_structure():
    """Схема 1: анатомія повного імені файлу."""
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 7); ax.axis("off")

    # Власне ім'я
    ax.add_patch(FancyBboxPatch((1.4, 3.0), 8.0, 1.2,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#DEEAF6", edgecolor="#2E75B6", linewidth=1.6))
    ax.text(5.4, 3.6, "Звіт_з_практики_2024", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#1F4E79")

    # Розширення
    ax.add_patch(FancyBboxPatch((9.5, 3.0), 2.4, 1.2,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#FFF2CC", edgecolor="#BF8F00", linewidth=1.6))
    ax.text(10.7, 3.6, ".docx", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#7F6000")

    # Підписи зверху
    ax.annotate("ВЛАСНЕ ІМ'Я\n(описує зміст файлу)",
                xy=(5.4, 4.25), xytext=(5.4, 5.8),
                ha="center", va="center", fontsize=11, fontweight="bold",
                color="#2E75B6",
                arrowprops=dict(arrowstyle="-|>", color="#2E75B6", linewidth=1.6))
    ax.annotate("РОЗШИРЕННЯ\n(тип файлу)",
                xy=(10.7, 4.25), xytext=(11.8, 5.8),
                ha="center", va="center", fontsize=11, fontweight="bold",
                color="#BF8F00",
                arrowprops=dict(arrowstyle="-|>", color="#BF8F00", linewidth=1.6))

    # Примітки знизу
    ax.annotate("Без пробілів і заборонених символів\n: * ? \" < > | \\ /",
                xy=(5.4, 2.95), xytext=(5.4, 1.6),
                ha="center", va="center", fontsize=10, color="#404040",
                arrowprops=dict(arrowstyle="-|>", color="#808080", linewidth=1.2))
    ax.annotate("Вказує, якою програмою\nвідкривати файл",
                xy=(10.7, 2.95), xytext=(12.0, 1.6),
                ha="center", va="center", fontsize=10, color="#404040",
                arrowprops=dict(arrowstyle="-|>", color="#808080", linewidth=1.2))

    ax.text(7.0, 0.4,
            "Схема 1. Анатомія повного імені файлу",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")
    return _save(fig, "scheme_filename")


def scheme_fs_comparison():
    """Схема 2: порівняння файлових систем FAT32 / NTFS / ext4."""
    fig, ax = plt.subplots(figsize=(11.5, 7))
    ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis("off")

    cards = [
        ("FAT32", "#C55A11", "#FBE5D6", [
            "Макс. розмір файлу: 4 ГБ",
            "Макс. розмір тому: 2 ТБ",
            "Сумісність: усі ОС",
            "Без журналювання",
            "Застосування:",
            "флешки, зовнішні диски",
        ]),
        ("NTFS", "#1F4E79", "#DEEAF6", [
            "Макс. розмір файлу: 16 ТБ",
            "Макс. розмір тому: 256 ТБ",
            "Сумісність: Windows, частк. Linux",
            "Журналювання, права доступу",
            "Застосування:",
            "системний диск Windows",
        ]),
        ("ext4", "#548235", "#E2EFDA", [
            "Макс. розмір файлу: 16 ТБ",
            "Макс. розмір тому: 1 ЕБ",
            "Сумісність: Linux",
            "Журналювання, POSIX-права",
            "Застосування:",
            "системний диск Linux",
        ]),
    ]

    card_w = 4.6
    card_h = 6.2
    gap = 0.6
    x0 = (16 - (3 * card_w + 2 * gap)) / 2
    y0 = 2.4

    for i, (title, accent, fill, lines) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        ax.add_patch(FancyBboxPatch((x, y0), card_w, card_h,
                                    boxstyle="round,pad=0.02,rounding_size=0.2",
                                    facecolor=fill, edgecolor=accent, linewidth=2.0))
        # заголовок картки
        ax.add_patch(FancyBboxPatch((x, y0 + card_h - 1.1), card_w, 1.1,
                                    boxstyle="round,pad=0.02,rounding_size=0.2",
                                    facecolor=accent, edgecolor=accent, linewidth=2.0))
        ax.text(x + card_w / 2, y0 + card_h - 0.55, title,
                ha="center", va="center", fontsize=16, fontweight="bold", color="white")

        for j, line in enumerate(lines):
            ty = y0 + card_h - 1.7 - j * 0.72
            fw = "bold" if line.endswith(":") else "normal"
            ax.text(x + 0.3, ty, "•  " + line if not line.endswith(":") else line,
                    ha="left", va="center", fontsize=10, fontweight=fw, color="#1a1a1a")

    ax.text(8.0, 9.3,
            "Схема 2. Порівняння файлових систем FAT32 / NTFS / ext4",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")
    ax.text(8.0, 1.2,
            "FAT32 — найстаріша та найсумісніша;  NTFS — стандарт Windows;  ext4 — стандарт Linux",
            ha="center", va="center", fontsize=10, style="italic", color="#595959")
    return _save(fig, "scheme_fs_comparison")


def scheme_file_tree():
    """Схема 3: ієрархічна структура файлової системи."""
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 14); ax.set_ylim(0, 9); ax.axis("off")

    def box(x, y, text, fc="#DEEAF6", ec="#2E75B6", tc="#1F4E79", fs=10):
        bw, bh = 2.4, 0.9
        ax.add_patch(FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=fc, edgecolor=ec, linewidth=1.4))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs,
                color=tc, fontweight="bold")

    def link(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color="#8FAADC", linewidth=1.6, zorder=0)

    root = (7.0, 8.0)
    lvl1 = [(3.0, 5.8, "Навчання"), (7.0, 5.8, "Фото"), (11.0, 5.8, "Програми")]
    lvl2 = [(1.6, 3.2, "Звіти"), (4.4, 3.2, "Конспекти"),
            (5.8, 3.2, "Родина"), (8.2, 3.2, "Подорожі"),
            (10.0, 3.2, "Офіс"), (12.0, 3.2, "Ігри")]
    lvl3 = [(1.6, 0.9, "звіт_1.docx"), (4.4, 0.9, "лекція_3.docx")]

    box(root[0], root[1], "Диск C:", fc="#1F4E79", ec="#0D2A42", tc="white", fs=11)
    for x, y, t in lvl1:
        link(root[0], root[1] - 0.45, x, y + 0.45)
        box(x, y, t)
    for i, (x, y, t) in enumerate(lvl2):
        px, py, _ = lvl1[i // 2]
        link(px, py - 0.45, x, y + 0.45)
        box(x, y, t, fc="#EAF1DD", ec="#548235", tc="#375623", fs=9)
    for x, y, t in lvl3:
        px, py, _ = lvl2[0] if x < 3.0 else lvl2[1]
        link(px, py - 0.45, x, y + 0.45)
        ax.add_patch(FancyBboxPatch((x - 1.1, y - 0.35), 2.2, 0.7,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor="#FFF2CC", edgecolor="#BF8F00",
                                    linewidth=1.2))
        ax.text(x, y, t, ha="center", va="center", fontsize=9,
                color="#7F6000", fontweight="bold")

    ax.text(7.0, 8.7,
            "Схема 3. Ієрархічна структура файлової системи",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")
    ax.text(7.0, 0.2,
            "Диск → папка → підпапка → файл:  «шафа → полиця → коробка → зошит»",
            ha="center", va="center", fontsize=10, style="italic", color="#595959")
    return _save(fig, "scheme_file_tree")


def scheme_algorithm():
    """Схема 4: алгоритм створення папки та файлу."""
    fig, ax = plt.subplots(figsize=(9, 10.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 13); ax.axis("off")

    steps = [
        "1. Увімкнути комп'ютер і дочекатися завантаження ОС",
        "2. Відкрити «Проводник» (або інший файловий менеджер)",
        "3. Перейти до потрібної папки (диск → папки)",
        "4. Клацнути правою кнопкою миші → «Створити» →\n«Папку» або «Текстовий документ»",
        "5. Ввести ім'я без заборонених символів : * ? \" < > |",
        "6. Натиснути Enter (або клацнути поза полем)",
        "7. Перевірити результат: об'єкт з'явився у папці",
    ]

    y_start = 11.6
    box_w, box_h = 6.8, 1.0
    spacing = 1.7

    for i, step in enumerate(steps):
        y = y_start - i * spacing
        ax.add_patch(FancyBboxPatch((5 - box_w / 2, y - box_h / 2), box_w, box_h,
                                    boxstyle="round,pad=0.02,rounding_size=0.15",
                                    facecolor="#DEEAF6", edgecolor="#2E75B6",
                                    linewidth=1.6))
        ax.text(5, y, step, ha="center", va="center", fontsize=10,
                fontweight="bold", color="#1F4E79", linespacing=1.3)
        if i < len(steps) - 1:
            ax.annotate("",
                        xy=(5, y - box_h / 2 - 0.02),
                        xytext=(5, y - spacing + box_h / 2 + 0.02),
                        arrowprops=dict(arrowstyle="-|>", color="#2E75B6",
                                        linewidth=1.6, mutation_scale=14))

    ax.text(5, 12.6, "Схема 4. Алгоритм створення папки та файлу",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1F4E79")
    return _save(fig, "scheme_algorithm")


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


def body(doc, text, bold_lead=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_lead:
        _style_run(p.add_run(bold_lead), bold=True)
    _style_run(p.add_run(text))
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
    img1 = scheme_filename_structure()
    img2 = scheme_fs_comparison()
    img3 = scheme_file_tree()
    img4 = scheme_algorithm()

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
    h1(doc, "Організація файлової системи. "
           "Створення та іменування файлів і папок")

    body(doc, "«Основи операційних систем» · спеціальність 013 Початкова освіта "
              "(Вчитель інформатики початкової школи)", space_after=10)

    # ---------- Мета ----------
    h2(doc, "Мета")
    body(doc, "дослідити принципи організації файлових систем, правила створення й "
              "іменування файлів та каталогів; розвивати навички самостійного пошуку "
              "та систематизації інформації про різні типи файлових систем "
              "(FAT, NTFS, ext); формувати акуратність та уважність до системи "
              "зберігання даних як складової інформаційної культури майбутнього "
              "вчителя початкової школи.")

    # ---------- Обладнання ----------
    h2(doc, "Обладнання")
    body(doc, "інструкційні картки; персональний комп'ютер (Windows / Linux) з "
              "файловим менеджером; пакет LibreOffice / MS Office для оформлення "
              "звіту; доступ до мережі Інтернет (для пошуку інформації про файлові "
              "системи).")

    # ---------- Завдання ----------
    h2(doc, "Завдання самостійної роботи")
    tasks = [
        "Опрацювати теоретичний матеріал за переліком опрацьовуваних питань.",
        "Заповнити порівняльну таблицю файлових систем FAT32, NTFS та ext4 "
        "(не менше п'яти параметрів порівняння).",
        "Виконати практичне завдання за інструкційною карткою: створити "
        "задану ієрархічну структуру папок і файлів.",
        "Скласти пам'ятку «Правила іменування файлів і папок» (7–10 пунктів).",
        "Дати письмові відповіді на теоретичні питання (див. нижче).",
        "Оформити звіт відповідно до наведених рекомендацій та надіслати "
        "викладачу у визначений термін.",
    ]
    for t in tasks:
        numbered(doc, t)

    # ---------- Терміни ----------
    h2(doc, "Терміни виконання")
    body(doc, "Робота виконується протягом одного тижня після отримання завдання; "
              "готовий звіт подається на наступному практичному занятті або "
              "завантажується в електронний курс дисципліни до вказаної дати.")

    # ---------- Очікувані результати ----------
    h2(doc, "Очікувані результати")
    results = [
        "знає визначення файлової системи та її призначення;",
        "розуміє ієрархічну структуру зберігання даних;",
        "характеризує основні файлові системи (FAT32, NTFS, ext4) та їх "
        "відмінності;",
        "володіє правилами іменування файлів і папок, знає перелік заборонених "
        "символів;",
        "вміє створювати папки та файли, перейменовувати й переміщувати їх у "
        "файловому менеджері;",
        "добирає доступні молодшим школярам аналогії для пояснення теми "
        "«Файли та папки».",
    ]
    for r in results:
        bullet(doc, r)

    # ---------- Література ----------
    h2(doc, "Рекомендовані джерела")
    sources = [
        "Микитишин А. Г., Чихіра І. В. Операційні системи : конспект лекцій. — "
        "Тернопіль : ТНТУ імені Івана Пулюя, 2016.",
        "Погребняк Б. І., Булаєнко М. В. Операційні системи : навч. посіб. — "
        "Харків : ХНУМГ ім. О. М. Бекетова, 2018.",
        "Сільвестр В., Гансен П. Основи операційних систем. — Київ : Нова Книга, 2016.",
    ]
    for s in sources:
        bullet(doc, s)

    # ---------- Опрацьовувані питання ----------
    h2(doc, "Перелік опрацьовуваних питань")
    topics = [
        "Поняття файлової системи, її основні функції.",
        "Ієрархічна структура зберігання даних: диск → папка → файл.",
        "Об'єкти файлової системи: файл, папка (каталог), ярлик.",
        "Структура імені файлу, правила іменування, заборонені символи.",
        "Розширення файлів та їх зв'язок із програмами.",
        "Файлові системи FAT32, NTFS, ext4: особливості й застосування.",
        "Створення, перейменування, копіювання та видалення об'єктів "
        "у файловому менеджері.",
        "Організація особистого інформаційного простору вчителя.",
    ]
    for tp in topics:
        numbered(doc, tp)

    # ---------- Теоретичні відомості ----------
    h2(doc, "Теоретичні відомості (стислий огляд)")

    body(doc, "Файлова система — це частина операційної системи, яка відповідає за "
              "зберігання, пошук і впорядкування даних на носіях інформації. Саме "
              "вона перетворює «сирий» диск на зрозумілу структуру папок і файлів, "
              "з якою працює користувач.")

    body(doc, "Файл — це поіменована область на носії для зберігання даних "
              "(тексту, зображення, відео, програми). Папка (каталог) — контейнер "
              "для групування файлів і вкладених папок. Ієрархія «диск → папка → "
              "підпапка → файл» утворює дерево файлової системи.")

    add_figure(doc, img3, 15.5)

    body(doc, "Повне ім'я файлу складається з власне імені та розширення, яке "
              "вказує на тип вмісту. У Windows ім'я може містити великі та малі "
              "літери, цифри, пробіли, але не може перевищувати 255 символів і "
              "не повинно містити заборонених символів.")

    add_figure(doc, img1, 15.0)

    callout(doc, "Правило.",
            "Ім'я файлу має бути змістовним: «Звіт_з_практики_2024.docx» — це "
            "добре, а «Документ1.docx» або «щщщ.docx» — погано. Учитель, який "
            "привчає учнів до осмислених назв, формує інформаційну культуру з "
            "перших класів.",
            fill="FFF4E5", accent="C55A11")

    add_table(
        doc,
        ["Розширення", "Тип файлу", "Програма для відкриття"],
        [
            [".docx / .doc", "Текстовий документ", "MS Word / LibreOffice Writer"],
            [".txt", "Простий текст", "Блокнот / будь-який редактор"],
            [".xlsx", "Електронна таблиця", "MS Excel / LibreOffice Calc"],
            [".pptx", "Презентація", "MS PowerPoint / LibreOffice Impress"],
            [".pdf", "Документ для перегляду й друку", "Браузер / Adobe Reader"],
            [".jpg / .png", "Зображення", "Перегляд фотографій"],
            [".mp4", "Відео", "Медіапрогравач"],
            [".exe", "Програма (Windows)", "Запускається ОС"],
        ],
        widths=[3.4, 6.6, 6.5],
    )

    body(doc, "Різні операційні системи використовують різні файлові системи. "
              "Найпоширеніші з них — FAT32, NTFS та ext4. Їхні ключові "
              "характеристики узагальнено на схемі 2 та в таблиці.")

    add_figure(doc, img2, 15.5)

    add_table(
        doc,
        ["Параметр", "FAT32", "NTFS", "ext4"],
        [
            ["Макс. розмір файлу", "4 ГБ", "16 ТБ", "16 ТБ"],
            ["Макс. розмір тому", "2 ТБ", "256 ТБ", "1 ЕБ"],
            ["Журналювання", "ні", "так", "так"],
            ["Права доступу", "немає", "є (ACL)", "є (POSIX)"],
            ["Сумісність", "усі ОС", "Windows, частк. Linux", "Linux"],
            ["Сфера застосування", "флешки, зовнішні диски",
             "системний диск Windows", "системний диск Linux"],
        ],
        widths=[4.4, 3.6, 4.4, 4.1],
    )

    body(doc, "Створення об'єктів файлової системи у сучасних ОС виконується "
              "однаково за простою послідовністю дій, яку варто довести до "
              "автоматизму (схема 4).")

    add_figure(doc, img4, 11.0)

    # ---------- Хід заняття ----------
    h2(doc, "Хід заняття (етапи самостійної роботи)")
    stages = [
        ("Організаційно-мотиваційний етап (5 хв). ",
         "Ознайомлення з темою, метою та завданнями; розподіл часу."),
        ("Актуалізація опорних знань (10 хв). ",
         "Пригадування понять «файл», «папка», «ярлик»; бесіда про те, "
         "як учні початкових класів щодня працюють із файловою системою."),
        ("Опрацювання теоретичного матеріалу (30 хв). ",
         "Самостійне читання конспекту, заповнення порівняльної таблиці, "
         "складання пам'ятки правил іменування."),
        ("Виконання практичних завдань (40 хв). ",
         "Робота за інструкційною карткою: створення структури папок, "
         "файлів, перейменування, копіювання, видалення."),
        ("Узагальнення та рефлексія (10 хв). ",
         "Самоперевірка за теоретичними питаннями, формулювання висновків."),
        ("Оформлення звіту (позааудиторно). ",
         "Подання результатів відповідно до рекомендацій нижче."),
    ]
    for lead, txt in stages:
        bullet(doc, txt, bold_lead=lead)

    # ---------- Теоретичні питання ----------
    h2(doc, "Теоретичні питання для самоперевірки")
    questions = [
        "Що таке файлова система і які її основні функції?",
        "Опишіть ієрархічну структуру зберігання даних на прикладі власного "
        "навчального диска.",
        "Чим файл відрізняється від папки? Що таке ярлик?",
        "Які правила іменування файлів і папок діють у Windows? Назвіть "
        "заборонені символи.",
        "Для чого потрібне розширення файлу? Наведіть приклади трьох розширень "
        "і програм для їх відкриття.",
        "Охарактеризуйте файлову систему FAT32: переваги, обмеження, сфера "
        "застосування.",
        "Порівняйте NTFS та ext4 за ключовими характеристиками.",
        "Які переваги дає журналювання у файлових системах?",
        "Опишіть алгоритм створення нової папки та текстового файлу.",
        "Запропонуйте структуру папок для зберігання матеріалів учителя "
        "початкової школи (не менше трьох рівнів).",
        "Сформулюйте три поради молодшому школяреві щодо збереження файлів.",
    ]
    for q in questions:
        numbered(doc, q)

    # ---------- Рекомендації до оформлення ----------
    h2(doc, "Рекомендації до оформлення звіту")
    body(doc, "Звіт оформлюється у текстовому редакторі (MS Word / LibreOffice "
              "Writer) і повинен містити такі обов'язкові структурні елементи:")
    structure = [
        "Титульна сторінка: назва навчального закладу, тема, ПІБ студента, "
        "група, ПІБ викладача, рік.",
        "Мета та завдання роботи.",
        "Теоретична частина: порівняльна таблиця файлових систем, пам'ятка "
        "«Правила іменування файлів і папок».",
        "Практична частина: скріншоти створеної структури папок і файлів "
        "(не менше 3 зображень) з короткими коментарями.",
        "Відповіді на теоретичні питання (письмово, стисло).",
        "Висновок: 4–6 речень про те, що нового дізналися і як "
        "використовуватимете ці знання у роботі з молодшими школярами.",
        "Список використаних джерел (оформлений за ДСТУ 8302:2015).",
    ]
    for s in structure:
        numbered(doc, s)

    body(doc, "Технічні параметри оформлення: шрифт Times New Roman, 14 pt, "
              "міжрядковий інтервал 1,15, поля 2 см, абзацний відступ 1,25 см, "
              "вирівнювання за шириною. Обсяг звіту — 5–7 сторінок без урахування "
              "титульної сторінки та додатків.")

    # ---------- Критерії оцінювання ----------
    h2(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Критерій", "Бали"],
        [
            ["Повнота й коректність теоретичної частини", "3"],
            ["Правильність заповнення порівняльної таблиці", "2"],
            ["Виконання практичного завдання за інструкційною карткою", "3"],
            ["Якість пам'ятки «Правила іменування»", "1"],
            ["Відповіді на теоретичні питання", "2"],
            ["Оформлення звіту згідно з рекомендаціями", "1"],
            ["Творчий підхід, власні приклади й аналогії для початкової школи", "1"],
        ],
        widths=[11.5, 5.0],
    )
    body(doc, "Максимальна кількість балів — 13. Оцінка «відмінно» — 12–13 балів, "
              "«добре» — 9–11, «задовільно» — 6–8, «незадовільно» — менше 6 балів.")

    callout(doc, "Порада викладачу.",
            "Під час перевірки звітів звертайте увагу на те, чи вміє студент "
            "не лише описати технічні характеристики файлових систем, а й "
            "пояснити їхньою мовою дитини 6–10 років. Найкращі аналогії "
            "варто обговорити на наступному занятті та включити до методичної "
            "скарбнички групи.",
            fill="E2EFDA", accent="548235")

    doc.save("Самостійна_робота_Файлова_система.docx")
    print("Готово: Самостійна_робота_Файлова_система.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()