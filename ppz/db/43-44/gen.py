#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import zlib
import logging
import random

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
    print("Потрібен python-docx: pip install python-docx"); sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Потрібен Pillow: pip install pillow"); sys.exit(1)

# ==================== КОНФІГУРАЦІЯ ====================
FONT_NAME      = "Times New Roman"
FONT_SIZE      = Pt(14)
CODE_FONT_SIZE = Pt(10)
TABLE_FONT     = 11
LINE_SPACING   = 1.25
OUTPUT_FILE    = "Практичне_заняття_12_БД.docx"
IMG_DIR        = "img"
SKIP_DIAGRAMS  = False

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


# ==================== ШРИФТИ ДЛЯ PIL ====================

def get_font(size, bold=False):
    for name in (("arialbd.ttf" if bold else "arial.ttf"),
                 ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


# ==================== ДОПОМІЖНІ ФУНКЦІЇ МАЛЮВАННЯ ====================

def draw_window_frame(draw, w, h, title):
    draw.rectangle([0, 0, w - 1, h - 1], fill="#F5F5F5", outline="#666", width=2)
    draw.rectangle([2, 2, w - 3, 30], fill="#4A6B8A")
    draw.text((12, 8), title, fill="white", font=get_font(12, bold=True))
    for i, ch in enumerate("— □ ✕"):
        draw.text((w - 95 + i * 30, 8), ch, fill="white", font=get_font(11))
    draw.rectangle([2, 30, w - 3, 55], fill="#EAEAEA")
    x = 15
    for m in ["Файл", "Редагування", "Вигляд", "Вставка", "Інструменти", "Вікно", "Довідка"]:
        draw.text((x, 36), m, fill="#333", font=get_font(10))
        x += 78
    draw.rectangle([2, 55, w - 3, 82], fill="#DCDCDC")
    for i in range(10):
        draw.rectangle([10 + i * 32, 60, 34 + i * 32, 77], fill="#BFBFBF", outline="#999")


def draw_button(draw, x, y, w, h, text, primary=False):
    fill = "#4A6B8A" if primary else "#E5E5E5"
    color = "white" if primary else "#333"
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline="#888")
    try:
        bbox = draw.textbbox((0, 0), text, font=get_font(10))
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        tw, th = len(text) * 6, 12
    draw.text((x + (w - tw) // 2, y + (h - th) // 2 - 2),
              text, fill=color, font=get_font(10))


# ==================== UI-МАКЕТИ ====================

def make_main_window(path):
    W, H = 820, 540
    img = Image.new("RGB", (W, H), "#F5F5F5")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, W, H, "LibreOffice Base — Прізвище_ПЗ12_бібліотека.odb")
    draw.rectangle([15, 95, 260, H - 15], fill="white", outline="#BBB")
    draw.text((25, 102), "База даних", fill="#333", font=get_font(11, bold=True))
    draw.line([15, 122, 260, 122], fill="#BBB")
    for i, o in enumerate(["📋  Таблиці", "🔍  Запити", "📝  Форми", "📊  Звіти"]):
        y = 132 + i * 28
        if i == 0:
            draw.rectangle([20, y - 3, 255, y + 20], fill="#DCE7F3")
        draw.text((30, y), o, fill="#333", font=get_font(11))
    draw.rectangle([275, 95, W - 15, H - 15], fill="white", outline="#BBB")
    draw.text((295, 115), "Вітаємо у LibreOffice Base!",
              fill="#4A6B8A", font=get_font(15, bold=True))
    draw.text((295, 150), "Виберіть тип об'єкта на лівій панелі.",
              fill="#555", font=get_font(11))
    for i, t in enumerate([
        "• Створити таблицю (майстер або вручну)",
        "• Створити форму для введення даних",
        "• Побудувати запит для вибірки",
        "• Сформувати звіт для друку",
        "• Імпортувати дані з Excel / CSV",
        "• Експортувати у .ods, .csv, .pdf",
    ]):
        draw.text((305, 200 + i * 22), t, fill="#555", font=get_font(10))
    img.save(path)


