# -*- coding: utf-8 -*-
"""
Генерація презентації до практичного заняття
«Методи та форми роботи на уроках інформатики в початковій школі»
Формат: 16:9, шрифт Times New Roman, єдиний дизайн.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import cairosvg
import io

# ============================================================
# 1. КОЛЬОРОВА ПАЛІТРА
# ============================================================
DARK        = RGBColor(0x1F, 0x29, 0x37)
NAVY        = RGBColor(0x1E, 0x3A, 0x8A)
PRIMARY     = RGBColor(0x1E, 0x40, 0xAF)
BLUE        = RGBColor(0x3B, 0x82, 0xF6)
LIGHT_BLUE  = RGBColor(0xDB, 0xEA, 0xFE)
TEAL        = RGBColor(0x08, 0x91, 0xB2)
LIGHT_TEAL  = RGBColor(0xCF, 0xF2, 0xF7)
GREEN       = RGBColor(0x05, 0x96, 0x69)
LIGHT_GREEN = RGBColor(0xD1, 0xFA, 0xE5)
ORANGE      = RGBColor(0xEA, 0x58, 0x0C)
LIGHT_ORANGE= RGBColor(0xFE, 0xE7, 0xD9)
PURPLE      = RGBColor(0x7C, 0x3A, 0xED)
LIGHT_PURPLE= RGBColor(0xED, 0xE9, 0xFE)
ROSE        = RGBColor(0xE1, 0x1D, 0x48)
AMBER       = RGBColor(0xF5, 0x9E, 0x0B)
LIGHT_AMBER = RGBColor(0xFE, 0xF3, 0xC7)
GRAY        = RGBColor(0x6B, 0x72, 0x80)
LGRAY       = RGBColor(0xE5, 0xE7, 0xEB)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
CREAM       = RGBColor(0xFF, 0xFB, 0xF0)

FONT = 'Times New Roman'

# ============================================================
# 2. НАЛАШТУВАННЯ ПРЕЗЕНТАЦІЇ
# ============================================================
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height

# ============================================================
# 3. ДОПОМІЖНІ ФУНКЦІЇ
# ============================================================
def new_slide():
    return prs.slides.add_slide(prs.slide_layouts[6])

def add_bg(slide, color=WHITE):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.fill.solid(); bg.fill.fore_color.rgb = color; bg.line.fill.background()
    sp = bg._element; sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)
    return bg

def add_rect(slide, l, t, w, h, color, shape=MSO_SHAPE.RECTANGLE, line_color=None):
    sh = slide.shapes.add_shape(shape, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color; sh.line.width = Pt(1)
    return sh

def add_text(slide, l, t, w, h, text, size=18, bold=False, italic=False,
             color=DARK, align=PP_ALIGN.LEFT, font=FONT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = Pt(2); tf.margin_right = Pt(2)
    tf.margin_top = Pt(2);  tf.margin_bottom = Pt(2)
    lines = text.split('\n') if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = line
        r.font.name = font; r.font.size = Pt(size); r.font.bold = bold
        r.font.italic = italic; r.font.color.rgb = color
    return tb

def add_bullets(slide, l, t, w, h, items, size=16, color=DARK,
                bullet_color=PRIMARY, spacing=6, line_spacing=1.15):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = Pt(4)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(spacing); p.line_spacing = line_spacing
        r1 = p.add_run(); r1.text = '▪  '
        r1.font.name = FONT; r1.font.size = Pt(size)
        r1.font.color.rgb = bullet_color; r1.font.bold = True
        r2 = p.add_run(); r2.text = item
        r2.font.name = FONT; r2.font.size = Pt(size); r2.font.color.rgb = color
    return tb

def add_svg(slide, svg_str, left, top, width=None):
    png = cairosvg.svg2png(bytestring=svg_str.encode('utf-8'), scale=2)
    stream = io.BytesIO(png)
    if width:
        return slide.shapes.add_picture(stream, left, top, width=width)
    return slide.shapes.add_picture(stream, left, top)

def add_header(slide, title, accent=PRIMARY):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.2), Inches(1.15))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent; bar.line.fill.background()
    add_text(slide, Inches(0.45), Inches(0.25), Inches(12.5), Inches(0.7),
             title, size=30, bold=True, color=DARK)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(0.45), Inches(1.0), Inches(1.2), Inches(0.05))
    line.fill.solid(); line.fill.fore_color.rgb = accent; line.line.fill.background()

def add_footer(slide, page_num):
    add_text(slide, Inches(0.45), Inches(7.15), Inches(11), Inches(0.3),
             'Методи та форми роботи на уроках інформатики в початковій школі',
             size=10, color=GRAY, italic=True)
    add_text(slide, Inches(12), Inches(7.15), Inches(1), Inches(0.3),
             str(page_num), size=10, color=GRAY, align=PP_ALIGN.RIGHT)

def add_card(slide, l, t, w, h, title, body, accent=PRIMARY, bg=WHITE, title_size=19):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    card.fill.solid(); card.fill.fore_color.rgb = bg
    card.line.color.rgb = LGRAY; card.line.width = Pt(1)
    card.adjustments[0] = 0.05
    strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, Inches(0.12))
    strip.fill.solid(); strip.fill.fore_color.rgb = accent
    strip.line.fill.background(); strip.adjustments[0] = 0.5
    add_text(slide, l + Inches(0.2), t + Inches(0.28),
             w - Inches(0.4), Inches(0.5), title, size=title_size, bold=True, color=accent)
    add_text(slide, l + Inches(0.2), t + Inches(0.85),
             w - Inches(0.4), h - Inches(1.0), body, size=13, color=DARK)

def add_pill(slide, l, t, w, h, text, bg, fg=WHITE, size=12, bold=True):
    p = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    p.fill.solid(); p.fill.fore_color.rgb = bg
    p.line.fill.background(); p.adjustments[0] = 0.5
    add_text(slide, l, t, w, h, text, size=size, bold=bold, color=fg,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ============================================================
# 4. SVG-ДІАГРАМИ
# ============================================================

SVG_METHODS = '''<svg viewBox="0 0 1200 700" xmlns="http://www.w3.org/2000/svg"
  font-family="Times New Roman, Liberation Serif, serif">
  <rect width="1200" height="700" fill="#FFFFFF"/>

  <!-- center -->
  <circle cx="600" cy="350" r="115" fill="#DBEAFE"/>
  <circle cx="600" cy="350" r="95" fill="#1E40AF"/>
  <text x="600" y="338" text-anchor="middle" fill="#FFFFFF" font-size="22" font-weight="bold">МЕТОДИ</text>
  <text x="600" y="365" text-anchor="middle" fill="#FFFFFF" font-size="22" font-weight="bold">НАВЧАННЯ</text>

  <!-- Словесні -->
  <line x1="510" y1="290" x2="345" y2="190" stroke="#3B82F6" stroke-width="4"/>
  <rect x="55" y="60" width="290" height="180" rx="16" fill="#EFF6FF" stroke="#3B82F6" stroke-width="3"/>
  <text x="200" y="98" text-anchor="middle" font-size="22" font-weight="bold" fill="#1E40AF">СЛОВЕСНІ</text>
  <text x="78" y="135" font-size="16" fill="#333">• Розповідь</text>
  <text x="78" y="168" font-size="16" fill="#333">• Бесіда</text>
  <text x="78" y="201" font-size="16" fill="#333">• Інструктаж</text>

  <!-- Наочні -->
  <line x1="690" y1="290" x2="855" y2="190" stroke="#0891B2" stroke-width="4"/>
  <rect x="855" y="60" width="290" height="180" rx="16" fill="#ECFEFF" stroke="#0891B2" stroke-width="3"/>
  <text x="1000" y="98" text-anchor="middle" font-size="22" font-weight="bold" fill="#0891B2">НАОЧНІ</text>
  <text x="878" y="135" font-size="16" fill="#333">• Демонстрація</text>
  <text x="878" y="168" font-size="16" fill="#333">• Спостереження</text>
  <text x="878" y="201" font-size="16" fill="#333">• Ілюстрації</text>

  <!-- Практичні -->
  <line x1="510" y1="410" x2="345" y2="510" stroke="#EA580C" stroke-width="4"/>
  <rect x="55" y="460" width="290" height="200" rx="16" fill="#FFF7ED" stroke="#EA580C" stroke-width="3"/>
  <text x="200" y="498" text-anchor="middle" font-size="22" font-weight="bold" fill="#EA580C">ПРАКТИЧНІ</text>
  <text x="78" y="535" font-size="15" fill="#333">• Вправи</text>
  <text x="78" y="568" font-size="15" fill="#333">• Графічні роботи</text>
  <text x="78" y="601" font-size="15" fill="#333">• Моделювання</text>
  <text x="78" y="634" font-size="15" fill="#333">• Проєктна діяльність</text>

  <!-- Ігрові -->
  <line x1="690" y1="410" x2="855" y2="510" stroke="#7C3AED" stroke-width="4"/>
  <rect x="855" y="460" width="290" height="200" rx="16" fill="#FAF5FF" stroke="#7C3AED" stroke-width="3"/>
  <text x="1000" y="498" text-anchor="middle" font-size="22" font-weight="bold" fill="#7C3AED">ІГРОВІ</text>
  <text x="878" y="535" font-size="15" fill="#333">• Дидактичні ігри</text>
  <text x="878" y="568" font-size="15" fill="#333">• Сюжетно-рольові</text>
  <text x="878" y="601" font-size="15" fill="#333">• Комп’ютерні ігри</text>
</svg>'''

SVG_FORMS = '''<svg viewBox="0 0 1200 700" xmlns="http://www.w3.org/2000/svg"
  font-family="Times New Roman, Liberation Serif, serif">
  <rect width="1200" height="700" fill="#FFFFFF"/>

  <circle cx="600" cy="350" r="115" fill="#D1FAE5"/>
  <circle cx="600" cy="350" r="95" fill="#059669"/>
  <text x="600" y="338" text-anchor="middle" fill="#FFFFFF" font-size="22" font-weight="bold">ФОРМИ</text>
  <text x="600" y="365" text-anchor="middle" fill="#FFFFFF" font-size="22" font-weight="bold">РОБОТИ</text>

  <!-- Фронтальна -->
  <line x1="510" y1="290" x2="345" y2="190" stroke="#1E40AF" stroke-width="4"/>
  <rect x="55" y="60" width="290" height="180" rx="16" fill="#EFF6FF" stroke="#1E40AF" stroke-width="3"/>
  <text x="200" y="98" text-anchor="middle" font-size="20" font-weight="bold" fill="#1E40AF">ФРОНТАЛЬНА</text>
  <text x="78" y="135" font-size="14" fill="#333">Учитель → весь клас</text>
  <text x="78" y="165" font-size="14" fill="#555">• Вступ до теми</text>
  <text x="78" y="192" font-size="14" fill="#555">• Інструктаж</text>
  <text x="78" y="219" font-size="14" fill="#555">• Підсумок</text>

  <!-- Індивідуальна -->
  <line x1="690" y1="290" x2="855" y2="190" stroke="#EA580C" stroke-width="4"/>
  <rect x="855" y="60" width="290" height="180" rx="16" fill="#FFF7ED" stroke="#EA580C" stroke-width="3"/>
  <text x="1000" y="98" text-anchor="middle" font-size="19" font-weight="bold" fill="#EA580C">ІНДИВІДУАЛЬНА</text>
  <text x="878" y="135" font-size="14" fill="#333">Кожен у власному темпі</text>
  <text x="878" y="165" font-size="14" fill="#555">• Практичні навички</text>
  <text x="878" y="192" font-size="14" fill="#555">• Творчі завдання</text>
  <text x="878" y="219" font-size="14" fill="#555">• Контроль знань</text>

  <!-- Групова/парна -->
  <line x1="510" y1="410" x2="345" y2="510" stroke="#7C3AED" stroke-width="4"/>
  <rect x="55" y="460" width="290" height="200" rx="16" fill="#FAF5FF" stroke="#7C3AED" stroke-width="3"/>
  <text x="200" y="498" text-anchor="middle" font-size="19" font-weight="bold" fill="#7C3AED">ГРУПОВА / ПАРНА</text>
  <text x="78" y="533" font-size="14" fill="#333">2–4 особи</text>
  <text x="78" y="563" font-size="14" fill="#555">• Проєкти</text>
  <text x="78" y="590" font-size="14" fill="#555">• Складні завдання</text>
  <text x="78" y="617" font-size="14" fill="#555">• «Одна мишка — дві голови»</text>
  <text x="78" y="644" font-size="14" fill="#555">• Взаємоперевірка</text>

  <!-- Колективна -->
  <line x1="690" y1="410" x2="855" y2="510" stroke="#E11D48" stroke-width="4"/>
  <rect x="855" y="460" width="290" height="200" rx="16" fill="#FFF1F2" stroke="#E11D48" stroke-width="3"/>
  <text x="1000" y="498" text-anchor="middle" font-size="20" font-weight="bold" fill="#E11D48">КОЛЕКТИВНА</text>
  <text x="878" y="533" font-size="14" fill="#333">Командна взаємодія</text>
  <text x="878" y="563" font-size="14" fill="#555">• Вікторини</text>
  <text x="878" y="590" font-size="14" fill="#555">• Брейн-ринг</text>
  <text x="878" y="617" font-size="14" fill="#555">• Конкурси</text>
  <text x="878" y="644" font-size="14" fill="#555">• Змагання</text>
</svg>'''

SVG_ALGO_FLOW = '''<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg"
  font-family="Times New Roman, Liberation Serif, serif">
  <rect width="1200" height="640" fill="#FFFFFF"/>

  <text x="600" y="40" text-anchor="middle" font-size="24" font-weight="bold" fill="#1E2937">Урок «Алгоритми в нашому житті»</text>
  <text x="600" y="68" text-anchor="middle" font-size="14" fill="#6B7280" font-style="italic">поєднання методів і форм на різних етапах</text>

  <!-- Stage 1 -->
  <rect x="70" y="100" width="1060" height="105" rx="14" fill="#EFF6FF" stroke="#1E40AF" stroke-width="2"/>
  <circle cx="130" cy="152" r="28" fill="#1E40AF"/>
  <text x="130" y="160" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">1</text>
  <text x="185" y="140" font-size="18" font-weight="bold" fill="#1E40AF">Мотивація</text>
  <text x="185" y="168" font-size="14" fill="#374151">Метод: бесіда  |  Форма: фронтальна</text>
  <text x="185" y="190" font-size="13" fill="#6B7280">Питання про порядок дій у побуті</text>

  <!-- arrow 1 -->
  <polygon points="600,205 615,220 585,220" fill="#1E40AF"/>

  <!-- Stage 2 -->
  <rect x="70" y="225" width="1060" height="105" rx="14" fill="#ECFEFF" stroke="#0891B2" stroke-width="2"/>
  <circle cx="130" cy="277" r="28" fill="#0891B2"/>
  <text x="130" y="285" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">2</text>
  <text x="185" y="265" font-size="18" font-weight="bold" fill="#0891B2">Пояснення нового матеріалу</text>
  <text x="185" y="293" font-size="14" fill="#374151">Методи: розповідь + демонстрація  |  Форма: фронтальна</text>
  <text x="185" y="315" font-size="13" fill="#6B7280">Плакат «Алгоритм миття рук»</text>

  <!-- arrow 2 -->
  <polygon points="600,330 615,345 585,345" fill="#0891B2"/>

  <!-- Stage 3 -->
  <rect x="70" y="350" width="1060" height="115" rx="14" fill="#FAF5FF" stroke="#7C3AED" stroke-width="2"/>
  <circle cx="130" cy="407" r="28" fill="#7C3AED"/>
  <text x="130" y="415" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">3</text>
  <text x="185" y="390" font-size="18" font-weight="bold" fill="#7C3AED">Закріплення</text>
  <text x="185" y="418" font-size="14" fill="#374151">Методи: гра, моделювання  |  Форми: групова + індивідуальна</text>
  <text x="185" y="440" font-size="13" fill="#6B7280">Складання алгоритмів з карток; робота з Lightbot</text>
  <text x="185" y="458" font-size="13" fill="#6B7280">Паралельна організація двох видів діяльності</text>

  <!-- arrow 3 -->
  <polygon points="600,465 615,480 585,480" fill="#7C3AED"/>

  <!-- Stage 4 -->
  <rect x="70" y="485" width="1060" height="105" rx="14" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
  <circle cx="130" cy="537" r="28" fill="#EA580C"/>
  <text x="130" y="545" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">4</text>
  <text x="185" y="525" font-size="18" font-weight="bold" fill="#EA580C">Підсумок</text>
  <text x="185" y="553" font-size="14" fill="#374151">Метод: бесіда  |  Форма: фронтальна</text>
  <text x="185" y="575" font-size="13" fill="#6B7280">Колективне обговорення важливості послідовності дій</text>
</svg>'''

SVG_PAINT_FLOW = '''<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg"
  font-family="Times New Roman, Liberation Serif, serif">
  <rect width="1200" height="640" fill="#FFFFFF"/>

  <text x="600" y="40" text-anchor="middle" font-size="24" font-weight="bold" fill="#1E2937">Урок «Створення цифрового малюнка»</text>
  <text x="600" y="68" text-anchor="middle" font-size="14" fill="#6B7280" font-style="italic">від інструктажу до творчої виставки</text>

  <!-- Stage 1 -->
  <rect x="70" y="100" width="1060" height="105" rx="14" fill="#EFF6FF" stroke="#1E40AF" stroke-width="2"/>
  <circle cx="130" cy="152" r="28" fill="#1E40AF"/>
  <text x="130" y="160" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">1</text>
  <text x="185" y="140" font-size="18" font-weight="bold" fill="#1E40AF">Фронтальний інструктаж</text>
  <text x="185" y="168" font-size="14" fill="#374151">Методи: інструктаж + демонстрація  |  Форма: фронтальна</text>
  <text x="185" y="190" font-size="13" fill="#6B7280">Показ інструментів графічного редактора</text>

  <polygon points="600,205 615,220 585,220" fill="#1E40AF"/>

  <!-- Stage 2 -->
  <rect x="70" y="225" width="1060" height="105" rx="14" fill="#ECFEFF" stroke="#0891B2" stroke-width="2"/>
  <circle cx="130" cy="277" r="28" fill="#0891B2"/>
  <text x="130" y="285" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">2</text>
  <text x="185" y="265" font-size="18" font-weight="bold" fill="#0891B2">Індивідуальна практика</text>
  <text x="185" y="293" font-size="14" fill="#374151">Метод: вправа  |  Форма: індивідуальна</text>
  <text x="185" y="315" font-size="13" fill="#6B7280">Експериментування з інструментами</text>

  <polygon points="600,330 615,345 585,345" fill="#0891B2"/>

  <!-- Stage 3 -->
  <rect x="70" y="350" width="1060" height="105" rx="14" fill="#FAF5FF" stroke="#7C3AED" stroke-width="2"/>
  <circle cx="130" cy="402" r="28" fill="#7C3AED"/>
  <text x="130" y="410" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">3</text>
  <text x="185" y="390" font-size="18" font-weight="bold" fill="#7C3AED">Парна творча робота</text>
  <text x="185" y="418" font-size="14" fill="#374151">Методи: гра + практична  |  Форма: парна</text>
  <text x="185" y="440" font-size="13" fill="#6B7280">По черзі малюють та розфарбовують фігури</text>

  <polygon points="600,455 615,470 585,470" fill="#7C3AED"/>

  <!-- Stage 4 -->
  <rect x="70" y="475" width="1060" height="105" rx="14" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
  <circle cx="130" cy="527" r="28" fill="#EA580C"/>
  <text x="130" y="535" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">4</text>
  <text x="185" y="515" font-size="18" font-weight="bold" fill="#EA580C">Індивідуальний проєкт + виставка</text>
  <text x="185" y="543" font-size="14" fill="#374151">Метод: проєкт  |  Форми: індивідуальна → фронтальна</text>
  <text x="185" y="565" font-size="13" fill="#6B7280">Презентація робіт, обговорення</text>
</svg>'''

SVG_PRINCIPLES = '''<svg viewBox="0 0 1200 320" xmlns="http://www.w3.org/2000/svg"
  font-family="Times New Roman, Liberation Serif, serif">
  <rect width="1200" height="320" fill="#FFFFFF"/>

  <!-- 5 hexagons -->
  <!-- 1 -->
  <polygon points="120,40 190,75 190,145 120,180 50,145 50,75"
    fill="#EFF6FF" stroke="#1E40AF" stroke-width="3"/>
  <text x="120" y="100" text-anchor="middle" font-size="34" fill="#1E40AF">🛡</text>
  <text x="120" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#1E40AF">Безпека та</text>
  <text x="120" y="153" text-anchor="middle" font-size="13" font-weight="bold" fill="#1E40AF">здоров’я</text>
  <text x="120" y="215" text-anchor="middle" font-size="11" fill="#6B7280">≤ 15–20 хв/ПК</text>

  <!-- 2 -->
  <polygon points="345,40 415,75 415,145 345,180 275,145 275,75"
    fill="#ECFEFF" stroke="#0891B2" stroke-width="3"/>
  <text x="345" y="100" text-anchor="middle" font-size="34" fill="#0891B2">👁</text>
  <text x="345" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#0891B2">Доступність</text>
  <text x="345" y="153" text-anchor="middle" font-size="13" font-weight="bold" fill="#0891B2">матеріалу</text>
  <text x="345" y="215" text-anchor="middle" font-size="11" fill="#6B7280">проста мова, наочність</text>

  <!-- 3 -->
  <polygon points="570,40 640,75 640,145 570,180 500,145 500,75"
    fill="#FAF5FF" stroke="#7C3AED" stroke-width="3"/>
  <text x="570" y="100" text-anchor="middle" font-size="34" fill="#7C3AED">↑</text>
  <text x="570" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#7C3AED">Поступовість</text>
  <text x="570" y="153" text-anchor="middle" font-size="13" font-weight="bold" fill="#7C3AED">(від простого)</text>
  <text x="570" y="215" text-anchor="middle" font-size="11" fill="#6B7280">мишка → клавіатура</text>

  <!-- 4 -->
  <polygon points="795,40 865,75 865,145 795,180 725,145 725,75"
    fill="#FFF7ED" stroke="#EA580C" stroke-width="3"/>
  <text x="795" y="100" text-anchor="middle" font-size="34" fill="#EA580C">🌍</text>
  <text x="795" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#EA580C">Зв’язок</text>
  <text x="795" y="153" text-anchor="middle" font-size="13" font-weight="bold" fill="#EA580C">з життям</text>
  <text x="795" y="215" text-anchor="middle" font-size="11" fill="#6B7280">навігація, покупки</text>

  <!-- 5 -->
  <polygon points="1020,40 1090,75 1090,145 1020,180 950,145 950,75"
    fill="#FDF2F8" stroke="#E11D48" stroke-width="3"/>
  <text x="1020" y="100" text-anchor="middle" font-size="34" fill="#E11D48">✦</text>
  <text x="1020" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#E11D48">Творчий</text>
  <text x="1020" y="153" text-anchor="middle" font-size="13" font-weight="bold" fill="#E11D48">підхід</text>
  <text x="1020" y="215" text-anchor="middle" font-size="11" fill="#6B7280">експерименти</text>

  <text x="600" y="285" text-anchor="middle" font-size="14" fill="#1E2937" font-style="italic">
    Дотримання цих принципів перетворює урок на потужний інструмент розвитку особистості
  </text>
</svg>'''

# ============================================================
# 5. ПОБУДОВА СЛАЙДІВ
# ============================================================

# ---------- СЛАЙД 1: ТИТУЛЬНИЙ ----------
s = new_slide()
add_bg(s, NAVY)

# Декоративні фігури
add_rect(s, Inches(-1.5), Inches(-1.5), Inches(5), Inches(5), PRIMARY, MSO_SHAPE.OVAL)
add_rect(s, Inches(10.5), Inches(4.5), Inches(4.5), Inches(4.5), TEAL, MSO_SHAPE.OVAL)
add_rect(s, Inches(9.5), Inches(-1), Inches(2.5), Inches(2.5), PURPLE, MSO_SHAPE.OVAL)

# Акцентна смуга
add_rect(s, Inches(1), Inches(2.3), Inches(0.15), Inches(2.5), AMBER)

add_text(s, Inches(1.4), Inches(1.2), Inches(11), Inches(0.6),
         'ПРАКТИЧНЕ ЗАНЯТТЯ', size=20, bold=True, color=AMBER)

add_text(s, Inches(1.4), Inches(2.2), Inches(11), Inches(2.6),
         'Методи та форми роботи\nна уроках інформатики\nв початковій школі',
         size=44, bold=True, color=WHITE)

add_text(s, Inches(1.4), Inches(5.2), Inches(11), Inches(0.5),
         'Спеціальність: Вчитель інформатики початкової школи',
         size=18, color=LIGHT_BLUE, italic=True)

add_text(s, Inches(1.4), Inches(6.4), Inches(11), Inches(0.4),
         'Формування вмінь добирати й комбінувати методи та форми роботи',
         size=14, color=LIGHT_BLUE)

# ---------- СЛАЙД 2: МЕТА ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Мета заняття', PRIMARY)

cards_data = [
    ('НАВЧАЛЬНА', 'Формувати вміння відбирати та комбінувати методи і форми роботи з урахуванням вікових особливостей молодших школярів.', PRIMARY, LIGHT_BLUE),
    ('РОЗВИВАЛЬНА', 'Розвивати практичні навички моделювання фрагментів уроку з використанням різних методів і форм роботи.', TEAL, LIGHT_TEAL),
    ('ВИХОВНА', 'Виховувати інтерес до пошуку креативних рішень у педагогічній діяльності, до саморозвитку.', PURPLE, LIGHT_PURPLE),
]
for i, (t, b, accent, bg) in enumerate(cards_data):
    left = Inches(0.5 + i * 4.3)
    add_card(s, left, Inches(2.0), Inches(4.0), Inches(4.2), t, b, accent=accent, bg=bg)

# Маленькі кружечки-номери
for i in range(3):
    c = add_rect(s, Inches(0.75 + i * 4.3), Inches(1.55), Inches(0.7), Inches(0.7),
                 WHITE, MSO_SHAPE.OVAL, line_color=PRIMARY)
    add_text(s, Inches(0.75 + i * 4.3), Inches(1.55), Inches(0.7), Inches(0.7),
             str(i + 1), size=20, bold=True, color=PRIMARY,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

add_footer(s, 2)

# ---------- СЛАЙД 3: КЛАСИФІКАЦІЯ МЕТОДІВ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Класифікація методів навчання', BLUE)
add_svg(s, SVG_METHODS, Inches(0.4), Inches(1.3), width=Inches(12.5))
add_footer(s, 3)

# ---------- СЛАЙД 4: СЛОВЕСНІ МЕТОДИ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Словесні методи', BLUE)

verbal = [
    ('РОЗПОВІДЬ', 'Коротка, образна, з яскравими прикладами.\n\nПриклад: пояснення понять «алгоритм» чи «принцип роботи мишки».', BLUE, LIGHT_BLUE),
    ('БЕСІДА', 'Діалог, що залучає учнів до обговорення.\n\nПриклад: після відео про кібербезпеку — «Чому не можна ділитися адресою?»', TEAL, LIGHT_TEAL),
    ('ІНСТРУКТАЖ', 'Чітке, послідовне пояснення правил.\n\nПриклад: правила поведінки в комп’ютерному класі; алгоритм дій для завдання.', PURPLE, LIGHT_PURPLE),
]
for i, (t, b, accent, bg) in enumerate(verbal):
    left = Inches(0.5 + i * 4.3)
    add_card(s, left, Inches(1.6), Inches(4.0), Inches(5.0), t, b, accent=accent, bg=bg, title_size=20)

add_footer(s, 4)

# ---------- СЛАЙД 5: НАОЧНІ МЕТОДИ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Наочні методи', TEAL)

visual = [
    ('ДЕМОНСТРАЦІЯ', 'Показ на екрані/проекторі.\n\nПриклад: створення папки, малювання фігури в графічному редакторі.', TEAL, LIGHT_TEAL),
    ('СПОСТЕРЕЖЕННЯ', 'Учні уважно слідкують за роботою програми чи анімацією.\n\nПриклад: спостереження за роботою алгоритму.', GREEN, LIGHT_GREEN),
    ('ІЛЮСТРАЦІЇ', 'Плакати, картки, схеми.\n\nПриклад: пристрої комп’ютера, елементи блок-схем, «Алгоритм миття рук».', BLUE, LIGHT_BLUE),
]
for i, (t, b, accent, bg) in enumerate(visual):
    left = Inches(0.5 + i * 4.3)
    add_card(s, left, Inches(1.6), Inches(4.0), Inches(5.0), t, b, accent=accent, bg=bg, title_size=20)

add_footer(s, 5)

# ---------- СЛАЙД 6: ПРАКТИЧНІ МЕТОДИ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Практичні методи', ORANGE)

practical = [
    ('ВПРАВА', 'Багаторазове повторення дій.\n\nПриклад: швидкісний набір тексту, «гарячі» клавіші.', ORANGE, LIGHT_ORANGE),
    ('ГРАФІЧНІ РОБОТИ', 'Робота в Paint / Tux Paint.\n\nРозвиток роботи з мишкою та креативності.', ROSE, RGBColor(0xFF, 0xF1, 0xF2)),
    ('МОДЕЛЮВАННЯ', 'Створення простих моделей.\n\nПриклад: «падіння снігу» в Scratch, будинок з блоків.', PURPLE, LIGHT_PURPLE),
    ('ПРОЄКТНА ДІЯЛЬНІСТЬ', 'Творчі завдання.\n\nПриклад: листівка до свята, презентація про тварину.', GREEN, LIGHT_GREEN),
]
for i, (t, b, accent, bg) in enumerate(practical):
    left = Inches(0.35 + i * 3.2)
    add_card(s, left, Inches(1.6), Inches(3.0), Inches(5.1), t, b, accent=accent, bg=bg, title_size=17)

add_footer(s, 6)

# ---------- СЛАЙД 7: ІГРОВІ МЕТОДИ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Ігрові методи', PURPLE)

games = [
    ('ДИДАКТИЧНІ ІГРИ', '«Знайди пару», «Хто зайвий?».\n\nЗасвоєння призначення пристроїв комп’ютера в ігровій формі.', PURPLE, LIGHT_PURPLE),
    ('СЮЖЕТНО-РОЛЬОВІ', '«Подорож до Країни Алгоритмів».\n\nДіти стають роботами, що виконують команди.', ROSE, RGBColor(0xFF, 0xF1, 0xF2)),
    ('КОМП’ЮТЕРНІ ІГРИ', '«Вчимось з Бубою», «Логічні вірші».\n\nРозвиток логіки, уваги, пам’яті.', TEAL, LIGHT_TEAL),
]
for i, (t, b, accent, bg) in enumerate(games):
    left = Inches(0.5 + i * 4.3)
    add_card(s, left, Inches(1.6), Inches(4.0), Inches(5.0), t, b, accent=accent, bg=bg, title_size=20)

add_footer(s, 7)

# ---------- СЛАЙД 8: ФОРМИ ОРГАНІЗАЦІЇ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Форми організації навчальної діяльності', GREEN)
add_svg(s, SVG_FORMS, Inches(0.4), Inches(1.3), width=Inches(12.5))
add_footer(s, 8)

# ---------- СЛАЙД 9: ФРОНТАЛЬНА РОБОТА ----------
def form_slide(title, accent, bg_light, definition, optimal, example_title, example_text, page):
    s = new_slide()
    add_bg(s, WHITE)
    add_header(s, title, accent)
    # Left panel
    add_text(s, Inches(0.5), Inches(1.5), Inches(6), Inches(0.5),
             'Сутність', size=18, bold=True, color=accent)
    add_text(s, Inches(0.5), Inches(2.0), Inches(6), Inches(1.5),
             definition, size=16, color=DARK)
    add_text(s, Inches(0.5), Inches(3.6), Inches(6), Inches(0.5),
             'Оптимальні ситуації', size=18, bold=True, color=accent)
    add_bullets(s, Inches(0.5), Inches(4.1), Inches(6), Inches(2.5),
                optimal, size=15, bullet_color=accent)
    # Right panel (example)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(7.0), Inches(1.5), Inches(5.8), Inches(5.3))
    box.fill.solid(); box.fill.fore_color.rgb = bg_light
    box.line.color.rgb = accent; box.line.width = Pt(2)
    box.adjustments[0] = 0.05
    add_text(s, Inches(7.3), Inches(1.7), Inches(5.3), Inches(0.5),
             example_title, size=20, bold=True, color=accent)
    add_text(s, Inches(7.3), Inches(2.4), Inches(5.3), Inches(4.2),
             example_text, size=14, color=DARK)
    add_footer(s, page)
    return s

form_slide(
    'Фронтальна робота', PRIMARY, LIGHT_BLUE,
    'Учитель працює одночасно з усім класом: пояснює, інструктує, проводить колективне обговорення.',
    ['Введення в нову тему',
     'Інструктаж перед практичною роботою',
     'Колективне обговорення результатів',
     'Підбиття підсумків уроку'],
    'Приклад із практики',
    'Усі учні одночасно виконують вправу на клавіатурному тренажері під керівництвом учителя. Вчитель демонструє на екрані, коментує, а діти повторюють дії.',
    9)

form_slide(
    'Індивідуальна робота', ORANGE, LIGHT_ORANGE,
    'Кожен учень працює самостійно у власному темпі за комп’ютером або з роздатковим матеріалом.',
    ['Відпрацювання практичних навичок',
     'Виконання творчих завдань (малюнок, презентація)',
     'Контроль і самоконтроль знань',
     'Робота з учнями з різним темпом'],
    'Приклад із практики',
    'Створення власного малюнка в Paint: кожен учень обирає сюжет, інструменти й час завершення роботи. Учитель консультує індивідуально.',
    10)

form_slide(
    'Групова (парна) робота', PURPLE, LIGHT_PURPLE,
    'Об’єднання учнів у групи по 2–4 особи для спільного виконання завдання. Особливо ефективна робота в парах за одним комп’ютером.',
    ['Проєкти та складні завдання',
     'Завдання, що вимагають обміну ідеями',
     'Взаємоперевірка',
     'Принцип «одна мишка — дві голови»'],
    'Приклад із практики',
    'Створення спільної презентації «Тварини нашого лісу»: один учень шукає зображення, другий пише текст, третій відповідає за оформлення.',
    11)

form_slide(
    'Колективна форма', ROSE, RGBColor(0xFF, 0xF1, 0xF2),
    'Клас ділиться на команди, які змагаються між собою у виконанні завдань. Підвищує мотивацію та дозволяє узагальнити знання.',
    ['Вікторини та брейн-ринги',
     'Конкурси на найкраще оформлення',
     'Узагальнення знань у захопливій формі',
     'Підвищення мотивації учнів'],
    'Приклад із практики',
    'Брейн-ринг із теми безпеки в інтернеті: команди по черзі відповідають на запитання, отримують бали за швидкість і правильність, обговорюють помилки.',
    12)

# ---------- СЛАЙД 13: ІНТЕГРАЦІЯ - АЛГОРИТМИ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Інтеграція методів і форм: приклад 1', PRIMARY)
add_svg(s, SVG_ALGO_FLOW, Inches(0.4), Inches(1.2), width=Inches(12.5))
add_footer(s, 13)

# ---------- СЛАЙД 14: ІНТЕГРАЦІЯ - МАЛЮНОК ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Інтеграція методів і форм: приклад 2', ORANGE)
add_svg(s, SVG_PAINT_FLOW, Inches(0.4), Inches(1.2), width=Inches(12.5))
add_footer(s, 14)

# ---------- СЛАЙД 15: КЛЮЧОВІ ПРИНЦИПИ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Ключові принципи ефективного навчання', GREEN)
add_svg(s, SVG_PRINCIPLES, Inches(0.4), Inches(1.4), width=Inches(12.5))
add_footer(s, 15)

# ---------- СЛАЙД 16: ПРАКТИЧНЕ ЗАВДАННЯ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Практичне завдання: ментальна карта', PRIMARY)

add_text(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(0.5),
         'Створіть ментальну карту на тему:', size=18, bold=True, color=DARK)
add_text(s, Inches(0.5), Inches(2.0), Inches(12.3), Inches(0.6),
         '«Методи та форми роботи на уроках інформатики в початковій школі»',
         size=22, bold=True, color=PRIMARY)

# 4 обов'язкові гілки
branches = [
    ('Методи навчання', 'словесні, наочні, практичні, ігрові', BLUE, LIGHT_BLUE),
    ('Форми організації', 'фронтальна, індивідуальна, групова, колективна', GREEN, LIGHT_GREEN),
    ('Принципи навчання', 'безпека, доступність, поступовість, зв’язок з життям, творчість', ORANGE, LIGHT_ORANGE),
    ('Приклади інтеграції', '2–3 приклади уроків із поєднанням методів і форм', PURPLE, LIGHT_PURPLE),
]
for i, (t, d, accent, bg) in enumerate(branches):
    row, col = divmod(i, 2)
    left = Inches(0.5 + col * 6.2)
    top = Inches(3.0 + row * 1.85)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.9), Inches(1.65))
    box.fill.solid(); box.fill.fore_color.rgb = bg
    box.line.color.rgb = accent; box.line.width = Pt(2)
    box.adjustments[0] = 0.1
    add_text(s, left + Inches(0.3), top + Inches(0.25), Inches(5.3), Inches(0.45),
             t, size=18, bold=True, color=accent)
    add_text(s, left + Inches(0.3), top + Inches(0.75), Inches(5.3), Inches(0.8),
             d, size=13, color=DARK)

add_footer(s, 16)

# ---------- СЛАЙД 17: ВИМОГИ ДО ВИКОНАННЯ ----------
s = new_slide()
add_bg(s, WHITE)
add_header(s, 'Вимоги до виконання та оцінювання', TEAL)

add_text(s, Inches(0.5), Inches(1.5), Inches(6), Inches(0.5),
         'Змістовне наповнення', size=18, bold=True, color=TEAL)
add_bullets(s, Inches(0.5), Inches(2.05), Inches(6), Inches(2.5),
            ['2–3 приклади для кожного методу',
             'Оптимальні ситуації для кожної форми',
             'Взаємозв’язки між методами та формами',
             'Гілки 2-го та 3-го рівнів'],
            size=15, bullet_color=TEAL)

add_text(s, Inches(7.0), Inches(1.5), Inches(5.8), Inches(0.5),
         'Візуальне оформлення', size=18, bold=True, color=ORANGE)
add_bullets(s, Inches(7.0), Inches(2.05), Inches(5.8), Inches(2.5),
            ['Кольорова палітра для категорій',
             'Символи, іконки, емодзі',
             'Різні види ліній та шрифтів',
             'Центральний образ + основні гілки'],
            size=15, bullet_color=ORANGE)

# Технічні вимоги (у вигляді плашок)
add_text(s, Inches(0.5), Inches(4.8), Inches(12.3), Inches(0.4),
         'Технічні вимоги', size=16, bold=True, color=DARK)

tech = [
    ('ПЗ на вибір', 'MindMeister, XMind, Coggle, Canva', PURPLE, LIGHT_PURPLE),
    ('Формат', 'PDF або PNG', PRIMARY, LIGHT_BLUE),
    ('Роздільна здатність', '≥ 1920 × 1080 px', GREEN, LIGHT_GREEN),
]
for i, (label, val, accent, bg) in enumerate(tech):
    left = Inches(0.5 + i * 4.3)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        left, Inches(5.3), Inches(4.0), Inches(1.4))
    box.fill.solid(); box.fill.fore_color.rgb = bg
    box.line.color.rgb = accent; box.line.width = Pt(2)
    box.adjustments[0] = 0.15
    add_text(s, left + Inches(0.25), Inches(5.45), Inches(3.5), Inches(0.4),
             label, size=13, bold=True, color=accent)
    add_text(s, left + Inches(0.25), Inches(5.85), Inches(3.5), Inches(0.7),
             val, size=15, bold=True, color=DARK)

add_footer(s, 17)

# ---------- СЛАЙД 18: ДЯКУЮ ----------
s = new_slide()
add_bg(s, NAVY)

# Декоративні елементи
add_rect(s, Inches(10.5), Inches(-2), Inches(5), Inches(5), TEAL, MSO_SHAPE.OVAL)
add_rect(s, Inches(-1.5), Inches(5), Inches(4), Inches(4), PURPLE, MSO_SHAPE.OVAL)

add_text(s, Inches(1), Inches(2.5), Inches(11.3), Inches(1.5),
         'Дякую за увагу!', size=64, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(4.3), Inches(11.3), Inches(0.7),
         'Творчих успіхів у педагогічній діяльності!',
         size=24, italic=True, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(5.5), Inches(11.3), Inches(0.5),
         'Практичне заняття • Методи та форми роботи на уроках інформатики',
         size=14, color=LIGHT_TEAL, align=PP_ALIGN.CENTER)

# ============================================================
# 6. ЗБЕРЕЖЕННЯ
# ============================================================
output = 'presentation_methods_forms.pptx'
prs.save(output)
print(f'✓ Презентацію збережено: {output}')
print(f'✓ Усього слайдів: {len(prs.slides)}')