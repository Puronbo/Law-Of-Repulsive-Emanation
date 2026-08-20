"""Generate MILLENNIUM.pdf from markdown."""
from fpdf import FPDF

def sanitize(text):
    replacements = {
        '\u2014': '--', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u2026': '...',
        '\u03c0': 'pi', '\u2260': '!=', '\u2264': '<=', '\u2265': '>=',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def safe_multi(pdf, w, h, txt, **kw):
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, h, txt, **kw)

with open('docs/MILLENNIUM.md', 'r', encoding='utf-8') as f:
    md = f.read()

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
pdf.set_margins(15, 15, 15)

W = pdf.w - 30

pdf.set_font('Helvetica', 'B', 14)
safe_multi(pdf, W, 10, sanitize('The Millennium Prize Problems Through the Removable Singularity Lens'), align='C')
pdf.set_font('Helvetica', '', 10)
safe_multi(pdf, W, 7, 'Michael Grafiel S Puno', align='C')
safe_multi(pdf, W, 7, 'August 2026', align='C')
pdf.ln(6)

lines = md.split('\n')
skip_first_title = True
for line in lines:
    line = sanitize(line)
    if skip_first_title:
        if line.startswith('# '):
            skip_first_title = False
            continue
        continue
    if line.startswith('# '):
        pdf.set_font('Helvetica', 'B', 13)
        safe_multi(pdf, W, 9, line[2:])
        pdf.set_font('Helvetica', '', 9)
    elif line.startswith('## '):
        pdf.set_font('Helvetica', 'B', 11)
        safe_multi(pdf, W, 8, line[3:])
        pdf.set_font('Helvetica', '', 9)
    elif line.startswith('### '):
        pdf.set_font('Helvetica', 'B', 9)
        safe_multi(pdf, W, 7, line[4:])
        pdf.set_font('Helvetica', '', 9)
    elif line.startswith('---'):
        pdf.ln(2)
        pdf.line(15, pdf.get_y(), pdf.w - 15, pdf.get_y())
        pdf.ln(2)
    elif line.strip() == '':
        pdf.ln(2)
    else:
        line = line.replace('**', '')
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent >= 4 or (stripped and len(stripped) > 0 and stripped[0] in ('=', '+')):
            pdf.set_font('Courier', '', 7)
            pdf.set_x(pdf.l_margin + 5)
            pdf.multi_cell(W - 5, 3.5, stripped)
            pdf.set_font('Helvetica', '', 9)
        elif len(stripped) > 100:
            pdf.set_font('Courier', '', 6)
            safe_multi(pdf, W, 3, stripped)
            pdf.set_font('Helvetica', '', 9)
        else:
            safe_multi(pdf, W, 4.5, stripped)

pdf.output('docs/MILLENNIUM.pdf')
print(f'PDF generated: docs/MILLENNIUM.pdf ({pdf.page_no()} pages)')
