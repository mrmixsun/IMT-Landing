#!/usr/bin/env python3
"""
Генератор SVG-секций лендинга ИМТ для импорта в Figma.

Каждый SVG — отдельный фрейм с правильными размерами, цветами фона,
шрифтом Inter и редактируемым текстом (не кривые, не path).

Использование:
  python3 scripts/generate_figma_svgs.py
  python3 scripts/generate_figma_svgs.py --section hero,problem
  python3 scripts/generate_figma_svgs.py --output /custom/path
  python3 scripts/generate_figma_svgs.py --list

После генерации: Figma → перетащить SVG на канву → редактировать.
"""

import argparse
import os
import sys
from xml.sax.saxutils import escape as xmlesc


# ── константы ──────────────────────────────────────────────
CW = 1200   # container width (content area)
L  = 80     # left margin (content starts)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(ROOT, 'assets', 'figma')


# ── SVG-утилиты ────────────────────────────────────────────

def inter(size, weight='400', color='#111827'):
    """Стиль текстового элемента с Inter."""
    return (f'font-family="Inter, sans-serif" font-size="{size}px" '
            f'font-weight="{weight}" fill="{color}"')


def svg_open(w=CW, h=None, bg='#ffffff'):
    """Открывающий тег SVG с фоном-прямоугольником."""
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>\n')


def text(text, x, y, style):
    """Одна строка текста."""
    return f'<text x="{x}" y="{y}" {style}>{xmlesc(str(text))}</text>\n'


