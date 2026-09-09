"""validate_certificate_vacuity_audit: independent re-derivation of the
mutation battery.

The audit's flip contracts are re-derived here with a separate copy of
the mutation battery (rebuilt from the raw module constants, not
borrowed from the audit's mutator code) and independently re-scored
certificate statuses.  The module certificates under test are
recomputed by the module's own functions over each mutation, and every
vacuity certificate's status is re-derivable from this file's own
evaluation.
"""
from __future__ import annotations

import sys
import math
from pathlib import Path

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
from soliton_eca.certificate_vacuity_audit import (  # noqa: E402
    vacuity_certificates,
)

_TRIPLE = _ERS


def _deep(x):
    if isinstance(x, dict):
        return {k: _deep(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_deep(v) for v in x]
    return x


def _walk(x, fn):
    if isinstance(x, dict):
        return {k: _walk(v, fn) for k, v in x.items()}
    if isinstance(x, list):
        return [_walk(v, fn) for v in x]
    if isinstance(x, float):
        return fn(x)
    return x


def _battery(data_fn, mut_maker):
    data = data_fn()
    batterie = [("zero", _walk(data, lambda f: 0.0)),
                ("tiny", _walk(data, lambda f: 1e-5))]
    for name, make in mut_maker(_deep(data)):
        batterie.append((name, make))
    return data, batterie


def _retention_mut(base):
    out = []
    flat0 = _deep(base)
    for row in flat0.values():
        for c in row.values():
            if c is not None:
                c["p0"] = 0.0
    out.append(("flat_p0_zero", flat0))
    delta = _deep(base)
    for row in delta.values():
        for c in row.values():
            if c is not None:
                c["delta"] = 1.0 - c["p0"]
    out.append(("delta_min_winner", delta))
    rel1 = _deep(base)
    for row in rel1.values():
        for c in row.values():
            if c is not None:
                c["rel1"] = c["p0"]
    out.append(("rel1_eq_p0", rel1))
    mono = _deep(base)
    for (om, eps), row in mono.items():
        if om == 1.0:
            for c in row.values():
                if c is not None:
                    c["p0"] = 0.2 + 0.1 * {0.20: 0, 0.30: 1,
                                           0.45: 2}[eps]
    out.append(("mono_omega1", mono))
    return out


def _closure_mut(base):
    tight = _deep(base)
    for phases in tight.values():
        for ch in phases.values():
            if ch:
                for c in ch:
                    c["delta"] = ch[0]["delta"]
    flat = _deep(base)
    for phases in flat.values():
        for ch in phases.values():
            for c in ch:
                c["delta"] = 0.0
    mm = _deep(base)
    for phases in mm.values():
        for ch in phases.values():
            if ch:
                m = max(c["p0"] for c in ch)
                for c in ch:
                    c["delta"] = m
    return [("tight", tight), ("flat_delta", flat),
            ("delta_eq_chainmax", mm)]


def _phase_mut(base):
    z = _deep(base)
    for ch in z.values():
        for c in ch:
            c["rel1"] = 0.0
    b6 = _deep(base)
    for p, ch in b6.items():
        for c in ch:
            c["p0"] = 0.01
    for c in b6.get("p6", []):
        c["p0"] = 0.02
    cm = _deep(base)
    secs = sorted(((p, ch[1]) for p, ch in cm.items()
                   if len(ch) > 1),
                  key=lambda kv: math.cos(kv[1]["rel1"]))
    for rank, (_, cre) in enumerate(secs):
        cre["p0"] = 0.001 + 0.001 * rank
    return [("zero_rel1", z), ("boost_p6", b6), ("cos_mono", cm)]


def _damage_mut(base):
    f1 = {r: list(v) for r, v in base["f1"].items()}
    f2 = {r: {d: list(v) for d, v in dd.items()}
          for r, dd in base["f2"].items()}
    out = []
    detach = {"f1": _deep(f1), "f2": _deep(f2)}
    detach["f2"][204][4][0] += 0.1
    out.append(("detach_break", detach))
    unwipe = {"f1": _deep(f1), "f2": _deep(f2)}
    for d in _DISTANCES:
        for p in range(8):
            unwipe["f2"][36][d][p] = 1.0
    out.append(("unwipe_36", unwipe))
    triple = {"f1": _deep(f1), "f2": _deep(f2)}
    for r, dd in triple["f2"].items():
        for d, vals in dd.items():
            for p in range(8):
                vals[p] = 0.0 if r in _TRIPLE else 2.0
    out.append(("wipe_triple", triple))
    satb = {"f1": _deep(f1), "f2": _deep(f2)}
    for p in range(8):
        satb["f2"][147][4][p] = 2 * satb["f1"][147][p] + 0.5
    out.append(("sat_break_147", satb))
    satf = {"f1": _deep(f1), "f2": _deep(f2)}
    for p in range(8):
        satf["f2"][147][4][p] = 2 * satf["f1"][147][p] - 0.5
    out.append(("sat_full_147", satf))
    ff = {"f1": _deep(f1), "f2": _deep(f2)}
    for r in ff["f2"]:
        for p in range(8):
            ff["f2"][r][256][p] = 2 * ff["f1"][r][p]
    out.append(("far_fit", ff))
    return out


def _extent_mut(base):
    tb = _deep(base)
    tb[204][32][4] = 0.99
    re = _deep(base)
    for k in _EXT_KS:
        re[147][k][3] = 0.0
    lk = _deep(base)
    lk[251][1][7] = 0.01
    tr = _deep(base)
    for r in tr:
        for k in _EXT_KS:
            for p in range(8):
                tr[r][k][p] = 0.0 if r in _TRIPLE else 1.0
    sb = _deep(base)
    sb[147][32][4] = _AFFINE_F32_FLOOR + 0.01
    return [("trans_break", tb), ("renegade_60", re),
            ("sink_leak", lk), ("triple_sets", tr),
            ("sat_break_147", sb)]


def _universe_mut(base):
    bo = _deep(base)
    bo[147][32] = _AFFINE_F32_FLOOR + 0.01
    f = _deep(base)
    f[147][32] = 0.2
    st = _deep(base)
    st[147][32] = 5.0
    tr = _deep(base)
    for r in tr:
        for k in _UNI_KS:
            tr[r][k] = k / 512.0 if r in {204, 51} else k / 512.0 + 1e-6
    return [("boost_147", bo), ("family_boost_147", f),
            ("strong_147", st), ("trans_only", tr)]


_MODULES = [
    ("mi_retention_mechanism", retention_table,
     retention_certificates, _retention_mut),
    ("mi_closure_chain", closure_chains,
     closure_certificates, _closure_mut),
    ("mi_phase_mechanism", mechanism_data,
     mechanism_certificates, _phase_mut),
    ("collision_damage_probe", probe_data,
     damage_probe_certificates, _damage_mut),
    ("extent_spectrum_probe", extent_probe_table,
     extent_probe_certificates, _extent_mut),
    ("universe_transducer", universe_table,
     universe_certificates, _universe_mut),
]

audit_top, _ = vacuity_certificates()
assert all(c["status"] == "PASS" for c in audit_top)

for tag, data_fn, certs_fn, mut_spec in _MODULES:
    base, battery = _battery(data_fn, mut_spec)
    base_certs, _ = certs_fn(_deep(base))
    base_assert = {c["label"]: c["asserted"] for c in base_certs}
    base_status = {c["label"]: c["status"] for c in base_certs}
    for lab, st in base_status.items():
        assert _CONTRACT_EXPECTED.get(lab) == st, (tag, lab, st)
    flips = {lab: [] for lab in base_assert}
    for name, mut in battery:
        mc, _ = certs_fn(mut)
        assert {c["label"] for c in mc} == set(base_assert), tag
        any_flip = False
        for c in mc:
            if c["asserted"] != base_assert[c["label"]]:
                flips[c["label"]].append(name)
                any_flip = True
        assert any_flip, (tag, name)
    for lab, st in base_status.items():
        assert flips[lab], (tag, lab)
    print("  vacuity", tag, "ok") 

print("certificate vacuity audit validation passed")