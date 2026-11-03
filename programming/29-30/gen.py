#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор DOCX для Самостійної роботи №6
Тема: Алгоритми з циклом з лічильником (for)
Формат: Times New Roman, 14 pt, інтервал 1.25
"""

import os
import sys
import zlib
import logging

try:
    import requests
except ImportError:
    print("Потрібен пакет requests: pip install requests"); sys.exit(1)

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("Потрібен пакет python-docx: pip install python-docx"); sys.exit(1)


# ==================== КОНФІГУРАЦІЯ ====================
FONT_NAME        = "Times New Roman"
FONT_SIZE        = Pt(14)
CODE_FONT_NAME   = "Consolas"
CODE_FONT_SIZE   = Pt(10)
TABLE_FONT_SIZE  = Pt(11)
LINE_SPACING     = 1.25
OUTPUT_FILE      = "Самостійна_робота_6_цикл_лічильник.docx"
DIAGRAMS_DIR     = "diagrams"
SKIP_DIAGRAMS    = False

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


# ==================== PLANTUML ====================

def encode_plantuml(text):
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    data = compressor.compress(text.encode("utf-8")) + compressor.flush()
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    result = ""
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        if len(chunk) == 3:
            b1, b2, b3 = chunk
            result += alphabet[b1 >> 2]
            result += alphabet[((b1 & 0x3) << 4) | (b2 >> 4)]
            result += alphabet[((b2 & 0xF) << 2) | (b3 >> 6)]
            result += alphabet[b3 & 0x3F]
        elif len(chunk) == 2:
            b1, b2 = chunk
            result += alphabet[b1 >> 2]
            result += alphabet[((b1 & 0x3) << 4) | (b2 >> 4)]
            result += alphabet[(b2 & 0xF) << 2]
        elif len(chunk) == 1:
            b1 = chunk[0]
            result += alphabet[b1 >> 2]
            result += alphabet[(b1 & 0x3) << 4]
    return result


def download_plantuml_png(source, output_path):
    encoded = encode_plantuml(source)
    url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    try:
        log.info(f"  ↳ {output_path}")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        if not resp.content.startswith(b"\x89PNG"):
            log.error("  ↳ отримано не PNG"); return False
        with open(output_path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        log.error(f"  ↳ помилка: {e}"); return False


# ==================== СТИЛІ ====================

def _set_font_on_rpr(rpr_element, font_name):
    rfonts = rpr_element.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr_element.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), font_name)


def setup_document_styles(doc):
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


# ==================== ХЕЛПЕРИ ====================

def add_para(doc, text="", bold=False, italic=False, size=None,
             align=None, space_after=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold; run.italic = italic
    if size: run.font.size = Pt(size)
    if align is not None: p.alignment = align
    if space_after is not None: p.paragraph_format.space_after = Pt(space_after)
    return p


def add_code_block(doc, code):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.0
    pf.space_before = Pt(4); pf.space_after = Pt(8)
    pf.left_indent = Cm(0.5)

    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "4")
        b.set(qn("w:space"), "4"); b.set(qn("w:color"), "CCCCCC")
        pBdr.append(b)
    pPr.append(pBdr)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F2F2F2")
    pPr.append(shd)

    lines = code.split("\n")
    for i, line in enumerate(lines):
        run = p.add_run(line if line else " ")
        if i < len(lines) - 1:
            run.add_break()
        run.font.name = CODE_FONT_NAME
        run.font.size = CODE_FONT_SIZE
        _set_font_on_rpr(run._r.get_or_add_rPr(), CODE_FONT_NAME)
    return p


def add_table(doc, headers, rows, font_size=11, fill_empty=False):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

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
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
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
            if fill_empty and str(val) == "":
                tcPr = cell._tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd")
                shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
                shd.set(qn("w:fill"), "FFF9E6")
                tcPr.append(shd)
    return table


def add_writing_lines(doc, n=5):
    for _ in range(n):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(6)
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "4")
        bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), "AAAAAA")
        pBdr.append(bottom)
        pPr.append(pBdr)


def add_writing_box(doc, n_lines=6):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    cell = table.cell(0, 0)
    cell.text = ""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "dashed"); b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), "AAAAAA")
        tcBorders.append(b)
    tcPr.append(tcBorders)
    for i in range(n_lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(2)
        p.add_run(" ")
    add_para(doc, "", space_after=2)


def add_diagram(doc, puml_source, filename, caption=""):
    if SKIP_DIAGRAMS:
        add_para(doc, f"[Діаграма {filename} — режим без завантаження]",
                 italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        return

    path = os.path.join(DIAGRAMS_DIR, filename)
    if download_plantuml_png(puml_source, path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        try:
            p.add_run().add_picture(path, width=Inches(4.5))
        except Exception as e:
            log.error(f"Не вдалося вставити {path}: {e}")
    else:
        add_para(doc, "Діаграма недоступна. Джерело:",
                 italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        add_code_block(doc, puml_source)

    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(caption)
        run.italic = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


def add_answer_text(doc, text, label="Відповідь:"):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F0FDF4")
    pPr.append(shd)
    run = p.add_run(label + " ")
    run.bold = True; run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x16, 0x65, 0x34)
    run2 = p.add_run(text)
    run2.font.size = Pt(12)
    run2.font.color.rgb = RGBColor(0x16, 0x65, 0x34)
    return p


# ==================== PLANTUML ДЖЕРЕЛА ====================

PUML_FOR_GENERAL = """@startuml
skinparam style strictuml
skinparam activity {
  BackgroundColor #DBEAFE
  BorderColor #2563EB
  DiamondBackgroundColor #EDE9FE
  DiamondBorderColor #7C3AED
}
start
:i := start;
while (i <= stop?) is (Так)
  :Тіло циклу;
  :i := i + step;
