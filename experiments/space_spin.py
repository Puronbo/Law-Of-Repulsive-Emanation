"""
space_spin.py
=============
The spinning mechanism for three-dimensional movement in space, reduced to
closed forms. Every number is recomputed here from its equation with stated
constants and written to data/space_spin_data.json so the book's appendix
and the artifact stay in lockstep. Verdicts are ANALYTIC (equation output
with the stated constants), HYPOTHESIS (the equation holds but the input
inventory - inertias, wheel speeds, cluster geometry - is an assumption),
or MEASURED (the equation reproduced on published flight hardware).

The mechanism, and its closed forms:

 1. MOMENTUM EXCHANGE (reaction wheels). A wheel of inertia I_w spun to
    omega_w stores angular momentum  H_w = I_w omega_w. Conservation turns
    the spacecraft (inertia I_s) the other way:
        H_w = I_s Omega_s          (angular momentum conservation)
        Omega_s = H_w / I_s        (spacecraft spin rate)
        slew angle  theta = Omega_s t,  time  t = theta / Omega_s
    Wheel sizing:  I_w = H_w / omega_w.  Desaturation (momentum dumping)
    needs an external torque source (thrusters or magnetic torquers).

 2. CONTROL MOMENT GYROSCOPE (CMG). A constant-speed rotor of momentum
    h, gimballed at rate omega_g, outputs the gyroscopic torque
        tau = h x omega_g,        |tau| = h omega_g      (torque amplifier)
    A cluster of n single-gimbal CMGs spans 3D torque via the Jacobian:
        tau = -A(Delta) Delta_dot,   A = [g_i x h_i],   rank(A) <= 3
    Singularity:  det(A A^T) = 0  -  torque directions become coplanar and
    one axis is un-torqueable. n >= 3 for 3-axis control; the pyramid
    cluster of 4 at skew beta = arcsin(1/sqrt(3)) = 54.73 deg is the
    standard redundancy + singularity-escape geometry.

 3. SPIN STABILITY (tennis racket / intermediate axis). Torque-free Euler
    equations. Spin about principal axis k is linearly stable iff
        (I_k - I_i)(I_k - I_j) > 0
    i.e. about the MAXIMUM or MINIMUM inertia axis. The intermediate axis
    gives (I_k - I_i)(I_k - I_j) < 0 - a saddle - and the body flips
    (Dzhanibekov effect). With internal energy dissipation the body
    relaxes to spin about the major axis (Explorer 1: spun about its long
    minor axis, precessed and tumbled).

 4. THREE-AXIS COVERAGE. Three non-coplanar wheel axes span torque space;
    the 4th wheel (and the 4-CMG pyramid) buys failure tolerance and
    singularity escape. Because total angular momentum is conserved, a
    wheel/CMG set reorients the spacecraft to ANY attitude without
    propellant - the zero-propellant 3D movement mechanism.

Usage: python space_spin.py
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT_FILE = os.path.join(DATA, "space_spin_data.json")

DEG = math.pi / 180.0


def banner(title):
    print("=" * 72)
    print(title)
    print("=" * 72)


# ---------------------------------------------------------------------- #
# 1. momentum exchange - reaction wheels                                  #
# ---------------------------------------------------------------------- #
def momentum_exchange():
    out = {"note": "H_w = I_w omega_w;  I_s Omega_s = H_w;  slew theta = Omega_s t"}

    # Hubble-class example: published figures from the HST Pointing Control
    # System (4 x 45 kg reaction wheel assemblies, 500 Nms total momentum
    # storage, ~90 deg in 15 min slew; magnetic torquers for desaturation).
    I_s = 7.7e4       # kg m^2  (HST bus inertia, stated inventory)
    H_cap = 500.0     # Nms     (published momentum-storage capacity)
    n = 4
    H_wheel = H_cap / n
    omega_max = H_cap / I_s
    t_full = (math.pi / 2.0) / omega_max       # 90 deg at full capacity

    # published pace: 90 deg in 15 min
    omega_pub = (math.pi / 2.0) / 900.0
    H_pub = I_s * omega_pub

    # wheel physics: solid disk  I_w = (1/2) m r^2
    m_w, r_w = 45.0, 0.25     # kg, m  (radius is stated inventory)
    I_w = 0.5 * m_w * r_w * r_w
    omega_wheel = H_wheel / I_w

    out.update({
        "I_s_kgm2": I_s,
        "H_cap_total_Nms": H_cap,
        "n_wheels": n,
        "H_per_wheel_Nms": round(H_wheel, 1),
        "omega_s_max_rad_s": round(omega_max, 5),
        "omega_s_max_deg_s": round(math.degrees(omega_max), 3),
        "slew_90deg_at_capacity_s": round(t_full, 0),
        "slew_90deg_published_pace_rad_s": round(omega_pub, 6),
        "H_used_published_90deg_Nms": round(H_pub, 1),
        "H_used_frac_of_capacity": round(H_pub / H_cap, 3),
        "wheel_I_w_kgm2": round(I_w, 3),
        "wheel_spin_rad_s": round(omega_wheel, 1),
        "wheel_spin_rpm": round(omega_wheel * 30.0 / math.pi, 0),
        "verdict": ("ANALYTIC: H_w = I_w omega_w with I_s Omega_s = H_w. "
                    "The published Hubble numbers close: 500 Nms over 4 "
                    "wheels = 125 Nms each, spinning a 45 kg, 0.25 m radius "
                    "disk at ~850 rpm; the 90 deg-in-15-min slew uses "
                    "I_s omega = 134 Nms, ~27% of the 500 Nms budget; full "
                    "capacity would slew 90 deg in ~242 s. The wheel never "
                    "produces net rotation - it exchanges momentum, and "
                    "desaturation needs an external torque source (magnetic "
                    "torquers, thrusters)."),
    })
    return out


# ---------------------------------------------------------------------- #
# 2. control moment gyroscope - the torque amplifier                      #
# ---------------------------------------------------------------------- #
def cmg():
    out = {"note": "tau = h x omega_g;  cluster tau = -A(Delta) Delta_dot;  "
                   "rank(A) <= 3;  singularity det(A A^T) = 0"}

    # single-unit: published hardware cross-check (Georgia Tech CMG testbed:
    # rotor momentum 1.759 Nms, max gimbal rate 25 deg/s, published max
    # output torque 768 mNm).
    h_unit = 1.759        # Nms
    wg_max = 25.0 * DEG   # rad/s
    tau_unit = h_unit * wg_max
    out["cmg_testbed"] = {
        "h_Nms": h_unit,
        "wg_max_deg_s": 25.0,
        "tau_max_Nm": round(tau_unit, 3),
        "published_tau_mNm": 768,
        "match_mNm": round(tau_unit * 1000.0, 0),
    }

    # ISS-class: each CMG rotor momentum 4760 Nms (published), 4 units.
    h_iss = 4760.0
    out["iss_cmg"] = {
        "h_each_Nms": h_iss,
        "n": 4,
        "cluster_momentum_Nms": 4 * h_iss,
    }

    # small-sat pyramid cluster of 4 testbed-class modules on a 100 kg,
    # 2 m spacecraft (I ~ M L^2 / 12 = 33.3 kg m^2).
    I_small = 100.0 * 4.0 / 12.0
    h_cluster = 4.0 * h_unit
    out["small_sat_pyramid"] = {
        "I_s_kgm2": round(I_small, 1),
        "cluster_H_Nms": round(h_cluster, 2),
        "omega_s_max_rad_s": round(h_cluster / I_small, 4),
        "omega_s_max_deg_s": round(math.degrees(h_cluster / I_small), 2),
        "skew_deg": math.degrees(math.asin(math.sqrt(2.0 / 3.0))),
    }

    out["verdict"] = ("ANALYTIC (hardware-validated): tau = h omega_g "
                      "reproduces the Georgia Tech testbed exactly - "
                      "1.759 Nms at 25 deg/s gimbal rate gives 768 mNm, the "
                      "published rating. The CMG is a torque amplifier: the "
                      "gimbal motor turns a constant-speed rotor's momentum "
                      "vector, not the rotor's speed. Three single-gimbal "
                      "units span 3-axis torque; a 4-unit pyramid at "
                      "54.73 deg gives redundancy and singularity escape. "
                      "The singular states (det(A A^T) = 0) are the known "
                      "wall, escaped by steering laws (Moore-Penrose, "
                      "singularity-robust).")
    return out


# ---------------------------------------------------------------------- #
# 3. spin stability - tennis racket / intermediate axis                   #
# ---------------------------------------------------------------------- #
def spin_stability():
    out = {"note": "(I_k - I_i)(I_k - I_j) > 0 stable;  < 0 saddle (flip)"}

    # cuboid 0.20 x 0.05 x 0.15 m, 1 kg: I_a = m/12 (b^2 + c^2), etc.
    m, a, b, c = 1.0, 0.20, 0.05, 0.15
    I_x = m / 12.0 * (b * b + c * c)     # spin axis along a (x)
    I_y = m / 12.0 * (a * a + c * c)     # spin axis along b (y)
    I_z = m / 12.0 * (a * a + b * b)     # spin axis along c (z)
    axes = {"x(minor)": I_x, "y(major)": I_y, "z(intermediate)": I_z}
    ranked = sorted(axes.items(), key=lambda kv: kv[1])
    verdicts = {}
    for name, I_k in axes.items():
        others = [I for n, I in axes.items() if n != name]
        prod = (I_k - others[0]) * (I_k - others[1])
        verdicts[name] = {"I": round(I_k, 6),
                          "product": round(prod, 8),
                          "stable": prod > 0}
    out["cuboid_inertias_kgm2"] = {k: round(v, 6) for k, v in axes.items()}
    out["ranked_axes"] = [n for n, _ in ranked]
    out["stability"] = verdicts
    out["example_flip_axis"] = "z(intermediate)"

    # Explorer 1 lesson: spin about the minor (long) axis is stable in the
    # rigid Euler equations but energy dissipation relaxes the body to the
    # major axis - the real-world spin-stabilization failure mode.
    out["energy_relaxation"] = {
        "explorer1": "spun about its long (minor-inertia) axis; internal "
                     "dissipation drove precession relaxation to the major "
                     "axis and the spacecraft tumbled",
        "soho_1998": "unintentional spin destabilized the control laws; "
                     "dissipation in hydrazine tanks settled it on the "
                     "maximum-momentum axis",
    }

    out["verdict"] = ("ANALYTIC: the product criterion reproduces the "
                      "tennis-racket theorem - spin about the minor and "
                      "major axes is stable ((I_k-I_i)(I_k-I_j) > 0), spin "
                      "about the intermediate axis is a saddle (< 0) and "
                      "flips (Dzhanibekov). On the cuboid, x(minor) and "
                      "y(major) are stable, z(intermediate) flips. The "
                      "rigid-body verdict is not the full story: with any "
                      "energy dissipation the spin relaxes to the major "
                      "axis (Explorer 1, SOHO). A spin-stabilized vehicle "
                      "must spin about its major axis or carry wheels/CMGs "
                      "to hold the intended axis.")
    return out


# ---------------------------------------------------------------------- #
# 4. three-axis coverage - why 3, why 4, why no propellant                 #
# ---------------------------------------------------------------------- #
def three_axis():
    out = {
        "note": "3 non-coplanar wheel/CMG axes span torque space; the 4th "
                "buys failure tolerance and singularity escape; momentum "
                "conservation makes reorientation propellant-free",
        "span_condition": "no three spin axes coplanar (non-defective "
                          "configuration)",
        "reaction_wheels": "4 wheels, pyramid or orthogonal + 1 spare, "
                           "provide 3-axis control after any single failure",
        "cmg_cluster": ">= 3 single-gimbal units for 3-axis control; the "
                       "standard pyramid of 4 at 54.73 deg for redundancy "
                       "and singularity escape",
        "zero_propellant": "total angular momentum conserved: I_s Omega_s + "
                           "H_wheels = const, so internal wheels reorient "
                           "the spacecraft to any attitude without fuel; "
                           "only desaturation consumes external torque",
    }
    out["verdict"] = "ANALYTIC: 3 axes span R^3, the 4th covers failure."
    return out


def main():
    banner("SPIN: the spinning mechanism for 3D movement in space")
    sections = [
        ("momentum_exchange", momentum_exchange()),
        ("cmg", cmg()),
        ("spin_stability", spin_stability()),
        ("three_axis", three_axis()),
    ]
    data = {}
    for name, out in sections:
        data[name] = out
        print("\n[%s] %s" % (name, out["verdict"]))
    os.makedirs(DATA, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)
    print("\nwrote %s" % OUT_FILE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
