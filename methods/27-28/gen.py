# -*- coding: utf-8 -*-
"""
Генерація конспекту практичного заняття у форматі DOCX.
Форматування: Times New Roman, 14 pt, інтервал 1.25, вирівнювання по ширині.
"""

import os
import io
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import cairosvg
from PIL import Image

# ============================================================
# 1. НАЛАШТУВАННЯ ДОКУМЕНТА
# ============================================================

doc = Document()

# Базовий стиль
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(14)
style.paragraph_format.line_spacing = 1.25
style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
style.paragraph_format.space_after = Pt(6)

# Стилі для заголовків
for i in range(1, 4):
    heading_style = doc.styles[f'Heading {i}']
    heading_style.font.name = 'Times New Roman'
    heading_style.font.size = Pt(16 - i)  # H1=16, H2=15, H3=14
    heading_style.font.bold = True
    heading_style.font.color.rgb = RGBColor(0, 0, 0)
    heading_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    heading_style.paragraph_format.space_before = Pt(12)
    heading_style.paragraph_format.space_after = Pt(6)

# Поля сторінки
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)

# ============================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ
# ============================================================

def add_paragraph(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=14):
    """Додає параграф із заданим форматуванням."""
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    return p

def add_heading_custom(text, level=1):
    """Додає заголовок із налаштованим стилем."""
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16 - level)
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_svg_image(svg_string, width_inches=6.0, caption=None):
    """
    Конвертує SVG-рядок у PNG і вставляє в документ.
    """
    # Конвертація SVG -> PNG
    png_data = cairosvg.svg2png(bytestring=svg_string.encode('utf-8'))
    image_stream = io.BytesIO(png_data)

    # Вставка зображення
    doc.add_picture(image_stream, width=Inches(width_inches))
    # Вирівнювання зображення по центру
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cap.add_run(caption)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.italic = True
        run.font.color.rgb = RGBColor(80, 80, 80)

