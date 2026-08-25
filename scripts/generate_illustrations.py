#!/usr/bin/env python3
"""Generate SVG illustrations for IMT-Landing sections.

Usage:
    python3 scripts/generate_illustrations.py
"""

import os
import textwrap

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'img')
os.makedirs(OUT_DIR, exist_ok=True)


def save(name, svg):
    path = os.path.join(OUT_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  ✓ {name}  ({len(svg)} chars)")


# ─── STYLED SVG WRAPPER ────────────────────────────────────────

def wrap(content, width=500, height=400, bg="#0F172A", extra=""):
    """Wrap SVG content with consistent viewBox and styling."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" fill="none"{extra}>
{content}
</svg>'''


# ─── 1. HERO — Digital territory abstraction ──────────────────

def hero_illustration():
    nodes_svg = ''
    connections_svg = ''

    # City grid points
    pts = [(120,80), (250,60), (380,90),  # top row
           (80,180), (200,170), (340,160), (450,180),  # mid row
           (150,280), (280,270), (400,290),  # bottom row
           (200,350), (350,340)]  # deep

    # Glowing connections
    pairs = [
        (0,1), (1,2), (3,4), (4,5), (5,6), (7,8), (8,9), (10,11),
        (0,3), (1,4), (2,5), (0,4), (1,5), (2,6),
        (3,7), (4,8), (5,9), (6,9),
        (7,10), (8,11), (8,10), (9,11)
    ]

    for i, j in pairs:
        if i < len(pts) and j < len(pts):
            x1, y1 = pts[i]
            x2, y2 = pts[j]
            connections_svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgba(59,130,246,0.25)" stroke-width="1.5" stroke-dasharray="4 3"/>\n'

    # Outer glow nodes (hub)
    hub_indices = [4, 8]
    for idx in pts:
        x, y = idx
        if idx in pts and pts.index(idx) in [0, 4, 8]:
            connections_svg += f'<circle cx="{x}" cy="{y}" r="18" fill="rgba(59,130,246,0.07)" stroke="rgba(59,130,246,0.12)" stroke-width="1"/>\n'

    for i, (x, y) in enumerate(pts):
        is_hub = i in [1, 4, 8]
        size = 5 if is_hub else 3
        color = '#3B82F6' if is_hub else '#64748B'
        nodes_svg += f'<circle cx="{x}" cy="{y}" r="{size}" fill="{color}" opacity="{0.9 if is_hub else 0.5}"/>\n'

    # Additional decorative elements
    decor = ''
    for _ in range(3):
        decor += '<rect x="40" y="40" width="420" height="320" rx="8" stroke="rgba(59,130,246,0.06)" stroke-width="1" fill="none"/>\n'

    return wrap(connections_svg + decor + nodes_svg, width=500, height=400)


# ─── 2. PROBLEM — PDF stack vs Data network ──────────────────

def problem_illustration():
    svg = ''
    # Left: PDF stack
    svg += '''<!-- PDF stack -->
    <g transform="translate(60, 80)">
        <rect x="0" y="0" width="160" height="200" rx="6" fill="#1E293B" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
        <rect x="-6" y="8" width="160" height="200" rx="6" fill="#1E293B" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
        <rect x="-12" y="16" width="160" height="200" rx="6" fill="#1E293B" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
        <!-- Icon: document lines -->
        <rect x="20" y="30" width="120" height="8" rx="2" fill="rgba(255,255,255,0.15)"/>
        <rect x="20" y="50" width="100" height="8" rx="2" fill="rgba(255,255,255,0.10)"/>
        <rect x="20" y="70" width="110" height="8" rx="2" fill="rgba(255,255,255,0.10)"/>
        <rect x="20" y="90" width="90" height="8" rx="2" fill="rgba(255,255,255,0.08)"/>
        <rect x="20" y="110" width="120" height="8" rx="2" fill="rgba(255,255,255,0.08)"/>
        <rect x="20" y="130" width="80" height="8" rx="2" fill="rgba(255,255,255,0.06)"/>
        <rect x="20" y="150" width="105" height="8" rx="2" fill="rgba(255,255,255,0.06)"/>
    </g>'''

    # Arrow
    svg += '<g transform="translate(240, 170)"><line x1="0" y1="0" x2="60" y2="0" stroke="#3B82F6" stroke-width="2" stroke-dasharray="6 4"/><polygon points="60,-6 72,0 60,6" fill="#3B82F6"/></g>'

    # Right: Data network (connected nodes)
    svg += '''<g transform="translate(310, 60)">
        <!-- Hex outline -->
        <polygon points="110,10 190,55 190,145 110,190 30,145 30,55" fill="rgba(59,130,246,0.05)" stroke="rgba(59,130,246,0.15)" stroke-width="1"/>
        <!-- data nodes -->
        <circle cx="110" cy="50" r="20" fill="rgba(59,130,246,0.12)" stroke="#3B82F6" stroke-width="1.5"/>
        <circle cx="110" cy="50" r="6" fill="#3B82F6"/>
        <circle cx="70" cy="110" r="16" fill="rgba(99,102,241,0.10)" stroke="#6366F1" stroke-width="1.5"/>
        <circle cx="70" cy="110" r="5" fill="#6366F1"/>
        <circle cx="150" cy="110" r="16" fill="rgba(59,130,246,0.10)" stroke="#3B82F6" stroke-width="1.5"/>
        <circle cx="150" cy="110" r="5" fill="#3B82F6"/>
        <circle cx="110" cy="160" r="16" fill="rgba(139,92,246,0.10)" stroke="#8B5CF6" stroke-width="1.5"/>
        <circle cx="110" cy="160" r="5" fill="#8B5CF6"/>
        <!-- connections -->
        <line x1="110" y1="70" x2="70" y2="95" stroke="rgba(59,130,246,0.25)" stroke-width="1.5"/>
        <line x1="110" y1="70" x2="150" y2="95" stroke="rgba(59,130,246,0.25)" stroke-width="1.5"/>
        <line x1="70" y1="125" x2="110" y2="145" stroke="rgba(99,102,241,0.2)" stroke-width="1.5"/>
        <line x1="150" y1="125" x2="110" y2="145" stroke="rgba(59,130,246,0.2)" stroke-width="1.5"/>
        <line x1="70" y1="105" x2="150" y2="105" stroke="rgba(99,102,241,0.15)" stroke-width="1" stroke-dasharray="3 3"/>
    </g>'''

    return wrap(svg, width=500, height=360)


# ─── 3. SOLUTION — Platform architecture ──────────────────────

def solution_illustration():
    svg = '''
    <!-- Three connected blocks -->
    <g transform="translate(30, 50)">
        <!-- Block 1: Geo data -->
        <rect x="0" y="40" width="140" height="260" rx="12" fill="rgba(59,130,246,0.08)" stroke="rgba(59,130,246,0.15)" stroke-width="1.5"/>
        <circle cx="70" cy="95" r="24" fill="rgba(59,130,246,0.12)" stroke="#3B82F6" stroke-width="1.5"/>
        <circle cx="70" cy="95" r="10" fill="#3B82F6"/>
        <text x="70" y="150" text-anchor="middle" fill="#CBD5E1" font-size="12" font-weight="600">Геоданные</text>
        <text x="70" y="168" text-anchor="middle" fill="#64748B" font-size="10">Генплан, ПЗЗ</text>
        <text x="70" y="182" text-anchor="middle" fill="#64748B" font-size="10">Сети, ДЗЗ</text>

        <!-- Connection line 1-2 -->
        <line x1="140" y1="170" x2="175" y2="170" stroke="#3B82F6" stroke-width="1.5" stroke-dasharray="5 3"/>
        <polygon points="175,164 185,170 175,176" fill="#3B82F6"/>

        <!-- Block 2: Integrations -->
        <rect x="185" y="40" width="140" height="260" rx="12" fill="rgba(99,102,241,0.08)" stroke="rgba(99,102,241,0.15)" stroke-width="1.5"/>
        <rect x="215" y="70" width="80" height="16" rx="4" fill="rgba(99,102,241,0.15)"/>
        <rect x="230" y="92" width="60" height="16" rx="4" fill="rgba(99,102,241,0.10)"/>
        <rect x="220" y="114" width="70" height="16" rx="4" fill="rgba(99,102,241,0.15)"/>
        <text x="255" y="150" text-anchor="middle" fill="#CBD5E1" font-size="12" font-weight="600">Интеграции</text>
        <text x="255" y="168" text-anchor="middle" fill="#64748B" font-size="10">СМЭВ 4, ЕГРН</text>
        <text x="255" y="182" text-anchor="middle" fill="#64748B" font-size="10">НСПД, РСО</text>

        <!-- Connection line 2-3 -->
        <line x1="325" y1="170" x2="360" y2="170" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="5 3"/>
        <polygon points="360,164 370,170 360,176" fill="#8B5CF6"/>

        <!-- Block 3: Analytics -->
        <rect x="370" y="40" width="140" height="260" rx="12" fill="rgba(139,92,246,0.08)" stroke="rgba(139,92,246,0.15)" stroke-width="1.5"/>
        <!-- Chart bars -->
        <rect x="400" y="110" width="14" height="40" rx="2" fill="#8B5CF6" opacity="0.6"/>
        <rect x="420" y="80" width="14" height="70" rx="2" fill="#8B5CF6" opacity="0.8"/>
        <rect x="440" y="60" width="14" height="90" rx="2" fill="#8B5CF6"/>
        <rect x="460" y="95" width="14" height="55" rx="2" fill="#A78BFA" opacity="0.6"/>
        <text x="440" y="150" text-anchor="middle" fill="#CBD5E1" font-size="12" font-weight="600">Аналитика</text>
        <text x="440" y="168" text-anchor="middle" fill="#64748B" font-size="10">СППР, прогнозы</text>
        <text x="440" y="182" text-anchor="middle" fill="#64748B" font-size="10">Мониторинг</text>
    </g>'''

    return wrap(svg, width=560, height=360)


# ─── 4. DIRECTIONS — Timeline / Roadmap ───────────────────────

def directions_illustration():
    svg = '''
    <g transform="translate(0, 20)">
        <!-- Timeline line -->
        <line x1="40" y1="180" x2="520" y2="180" stroke="rgba(59,130,246,0.2)" stroke-width="2"/>

        <!-- Arrow on the right end -->
        <polygon points="520,174 535,180 520,186" fill="rgba(59,130,246,0.3)"/>
    </g>'''

    milestones = [
        (50, "Переход", "к ИМТ"),
        (120, "Автоматизация", "услуг"),
        (190, "Эл. согласование", "бумаги → цифра"),
        (260, "КРТ", "мастер-планы"),
        (330, "Витрина", "данных ГИСОГД"),
        (400, "Открытые", "данные"),
        (470, "Инженерные", "сети"),
    ]

    for i, (x, title, sub) in enumerate(milestones):
        # Node circle
        dot_color = ['#3B82F6', '#3B82F6', '#6366F1', '#6366F1', '#8B5CF6', '#8B5CF6', '#A78BFA'][i]
        glow = i == 0 or i == 3
        if glow:
            svg += f'<circle cx="{x}" cy="180" r="18" fill="rgba(59,130,246,0.06)"/>\n'
        svg += f'<circle cx="{x}" cy="180" r="{5 if glow else 4}" fill="{dot_color}"/>\n'
        # Number above
        svg += f'<text x="{x}" y="{145}" text-anchor="middle" fill="{dot_color}" font-size="11" font-weight="700">{i+1:02d}</text>\n'
        # Labels below
        svg += f'<text x="{x}" y="208" text-anchor="middle" fill="#CBD5E1" font-size="11" font-weight="600">{title}</text>\n'
        svg += f'<text x="{x}" y="224" text-anchor="middle" fill="#64748B" font-size="10">{sub}</text>\n'

    return wrap(svg, width=560, height=280)


# ─── 5. GEMS — Dashboard / Stats ──────────────────────────────

def gems_illustration():
    svg = '''
    <g transform="translate(0, 30)">
        <!-- Grid lines -->
        <rect x="30" y="10" width="440" height="310" rx="12" fill="rgba(59,130,246,0.03)" stroke="rgba(59,130,246,0.08)" stroke-width="1"/>
    </g>

    <!-- Dashboard row -->
    <g transform="translate(30, 30)">
        <!-- Stat card 1 -->
        <rect x="0" y="0" width="200" height="100" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
        <text x="100" y="38" text-anchor="middle" fill="#F59E0B" font-size="28" font-weight="800">150+</text>
        <text x="100" y="60" text-anchor="middle" fill="#94A3B8" font-size="11">сотрудников</text>
        <rect x="30" y="72" width="140" height="4" rx="2" fill="rgba(59,130,246,0.1)"/>
        <rect x="30" y="72" width="110" height="4" rx="2" fill="#3B82F6"/>

        <!-- Stat card 2 -->
        <rect x="215" y="0" width="200" height="100" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
        <text x="315" y="38" text-anchor="middle" fill="#3B82F6" font-size="28" font-weight="800">54</text>
        <text x="315" y="60" text-anchor="middle" fill="#94A3B8" font-size="11">регионов на Geometa</text>
        <rect x="245" y="72" width="140" height="4" rx="2" fill="rgba(59,130,246,0.1)"/>
        <rect x="245" y="72" width="120" height="4" rx="2" fill="#3B82F6"/>

        <!-- Stat card 3 -->
        <rect x="0" y="115" width="200" height="100" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
        <text x="100" y="153" text-anchor="middle" fill="#6366F1" font-size="28" font-weight="800">600+</text>
        <text x="100" y="175" text-anchor="middle" fill="#94A3B8" font-size="11">проектов</text>
        <rect x="30" y="187" width="140" height="4" rx="2" fill="rgba(99,102,241,0.1)"/>
        <rect x="30" y="187" width="130" height="4" rx="2" fill="#6366F1"/>

        <!-- Stat card 4 -->
        <rect x="215" y="115" width="200" height="100" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
        <text x="315" y="153" text-anchor="middle" fill="#8B5CF6" font-size="26" font-weight="800">1 млн+</text>
        <text x="315" y="175" text-anchor="middle" fill="#94A3B8" font-size="11">услуг/год</text>
        <rect x="245" y="187" width="140" height="4" rx="2" fill="rgba(139,92,246,0.1)"/>
        <rect x="245" y="187" width="100" height="4" rx="2" fill="#8B5CF6"/>
    </g>'''

    return wrap(svg, width=500, height=360)


# ─── 6. AUDIENCE — Three personas ─────────────────────────────

def audience_illustration():
    svg = '''
    <g transform="translate(0, 10)">
        <!-- Three persona columns -->
        <!-- Gov -->
        <rect x="20" y="20" width="140" height="320" rx="12" fill="rgba(59,130,246,0.05)" stroke="rgba(59,130,246,0.12)" stroke-width="1.5"/>
        <rect x="50" y="42" width="80" height="80" rx="40" fill="rgba(59,130,246,0.10)" stroke="#3B82F6" stroke-width="1.5" stroke-dasharray="4 3"/>
        <circle cx="90" cy="82" r="20" fill="#3B82F6" opacity="0.8"/>
        <rect x="70" y="96" width="40" height="3" rx="1.5" fill="#3B82F6" opacity="0.6"/>
        <text x="90" y="148" text-anchor="middle" fill="#CBD5E1" font-size="12" font-weight="600">Государство</text>
        <text x="90" y="163" text-anchor="middle" fill="#64748B" font-size="10">КПЭ, контроль</text>
        <text x="90" y="178" text-anchor="middle" fill="#64748B" font-size="10">прозрачность</text>

        <!-- Biz -->
        <rect x="180" y="20" width="140" height="320" rx="12" fill="rgba(99,102,241,0.05)" stroke="rgba(99,102,241,0.12)" stroke-width="1.5"/>
        <rect x="210" y="42" width="80" height="80" rx="40" fill="rgba(99,102,241,0.10)" stroke="#6366F1" stroke-width="1.5" stroke-dasharray="4 3"/>
        <rect x="235" y="72" width="16" height="16" rx="2" fill="#6366F1" opacity="0.8"/>
        <rect x="255" y="72" width="10" height="16" rx="2" fill="#A78BFA" opacity="0.5"/>
        <rect x="245" y="92" width="20" height="10" rx="2" fill="#818CF8" opacity="0.6"/>
        <text x="250" y="148" text-anchor="middle" fill="#CBD5E1" font-size="12" font-weight="600">Бизнес</text>
        <text x="250" y="163" text-anchor="middle" fill="#64748B" font-size="10">скорость, данные</text>
        <text x="250" y="178" text-anchor="middle" fill="#64748B" font-size="10">экономия</text>

        <!-- Citizens -->
        <rect x="340" y="20" width="140" height="320" rx="12" fill="rgba(139,92,246,0.05)" stroke="rgba(139,92,246,0.12)" stroke-width="1.5"/>
        <rect x="370" y="42" width="80" height="80" rx="40" fill="rgba(139,92,246,0.10)" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="4 3"/>
        <circle cx="410" cy="72" r="10" fill="#8B5CF6" opacity="0.6"/>
        <circle cx="395" cy="92" r="5" fill="#A78BFA" opacity="0.4"/>
        <circle cx="425" cy="92" r="5" fill="#A78BFA" opacity="0.4"/>
        <text x="410" y="148" text-anchor="middle" fill="#CBD5E1" font-size="12" font-weight="600">Граждане</text>
        <text x="410" y="163" text-anchor="middle" fill="#64748B" font-size="10">доступ, участие</text>
        <text x="410" y="178" text-anchor="middle" fill="#64748B" font-size="10">контроль</text>
    </g>'''

    return wrap(svg, width=500, height=370)


# ─── 7. EFFECTS — Before vs After comparison ──────────────────

def effects_illustration():
    svg = '''
    <!-- Before -->
    <g transform="translate(0, 20)">
        <rect x="20" y="20" width="210" height="310" rx="12" fill="rgba(239,68,68,0.04)" stroke="rgba(239,68,68,0.1)" stroke-width="1.5"/>
        <text x="125" y="52" text-anchor="middle" fill="#EF4444" font-size="13" font-weight="600">Сейчас</text>
        <!-- Slow spinning gear -->
        <circle cx="125" cy="110" r="30" fill="none" stroke="rgba(239,68,68,0.15)" stroke-width="2"/>
        <circle cx="125" cy="110" r="10" fill="rgba(239,68,68,0.1)"/>
        <line x1="125" y1="75" x2="125" y2="145" stroke="rgba(239,68,68,0.12)" stroke-width="1"/>
        <line x1="90" y1="110" x2="160" y2="110" stroke="rgba(239,68,68,0.12)" stroke-width="1"/>
        <text x="125" y="170" text-anchor="middle" fill="#CBD5E1" font-size="12">~1 200 дней</text>
        <text x="125" y="186" text-anchor="middle" fill="#64748B" font-size="10">инвестцикл</text>
        <text x="125" y="210" text-anchor="middle" fill="#64748B" font-size="10">бумажные</text>
        <text x="125" y="224" text-anchor="middle" fill="#64748B" font-size="10">процедуры</text>
    </g>

    <!-- Arrow -->
    <g transform="translate(230, 170)">
        <line x1="0" y1="0" x2="30" y2="0" stroke="#3B82F6" stroke-width="2"/>
        <polygon points="30,-5 40,0 30,5" fill="#3B82F6"/>
    </g>

    <!-- After -->
    <g transform="translate(270, 20)">
        <rect x="20" y="20" width="210" height="310" rx="12" fill="rgba(34,197,94,0.04)" stroke="rgba(34,197,94,0.1)" stroke-width="1.5"/>
        <text x="125" y="52" text-anchor="middle" fill="#22C55E" font-size="13" font-weight="600">Цель</text>
        <!-- Fast data flow -->
        <circle cx="125" cy="110" r="30" fill="rgba(34,197,94,0.06)"/>
        <circle cx="125" cy="110" r="10" fill="rgba(34,197,94,0.15)"/>
        <path d="M95,100 Q110,85 125,90 Q140,85 155,100" stroke="#22C55E" stroke-width="1.5" fill="none" opacity="0.5"/>
        <path d="M95,120 Q110,135 125,130 Q140,135 155,120" stroke="#22C55E" stroke-width="1.5" fill="none" opacity="0.5"/>
        <text x="125" y="170" text-anchor="middle" fill="#CBD5E1" font-size="12">~900 дней</text>
        <text x="125" y="186" text-anchor="middle" fill="#64748B" font-size="10">цифровой</text>
        <text x="125" y="200" text-anchor="middle" fill="#64748B" font-size="10">взаимодействие</text>
        <text x="125" y="214" text-anchor="middle" fill="#64748B" font-size="10">15 минут</text>
    </g>'''

    return wrap(svg, width=520, height=360)


# ─── GENERATE ALL ──────────────────────────────────────────────

if __name__ == '__main__':
    print("\nGenerating SVG illustrations...\n")

    illustrations = [
        ('hero-illustration.svg', hero_illustration()),
        ('problem-illustration.svg', problem_illustration()),
        ('solution-illustration.svg', solution_illustration()),
        ('directions-illustration.svg', directions_illustration()),
        ('gems-illustration.svg', gems_illustration()),
        ('audience-illustration.svg', audience_illustration()),
        ('effects-illustration.svg', effects_illustration()),
    ]

    for name, svg in illustrations:
        save(name, svg)

    print(f"\nDone! {len(illustrations)} SVGs in {OUT_DIR}")