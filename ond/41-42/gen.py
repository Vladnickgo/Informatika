# -*- coding: utf-8 -*-
"""
Генерація DOCX-документа до лекційного заняття № 10
Тема: Побудова методики формувального етапу експерименту
"""

import os
import math
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False
    print("[!] cairosvg не встановлено — SVG буде збережено, PNG-заглушки створено.")

OUTPUT_DIR = "output"
SVG_DIR = os.path.join(OUTPUT_DIR, "svg")
PNG_DIR = os.path.join(OUTPUT_DIR, "png")
os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

FONT = "Arial, DejaVu Sans, sans-serif"

# ---------------------------------------------------------------------------
# SVG-хелпери
# ---------------------------------------------------------------------------

def _polar(cx, cy, r, angle_deg):
    a = math.radians(angle_deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def _donut_segment(cx, cy, r_out, r_in, start_deg, end_deg):
    x1, y1 = _polar(cx, cy, r_out, start_deg)
    x2, y2 = _polar(cx, cy, r_out, end_deg)
    x3, y3 = _polar(cx, cy, r_in, end_deg)
    x4, y4 = _polar(cx, cy, r_in, start_deg)
    large = 1 if (end_deg - start_deg) > 180 else 0
    return (f"M {x1:.2f} {y1:.2f} "
            f"A {r_out} {r_out} 0 {large} 1 {x2:.2f} {y2:.2f} "
            f"L {x3:.2f} {y3:.2f} "
            f"A {r_in} {r_in} 0 {large} 0 {x4:.2f} {y4:.2f} Z")


def save_svg_and_png(svg: str, name: str) -> str:
    svg_path = os.path.join(SVG_DIR, f"{name}.svg")
    png_path = os.path.join(PNG_DIR, f"{name}.png")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    if HAS_CAIROSVG:
        try:
            cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                             write_to=png_path, scale=2.0,
                             background_color="white")
            return png_path
        except Exception as e:
            print(f"[cairosvg] {name}: {e}")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.text(0.5, 0.5,
                f"[SVG: {name}]\nВстановіть cairosvg:\npip install cairosvg",
                ha="center", va="center", fontsize=11)
        ax.axis("off")
        fig.savefig(png_path, dpi=120, bbox_inches="tight")
        plt.close(fig)
    except Exception:
        pass
    return png_path


# ---------------------------------------------------------------------------
# SVG № 1 — Структура педагогічного експерименту
# ---------------------------------------------------------------------------

def svg_experiment_structure() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 340" width="900" height="340">
  <style>text {{ font-family: {FONT}; }}</style>
  <rect width="900" height="340" fill="#FFFFFF"/>
  <text x="450" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F3864">Структура педагогічного експерименту</text>

  <rect x="50" y="100" width="220" height="140" rx="12" fill="#DEEBF7" stroke="#4472C4" stroke-width="2.5"/>
  <text x="160" y="140" text-anchor="middle" font-size="16" font-weight="bold" fill="#1F3864">1. Констатувальний</text>
  <text x="160" y="172" text-anchor="middle" font-size="12" fill="#404040">Вимірювання</text>
  <text x="160" y="190" text-anchor="middle" font-size="12" fill="#404040">вихідного рівня</text>
  <text x="160" y="215" text-anchor="middle" font-size="11" font-style="italic" fill="#4472C4">«діагностика»</text>

  <line x1="282" y1="170" x2="330" y2="170" stroke="#1F3864" stroke-width="3"/>
  <polygon points="330,162 345,170 330,178" fill="#1F3864"/>

  <rect x="340" y="90" width="230" height="160" rx="12" fill="#FCE4D6" stroke="#ED7D31" stroke-width="4"/>
  <rect x="395" y="68" width="130" height="30" rx="8" fill="#ED7D31"/>
  <text x="460" y="88" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">ОСНОВНИЙ ЕТАП</text>
  <text x="460" y="140" text-anchor="middle" font-size="16" font-weight="bold" fill="#1F3864">2. Формувальний</text>
  <text x="460" y="172" text-anchor="middle" font-size="12" fill="#404040">Впровадження</text>
  <text x="460" y="190" text-anchor="middle" font-size="12" fill="#404040">авторської методики</text>
  <text x="460" y="215" text-anchor="middle" font-size="11" font-style="italic" fill="#ED7D31">«вплив»</text>

  <line x1="582" y1="170" x2="630" y2="170" stroke="#1F3864" stroke-width="3"/>
  <polygon points="630,162 645,170 630,178" fill="#1F3864"/>

  <rect x="650" y="100" width="220" height="140" rx="12" fill="#E2EFDA" stroke="#70AD47" stroke-width="2.5"/>
  <text x="760" y="140" text-anchor="middle" font-size="16" font-weight="bold" fill="#1F3864">3. Контрольний</text>
  <text x="760" y="172" text-anchor="middle" font-size="12" fill="#404040">Повторне</text>
  <text x="760" y="190" text-anchor="middle" font-size="12" fill="#404040">вимірювання</text>
  <text x="760" y="215" text-anchor="middle" font-size="11" font-style="italic" fill="#70AD47">«оцінка змін»</text>

  <text x="450" y="305" text-anchor="middle" font-size="13" font-style="italic" fill="#404040">Формувальний етап — «ядро» експерименту, де реалізується авторська методика</text>
