"""Verify sigma.html structure."""
import os

f = 'webapp/sigma.html'
size = os.path.getsize(f)
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

checks = {
    'DOCTYPE': '<!DOCTYPE html>' in content,
    'charset UTF-8': 'UTF-8' in content,
    'viewport': 'viewport' in content,
    'title': '<title>Sigma' in content,
    'CSS block': '<style>' in content and '</style>' in content,
    'JS block': '<script>' in content and '</script>' in content,
    'closing html': '</html>' in content,
    'closing body': '</body>' in content,
    'tab-home': 'tab-home' in content,
    'tab-explorer': 'tab-explorer' in content,
    'tab-bridge': 'tab-bridge' in content,
    'tab-e8': 'tab-e8' in content,
    'tab-currency': 'tab-currency' in content,
    'tab-fields': 'tab-fields' in content,
    'tab-verify': 'tab-verify' in content,
    'lhopital func': 'function lhopital' in content,
    'parseExpr func': 'function parseExpr' in content,
    'drawSinc func': 'function drawSinc' in content,
    'computeChi func': 'function computeChi' in content,
    'drawE8 func': 'function drawE8' in content,
    'runAllTests func': 'function runAllTests' in content,
    'exportJSON func': 'function exportJSON' in content,
    'showTab func': 'function showTab' in content,
    'canvas-sinc': 'canvas-sinc' in content,
    'canvas-chi': 'canvas-chi' in content,
    'canvas-e8': 'canvas-e8' in content,
    'SINGULARITIES data': 'var SINGULARITIES' in content,
    'E8 exponents data': '[1,7,11,13,17,19,23,29]' in content,
    'ZETA_ZEROS data': 'var ZETA_ZEROS' in content,
    'no external refs': 'http://' not in content.split('<script>')[0],
    'no API keys': 'api_key' not in content.lower(),
}

print("HTML Structure Verification")
print("=" * 50)
print("File size: %d bytes (%.1f KB)" % (size, size / 1024))
print()
all_ok = True
for name, ok in sorted(checks.items()):
    status = "PASS" if ok else "FAIL"
    if not ok:
        all_ok = False
    print("  %-25s [%s]" % (name, status))
print()
print("Result: %s (%d/%d)" % (
    "ALL PASS" if all_ok else "SOME FAIL",
    sum(checks.values()), len(checks)))
