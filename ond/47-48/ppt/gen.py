import os
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE

# --- КОЛЬОРОВА ПАЛІТРА ---
COLOR_DARK_BLUE = RGBColor(31, 78, 121)
COLOR_ORANGE = RGBColor(237, 125, 49)
COLOR_GREEN = RGBColor(44, 160, 44)
COLOR_LIGHT_GRAY = RGBColor(242, 242, 242)
COLOR_TEXT_DARK = RGBColor(50, 50, 50)
COLOR_WHITE = RGBColor(255, 255, 255)

# --- ДОПОМІЖНІ ФУНКЦІЇ ---
def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_title(slide, text, color=COLOR_DARK_BLUE):
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = color
    p.font.name = 'Arial'
    return txBox

def add_bullet_text(slide, text, left, top, width, height, font_size=20, color=COLOR_TEXT_DARK):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.name = 'Arial'
    return txBox

def create_chart():
    """Створює діаграму за допомогою matplotlib"""
    fig, ax = plt.subplots(figsize=(6, 4))
    categories = ['Високий', 'Середній', 'Низький']
    before = [20, 45, 35]
    after = [45, 40, 15]
    
    x = range(len(categories))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], before, width, label='До', color='#ED7D31')
    ax.bar([i + width/2 for i in x], after, width, label='Після', color='#2CA02C')
    
    ax.set_ylabel('Відсотки (%)', fontsize=12)
    ax.set_title('Динаміка рівнів сформованості', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    chart_path = 'chart_temp.png'
    plt.savefig(chart_path, dpi=150)
    plt.close()
    return chart_path

# --- СТВОРЕННЯ ПРЕЗЕНТАЦІЇ ---
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Слайд 1: Титульний
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide, COLOR_DARK_BLUE)
add_title(slide, "Формулювання висновків.\nУзагальнення результатів,\nрозробка рекомендацій", COLOR_WHITE)
add_bullet_text(slide, "Практичне заняття № 8", 0.5, 5.5, 9, 0.5, 24, COLOR_ORANGE)

# Слайд 2: Піраміда узагальнення
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Піраміда узагальнення результатів")

# Малювання піраміди за допомогою фігур
# Рівень 1: Результати (Основа)
shape = slide.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Inches(1.5), Inches(6), Inches(7), Inches(1))
shape.fill.solid()
shape.fill.fore_color.rgb = COLOR_ORANGE
shape.line.color.rgb = COLOR_WHITE
tf = shape.text_frame
tf.text = "РЕЗУЛЬТАТИ ДОСЛІДЖЕННЯ (емпіричні дані, факти)"
tf.paragraphs[0].font.color.rgb = COLOR_WHITE
tf.paragraphs[0].font.bold = True

# Рівень 2: Узагальнення
shape = slide.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Inches(2.2), Inches(4.8), Inches(5.6), Inches(1.1))
shape.fill.solid()
shape.fill.fore_color.rgb = COLOR_GREEN
shape.line.color.rgb = COLOR_WHITE
tf = shape.text_frame
tf.text = "УЗАГАЛЬНЕННЯ (закономірності, тенденції)"
tf.paragraphs[0].font.color.rgb = COLOR_WHITE
tf.paragraphs[0].font.bold = True

# Рівень 3: Висновки
shape = slide.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Inches(3.2), Inches(3.6), Inches(3.6), Inches(1.1))
shape.fill.solid()
shape.fill.fore_color.rgb = COLOR_DARK_BLUE
shape.line.color.rgb = COLOR_WHITE
tf = shape.text_frame
tf.text = "ВИСНОВКИ (узагальнені положення)"
tf.paragraphs[0].font.color.rgb = COLOR_WHITE
tf.paragraphs[0].font.bold = True

# Рівень 4: Рекомендації
shape = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(3.75), Inches(2.2), Inches(2.5), Inches(1.4))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(11, 42, 72)
shape.line.color.rgb = COLOR_WHITE
tf = shape.text_frame
tf.text = "РЕКОМЕНДАЦІЇ"
tf.paragraphs[0].font.color.rgb = COLOR_WHITE
tf.paragraphs[0].font.bold = True

