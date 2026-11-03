"""
pip install python-docx cairosvg
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import cairosvg
import io


# ---------------------------------------------------------------------------
# SVG-ілюстрації для запитань (конвертуються в PNG і вставляються у DOCX)
# ---------------------------------------------------------------------------
SVG_TIMELINE = '''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="110" viewBox="0 0 500 110">
  <line x1="20" y1="60" x2="480" y2="60" stroke="#2c3e50" stroke-width="3"/>
  <polygon points="480,60 468,54 468,66" fill="#2c3e50"/>
  <circle cx="130" cy="60" r="9" fill="#e74c3c"/>
  <text x="130" y="30" text-anchor="middle" font-family="DejaVu Sans" font-size="13" fill="#c0392b" font-weight="bold">XV століття</text>
  <text x="130" y="88" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#2c3e50">Книгодрукування</text>
  <circle cx="370" cy="60" r="9" fill="#3498db"/>
  <text x="370" y="30" text-anchor="middle" font-family="DejaVu Sans" font-size="13" fill="#2980b9" font-weight="bold">XIX століття</text>
  <text x="370" y="88" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#2c3e50">Фотографія</text>
</svg>'''

SVG_SERIF = '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="160" viewBox="0 0 420 160">
  <rect x="10" y="10" width="195" height="140" fill="#f8f9fa" stroke="#dee2e6" rx="6"/>
  <text x="107" y="105" text-anchor="middle" font-family="DejaVu Serif" font-size="95" fill="#2c3e50">A</text>
  <text x="107" y="145" text-anchor="middle" font-family="DejaVu Sans" font-size="14" fill="#2c3e50" font-weight="bold">Serif (з засічками)</text>
  <rect x="215" y="10" width="195" height="140" fill="#f8f9fa" stroke="#dee2e6" rx="6"/>
  <text x="312" y="105" text-anchor="middle" font-family="DejaVu Sans" font-size="95" fill="#2c3e50">A</text>
  <text x="312" y="145" text-anchor="middle" font-family="DejaVu Sans" font-size="14" fill="#2c3e50" font-weight="bold">Sans-Serif (без засічок)</text>
</svg>'''

SVG_PSYCHOLOGY = '''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="170" viewBox="0 0 480 170">
  <text x="240" y="20" text-anchor="middle" font-family="DejaVu Sans" font-size="13" fill="#2c3e50" font-weight="bold">Кольоропсихологія та гештальт-принципи</text>
  <circle cx="60" cy="70" r="28" fill="#e74c3c"/>
  <circle cx="140" cy="70" r="28" fill="#f39c12"/>
  <circle cx="220" cy="70" r="28" fill="#2ecc71"/>
  <circle cx="300" cy="70" r="28" fill="#3498db"/>
  <circle cx="380" cy="70" r="28" fill="#9b59b6"/>
  <text x="60" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="10">енергія</text>
  <text x="140" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="10">радість</text>
  <text x="220" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="10">спокій</text>
  <text x="300" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="10">довіра</text>
  <text x="380" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="10">творчість</text>
  <g fill="#2c3e50">
    <circle cx="60" cy="150" r="6"/><circle cx="80" cy="150" r="6"/><circle cx="100" cy="150" r="6"/>
    <circle cx="200" cy="150" r="6"/><circle cx="240" cy="150" r="6"/><circle cx="280" cy="150" r="6"/>
  </g>
  <text x="80" y="168" text-anchor="middle" font-family="DejaVu Sans" font-size="10">близькість</text>
  <text x="240" y="168" text-anchor="middle" font-family="DejaVu Sans" font-size="10">подібність</text>
</svg>'''

SVG_PORTFOLIO = '''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="160" viewBox="0 0 480 160">
  <rect x="20" y="20" width="440" height="120" rx="8" fill="#ecf0f1" stroke="#2c3e50" stroke-width="2"/>
  <rect x="20" y="20" width="440" height="22" rx="8" fill="#2c3e50"/>
  <circle cx="38" cy="31" r="5" fill="#e74c3c"/>
  <circle cx="55" cy="31" r="5" fill="#f39c12"/>
  <circle cx="72" cy="31" r="5" fill="#2ecc71"/>
  <rect x="40" y="60" width="90" height="65" rx="4" fill="#3498db"/>
  <rect x="145" y="60" width="90" height="65" rx="4" fill="#e74c3c"/>
  <rect x="250" y="60" width="90" height="65" rx="4" fill="#2ecc71"/>
  <rect x="355" y="60" width="90" height="65" rx="4" fill="#f39c12"/>
  <text x="85" y="97" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#fff">Відео</text>
  <text x="190" y="97" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#fff">Фото</text>
  <text x="295" y="97" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#fff">PDF</text>
  <text x="400" y="97" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#fff">Сайт</text>
</svg>'''


def make_pixel_svg():
    """Проста піксельна сітка — ілюстрація растрової графіки."""
    import random
    random.seed(7)
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
    cells = []
    for y in range(10):
        for x in range(10):
            c = random.choice(colors)
            cells.append(
                f'<rect x="{x*20}" y="{y*20}" width="20" height="20" '
                f'fill="{c}" stroke="#ffffff" stroke-width="0.5"/>'
            )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">'
            f'{"".join(cells)}</svg>')


def make_vector_vs_raster_svg():
    """Порівняння растрового (пікселі) і векторного (криві) зображень."""
    squares = []
    cx, cy, r = 100, 100, 60
    step = 12
    for y in range(cy - r, cy + r, step):
        for x in range(cx - r, cx + r, step):
            dx = x + step / 2 - cx
            dy = y + step / 2 - cy
            if dx * dx + dy * dy <= r * r:
                squares.append(
                    f'<rect x="{x}" y="{y}" width="{step}" height="{step}" '
                    f'fill="#3498db" stroke="#ffffff" stroke-width="0.6"/>'
                )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <text x="100" y="20" text-anchor="middle" font-family="DejaVu Sans" font-size="12"
        fill="#2c3e50" font-weight="bold">Растрова (пікселі)</text>
  {''.join(squares)}
  <text x="300" y="20" text-anchor="middle" font-family="DejaVu Sans" font-size="12"
        fill="#2c3e50" font-weight="bold">Векторна (криві й вузли)</text>
  <circle cx="300" cy="105" r="60" fill="#2ecc71" stroke="#27ae60" stroke-width="2"/>
  <circle cx="300" cy="105" r="4.5" fill="#e74c3c"/>
  <circle cx="360" cy="105" r="4.5" fill="#e74c3c"/>
  <circle cx="300" cy="165" r="4.5" fill="#e74c3c"/>
  <circle cx="300" cy="45"  r="4.5" fill="#e74c3c"/>
</svg>'''


# ---------------------------------------------------------------------------
# Допоміжні функції для DOCX
# ---------------------------------------------------------------------------
def svg_to_buffer(svg_str: str, width_px: int = 900) -> io.BytesIO:
    png = cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), output_width=width_px)
    return io.BytesIO(png)


def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(18)


def add_question(doc, num, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"Питання {num}. ")
    r.bold = True
    r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
    p.add_run(text)


def add_svg_image(doc, svg_str, width_inches=5.0):
    buf = svg_to_buffer(svg_str)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(buf, width=Inches(width_inches))


def add_answer_lines(doc, n=3):
    for _ in range(n):
        p = doc.add_paragraph("_" * 92)
        p.paragraph_format.space_after = Pt(2)
    doc.add_paragraph()


def add_label(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.color.rgb = RGBColor(0x27, 0xAE, 0x60)


def add_checkboxes(doc, options):
    for opt in options:
        p = doc.add_paragraph(f"   [   ]   {opt}")
        p.paragraph_format.space_after = Pt(2)


# ---------------------------------------------------------------------------
# Побудова документа
# ---------------------------------------------------------------------------
def build_document(path="kontrolni_pytannya.docx"):
    doc = Document()

    # Базовий стиль
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)

    # Заголовок
    add_title(doc, "КОНТРОЛЬНІ ПИТАННЯ")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("з дисципліни «Графічна культура»")
    r.italic = True
    r.font.size = Pt(13)
    doc.add_paragraph()

    # Таблиця з даними студента
    info = doc.add_table(rows=2, cols=4)
    info.style = "Table Grid"
    info.cell(0, 0).text = "ПІБ студента:"
    info.cell(0, 1).merge(info.cell(0, 3))
    info.cell(1, 0).text = "Група:"
    info.cell(1, 1).merge(info.cell(1, 3))
    doc.add_paragraph()

    # ---------------- Питання 1 ----------------
    add_question(doc, 1,
        "Назвіть дві ключові події в історії графічної культури, які передували "
        "цифровій ері, та вкажіть століття, коли вони відбулися.")
    add_svg_image(doc, SVG_TIMELINE, width_inches=5.5)
    add_label(doc, "Ваша відповідь:")
    add_answer_lines(doc, 3)

    # ---------------- Питання 2 ----------------
    add_question(doc, 2,
        "Що таке растрове зображення та назвіть один з його основних недоліків "
        "при масштабуванні?")
    add_svg_image(doc, make_pixel_svg(), width_inches=2.8)
    add_label(doc, "Визначення растрового зображення:")
    add_answer_lines(doc, 2)
    add_label(doc, "Оберіть правильний недолік (можна декілька):")
    add_checkboxes(doc, [
        "Втрата якості (пікселізація) при збільшенні",
        "Файл зменшується при масштабуванні",
        "Кольори інвертуються при збільшенні",
        "Зображення складається з векторних кривих",
    ])
    doc.add_paragraph()

    # ---------------- Питання 3 ----------------
    add_question(doc, 3,
        "Яка основна відмінність між шрифтами з засічками (Serif) та без засічок "
        "(Sans-Serif) з точки зору їхнього характерного враження?")
    add_svg_image(doc, SVG_SERIF, width_inches=5.0)
    add_label(doc, "Оберіть найточніше твердження:")
    add_checkboxes(doc, [
        "Serif — сучасний і технологічний; Sans-Serif — традиційний і класичний",
        "Serif — традиційний, офіційний, «книжковий»; Sans-Serif — сучасний, мінімалістичний",
        "Serif — лише для заголовків; Sans-Serif — лише для основного тексту",
        "Різниці у сприйнятті немає",
    ])
    add_label(doc, "Коротке обґрунтування вибору:")
    add_answer_lines(doc, 2)

    # ---------------- Питання 4 ----------------
    add_question(doc, 4,
        "Порівняйте принципи зберігання та масштабування растрової та векторної "
        "графіки. Чому векторна графіка є кращим вибором для створення логотипів, "
        "які потрібно використовувати в різних розмірах?")
    add_svg_image(doc, make_vector_vs_raster_svg(), width_inches=5.0)
    add_label(doc, "Порівняння та відповідь:")
    add_answer_lines(doc, 5)

    # ---------------- Питання 5 ----------------
    add_question(doc, 5,
        "Поясніть, як принципи психології сприйняття (наприклад, кольоропсихологія "
        "або гештальт-принципи) можуть бути використані при створенні навчального "
        "плаката для молодших школярів. Наведіть конкретні приклади.")
    add_svg_image(doc, SVG_PSYCHOLOGY, width_inches=5.5)
    add_label(doc, "Відповідь з прикладами:")
    add_answer_lines(doc, 5)

    # ---------------- Питання 6 ----------------
    add_question(doc, 6,
        "Уявіть, що ви створюєте електронне портфоліо. Які переваги електронного "
        "формату перед друкованим ви можете використати, щоб найкраще "
        "продемонструвати саме ваші педагогічні здібності та досягнення? "
        "Наведіть не менше двох прикладів.")
    add_svg_image(doc, SVG_PORTFOLIO, width_inches=5.5)
    add_label(doc, "Приклади переваг (мінімум 2):")
    add_answer_lines(doc, 5)

    # Збереження
    doc.save(path)
    print(f"✔ Документ створено: {path}")


if __name__ == "__main__":
    build_document()