"""law_proposer: the T2 seed -- an autonomous law-proposing agent kept
honest by the certificate gate.

Protocol (no human in the loop, no ungrounded claims):
    1. MEASURE  attractor sizes |A(N, rule)| over train N in a small
       interval for rules 29/71 (full 2^N state spaces).
    2. FIT      each small hypothesis family by exhaustive bounded
       integer search; keep only laws with ZERO error on the training
       domain.
    3. CERTIFY   every surviving law out-of-sample on fresh N (never
       seen at fit time) using law_checker.certify_statement.  A law is
       believed iff it passes on the fresh data (PASS); otherwise it is
       recorded HONEST_NEGATIVE with the exact first failure.
Families whose best fit already errs on training data are reported as
train_failed -- the proposer will not even float them.

Families searched (documented hypothesis space):
    lucas_affine : y = a*L_N + b            (independent sets of C_N)
    lucas_parity : y = a*L_N + (be if N even else bo)
    fib_affine   : y = a*F_{N+1} + b        (independent sets of P_N;
                                             control: plausible, wrong)
    constant     : y = c                    (control)
Expected outcome: only y = 2*L_N - 2*[N even] survives certification;
the fibonacci and constant looks-alikes must die at fit or at test.
"""
import itertools
import json
import os

from experiments.emanation import erasure_audit as ea
from experiments.emanation import law_checker as lc

_LAB = os.path.dirname(os.path.abspath(__file__))
_RESULTS = os.path.join(_LAB, "data", "law_proposer_results.json")

# memoize measured attractor sizes across calls (deterministic re-runs)
_ATTR = {}


def lucas(N):
    return lc.independent_sets_ring(N)


