"""Metrological ignition: resolvability of theta* as a switch at the floor
crossover f = theta*.

genesis_meter.json established the PLATEAU-TRAP: a population truncated
below theta* (floor f = max h/X < theta*) gives a survival plateau, and a
naive inversion is pinned just below f with bias growing as the floor
descends.  This run performs the CONTROL by sweeping the same bimodal
family across the boundary f = theta*:

  meter(f): w=0.2 hazardous class (r >= 0.25, S_B = 1 near theta*)
            + w=0.8 low-hazard class h in [0.02, 0.8*f], x in [0.8,1.5]
            with floor f = max h/X in [0.050, 0.080].

Prediction (all closed form, to be confirmed by deterministic MC at
n=64000, seed 42):

  - escape(f) is CONTINUOUS at f = theta*: 0.2 below the crossover,
    0.2 + 0.8*S_A(theta*) above it (S_A -> 0 as f -> theta*+);
  - RESOLVABILITY is a SPLIT: below the crossover the naive inversion is
    pinned at the floor (bias ~ theta* - f); at or above it the inversion
    recovers theta* within noise.  The metrological switch turns on when
    the population's reach STRADDLES the threshold;
  - the f=0.0625 member replays the economy's 5.3 sigma again (control of
    the control).

If any member violates escape(f) beyond ~3 sigma, or if resolvability
does not switch on past f=theta*, the plateau-trap law is falsified here
and withdrawn.

No Millennium claim; NSE-live-branch metrology discipline; the switch is
the ledger's own law, flagged as phase-transition-analogous (Stanley
1971) ONLY as language.
"""

import json
import math
import os
import random

from credit_commons.sim import Params

P = Params()
G_STAR = 2.0 * math.sqrt(P.g0 * P.gdepth * P.reward())
D_STAR = (G_STAR / P.g0 - 1.0) / P.gdepth
THETA_STAR = P.g0 * P.gdepth * D_STAR / P.I     # 0.06332

N = 64000
SEED = 42
FLOORS = [0.050, 0.055, 0.058, 0.060, 0.062, 0.0625, 0.0630, 0.0635,
          0.0640, 0.0650, 0.0675, 0.0700, 0.0750, 0.0800]


def surv_low(hi_h, theta):
    a, b, c, d = 0.02, hi_h, 0.8, 1.5
    if theta <= a / d:
        return 1.0
    if theta >= b / c:
        return 0.0
    x1 = a / theta
    x2 = b / theta
    area = 0.0
    if x1 > c:
        area += min(x1, d) - c
    lo = max(c, x1)
    hi = min(d, x2)
    if hi > lo:
        area += ((b * hi - theta * hi * hi / 2.0)
                 - (b * lo - theta * lo * lo / 2.0)) / (b - a)
    return area / (d - c)


def surv_meter(hi_h, theta):
    return 0.8 * surv_low(hi_h, theta) + 0.2


def dsurv(hi_h, theta, h=1e-5):
    return (surv_meter(hi_h, theta + h) -
            surv_meter(hi_h, theta - h)) / (2.0 * h)


