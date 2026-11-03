# -*- coding: utf-8 -*-
"""
Генерація DOCX-документа для самостійної роботи №4
Тема: Методика аналізу науково-педагогічної літератури та формулювання робочої гіпотези
"""

import os
import io
import zlib
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT_DIR = "output"
IMG_DIR = os.path.join(OUTPUT_DIR, "img")
os.makedirs(IMG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Допоміжні функції
# ---------------------------------------------------------------------------

def render_plantuml(uml_code: str, filename: str) -> str:
    """
    Рендерить PlantUML-схему у PNG.
    Використовує публічний сервер. Для офлайн-режиму:
        - встановіть plantuml.jar
        - замініть тіло функції на subprocess.run(["java","-jar","plantuml.jar",...])
    """
    path = os.path.join(IMG_DIR, filename)
    if os.path.exists(path):
        return path
    try:
        # PlantUML використовує deflate + власне кодування
        compressed = zlib.compress(uml_code.encode("utf-8"))[2:-4]
        # кодування PlantUML (спрощене через hex-варіант ~h)
        hex_code = "~h" + compressed.hex()
        url = f"http://www.plantuml.com/plantuml/png/{hex_code}"
        r = requests.get(url, timeout=30)
        if r.status_code == 200 and r.content[:8] == b"\x89PNG\r\n\x1a\n":
            with open(path, "wb") as f:
                f.write(r.content)
            return path
    except Exception as e:
        print(f"[PlantUML] Не вдалося відрендерити {filename}: {e}")
    # fallback — створимо просту заглушку
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.text(0.5, 0.5, f"[PlantUML схема: {filename}]\n(не вдалося завантажити)",
            ha="center", va="center", fontsize=12)
    ax.axis("off")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def set_cell_background(cell, color_hex: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color_hex)
    tc_pr.append(shd)


def add_heading(doc, text, level=1, color="1F3864"):
    h = doc.add_heading(level=level)
    run = h.add_run(text)
    run.font.color.rgb = RGBColor.from_string(color)
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    return h


def add_paragraph(doc, text, bold=False, italic=False, size=12, align=None, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    if align:
        p.alignment = align
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.left_indent = Cm(0.63 + level * 0.63)
    for run in p.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
    return p


def add_numbered(doc, text):
    p = doc.add_paragraph(text, style="List Number")
    for run in p.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
    return p


def add_image(doc, path, width_cm=15.5, caption=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cp.add_run(caption)
        r.italic = True
        r.font.size = Pt(10)
        r.font.name = "Times New Roman"


def add_table(doc, headers, rows, col_widths=None, header_fill="1F3864"):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = "Times New Roman"
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(hdr[i], header_fill)
    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(11)
            run.font.name = "Times New Roman"
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)
    return table


# ---------------------------------------------------------------------------
# Побудова діаграми (структура повідомлення — "пиріг" таймінгу)
# ---------------------------------------------------------------------------

def make_timing_chart() -> str:
    path = os.path.join(IMG_DIR, "timing_chart.png")
    labels = [
        "Вибір теми\n(3 хв)",
        "Пошук джерел\n(5 хв)",
        "Опрацювання\nджерел (7 хв)",
        "Формулювання\nгіпотези (8 хв)",
        "Оформлення\nвисновків (5 хв)",
        "Самоперевірка\n(2 хв)",
    ]
    sizes = [3, 5, 7, 8, 5, 2]
    colors = ["#4472C4", "#5B9BD5", "#70AD47", "#FFC000", "#ED7D31", "#A5A5A5"]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.0f%%",
        colors=colors, startangle=90,
        textprops={"fontsize": 10, "fontname": "DejaVu Sans"},
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")
    ax.set_title("Розподіл часу на виконання самостійної роботи (30 хв)",
                 fontsize=13, fontweight="bold", pad=15)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def make_hypothesis_scheme() -> str:
    """Схема структури гіпотези (без PlantUML — matplotlib для надійності)."""
    path = os.path.join(IMG_DIR, "hypothesis_scheme.png")
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    boxes = [
        (0.3, 1.5, 2.6, 1.4, "УМОВА\n(фактор впливу)", "#4472C4"),
        (4.2, 1.5, 2.6, 1.4, "ОЧІКУВАНИЙ\nРЕЗУЛЬТАТ", "#70AD47"),
        (8.1, 1.5, 2.6, 1.4, "ПЕРЕВІРКА\n(метод)", "#ED7D31"),
    ]
    for x, y, w, h, text, color in boxes:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                             linewidth=2, edgecolor=color, facecolor=color + "33")
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=12, fontweight="bold", color="#1F3864")

    arrows = [
        (2.95, 2.2, 4.15, 2.2),
        (6.85, 2.2, 8.05, 2.2),
    ]
    for x1, y1, x2, y2 in arrows:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="->", mutation_scale=25,
                                     linewidth=2.5, color="#1F3864"))

    ax.text(5.5, 3.7, "«ЯКЩО ... , ТО ... , ЗА УМОВИ ...»",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="#C00000",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF2CC", edgecolor="#C00000"))
    ax.text(5.5, 0.6, "Структура робочої гіпотези педагогічного дослідження",
            ha="center", va="center", fontsize=11, style="italic", color="#404040")

    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# PlantUML-схеми
# ---------------------------------------------------------------------------

PUML_LITERATURE = """
@startuml
skinparam backgroundColor #FEFEFE
skinparam defaultFontName "DejaVu Sans"
skinparam defaultFontSize 12
skinparam rectangle {
    BackgroundColor #E8F0FE
    BorderColor #1F3864
}
skinparam arrowColor #1F3864

title Етапи аналізу науково-педагогічної літератури

start
:Визначення теми та проблеми дослідження;
:Пошук джерел (каталоги, Google Scholar, фахові журнали);
:Відбір 5-7 релевантних джерел;
:Читання та конспектування (2-3 ключові тези на джерело);
:Групування джерел за тематичними напрямами;
:Виявлення досліджених аспектів і прогалин;
:Формулювання робочої гіпотези;
:Визначення методу перевірки гіпотези;
stop
@enduml
"""

PUML_REPORT_STRUCTURE = """
@startuml
skinparam backgroundColor #FEFEFE
skinparam defaultFontName "DejaVu Sans"
skinparam defaultFontSize 11
skinparam packageStyle rectangle

title Структура повідомлення студента

package "ПОВІДОМЛЕННЯ" {
  rectangle "1. Тема дослідження" as T1 #DEEBF7
  rectangle "2. Актуальність (2-3 речення)" as T2 #DEEBF7
  rectangle "3. Аналіз 5-7 джерел\\n(ключові тези)" as T3 #C6E0B4
  rectangle "4. Систематизація джерел\\n(напрями / прогалини)" as T4 #C6E0B4
  rectangle "5. Робоча гіпотеза\\n(якщо..., то...)" as T5 #FFE699
  rectangle "6. Метод перевірки гіпотези" as T6 #FFE699
  rectangle "7. Висновки + джерела" as T7 #F4B183
}

T1 --> T2
T2 --> T3
T3 --> T4
T4 --> T5
T5 --> T6
T6 --> T7
@enduml
"""

PUML_TIMELINE = """
@startuml
skinparam backgroundColor #FEFEFE
skinparam defaultFontName "DejaVu Sans"
skinparam defaultFontSize 11
skinparam sequenceArrowColor #1F3864
skinparam sequenceLifeLineBorderColor #1F3864

title Часова шкала виконання (30 хв)

|#4472C4|Студент|
|#70AD47|Керівник|

|Студент|
start
:0-3 хв\nВибір теми, формулювання актуальності;
:3-8 хв\nПошук 5-7 джерел;
:8-15 хв\nОпрацювання: ключові тези;
:15-18 хв\nСистематизація за напрямами;
:18-26 хв\nФормулювання гіпотези + метод;
:26-28 хв\nВисновки;
:28-30 хв\nСамоперевірка за критеріями;
stop

|Керівник|
start
:Консультація на етапі вибору теми;
:Перевірка релевантності джерел;
:Фідбек щодо гіпотези;
stop
@enduml
"""


# ---------------------------------------------------------------------------
# Основна побудова документа
# ---------------------------------------------------------------------------

def build_document():
    doc = Document()

    # Базові налаштування
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)

    # ---- Титульна частина ----
    add_paragraph(doc, "САМОСТІЙНА РОБОТА № 4", bold=True, size=16,
                  align=WD_ALIGN_PARAGRAPH.CENTER, color="1F3864")
    add_paragraph(doc, "з дисципліни «Основи науково-педагогічних досліджень»",
                  size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "")
    add_paragraph(doc,
        "Тема: Методика аналізу науково-педагогічної літератури та формулювання робочої гіпотези дослідження",
        bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, color="C00000")
    add_paragraph(doc, "")

    # Мета
    add_heading(doc, "Мета та завдання", level=1)
    add_paragraph(doc, "Мета: підготовка повідомлення за результатами аналізу науково-педагогічної літератури та формулювання робочої гіпотези дослідження.")
    add_paragraph(doc, "Завдання:")
    add_bullet(doc, "формувати вміння аналізувати науково-педагогічну літературу;")
    add_bullet(doc, "розвивати вміння формулювати робочу гіпотезу;")
    add_bullet(doc, "розвивати аналітичне та критичне мислення під час роботи з джерелами;")
    add_bullet(doc, "виховувати повагу до наукових джерел та академічну доброчесність.")

    add_paragraph(doc, "Обладнання: інструкційні картки, комп'ютер з доступом до Інтернету (Google Scholar), бібліотечні каталоги.")
    add_paragraph(doc, "Тривалість виконання: 20-30 хв.")
    add_paragraph(doc, "Форма звітності: підготовлене повідомлення (текст + таблиці + схеми).")

    # Література
    add_heading(doc, "Рекомендована література", level=1)
    add_numbered(doc, "Кравець Н. П. Основи наукових досліджень: навчальний посібник. Київ: Вид-во НПУ імені М. П. Драгоманова, 2020. 74 с.")
    add_numbered(doc, "Методичні рекомендації щодо написання та оформлення курсової роботи. Путивль: КЗСОР «Путивльський педагогічний фаховий коледж імені С. В. Руднєва», 2024. 14 с.")

    doc.add_page_break()

    # ---- Теоретичний блок ----
    add_heading(doc, "Теоретичні відомості", level=1)

    add_heading(doc, "1. Аналіз науково-педагогічної літератури", level=2)
    add_paragraph(doc,
        "Аналіз науково-педагогічної літератури — це систематичне вивчення, "
        "опрацювання та узагальнення змісту наукових джерел з метою з'ясування "
        "стану розробленості обраної проблеми, виявлення прогалин у знаннях та "
        "визначення напрямів подальшого дослідження. Цей етап є фундаментом "
        "будь-якої наукової роботи, адже дозволяє досліднику не «винаходити "
        "велосипед», а спиратися на вже здобуті знання та розвивати їх.")

    add_paragraph(doc, "Основні види науково-педагогічних джерел:", bold=True)
    add_table(doc,
        ["Вид джерела", "Опис", "Приклади"],
        [
            ["Монографії", "Ґрунтовні наукові праці, присвячені одній темі", "Колективні монографії з педагогіки"],
            ["Підручники та посібники", "Систематизований виклад навчального матеріалу", "Підручники з методики викладання"],
            ["Наукові статті", "Результати конкретних досліджень у періодиці", "Фахові журнали («Педагогіка і психологія»)"],
            ["Дисертації та автореферати", "Кваліфікаційні роботи на здобуття наукових ступенів", "Кандидатські та докторські дисертації"],
            ["Матеріали конференцій", "Тези та доповіді науковців", "Збірники конференцій"],
            ["Нормативні документи", "Закони, стандарти, концепції", "Закон України «Про освіту», Держстандарт"],
        ],
        col_widths=[3.5, 6.0, 6.0],
    )

    # PlantUML: етапи аналізу
    add_paragraph(doc, "")
    add_paragraph(doc, "Схема 1. Етапи аналізу науково-педагогічної літератури", bold=True,
                  align=WD_ALIGN_PARAGRAPH.CENTER)
    puml_path_1 = render_plantuml(PUML_LITERATURE, "literature_stages.png")
    add_image(doc, puml_path_1, width_cm=9, caption="Рис. 1. Етапи аналізу літератури (PlantUML)")

    add_heading(doc, "2. Робоча гіпотеза дослідження", level=2)
    add_paragraph(doc,
        "Робоча гіпотеза — це наукове припущення про ймовірні зв'язки, "
        "закономірності або причини досліджуваного явища, яке висувається на "
        "початку дослідження і потребує перевірки. Вона є «робочою», оскільки "
        "ще не підтверджена остаточно і може бути скоригована в процесі дослідження.")

    add_paragraph(doc, "Вимоги до формулювання гіпотези:", bold=True)
    add_table(doc,
        ["Вимога", "Пояснення"],
        [
            ["Конкретність", "Гіпотеза має стосуватися чітко визначеного явища, а не бути загальною"],
            ["Перевірюваність", "Має існувати спосіб перевірити гіпотезу (експеримент, опитування)"],
            ["Однозначність", "Формулювання не повинно допускати подвійного тлумачення"],
            ["Обґрунтованість", "Гіпотеза має спиратися на аналіз літератури та попередні дослідження"],
            ["Новизна", "Гіпотеза має містити елемент нового знання"],
        ],
        col_widths=[4.0, 11.5],
    )

    # Схема гіпотези (matplotlib)
    add_paragraph(doc, "")
    add_paragraph(doc, "Схема 2. Структура робочої гіпотези", bold=True,
                  align=WD_ALIGN_PARAGRAPH.CENTER)
    hyp_path = make_hypothesis_scheme()
    add_image(doc, hyp_path, width_cm=16, caption="Рис. 2. Структура гіпотези: умова → очікуваний результат → перевірка")

    add_paragraph(doc, "Приклад гіпотези:", bold=True)
    add_paragraph(doc,
        "«Ми припускаємо, що використання інтерактивних методів навчання на уроках "
        "інформатики в початковій школі сприятиме підвищенню пізнавальної активності "
        "молодших школярів, якщо ці методи будуть систематично застосовуватися та "
        "враховувати вікові особливості учнів».", italic=True)

    add_heading(doc, "3. Академічна доброчесність", level=2)
    add_paragraph(doc, "Під час роботи з літературою необхідно дотримуватися:")
    add_bullet(doc, "коректного цитування джерел (автор, назва, рік, сторінка);")
    add_bullet(doc, "уникнення плагіату (привласнення чужих ідей);")
    add_bullet(doc, "самостійного формулювання висновків на основі опрацьованого матеріалу;")
    add_bullet(doc, "поваги до авторських прав.")

    doc.add_page_break()

    # ---- Практичне завдання ----
    add_heading(doc, "Практичне завдання (20-30 хв)", level=1)
    add_paragraph(doc,
        "Результат роботи: підготовлене повідомлення «Аналіз науково-педагогічної "
        "літератури з обраної теми та формулювання робочої гіпотези дослідження».")

    # Діаграма таймінгу
    add_paragraph(doc, "Розподіл часу на виконання:", bold=True,
                  align=WD_ALIGN_PARAGRAPH.CENTER)
    timing_path = make_timing_chart()
    add_image(doc, timing_path, width_cm=15, caption="Рис. 3. Часова діаграма виконання самостійної роботи")

    # PlantUML: структура повідомлення
    add_paragraph(doc, "Схема 3. Структура підсумкового повідомлення", bold=True,
                  align=WD_ALIGN_PARAGRAPH.CENTER)
    puml_path_2 = render_plantuml(PUML_REPORT_STRUCTURE, "report_structure.png")
    add_image(doc, puml_path_2, width_cm=14, caption="Рис. 4. Структура повідомлення (PlantUML)")

    # PlantUML: таймлайн
    add_paragraph(doc, "Схема 4. Часова шкала виконання (PlantUML)", bold=True,
                  align=WD_ALIGN_PARAGRAPH.CENTER)
    puml_path_3 = render_plantuml(PUML_TIMELINE, "timeline.png")
    add_image(doc, puml_path_3, width_cm=13, caption="Рис. 5. Покрокова часова шкала")

    doc.add_page_break()

    # Завдання 1
    add_heading(doc, "Завдання 1. Вибір теми та обґрунтування актуальності (3 хв, 3 бали)", level=2)
    add_bullet(doc, "Оберіть тему дослідження з методики викладання інформатики в початковій школі.")
    add_bullet(doc, "Запишіть тему та обґрунтуйте її актуальність (2-3 речення).")
    add_table(doc, ["Поле", "Ваша відповідь"], [["Тема дослідження", ""], ["Актуальність", ""]],
              col_widths=[5.0, 10.5])

    # Завдання 2
    add_heading(doc, "Завдання 2. Пошук та опрацювання джерел (5 хв, 10 балів)", level=2)
    add_bullet(doc, "Знайдіть 5-7 науково-педагогічних джерел з обраної теми.")
    add_bullet(doc, "Складіть бібліографічний список згідно з вимогами.")
    add_bullet(doc, "Для кожного джерела запишіть 2-3 ключові тези.")
    add_table(doc,
        ["№", "Автор, назва, рік", "Ключові тези"],
        [[str(i), "", ""] for i in range(1, 8)],
        col_widths=[1.0, 6.0, 8.5])

    # Завдання 3
    add_heading(doc, "Завдання 3. Систематизація джерел (3 хв, 7 балів)", level=2)
    add_bullet(doc, "Згрупуйте джерела за тематичними напрямами.")
    add_bullet(doc, "Визначте, що вже досліджено, а що потребує подальшого вивчення.")
    add_table(doc,
        ["Напрям / підхід", "Джерела", "Що досліджено", "Що потребує уваги"],
        [["", "", "", ""] for _ in range(4)],
        col_widths=[3.5, 3.0, 4.5, 4.5])

    # Завдання 4
    add_heading(doc, "Завдання 4. Формулювання робочої гіпотези (8 хв, 10 балів)", level=2)
    add_bullet(doc, "Сформулюйте гіпотезу за схемою «якщо..., то...».")
    add_bullet(doc, "Перевірте відповідність вимогам (конкретність, перевірюваність, обґрунтованість).")
    add_bullet(doc, "Запишіть метод перевірки (метод, вибірка).")
    add_table(doc,
        ["Елемент гіпотези", "Ваша відповідь"],
        [
            ["Гіпотеза (формулювання)", ""],
            ["Умова (що впливає)", ""],
            ["Очікуваний результат (що зміниться)", ""],
            ["Як перевіряти (метод, вибірка)", ""],
        ],
        col_widths=[6.0, 9.5])

    # Завдання 5
    add_heading(doc, "Завдання 5. Висновки (5 хв, 5 балів)", level=2)
    add_paragraph(doc, "Напишіть висновки (5-7 речень):")
    add_bullet(doc, "Що нового ви дізналися під час аналізу літератури?")
    add_bullet(doc, "Чому аналіз джерел є важливим етапом дослідження?")
    add_bullet(doc, "Які труднощі виникли при формулюванні гіпотези?")
    add_bullet(doc, "Як ви дотримувалися академічної доброчесності?")
    for _ in range(6):
        add_paragraph(doc, "_" * 95)

    doc.add_page_break()

    # Критерії оцінювання
    add_heading(doc, "Критерії оцінювання", level=1)
    add_table(doc,
        ["Критерій", "Бали"],
        [
            ["Вибір теми та обґрунтування актуальності (завдання 1)", "3"],
            ["Пошук та опрацювання джерел (завдання 2)", "10"],
            ["Аналіз та систематизація джерел (завдання 3)", "7"],
            ["Формулювання робочої гіпотези (завдання 4)", "10"],
            ["Висновки (завдання 5)", "5"],
            ["Дотримання академічної доброчесності", "3"],
            ["Оформлення роботи (структурованість, грамотність)", "2"],
            ["Максимальна кількість балів", "40"],
        ],
        col_widths=[12.5, 3.0])

    # Контрольні запитання
    add_heading(doc, "Контрольні запитання", level=1)
    questions = [
        "Що таке аналіз науково-педагогічної літератури? Які його основні методи?",
        "Які види науково-педагогічних джерел ви знаєте?",
        "Для чого досліднику потрібно аналізувати літературу перед початком дослідження?",
        "Що таке робоча гіпотеза? Чим вона відрізняється від наукової гіпотези?",
        "Які вимоги висуваються до формулювання гіпотези?",
        "Наведіть приклад гіпотези педагогічного дослідження.",
        "Що таке академічна доброчесність? Як вона стосується роботи з літературою?",
        "Як уникнути плагіату при написанні наукової роботи?",
        "Які методи можна використовувати для перевірки гіпотези?",
        "Чому гіпотеза може бути скоригована в процесі дослідження?",
    ]
    for q in questions:
        add_numbered(doc, q)

    # Додаток
    add_heading(doc, "Додаток. Зразок оформлення повідомлення", level=1)
    add_paragraph(doc, "Тема дослідження: «Використання ігрових технологій на уроках інформатики в 2 класі».", bold=True)
    add_paragraph(doc,
        "Актуальність: у молодшому шкільному віці гра є провідним видом діяльності, "
        "тому використання ігрових технологій на уроках інформатики сприяє підвищенню "
        "мотивації та кращому засвоєнню матеріалу.")
    add_table(doc,
        ["№", "Джерело", "Ключові тези"],
        [
            ["1", "Кравець Н. П. Основи наукових досліджень, 2020", "Визначення гіпотези, вимоги до її формулювання"],
            ["2", "Методичні рекомендації щодо написання курсової роботи, 2024", "Структура дослідження, правила оформлення"],
            ["3", "…", "…"],
        ],
        col_widths=[1.0, 6.0, 8.5])
    add_paragraph(doc,
        "Робоча гіпотеза: використання ігрових технологій на уроках інформатики в 2 класі "
        "підвищить пізнавальну активність учнів, якщо ігри будуть добиратися відповідно "
        "до теми уроку та вікових особливостей школярів.", italic=True)
    add_paragraph(doc,
        "Метод перевірки: педагогічний експеримент (порівняння результатів навчання в "
        "контрольній та експериментальній групах), анкетування учнів.")

    # Збереження
    out_path = os.path.join(OUTPUT_DIR, "Самостійна_робота_4_Аналіз_літератури_і_гіпотеза.docx")
    doc.save(out_path)
    print(f"[OK] Документ збережено: {out_path}")
    return out_path


if __name__ == "__main__":
    build_document()