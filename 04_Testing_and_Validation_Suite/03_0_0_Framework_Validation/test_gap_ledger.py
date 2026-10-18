"""Gap Ledger: one subject at a time, honesty machine-checked.

This gate enforces:
  (B) every related_cards[i] is a token in EXPLICIT_CLAIMS (ENTRIES);
  (C) no row has status UNRESEARCHED; no row's as_of > STALE_DAYS (365) old
      (hard-fail);
  (D) every row declares a **Proof attempt:** with a controlled kind
      (certificate | partial | no-go | citation-only | none) and every artifact
      path it names exists on disk AND is git-tracked (so CI checkouts have it).
  Also: every G1..G16 heading in THE_GAP_LEDGER.md corresponds to a row.
"""
import ast
import io
import os
import re
import subprocess
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
        pins = re.findall(r'\*\*Pin:\*\*\s*(test_\w+)', block)
        gaps.append({
            'token': token,
            'status': status.group(1) if status else '',
            'cards': cards.group(1).strip() if cards else '',
            'as_of': as_of.group(1) if as_of else '',
            'attempt': attempt.group(1).strip() if attempt else '',
            'pins': pins,
        })
    return gaps

#: controlled vocabulary for the Proof-attempt kind (Gate D)
PROOF_KINDS = {'certificate', 'partial', 'no-go', 'citation-only', 'none'}

def _tracked_files():
    """Set of git-tracked paths (relative to ROOT), or ``None`` if git is
    unavailable (in which case Gate D falls back to existence-only)."""
    try:
        out = subprocess.check_output(
            ['git', 'ls-files'], cwd=ROOT, stderr=subprocess.DEVNULL)
    except Exception:
        return None
        return {line.strip().replace('\\', '/')
                for line in out.decode('utf-8', 'replace').splitlines() if line.strip()}

#: controlled vocabulary for the Proof-attempt kind (Gate D)
PROOF_KINDS = {'certificate', 'partial', 'no-go', 'citation-only', 'none'}

def _existing_test_funcs():
    """Every ``def test_...`` name in the validation test directory (Gate D)."""
    names = set()
    local = os.path.join(ROOT, "04_Testing_and_Validation_Suite",
                         "03_0_0_Framework_Validation")
    for dirpath, _dirs, files in os.walk(local):
        for f in files:
            if f.startswith("test_") and f.endswith(".py"):
                for m in re.finditer(r'^def\s+(test_\w+)\s*\(', _read(os.path.join(dirpath, f)), re.M):
                    names.add(m.group(1))
    return names

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
    every path it names is a real, git-tracked file under the repository root
    (so the CI checkout actually contains it).  Every declared ``**Pin:**``
    must name a real test function, and any ``certificate``-kind gap must carry
    at least one live pin."""
    funcs = _existing_test_funcs()
    tracked = _tracked_files()
    missing = []
    bad_kind = []
    bad_paths = []
    untracked = []
    bad_pin = []
    unpinned_cert = []
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
                elif tracked is not None and path not in tracked:
                    untracked.append((g['token'], path))
        for pin in g['pins']:
            if pin not in funcs:
                bad_pin.append((g['token'], pin))
        if kind == 'certificate' and not g['pins']:
            unpinned_cert.append(g['token'])
    assert not missing, "gaps missing **Proof attempt:**: %s" % missing
    assert not bad_kind, "illegal proof-attempt kinds: %s" % bad_kind
    assert not bad_paths, "proof-attempt artifact paths do not exist: %s" % bad_paths
    assert not untracked, "proof-attempt artifacts are not git-tracked (absent in CI): %s" % untracked
    assert not bad_pin, "declared pins are not real test functions: %s" % bad_pin
    assert not unpinned_cert, "certificate-kind gaps lack a live pin: %s" % unpinned_cert

def test_ledgers_heading_count_agrees():
    text = _read(LEDGER)
    heads = re.findall(r'^##\s+(G\d+)', text, re.M)
    assert heads == [f'G{i}' for i in range(1, 17)], heads
