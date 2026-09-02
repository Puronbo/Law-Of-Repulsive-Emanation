"""law_discovery: the self-directed discovery agent (T2) over the whole
256-rule space.

The agent owns its epistemology: it MEASURES the attractor of every rule
on rings (full 2^N state spaces), FITS candidate laws from a documented
hypothesis zoo, and CERTIFIES every train-perfect candidate out-of-sample
on fresh N it has never seen.  It then files an honest self-report:
    certified              : rule has a law, certified PASS out-of-sample;
    failed_to_generalize   : a law was perfect on training data but the
                             agent refused to believe it at test time;
    no_small_form_law      : no zero-error law exists in the documented
                             zoo (possibly N-dependent structure -- e.g.
                             nilpotency that holds only for certain N).
The report is machine-readable (`data/law_discovery_table.json` +
`data/discovery_verdict.json`) and the CI gate refuses a stale discovery
self-report -- the system may not silently forget what it failed to know.

Hypothesis zoo (documented, bounded exhaustive integer coefficients;
family names are the contract):
    constant     y = c
    linear       y = a*N + b
    quadratic    y = a*N^2 + b*N + c
    lucas        y = a*L_N + b          (independent sets of C_N)
    lucas_parity y = a*L_N + (be if N even else bo)
    fib          y = a*F_{N+1} + b      (independent sets of P_N)
    orbit2       y = a*2^N + b
    orbit3       y = a*3^N + b
"""
import itertools
import json
import os
import time

from experiments.emanation import erasure_audit as ea
from experiments.emanation import law_checker as lc
from experiments.emanation import law_proposer as lp

_LAB = os.path.dirname(os.path.abspath(__file__))
_TBL = os.path.join(_LAB, "data", "law_discovery_table.json")
_VER = os.path.join(_LAB, "data", "discovery_verdict.json")
_ALL_RULES = tuple(range(256))

# measured sizes, memoized in-process (deterministic pure measurements)
_SIZES = {}
# (rule, N) -> len(attractor) or None if the attractor did not close
_INCONCLUSIVE = set()


def measure(rule, N, max_steps=64):
    """Attractor size of rule on the N-ring over the full 2^N state
    space; None if closure was not reached within max_steps (that point
    is then excluded from fit and certification)."""
    key = (rule, N)
    if key not in _SIZES:
        domain = tuple(itertools.product((0, 1), repeat=N))
        acc, closed = ea.attractor(
            domain, lambda s, r=rule: ea.eca_ring_step(r, s),
            max_steps=max_steps)
        _SIZES[key] = len(acc) if closed else None
        if not closed:
            _INCONCLUSIVE.add(key)
    return _SIZES[key]


def lucas(N):
    return lc.independent_sets_ring(N)


