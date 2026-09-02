import json
import os

from experiments.emanation import erasure_audit as ea
from experiments.emanation import law_checker as lc
from experiments.emanation import supervisor as sv

_DATA = os.path.join(os.path.dirname(os.path.abspath(sv.__file__)), "data")


def test_statement_certificate_pass_and_fail():
    certs = lc.statement_certificates()
    good = [c for c in certs if c["label"] == "L13_ring_attractor_29_71"][0]
    bad = [c for c in certs if c["label"] == "L13_bad_even_omitted"][0]
    assert good["kind"] == "statement" and good["status"] == "PASS"
    assert good["points_checked"] == 14
    assert bad["status"] == "HONEST_NEGATIVE"
    assert bad["first_failure"] is not None


def test_statement_bad_law_domain_checked():
    # the flawed candidate (no even correction) fails exactly on even N:
    # recompute attractor sizes directly and compare to 2*L_N
    import itertools
    failing = sorted({N for N in range(3, 10)
                      for rule in (29, 71)
                      if (lambda d, r=rule, N=N: len(ea.attractor(
                          d, lambda s, r=r: ea.eca_ring_step(r, s),
                          max_steps=48)[0]) != 2 * lc.independent_sets_ring(N))
                      (tuple(itertools.product((0, 1), repeat=N)))})
    assert failing == [4, 6, 8]


def test_attractor_formula_recomputed():
    # L13 ground truth: independent-set counts and the attractor tool
    assert lc.independent_sets_ring(8) == 47
    assert lc.independent_sets_ring(5) == 11
    c = [c for c in lc.statement_certificates()
         if c["label"] == "L13_ring_attractor_29_71"][0]
    assert c["status"] == "PASS"


def test_supervisor_accepts_and_rejects():
    certs = lc.all_certificates()
    verdict = sv.supervise_build(sv.demo_claims(), certs)
    assert verdict["accepted"] is False          # demo includes rejects
    by_law = {r["law"]: r for r in verdict["results"]}
    assert by_law["L1 free streaming (rule 29, sector gap>=2)"]["ok"] is True
    assert by_law["29-traffic law as a law of rule 44 (must reject)"]["ok"] \
        is False
    assert "HONEST_NEGATIVE" in by_law[
        "29-traffic law as a law of rule 44 (must reject)"]["rejection_reasons"][0]
    assert by_law["a law we never certified (must reject)"]["ok"] is False
    assert by_law["rule 29 ring attractor = 2*L_N (must reject, even N)"]["ok"] \
        is False


def test_supervisor_clean_build_accepted():
    certs = lc.all_certificates()
    claims = [
        {"law": "L1 free streaming", "requires": ["L1_free_streaming_29"]},
        {"law": "melt window", "requires": ["L2_melt_single_cluster_29"]},
        {"law": "ring attractor law",
         "requires": ["L13_ring_attractor_29_71"]},
    ]
    verdict = sv.supervise_build(claims, certs)
    assert verdict["accepted"] is True
    assert verdict["n_negative_claims"] == 0


def test_supervisor_zero_points_cert_nov_evidence():
    certs = lc.all_certificates()
    fake = {"label": "X_EMPTY", "status": "PASS", "points_checked": 0}
    verdict = sv.supervise_build(
        [{"law": "empty evidence", "requires": ["X_EMPTY"]}], certs + [fake])
    assert verdict["accepted"] is False
    assert "zero checked points" in verdict["results"][0]["rejection_reasons"][0]


def test_supervisor_verdict_roundtrip():
    certs = lc.all_certificates()
    path = os.path.join(_DATA, "_verdict_tmp.json")
    sv.write_verdict(sv.demo_claims(), certs, path)
    with open(path, encoding="utf-8") as fh:
        again = json.load(fh)
    os.remove(path)
    assert again["n_claims"] == 8
    assert again["accepted"] is False
    assert "timestamp" in again


def test_certificate_table_roundtrip_with_statements():
    # the persisted law_certificates.json must contain the statements
    path = os.path.join(_DATA, "law_certificates.json")
    with open(path, encoding="utf-8") as fh:
        again = json.load(fh)
    labels = {c["label"] for c in again}
    assert "L13_ring_attractor_29_71" in labels
    assert "L13_bad_even_omitted" in labels


def test_veto_rejects_claim_over_unsolved_rule():
    from experiments.emanation import law_discovery as ld
    claims, veto = ld.discovery_claims()
    assert 105 in veto and 150 in veto and 29 not in veto
    # even a PASS-looking certificate cannot save a claim over a vetoed rule
    fake = {"label": ld.cert_label(105, "orbit2", [1, 0]), "status": "PASS",
            "points_checked": 3}
    verdict = sv.supervise_build(
        [{"law": "rule 105 attractor is 2^N",
          "requires": [ld.cert_label(105, "orbit2", [1, 0])], "rule": 105}],
        [fake], veto=veto)
    assert verdict["accepted"] is False
    reasons = verdict["results"][0]["rejection_reasons"]
    assert "vetoed by the discovery self-report" in reasons[0]


def test_veto_allows_certified_rule():
    from experiments.emanation import law_discovery as ld
    claims, veto = ld.discovery_claims()
    c29 = next(c for c in claims if c.get("rule") == 29)
    certs = ld.discovery_certificates()
    verdict = sv.supervise_build(claims, certs, veto=veto)
    assert verdict["accepted"] is True
    assert verdict["n_claims"] == len(claims)
    assert verdict["n_negative_claims"] == 0


def test_veto_lists_failed_to_generalize_kind():
    # a fabricated self-report with a fails-to-generalize rule must veto it
    from experiments.emanation import law_discovery as ld
    rep = ld.discovery_report_from_persisted()
    rep = dict(rep)
    rep["table"] = dict(rep["table"])
    rep["table"]["90"] = {"kind": "failed_to_generalize",
                          "family": "lucas", "params": [1, 0],
                          "law": "|A(N,r)| = 1*L_N + 0"}
    path = os.path.join(_DATA, "_veto_tmp.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"report": rep}, fh)
    try:
        _, veto = ld.discovery_claims(path)
        assert veto.get(90) == "failed_to_generalize"
        verdict = sv.supervise_build(
            [{"law": "rule 90 is lucas-like",
              "requires": ["DISCOVERED_r90_lucas_1_0"], "rule": 90}],
            [], veto=veto)
        assert verdict["accepted"] is False
        assert "failed_to_generalize" in \
            verdict["results"][0]["rejection_reasons"][0]
    finally:
        os.remove(path)