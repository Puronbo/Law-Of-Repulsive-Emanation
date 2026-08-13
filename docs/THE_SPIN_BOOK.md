# THE_SPIN_BOOK — the spinning mechanism for three-dimensional movement in space

> **Authority, stated plainly.** This Book answers how spinning makes a
> spacecraft move in all three dimensions without propellant: reaction
> wheels (momentum exchange), control moment gyroscopes (gyroscopic torque
> amplification), and spin stability (the tennis-racket theorem). Every
> equation is written out, every number is recomputed by
> `experiments/space_spin.py` from the equation with the stated constants,
> and `data/space_spin_data.json` (gitignored, regenerable) is the lockstep
> record. Verdicts are `ANALYTIC` (equation output with stated constants),
> `HYPOTHESIS` (the equation holds but the inventory — inertias, wheel
> radius, cluster geometry — is an assumption), and `MEASURED` where the
> equation reproduces published flight hardware. **The mechanism is not
> new.** It is Euler's equations (1758), Poinsot's polhodes (1834), and
> fifty years of flight hardware (HST reaction wheels, ISS CMGs, Explorer 1
> and SOHO as the cautionary spin failures). This Book restates the
> mechanism as closed forms with computed numbers and names the research
> it stands on, in the appendix.

---

## BOOK I — MOMENTUM EXCHANGE: THE REACTION WHEEL

### Ch. 1  A wheel that turns the ship