def fib(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a


_RB = range(-13, 14)


def _y(N, fam, params):
    if fam == "constant":
        return params[0]
    if fam == "linear":
        a, b = params
        return a * N + b
    if fam == "quadratic":
        a, b, c = params
        return a * N * N + b * N + c
    if fam == "lucas":
        a, b = params
        return a * lucas(N) + b
    if fam == "lucas_parity":
        a, be, bo = params
        return a * lucas(N) + (be if N % 2 == 0 else bo)
    if fam == "fib":
        a, b = params
        return a * fib(N + 1) + b
    if fam == "orbit2":
        a, b = params
        return a * (1 << N) + b
    if fam == "orbit3":
        a, b = params
        return a * (3 ** N) + b
    raise KeyError(fam)


ZOOS = {
    "constant": (range(0, 3000),),
    "linear": (range(0, 9), _RB),
    "quadratic": (range(0, 7), range(0, 7), _RB),
    "lucas": (range(0, 7), _RB),
    "lucas_parity": (range(0, 7), _RB, _RB),
    "fib": (range(0, 7), _RB),
    "orbit2": (range(0, 6), _RB),
    "orbit3": (range(0, 3), _RB),
}
ZOO_FAMILIES = tuple(ZOOS)


def _law_text(fam, params):
    if fam == "constant":
        return "|A(N,r)| = %d" % params[0]
    if fam == "linear":
        a, b = params
        return "|A(N,r)| = %d*N %s %d" % (a, "+" if b >= 0 else "-", abs(b))
    if fam == "quadratic":
        a, b, c = params
        return ("|A(N,r)| = %d*N^2 %s %d*N %s %d"
                % (a, "+" if b >= 0 else "-", abs(b),
                   "+" if c >= 0 else "-", abs(c)))
    if fam == "lucas":
        a, b = params
        return "|A(N,r)| = %d*L_N %s %d" % (a, "+" if b >= 0 else "-", abs(b))
    if fam == "lucas_parity":
        a, be, bo = params
        return ("|A(N,r)| = %d*L_N %s %d (N even) %s %d (N odd)"
                % (a, "+" if be >= 0 else "-", abs(be),
                   "+" if bo >= 0 else "-", abs(bo)))
    if fam == "fib":
        a, b = params
        return "|A(N,r)| = %d*F_{N+1} %s %d" % (a, "+" if b >= 0 else "-",
                                                abs(b))
    if fam == "orbit2":
        a, b = params
        return "|A(N,r)| = %d*2^N %s %d" % (a, "+" if b >= 0 else "-", abs(b))
    return "|A(N,r)| = %d*3^N %s %d" % (params[0],
                                        "+" if params[1] >= 0 else "-",
                                        abs(params[1]))


def fit(rule, trains):
    """ALL zero-error-on-training survivors from the documented zoo
    (every family gets a chance; out-of-sample judges)."""
    ys = {N: measure(rule, N) for N in trains}
    if any(v is None for v in ys.values()):
        return None
    survivors = []
    for fam in ZOO_FAMILIES:
        ranges = ZOOS[fam]
        for params in itertools.product(*ranges):
            for N in trains:
                if _y(N, fam, params) != ys[N]:
                    break
            else:
                survivors.append({"family": fam, "params": list(params),
                                  "law_text": _law_text(fam, params)})
    return survivors


def cert_label(rule, family, params):
    """The canonical certificate label of a discovered law (the label the
    supervisor's formal claims must name; MUST match the label emitted by
    the certificate builder below)."""
    return "DISCOVERED_r%d_%s_%s" % (rule, family,
                                     "_".join(map(str, params)))


def statement_certificate(rule, survivor, trains, tests):
    """The machine-readable PASS/negative certificate for one discovery
    law, recomputed fresh at every call (deterministic, out-of-sample on
    the CURRENT attractor implementation -- no cached measurement)."""
    label = cert_label(rule, survivor["family"], survivor["params"])
    domain = [(N, rule) for N in tests]
    pred = lambda d, s=survivor: _y(d[0], s["family"], s["params"]) == \
        measure(d[1], d[0])
    return lc.certify_statement(
        label,
        {"domain": "out-of-sample (N, rule) in %s (full 2^N state "
                   "spaces)" % (list(tests),),
         "law": survivor["law_text"],
         "trained_on": "N in %s (zero error; documented zoo fit)"
                       % (list(trains),),
         "proposer": "law_discovery.fit (bounded exhaustive integer "
                     "search over the documented zoo)"},
        pred, domain)


def certify(rule, survivors, trains, tests):
    """Every survivor goes out-of-sample; first PASS (zoo order) wins,
    otherwise the first survivor is reported with its first failure."""
    picked = None
    fails = []
    for s in survivors:
        cert = statement_certificate(rule, s, trains, tests)
        s["status"] = cert["status"]
        s["first_failure"] = cert["first_failure"]
        s["points_checked"] = cert["points_checked"]
        if cert["status"] == "PASS":
            picked = s
            break
        fails.append(s)
    if picked is None and survivors:
        picked = fails[0]
    return picked, (picked is not None and picked["status"] == "PASS")


def discovery_certificates(table=_TBL):
    """PASS certificates for every rule the discovery self-report
    certified -- the discovery layer's contribution to the shared gate
    table (joins lab + system + proposer certificates).  Computed fresh
    from the CURRENT code and the CURRENT attractor implementation."""
    report = discovery_report_from_persisted(table)
    trains, tests = report["trains"], report["tests"]
    certs = []
    for rule, entry in report["table"].items():
        if entry["kind"] != "certified":
            continue
        surv = [{"family": entry["family"], "params": entry["params"],
                 "law_text": entry["law"]}]
        certs.append(statement_certificate(int(rule), surv[0], trains,
                                           tests))
    return certs


def discovery_claims(table=_TBL):
    """Auto-derived formal claims + veto registry from the discovery
    self-report.  claims: for every rule the agent certified, a claim
    requiring its DISCOVERED certificate.  veto: {rule: kind} for every
    rule the agent classified unsolved -- no believed claim may name
    those rules (the system cannot bless its own ungeneralized guesses,
    nor any guess a human floats over an unsolved rule)."""
    report = discovery_report_from_persisted(table)
    claims = []
    veto = {}
    for rule, entry in report["table"].items():
        if entry["kind"] == "certified":
            claims.append({
                "law": "rule %s attractor law (self-discovered, "
                       "out-of-sample certified): %s" % (rule, entry["law"]),
                "requires": [cert_label(int(rule), entry["family"],
                                        entry["params"])],
                "rule": int(rule),
            })
        elif entry["kind"] in ("no_small_form_law", "failed_to_generalize",
                               "measurement_inconclusive"):
            veto[int(rule)] = entry["kind"]
    return claims, veto


def discover(rules=None, trains=(3, 4, 5, 6), tests=(8, 9, 10)):
    """Full self-directed scan of the rule space; returns the report."""
    rules = list(_ALL_RULES if rules is None else rules)
    table = {}
    summary = {"scanned": len(rules), "certified": 0,
               "failed_to_generalize": 0, "no_small_form_law": 0,
               "measurement_inconclusive": 0}
    for rule in rules:
        survivors = fit(rule, trains)
        if survivors is None:
            summary["measurement_inconclusive"] += 1
            table[str(rule)] = {"kind": "measurement_inconclusive",
                                "note": "attractor did not close within "
                                        "the measurement budget"}
            continue
        if not survivors:
            summary["no_small_form_law"] += 1
            table[str(rule)] = {"kind": "no_small_form_law",
                                "note": "no zero-error law in the "
                                        "documented zoo on training"}
            continue
        survivor, passed = certify(rule, survivors, trains, tests)
        if passed:
            summary["certified"] += 1
            table[str(rule)] = {"kind": "certified",
                                "family": survivor["family"],
                                "params": survivor["params"],
                                "law": survivor["law_text"],
                                "points_checked": survivor["points_checked"]}
        else:
            summary["failed_to_generalize"] += 1
            table[str(rule)] = {"kind": "failed_to_generalize",
                                "family": survivor["family"],
                                "params": survivor["params"],
                                "law": survivor["law_text"],
                                "first_failure": survivor["first_failure"]}
    return {"trains": list(trains), "tests": list(tests),
            "zoo": list(ZOO_FAMILIES), "table": table, "summary": summary}


def save_discovery(report, tbl=_TBL, ver=_VER):
    with open(tbl, "w", encoding="utf-8") as fh:
        json.dump({"report": report}, fh, indent=1, sort_keys=True)
    verdict = {
        "scanned_rules": report["summary"]["scanned"],
        "certified_laws": report["summary"]["certified"],
        "failed_to_generalize": report["summary"]["failed_to_generalize"],
        "no_small_form_law": report["summary"]["no_small_form_law"],
        "measurement_inconclusive": report["summary"]
            ["measurement_inconclusive"],
        "zoo": list(ZOO_FAMILIES),
        "certified_laws_by_rule": {
            k: v["law"] for k, v in report["table"].items()
            if v["kind"] == "certified"},
        "honesty": "no_small_form_law and failed_to_generalize are "
                   "first-class facts, shipped with the certified laws; "
                   "the gate refuses a stale report.",
    }
    with open(ver, "w", encoding="utf-8") as fh:
        json.dump(verdict, fh, indent=1, sort_keys=True)
    return tbl, ver


def discovery_report_from_persisted(tbl=_TBL):
    with open(tbl, encoding="utf-8") as fh:
        return json.load(fh)["report"]


def fresh(tbl=_TBL):
    """Refit + recertify from the persisted measured facts and compare to
    the persisted report (drift detection for the discovery layer)."""
    report = discovery_report_from_persisted(tbl)
    again = discover(rules=[int(r) for r in report["table"]],
                     trains=report["trains"], tests=report["tests"])
    # compare only the judgement (family/params/status) on common points
    for rule, entry in report["table"].items():
        other = again["table"].get(rule)
        if other is None:
            return False, "rule %s missing on refit" % rule
        if entry["kind"] != other["kind"]:
            return False, "rule %s kind %s != %s" % (rule, entry["kind"],
                                                     other["kind"])
        if entry["kind"] in ("certified", "failed_to_generalize"):
            if entry["family"] != other["family"] or \
                    entry["params"] != other["params"]:
                return False, "rule %s law drifted" % rule
    return True, None


if __name__ == "__main__":
    import sys
    args = set(sys.argv[1:])
    if "--regenerate" in args:
        t0 = time.time()
        rep = discover()
        save_discovery(rep)
        print("discovery regenerated: %d rules scanned in %.1fs; "
              "%d certified / %d failed to generalize / "
              "%d no small-form law"
              % (rep["summary"]["scanned"], time.time() - t0,
                 rep["summary"]["certified"],
                 rep["summary"]["failed_to_generalize"],
                 rep["summary"]["no_small_form_law"]))
    if "--gate" in args:
        ok, why = fresh()
        if not ok:
            print("discovery gate: STALE (%s)" % why)
            sys.exit(1)
        print("discovery gate: fresh (self-report matches current code)")