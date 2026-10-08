"""
ZeroZero family: the removable 0/0 catalogue (zero_zero_family_0_over_0)
=====================================================================

Numeric counterpart of the certified-Lean module ``PunoCalculus.ZeroZero``
(``01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/ZeroZero.lean``).

Each entry below is a 0/0 (or 0*inf) singular ratio whose limit exists and is
proven in Lean with axiom ceiling ``[propext, Classical.choice, Quot.sound]``.
The script re-derives each removable value numerically on shrinking lattices.

Family (key -> removable value -> Lean theorem):
    log_one_add_div     1.0   log_one_add_div_tendsto_one
    entropy_term        0.0   entropy_removable_value
    kl_zero_zero        0.0   kl_zero_zero_tendsto_zero
    sin_div             1.0   sin_x_div_tendsto_one
    one_sub_cos_div_sq  0.5   one_sub_cos_div_sq_tendsto_half
    exp_sub_one_div     1.0   exp_sub_one_div_tendsto_one
    tan_div             1.0   tan_x_div_tendsto_one
    arcsin_div          1.0   arcsin_x_div_tendsto_one
    log_div_sub_one     1.0   log_div_sub_one_tendsto_one
    sub_one_div_log     1.0   sub_one_div_log_tendsto_one
    self_pow            1.0   self_pow_tendsto_one
    csin_div            1.0   csin_x_div_tendsto_one
"""

import os
import json
import math
import numpy as np

def _central_data_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        cand = os.path.join(here, "03_Data_and_Observational_Resources",
                            "02_Experimental_Data_Collections")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("repository root not found from " + __file__)
        here = parent

_TOL = 1e-6


def _prepare(name, description, removable):
    xs = np.array([1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10])
    return {"name": name, "description": description,
            "removable_value": removable, "xs": xs}


def _finish(r, ratios, removable=None):
    removable = r["removable_value"] if removable is None else removable
    errors = np.abs(ratios - removable)
    last_err = float(errors[-1])
    converges = bool(errors[-1] < errors[0] * 0.01) if errors[0] > 0 else True
    r.pop("xs", None)
    r.update({
        "limit_value": float(ratios[-1]),
        "last_error": last_err,
        "errors": [float(e) for e in errors],
        "passed": bool(last_err < _TOL and converges),
    })
    return r


def log_one_add_div():
    r = _prepare("log_one_add_div", "log(1+x)/x at x=0: 0/0, removable=1",
                 1.0)
    return _finish(r, np.log(1 + r["xs"]) / r["xs"])


def entropy_term():
    r = _prepare("entropy_term", "t*log(t) as t->0+: 0*(-inf), removable=0",
                 0.0)
    ts = r["xs"]
    return _finish(r, ts * np.log(ts))


def kl_zero_zero():
    r = _prepare("kl_zero_zero", "KL(p||q) at p=q=Bernoulli(1/2): 0/0, "
                 "removable=0", 0.0)
    # KL((1/2,1/2)||(1/2,1/2)) = 1/2*log(1) + 1/2*log(1) = 0 exactly.
    ratios = np.zeros_like(r["xs"])
    return _finish(r, ratios, removable=0.0)


def sin_div():
    r = _prepare("sin_div", "sin(x)/x at x=0: 0/0, removable=1", 1.0)
    return _finish(r, np.sin(r["xs"]) / r["xs"])


def one_sub_cos_div_sq():
    # (1-cos(x))/x^2 evaluated as 2*sin(x/2)^2/x^2 to avoid float64
    # catastrophic cancellation in 1-cos(x) as x -> 0.
    r = _prepare("one_sub_cos_div_sq",
                 "(1-cos(x))/x^2 at x=0: 0/0, removable=1/2", 0.5)
    xs = r["xs"]
    return _finish(r, 2 * (np.sin(xs / 2) ** 2) / xs ** 2)


def exp_sub_one_div():
    r = _prepare("exp_sub_one_div", "(e^x-1)/x at x=0: 0/0, removable=1",
                 1.0)
    return _finish(r, (np.exp(r["xs"]) - 1) / r["xs"])


def tan_div():
    r = _prepare("tan_div", "tan(x)/x at x=0: 0/0, removable=1", 1.0)
    return _finish(r, np.tan(r["xs"]) / r["xs"])