def make_table_wizard(path):
    W, H = 820, 540
    img = Image.new("RGB", (W, H), "#F5F5F5")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, W, H, "LibreOffice Base — Майстер створення таблиці")
    dx, dy, dw, dh = 60, 95, 700, H - 115
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill="white", outline="#666", width=2)
    draw.rectangle([dx, dy, dx + dw, dy + 30], fill="#4A6B8A")
    draw.text((dx + 12, dy + 8), "Майстер створення таблиці",
              fill="white", font=get_font(12, bold=True))
    draw.text((dx + 20, dy + 45),
              "Крок 1 із 3. Вибір категорії та зразка",
              fill="#333", font=get_font(11, bold=True))
    draw.text((dx + 20, dy + 80), "Категорія:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 110, dy + 76, dx + 400, dy + 100], fill="white", outline="#888")
    draw.text((dx + 118, dy + 80), "Бізнес ▼", fill="#333", font=get_font(11))
    draw.text((dx + 20, dy + 120), "Зразки таблиць:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 20, dy + 145, dx + 260, dy + 290], fill="white", outline="#888")
    for i, t in enumerate(["Книги", "Клієнти", "Замовлення",
                           "Співробітники", "Товари", "Рахунки"]):
        y = dy + 150 + i * 22
        if t == "Книги":
            draw.rectangle([dx + 22, y - 2, dx + 258, y + 20], fill="#DCE7F3")
        draw.text((dx + 30, y), t, fill="#333", font=get_font(10))
    draw.text((dx + 290, dy + 120), "Поля таблиці «Книги»:",
              fill="#333", font=get_font(11))
    draw.rectangle([dx + 290, dy + 145, dx + 520, dy + 290], fill="#F9F9F9", outline="#888")
    for i, f in enumerate(["Код_книги   (INTEGER, ключ)",
                           "Назва       (VARCHAR)",
                           "Автор       (VARCHAR)",
                           "Рік_видання (INTEGER)"]):
        draw.text((dx + 300, dy + 152 + i * 22), "• " + f, fill="#333", font=get_font(10))
    btn_y = dy + dh - 40
    draw_button(draw, dx + dw - 230, btn_y, 95, 28, "Скасувати")
    draw_button(draw, dx + dw - 130, btn_y, 115, 28, "Далі →", primary=True)
    img.save(path)


def make_table_wizard_fields(path):
    W, H = 820, 540
    img = Image.new("RGB", (W, H), "#F5F5F5")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, W, H, "LibreOffice Base — Майстер створення таблиці")
    dx, dy, dw, dh = 60, 95, 700, H - 115
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill="white", outline="#666", width=2)
    draw.rectangle([dx, dy, dx + dw, dy + 30], fill="#4A6B8A")
    draw.text((dx + 12, dy + 8), "Майстер створення таблиці",
              fill="white", font=get_font(12, bold=True))
    draw.text((dx + 20, dy + 45),
              "Крок 2 із 3. Вибір полів",
              fill="#333", font=get_font(11, bold=True))
    draw.text((dx + 20, dy + 80), "Доступні поля:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 20, dy + 105, dx + 280, dy + 290], fill="white", outline="#888")
    for i, f in enumerate(["Код_книги", "Назва", "Автор", "Рік_видання",
                           "Жанр", "ISBN", "Кількість", "Ціна", "Анотація"]):
        draw.text((dx + 30, dy + 112 + i * 20), f, fill="#333", font=get_font(10))
    draw_button(draw, dx + 295, dy + 155, 35, 28, "→", primary=True)
    draw_button(draw, dx + 295, dy + 195, 35, 28, "←")
    draw.text((dx + 345, dy + 80), "Поля нової таблиці:",
              fill="#333", font=get_font(11))
    draw.rectangle([dx + 345, dy + 105, dx + 620, dy + 290], fill="#F9F9F9", outline="#888")
    for i, f in enumerate(["Код_книги", "Назва", "Автор", "Рік_видання"]):
        draw.text((dx + 355, dy + 112 + i * 20), "• " + f, fill="#333", font=get_font(10))
    btn_y = dy + dh - 40
    draw_button(draw, dx + dw - 340, btn_y, 95, 28, "← Назад")
    draw_button(draw, dx + dw - 230, btn_y, 95, 28, "Скасувати")
    draw_button(draw, dx + dw - 130, btn_y, 115, 28, "Готово", primary=True)
    img.save(path)


def make_form_wizard(path):
    W, H = 820, 540
    img = Image.new("RGB", (W, H), "#F5F5F5")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, W, H, "LibreOffice Base — Майстер форм")
    dx, dy, dw, dh = 60, 95, 700, H - 115
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill="white", outline="#666", width=2)
    draw.rectangle([dx, dy, dx + dw, dy + 30], fill="#4A6B8A")
    draw.text((dx + 12, dy + 8), "Майстер форм", fill="white", font=get_font(12, bold=True))
    draw.text((dx + 20, dy + 45),
              "Крок 1 із 8. Вибір таблиці та полів",
              fill="#333", font=get_font(11, bold=True))
    draw.text((dx + 20, dy + 80), "Таблиця:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 100, dy + 76, dx + 340, dy + 100], fill="white", outline="#888")
    draw.text((dx + 108, dy + 80), "Учні ▼", fill="#333", font=get_font(11))
    draw.text((dx + 20, dy + 125), "Доступні поля:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 20, dy + 150, dx + 260, dy + 290], fill="white", outline="#888")
    for i, f in enumerate(["Код_учня", "Прізвище", "Ім'я", "Клас", "Телефон"]):
        draw.text((dx + 30, dy + 158 + i * 22), f, fill="#333", font=get_font(10))
    draw_button(draw, dx + 275, dy + 190, 35, 28, "→", primary=True)
    draw_button(draw, dx + 275, dy + 230, 35, 28, "←")
    draw.text((dx + 325, dy + 125), "Поля форми:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 325, dy + 150, dx + 560, dy + 290], fill="#F9F9F9", outline="#888")
    for i, f in enumerate(["Код_учня", "Прізвище", "Ім'я", "Клас", "Телефон"]):
        draw.text((dx + 335, dy + 158 + i * 22), "• " + f, fill="#333", font=get_font(10))
    draw.text((dx + 20, dy + 320),
              "Наступні кроки: субформа → макет → стиль → назва «Форма_Учні»",
              fill="#666", font=get_font(10, bold=True))
    btn_y = dy + dh - 40
    draw_button(draw, dx + dw - 230, btn_y, 95, 28, "Скасувати")
    draw_button(draw, dx + dw - 130, btn_y, 115, 28, "Далі →", primary=True)
    img.save(path)


def make_completed_form(path):
    W, H = 820, 540
    img = Image.new("RGB", (W, H), "#F5F5F5")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, W, H, "LibreOffice Base — Форма_Учні")
    draw.rectangle([15, 95, W - 15, 130], fill="#EAEAEA", outline="#BBB")
    draw.text((25, 103), "Запис  1  із  25", fill="#333", font=get_font(11, bold=True))
    for i, ch in enumerate(["◀", "▶", "◀|", "|▶", "+", "✕"]):
        draw_button(draw, W - 220 + i * 34, 101, 30, 24, ch)
    draw.rectangle([15, 140, W - 15, H - 15], fill="white", outline="#BBB")
    draw.text((35, 155), "Картка учня", fill="#4A6B8A", font=get_font(15, bold=True))
    draw.line([35, 180, W - 35, 180], fill="#DDD")
    fields = [("Код учня:", "1001"), ("Прізвище:", "Шевченко"),
              ("Ім'я:", "Тарас"), ("Клас:", "10-А"),
              ("Телефон:", "+380 67 123 45 67")]
    for i, (label, value) in enumerate(fields):
        y = 200 + i * 55
        draw.text((50, y + 5), label, fill="#333", font=get_font(11, bold=True))
        draw.rectangle([220, y, 550, y + 32], fill="#F8F8F8", outline="#888")
        draw.text((230, y + 8), value, fill="#222", font=get_font(11))
    btn_y = H - 55
    draw_button(draw, 50, btn_y, 100, 30, "◀ Попередній")
    draw_button(draw, 160, btn_y, 100, 30, "Наступний ▶")
    draw_button(draw, 270, btn_y, 110, 30, "Новий запис", primary=True)
    draw_button(draw, 390, btn_y, 100, 30, "Зберегти")
    img.save(path)


def make_report_wizard(path):
    W, H = 820, 540
    img = Image.new("RGB", (W, H), "#F5F5F5")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, W, H, "LibreOffice Base — Майстер звітів")
    dx, dy, dw, dh = 60, 95, 700, H - 115
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill="white", outline="#666", width=2)
    draw.rectangle([dx, dy, dx + dw, dy + 30], fill="#4A6B8A")
    draw.text((dx + 12, dy + 8), "Майстер звітів", fill="white", font=get_font(12, bold=True))
    draw.text((dx + 20, dy + 45),
              "Крок 5 із 7. Вибір макета звіту",
              fill="#333", font=get_font(11, bold=True))
    layouts = [("Табличний", "Поля у вигляді таблиці", True),
               ("Стовпчиковий", "Кожне поле — окремим рядком", False),
               ("У два стовпці", "Двоколонковий макет", False)]
    for i, (name, desc, sel) in enumerate(layouts):
        y = dy + 80 + i * 65
        fill = "#DCE7F3" if sel else "#F8F8F8"
        draw.rectangle([dx + 20, y, dx + 600, y + 55], fill=fill, outline="#888")
        draw.text((dx + 40, y + 10), name, fill="#333", font=get_font(12, bold=True))
        draw.text((dx + 40, y + 32), desc, fill="#666", font=get_font(10))
        if sel:
            draw.text((dx + 570, y + 18), "✓", fill="#4A6B8A", font=get_font(16, bold=True))
    draw.text((dx + 20, dy + 290), "Макет:", fill="#333", font=get_font(10, bold=True))
    draw.rectangle([dx + 20, dy + 310, dx + 600, dy + 350], fill="#F8F8F8", outline="#DDD")
    draw.text((dx + 30, dy + 320),
              "| Прізвище | Назва | Дата видачі | Дата повернення |",
              fill="#555", font=get_font(10))
    btn_y = dy + dh - 40
    draw_button(draw, dx + dw - 340, btn_y, 95, 28, "← Назад")
    draw_button(draw, dx + dw - 230, btn_y, 95, 28, "Скасувати")
    draw_button(draw, dx + dw - 130, btn_y, 115, 28, "Далі →", primary=True)
    img.save(path)