</svg>'''


# ---------------------------------------------------------------------------
# SVG № 2 — Алгоритм побудови методики
# ---------------------------------------------------------------------------

def svg_building_algorithm() -> str:
    steps = [
        ("1", "#4472C4", "#DEEBF7", "Визначення мети і завдань",
         "Чого хочемо досягти? Які зміни очікуємо?"),
        ("2", "#70AD47", "#E2EFDA", "Вибір критеріїв і показників",
         "За чим вимірюватимемо результат?"),
        ("3", "#FFC000", "#FFF2CC", "Розробка змісту впливів",
         "Які методи, форми, засоби впроваджуємо?"),
        ("4", "#ED7D31", "#FCE4D6", "Визначення етапів упровадження",
         "Послідовність кроків реалізації методики"),
        ("5", "#4472C4", "#DEEBF7", "Підбір методів фіксації результатів",
         "Як збиратимемо й опрацьовуватимемо дані?"),
        ("6", "#70AD47", "#E2EFDA", "Опис процедури контролю",
         "Порівняння, аналіз, коригування, висновки"),
    ]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 740" width="720" height="740">',
             f'<style>text {{ font-family: {FONT}; }}</style>',
             '<rect width="720" height="740" fill="#FFFFFF"/>',
             '<text x="360" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F3864">Алгоритм побудови методики формувального етапу</text>']
    y0 = 70
    step_h = 82
    gap = 22
    for i, (num, num_color, fill, title, subtitle) in enumerate(steps):
        y = y0 + i * (step_h + gap)
        parts.append(f'<rect x="80" y="{y}" width="560" height="{step_h}" rx="12" fill="{fill}" stroke="{num_color}" stroke-width="2"/>')
        parts.append(f'<circle cx="125" cy="{y + step_h/2}" r="23" fill="{num_color}"/>')
        parts.append(f'<text x="125" y="{y + step_h/2 + 7}" text-anchor="middle" font-size="19" font-weight="bold" fill="#FFFFFF">{num}</text>')
        parts.append(f'<text x="168" y="{y + 30}" font-size="14" font-weight="bold" fill="#1F3864">{title}</text>')
        parts.append(f'<text x="168" y="{y + 56}" font-size="12" fill="#404040">{subtitle}</text>')
        if i < len(steps) - 1:
            ay = y + step_h
            parts.append(f'<line x1="360" y1="{ay + 2}" x2="360" y2="{ay + gap - 6}" stroke="#1F3864" stroke-width="2"/>')
            parts.append(f'<polygon points="{360-6},{ay + gap - 6} 360,{ay + gap + 4} {360+6},{ay + gap - 6}" fill="#1F3864"/>')
    parts.append('</svg>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# SVG № 3 — Дизайн експерименту (паралельні групи)
# ---------------------------------------------------------------------------

def svg_experimental_design() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 470" width="900" height="470">
  <style>text {{ font-family: {FONT}; }}</style>
  <rect width="900" height="470" fill="#FFFFFF"/>
  <text x="450" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F3864">Дизайн формувального експерименту</text>

  <text x="270" y="92" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">До (констат.)</text>
  <text x="480" y="92" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Вплив (форм.)</text>
  <text x="700" y="92" text-anchor="middle" font-size="15" font-weight="bold" fill="#1F3864">Після (контр.)</text>

  <!-- ЕГ row -->
  <rect x="40" y="115" width="90" height="130" rx="10" fill="#FCE4D6" stroke="#ED7D31" stroke-width="2.5"/>
  <text x="85" y="165" text-anchor="middle" font-size="22" font-weight="bold" fill="#1F3864">ЕГ</text>
  <text x="85" y="192" text-anchor="middle" font-size="11" fill="#404040">експерим.</text>
  <text x="85" y="208" text-anchor="middle" font-size="11" fill="#404040">група</text>

  <rect x="160" y="115" width="220" height="130" rx="10" fill="#DEEBF7" stroke="#4472C4" stroke-width="2"/>
  <text x="270" y="170" text-anchor="middle" font-size="14" fill="#1F3864">Вимірювання</text>
  <text x="270" y="192" text-anchor="middle" font-size="14" fill="#1F3864">вихідного рівня</text>

  <rect x="405" y="115" width="150" height="130" rx="10" fill="#FCE4D6" stroke="#ED7D31" stroke-width="3"/>
  <text x="480" y="165" text-anchor="middle" font-size="14" font-weight="bold" fill="#C00000">МЕТОДИКА</text>
  <text x="480" y="188" text-anchor="middle" font-size="12" fill="#C00000">(впровадження)</text>

  <rect x="580" y="115" width="220" height="130" rx="10" fill="#E2EFDA" stroke="#70AD47" stroke-width="2"/>
  <text x="690" y="170" text-anchor="middle" font-size="14" fill="#1F3864">Повторне</text>
  <text x="690" y="192" text-anchor="middle" font-size="14" fill="#1F3864">вимірювання</text>

  <line x1="382" y1="180" x2="402" y2="180" stroke="#1F3864" stroke-width="2"/>
  <polygon points="402,175 410,180 402,185" fill="#1F3864"/>
  <line x1="557" y1="180" x2="577" y2="180" stroke="#1F3864" stroke-width="2"/>
  <polygon points="577,175 585,180 577,185" fill="#1F3864"/>

  <!-- КГ row -->
  <rect x="40" y="285" width="90" height="130" rx="10" fill="#E2EFDA" stroke="#70AD47" stroke-width="2.5"/>
  <text x="85" y="335" text-anchor="middle" font-size="22" font-weight="bold" fill="#1F3864">КГ</text>
  <text x="85" y="362" text-anchor="middle" font-size="11" fill="#404040">контр.</text>
  <text x="85" y="378" text-anchor="middle" font-size="11" fill="#404040">група</text>

  <rect x="160" y="285" width="220" height="130" rx="10" fill="#DEEBF7" stroke="#4472C4" stroke-width="2"/>
  <text x="270" y="340" text-anchor="middle" font-size="14" fill="#1F3864">Вимірювання</text>
  <text x="270" y="362" text-anchor="middle" font-size="14" fill="#1F3864">вихідного рівня</text>

  <rect x="405" y="285" width="150" height="130" rx="10" fill="#F2F2F2" stroke="#A5A5A5" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="480" y="335" text-anchor="middle" font-size="13" fill="#666666">Традиційне</text>
  <text x="480" y="355" text-anchor="middle" font-size="13" fill="#666666">навчання</text>
  <text x="480" y="378" text-anchor="middle" font-size="11" fill="#666666">(без змін)</text>

  <rect x="580" y="285" width="220" height="130" rx="10" fill="#E2EFDA" stroke="#70AD47" stroke-width="2"/>
  <text x="690" y="340" text-anchor="middle" font-size="14" fill="#1F3864">Повторне</text>
  <text x="690" y="362" text-anchor="middle" font-size="14" fill="#1F3864">вимірювання</text>

  <line x1="382" y1="350" x2="402" y2="350" stroke="#1F3864" stroke-width="2"/>
  <polygon points="402,345 410,350 402,355" fill="#1F3864"/>
  <line x1="557" y1="350" x2="577" y2="350" stroke="#1F3864" stroke-width="2"/>
  <polygon points="577,345 585,350 577,355" fill="#1F3864"/>

  <text x="450" y="455" text-anchor="middle" font-size="12" font-style="italic" fill="#404040">Порівняння приросту показників ЕГ і КГ доводить ефективність методики</text>
</svg>'''


