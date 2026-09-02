"""Law supervisor (T1): the process that decides which law-claims a
system may rely on, using ONLY machine-readable certificates.

Rules of belief:
    * a claim is believed iff EVERY certificate it names as its
      `requires` has status PASS in the certified table;
    * a needed HONEST_NEGATIVE certificate rejects the claim, carrying
      the exact counter-example (first_mismatch / first_failure);
    * a needed certificate that does not exist rejects the claim as
      UNCERTIFIED (no belief without a certificate);
    * a PASS certificate with zero checked points is not evidence.

Output: a JSON verdict (data/supervision_verdict.json) -- the audit log
of which claims this build is allowed to believe and why.  A supervisor
never invents truth; it only enforces the boundary between verified and
unverified.
"""
import json
import os
import time

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
_CERTS = os.path.join(_DATA, "law_certificates.json")
_VERDICT = os.path.join(_DATA, "supervision_verdict.json")


def load_certificates(path=_CERTS):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def status_of(certs, label):
    """(status, certificate_or_None): PASS / HONEST_NEGATIVE /
    UNCERTIFIED."""
    for c in certs:
        if c["label"] == label:
            return c["status"], c
    return "UNCERTIFIED", None


def supervise_build(claims, certs):
    """claims: list of {law, requires:[cert labels]}.  Returns the
    per-claim results plus the build-level verdict."""
    results = []
    for claim in claims:
        ok = True
        reasons = []
        evidence = []
        for lbl in claim.get("requires", []):
            status, c = status_of(certs, lbl)
            if status == "PASS":
                if (c.get("points_checked") or 0) < 1:
                    ok = False
                    reasons.append("certificate %s has zero checked points"
                                   % lbl)
                evidence.append(lbl)
            elif status == "UNCERTIFIED":
                ok = False
                reasons.append("required certificate %r not in table" % lbl)
            else:  # HONEST_NEGATIVE
                ok = False
                reasons.append(
                    "required certificate %s is HONEST_NEGATIVE; "
                    "counter-example: %s" % (lbl, c.get("first_mismatch")
                                             or c.get("first_failure")))
        results.append({
            "law": claim.get("law"),
            "ok": ok,
            "status": "BELIEVED FORMALLY" if ok else "REJECTED",
            "requires": claim.get("requires", []),
            "pass_evidence": evidence,
            "rejection_reasons": reasons,
        })
    n_req = sum(len(c.get("requires", [])) for c in claims)
    accepted = all(r["ok"] for r in results)
    return {
        "verdict": "ACCEPTED" if accepted else "REJECTED (see records)",
        "accepted": accepted,
        "n_claims": len(claims),
        "n_required_certs": n_req,
        "n_negative_claims": sum(1 for r in results if not r["ok"]),
        "results": results,
    }


def write_verdict(claims, certs, path=_VERDICT):
    verdict = supervise_build(claims, certs)
    verdict["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S UTC",
                                         time.gmtime())
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(verdict, fh, indent=1, sort_keys=True)
    return path


def demo_claims():
    return [
        {"law": "L1 free streaming (rule 29, sector gap>=2)",
         "requires": ["L1_free_streaming_29"]},
        {"law": "29-traffic law as a law of rule 44 (must reject)",
         "requires": ["HONEST_NEGATIVE_29law_on_44"]},
        {"law": "rule 29 ring attractor = 2*L_N - 2*(even) (must accept)",
         "requires": ["L13_ring_attractor_29_71"]},
        {"law": "rule 29 ring attractor = 2*L_N (must reject, even N)",
         "requires": ["L13_bad_even_omitted"]},
        {"law": "a law we never certified (must reject)",
         "requires": ["L999_never_certified"]},
        {"law": "melt window exact on any single cluster (must accept)",
         "requires": ["L2_melt_single_cluster_29"]},
        {"law": "commons reserve conservation, gate 6 (must accept)",
         "requires": ["L14_gate6_conservation"]},
        {"law": "candidate: credit-sum-only invariant (must reject)",
         "requires": ["L14_bad_credit_sum_invariant"]},
    ]