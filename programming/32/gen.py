#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор різнорівневих завдань для тематичного заліку.
Тема: лінійні, розгалужені та циклічні алгоритми.
Формат: Times New Roman, 14 pt, інтервал 1.25.
"""

import random
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ==================== КОНФІГУРАЦІЯ ====================
FONT_NAME = "Times New Roman"
FONT_SIZE = Pt(14)
LINE_SPACING = 1.25
OUTPUT_FILE = "Тематичний_залік_варіант.docx"

N_TEST_QUESTIONS = 10      # рівень 1 (по 0.6 бала)
N_LEVEL2_TASKS = 2         # рівень 2 (по 2 бали)
N_LEVEL3_TASKS = 1         # рівень 3 (2 бали)
TOTAL_POINTS = 12


# ==================== СТИЛІ ====================

def _set_font_on_rpr(rpr_element, font_name):
    rfonts = rpr_element.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr_element.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), font_name)


def setup_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = FONT_NAME
    normal.font.size = FONT_SIZE
    _set_font_on_rpr(normal.element.get_or_add_rPr(), FONT_NAME)
    pf = normal.paragraph_format
    pf.line_spacing = LINE_SPACING
    pf.space_after = Pt(6)

    for name, size in [("Heading 1", 16), ("Heading 2", 15), ("Heading 3", 14)]:
        style = doc.styles[name]
        style.font.name = FONT_NAME
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0x1F, 0x3A, 0x8A)
        _set_font_on_rpr(style.element.get_or_add_rPr(), FONT_NAME)
        pf = style.paragraph_format
        pf.line_spacing = LINE_SPACING
        pf.space_before = Pt(12)
        pf.space_after = Pt(6)


def add_para(doc, text="", bold=False, italic=False, size=None,
             align=None, space_after=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = Pt(size)
    if align is not None:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def add_table(doc, headers, rows, font_size=12):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.name = FONT_NAME
        run.font.size = Pt(font_size)
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "DBEAFE")
        tcPr.append(shd)
    for row_data in rows:
        row = table.add_row()
        for i, val in enumerate(row_data):
            cell = row.cells[i]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.name = FONT_NAME
            run.font.size = Pt(font_size)
    return table


def add_writing_lines(doc, n=6):
    for _ in range(n):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = LINE_SPACING
        p.paragraph_format.space_after = Pt(4)
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "4")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "AAAAAA")
        pBdr.append(bottom)
        pPr.append(pBdr)


# ==================== ПУЛ ТЕСТОВИХ ПИТАНЬ ====================
TEST_POOL = [
    ("Яка структура передбачає повторення серії команд?",
     ["структура розгалуження", "структура повторення",
      "лінійна структура", "послідовна структура"], "Б"),
    ("Як називається серія команд, що повторюється в циклі?",
     ["голова циклу", "тіло циклу", "умова циклу", "параметр циклу"], "Б"),
    ("Який цикл перевіряє умову ПЕРЕД виконанням тіла циклу?",
     ["цикл з післяумовою", "цикл з передумовою",
      "цикл з параметром", "вкладений цикл"], "Б"),
    ("Як ще називають цикл з передумовою?",
     ["цикл-«до»", "цикл-«доки»", "цикл-«для»", "цикл-«поки»"], "Б"),
    ("Коли завершується цикл з передумовою?",
     ["коли умова виконується", "коли умова перестає виконуватися",
      "після першого виконання", "після заданої кількості повторень"], "Б"),
    ("Який цикл перевіряє умову ПІСЛЯ виконання тіла циклу?",
     ["цикл з передумовою", "цикл з параметром",
      "цикл з післяумовою", "послідовний цикл"], "В"),
    ("Який цикл виконується відому кількість разів?",
     ["цикл з передумовою", "цикл з післяумовою",
      "цикл з параметром", "всі відповіді правильні"], "В"),
    ("Як називається змінна, що змінюється в циклі з параметром?",
     ["умова циклу", "параметр циклу", "крок циклу", "тіло циклу"], "Б"),
    ("Який оператор використовується для циклу з параметром у VBA?",
     ["do while", "do until", "for...next", "if...then"], "В"),
    ("Що таке «крок» у циклі з параметром?",
     ["початкове значення", "кінцеве значення",
      "величина зміни параметра", "умова виходу"], "В"),
    ("Які цикли називаються послідовними?",
     ["ті, що містять один одного", "ті, що слідують один за одним",
      "ті, що мають однакову умову", "ті, що виконуються паралельно"], "Б"),
    ("Що таке вкладений цикл?",
     ["цикл у тілі іншого циклу", "цикл з декількома умовами",
      "цикл зі змінним кроком", "цикл без умови виходу"], "А"),
    ("Скільки разів мінімум виконається тіло циклу з післяумовою?",
     ["0", "1", "2", "залежить від умови"], "Б"),
    ("Скільки разів мінімум виконається тіло циклу з передумовою?",
     ["0", "1", "2", "залежить від умови"], "А"),
    ("Який цикл гарантовано виконається хоча б один раз?",
     ["цикл з передумовою", "цикл з післяумовою",
      "цикл з параметром", "жоден"], "Б"),
    ("Що відбувається, якщо в циклі з параметром не вказано крок?",
     ["виникає помилка", "крок вважається рівним 0",
      "крок вважається рівним 1", "цикл виконується нескінченно"], "В"),
    ("Яка структура є окремим випадком циклу з передумовою?",
     ["цикл з післяумовою", "цикл з параметром",
      "вкладений цикл", "послідовний цикл"], "Б"),
    ("Що таке «виконавець алгоритму»?",
     ["пристрій для зберігання даних",
      "об'єкт, здатний виконувати певний набір команд",
      "мова програмування", "алгоритмічна конструкція"], "Б"),
    ("Чому система команд виконавця повинна бути обмеженою?",
     ["щоб ускладнити програмування",
      "для гарантії точного виконання команд",
      "для зменшення вартості пристрою",
      "щоб збільшити швидкість роботи"], "Б"),
    ("Що таке «середовище існування» виконавця?",
     ["набір доступних команд",
      "простір, у якому виконавець працює",
      "апаратне забезпечення", "операційна система"], "Б"),
]


# ==================== ГЕНЕРАТОРИ ПРАКТИЧНИХ ЗАВДАНЬ ====================

def gen_linear_task():
    """Лінійний алгоритм: обчислити вираз."""
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    c = random.randint(2, 9)
    variants = [
        (f"Обчисліть значення виразу: y = {a}x + {b}, якщо x = {c}.",
         f"y = {a}·{c} + {b} = {a*c + b}"),
        (f"Обчисліть площу прямокутника зі сторонами a = {a} см, b = {b} см.",
         f"S = {a}·{b} = {a*b} см²"),
        (f"Обчисліть середнє арифметичне чисел {a}, {b}, {c}.",
         f"({a}+{b}+{c})/3 = {(a+b+c)/3:.2f}"),
    ]
    return random.choice(variants)


def gen_branching_task():
    """Розгалуження: визначити тип числа / трикутника / високосний рік."""
    variants = []

    # --- 1. Додатне / від'ємне / нуль ---
    x = random.randint(-20, 20)
    if x > 0:
        kind = "додатне"
    elif x < 0:
        kind = "від'ємне"
    else:
        kind = "нуль"

    variants.append((
        f"Визначте, чи є число {x} додатним, від'ємним або нулем. "
        f"Напишіть фрагмент коду (Python або VBA).",
        f"{x} — {kind}"
    ))

    # --- 2. Трикутник ---
    a, b, c = sorted(random.sample(range(2, 15), 3))
    if random.random() < 0.5:
        a = b

    if a + b > c and a + c > b and b + c > a:
        if a == b == c:
            triangle_type = "рівносторонній"
        elif a == b or a == c or b == c:
            triangle_type = "рівнобедрений"
        else:
            triangle_type = "різносторонній"
        triangle_answer = f"Трикутник існує, тип: {triangle_type}"
    else:
        triangle_answer = "Трикутник не існує"

    variants.append((
        f"Дано сторони трикутника: a = {a}, b = {b}, c = {c}. "
        f"Визначте, чи існує трикутник, і якщо так — його тип "
        f"(рівносторонній / рівнобедрений / різносторонній).",
        triangle_answer
    ))

    # --- 3. Високосний рік ---
    year = random.choice([1900, 2000, 2023, 2024, 2100, 1600])
    is_leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
    variants.append((
        f"Визначте, чи є рік {year} високосним. Напишіть умову перевірки.",
        f"{year} — {'високосний' if is_leap else 'не високосний'}"
    ))

    return random.choice(variants)


def gen_loop_task():
    """Цикл: сума, факторіал, парні числа."""
    variants = []

    n = random.randint(5, 15)
    variants.append((
        f"Обчисліть суму всіх чисел від 1 до {n} включно. "
        f"Напишіть код (Python або VBA).",
        f"Сума = {n * (n + 1) // 2}"
    ))

    n = random.randint(4, 8)
    fact = 1
    for i in range(1, n + 1):
        fact *= i
    variants.append((
        f"Обчисліть факторіал числа {n} ({n}! = 1·2·…·{n}). Напишіть код.",
        f"{n}! = {fact}"
    ))

    a = random.randint(1, 10)
    b = random.randint(a + 5, a + 20)
    s = sum(i for i in range(a, b + 1) if i % 2 == 0)
    variants.append((
        f"Знайдіть суму всіх парних чисел у діапазоні від {a} до {b} включно. "
        f"Напишіть код.",
        f"Сума = {s}"
    ))

    return random.choice(variants)


def gen_advanced_task():
    """Складніша задача (рівень 3)."""
    variants = []

    n = random.randint(10, 50)
    primes = [str(x) for x in range(2, n + 1)
              if all(x % d != 0 for d in range(2, int(x ** 0.5) + 1))]
    variants.append((
        f"Знайдіть усі прості числа в діапазоні від 2 до {n}. "
        f"Напишіть програму (Python або VBA) та поясніть алгоритм.",
        "Прості числа: " + ", ".join(primes)
    ))

    n = random.randint(3, 6)
    variants.append((
        f"Виведіть «піраміду» зі зірочок заввишки {n} рівнів. "
        f"Напишіть програму з вкладеними циклами.",
        "Піраміда: " + " | ".join("*" * (2 * i - 1) for i in range(1, n + 1))
    ))

    n = random.randint(2, 5)
    variants.append((
        f"Виведіть таблицю множення розміром {n} × {n}. "
        f"Використайте вкладені цикли.",
        f"Розмір таблиці: {n}×{n} = {n * n} клітинок"
    ))

    return random.choice(variants)


# ==================== ПОБУДОВА ДОКУМЕНТА ====================

def build_document():
    doc = Document()
    setup_styles(doc)
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)

    # === Титульна ===
    add_para(doc, "", space_after=40)
    add_para(doc, "ТЕМАТИЧНИЙ ЗАЛІК", bold=True, size=22,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_para(doc, "Підсумкове тестування", bold=True, size=16,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_para(doc, "Тема: лінійні, розгалужені та циклічні алгоритми",
             italic=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER,
             space_after=30)

    add_para(doc, "Прізвище, ім'я: _________________________________________", size=12)
    add_para(doc, "Клас: ____________     Дата: ________________", size=12)
    add_para(doc, "Варіант: ____________", size=12)
    add_para(doc, "", space_after=20)

    add_para(doc, f"Максимальна кількість балів: {TOTAL_POINTS}", bold=True, size=12)
    add_para(doc, "Час виконання: 30 хв.", italic=True, size=12)

    doc.add_page_break()

    # === Рівень 1 ===
    add_para(doc, "Рівень 1. Тестові завдання (по 0.6 бала, разом 6 балів)",
             bold=True, size=15, space_after=8)
    add_para(doc, "Оберіть одну правильну відповідь.", italic=True, size=12)

    questions = random.sample(TEST_POOL, N_TEST_QUESTIONS)
    letters = ["А", "Б", "В", "Г"]
    answers_key = []

    for i, (text, options, correct) in enumerate(questions, 1):
        add_para(doc, f"{i}. {text}", bold=True, size=13)
        # правильний текст зберігаємо ДО перемішування
        correct_text = options[letters.index(correct)]
        pairs = list(zip(letters, options))
        random.shuffle(pairs)
        for letter, option in pairs:
            add_para(doc, f"   {letter}) {option}", size=13)
            if option == correct_text:
                answers_key.append(letter)
        add_para(doc, "", space_after=2)

    # === Рівень 2 ===
    doc.add_page_break()
    add_para(doc, "Рівень 2. Практичні завдання (по 2 бали, разом 4 бали)",
             bold=True, size=15, space_after=8)
    add_para(doc, "Напишіть код (Python, Java або VBA) та вкажіть результат.",
             italic=True, size=12)

    level2_tasks = [gen_linear_task(), gen_branching_task(), gen_loop_task()]
    random.shuffle(level2_tasks)
    selected_l2 = level2_tasks[:N_LEVEL2_TASKS]
    l2_answers = [t[1] for t in selected_l2]

    for i, (task_text, _) in enumerate(selected_l2, 1):
        add_para(doc, f"Завдання {i}. {task_text}", bold=True, size=13)
        add_para(doc, "Код:", bold=True, size=12)
        add_writing_lines(doc, n=6)
        add_para(doc, "Результат: _________________________________________", size=12)
        add_para(doc, "", space_after=8)

    # === Рівень 3 ===
    doc.add_page_break()
    add_para(doc, "Рівень 3. Завдання підвищеної складності (2 бали)",
             bold=True, size=15, space_after=8)
    add_para(doc, "Напишіть програму та коротко поясніть алгоритм.",
             italic=True, size=12)

    level3_task = gen_advanced_task()
    add_para(doc, level3_task[0], bold=True, size=13)
    add_para(doc, "Код:", bold=True, size=12)
    add_writing_lines(doc, n=10)
    add_para(doc, "Пояснення алгоритму:", bold=True, size=12)
    add_writing_lines(doc, n=4)

    # === Критерії оцінювання ===
    doc.add_page_break()
    add_para(doc, "Критерії оцінювання", bold=True, size=15, space_after=8)
    add_table(
        doc,
        ["Діапазон балів", "Оцінка (12)", "Рівень"],
        [
            ["12 (100%)", "12", "Відмінно"],
            ["10–11 (90–99%)", "10–11", "Добре+"],
            ["8–9 (75–89%)", "8–9", "Добре"],
            ["6–7 (60–74%)", "6–7", "Задовільно"],
            ["4–5 (50–59%)", "4–5", "Початковий"],
            ["менше 4 (<50%)", "1–3", "Незадовільно"],
        ],
        font_size=12,
    )
    add_para(doc, "Кожне тестове питання — 0.6 бала. "
                  "Кожне практичне завдання рівня 2 — 2 бали. "
                  "Завдання рівня 3 — 2 бали.", italic=True, size=12)

    # === Ключ відповідей ===
    doc.add_page_break()
    add_para(doc, "Ключ відповідей (для вчителя)", bold=True, size=15, space_after=8)

    add_para(doc, "Рівень 1:", bold=True, size=13)
    key_rows = [[str(i + 1), answers_key[i]] for i in range(N_TEST_QUESTIONS)]
    add_table(doc, ["№", "Відповідь"], key_rows, font_size=12)

    add_para(doc, "", space_after=8)
    add_para(doc, "Рівень 2:", bold=True, size=13)
    for i, ans in enumerate(l2_answers, 1):
        add_para(doc, f"Завдання {i}. {ans}", size=12)

    add_para(doc, "", space_after=8)
    add_para(doc, "Рівень 3:", bold=True, size=13)
    add_para(doc, level3_task[1], size=12)

    return doc


# ==================== ГОЛОВНА ====================

def main():
    doc = build_document()
    doc.save(OUTPUT_FILE)
    print(f"✓ Документ збережено: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()