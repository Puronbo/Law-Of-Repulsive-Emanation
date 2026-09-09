"""validate_certificate_contract_audit: independent re-derivation.

Does NOT trust contract_checks(): it recomputes the four modules'
measured data from their exported table functions, re-evaluates EVERY
certificate predicate against a freshly declared expectation list
(duplicated here, not imported), and re-pins the load-bearing number
facts.  The expectation list repeats the corpus-fact oracle
independently so a drift in EITHER the audit's _EXPECTED or a
module's predicate cannot self-certify.

Recomputed assertions:

  - all sixteen contract certificates are PASS;
  - every module certificate's live status equals this file's
    independently redeclared expectation (inversion-class detector,
    second independent copy);
  - pinned data facts regenerate identically:
      universe: strongest = 105 at 0.3125, family F(32) < 0.125;
      retention: best phases p0 at (1.0, 0.30), p2 at (1.0, 0.45);
      closure:  worst crest spread > 1.0 rad;
      extent probe: 251 is an absolute sink, eraser sets are family
      subsets in every placement.
"""
import sys
from pathlib import Path

import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

from soliton_eca.soliton_mi_retention_mechanism_audit import (  # noqa: E402
    _best_phase,
    retention_certificates,
    retention_table,
)
from soliton_eca.soliton_mi_closure_chain_audit import (  # noqa: E402
    closure_certificates,
    closure_chains,
)
from soliton_eca.soliton_mi_phase_mechanism_audit import (  # noqa: E402
    _wrap_pi,
    mechanism_certificates,
    mechanism_data,
)
from soliton_eca.soliton_collision_damage_probe_audit import (  # noqa: E402
    damage_probe_certificates,
    probe_data,
)
from soliton_eca.soliton_extent_spectrum_probe_audit import (  # noqa: E402
    extent_probe_certificates,
    extent_probe_table,
)
from soliton_eca.soliton_universe_transducer_audit import (  # noqa: E402
    universe_certificates,
    universe_table,
)
from soliton_eca.certificate_contract_audit import (  # noqa: E402
    contract_certificates,
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

flat = contract_certificates()
assert len(flat) == 24
for c in flat:
    assert c["status"] == "PASS", c["label"]

kas = {1, 16, 32}
n_module_certs = 0
for (data, certs_fn) in [
    (retention_table(), retention_certificates),
    (closure_chains(), closure_certificates),
    (mechanism_data(), mechanism_certificates),
    (probe_data(), damage_probe_certificates),
    (extent_probe_table(), extent_probe_certificates),
    (universe_table(), universe_certificates),
]:
    certs = certs_fn(data)[0]
    n_module_certs += len(certs)
    for c in certs:
        assert c["label"] in _EXPECTED
        assert c["status"] == _EXPECTED[c["label"]], (
            c["label"], c["status"], _EXPECTED[c["label"]])
        assert ("asserted" in c and "negated" in c and
                c["asserted"] != c["negated"])
assert n_module_certs == 27

t = universe_table()
assert max(range(256), key=lambda r: t[r][32]) == 105
assert abs(t[105][32] - 0.3125) < 1e-4
assert max(t[r][32] for r in RULES) < 0.125

rt = retention_table()
assert _best_phase(rt[(1.0, 0.30)]) == "p0"
assert _best_phase(rt[(1.0, 0.45)]) == "p2"

ct = closure_chains()
worst = 0.0
for (om, eps), phases in ct.items():
    for p in range(8):
        ch = phases[f"p{p}"]
        if len(ch) >= 1:
            ds = [c["delta"] for c in ch]
            m = sum(ds) / len(ds)
            worst = max(worst, max(abs(_wrap_pi(dv - m)) for dv in ds))
assert worst > 1.0

et = extent_probe_table()
ers = {36, 219, 251}
for p in range(8):
    pset = {r for r in et if all(et[r][k][p] <= 0.005 for k in kas)}
    assert pset <= ers, (p, pset)
for k in kas:
    for p in range(8):
        assert et[251][k][p] == 0.0

md = mechanism_data()
assert max(abs(_wrap_pi(c["rel1"] - 2 * p * np.pi / 8))
           for p in range(8) for c in md[f"p{p}"]) <= 0.30
cm = {k: max(c["p0"] for c in chain) for k, chain in md.items()}
assert cm["p4"] == max(cm.values())

pd = probe_data()
f1 = pd["f1"]
f2 = pd["f2"]
from soliton_eca.soliton_collision_damage_probe_audit import (  # noqa: E402
    RULES as _RULES,
    _DISTANCES,
    _PROBES,
    _SAT_LEVEL,
    _WIPE_LEVEL,
)
ws = [{r for r in _RULES if max(f2[r][d][p] for d in _DISTANCES)
       <= _WIPE_LEVEL} for p in range(_PROBES)]
assert set.intersection(*ws) == {36, 251}
assert all(36 in s and 251 in s for s in ws)
sat_p = [f2[147][4][p] - 2 * f1[147][p] for p in range(_PROBES)]
assert sum(v <= _SAT_LEVEL for v in sat_p) >= _PROBES - 1
assert sat_p[3] > 0.0

print("certificate contract audit validation passed")