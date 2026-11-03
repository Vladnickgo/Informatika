import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def create_methodical_recommendations():
    # 1. Створення документа
    doc = Document()

    # 2. Налаштування полів сторінки (стандарт: ліве 3 см, праве 1.5 см, верхнє і нижнє 2 см)
    section = doc.sections[0]
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(1.5)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)

    # 3. Допоміжна функція для застосування стилів до абзацу
    def set_base_style(paragraph, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=True, bold=False):
        paragraph.alignment = align
        paragraph.paragraph_format.line_spacing = 1.25
        if indent:
            paragraph.paragraph_format.first_line_indent = Cm(1.25)
        else:
            paragraph.paragraph_format.first_line_indent = Cm(0)
        
        for run in paragraph.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(14)
            run.bold = bold
            # Примусове встановлення шрифту для коректного відображення кирилиці в Word
            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    # 4. Допоміжна функція для заголовків
    def add_heading(text, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, space_after=12):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.bold = bold
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
        return p

    # ================= ТИТУЛЬНА СТОРІНКА =================
    add_heading("КЗСОР «Путивльський педагогічний фаховий коледж імені С.В. Руднєва»", space_after=24)
    add_heading("Методичні рекомендації\nщодо виконання самостійної роботи\nз навчальної дисципліни", space_after=24)
    add_heading("«Інформатика та методика її навчання»", space_after=36)
    add_heading("галузь знань: 01 Освіта\nспеціальність: 013 Початкова освіта", space_after=48)
    add_heading("Укладач: викладач інформатики", space_after=12)
    add_heading("м. Путивль, 2024", space_after=0) # Рік виправлено на актуальний за зразком
    
    doc.add_page_break()

    # ================= ЗМІСТ =================
    add_heading("ЗМІСТ", align=WD_ALIGN_PARAGRAPH.CENTER)
    
    toc_items = [
        "1. Загальні методичні рекомендації з виконання самостійної роботи студента",
        "2. Тематика самостійної роботи",
        "3. Зміст самостійної роботи студента і методичні рекомендації щодо її виконання",
        "   Тема: Покадрова анімація. Анімація на основі фотоколажу.",
        "4. Критерії оцінювання навчальних досягнень здобувачів освіти"
    ]
    for item in toc_items:
        p = doc.add_paragraph(item)
        set_base_style(p, align=WD_ALIGN_PARAGRAPH.LEFT, indent=True)

    doc.add_page_break()

    # ================= РОЗДІЛ 3: ЗМІСТ САМОСТІЙНОЇ РОБОТИ =================
    add_heading("3. ЗМІСТ САМОСТІЙНОЇ РОБОТИ СТУДЕНТА І МЕТОДИЧНІ РЕКОМЕНДАЦІЇ ЩОДО ЇЇ ВИКОНАННЯ", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)

    # Тема
    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("Тема: ").bold = True
    p.add_run("Покадрова анімація. Анімація на основі фотоколажу.")

    # Мета
    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("Мета: ").bold = True
    p.add_run("\n- Формувати практичні навички створення покадрової анімації на основі заздалегідь створеного фотоколажу, редагуючи часові проміжки та візуальний вміст окремих кадрів.\n- Розвивати спостережливість та уяву, моделюючи поведінку складених колажних об’єктів у часі та просторі анімаційного ролика.\n- Виховувати креативність та емоційну виразність, створюючи анімовані історії, які викликають позитивні емоції у глядача.")

    # План
    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("План:").bold = True
    p.add_run("\n1. Теоретичні основи покадрової анімації та анімації на основі фотоколажу.\n2. Алгоритм створення анімації: планування, створення кадрів, об'єднання в GIF.\n3. Виконання практичного завдання зі створення навчальної анімації.\n4. Оформлення звіту у вигляді презентації та самоперевірка.")

    # Література
    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("Література:").bold = True
    p.add_run("\n1. Потієнко В. О. Графічний дизайн : рівень стандарту (вибірковий модуль для 10–11 кл). Харків : Ранок, 2020. 160 с.\n2. Речич Н. В. Вебтехнології : рівень стандарту (вибірковий модуль для 10–11 кл.). Харків : Ранок, 2020. 160 с.\n3. Мирошниченко В. О. Використання сучасних інформаційних технологій: формування мультимедійної компетентності. Київ : Центр учбової літератури, 2022. 296 с.")

    # Знання та вміння
    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("Перелік знань та вмінь, які набудуть студенти:").bold = True
    p.add_run("\n- Знати: принцип роботи покадрової анімації, переваги використання фотоколажу в навчальному процесі, базовий алгоритм створення GIF-анімації.\n- Вміти: планувати етапи анімаційного процесу, створювати та компонувати графічні кадри в редакторі, об'єднувати кадри в анімаційний файл, оптимізувати графічні файли для веб-середовища, оформлювати результати роботи у вигляді структурованої презентації.")

    doc.add_paragraph() # Порожній абзац для відступу

    # Завдання
    add_heading("Конкретні завдання та методичні поради щодо їх виконання", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)

    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("Завдання 1. Опрацювання теоретичного матеріалу.").bold = True
    p.add_run(" Методична порада: уважно ознайомтеся з визначенням покадрової анімації та її відмінністю від інших видів анімації. Проаналізуйте наведені приклади використання фотоколажу в педагогічній діяльності. Зверніть увагу на оптимальні параметри швидкості зміни кадрів (70–100 сотих секунди) для навчального контенту.")

    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("Завдання 2. Виконання практичного завдання.").bold = True
    p.add_run(" Тема: «Створення навчальної анімації \"Кругообіг води в природі\" / \"Ріст рослини\" / \"Зміна пір року\"». Методична порада: дотримуйтесь алгоритму з 3-х кроків: 1) Планування: розбийте процес на 4–6 ключових етапів. Створіть основу однакового розміру в Canva або GIMP. 2) Об'єднання: завантажте кадри на ezgif.com/maker, встановіть час затримки, змініть порядок за потреби та експортуйте у GIF. 3) Оптимізація: перевірте файл у браузері. Якщо розмір перевищує 10–15 МБ, використайте ezgif.com/optimize для стиснення. Використовуйте безкоштовні зображення з Pixabay, Unsplash або Freepik.")

    p = doc.add_paragraph()
    set_base_style(p)
    p.add_run("Завдання 3. Оформлення звіту.").bold = True
    p.add_run(" Формат: презентація (5–6 слайдів). Методична порада: дотримуйтесь єдиного стилю оформлення, перевірте грамотність тексту та читабельність зображень. Обов'язково вкажіть посилання на використані ресурси. Структура: 1) Титульний слайд; 2) Теоретичні відомості; 3) Алгоритм створення; 4) Кадри колажу (скріншоти 4-6 кадрів); 5) Готова анімація (скріншот або GIF + посилання); 6) Висновки (як використати на уроці, для якого класу/предмета).")

    doc.add_paragraph()

    # Питання для самоконтролю
    add_heading("Питання для самоконтролю", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)
    questions = [
        "1. У чому полягає основний принцип покадрової анімації та яка оптимальна швидкість зміни кадрів для сприйняття людським оком?",
        "2. Які три головні переваги має використання анімації на основі фотоколажу в педагогічній діяльності?",
        "3. Які етапи включає алгоритм створення анімації на основі фотоколажу?",
        "4. Які онлайн-інструменти та ресурси можна використати для створення, об'єднання та оптимізації GIF-анімації?",
        "5. Які вимоги висуваються до структури та оформлення звіту (презентації) про виконання самостійної роботи?"
    ]
    for q in questions:
        p = doc.add_paragraph(q)
        set_base_style(p)

    doc.add_paragraph()

    # ================= КРИТЕРІЇ ОЦІНЮВАННЯ (ТАБЛИЦЯ) =================
    add_heading("4. КРИТЕРІЇ ОЦІНЮВАННЯ НАВЧАЛЬНИХ ДОСЯГНЕНЬ ЗДОБУВАЧІВ ОСВІТИ", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=12)
    
    p = doc.add_paragraph("Оцінювання виконання самостійної роботи № 5 здійснюється за 25-бальною шкалою згідно з наступними критеріями:")
    set_base_style(p)

    # Дані для таблиці
    table_data = [
        ["Критерій оцінювання", "Бали"],
        ["Повнота розкриття теоретичної частини", "3"],
        ["Наявність та якість покрокового алгоритму (слайд 3)", "4"],
        ["Кількість та якість створених кадрів (не менше 4)", "5"],
        ["Якість колажу (композиція, єдиний стиль, читабельність тексту)", "5"],
        ["Відповідність анімації навчальній темі", "3"],
        ["Оформлення презентації (єдиний стиль, грамотність)", "3"],
        ["Висновки та практична цінність", "2"],
        ["Максимальна кількість балів", "25"]
    ]

    table = doc.add_table(rows=len(table_data), cols=2)
    table.style = 'Table Grid'

    for i, row_data in enumerate(table_data):
        for j, cell_text in enumerate(row_data):
            cell = table.cell(i, j)
            cell.text = cell_text
            
            # Форматування тексту в комірках таблиці
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else (WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER)
                paragraph.paragraph_format.line_spacing = 1.25
                for run in paragraph.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(14)
                    run.bold = (i == 0 or i == len(table_data) - 1)
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    # Збереження файлу в поточній активній директорії
    file_name = "Самостійна_робота_5_Покадрова_анімація.docx"
    doc.save(file_name)
    
    # Виведення повного шляху для впевненості
    current_dir = os.getcwd()
    print(f"✅ Документ успішно створено!")
    print(f"📁 Шлях збереження: {current_dir}\\{file_name}")

if __name__ == "__main__":
    create_methodical_recommendations()