def make_import_dialog(path):
    W, H = 820, 540
    img = Image.new("RGB", (W, H), "#F5F5F5")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, W, H, "LibreOffice Base — Імпорт даних")
    dx, dy, dw, dh = 60, 95, 700, H - 115
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill="white", outline="#666", width=2)
    draw.rectangle([dx, dy, dx + dw, dy + 30], fill="#4A6B8A")
    draw.text((dx + 12, dy + 8), "Імпорт даних зі стороннього файлу",
              fill="white", font=get_font(12, bold=True))
    draw.text((dx + 20, dy + 45), "Крок 1. Вибір файлу-джерела",
              fill="#333", font=get_font(11, bold=True))
    draw.text((dx + 20, dy + 80), "Файл:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 90, dy + 76, dx + 500, dy + 102], fill="#F8F8F8", outline="#888")
    draw.text((dx + 100, dy + 82), "C:\\Документи\\нові_учні.xlsx",
              fill="#333", font=get_font(10))
    draw_button(draw, dx + 515, dy + 76, 100, 26, "Огляд…", primary=True)
    draw.text((dx + 20, dy + 120), "Тип файлу:", fill="#333", font=get_font(11))
    draw.rectangle([dx + 120, dy + 116, dx + 400, dy + 140], fill="white", outline="#888")
    draw.text((dx + 128, dy + 120), "Електронна таблиця Excel (*.xlsx) ▼",
              fill="#333", font=get_font(10))
    draw.text((dx + 20, dy + 170), "Крок 2. Попередній перегляд",
              fill="#333", font=get_font(11, bold=True))
    draw.rectangle([dx + 20, dy + 200, dx + 620, dy + 370], fill="white", outline="#888")
    headers = ["Код_учня", "Прізвище", "Ім'я", "Клас", "Телефон"]
    for i, h in enumerate(headers):
        x = dx + 25 + i * 120
        draw.rectangle([x, dy + 205, x + 118, dy + 228], fill="#DCE7F3")
        draw.text((x + 5, dy + 210), h, fill="#333", font=get_font(10, bold=True))
    rows = [["1010", "Іваненко", "Олена", "10-Б", "+380 66 111 22 33"],
            ["1011", "Петренко", "Максим", "10-А", "+380 50 222 33 44"],
            ["1012", "Коваленко", "Анна", "11-А", "+380 97 333 44 55"]]
    for r, row in enumerate(rows):
        y = dy + 230 + r * 22
        for c, val in enumerate(row):
            x = dx + 25 + c * 120
            draw.text((x + 5, y + 4), val, fill="#333", font=get_font(10))
    draw.text((dx + 20, dy + 380), "3 рядки буде додано до таблиці «Учні»",
              fill="#666", font=get_font(10))
    btn_y = dy + dh - 40
    draw_button(draw, dx + dw - 340, btn_y, 95, 28, "← Назад")
    draw_button(draw, dx + dw - 230, btn_y, 95, 28, "Скасувати")
    draw_button(draw, dx + dw - 130, btn_y, 115, 28, "Імпортувати", primary=True)
    img.save(path)


# ==================== PLANTUML ====================

def encode_plantuml(text):
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    data = compressor.compress(text.encode("utf-8")) + compressor.flush()
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    out = ""
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        if len(chunk) == 3:
            b1, b2, b3 = chunk
            out += alphabet[b1 >> 2]
            out += alphabet[((b1 & 0x3) << 4) | (b2 >> 4)]
            out += alphabet[((b2 & 0xF) << 2) | (b3 >> 6)]
            out += alphabet[b3 & 0x3F]
        elif len(chunk) == 2:
            b1, b2 = chunk
            out += alphabet[b1 >> 2]
            out += alphabet[((b1 & 0x3) << 4) | (b2 >> 4)]
            out += alphabet[(b2 & 0xF) << 2]
        elif len(chunk) == 1:
            b1 = chunk[0]
            out += alphabet[b1 >> 2]
            out += alphabet[(b1 & 0x3) << 4]
    return out


def download_plantuml(source, path):
    encoded = encode_plantuml(source)
    url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    try:
        log.info(f"  ↳ {os.path.basename(path)}")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        if not r.content.startswith(b"\x89PNG"):
            log.error("  ↳ отримано не PNG"); return False
        with open(path, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        log.error(f"  ↳ помилка: {e}"); return False


PUML_ERD = """@startuml
skinparam linetype ortho
skinparam entity {
  BackgroundColor #DBEAFE
  BorderColor #2563EB
}
entity "Книги" {
  * Код_книги : INTEGER <<PK>>
  --
  Назва : VARCHAR
  Автор : VARCHAR
  Рік_видання : INTEGER
}
entity "Учні" {
  * Код_учня : INTEGER <<PK>>
  --
  Прізвище : VARCHAR
  Ім'я : VARCHAR
  Клас : VARCHAR
  Телефон : VARCHAR
}
entity "Видача" {
  * Код_видачі : INTEGER <<PK>>
  --
  Код_книги : INTEGER <<FK>>
  Код_учня : INTEGER <<FK>>
  Дата_видачі : DATE
  Дата_повернення : DATE
}
Книги ||--o{ Видача
Учні ||--o{ Видача
@enduml"""

PUML_USECASE = """@startuml
skinparam usecase {
  BackgroundColor #FEF3C7
  BorderColor #D97706
}
skinparam actor {
  BackgroundColor #DCFCE7
  BorderColor #16A34A
}
left to right direction
actor "Учень БД" as U
rectangle "LibreOffice Base" {
  usecase "Створити таблицю (майстер)" as UC1
  usecase "Створити форму (майстер)" as UC2
  usecase "Створити запит (майстер)" as UC3
  usecase "Створити звіт (майстер)" as UC4
  usecase "Імпортувати дані" as UC5
  usecase "Експортувати дані" as UC6
  usecase "Спільний доступ" as UC7
}
U --> UC1
U --> UC2
U --> UC3
U --> UC4
U --> UC5
U --> UC6
U --> UC7
UC2 ..> UC1
UC3 ..> UC1
UC4 ..> UC3
UC6 ..> UC3
@enduml"""

PUML_IMPORT = """@startuml
skinparam activity {
  BackgroundColor #DBEAFE
  BorderColor #2563EB
  DiamondBackgroundColor #EDE9FE
  DiamondBorderColor #7C3AED
}
start
:Файл → Відкрити;
:Вибрати .xlsx / .csv / .ods;
:Попередній перегляд;
if (Дані коректні?) then (Так)
  :Вибрати цільову таблицю;
  :Налаштувати типи полів;
  :Імпортувати;
  :Перевірити результат;
else (Ні)
  :Виправити джерело;
endif
stop
@enduml"""

PUML_REPORT = """@startuml
skinparam activity {
  BackgroundColor #FEF3C7
  BorderColor #D97706
  DiamondBackgroundColor #FDE68A
  DiamondBorderColor #D97706
}
start
:Звіти → Майстер звітів;
:Вибір джерела;
:Вибір полів;
:Групування;
:Сортування;
:Макет;
:Стиль;
:Назва звіту;
:Готово;
:Експорт у PDF;
stop
@enduml"""


# ==================== СТИЛІ DOCX ====================

def _set_font_on_rpr(rpr, name):
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), name)


