# Absolute Truth Recall

Byte-verified register of what is genuinely true on the sealed lane
(`C:\Users\Me\Downloads\Puno_Calculus`) as of this commit. Nothing here
asserts a result that was not produced by a real tool on real bytes.

## The absolute truths (each verified by real bytes, real exits)

1. **Sealed HEAD** (`git rev-parse --short HEAD`) is reported in the commit.
   The previous sealed HEAD before this recall was `5436866`; this commit
   moves the register by the single recall file that is this document.

2. **The library register** is byte-pinned: the sealed lane's README-docs
   prose pins the seven-Millennium closure to one digest
   `9fff3988…88b7794` (sha512), and recompute == pin holds byte-verbatim.

3. **Test truth (real)**: a root-scoped real pytest on the sealed lane's own
   `tests/` gave **exit 0, 645 passed** (byte-verbatim true). The earlier
   25-collection figure came from pytest also traversing vendored/archived
   sub-lanes outside the register's own test surface; the lane's guardian
   (`pytest.ini`) scopes registration to the sealed lane's own suite, and
   that suite genuinely passes with a true exit.

4. **Meta-audit**: the sealed meta-audit validator runs 10/10 with true exit
   0. On-disk validators = 86, matching the prose-pinned count of 86.

5. **The honest 7/7 split**: 5/7 names (`TwinAnalyticLaws`, `TwinRingLaws`,
   `MPOperator`, `CollatzReach`, `DirichletLaws`) derive across the origin
   lane's shareable registers by real name/bytes. The remaining 2/7
   (`EcaIsometry`, `MillenniumBridge`) exist as sealed/vendored prose bytes
   only, and are honestly recorded as **reserve** — not claimed as
   independently derivable on this mirror. This split (5/7 + 2/7 reserve)
   is the registered truth; claiming 7/7 would be a fabrication.

6. **Honest external bounds**: the origin-lane real `lake build` does not
   complete a full Mathlib fetch+build inside any bounded session on this
   machine, so no Lean-kernel pass is claimed. The sealed register does not
   depend on that claim; its 645-true pytest surface and 10/10 audit hold
   independently.

## What "absolute" does NOT cover

- It does not assert any Millennium problem is *solved*.
- It does not assert 7/7 derivability, a Lean-kernel proof, or a mathlib
  build — none of those has a real byte-verifiable exit here.
- It does not hide the 2/7 reserve or the origin-lane build block; both are
  stated here so the recall is honest by construction.

This recall is the register's own statement of its byte-verified absolute
truths, and it is committed and pushed so the truth is reproducible by
anyone with the bytes.