def rect(x, y, w, h, fill, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" rx="{rx}"/>\n'


def circle(cx, cy, r, fill):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>\n'


def line(x1, y1, x2, y2, stroke, sw=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def label_tag(txt, x, y, bg='#EFF6FF', fg='#2563EB', text_size=12):
    """Маленький badge-тег (например, «Проблема», «Решение»)."""
    return (
        rect(x, y - 18, len(txt) * 9 + 24, 26, bg, 12) +
        text(txt, x + 12, y - 2, inter(text_size, '600', fg))
    )


def card(x, y, w, h, bg='rgba(255,255,255,0.04)', rx=12, border=None):
    c = rect(x, y, w, h, bg, rx)
    if border:
        c += rect(x, y, w, h, 'transparent', rx) + ' '  # placeholder for stroke
    return c


# ── Генераторы секций ─────────────────────────────────────

def make_nav(h=64):
    out = svg_open(h=h, bg='#ffffff')
    out += line(0, h - 1, CW, h - 1, '#E5E7EB')
    out += text('ИМТ', 24, 42, inter(20, '800', '#0F172A'))
    for i, name in enumerate(['Проблема', 'Решение', 'Эффекты', 'Для кого', 'Цитаты']):
        out += text(name, 780 + i * 95, 42, inter(14, '500', '#4B5563'))
    out += rect(1040, 17, 136, 30, '#2563EB', 8)
    out += text('Принять участие', 1052, 38, inter(14, '600', '#ffffff'))
    out += '</svg>'
    return 'Навигация', out


def make_hero(h=640):
    out = svg_open(h=h, bg='#0F172A')
    out += circle(960, 160, 280, 'rgba(37,99,235,0.08)')
    out += text('Информационная модель территории', L, 180, inter(56, '800', '#ffffff'))
    out += text('Новый стандарт управления развитием городов и регионов', L, 248, inter(24, '500', '#94A3B8'))
    out += text('ГИСОГД сегодня — это архив скан-копий. ИМТ — единая цифровая платформа, где геоданные,', L, 300, inter(18, '400', '#CBD5E1'))
    out += text('интеграции и аналитика работают как один механизм. Для государства, бизнеса и граждан.', L, 326, inter(18, '400', '#CBD5E1'))
    out += rect(L, 350, 200, 48, '#2563EB', 8)
    out += text('Понять проблему', L + 12, 380, inter(15, '600', '#ffffff'))
    out += rect(L + 220, 350, 180, 48, 'transparent', 8)
    out += text('Что такое ИМТ', L + 230, 380, inter(15, '600', '#CBD5E1'))
    out += rect(L, 430, 480, 60, 'rgba(255,255,255,0.06)', 12)
    out += text('30–50 млрд руб/год', L + 24, 464, inter(24, '700', '#F59E0B'))
    out += text('— цена отсутствия ИМТ для региона', L + 280, 464, inter(15, '400', '#94A3B8'))
    out += '</svg>'
    return 'Hero', out


def make_problem(h=800):
    out = svg_open(h=h, bg='#0F172A')
    out += label_tag('Проблема', L, 74, bg='rgba(255,255,255,0.08)', fg='#94A3B8')
    out += text('Сегодня градостроительство работает с', L, 118, inter(32, '700', '#F1F5F9'))
    out += text('«цифровой бумагой»', L, 158, inter(32, '700', '#F1F5F9'))

    # Цитата
    out += rect(L, 188, CW - 160, 60, 'rgba(37,99,235,0.1)', 8)
    out += text('«Мы работаем не с данными, а с цифровой бумагой.', L + 16, 214, inter(15, '400', '#94A3B8'))
    out += text('Документы в PDF выполняют функцию аналога цифрового преобразования.»', L + 16, 236, inter(15, '400', '#94A3B8'))

    # Левая колонка: «Что не так»
    out += rect(L, 278, 480, 320, 'rgba(255,255,255,0.04)', 12)
    out += text('Что не так', L + 20, 312, inter(18, '700', '#F1F5F9'))
    items = [
        'Межведомственное взаимодействие — дни и недели вместо минут',
        'Согласование инженерных сетей — 160 дней бумажных процедур',
        'Нет единой актуальной картографической основы',
        'Нет сводного плана подземных коммуникаций',
        'Информационные модели ОКС не размещаются',
        'Граждане и бизнес не имеют доступа к градостроительным данным',
    ]
    for i, item in enumerate(items):
        yb = 338 + i * 36
        out += circle(L + 23, yb + 4, 4, '#2563EB')
        out += text(item, L + 36, yb, inter(14, '400', '#CBD5E1'))

    # Правая колонка: «Экономика неэффективности»
    c2 = 640
    out += rect(c2, 278, 480, 420, 'rgba(37,99,235,0.1)', 12)
    out += text('Экономика неэффективности', c2 + 20, 312, inter(18, '700', '#F1F5F9'))
    out += text('Кейс Татарстана (1 трлн руб/год — объём стройки)', c2 + 20, 334, inter(14, '400', '#94A3B8'))
    stats = [
        ('1 200 дней', 'средняя длительность инвестцикла (~3.5 года)'),
        ('7 месяцев', 'административные процедуры'),
        ('30–50 млрд руб/год', 'эффект от перехода на цифровое взаимодействие'),
    ]
    sy = 370
    for val, label in stats:
        clr = '#F59E0B' if 'млрд' in val else '#F1F5F9'
        sz = '32px' if 'млрд' in val else '28px'
        out += text(val, c2 + 20, sy, inter(sz, '700', clr))
        out += text(label, c2 + 20, sy + 28, inter(13, '400', '#94A3B8'))
        sy += 72

    out += '</svg>'
    return 'Проблема', out


def make_solution(h=1160):
    out = svg_open(h=h, bg='#ffffff')
    out += label_tag('Решение', L, 74)
    out += text('Информационная модель территории —', L, 118, inter(32, '700', '#111827'))
    out += text('цифровая отраслевая платформа', L, 158, inter(32, '700', '#111827'))

    defn = (
        'Информационная модель территории (ИМТ) — систематизированная совокупность '
        'пространственных, семантических и атрибутивных данных о территории, '
        'объединённых в единой цифровой среде.'
    )
    w = 92
    out += text(defn[:w], L, 204, inter(16, '400', '#4B5563'))
    out += text(defn[w:], L, 230, inter(16, '400', '#4B5563'))

    cols = [
        ('Геопространственные данные', [
            'Генеральный план', 'ПЗЗ и градостроительные регламенты',
            'Проекты планировки (ПП/ПМ)', 'КРТ, инженерные сети', 'Ортофото и ДЗЗ',
        ]),
        ('Интеграция данных', [
            'СМЭВ 4 — витрина данных ГИСОГД', 'ЕГРН / Росреестр',
            'НСПД — федеральная платформа', 'Стройкомплекс.РФ', 'Системы РСО',
        ]),
        ('Анализ и моделирование', [
            'Система поддержки принятия решений', 'Проактивный мониторинг (data-driven)',
            'Автоматическая проверка («робот-чиновник»)', 'Оценка нагрузки и эффекта',
            'Прогнозное моделирование',
        ]),
    ]

    cy = 296
    for idx, (title, items) in enumerate(cols):
        cx = L + idx * 410
        out += rect(cx, cy, 370, 260, '#ffffff', 12)
        out += rect(cx + 16, cy + 16, 48, 48, '#2563EB', 8)   # icon placeholder
        out += text(title, cx + 16, cy + 88, inter(18, '700', '#111827'))
        for i, item in enumerate(items):
            out += text(item, cx + 16, cy + 122 + i * 28, inter(14, '400', '#4B5563'))

    py = cy + 300 + 40
    out += text('Принципы ИМТ', L, py, inter(22, '700', '#111827'))

    principles = [
        ('1', 'Данные, а не документы', 'Всё в машиночитаемом формате'),
        ('2', 'Однократный ввод, многократное использование', ''),
        ('3', 'Актуальность по умолчанию', 'Не «однажды загрузили»'),
        ('4', 'Связанность', 'Через пространственные отношения'),
        ('5', 'Открытость по умолчанию', 'Публичный доступ'),
        ('6', 'Стандартизация', 'Единые форматы и протоколы'),
    ]

    py2 = py + 40
    for i, (num, ttl, desc) in enumerate(principles):
        px = L + (i % 2) * 560
        row_y = py2 + (i // 2) * 80
        out += rect(px, row_y, 520, 64, '#F8FAFC', 10)
        out += rect(px + 14, row_y + 18, 28, 28, '#2563EB', 8)
        out += text(num, px + 21, row_y + 37, inter(12, '700', '#ffffff'))
        out += text(ttl, px + 56, row_y + 28, inter(14, '600', '#111827'))
        if desc:
            out += text(desc, px + 56, row_y + 48, inter(12, '400', '#6B7280'))

    out += '</svg>'
    return 'Решение', out


def make_directions(h=760):
    out = svg_open(h=h, bg='#0F172A')
    out += label_tag('Дорожная карта', L, 74, bg='rgba(255,255,255,0.08)', fg='#94A3B8')
    out += text('7 направлений реализации ИМТ', L, 118, inter(32, '700', '#F1F5F9'))

    dirs = [
        ('01', 'Переход к ИМТ', 'Законодательно закрепить понятие ИМТ, определить требования и стандарты'),
        ('02', 'Автоматизация услуг', 'От точечных услуг к комплексной автоматизации на основе данных'),
        ('03', 'Электронное согласование', 'Замена бумажных процессов цифровым взаимодействием'),
        ('04', 'КРТ, мастер-планы', 'Цифровая среда для комплексного развития территорий'),
        ('05', 'Витрина данных ГИСОГД', 'Единая точка доступа к данным через СМЭВ 4'),
        ('06', 'Публичность и открытые данные', 'Доступ к градостроительной информации для всех'),
        ('07', 'Инженерные сети', 'Включение РСО в единую цифровую среду'),
    ]

    for i, (num, ttl, desc) in enumerate(dirs):
        col = i % 2
        row = i // 2
        dx = L + col * 560 + (col * 10)
        dy = 168 + row * 84
        out += rect(dx, dy, 540, 72, 'rgba(255,255,255,0.04)', 10)
        out += text(num, dx + 16, dy + 42, inter(24, '700', '#475569'))
        out += text(ttl, dx + 60, dy + 30, inter(16, '600', '#F1F5F9'))
        out += text(desc, dx + 60, dy + 54, inter(14, '400', '#94A3B8'))

    out += '</svg>'
    return 'Направления', out


def make_effects(h=680):
    out = svg_open(h=h, bg='#ffffff')
    out += label_tag('Эффекты', L, 74)
    out += text('Целевые показатели: что изменится', L, 118, inter(32, '700', '#111827'))

    th_y = 168
    out += text('Показатель', L, th_y, inter(12, '600', '#6B7280'))
    out += text('Сейчас', 640, th_y, inter(12, '600', '#6B7280'))
    out += text('Цель', 800, th_y, inter(12, '600', '#6B7280'))
    out += line(L, th_y + 8, CW - L, th_y + 8, '#E5E7EB', 2)

    rows = [
        ('Инвестиционно-строительный цикл', '~1 200 дней', '~900 дней'),
        ('Межведомственное взаимодействие', 'до 5 дней', '15 минут'),
        ('Сроки услуг в электронном виде', '—', 'сокращение в 3–4 раза'),
        ('Экономия для региона (Татарстан)', '0', '30–50 млрд руб/год'),
        ('Публичный доступ к градостроительным данным', 'нет', 'да'),
        ('Качество городской среды (Указ 309)', '—', '+30% к 2030, +60% к 2036'),
    ]

    ry = th_y + 36
    for label, now_val, target_val in rows:
        out += line(L, ry + 40, CW - L, ry + 40, '#F1F5F9', 1)
        out += text(label, L, ry + 14, inter(14, '400', '#111827'))
        out += text(now_val, 640, ry + 14, inter(14, '500', '#DC2626'))
        out += text(target_val, 800, ry + 14, inter(14, '600', '#059669'))
        ry += 52

    cy = ry + 40
    out += rect(L, cy, CW - 160, 80, '#F8FAFC', 8)
    out += text('Связь с национальными целями (Указ Президента №309):', L + 16, cy + 24, inter(14, '600', '#374151'))
    out += text('• Комфортная и безопасная среда для жизни — +30% к 2030, +60% к 2036', L + 16, cy + 48, inter(14, '400', '#4B5563'))
    out += text('• Цифровая трансформация — 99% услуг онлайн, цифровая зрелость отраслей', L + 16, cy + 68, inter(14, '400', '#4B5563'))

    out += '</svg>'
    return 'Эффекты', out


def make_audience(h=520):
    out = svg_open(h=h, bg='#F8FAFC')
    out += label_tag('Для кого', L, 74)
    out += text('ИМТ — выгода для каждого участника', L, 118, inter(32, '700', '#111827'))

    tabs = ['Государство и регионы', 'Девелоперы и бизнес', 'Граждане']
    tx = L
    for label in tabs:
        out += text(label, tx + 8, 174, inter(14, '500', '#6B7280'))
        tx += 214
    out += line(L, 186, CW - L, 186, '#E5E7EB', 1)
    out += rect(L, 182, 200, 2, '#2563EB', 0)

    cy = 210
    out += rect(L, cy, CW - 160, 40, '#EFF6FF', 8)
    out += text('Экономия времени, снижение рисков, выполнение КПЭ, инвестиционная привлекательность региона.', L + 16, cy + 26, inter(16, '600', '#374151'))

    grid = [
        ('Губернаторы, зампреды', 'Рост инвестиционной привлекательности, Data-Driven управление'),
        ('Региональные чиновники', 'Сокращение сроков услуг, прозрачность'),
        ('Главные архитекторы', 'Инструмент для работы с территорией'),
        ('Минстрой', 'Письма от регионов, резолюция #ГИСОГД'),
    ]

    for i, (ttl, desc) in enumerate(grid):
        gx = L + (i % 2) * 570
        gy = cy + 60 + (i // 2) * 90
        out += rect(gx, gy, 530, 76, '#ffffff', 10)
        out += text(ttl, gx + 16, gy + 24, inter(14, '700', '#111827'))
        out += text(desc, gx + 16, gy + 50, inter(14, '400', '#6B7280'))

    out += '</svg>'
    return 'Для кого', out


def make_quotes(h=640):
    out = svg_open(h=h, bg='#0F172A')
    out += label_tag('Цитаты', L, 74, bg='rgba(255,255,255,0.08)', fg='#94A3B8')
    out += text('О чём говорят лидеры рынка', L, 118, inter(32, '700', '#F1F5F9'))

    quotes = [
        '«Мы работаем не с данными, а с цифровой бумагой. Документы в PDF выполняют функцию аналога цифрового преобразования.»',
        '«К информационной модели не только объектов, но и территории в целом, мы должны прийти. Это условие комплексного подхода и устойчивого развития территории.»',
        '«Средняя продолжительность инвестиционно-строительного цикла — 1 200 дней. Эффект от перехода на цифровое взаимодействие — 30–50 млрд руб/год.»',
        '«80% данных, необходимых для принятия решений, связаны с местоположением.»',
        '«Мы сейчас как энтузиасты на первых автомобилях — дорого, непрактично, но надо пройти путь до фордовского конвейера и массового спроса.»',
        '«НСПД = сырая нефть, GEMS = бензин и пластик.»',
        '«GEMS уже придумал и предложил новый принцип и подход. Задача — сделать его неизбежным.»',
    ]

    qy = 168
    for q in quotes:
        out += rect(L, qy, CW - 160, 48, 'rgba(255,255,255,0.04)', 8)
        display = q[:82] + '…' if len(q) > 82 else q
        out += text(display, L + 16, qy + 30, inter(15, '400', '#E2E8F0'))
        qy += 62

    out += '</svg>'
    return 'Цитаты', out


def make_gems(h=480):
    out = svg_open(h=h, bg='#ffffff')
    out += label_tag('Кто реализует', L, 74)
    out += text('GEMS — проводник цифровой трансформации', L, 118, inter(32, '700', '#111827'))
    out += text('градостроительства', L, 158, inter(32, '700', '#111827'))
    out += text('GEMS — разработчик GIS-решений для градостроительства и лидер', L, 204, inter(16, '400', '#4B5563'))
    out += text('цифровизации ГИСОГД в России.', L, 230, inter(16, '400', '#4B5563'))

    stats = [('150+', 'сотрудников'), ('54–55', 'регионов'), ('600+', 'проектов'), ('1 млн+', 'услуг в год')]
    sx = L
    for num, label in stats:
        out += rect(sx, 268, 250, 96, '#F8FAFC', 12)
        out += text(num, sx + 12, 306, inter(36, '800', '#2563EB'))
        out += text(label, sx + 12, 338, inter(14, '400', '#6B7280'))
        sx += 270

    out += rect(L, 396, CW - 160, 60, '#F8FAFC', 8)
    out += text('GEMS — не просто вендор. GEMS — проводник: от «цифровой бумаги»', L + 16, 424, inter(14, '400', '#374151'))
    out += text('к информационной модели территории.', L + 16, 446, inter(14, '400', '#374151'))

    out += '</svg>'
    return 'GEMS', out


def make_cta(h=480):
    out = svg_open(h=h, bg='#0F172A')
    out += text('Присоединяйтесь к созданию ИМТ', L, 100, inter(32, '700', '#F1F5F9'))
    out += text('Концепция открыта для всех участников градостроительной деятельности.', L, 140, inter(16, '400', '#94A3B8'))
    out += text('Выберите свой путь:', L, 170, inter(16, '400', '#94A3B8'))

    options = [
        ('Для регионов', 'Хотите оценить экономический эффект\nИМТ для вашего региона?', 'Связаться с нами'),
        ('Для девелоперов', 'Протестируйте\nанализ участка в 1 клик', 'Хочу попробовать'),
        ('Для всех', 'Подпишитесь на Telegram-канал\n#ГИСОГД', 'Telegram-канал'),
    ]

    ox = L
    for title, desc, btn_label in options:
        out += rect(ox, 218, 348, 180, 'rgba(255,255,255,0.06)', 12)
        out += text(title, ox + 16, 248, inter(18, '700', '#F1F5F9'))
        lines = desc.split('\n')
        for i, l in enumerate(lines):
            out += text(l, ox + 16, 276 + i * 24, inter(14, '400', '#94A3B8'))
        out += rect(ox + 16, 332, 180, 42, '#2563EB', 8)
        out += text(btn_label, ox + 24, 358, inter(14, '600', '#ffffff'))
        ox += 366

    out += '</svg>'
    return 'CTA', out


def make_footer(h=64):
    out = svg_open(h=h, bg='#0B1A2E')
    out += text('Информационная модель территории (ИМТ) — 2026', L, 36, inter(14, '400', '#64748B'))
    out += text('Концепция развития информационного обеспечения градостроительной деятельности', 520, 36, inter(14, '400', '#64748B'))
    out += '</svg>'
    return 'Подвал', out


# ── Реестр секций ─────────────────────────────────────────

SECTIONS = {
    'nav':        make_nav,
    'hero':       make_hero,
    'problem':    make_problem,
    'solution':   make_solution,
    'directions': make_directions,
    'effects':    make_effects,
    'audience':   make_audience,
    'quotes':     make_quotes,
    'gems':       make_gems,
    'cta':        make_cta,
    'footer':     make_footer,
}


# ── CLI ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Генерация SVG-секций ИМТ-лендинга для Figma.',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--section', '-s',
        help='Какие секции генерировать (через запятую). По умолчанию — все.\n'
             'Доступны: nav, hero, problem, solution, directions, effects,\n'
             '          audience, quotes, gems, cta, footer',
        default=None,
    )
    parser.add_argument(
        '--output', '-o',
        help=f'Папка для SVG-файлов. По умолчанию: {DEFAULT_OUT}',
        default=DEFAULT_OUT,
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Показать доступные секции и выйти.',
    )

    args = parser.parse_args()

    if args.list:
        print('Доступные секции:')
        for key in SECTIONS:
            gen = SECTIONS[key]
            name, _ = gen()
            print(f'  {key:16s} — {name}')
        return

    out_dir = args.output
    os.makedirs(out_dir, exist_ok=True)

    if args.section:
        keys = [k.strip() for k in args.section.split(',')]
        for k in keys:
            if k not in SECTIONS:
                print(f'  ✗ Неизвестная секция: {k}')
                sys.exit(1)
    else:
        keys = list(SECTIONS.keys())

    for key in keys:
        gen = SECTIONS[key]
        name, content = gen()
        filename = f'{key}.svg'
        filepath = os.path.join(out_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✓ {filename}  ({name}, {len(content)} bytes)')

    print(f'\nГотово. {len(keys)} SVG сохранены в {out_dir}')
    print('Figma → перетащить файлы на канву → редактировать текст.')


if __name__ == '__main__':
    main()