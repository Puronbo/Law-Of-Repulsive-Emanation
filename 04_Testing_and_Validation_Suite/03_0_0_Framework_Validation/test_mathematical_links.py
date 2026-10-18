"""Mathematical link graph: the verified insights joined to each other and to
their provided references.

`MATHEMATICAL_LINK_GRAPH.md` completes the coverage triangle alongside
`CLAIM_TRACEABILITY.md` (card -> our declarations), `PHYSICS_CROSSWALK.md`
(card -> physics) and `EXTERNAL_CORPORA_CROSSWALK.md` (module -> external corpus).
It adds two axes: the *internal* mesh (which machine-checked module is built on
which, read off the Lean `import` statements) and the *provided* references
(the citation in each module header, joined to a tracked framework document).

The checks, all offline:

1. the map exists, links `WHAT_THIS_DOES_NOT_PROVE.md`, and states the
   adjacency != equivalence rule;
2. the edge block equals the imports actually parsed from
   `.../PunoCalculus/**.lean` (no missing, extra, or self edges);
3. every module named in the edges or reference rows exists on disk, and every
   edge target resolves;
4. every in-header citation string in the reference table appears in its module;
5. every non-`--` provided document exists under the documentation directory;
6. all 38 card tokens ``C1 ... C38`` are present in the card list;
7. the stated `N module nodes` / `M directed edges` counts equal the real module
   and import counts, and every module on disk is enumerated as a node (so a new
   module cannot appear in the edge block yet be missing from the node lists).

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_mathematical_links.py -q
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_DIR = os.path.join(
    ROOT, "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)
MAP_MD = os.path.join(DOC_DIR, "MATHEMATICAL_LINK_GRAPH.md")

IMPORT_RE = re.compile(r"^import\s+PunoCalculus\.([\w.]+)", re.M)
EDGE_LINE_RE = re.compile(r"^\s*([\w.]+)\s*->\s*([\w.]+)\s*$")
REF_ROW_RE = re.compile(r"^\|")


def _read(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def _block(doc, name):
    """Text between <!-- NAME:BEGIN --> and <!-- NAME:END -->."""
    start = doc.index("<!-- %s:BEGIN -->" % name)
    end = doc.index("<!-- %s:END -->" % name)
    return doc[start:end]


def _module_path(name):
    return os.path.join(LEAN_DIR, *name.split(".")) + ".lean"


def _actual_edges():
    """(from, to) for every internal `import PunoCalculus.*` in the tree."""
    edges = set()
    for root, _dirs, files in os.walk(LEAN_DIR):
        for fname in files:
            if not fname.endswith(".lean"):
                continue
            path = os.path.join(root, fname)
            module = os.path.relpath(path, LEAN_DIR).replace("\\", ".")[:-5]
            for target in IMPORT_RE.findall(_read(path)):
                if target != module:
                    edges.add((module, target))
    return edges


def _disk_modules():
    """Every Lean module under PunoCalculus (recursively), dotted."""
    mods = set()
    for root, _dirs, files in os.walk(LEAN_DIR):
        for fname in files:
            if fname.endswith(".lean"):
                path = os.path.join(root, fname)
                mods.add(os.path.relpath(path, LEAN_DIR).replace("\\", ".")[:-5])
    return mods


def _doc_node_sets(doc):
    """(card_modules, noncard_modules) named in the 'Node labels' section."""
    seg = doc[doc.index("### Node labels"):doc.index("## 2.")]
    card = set()
    for line in seg.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for c in cells[0::2]:
            if c and c != "module" and not set(c) <= set("-: "):
                card.add(c)
    noncard = set(re.findall(r"`([^`]+)`", seg[seg.index("The remaining"):]))
    return card, noncard


def _doc_edges(doc):
    edges = set()
    for line in _block(doc, "EDGES").splitlines():
        m = EDGE_LINE_RE.match(line)
        if m:
            edges.add((m.group(1), m.group(2)))
    return edges


def _ref_rows(doc):
    rows = []
    for line in _block(doc, "REFS").splitlines():
        if not REF_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("module", "") or set(cells[0]) <= set("-: "):
            continue
        rows.append(tuple(cells))
    return rows


def _doc_cards(doc):
    return set(re.findall(r"\bC\d+\b", _block(doc, "CARDS")))


def test_map_exists_and_carries_scope_banner():
    assert os.path.isfile(MAP_MD), MAP_MD
    doc = _read(MAP_MD)
    assert "WHAT_THIS_DOES_NOT_PROVE.md" in doc, "map must link the scope boundary"
    low = doc.lower()
    assert "adjacency" in low and "equivalence" in low, (
        "map must state the adjacency != equivalence rule"
    )


def test_edge_block_equals_real_imports():
    doc = _read(MAP_MD)
    documented = _doc_edges(doc)
    actual = _actual_edges()
    assert documented, "no edges parsed from the map"
    missing = sorted(actual - documented)
    extra = sorted(documented - actual)
    assert not missing, "real imports absent from the map: %s" % missing
    assert not extra, "map lists edges that are not real imports: %s" % extra


def test_every_named_module_exists():
    doc = _read(MAP_MD)
    nodes = set()
    for a, b in _doc_edges(doc):
        nodes.add(a)
        nodes.add(b)
    for module, _citation, _dref in _ref_rows(doc):
        nodes.add(module)
    missing = sorted(n for n in nodes if not os.path.isfile(_module_path(n)))
    assert not missing, "modules named in the map with no file on disk: %s" % missing


def test_edge_targets_resolve():
    for _a, b in _doc_edges(_read(MAP_MD)):
        assert os.path.isfile(_module_path(b)), "edge target does not resolve: %s" % b


def test_in_header_citations_are_present():
    doc = _read(MAP_MD)
    bad = []
    for module, citation, _dref in _ref_rows(doc):
        src = _read(_module_path(module))
        if citation not in src:
            bad.append("%s: %r" % (module, citation))
    assert not bad, "citation not found in its module source: %s" % bad


def test_provided_documents_exist():
    doc = _read(MAP_MD)
    missing = []
    for _module, _citation, dref in _ref_rows(doc):
        if ".md" not in dref:
            continue
        if not os.path.isfile(os.path.join(DOC_DIR, dref)):
            missing.append(dref)
    assert not missing, "provided documents missing on disk: %s" % missing


def test_all_cards_present():
    doc = _read(MAP_MD)
    cards = _doc_cards(doc)
    expected = {"C%d" % i for i in range(1, 39)}
    missing = sorted(expected - cards)
    assert not missing, "card tokens missing from the card list: %s" % missing


def test_stated_module_and_edge_counts_match():
    doc = _read(MAP_MD)
    m_nodes = re.search(r"\*\*(\d+) module nodes\*\*", doc)
    m_edges = re.search(r"\*\*(\d+) directed edges\*\*", doc)
    assert m_nodes, "map must state '**N module nodes**'"
    assert m_edges, "map must state '**M directed edges**'"
    mods = _disk_modules()
    edges = _actual_edges()
    assert int(m_nodes.group(1)) == len(mods), (
        "map states %s module nodes, %d on disk" % (m_nodes.group(1), len(mods))
    )
    assert int(m_edges.group(1)) == len(edges), (
        "map states %s directed edges, %d real imports" % (m_edges.group(1), len(edges))
    )


def test_every_module_is_enumerated_as_a_node():
    card, noncard = _doc_node_sets(_read(MAP_MD))
    enumerated = card | noncard
    mods = _disk_modules()
    missing = sorted(mods - enumerated)
    extra = sorted(enumerated - mods)
    assert not missing, "modules on disk absent from the node lists: %s" % missing
    assert not extra, "node lists name modules with no file on disk: %s" % extra
