"""certify_repo: CI-gate the law-supervisor over this repository.

Usage:
    python scripts/certify_repo.py            # status summary (exit 0/1)
    python scripts/certify_repo.py --gate     # hard gate for CI
    python scripts/certify_repo.py --regenerate   # rebuild certs + verdict

The gate fails (exit 1) if:
    * the persisted certificate table does not reproduce exactly from the
      current code (drift in a certificate, missing/stale entries), or
    * the T2 discovery self-report no longer reproduces from current code
      (the system may not forget what it failed to know), or
    * any claimed law is not formally believed by the supervisor
      (its named certificate missing or HONEST_NEGATIVE).
These artifacts are machine-readable (data/law_certificates.json,
data/supervision_verdict.json, data/law_discovery_table.json,
data/discovery_verdict.json), so CI, the webapp, and agents query the
same gated truth -- the physics-replaces-the-proof-checker contract.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.emanation import repo_audit as ra
from experiments.emanation import supervisor as sv
from experiments.emanation import law_discovery as ld


def claims():
    """FORMAL claims this repo stands behind (every named certificate must
    be PASS).  Hand-written core laws PLUS the discovery agent's own
    self-deriverd claims -- the gate now vets the whole learning loop:
    every rule the agent certified, and nothing over the rules it
    couldn't (veto).  The supervisor's richer demo_claims() deliberately
    includes rejects; the gate must not."""
    base = [
        {"law": "L1 free streaming (rule 29, gap>=2 sector)",
         "requires": ["L1_free_streaming_29"]},
        {"law": "L1 free streaming (rule 71, gap>=2 sector)",
         "requires": ["L1_free_streaming_71"]},
        {"law": "melt window exact on any single cluster (29)",
         "requires": ["L2_melt_single_cluster_29"]},
        {"law": "melt window exact on any single cluster (71)",
         "requires": ["L2_melt_single_cluster_71"]},
        {"law": "L3 per-cluster union law (merge-free sector)",
         "requires": ["L3_composition_mergerfree_29"]},
        {"law": "ring attractor = 2*L_N - 2*(N even)",
         "requires": ["L13_ring_attractor_29_71"]},
        {"law": "commons reserve conservation (spec gate 6)",
         "requires": ["L14_gate6_conservation"]},
        {"law": "Gregorian roundtrip exactness (400-year cycle)",
         "requires": ["L18_gregorian_roundtrip"]},
        {"law": "Julian roundtrip exactness (4-year cycle)",
         "requires": ["L19_julian_roundtrip"]},
        {"law": "Tzolkin 260-day periodicity",
         "requires": ["L20_tzolkin_periodicity"]},
        {"law": "Gregorian monotonicity (date ordering)",
         "requires": ["L21_gregorian_monotonicity"]},
        {"law": "Day-of-year range consistency",
         "requires": ["L22_day_of_year_consistent"]},
        {"law": "hash-chain verifies when untampered",
         "requires": ["L24_chain_verify_untampered"]},
        {"law": "non-terminal payload tamper (no re-hash) always detected",
         "requires": ["L25_tamper_no_rehash_detected"]},
        {"law": "non-terminal re-hash tamper caught at successor block",
         "requires": ["L26_rehash_tamper_detected"]},
        {"law": "to_disk radial clamp preserves in-disk points exactly",
         "requires": ["L28_to_disk_inside_preserved"]},
        {"law": "to_disk maps out-of-rim points exactly onto the sphere",
         "requires": ["L29_to_disk_rim_exact"]},
        {"law": "flow_over dedups edges and ignores self/out-of-range links",
         "requires": ["L30_flow_over_dedup_and_self_loop_invariant"]},
    ]
    discovered, _ = ld.discovery_claims()
    return base + discovered


def discovery_veto():
    _, veto = ld.discovery_claims()
    return veto


def gate():
    ok, drift = ra.fresh_table_matches()
    if not ok:
        return False, "certificate table drift:\n  " + "\n  ".join(drift)
    ok, why = ld.fresh()
    if not ok:
        return False, "discovery self-report drift: %s" % why
    certs = ra.full_table()
    verdict = sv.supervise_build(claims(), certs, veto=discovery_veto())
    rejected = [r for r in verdict["results"] if not r["ok"]]
    if verdict["accepted"] is False:
        lines = ["%d claims not believed:" % len(rejected)]
        for r in rejected:
            lines.append("  %-46s %s" % (r["law"], "; ".join(
                r["rejection_reasons"])))
        return False, "\n".join(lines)
    return True, "all %d claims believed; table fresh (%d certificates)" % (
        verdict["n_claims"], len(certs))


def summary():
    certs = ra.full_table()
    from experiments.emanation import law_checker as lc
    kinds = {}
    for c in certs:
        key = (c["status"], c.get("kind", "trajectory"))
        kinds[key] = kinds.get(key, 0) + 1
    print("certificate table: %d entries" % len(certs))
    for (status, kind), n in sorted(kinds.items()):
        print("  %-16s %-10s %d" % (status, kind, n))
    ok, drift = ra.fresh_table_matches()
    print("table fresh: %s" % (ok and "yes" or "DRIFT: %s" % drift))
    ok2, why2 = ld.fresh()
    print("discovery fresh: %s" % (ok2 and "yes" or "STALE: %s" % why2))
    verdict = sv.supervise_build(claims(), certs, veto=discovery_veto())
    print("supervisor: accepted=%s (%d claims, %d negative)" % (
        verdict["accepted"], verdict["n_claims"],
        verdict["n_negative_claims"]))
    return verdict["accepted"] and ok and ok2


def regenerate():
    ra.write_full_table()
    sv.write_verdict(claims(), ra.full_table())
    rep = ld.discover()
    ld.save_discovery(rep)
    print("regenerated certificates + verdict + discovery self-report")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gate", action="store_true",
                    help="hard CI gate (exit 0/1)")
    ap.add_argument("--regenerate", action="store_true",
                    help="rebuild certs and verdict from current code")
    ap.add_argument("--claims", action="store_true",
                    help="list the formal claims this repo gates on")
    args = ap.parse_args(argv)
    if args.regenerate:
        regenerate()
    if args.claims:
        for c in claims():
            print("CLAIM  %-44s  requires %s" % (c["law"], c["requires"]))
    if args.gate:
        ok, msg = gate()
        print(msg)
        return 0 if ok else 1
    ok = summary()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())