add_bullet_text(slide, "Від конкретних фактів → через узагальнення → до обґрунтованих порад", 1, 1.5, 8, 0.5, 18, COLOR_TEXT_DARK)

# Слайд 3: Структура наукового висновку
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Структура наукового висновку")

components = [
    ("1. ТВЕРДЖЕННЯ", "що саме встановлено", COLOR_DARK_BLUE),
    ("2. ОБҐРУНТУВАННЯ", "на основі яких даних", COLOR_GREEN),
    ("3. ПОЯСНЕННЯ", "чому саме так", COLOR_ORANGE),
    ("4. ЗНАЧЕННЯ", "для теорії та практики", RGBColor(112, 48, 160))
]

for i, (title, desc, color) in enumerate(components):
    left = 0.5 + i * 2.3
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(2), Inches(2.1), Inches(2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = COLOR_WHITE
    
    tf = shape.text_frame
    tf.text = title
    tf.paragraphs[0].font.color.rgb = COLOR_WHITE
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(16)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.color.rgb = COLOR_WHITE
    p.font.size = Pt(14)

# Приклад
add_bullet_text(slide, "Приклад: «Встановлено, що систематичне використання дидактичних ігор підвищує пізнавальний інтерес молодших школярів на 25 % (на основі порівняння констатувального й контрольного зрізів), що має значення для методики...»", 0.5, 4.5, 9, 2, 18, COLOR_TEXT_DARK)

# Слайд 4: Типи висновків
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Типи висновків у науково-педагогічному дослідженні")

types = [
    ("Теоретичні", "Узагальнення наукових положень,\nуточнення понять", COLOR_DARK_BLUE),
    ("Емпіричні", "Узагальнення отриманих даних,\nвиявлені тенденції", COLOR_GREEN),
    ("Практичні", "Рекомендації для вчителів,\nучнів, батьків", COLOR_ORANGE)
]

for i, (title, desc, color) in enumerate(types):
    left = 0.5 + i * 3.2
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(2), Inches(2.8), Inches(2.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_LIGHT_GRAY
    shape.line.color.rgb = color
    shape.line.width = Pt(3)
    
    tf = shape.text_frame
    tf.text = title
    tf.paragraphs[0].font.color.rgb = color
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(20)
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.color.rgb = COLOR_TEXT_DARK
    p.font.size = Pt(16)

add_bullet_text(slide, "Загальна структура розділу «Висновки»:\n1) загальний підсумок;\n2) конкретні результати за кожним завданням;\n3) підтвердження / спростування гіпотези.", 1, 5, 8, 1.5, 18, COLOR_TEXT_DARK)

# Слайд 5: Рекомендації (Адресати)
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Розробка рекомендацій")

# Центральний вузол
center_shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(4), Inches(2.8), Inches(2), Inches(2))
center_shape.fill.solid()
center_shape.fill.fore_color.rgb = COLOR_DARK_BLUE
center_shape.line.color.rgb = COLOR_WHITE
tf = center_shape.text_frame
tf.text = "РЕКОМЕНДАЦІЇ\nза результатами"
tf.paragraphs[0].font.color.rgb = COLOR_WHITE
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.size = Pt(14)

# Адресати
audiences = [
    ("Вчителям початкових класів", 3.5, 1),
    ("Учням початкової школи", 7, 2),
    ("Батькам молодших школярів", 7, 4.5),
    ("Адміністрації школи", 3.5, 5.5),
    ("Методичним об'єднанням", 0.5, 4.5),
    ("Авторам програм", 0.5, 2)
]

for text, left, top in audiences:
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(2.5), Inches(0.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_LIGHT_GRAY
    shape.line.color.rgb = COLOR_ORANGE
    tf = shape.text_frame
    tf.text = text
    tf.paragraphs[0].font.color.rgb = COLOR_TEXT_DARK
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

# Слайд 6: Вимоги до презентації (Візуалізація правил)
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Вимоги до підсумкової презентації")

rules = [
    ("10–12 слайдів", "Структура"),
    ("7–10 хвилин", "Час виступу"),
    ("Макс. 6 рядків", "Текст на слайді"),
    ("1 візуальний об'єкт", "Діаграма/схема"),
    ("Шрифт ≥ 20 pt", "Читабельність"),
    ("Мінімум тексту", "Максимум наочності")
]

for i, (title, desc) in enumerate(rules):
    row = i // 3
    col = i % 3
    left = 0.5 + col * 3.2
    top = 2 + row * 2
    
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(2.8), Inches(1.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_DARK_BLUE if i % 2 == 0 else COLOR_GREEN
    shape.line.color.rgb = COLOR_WHITE
    
    tf = shape.text_frame
    tf.text = title
    tf.paragraphs[0].font.color.rgb = COLOR_WHITE
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    p = tf.add_paragraph()
    p.text = desc
    p.font.color.rgb = COLOR_WHITE
    p.font.size = Pt(14)
    p.alignment = PP_ALIGN.CENTER

# Слайд 7: Структура презентації (Сітка)
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Структура презентації (10–12 слайдів)")

slides_content = [
    "1. Титульний", "2. Актуальність", "3. Об'єкт, предмет",
    "4. Методи", "5. Гіпотеза", "6. Огляд джерел",
    "7. Методика", "8. Результати", "9. Інтерпретація",
    "10. Висновки", "11. Рекомендації", "12. Дякую"
]

for i, text in enumerate(slides_content):
    row = i // 4
    col = i % 4
    left = 0.5 + col * 2.3
    top = 2 + row * 1.5
    
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(2.1), Inches(1.2))
    shape.fill.solid()
    if i < 5:
        shape.fill.fore_color.rgb = COLOR_DARK_BLUE
    elif i < 10:
        shape.fill.fore_color.rgb = COLOR_GREEN
    else:
        shape.fill.fore_color.rgb = COLOR_ORANGE
        
    shape.line.color.rgb = COLOR_WHITE
    tf = shape.text_frame
    tf.text = text
    tf.paragraphs[0].font.color.rgb = COLOR_WHITE
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

# Слайд 8: Приклад слайда з результатами (Діаграма)
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Приклад слайда з результатами")

# Генерація та вставка діаграми
chart_path = create_chart()
slide.shapes.add_picture(chart_path, Inches(0.5), Inches(2), width=Inches(5.5))

# Висновок за слайдом (текст доповнює зображення)
conclusion_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5), Inches(2), Inches(3), Inches(4.5))
conclusion_box.fill.solid()
conclusion_box.fill.fore_color.rgb = RGBColor(255, 242, 204) # Світло-жовтий
conclusion_box.line.color.rgb = COLOR_ORANGE

tf = conclusion_box.text_frame
tf.text = "Висновок за слайдом:"
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.size = Pt(18)
tf.paragraphs[0].font.color.rgb = COLOR_ORANGE

bullets = [
    "Високий рівень зріс на 25%",
    "Низький рівень знизився",
    "Відмінності статистично значущі (p<0.05)",
    "Порівняння з теорією: узгоджується з працями (Автор, рік)"
]
for b in bullets:
    p = tf.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_TEXT_DARK
    p.space_after = Pt(10)

# Слайд 9: Завершення
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide, COLOR_DARK_BLUE)
add_title(slide, "Дякую за увагу!", COLOR_WHITE)
add_bullet_text(slide, "Питання та обговорення", 0.5, 3.5, 9, 0.5, 24, COLOR_ORANGE)

# Збереження
prs.save('PZ8_Presentation.pptx')
print("Презентацію успішно створено: PZ8_Presentation.pptx")

# Видалення тимчасового файлу діаграми
if os.path.exists('chart_temp.png'):
    os.remove('chart_temp.png')
    