def fib(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a


def attractor_size(N, rule, use_cache=True):
    key = (N, rule)
    if use_cache and key in _ATTR:
        return _ATTR[key]
    domain = tuple(itertools.product((0, 1), repeat=N))
    acc, _ = ea.attractor(
        domain, lambda s, r=rule: ea.eca_ring_step(r, s), max_steps=48)
    size = len(acc)
    if use_cache:
        _ATTR[key] = size
    return size


# hypothesis families: (name, params tuple, fn(meta, params))
_RANGE_A = range(0, 5)
_RANGE_B = range(-4, 5)
_RANGE_C = range(700)


def _luc_aff(N, a, b):
    return a * lucas(N) + b


def _luc_par(N, a, be, bo):
    return a * lucas(N) + (be if N % 2 == 0 else bo)


def _fib_aff(N, a, b):
    return a * fib(N + 1) + b


def _const(N, c):
    return c


FAMILIES = {
    "lucas_affine": (_RANGE_A, _RANGE_B, _luc_aff),
    "lucas_parity": (_RANGE_A, _RANGE_B, _RANGE_B, _luc_par),
    "fib_affine": (_RANGE_A, _RANGE_B, _fib_aff),
    "constant": (_RANGE_C, _const),
}


def observable(keys, rules=(29, 71)):
    """{key: ys list parallel to rules} measured on the real attractor."""
    out = {}
    for key in keys:
        out[key] = [attractor_size(key, r) for r in rules]
    return out


def fit_laws(trains, rules=(29, 71)):
    """Exhaustive bounded fit; returns
    (survivors, train_failed): survivor = {family, params, law_text,
    train_keys}; train_failed lists families with no zero-error law."""
    survivors = []
    train_failed = []
    for fam, spec in FAMILIES.items():
        ranges = spec[:-1]
        fn = spec[-1]
        found = False
        for params in itertools.product(*ranges):
            for key in trains:
                for r, y in zip(rules, observable([key], rules)[key]):
                    if fn(key, *params) != y:
                        break
                else:
                    continue
                break
            else:
                # zero error on the whole training domain
                found = True
                survivors.append({"family": fam, "params": list(params),
                                  "law_text": _law_text(fam, params)})
        if not found:
            train_failed.append(fam)
    return survivors, train_failed


def _law_text(fam, params):
    if fam == "lucas_affine":
        a, b = params
        return "|A(N,29/71)| = %d*L_N %s %d" % (
            a, "+" if b >= 0 else "-", abs(b))
    if fam == "lucas_parity":
        a, be, bo = params
        return "|A(N,29/71)| = %d*L_N %s %d (N even) %s %d (N odd)" % (
            a, "+" if be >= 0 else "-", abs(be),
            "+" if bo >= 0 else "-", abs(bo))
    if fam == "fib_affine":
        a, b = params
        return "|A(N,29/71)| = %d*F_{N+1} %s %d" % (
            a, "+" if b >= 0 else "-", abs(b))
    return "|A(N,29/71)| = %d" % params[0]


def certify_survivors(survivors, tests, rules=(29, 71)):
    """Out-of-sample certificates for every training-perfect law.  The
    certified predicate calls the CURRENT attractor implementation and
    the CURRENT Lucas/Fibonacci counts -- no cached constant can leak in.
    The cached _ATTR measure table is NOT consulted on the test domain.
    """
    certs = []
    domain = [(N, r) for N in tests for r in rules]
    for s in survivors:
        pred = lambda d, fam=s["family"], p=s["params"]: (
            _apply(fam, p, d[0]) == attractor_size(
                d[0], d[1], use_cache=False))
        cert = lc.certify_statement(
            "PROPOSED_" + s["family"] + "_" + "_".join(map(str, s["params"])),
            {"domain": "out-of-sample (N, rule) in %s x {29,71}, attractor "
                       "over the full 2^N state space" % (tests,),
             "law": s["law_text"],
             "trained_on": "N in 3..7 (zero error on training)",
             "proposer": "law_proposer.fit_laws (exhaustive bounded "
                         "integer search over the documented families)"},
            pred, domain)
        certs.append(cert)
        s["status"] = cert["status"]
        s["first_failure"] = cert["first_failure"]
    return certs


def _apply(fam, params, N):
    if fam == "lucas_affine":
        return _luc_aff(N, *params)
    if fam == "lucas_parity":
        return _luc_par(N, *params)
    if fam == "fib_affine":
        return _fib_aff(N, *params)
    return _const(N, params[0])


def propose(train=(3, 4, 5, 6, 7), test=(8, 9, 10, 11, 12), rules=(29, 71)):
    """Full propose->certify run; returns the result record."""
    survivors, train_failed = fit_laws(list(train), rules=rules)
    certs = certify_survivors(survivors, list(test), rules=rules)
    result = {
        "trained_N": list(train),
        "tested_N": list(test),
        "rules": list(rules),
        "train_perfect_laws": survivors,
        "certificates": certs,
        "families_train_failed": train_failed,
        "summary": {
            "n_survivors": len(survivors),
            "n_pass": sum(1 for c in certs if c["status"] == "PASS"),
            "n_negative": sum(1 for c in certs
                              if c["status"] == "HONEST_NEGATIVE"),
        },
    }
    return result


def save_proposer_result(result, path=_RESULTS):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    return path


_TRAIN_ONCE = {"res": None}


def propose_trained_once(train=(3, 4, 5, 6, 7), test=(8, 9, 10, 11, 12),
                         rules=(29, 71)):
    """The canonical propose->certify run, computed at most once per
    process (attractor measurements are memoized, so recompute is cheap;
    this wrapper just pins the headline result for tests/docs)."""
    if _TRAIN_ONCE["res"] is None:
        _TRAIN_ONCE["res"] = propose(train=train, test=test, rules=rules)
    return _TRAIN_ONCE["res"]


def proposer_certificates():
    """The certified survivors, as statements in the full table."""
    return certify_survivors(*_rep(), (29, 71))


def _rep():
    survivors, _ = fit_laws(list(range(3, 8)))
    return survivors, list(range(8, 13))


if __name__ == "__main__":
    res = propose_trained_once()
    save_proposer_result(res)
    print("proposed: %d training-perfect laws; certificates: "
          "%d PASS / %d HONEST_NEGATIVE; families failing at train: %s"
          % (len(res["train_perfect_laws"]), res["summary"]["n_pass"],
             res["summary"]["n_negative"],
             res["families_train_failed"] or "none"))
    for s in res["train_perfect_laws"]:
        print("  %-10s %-14s %s" % (s["family"], s["status"], s["law_text"]))