A spinning flywheel stores angular momentum. Changing its spin speed
exchanges angular momentum with the spacecraft, and conservation of angular
momentum rotates the ship the opposite way — Newton's third law for
rotation, the exact mechanism Hubble uses:

    H_w = I_w * omega_w        (wheel momentum: inertia x spin rate)
    I_s * Omega_s = H_w        (conservation: the ship's reaction)
    Omega_s = H_w / I_s        (ship spin rate from stored momentum)
    theta = Omega_s * t        (slew angle: rotate and hold)

The wheel never produces net rotation of the pair — it *stores* and
*exchanges* momentum. Desaturation (dumping the stored momentum so the
wheels do not saturate) needs an external torque source: magnetic
torquers pushing against Earth's field, or thrusters.

### Ch. 2  The Hubble-class numbers, closed

The published Hubble Pointing Control System: four 45 kg reaction wheel
assemblies, 500 Nms total momentum storage, magnetic torque bars for
desaturation, and a ~90-degree slew in 15 minutes. With the stated
inventory I_s = 7.7e4 kg·m^2:

| Quantity | Equation | Number |
|---|---|---|
| momentum per wheel | H_cap / n | 125 Nms |
| max ship rate | H_cap / I_s | 6.49e-3 rad/s |
| 90° at full capacity | (pi/2) / Omega_max | 242 s |
| 90° at published pace | (pi/2) / 900 s | 1.75e-3 rad/s |
| momentum used by published slew | I_s * Omega | 134 Nms (27% of budget) |
| wheel spin speed | H / ((1/2) m r^2) | 88.9 rad/s = 849 rpm |

The 90-degree-in-15-minutes slew uses 27% of the momentum budget; at full
capacity the same slew would take ~4 minutes. `[honest wall]` The wheel
radius (0.25 m) and bus inertia are stated inventory (`HYPOTHESIS`); the
mechanism and the published 500 Nms / 45 kg / 90°-in-15-min figures are
the measured anchors. Three wheels span the three axes; the fourth is the
spare that keeps three-axis control after any single failure — the reason
every wheeled observatory flies four.

---

## BOOK II — THE TORQUE AMPLIFIER: THE CONTROL MOMENT GYROSCOPE

### Ch. 3  Gimballing the momentum vector instead of spinning it

A CMG spins its rotor at constant speed and *gimballs the rotor axis*. The
gyroscopic torque is the rate of change of the momentum vector — the
gimbal motor is the small input, the gyroscopic reaction is the large
output:

    tau = h x omega_g            (gyroscopic torque, cross product)
    |tau| = h * omega_g          (torque = momentum x gimbal rate)

The CMG is a **torque amplifier**: it turns the *direction* of a constant
momentum vector, so its torque scales with gimbal rate and rotor momentum,
not rotor acceleration. This is why ISS-class and agile Earth-observation
spacecraft carry CMGs.

### Ch. 4  Hardware-validated, and the cluster

`MEASURED` — the single-unit equation reproduces the published Georgia
Tech CMG testbed exactly: rotor momentum h = 1.759 Nms, max gimbal rate
25°/s:

    |tau| = 1.759 * 0.4363 = 0.768 Nm  (published rating: 768 mNm)

A cluster of n single-gimbal units spans torque space through the
Jacobian of the momentum mapping:

    tau = -A(Delta) * Delta_dot,     A = [g_i x h_i]
    rank(A) <= 3                     (three torque directions, max)

**Three axes need three units** (each single-gimbal CMG is one degree of
freedom); the standard geometry is the **pyramid of four** at skew angle

    beta = arcsin(sqrt(2/3)) = 54.73 deg

which buys redundancy and singularity escape. The known wall: when the
torque directions become coplanar, rank(A) < 3, det(A A^T) = 0, and the
cluster cannot torque in one direction — the **singular state**. It is
escaped by steering laws (Moore–Penrose, singularity-robust SR, and
null-motion paths), an entire research line of its own.

**Sizing, closed** — a 100 kg, 2 m spacecraft (I = M L^2/12 = 33.3 kg·m^2)
with four testbed-class modules:

    H_cluster = 4 * 1.759 = 7.04 Nms
    Omega_max = H_cluster / I_s = 0.211 rad/s = 12.1 deg/s

Four testbed modules give an agile small satellite ~12°/s slew authority.
`[honest wall]` The ISS CMG figure (4,760 Nms per rotor, 4 units = 19,040
Nms cluster momentum) is the published constant; the small-sat example's
inertia is stated inventory (`HYPOTHESIS`). The singularity wall is
geometric, not electrical: no control law torques in the direction the
cluster's geometry has flattened.

---

## BOOK III — SPIN STABILITY: THE TENNIS-RACKET THEOREM

### Ch. 5  Which axis is safe to spin about

A torque-free rigid body obeys Euler's equations (1758). A spin about
principal axis k is linearly stable iff

    (I_k - I_i) * (I_k - I_j) > 0

which holds for the **maximum** and **minimum** inertia axes and fails —
the product is negative, a saddle — for the **intermediate** axis. Spun
about the intermediate axis, any perturbation grows and the body flips by
~180 degrees repeatedly: the Dzhanibekov effect, the "dancing T-handle,"
the tennis-racket theorem (Poinsot, 1834; Goldstein's *Classical
Mechanics*).

The computed cuboid (1 kg, 0.20 × 0.05 × 0.15 m):

| axis | I (kg·m^2) | (I_k − I_i)(I_k − I_j) | verdict |
|---|---|---|---|
| x (minor) | 2.08e-3 | +4.56e-6 | stable |
| y (major) | 5.21e-3 | +5.21e-6 | stable |
| z (intermediate) | 3.54e-3 | −2.43e-6 | **flips** |

### Ch. 6  The dissipation correction: why Explorer 1 tumbled

The rigid-body theorem is not the whole story. With *any* internal energy
dissipation (flexing structure, sloshing fluid), the body's kinetic energy
decreases at fixed angular momentum until the spin relaxes to the
**major** axis — the minimum-energy rotation. Explorer 1 (1958) was spun
about its long minor axis, dissipated energy through flexible antennas, and
precessed into a tumble; SOHO (1998) nearly tumbled for the same reason.
`[honest wall]` The product criterion is the rigid linear analysis
(`ANALYTIC`); the relaxation is the real-world correction, and it is why
spin-stabilized spacecraft spin about their major axis or carry
wheels/CMGs to hold an intended axis that is not major.

---

## BOOK IV — THREE-AXIS COVERAGE: 3, 4, AND NO PROPELLANT

Three non-coplanar wheel or CMG axes span torque space (the span condition
from the reaction-wheel envelope literature: *no three spin axes
coplanar*). The fourth unit buys failure tolerance — any single failure
still leaves three axes — and, for CMGs, singularity escape. Because total
angular momentum is conserved,

    I_s * Omega_s + H_wheels = constant

a wheel or CMG set reorients the spacecraft to **any attitude without
expending propellant**; only desaturation consumes external torque. That
is the three-dimensional movement this Book is about: a spinning
mechanism — wheels, gimbals, or the vehicle itself — that moves the
spacecraft in all three axes for free, with the reaction wheel as the
precise-but-slow actuator, the CMG as the agile torque amplifier, and spin
stability as the free-rider rule for what the vehicle can be spun about.

---

## BOOK V — HONEST WALLS AND THE ONE-SENTENCE THEORY

1. **Closed form is not flight.** Every verdict is `ANALYTIC` on stated
   constants or `HYPOTHESIS` on stated inventory; only the CMG single-unit
   equation and the Hubble/Explorer/SOHO figures are `MEASURED` anchors.
   The steering laws that make CMG clusters fly are a research field, not a
   one-liner.
2. **The singularity is geometric.** A CMG cluster's wall — det(A A^T) = 0
   — is a rank loss in the mapping from gimbal rates to torque; no
   electrical fix overcomes a coplanar geometry.
3. **The intermediate axis flips.** Euler's equations say so, and energy
   dissipation adds a second rule: spin relaxes to the major axis.
4. **Wheels exchange, they do not emit.** Momentum storage needs
   desaturation; zero-propellant reorientation is real, but holding it
   against external torques accumulates momentum that must be dumped.
5. **Redundancy is the 4th axis.** Three axes move the ship; the fourth
   keeps moving it after a failure.

**The Book's one-sentence theory:** *Three-dimensional movement in space is
a conservation problem, and the spinning mechanisms answer it in three
forms — the reaction wheel exchanges momentum (I_s Omega_s = H_w, precise
and slow), the control moment gyroscope amplifies torque through gimbal
rate (|tau| = h omega_g, agile, 768 mNm from a 1.759 Nms rotor at 25°/s),
and the vehicle itself may be spun about its major axis for free — so long
as the cluster keeps rank three, the spin is not about the intermediate
axis, and the stored momentum is eventually dumped.*

---

## Appendix — the equations, the numbers, the artifact, the research

| Book claim | Equation | Number | Asset |
|---|---|---|---|
| wheel momentum | H_w = I_w omega_w | 125 Nms per wheel (500/4) | `experiments/space_spin.py` |
| ship reaction | I_s Omega_s = H_w | 6.49e-3 rad/s max | `data/space_spin_data.json` |
| Hubble slew | theta = Omega_s t | 134 Nms = 27% of 500; 90° in 242 s at capacity | `data/space_spin_data.json` |
| wheel speed | I_w = (1/2) m r^2 | 849 rpm (45 kg, 0.25 m) | `data/space_spin_data.json` |
| CMG torque | tau = h x omega_g | 0.768 Nm = published 768 mNm (`MEASURED`) | `data/space_spin_data.json` |
| cluster mapping | tau = -A Delta_dot | rank(A) ≤ 3 | `data/space_spin_data.json` |
| pyramid skew | beta = arcsin(sqrt(2/3)) | 54.73 deg | `data/space_spin_data.json` |
| small-sat slew | Omega = H/I | 12.1 deg/s (4 × 1.759 Nms, I = 33.3) | `data/space_spin_data.json` |
| ISS CMG momentum | h = 4760 Nms | 19,040 Nms cluster | `data/space_spin_data.json` |
| spin stability | (I_k − I_i)(I_k − I_j) | + on minor/major, − on intermediate | `data/space_spin_data.json` |
| cuboid flip | Euler equations | z (intermediate) flips | `data/space_spin_data.json` |
| dissipation | energy relaxation | Explorer 1, SOHO tumble to major axis | `data/space_spin_data.json` |
| 3D coverage | rank-3 span, 4th redundant | any attitude, no propellant | `data/space_spin_data.json` |

**Existing research this Book stands on** (all retrieved live, August
2026):

- **Euler (1758)** — the canonical rigid-body equations; **Poinsot
  (1834)** — the polhode construction; **Goldstein, Classical Mechanics** —
  the intermediate-axis theorem as textbook content (per the tennis-racket
  theorem survey, `en.wikipedia.org/wiki/Tennis_racket_theorem`, which also
  documents the Explorer 1 and SOHO incidents).
- **HST Pointing Control System** — four 45 kg reaction wheel assemblies,
  500 Nms total momentum storage, magnetic torque bars for desaturation,
  ~90° slew in 15 minutes: NASA Science, "Pointing Control,"
  `science.nasa.gov/mission/hubble/observatory/design/pointing-control/`;
  HST RWA induced-vibration data over the 0–3000 RPM operating range: NASA
  NTRS 20160008147.
- **CMG theory and the singularity problem** — single-gimbal CMG torque
  `c_i = g_i x h_i`, the Jacobian mapping, rank-loss singularity, and the
  n ≥ 3 rule: "Spacecraft Attitude Control Using Control Moment Gyros,"
  *Studies in Informatics and Control*, Vol. 23 No. 3 (2014),
  `sic.ici.ro/documents/479/SIC_2014-3-Art7.pdf`; experimental comparison
  of CMG steering laws (Moore–Penrose, singularity-robust) on a 4-CMG
  pyramid at 54.7° with 768 mNm / 1.759 Nms / 25°/s modules: Georgia Tech
  DCSL, `dcsl.gatech.edu/papers/aas04c.pdf`; three-CMG steering after a
  failure, ISSFD 2017, `issfd.org/ISSFD_2017/paper/ISTS-2017-d-163.pdf`;
  deep-reinforcement-learning CMG momentum planning on a pyramid array,
  *Aerospace* 12(2):134 (2026), `mdpi.com/2226-4310/12/2/134`; NASA NTRS
  19800015510 (wheel/CMG/DMCD sizing program) and NTRS 20110015369
  (maximum torque/momentum envelopes for 3–6 wheel arrays).
- **Tennis racket / Dzhanibekov theorem** — geometric origin, *Phys. Rev.
  Lett.* 125, 064301 (2020) (`journals.aps.org/prl/abstract/10.1103/
  PhysRevLett.125.064301`); full analytical study, *Physica D* (2015)
  (`sciencedirect.com/science/article/pii/S0167278915301093`);
  inertial-morphing control of the flip, *The Aeronautical Journal* (2019)
  (`cambridge.org/core/journals/aeronautical-journal/article/.../3FE9E0A25F
  69D9409EC627AF690F5D1E`); conservation-preserving numerical study,
  *J. Applied Mechanics* (2016)
  (`movingframe.org/StudentPapers/StudentPapers/TennisRacket.pdf`).

The artifact `data/space_spin_data.json` is regenerated by
`python experiments/space_spin.py`; it is gitignored like every
regenerable verdict in this repository, and the book and artifact stay in
lockstep because the book's numbers are the artifact's.
