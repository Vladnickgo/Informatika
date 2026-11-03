# -*- coding: utf-8 -*-
"""
Генерація конспекту матеріалів для самостійної роботи у форматі DOCX.
Тема: Форми організації навчання. Сутність організаційних форм навчання.
Форматування: Times New Roman, 14 pt, інтервал 1.25, вирівнювання по ширині.
"""

import io
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import cairosvg

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

# Стилі заголовків
for i in range(1, 4):
    heading_style = doc.styles[f'Heading {i}']
    heading_style.font.name = 'Times New Roman'
    heading_style.font.size = Pt(16 - i)
    heading_style.font.bold = True
    heading_style.font.color.rgb = RGBColor(0, 0, 0)
    heading_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    heading_style.paragraph_format.space_before = Pt(12)
    heading_style.paragraph_format.space_after = Pt(6)

# Поля
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)

# ============================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ
# ============================================================

def add_paragraph(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=14):
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
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16 - level)
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_svg_image(svg_string, width_inches=6.0, caption=None):
    png_data = cairosvg.svg2png(bytestring=svg_string.encode('utf-8'))
    image_stream = io.BytesIO(png_data)
    doc.add_picture(image_stream, width=Inches(width_inches))
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
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = ''
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
    for row_data in rows:
        row_cells = table.add_row().cells
        for i, cell_text in enumerate(row_data):
            row_cells[i].text = ''
            p = row_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(cell_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
    if col_widths:
        for row in table.rows:
            for i, width in enumerate(col_widths):
                row.cells[i].width = Cm(width)
    return table

# ============================================================
# 3. SVG-ДІАГРАМИ
# ============================================================

SVG_DIAGRAM_1 = """<svg width="700" height="500" viewBox="0 0 700 500" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, serif" font-size="14">
  <rect x="1" y="1" width="698" height="498" fill="#ffffff" stroke="#333" stroke-width="1"/>
  <text x="350" y="30" text-anchor="middle" font-size="18" font-weight="bold">Сутність організаційної форми навчання</text>
  <text x="350" y="55" text-anchor="middle" font-size="13" fill="#555">(структурно-логічна схема)</text>

  <ellipse cx="350" cy="150" rx="140" ry="55" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2.5"/>
  <text x="350" y="145" text-anchor="middle" font-size="15" font-weight="bold" fill="#1a73e8">Форма організації</text>
  <text x="350" y="165" text-anchor="middle" font-size="15" font-weight="bold" fill="#1a73e8">навчання</text>

  <rect x="30" y="240" width="120" height="60" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="90" y="270" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Просторово-часова</text>
  <text x="90" y="290" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">визначеність</text>
  <line x1="250" y1="200" x2="120" y2="240" stroke="#333" stroke-width="1.5"/>

  <rect x="170" y="240" width="120" height="60" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="230" y="270" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">Склад</text>
  <text x="230" y="290" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">учасників</text>
  <line x1="300" y1="200" x2="230" y2="240" stroke="#333" stroke-width="1.5"/>

  <rect x="310" y="240" width="120" height="60" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="370" y="270" text-anchor="middle" font-size="12" font-weight="bold" fill="#6a1b9a">Порядок і</text>
  <text x="370" y="290" text-anchor="middle" font-size="12" font-weight="bold" fill="#6a1b9a">режим</text>
  <line x1="350" y1="205" x2="370" y2="240" stroke="#333" stroke-width="1.5"/>

  <rect x="450" y="240" width="120" height="60" rx="8" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
  <text x="510" y="270" text-anchor="middle" font-size="12" font-weight="bold" fill="#00838f">Характер</text>
  <text x="510" y="290" text-anchor="middle" font-size="12" font-weight="bold" fill="#00838f">керівництва</text>
  <line x1="420" y1="200" x2="510" y2="240" stroke="#333" stroke-width="1.5"/>

  <rect x="560" y="240" width="120" height="60" rx="8" fill="#fce4ec" stroke="#ad1457" stroke-width="2"/>
  <text x="620" y="270" text-anchor="middle" font-size="12" font-weight="bold" fill="#ad1457">Ступінь</text>
  <text x="620" y="290" text-anchor="middle" font-size="12" font-weight="bold" fill="#ad1457">самостійності</text>
  <line x1="450" y1="200" x2="620" y2="240" stroke="#333" stroke-width="1.5"/>

  <text x="350" y="360" text-anchor="middle" font-size="14" font-weight="bold">Функції форми організації навчання</text>
  <rect x="40" y="380" width="140" height="55" rx="6" fill="#e3f2fd" stroke="#1565c0"/>
  <text x="110" y="412" text-anchor="middle" font-size="12">Впорядкування</text>

  <rect x="195" y="380" width="140" height="55" rx="6" fill="#bbdefb" stroke="#1565c0"/>
  <text x="265" y="412" text-anchor="middle" font-size="12">Організація взаємодії</text>

  <rect x="350" y="380" width="140" height="55" rx="6" fill="#90caf9" stroke="#1565c0"/>
  <text x="420" y="412" text-anchor="middle" font-size="12">Реалізація змісту</text>

  <rect x="505" y="380" width="150" height="55" rx="6" fill="#64b5f6" stroke="#1565c0"/>
  <text x="580" y="412" text-anchor="middle" font-size="12">Керування діяльністю</text>

  <text x="350" y="475" text-anchor="middle" font-size="11" fill="#888">Рис. 1. Структурно-логічна схема сутності форми організації навчання</text>
</svg>"""

SVG_DIAGRAM_2 = """<svg width="700" height="560" viewBox="0 0 700 560" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, serif" font-size="13">
  <rect x="1" y="1" width="698" height="558" fill="#ffffff" stroke="#333" stroke-width="1"/>
  <text x="350" y="28" text-anchor="middle" font-size="17" font-weight="bold">Класифікація організаційних форм навчання</text>
  <text x="350" y="50" text-anchor="middle" font-size="12" fill="#555">(за різними критеріями)</text>

  <ellipse cx="350" cy="110" rx="150" ry="30" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2"/>
  <text x="350" y="116" text-anchor="middle" font-size="14" font-weight="bold" fill="#1a73e8">Форми організації навчання</text>

  <line x1="220" y1="135" x2="110" y2="170" stroke="#333" stroke-width="1.5"/>
  <rect x="20" y="170" width="180" height="35" rx="6" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="110" y="192" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">За кількістю учнів</text>
  <text x="110" y="220" text-anchor="middle" font-size="11">Індивідуальна, парна,</text>
  <text x="110" y="236" text-anchor="middle" font-size="11">групова, фронтальна</text>

  <line x1="290" y1="140" x2="270" y2="170" stroke="#333" stroke-width="1.5"/>
  <rect x="200" y="170" width="150" height="35" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="275" y="192" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">За місцем</text>
  <text x="275" y="220" text-anchor="middle" font-size="11">У класі, кабінеті,</text>
  <text x="275" y="236" text-anchor="middle" font-size="11">на природі</text>

  <line x1="350" y1="140" x2="350" y2="170" stroke="#333" stroke-width="1.5"/>
  <rect x="355" y="170" width="130" height="35" rx="6" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="1.5"/>
  <text x="420" y="192" text-anchor="middle" font-size="12" font-weight="bold" fill="#6a1b9a">За тривалістю</text>
  <text x="420" y="220" text-anchor="middle" font-size="11">Урок, факультатив,</text>
  <text x="420" y="236" text-anchor="middle" font-size="11">гурток</text>

  <line x1="410" y1="135" x2="500" y2="170" stroke="#333" stroke-width="1.5"/>
  <rect x="485" y="170" width="195" height="35" rx="6" fill="#e0f7fa" stroke="#00838f" stroke-width="1.5"/>
  <text x="582" y="192" text-anchor="middle" font-size="12" font-weight="bold" fill="#00838f">За дидактичною метою</text>
  <text x="582" y="220" text-anchor="middle" font-size="11">Засвоєння, комбінований,</text>
  <text x="582" y="236" text-anchor="middle" font-size="11">узагальнення, контроль</text>

  <line x1="230" y1="145" x2="140" y2="300" stroke="#333" stroke-width="1.5"/>
  <rect x="30" y="300" width="220" height="35" rx="6" fill="#fce4ec" stroke="#ad1457" stroke-width="1.5"/>
  <text x="140" y="322" text-anchor="middle" font-size="12" font-weight="bold" fill="#ad1457">За ступенем самостійності</text>
  <text x="140" y="350" text-anchor="middle" font-size="11">Під керівництвом учителя,</text>
  <text x="140" y="366" text-anchor="middle" font-size="11">самостійна робота</text>

  <line x1="470" y1="145" x2="560" y2="300" stroke="#333" stroke-width="1.5"/>
  <rect x="450" y="300" width="220" height="35" rx="6" fill="#f1f8e9" stroke="#558b2f" stroke-width="1.5"/>
  <text x="560" y="322" text-anchor="middle" font-size="12" font-weight="bold" fill="#558b2f">За змістом</text>
  <text x="560" y="350" text-anchor="middle" font-size="11">Предметні, міжпредметні,</text>
  <text x="560" y="366" text-anchor="middle" font-size="11">інтегровані</text>

  <text x="350" y="440" text-anchor="middle" font-size="12" fill="#666" font-style="italic">Форми тісно взаємопов’язані: одна й та сама форма може</text>
  <text x="350" y="458" text-anchor="middle" font-size="12" fill="#666" font-style="italic">належати до кількох класифікаційних груп</text>

  <text x="350" y="530" text-anchor="middle" font-size="11" fill="#888">Рис. 2. Багатокритеріальна класифікація організаційних форм навчання</text>
</svg>"""

SVG_DIAGRAM_3 = """<svg width="700" height="380" viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, serif" font-size="13">
  <rect x="1" y="1" width="698" height="378" fill="#ffffff" stroke="#333" stroke-width="1"/>
  <text x="350" y="30" text-anchor="middle" font-size="17" font-weight="bold">Співвідношення форм навчання</text>
  <text x="350" y="52" text-anchor="middle" font-size="12" fill="#555">за місцем у навчальному процесі</text>

  <rect x="40" y="80" width="620" height="270" rx="20" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="350" y="110" text-anchor="middle" font-size="14" font-weight="bold" fill="#0d47a1">Основна форма</text>
  <rect x="180" y="120" width="340" height="60" rx="10" fill="#bbdefb" stroke="#1565c0" stroke-width="2"/>
  <text x="350" y="155" text-anchor="middle" font-size="15" font-weight="bold" fill="#0d47a1">УРОК</text>

  <text x="350" y="210" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565c0">Додаткові форми</text>
  <rect x="80" y="225" width="130" height="45" rx="8" fill="#90caf9" stroke="#1565c0"/>
  <text x="145" y="252" text-anchor="middle" font-size="12">Екскурсія</text>
  <rect x="220" y="225" width="130" height="45" rx="8" fill="#90caf9" stroke="#1565c0"/>
  <text x="285" y="252" text-anchor="middle" font-size="12">Факультатив</text>
  <rect x="360" y="225" width="130" height="45" rx="8" fill="#90caf9" stroke="#1565c0"/>
  <text x="425" y="252" text-anchor="middle" font-size="12">Гурток</text>
  <rect x="500" y="225" width="130" height="45" rx="8" fill="#90caf9" stroke="#1565c0"/>
  <text x="565" y="252" text-anchor="middle" font-size="12">Проєкт</text>

  <text x="350" y="300" text-anchor="middle" font-size="13" font-weight="bold" fill="#0d47a1">Допоміжні форми</text>
  <rect x="130" y="310" width="130" height="35" rx="8" fill="#64b5f6" stroke="#1565c0"/>
  <text x="195" y="333" text-anchor="middle" font-size="12" fill="white">Консультація</text>
  <rect x="280" y="310" width="130" height="35" rx="8" fill="#64b5f6" stroke="#1565c0"/>
  <text x="345" y="333" text-anchor="middle" font-size="12" fill="white">Домашня робота</text>
  <rect x="430" y="310" width="130" height="35" rx="8" fill="#64b5f6" stroke="#1565c0"/>
  <text x="495" y="333" text-anchor="middle" font-size="12" fill="white">Самостійна</text>

  <text x="350" y="370" text-anchor="middle" font-size="11" fill="#888">Рис. 3. Форми навчання за місцем у навчальному процесі</text>
</svg>"""

# ============================================================
# 4. НАПОВНЕННЯ ДОКУМЕНТА
# ============================================================

add_heading_custom('САМОСТІЙНА РОБОТА', level=1)
add_heading_custom('Тема: Форми організації навчання. Сутність організаційних форм навчання', level=2)

add_paragraph('Вид роботи: підготовка доповіді.', bold=True)
add_paragraph('Спеціальність: Вчитель інформатики початкової школи.', bold=True)
add_paragraph('Обсяг: до 30 хв самостійної роботи + оформлення доповіді.', bold=True)

add_heading_custom('МЕТА САМОСТІЙНОЇ РОБОТИ', level=2)
add_paragraph('навчальна: поглибити та систематизувати знання про сутність організаційних форм навчання, їх класифікацію та особливості застосування в початковій школі на уроках інформатики;')
add_paragraph('розвивальна: розвивати вміння самостійно опрацьовувати науково-педагогічну літературу, аналізувати й узагальнювати матеріал, готувати усну та письмову доповідь;')
add_paragraph('виховна: формувати професійну відповідальність, самостійність, критичне мислення майбутнього вчителя інформатики початкової школи.')
add_paragraph('Форма звітності: доповідь (письмовий текст обсягом 3–5 сторінок, підготовлений для усного виступу на 5–7 хв).', bold=True)

# ТЕОРЕТИЧНА ЧАСТИНА
add_heading_custom('ТЕОРЕТИЧНА ЧАСТИНА', level=1)

add_heading_custom('1. Поняття «форма організації навчання» та її сутність', level=2)
add_paragraph('У дидактиці форма організації навчання — це спосіб упорядкування навчальної діяльності, зовнішнє вираження узгодженої взаємодії вчителя й учнів, що здійснюється у визначеному порядку та режимі. Поняття «організаційна форма навчання» охоплює: склад учнів, місце й час навчання, послідовність видів роботи, характер керівництва з боку вчителя.')
add_paragraph('Сутність організаційних форм навчання полягає в тому, що вони впорядковують навчальний процес, забезпечують цілеспрямовану взаємодію учасників, уможливлюють реалізацію змісту, методів і засобів навчання. Форма виступає своєрідною «оболонкою» навчального процесу, яка визначає його структуру та динаміку.')
add_paragraph('Ключові ознаки організаційної форми навчання:')
add_paragraph('1. Просторово-часова визначеність (де і коли відбувається навчання).')
add_paragraph('2. Склад учасників (хто навчається і хто навчає).')
add_paragraph('3. Порядок і режим діяльності (як організовано взаємодію).')
add_paragraph('4. Характер керівництва навчально-пізнавальною діяльністю.')
add_paragraph('5. Ступінь самостійності учнів.')
add_paragraph('На рис. 1 подано структурно-логічну схему сутності організаційної форми навчання.')
add_svg_image(SVG_DIAGRAM_1, width_inches=6.0, caption='Рис. 1. Структурно-логічна схема сутності форми організації навчання')

add_heading_custom('2. Історичний розвиток форм організації навчання', level=2)
add_paragraph('Форми організації навчання історично змінювалися разом із розвитком суспільства та педагогічної думки. У педагогічній науці виокремлюють такі історичні системи: індивідуальне навчання (до XVII ст.) — робота вчителя з одним учнем; індивідуально-групове навчання — учитель працює з групою учнів різного віку; класно-урочна система (Я. А. Коменський, XVII ст.) — учні одного віку об’єднуються в клас, навчання проводиться за єдиним розкладом; белль-ланкастерська система — старші учні навчають молодших; мангеймська система — розподіл класів за здібностями; дальтон-план — індивідуалізоване навчання за завданнями; бригадно-лабораторна система — поєднання колективної та індивідуальної роботи.')
add_paragraph('Сучасна школа ґрунтується на класно-урочній системі, яка доповнюється іншими формами (екскурсії, гуртки, факультативи, самостійна робота, проєктна діяльність).')

add_heading_custom('3. Класифікація організаційних форм навчання', level=2)
add_paragraph('Класифікацію форм організації навчання здійснюють за різними ознаками. Найпоширеніші підходи:')
add_paragraph('1. За кількістю учнів (індивідуальна, парна, групова, фронтальна, колективна).')
add_paragraph('2. За місцем проведення (у класі, у комп’ютерному кабінеті, на природі, в музеї).')
add_paragraph('3. За тривалістю (урок, спарений урок, факультатив, гурток, екскурсія).')
add_paragraph('4. За дидактичною метою (урок засвоєння нових знань, комбінований, узагальнення, контрольний, нестандартний).')
add_paragraph('5. За ступенем самостійності (під керівництвом учителя, самостійна робота, самопідготовка).')
add_paragraph('6. За змістом (предметні, міжпредметні, інтегровані).')
add_paragraph('На рис. 2 подано багатокритеріальну класифікацію організаційних форм навчання.')
add_svg_image(SVG_DIAGRAM_2, width_inches=6.0, caption='Рис. 2. Багатокритеріальна класифікація організаційних форм навчання')

add_heading_custom('4. Урок як основна організаційна форма навчання', level=2)
add_paragraph('У сучасній школі урок залишається основною формою організації навчання. Його характерні ознаки: постійний склад учнів, єдиний час і місце, керівна роль учителя, чітка структура, обмежена тривалість (у початковій школі — 35–40 хв).')
add_paragraph('Сутнісні риси уроку:')
add_paragraph('1. Наявність дидактичної мети (навчальної, розвивальної, виховної).')
add_paragraph('2. Організаційна чіткість і структурна завершеність.')
add_paragraph('3. Керівництво з боку вчителя при активній пізнавальній діяльності учнів.')
add_paragraph('4. Поєднання фронтальної, групової та індивідуальної роботи.')
add_paragraph('5. Раціональне використання часу та засобів навчання.')

add_heading_custom('5. Інші форми організації навчання та їх сутність', level=2)
add_paragraph('Окрім уроку, виділяють такі організаційні форми: екскурсія — навчання в умовах безпосереднього спостереження об’єктів; домашня навчальна робота — самостійне опрацювання матеріалу; факультатив — поглиблене вивчення окремих тем; гурток — позакласна робота за інтересами; консультація — індивідуальна або групова допомога вчителя; навчальний проєкт — дослідницька діяльність учнів; самостійна робота — діяльність без безпосереднього керівництва вчителя.')
add_paragraph('На рис. 3 подано співвідношення форм навчання за місцем у навчальному процесі.')
add_svg_image(SVG_DIAGRAM_3, width_inches=6.0, caption='Рис. 3. Форми навчання за місцем у навчальному процесі')

add_heading_custom('6. Сутність організаційних форм навчання інформатики в початковій школі', level=2)
add_paragraph('Для початкової школи сутність організаційних форм навчання інформатики визначається такими чинниками:')
add_paragraph('1. Вікові особливості молодших школярів — переважання наочно-образного мислення, мимовільна увага, швидка втомлюваність, потреба в частій зміні діяльності та грі.')
add_paragraph('2. Санітарно-гігієнічні норми — обмеження безперервної роботи за комп’ютером (до 15 хв), необхідність фізкультхвилинок і вправ для очей.')
add_paragraph('3. Подвійна природа уроку інформатики — поєднання безкомп’ютерної (теоретичної) та комп’ютерної (практичної) частин.')
add_paragraph('4. Поділ класу на групи у комп’ютерному кабінеті (за кількістю робочих місць).')
add_paragraph('5. Урізноманітнення форм — використання гри, казки, подорожі, проєкту, змагання як організаційних оболонок уроку.')
add_paragraph('Отже, сутність організаційних форм навчання в початковій школі полягає в забезпеченні оптимального поєднання колективної, групової, парної та індивідуальної роботи з урахуванням вікових можливостей дітей та специфіки предмета «Інформатика».')

add_heading_custom('7. Висновки до теоретичної частини', level=2)
add_paragraph('Організаційна форма навчання — це дидактична категорія, що виражає зовнішню впорядкованість навчального процесу. Сутність форм організації навчання полягає у забезпеченні цілеспрямованої, структурованої та керованої взаємодії вчителя й учнів. Для початкової школи особливо важливим є урізноманітнення форм, їх відповідність віковим особливостям дітей та санітарно-гігієнічним нормам.')

# ПРАКТИЧНА ЧАСТИНА
add_heading_custom('ПРАКТИЧНА ЧАСТИНА: РІЗНОРІВНЕВЕ ЗАВДАННЯ ДЛЯ САМОСТІЙНОЇ РОБОТИ (до 30 хв)', level=1)
add_paragraph('Форма звітності: доповідь (3–5 сторінок письмового тексту, розрахована на усний виступ 5–7 хв).', bold=True)

add_heading_custom('Завдання 1. Репродуктивний рівень (10 хв)', level=3)
add_paragraph('Мета: перевірити розуміння базових понять теми.')
add_paragraph('Інструкція: дайте письмові відповіді на запитання (2–3 речення кожна), які стануть основою вступної частини доповіді:')
add_paragraph('1. Дайте визначення поняття «форма організації навчання».')
add_paragraph('2. Назвіть п’ять ключових ознак організаційної форми навчання.')
add_paragraph('3. Які функції виконує форма організації навчання?')
add_paragraph('4. Назвіть основну форму організації навчання в сучасній школі та охарактеризуйте її сутнісні риси.')
add_paragraph('Критерії оцінювання: точність і повнота відповідей (максимум 5 балів).')

add_heading_custom('Завдання 2. Конструктивний рівень (10 хв)', level=3)
add_paragraph('Мета: навчитися аналізувати та порівнювати організаційні форми навчання.')
add_paragraph('Інструкція: заповніть порівняльну таблицю «Історичні системи організації навчання» та підготуйте на її основі аналітичний абзац доповіді.')
add_table(
    ['Історична система', 'Автор / період', 'Основна ідея', 'Переваги', 'Недоліки'],
    [
        ['Індивідуальне навчання', '', '', '', ''],
        ['Індивідуально-групове', '', '', '', ''],
        ['Класно-урочна система', '', '', '', ''],
        ['Белль-ланкастерська', '', '', '', ''],
        ['Дальтон-план', '', '', '', ''],
    ],
    col_widths=[3.5, 3, 4, 3, 3]
)
add_paragraph('Критерії оцінювання: повнота та правильність заповнення таблиці, логічність аналітичного абзацу (максимум 6 балів).')

add_heading_custom('Завдання 3. Творчий рівень (10 хв)', level=3)
add_paragraph('Мета: розвивати вміння застосовувати теоретичні знання до практики початкової школи, готувати доповідь.')
add_paragraph('Інструкція: оберіть одну з тем для доповіді та підготуйте її письмовий текст (3–5 сторінок). У доповіді обов’язково:')
add_paragraph('— розкрийте сутність обраної форми навчання;')
add_paragraph('— наведіть приклади застосування на уроках інформатики в початковій школі;')
add_paragraph('— вкажіть переваги та можливі труднощі;')
add_paragraph('— зробіть висновки.')
add_paragraph('Орієнтовні теми доповідей:', bold=True)
topics = [
    'Сутність класно-урочної системи навчання та її значення для початкової школи.',
    'Групова форма навчання на уроках інформатики в початкових класах: сутність і методика.',
    'Індивідуальна форма навчання інформатики в початковій школі.',
    'Парна робота як ефективна форма навчання молодших школярів інформатики.',
    'Нестандартні форми уроку інформатики в початковій школі (урок-гра, урок-подорож, урок-казка).',
    'Екскурсія як форма організації навчання інформатики в початковій школі.',
    'Проєктна діяльність як організаційна форма навчання інформатики в початкових класах.',
    'Сутність і особливості самостійної роботи молодших школярів з інформатики.',
    'Історичний розвиток організаційних форм навчання та їх відображення в сучасній початковій школі.',
    'Санітарно-гігієнічні вимоги до організаційних форм навчання інформатики в початковій школі.',
]
for i, t in enumerate(topics, 1):
    add_paragraph(f'{i}. {t}')
add_paragraph('Структура доповіді: вступ (актуальність, мета); основна частина (сутність питання, приклади, аналіз); висновки; список використаних джерел (2–3 позиції).')
add_paragraph('Критерії оцінювання: повнота розкриття теми, логічність викладу, наявність прикладів з практики початкової школи, самостійність, оформлення (максимум 9 балів).')

# КОНТРОЛЬНІ ЗАПИТАННЯ
add_heading_custom('КОНТРОЛЬНІ ЗАПИТАННЯ', level=1)
questions = [
    'Дайте визначення поняття «форма організації навчання». Які два значення має поняття «форма» у дидактиці?',
    'У чому полягає сутність організаційної форми навчання?',
    'Назвіть і охарактеризуйте ключові ознаки організаційної форми навчання.',
    'Які функції виконує форма організації навчання?',
    'Охарактеризуйте історичні системи організації навчання: індивідуальне, індивідуально-групове, класно-урочне.',
    'У чому полягають переваги та недоліки класно-урочної системи?',
    'За якими критеріями класифікують організаційні форми навчання?',
    'Які форми навчання належать до основних, додаткових і допоміжних? Наведіть приклади.',
    'У чому полягає сутність уроку як основної форми організації навчання?',
    'Які чинники визначають сутність організаційних форм навчання інформатики в початковій школі?',
    'Чому в початковій школі доцільно урізноманітнювати форми організації навчання інформатики?',
    'Як санітарно-гігієнічні вимоги впливають на вибір форм організації навчання інформатики молодших школярів?',
]
for i, q in enumerate(questions, 1):
    add_paragraph(f'{i}. {q}')

# ============================================================
# 5. ЗБЕРЕЖЕННЯ
# ============================================================

output_file = 'samostiyna_robota_formy_orhanizatsii_navchannya.docx'
doc.save(output_file)
print(f'Документ збережено: {output_file}')