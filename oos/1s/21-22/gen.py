#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерація DOCX з HTML-сторінки практичного заняття.
- Основний шрифт: Times New Roman, 14pt
- Міжрядковий інтервал: 1.25
- Вирівнювання: по ширині (justify)
- Для команд (code, .cmd, .cmd-block) — моноширинний шрифт (Consolas/Courier New)
"""

import re
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ==================== НАЛАШТУВАННЯ ====================

HTML_FILE = "index.html"          # вхідний HTML
OUTPUT_FILE = "praktychne_zanyattya.docx"  # вихідний DOCX

MAIN_FONT = "Times New Roman"
MAIN_FONT_SIZE = Pt(14)
LINE_SPACING = 1.25

CODE_FONT = "Consolas"            # для команд; якщо немає — Courier New
CODE_FONT_FALLBACK = "Courier New"
CODE_FONT_SIZE = Pt(12)

# Кольори (як на сторінці)
COLOR_MAIN = RGBColor(0x16, 0x21, 0x2c)
COLOR_H1 = RGBColor(0x0f, 0x3d, 0x2e)
COLOR_H2 = RGBColor(0x14, 0x52, 0x39)
COLOR_H3 = RGBColor(0x1a, 0x6b, 0x46)
COLOR_CODE_TEXT = RGBColor(0xb8, 0xf0, 0xd2)
COLOR_CODE_BG = "1E2B36"          # hex без #


# ==================== ДОПОМІЖНІ ФУНКЦІЇ ====================

def set_run_font(run, name=MAIN_FONT, size=MAIN_FONT_SIZE, bold=None, italic=None, color=None):
    """Встановлює шрифт, розмір, накреслення та колір для run."""
    run.font.name = name
    run.font.size = size
    # Встановлюємо шрифт для всіх алфавітів (кирилиця, латиниця)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rFonts.set(qn('w:eastAsia'), name)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def set_paragraph_format(paragraph, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                         spacing=LINE_SPACING, space_before=Pt(0), space_after=Pt(6),
                         left_indent=None, first_line_indent=None):
    """Налаштовує формат абзацу."""
    pf = paragraph.paragraph_format
    pf.alignment = align
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = spacing
    pf.space_before = space_before
    pf.space_after = space_after
    if left_indent is not None:
        pf.left_indent = left_indent
    if first_line_indent is not None:
        pf.first_line_indent = first_line_indent


def shade_paragraph(paragraph, fill_hex):
    """Додає фон (заливку) до абзацу."""
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    pPr.append(shd)


def add_horizontal_border(paragraph, color="1F8A5B", size=12):
    """Додає нижню межу до абзацу (для заголовків)."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_left_border(paragraph, color="1F8A5B", size=24):
    """Додає ліву межу до абзацу (для цитат/виділень)."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), str(size))
    left.set(qn('w:space'), '8')
    left.set(qn('w:color'), color)
    pBdr.append(left)
    pPr.append(pBdr)


def clean_text(text):
    """Прибирає зайві пробіли та переноси."""
    if text is None:
        return ""
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ==================== ОБРОБКА INLINE-ЕЛЕМЕНТІВ ====================

def add_inline_content(paragraph, node, base_bold=False, base_italic=False):
    """
    Рекурсивно додає inline-вміст (текст, <strong>, <em>, <code>, <kbd> тощо)
    до абзацу paragraph.
    """
    if isinstance(node, NavigableString):
        text = str(node)
        if not text.strip():
            # зберігаємо пробіли між словами
            if text and paragraph.runs:
                paragraph.runs[-1].text += " "
            return
        run = paragraph.add_run(text)
        set_run_font(run, bold=base_bold or None, italic=base_italic or None,
                     color=COLOR_MAIN)
        return

    if not isinstance(node, Tag):
        return

    name = node.name.lower()

    if name in ('strong', 'b'):
        for child in node.children:
            add_inline_content(paragraph, child, base_bold=True, base_italic=base_italic)
    elif name in ('em', 'i'):
        for child in node.children:
            add_inline_content(paragraph, child, base_bold=base_bold, base_italic=True)
    elif name in ('code', 'kbd', 'samp', 'tt'):
        text = clean_text(node.get_text())
        if text:
            run = paragraph.add_run(text)
            set_run_font(run, name=CODE_FONT, size=CODE_FONT_SIZE,
                         bold=base_bold or None, italic=base_italic or None,
                         color=RGBColor(0x0d, 0x3b, 0x5c))
            # Легка заливка для inline-коду
            rPr = run._element.get_or_add_rPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), 'E7F4EE')
            rPr.append(shd)
    elif name == 'br':
        paragraph.add_run().add_break()
    elif name == 'a':
        for child in node.children:
            add_inline_content(paragraph, child, base_bold=base_bold, base_italic=base_italic)
    else:
        # невідомий тег — просто обробляємо вміст
        for child in node.children:
            add_inline_content(paragraph, child, base_bold=base_bold, base_italic=base_italic)


# ==================== ОБРОБКА БЛОКІВ ====================

def add_heading(doc, text, level):
    """Додає заголовок відповідного рівня."""
    paragraph = doc.add_paragraph()
    set_paragraph_format(paragraph, align=WD_ALIGN_PARAGRAPH.LEFT,
                         space_before=Pt(12), space_after=Pt(8))
    run = paragraph.add_run(text)
    if level == 1:
        set_run_font(run, size=Pt(20), bold=True, color=COLOR_H1)
        add_horizontal_border(paragraph)
    elif level == 2:
        set_run_font(run, size=Pt(16), bold=True, color=COLOR_H2)
        add_left_border(paragraph)
    elif level == 3:
        set_run_font(run, size=Pt(14), bold=True, color=COLOR_H3)
    else:
        set_run_font(run, size=Pt(14), bold=True, color=COLOR_H3)
    return paragraph


def add_paragraph(doc, node, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    """Додає звичайний абзац із inline-вмістом."""
    paragraph = doc.add_paragraph()
    set_paragraph_format(paragraph, align=align, first_line_indent=Cm(1.25))
    add_inline_content(paragraph, node)
    return paragraph


def add_list_item(doc, node, ordered=False, level=0):
    """Додає елемент списку."""
    paragraph = doc.add_paragraph()
    set_paragraph_format(paragraph, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                         space_after=Pt(4))
    # Відступ
    paragraph.paragraph_format.left_indent = Cm(0.75 + level * 0.75)
    paragraph.paragraph_format.first_line_indent = Cm(-0.5)
    # Маркер
    if ordered:
        # Нумерація — просто ставимо цифру (без автоматичного списку)
        marker = "• " if not ordered else ""
    else:
        marker = "• "
    if marker:
        run = paragraph.add_run(marker)
        set_run_font(run, color=COLOR_H3, bold=True)
    # Вміст
    for child in node.children:
        if isinstance(child, Tag) and child.name in ('ul', 'ol'):
            continue
        add_inline_content(paragraph, child)
    # Вкладені списки
    for child in node.children:
        if isinstance(child, Tag) and child.name in ('ul', 'ol'):
            handle_list(doc, child, level=level + 1)


def handle_list(doc, node, level=0):
    """Обробляє <ul> або <ol>."""
    ordered = node.name.lower() == 'ol'
    counter = 0
    for li in node.find_all('li', recursive=False):
        counter += 1
        paragraph = doc.add_paragraph()
        set_paragraph_format(paragraph, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                             space_after=Pt(4))
        paragraph.paragraph_format.left_indent = Cm(0.75 + level * 0.75)
        paragraph.paragraph_format.first_line_indent = Cm(-0.5)
        # Маркер
        if ordered:
            marker = f"{counter}. "
        else:
            marker = "• "
        run = paragraph.add_run(marker)
        set_run_font(run, color=COLOR_H3, bold=True)
        # Вміст li
        for child in li.children:
            if isinstance(child, Tag) and child.name in ('ul', 'ol'):
                continue
            add_inline_content(paragraph, child)
        # Вкладені списки
        for child in li.children:
            if isinstance(child, Tag) and child.name in ('ul', 'ol'):
                handle_list(doc, child, level=level + 1)


def add_code_block(doc, text):
    """Додає блок коду (темний фон, моноширинний шрифт)."""
    # Розбиваємо на рядки, кожен — окремий абзац із заливкою
    lines = text.strip('\n').split('\n')
    for i, line in enumerate(lines):
        paragraph = doc.add_paragraph()
        set_paragraph_format(paragraph, align=WD_ALIGN_PARAGRAPH.LEFT,
                             space_before=Pt(0),
                             space_after=Pt(0) if i < len(lines) - 1 else Pt(8))
        paragraph.paragraph_format.left_indent = Cm(0.5)
        shade_paragraph(paragraph, COLOR_CODE_BG)
        run = paragraph.add_run(line if line else " ")
        set_run_font(run, name=CODE_FONT, size=CODE_FONT_SIZE,
                     color=COLOR_CODE_TEXT)


def add_table(doc, table_node):
    """Додає таблицю."""
    headers = []
    rows = []
    thead = table_node.find('thead')
    if thead:
        headers = [clean_text(th.get_text()) for th in thead.find_all('th')]
    tbody = table_node.find('tbody') or table_node
    for tr in tbody.find_all('tr'):
        cells = [clean_text(td.get_text()) for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

    if not headers and not rows:
        return

    cols = max(len(headers), max((len(r) for r in rows), default=0))
    table = doc.add_table(rows=0, cols=cols)
    table.style = 'Table Grid'

    # Заголовки
    if headers:
        row_cells = table.add_row().cells
        for i, h in enumerate(headers):
            if i >= cols:
                break
            cell = row_cells[i]
            cell.text = ""
            p = cell.paragraphs[0]
            set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.LEFT,
                                 space_before=Pt(2), space_after=Pt(2))
            run = p.add_run(h)
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff))
            # Заливка заголовка
            tcPr = cell._tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), '0F3D2E')
            tcPr.append(shd)

    # Дані
    for r in rows:
        row_cells = table.add_row().cells
        for i, val in enumerate(r):
            if i >= cols:
                break
            cell = row_cells[i]
            cell.text = ""
            p = cell.paragraphs[0]
            set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.LEFT,
                                 space_before=Pt(2), space_after=Pt(2))
            # Якщо в клітинці код — моноширинний шрифт
            run = p.add_run(val)
            if re.match(r'^[A-Za-z0-9_\-\.\\/:<>\[\] ]+$', val) and any(
                    c in val for c in ['DIR', 'COPY', 'CD', 'MD', 'RD', 'TYPE',
                                        'FIND', 'DEL', 'REN', 'cls', 'time', 'date',
                                        'format', 'FORMAT', 'MORE', 'EDIT', 'copy',
                                        'find', 'type', 'more', 'edit', 'del', 'ren']):
                set_run_font(run, name=CODE_FONT, size=Pt(11), color=COLOR_MAIN)
            else:
                set_run_font(run, color=COLOR_MAIN)
    doc.add_paragraph()


def add_callout(doc, node, border_color="1F8A5B", fill="E7F4EE"):
    """Додає кольоровий блок-виділення (highlight, note, meta-info)."""
    # Збираємо весь вміст у один блок з заливкою
    for child in node.children:
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if not text:
                continue
            p = doc.add_paragraph()
            set_paragraph_format(p, space_after=Pt(2))
            p.paragraph_format.left_indent = Cm(0.5)
            shade_paragraph(p, fill)
            add_left_border(p, color=border_color)
            run = p.add_run(text)
            set_run_font(run, color=COLOR_MAIN)
        elif isinstance(child, Tag):
            if child.name in ('p',):
                p = doc.add_paragraph()
                set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                                     space_after=Pt(2))
                p.paragraph_format.left_indent = Cm(0.5)
                shade_paragraph(p, fill)
                add_left_border(p, color=border_color)
                add_inline_content(p, child)
            elif child.name in ('ul', 'ol'):
                handle_list(doc, child)
            elif child.name in ('ol',):
                handle_list(doc, child)
            else:
                p = doc.add_paragraph()
                set_paragraph_format(p, space_after=Pt(2))
                p.paragraph_format.left_indent = Cm(0.5)
                shade_paragraph(p, fill)
                add_left_border(p, color=border_color)
                add_inline_content(p, child)


def add_level_block(doc, node):
    """Додає блок рівня складності (level)."""
    # Заголовок рівня
    header = node.find(class_='level-header')
    badge = node.find(class_='level-badge')
    title = node.find(class_='level-title')
    time_el = node.find(class_='level-time')

    if badge or title:
        p = doc.add_paragraph()
        set_paragraph_format(p, space_before=Pt(10), space_after=Pt(4))
        if badge:
            badge_text = clean_text(badge.get_text()).upper()
            run = p.add_run(f"[{badge_text}] ")
            set_run_font(run, bold=True, color=COLOR_H2, size=Pt(13))
        if title:
            run = p.add_run(clean_text(title.get_text()))
            set_run_font(run, bold=True, color=COLOR_H1, size=Pt(13))
        if time_el:
            run = p.add_run(f"  {clean_text(time_el.get_text())}")
            set_run_font(run, italic=True, size=Pt(11),
                         color=RGBColor(0x5a, 0x6f, 0x7e))

    # Вміст (списки)
    for child in node.children:
        if isinstance(child, Tag) and child.name in ('ol', 'ul'):
            handle_list(doc, child)


def add_form(doc, node):
    """Додає форму звіту (поля як підкреслені лінії)."""
    h3 = node.find('h3')
    if h3:
        add_heading(doc, clean_text(h3.get_text()), 3)

    for group in node.find_all(class_='form-group'):
        label = group.find('label')
        if label:
            p = doc.add_paragraph()
            set_paragraph_format(p, space_before=Pt(6), space_after=Pt(2))
            run = p.add_run(clean_text(label.get_text()))
            set_run_font(run, bold=True, color=COLOR_H2)

        # Поле вводу
        input_el = group.find(['input', 'textarea', 'select'])
        if input_el:
            p = doc.add_paragraph()
            set_paragraph_format(p, space_after=Pt(4))
            run = p.add_run("_" * 70)
            set_run_font(run, color=RGBColor(0x9a, 0xaa, 0xb5))

        # Радіокнопки
        radios = group.find_all('input', {'type': 'radio'})
        if radios:
            p = doc.add_paragraph()
            set_paragraph_format(p, space_after=Pt(4))
            for r in radios:
                parent_label = r.find_parent('label')
                text = clean_text(parent_label.get_text()) if parent_label else ""
                run = p.add_run(f"☐ {text}    ")
                set_run_font(run, color=COLOR_MAIN)


def add_report_form_static(doc):
    """Додає статичну форму звіту, якщо в HTML її не знайдено."""
    add_heading(doc, "Форма звіту про виконання практичного заняття", 3)
    fields = [
        "Прізвище та ім'я студента",
        "Група",
        "Дата виконання",
        "Виконаний рівень складності",
        "Чи вдалося виконати всі завдання",
        "Які команди використовували у роботі",
        "Отримані результати",
        "Труднощі та запитання",
        "Висновки",
    ]
    for f in fields:
        p = doc.add_paragraph()
        set_paragraph_format(p, space_before=Pt(6), space_after=Pt(2))
        run = p.add_run(f + ":")
        set_run_font(run, bold=True, color=COLOR_H2)
        p2 = doc.add_paragraph()
        set_paragraph_format(p2, space_after=Pt(6))
        run = p2.add_run("_" * 70)
        set_run_font(run, color=RGBColor(0x9a, 0xaa, 0xb5))


# ==================== ГОЛОВНА ФУНКЦІЯ ====================

def process_node(doc, node):
    """Рекурсивно обробляє вузол HTML."""
    if isinstance(node, NavigableString):
        text = str(node).strip()
        if text:
            p = doc.add_paragraph()
            set_paragraph_format(p)
            run = p.add_run(text)
            set_run_font(run)
        return

    if not isinstance(node, Tag):
        return

    name = node.name.lower()
    classes = node.get('class', [])
    class_str = ' '.join(classes) if classes else ''

    # Пропускаємо службові елементи
    if name in ('style', 'script', 'head', 'meta', 'title', 'link'):
        return

    # Заголовки
    if name == 'h1':
        add_heading(doc, clean_text(node.get_text()), 1)
        return
    if name == 'h2':
        add_heading(doc, clean_text(node.get_text()), 2)
        return
    if name == 'h3':
        add_heading(doc, clean_text(node.get_text()), 3)
        return
    if name in ('h4', 'h5', 'h6'):
        add_heading(doc, clean_text(node.get_text()), 4)
        return

    # Кодові блоки
    if 'cmd-block' in class_str:
        add_code_block(doc, node.get_text())
        return

    # Рівні складності
    if 'level' in class_str and 'level-header' not in class_str:
        add_level_block(doc, node)
        return

    # Кольорові виділення
    if 'highlight' in class_str or 'note' in class_str or 'meta-info' in class_str:
        if 'highlight-green' in class_str:
            add_callout(doc, node, border_color="1F8A5B", fill="E7F4EE")
        elif 'highlight' in class_str:
            add_callout(doc, node, border_color="E0B64A", fill="FDF8EC")
        elif 'note' in class_str:
            add_callout(doc, node, border_color="1F8A5B", fill="E7F4EE")
        elif 'meta-info' in class_str:
            add_callout(doc, node, border_color="1F8A5B", fill="E7F4EE")
        return

    # Блоки завдань
    if 'task-box' in class_str:
        h3 = node.find('h3')
        if h3:
            add_heading(doc, clean_text(h3.get_text()), 3)
        for child in node.children:
            if isinstance(child, Tag) and child.name in ('ol', 'ul'):
                handle_list(doc, child)
        return

    # Контрольні запитання
    if 'questions' in class_str:
        h3 = node.find('h3')
        if h3:
            add_heading(doc, clean_text(h3.get_text()), 3)
        for child in node.children:
            if isinstance(child, Tag) and child.name in ('ol', 'ul'):
                handle_list(doc, child)
        return

    # Форма звіту
    if 'report-form' in class_str:
        add_form(doc, node)
        return

    # Шапка коледжу
    if 'college-header' in class_str:
        for child in node.children:
            if isinstance(child, Tag) and 'institution' in ' '.join(child.get('class', [])):
                p = doc.add_paragraph()
                set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(2))
                run = p.add_run(clean_text(child.get_text()))
                set_run_font(run, bold=True, color=COLOR_H2, size=Pt(11))
            elif isinstance(child, Tag) and 'discipline' in ' '.join(child.get('class', [])):
                p = doc.add_paragraph()
                set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(10))
                run = p.add_run(clean_text(child.get_text()))
                set_run_font(run, bold=True, color=COLOR_H1, size=Pt(12))
        return

    # Таблиці
    if name == 'table':
        add_table(doc, node)
        return

    # Списки
    if name in ('ul', 'ol'):
        handle_list(doc, node)
        return

    # Абзаци
    if name == 'p':
        # Перевірка, чи не порожній абзац
        text = clean_text(node.get_text())
        if not text and not node.find(['code', 'kbd']):
            return
        # Абзац із кодом всередині
        if node.find('code') or node.find('kbd'):
            p = doc.add_paragraph()
            set_paragraph_format(p)
            add_inline_content(p, node)
            return
        add_paragraph(doc, node)
        return

    # Невідомі теги — обробляємо вміст
    for child in node.children:
        process_node(doc, child)


def main():
    # Читаємо HTML
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'lxml')

    # Створюємо документ
    doc = Document()

    # Налаштовуємо базовий стиль Normal
    style = doc.styles['Normal']
    style.font.name = MAIN_FONT
    style.font.size = MAIN_FONT_SIZE
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), MAIN_FONT)
    rFonts.set(qn('w:hAnsi'), MAIN_FONT)
    rFonts.set(qn('w:cs'), MAIN_FONT)
    rFonts.set(qn('w:eastAsia'), MAIN_FONT)

    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    style.paragraph_format.line_spacing = LINE_SPACING

    # Поля сторінки
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)

    # Знаходимо контейнер
    container = soup.find(class_='container')
    if container is None:
        container = soup.body or soup

    # Обробляємо всі дочірні елементи
    for child in container.children:
        process_node(doc, child)

    # Якщо форма звіту не знайдена — додаємо статичну
    if not soup.find(class_='report-form'):
        add_report_form_static(doc)

    # Зберігаємо
    doc.save(OUTPUT_FILE)
    print(f"✅ Документ збережено: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()