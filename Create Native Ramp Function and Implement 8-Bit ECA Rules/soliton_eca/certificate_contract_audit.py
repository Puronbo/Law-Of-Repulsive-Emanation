"""certificate_contract_audit: a meta-audit over the certificates.

The certificate culture failed six times this session in ONE way:
the predicate encoded the claim's NEGATION (or a variable named "ok"
meant "the refutation holds"), so a false claim was certified PASS.
Each failure was caught by hand, by re-reading prose.  This audit
mechanizes that guardrail: it pulls the measured data of every audit
module ONCE, recomputes the certificates, and checks the certificate
CONTRACT against expectations declared independently of the
predicates (the expectations are the corpus's documented facts; the
predicates are code).

Contract checks, for every certificate in the registry:

    L_cc_expected_polarity  the certificate's live status equals the
                            declared expectation for that label --
                            the mechanical inversion-class detector;
    L_cc_status_sound       status PASS <=> the predicate asserted,
                            HONEST_NEGATIVE <=> it negated;
    L_cc_polarity_complete  every certificate carries the asserted /
                            negated contract fields;
    L_cc_data_pinned        each module regenerated the same pinned
                            facts (strongest transducer 105 at
                            0.3125; family F(32) < 0.125; the
                            10-rule isometry class; closure worst
                            crest spread > 1.0; retention best phase
                            at (1.0, 0.30) = p0).

The registry builds the expectations FROM THE DOCUMENTED FACTS -- a
separate oracle from the predicate code -- so a future edit that
inverts a predicate, vacuity-installs a constant, or falsifies the
status is caught here before it can enter the register.

Expected statuses (from the corpus, not from the code):

    mi_retention_mechanism:   L_ret_migration PASS,
                              L_ret_band_amplitude PASS,
                              L_ret_closure_resonance HN,
                              L_ret_rel1_insufficient HN,
                              L_ret_amplitude_bounces HN,
    mi_closure_chain:         L_cl_chain_frozen HN,
                              L_cl_phase_dependent PASS,
                              L_cl_closure_label HN,
    extent_spectrum_probe:    L_es_transparent_placewise PASS,
                              L_es_erasers_family_exhaust PASS,
                              L_es_eraser_251_absolute PASS,
                              L_es_erasers_triple_placewise HN,
                              L_es_saturation_placewise PASS,
    universe_transducer:      L_univ_transducer_set PASS,
                              L_univ_family_tail PASS,
                              L_univ_strongest_affine PASS,
                              L_univ_transparent_only HN.
"""
from __future__ import annotations

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
from soliton_eca.soliton_extent_spectrum_probe_audit import (  # noqa: E402
    extent_probe_certificates,
    extent_probe_table,
)
from soliton_eca.soliton_eca import RULES  # noqa: E402
from soliton_eca.soliton_universe_transducer_audit import (  # noqa: E402
    universe_certificates,
    universe_table,
)

from soliton_eca.soliton_mi_phase_mechanism_audit import (  # noqa: E402
    mechanism_certificates,
    mechanism_data,
)
from soliton_eca.soliton_collision_damage_probe_audit import (  # noqa: E402
    damage_probe_certificates,
    probe_data,
)