endwhile (Ні)
stop
@enduml"""

PUML_SUM_EVEN = """@startuml
skinparam style strictuml
skinparam activity {
  BackgroundColor #F0FDF4
  BorderColor #16A34A
  DiamondBackgroundColor #DCFCE7
  DiamondBorderColor #16A34A
}
start
:Ввести A, B;
:sum := 0;
:i := A;
while (i <= B?) is (Так)
  if (i Mod 2 = 0?) then (Так)
    :sum := sum + i;
  endif
  :i := i + 1;
endwhile (Ні)
:Вивести sum;
stop
@enduml"""

PUML_TABULATE = """@startuml
skinparam style strictuml
skinparam activity {
  BackgroundColor #FEF3C7
  BorderColor #D97706
  DiamondBackgroundColor #FDE68A
  DiamondBorderColor #D97706
}
start
:Ввести a, b, h;
:x := a;
while (x <= b?) is (Так)
  :y := 2*x*x - 5;
  :Вивести x, y;
  :x := x + h;
endwhile (Ні)
stop
@enduml"""

PUML_PYRAMID = """@startuml
skinparam style strictuml
skinparam activity {
  BackgroundColor #EDE9FE
  BorderColor #7C3AED
  DiamondBackgroundColor #DDD6FE
  DiamondBorderColor #7C3AED
}
start
:Ввести N;
:i := 1;
while (i <= N?) is (Так)
  :Вивести (N - i) пробілів;
  :k := 1;
  while (k <= 2*i - 1?) is (Так)
    :Вивести "*";
    :k := k + 1;
  endwhile (Ні)
  :Перейти на новий рядок;
  :i := i + 1;
