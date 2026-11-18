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

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

COLOR_DARK = "#1D1D1F"
COLOR_GRAY = "#86868B"
COLOR_CARD = "#F5F5F7"
COLOR_BORDER = "#E5E5EA"
ACCENTS = {
    "blue": "#0071E3",
    "green": "#248A3D",
    "orange": "#C93400",
    "red": "#C4001D",
    "purple": "#6E30A8",
}


def save_scheme(fig, name):
    fig.savefig(
        os.path.join(OUTPUT_DIR, f"{name}.png"),
        dpi=220,
        bbox_inches="tight",
        pad_inches=0.15,
    )
    fig.savefig(
        os.path.join(OUTPUT_DIR, f"{name}.svg"),
        bbox_inches="tight",
        pad_inches=0.15,
    )
    plt.close(fig)


def draw_cards(cards, filename, title, figsize=(12, 3.6), card_w=2.55, gap=0.45, h=1.85):
    n = len(cards)
    total_w = n * card_w + (n - 1) * gap
    x0 = (12 - total_w) / 2

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.6)
    ax.axis("off")

    ax.text(
        6,
        3.35,
        title,
        ha="center",
        va="center",
        fontsize=14.5,
        fontweight="bold",
        color=COLOR_DARK,
    )

    y = 0.85
    for i, card in enumerate(cards):
        x = x0 + i * (card_w + gap)
        patch = FancyBboxPatch(
            (x, y),
            card_w,
            h,
            boxstyle="round,pad=0,rounding_size=0.18",
            facecolor=COLOR_CARD,
            edgecolor=COLOR_BORDER,
            linewidth=1.4,
        )
        ax.add_patch(patch)

        accent = card.get("accent", ACCENTS["blue"])
        ax.plot(
            [x + 0.15, x + card_w - 0.15],
            [y + h - 0.12, y + h - 0.12],
            color=accent,
            lw=3,
            solid_capstyle="round",
        )

        ax.text(
            x + card_w / 2,
            y + h * 0.68,
            card["title"],
            ha="center",
            va="center",
            fontsize=12.5,
            fontweight="bold",
            color=COLOR_DARK,
        )

        lines = card.get("lines", [])
        if lines:
            ax.text(
                x + card_w / 2,
                y + h * 0.32,
                "\n".join(lines),
                ha="center",
                va="center",
                fontsize=10.6,
                color=COLOR_DARK,
                linespacing=1.35,
            )

        if i < n - 1:
            arrow = FancyArrowPatch(
                (x + card_w + 0.05, y + h / 2),
                (x + card_w + gap - 0.05, y + h / 2),
                arrowstyle="-|>",
                mutation_scale=12,
                color=COLOR_GRAY,
                lw=1.4,
            )
            ax.add_patch(arrow)

    save_scheme(fig, filename)


def make_schemes():
    draw_cards(
        [
            {"title": "Сцена", "lines": ["візуальний", "результат"], "accent": ACCENTS["blue"]},
            {"title": "Спрайти", "lines": ["персонажі", "та об’єкти"], "accent": ACCENTS["green"]},
            {"title": "Палітра блоків", "lines": ["команди", "за категоріями"], "accent": ACCENTS["orange"]},
            {"title": "Поле скриптів", "lines": ["збирання", "алгоритму"], "accent": ACCENTS["purple"]},
        ],
        "scheme_scratch_interface",
        "Складові середовища Scratch",
    )

    draw_cards(
        [
            {"title": "Обрати спрайт", "lines": ["з бібліотеки", "або намалювати"], "accent": ACCENTS["blue"]},
            {"title": "Редагувати", "lines": ["костюм, розмір", "колір"], "accent": ACCENTS["green"]},
            {"title": "Додати скрипт", "lines": ["подія +", "команди"], "accent": ACCENTS["orange"]},
            {"title": "Запустити", "lines": ["прапорець", "або клавіша"], "accent": ACCENTS["red"]},
        ],
        "scheme_sprite_workflow",
        "Створення та запуск спрайта",
    )

    draw_cards(
        [
            {
                "title": "Рух",
                "lines": ["перемістити на 10", "поворот на 15°", "перейти в x:0 y:0"],
                "accent": ACCENTS["blue"],
            },
            {
                "title": "Вигляд",
                "lines": ["сказати «Привіт!»", "змінити костюм", "змінити розмір"],
                "accent": ACCENTS["green"],
            },
            {
                "title": "Керування",
                "lines": ["чекати 1 с", "повторити 10", "якщо <умова>"],
                "accent": ACCENTS["orange"],
            },
        ],
        "scheme_blocks_categories",
        "Базові категорії блоків",
    )

    draw_cards(
        [
            {"title": "Рівень 1", "lines": ["репродуктивний", "≈ 7 хв"], "accent": ACCENTS["green"]},
            {"title": "Рівень 2", "lines": ["продуктивний", "≈ 10 хв"], "accent": ACCENTS["orange"]},
            {"title": "Рівень 3", "lines": ["творчий", "≈ 10 хв"], "accent": ACCENTS["purple"]},
        ],
        "scheme_levels",
        "Три рівні практичних завдань",
    )


