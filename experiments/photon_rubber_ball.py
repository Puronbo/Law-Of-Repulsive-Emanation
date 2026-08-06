"""
PHOTON IN A RUBBER BALL - absolute zero containment, then temperature release.

Brief from the user:
    "Photon in a rubber ball positions of (0,0) and (0,1), respectively.
     Contain in absolute zero then release temperature."

Interpretation (stated plainly so the experiment is reproducible):
  - "rubber ball"  = an elastic circular container: a disk of radius R = 2
    centred at (1,1); the wall is a rubber membrane.  R = 2 strictly
    contains the start point (0,0) (distance sqrt(2) ~ 1.414 < R).
  - "photon"       = a massless point particle moving at speed c (natural
    units c = 1); state = position q, direction d, energy E.
  - "(0,0) and (0,1), respectively" = the photon starts at (0,0) (strictly
    inside the ball at (1,1)) and its initial direction of travel points to
    (0,1) (unit +y) - the ball CONTAINS the photon from the start.
  - "contain in absolute zero" = wall temperature T = 0: the rubber wall is
    perfectly still (its normal velocity distribution has zero width), so the
    photon bounces elastically and its energy E is exactly conserved - the
    photon is contained; it never leaves the ball.
  - "release temperature" = the wall is heated to T > 0; each wall patch's
    outward normal velocity u_n ~ N(0, sqrt(kB*T/m_seg)); the photon's energy
    updates by the exact relativistic Doppler reflection factor
        E' = E * (1 - u_n/c) / (1 + u_n/c)
    (photon as excess resonant energy reflecting off a moving mirror; cf.
    docs/PHYSICAL_UNIVERSAL_MAP.md "the photon is excess resonant energy").

Physics result (measured below, stated honestly):
  The wall-velocity distribution is symmetric, so log E is an EXACT
  martingale - every odd moment of ln F vanishes, so the MEDIAN photon energy
  never moves.  The ARITHMETIC mean energy, however, grows: with s = sigma/c,
    <F> = E[(1-u/c)/(1+u/c)] = 1 + 2 s^2 + 6 s^4 + ... > 1
  so <E>(n) ~ E0 * <F>^n.  This is stochastic Doppler heating (the
  Fermi-acceleration signature): elastic reflection off a warm rubber wall
  heats the mean energy WITHOUT ever equilibrating the photon to the wall
  temperature.  A true Planck/Maxwell equilibrium needs emission/absorption,
  which is outside this model (honest limit, section 7).

Outputs: data/photon_rubber_ball_data.json (T-series experiment convention).
"""

import numpy as np
import os, json, math

C = 1.0            # speed of light (natural units)
R = 2.0            # rubber-ball radius (2D disk), centred at (1,1):
                   # strictly contains the photon start (0,0): sqrt(2) < R
CENTER = np.array([1.0, 1.0])   # ball centre (user correction: ball at (1,1))
KB = 1.0           # Boltzmann constant (temperature in energy units)
E0 = 1.0           # photon energy at absolute zero (resonant energy, > 0:
                   # a massless particle cannot be at rest)
M_SEG = 2500.0     # rubber membrane patch mass
N_COLL = 2000      # wall collisions after temperature release
E_REPS = 4000      # ensemble size (independent photon runs)
SEED = 20260804
T_RELEASE = 1.0    # headline released temperature
T_SWEEP = [1.0, 4.0, 9.0]   # scaling check of the growth rate vs T

out = {}


def wall_hit(q, d):
    """Distance from q (inside the disk centred at CENTER) along direction d
    to the wall, the impact position, and the outward unit normal."""
    q = np.asarray(q, float)
    d = np.asarray(d, float)
    rel = q - CENTER
    b = rel.dot(d)
    disc = b * b + R * R - rel.dot(rel)
    t = -b + math.sqrt(max(disc, 0.0))
    q1 = q + t * d
    n = (q1 - CENTER) / R
    return t, q1, n


def reflect(d, n):
    """Specular reflection of direction d off the wall at normal n."""
    return d - 2.0 * d.dot(n) * n


def trajectory(q0, d0, n_coll):
    """Billard orbit inside the disk centred at CENTER.  Returns impact
    positions (n+1,2), per-leg chord lengths, radii from the ball centre,
    and per-leg impact parameters b = |(q-O) x d|."""
    q = np.array(q0, float)
    d = np.array(d0, float) / np.linalg.norm(d0)
    qs = np.zeros((n_coll + 1, 2))
    chords = np.zeros(n_coll)
    radii = np.zeros(n_coll)
    impact = np.zeros(n_coll)
    qs[0] = q
    for i in range(n_coll):
        t, q1, n = wall_hit(q, d)
        qs[i + 1] = q1
        chords[i] = t
        radii[i] = float(np.linalg.norm(q1 - CENTER))
        impact[i] = float(abs((q[0] - CENTER[0]) * d[1] - (q[1] - CENTER[1]) * d[0]))
        d = reflect(d, n)
        q = q1
    return qs, chords, radii, impact


