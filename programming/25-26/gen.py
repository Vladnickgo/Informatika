#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор DOCX документа для Самостійної роботи №5
Тема: Використання повного та неповного розгалуження

Залежності:
    pip install python-docx requests

Запуск:
    python generate_docx.py
"""

import os
import sys
import zlib
import logging

try:
    import requests
except ImportError:
    print("❌ Потрібен пакет requests. Встановіть: pip install requests")
    sys.exit(1)

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("❌ Потрібен пакет python-docx. Встановіть: pip install python-docx")
    sys.exit(1)


# ============ КОНФІГУРАЦІЯ ============
FONT_NAME        = "Times New Roman"
FONT_SIZE        = Pt(14)
CODE_FONT_NAME   = "Consolas"
CODE_FONT_SIZE   = Pt(10)
LINE_SPACING     = 1.25
OUTPUT_FILE      = "Самостійна_робота_5.docx"
DIAGRAMS_DIR     = "diagrams"
SKIP_DIAGRAMS    = False  # True → офлайн-режим (без завантаження блок-схем)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


# ============ PLANTUML ============

def encode_plantuml(text: str) -> str:
    """Кодує PlantUML-джерело у формат, який приймає plantuml.com."""
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


def download_plantuml_png(source: str, output_path: str) -> bool:
    """Завантажує PNG-зображення діаграми з plantuml.com."""
    encoded = encode_plantuml(source)
    url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    try:
        log.info(f"  ↳ {output_path}")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        if not resp.content.startswith(b"\x89PNG"):
            log.error(f"  ↳ отримано не PNG")
            return False
        with open(output_path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        log.error(f"  ↳ помилка: {e}")
        return False


# ============ СТИЛІ ============

def _set_font_on_rpr(rpr_element, font_name: str):
    """Встановлює шрифт для всіх 'мов' (ascii, hAnsi, eastAsia, cs)."""
    rfonts = rpr_element.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr_element.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), font_name)


def setup_document_styles(doc: Document):
    """Times New Roman 14pt, міжрядковий інтервал 1.25."""
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


# ============ ХЕЛПЕРИ ============

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


def add_code_block(doc, code: str):
    """Блок коду: моноширинний шрифт, світло-сірий фон, тонка рамка."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.0
    pf.space_before = Pt(4)
    pf.space_after = Pt(8)
    pf.left_indent = Cm(0.5)

    pPr = p._p.get_or_add_pPr()
    # Рамка
    pBdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:space"), "4")
        b.set(qn("w:color"), "CCCCCC")
        pBdr.append(b)
    pPr.append(pBdr)
    # Фон
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F2F2F2")
    pPr.append(shd)

    run = p.add_run(code)
    run.font.name = CODE_FONT_NAME
    run.font.size = CODE_FONT_SIZE
    _set_font_on_rpr(run._r.get_or_add_rPr(), CODE_FONT_NAME)
    return p


def add_table(doc, headers, rows, font_size=11, fill_empty=False):
    """Таблиця з шапкою. Порожні клітинки (fill_empty=True) — жовтий фон."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # Заголовки
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

    # Дані
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
                shd.set(qn("w:val"), "clear")
                shd.set(qn("w:color"), "auto")
                shd.set(qn("w:fill"), "FFF9E6")
                tcPr.append(shd)

    return table


def add_diagram(doc, puml_source: str, filename: str, caption: str = ""):
    """Діаграма PlantUML: завантажує PNG і вставляє в документ."""
    if SKIP_DIAGRAMS:
        add_para(doc, f"[Діаграма {filename} — режим без завантаження]",
                 italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        return

    path = os.path.join(DIAGRAMS_DIR, filename)
    if download_plantuml_png(puml_source, path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        try:
            p.add_run().add_picture(path, width=Inches(4))
        except Exception as e:
            log.error(f"Не вдалося вставити {path}: {e}")
            p.add_run("[помилка вставки]").italic = True
    else:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("[Діаграма недоступна — перевірте інтернет]")
        run.italic = True
        run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(caption)
        run.italic = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


# ============ PLANTUML ДЖЕРЕЛА ============

PUML_FULL_X = """@startuml
skinparam style strictuml
skinparam activity {
  BackgroundColor #DBEAFE
  BorderColor #2563EB
  DiamondBackgroundColor #EDE9FE
  DiamondBorderColor #7C3AED
}
start
:Ввести число x;
if (x > 0?) then (Так)
  :Вивести "Додатне";
else (Ні)
  :Вивести "Не додатне";