def setup_styles(doc):
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


def add_para(doc, text="", bold=False, italic=False, size=None,
             align=None, space_after=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold; run.italic = italic
    if size: run.font.size = Pt(size)
    if align is not None: p.alignment = align
    if space_after is not None: p.paragraph_format.space_after = Pt(space_after)
    return p


def add_table(doc, headers, rows, font_size=TABLE_FONT, fill_empty=False):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
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
        p.paragraph_format.line_spacing = LINE_SPACING
        p.paragraph_format.space_after = Pt(4)
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "4")
        bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), "AAAAAA")
        pBdr.append(bottom)
        pPr.append(pBdr)


def add_image(doc, path, caption="", width=5.5):
    if not os.path.exists(path):
        add_para(doc, f"[Зображення недоступне: {os.path.basename(path)}]",
                 italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    try:
        p.add_run().add_picture(path, width=Inches(width))
    except Exception as e:
        log.error(f"Не вдалося вставити {path}: {e}")
        return
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cp.add_run(caption)
        run.italic = True
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


def add_answer_box(doc, text, label="Очікувана відповідь:"):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F0FDF4")
    pPr.append(shd)
    r1 = p.add_run(label + " ")
    r1.bold = True; r1.font.size = Pt(11)
    r1.font.color.rgb = RGBColor(0x16, 0x65, 0x34)
    r2 = p.add_run(text)
    r2.font.size = Pt(11)
    r2.font.color.rgb = RGBColor(0x16, 0x65, 0x34)
    return p


# ==================== ГЕНЕРАЦІЯ ЗОБРАЖЕНЬ ====================

def generate_images():
    os.makedirs(IMG_DIR, exist_ok=True)
    log.info("Малюю UI-макети…")
    make_main_window(os.path.join(IMG_DIR, "01_main_window.png"))
    make_table_wizard(os.path.join(IMG_DIR, "02_table_wizard.png"))
    make_table_wizard_fields(os.path.join(IMG_DIR, "03_table_wizard_fields.png"))
    make_form_wizard(os.path.join(IMG_DIR, "04_form_wizard.png"))
    make_completed_form(os.path.join(IMG_DIR, "05_completed_form.png"))
    make_report_wizard(os.path.join(IMG_DIR, "06_report_wizard.png"))
    make_import_dialog(os.path.join(IMG_DIR, "07_import_dialog.png"))
    if not SKIP_DIAGRAMS:
        log.info("Завантажую UML-діаграми…")
        download_plantuml(PUML_ERD, os.path.join(IMG_DIR, "uml_erd.png"))
        download_plantuml(PUML_USECASE, os.path.join(IMG_DIR, "uml_usecase.png"))
        download_plantuml(PUML_IMPORT, os.path.join(IMG_DIR, "uml_import.png"))
        download_plantuml(PUML_REPORT, os.path.join(IMG_DIR, "uml_report.png"))


# ==================== КОНТЕНТ ДОКУМЕНТА ====================

def build_title(doc):
    add_para(doc, "", space_after=60)
    add_para(doc, "ПРАКТИЧНЕ ЗАНЯТТЯ № 12", bold=True, size=20,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "Створення таблиць, форм, запитів і звітів "
                  "за допомогою майстрів", bold=True, size=15,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, "Обмін даними між СКБД та іншими програмами. "
                  "Спільне використання бази даних", italic=True, size=13,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    add_para(doc, "Мета:", bold=True)
    add_para(doc, "Навчати комплексно створювати об'єкти БД майстрами, "
                  "імпортувати/експортувати дані (Excel, текст, XML), "
                  "налаштовувати спільний доступ. Розвивати інтегральне "
                  "мислення, вміння бачити систему в цілому. Виховувати "
                  "відповідальність при спільному доступі до даних, розуміння "
                  "прав доступу, командний дух.")
    add_para(doc, "Обладнання:", bold=True)
    add_para(doc, "Інструкційні картки, ПК з LibreOffice Base, LibreOffice Calc.")
    add_para(doc, "Література:", bold=True)
    add_para(doc, "1. Мирошниченко В. О. Використання сучасних інформаційних "
                  "технологій. Київ: Центр учбової літератури, 2022. 296 с.")
    add_para(doc, "2. Потієнко В. О. Графічний дизайн. Харків: Ранок, 2020. 160 с.")
    add_para(doc, "3. Речич Н. В. Вебтехнології. Харків: Ранок, 2020. 160 с.")
    add_para(doc, "", space_after=30)
    add_para(doc, "Виконав(ла): ____________________________", size=12)
    add_para(doc, "Клас: __________     Дата: ____________", size=12)


def build_discussion(doc):
    doc.add_heading("Питання для обговорення", level=1)
    qa = [
        ("Які переваги дає використання майстрів для створення об'єктів БД "
         "порівняно з ручним створенням?",
         "Швидкість створення, зменшення кількості помилок, навчання на "
         "прикладах, автоматичне налаштування зв'язків між таблицями."),
        ("У яких ситуаціях може знадобитися імпорт даних з Excel у БД?",
         "Коли дані вже зібрані в Excel (список учнів від класного керівника), "
         "при міграції з іншої системи, при об'єднанні даних з різних джерел."),
        ("Які формати даних підтримує LibreOffice Base для імпорту/експорту?",
         "Імпорт: .ods, .xls, .xlsx, .csv, .txt, .xml, .dbf, .mdb/.accdb. "
         "Експорт: .ods, .xlsx, .csv, .pdf, .html."),
        ("Які проблеми можуть виникнути під час спільного доступу до БД?",
         "Одночасне редагування (конфлікти), ризик пошкодження файлу, "
         "необхідність блокування записів, відсутність резервних копій, "
         "нестача прав доступу."),
        ("Чому важливо розмежовувати права доступу користувачів до БД?",
         "Щоб запобігти випадковому видаленню/зміні даних, забезпечити "
         "конфіденційність, відстежувати відповідальність, дотримуватися "
         "принципу мінімальних привілеїв."),
    ]
    for i, (q, a) in enumerate(qa, 1):
        add_para(doc, f"{i}. {q}", bold=True)
        add_para(doc, a)
        add_para(doc, "", space_after=4)


def build_theory(doc):
    doc.add_heading("Теоретичні відомості", level=1)
    doc.add_heading("1. Майстри LibreOffice Base", level=2)
    add_para(doc, "LibreOffice Base надає майстри для створення всіх основних об'єктів:")
    add_table(doc, ["Об'єкт", "Майстер"],
              [["Таблиці", "Майстер створення таблиць"],
               ["Форми", "Майстер форм"],
               ["Запити", "Майстер простих/перехресних запитів"],
               ["Звіти", "Майстер звітів"]])
    add_para(doc, "Переваги використання майстрів:", bold=True)
    for t in ["1) Швидкість створення об'єктів.",
              "2) Зменшення кількості помилок.",
              "3) Можливість навчання на прикладах.",
              "4) Автоматичне налаштування зв'язків."]:
        add_para(doc, t)

    doc.add_heading("2. Імпорт даних", level=2)
    add_table(doc, ["Формат", "Розширення", "Призначення"],
              [["Таблиці Calc", ".ods, .xls, .xlsx", "Імпорт з таблиць"],
               ["Текстовий файл", ".csv, .txt", "Дані з розділювачами"],
               ["Таблиці Access", ".mdb, .accdb", "Імпорт з Access"],
               ["XML", ".xml", "Структуровані дані"],
               ["dBase", ".dbf", "Старий формат БД"]])
    add_para(doc, "Способи імпорту:", bold=True)
    add_table(doc, ["Спосіб", "Дія", "Коли використовувати"],
              [["Копіювання через буфер", "Ctrl+C / Ctrl+V", "Невеликі обсяги"],
               ["Майстер імпорту", "Файл → Відкрити → вибрати файл", "Великі обсяги"],
               ["Зв'язування з файлом", "Вставка → Таблиця з файлу", "Дані оновлюються зовні"]])

    doc.add_heading("3. Експорт даних", level=2)
    add_para(doc, "LibreOffice Base підтримує: .ods, .xlsx, .csv, .pdf, .html.")
    add_para(doc, "При експорті запиту в CSV важливо вибрати роздільник "
                  "(кома, крапка з комою, табуляція), кодування (UTF-8) та "
                  "наявність заголовків.")

    doc.add_heading("4. Створення звітів", level=2)
    for t in ["1) Вибір джерела (таблиця або запит).",
              "2) Вибір полів для виведення.",
              "3) Налаштування групування.",
              "4) Налаштування сортування.",
              "5) Вибір макета (табличний, стовпчиковий, у два стовпці).",
              "6) Вибір стилю (діловий, звичайний).",
              "7) Назва звіту → Готово."]:
        add_para(doc, t)

    doc.add_heading("5. Спільне використання БД", level=2)
    add_table(doc, ["Спосіб", "Переваги", "Недоліки"],
              [["Мережева папка", "Простота", "Ризик пошкодження файлу"],
               ["Сервер БД (Firebird)", "Безпека, цілісність", "Складне налаштування"],
               ["Хмарне сховище", "Доступ звідусіль", "Не для одночасного редагування"]])
    add_para(doc, "Для справжньої багатокористувацької роботи рекомендується "
                  "сервер БД (Firebird або MySQL), а не файл .odb у спільній папці.",
             bold=True, size=12)

def build_uml_section(doc):
    doc.add_heading("Схеми та діаграми", level=1)

    doc.add_heading("UML-діаграма «Сутність–Зв'язок» (ERD)", level=2)
    add_para(doc, "Структура бази даних «Шкільна бібліотека» — три пов'язані "
                  "таблиці: «Книги» та «Учні» зв'язані через «Видача» "
                  "зв'язком один-до-багатьох.")
    add_image(doc, os.path.join(IMG_DIR, "uml_erd.png"),
              "Рисунок 1. ERD бази даних «Шкільна бібліотека»", width=5.5)

    doc.add_heading("UML-діаграма варіантів використання (Use Case)", level=2)
    add_para(doc, "Основні сценарії роботи користувача з LibreOffice Base:")
    add_image(doc, os.path.join(IMG_DIR, "uml_usecase.png"),
              "Рисунок 2. Use Case діаграма — сценарії роботи з БД", width=5.5)

    doc.add_heading("UML-діаграма діяльності: імпорт даних", level=2)
    add_image(doc, os.path.join(IMG_DIR, "uml_import.png"),
              "Рисунок 3. Алгоритм імпорту даних у БД", width=4.2)

    doc.add_heading("UML-діаграма діяльності: створення звіту", level=2)
    add_image(doc, os.path.join(IMG_DIR, "uml_report.png"),
              "Рисунок 4. Покроковий алгоритм створення звіту", width=3.8)


def build_ui_section(doc):
    doc.add_heading("Інтерфейс LibreOffice Base", level=1)
    add_para(doc, "Нижче — візуалізація ключових вікон та діалогів, з якими "
                  "ви працюватимете під час виконання практичної роботи.")

    doc.add_heading("Головне вікно LibreOffice Base", level=2)
    add_image(doc, os.path.join(IMG_DIR, "01_main_window.png"),
              "Рисунок 5. Головне вікно БД: ліва панель — об'єкти, "
              "права — робоча область", width=6.0)

    doc.add_heading("Майстер створення таблиці — крок 1", level=2)
    add_para(doc, "Вибір категорії («Бізнес») та зразка таблиці («Книги»). "
                  "Праворуч автоматично показуються поля, які будуть створені.")
    add_image(doc, os.path.join(IMG_DIR, "02_table_wizard.png"),
              "Рисунок 6. Майстер створення таблиці, крок 1",
              width=6.0)

    doc.add_heading("Майстер створення таблиці — крок 2", level=2)
    add_para(doc, "Перенесення потрібних полів зі списку «Доступні поля» "
                  "до списку «Поля нової таблиці».")
    add_image(doc, os.path.join(IMG_DIR, "03_table_wizard_fields.png"),
              "Рисунок 7. Вибір полів майбутньої таблиці",
              width=6.0)

    doc.add_heading("Майстер форм", level=2)
    add_para(doc, "Вибір таблиці-джерела та полів для форми. "
                  "Наступні кроки: субформа → макет → стиль → назва.")
    add_image(doc, os.path.join(IMG_DIR, "04_form_wizard.png"),
              "Рисунок 8. Майстер форм, крок 1", width=6.0)

    doc.add_heading("Готова форма для введення даних", level=2)
    add_para(doc, "Після завершення майстра форма відкривається у режимі "
                  "введення даних. Кнопки навігації дозволяють переглядати "
                  "записи, додавати нові та зберігати зміни.")
    add_image(doc, os.path.join(IMG_DIR, "05_completed_form.png"),
              "Рисунок 9. Форма «Форма_Учні» у режимі введення даних",
              width=6.0)

    doc.add_heading("Майстер звітів — вибір макета", level=2)
    add_para(doc, "На кроці 5 обирається макет звіту. Найчастіше "
                  "використовується табличний — для переглядів списків.")
    add_image(doc, os.path.join(IMG_DIR, "06_report_wizard.png"),
              "Рисунок 10. Майстер звітів — вибір макета", width=6.0)

    doc.add_heading("Діалог імпорту даних", level=2)
    add_para(doc, "Вікно імпорту з попереднім переглядом даних із "
                  "зовнішнього файлу .xlsx перед вставкою в таблицю «Учні».")
    add_image(doc, os.path.join(IMG_DIR, "07_import_dialog.png"),
              "Рисунок 11. Імпорт даних з Excel-файлу", width=6.0)


def build_level1(doc):
    doc.add_heading("Рівень 1 — Базовий", level=1)
    add_para(doc, "Розпізнавання та розуміння.", italic=True)

    doc.add_heading("Завдання 1.1. Відповідність «об'єкт — майстер»", level=2)
    add_para(doc, "З'єднайте стрілками об'єкт БД та відповідний майстер.")
    add_table(
        doc,
        ["Об'єкт", "Майстер (впишіть)"],
        [
            ["Таблиця «Книги»", ""],
            ["Форма для «Учні»", ""],
            ["Запит «Видача_книг»", ""],
            ["Звіт за запитом", ""],
        ],
        fill_empty=True,
    )
    add_answer_box(doc,
        "Таблиця → Майстер створення таблиць; Форма → Майстер форм; "
        "Запит → Майстер простих запитів; Звіт → Майстер звітів.")

    doc.add_heading("Завдання 1.2. Формати файлів", level=2)
    add_para(doc, "Заповніть таблицю: для кожного розширення вкажіть, "
                  "що це за формат і для чого він використовується.")
    add_table(
        doc,
        ["Розширення", "Що це?", "Імпорт / експорт"],
        [["", ".ods", ""], ["", ".csv", ""], ["", ".xlsx", ""],
         ["", ".pdf", ""], ["", ".html", ""]],
        fill_empty=True,
    )
    add_answer_box(doc,
        ".ods — ODF-таблиця (Calc), імпорт/експорт; .csv — текстовий файл з "
        "розділювачами, імпорт/експорт; .xlsx — Excel-таблиця, імпорт/експорт; "
        ".pdf — документ для друку, тільки експорт; .html — веб-сторінка, тільки експорт.")

    doc.add_heading("Завдання 1.3. Кроки майстра звітів", level=2)
    add_para(doc, "Розташуйте кроки майстра звітів у правильному порядку "
                  "(поставте номери 1–7).")
    steps = [
        ("Вибір стилю", ""),
        ("Вибір джерела (таблиця/запит)", ""),
        ("Вибір полів", ""),
        ("Групування", ""),
        ("Назва звіту", ""),
        ("Сортування", ""),
        ("Вибір макета", ""),
    ]
    add_table(doc, ["Крок", "№"], steps, fill_empty=True)
    add_answer_box(doc,
        "1) Джерело → 2) Поля → 3) Групування → 4) Сортування → "
        "5) Макет → 6) Стиль → 7) Назва.")

    doc.add_heading("Завдання 1.4. Терміни", level=2)
    add_para(doc, "Дайте визначення:")
    add_para(doc, "1) Майстер БД — ___________________________________________")
    add_writing_lines(doc, n=1)
    add_para(doc, "2) Імпорт даних — ________________________________________")
    add_writing_lines(doc, n=1)
    add_para(doc, "3) Експорт даних — _______________________________________")
    add_writing_lines(doc, n=1)


def build_level2(doc):
    doc.add_heading("Рівень 2 — Середній", level=1)
    add_para(doc, "Застосування знань на практиці.", italic=True)

    doc.add_heading("Завдання 2.1. Порівняйте способи імпорту", level=2)
    add_para(doc, "Заповніть таблицю: для кожного способу імпорту вкажіть "
                  "переваги та недоліки.")
    add_table(
        doc,
        ["Спосіб", "Переваги", "Недоліки"],
        [
            ["Копіювання через буфер", "", ""],
            ["Майстер імпорту", "", ""],
            ["Зв'язування з файлом", "", ""],
        ],
        fill_empty=True,
    )
    add_answer_box(doc,
        "Буфер: швидко, але для малих обсягів, без перевірки типів. "
        "Майстер: для великих обсягів, перевірка типів, але повільніше. "
        "Зв'язування: автоматичне оновлення, але залежність від зовнішнього файлу.")

    doc.add_heading("Завдання 2.2. Спільний доступ — аналіз", level=2)
    add_para(doc, "Для трьох способів спільного доступу до БД заповніть "
                  "таблицю «коли доцільно»:")
    add_table(
        doc,
        ["Спосіб", "Коли доцільно використовувати"],
        [
            ["Мережева папка", ""],
            ["Сервер БД (Firebird)", ""],
            ["Хмарне сховище", ""],
        ],
        fill_empty=True,
    )
    add_answer_box(doc,
        "Мережева папка — 2–3 користувачі, локальна мережа, некритичні дані. "
        "Сервер БД — 5+ користувачів, критичні дані, потрібен контроль доступу. "
        "Хмарне — один користувач з різних пристроїв (не для одночасного редагування).")

    doc.add_heading("Завдання 2.3. Покрокова інструкція", level=2)
    add_para(doc, "Опишіть покроково, як створити звіт «Звіт_Видача_книг» "
                  "на основі запиту «Видача_книг» за допомогою майстра.")
    add_writing_lines(doc, n=8)
    add_answer_box(doc,
        "1) Звіти → Використати майстер для створення звіту. "
        "2) Джерело: запит «Видача_книг». "
        "3) Поля: Прізвище, Назва, Дата_видачі, Дата_повернення. "
        "4) Групування: за класом (або без). "
        "5) Сортування: за прізвищем. "
        "6) Макет: табличний. Стиль: діловий. "
        "7) Назва: «Звіт_Видача_книг» → Готово.")

    doc.add_heading("Завдання 2.4. CSV vs ODS", level=2)
    add_para(doc, "Порівняйте два формати експорту. Заповніть таблицю.")
    add_table(
        doc,
        ["Ознака", ".csv", ".ods"],
        [
            ["Зберігає типи даних?", "", ""],
            ["Зберігає форматування?", "", ""],
            ["Сумісність з іншими програмами", "", ""],
            ["Підходить для великих обсягів?", "", ""],
        ],
        fill_empty=True,
    )
    add_answer_box(doc,
        "CSV: тільки текст, без форматування, максимальна сумісність, "
        "підходить для великих обсягів. "
        "ODS: зберігає типи й форматування, сумісний з LibreOffice, "
        "для великих файлів потребує більше пам'яті.")


def build_level3(doc):
    doc.add_heading("Рівень 3 — Достатній / Високий", level=1)
    add_para(doc, "Аналіз, синтез, розв'язання проблемних ситуацій.", italic=True)

    doc.add_heading("Завдання 3.1. Проблемна ситуація з імпортом", level=2)
    add_para(doc, "Під час імпорту файлу «нові_учні.xlsx» у таблицю «Учні» "
                  "з'явилося повідомлення: «Помилка: невірний тип даних у "
                  "стовпці «Клас» (очікується VARCHAR, отримано число)».")
    add_para(doc, "Дайте відповіді:", bold=True)
    add_para(doc, "1) Чому виникла помилка?")
    add_para(doc, "2) Як виправити — у джерелі (Excel) чи в цільовій таблиці?")
    add_para(doc, "3) Який тип поля «Клас» доцільно використовувати?")
    add_para(doc, "4) Чи можна імпортувати решту рядків, пропустивши проблемні?")
    add_writing_lines(doc, n=8)
    add_answer_box(doc,
        "1) У Excel значення «10-А» могло зберегтися як число або дата. "
        "2) Виправляти краще в Excel: форматувати стовпець як текст. "
        "3) VARCHAR(10) — клас має літеру. "
        "4) Так, майстер імпорту дозволяє пропустити помилкові рядки — але "
        "краще спочатку виправити джерело, щоб не втратити дані.")

    doc.add_heading("Завдання 3.2. Дизайн бази даних", level=2)
    add_para(doc, "Для шкільної бібліотеки запропонуйте структуру БД "
                  "(не менше 4 таблиць) із поясненням зв'язків:")
    add_para(doc, "• Таблиця «Книги» — що зберігаємо?")
    add_para(doc, "• Таблиця «Автори» — навіщо окремо?")
    add_para(doc, "• Таблиця «Учні» — які поля обов'язкові?")
    add_para(doc, "• Таблиця «Видача» — які зв'язки реалізує?")
    add_para(doc, "• Додатково: «Жанри», «Видавництва», «Читацькі квитки»?")
    add_writing_lines(doc, n=10)
    add_answer_box(doc,
        "«Книги» (Код_книги, Назва, Код_автора, Код_жанру, Рік, ISBN). "
        "«Автори» (Код_автора, Прізвище, Ім'я, Країна) — щоб уникнути "
        "дублювання при кількох книгах одного автора. "
        "«Учні» (Код_учня, Прізвище, Ім'я, Клас, Телефон) — ПІБ і клас обов'язкові. "
        "«Видача» (Код_видачі, Код_книги, Код_учня, Дата, Дата_повернення) — "
        "реалізує зв'язки книга-учень (багато-до-багатьох).")

    doc.add_heading("Завдання 3.3. Спільний доступ — вибір рішення", level=2)
    add_para(doc, "Шкільна бібліотека має 3 комп'ютери в локальній мережі. "
                  "Бібліотекар і два помічники одночасно вводять дані про "
                  "видані книги. Яке рішення для спільного доступу обрати?")
    add_para(doc, "Обґрунтуйте відповідь, порівнявши 3 варіанти (мережева "
                  "папка, Firebird-сервер, хмара).")
    add_writing_lines(doc, n=8)
    add_answer_box(doc,
        "Оптимально — Firebird-сервер (або інший СКБД): "
        "3 користувачі одночасно, потрібна цілісність даних, блокування записів, "
        "резервні копії. Мережева папка ризикована (конфлікти при одночасному "
        "записі, ризик пошкодження .odb). Хмара — не для одночасного редагування.")

    doc.add_heading("Завдання 3.4. Рефлексія", level=2)
    add_para(doc, "Дайте розгорнуту відповідь (5–7 речень):")
    add_para(doc, "• Які переваги дають майстри порівняно з ручним створенням?")
    add_para(doc, "• У яких ситуаціях краще створювати об'єкти вручну?")
    add_para(doc, "• Які навички з цього заняття знадобляться в реальній роботі?")
    add_writing_lines(doc, n=8)


def build_evaluation(doc):
    doc.add_heading("Критерії оцінювання", level=1)
    add_table(
        doc,
        ["Критерій", "Бали"],
        [
            ["Базу даних створено з правильною назвою", "1"],
            ["Таблицю «Книги» створено майстром", "2"],
            ["Таблицю «Учні» створено майстром", "2"],
            ["Форму «Форма_Учні» створено майстром", "2"],
            ["Запит «Видача_книг» створено майстром", "2"],
            ["Звіт «Звіт_Видача_книг» створено майстром", "2"],
            ["Імпорт даних з .ods виконано", "2"],
            ["Експорт даних у .ods, .csv, .pdf виконано", "3"],
            ["Завдання виконано самостійно та акуратно", "4"],
            ["Максимум", "20"],
        ],
    )
    add_para(doc, "", space_after=8)
    add_para(doc, "Шкала переведення:", bold=True)
    add_table(
        doc,
        ["Бали", "Оцінка"],
        [
            ["20–19", "«Відмінно»"],
            ["18–15", "«Добре»"],
            ["14–10", "«Задовільно»"],
            ["9–0", "«Незадовільно»"],
        ],
    )


def build_control_questions(doc):
    doc.add_heading("Контрольні запитання", level=1)
    qa = [
        ("Які об'єкти БД можна створити за допомогою майстрів у LibreOffice Base?",
         "Таблиці, форми, запити, звіти — для кожного є окремий майстер."),
        ("Які формати даних підтримує Base для імпорту?",
         ".ods, .xls, .xlsx, .csv, .txt, .xml, .dbf, .mdb, .accdb."),
        ("Як експортувати результати запиту у формат CSV?",
         "Відкрити запит → Файл → Експорт → вибрати формат CSV → "
         "вказати роздільник (кома, крапка з комою або табуляція) та "
         "кодування UTF-8 → зберегти."),
        ("Для чого призначений звіт у базі даних?",
         "Для виведення даних у зручному для друку вигляді (друкована форма), "
         "з можливістю групування, сортування, підсумків."),
        ("Як імпортувати дані з Excel-файлу в Base?",
         "Файл → Відкрити → вибрати .xlsx → у майстрі імпорту вибрати цільову "
         "таблицю → налаштувати типи полів → Імпортувати. Або скопіювати "
         "діапазон з Excel і вставити в таблицю Base через Ctrl+V."),
        ("Як експортувати таблицю з Base у LibreOffice Calc?",
         "Відкрити таблицю → Файл → Експорт → вибрати формат ODS або XLSX → "
         "зберегти. Або скопіювати дані й вставити в Calc."),
        ("Які заходи безпеки слід вжити при спільному доступі до БД?",
         "Резервні копії, розмежування прав доступу, пароль на файл .odb, "
         "використання сервера БД замість файлу в мережевій папці, "
         "регулярне оновлення, журналювання змін."),
        ("Як створити резервну копію бази даних?",
         "Скопіювати файл .odb у безпечне місце, попередньо закривши його в "
         "усіх користувачів. Для сервера БД — використовувати засоби "
         "резервного копіювання СКБД (наприклад, gbak для Firebird)."),
        ("Як встановити пароль на базу даних?",
         "У LibreOffice Base: Інструменти → Параметри → Захист → "
         "встановити пароль. Або при збереженні файлу .odb вказати пароль "
         "у діалозі збереження."),
        ("Які проблеми можуть виникнути при імпорті даних з Excel?",
         "Невідповідність типів (числа зберігаються як текст або дати), "
         "порожні клітинки, об'єднані клітинки, формули замість значень, "
         "зайві заголовки, змінені кодування (кирилиця)."),
    ]
    for i, (q, a) in enumerate(qa, 1):
        add_para(doc, f"{i}. {q}", bold=True)
        add_para(doc, a)
        add_para(doc, "", space_after=4)


# ==================== ГОЛОВНА ====================

def build_document():
    doc = Document()
    setup_styles(doc)
    for s in doc.sections:
        s.top_margin = Cm(2)
        s.bottom_margin = Cm(2)
        s.left_margin = Cm(2.5)
        s.right_margin = Cm(1.5)

    build_title(doc)
    doc.add_page_break()
    build_discussion(doc)
    build_theory(doc)
    doc.add_page_break()
    build_uml_section(doc)
    doc.add_page_break()
    build_ui_section(doc)
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
    os.makedirs(IMG_DIR, exist_ok=True)
    generate_images()
    log.info("Побудова документа…")
    doc = build_document()
    doc.save(OUTPUT_FILE)
    log.info(f"✓ Документ збережено: {OUTPUT_FILE}")
    log.info(f"✓ Зображення: ./{IMG_DIR}/")


if __name__ == "__main__":
    main()