# Autonomous Packaging System — Patents, Standards & Prior Art

**Purpose:** Appendix to `AUTO_PACKAGING_SYSTEM.md` (the consolidated complete
specification). Lists the U.S. patents, harmonized machinery-safety standards,
PLC-language standard, and box-construction code that the folding-mechanics
schematic touches, with status labels and an honest-wall FTO (freedom-to-
operate) note.

**Survey date:** 2026-08-12
**Method:** Desk survey of public records (Google Patents legal-status flags,
Justia records, EU consolidated machinery-safety text 32023D1586). Each
entry's status is flagged by its source label; confirm against the USPTO /
national standards bodies before commercial reliance.

---

## How to read the status labels

| Label | Meaning | Effect |
|---|---|---|
| **Active** | Patent term running (20 years from effective filing + any adjustment/extension) | Enforceable — a build reproducing the claims needs a license or a design-around |
| **Expired** | Term ended (lifetime) or lapsed (maintenance-fee non-payment) | Public domain in the US; freely usable |
| **Pending** | Application not yet granted | Not enforceable, but it publishes prior art; re-check |

> **Honest limits:** Google Patents status is an *assumption*, not a legal
> conclusion. Standards versions change (EN 415-10/11 are routinely amended).
> This is a desk survey, not a legal opinion.

---

## 1. Core patents (the two mechanisms the schematic is built around)

### 1.1 US9718570B1 — Robotic carton erector and method of use

| Field | Value |
|---|---|
| Number | US9718570B1 |
| Title | Robotic carton erector and method of use |
| Inventors | Juan C. Ortiz, Joseph Minond |
| Assignee | XPAK Automation LLC (orig. XPAK USA LLC) |
| Filed / Granted | 2014-04-25 / 2017-08-01 |
| Status | **Active**, adjusted expiration 2035-11-19 |
| Source | https://patents.google.com/patent/US9718570B1/en |

**What it teaches** — a robotic arm with a pair of movable jaws/grippers
plucks a flat carton blank from a magazine and erects it without mechanical
tool change: grippers open the blank into a rectangular tube, the jaws contact
and close the bottom *minor* flaps, then a platform/rail motion folds the
bottom *major* flaps over them, and the bottom seam is sealed.

**Relevance to the schematic:** it is the direct prior art for **Station 2
(erector)** — same core sequence the schematic's `ERECT` step runs
(vacuum grip → side panels 90° → bottom majors → minors → tape bottom seam →
raise). The schematic's contribution is not the flap sequence (that is this
patent, and it is **Active**) but the *control discipline* around it: measured
per-lot restoring-torque calibration, near-crease in-loop correction, and
invariant-based squareness QC — none of which this patent claims.

### 1.2 US10532842 — Tape applicator with tape end fold and associated case sealing machine and method

| Field | Value |
|---|---|
| Number | US10532842 |
| Title | Tape applicator with tape end fold and associated case sealing machine and method |
| Inventors | Jeremy K. Zoss, Thomas E. Lyons Jr., Stephen L. Wiedmann |
| Assignee | Wexxar Packaging Inc. (Delta, BC, CA) |
| Filed / Granted | 2016-09-01 / 2020-01-14 |
| Status | **Active** (term ≈ 2036 + adjustments) |
| Source | https://patents.justia.com/patent/10532842 |

**What it teaches** — a tape head for a case sealer that *folds the free end of
the adhesive tape over onto itself*, creating a grippable non-adhesive pull
tab. The fold-over is triggered by movement of the knife; the tab lets an
operator (or robot) peel the tape open without touching adhesive.

**Relevance to the schematic:** prior art for the **Station 4 tape head**
detail — the schematic's tape head already assumes "wipes the tape around the
case edges." A build wanting the end-fold pull tab must license this patent or
design around the specific knife-triggered fold-over (e.g., leave a plain cut
end, or pre-apply a release liner). The pull-tab is an ergonomics feature, not
a requirement of the squareness/seam invariants.

---

## 2. Surrounding art (family & adjacent mechanisms)

| Patent / App. | Title | Assignee | Key dates | Status |
|---|---|---|---|---|
| US4553954 (cited in §1-family specs) | Automatic case erector and sealer (case puncturing/gripping pins) | — | 1980s era | **Expired**-era art; verify number/status on Google Patents |
| US8393375B2 | Edge folding tape applicator (tape folded edge-to-edge for grip) | Lamus Enterprises Inc. | granted 2013-03-12 | **Active** (verify) |
| US11897718B2 | Tape edge folding roller (folds tape edges before application) | Intertape Polymer Corp. | granted 2024-02-13 | **Active** |
| US10173858 | Adhesive tape dispenser for folded edge tape | TREA | granted 2018 | **Active** (verify) |
| US20240383219A1 | Box erecting device (robotic erector; picks, opens, folds minor then major flaps, seals) | Flex-Line Automation Inc. | published 2024-11-21 | **Pending** |