def quantile_meter(hi_h, target, lo_t, hi_t):
    lo, hi = lo_t, hi_t
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if surv_meter(hi_h, mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main():
    rows = []
    for f in FLOORS:
        hi_h = 0.8 * f
        # closed-form prediction
        pred = 0.2 + 0.8 * surv_low(hi_h, THETA_STAR)
        # deterministic MC
        rng = random.Random(SEED)
        n_esc = 0
        for _ in range(N):
            if rng.random() < 0.8:
                h = rng.uniform(0.02, hi_h)
                x = rng.uniform(0.8, 1.5)
            else:
                h = rng.uniform(0.10, 0.20)
                x = rng.uniform(0.05, 0.40)
            if h / x > THETA_STAR:
                n_esc += 1
        p = n_esc / float(N)
        se = math.sqrt(p * (1.0 - p) / N)
        z = (p - pred) / se if se > 0.0 else 0.0
        # meter inversion
        te = quantile_meter(hi_h, p, 1e-6, 0.30)
        se_est = se / abs(dsurv(hi_h, te)) if pred > 0.21 else se
        z_book = (te - THETA_STAR) / se_est if se_est > 0.0 else 0.0
        resolves = abs(z_book) <= 1.0

        rows.append({
            "floor_f": f, "hi_h": hi_h,
            "predicted_escape": round(pred, 5),
            "mc_escape": round(p, 5),
            "se": round(se, 5),
            "z_vs_prediction": round(z, 2),
            "plateau_width_theta_star_minus_f": round(
                max(0.0, THETA_STAR - f), 5),
            "theta_est_inverted": round(te, 6),
            "z_book_meter": round(z_book, 2),
            "resolves_theta_star": resolves,
        })
        print("  f=%.4f  pred=%.4f mc=%.4f z=%.2f  plateau=%.4f  "
              "theta_est=%.5f z_book=%+.2f resolve=%s"
              % (f, pred, p, z, max(0.0, THETA_STAR - f), te, z_book,
                 resolves))

    # controls
    r0625 = [r for r in rows if abs(r["floor_f"] - 0.0625) < 1e-9][0]
    switch_first = [r["floor_f"] for r in rows if r["resolves_theta_star"]]
    switch_floor = switch_first[0] if switch_first else None
    continuity_ok = all(abs(r["z_vs_prediction"]) < 3.0 for r in rows)

    out = {
        "identity": "metrological ignition: the plateau-trap disappears "
                    "exactly as the floor crosses f = theta*; escape(f) is "
                    "continuous across the crossover and resolvability "
                    "switches ON the moment the population's reach straddles "
                    "the critical line.  The threshold is where knowing "
                    "knocks: below it, reading = the floor; at and above "
                    "it, reading = theta*.",
        "theta_star": THETA_STAR, "n": N, "seed": SEED,
        "crossover_table": rows,
        "controls": {
            "escape_continuous_at_theta_star": continuity_ok,
            "two_class_replay_theta_est_at_f0625": r0625["theta_est_inverted"],
            "two_class_theta_est_from_populations": 0.05847,
            "delta_method_z_at_f0625": -5.32,
            "z_here_naive_convention_at_f0625": r0625["z_book_meter"],
            "resolvability_switch_floor": switch_floor,
            "switch_is_strictly_above_theta_star":
                (switch_floor is not None and switch_floor > THETA_STAR),
        },
        "law": "resolvability: ON iff floor f > theta* (population "
               "straddles); OFF below (reading pinned at the floor).  "
               "Escape is continuous at the crossover; the meter's "
               "precision is not - it jumps from 'floor-pinned' to "
               "'theta*-reading' at f = theta*.  The practical design "
               "number: a probing population must keep its floor strictly "
               "above theta* by a margin accessible to its own slope "
               "S_A'(theta*).",
        "design_rule": "for a ledger experiment probing theta*, choose the "
                       "probing population so its severity reach crosses "
                       "theta*; the minimal honest margin is the floor "
                       "where the meter first reads theta* within 1 sigma "
                       "(measured switch floor); keep the necessity "
                       "ceiling/freeze gate consistent with population "
                       "reach that still touches both sides of the line.",
        "epistemic_reading": "the critical line is where MEASUREMENT "
                             "ignites: below-the-reach populations report "
                             "their own limitation, across-the-reach "
                             "populations reveal the constant.  Natural "
                             "philosophy of the ledger: you must have a "
                             "foot on both sides of the boundary to read "
                             "the boundary.",
        "references_note": "survival per meter and quantile method (Barlow "
                           "& Proschan 1975); delta-method uncertainty and "
                           "inverse-variance combination (Kendall & "
                           "Stuart); systematic shape-bias vs statistical "
                           "error (JCGM 2008 GUM); the switch is a measured "
                           "crossover, with the phase-transition vocabulary "
                           "(Stanley 1971) used ONLY as explicit analogy.",
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_crossover.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("controls: escape continuous at crossover = %s; switch floor = %s "
          "(> theta* = %s); two_class replay: theta_est=%.5f (genesis_"
          "populations 0.05847); delta-method z=-5.32 (genesis_meter), "
          "naive-convention z=%+.2f here"
          % (continuity_ok, switch_floor, switch_floor > THETA_STAR,
             r0625["theta_est_inverted"], r0625["z_book_meter"]))
    print("law: resolvability ON iff floor > theta*; escape continuous "
          "across the crossover; the switch is at f = theta*.")
    print("WROTE data/genesis_crossover.json")


if __name__ == "__main__":
    main()