# ---------------------------------------------------------------------------
# SVG № 4 — Кругова діаграма розподілу часу
# ---------------------------------------------------------------------------

def svg_time_donut() -> str:
    segments = [
        ("Вибір мети і завдань", 3, "#4472C4"),
        ("Зміст впливів", 5, "#70AD47"),
        ("План упровадження", 5, "#FFC000"),
        ("Критерії результативності", 5, "#ED7D31"),
        ("Структура повідомлення", 8, "#5B9BD5"),
        ("Самоперевірка", 4, "#A5A5A5"),
    ]
    total = sum(s[1] for s in segments)
    cx, cy = 270, 290
    r_out, r_in = 160, 85
    cumulative = 0
    paths = []
    labels = []
    for name, val, color in segments:
        start_deg = cumulative / total * 360
        end_deg = (cumulative + val) / total * 360
        path = _donut_segment(cx, cy, r_out, r_in, start_deg, end_deg)
        paths.append(f'<path d="{path}" fill="{color}" stroke="#FFFFFF" stroke-width="2"/>')
        mid = (start_deg + end_deg) / 2
        lx, ly = _polar(cx, cy, (r_out + r_in) / 2, mid)
        labels.append(f'<text x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">{val} хв</text>')
        cumulative += val

    legend_x = 520
    legend_y0 = 150
    legend = []
    for i, (name, val, color) in enumerate(segments):
        y = legend_y0 + i * 38
        legend.append(f'<rect x="{legend_x}" y="{y}" width="20" height="20" fill="{color}"/>')
        legend.append(f'<text x="{legend_x + 30}" y="{y + 15}" font-size="13" fill="#1F3864">{name} — {val} хв</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560" width="900" height="560">
  <style>text {{ font-family: {FONT}; }}</style>
  <rect width="900" height="560" fill="#FFFFFF"/>
  <text x="450" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F3864">Розподіл часу виконання практичного завдання (30 хв)</text>
  {''.join(paths)}
  {''.join(labels)}
  <text x="{cx}" y="{cy - 5}" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F3864">30 хв</text>
  <text x="{cx}" y="{cy + 18}" text-anchor="middle" font-size="12" fill="#404040">усього</text>
  {''.join(legend)}
</svg>'''


# ---------------------------------------------------------------------------
# SVG № 5 — Структура повідомлення студента
# ---------------------------------------------------------------------------

def svg_report_structure() -> str:
    items = [
        ("1", "Тема дослідження та актуальність", "#DEEBF7", "#4472C4"),
        ("2", "Мета і завдання формувального етапу", "#E2EFDA", "#70AD47"),
        ("3", "Зміст впливів (методи, форми, засоби)", "#FFF2CC", "#FFC000"),
        ("4", "План упровадження (етапи й терміни)", "#FCE4D6", "#ED7D31"),
        ("5", "Критерії результативності та методи фіксації", "#DEEBF7", "#4472C4"),
        ("6", "Очікувані результати та способи контролю", "#E2EFDA", "#70AD47"),
        ("7", "Висновки + список джерел", "#FFF2CC", "#FFC000"),
    ]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 640" width="820" height="640">',
             f'<style>text {{ font-family: {FONT}; }}</style>',
             '<rect width="820" height="640" fill="#FFFFFF"/>',
             '<text x="410" y="38" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F3864">Структура підсумкового повідомлення студента</text>']
    y0 = 80
    h = 62
    gap = 15
    for i, (num, text, fill, accent) in enumerate(items):
        y = y0 + i * (h + gap)
        parts.append(f'<rect x="70" y="{y}" width="680" height="{h}" rx="10" fill="{fill}" stroke="{accent}" stroke-width="2.5"/>')
        parts.append(f'<rect x="70" y="{y}" width="55" height="{h}" rx="10" fill="{accent}"/>')
        parts.append(f'<text x="97" y="{y + h/2 + 8}" text-anchor="middle" font-size="22" font-weight="bold" fill="#FFFFFF">{num}</text>')
        parts.append(f'<text x="145" y="{y + h/2 + 6}" font-size="15" fill="#1F3864">{text}</text>')
    parts.append(f'<text x="410" y="620" text-anchor="middle" font-size="12" font-style="italic" fill="#404040">Кожен блок — 2–3 речення; повідомлення = 1–1,5 сторінки</text>')
    parts.append('</svg>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# SVG № 6 — Часова шкала
# ---------------------------------------------------------------------------

def svg_timeline() -> str:
    milestones = [
        (0, "0 хв", "Старт"),
        (5, "5 хв", "Мета + завдання"),
        (10, "10 хв", "Зміст впливів"),
        (15, "15 хв", "План упровадження"),
        (20, "20 хв", "Критерії результативності"),
        (26, "26 хв", "Повідомлення"),
        (30, "30 хв", "Самоперевірка"),
    ]
    x0, x1 = 70, 840
    y = 130
    total = 30
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 280" width="900" height="280">',
             f'<style>text {{ font-family: {FONT}; }}</style>',
             '<rect width="900" height="280" fill="#FFFFFF"/>',
             '<text x="450" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F3864">Часова шкала виконання (30 хв)</text>',
             f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#1F3864" stroke-width="4"/>',
             f'<polygon points="{x1},{y-8} {x1+18},{y} {x1},{y+8}" fill="#1F3864"/>']
    for i, (t, label, name) in enumerate(milestones):
        x = x0 + (x1 - x0) * t / total
        color = "#ED7D31" if i == len(milestones) - 1 else "#4472C4"
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="11" fill="{color}" stroke="#FFFFFF" stroke-width="2"/>')
        above = (i % 2 == 0)
        if above:
            parts.append(f'<text x="{x:.1f}" y="{y - 30}" text-anchor="middle" font-size="13" font-weight="bold" fill="{color}">{label}</text>')
            parts.append(f'<text x="{x:.1f}" y="{y - 48}" text-anchor="middle" font-size="11" fill="#404040">{name}</text>')
        else:
            parts.append(f'<text x="{x:.1f}" y="{y + 30}" text-anchor="middle" font-size="13" font-weight="bold" fill="{color}">{label}</text>')
            parts.append(f'<text x="{x:.1f}" y="{y + 48}" text-anchor="middle" font-size="11" fill="#404040">{name}</text>')
    parts.append('</svg>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# Хелпери для DOCX
# ---------------------------------------------------------------------------

def set_cell_bg(cell, color_hex: str):
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


def add_bullet(doc, text):
    p = doc.add_paragraph(text, style="List Bullet")
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
        set_cell_bg(hdr[i], header_fill)
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
# Побудова документа
# ---------------------------------------------------------------------------

def build_document():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    sec = doc.sections[0]
    sec.top_margin = Cm(2)
    sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(1.5)

    # =================== ТИТУЛ ===================
    add_paragraph(doc, "ЛЕКЦІЙНЕ ЗАНЯТТЯ № 10", bold=True, size=16,
                  align=WD_ALIGN_PARAGRAPH.CENTER, color="1F3864")
    add_paragraph(doc, "з дисципліни «Основи науково-педагогічних досліджень»",
                  size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_paragraph(doc, "")
    add_paragraph(doc,
        "Тема: Побудова методики формувального етапу експерименту та її реалізація в процесі дослідження",
        bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, color="C00000")
    add_paragraph(doc, "")

    add_heading(doc, "Мета та завдання", level=1)
    add_paragraph(doc,
        "Мета: формувати вміння будувати методику формувального етапу "
        "експерименту та реалізовувати її; розвивати практичні навички "
        "впровадження формувальних впливів у освітній процес.")
    add_paragraph(doc, "Завдання:")
    add_bullet(doc, "засвоїти сутність і структуру формувального етапу експерименту;")
    add_bullet(doc, "навчитися визначати мету, критерії та показники методики;")
    add_bullet(doc, "опанувати алгоритм побудови методики формувального етапу;")
    add_bullet(doc, "розвивати вміння планувати впровадження та контролювати результати;")
    add_bullet(doc, "виховувати відповідальність за результати формувального експерименту.")

    add_paragraph(doc, "Обладнання: інструкційні картки, комп'ютер, проєктор, роздатковий матеріал.")
    add_paragraph(doc, "Тривалість: 80 хв (з них практичне завдання — 20–30 хв).")
    add_paragraph(doc, "Форма звітності: підготовлене студентом повідомлення (1–1,5 стор.) + таблиці.")

    add_heading(doc, "Рекомендована література", level=1)
    add_numbered(doc,
        "Лаппо В. В. Основи педагогічних досліджень. Івано-Франківськ: НАІР, 2016. 284 с.")
    add_numbered(doc,
        "Сисоєва С. О., Кристопчук Т. Є. Методологія науково-педагогічних досліджень. "
        "Рівне: Волинські обереги, 2013. 360 с.")

    doc.add_page_break()

    # =================== ТЕОРЕТИЧНИЙ БЛОК ===================
    add_heading(doc, "Теоретичні відомості", level=1)

    add_heading(doc, "1. Місце формувального етапу в педагогічному експерименті", level=2)
    add_paragraph(doc,
        "Педагогічний експеримент традиційно охоплює три етапи: констатувальний, "
        "формувальний і контрольний. Якщо констатувальний етап — це «діагностика» "
        "реального стану проблеми, то формувальний — це «лікування»: цілеспрямоване "
        "впровадження авторської методики з метою змінити виявлені недоліки.")

    puml_path_1 = save_svg_and_png(svg_experiment_structure(), "experiment_structure")
    add_image(doc, puml_path_1, width_cm=16,
              caption="Рис. 1. Місце формувального етапу в структурі педагогічного експерименту")

    add_paragraph(doc,
        "Формувальний етап — це основний, найтриваліший і найскладніший етап "
        "дослідження. Саме тут перевіряється робоча гіпотеза, сформульована на "
        "попередньому етапі. Від якості методики формувального етапу залежить "
        "уся наукова новизна та практична цінність дослідження.")

    add_heading(doc, "2. Сутність і структура методики формувального етапу", level=2)
    add_paragraph(doc,
        "Методика формувального етапу — це цілісна система взаємопов'язаних "
        "компонентів: мети, завдань, критеріїв, змісту впливів, етапів "
        "упровадження, методів фіксації результатів та способів контролю. "
        "Вона має відповідати певним вимогам (див. таблицю).")

    add_table(doc,
        ["Вимога", "Пояснення"],
        [
            ["Цілеспрямованість", "Усі впливи підпорядковані чітко визначеній меті"],
            ["Системність", "Впливи утворюють цілісну систему, а не набір випадкових заходів"],
            ["Наукова обґрунтованість", "Спирається на теорію та результати констатувального етапу"],
            ["Відтворюваність", "Інший дослідник може повторити методику за її описом"],
            ["Етичність", "Дотримання прав, згод, конфіденційності учасників"],
            ["Контрольованість", "Можливість фіксувати проміжні та кінцеві результати"],
        ],
        col_widths=[4.0, 11.5])

    add_paragraph(doc, "")
    add_paragraph(doc, "Схема 1. Алгоритм побудови методики формувального етапу",
                  bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    puml_path_2 = save_svg_and_png(svg_building_algorithm(), "building_algorithm")
    add_image(doc, puml_path_2, width_cm=11.5,
              caption="Рис. 2. Шість кроків побудови методики формувального етапу")

    add_heading(doc, "3. Дизайн експерименту: ЕГ і КГ", level=2)
    add_paragraph(doc,
        "Щоб довести, що зміни зумовлені саме авторською методикою, а не "
        "випадковими чинниками, дослідження організовують з двома групами: "
        "експериментальною (ЕГ) та контрольною (КГ). В ЕГ упроваджується "
        "авторська методика, у КГ — традиційне навчання. Порівняння приросту "
        "показників у двох групах і є доказом ефективності.")

    puml_path_3 = save_svg_and_png(svg_experimental_design(), "experimental_design")
    add_image(doc, puml_path_3, width_cm=16,
              caption="Рис. 3. Дизайн формувального експерименту з паралельними групами")

    add_heading(doc, "4. Реалізація та контроль", level=2)
    add_paragraph(doc,
        "Реалізація методики — це не одноразовий акт, а керований процес, що "
        "включає: підготовчий етап (підготовка вчителя, матеріалів, обладнання), "
        "основний (систематичне впровадження впливів), заключний (фіксація "
        "результатів, порівняння, коригування).")
    add_paragraph(doc, "Ключові вимоги до реалізації:", bold=True)
    add_bullet(doc, "систематичність і послідовність впливів (не епізодичні заходи);")
    add_bullet(doc, "урахування вікових та індивідуальних особливостей учасників;")
    add_bullet(doc, "фіксація проміжних результатів (після кожного етапу);")
    add_bullet(doc, "готовність до коригування методики за потреби;")
    add_bullet(doc, "дотримання етичних норм і академічної доброчесності.")

    doc.add_page_break()

    # =================== ПРАКТИЧНЕ ЗАВДАННЯ ===================
    add_heading(doc, "Практичне завдання (20–30 хв)", level=1)
    add_paragraph(doc,
        "Результат роботи: підготовлене студентом повідомлення «Методика "
        "формувального етапу експерименту з обраної теми дослідження».")

    # Діаграма часу
    puml_path_4 = save_svg_and_png(svg_time_donut(), "time_donut")
    add_image(doc, puml_path_4, width_cm=15,
              caption="Рис. 4. Розподіл часу на виконання завдань (кругова діаграма)")

    # Часова шкала
    puml_path_5 = save_svg_and_png(svg_timeline(), "timeline")
    add_image(doc, puml_path_5, width_cm=16,
              caption="Рис. 5. Часова шкала виконання (0–30 хв)")

    # Структура повідомлення
    puml_path_6 = save_svg_and_png(svg_report_structure(), "report_structure")
    add_image(doc, puml_path_6, width_cm=14.5,
              caption="Рис. 6. Структура підсумкового повідомлення")

    doc.add_page_break()

    # --- Завдання 1 ---
    add_heading(doc, "Завдання 1. Мета і завдання формувального етапу (5 хв, 6 балів)", level=2)
    add_paragraph(doc, "Сформулюйте мету й завдання формувального етапу для обраної теми дослідження.")
    add_table(doc,
        ["Поле", "Ваша відповідь"],
        [
            ["Тема дослідження", ""],
            ["Мета формувального етапу (1 речення)", ""],
            ["Завдання (3–4 пункти)", ""],
            ["Очікуваний результат", ""],
        ],
        col_widths=[6.5, 9.0])

    # --- Завдання 2 ---
    add_heading(doc, "Завдання 2. Зміст впливів (5 хв, 8 балів)", level=2)
    add_paragraph(doc, "Опишіть, що саме впроваджуватимете: методи, форми, засоби.")
    add_table(doc,
        ["Напрям впливу", "Методи / форми", "Тривалість", "Хто відповідальний"],
        [["", "", "", ""] for _ in range(4)],
        col_widths=[3.5, 5.5, 3.0, 3.5])

    # --- Завдання 3 ---
    add_heading(doc, "Завдання 3. План упровадження (5 хв, 8 балів)", level=2)
    add_paragraph(doc, "Розбийте методику на етапи з конкретними термінами.")
    add_table(doc,
        ["Етап", "Термін", "Зміст роботи", "Проміжний результат"],
        [["Підготовчий", "", "", ""],
         ["Основний", "", "", ""],
         ["Заключний", "", "", ""]],
        col_widths=[3.0, 2.5, 6.0, 4.0])

    # --- Завдання 4 ---
    add_heading(doc, "Завдання 4. Критерії результативності (5 хв, 8 балів)", level=2)
    add_paragraph(doc, "Визначте, за чим оцінюватимете ефективність методики.")
    add_table(doc,
        ["Критерій", "Показник", "Метод фіксації", "Цільове значення"],
        [["", "", "", ""] for _ in range(4)],
        col_widths=[3.5, 4.0, 4.5, 3.5])

    # --- Завдання 5 ---
    add_heading(doc, "Завдання 5. Структура повідомлення (5 хв, 6 балів)", level=2)
    add_paragraph(doc, "Заповніть структуру підсумкового повідомлення за рис. 6.")
    add_table(doc,
        ["Розділ", "Зміст (2–3 речення)"],
        [
            ["1. Тема й актуальність", ""],
            ["2. Мета і завдання форм. етапу", ""],
            ["3. Зміст впливів", ""],
            ["4. План упровадження", ""],
            ["5. Критерії результативності", ""],
            ["6. Очікувані результати", ""],
            ["7. Висновки", ""],
        ],
        col_widths=[6.0, 9.5])

    # --- Завдання 6 ---
    add_heading(doc, "Завдання 6. Самоперевірка (4 хв, 4 бали)", level=2)
    add_paragraph(doc, "Перевірте повідомлення за чек-листом:")
    add_table(doc,
        ["Критерій перевірки", "Так / Ні"],
        [
            ["Мета сформульована одним чітким реченням", ""],
            ["Завдання відображають шлях досягнення мети", ""],
            ["Впливи системні, а не епізодичні", ""],
            ["Визначено ЕГ і КГ (або обґрунтовано їх відсутність)", ""],
            ["Критерії вимірювані та мають методи фіксації", ""],
            ["План містить терміни й проміжні результати", ""],
            ["Дотримано етичних норм і академічної доброчесності", ""],
        ],
        col_widths=[13.0, 2.5])

    doc.add_page_break()

    # =================== КРИТЕРІЇ ОЦІНЮВАННЯ ===================
    add_heading(doc, "Критерії оцінювання", level=1)
    add_table(doc,
        ["Критерій", "Бали"],
        [
            ["Завдання 1. Мета і завдання форм. етапу", "6"],
            ["Завдання 2. Зміст впливів", "8"],
            ["Завдання 3. План упровадження", "8"],
            ["Завдання 4. Критерії результативності", "8"],
            ["Завдання 5. Структура повідомлення", "6"],
            ["Завдання 6. Самоперевірка", "4"],
            ["Максимальна кількість балів", "40"],
        ],
        col_widths=[12.5, 3.0])

    # =================== КОНТРОЛЬНІ ПИТАННЯ ===================
    add_heading(doc, "Контрольні запитання", level=1)
    questions = [
        "Яке місце посідає формувальний етап у структурі педагогічного експерименту?",
        "Що таке методика формувального етапу і з яких компонентів вона складається?",
        "Які вимоги висуваються до методики формувального етапу?",
        "Для чого в експерименті потрібні експериментальна і контрольна групи?",
        "Як пов'язані результати констатувального етапу з методикою формувального?",
        "Які етапи впровадження методики ви знаєте?",
        "Як фіксувати проміжні результати формувального етапу?",
        "Чому методика має бути відтворюваною?",
        "Які етичні вимоги висуваються до формувального експерименту?",
        "Як співвідносяться робоча гіпотеза і методика формувального етапу?",
    ]
    for q in questions:
        add_numbered(doc, q)

    # =================== ДОДАТОК ===================
    add_heading(doc, "Додаток. Зразок повідомлення", level=1)
    add_paragraph(doc,
        "Тема: «Використання ігрових технологій на уроках інформатики в 2 класі».",
        bold=True)
    add_paragraph(doc,
        "Мета формувального етапу: перевірити ефективність системи ігрових "
        "технологій для підвищення пізнавальної активності учнів 2 класу на "
        "уроках інформатики.")
    add_paragraph(doc, "Завдання:")
    add_bullet(doc, "розробити систему ігор для уроків інформатики у 2 класі;")
    add_bullet(doc, "упровадити систему в ЕГ протягом 8 тижнів;")
    add_bullet(doc, "порівняти динаміку показників в ЕГ і КГ.")
    add_table(doc,
        ["Етап", "Термін", "Зміст роботи"],
        [
            ["Підготовчий", "2 тижні", "Добір ігор, підготовка вчителя, узгодження з адміністрацією"],
            ["Основний", "8 тижнів", "Систематичне впровадження ігор на уроках інформатики"],
            ["Заключний", "1 тиждень", "Повторна діагностика, порівняння з КГ, висновки"],
        ],
        col_widths=[3.0, 2.5, 10.0])
    add_paragraph(doc,
        "Критерії результативності: пізнавальна активність (анкетування, "
        "спостереження), навчальні досягнення (контрольні роботи), мотивація "
        "(опитування).", italic=True)

    # =================== ЗБЕРЕЖЕННЯ ===================
    out_path = os.path.join(OUTPUT_DIR, "Лекція_10_Формувальний_етап.docx")
    doc.save(out_path)
    print(f"\n[OK] Документ збережено: {out_path}")
    print(f"[SVG] Збережено у: {SVG_DIR}")
    print(f"[PNG] Збережено у: {PNG_DIR}")
    return out_path


if __name__ == "__main__":
    build_document()