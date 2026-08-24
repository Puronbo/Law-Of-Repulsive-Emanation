"""Generate EXACT_KOLMOGOROV_RATIOS.pdf from markdown."""
from fpdf import FPDF


def sanitize(text):
    replacements = {
        '\u2014': '--', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u2026': '...',
        '\u2260': '!=', '\u2264': '<=', '\u2265': '>=',
        '\u2192': '->', '\u2190': '<-', '\u2194': '<->',
        '\u221a': 'sqrt', '\u221e': 'inf',
        '\u00b2': '^2', '\u00b3': '^3',
        '\u2261': '=', '\u2248': '~', '\u00d7': 'x',
        '\u00f7': '/', '\u03b1': 'alpha', '\u03b2': 'beta',
        '\u03b3': 'gamma', '\u03b4': 'delta', '\u03bb': 'lambda',
        '\u03bd': 'nu', '\u03c3': 'sigma', '\u03be': 'xi',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text


def safe_multi(pdf, w, h, txt, **kw):
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, h, txt, **kw)


with open('docs/EXACT_KOLMOGOROV_RATIOS.md', 'r', encoding='utf-8') as f:
    md = f.read()

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
pdf.set_margins(15, 15, 15)

W = pdf.w - 30

pdf.set_font('Helvetica', 'B', 14)
safe_multi(pdf, W, 10,
           sanitize('Exact Kolmogorov Ratios under Self-Similar Focusing'),
           align='C')
pdf.set_font('Helvetica', '', 10)
safe_multi(pdf, W, 7, 'Michael Grafiel S Puno', align='C')
safe_multi(pdf, W, 7, 'August 2026 (v0.1.0)', align='C')
pdf.ln(6)

lines = md.split('\n')
skip_first_title = True
for line in lines:
    line = sanitize(line)
    if skip_first_title:
        if line.startswith('# '):
            skip_first_title = False
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
        if indent >= 4 or (stripped and stripped[0] in ('=', '+')):
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

pdf.output('docs/EXACT_KOLMOGOROV_RATIOS.pdf')
print(f'PDF generated: docs/EXACT_KOLMOGOROV_RATIOS.pdf '
      f'({pdf.page_no()} pages)')