def add_table(headers, rows, col_widths=None):
    """Додає таблицю з заданими заголовками та рядками."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Заголовки
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = ''
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

    # Рядки
    for row_data in rows:
        row_cells = table.add_row().cells
        for i, cell_text in enumerate(row_data):
            row_cells[i].text = ''
            p = row_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(cell_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)

    # Ширина колонок
    if col_widths:
        for row in table.rows:
            for i, width in enumerate(col_widths):
                row.cells[i].width = Cm(width)

    return table

# ============================================================
# 3. SVG-ДІАГРАМИ
# ============================================================

SVG_DIAGRAM_1 = """<svg width="700" height="520" viewBox="0 0 700 520" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, serif" font-size="14">
  <rect x="1" y="1" width="698" height="518" fill="#ffffff" stroke="#333" stroke-width="1"/>
  <text x="350" y="30" text-anchor="middle" font-size="18" font-weight="bold">Класифікація форм організації навчання інформатики</text>
  <text x="350" y="55" text-anchor="middle" font-size="14" fill="#555">в початковій школі</text>

  <rect x="250" y="80" width="200" height="50" rx="10" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2"/>
  <text x="350" y="110" text-anchor="middle" font-size="14" font-weight="bold" fill="#1a73e8">Форми організації</text>

  <line x1="350" y1="130" x2="130" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="350" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="570" y2="190" stroke="#333" stroke-width="2"/>

  <rect x="30" y="190" width="200" height="45" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="130" y="217" text-anchor="middle" font-size="13" font-weight="bold" fill="#e65100">За кількістю учасників</text>

  <rect x="20" y="255" width="90" height="40" rx="6" fill="#ffe0b2" stroke="#e65100"/>
  <text x="65" y="280" text-anchor="middle" font-size="12">Індивідуальна</text>

  <rect x="115" y="255" width="90" height="40" rx="6" fill="#ffe0b2" stroke="#e65100"/>
  <text x="160" y="280" text-anchor="middle" font-size="12">Парна</text>

  <rect x="20" y="305" width="90" height="40" rx="6" fill="#ffe0b2" stroke="#e65100"/>
  <text x="65" y="330" text-anchor="middle" font-size="12">Групова</text>

  <rect x="115" y="305" width="90" height="40" rx="6" fill="#ffe0b2" stroke="#e65100"/>
  <text x="160" y="330" text-anchor="middle" font-size="12">Фронтальна</text>

  <rect x="65" y="355" width="100" height="35" rx="6" fill="#ffe0b2" stroke="#e65100"/>
  <text x="115" y="377" text-anchor="middle" font-size="12">Колективна</text>

  <rect x="250" y="190" width="200" height="45" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="350" y="217" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">За місцем проведення</text>

  <rect x="240" y="255" width="100" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32"/>
  <text x="290" y="280" text-anchor="middle" font-size="12">Урок у класі</text>

  <rect x="350" y="255" width="120" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32"/>
  <text x="410" y="280" text-anchor="middle" font-size="12">Урок у кабінеті</text>

  <rect x="240" y="305" width="100" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32"/>
  <text x="290" y="330" text-anchor="middle" font-size="12">Екскурсія</text>

  <rect x="350" y="305" width="120" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32"/>
  <text x="410" y="330" text-anchor="middle" font-size="12">Позакласне</text>

  <rect x="470" y="190" width="200" height="45" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="570" y="217" text-anchor="middle" font-size="13" font-weight="bold" fill="#6a1b9a">За дидактичною метою</text>

  <rect x="460" y="255" width="100" height="40" rx="6" fill="#e1bee7" stroke="#6a1b9a"/>
  <text x="510" y="280" text-anchor="middle" font-size="12">Засвоєння знань</text>

  <rect x="570" y="255" width="100" height="40" rx="6" fill="#e1bee7" stroke="#6a1b9a"/>
  <text x="620" y="280" text-anchor="middle" font-size="12">Комбінований</text>

  <rect x="460" y="305" width="100" height="40" rx="6" fill="#e1bee7" stroke="#6a1b9a"/>
  <text x="510" y="330" text-anchor="middle" font-size="12">Узагальнення</text>

  <rect x="570" y="305" width="100" height="40" rx="6" fill="#e1bee7" stroke="#6a1b9a"/>
  <text x="620" y="330" text-anchor="middle" font-size="12">Контроль</text>

  <rect x="515" y="355" width="110" height="35" rx="6" fill="#e1bee7" stroke="#6a1b9a"/>
  <text x="570" y="377" text-anchor="middle" font-size="12">Нестандартні</text>

  <text x="350" y="450" text-anchor="middle" font-size="12" fill="#666">Рис. 1. Класифікація форм організації навчання інформатики</text>
</svg>"""

SVG_DIAGRAM_2 = """<svg width="700" height="420" viewBox="0 0 700 420" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, serif" font-size="14">
  <rect x="1" y="1" width="698" height="418" fill="#ffffff" stroke="#333" stroke-width="1"/>
  <text x="350" y="30" text-anchor="middle" font-size="17" font-weight="bold">Структура уроку інформатики в початковій школі</text>

  <rect x="50" y="80" width="600" height="35" rx="5" fill="#e3f2fd" stroke="#1565c0"/>
  <text x="80" y="103" font-size="13">1. Організація класу (1–2 хв)</text>

  <rect x="50" y="125" width="600" height="35" rx="5" fill="#bbdefb" stroke="#1565c0"/>
  <text x="80" y="148" font-size="13">2. Розминка (5–7 хв)</text>

  <rect x="50" y="170" width="600" height="35" rx="5" fill="#90caf9" stroke="#1565c0"/>
  <text x="80" y="193" font-size="13">3. Опрацювання нового матеріалу (10–12 хв)</text>

  <rect x="50" y="215" width="600" height="35" rx="5" fill="#64b5f6" stroke="#1565c0"/>
  <text x="80" y="238" font-size="13">4. Фізкультпауза (2 хв)</text>

  <rect x="50" y="260" width="600" height="35" rx="5" fill="#42a5f5" stroke="#1565c0"/>
  <text x="80" y="283" font-size="13">5. Робота за комп’ютером (8–15 хв)</text>

  <rect x="50" y="305" width="600" height="35" rx="5" fill="#1e88e5" stroke="#1565c0"/>
  <text x="80" y="328" font-size="13">6. Релаксація для очей</text>

  <rect x="50" y="350" width="600" height="35" rx="5" fill="#1565c0" stroke="#0d47a1"/>
  <text x="80" y="373" font-size="13" fill="white">7. Підведення підсумків (2–5 хв)</text>

  <text x="350" y="405" text-anchor="middle" font-size="11" fill="#888">Рис. 2. Етапи уроку інформатики в початковій школі</text>