_EXPECTED = {
    "L_ret_migration": "PASS",
    "L_ret_band_amplitude": "PASS",
    "L_ret_closure_resonance": "HONEST_NEGATIVE",
    "L_ret_rel1_insufficient": "HONEST_NEGATIVE",
    "L_ret_amplitude_bounces": "HONEST_NEGATIVE",
    "L_cl_chain_frozen": "HONEST_NEGATIVE",
    "L_cl_phase_dependent": "PASS",
    "L_cl_closure_label": "HONEST_NEGATIVE",
    "L_es_transparent_placewise": "PASS",
    "L_es_erasers_family_exhaust": "PASS",
    "L_es_eraser_251_absolute": "PASS",
    "L_es_erasers_triple_placewise": "HONEST_NEGATIVE",
    "L_es_saturation_placewise": "PASS",
    "L_univ_transducer_set": "PASS",
    "L_univ_family_tail": "PASS",
    "L_univ_strongest_affine": "PASS",
    "L_univ_transparent_only": "HONEST_NEGATIVE",
    "L_ph_rel1_conserved": "PASS",
    "L_ph_antiphase_peak": "PASS",
    "L_ph_rel1_mechanism": "HONEST_NEGATIVE",
    "L_cdp_detach_exact": "PASS",
    "L_cdp_wipe_core": "PASS",
    "L_cdp_saturation_signature": "PASS",
    "L_cdp_wipe_set_exact": "HONEST_NEGATIVE",
    "L_cdp_saturation_universal": "HONEST_NEGATIVE",
    "L_cdp_far_antipode": "HONEST_NEGATIVE",
    "L_cdp_synergy_none": "HONEST_NEGATIVE",
}

_REGISTRY: list[tuple[str, Callable[[], Any], Callable[[Any], Any]]] = [
    ("mi_retention_mechanism", retention_table, retention_certificates),
    ("mi_closure_chain", closure_chains, closure_certificates),
    ("mi_phase_mechanism", mechanism_data, mechanism_certificates),
    ("collision_damage_probe", probe_data, damage_probe_certificates),
    ("extent_spectrum_probe", extent_probe_table, extent_probe_certificates),
    ("universe_transducer", universe_table, universe_certificates),
]


def _certify(label: str, meta: dict[str, object],
             pred: Callable[[], bool]) -> dict[str, object]:
    asserted = bool(pred())
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "status": "PASS" if asserted else "HONEST_NEGATIVE",
        "asserted": asserted,
        "negated": not asserted,
        "n_ok": 1 if asserted else 0,
        "n_fail": 0 if asserted else 1,
        "first_failure": None if asserted else {"datum": "the predicate Failed"},
    }