endif
stop
@enduml"""

PUML_INC_X = """@startuml
skinparam style strictuml
skinparam activity {
  BackgroundColor #DBEAFE
  BorderColor #2563EB
  DiamondBackgroundColor #EDE9FE
  DiamondBorderColor #7C3AED
}
start
:Ввести число x;
if (x > 0?) then (Так)
  :Вивести "Додатне";
endif
stop
@enduml"""

PUML_FULL_AB = """@startuml
skinparam style strictuml
skinparam activity {
  BackgroundColor #F0FDF4
  BorderColor #16A34A
  DiamondBackgroundColor #DCFCE7
  DiamondBorderColor #16A34A
}
start
:Ввести a, b;
if (a > b?) then (Так)
  :Вивести "a більше";
else (Ні)
  :Вивести "b більше або рівне";
endif
stop
@enduml"""


# ============ ПОБУДОВА ДОКУМЕНТА ============

def build_document() -> Document:
    doc = Document()
    setup_document_styles(doc)

    for s in doc.sections:
        s.top_margin = Cm(2)
        s.bottom_margin = Cm(2)
        s.left_margin = Cm(2.5)
        s.right_margin = Cm(1.5)

    # ===== ТИТУЛЬНА =====
    add_para(doc, "", space_after=60)
    add_para(doc, "САМОСТІЙНА РОБОТА №5", bold=True, size=20,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "Використання повного та неповного розгалуження",
             bold=True, size=18, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)

    add_para(doc, "Мета:", bold=True)
    add_para(doc, "Закріпити знання про повне та неповне розгалуження. "
                  "Проаналізувати приклади застосування кожного типу в реальних задачах. "
                  "Розвивати вміння вибирати оптимальний тип розгалуження для конкретної "
                  "ситуації. Розвивати логічне мислення через аналіз умов. Виховувати "
                  "гнучкість мислення, здатність знаходити різні шляхи вирішення однієї проблеми.")

    add_para(doc, "Обладнання:", bold=True)
    add_para(doc, "Інструкційні картки.")

    add_para(doc, "Література:", bold=True)
    add_para(doc, "1. Васильєв О. Алгоритми. Київ: Навчальна книга – Богдан, 2022. 424 с.")
    add_para(doc, "2. Васильєв О. Програмування мовою Java. Київ: Навчальна книга – Богдан, 2020. 696 с.")

    doc.add_page_break()

    # ===== ПИТАННЯ ДЛЯ ОБГОВОРЕННЯ =====
    doc.add_heading("Питання для обговорення", level=1)
    questions = [
        "У чому відмінність між повним та неповним розгалуженням?",
        "Наведіть приклад із життя, де використовується повне розгалуження.",
        "Наведіть приклад із життя, де використовується неповне розгалуження.",
        "Як вибрати, який тип розгалуження краще використати для певної задачі?",
        "Чому неповне розгалуження називають ще «обхідним»?",
    ]
    for i, q in enumerate(questions, 1):
        add_para(doc, f"{i}. {q}")

    # ===== ТЕОРІЯ =====
    doc.add_heading("Теоретичні відомості", level=1)

    doc.add_heading("1. Що таке розгалуження?", level=2)
    add_para(doc, "Розгалуження — це алгоритмічна структура, яка передбачає вибір однієї "
                  "з кількох можливих дій залежно від виконання певної умови.")

    doc.add_heading("2. Повне розгалуження", level=2)
    add_para(doc, "Повне розгалуження — це конструкція, в якій передбачені дії як для випадку, "
                  "коли умова істинна, так і для випадку, коли умова хибна.")
    add_para(doc, "Синтаксис у мовах програмування:", bold=True)
    add_table(
        doc,
        ["Мова", "Синтаксис"],
        [
            ["Java",        "if (умова) { дія1; } else { дія2; }"],
            ["Python",      "if умова: дія1\nelse: дія2"],
            ["VBA (Excel)", "If умова Then дія1 Else дія2"],
            ["Scratch",     "якщо <умова> тоді дія1 інакше дія2"],
        ],
    )
    add_para(doc, "")
    add_para(doc, "Приклад (перевірка парності, Java):", bold=True)
    add_code_block(doc,
                   'if (число % 2 == 0) {\n'
                   '    System.out.println("Число парне");\n'
                   '} else {\n'
                   '    System.out.println("Число непарне");\n'
                   '}')
    add_para(doc, "Приклад із життя:", bold=True)
    add_para(doc, "«Якщо на вулиці дощ, то візьми парасольку, інакше — залиш парасольку вдома».")

    doc.add_heading("3. Неповне розгалуження", level=2)
    add_para(doc, "Неповне розгалуження — це конструкція, в якій дія передбачена тільки "
                  "для випадку, коли умова істинна. Якщо умова хибна, виконання алгоритму "
                  "продовжується без додаткових дій (обхід).")
    add_para(doc, "Синтаксис у мовах програмування:", bold=True)
    add_table(
        doc,
        ["Мова", "Синтаксис"],
        [
            ["Java",        "if (умова) { дія1; }"],
            ["Python",      "if умова: дія1"],
            ["VBA (Excel)", "If умова Then дія1"],
            ["Scratch",     "якщо <умова> тоді дія1"],
        ],
    )
    add_para(doc, "")
    add_para(doc, "Приклад (дія тільки при істинній умові, Java):", bold=True)
    add_code_block(doc,
                   'if (температура < 0) {\n'
                   '    System.out.println("На вулиці мороз! Одягнись тепліше.");\n'
                   '}')
    add_para(doc, "Приклад із життя:", bold=True)
    add_para(doc, "«Якщо на світлофорі червоне світло — зупинись».")

    doc.add_heading("4. Порівняння повного та неповного розгалуження", level=2)
    add_table(
        doc,
        ["Ознака", "Повне розгалуження", "Неповне розгалуження"],
        [
            ["Кількість гілок", "2", "1"],
            ["Наявність else", "Так", "Ні"],
            ["Обхід дії", "Ні", "Так"],
            ["Коли використовувати",
             "Коли потрібно виконати дію в обох випадках",
             "Коли дія потрібна тільки при виконанні умови"],
        ],
    )

    doc.add_heading("5. Блок-схеми розгалужень", level=2)
    add_para(doc, "Блок-схема повного розгалуження:", bold=True)
    add_diagram(doc, PUML_FULL_X, "full_x.png",
                "Малюнок 1. Повне розгалуження (обидві гілки)")
    add_para(doc, "Блок-схема неповного розгалуження:", bold=True)
    add_diagram(doc, PUML_INC_X, "incomplete_x.png",
                "Малюнок 2. Неповне розгалуження (одна гілка)")

    doc.add_heading("6. Приклади для початкової школи", level=2)
    add_para(doc, "Приклад 1. Неповне розгалуження (Scratch):", bold=True)
    add_code_block(doc,
                   "якщо <(відповідь) = (10)> тоді\n"
                   "    сказати [Правильно!]")
    add_para(doc, "Приклад 2. Повне розгалуження (Scratch):", bold=True)
    add_code_block(doc,
                   "якщо <(відповідь) = (10)> тоді\n"
                   "    сказати [Правильно!]\n"
                   "інакше\n"
                   "    сказати [Неправильно! Спробуй ще раз]")

    doc.add_heading("7. Типові помилки при використанні розгалужень", level=2)
    add_table(
        doc,
        ["Помилка", "Опис", "Виправлення"],
        [
            ["Зайве else",
             "Використання else, коли дія в гілці «ні» не потрібна",
             "Замінити на неповне розгалуження"],
            ["Пропущене else",
             "Коли потрібна дія в обох випадках",
             "Додати else"],
            ["Зайві фігурні дужки (Java)",
             "Неправильне групування дій",
             "Правильно розставити дужки"],
        ],
    )

    doc.add_page_break()

    # ===== ПРАКТИЧНІ ЗАВДАННЯ =====
    doc.add_heading("Практичне завдання", level=1)
    add_para(doc, "Тема роботи: «Аналіз та створення алгоритмів з використанням "
                  "повного та неповного розгалуження».", bold=True)

    doc.add_heading("Завдання 1. Визначення типу розгалуження (8 балів)", level=2)
    add_para(doc, "Визначте, який тип розгалуження (повне чи неповне) використаний "
                  "у наведених прикладах:")
    add_table(
        doc,
        ["№", "Приклад", "Тип розгалуження", "Чому?"],
        [
            ["1", "Якщо на вулиці дощ, то візьми парасольку", "", ""],
            ["2", "Якщо на вулиці дощ, то візьми парасольку, інакше — залиш вдома", "", ""],
            ["3", "Якщо оцінка >= 12, то повідомлення «Відмінно», інакше — «Добре»", "", ""],
            ["4", "Якщо число додатне, то збільшити його на 1", "", ""],
            ["5", "Якщо клієнт купив більше ніж на 1000 грн, то надати знижку 10%", "", ""],
            ["6", "Якщо температура повітря нижче 0, то надіти шапку", "", ""],
            ["7", "Якщо дитина хворіє, то залишити її вдома, інакше — відвести до школи", "", ""],
            ["8", "Якщо число дорівнює 0, то вивести повідомлення «Число нульове»", "", ""],
        ],
        font_size=11, fill_empty=True,
    )

    doc.add_heading("Завдання 2. Перетворення між формами (6 балів)", level=2)
    add_para(doc, "2.1. Перетворіть неповне розгалуження на повне:", bold=True)
    add_para(doc, "Неповне: Якщо пароль введено правильно, то надати доступ.")
    add_para(doc, "Повне: Якщо пароль введено правильно, то надати доступ, інакше _______________. ")
    add_para(doc, "2.2. Перетворіть повне розгалуження на неповне:", bold=True)
    add_para(doc, "Повне: Якщо значення більше 100, то повідомити «Дуже велике», "
                  "інакше повідомити «Допустиме».")
    add_para(doc, "Неповне: Якщо значення більше 100, то ________________________________.")
    add_para(doc, "2.3. Перетворіть текстовий опис на код (Java або Scratch):", bold=True)
    add_para(doc, "Умова: Якщо вік людини більший або дорівнює 18, то вивести повідомлення "
                  "«Повнолітній», інакше вивести «Неповнолітній».")

    doc.add_heading("Завдання 3. Складання блок-схем (10 балів)", level=2)
    add_para(doc, "Побудуйте блок-схеми для наведених алгоритмів:")
    add_para(doc, "1. Якщо x > 0, то вивести «Додатне» (3 бали)", bold=True)
    add_diagram(doc, PUML_INC_X, "task3_1.png",
                "Малюнок 3. Неповне розгалуження для x > 0")
    add_para(doc, "2. Якщо x > 0, то вивести «Додатне», інакше вивести "
                  "«Не додатне» (3 бали)", bold=True)
    add_diagram(doc, PUML_FULL_X, "task3_2.png",
                "Малюнок 4. Повне розгалуження для x > 0")
    add_para(doc, "3. Якщо a > b, то вивести «a більше», інакше вивести "
                  "«b більше або рівне» (4 бали)", bold=True)
    add_diagram(doc, PUML_FULL_AB, "task3_3.png",
                "Малюнок 5. Повне розгалуження для a > b")

    doc.add_heading("Завдання 4. Написання програмного коду (12 балів)", level=2)
    add_para(doc, "Напишіть програмний код (Java, Python або Scratch) для наведених завдань:")
    add_para(doc, "Як запустити VBA в Excel: Alt+F11 → Insert → Module → F5.",
             italic=True, size=12)

    add_para(doc, "1. Визначити, чи є введене число додатним. "
                  "Якщо так, вивести «Число додатне» (3 бали)", bold=True)
    add_para(doc, "Приклад розв'язку (VBA для Excel):")
    add_code_block(doc,
                   'Sub CheckPositive()\n'
                   '    Dim x As Double\n'
                   '    x = CDbl(InputBox("Введіть число:"))\n'
                   '\n'
                   '    If x > 0 Then\n'
                   '        MsgBox "Число додатне"\n'
                   '    End If\n'
                   'End Sub')

    add_para(doc, "2. Визначити, чи є введене число парним. Вивести відповідне "
                  "повідомлення для обох випадків (4 бали)", bold=True)
    add_para(doc, "Приклад розв'язку (VBA для Excel):")
    add_code_block(doc,
                   'Sub CheckEven()\n'
                   '    Dim x As Long\n'
                   '    x = CLng(InputBox("Введіть ціле число:"))\n'
                   '\n'
                   '    If x Mod 2 = 0 Then\n'
                   '        MsgBox "Число парне"\n'
                   '    Else\n'
                   '        MsgBox "Число непарне"\n'
                   '    End If\n'
                   'End Sub')

    add_para(doc, "3. Ввести два числа. Вивести більше з них (5 балів)", bold=True)
    add_para(doc, "Приклад розв'язку (VBA для Excel):")
    add_code_block(doc,
                   'Sub MaxOfTwo()\n'
                   '    Dim a As Double, b As Double\n'
                   '    a = CDbl(InputBox("a ="))\n'
                   '    b = CDbl(InputBox("b ="))\n'
                   '\n'
                   '    If a > b Then\n'
                   '        MsgBox "Більше: " & a\n'
                   '    Else\n'
                   '        MsgBox "Більше: " & b\n'
                   '    End If\n'
                   'End Sub')

    doc.add_heading("Завдання 5. Аналіз педагогічних ситуацій (8 балів)", level=2)
    add_para(doc, "Для кожної ситуації визначте, який тип розгалуження (повне чи неповне) "
                  "потрібно використати, та поясніть чому.")
    situations = [
        "Ситуація 1. На уроці інформатики вчитель перевіряє, чи правильно учень "
        "відповів на запитання. Якщо правильно — ставить «+», якщо ні — ставить «-».",
        "Ситуація 2. Вчитель перевіряє, чи є домашнє завдання в окремого учня. "
        "Якщо є — ставить оцінку, якщо немає — не ставить.",
        "Ситуація 3. Учні грають у гру. Якщо гравець набрав більше 10 очок, "
        "він переходить на наступний рівень. Інакше — залишається на поточному.",
        "Ситуація 4. Програма перевіряє, чи введений пароль правильний. Якщо ні — "
        "просить ввести ще раз (цикл + розгалуження). Якщо правильний — надає доступ.",
    ]
    for s in situations:
        add_para(doc, s)
        add_para(doc, "Тип: ______________________. Пояснення: _______________________________.")

    doc.add_heading("Завдання 6. Створення власних прикладів (+6 балів, додаткове)", level=2)
    add_para(doc, "Складіть по 2 приклади:")
    add_para(doc, "Для повного розгалуження (з життя молодшого школяра):", bold=True)
    add_para(doc, "1. _____________________________________________________________")
    add_para(doc, "2. _____________________________________________________________")
    add_para(doc, "Для неповного розгалуження (з життя молодшого школяра):", bold=True)
    add_para(doc, "1. _____________________________________________________________")
    add_para(doc, "2. _____________________________________________________________")

    doc.add_heading("Завдання 7. Рефлексія (5 балів)", level=2)
    add_para(doc, "Напишіть короткий текст (5-7 речень) на тему:")
    add_para(doc, "— У чому різниця між повним та неповним розгалуженням?")
    add_para(doc, "— Коли доцільно використовувати кожен тип?")
    add_para(doc, "— Які труднощі можуть виникнути в учнів початкової школи "
                  "при вивченні розгалужень?")
    for _ in range(6):
        add_para(doc, "_" * 85)

    doc.add_page_break()

    # ===== КРИТЕРІЇ ОЦІНЮВАННЯ =====
    doc.add_heading("Критерії оцінювання", level=1)
    add_table(
        doc,
        ["Критерій", "Бали"],
        [
            ["Визначення типу розгалуження (завдання 1)", "8"],
            ["Перетворення між формами (завдання 2)", "6"],
            ["Блок-схеми (завдання 3)", "10"],
            ["Написання програмного коду (завдання 4)", "12"],
            ["Аналіз педагогічних ситуацій (завдання 5)", "8"],
            ["(додаткове) Власні приклади (завдання 6)", "+6"],
            ["Рефлексія (завдання 7)", "5"],
            ["Максимальна кількість балів", "49 (+6 додаткових)"],
        ],
    )

    # ===== КОНТРОЛЬНІ ЗАПИТАННЯ =====
    doc.add_heading("Контрольні запитання", level=1)
    control = [
        "Що таке повне розгалуження? Наведіть приклад.",
        "Що таке неповне розгалуження? Наведіть приклад.",
        "Як розпізнати повне розгалуження на блок-схемі?",
        "Як розпізнати неповне розгалуження на блок-схемі?",
        "У яких випадках використовують if-else, а в яких лише if?",
        "Чи можна замінити повне розгалуження неповним? Якщо так, то як?",
        "Чи можна замінити неповне розгалуження повним? Якщо так, то як?",
        "Як вибрати тип розгалуження для конкретної задачі?",
        "Що станеться, якщо в повному розгалуженні забути написати else?",
        "Наведіть приклад неповного розгалуження в навчальному процесі "
        "початкової школи.",
    ]
    for i, q in enumerate(control, 1):
        add_para(doc, f"{i}. {q}")

    return doc


# ============ ТОЧКА ВХОДУ ============

def main():
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    log.info("Побудова документа…")
    doc = build_document()
    doc.save(OUTPUT_FILE)
    log.info(f"✓ Документ збережено: {OUTPUT_FILE}")
    log.info(f"✓ Діаграми: ./{DIAGRAMS_DIR}/")


if __name__ == "__main__":
    main()