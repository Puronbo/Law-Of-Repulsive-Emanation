# Expired Patents Relevant to the Puno Calculus Inventions

**Purpose:** Freedom-to-operate / prior-art reference for the subject matter of the three provisional applications (PUNO-PPA-001..003). Lists U.S. patents whose exclusivity has ended (term expired or lapsed for non-payment of maintenance fees), so the disclosed methods are freely usable without a license.

**Survey date:** 2026-08-06
**Method:** Desk survey of public patent records (Google Patents legal-status flags, USPTO documents, published accounts). Each entry's status is flagged by its Google Patents legal-status label and key dates.

---

## How to read the status labels

| Label | Meaning | Effect |
|---|---|---|
| **Expired - Lifetime** | Patent term has run (20 years from effective filing, or 17 from grant for pre-1995 filings, whichever later). | Permanently public domain. No license required. |
| **Expired - Fee Related** | Lapsed because a maintenance fee (3.5 / 7.5 / 11.5 yr) was not paid. | No longer enforceable; may be reinstated on petition within limits (37 CFR 1.378). Treat as unencumbered but re-check status before commercial reliance. |
| **Ceased** | No longer in force (non-payment or abandonment in this jurisdiction). | Same as Expired - Fee Related. |

> **Honest limits:** Legal-status labels on Google Patents are an assumption, not a legal conclusion. The USPTO (Patent Center / maintenance-fee records) is the authoritative source. This is a desk survey, not a legal opinion.

---

## PPA-001 — Spatial-Indexed Population Flow (exact k-nearest-neighbor grid + tree)

| Patent | Title | Inventor / Assignee | Key dates | Status |
|---|---|---|---|---|
| US6700574B1 | Spatial data object indexing engine (grid/cluster-based spatial indexing) | Yiping Song / Siemens | filed 1999-10-29, granted 2004-03-02, ant. exp. 2019-10-29 | **Expired - Lifetime** |
| US6446068B1 | System and method of finding near neighbors in large metric space databases (near-neighbor link graph) | Chris Alan Kortge | filed 1999-11-15, granted 2002-09-03, ant. exp. 2019-11-15 | **Expired - Lifetime** |
| US6836225B2 | Fast search method for nearest neighbor vector quantization (bounded-search VQ) | Nam-Il Lee et al. / Samsung | filed 2003-09-26, granted 2004-12-28, ant. exp. 2023-09-26 | **Expired - Lifetime** |
| US6252605B1 | System and method for packing spatial data in an R-tree | Darin J. Beesley et al. / Garmin | filed 1997-08-01, granted 2001-06-26, ant. exp. 2017-08-01 | **Expired - Lifetime** |
| US8645380B2 | Optimized KD-tree for scalable search | Jingdong Wang et al. / Microsoft | filed 2010-11-05, granted 2014-02-04, adjusted exp. 2031-10-24 | **Expired - Fee Related** |
| US7619623B2 | Perfect multidimensional spatial hashing | Hugues Hoppe, Sylvain Lefebvre / Microsoft | filed 2006-04-17, granted 2009-11-17, adjusted exp. 2027-11-26 | **Expired - Fee Related** |

**Public-domain foundations (publications, not patents):**
- **k-d tree** — J. L. Bentley, *Multidimensional binary search trees used for associative searching*, CACM 18(9), 1975. Never patented; pure publication prior art.
- **R-tree** — A. Guttman, *R-trees: a dynamic index structure for spatial searching*, SIGMOD 1984. Never patented; the structure itself is publication prior art (R-tree *packing* was patented, US6252605 above — expired).

**Relevance:** The grid-index + ring-scan kNN method in PPA-001 is an *exact* variant of classic spatial-index / near-neighbor search. The foundational spatial-indexing art (grid indexing, R-trees, k-d trees, spatial hashing, bounded NN search) is free to practice. The patentable contribution remains the *proven-exact termination bound* (`d_k ≤ r·cell`) with bit-identical trajectories — not the existence of spatial indexing itself.

---

## PPA-002 — Crease-Density Neural-Network Diagnostics (pruning / early stopping / OOD / subgradient)

| Patent | Title | Inventor / Assignee | Key dates | Status |
|---|---|---|---|---|
| US5636326A | Method for operating an optimal weight pruning apparatus for designing artificial neural networks (Optimal Brain Surgeon / Hessian-inverse pruning) | David G. Stork, Babak Hassibi / Ricoh | priority 1992-09-04, filed 1995-07-07, granted 1997-06-03, ant. exp. 2012-09-04 | **Expired - Lifetime** |
| US3934231 | Adaptive Boolean Logic Element (adaptive logic networks; early adaptive-training art) | W. W. Armstrong / Dendronic | filed 1974-02-28, granted 1976-01-20, expired ~1991 (17-yr term) | **Expired - Lifetime** |

> **Note (verified 2026-08-06):** Optimal Brain Damage (LeCun, Denker & Solla, NIPS 1989) was **published but never patented** — it is free as publication prior art. Common guesses for an "OBD patent" (`US5046019A` = fuzzy data comparator, `US5274714A` = feature-vector neural recognition) were checked on Google Patents and are **not** OBD; both are irrelevant to this invention. OBD remains cited here as publication prior art alongside the expired OBS patent above.

