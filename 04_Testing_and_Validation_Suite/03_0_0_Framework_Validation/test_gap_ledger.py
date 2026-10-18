"""Gap Ledger: one subject at a time, honesty machine-checked.

This gate enforces:
  (B) every related_cards[i] is a token in EXPLICIT_CLAIMS (ENTRIES);
  (C) no row has status UNRESEARCHED; no row's as_of > STALE_DAYS (365) old
      (hard-fail);
  (D) every row declares a **Proof attempt:** with a controlled kind
      (certificate | partial | no-go | citation-only | none) and every artifact
      path it names exists on disk.
  Also: every G1..G11 heading in THE_GAP_LEDGER.md corresponds to a row.
"""
import ast
import io
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_DIR = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
TRACE = os.path.join(
    ROOT,
    "04_Testing_and_Validation_Suite",
    "03_0_0_Framework_Validation",
    "test_claim_traceability.py",
)
LEDGER = os.path.join(DOC_DIR, "THE_GAP_LEDGER.md")

STALE_DAYS = 365

def _read(p):
    with io.open(p, encoding='utf-8', errors='replace') as fp:
        return fp.read()

def _card_tokens():
    src = _read(TRACE)
    start = src.index('ENTRIES = [')
    i = src.index('[', start)
    depth = 0
    for j in range(i, len(src)):
        if src[j] == '[':
            depth += 1
        elif src[j] == ']':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    entries = eval(src[i:end], {'__builtins__': {}})
    return {tok for tok, _, _ in entries}

def _parse_gaps():
    text = _read(LEDGER)
    gaps = []
    for m in re.finditer(r'^##\s+(G\d+)\b', text, re.M):
        token = m.group(1)
        # read forward a few lines
        # find status, related_cards, as_of
        start = m.end()
        # crude: next 40 lines
        block = '\n'.join(text[start:start+2000].splitlines()[:40])
        status = re.search(r'\*\*Status:\*\*\s*(\w+)', block)
        cards = re.search(r'\*\*Related cards:\*\*\s*(.*)$', block, re.M)
        as_of = re.search(r'\*\*as_of:\*\*\s*(\d{4}-\d{2}-\d{2})', block)
        attempt = re.search(r'\*\*Proof attempt:\*\*\s*(.*)$', block, re.M)
        gaps.append({
            'token': token,
            'status': status.group(1) if status else '',
            'cards': cards.group(1).strip() if cards else '',
            'as_of': as_of.group(1) if as_of else '',
            'attempt': attempt.group(1).strip() if attempt else '',
        })
    return gaps

#: controlled vocabulary for the Proof-attempt kind (Gate D)
PROOF_KINDS = {'certificate', 'partial', 'no-go', 'citation-only', 'none'}

def test_b_all_related_cards_are_real():
    cards = _card_tokens()
    bad = []
    for g in _parse_gaps():
        cs = g['cards']
        if cs == '[]' or cs == '':
            continue
        # split C3, C8-open etc
        for c in re.findall(r'C\d+(?:-open)?', cs):
            if c not in cards:
                bad.append((g['token'], c))
    assert not bad, "phantom card refs in gap ledger: %s" % bad

def test_c_no_unresearched_and_no_stale_rows():
    today = datetime.today()
    bad_unres = []
    bad_stale = []
    for g in _parse_gaps():
        if g['status'] == 'UNRESEARCHED':
            bad_unres.append(g['token'])
        if g['as_of']:
            try:
                d = datetime.strptime(g['as_of'], '%Y-%m-%d')
            except ValueError:
                bad_stale.append((g['token'], 'bad-date', g['as_of']))
                continue
            age = (today - d).days
            if age > STALE_DAYS:
                bad_stale.append((g['token'], 'stale', age))
    assert not bad_unres, "UNRESEARCHED rows: %s" % bad_unres
    assert not bad_stale, "stale rows: %s" % bad_stale

def test_d_proof_attempt_kind_and_artifacts_exist():
    """Gate D: every gap declares what *kind* of proof artifact exists, and
    every path it names is a real file under the repository root."""
    missing = []
    bad_kind = []
    bad_paths = []
    for g in _parse_gaps():
        attempt = g['attempt']
        if not attempt:
            missing.append(g['token'])
            continue
        parts = re.split(r'\s+[-\u2014\u2013]\s+', attempt, maxsplit=1)
        kind = parts[0].strip()
        if kind not in PROOF_KINDS:
            bad_kind.append((g['token'], kind))
        if len(parts) > 1:
            for path in [x.strip() for x in parts[1].split(',') if x.strip()]:
                if path == 'n/a':
                    continue
                if not os.path.exists(os.path.join(ROOT, path)):
                    bad_paths.append((g['token'], path))
    assert not missing, "gaps missing **Proof attempt:**: %s" % missing
    assert not bad_kind, "illegal proof-attempt kinds: %s" % bad_kind
    assert not bad_paths, "proof-attempt artifact paths do not exist: %s" % bad_paths

def test_ledgers_heading_count_agrees():
    text = _read(LEDGER)
    heads = re.findall(r'^##\s+(G\d+)', text, re.M)
    assert len(heads) == 11 and heads == [f'G{i}' for i in range(1,12)], heads
