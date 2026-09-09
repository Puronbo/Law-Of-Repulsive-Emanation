"""certificate_vacuity_audit: a mutation battery over the registered
certificates.

The certificate-contract audit (round 43) catches the inversion class
-- a predicate that encodes the claim's negation or flips the status.
It does NOT catch the dual defect: a predicate so insensitive to its
data that ANY data would produce the same certificate (a vacuity
install -- literally `lambda: True`, or a threshold so loose that the
law can never fail on measured data).  This audit runs every
registered module's certificates over a battery of data mutants:

    zero       every float -> 0.0            (ablate the law's domain)
    tiny       every float -> 1e-5           (kill the scale)
    *_t*       per-module targeted mutants   (break / witness each law)

and requires, for every certificate:

    pass_defeasible   every PASS certificate has a mutant under which
                      its predicate flips to NOT asserted -- no PASS
                      law is unbreechable by construction;
    hn_witnessed      every HONEST_NEGATIVE certificate has a mutant
                      under which its predicate flips to asserted --
                      no HN statement is a literal `lambda: False`;

plus the battery itself must be live (every mutant flips at least one
certificate of its module) and the domain must be stable (every
mutant preserves the data's shape: the same labels come back from the
same certificate function without error).

The mutators transform the module's measured in-memory table; the
certificate functions re-run over the mutated table only (no re-
propagation), so the battery is cheap and deterministic.

Certificates (per registered module, tags as in the contract audit):

    L_vc_<tag>_pass_defeasible   every PASS cert of the module flips
                                  to False under some mutant.
    L_vc_<tag>_hn_witnessed      every HONEST_NEGATIVE cert flips to
                                  True under some mutant.
    L_vc_<tag>_battery_live      every mutant of the module flips at
                                  least one certificate.

Global certificates:

    L_vc_contract_aligned        every live registered status equals
                                  the contract audit's independent
                                  expectation for that label.
    L_vc_all_pass_defeasible     aggregating across the registry.
    L_vc_all_hn_witnessed        aggregating across the registry.
    L_vc_all_battery_live        aggregating across the registry.
    L_vc_domains_stable          every mutant keeps the certificate
                                  arity and label set intact.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_mi_retention_mechanism_audit import (  # noqa: E402
    retention_certificates,
    retention_table,
)
from soliton_eca.soliton_mi_closure_chain_audit import (  # noqa: E402
    closure_certificates,
    closure_chains,
)
from soliton_eca.soliton_mi_phase_mechanism_audit import (  # noqa: E402
    mechanism_certificates,
    mechanism_data,
)
from soliton_eca.soliton_collision_damage_probe_audit import (  # noqa: E402
    _DISTANCES,
    damage_probe_certificates,
    probe_data,
)
from soliton_eca.soliton_extent_spectrum_probe_audit import (  # noqa: E402
    _AFFINE_F32_FLOOR,
    _ERS,
    _KS as _EXT_KS,
    extent_probe_certificates,
    extent_probe_table,
)
from soliton_eca.soliton_universe_transducer_audit import (  # noqa: E402
    _AFFINE,
    _KS as _UNI_KS,
    universe_certificates,
    universe_table,
)
from soliton_eca.certificate_contract_audit import (  # noqa: E402
    _EXPECTED as _CONTRACT_EXPECTED,
)

_DMG_DISTANCES = _DISTANCES
_DMG_TRIPLE = {36, 219, 251}
_EXT_TRIPLE = _ERS
_UNI_TRANSP = {204, 51}


def _walk(x: Any, fn: Callable[[float], float]) -> Any:
    if isinstance(x, dict):
        return {k: _walk(v, fn) for k, v in x.items()}
    if isinstance(x, list):
        return [_walk(v, fn) for v in x]
    if isinstance(x, float):
        return fn(x)
    return x


def _deep(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: _deep(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_deep(v) for v in x]
    return x


def generic_mutators(data: Any) -> dict[str, Any]:
    return {
        "zero": _walk(data, lambda f: 0.0),
        "tiny": _walk(data, lambda f: 1e-5),
    }


def retention_mutators(t: dict) -> dict[str, dict]:
    out: dict[str, dict] = {"flat_p0_zero": _deep(t),
                            "flat_p0_one": _deep(t)}
    for row in out["flat_p0_zero"].values():
        for c in row.values():
            if c is not None:
                c["p0"] = 0.0
    for row in out["flat_p0_one"].values():
        for c in row.values():
            if c is not None:
                c["p0"] = 1.0
    delta_min_winner = _deep(t)
    for row in delta_min_winner.values():
        for c in row.values():
            if c is not None:
                c["delta"] = 1.0 - c["p0"]
    rel1_p0 = _deep(t)
    for row in rel1_p0.values():
        for c in row.values():
            if c is not None:
                c["rel1"] = c["p0"]
    mono = _deep(t)
    for (om, eps), row in mono.items():
        if om == 1.0:
            for c in row.values():
                if c is not None:
                    c["p0"] = 0.2 + 0.1 * {0.20: 0, 0.30: 1,
                                          0.45: 2}[eps]
    out["delta_min_winner"] = delta_min_winner
    out["rel1_eq_p0"] = rel1_p0
    out["mono_omega1"] = mono
    return out


def closure_mutators(t: dict) -> dict[str, dict]:
    tight = _deep(t)
    for phases in tight.values():
        for ch in phases.values():
            if ch:
                seed = ch[0]["delta"]
                for c in ch:
                    c["delta"] = seed
    flat = _deep(t)
    for phases in flat.values():
        for ch in phases.values():
            for c in ch:
                c["delta"] = 0.0
    maxmap = _deep(t)
    for phases in maxmap.values():
        for ch in phases.values():
            if ch:
                mm = max(c["p0"] for c in ch)
                for c in ch:
                    c["delta"] = mm
    return {"tight": tight, "flat_delta": flat,
            "delta_eq_chainmax": maxmap}


def phase_mutators(data: dict) -> dict[str, dict]:
    zero = _deep(data)
    for ch in zero.values():
        for c in ch:
            c["rel1"] = 0.0
    boost6 = _deep(data)
    for p, ch in boost6.items():
        for c in ch:
            c["p0"] = 0.01
    for c in boost6.get("p6", []):
        c["p0"] = 0.02
    cosmono = _deep(data)
    seconds = [(p, ch[1]) for p, ch in cosmono.items() if len(ch) > 1]
    secs = sorted(seconds, key=lambda kv: math.cos(kv[1]["rel1"]))
    for rank, (_, cre) in enumerate(secs):
        cre["p0"] = 0.001 + 0.001 * rank
    return {"zero_rel1": zero, "boost_p6": boost6,
            "cos_mono": cosmono}


def damage_mutators(dat: dict) -> dict[str, dict]:
    def reap_f1(d):
        return {r: list(v) for r, v in d.items()}

    f1b = reap_f1(dat["f1"])
    f2b = {r: {d: list(v) for d, v in dd.items()}
           for r, dd in dat["f2"].items()}

    detach = {"f1": _deep(f1b), "f2": _deep(f2b)}
    detach["f2"][204][4][0] += 0.1

    unwipe = {"f1": _deep(f1b), "f2": _deep(f2b)}
    for d in _DMG_DISTANCES:
        for p in range(len(unwipe["f2"][36][d])):
            unwipe["f2"][36][d][p] = 1.0

    triple = {"f1": _deep(f1b), "f2": _deep(f2b)}
    for r, dd in triple["f2"].items():
        for d, vals in dd.items():
            for p in range(len(vals)):
                vals[p] = 0.0 if r in _DMG_TRIPLE else 2.0

    satbreak = {"f1": _deep(f1b), "f2": _deep(f2b)}
    for p in range(len(satbreak["f2"][147][4])):
        satbreak["f2"][147][4][p] = 2 * satbreak["f1"][147][p] + 0.5

    satfull = {"f1": _deep(f1b), "f2": _deep(f2b)}
    for p in range(len(satfull["f2"][147][4])):
        satfull["f2"][147][4][p] = 2 * satfull["f1"][147][p] - 0.5

    farfit = {"f1": _deep(f1b), "f2": _deep(f2b)}
    for r in farfit["f2"]:
        for p in range(len(farfit["f2"][r][256])):
            farfit["f2"][r][256][p] = 2 * farfit["f1"][r][p]

    synfit = {"f1": _deep(f1b), "f2": _deep(f2b)}
    for r in synfit["f2"]:
        for d, vals in synfit["f2"][r].items():
            for p in range(len(vals)):
                vals[p] = 2 * synfit["f1"][r][p]

    return {"detach_break": detach, "unwipe_36": unwipe,
            "wipe_triple": triple, "sat_break_147": satbreak,
            "sat_full_147": satfull, "far_fit": farfit,
            "synergy_fit": synfit}


def extent_mutators(acc: dict) -> dict[str, dict]:
    transbreak = _deep(acc)
    transbreak[204][32][4] = 0.99

    renegade = _deep(acc)
    for k in _EXT_KS:
        renegade[147][k][3] = 0.0

    leak = _deep(acc)
    leak[251][1][7] = 0.01

    triple = _deep(acc)
    for r in triple:
        for k in _EXT_KS:
            for p in range(len(triple[r][k])):
                triple[r][k][p] = 0.0 if r in _EXT_TRIPLE else 1.0

    satbreak = _deep(acc)
    satbreak[147][32][4] = _AFFINE_F32_FLOOR + 0.01

    return {"trans_break": transbreak, "renegade_60": renegade,
            "sink_leak": leak, "triple_sets": triple,
            "sat_break_147": satbreak}


def universe_mutators(t: dict) -> dict[str, dict]:
    boost = _deep(t)
    boost[147][32] = _AFFINE_F32_FLOOR + 0.01

    fam = _deep(t)
    fam[147][32] = 0.2

    strong = _deep(t)
    strong[147][32] = 5.0

    trans = _deep(t)
    for r in trans:
        for k in _UNI_KS:
            trans[r][k] = k / 512.0 if r in _UNI_TRANSP else k / 512.0 + 1e-6

    return {"boost_147": boost, "family_boost_147": fam,
            "strong_147": strong, "trans_only": trans}


_REGISTRY = [
    ("mi_retention_mechanism", retention_table,
     retention_certificates, retention_mutators),
    ("mi_closure_chain", closure_chains,
     closure_certificates, closure_mutators),
    ("mi_phase_mechanism", mechanism_data,
     mechanism_certificates, phase_mutators),
    ("collision_damage_probe", probe_data,
     damage_probe_certificates, damage_mutators),
    ("extent_spectrum_probe", extent_probe_table,
     extent_probe_certificates, extent_mutators),
    ("universe_transducer", universe_table,
     universe_certificates, universe_mutators),
]


def _certify(label: str, meta: dict[str, object],
             pred: Callable[[], bool]) -> dict[str, object]:
    asserted = bool(pred())
    n_ok = 1 if asserted else 0
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "status": "PASS" if asserted else "HONEST_NEGATIVE",
        "asserted": asserted,
        "negated": not asserted,
        "n_ok": n_ok,
        "n_fail": 0 if n_ok else 1,
        "first_failure": None if n_ok else {"datum": "predicate Failed"},
    }


def vacuity_certificates() -> tuple[list[dict[str, object]],
                                    dict[str, object]]:
    certs: list[dict[str, object]] = []
    stats: dict[str, object] = {}
    liveness: list[bool] = []
    domains: list[bool] = []
    all_pass_defeasible: list[bool] = []
    all_hn_witnessed: list[bool] = []

    aligned = True
    for tag, data_fn, certs_fn, mut_fn in _REGISTRY:
        data = data_fn()
        base, _ = certs_fn(_deep(data))
        base_status = {c["label"]: c["status"] for c in base}
        for lab, st in base_status.items():
            aligned = aligned and _CONTRACT_EXPECTED.get(lab) == st
        flips: dict[str, list[str]] = {c["label"]: []
                                       for c in base}
        live: list[bool] = []
        mut_keys: list[str] = []
        for name, mut in list(generic_mutators(data).items()) \
                + list(mut_fn(data).items()):
            mut_keys.append(name)
            try:
                mc, _ = certs_fn(mut)
            except Exception:
                domains.append(False)
                continue
            domains.append(True)
            labels = {c["label"] for c in mc}
            domains.append(labels == set(base_status))
            any_flip = False
            for c in mc:
                if c["label"] not in flips:
                    flips[c["label"]] = []
                if c["asserted"] != dict(
                        (cc["label"], cc["asserted"])
                        for cc in base)[c["label"]]:
                    flips[c["label"]].append(name)
                    any_flip = True
            live.append(any_flip)
        liveness.extend(live)

        pass_labs = [lab for lab, st in base_status.items()
                     if st == "PASS"]
        hn_labs = [lab for lab, st in base_status.items()
                   if st == "HONEST_NEGATIVE"]
        pass_ok = all(flips[lab] for lab in pass_labs)
        hn_ok = all(flips[lab] for lab in hn_labs)
        live_ok = all(live)
        all_pass_defeasible.append(pass_ok)
        all_hn_witnessed.append(hn_ok)

        certs.append(_certify(
            f"L_vc_{tag}_pass_defeasible",
            {"mode": f"{tag}: every PASS certificate flips to "
                     "NOT asserted under some mutant of its battery",
             "mutants": mut_keys,
             "pass_labels": pass_labs},
            lambda ok=pass_ok: ok))
        certs.append(_certify(
            f"L_vc_{tag}_hn_witnessed",
            {"mode": f"{tag}: every HONEST_NEGATIVE certificate flips "
                     "to asserted under some mutant of its battery",
             "hn_labels": hn_labs},
            lambda ok=hn_ok: ok))
        certs.append(_certify(
            f"L_vc_{tag}_battery_live",
            {"mode": f"{tag}: every mutant flips at least one "
                     "certificate"},
            lambda ok=live_ok: ok))
        stats[tag] = {
            "n_certs": len(base_status),
            "pass": len(pass_labs),
            "hn": len(hn_labs),
            "mutants": mut_keys,
            "flips": flips,
        }

    certs.append(_certify(
        "L_vc_contract_aligned",
        {"law": "every live registered certificate's status equals the "
                "contract audit's independently declared expectation "
                "for that label",
         "checked": sum(len(m["n_certs"]) if isinstance(m["n_certs"], list)
                        else m["n_certs"] for m in stats.values())},
        lambda ok=aligned: ok))
    certs.append(_certify(
        "L_vc_all_pass_defeasible",
        {"law": "in every registered module every PASS certificate is "
                "defeasible (flips to False on some mutant)"},
        lambda ok=all(all_pass_defeasible): ok))
    certs.append(_certify(
        "L_vc_all_hn_witnessed",
        {"law": "in every registered module every HONEST_NEGATIVE "
                "certificate has a witness mutant (flips to True)"},
        lambda ok=all(all_hn_witnessed): ok))
    certs.append(_certify(
        "L_vc_all_battery_live",
        {"law": "every mutant of the whole battery flips at least one "
                "certificate somewhere"},
        lambda ok=all(liveness): ok))
    certs.append(_certify(
        "L_vc_domains_stable",
        {"law": "every mutant preserves the certificate arity and label "
                "set of its module (the mutation battery is in-domain)"},
        lambda ok=all(domains): ok))
    return certs, stats


if __name__ == "__main__":
    certs, stats = vacuity_certificates()
    for c in certs:
        print("  %-42s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    for tag, m in stats.items():
        print(" ", tag, "certs", m["n_certs"],
              "pass", m["pass"], "hn", m["hn"],
              "mutants", len(m["mutants"]))