**Relevance:** Weight/saliency-based pruning (including second-order Optimal Brain Surgeon) is fully public domain. PPA-002's crease-density pruning is an *input-activation-band* criterion, distinct from weight-saliency art. The early-stopping, OOD-detection, and fold-adjacent subgradient claims build on label-free signals; no directly-covering expired patents were found in this survey for those specific claims.

> **Note:** Modern neural-network training patents (e.g., dropout, US9406017B2 / Google) remain **active** — do not assume freedom to practice all training techniques; only the expired art above is unencumbered.

---

## PPA-003 — Decentralized Fragment Bank (hash-chained ledger, Ed25519, witness quorum)

| Patent | Title | Inventor / Assignee | Key dates | Status |
|---|---|---|---|---|
| US4309569A | Method of providing digital signatures (**Merkle hash-tree authentication**) | Ralph C. Merkle / Stanford | filed 1979-09-05, granted 1982-01-05, expired 1999-09-05 | **Expired - Lifetime** |
| US4200770A | Cryptographic apparatus and method (**Diffie-Hellman public-key exchange**) | Hellman, Diffie, Merkle / Stanford | filed 1977-09-06, granted 1980-04-29, expired 1997-09-06 | **Expired - Lifetime** |
| US4405829A | Cryptographic communications system and method (**RSA**) | Rivest, Shamir, Adleman / MIT | filed 1977-12-14, granted 1983-09-20, expired 2000-09-20 | **Expired - Lifetime** |
| US4759063A | Blind signature systems (privacy-protecting e-cash; Chaum) | David L. Chaum | filed 1983-08-22, granted 1988-07-19, expired 2005-07-19 | **Expired - Lifetime** |
| US5136646A | Digital document time-stamping with catenate certificate (**hash-chained timestamp ledger — "private blockchain" core**) | Haber, Stornetta / Bellcore | filed 1991-03-08, granted 1992-08-04, ant. exp. 2011-03-08 | **Expired - Lifetime** |
| US5136647A | Method for secure time-stamping of digital documents (multi-agency variant) | Haber, Stornetta / Bellcore | filed 1990-08-02, granted 1992-08-04, ant. exp. 2010-08-02 | **Ceased** |

**Ed25519 stack (used by PPA-003):** The Ed25519 authors state they have *not been notified of any patent claims* against Ed25519; reference implementations are public domain (CC0/0BSD). The historical elliptic-curve patents are all expired (per the authors' public chart):
- US4964164 batch RSA — expired 2007-10-16
- US4995082 Schnorr signatures — expired 2008-02-19
- US5159632 / US5271061 / US5463690 ECC arithmetic mod p — expired 2011-09-17
- US5299262 fixed-base exponentiation — expired 2012-08-13
- US5347581 batch verification — expired 2013-09-15
- US6141420 point compression — expired 2014-07-29
- US5999627 fixed-base exponentiation — expired 2015-06-06

**Relevance:** Every cryptographic primitive the fragment bank builds on — public-key encryption/signatures (RSA, Diffie-Hellman), Merkle hash trees for block hashing, hash-chained timestamp ledgers (Haber–Stornetta, the direct ancestor of the PPA-003 hash-chained ledger), and privacy-preserving e-cash (Chaum) — is in the public domain. The patentable contribution remains the *routing-defined ownership* (ownership IS routing), the *majority-honesty witness quorum with measured liveness curve*, and the *benchmarked anomaly layer* — not the primitives themselves.

**Routing-defined ownership — publication prior art (not patents):** The concept that an account's custodian is a *pure function of a hashed identifier* (deterministic routing with no registry) descends directly from distributed hash-table routing, which was published, never patented:
- **Consistent hashing** — Karger et al., *Consistent hashing and random trees*, STOC 1997.
- **Chord** — Stoica et al., *Chord: a scalable peer-to-peer lookup service*, SIGCOMM 2001.
- **Kademlia** — Maymounkov & Mazières, *Kademlia: a peer-to-peer information system based on the XOR metric*, IPTPS 2002.
- **Pastry** — Rowstron & Druschel, SIGOPS 2001.
A search of Google Patents for expired consistent-hashing/DHT patents returned only **active** or non-expired family members (e.g., `US11150953B2` consistent-hash, `US9378106B1` hash-based replication, `US8725862B1` query-hashing) — none expired and none a direct antecedent. The routing-defined-ownership claim therefore stands on the publication foundation above plus the invention's specific embedding and re-resolution rule, not on any expired patent.

---

## Summary for FTO

| Area | Foundational art | Status | Your contribution (distinct) |
|---|---|---|---|
| PPA-001 | Grid/space indexing, R-tree, k-d tree, spatial hashing, bounded NN search | **Free** (expired/publication) | Proven-exact Chebyshev-ring termination + bit-identical trajectory guarantee |
| PPA-002 | Weight-saliency and second-order pruning (OBS), adaptive networks | **Free** (expired) | Crease-density (near-fold pre-activation) criteria; label-free stop/OOD signal |
| PPA-003 | Merkle trees, RSA/DH, Chaum e-cash, Haber–Stornetta hash-chained timestamps, Ed25519 | **Free** (expired/public-domain design) | Routing-defined ownership; majority-honesty quorum; measured anomaly layer |

---

*This document records a public-database survey performed 2026-08-06. Patent status is subject to change (fee-related lapses may be reinstated); confirm against the USPTO before commercial reliance. No legal opinion is expressed.*
