"""The multi-dimensional map must stay a faithful picture of the repository.

`build_multidimensional_map.py` renders `MULTIDIMENSIONAL_MAP.html` from the
ledgers.  A visualisation that silently drifts from its source is worse than no
visualisation: it would assert counts and relationships that the repository does
not have.  This checker therefore re-derives the numbers and asserts that the
rendered artifact says the same thing.

Checks:

1. the generator runs and produces the JSON + HTML;
2. the map's module count equals the modules actually on disk (recursively);
3. the map's module count equals the rows of `MODULE_LEDGER.md`;
4. the map's edge list equals the real ``import`` edges in the Lean tree;
5. every module in the map is a real file, and every file is in the map;
6. every gap id in the map is a real `Gn` row of `THE_GAP_LEDGER.md`;
7. every card id in the map is a real card of `CLAIM_TRACEABILITY.md`;
8. the rendered HTML embeds the data and does not depend on any external file.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_multidimensional_map.py -q
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(
    ROOT, "05_Documentation_and_Research_Specifications", "05_Complete_Framework_Documentation"
)
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)
BUILDER = os.path.join(
    ROOT, "04_Testing_and_Validation_Suite", "03_0_0_Framework_Validation",
    "build_multidimensional_map.py",
)
HTML = os.path.join(DOCS, "MULTIDIMENSIONAL_MAP.html")
JSON_OUT = os.path.join(
    ROOT, "02_Experimental_Implementations_and_Verification", "data",
    "multidimensional_map_data.json",
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_multidimensional_map as bmm  # noqa: E402


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as fp:
        return fp.read()


def _disk_modules():
    mods = set()
    for dirpath, _, filenames in os.walk(LEAN_DIR):
        for name in filenames:
            if name.endswith(".lean"):
                rel = os.path.relpath(os.path.join(dirpath, name), LEAN_DIR)[:-5]
                mods.add(rel.replace(os.sep, "."))
    return mods


def _real_import_edges():
    """Every `import PunoCalculus.X` line, read straight off the Lean sources."""
    edges = set()
    for mod in _disk_modules():
        path = os.path.join(LEAN_DIR, mod.replace(".", os.sep) + ".lean")
        with open(path, encoding="utf-8", errors="replace") as fp:
            for line in fp:
                m = re.match(r"^import PunoCalculus\.([A-Za-z0-9_.'-]+)\s*$", line.strip())
                if m:
                    edges.add((mod, m.group(1)))
    return edges


def _data():
    return bmm.build()


def test_generator_runs_and_writes_both_artifacts():
    """The generator must be runnable and must emit the JSON and the HTML."""
    res = subprocess.run(
        [sys.executable, BUILDER], cwd=ROOT, capture_output=True, text=True
    )
    assert res.returncode == 0, "builder failed:\n%s" % res.stderr
    assert os.path.exists(HTML), "builder did not write %s" % HTML
    assert os.path.exists(JSON_OUT), "builder did not write %s" % JSON_OUT


def test_map_module_count_matches_disk():
    data = _data()
    assert data["counts"]["modules"] == len(_disk_modules()), (
        "map says %d modules, %d .lean files exist"
        % (data["counts"]["modules"], len(_disk_modules()))
    )


def test_map_module_count_matches_the_ledger_table():
    data = _data()
    rows = bmm.parse_module_ledger(_read(os.path.join(DOCS, "MODULE_LEDGER.md")))
    assert data["counts"]["modules"] == len(rows), (
        "map says %d modules, MODULE_LEDGER.md has %d rows"
        % (data["counts"]["modules"], len(rows))
    )


def test_map_edges_match_the_real_import_graph():
    """The drawn edges must be the real ones -- not an artist's impression."""
    data = _data()
    real = _real_import_edges()
    drawn = set(tuple(e) for e in data["edges"])
    assert drawn == real, (
        "map edges differ from the real import graph; "
        "missing=%s extra=%s"
        % (sorted(real - drawn)[:8], sorted(drawn - real)[:8])
    )


def test_every_mapped_module_is_a_real_file():
    data = _data()
    disk = _disk_modules()
    mapped = {i["id"] for i in data["items"] if i["kind"] == "module"}
    assert mapped == disk, (
        "map modules differ from disk; missing=%s extra=%s"
        % (sorted(disk - mapped)[:8], sorted(mapped - disk)[:8])
    )


def test_every_mapped_gap_is_a_real_gap_row():
    data = _data()
    gaps = bmm.parse_gap_ledger(_read(os.path.join(DOCS, "THE_GAP_LEDGER.md")))
    real = {g["id"] for g in gaps}
    mapped = {i["id"] for i in data["items"] if i["kind"] == "gap"}
    assert mapped == real, (
        "map gaps differ from THE_GAP_LEDGER.md; missing=%s extra=%s"
        % (sorted(real - mapped)[:8], sorted(mapped - real)[:8])
    )


def test_every_mapped_card_is_a_real_card():
    data = _data()
    cards = bmm.parse_claim_traceability(_read(os.path.join(DOCS, "CLAIM_TRACEABILITY.md")))
    real = {c["id"] for c in cards}
    mapped = {i["id"] for i in data["items"] if i["kind"] == "card"}
    assert mapped == real, (
        "map cards differ from CLAIM_TRACEABILITY.md; missing=%s extra=%s"
        % (sorted(real - mapped)[:8], sorted(mapped - real)[:8])
    )


def test_rendered_html_is_self_contained():
    """The HTML must embed its data and load nothing from the network."""
    html = _read(HTML)
    assert "const DATA = {" in html, "the HTML does not embed the map data"
    assert "fetch(" not in html, "the HTML must not fetch anything at runtime"
    assert not re.search(r'(src|href)="https?://', html), (
        "the HTML must not reference external resources"
    )


def test_rendered_html_quotes_the_current_counts():
    """The numbers rendered in the page must match the current data."""
    data = _data()
    html = _read(HTML)
    m = re.search(r"const DATA = (\{.*?\});\n", html, re.S)
    assert m, "the HTML does not embed the map data"
    embedded = json.loads(m.group(1))
    assert embedded["counts"] == data["counts"], (
        "the embedded counts %s differ from the current counts %s"
        % (embedded["counts"], data["counts"])
    )
    assert len(embedded["items"]) == len(data["items"]), (
        "the embedded item list is stale (%d vs %d)"
        % (len(embedded["items"]), len(data["items"]))
    )


def test_generated_json_is_loadable():
    with open(JSON_OUT, encoding="utf-8") as fp:
        data = json.load(fp)
    for key in ("items", "edges", "dims", "counts"):
        assert key in data, "the generated JSON is missing %r" % key
    assert data["counts"]["items"] == len(data["items"])
