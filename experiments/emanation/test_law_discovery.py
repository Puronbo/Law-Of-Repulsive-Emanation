import json
import os

from experiments.emanation import law_discovery as ld

_DATA = os.path.join(os.path.dirname(os.path.abspath(ld.__file__)), "data")


def test_known_laws_are_certified():
    rep = ld.discover(rules=(0, 12, 29, 71, 204, 240))
    t = rep["table"]
    assert t["0"]["kind"] == "certified" and t["0"]["law"].endswith("= 1")
    assert t["204"]["kind"] == "certified"
    assert t["204"]["law"] == "|A(N,r)| = 1*2^N + 0"
    assert t["240"]["law"] == "|A(N,r)| = 1*2^N + 0"
    for r in ("29", "71"):
        e = t[r]
        assert e["kind"] == "certified"
        assert e["family"] == "lucas_parity"
        assert e["params"] == [2, -2, 0]
        assert "2*L_N" in e["law"]


def test_rule_12_is_lucas():
    e = ld.discover(rules=(12,))["table"]["12"]
    assert e["kind"] == "certified" and e["family"] == "lucas"
    assert e["params"] == [1, 0]  # |A(N,12)| = L_N exactly


def test_105_and_150_are_not_blessed_as_permutations():
    rep = ld.discover(rules=(105, 150))
    for r in ("105", "150"):
        assert rep["table"][r]["kind"] == "no_small_form_law"
    # the mod-3 defect is a measured fact: bijective iff 3 does not
    # divide N (permutation census 'exactly 8' holds only at N=8)
    for r in (105, 150):
        sizes = {N: ld.measure(r, N) for N in (5, 7, 9, 10)}
        assert sizes[5] == 2 ** 5 and sizes[7] == 2 ** 7
        assert sizes[10] == 2 ** 10
        assert sizes[9] == 2 ** 7  # 3 | 9 -> 128, not 512


def test_agent_refuses_generalization_when_train_permits():
    # if a rule's attractor deviates only past training, certification
    # must catch it out-of-sample (design guarantee of the layer)
    for rule in (105, 150):
        assert ld.fit(rule, (3, 4, 5, 6)) == []  # no zero-train-error law
    # training on a fallacious window (only N coprime to 3) floats the
    # wrong 2^N law, but the fresh test domain includes N=9 -> negative
    survivors = ld.fit(105, (5, 7, 10)) or ld.fit(105, (5, 7, 8))
    if survivors:
        picked, passed = ld.certify(105, survivors[:1], (5, 7, 8),
                                    (6, 9))
        assert picked["status"] == "HONEST_NEGATIVE"
        assert passed is False


def test_landscape_is_deterministic():
    a = ld.discover(rules=(1, 2, 3, 7, 21, 34, 68))
    b = ld.discover(rules=(1, 2, 3, 7, 21, 34, 68))
    assert a["table"] == b["table"]
    assert a["summary"] == b["summary"]


def test_drift_detection_tampered_table():
    path = os.path.join(_DATA, "_drift_tmp.json")
    with open(os.path.join(_DATA, "law_discovery_table.json"),
              encoding="utf-8") as fh:
        saved = json.load(fh)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(saved, fh)
    saved["report"]["table"]["29"]["params"] = [3, -3999, 0]
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(saved, fh)
    try:
        ok, why = ld.fresh(path)
        assert ok is False and why is not None
    finally:
        os.remove(path)


def test_verdict_self_report_completeness():
    rep = ld.discover()  # full 256 scan (3s, memoized)
    assert rep["summary"]["scanned"] == 256
    assert rep["summary"]["certified"] \
        + rep["summary"]["failed_to_generalize"] \
        + rep["summary"]["no_small_form_law"] \
        + rep["summary"]["measurement_inconclusive"] == 256
    certified = [e for e in rep["table"].values()
                 if e["kind"] == "certified"]
    assert any("2*L_N" in e["law"] for e in certified)   # 29/71
    assert any("2^N" in e["law"] for e in certified)     # permutations
    assert any(e["law"] == "|A(N,r)| = 1" for e in certified)  # rule 0
    # every certified law passed strictly out-of-sample on fresh N
    for e in certified:
        assert e["points_checked"] == len(rep["tests"])


def test_zoo_contract():
    assert set(ld.ZOO_FAMILIES) == {"constant", "linear", "quadratic",
                                    "lucas", "lucas_parity", "fib",
                                    "orbit2", "orbit3"}
    assert set(ld.ZOOS) == set(ld.ZOO_FAMILIES)