</svg>"""

# ============================================================
# 4. НАПОВНЕННЯ ДОКУМЕНТА
# ============================================================

# Титульна частина
add_heading_custom('ПРАКТИЧНЕ ЗАНЯТТЯ', level=1)
add_heading_custom('Тема: Форми організації навчання інформатики. Класифікація форм організації навчання з інформатики в початковій школі', level=2)

add_paragraph('Мета:', bold=True)
add_paragraph('навчальна: засвоїти поняття «форма організації навчання», розглянути класифікацію форм організації навчання інформатики в початковій школі, визначити особливості основного уроку інформатики та інших форм;')
add_paragraph('розвивальна: розвивати вміння аналізувати педагогічні явища, класифікувати форми навчання, добирати оптимальні форми для уроків інформатики в початкових класах;')
add_paragraph('виховна: формувати професійну компетентність майбутнього вчителя інформатики початкової школи, усвідомлення важливості урізноманітнення форм навчальної діяльності молодших школярів.')

# ТЕОРЕТИЧНА ЧАСТИНА
add_heading_custom('ТЕОРЕТИЧНА ЧАСТИНА', level=1)

add_heading_custom('1. Поняття форми організації навчання', level=2)
add_paragraph('У дидактиці форма організації навчання розуміється як зовнішнє вираження, спосіб структурування та організації навчального процесу, що визначає, як саме зміст освіти буде поданий і засвоєний учнями. Поняття «форма» використовується у двох значеннях: як форма навчання (загальна організація освітнього процесу) та як форма організації навчальної діяльності (спосіб взаємодії учасників на конкретному занятті).')
add_paragraph('Для початкової школи вибір форм організації навчання інформатики зумовлений віковими особливостями молодших школярів, санітарно-гігієнічними вимогами до роботи за комп’ютером та необхідністю частої зміни видів діяльності.')

add_heading_custom('2. Класифікація форм організації навчання інформатики', level=2)
add_paragraph('Форми організації навчальної діяльності з інформатики класифікують за кількома критеріями. Найпоширенішою є класифікація за кількістю учасників спільної діяльності: індивідуальна, парна, групова, фронтальна, колективна. Також виокремлюють форми за місцем проведення (урок у класі, урок у комп’ютерному кабінеті, екскурсія, позакласне заняття) та за дидактичною метою (урок засвоєння нових знань, комбінований урок, урок узагальнення та систематизації, урок контролю й корекції, нестандартні уроки).')
add_paragraph('На рис. 1 подано узагальнену схему класифікації форм організації навчання інформатики в початковій школі.')
add_svg_image(SVG_DIAGRAM_1, width_inches=6.0, caption='Рис. 1. Класифікація форм організації навчання інформатики в початковій школі')

add_heading_custom('3. Урок інформатики як основна форма організації навчання', level=2)
add_paragraph('У початковій школі урок є основною формою організації навчальної роботи з інформатики. Специфіка уроку інформатики зумовлена поєднанням теоретичної (безкомп’ютерної) та практичної (комп’ютерної) частин. Тривалість безперервної роботи молодших школярів за комп’ютером не повинна перевищувати 15 хвилин, тому вчитель має передбачати часту зміну видів діяльності.')
add_paragraph('Типова структура уроку інформатики в початковій школі:')
add_paragraph('1. Організація класу — 1–2 хв.')
add_paragraph('2. Розминка (логічні, математичні завдання, завдання на увагу) — 5–7 хв.')
add_paragraph('3. Опрацювання нового матеріалу (бесіда, пояснення, фронтальна робота) — 10–12 хв.')
add_paragraph('4. Фізкультпауза — 2 хв.')
add_paragraph('5. Робота за комп’ютером або творче завдання — 8–15 хв.')
add_paragraph('6. Хвилинка релаксації для очей.')
add_paragraph('7. Підведення підсумків — 2–5 хв.')
add_paragraph('На рис. 2 схематично відображено структуру уроку інформатики в початковій школі.')
add_svg_image(SVG_DIAGRAM_2, width_inches=6.0, caption='Рис. 2. Структура уроку інформатики в початковій школі')

add_heading_custom('4. Характеристика основних форм навчальної діяльності на уроках інформатики', level=2)
add_paragraph('Фронтальна форма передбачає роботу вчителя з усім класом в єдиному темпі. На уроках інформатики в початковій школі фронтальна робота ефективна під час пояснення нового матеріалу, демонстрації презентацій, фронтальної бесіди.')
add_paragraph('Індивідуальна форма забезпечує взаємодію вчителя з одним учнем. У комп’ютерному класі індивідуальна робота реалізується під час виконання практичних завдань за комп’ютером, коли кожен учень працює у власному темпі.')
add_paragraph('Групова форма (робота в малих групах) сприяє розвитку комунікативних навичок, взаємодопомоги та критичного мислення. На уроках інформатики в початкових класах групову роботу доцільно використовувати під час проєктної діяльності, розв’язування проблемних ситуацій, виконання творчих завдань.')
add_paragraph('Парна форма (робота в парах) є різновидом групової, але з мінімальною кількістю учасників. Вона особливо ефективна на уроках інформатики під час взаємоперевірки, спільного виконання завдань за комп’ютером, обговорення алгоритмів дій.')
add_paragraph('Колективна форма відрізняється від фронтальної тим, що учні класу залучаються до спільної діяльності з урахуванням їхніх індивідуальних можливостей, а результат досягається зусиллями всього колективу.')
add_paragraph('Окремо слід зазначити поділ класу на дві групи під час уроку інформатики в комп’ютерному кабінеті. Це дає змогу організувати почергову роботу: одна група займається безкомп’ютерною частиною з учителем початкової школи, інша — комп’ютерною частиною з учителем інформатики, після чого групи змінюються.')

# ПРАКТИЧНА ЧАСТИНА
add_heading_custom('ПРАКТИЧНА ЧАСТИНА', level=1)
add_paragraph('Різнорівневе практичне завдання (до 30 хв)', bold=True)

add_heading_custom('Завдання 1. Репродуктивний рівень (10 хв)', level=3)
add_paragraph('Мета: перевірити засвоєння базових понять теми.')
add_paragraph('Інструкція: заповніть таблицю «Форми організації навчання інформатики в початковій школі». У першій колонці вкажіть форму, у другій — її сутність, у третій — приклад використання на уроці інформатики в початкових класах.')

add_table(
    ['Форма організації', 'Сутність', 'Приклад використання'],
    [
        ['Фронтальна', '', ''],
        ['Індивідуальна', '', ''],
        ['Парна', '', ''],
        ['Групова', '', ''],
        ['Колективна', '', ''],
    ],
    col_widths=[4, 6, 6]
)
add_paragraph('Критерії оцінювання: повнота та правильність заповнення таблиці (максимум 5 балів).')

add_heading_custom('Завдання 2. Конструктивний рівень (10 хв)', level=3)
add_paragraph('Мета: навчитися аналізувати педагогічний досвід та визначати форми організації навчальної діяльності.')
add_paragraph('Інструкція: прочитайте фрагмент конспекту уроку інформатики для 2 класу (додається). Визначте, які форми організації навчальної діяльності використовує вчитель на кожному етапі уроку. Заповніть таблицю.')
add_paragraph('Фрагмент конспекту уроку (тема «Алгоритми в нашому житті»):', italic=True)
add_paragraph('1. Учитель вітається, перевіряє готовність учнів до уроку (1 хв).')
add_paragraph('2. Учитель демонструє презентацію з прикладами алгоритмів у побуті, ставить запитання всьому класу, учні відповідають (5 хв).')
add_paragraph('3. Учні об’єднуються в пари та складають алгоритм «Ранкові збори до школи» на картках (7 хв).')
add_paragraph('4. Учитель пропонує учням за комп’ютерами індивідуально виконати завдання в програмі-тренажері «Послідовність дій» (10 хв).')
add_paragraph('5. Учні в групах по 4 особи презентують свої алгоритми, обговорюють, який алгоритм найзручніший (5 хв).')
add_paragraph('6. Підсумок уроку: учитель разом з учнями пригадує, що таке алгоритм, оцінює роботу (2 хв).')

add_table(
    ['Етап уроку', 'Форма організації навчальної діяльності'],
    [
        ['1. Організація класу', ''],
        ['2. Демонстрація презентації, бесіда', ''],
        ['3. Складання алгоритму в парах', ''],
        ['4. Робота за комп’ютерами', ''],
        ['5. Презентація в групах', ''],
        ['6. Підсумок', ''],
    ],
    col_widths=[8, 8]
)
add_paragraph('Критерії оцінювання: правильність визначення форм для кожного етапу (максимум 6 балів).')

add_heading_custom('Завдання 3. Творчий рівень (10 хв)', level=3)
add_paragraph('Мета: розвивати вміння проєктувати фрагмент уроку з використанням різних форм організації навчання.')
add_paragraph('Інструкція: оберіть одну з тем з інформатики для початкової школи (наприклад, «Поняття про інформацію», «Комп’ютер та його складові», «Виконавці та алгоритми»). Розробіть фрагмент уроку (тривалістю 10–12 хвилин), у якому доцільно поєднати фронтальну, парну та індивідуальну форми роботи. Заповніть таблицю.')

add_table(
    ['Етап фрагмента', 'Зміст діяльності', 'Форма організації', 'Тривалість'],
    [
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
    ],
    col_widths=[4, 6, 3, 3]
)
add_paragraph('Критерії оцінювання: логічність побудови фрагмента, доцільність обраних форм, відповідність віковим особливостям учнів (максимум 9 балів).')

# КОНТРОЛЬНІ ЗАПИТАННЯ
add_heading_custom('КОНТРОЛЬНІ ЗАПИТАННЯ', level=1)
questions = [
    'Дайте визначення поняття «форма організації навчання». Які два значення має поняття «форма» у дидактиці?',
    'За якими критеріями класифікують форми організації навчальної діяльності з інформатики?',
    'Охарактеризуйте фронтальну, індивідуальну, парну, групову та колективну форми роботи. Наведіть приклади їх використання на уроках інформатики в початковій школі.',
    'Чому урок є основною формою організації навчання інформатики в початковій школі?',
    'Опишіть типову структуру уроку інформатики в початковій школі. Чим зумовлена необхідність частих змін видів діяльності?',
    'Які санітарно-гігієнічні вимоги слід враховувати під час організації роботи молодших школярів за комп’ютером?',
    'У чому полягає доцільність поділу класу на дві групи під час уроку інформатики в комп’ютерному кабінеті?',
    'Наведіть приклади нестандартних форм уроку інформатики, які можна використовувати в початковій школі.',
]
for i, q in enumerate(questions, 1):
    add_paragraph(f'{i}. {q}')

# ============================================================
# 5. ЗБЕРЕЖЕННЯ
# ============================================================

output_file = 'praktychne_zanyattya_formy_orhanizatsii_informatyky.docx'
doc.save(output_file)
print(f'Документ збережено: {output_file}')