def set_run_font(run, size=14, bold=False, color=None, name="Times New Roman"):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color.replace("#", ""))

    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)


def add_para(doc, text="", bold=False, align=None, color=None, size=14, space_after=4, style=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color)
    return p


def add_heading_custom(doc, text, level=1):
    color = "#1F4E79" if level == 1 else "#2E75B6"
    return add_para(doc, text, bold=True, color=color, size=14, space_after=5)


def add_mixed_para(doc, parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    for text, mono in parts:
        run = p.add_run(text)
        if mono:
            set_run_font(run, size=14, name="Consolas", color="#C0392B")
        else:
            set_run_font(run, size=14)
    return p


def set_cell_background(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)

    for edge in ("top", "left", "bottom", "right"):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f"w:{edge}"
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ("sz", "val", "color", "space"):
                if key in edge_data:
                    element.set(qn(f"w:{key}"), str(edge_data[key]))


def add_callout(doc, text, fill="EAF2F8", border_color="0071E3"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Cm(16.0)
    set_cell_background(cell, fill)
    set_cell_border(cell, left={"sz": 28, "val": "single", "color": border_color})
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    set_run_font(run, size=14)


def add_numbered_list(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(item)
        set_run_font(run, size=14)


def add_bullet_list(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(item)
        set_run_font(run, size=14)


def numbered_paren(doc, items):
    for i, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        run_num = p.add_run(f"{i}) ")
        set_run_font(run_num, size=14)
        run_text = p.add_run(item)
        set_run_font(run_text, size=14)


def set_repeat_table_header(row):
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def set_col_widths(table, widths):
    for idx, width in enumerate(widths):
        table.columns[idx].width = Cm(width)
        for row in table.rows:
            row.cells[idx].width = Cm(width)


def add_table(doc, headers, rows, widths, mono_cols=None):
    mono_cols = mono_cols or set()
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    header_row = table.rows[0]
    set_repeat_table_header(header_row)
    for idx, header in enumerate(headers):
        cell = header_row.cells[idx]
        set_cell_background(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        set_run_font(run, size=12, bold=True, color="FFFFFF")

    for row_data in rows:
        row = table.add_row()
        for idx, value in enumerate(row_data):
            cell = row.cells[idx]
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(str(value))
            if idx in mono_cols:
                set_run_font(run, size=11.5, name="Consolas", color="#C0392B")
            else:
                set_run_font(run, size=12)

    set_col_widths(table, widths)
    return table


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    set_run_font(run, size=10)


def main():
    make_schemes()

    doc = Document()

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(14)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(5)
    style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    section = doc.sections[0]
    add_page_number(section.footer.paragraphs[0])

    add_para(
        doc,
        "ПРАКТИЧНЕ ЗАНЯТТЯ №9",
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        color="#1F4E79",
        size=14,
        space_after=3,
    )
    add_para(
        doc,
        "Тема: Виконавці Scratch. Керування спрайтом за допомогою скриптів.",
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        size=14,
        space_after=6,
    )

    add_heading_custom(doc, "Мета")
    add_para(
        doc,
        "Навчитися створювати та редагувати спрайти; навчитися керувати спрайтом за допомогою "
        "базових скриптів руху, вигляду та керування; розвивати практичні навички роботи в "
        "середовищі Scratch, уяву та творчі здібності через створення анімаційних ефектів; "
        "виховувати задоволення від миттєвого візуального результату власних дій і стимулювати "
        "творчу активність.",
    )

    add_heading_custom(doc, "Обладнання та програмне забезпечення")
    numbered_paren(
        doc,
        [
            "інструкційні картки;",
            "персональний комп’ютер;",
            "середовище Scratch 3.0 (онлайн або офлайн);",
            "проєктор для демонстрації.",
        ],
    )

    add_heading_custom(doc, "Література")
    add_numbered_list(
        doc,
        [
            "Морзе Н. В., Вембер В. П. Інформатика (рівень стандарт) : підручник для 10 класу закладів загальної середньої освіти. Київ : Оріон, 2023.",
            "Ривкінд Й. Я., Лисенко Т. І., Чернікоєва Л. А., Шакотько В. В. Інформатика (рівень стандарт) : підручник для 10 класу закладів загальної середньої освіти. Київ : Генеза, 2023.",
            "Руденко В. Д., Речич Н. В., Потієнко В. О. Інформатика (рівень стандарт) : підручник для 10 класу закладів загальної середньої освіти. Харків : Ранок, 2023.",
        ],
    )

    add_heading_custom(doc, "Теоретичні відомості")

    add_heading_custom(doc, "1. Середовище Scratch і спрайти", level=2)
    add_para(
        doc,
        "Scratch — це візуальне середовище програмування, у якому алгоритм збирають із готових "
        "блоків. Основні частини середовища: сцена, список спрайтів, палітра блоків і робоче поле "
        "скриптів. Сцена показує результат виконання програми, а спрайт є виконавцем, яким керують "
        "через скрипти.",
    )
    doc.add_picture(os.path.join(OUTPUT_DIR, "scheme_scratch_interface.png"), width=Cm(16.0))
    add_callout(
        doc,
        "Спрайт — це персонаж або об’єкт на сцені. У кожного спрайта є ім’я, координати, напрям, "
        "розмір і набір костюмів. Скрипт спрайта визначає, як саме він рухається, змінюється та "
        "реагує на події.",
        fill="EAF2F8",
        border_color="0071E3",
    )

    add_heading_custom(doc, "2. Створення та редагування спрайта", level=2)
    add_para(
        doc,
        "Спрайт можна обрати з бібліотеки, намалювати самостійно, завантажити зображення або "
        "створити за допомогою камери. Редактор спрайта дає змогу змінювати костюми, розмір, "
        "колір, положення та інші властивості. Для анімації часто використовують кілька костюмів "
        "одного спрайта.",
    )
    doc.add_picture(os.path.join(OUTPUT_DIR, "scheme_sprite_workflow.png"), width=Cm(16.0))
    add_callout(
        doc,
        "Якщо спрайт має кілька костюмів, команда зміни костюма створює ефект руху, крокування, "
        "помаху крил або іншої простої анімації. Костюми зручно редагувати в розділі «Костюми».",
        fill="FFF4E6",
        border_color="C93400",
    )

    add_heading_custom(doc, "3. Скрипти: події, рух, вигляд і керування", level=2)
    add_para(
        doc,
        "Скрипт починається з події, наприклад «коли натиснуто прапорець». Далі додають команди "
        "руху, вигляду та керування. Команди руху змінюють координати й напрям спрайта, команди "
        "вигляду — його текст, костюм, розмір і ефекти, а команди керування задають послідовність, "
        "повторення, очікування та умови.",
    )
    doc.add_picture(os.path.join(OUTPUT_DIR, "scheme_blocks_categories.png"), width=Cm(16.0))

    add_para(doc, "Таблиця 1. Базові блоки для керування спрайтом", bold=True, space_after=3)
    add_table(
        doc,
        ["Категорія", "Приклад блоку", "Призначення"],
        [
            ["Рух", "перемістити на 10", "змінює положення спрайта на сцені"],
            ["Вигляд", "сказати «Привіт!»", "показує текст або змінює вигляд спрайта"],
            ["Керування", "повторити 10", "забезпечує повторення дій"],
            ["Події", "коли натиснуто прапорець", "запускає скрипт"],
        ],
        widths=[3.2, 6.0, 6.5],
        mono_cols={1},
    )

    add_heading_custom(doc, "4. Цикли та умови в керуванні спрайтом", level=2)
    add_para(
        doc,
        "Для повторюваних дій використовують блоки «повторити» та «завжди». Наприклад, спрайт може "
        "рухатися по колу, постійно змінюючи напрям. Умова «якщо» дає змогу перевірити положення "
        "спрайта, торкання краю або натискання клавіші. Поєднання циклу й умови робить поведінку "
        "спрайта схожою на гру або анімацію.",
    )
    add_mixed_para(
        doc,
        [
            ("Наприклад, скрипт із блоків ", False),
            ("коли натиснуто прапорець", True),
            (" → ", False),
            ("повторити 10", True),
            (" → ", False),
            ("перемістити на 10", True),
            (" → ", False),
            ("наступний костюм", True),
            (" створює просту анімацію руху.", False),
        ],
    )

    add_heading_custom(doc, "5. Анімаційні ефекти та взаємодія", level=2)
    add_para(
        doc,
        "Анімаційні ефекти в Scratch створюють через зміну костюмів, розміру, кольору, прозорості "
        "та положення. Для взаємодії спрайтів використовують повідомлення, наприклад «надіслати "
        "повідомлення» та «коли я отримую повідомлення». Це дає змогу будувати діалоги, сцени та "
        "невеликі ігри.",
    )
    add_callout(
        doc,
        "Після завершення роботи збережіть проєкт у форматі .sb3. Для звіту також підготуйте "
        "скріншот скриптів і коротко поясніть, які блоки використано для руху, вигляду та керування.",
        fill="EDF7ED",
        border_color="248A3D",
    )

    add_heading_custom(doc, "Покроковий алгоритм виконання різнорівневих завдань")
    add_para(
        doc,
        "Практична частина триває 25–30 хв. Виконуйте завдання послідовно: кожен наступний рівень "
        "ускладнює попередній і завершується творчим мініпроєктом.",
    )
    doc.add_picture(os.path.join(OUTPUT_DIR, "scheme_levels.png"), width=Cm(16.0))

    add_heading_custom(doc, "Рівень 1. Репродуктивний (≈ 7 хв)", level=2)
    add_table(
        doc,
        ["Крок", "Дія", "Команда / блок"],
        [
            ["1", "Відкрити Scratch і створити новий проєкт", "Новий проєкт"],
            ["2", "Обрати спрайт із бібліотеки", "Обрати спрайт"],
            ["3", "Додати подію запуску", "коли натиснуто прапорець"],
            ["4", "Додати рух спрайта", "перемістити на 10"],
            ["5", "Запустити та перевірити результат", "прапорець"],
        ],
        widths=[1.5, 8.2, 6.0],
        mono_cols={2},
    )

    add_heading_custom(doc, "Рівень 2. Продуктивний (≈ 10 хв)", level=2)
    add_table(
        doc,
        ["Крок", "Дія", "Команда / блок"],
        [
            ["1", "Створити подію запуску", "коли натиснуто прапорець"],
            ["2", "Додати повторення руху", "повторити 10"],
            ["3", "Додати переміщення", "перемістити на 10"],
            ["4", "Додати зміну костюма", "наступний костюм"],
            ["5", "Додати паузу", "чекати 0.2 с"],
            ["6", "Додати відбивання від краю", "якщо на межі, відбити"],
            ["7", "Запустити та перевірити анімацію", "прапорець"],
        ],
        widths=[1.5, 8.2, 6.0],
        mono_cols={2},
    )

    add_heading_custom(doc, "Рівень 3. Творчий (≈ 10 хв)", level=2)
    add_para(
        doc,
        "Створіть коротку анімацію з двома спрайтами: один спрайт рухається й змінює костюм, "
        "другий реагує на його наближення або отримує повідомлення. Додайте щонайменше один ефект "
        "вигляду та одну умову. Продемонструйте результат групі.",
    )
    add_table(
        doc,
        ["Вимога", "Опис"],
        [
            ["Спрайти", "використано щонайменше два спрайти"],
            ["Рух", "є цикл і переміщення"],
            ["Вигляд", "є зміна костюма або розміру"],
            ["Керування", "є умова або повідомлення"],
        ],
        widths=[4.5, 11.2],
    )

    add_heading_custom(doc, "Критерії оцінювання")
    add_table(
        doc,
        ["Вид роботи", "Критерій", "Бали"],
        [
            ["Рівень 1", "відтворено базовий скрипт руху спрайта", "4"],
            ["Рівень 2", "використано цикл, зміну костюмів і умову", "5"],
            ["Рівень 3", "створено творчий мініпроєкт з анімацією", "4"],
            ["Разом", "максимальна кількість балів", "13"],
        ],
        widths=[3.5, 10.2, 2.0],
    )

    add_heading_custom(doc, "Форма звітності")
    add_bullet_list(
        doc,
        [
            "збережений файл проєкту у форматі .sb3;",
            "скріншот вікна Scratch зі створеними скриптами;",
            "коротке усне пояснення використаних блоків руху, вигляду та керування;",
            "висновок про досягнення мети заняття.",
        ],
    )

    doc.save("Практичне_заняття_9_Scratch.docx")
    print("Створено документ: Практичне_заняття_9_Scratch.docx")
    print("Схеми збережено в папці: output/ (PNG + SVG)")


if __name__ == "__main__":
    main()