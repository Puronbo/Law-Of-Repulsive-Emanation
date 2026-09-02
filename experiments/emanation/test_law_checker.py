import json
import os

import shift_bus as sh

from experiments.emanation import law_checker as lc
from experiments.emanation import traffic_law as tl


def _cert(label):
    for c in lc.open_certificates():
        if c["label"] == label:
            return c
    return None


def test_l1_free_streaming_pass_29():
    c = _cert("L1_free_streaming_29")
    assert c is not None
    assert c["status"] == "PASS", c.get("first_mismatch")
    assert c["first_mismatch"] is None
    assert c["configs_checked"] > 100
    assert c["points_checked"] > 1000


def test_l1_free_streaming_pass_71():
    c = _cert("L1_free_streaming_71")
    assert c is not None and c["status"] == "PASS"
    assert c["first_mismatch"] is None


def test_l2_melt_single_cluster_pass():
    for label in ("L2_melt_single_cluster_29", "L2_melt_single_cluster_71"):
        c = _cert(label)
        assert c is not None and c["status"] == "PASS", label
        assert c["first_mismatch"] is None


def test_l3_composition_mergerfree_pass():
    c = _cert("L3_composition_mergerfree_29")
    assert c is not None and c["status"] == "PASS", c.get("first_mismatch")
    assert c["meta"]["domain"].startswith("sampled")
    assert c["meta"].get("theorem") is not None


def test_honest_negatives_44_100():
    for label in ("HONEST_NEGATIVE_29law_on_44",
                  "HONEST_NEGATIVE_29law_on_100"):
        c = _cert(label)
        assert c is not None
        assert c["status"] == "HONEST_NEGATIVE", label
        fm = c["first_mismatch"]
        assert fm is not None
        # the mismatch must be real: truth computed by the actual rule
        T = fm["T"]
        assert sh.evolve(int(label.split("_")[-1]), fm["config"], 64,
                         T) == set(fm["actual"])


def test_honest_negative_free_streaming_on_contact():
    c = _cert("HONEST_NEGATIVE_free_streaming_on_touching")
    assert c is not None and c["status"] == "HONEST_NEGATIVE"
    assert any(b - a < 2 for a, b in
               zip(c["first_mismatch"]["config"], c["first_mismatch"]
                   ["config"][1:]))


def test_honest_negative_composition_merge_sector():
    c = _cert("HONEST_NEGATIVE_composition_merge_sector")
    assert c is not None and c["status"] == "HONEST_NEGATIVE"
    assert c["first_mismatch"]["config"] == [4, 7, 9, 10] \
        and c["first_mismatch"]["T"] == 6
    # truth recomputed from the actual rule: {10,12,14,16}
    assert c["first_mismatch"]["actual"] == [10, 12, 14, 16]
    # the too-optimistic union law predicted the trailing particle free
    assert c["first_mismatch"]["law"] == [10, 13, 14, 16]
    assert "retracted" in c["meta"]["claim_corrected"] or \
        "FALSE" in c["meta"]["claim_corrected"]


def test_verify_reports_true_mismatch():
    # law_trajectory(29) IS true for 29, but rule 44 differs somewhere
    dom = [(0, 1)]
    checked, first = lc.verify_trajectory_law(
        lambda conf, T: sh.evolve(44, conf, 64, T),
        lambda conf, T: tl.law_trajectory(29, list(conf), T),
        dom, range(1, 8))
    assert checked == 7
    assert first is not None
    assert first["config"] == [0, 1]
    assert set(first["actual"]) != set(first["law"])


def test_certificate_roundtrip():
    path = os.path.join(
        os.path.dirname(os.path.abspath(lc.__file__)), "data",
        "_law_cert_tmp.json")
    certs = lc.open_certificates()
    lc.save_certificates(certs, path)
    with open(path, encoding="utf-8") as fh:
        again = json.load(fh)
    os.remove(path)
    assert again == certs
    assert len(certs) == 9
    assert sum(c["status"] == "PASS" for c in certs) == 5
    assert sum(c["status"] == "HONEST_NEGATIVE" for c in certs) == 4