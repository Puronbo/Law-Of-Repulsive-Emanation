"""Generate docs/THE_FOLD_OF_ZETA.pdf from docs/THE_FOLD_OF_ZETA.md.

Uses Arial Unicode (ARIALUNI.ttf) so Greek/maths unicode render directly.
Strips light markdown (backticks, **bold**, *italic*, tables, rules).
"""
import re
from fpdf import FPDF

SRC = 'docs/THE_FOLD_OF_ZETA.md'
OUT = 'docs/THE_FOLD_OF_ZETA.pdf'
FONT_DIR = 'C:/Windows/Fonts'

INLINE_RE = re.compile(r'(`+)(.*?)\1')        # inline code / backticks
BOLD_RE = re.compile(r'\*\*(\S(?:.*?\S)?)\*\*')  # **bold**
ITAL_RE = re.compile(r'\*(?!\s)(\S(?:.*?\S)?)\*')  # *italic* (not **)


def strip_inline(text):
    text = INLINE_RE.sub(lambda m: m.group(1), text)
    text = BOLD_RE.sub(lambda m: m.group(1), text)
    text = ITAL_RE.sub(lambda m: m.group(1), text)
    return text


RENDER = {
    '\u2194': '<->',   # <->  bidirectional arrow
    '\u2192': '->',
}


def clean(text):
    for k, v in RENDER.items():
        text = text.replace(k, v)
    return text


with open(SRC, 'r', encoding='utf-8') as f:
    md = f.read()

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()
pdf.set_margins(16, 16, 16)
W = pdf.w - 32
pdf.set_compression(True)

pdf.add_font('Uni', '', f'{FONT_DIR}/ARIALUNI.ttf')
pdf.add_font('Uni', 'B', f'{FONT_DIR}/arialbd.ttf')
pdf.add_font('Uni', 'I', f'{FONT_DIR}/ariali.ttf')
pdf.add_font('Uni', 'BI', f'{FONT_DIR}/arialbi.ttf')


def emit_table(line):
    cells = [clean(strip_inline(c)).strip() for c in line.strip('|').split('|')]
    if all(not c for c in cells):
        return
    if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
        return
    widths = [W / len(cells)] * len(cells)
    y0 = pdf.get_y()
    line_h = 4.6
    start_x = pdf.l_margin
    for i, c in enumerate(cells):
        pdf.set_xy(start_x + sum(widths[:i]), y0)
        pdf.set_font('Uni', '', 8)
        pdf.multi_cell(widths[i], line_h, c, border=0)
    h = pdf.get_y() - y0
    pdf.set_y(y0 + max(h, line_h))


for raw in md.split('\n'):
    line = raw.rstrip()
    stripped_lead = line.lstrip()
    if line.startswith('# '):
        continue
    elif line.startswith('## '):
        pdf.set_font('Uni', 'B', 12)
        pdf.multi_cell(W, 6.5, clean(strip_inline(line[3:].strip())))
        pdf.ln(1.5)
    elif line.startswith('### '):
        pdf.set_font('Uni', 'B', 10)
        pdf.multi_cell(W, 5.5, clean(strip_inline(line[4:].strip())))
        pdf.ln(1)
    elif line.startswith('|---') or line.startswith('| ---') or re.fullmatch(r'\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*', stripped_lead):
        continue
    elif line.startswith('|'):
        emit_table(line)
    elif line.strip() == '':
        pdf.ln(2)
    elif stripped_lead.startswith('---'):
        pdf.ln(2)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.l_margin, pdf.get_y())
        pdf.ln(2)
    elif stripped_lead.startswith(('`', '* ', '- ', '> ')):
        txt = clean(strip_inline(stripped_lead.lstrip('`*-> ').rstrip('`')))
        pdf.set_font('Uni', '', 8.5)
        pdf.set_x(pdf.l_margin + 6)
        pdf.multi_cell(W - 12, 4.8, txt)
        pdf.ln(.5)
    else:
        txt = clean(strip_inline(stripped_lead))
        pdf.set_font('Uni', '', 9.2)
        pdf.multi_cell(W, 5.0, txt)

pdf.output(OUT)
print(f'PDF generated: {OUT} ({pdf.page_no()} pages)')