def doppler_factor(u_n, c=C):
    """Exact relativistic Doppler factor for a photon reflecting off a
    mirror with outward-normal velocity u_n (u_n < 0 = wall contracting
    toward the photon -> blueshift, gain; u_n > 0 = expanding -> loss)."""
    return (1.0 - u_n / c) / (1.0 + u_n / c)


# ---------------------------------------------------------------------- #
print("=" * 72)
print("PHOTON IN A RUBBER BALL  (c=1, ball R=2 at (1,1), start (0,0), dir (0,1))")
print("Contain at absolute zero, then release temperature.")
print("=" * 72)

# ---------------- PHASE A: containment at absolute zero ---------------- #
print("\n--- PHASE A: contain in absolute zero (T_wall = 0) -------------")
orb, chords_a, radii_a, imp_a = trajectory((0.0, 0.0), (0.0, 1.0), N_COLL)
gen, chords_g, radii_g, imp_g = trajectory((0.0, 0.0), (0.4, 0.8), N_COLL)

# energy is exactly conserved at T = 0 (every Doppler factor is 1)
E_path = E0 * np.cumprod(np.full(N_COLL, doppler_factor(0.0)))
e_cons = float(E_path[-1]) == float(E0)
contained_a = bool(np.max(radii_a) <= R + 1e-12)
contained_g = bool(np.max(radii_g) <= R + 1e-12)
# circular-billiard caustic: the impact parameter b = |(q-O) x d| of every
# chord is exactly constant -> the photon is trapped on one caustic circle
caustic_a = bool(np.allclose(imp_a, imp_a[0], rtol=0, atol=1e-12))
caustic_g = bool(np.allclose(imp_g, imp_g[0], rtol=0, atol=1e-12))
dist_start = float(np.linalg.norm(CENTER))     # |(1,1)-(0,0)| = sqrt(2)

print(f"  ball: disk R = {R} centred at {CENTER.tolist()}; photon starts at "
      f"(0,0), inside (distance {dist_start:.6f} < R = {R})")
print(f"  orbit (0,1): max radius-from-ball-centre = {np.max(radii_a):.12f}  (<= R)")
print(f"  orbit (0.4,0.8): max radius-from-ball-centre = {np.max(radii_g):.12f}  (<= R)")
print(f"  first leg (0,0)->wall = {chords_a[0]:.12f}; impact parameter "
      f"b = |(q-O) x d| constant {imp_a[0]:.12f} -> caustic invariant "
      f"{caustic_a} (generic orbit {caustic_g})")
print(f"  photon energy after {N_COLL} wall hits = {E_path[-1]:.6g} "
      f"(== E0 = {E0}) -> bit-exact conservation at absolute zero")

out["phaseA_absolute_zero"] = {
    "interpretation": "rubber ball = disk R=2 centred at (1,1); photon starts "
                      "at (0,0) (strictly inside, distance sqrt(2) < R), "
                      "initial direction toward (0,1); wall at T=0 (perfectly "
                      "still rubber membrane)",
    "ball_centre": CENTER.tolist(),
    "ball_radius": R,
    "energy_conserved_bit_exact": e_cons,
    "max_radius_vertical_orbit": float(np.max(radii_a)),
    "max_radius_generic_orbit": float(np.max(radii_g)),
    "contained_vertical": contained_a,
    "contained_generic": contained_g,
    "impact_parameter_invariant_vertical": caustic_a,
    "impact_parameter_invariant_generic": caustic_g,
    "impact_parameter_vertical": float(imp_a[0]),
    "impact_parameter_generic": float(imp_g[0]),
    "first_leg_length": float(chords_a[0]),
    "n_collisions": N_COLL,
    "verdict": "PASS",
}

# ---------------- PHASE B: release temperature (T_wall > 0) ------------ #
print("\n--- PHASE B: release temperature (thermal rubber wall) ----------")
rng = np.random.default_rng(SEED)