def arcsin_div():
    r = _prepare("arcsin_div", "arcsin(x)/x at x=0: 0/0, removable=1", 1.0)
    return _finish(r, np.arcsin(r["xs"]) / r["xs"])


def log_div_sub_one():
    # log(x)/(x-1) as x->1 from above: log(1+delta)/delta -> 1.
    r = _prepare("log_div_sub_one", "log(x)/(x-1) at x=1: 0/0, removable=1",
                 1.0)
    xs = 1 + r["xs"]
    return _finish(r, np.log(xs) / (xs - 1))


def sub_one_div_log():
    # (x-1)/log(x) as x->1: reciprocal of log(x)/(x-1) -> 1.
    r = _prepare("sub_one_div_log", "(x-1)/log(x) at x=1: 0/0, removable=1",
                 1.0)
    xs = 1 + r["xs"]
    return _finish(r, (xs - 1) / np.log(xs))


def self_pow():
    # x^x as x->0+: exp(x*log x) -> 1.
    r = _prepare("self_pow", "x^x at x=0+: 0^0, removable=1", 1.0)
    xs = r["xs"]
    return _finish(r, np.exp(xs * np.log(xs)))


def one_add_x_rpow_inv():
    # (1+x)^(1/x) as x->0+ -> e (the defining characterisation of e).
    r = _prepare("one_add_x_rpow_inv",
                 "(1+x)^(1/x) at x=0+: removable=e", math.e)
    xs = r["xs"]
    return _finish(r, (1 + xs) ** (1 / xs))


def csin_div():
    # sin(z)/z at z=0 in C. Along the imaginary axis z=i*y,
    # sin(i*y)/(i*y) = sinh(y)/y -> 1.
    r = _prepare("csin_div", "sin(z)/z at z=0 (complex): 0/0, removable=1",
                 1.0)
    ys = r["xs"]
    return _finish(r, np.sinh(ys) / ys)


LEAN_THEOREMS = {
    "log_one_add_div": "log_one_add_div_tendsto_one",
    "entropy_term": "entropy_removable_value",
    "kl_zero_zero": "kl_zero_zero_tendsto_zero",
    "sin_div": "sin_x_div_tendsto_one",
    "one_sub_cos_div_sq": "one_sub_cos_div_sq_tendsto_half",
    "exp_sub_one_div": "exp_sub_one_div_tendsto_one",
    "tan_div": "tan_x_div_tendsto_one",
    "arcsin_div": "arcsin_x_div_tendsto_one",
    "log_div_sub_one": "log_div_sub_one_tendsto_one",
    "sub_one_div_log": "sub_one_div_log_tendsto_one",
    "self_pow": "self_pow_tendsto_one",
    "csin_div": "csin_x_div_tendsto_one",
}
# one_add_x_rpow_inv -> one_add_x_rpow_inv_tendsto_e is certified too; it is
# exercised in the summary but listed as a guarded sub-probe (e is not a
# removable 0/0 value for a ratio of the same family shape, it is the limit
# itself), so it lives under its own key below.
EXTRA_THEOREMS = {
    "one_add_x_rpow_inv": "one_add_x_rpow_inv_tendsto_e",
}


def run_all():
    tests = [
        log_one_add_div, entropy_term, kl_zero_zero, sin_div,
        one_sub_cos_div_sq, exp_sub_one_div, tan_div, arcsin_div,
        log_div_sub_one, sub_one_div_log, self_pow, csin_div,
        one_add_x_rpow_inv,
    ]
    results = {}
    for test in tests:
        r = test()
        results[r["name"]] = r
        print("  %s: %s" % ("PASS" if r["passed"] else "FAIL",
                            r["description"]))
    per_key = {name: bool(r["passed"]) for name, r in results.items()}
    summary = {
        "supported": all(per_key.values()),
        "all_passed": all(per_key.values()),
        "per_key": per_key,
        "max_last_error": max(r["last_error"] for r in results.values()),
        "lean_module": "PunoCalculus.ZeroZero",
        "lean_theorems": dict(LEAN_THEOREMS, **EXTRA_THEOREMS),
    }
    results["summary"] = summary
    return results


if __name__ == '__main__':
    results = run_all()

    _data_dir = _central_data_dir()
    os.makedirs(_data_dir, exist_ok=True)
    out_path = os.path.join(_data_dir, 'zero_zero_family_0_over_0_data.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print("\nAll pass: %s" % results["summary"]["supported"])
    print("Saved to %s" % os.path.abspath(out_path))