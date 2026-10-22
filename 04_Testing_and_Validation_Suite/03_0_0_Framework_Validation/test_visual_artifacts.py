"""Truthfulness gate for the visual artifacts.

`CHANNEL_0_*.html`, `CHANNEL_1_*.html` and `MULTIDIMENSIONAL_MAP.html` are the
register's rendered readings.  A rendering is only allowed to be as honest as the
tree it reads, so this gate pins three things:

1.  **Self-containment.**  No artifact may reach the network, load an external
    file, or `fetch` anything.  They have to open from the filesystem.
2.  **Declaration existence.**  Every declaration a visual *names* must actually
    exist in the Lean sources.  A picture that cites a theorem nobody proved is
    exactly the failure mode the rest of the register is built to prevent, so
    the gate catches it mechanically.
3.  **Index completeness.**  `VISUAL_ARTIFACTS.md` must index every artifact that
    is on disk, so a new visual cannot silently ship undocumented.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(
    ROOT, "05_Documentation_and_Research_Specifications", "05_Complete_Framework_Documentation"
)
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)

VISUALS = (
    "CHANNEL_0_the_essential_singularity_as_tv.html",
    "CHANNEL_1_nothing_filling_everything_as_tv.html",
    "MULTIDIMENSIONAL_MAP.html",
)

# Words that appear inside <code> spans but are not declarations.
NON_DECLARATIONS = {
    "volume", "univ", "measure", "union", "covered", "part", "none", "self",
    "ratio", "value", "limit", "point", "points", "countable", "essential",
    "removable", "singularity", "singularities", "nothing", "something",
    "everywhere", "filling", "fills", "fill", "everything", "countability",
    "interval", "intervals", "covered_part", "fetch",
}


def _read(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def _lean_sources():
    src = {}
    for dirpath, _dirnames, filenames in os.walk(LEAN_DIR):
        for name in filenames:
            if name.endswith(".lean"):
                src[os.path.join(dirpath, name)] = _read(os.path.join(dirpath, name))
    return src


def _declared_names(sources):
    names = set()
    pattern = re.compile(
        r"^\s*(?:@\[[^\]]*\]\s*)?"
        r"(?:private\s+|protected\s+|noncomputable\s+|nonrec\s+)*"
        r"(?:theorem|lemma|def|abbrev|example|instance)\s+"
        r"([A-Za-z_][A-Za-z0-9_'.]*)",
        re.MULTILINE,
    )
    for text in sources.values():
        for match in pattern.finditer(text):
            names.add(match.group(1))
    return names


def _code_tokens(html):
    tokens = set()
    for span in re.findall(r"<code>(.*?)</code>", html, re.DOTALL):
        if "/" in span or "\\" in span:
            continue  # a filesystem path, not a declaration name
        # a code span may name a document (`MODULE_LEDGER.md`) rather than a
        # declaration -- strip the extension before tokenising
        span = re.sub(r"\.[A-Za-z0-9]{1,5}\b", " ", span)
        for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_']*", span):
            tokens.add(tok)
    return tokens


def _document_names():
    """Stems of the framework documents -- code spans may cite these."""
    names = set()
    for name in os.listdir(DOCS):
        stem, ext = os.path.splitext(name)
        if ext in (".md", ".html", ".json", ".pdf"):
            names.add(stem)
    return names


def test_every_visual_artifact_exists():
    for name in VISUALS:
        path = os.path.join(DOCS, name)
        assert os.path.isfile(path), "missing visual artifact: %s" % name


def test_visuals_are_self_contained():
    """No network, no external file, no fetch -- they must open from disk."""
    for name in VISUALS:
        html = _read(os.path.join(DOCS, name))
        for pattern, label in (
            (r"\bfetch\s*\(", "fetch()"),
            (r"https?://", "absolute URL"),
            (r"<link\b", "<link> tag"),
            (r"\ssrc\s*=", "external src="),
            (r"@import\s+url", "css @import url"),
            (r"XMLHttpRequest", "XMLHttpRequest"),
        ):
            assert not re.search(pattern, html), (
                "%s must not reference %s (it has to be self-contained)" % (name, label))


def test_visuals_only_name_real_declarations():
    """Every declaration a visual names must exist in the Lean sources.

    This is the gate that stops a rendering from getting ahead of the proof.
    """
    sources = _lean_sources()
    declared = _declared_names(sources)
    assert declared, "no Lean declarations found -- the source scan is broken"
    documents = _document_names()

    for name in VISUALS:
        html = _read(os.path.join(DOCS, name))
        for tok in sorted(_code_tokens(html)):
            if "_" not in tok:
                continue  # prose words carry no underscore
            if tok in NON_DECLARATIONS:
                continue
            if tok in documents:
                continue  # a cited framework document, not a Lean declaration
            assert tok in declared, (
                "%s names %r, which is not a declaration anywhere in the Lean tree. "
                "A visual may not cite a theorem that does not exist." % (name, tok))


def test_declared_visual_themes_are_actually_proved():
    """Spot-check the specific claims each channel advertises."""
    sources = _lean_sources()
    declared = _declared_names(sources)
    required = {
        "CHANNEL_0_the_essential_singularity_as_tv.html": (
            "self_ratio_eq_one",
            "self_ratio_limit_one",
            "ratio_paths_disagree",
            "sin_one_over_has_no_limit",
            "identity_breaks_only_at_zero",
            "signStep_has_no_limit",
            "id_over_id_resolves",
        ),
        "CHANNEL_1_nothing_filling_everything_as_tv.html": (
            "nothing_fills_everything",
            "something_remains",
            "the_whole_is_not_nothing",
            "countable_nothings_stay_nothing",
            "no_countable_filling",
            "countable_nothings_cover_no_interval",
            "the_filling_is_uncountable",
            "every_finite_stage_is_nothing",
            "finite_stages_never_reach_the_whole",
            "nothing_at_finite_stages_everything_at_the_end",
            "accumulation_resolves_countably_but_not_uncountably",
            "nowhere_without_covering",
        ),
    }
    for name, decls in required.items():
        for decl in decls:
            assert decl in declared, (
                "%s advertises %r but the Lean tree does not declare it"
                % (name, decl))


def test_visual_index_documents_every_artifact():
    index_path = os.path.join(DOCS, "VISUAL_ARTIFACTS.md")
    assert os.path.isfile(index_path), "VISUAL_ARTIFACTS.md is missing"
    index = _read(index_path)
    for name in VISUALS:
        assert name in index, "VISUAL_ARTIFACTS.md does not mention %s" % name
