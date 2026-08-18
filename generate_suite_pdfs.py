"""Generate PDFs for the 0/0 paper suite from markdown sources."""

import re
import os
from fpdf import FPDF

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')

PAPERS = [
    ('THE_LAW_OF_SINGULARITIES.md', 'The Law of Singularities', 'A Formal Theory of Indeterminate Form as Mathematical Structure'),
    ('THE_UNIVERSAL_ZERO.md', 'The Universal Zero', 'Indeterminate Form as the Deep Structure of Mathematics'),
    ('ON_THE_NATURE_OF_ZERO.md', 'On the Nature of Zero', 'Three Identities of Nothing'),
    ('THE_0_OVER_0_ATLAS.md', 'The 0/0 Atlas', 'A Complete Catalog of Indeterminate Form in Mathematics'),
    ('REMOVABLE_SINGULARITIES.md', 'Removable Singularities', 'What the 0/0 Form Tells Us About Knowledge'),
]


def sanitize(text):
    """Replace Unicode chars that fpdf can't handle with ASCII equivalents."""
    replacements = {
        '\u2014': '--',   # em dash
        '\u2013': '-',    # en dash
        '\u2018': "'",    # left single quote
        '\u2019': "'",    # right single quote
        '\u201c': '"',    # left double quote
        '\u201d': '"',    # right double quote
        '\u2022': '-',    # bullet
        '\u2026': '...',  # ellipsis
        '\u03b1': 'alpha',  # α
        '\u03b2': 'beta',   # β
        '\u03b3': 'gamma',  # γ
        '\u03b4': 'delta',  # δ
        '\u03b5': 'epsilon',# ε
        '\u03b6': 'zeta',   # ζ
        '\u03b7': 'eta',    # η
        '\u03b8': 'theta',  # θ
        '\u03b9': 'iota',   # ι
        '\u03ba': 'kappa',  # κ
        '\u03bb': 'lambda', # λ
        '\u03bc': 'mu',     # μ
        '\u03bd': 'nu',     # ν
        '\u03be': 'xi',     # ξ
        '\u03c0': 'pi',     # π
        '\u03c1': 'rho',    # ρ
        '\u03c3': 'sigma',  # σ
        '\u03c4': 'tau',    # τ
        '\u03c5': 'upsilon',# υ
        '\u03c6': 'phi',    # φ
        '\u03c7': 'chi',    # χ
        '\u03c8': 'psi',    # ψ
        '\u03c9': 'omega',  # ω
        '\u0393': 'Gamma',  # Γ
        '\u0394': 'Delta',  # Δ
        '\u0398': 'Theta',  # Θ
        '\u039b': 'Lambda', # Λ
        '\u03a3': 'Sigma',  # Σ
        '\u03a6': 'Phi',    # Φ
        '\u03a8': 'Psi',    # Ψ
        '\u03a9': 'Omega',  # Ω
        '\u221e': 'inf',    # ∞
        '\u2211': 'Sum',    # Σ
        '\u220f': 'Prod',   # ∏
        '\u222b': 'int',    # ∫
        '\u2248': '~',      # ≈
        '\u2264': '<=',     # ≤
        '\u2265': '>=',     # ≥
        '\u2260': '!=',     # ≠
        '\u221a': 'sqrt',   # √
        '\u00d7': 'x',      # ×
        '\u00f7': '/',      # ÷
        '\u00b0': ' deg',   # °
        '\u2032': "'",      # ′ (prime)
        '\u2033': '"',      # ″ (double prime)
        '\u2192': '->',     # →
        '\u2190': '<-',     # ←
        '\u2194': '<->',    # ↔
        '\u2208': 'in',     # ∈
        '\u2286': 'sub',    # ⊆
        '\u2287': 'sup',    # ⊇
        '\u2205': '{}',     # ∅
        '\u00a0': ' ',      # non-breaking space
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fallback: replace any remaining non-latin1 chars with ?
    result = []
    for ch in text:
        try:
            ch.encode('latin-1')
            result.append(ch)
        except UnicodeEncodeError:
            result.append('?')
    return ''.join(result)


def strip_md(text):
    """Strip markdown formatting to plain text for fpdf."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = text.replace('\\', '')
    text = text.replace('|', ' ')
    return sanitize(text)


class SuitePDF(FPDF):
    def __init__(self, short_title):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=25)
        self.short_title = short_title

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, self.short_title, new_x='LMARGIN', new_y='NEXT', align='C')
        self.set_draw_color(180, 180, 180)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, str(self.page_no()), new_x='LMARGIN', new_y='NEXT', align='C')

    def title_page(self, title, subtitle, authors, date):
        self.ln(25)
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 11, sanitize(title), align='C')
        if subtitle:
            self.ln(4)
            self.set_font('Helvetica', 'I', 13)
            self.set_text_color(60, 60, 60)
            self.multi_cell(0, 7, sanitize(subtitle), align='C')
        self.ln(10)
        self.set_font('Helvetica', '', 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 7, 'The L.O.R.E. Collaboration', new_x='LMARGIN', new_y='NEXT', align='C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 7, 'Puronbo Laboratory', new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(3)
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, date, new_x='LMARGIN', new_y='NEXT', align='C')
        self.cell(0, 6, 'arXiv: 2026.PunoCalculus', new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(8)
        self.set_draw_color(0, 0, 0)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(4)

    def section(self, text, level=1):
        text = sanitize(text)
        if level == 1:
            self.set_font('Helvetica', 'B', 16)
            self.set_text_color(0, 0, 0)
            self.ln(6)
            self.multi_cell(0, 9, text)
            self.ln(3)
            self.set_draw_color(0, 0, 0)
            self.line(20, self.get_y(), 190, self.get_y())
            self.ln(4)
        elif level == 2:
            self.set_font('Helvetica', 'B', 13)
            self.set_text_color(20, 20, 20)
            self.ln(5)
            self.multi_cell(0, 7, text)
            self.ln(2)
        elif level == 3:
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(40, 40, 40)
            self.ln(3)
            self.multi_cell(0, 6, text)
            self.ln(2)

    def body_text(self, text):
        text = sanitize(text)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bold_line(self, text):
        text = sanitize(text)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def table_row(self, cells, bold=False):
        cells = [sanitize(str(c)) for c in cells]
        if bold:
            self.set_font('Helvetica', 'B', 9)
        else:
            self.set_font('Helvetica', '', 9)
        self.set_text_color(30, 30, 30)
        col_w = 170 / max(len(cells), 1)
        for cell in cells:
            cell_text = strip_md(str(cell))[:80]
            self.cell(col_w, 5, cell_text, border=1, new_x='RIGHT', new_y='TOP')
        self.ln()

    def blockquote(self, text):
        text = sanitize(text)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(80, 80, 80)
        x = self.get_x()
        self.set_x(x + 10)
        self.multi_cell(160, 5, text)
        self.ln(2)

    def bullet(self, text, indent=0):
        text = sanitize(text)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        x = 20 + indent * 5
        self.set_x(x)
        self.cell(4, 5, '-', new_x='RIGHT', new_y='TOP')
        self.multi_cell(170 - indent * 5, 5, strip_md(text))
        self.ln(1)

    def numbered_item(self, num, text, indent=0):
        text = sanitize(text)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(30, 30, 30)
        x = 20 + indent * 5
        self.set_x(x)
        prefix = f'{num}. '
        self.cell(self.get_string_width(prefix) + 1, 5, prefix, new_x='RIGHT', new_y='TOP')
        self.set_font('Helvetica', '', 10)
        self.multi_cell(170 - indent * 5 - self.get_string_width(prefix), 5, strip_md(text))
        self.ln(1)

    def code_block(self, lines):
        self.set_font('Courier', '', 9)
        self.set_text_color(40, 40, 40)
        self.set_fill_color(245, 245, 245)
        for line in lines:
            self.set_x(25)
            self.cell(160, 4.5, sanitize(line[:95]), new_x='LMARGIN', new_y='NEXT', fill=True)
        self.ln(3)


def parse_and_render(pdf, md_text):
    """Parse markdown and render to PDF."""
    lines = md_text.split('\n')
    i = 0
    in_code = False
    code_lines = []
    table_rows = []
    in_table = False

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if in_code:
                pdf.code_block(code_lines)
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Skip empty lines
        if not line.strip():
            if in_table and table_rows:
                # Render accumulated table
                for ri, row in enumerate(table_rows):
                    cells = [c.strip() for c in row.split('|') if c.strip()]
                    if cells and not all(set(c) <= set('- :') for c in cells):
                        pdf.table_row(cells, bold=(ri == 0))
                table_rows = []
                in_table = False
            i += 1
            continue

        # Table rows
        if '|' in line and line.strip().startswith('|'):
            stripped = line.strip()
            cells = [c.strip() for c in stripped.split('|') if c.strip()]
            if cells and all(set(c) <= set('- :') for c in cells):
                # Separator row, skip
                i += 1
                continue
            table_rows.append(stripped)
            in_table = True
            i += 1
            continue

        # Flush table if we hit a non-table line
        if in_table and table_rows:
            for ri, row in enumerate(table_rows):
                cells = [c.strip() for c in row.split('|') if c.strip()]
                if cells:
                    pdf.table_row(cells, bold=(ri == 0))
            table_rows = []
            in_table = False

        # Horizontal rule
        if line.strip() in ('---', '***', '___'):
            pdf.ln(2)
            pdf.set_draw_color(180, 180, 180)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(4)
            i += 1
            continue

        # Headings
        if line.startswith('######'):
            text = strip_md(line[6:].strip())
            pdf.set_font('Helvetica', 'I', 9)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 5, text)
            pdf.ln(1)
            i += 1
            continue

        if line.startswith('#####'):
            text = strip_md(line[5:].strip())
            pdf.set_font('Helvetica', 'BI', 10)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 5, text)
            pdf.ln(2)
            i += 1
            continue

        if line.startswith('####'):
            text = strip_md(line[4:].strip())
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 6, text)
            pdf.ln(2)
            i += 1
            continue

        if line.startswith('###'):
            text = strip_md(line[3:].strip())
            pdf.section(text, level=3)
            i += 1
            continue

        if line.startswith('##'):
            text = strip_md(line[2:].strip())
            pdf.section(text, level=2)
            i += 1
            continue

        if line.startswith('#'):
            text = strip_md(line[1:].strip())
            pdf.section(text, level=1)
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            text = strip_md(line[1:].strip())
            # Collect continuation lines
            while i + 1 < len(lines) and lines[i + 1].startswith('>'):
                i += 1
                text += ' ' + strip_md(lines[i][1:].strip())
            pdf.blockquote(text)
            i += 1
            continue

        # Bullet points
        m = re.match(r'^(\s*)([-*+]|\d+\.) (.+)', line)
        if m:
            indent = len(m.group(1)) // 2
            marker = m.group(2)
            text = strip_md(m.group(3))
            if re.match(r'\d+\.', marker):
                num = int(marker.rstrip('.'))
                pdf.numbered_item(num, text, indent)
            else:
                pdf.bullet(text, indent)
            i += 1
            continue

        # Bold-only lines (like **Definition 1:** ...)
        if line.strip().startswith('**') and line.strip().endswith('**'):
            text = strip_md(line.strip())
            pdf.bold_line(text)
            i += 1
            continue

        # Regular paragraph - collect continuation
        text = strip_md(line.strip())
        while i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if (not next_line or next_line.startswith('#') or
                next_line.startswith('|') or next_line.startswith('```') or
                next_line.startswith('>') or next_line.startswith('-') or
                next_line.startswith('*') or next_line.startswith('+') or
                next_line.startswith('---') or re.match(r'^\d+\.', next_line)):
                break
            i += 1
            text += ' ' + strip_md(next_line)
        pdf.body_text(text)
        i += 1

    # Flush remaining table
    if in_table and table_rows:
        for ri, row in enumerate(table_rows):
            cells = [c.strip() for c in row.split('|') if c.strip()]
            if cells:
                pdf.table_row(cells, bold=(ri == 0))


def generate_pdf(md_file, short_title, subtitle):
    md_path = os.path.join(OUT_DIR, md_file)
    pdf_name = md_file.replace('.md', '.pdf')
    pdf_path = os.path.join(OUT_DIR, pdf_name)

    with open(md_path, encoding='utf-8') as f:
        md_text = f.read()

    pdf = SuitePDF(short_title)
    pdf.add_page()

    # Extract date from metadata
    date_match = re.search(r'\*\*Date:\*\*\s*(.+)', md_text)
    date = date_match.group(1).strip() if date_match else 'August 2026'

    pdf.title_page(short_title, subtitle, 'The L.O.R.E. Collaboration', date)

    # Parse body
    parse_and_render(pdf, md_text)

    pdf.output(pdf_path)
    size_kb = os.path.getsize(pdf_path) / 1024
    print(f'  {pdf_name} ({size_kb:.0f} KB, {pdf.page_no()} pages)')
    return pdf_path


if __name__ == '__main__':
    print('Generating 0/0 paper suite PDFs...')
    for md_file, short_title, subtitle in PAPERS:
        generate_pdf(md_file, short_title, subtitle)
    print('Done.')