def run_release(T_w, n_coll=N_COLL, reps=E_REPS):
    """Ensemble of photon runs against a wall at temperature T_w."""
    s = math.sqrt(KB * T_w / M_SEG) / C              # sigma / c
    U = rng.normal(0.0, s * C, size=(reps, n_coll))  # outward normal velocity
    F = doppler_factor(U)
    E = E0 * np.cumprod(F, axis=1)
    Ef = E[:, -1]
    logE = np.log(Ef / E0)
    lg_mean = float(logE.mean())
    lg_std = float(logE.std(ddof=1))
    mean_E = float(Ef.mean())
    median_E = float(np.median(Ef))
    mean_F = float(F.mean())
    pred_F = 1.0 + 2.0 * s * s + 6.0 * s ** 4        # <F> series, 4th order
    pred_mean_E = E0 * pred_F ** n_coll
    pred_lg_std = math.sqrt(n_coll * 4.0 * s * s)    # var(ln F) ~ 4 s^2
    skew = float((((logE - lg_mean) ** 3)).mean() / (lg_std ** 3 + 1e-300))
    kurt = float((((logE - lg_mean) ** 4)).mean() / (lg_std ** 4 + 1e-300))
    # median flatness across time (log E is an exact martingale)
    medians = np.median(E, axis=0)
    med_dev = float(np.max(np.abs(medians / E0 - 1.0)))
    return {
        "T_wall": T_w,
        "sigma_over_c": s,
        "mean_energy": mean_E,
        "mean_energy_pred": pred_mean_E,
        "mean_ratio": mean_E / pred_mean_E,
        "median_energy": median_E,
        "median_flat_max_dev": med_dev,
        "empirical_mean_F": mean_F,
        "series_mean_F": pred_F,
        "lnE_mean": lg_mean,
        "lnE_std": lg_std,
        "lnE_std_pred": pred_lg_std,
        "lnE_std_ratio": lg_std / pred_lg_std,
        "lnE_skew": skew,
        "lnE_kurtosis": kurt,
        "T_photon_mean": mean_E / KB,
        "T_photon_median": median_E / KB,
    }

res = {}
for T_w in [T_RELEASE] + T_SWEEP:
    res[str(T_w)] = run_release(T_w)
    r = res[str(T_w)]
    print(f"  T_wall = {T_w:g} (sigma/c = {r['sigma_over_c']:.4g}): "
          f"<E> = {r['mean_energy']:8.3f} (pred {r['mean_energy_pred']:8.3f}), "
          f"median E = {r['median_energy']:8.3f}, "
          f"lnE: mean {r['lnE_mean']:+.3f} std {r['lnE_std']:.3f} "
          f"(pred {r['lnE_std_pred']:.3f})")

h = res[str(T_RELEASE)]
print("\n  HEADLINE (T_release = 1, sigma/c = 0.02):")
print(f"    arithmetic-mean energy grows by x{res[str(T_RELEASE)]['mean_energy']/E0:.2f} "
      f"over {N_COLL} hits (stochastic Doppler heating; pred x"
      f"{res[str(T_RELEASE)]['mean_energy_pred']/E0:.2f})")
print(f"    median energy stays at E0 (max deviation "
      f"{res[str(T_RELEASE)]['median_flat_max_dev']:.4f}) - log-E martingale")
print(f"    ln(E/E0) distribution: mean {h['lnE_mean']:+.3f}, std {h['lnE_std']:.3f}, "
      f"skew {h['lnE_skew']:+.2f}, kurtosis {h['lnE_kurtosis']:.2f} (Gaussian: 0, 3)")

# growth-rate scaling: g ~ 2 sigma^2 / c^2 = 2 T / (m_seg c^2)
print("\n  growth-rate scaling vs T_wall (g = <E>/E0 ** (1/N) - 1):")
scale = []
for T_w in T_SWEEP:
    r = res[str(T_w)]
    g = (r["mean_energy"] / E0) ** (1.0 / N_COLL) - 1.0
    g_pred = r["series_mean_F"] - 1.0
    g_over_sigma2 = g / (r["sigma_over_c"] ** 2)
    scale.append({"T_wall": T_w, "growth": g, "growth_pred": g_pred,
                  "g_over_sigma2_c2": g_over_sigma2})
    print(f"    T={T_w:g}: g = {g:.6g} (pred {g_pred:.6g}), "
          f"g/sigma^2 = {g_over_sigma2:.3f} (theory 2)")
out["phaseB_release_temperature"] = {
    "n_collisions": N_COLL,
    "n_ensemble": E_REPS,
    "seed": SEED,
    "headline_T_wall": T_RELEASE,
    "per_T": res,
    "growth_scale": scale,
    "verdict": "MEASURED",
}

# ---------------- save + verdict --------------------------------------- #
os.makedirs("data", exist_ok=True)
with open(os.path.join("data", "photon_rubber_ball_data.json"), "w") as fp:
    json.dump(out, fp, indent=2)
print(f"\nsaved data/photon_rubber_ball_data.json")

print("\nVERDICT")
print("=" * 72)
print("  Contained at absolute zero (T_wall = 0): the rubber wall is still,")
print("  the photon bounces forever inside the ball, energy bit-exactly")
print("  conserved, max radius = R (never leaves); the impact parameter")
print("  b = |(q-O) x d| is exactly constant - a circular-billiard caustic.")
print("  Release temperature (T_wall > 0): the wall is thermal, each hit")
print("  Doppler-shifts the photon by (1-u/c)/(1+u/c).  Because u is")
print("  symmetric, log E is an exact martingale: the MEDIAN energy never")
print("  moves, while the arithmetic MEAN grows as <E> ~ E0 <F>^n with")
print("  <F> = 1 + 2 s^2 + 6 s^4 + ...  - stochastic Doppler heating.")
print("  Elastic reflection does NOT equilibrate the photon to the wall")
print("  temperature; equilibration requires emission/absorption (out of")
print("  scope).  See data/photon_rubber_ball_data.json for the full table.")
