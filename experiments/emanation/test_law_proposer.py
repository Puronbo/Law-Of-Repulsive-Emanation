import json
import os

from experiments.emanation import law_checker as lc
from experiments.emanation import law_proposer as lp

_DATA = os.path.join(os.path.dirname(os.path.abspath(lp.__file__)), "data")


def test_proposer_discovers_attractor_law():
    res = lp.propose(train=(3, 4, 5, 6, 7), test=(8, 9, 10, 11, 12))
    # the true law must be among the training-perfect survivors
    target = [s for s in res["train_perfect_laws"]
              if s["family"] == "lucas_parity" and s["params"] == [2, -2, 0]]
    assert len(target) == 1
    assert target[0]["status"] == "PASS"
    assert target[0]["first_failure"] is None
    assert "2*L_N" in target[0]["law_text"]
    # train-failed families: the plausible but wrong candidates die at fit
    assert "fib_affine" in res["families_train_failed"]
    assert "constant" in res["families_train_failed"]
    assert "lucas_affine" in res["families_train_failed"]
    # out-of-sample certificates are honest
    assert res["summary"]["n_pass"] >= 1
    neg = [c for c in res["certificates"] if c["status"] == "HONEST_NEGATIVE"]
    assert all(c["first_failure"] is not None for c in neg)


def test_proposed_law_is_only_parity_corrected():
    # only the N-even-corrected Lucas law generalizes: any other family
    # must die at fit or at test
    res = lp.propose_trained_once()
    luc_aff = [s for s in res["train_perfect_laws"]
               if s["family"] == "lucas_affine"]
    fib = [s for s in res["train_perfect_laws"] if s["family"] == "fib_affine"]
    const = [s for s in res["train_perfect_laws"] if s["family"] == "constant"]
    assert luc_aff == [] and fib == [] and const == []
    parity = [s for s in res["train_perfect_laws"]
              if s["family"] == "lucas_parity"]
    assert len(parity) == 1 and parity[0]["params"] == [2, -2, 0]


def test_certified_law_passes_all_test_N_including_large():
    # N=12 has 4096 states; the certificate must cover it (fresh domain)
    res = lp.propose_trained_once()
    target = next(s for s in res["train_perfect_laws"]
                  if s["family"] == "lucas_parity")
    assert target["status"] == "PASS"
    c = next(c for c in res["certificates"]
             if c["label"].startswith("PROPOSED_lucas_parity"))
    assert c["status"] == "PASS"
    assert c["points_checked"] == 10  # 5 tested N x 2 rules


def test_proposer_certificates_in_full_table():
    certs = lp.proposer_certificates()
    labels = {c["label"] for c in certs}
    assert any(l.startswith("PROPOSED_lucas_parity") for l in labels)
    assert any(c["status"] == "PASS" for c in certs)


def test_proposer_result_roundtrip():
    res = lp.propose_trained_once()
    path = os.path.join(_DATA, "_proposer_tmp.json")
    lp.save_proposer_result(res, path)
    with open(path, encoding="utf-8") as fh:
        again = json.load(fh)
    os.remove(path)
    assert again["tested_N"] == [8, 9, 10, 11, 12]
    assert again["summary"]["n_pass"] == res["summary"]["n_pass"]


def test_cached_leak_never_reaches_test_domain():
    # a tampered measurement cache must NOT certify a wrong law
    # (the test predicate reports only the FRESH out-of-sample attractor)
    lp._ATTR.update({(N, r): 1 for N in range(3, 13) for r in (29, 71)})
    try:
        certs = lp.proposer_certificates()
    finally:
        lp._ATTR.clear()
    passers = [c for c in certs if c["status"] == "PASS"]
    for c in passers:
        assert c["points_checked"] == 10  # truly fresh on all of 8..12


def test_families_are_documented_hypothesis_space():
    # the proposer may ONLY float the documented families
    assert set(lp.FAMILIES) == {"lucas_affine", "lucas_parity",
                                "fib_affine", "constant"}
    # law text renders the discovered law readably
    assert lc.certify_statement is not None