def contract_checks() -> dict[str, list[dict[str, object]]]:
    checks: dict[str, list[dict[str, object]]] = {}
    for tag, data_fn, certs_fn in _REGISTRY:
        data = data_fn()
        certs = certs_fn(data)[0]
        polarity_ok = all(c["status"] == _EXPECTED[c["label"]]
                          for c in certs)
        sound_ok = all(
            (c["asserted"] and c["status"] == "PASS")
            or (not c["asserted"] and c["status"] == "HONEST_NEGATIVE")
            for c in certs)
        complete_ok = all("asserted" in c and "negated" in c
                          for c in certs)

        pinned: list[bool] = []
        if tag == "universe_transducer":
            t = data
            pinned.append(max(range(256), key=lambda r: t[r][32]) == 105)
            pinned.append(abs(t[105][32] - 0.3125) < 1e-4)
            pinned.append(max(t[r][32] for r in RULES) < 0.125)
            pins = 3
        elif tag == "mi_closure_chain":
            tbl = data
            spreads = []
            for (om, eps), phases in tbl.items():
                for p in range(8):
                    ch = phases[f"p{p}"]
                    if len(ch) >= 1:
                        ds = [c["delta"] for c in ch]
                        m = float(sum(ds) / len(ds))
                        from soliton_eca.soliton_mi_phase_mechanism_audit import _wrap_pi  # noqa: E402
                        spends = max(abs(_wrap_pi(dv - m)) for dv in ds)
                        spreads.append(spends)
            pinned.append(max(spreads) > 1.0)
            pins = 1
        elif tag == "extent_spectrum_probe":
            acc = data
            ers = {36, 219, 251}
            sub_ok = all(
                {r for r in acc if all(acc[r][k][p] <= 0.005
                                       for k in (1, 16, 32))}
                <= ers for p in range(8))
            pinned.append(all(acc[251][k][p] == 0.0
                              for k in (1, 16, 32) for p in range(8)))
            pinned.append(sub_ok)
            pins = 2
        elif tag == "mi_retention_mechanism":
            tbl = data
            from soliton_eca.soliton_mi_retention_mechanism_audit import (  # noqa: E402
                _best_phase,
            )
            pinned.append(_best_phase(tbl[(1.0, 0.30)]) == "p0")
            pinned.append(_best_phase(tbl[(1.0, 0.45)]) == "p2")
            pins = 2
        elif tag == "mi_phase_mechanism":
            import numpy as np  # noqa: F401
            from soliton_eca.soliton_mi_phase_mechanism_audit import (  # noqa: E402
                _wrap_pi,
            )
            dat = data
            drift = max(
                abs(_wrap_pi(c["rel1"] - 2 * p * np.pi / 8))
                for p in range(8) for c in dat[f"p{p}"])
            pinned.append(drift <= 0.30)
            chain_max = {k: max(c["p0"] for c in chain)
                         for k, chain in dat.items()}
            pinned.append(chain_max["p4"] == max(chain_max.values()))
            pins = 2
        elif tag == "collision_damage_probe":
            from soliton_eca.soliton_collision_damage_probe_audit import (  # noqa: E402
                _DISTANCES,
                _PROBES,
                _SAT_LEVEL,
                _WIPE_LEVEL,
            )
            dat = data
            f1: dict[int, list[float]] = dat["f1"]
            f2: dict[int, dict[int, list[float]]] = dat["f2"]

            def max_d(p: int, r: int) -> float:
                return max(f2[r][d][p] for d in _DISTANCES)

            ws = [{r for r in RULES if max_d(p, r) <= _WIPE_LEVEL}
                  for p in range(_PROBES)]
            pinned.append(set.intersection(*ws) == {36, 251})
            pinned.append(all(36 in s and 251 in s for s in ws))
            sat_p = [f2[147][4][p] - 2 * f1[147][p]
                     for p in range(_PROBES)]
            pinned.append(sum(v <= _SAT_LEVEL for v in sat_p)
                          >= _PROBES - 1)
            pinned.append(sat_p[3] > 0.0)
            pins = 4

        data_ok = bool(pinned) and all(pinned)
        checks[tag] = [
            _certify(
                "L_cc_expected_polarity",
                {"domain": f"certificates of {tag}",
                 "law": "every certificate's live status equals the "
                        "independently-declared expectation for its "
                        "label -- a future predicate inversion, "
                        "falsified claim, or status edit is caught "
                        "here",
                 "expected": {
                     c["label"]: _EXPECTED[c["label"]] for c in certs}},
                lambda tag=tag, certs=certs, polarity_ok=polarity_ok:
                    polarity_ok),
            _certify(
                "L_cc_status_sound",
                {"domain": f"certificates of {tag}",
                 "law": "the status label is a pure function of the "
                        "predicate result: PASS iff asserted, "
                        "HONEST_NEGATIVE iff negated",
                 "checks": len(certs)},
                lambda: sound_ok),
            _certify(
                "L_cc_polarity_complete",
                {"domain": f"certificates of {tag}",
                 "law": "every certificate carries the asserted / "
                        "negated contract fields (the polarization "
                        "contract adopted this round)",
                 "checks": len(certs)},
                lambda: complete_ok),
            _certify(
                "L_cc_data_pinned",
                {"domain": f"regenerated data of {tag}",
                 "law": "the module regenerated the same pinned facts "
                        "(" + ", ".join(
                            [f"{pins} pins"]) + ")",
                 "pins": pins},
                lambda: data_ok),
        ]
    return checks


def contract_certificates() -> list[dict[str, object]]:
    flat = []
    for tag, certs in sorted(contract_checks().items()):
        flat.extend(certs)
    return flat


if __name__ == "__main__":
    flat = contract_certificates()
    for c in flat:
        print("  %-38s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    over_expected = sum(1 for c in flat
                        if c["label"] in _EXPECTED
                        and c["status"] != _EXPECTED[c["label"]])
    print("  certificates checked:", len(flat),
          " expected-polarity violations:", over_expected)