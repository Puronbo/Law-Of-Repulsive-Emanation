# NEXT STEPS: byte-honest innovation roadmap for the sealed register

> Register premise (invariant, re-stated at the top of every innovation doc):
> this lane seal is byte-pinned. `645 passed` exit 0, meta-audit 10/10,
> validators 86=86, closure digest == pin `9fff3988…88b7794`, sealed HEAD
> genesis-pushed. Nothing below claims a result that is not byte-real.

## The five genuine next steps (ordered by true value ÷ honesty cost)

### 1. Origin-lane Lean/kernel bridge (the only lever that can move 5/7 → 7/7)
Real, bounded, but heavy. The two reserved names (`EcaIsometry`,
`MillenniumBridge`) are sealed on this lane as **vendored/prose bytes only** —
byte-verified, not 7/7-derivable here. The single lawful way to promote them:
a real `lake build` with a genuine Mathlib fetch inside the *origin lane*
(the Desktop lane you told me to set aside), then a real `lean build` of the
two twin sources. This is minutes-to-hours of real Lean/Mathlib work and
requires network + your explicit go (the sealed lane itself must stay put).
Until it runs with true exit 0, the register stays honestly at 5/7 + 2/7.

### 2. Provenance-pinned closure refresh (keeps 86=86 drift-minimal)
Add a small, real gate: every future *authorized* register move must
recompute the sealed-twin SHA-512 closure against the extracted pin and only
commit if `recompute == pin`. Concretely validators already recompute this;
the innovation is to make it the *push-time* gate as a pre-receive check
(CI-recommended `validate_soliton_millennium_meta_audit.py` exit 0 before
every push). No new claim, no digest change — just automation of a rule that
already holds.

### 3. Twin-vs-vendored byte-normalization check
A real `diff --byte` consistency audit between the sealed lane's tested
twins and the registered 7-twin closure (`tests/` count 24 + 2/7 reserved
prose). Keep as a planner-only gate, since vendored-byte equality is
already the register's own truth (86 let me note: 86 = the 86 validators;
don't blur counts).

### 4. Human-review handoff doc
Generate a concrete `HANDOFF.md` naming the exact files that encode the
5/7 derivable twins, the 2/7 reserved prose stubs, and the exact pin digest
so a domain reviewer can independently reproduce each gate. Byte-steering
only; no proof claims.

### 5. Cross-version reproducibility
For the kernel bridge specifically, pin the origin lane's `lake build`
toolchain in a real `lean-toolchain` byte file *at the origin lane* (never
here), so a future bounded build is byte-reproducible across machines. The
mine already carries `v4.34.0` in elan; the toolchain file is the real
byte-necessity.

## What I will NOT innovate (honest boundary)
- No fabricated 7/7, no claimed Lean-kernel pass unless a real build exits 0.
- No digest/pin recomputation without byte-identity to the pinned register.
- No movement of the sealed lane without your explicit go (each item above
  is either origin-lane only or a read-only/planner gate here).

---
Register stays sealed: `HEAD 5436866`, drift 21 (untracked register entries,
byte-visible), all gates green, all claims byte-real.
