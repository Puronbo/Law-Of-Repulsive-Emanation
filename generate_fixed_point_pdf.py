"""Generate THE_UNIVERSE_FROM_A_FIXED_POINT.pdf from markdown."""
from fpdf import FPDF


def sanitize(text):
    replacements = {
        '\u2014': '--', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u2026': '...',
        '\u2260': '!=', '\u2264': '<=', '\u2265': '>=',
        '\u2192': '->', '\u2190': '<-', '\u2194': '<->',
        '\u221a': 'sqrt', '\u221e': 'inf',
        '\u00b2': '^2', '\u00b3': '^3', '\u2070': '^0',
        '\u2081': '_1', '\u2082': '_2', '\u2083': '_3',
        '\u2080': '_0', '\u2084': '_4', '\u2085': '_5',
        '\u2261': '=', '\u2248': '~', '\u00d7': 'x',
        '\u00f7': '/', '\u03b1': 'alpha', '\u03b2': 'beta',
        '\u03b3': 'gamma', '\u03b4': 'delta', '\u03bb': 'lambda',
        '\u03c9': 'omega', '\u03a9': 'Omega',
        '\u03c3': 'sigma', '\u03b6': 'zeta', '\u03bc': 'mu',
        '\u03bd': 'nu', '\u03c1': 'rho',
        '\u03c6': 'phi', '\u03c8': 'psi', '\u03a3': 'Sum',
        '\u222b': 'integral', '\u2200': 'for all', '\u2203': 'exists',
        '\u2208': 'in', '\u2286': 'subset', '\u2287': 'supset',
        '\u2229': 'intersect', '\u222a': 'union',
        '\u2207': 'nabla', '\u0394': 'Delta',
        '\u25a1': 'box', '\u25cf': 'circle', '\u2020': 'dag',
        '\u00e9': 'e', '\u00e8': 'e', '\u00f4': 'o',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Greek letters used in this paper specifically
    for k, v in {'\u03be': 'xi', '\u039e': 'Xi', '\u03b5': 'eps',
                 '\u03b8': 'theta', '\u03ba': 'kappa', '\u03c4': 'tau'}.items():
        text = text.replace(k, v)
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text


def safe_multi(pdf, w, h, txt, **kw):
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, h, txt, **kw)


with open('docs/THE_UNIVERSE_FROM_A_FIXED_POINT.md', 'r', encoding='utf-8') as f:
    md = f.read()

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
pdf.set_margins(15, 15, 15)

W = pdf.w - 30

pdf.set_font('Helvetica', 'B', 14)
safe_multi(pdf, W, 10,
           sanitize('The Universe from a Fixed Point'), align='C')
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

pdf.output('docs/THE_UNIVERSE_FROM_A_FIXED_POINT.pdf')
print(f'PDF generated: docs/THE_UNIVERSE_FROM_A_FIXED_POINT.pdf '
      f'({pdf.page_no()} pages)')
