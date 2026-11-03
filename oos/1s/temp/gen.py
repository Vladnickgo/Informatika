# -*- coding: utf-8 -*-
"""
Генератор docx-матеріалу з дисципліни "Основи операційних систем"
Тип матеріалу: ЛЕКЦІЯ
Тема: Операційна система: поняття, призначення, складові та класифікація
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
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


def scheme_layers():
    """Схема 1: Користувач → Програми → ОС → Апаратне забезпечення."""
    fig, ax = plt.subplots(figsize=(8.2, 6.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    layers = [
        ("КОРИСТУВАЧ\n(учень, учитель)", "#1F4E79", 8.7, "white"),
        ("ПРИКЛАДНІ ПРОГРАМИ\nредактор, браузер, навчальні тренажери", "#2E75B6", 6.7, "white"),
        ("ОПЕРАЦІЙНА СИСТЕМА\nядро · драйвери · файлова система · інтерфейс", "#F4B183", 4.5, "#1a1a1a"),
        ("АПАРАТНЕ ЗАБЕЗПЕЧЕННЯ\nпроцесор · пам'ять · диски · пристрої", "#548235", 2.3, "white"),
    ]

    x0, w, h = 1.0, 8.0, 1.5
    for text, color, y, tc in layers:
        box = FancyBboxPatch((x0, y - h / 2), w, h,
                             boxstyle="round,pad=0.02,rounding_size=0.18",
                             linewidth=1.6, edgecolor="#333333", facecolor=color)
        ax.add_patch(box)
        ax.text(x0 + w / 2, y, text, ha="center", va="center",
                fontsize=11, color=tc, fontweight="bold",
                family="DejaVu Sans", linespacing=1.4)

    ys = [8.7, 6.7, 4.5, 2.3]
    for i in range(len(ys) - 1):
        y_top = ys[i] - h / 2
        y_bot = ys[i + 1] + h / 2
        ax.add_patch(FancyArrowPatch((5.0, y_top), (5.0, y_bot),
                                     arrowstyle="<|-|>,head_width=4,head_length=9",
                                     mutation_scale=1.0, color="#7F7F7F", linewidth=1.8))

    ax.text(5.0, 9.6, "Схема 1. Роль операційної системи",
            ha="center", va="center", fontsize=12, fontweight="bold",
            family="DejaVu Sans", color="#1F4E79")
    ax.text(5.6, 5.6, "запити", ha="left", va="center", fontsize=9,
            style="italic", color="#595959", family="DejaVu Sans")
    ax.text(4.4, 5.6, "результати", ha="right", va="center", fontsize=9,
            style="italic", color="#595959", family="DejaVu Sans")
    return _save(fig, "scheme_os_layers")


def scheme_components():
    """Схема 2: складові операційної системи."""
    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")

    cx, cy = 6.0, 3.9
    comps = [
        ("ЯДРО\n(керує процесами)", 1.9, 6.5),
        ("ДРАЙВЕРИ\n(«перекладачі»)", 6.0, 7.0),
        ("ФАЙЛОВА\nСИСТЕМА", 10.1, 6.5),
        ("ІНТЕРФЕЙС\nКОРИСТУВАЧА", 1.9, 1.3),
        ("СЛУЖБОВІ\nПРОГРАМИ", 6.0, 0.8),
        ("МЕРЕЖЕВІ\nЗАСОБИ", 10.1, 1.3),
    ]

    for _, x, y in comps:
        ax.add_patch(FancyArrowPatch((x, y), (cx, cy),
                                     arrowstyle="-|>", mutation_scale=14,
                                     color="#2E75B6", linewidth=1.6))

    for text, x, y in comps:
        bw, bh = 2.5, 1.15
        ax.add_patch(FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor="#DEEAF6", edgecolor="#2E75B6",
                                    linewidth=1.5))
        ax.text(x, y, text, ha="center", va="center", fontsize=9,
                color="#1F4E79", fontweight="bold",
                family="DejaVu Sans", linespacing=1.3)

    cw, ch = 3.2, 1.6
    ax.add_patch(FancyBboxPatch((cx - cw / 2, cy - ch / 2), cw, ch,
                                boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor="#1F4E79", edgecolor="#0D2A42",
                                linewidth=1.8))
    ax.text(cx, cy, "ОПЕРАЦІЙНА\nСИСТЕМА", ha="center", va="center",
            fontsize=12, color="white", fontweight="bold",
            family="DejaVu Sans", linespacing=1.4)

    ax.text(6.0, 7.7, "Схема 2. Основні складові операційної системи",
            ha="center", va="center", fontsize=12, fontweight="bold",
            family="DejaVu Sans", color="#1F4E79")
    return _save(fig, "scheme_os_components")


def scheme_file_tree():
    """Схема 3: ієрархія файлової системи (навчальна аналогія)."""
    fig, ax = plt.subplots(figsize=(9.6, 6.0))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")

    def box(x, y, text, fc="#DEEAF6", ec="#2E75B6", tc="#1F4E79", fs=9):
        bw, bh = 1.9, 0.85
        ax.add_patch(FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=fc, edgecolor=ec, linewidth=1.4))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs,
                color=tc, fontweight="bold", family="DejaVu Sans")

    def link(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color="#8FAADC", linewidth=1.5, zorder=0)

    root = (6.0, 7.1)
    lvl1 = [(3.0, 4.9, "Навчання"), (6.0, 4.9, "Фото"), (9.0, 4.9, "Програми")]
    lvl2 = [(1.6, 2.4, "Звіти"), (4.4, 2.4, "Плани"),
            (6.0 - 1.4, 2.4, "Родина"), (6.0 + 1.4, 2.4, "Свято"),
            (7.6, 2.4, "Офіс"), (10.4, 2.4, "Ігри")]

    box(root[0], root[1], "Диск C:", fc="#1F4E79", ec="#0D2A42", tc="white", fs=10)
    for x, y, t in lvl1:
        link(root[0], root[1] - 0.42, x, y + 0.42)
        box(x, y, t)
    for i, (x, y, t) in enumerate(lvl2):
        px, py, _ = lvl1[i // 2]
        link(px, py - 0.42, x, y + 0.42)
        box(x, y, t, fc="#EAF1DD", ec="#548235", tc="#375623")

    ax.text(6.0, 0.9, "Схема 3. Ієрархія файлової системи: «шафа → полиця → папка»",
            ha="center", va="center", fontsize=11, fontweight="bold",
            family="DejaVu Sans", color="#1F4E79")
    return _save(fig, "scheme_file_tree")


# ============================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ DOCX
# ============================================================

FONT = "Times New Roman"
BLUE = RGBColor(0x1F, 0x4E, 0x79)
DARK = RGBColor(0x1A, 0x1A, 0x1A)


def _style_run(run, size=14, bold=False, italic=False, color=None):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rpr = run._r.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    rf.set(qn("w:ascii"), FONT)
    rf.set(qn("w:hAnsi"), FONT)
    rf.set(qn("w:cs"), FONT)
    rf.set(qn("w:eastAsia"), FONT)
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
    img1 = scheme_layers()
    img2 = scheme_components()
    img3 = scheme_file_tree()

    doc = Document()

    # --- базовий стиль ---
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

    # ---------- Шапка ----------
    h1(doc, "Лекція 1. Операційна система: поняття, призначення, складові та класифікація")

    body(doc, "«Основи операційних систем» · спеціальність 013 Початкова освіта "
              "(Вчитель інформатики початкової школи)", space_after=10)

    # ---------- Мета ----------
    h2(doc, "Мета лекції")
    body(doc, "сформувати у майбутніх учителів інформатики початкової школи цілісне "
              "уявлення про операційну систему як базове програмне забезпечення "
              "комп'ютера; розкрити її призначення, основні складові та підходи до "
              "класифікації; навчити добирати доступні учням 1–4 класів аналогії для "
              "пояснення складних технічних понять.")

    # ---------- Ключові поняття ----------
    h2(doc, "Ключові поняття")
    body(doc, "операційна система, ядро, драйвер, файлова система, інтерфейс "
              "користувача, графічний інтерфейс, командний рядок, багатозадачність, "
              "утиліта, програмне забезпечення.")

    # ---------- План ----------
    h2(doc, "План лекції")
    plan = [
        "Поняття операційної системи. Місце ОС серед програмного забезпечення.",
        "Призначення та основні функції операційної системи.",
        "Архітектура ОС: ядро, драйвери, оболонка, службові програми.",
        "Файлова система та принципи зберігання даних.",
        "Класифікація операційних систем.",
        "Операційна система у змісті початкового курсу інформатики.",
    ]
    for item in plan:
        numbered(doc, item)

    # ---------- Блок 1 ----------
    h2(doc, "1. Поняття операційної системи")
    body(doc, "Операційна система (ОС) — це комплекс взаємопов'язаних програм, які "
              "забезпечують керування апаратним забезпеченням комп'ютера, запуск і "
              "взаємодію прикладних програм та зручний інтерфейс для користувача. "
              "Без операційної системи комп'ютер — це набір деталей, які «не знають», "
              "що їм робити разом.")

    callout(doc, "Аналогія для пояснення учням початкової школи.",
            "Уявіть шкільний оркестр. Музичні інструменти — це апаратне забезпечення "
            "(процесор, пам'ять, принтер). Музиканти — прикладні програми. А диригент, "
            "який змахує паличкою і домовляється, хто коли грає, — це операційна "
            "система. Без диригента кожен музикант грає своє, і виходить шум. "
            "З диригентом — виходить слаженний твір.")

    body(doc, "Операційна система належить до системного програмного забезпечення. "
              "Вона завантажується першою після ввімкнення комп'ютера і працює до "
              "моменту його вимкнення, «супроводжуючи» всі дії користувача. "
              "Найпоширеніші приклади: Windows, Linux, macOS, Android, iOS.")

    # ---------- Блок 2 ----------
    h2(doc, "2. Призначення та основні функції ОС")
    body(doc, "Узагальнено всі операційні системи виконують дві групи функцій: "
              "взаємодію з апаратним забезпеченням та взаємодію з користувачем і "
              "прикладними програмами. Конкретно це проявляється так:")

    functions = [
        ("Керування пристроями — ", "ОС «розмовляє» з процесором, пам'яттю, "
         "дисками, принтером, мишею і клавіатурою зрозумілою їм мовою."),
        ("Керування файлами — ", "створення, збереження, перейменування, "
         "копіювання та видалення папок і документів."),
        ("Розподіл ресурсів — ", "ОС вирішує, якій програмі скільки пам'яті та "
         "часу процесора надати, щоб усі працювали одночасно."),
        ("Запуск і завершення програм — ", "саме ОС «відкриває двері» програмі, "
         "коли користувач двічі клацає ярлик."),
        ("Забезпечення інтерфейсу — ", "надає користувачу робочий стіл, вікна, "
         "меню, кнопки (графічний інтерфейс) або командний рядок."),
        ("Захист даних і розмежування доступу — ", "паролі, облікові записи, "
         "права користувачів, антивірусні механізми."),
    ]
    for lead, txt in functions:
        bullet(doc, txt, bold_lead=lead)

    callout(doc, "Методична підказка.",
            "У 3–4 класі доречно запропонувати учням порівняти ОС із завгоспом школи: "
            "він видає ключі від кабінетів (доступ до ресурсів), стежить, щоб у класі "
            "не було одночасно двох уроків (багатозадачність), веде облік інвентарю "
            "(файлова система). Такий образ добре запам'ятовується і не спрощує "
            "сутність явища до рівня «віконечка на екрані».",
            fill="FFF4E5", accent="C55A11")

    # ---------- Блок 3 ----------
    h2(doc, "3. Архітектура операційної системи")
    body(doc, "Операційна система — це «прошарок» між людиною та залізом. "
              "Схематично її місце в роботі комп'ютера показано на схемі 1.")

    add_figure(doc, img1, 15.0)

    body(doc, "Як бачимо, користувач безпосередньо не «торкається» процесора чи "
              "диска. Усі його команди проходять через прикладні програми, а ті — "
              "через операційну систему, яка перетворює їх на зрозумілі апаратурі "
              "сигнали. Зворотно до користувача надходять результати: зображення на "
              "екрані, звук, надрукований документ.")

    body(doc, "Внутрішньо операційна система складається з кількох частин. "
              "Їхню взаємодію відображено на схемі 2.")

    add_figure(doc, img2, 15.5)

    add_table(
        doc,
        ["Складова ОС", "Що робить", "Аналогія зі шкільного життя"],
        [
            ["Ядро", "Постійно перебуває в оперативній пам'яті, керує процесами, "
                     "пам'яттю та пристроями", "Директор школи, який ухвалює ключові рішення"],
            ["Драйвери", "Програми-«перекладачі», що пояснюють ОС, як працювати з "
                         "конкретним пристроєм", "Перекладачі для іноземних гостей"],
            ["Файлова система", "Зберігає файли й папки, веде їх облік і пошук",
             "Бібліотекар, який знає, де стоїть кожна книжка"],
            ["Інтерфейс користувача", "Забезпечує спосіб спілкування людини з "
                                      "комп'ютером (вікна, меню, команди)",
             "Вітрина та адміністратор на вході"],
            ["Службові програми (утиліти)", "Обслуговують систему: очищення дисків, "
                                            "архівування, перевірка на віруси",
             "Завгосп і медсестра: лагодять, прибирають, дбають про порядок"],
        ],
        widths=[4.2, 6.5, 5.8],
    )

    # ---------- Блок 4 ----------
    h2(doc, "4. Файлова система")
    body(doc, "Файл — це поіменована область на носії інформації, у якій зберігаються "
              "дані (текст, малюнок, відео, програма). Файли об'єднуються в папки "
              "(каталоги), папки — у папки вищого рівня, і так утворюється ієрархія — "
              "дерево файлової системи.")

    add_figure(doc, img3, 15.5)

    body(doc, "Ім'я файлу складається з власне назви та розширення, яке вказує на тип "
              "вмісту: .txt — текст, .docx — документ, .jpg — зображення, .mp4 — відео, "
              ".exe — програма. Розширення допомагає операційній системі зрозуміти, "
              "якою програмою відкривати файл.")

    bullet(doc, "шлях до файлу — послідовність папок від диска до файлу, "
                "наприклад: C:\\Навчання\\Плани\\урок_1.docx;")
    bullet(doc, "повне ім'я файлу — шлях разом з іменем та розширенням;")
    bullet(doc, "атрибути файлу — «тільки для читання», «прихований», дата змінення, "
                "розмір.")

    # ---------- Блок 5 ----------
    h2(doc, "5. Класифікація операційних систем")
    body(doc, "Операційні системи розрізняють за кількома ознаками. Узагальнену "
              "класифікацію подано в таблиці.")

    add_table(
        doc,
        ["Ознака класифікації", "Види", "Приклади"],
        [
            ["Кількість користувачів", "Одно- та багатокористувацькі",
             "Windows 10/11, Linux, Windows Server"],
            ["Кількість задач", "Одно- та багатозадачні",
             "MS-DOS (одно), Windows, Linux (багато)"],
            ["Тип інтерфейсу", "З командним рядком / з графічним інтерфейсом",
             "MS-DOS / Windows, macOS, Linux"],
            ["Призначення", "Універсальні, серверні, мобільні, вбудовані (IoT)",
             "Windows, Windows Server, Android,嵌入式 Linux"],
            ["Модель розповсюдження", "Пропрієтарні (платні) та вільні",
             "Windows, macOS / Linux, FreeBSD"],
        ],
        widths=[4.6, 6.4, 5.5],
    )

    callout(doc, "Цікавий факт для учнів.",
            "Найпоширенішою операційною системою у світі є не Windows, а Android — "
            "саме вона встановлена на більшості смартфонів і планшетів. А на "
            "суперкомп'ютерах, які моделюють клімат і космос, майже завжди працює "
            "Linux.",
            fill="E2EFDA", accent="548235")

    # ---------- Блок 6 ----------
    h2(doc, "6. Операційна система у змісті початкового курсу інформатики")
    body(doc, "У початковій школі учні не вивчають архітектуру ОС, однак щодня з нею "
              "працюють. Тому вчителю важливо сформувати такі практичні вміння:")
    bullet(doc, "увімкнення та коректне вимкнення комп'ютера;")
    bullet(doc, "орієнтування на робочому столі, запуск програм через ярлики;")
    bullet(doc, "робота з вікнами: відкрити, згорнути, розгорнути, закрити;")
    bullet(doc, "створення, збереження та відкриття власних файлів у визначеній папці;")
    bullet(doc, "дотримання правил безпечної роботи з комп'ютером.")

    callout(doc, "Методична підказка.",
            "Не варто починати знайомство з темою з термінів. Почніть із запитання: "
            "«Що станеться, якщо ввімкнути комп'ютер, а операційна система не "
            "завантажиться?» Далі — спільне формулювання висновку: ОС — це "
            "«головний помічник», без якого «залізо» не працює.",
            fill="FFF4E5", accent="C55A11")

    # ---------- Контрольні питання ----------
    h2(doc, "Контрольні питання")
    questions = [
        "Дайте означення операційної системи. До якого виду програмного "
        "забезпечення вона належить?",
        "Чому комп'ютер не може працювати без операційної системи? Наведіть "
        "побутову аналогію.",
        "Назвіть і охарактеризуйте основні функції операційної системи.",
        "Що таке ядро ОС і чому його називають «серцем» системи?",
        "Поясніть роль драйверів. Наведіть приклад ситуації, коли без драйвера "
        "пристрій не працює.",
        "Що таке файлова система? Які об'єкти вона впорядковує?",
        "З яких частин складається ім'я файлу? Навіщо потрібне розширення?",
        "За якими ознаками класифікують операційні системи? Наведіть приклади.",
        "Чим графічний інтерфейс відрізняється від командного рядка? Який зручніший "
        "для молодших школярів і чому?",
        "Які практичні вміння роботи з ОС має сформувати вчитель в учнів 1–4 класів?",
        "Запропонуйте власну аналогію для пояснення учням поняття «операційна "
        "система». Обґрунтуйте її доцільність.",
    ]
    for q in questions:
        numbered(doc, q)

    # ---------- Література ----------
    h2(doc, "Рекомендовані джерела")
    bullet(doc, "Морзе Н. В., Барна О. В. Інформатика : підручник для 4 класу "
                "закладів загальної середньої освіти. — К. : УОВЦ «Оріон», 2021.")
    bullet(doc, "Ривкінд Й. Я., Лисенко Т. І., Чернікова Л. А., Шакотько В. В. "
                "Інформатика : підручник для 4 класу. — К. : Генеза, 2021.")
    bullet(doc, "Таненбаум Е., Бос Х. Сучасні операційні системи. — 4-те вид. — "
                "СПб. : Пітер, 2015.")
    bullet(doc, "Сайт Microsoft Learn — розділ «Windows for education».")

    doc.save("Лекція_1_Операційна_система.docx")
    print("Готово: Лекція_1_Операційна_система.docx")
    print("Схеми збережено у папці:", os.path.abspath(OUT))


if __name__ == "__main__":
    build_document()