endwhile (Ні)
stop
@enduml"""


# ==================== КОНТЕНТ ====================

def build_title_page(doc):
    add_para(doc, "", space_after=60)
    add_para(doc, "САМОСТІЙНА РОБОТА №6", bold=True, size=20,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "Алгоритми з циклом з лічильником",
             bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, "(цикл for)", italic=True, size=14,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)

    add_para(doc, "Мета:", bold=True)
    add_para(doc, "Поглибити знання про цикли з лічильником (for). Вивчити "
                  "особливості їх застосування для перебору елементів, роботи з "
                  "масивами, табулювання функцій. Розвивати вміння формалізувати "
                  "процеси, що мають явно виражену кількість повторень. Розвивати "
                  "математичну інтуїцію. Виховувати акуратність у роботі з "
                  "границями циклів (початкове/кінцеве значення лічильника), "
                  "уважність до деталей.")

    add_para(doc, "Обладнання:", bold=True)
    add_para(doc, "Інструкційні картки.")

    add_para(doc, "Література:", bold=True)
    add_para(doc, "1. Руденко В. Д., Жугастров О. О. Основи алгоритмізації і "
                  "програмування мовою Python. Харків: Ранок, 2019. 192 с.")
    add_para(doc, "2. Руденко В. Д., Жугастров О. О. Перші кроки програмування "
                  "мовою Java. Харків: Ранок, 2018. 112 с.")
    add_para(doc, "3. Сліпченко В. О. Задачі з програмування мовою Python. "
                  "Київ: Шкільний світ, 2019. 120 с.")

    add_para(doc, "", space_after=40)
    add_para(doc, "Виконав(ла): ____________________________", size=12)
    add_para(doc, "Клас: __________     Дата: ____________", size=12)


def build_discussion(doc):
    doc.add_heading("Питання для обговорення", level=1)
    qa = [
        ("У яких випадках доцільно використовувати цикл for, а не while?",
         "Коли кількість повторень відома заздалегідь або може бути обчислена "
         "перед початком циклу (наприклад, «пройтися по всіх елементах масиву», "
         "«обчислити значення функції для N точок», «вивести числа від 1 до 10»). "
         "While зручніше, коли умова виходу залежить від самого тіла циклу "
         "(наприклад, «шукати, доки не знайдемо», «вводити, доки не введуть 0»)."),
        ("Як впливає зміна кроку лічильника на кількість ітерацій циклу?",
         "Чим більший крок, тим менше ітерацій (при фіксованому діапазоні). "
         "Наприклад, від 1 до 10 з кроком 1 — 10 ітерацій, з кроком 2 — 5, "
         "з кроком 3 — 4 (1, 4, 7, 10). Крок 0 → нескінченний цикл! "
         "Від'ємний крок потребує початку > кінця (зворотний порядок)."),
        ("Чи може лічильник циклу приймати дробові значення в різних мовах?",
         "У Python — так (range не працює з float, але while або генератори — так; "
         "дробовий крок через for i in [0, 0.5, 1.0, ...] або за допомогою numpy). "
         "У Java — так, якщо лічильник типу double. "
         "У VBA — так, якщо лічильник типу Double: For x = 0 To 1 Step 0.1. "
         "Однак дробові лічильники накопичують похибку (0.1 + 0.2 ≠ 0.3 у "
         "float), тому для точних обчислень краще використовувати цілий "
         "лічильник і обчислювати значення через формулу."),
        ("Що станеться, якщо кінцеве значення менше за початкове, а крок позитивний?",
         "Цикл не виконається жодного разу — умова start <= stop з першого ж "
         "разу хибна. У Python: range(10, 1, 1) — порожній діапазон. "
         "У Java: for (i = 10; i <= 1; i++) — 0 ітерацій. "
         "У VBA: For i = 10 To 1 Step 1 — 0 ітерацій. "
         "Це важливо пам'ятати: цикл не «зламається», а просто пропуститься."),
    ]
    for i, (q, a) in enumerate(qa, 1):
        add_para(doc, f"{i}. {q}", bold=True)
        add_para(doc, a)
        add_para(doc, "", space_after=4)


def build_theory(doc):
    doc.add_heading("Теоретичні відомості", level=1)

    doc.add_heading("1. Що таке цикл з лічильником", level=2)
    add_para(doc, "Цикл із лічильником (цикл типу for) використовується тоді, "
                  "коли кількість повторень відома заздалегідь або може бути "
                  "обчислена перед початком виконання циклу.")
    add_para(doc, "Цикл складається з трьох частин:", bold=True)
    add_para(doc, "1) Ініціалізація — встановлення початкового значення "
                  "лічильника. Виконується один раз перед першою ітерацією.")
    add_para(doc, "2) Умова — вираз, який перевіряється перед кожною ітерацією. "
                  "Цикл триває, поки умова істинна.")
    add_para(doc, "3) Крок (ітерація) — зміна значення лічильника після "
                  "кожного виконання тіла циклу. Виконується перед наступною "
                  "перевіркою умови.")

    doc.add_heading("2. Синтаксис у різних мовах", level=2)
    add_table(
        doc,
        ["Мова", "Синтаксис", "Особливості"],
        [
            ["Python", "for i in range(start, stop, step):\n    тіло",
             "stop НЕ включається; крок за замовчуванням 1"],
            ["Java", "for (i = start; i <= stop; i += step) {\n    тіло\n}",
             "stop включається (бо умова <=); крок задається вручну"],
            ["VBA (Excel)", "For i = start To stop Step step\n    тіло\nNext i",
             "stop включається; Next закриває цикл"],
        ],
        font_size=10,
    )

    add_para(doc, "Важливо: у Python range(start, stop) не включає stop, "
                  "у Java та VBA діапазон включає кінцеве значення. Це найчастіше "
                  "джерело помилок при переході між мовами!", bold=True, size=12)

    doc.add_heading("3. Блок-схема загальної структури", level=2)
    add_diagram(doc, PUML_FOR_GENERAL, "for_general.png",
                "Малюнок 1. Загальна структура циклу з лічильником")

    doc.add_heading("4. Скільки ітерацій виконується?", level=2)
    add_para(doc, "Формула для кількості ітерацій при кроці > 0:")
    add_para(doc, "N = (stop − start) / step + 1 (округлено вниз, якщо значення "
                  "не досягає stop точно).", italic=True)
    add_table(
        doc,
        ["start", "stop", "step", "Ітерацій", "Значення лічильника"],
        [
            ["1", "10", "1", "10", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"],
            ["1", "10", "2", "5", "1, 3, 5, 7, 9"],
            ["1", "10", "3", "4", "1, 4, 7, 10"],
            ["0", "10", "5", "3", "0, 5, 10"],
            ["10", "1", "−1", "10", "10, 9, 8, 7, 6, 5, 4, 3, 2, 1"],
            ["10", "1", "1", "0", "(цикл не виконується)"],
        ],
    )

    doc.add_heading("5. Застосування", level=2)
    add_para(doc, "Табулювання функцій — обчислення значень y = f(x) на проміжку "
                  "із заданим кроком. Приклад: y = 2x² − 5 на [−5; 5] з кроком 0.5.")
    add_para(doc, "Робота з масивами — почерговий доступ до кожного елемента "
                  "за його індексом.")
    add_para(doc, "Обчислення сум і добутків — наприклад, факторіал "
                  "n! = 1·2·…·n.")
    add_para(doc, "Перебір чисел — пошук простих, парних, кратних, чисел "
                  "Армстронга тощо.")

    doc.add_heading("6. Основні приклади", level=2)
    add_para(doc, "Приклад 1. Сума чисел від 1 до N (Python):", bold=True)
    add_code_block(doc,
                   "N = int(input('N = '))\n"
                   "s = 0\n"
                   "for i in range(1, N + 1):\n"
                   "    s += i\n"
                   "print('Сума =', s)")
    add_para(doc, "Приклад 2. Те саме на VBA:", bold=True)
    add_code_block(doc,
                   "Sub SumToN()\n"
                   "    Dim N As Long, s As Long, i As Long\n"
                   "    N = CLng(InputBox(\"N =\"))\n"
                   "    s = 0\n"
                   "    For i = 1 To N\n"
                   "        s = s + i\n"
                   "    Next i\n"
                   "    MsgBox \"Сума = \" & s\n"
                   "End Sub")
    add_para(doc, "Приклад 3. Зворотний цикл (від 10 до 1):", bold=True)
    add_code_block(doc,
                   "# Python\n"
                   "for i in range(10, 0, -1):\n"
                   "    print(i)\n"
                   "\n"
                   "' VBA\n"
                   "For i = 10 To 1 Step -1\n"
                   "    Debug.Print i\n"
                   "Next i")

    doc.add_heading("7. Типові помилки", level=2)
    add_table(
        doc,
        ["Помилка", "Приклад", "Наслідок"],
        [
            ["Off-by-one у Python",
             "range(1, N) замість range(1, N+1)",
             "Останнє значення N не обробляється"],
            ["Крок 0",
             "range(1, 10, 0)",
             "Помилка ValueError / нескінченний цикл"],
            ["Забути зміну лічильника",
             "while i < 10: без i += 1",
             "Нескінченний цикл"],
            ["Дробовий крок через range",
             "range(0, 1, 0.1) — TypeError",
             "Використовуйте while або список"],
            ["Ділення на 0 у тілі",
             "s / (i - 5) при i = 5",
             "Помилка виконання"],
            ["Накопичення похибки float",
             "0.1 + 0.2 != 0.3",
             "Неправильні порівняння з дробовими"],
        ],
        font_size=10,
    )


def build_block_diagrams_section(doc):
    doc.add_heading("Блок-схеми до прикладів", level=1)

    add_para(doc, "1. Сума всіх парних чисел у діапазоні від A до B:", bold=True)
    add_diagram(doc, PUML_SUM_EVEN, "sum_even.png",
                "Малюнок 2. Підрахунок суми парних чисел")

    add_para(doc, "2. Табулювання функції y = 2x² − 5 на відрізку [a; b] з кроком h:",
             bold=True)
    add_diagram(doc, PUML_TABULATE, "tabulate.png",
                "Малюнок 3. Табулювання функції")

    add_para(doc, "3. Піраміда зі зірочок заввишки N (вкладені цикли):", bold=True)
    add_diagram(doc, PUML_PYRAMID, "pyramid.png",
                "Малюнок 4. Побудова піраміди зірочок")


def build_level1(doc):
    doc.add_heading("Рівень 1 — Базовий", level=1)
    add_para(doc, "Розпізнавання та розуміння.", italic=True)

    doc.add_heading("Завдання 1.1. Визначте кількість ітерацій", level=2)
    add_para(doc, "Для кожного фрагмента вкажіть, скільки разів виконається "
                  "тіло циклу та які значення прийме лічильник.")
    add_table(
        doc,
        ["№", "Фрагмент коду", "Ітерацій", "Значення i"],
        [
            ["1", "for i in range(1, 6):", "", ""],
            ["2", "for i in range(0, 10, 2):", "", ""],
            ["3", "for i in range(5, 0, -1):", "", ""],
            ["4", "for (i = 1; i <= 3; i++)", "", ""],
            ["5", "For i = 1 To 7 Step 3", "", ""],
            ["6", "for i in range(10, 1):", "", ""],
        ],
        fill_empty=True,
    )
    add_answer_text(
        doc,
        "1) 5 ітерацій, i = 1,2,3,4,5. 2) 5 ітерацій, i = 0,2,4,6,8. "
        "3) 5 ітерацій, i = 5,4,3,2,1. 4) 3 ітерації, i = 1,2,3. "
        "5) 3 ітерації, i = 1,4,7. 6) 0 ітерацій — start > stop при додатному кроці."
    )

    doc.add_heading("Завдання 1.2. Порівняйте for і while", level=2)
    add_table(
        doc,
        ["Ознака", "for", "while"],
        [
            ["Кількість повторень відома?", "", ""],
            ["Що перевіряється перед ітерацією?", "", ""],
            ["Де задається зміна лічильника?", "", ""],
            ["Нескінченний цикл можливий?", "", ""],
            ["Коли доцільніше використовувати?", "", ""],
        ],
        fill_empty=True,
    )
    add_answer_text(
        doc,
        "for: кількість відома; умова = досягнення кінця; зміна в заголовку "
        "циклу; нескінченний цикл можливий лише при кроці 0 або зміні меж; "
        "доцільно для перебору відомого діапазону. "
        "while: кількість може бути невідома; умова довільна; зміна — у тілі; "
        "нескінченний цикл — типова помилка; доцільно для пошуку за умовою."
    )

    doc.add_heading("Завдання 1.3. Прослідкуйте виконання", level=2)
    add_para(doc, "Що виведе фрагмент? Заповніть таблицю трасування.")
    add_code_block(doc,
                   "s = 0\n"
                   "for i in range(1, 5):\n"
                   "    s = s + i * 2\n"
                   "print(s)")
    add_table(
        doc,
        ["i", "i * 2", "s (після)"],
        [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]],
        fill_empty=True,
    )
    add_para(doc, "Виведеться: ____________", bold=True)
    add_answer_text(
        doc,
        "i=1: s=2; i=2: s=6; i=3: s=12; i=4: s=20. Виведеться 20."
    )

    doc.add_heading("Завдання 1.4. Напишіть простий цикл", level=2)
    add_para(doc, "Виведіть на екран числа від 1 до 10 включно. Оберіть мову "
                  "(Python, Java або VBA).")
    add_writing_box(doc, n_lines=6)
    add_para(doc, "Зразок (VBA):", bold=True)
    add_code_block(doc,
                   "Sub PrintOneToTen()\n"
                   "    Dim i As Long\n"
                   "    For i = 1 To 10\n"
                   "        Debug.Print i\n"
                   "    Next i\n"
                   "End Sub")


def build_level2(doc):
    doc.add_heading("Рівень 2 — Середній", level=1)
    add_para(doc, "Основні завдання заняття.", italic=True)

    # ===== Завдання 2.1 — сума парних =====
    doc.add_heading("Завдання 2.1. Сума всіх парних чисел у діапазоні [A; B]", level=2)
    add_para(doc, "Напишіть програму для обчислення суми всіх парних чисел у "
                  "діапазоні від A до B (значення A та B вводяться з клавіатури).")
    add_para(doc, "Підказки:", bold=True, size=12)
    add_para(doc, "• Перевірка парності: число % 2 == 0 (Python/Java) або "
                  "число Mod 2 = 0 (VBA).")
    add_para(doc, "• Не забудьте про випадок, коли A > B — цикл не виконається.")
    add_para(doc, "• Розгляньте можливість оптимізації: чи можна обійтися без "
                  "if, змінивши крок на 2?")

    add_diagram(doc, PUML_SUM_EVEN, "l2_sum_even.png",
                "Блок-схема. Сума парних чисел")
    add_writing_box(doc, n_lines=8)

    add_para(doc, "Зразок 1 (Python, з перевіркою всередині):", bold=True)
    add_code_block(doc,
                   "A = int(input('A = '))\n"
                   "B = int(input('B = '))\n"
                   "s = 0\n"
                   "for i in range(A, B + 1):\n"
                   "    if i % 2 == 0:\n"
                   "        s += i\n"
                   "print('Сума парних =', s)")

    add_para(doc, "Зразок 2 (Python, оптимізований — без if):", bold=True)
    add_code_block(doc,
                   "# Знаходимо перше парне >= A\n"
                   "start = A if A % 2 == 0 else A + 1\n"
                   "s = 0\n"
                   "for i in range(start, B + 1, 2):\n"
                   "    s += i\n"
                   "print('Сума парних =', s)")

    add_para(doc, "Зразок 3 (VBA для Excel):", bold=True)
    add_code_block(doc,
                   "Sub SumEven()\n"
                   "    Dim A As Long, B As Long, s As Long, i As Long\n"
                   "    A = CLng(InputBox(\"A =\"))\n"
                   "    B = CLng(InputBox(\"B =\"))\n"
                   "    s = 0\n"
                   "    For i = A To B\n"
                   "        If i Mod 2 = 0 Then s = s + i\n"
                   "    Next i\n"
                   "    MsgBox \"Сума парних = \" & s\n"
                   "End Sub")

    add_answer_text(
        doc,
        "Для A=1, B=10: парні 2,4,6,8,10, сума = 30. "
        "Для A=3, B=3: цикл виконується один раз, сума = 0. "
        "Для A=10, B=1: цикл не виконується, сума = 0."
    )

    # ===== Завдання 2.2 — табулювання =====
    doc.add_heading("Завдання 2.2. Табулювання функції y = 2x² − 5", level=2)
    add_para(doc, "Протабулюйте функцію y = 2x² − 5 на відрізку [−5; 5] із "
                  "кроком 0.5. Виведіть результат у вигляді таблиці (X | Y).")
    add_para(doc, "Підказки:", bold=True, size=12)
    add_para(doc, "• У Python range не приймає дробовий крок. Використайте "
                  "while або арифметичну прогресію: x = a + i * h.")
    add_para(doc, "• У Java та VBA — без проблем, якщо лічильник типу double.")
    add_para(doc, "• Обов'язково обмежте кількість знаків після коми (наприклад, "
                  "2 знаки) для читабельності.")

    add_diagram(doc, PUML_TABULATE, "l2_tabulate.png",
                "Блок-схема. Табулювання функції")
    add_writing_box(doc, n_lines=10)

    add_para(doc, "Зразок 1 (Python, з while):", bold=True)
    add_code_block(doc,
                   "a, b, h = -5.0, 5.0, 0.5\n"
                   "x = a\n"
                   "print(f'{\"X\":>6} | {\"Y\":>8}')\n"
                   "print('-' * 17)\n"
                   "while x <= b + 1e-9:        # +1e-9 компенсує похибку float\n"
                   "    y = 2 * x * x - 5\n"
                   "    print(f'{x:6.2f} | {y:8.2f}')\n"
                   "    x += h")

    add_para(doc, "Зразок 2 (Python, з for і цілим лічильником — точніше):", bold=True)
    add_code_block(doc,
                   "a, b, h = -5.0, 5.0, 0.5\n"
                   "n = int(round((b - a) / h)) + 1\n"
                   "print(f'{\"X\":>6} | {\"Y\":>8}')\n"
                   "for i in range(n):\n"
                   "    x = a + i * h\n"
                   "    y = 2 * x * x - 5\n"
                   "    print(f'{x:6.2f} | {y:8.2f}')")

    add_para(doc, "Зразок 3 (VBA для Excel):", bold=True)
    add_code_block(doc,
                   "Sub Tabulate()\n"
                   "    Dim x As Double, y As Double, h As Double\n"
                   "    Dim r As Long\n"
                   "    h = 0.5: r = 1\n"
                   "    Cells(1, 1) = \"X\": Cells(1, 2) = \"Y\"\n"
                   "    For x = -5 To 5 Step h\n"
                   "        r = r + 1\n"
                   "        y = 2 * x * x - 5\n"
                   "        Cells(r, 1) = x\n"
                   "        Cells(r, 2) = y\n"
                   "    Next x\n"
                   "End Sub")

    add_answer_text(
        doc,
        "Початкові рядки таблиці: x=-5 → y=45; x=-4.5 → y=35.5; x=-4 → y=27; "
        "x=0 → y=-5; x=4 → y=27; x=5 → y=45. Усього 21 рядок (n = (5−(−5))/0.5 + 1)."
    )

    # ===== Завдання 2.3 — піраміда =====
    doc.add_heading("Завдання 2.3. Піраміда зі зірочок", level=2)
    add_para(doc, "Створіть алгоритм, який виводить «піраміду» зі зірочок "
                  "заввишки N рівнів, де N задає користувач.")
    add_para(doc, "Приклад для N=4:", bold=True)
    add_code_block(doc,
                   "   *\n"
                   "  ***\n"
                   " *****\n"
                   "*******")
    add_para(doc, "Підказки:", bold=True, size=12)
    add_para(doc, "• Рядок i (від 1 до N) містить (N − i) пробілів і (2i − 1) зірочок.")
    add_para(doc, "• Це задача з вкладеними циклами: зовнішній — по рядках, "
                  "внутрішні — по пробілах і зірочках.")

    add_diagram(doc, PUML_PYRAMID, "l2_pyramid.png",
                "Блок-схема. Піраміда зірочок")
    add_writing_box(doc, n_lines=10)

    add_para(doc, "Зразок 1 (Python):", bold=True)
    add_code_block(doc,
                   "N = int(input('N = '))\n"
                   "for i in range(1, N + 1):\n"
                   "    spaces = ' ' * (N - i)\n"
                   "    stars = '*' * (2 * i - 1)\n"
                   "    print(spaces + stars)")

    add_para(doc, "Зразок 2 (Python, вкладені цикли — без множення рядків):", bold=True)
    add_code_block(doc,
                   "N = int(input('N = '))\n"
                   "for i in range(1, N + 1):\n"
                   "    for _ in range(N - i):\n"
                   "        print(' ', end='')\n"
                   "    for _ in range(2 * i - 1):\n"
                   "        print('*', end='')\n"
                   "    print()")

    add_para(doc, "Зразок 3 (VBA для Excel — вивід у комірки):", bold=True)
    add_code_block(doc,
                   "Sub Pyramid()\n"
                   "    Dim N As Long, i As Long, j As Long\n"
                   "    N = CLng(InputBox(\"N =\"))\n"
                   "    For i = 1 To N\n"
                   "        Cells(i, 1) = Space(N - i) & String(2 * i - 1, \"*\")\n"
                   "    Next i\n"
                   "End Sub")

    add_answer_text(
        doc,
        "Кількість зірочок у рядку i: 2i − 1 (1, 3, 5, 7, …). "
        "Загальна кількість зірочок N². "
        "Кількість пробілів у рядку i: N − i (для N=4: 3, 2, 1, 0)."
    )


def build_level3(doc):
    doc.add_heading("Рівень 3 — Достатній / Високий", level=1)
    add_para(doc, "Аналіз, синтез, оптимізація.", italic=True)

    # ===== 3.1 =====
    doc.add_heading("Завдання 3.1. Оптимізація та аналіз", level=2)
    add_para(doc, "Порівняйте два фрагменти коду для суми парних чисел [A; B]:")
    add_code_block(doc,
                   "# Варіант A: перевірка всередині\n"
                   "s = 0\n"
                   "for i in range(A, B + 1):\n"
                   "    if i % 2 == 0:\n"
                   "        s += i\n"
                   "\n"
                   "# Варіант B: зміна кроку\n"
                   "start = A if A % 2 == 0 else A + 1\n"
                   "s = 0\n"
                   "for i in range(start, B + 1, 2):\n"
                   "    s += i")
    add_para(doc, "Дайте відповіді:", bold=True)
    add_para(doc, "1) Скільки ітерацій виконує кожен варіант для A=1, B=1000?")
    add_para(doc, "2) Який варіант швидший і чому?")
    add_para(doc, "3) Чи завжди варіант B коректний? Розгляньте A=−3, B=0 та A=3, B=3.")
    add_writing_lines(doc, n=5)
    add_answer_text(
        doc,
        "A: 1000 ітерацій (з перевіркою). B: 500 ітерацій (без перевірки — "
        "крок 2). B швидший приблизно вдвічі — менше ітерацій, немає if. "
        "Коректність: при A=−3, B=0 — перше парне = −2; при A=3, B=3 — "
        "перше парне = 4, але 4 > B, тому цикл не виконається. Обидва варіанти "
        "дають правильний результат."
    )

    # ===== 3.2 =====
    doc.add_heading("Завдання 3.2. Числа Армстронга", level=2)
    add_para(doc, "Число називається числом Армстронга, якщо воно дорівнює сумі "
                  "своїх цифр, піднесених до степеня, що дорівнює кількості цифр. "
                  "Наприклад: 153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153.")
    add_para(doc, "Напишіть програму, яка знаходить усі числа Армстронга "
                  "від 1 до 9999 включно.")
    add_para(doc, "Підказки:", bold=True, size=12)
    add_para(doc, "• Розбийте число на цифри: d = n % 10, n //= 10 — у циклі.")
    add_para(doc, "• Використайте вкладений цикл: зовнішній по числах, "
                  "внутрішній — по цифрах.")
    add_writing_box(doc, n_lines=10)
    add_para(doc, "Зразок (Python):", bold=True)
    add_code_block(doc,
                   "def digits(n):\n"
                   "    return [int(c) for c in str(n)]\n"
                   "\n"
                   "found = []\n"
                   "for n in range(1, 10000):\n"
                   "    ds = digits(n)\n"
                   "    k = len(ds)\n"
                   "    total = 0\n"
                   "    for d in ds:\n"
                   "        total += d ** k\n"
                   "    if total == n:\n"
                   "        found.append(n)\n"
                   "print(found)")
    add_answer_text(
        doc,
        "Числа Армстронга до 9999: 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, "
        "407, 1634, 8208, 9474. Перевірка: 370 = 3³+7³+0³=27+343+0=370."
    )

    # ===== 3.3 =====
    doc.add_heading("Завдання 3.3. Вкладені цикли — таблиця множення", level=2)
    add_para(doc, "Виведіть таблицю множення розміром N × N (N — вводить "
                  "користувач) у вигляді:")
    add_code_block(doc,
                   "    1   2   3   4   5\n"
                   "1   1   2   3   4   5\n"
                   "2   2   4   6   8  10\n"
                   "3   3   6   9  12  15\n"
                   "4   4   8  12  16  20\n"
                   "5   5  10  15  20  25")
    add_para(doc, "Підказки:", bold=True, size=12)
    add_para(doc, "• Вкладені цикли: зовнішній — рядки, внутрішній — стовпці.")
    add_para(doc, "• Для вирівнювання використовуйте форматування (f-string у "
                  "Python: {x:4d}, Format у VBA).")
    add_writing_box(doc, n_lines=8)
    add_para(doc, "Зразок (Python):", bold=True)
    add_code_block(doc,
                   "N = int(input('N = '))\n"
                   "print(' ' * 4, end='')\n"
                   "for j in range(1, N + 1):\n"
                   "    print(f'{j:4d}', end='')\n"
                   "print()\n"
                   "for i in range(1, N + 1):\n"
                   "    print(f'{i:4d}', end='')\n"
                   "    for j in range(1, N + 1):\n"
                   "        print(f'{i * j:4d}', end='')\n"
                   "    print()")
    add_answer_text(
        doc,
        "Кількість ітерацій внутрішнього циклу: N² (для N=5 — 25). "
        "Загальна кількість операцій множення — теж N². "
        "Складність алгоритму — O(N²)."
    )

    # ===== 3.4 =====
    doc.add_heading("Завдання 3.4. Рефлексія", level=2)
    add_para(doc, "Дайте розгорнуту відповідь (5–7 речень):")
    add_para(doc, "• У чому полягає основна відмінність for від while?")
    add_para(doc, "• Які типові помилки виникають при роботі з межами циклу?")
    add_para(doc, "• Чому у Python range(1, N) не включає N, а в Java умова "
                  "i <= N — включає? Як це впливає на перенесення коду?")
    add_writing_lines(doc, n=8)


def build_evaluation(doc):
    doc.add_heading("Критерії оцінювання", level=1)
    add_para(doc, "Оцінювання проводиться за 4-рівневою шкалою:")
    add_table(
        doc,
        ["Оцінка", "Критерій"],
        [
            ["«Відмінно» (5)",
             "Студент вільно володіє матеріалом, завдання виконані в повному "
             "обсязі, код оптимізований, аргументація науково обґрунтована."],
            ["«Добре» (4)",
             "Виконано 100% обсягу роботи, але присутні незначні помилки в "
             "оформленні або неточності в поясненнях."],
            ["«Задовільно» (3)",
             "Виконано мінімум 50–60% завдань, студент допускає помилки в "
             "логіці циклів, потребує допомоги викладача."],
            ["«Незадовільно» (2)",
             "Завдання не виконані або виконані з грубими помилками, що "
             "свідчать про нерозуміння теми."],
        ],
    )
    add_para(doc, "", space_after=8)
    add_para(doc, "Розподіл балів за рівнями:", bold=True)
    add_table(
        doc,
        ["Рівень", "Завдання", "Балів"],
        [
            ["1", "1.1, 1.2, 1.3, 1.4", "8"],
            ["2", "2.1, 2.2, 2.3 (основні)", "20"],
            ["3", "3.1, 3.2, 3.3, 3.4", "20"],
        ],
    )


def build_control_questions(doc):
    doc.add_heading("Контрольні запитання", level=1)
    qa = [
        ("Яка функція у Python відповідає за генерацію послідовності чисел "
         "для циклу for?",
         "Функція range(start, stop, step). Вона генерує арифметичну "
         "прогресію від start до stop (не включаючи stop) з кроком step. "
         "Приклад: range(1, 10, 2) → 1, 3, 5, 7, 9."),
        ("Як реалізувати цикл for, що рахує у зворотному порядку (від 10 до 1)?",
         "Python: for i in range(10, 0, -1): ...  — від'ємний крок. "
         "Java: for (i = 10; i >= 1; i--). "
         "VBA: For i = 10 To 1 Step -1 ... Next i."),
        ("Що таке «ітерація» циклу?",
         "Один прохід тіла циклу. Якщо цикл має N ітерацій — тіло "
         "виконується N разів. Між ітераціями лічильник змінюється на крок."),
        ("Чи можна вийти з циклу for достроково? Якщо так, за допомогою якої "
         "команди?",
         "Так. Python: break — виходить із найближчого циклу. "
         "continue — пропускає решту тіла і переходить до наступної ітерації. "
         "Java: break, continue. VBA: Exit For, Continue (VBA не має — "
         "замість continue використовують If … Then GoTo або переписують умову). "
         "Цикл також можна перервати командою return із процедури, що його містить."),
    ]
    for i, (q, a) in enumerate(qa, 1):
        add_para(doc, f"{i}. {q}", bold=True)
        add_para(doc, a)
        add_para(doc, "", space_after=4)


# ==================== ГОЛОВНА ====================

def build_document():
    doc = Document()
    setup_document_styles(doc)

    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)

    build_title_page(doc)
    doc.add_page_break()
    build_discussion(doc)
    build_theory(doc)
    build_block_diagrams_section(doc)
    doc.add_page_break()
    build_level1(doc)
    doc.add_page_break()
    build_level2(doc)
    doc.add_page_break()
    build_level3(doc)
    doc.add_page_break()
    build_evaluation(doc)
    build_control_questions(doc)

    return doc


def main():
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    log.info("Побудова документа…")
    doc = build_document()
    doc.save(OUTPUT_FILE)
    log.info(f"✓ Документ збережено: {OUTPUT_FILE}")
    log.info(f"✓ Діаграми: ./{DIAGRAMS_DIR}/")


if __name__ == "__main__":
    main()