**Takeaway:** tape *edge folding* and *end folding* are crowded, mostly-active
art (Wexxar, Lamus, Intertape, TREA). Robotic *case erecting* is likewise
active (XPAK, Flex-Line). The folding-mechanics schematic does **not** need to
reproduce any specific tape-fold claim — its stated scope is control discipline
and invariant inspection, which sit outside these claims.

---

## 3. Standards (the line must be designed to these)

### 3.1 Machinery safety — harmonized under the Machinery Regulation

| Standard | Scope | Where it lands in the schematic |
|---|---|---|
| EN ISO 12100:2010 | Risk assessment and risk reduction (design principle) | Top-level hazard identification for all five stations (§1–§2) |
| EN ISO 13849-1:2015 | Safety-related parts of control systems, PL (a–e) | Safety logic: e-stop chain, light-curtain/STO wiring (§6.7), PL targets |
| EN IEC 62061:2021 | Functional safety of safety-related control systems, SIL | SIL allocation for the servo drives (safe torque off) and the reject gate |
| EN ISO 13850:2015 | Emergency stop — design principles | E-stop pushbuttons and reset semantics (§3 watchdogs) |
| EN 415-1:2014 | Safety of packaging machines — Part 1: terminology/classification | Classifies the case-erector/sealer so the right type-C standard applies |
| EN 415-10:2014 | Part 10: general requirements for safety of packaging machines | Station-level guarding, interlocks, hazard zones |
| EN 415-11:2014 | Part 11: efficiency and availability | OEE / availability targets for the §1.2 throughput and §8 estimates |
| EN 415-3 / -5 / -6 / -7 / -8 | FFS, wrapping, pallet wrapping, group/secondary, strapping machines | Neighboring type-C standards (reference only — this line is an erector/sealer) |

### 3.2 Control programming

| Standard | Scope | Where it lands |
|---|---|---|
| IEC 61131-3:2025 (ed. 4.0) | PLC programming languages: ST, LD, FBD, SFC; UTF-8 strings | The servo code in `packaging/plc_61131_3.py` is written in this ST dialect |

### 3.3 Box construction code

| Code | Scope | Where it lands |
|---|---|---|
| FEFCO-ESBO code | International 4-digit system for fibreboard case constructions, adopted by ICCA | The blank is a **FEFCO 0201** regular slotted container (RSC) — the code fixes which score lines are the fold seams for §2.1 |

---

## 4. Mapping — patents/standards → stations

| Patent / standard | Station / subsystem | Design consequence |
|---|---|---|
| US9718570B1 (Active) | 2 ERECT | Flap sequence is prior art → do NOT claim the sequence; claim the measured-calibration + near-crease control |
| US10532842 (Active) | 4 CLOSE+SEAL tape head | End-fold pull tab needs license or design-around; plain cut end is fine for the invariants |
| US8393375B2 / US11897718B2 / US10173858 | 4 tape head (edge fold) | Tape edge-folding is occupied art; not needed by this schematic |
| EN 415-1/-10/-11 | Line + stations | Terminology, general safety, OEE reporting |
| ISO 12100 + ISO 13849-1 + IEC 62061 + ISO 13850 | Control layer + safety | PL/SIL allocation, e-stop, STO wiring |
| IEC 61131-3:2025 | Control layer code | ST/SFC source dialect |
| FEFCO 0201 | 2 ERECTOR blank | Score-line positions from the code feed the fold targets |

---

## 5. Honest walls

- Patents and standards are **prior art / compliance references, not licenses
  and not proof that this schematic is novel or safe.** Both core patents are
  **Active**; a build must either license them or design around their claims.
- This document is a desk survey of public records (2026-08-12), not a legal
  opinion. Statuses change; confirm against USPTO Patent Center before
  commercial reliance.
- The schematic's genuine engineering content — per-lot restoring-torque
  calibration, near-crease in-loop correction, invariant-based inspection,
  majority-honesty quorum — sits in control logic and measurement, i.e.
  exactly the regions these patents do **not** claim. That is a freedom-to-
  operate *direction*, not a guarantee.

---

*Surveyed 2026-08-12. Sources: Google Patents, Justia, EU Consolidated TEXT
32023D1586 (machinery-safety harmonization), FEFCO/ICCA. No legal opinion is
expressed.*
