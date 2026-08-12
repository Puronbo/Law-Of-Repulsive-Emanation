"""
Regression suite pinning the solvable-theorem verdict artifacts (2026-08-08).

Each test loads a persisted verdict JSON from data/ and checks the headline
number so none of the resolved claims can silently drift:
  - continuum-limit drift converges to zero at first order
  - spectral C1/C3/C4 verdicts (100 modes, 120x120 grid)
  - Kawasaki 0.4866 reproduced and attributed to sampling scatter
  - PGT growth-form refutation at finite L
  - golden-ratio closure derived exactly (s(theta*)/s(TH) = 1/phi^2)
  - prime-time PAPER §8.4: uniform conservation; spectrum transient; recurrence unmeasurable
  - T-symmetry reversal error as a dt-dependent numerical bound
  - Bekenstein shift settled at n=100: significant raw, erased by index-matching
  - Wheeler-DeWitt constraint selects nothing (empty or C0-law relabeled)
  - fold-and-cut is not a unitary gate (non-injective, not norm-preserving)
  - Kawasaki is not a CTC/Novikov constraint (antecedent false)
  - C7 bridge extends to all primes trivially (no 2^n-k-special resonance)
   - Selberg paradigm not a concrete instance (Poisson, no zeros, no trace peaks)
   - C2 golden fold: retrace chain is not a phi/phi^2 ladder (1/4 rungs)
   - hierarchical C0 flow: SUPPORTED (NC parity with flat flow, router gain, 6 not 30 comps)
   - flow-guided active learning: margin-AL reaches targets with fewer labels than random; raw force-cancellation score is not the winner
   - balance survey: 50/50 is best shock absorber but NOT the layout optimum (PARTIAL)
   - balance scale (T54): scaling is a real confound (A* ~ n^1.086) but NOT the problem; dimension-independent shell
   - balance continual (T50): adaptive mu=0.5→0 schedule wins both axes; fixed balanced P5 is harmful
   - polysphere extensions: learned truths do not reproduce routing; S^2 repulsion does not preserve clustering (NOT SUPPORTED)
   - flow incremental: reflow buys separation (min_d) but not routing; random-add matches or beats (MIXED)
   - flow hier-incremental: hierarchical + incremental growth preserves old-class routing (no forgetting); hier beats flat (SUPPORTED)
   - polysphere use cases: classifier/anomaly/generator/continual claims hold at batch level; per-point weak; separation not bit-reproducible
   - polysphere routing: batch routing exact (identity confusion, chance 0.167); silhouette 0.943; per-point weak
   - golden survey: phi EXACT in cusp metric; golden rotation maxes min gap; static C0 packing has no golden structure; gap-filling does not lock to golden angle
   - fib stream (T52): Fibonacci-sized continual stream is steady; AD_phi (absorb on large terms) beats P0 on both axes in all 3 seeds; golden insertion washes out; no golden scaling signature
   - hamiltonian routing: C0 flow separates centroids (routing 0.420->0.765, nc reaches oracle 0.909); min pair dist barely moves; flow is not the ceiling
   - metric comparison: Poincare vs cusp geodesic from a 'stable' start blows up numerically in BOTH (Poincare NaN, cusp ~2e13; C0 broken, T-sym fails) - REFUTED at these settings
   - c0 crossing tsym: T-sym holds (err 0.066-0.226) but NO trajectory actually crossed the origin (closest approach = start dist) - PASS-with-caveat, crossing regime never exercised
   - c0 cusp flow: cusp-metric C0 geodesic at dt=0.005/5000 steps blows up (Poincare NaN, cusp escapes to ~2.7e23, drift 2.68e45, T-sym err 2.8e9) - REFUTED/unverifiable at settings
   - t39 cusp flow: cusp isometry w=log(q) verified EXACTLY (energy CV 3e-15, step ratio=phi exactly, w-plane R2=1.0 slope pi/(2 log phi), T-sym err 0) - SUPPORTED (deterministic)
   - van iterson T48a: NO golden-angle locking in ANY rule (discrete bisection, min-potential, min-dist, center+push-out; divergence 170-200 deg, r~n^0.4-0.5) - SUPPORTED negative, locking is an insertion-constraint special value
   - reverse pair gaps T57: NOT a reversal pair (reverse(10262)=26201 != 26102); 80-multiple + 11-sums hold but are plain arithmetic - REFUTED headline, census is ordinary
   - fibonacci spiral on disk: neither projection turns at golden angle (42.14 / 29.23 deg vs 137.51) and pseudo-energy not conserved (drift 1.00 / 11.81) - REFUTED, golden angle is a cusp-metric property
   - prime count from scratch T62: Lucy_Hedgehog pi exact at all chain points (pi(943901200001)=35575526191), endpoint prime, next gap 8 - SUPPORTED with corrections: 'gap 1 below' is wrong (measured 24), window max gap 176 exceeds own 40-100 note
   - fibonacci squares on disk: 90-deg turning is a square-construction artifact; pseudo-energy NOT conserved (drift 0.96, decay -0.357/step), escapes disk (r 1.117), T-sym fails (0.99 vs C0 6e-09) - REFUTED frictionless claim
   - rotation test T61: rotation preserves neighbor structure EXACTLY (overlap 1.0, sim corr 1.0, coords change 0.745); abs() drops overlap 1.0->0.426 but that is 6.5x chance, so 'collapse toward chance' overstated - SUPPORTED J1/J2 with J3 correction
   - clock test T59: calendar features nail the law at e0 (1.0000) but break at e0+15 (0.4167, BELOW chance -> anti-correlation), intrinsic mod-2/3/5/7 features survive both (1.0000) - SUPPORTED, convention carries then breaks
   - spring fold T58: mirror-fold area = 2*a^2*TH^3/6 EXACT, self-crosses at TH-pi; retrace fold closes EXACTLY to C0 (closure 0.00e+00, crease pi); golden fold ratio = phi EXACT but does NOT close to C0 (error 12.3); overcoil tucks end under start - SUPPORTED (by construction, deterministic)
   - eikonal fold T63: upwind viscosity solution of |r'|=a with C0 at both ends converges to the exact tent (err 3.3e-13); cut locus EXACT (0.00e+00); crease 0.0350*pi vs analytic 0.0318*pi (finite-diff approx); mirror area 2*a^2*TH^3/6 EXACT, retrace net area ~0 - SUPPORTED (deterministic; fold-as-integral semantics interpretive)
   - retrace boundary T64: equation + two pins admits infinitely many weak solutions (zig-zags all pass |r'|=a, r(0)=r(2TH)=0); viscosity selects the tent (all zig-zags fail at down-up corner); upwind from zig-zag converges to tent (err 5e-13); cut locus EXACT; reflection conserves |r'| to 3.6e-13 - SUPPORTED, retrace derived not assumed
   - fold optimizer T60: Hamiltonian spring conserves (drift 3.9e-3 bounded, area ratio 0.9921) and recurs to start (Poincare, min dist 3.3e-5); damped spring collapses (energy 0.00e+00 above min, area ratio ~0) and locks at x=+1 EXACT (stays 2000 steps) - SUPPORTED; 'cannot escape' is topological (shown by staying, not proved), mirror-fold=dissipation interpretive
   - t65 four-pack: P1 REFUTED (tau=1.4272 identical across all curiosity_drive, corr nan - knob has no effect); P2 REFUTED (ascent err 1.79-1.82, does not recover seed); P3 PARTIAL (2D proj MI 0.034 vs null 0.009 retains signal, but single coord already = 1.0, holography trivial); P4 REFUTED (converged fraction 0.00, max dist from final 0.45) - MIXED, mostly REFUTED
   - phi scheduler T53: FIB batching most robust on disk layouts (stream-old 0.912 best, final-old 0.910 at ~2.25 buffer); FIB+ABS buys final_all (+0.013) at old-routing cost (-0.063); P5 fixed mu=0.5 never usable (0.872); on MNIST scheduling NOT needed (NAIVE 0.953 > FIB 0.907 > FIB+ABS 0.887) - SUPPORTED with scope caveat (geometry-regime tool)
   - flow_regularized: flow regularizer at lambda=0.007 lifts routing 0.900->0.930 (+0.030) with test_acc 0.905 and sep 1.59x preserved, but the sweep is NON-MONOTONIC (0.003:+0.01, 0.005:-0.02, 0.007:+0.03, 0.01:-0.07, 0.015:+0.00) - SUPPORTED with narrow-window caveat, larger lambda clearly hurts routing
   - flow_hier_reg T48b: flow-REG does NOT stabilize - drift 6.616 (rel 0.686) vs baseline 6.549 (rel 0.647), forgetting -0.034 vs -0.029; flat routing worse (all 0.805 vs 0.885, old 0.873 vs 0.973); only hier routing better (all 0.790 vs 0.765, old 0.800 vs 0.760) - NOT SUPPORTED for stability headline, weak hier benefit only
   - flow_hier_reg_scaled T55b: n-scaling stage-2 reg per T54 A* law does NOT help materially - drift 6.5048 (rel 0.644) FIXED vs NSCAL 6.4636 (rel 0.640) and LIN 6.4573 (rel 0.640), a <=0.7% relative drift gain; ALL other metrics identical to 3 dp (acc 0.897/0.921, forget -0.031, route 0.895/0.933, hier 0.755/0.747); LIN nominally lowest - NOT SUPPORTED for a material effect
   - balance_auto T51: autonomous burst-detector regime switch does NOT deliver the claimed benefit - detector fires only on the explosive event, but AD ~= P0 on routing (MNIST old 0.990 vs 1.000, all 0.975 vs 0.985; synthetic burst 0.887 vs 0.873 old) and AD displacement slightly higher (1.816 vs 1.828); P5 constant-mu=0.5 decisively worse; on real MNIST embeddings reflow policy is nearly irrelevant (all >= 0.94, P0 best) - NOT SUPPORTED for the autonomous benefit (T50 absorb = one-shot recovery tool for a clean shell, not a stream policy)
   - self_balancing T55a: self-balancing router (fib batching + n-scaled absorb A=A*(n) + coherence gate) SUPPORTED in the geometry regime - the gate FIRES in a trapped crowded core: COH skips the absorb and lands exactly on P0 (old 0.900 ~ 0.900, all 0.860 = 0.860, disp 0.513 ~ 0.513) while ABS/ABS-SC pay the penalty (old 0.890, all 0.820-0.830); on the clean fib stream the all-routing gain survives (COH final_all 0.850 vs P0 0.770; multi-seed banner 0.880 vs 0.820) but seed-42 COH final_old 0.810 < ABS-SC 0.930 (banner tie 0.870/0.870 holds on average only); Part 4 MNIST adds NOTHING (COH final_all 0.873 < FIB 0.940); coherence is a shell-thickness signal, not a general crowding detector
   - polysphere_mnist: PolysphereRouter generalizes to REAL MNIST embeddings - mixed-batch routing 0.890 vs chance 0.100; anomaly gap 0.663 (in-dist 0.877 vs OOD 0.214); hierarchical end-to-end 0.753 vs combined chance ~0.111 (branching 10 -> 4); active learning flags unknowns 60% and routes 10/10 = 1.000 after faces added - SUPPORTED (embeddings are the MLP's own 2D bottleneck, single seed, hier below flat 0.890, threshold-dependent)
   - polysphere_nnflow_viz: three-extension probe - (1) learnable NN truths SUPPORTED: routing 0.880 (176/200) vs chance 0.100 on MLP embeddings (test_acc 0.885); (2) S^2 Hamiltonian flow NOT SUPPORTED: silhouette ~0.0 (intra ~= inter, no separation), only 3-4/6 faces self-route at low conf 0.24-0.56, repulsion destroys centroid structure (run-to-run variance: sil -0.016..0.022, 3-4 self-routed, part 2 draw not fully rng-seeded - verdict robust); (3) viz routing distribution tracks true per-class fractions within ~1-3 pts - PARTIAL
   - decentral_net T55c: fully local net (private home trap + k-NN repulsion + per-neuron steps, NO global mean/max/controller) SUPPORTED - decentralization ~free or better on old-routing (banner multi-seed: ABS-SC final_old 0.913 vs centralized 0.870; final_all 0.843 vs 0.853); shell EMERGES from local rules but needs the always-on home tether (without it collapses to rim 0.57 all-route -> 0.85 at mu0=0.12); self-heals with no repair unit (50% loss: spacing spread 0.16->0.11, regrown routing >= pre-damage 0.917 vs 0.877); MNIST part4 no collapse, ABS-SC final-all 0.813 > FIB 0.647; caveats: spacing gate never fired on clean stream (GATE ~ ABS-SC), k=4 worse than k=8, part4 single-seed
   - decentral_net_mnist T55d: no-dependency DecentralNet on real 64D MNIST embeddings SUPPORTED - local-settle routes at 0.810 vs nearest-centroid baseline 0.817 (within ~1 pt, no central controller); after killing 3/10 neurons survivors keep routing (0.834) and LOCAL heal alone restores spacing 0.562 -> 0.854 with routing preserved (0.822); regrow from fresh homes restores full 10-class net at 0.767 (~5 pts below grown 0.810); caveats: embeddings are the MLP's own 64D layer, single seed 42/4 epochs/disk radius 0.35
   - decentral_net_continual T55e: class-incremental LOCAL reflow on real 64D MNIST NOT SUPPORTED for the routing benefit - ADD old 0.805 vs raw-centroid CONTROL 0.863 (delta -0.057), all 0.647 vs 0.671 (homes ARE the data centroids, reflow cannot help); MIX (no reflow) collapses as the gauge freedom predicts - old 0.061/all 0.305, never mix frames; Part 2 tether NOT dimension-independent - mu0=0.12 2D-tuned over-drifts in 64D (0.49), mu0>=1 cuts drift to 0.11-0.21 but never beats CONTROL (best all 0.812 vs 0.817)
   - decentral_net_ceiling T55h: all-pairs kNN flow ceiling measured ~2*10^4 on this 31.7 GB box (dim=2, k=8) SUPPORTED - ms/step n^1.76 up to 5000 then exponent ~2.06 (D leaves cache); 66/1230/25422 ms/step at n=1k/5k/20k; peak WS 22.6 GB at n=20k vs D=3.2 GB (kNN sort temporaries blow past the estimate); n=40k would peak ~90 GB, not run - scaling beyond ~2*10^4 needs O(1) spatial search (T67)
   - decentral_net_t67: O(1)-per-neuron spatial search (uniform grid <=3D, scipy cKDTree >=4D) SUPPORTED - indexed flow BIT-IDENTICAL to exact all-pairs (grid 2D n=2000, tree 64D n=500) with spacing/predict equal and grid kNN == brute force on 3 seeds x 1D/2D/3D; 2D scaling exponent 1.11 (indexed) vs 1.92 (exact) - flow is now ~linear, and n=100k flows at 10.35 s/step where the all-pairs D would need 160 GB (10k real top-1M domains x 128D at 4.12 s/step, 102 GB) - the n^2 wall is gone for low-dim flow
   - decentral_net_live: the T55f live daemon's structural claims pinned by a bounded run - V1 population never exceeds CAP (30) through arrivals + damage + pruning (bounded O(CAP^2) cost); V2 after each random neuron death the local k-NN re-spread heals the survivors back into the healthy spacing band with NO repair unit (post-damage spacing within 0.5-2.0x of pre - removing a neuron legitimately enlarges mean k-NN distance, no clump, no rim blow-up; recovery ratio ~1.4); V3 the self-consistent routing probe stays 1.00 accurate through 3000-tick churn; V4 a checkpoint saved at tick 1500 and reloaded reproduces the uninterrupted trajectory bit-for-bit (positions identical, counters born/pruned/killed match, RNG stream carries on - the cycle is continuous with no damage) - all SUPPORTED on seeds 42/11/7, numpy-only DecentralNet, bounded ring memory, all as MECHANISM claims about the daemon design
    - bazaar_hybrid: the best-possible 4chan+reddit design (anonymity+bump-order honesty x reddit memory+curation, minus both status economies and central algorithms) verified as 6 structural claims on the repo's OWN machinery - C1 reason-tagged downvotes raise the brigade size to hide a good post 2.5x (reddit S50=8 free downvotes vs hybrid S50=20 pending-quorum-review; even then only HIDDEN, removal needs the quorum); C2 karma-free + tag-to-remove drops top-K spam frac 0.75->0.00 (reddit bot collusion saturates); C3 emergent DecentralNet mesh feed routes minority users 1.00 of their own community vs 0.30 on the global hot feed (overlap 1.0 -> local explicit clustering); C4 content-addressed ledger archive survives 50% node loss with retrieval 1.00 and tamper-evidence (verify() fails at seq 3); C5 9-guardian quorum collapses wrong-removal 0.20 -> 0.0031 at corruption p=0.20; C6 verified-vote-only membership (anonymity for cheap votes, EARNED mesh standing for the removal path) raises the brigade to suspend a good post 32x (S50 20 -> 640, sockpuppet standing 0.05 contributes ~nothing) and collapses quorum wrong-removal to 1e-08 (corrupt identity must ALSO hold guardian standing, 10% of population - a sockpuppet factory cannot mint guardians) at the honest cost of a removal-vote privacy leak - all SUPPORTED as MECHANISM claims (agent-based, no real users)
    - learn_creativity_test (T74): a test ascertaining LEARNED and CREATIVITY in a learning environment, one rubric (recognition/transfer for learned; novelty x appropriateness for creativity) re-used by a human protocol - L1 held-out probe accuracy climbs from near-chance 0.125 to >=0.90 as exemplar exposure grows 1..40/concept (a sparse stored-memory k-NN neighborhood is dominated by other concepts, a full one by the true concept); L2 first-taught concepts keep >=0.92 after every later concept is added (no forgetting under additive memory); C1 a measurable share of mid-size near-miss variations are simultaneously NOVEL and VALID (>=24% yield of never-presented new-but-right items); C2 random far nulls are ~100% novel but 0% creative (novelty alone is not creativity); C3 creative yield is interior-peaked over mutation size (too-close valid-but-not-novel, too-far novel-but-not-valid) - all SUPPORTED on seeds 42/11/7 as MECHANISM claims (stored-memory k-NN router over gaussian exemplars in a synthetic concept space)
    - learn_curve_scale (T75): the T74 acquisition curve is a density effect, not an artifact of its single operating point - S1 the sparse floor is chance: at one exemplar/concept held-out accuracy tracks 1/C and strictly decreases with curriculum size (0.50 -> 0.25 -> 0.125 -> ~0.07 for C = 2,4,8,16; a bigger curriculum is a denser confusion field); S2 the acquisition curve exists at every scale: the full-exposure ceiling holds >=0.90 for every C in {2,4,8}, so the dynamic range (ceiling - floor) grows with C (0.50 at C=2 -> 0.82 at C=8); S3 capacity saturation: beyond the well-separated regime the ceiling collapses once adjacent home separation reaches a few exemplar-sigma (0.94 at C=8 -> 0.61 -> 0.42 -> 0.30 at C=16,24,32), locating a real memory capacity C* ~= pi*HOME_R/(2*SIGMA) ~= 8 - all SUPPORTED on seeds 42/11/7 as MECHANISM claims, and the collapse tracks separation/sigma, not a magic C (SIGMA=0.03 holds 0.89 at C=16; SIGMA=0.10 collapses to 0.59 already at C=8)
    - human_trial_pilot: the T74 human protocol made concrete and validated - a trial package (teaching set, held-out probes, three-effort creativity prompts, pre-registered spacing thresholds and bars in data/human_trial_package.json) plus score_participant(), the SAME code that grades the machine, grading a human's recorded answers on the engine's bars; the pilot with simulated archetypes proves the instrument works: P1 a perfect participant attains every engine bar (L1 ceiling 1.0, L2 1.0, C1 mid creative ~0.24-0.36 >= 0.15, C2/C3 hold); P2 a random non-learner fails L1 (ceiling ~= 1/C) and C1 (yield ~= 0) - the bars are not passable by chance; P3 the joint criterion binds on both sides (trivial items valid-but-not-novel, wild items novel-but-not-valid, mid the only positive yield; a pure copycat scores exactly 0); P4 random far items grade ~100% novel but ~0% creative under the pre-registered thresholds - all SUPPORTED on seeds 42/11/7 as MECHANISM claims (simulated participants validate the instrument, not human behavior; a real trial hands the package to a human and scores with the same code)

Run:  python -m pytest tests/test_solvable_theorems.py -q
"""

import math
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, 'data', name)) as fp:
        return json.load(fp)


def test_continuum_limit_first_order_convergence():
    d = load('continuum_limit_drift.json')
    assert d['verdict'].startswith('PASS')
    fit = d['convergence_fit']
    assert fit['order'] >= 0.8
    assert fit['r2'] >= 0.98
    assert d['interior_trajectory_fit']['order'] >= 0.8
    assert d['interior_clean'] is True


def test_spectral_extended_verdicts():
    d = load('spectral_extended_data.json')
    v = d['verdict']
    assert v['c3a'] == 'NOT SUPPORTED'
    assert v['c3b'].startswith('SUPPORTED')
    assert v['c4'].startswith('MEASURED')
    assert 'poisson' in v['c4']
    # the dozenal hit: r_12 vs ln(12), 0.53%
    c1 = {row['k']: row for row in d['c1']}
    assert math.isclose(c1[12]['r_mode'], math.log(12), rel_tol=0.02)
    assert d['c3b']['delta'] < 0.05
    assert d['c4']['r_mean'] < 0.45  # toward Poisson (0.386), away from GOE
    assert d['selberg_zeros']['min_dist'] > 5.0


def test_kawasaki_null_reproduced_and_attributed():
    d = load('kawasaki_null_data.json')
    assert d['verdict'].startswith('RESOLVED')
    m = d['measured']
    assert math.isclose(m['deviation'], 0.4866, abs_tol=1e-3)
    assert math.isclose(m['fraction_eps'], 0.724, abs_tol=1e-2)
    # the uniform-scatter control scatters MORE (0.8349), i.e. the 0.4866
    # is line-structure, not flat-foldability
    assert d['random_control']['deviation'] > m['deviation']
    assert d['exact_2line_vertices']['fraction_eps_0.5'] < 0.15  # 9.5%


def test_pgt_finite_l_refuted():
    d = load('pgt_finite_l_data.json')
    assert d['verdict'].startswith('finite-L RESULT')
    assert 'REFUTED' in d['verdict']
    assert d['growth_form']['slope_logN_vs_L'] < 0.1  # 0.002 vs 1.0
    assert 0.5 < d['sieve_ordering']['pearson_log_log'] < 0.9  # partial: 0.696


def test_fold_golden_closure_derived():
    d = load('fold_golden_closure_data.json')
    assert d['verdict'].startswith('DERIVED')
    assert math.isclose(d['measured'], 0.6137690167, abs_tol=1e-6)
    assert math.isclose(d['derived_at_TH_20'], d['measured'], rel_tol=1e-9)
    assert d['delta'] == 0.0
    assert math.isclose(d['asymptotic_limit']['1/phi'],
                        1.0 / (0.5 * (1 + math.sqrt(5))), rel_tol=1e-6)


def test_prime_time_uniform_and_unmeasurable():
    d = load('prime_time_data.json')
    v = d['verdict']
    assert 'uniform energy conservation' in v
    # drift at prime-indexed steps equals drift at all steps (nothing prime-special)
    assert math.isclose(d['c1']['drift_ratio_prime_vs_all'], 1.0, abs_tol=0.05)
    assert d['c1']['uniform'] is True
    # the claimed N=50 mu=0.065 is not reproduced, and the spectrum diverges by N~214
    assert d['c2']['mu_50'] < 0.05
    assert d['c2']['mu_N'] > 0.5
    # no near-recurrences before the flow escapes the disk
    assert d['c3']['n_recurrences'] == 0
    assert 'UNMEASURABLE' in v


def test_time_reversal_convergence_bound():
    d = load('time_reversal_convergence_data.json')
    # error superconverges to far below the PAPER's 0.003 at finer dt
    rows = {r['dt']: r for r in d['rows']}
    assert rows[0.0005]['ts_error'] < 0.01          # 8.9e-3
    assert rows[0.00025]['ts_error'] < 1e-3         # 7.2e-5
    assert rows[0.000125]['ts_error'] < 1e-4        # 5.9e-7
    assert d['superconvergent'] is True
    assert d['verdict'].startswith('the coarsest dt escapes')


def test_bekenstein_rerun_settled():
    d = load('bekenstein_rerun_data.json')
    fc, fm = d['frictionless_control'], d['frictionless_matched']
    # raw frictionless shift IS significant at n=100 (the old n=30 was underpowered)
    assert fc['n_trajectories'] >= 60
    assert fc['p_value_paired_t'] < 0.01
    assert fc['mean_diff'] > 0
    # but the index-matched control on the same trajectories erases it
    assert fm['p_value_paired_t'] > 0.05
    assert fm['bootstrap_95_ci'][0] < 0 < fm['bootstrap_95_ci'][1]
    assert abs(fm['mean_diff']) < 0.1 * fc['mean_diff']
    assert 'NOT REPRODUCED' in d['verdict']
    assert 'artifact' in d['verdict']


def test_wheeler_dewitt_selects_nothing():
    d = load('wheeler_dewitt_selection_data.json')
    v = d['verdict']
    assert 'EMPTY' in v or 'selects nothing' in v
    # unshifted |H|<eps is empty on every conservative trajectory at eps<=2
    for r in d['results']:
        if r['friction'] == 0.0:
            for row in r['rows']:
                if row['epsilon'] <= 2.0:
                    assert row['unshifted_fraction'] == 0.0
    # the PUM's 86.8% figure is not reproduced by the current filters
    assert d['scan_for_86.8pct']['reproduced'] is False


def test_fold_not_a_unitary_gate():
    d = load('fold_unitary_data.json')
    assert d['verdict'].startswith('NOT a unitary gate')
    c = d['checks']
    assert c['n_preimages'] == 2
    assert c['angle_collisions'] > 0
    assert abs(c['L_ratio'] - 0.5) < 0.05  # fold ~ half the development length


def test_kawasaki_not_a_ctc_constraint():
    d = load('kawasaki_ctc_data.json')
    assert d['verdict'].startswith('NOT a CTC constraint')
    assert d['satisfaction_at_null_rate'] is True
    assert d['input']['kawasaki_exact_2line_fraction_eps_0_5'] < 0.15
    # admission collapses with loop size exactly as the null does
    for V in ('4', '8', '16'):
        assert d['loop_sizes'][V]['binding'] is False


def test_bridge_extends_to_all_primes_trivially():
    d = load('bridge_extension_data.json')
    # census's own 6/186 resonance is NOT significant vs uniform null
    assert d['census']['binom_p_gt_uniform'] > 0.05
    # extended bridge: near-integer rate barely above the 2% uniform null
    ext = d['extended']
    assert 0.02 <= ext['near_int_rate'] <= 0.03
    # random-integer control reproduces most of the elevation
    ctrl = d['random_integer_control']['near_int_rate']
    assert ctrl >= 0.022
    # prime-specific residue is real but tiny (< 0.5pp)
    pv = d['prime_vs_random']
    assert pv['prime_specific'] is True
    assert pv['elevation'] < 0.005
    assert 'trivially extends' in d['verdict'] or 'trivial' in d['verdict']


def test_selberg_paradigm_not_a_concrete_instance():
    d = load('selberg_paradigm_data.json')
    assert d['a_level_stats']['verdict'].startswith('POISSON')
    # GOE excluded at >5 sigma at 100 modes
    assert d['a_level_stats']['z_goe'] < -5.0
    # no Riemann-zero correspondence
    assert d['b_zeros']['within_0.5'] == 0
    assert d['b_zeros']['min_dist'] > 5.0
    # Mersenne lengths produce no trace-formula peaks
    assert d['c_form_factor']['n_strong_vs_null_95'] == 0
    assert d['c_form_factor']['null_mean_pctile'] < 50.0
    assert d['verdict'].startswith('SELBERG PARADIGM NOT SUPPORTED')


def test_golden_fold_not_a_chain_law():
    d = load('fold_ladder_phi_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    # only the celebrated upper rung 1,914,467/730,421 is golden
    assert d['adjacent_hits'] == 1
    assert d['adjacent_n'] == 4
    # the single hit is at the 0.115% coincidence scale, not a ladder
    upper = d['adjacent_rungs'][1]
    assert upper['hi'] == 1914467 and upper['lo'] == 730421
    assert upper['dev_nearest_target_pct'] < 0.5
    # all three other rungs miss by far more than 1%
    for row in (d['adjacent_rungs'][0], d['adjacent_rungs'][2],
                d['adjacent_rungs'][3]):
        assert row['hit_within_1pct'] is False
        assert row['dev_nearest_target_pct'] > 1.0
    # an isolated hit is not rare under the magnitude-matched null
    assert d['null']['p_any_golden_rung'] < 0.05
    # the giant is the chain top: no defined rung above it
    assert d['next_fold_above_giant']['hit_within_1pct'] is False


def test_hierarchical_c0_flow_supported():
    d = load('flow_hierarchical_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    r = d['results']
    # hierarchical routing beats flat C0 flow routing
    assert r['hierarchical']['router'] > r['flat_c0_flow']['router']
    # and costs far fewer comparisons per level than flat (30)
    assert r['comparisons_per_level'] == 6
    assert r['comparisons_per_level'] < r['flat_comparisons'] / 4
    # nearest-centroid accuracy stays high (~parity with flat)
    assert r['hierarchical']['nc'] > 0.95
    assert abs(r['hierarchical']['nc'] - r['flat_c0_flow']['nc']) < 0.05


def test_flow_active_learning_margin_beats_random():
    d = load('flow_active_learning_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    ltt = d['labels_to_target']
    # margin reaches 0.80 and 0.82 with strictly fewer labels than random
    for t in ('0.8', '0.82'):
        assert ltt[t]['margin'] is not None
        assert ltt[t]['random'] is not None
        assert ltt[t]['margin'] < ltt[t]['random']
    # honest wall is pinned too: raw force-cancellation is NOT the label-efficiency winner
    ltt078 = ltt['0.78']
    assert ltt078['force'] is None or ltt078['force'] > ltt078['margin']
    fin = d['final_accuracy']
    assert fin['margin_al'] >= fin['random'] - 0.02


def test_balance_survey_partial_not_layout_optimum():
    d = load('balance_survey_data.json')
    assert d['verdict'].startswith('PARTIAL')
    # the layout optima are NOT at mu=0.5
    assert d['part1']['mu0_5_is_peak'] is False
    assert d['part1']['best_packing_mu'] != 0.5
    assert d['part1']['best_uniformity_mu'] != 0.5
    # the balanced tier is the shock absorber; the tight core shatters
    t = d['part2']['tiers']
    assert t['n3_mu0_5'] == 'n3 equilibrate'
    assert t['n2_mu0_9'] == 'n1 shatter'
    # pure repulsion routes best
    assert d['part3']['pure_repulsion_routes_best'] is True


def test_balance_scale_confound_not_cause():
    d = load('balance_scale_data.json')
    assert d['verdict'].startswith('REFUTED')
    # the A*(n) fit is a real super-linear scaling
    assert d['part2']['beta'] > 1.0
    # A* is strictly increasing in n (trap must scale UP)
    a_star = d['part2']['A_star']
    keys = ['5', '10', '20', '40', '80']
    for i in range(len(keys) - 1):
        assert a_star[keys[i + 1]] > a_star[keys[i]]
    # fixed-A absorb does NOT underperform the scaled one (confound, not cause)
    assert d['part3_final']['FIB+ABS']['final_old'] >= 0.85
    # dimension-independence claim is persisted
    assert d['part4_dimension_independent'] is True


def test_balance_continual_adaptive_wins():
    d = load('balance_continual_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # adaptive beats pure-expansion on old-class routing (flat, seed 42)
    p1 = d['part1_flat_seed42']
    assert p1['AD']['old_route'] > p1['P0']['old_route']
    # fixed balanced P5 is harmful: lower all_route than AD
    assert p1['AD']['all_route'] > p1['P5']['all_route']
    # same in the hierarchical part
    p2 = d['part2_hier_seed42']
    assert p2['AD']['old_hier'] > p2['P0']['old_hier']
    assert p2['AD']['all_hier'] > p2['P5']['all_hier']
    # AD wins both axes across all three seeds
    for i in range(3):
        assert d['multi_seed_part1_old_route']['AD'][i] > d['multi_seed_part1_old_route']['P0'][i]
        assert d['multi_seed_part2_old_hier']['AD'][i] > d['multi_seed_part2_old_hier']['P0'][i]


def test_polysphere_extensions_not_supported():
    d = load('polysphere_extensions_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    # learned truths do not reproduce routing accuracy
    e2 = d['extension2_learned_truths']
    assert e2['learned_truth_acc'] < 0.6
    assert e2['true_truth_acc'] > 0.99
    # S^2 repulsion destroys the clustering that was present
    e4 = d['extension4_sphere']
    assert e4['initial_sep_ratio'] > 10.0
    assert e4['repulsion_only_ratio'] < 1.5
    assert e4['with_attraction_ratio'] < 2.0
    # the pieces that DO hold stay pinned
    assert d['extension3_scaling']['batch_acc_by_faces']['100'] > 0.9
    assert d['extension3_scaling']['anomaly_gap_by_faces']['6'] > 0.5


def test_flow_incremental_mixed_not_uniform():
    d = load('flow_incremental_data.json')
    assert d['verdict'].startswith('MIXED')
    rows = d['stage_rows']
    # reflow always keeps min_d strictly higher than random-add (separation)
    for k in rows:
        assert rows[k]['reflow']['min_d'] > rows[k]['random_add']['min_d']
    # but random-add matches or beats reflow on all-class routing at least once
    assert any(rows[k]['random_add']['all_acc'] >= rows[k]['reflow']['all_acc']
               for k in rows)
    # and reflow pays a displacement cost that random-add does not
    assert any(rows[k]['reflow']['disp_old'] > 0.1 for k in rows)


def test_flow_hier_incremental_no_forgetting_supported():
    d = load('flow_hier_incremental_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    s = d['summary']
    # no forgetting: old-class routing strictly above all-class routing
    assert s['old_hier_avg'] > s['all_hier_avg']
    # hierarchical routing beats the flat router
    assert s['all_hier_avg'] > s['flat_avg']
    # separation is bounded below at every growth stage
    assert all(r['min_d'] >= 0.11 for r in d['stage_rows'])
    # the coarse reflow (new group) translates old anchors 1:1 (pure shift)
    group_stage = [r for r in d['stage_rows'] if r['action'] == 'group']
    assert len(group_stage) == 1
    assert group_stage[0]['disp_c'] == group_stage[0]['disp_f']
    assert group_stage[0]['disp_c'] > 0.1


def test_polysphere_use_cases_batch_supported():
    d = load('polysphere_use_cases_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # batch/generative routing is perfect
    assert d['use_case_1_classifier']['batch_acc'] == 1.0
    assert d['use_case_1_classifier']['per_point_acc'] > 0.5  # 0.653 vs chance 0.167
    # anomaly detection: large confidence gap, high rejection
    u2 = d['use_case_2_anomaly']
    assert u2['gap'] > 0.6                      # 0.728
    assert u2['in_kept'] == 1.0
    assert u2['ood_rejected'] > 0.95            # 0.983
    # generated samples re-route to source; continual add keeps accuracy
    assert d['use_case_3_generation']['cross_gen_all_ok'] is True
    u4 = d['use_case_4_continual']
    assert u4['acc_before'] == 1.0 and u4['acc_after'] == 1.0
    assert u4['spherical_separation'] > 0.9     # ~0.94, not bit-reproducible
    assert 'not bit-reproducible' in u4['note'].lower()


def test_polysphere_routing_batch_exact():
    d = load('polysphere_routing_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # batch routing is exact: identity confusion matrix
    assert d['batch_acc'] == 1.0
    assert d['confusion_offdiag'] == 0
    # per-point routing is weak but well above chance
    assert d['per_point_acc'] > 0.5                      # 0.659 vs chance 0.167
    # spherical separation is strong
    s = d['spherical_separation']
    assert s['silhouette'] > 0.9
    assert s['inter_mean'] > 10 * s['intra_mean']


def test_golden_survey_exact_and_no_emergent_locking():
    d = load('golden_survey_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # Part 1: step ratio is phi EXACTLY (machine precision)
    p1 = d['part1_fib_spiral']
    assert abs(p1['diff_from_phi']) < 1e-9
    assert math.isclose(p1['radius_per_turn'], p1['phi4'], rel_tol=1e-6)
    # Part 2: static C0 packing is uniform rings (no golden structure)
    assert all(r['gap_cv'] < 0.15 for r in d['part2_static_packing'][1:])
    # Part 3a: golden rotation maximizes the minimum angular gap
    assert d['part3a_rotation']['golden_maximizes'] is True
    # Part 3b: gap-filling does NOT lock onto the golden angle
    assert all(r['within_5deg_fraction'] <= 0.1 for r in d['part3b_arc_model'])
    assert all(r['abs_diff_from_golden'] > 100.0 for r in d['part3b_arc_model'])
    # Part 4: metric-and-regime dependent (cusp phi, disk -> 1)
    p4 = d['part4_metric_terms']
    assert abs(p4['cusp_log_coords'] - d['phi']) < 1e-5
    assert p4['euclidean_asymptotic'] < 1.01
    assert p4['poincare_hyperbolic'] < 1.01


def test_fib_stream_steady_and_ad_wins_all_seeds():
    d = load('fib_stream_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # AD_phi (absorb during large terms) beats P0 on BOTH axes in all 3 seeds
    for sd, m in d['multi_seed_finals'].items():
        assert m['final_all_ad'] > m['final_all_p0']
        assert m['final_old_ad'] > m['final_old_p0']
    # golden-rotation insertion is neutral after the flow (washes out)
    for row in d['partB_golden_vs_center']:
        assert abs(row['golden_all'] - row['center_all']) < 0.2
        assert abs(row['golden_old'] - row['center_old']) < 0.2
    # scaling: mean_r pinned by the clamp, min_d obeys a ring-packing law
    c = d['partC_scaling']
    assert abs(c['fib_center_P0']['a_mean_r']) < 0.1
    assert -0.9 < c['fib_center_P0']['b_min_d'] < -0.5
    assert -0.9 < c['eq_center_P0']['b_min_d'] < -0.5


def test_hamiltonian_routing_flow_separates():
    d = load('hamiltonian_routing_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    pd = d['pair_dist']
    # the flow separates centroids in the MEAN
    assert pd['flow_mean'] > 5 * pd['init_mean']            # 1.1433 vs 0.1803
    # ...but NOT in the min (clamped to the boundary)
    assert pd['flow_min'] < 0.05
    r = d['routing_acc']
    assert r['flow'] > r['init'] + 0.2                      # +0.345
    assert r['flow'] > r['best_random']                     # 0.765 vs 0.260
    # nearest-centroid reaches the oracle ceiling
    nc = d['nearest_centroid']
    assert nc['flow'] > 0.9
    assert nc['flow'] >= nc['oracle'] - 0.05                # 0.909 vs 0.911


def test_metric_comparison_refuted_numerically():
    d = load('metric_comparison_data.json')
    assert d['verdict'].startswith('REFUTED')
    p = d['metrics']['poincare']
    c = d['metrics']['cusp']
    # Poincare has NaN states; cusp escapes to ~2e13
    assert p['has_nan']
    assert c['r_range'][1] > 1e6
    assert not p['c0_holds'] and not c['c0_holds']
    assert p['c0_max_dev'] > 20 and c['c0_max_dev'] > 20
    assert not p['tsym_ok'] and not c['tsym_ok']
    assert c['energy_drift'] > 1e10


def test_c0_crossing_tsym_caveat():
    d = load('c0_crossing_tsym_data.json')
    assert d['verdict'].startswith('CAVEAT')
    rows = d['experiments']
    assert len(rows) == 4
    # T-symmetry holds (err < 0.5) in every run
    assert all(r['pass'] for r in rows)
    assert max(r['ts_error'] for r in rows) < 0.5
    # BUT the crossing premise never occurred: closest approach == start dist
    assert all(r['min_dist_to_origin'] > 0.0 for r in rows)
    # A/B/C never cross the q1 axis
    assert not rows[0]['crossed_origin'] and not rows[1]['crossed_origin']


def test_c0_cusp_flow_refuted():
    d = load('c0_cusp_flow_data.json')
    assert d['verdict'].startswith('REFUTED')
    c = d['cusp']
    p = d['poincare']
    # cusp escaped to ~2.7e23
    assert c['r_range'][1] > 1e6
    # Poincare overflowed to NaN
    assert not isinstance(p['r_range'][1], float) or p['r_range'][1] > 1.0
    assert not c['c0_holds']
    assert not c['tsym_ok'] and not p['tsym_ok']
    assert c['energy_drift'] > 1e10
    assert c['tsym_err'] > 1e6


def test_t39_cusp_flow_supported():
    d = load('t39_cusp_flow_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    v = d['verification']
    # exact conservation / exact geodesic
    assert v['cusp_energy_cv'] < 1e-12
    assert abs(v['step_ratio_asymp'] - v['phi']) < 1e-6
    assert v['wplane_r2'] > 0.999999
    assert abs(v['wplane_slope'] - v['wplane_expected_slope']) < 1e-6
    assert v['tsym_error'] == 0.0


def test_van_iterson_no_golden_lock():
    d = load('van_iterson_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    assert d['any_golden_lock'] is False
    # all three continuous rules, all 12 (r0, relax) settings: no lock
    for rule, rows in d['continuous_rules'].items():
        assert len(rows) == 12
        for row in rows:
            assert row['locked'] is False
            assert row['within5_frac'] < 0.5
    # part 1 control also never locks
    for row in d['part1_control']:
        assert row['within5_frac'] < 0.5


def test_reverse_pair_gaps_refuted():
    d = load('reverse_pair_gaps_data.json')
    assert d['verdict'].startswith('REFUTED')
    r = d['relations']
    # NOT a reversal pair: reverse(10262) = 26201 != 26102
    assert r['is_reversal_pair'] is False
    assert r['reverse_10262'] == 26201
    # sub-relations do hold
    assert r['diff_80_multiple'] is True
    assert r['digit_sum_10262'] == 11 and r['digit_sum_26102'] == 11
    # censuses are ordinary exact arithmetic
    assert d['gap_census_pair']['n_primes'] > 1000
    assert d['gap_census_mid']['n_primes'] > 100000
    assert d['emirps']['count'] > 300


def test_fibonacci_spiral_disk_refuted():
    d = load('fibonacci_spiral_data.json')
    assert d['verdict'].startswith('REFUTED')
    c = d['comparison']
    # turning far from golden angle in both projections
    assert c['mod_square_diff_deg'] > 50
    assert c['ratio_diff_deg'] > 50
    # pseudo-energy not conserved
    assert c['ratio_energy_drift'] > 1.0
    assert c['spiral_energy_drift'] > 0.5


def test_prime_count_engine_supported_with_corrections():
    d = load('prime_engine_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # exact prime counts at every retrace-chain point
    assert d['pi']['10262'] == 1258
    assert d['pi']['26102'] == 2868
    assert d['pi']['943901200001'] == 35575526191
    # endpoint prime, next gap 8
    assert d['endpoint_prime'] is True
    assert d['gap_above'] == 8
    # correction 1: true gap below is 24, not 'gap 1'
    assert d['gap_below'] == 24
    # correction 2: window max gap 176 exceeds the script's own 40-100 note
    assert d['max_gap_window'] == 176
    assert d['max_gap_window'] < d['cramer_ln2']
    # PNT: mean gap near ln N
    assert d['mean_gap'] > 25


def test_fibonacci_squares_disk_refuted():
    d = load('fibonacci_squares_data.json')
    assert d['verdict'].startswith('REFUTED')
    m = d['measurements']
    # 90-deg turning is a construction artifact, but pseudo-energy not conserved
    assert m['mean_turn_deg'] == 90.0
    assert m['pseudo_energy_drift'] > 0.5
    assert m['energy_linear_trend_per_step'] < 0  # decaying
    assert m['escaped'] is True
    assert not m['fib_tsym_ok']
    assert m['fib_tsym_error'] > 0.5
    assert m['c0_geodesic_tsym_error'] < 1e-6


def test_rotation_test_supported_with_correction():
    d = load('rotation_test_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # J1: rotation preserves structure exactly
    assert d['overlap_rotation'] > 0.999
    assert d['sim_corr'] > 0.999
    # J2: coordinates all change
    assert d['coord_max'] > 0.5
    # J3 correction: abs() disrupts but does NOT collapse to chance
    assert d['overlap_abs'] < d['overlap_rotation']
    assert d['overlap_abs'] > 5 * d['chance']


def test_clock_test_supported():
    d = load('clock_test_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # F1: calendar convention carries the law exactly at e0
    assert d['f1'] > 0.999
    # F2: the +15 re-index breaks it (and even dips below chance)
    assert d['f2'] < 0.5
    # F3: intrinsic features survive both epochs
    assert d['f3a'] > 0.999 and d['f3b'] > 0.999


def test_spring_fold_supported():
    d = load('spring_fold_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # A: mirror fold sweeps growth twice exactly (analytic area)
    assert abs(d['A']['area'] - d['A']['area_pred']) / d['A']['area_pred'] < 1e-6
    # A1: retrace fold closes EXACTLY to C0 and crease is exactly pi
    assert d['A1']['closure'] == 0.0
    assert abs(d['A1']['crease_pi'] - 1.0) < 1e-3
    # A2: golden fold ratio is phi exactly, but does NOT close to C0
    assert abs(d['A2']['ratio'] - 1.618033988749895) < 1e-9
    assert d['A2']['closure'] > 1.0
    # C: overcoil lock tucks the end under the start (closed ring)
    assert d['C']['tuck_on_start'] is True


def test_eikonal_fold_supported():
    d = load('eikonal_fold_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # E1: upwind viscosity solution converges to the exact tent
    assert d['eikonal_err'] < 1e-10
    # E2: crease is the cut locus exactly (equal arrival times)
    assert d['cut_locus'] == 0.0
    # E4: polar swept area matches analytic 2*a^2*TH^3/6 exactly
    assert abs(d['area_mirror'] - d['area_pred']) / d['area_pred'] < 1e-6
    assert abs(d['area_retrace']) < 1e-9


def test_retrace_boundary_supported():
    d = load('retrace_boundary_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # E1: the zig-zag family are all genuine weak solutions
    assert all(ok for _, ok, _ in d['weak_family'])
    # E2: tent passes viscosity; every zig-zag fails (down-up corner)
    assert d['tent_passes'] is True
    assert all(not ok for _, ok, _, _ in d['zigzag_viscosity'])
    # E3: upwind from a zig-zag seed converges to the tent
    assert d['upwind_from_zigzag_err'] < 1e-10
    # E4: selected switch point is the cut locus (equal eikonal time, exact)
    assert d['cut_locus_eq'] == 0.0
    # E5: reflection conserves |r'| across the crease
    assert d['reflection'] < 1e-9


def test_fold_optimizer_supported():
    d = load('fold_optimizer_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # G1: Hamiltonian energy drift is small and bounded (not secular)
    assert d['drift_h'] < 0.01
    assert d['area_ratio_h'] > 0.9
    # G2: recurrence returns near the start (Poincare)
    assert d['recurrence'] < 1e-3
    # G3: damped energy collapses to the minimum, area contracts fully
    assert d['ed_final'] < 1e-6
    assert d['area_ratio_d'] < 1e-3
    # G4: locks at the minimum and stays
    assert d['lock_err'] < 1e-3
    assert d['stays'] is True


def test_t65_fourpack_mixed_refuted():
    d = load('t65_fourpack_results.json')
    assert d['verdict'].startswith('MIXED')
    # P1: tau is identical across curiosity_drive (degenerate -> corr nan)
    assert d['P1']['tau_constant'] is True
    assert d['P1']['corr_cd_tau'] == 'nan'
    assert len(set(d['P1']['mean_tau'])) == 1
    # P2: ascent does NOT recover the seed (far above near-zero)
    assert all(e > 1.0 for e in [p['hyperbolic_err_to_seed'] for p in d['P2']])
    # P3: projection retains signal above null, but a single coord already full
    assert d['P3']['mi_projection'] > 1.5 * d['P3']['mi_null']
    assert d['P3']['mi_single_coord'] > 0.99
    # P4: no fixed-point convergence under dream/remix
    assert d['P4']['converged_fraction'] == 0.0


def test_phi_scheduler_supported_with_caveat():
    d = load('phi_scheduler_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # P5 fixed mu=0.5 is never usable: worst stream routing (holds per-seed)
    assert d['P5']['stream_old'] <= min(v['stream_old'] for v in d.values()
                                        if isinstance(v, dict) and 'stream_old' in v)
    # FIB+ABS buys final whole-layout integrity at old-routing cost (per-seed)
    assert d['FIB+ABS']['final_all'] > d['FIB']['final_all']
    assert d['FIB+ABS']['final_old'] < d['FIB']['final_old']
    # FIB keeps bounded latency
    assert 0 < d['FIB']['mean_buf'] <= 2.5
    # Part 3 (MNIST): scheduling is not needed on real embeddings
    assert d['part3_final_all']['NAIVE'] > d['part3_final_all']['FIB'] > d['part3_final_all']['FIB+ABS']


def test_flow_regularized_supported_narrow_window():
    d = load('flow_regularized_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # baseline numbers pinned
    assert abs(d['baseline']['routing'] - 0.9) < 1e-6
    assert abs(d['baseline']['test_acc'] - 0.905) < 1e-6
    # best lambda=0.007 wins on routing with accuracy preserved
    best = d['best']
    assert best['lambda'] == 0.007
    assert best['routing'] == 0.93
    assert best['test_acc'] >= d['baseline']['test_acc'] - 0.01
    # stronger flow (lambda=0.01) clearly hurts routing
    row = next(r for r in d['sweep'] if r['lambda'] == 0.01)
    assert row['routing_delta'] < -0.05


def test_flow_hier_reg_not_supported():
    d = load('flow_hier_reg_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    b, f = d['baseline'], d['flow-REG']
    # flow does NOT reduce drift (it is slightly worse)
    assert f['drift'] > b['drift']
    # flow is clearly worse on flat routing at stage 2
    assert f['routing_all'] < b['routing_all']
    assert f['routing_old'] < b['routing_old']
    # accuracy essentially preserved
    assert f['stage2_test_all'] >= b['stage2_test_all'] - 0.01
    # the one flow benefit: hierarchical routing is better
    assert f['hier_all'] > b['hier_all']
    assert f['hier_old'] > b['hier_old']


def test_flow_hier_reg_scaled_not_supported():
    d = load('flow_hier_reg_scaled_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    f, n, l = d['means']['FIXED'], d['means']['NSCAL'], d['means']['LIN']
    # n-scaling gain is marginal (<1% relative drift), everything else identical
    assert f['drift_rel'] - n['drift_rel'] < 0.01
    assert f['drift_rel'] - l['drift_rel'] < 0.01
    assert f['drift_rel'] == n['drift_rel'] or f['drift_rel'] - n['drift_rel'] > 0
    for m in (f, n, l):
        assert abs(m['acc_all'] - n['acc_all']) < 1e-4  # identical to 3 dp
    assert d['best_drift_rule'] in ('FIXED', 'NSCAL', 'LIN')


def test_balance_auto_not_supported():
    d = load('balance_auto_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    # detector fires only on the explosive event
    assert d['detector_fires_only_on_burst']
    # but AD does NOT beat P0: routing gains are <= 0
    assert d['ad_vs_p0_gains']['old_route'] <= 0.0
    assert d['ad_vs_p0_gains']['all_route'] <= 0.0
    p2 = d['part2']
    # P0 marginally best on real MNIST; P5 clearly worst on min separation
    assert p2['P0']['all_route'] >= p2['AD']['all_route']
    assert p2['P5']['min_d'] < p2['P0']['min_d']


def test_self_balancing_supported_geometry_regime():
    d = load('self_balancing_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # the coherence gate FIRES: COH skips the absorb in the crowded core
    assert d['coh_skips_absorb_part3_seed_42']
    assert d['part3']['COH']['absorbed'] == 'no'
    assert d['part3']['ABS']['absorbed'] == 'yes'
    # COH lands exactly on P0 in the crowded core (T51 failure avoided)
    assert d['part3']['COH']['old_route'] == d['part3']['P0']['old_route']
    assert d['part3']['COH']['all_route'] == d['part3']['P0']['all_route']
    # all-routing gain survives on the clean stream
    assert d['part2']['COH']['final_all'] > d['part2']['P0']['final_all']
    # but Part 4 MNIST: COH final_all below FIB (controller adds nothing there)
    assert d['part4_summary']['COH']['final_all_last'] < d['part4_summary']['FIB']['final_all_last']


def test_polysphere_mnist_supported():
    d = load('polysphere_mnist_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    p1 = d['part1']
    # batch routing far above chance
    assert p1['batch_routing']['acc'] > 0.8
    # wide anomaly gap
    assert p1['anomaly_gap'] > 0.4
    assert p1['conf_in'] > p1['conf_ood'] + 0.4
    # hierarchical well above combined chance but below flat
    assert d['part2']['hier_acc'] > 0.5
    assert d['part2']['hier_acc'] < p1['batch_routing']['acc']
    # active learning reaches perfect routing after faces added
    assert d['part3']['final_10_acc'] == 1.0
    assert d['part3']['unknown_flagged']['rate'] > 0.4


def test_polysphere_nnflow_viz_partial():
    d = load('polysphere_nnflow_viz_data.json')
    assert d['verdict'].startswith('PARTIAL')
    p1, p2 = d['part1_nn_truths'], d['part2_s2_flow']
    # NN-truth routing supported: far above chance
    assert p1['routing_acc'] > 0.8
    # S^2 flow NOT supported: near-zero silhouette, <all faces self-route
    assert p2['silhouette'] < 0.1
    assert p2['self_routed'] < p2['n_faces']
    # viz distribution sanity: routed vs actual per-class fractions align
    for row in d['part3_viz_distribution']:
        assert abs(row['routed_pct'] - row['actual_pct']) < 5.0


def test_decentral_net_supported():
    d = load('decentral_net_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    p4 = d['part4_final']
    # local flow usable on real embeddings: ABS-SC beats FIB on all-routing
    assert p4['ABS-SC']['all_route'] > p4['FIB']['all_route']
    # old-routing preserved
    assert p4['ABS-SC']['old_route'] >= 0.8
    assert p4['FIB']['old_route'] >= 0.8
    # banner discloses multi-seed means for parts 0-3
    assert 'seeds 42/11/7' in d['multi_seed_banner_parts_0_3']


def test_decentral_net_mnist_supported():
    d = load('decentral_net_mnist_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    # local-settle routes ~ at nearest-centroid baseline
    assert d['acc_grown_decentralnet'] >= d['acc_base_nearest_centroid'] - 0.03
    # local heal restores spacing
    assert d['spacing_after'] > d['spacing_before']
    # survivors keep routing after killing 3 neurons
    assert d['acc_survivors_broken'] >= 0.8
    assert d['acc_survivors_healed'] >= 0.8
    # regrow restores full 10-class net (above chance)
    assert d['acc_regrown_full'] > 0.7


def test_decentral_net_continual_not_supported():
    d = load('decentral_net_continual_data.json')
    assert d['verdict'].startswith('NOT SUPPORTED')
    p1 = d['part1']
    # local reflow loses to raw centroids on real 64D embeddings
    assert d['add_vs_control_old_delta'] < 0.0
    assert p1['ADD']['old_route'] < p1['CONTROL']['old_route']
    # MIX collapses (gauge freedom: never mix frames)
    assert p1['MIX']['old_route'] < 0.2
    assert p1['MIX']['all_route'] < p1['CONTROL']['all_route']
    # tether not dimension-independent: mu0=0.12 over-drifts vs CONTROL
    p2 = d['part2']
    assert p2['mu0_sweep'][0]['drift'] > p2['control']['old_route'] * 0.4
    # no mu0 beats CONTROL on all-routing
    for row in p2['mu0_sweep']:
        assert row['all_route'] <= p2['control']['all_route'] + 1e-9


def test_decentral_net_ceiling_supported():
    d = load('decentral_net_ceiling_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    rows = {r['n']: r for r in d['n_sweep']}
    # scaling is superlinear: ms/step grows much faster than n
    assert rows[20000]['ms_per_step'] > rows[5000]['ms_per_step'] * 5
    assert rows[5000]['ms_per_step'] > rows[1000]['ms_per_step'] * 5
    # peak working set at 20k blew past the D-array estimate (3.2 GB)
    assert rows[20000]['peak_ws_mb'] > 5000
    # measured ceiling 20k, RAM wall confirmed
    assert d['measured_ceiling_n'] == 20000
    assert d['peak_ws_at_20000_gb'] > 15.0


def test_decentral_net_t67_supported():
    d = load('decentral_net_t67_data.json')
    c = d['correctness']
    assert c['verdict'] == 'PASS'
    assert all(c[k] for k in ('grid2d_flow_bit_identical',
                              'tree64d_flow_bit_identical', 'spacing_equal',
                              'predict_equal', 'grid_knn_equals_bruteforce'))
    s = d['scaling']
    # indexed flow is ~linear where exact is ~n^2
    assert s['indexed_exponent'] < 1.4
    assert s['exact_exponent'] > 1.7
    # indexed wins decisively at n=8000
    assert s['indexed_ms_per_step']['8000'] < \
        s['exact_ms_per_step']['8000'] * 0.3
    i = d['internet_scale']
    # n=100k 2D grid flows; the all-pairs D would need 160 GB
    assert i['grid2d_n100k_ms_per_step'] > 0
    assert i['grid2d_allpairs_d_gb'] > 100
    assert i['highdim_real_top1m'] is True
    assert i['highdim_n10k_ms_per_step'] > 0


def test_decentral_net_live_supported():
    d = load('decentral_net_live_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'V1', 'V2', 'V3', 'V4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # V1: population bounded by CAP under churn
        assert p['bounded_pop'] is True
        assert p['max_n'] <= p['cap']
        # V2: post-damage spacing lands in the healthy band (no clump/blow-up)
        assert p['healed'] is True
        assert 0.05 <= p['spacing_post_damage'] <= 0.9
        # V3: routing probe accurate through churn
        assert p['probe_acc'] > 0.8
        assert p['n_damage_events'] > 3
    # V4: checkpoint/resume reproduces the uninterrupted trajectory
    assert d['resume_continuity']['continuity'] is True
    assert d['resume_continuity']['pos_identical'] is True


def test_bazaar_hybrid_supported():
    d = load('bazaar_hybrid_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'C1', 'C2', 'C3', 'C4', 'C5', 'C6'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # C1: hybrid burial threshold strictly above reddit's (seed 42)
    c1 = d['C1_brigade']['42']
    assert c1['hybrid_S50'] > c1['reddit_S50']
    # C2: hybrid top-K spam fraction well below reddit's on every seed
    for s in d['seeds']:
        assert d['C2_spam'][str(s)]['hybrid_topk_spam_frac'] < 0.1
        assert d['C2_spam'][str(s)]['reddit_topk_spam_frac'] > 0.3
    # C3: minority users see mostly their own community on the mesh feed
    for s in d['seeds']:
        assert d['C3_feed'][str(s)][
            'hybrid_minority_share_in_minority_feed'] > 0.8
    # C4: archive survives 50% node loss, tamper detected
    for s in d['seeds']:
        assert d['C4_archive'][str(s)]['retrieval_after_50pct_loss'] > 0.99
        assert d['C4_archive'][str(s)]['tamper_detected'] is True
    # C5: quorum wrong-removal collapses below central at p=0.20
    c5 = d['C5_moderation']['rows'][2]
    assert c5['quorum_wrong_removal'] < c5['central_wrong_removal'] / 50.0
    # C6: verified-vote-only raises the suspension threshold and collapses
    # quorum corruption far below the anonymous-hybrid baseline
    for s in d['seeds']:
        c6 = d['C6_verified_vote'][str(s)]
        assert c6['verified_S50'] > c6['anon_S50'] * 10
        assert c6['quorum_wrong_removal_verified_at_p020'] < \
            c6['quorum_wrong_removal_anon_at_p020'] / 100.0


def test_bazaar_net_supported():
    d = load('bazaar_net_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'N1', 'N2', 'N3a', 'N3b', 'N3c', 'N4', 'N5'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # N1: one chain head, one length, every archive verifies, cross-node
        # search finds the content
        assert p['heads_set_size'] == 1
        assert len(p['lengths']) == 1
        assert p['verify_all'] is True
        assert p['search_hits'] > 0
        # N2: emergent mesh feed dominated by the minority's own authors
        assert p['minor_share'] >= 0.6
        # N3a: sockpuppet below the standing gate; good post NOT removed
        assert p['sock_standing'] < 0.5
        assert p['good_removed'] is False
        # N3b: spam removed through the guardian quorum
        assert p['spam_removed'] is True
        # N3c: fabricated brigade on a standing author's post rejected
        assert p['g3_standing'] >= 0.7
        # N5: content survives a node kill; stateless restart resyncs to a
        # bit-identical verifying chain
        assert p['survived_search_count'] > 0
        assert p['resynced'] is True
        assert p['resynced_equal'] is True
        assert p['snap3_verify'] is True
    # N4: tamper-evidence - flipped payload breaks verify at its sequence
    # while the other node's archive stays valid
    assert d['tamper']['tamper_detected'] is True
    assert d['tamper']['other_node_still_valid'] is True


def test_decentral_net_t72_supported():
    d = load('decentral_net_t72_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'T1', 'T2', 'T3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    fw = d['flow_whole_internet']
    # T1: the whole 1.9M-site internet flows; all-pairs D would be 58 TB
    assert fw['n_sites'] >= 1_900_000
    assert fw['allpairs_d_gb'] > 10_000
    assert fw['ms_per_step'] > 0
    # T2: 20% kill + one local heal recovers consensus spacing
    he = d['heal_whole_internet']
    assert he['killed'] >= 300_000
    assert he['survivors'] >= 1_500_000
    assert he['spacing_after_heal'] > he['spacing_after_kill']
    # T3: high-dim wall measured on a real 10k-site slice
    assert d['highdim_wall']['n'] >= 10_000
    assert d['highdim_wall']['ms_per_step'] > 0


def test_decentral_net_anomaly_supported():
    d = load('decentral_net_anomaly_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'A1', 'A2', 'A3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # A1: novelty axis - DGA-shape random strings fall below the legit p5
    # threshold at high rate while known-bad split novel/impersonation
    assert d['novel_share_random'] >= 0.7
    assert d['novel_share_bad'] >= 0.1
    # A2: impersonation axis - a measurable share of known-bad sit above the
    # legit median (near-miss of a real site)
    assert d['impersonation_share_bad'] >= 0.05
    # A3: the honest wall - a large share of known-bad still overlap the legit
    # range (tracking subdomains of real brands), so geometry is
    # necessary-but-not-sufficient
    assert d['legit_n'] >= 1_000_000
    assert d['threshold_legit_p5'] > 0


def test_decentral_net_internet_supported():
    d = load('decentral_net_internet_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'I1', 'I2', 'I3', 'I4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # I1: the top-1M real sites are bulk-loaded
    assert d['n_sites'] >= 900_000
    assert d['weights_gb'] > 0
    # I2: routing examples carry real web neighbors
    assert len(d['routing_examples']) > 0
    assert all(h['sim'] > 0.2 for h in d['routing_examples'])
    # I3: a 20% outage leaves the majority still routed
    assert d['survivors'] >= 0.75 * d['n_sites']
    # I4: local flow on a real slice runs and the heal recovers spacing
    assert d['flow_ms_per_step'] > 0
    assert d['spacing_after_heal'] > d['spacing_after_kill']


def test_decentral_net_union_supported():
    d = load('decentral_net_union_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'U1', 'U2', 'U3', 'U4', 'U5'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    # U1: union + dedupe of two real top-1M lists yields ~1.91M unique sites
    assert d['unique_domains'] >= 1_800_000
    # U2: holding is ~2 KB/site - capacity is not the wall
    assert d['weights_gb'] > 0
    # U3: routing works across the merged lists
    assert len(d['routing_examples']) > 0
    assert all(h['sim'] > 0.2 for h in d['routing_examples'])
    # U4: 20% outage leaves the majority routed
    assert d['survivors'] >= 0.75 * d['loaded_n']
    # U5: the persisted checkpoint reloads bit-identically
    assert d['q_identical_on_reload'] is True


def test_decentral_web_supported():
    d = load('decentral_web_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'W1', 'W2', 'W3', 'W4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # W1: one chain head + one length across all nodes; every archive
        # verifies; all name sets agree; a page publishes on one node and is
        # served (with integrity) from every other node
        assert p['heads_set_size'] == 1
        assert len(p['lengths']) == 1
        assert p['verify_all'] is True
        assert p['names_agree'] is True
        assert p['served_everywhere'] is True
        # W2: identical content dedups to one address (3 publishes, 2 addrs);
        # a GET by address is served directly from the content store
        assert p['dedup_ok'] is True
        assert p['n_addrs'] < 3
        assert p['addr_lookup_ok'] is True
        # W4: a near-miss query resolves to the intended page by n-gram
        # embedding (google.com -> gooogle.com pattern)
        assert p['near_resolves'] is True
        assert p['near_hit'][0]['name'] == 'home'
        assert p['maps_hit'][0]['name'] == 'maps'
        # W3: a crashed node's pages stay served by survivors; a stateless
        # restart resyncs to a bit-identical verifying archive
        assert p['survived_ok'] is True
        assert p['resynced'] is True
        assert p['resynced_equal'] is True
        assert p['resynced_names'] is True
        assert p['snap3_verify'] is True
    # TLS run must pass the same structural gates
    assert d['tls_run']['dedup_ok'] is True
    assert d['tls_run']['resynced_equal'] is True
    assert d['tls_run']['verify_all'] is True
    # tamper-evidence: flipping one byte of a page's content breaks its
    # content-address while the other node's archive stays valid
    assert d['tamper']['tamper_flip_detected'] is True
    assert d['tamper']['other_node_still_valid'] is True


def test_learn_creativity_supported():
    d = load('learn_creativity_test_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'L1', 'L2', 'C1', 'C2', 'C3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # L1: the curriculum is acquired - probe accuracy climbs from
        # near-chance at minimal exposure to >=0.9 at full exposure
        assert p['floor'] <= 0.35
        assert p['ceiling'] >= 0.90
        assert p['ceiling'] - p['floor'] >= 0.55
        # L2: no forgetting - first-taught concepts keep >=0.85 after every
        # later concept is added
        assert p['no_forgetting_min'] >= 0.85
        # C1: a measurable share of mid-size near-miss variations are
        # simultaneously novel AND valid (never-presented new-but-right items)
        assert p['mid_creative'] >= 0.15
        # C2: random far nulls are novel but not creative, so the joint
        # novelty x validity criterion is necessary
        assert p['null']['novel'] >= 0.90
        assert p['null']['creative'] <= 0.05
        # C3: creative yield is interior-peaked over mutation size (mid size
        # beats too-close and too-far)
        sizes = sorted(p['creative'], key=float)
        assert len(sizes) == 4
        ys = [p['creative'][k]['creative'] for k in sizes]
        assert ys[1] > ys[0] and ys[1] > ys[2] and ys[1] > ys[3]


def test_learn_curve_scale_supported():
    d = load('learn_curve_scale_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'S1', 'S2', 'S3'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        # S1: the sparse floor is chance and strictly decreases with C over
        # the well-separated regime C in {2,4,8,16}
        f = [p['floor'][str(c)] for c in (2, 4, 8, 16)]
        assert f[0] >= 0.45 and f[-1] <= 0.12
        assert all(f[i] > f[i + 1] for i in range(len(f) - 1))
        # S2: the acquisition curve exists at every scale - the full-exposure
        # ceiling holds >=0.90 for C in {2,4,8} and the dynamic range grows
        assert min(p['ceiling'][str(c)] for c in (2, 4, 8)) >= 0.90
        assert (p['ceiling']['8'] - p['floor']['8']) - \
            (p['ceiling']['2'] - p['floor']['2']) >= 0.25
        # S3: capacity saturation - the ceiling collapses monotonically once
        # adjacent homes reach a few exemplar-sigma
        cs = [p['ceiling'][str(c)] for c in (8, 16, 24, 32)]
        assert cs[1] < cs[0] - 0.15 and cs[-1] <= 0.50
        assert all(cs[i] > cs[i + 1] for i in range(len(cs) - 1))
        assert p['critical_scale'] <= 10


def test_human_trial_pilot_supported():
    d = load('human_trial_pilot_data.json')
    assert d['verdict'].startswith('SUPPORTED')
    claims = {c['id']: c for c in d['claims']}
    assert set(claims) == {'P1', 'P2', 'P3', 'P4'}
    assert all(c['verdict'] == 'SUPPORTED' for c in claims.values())
    for s in d['seeds']:
        p = d['per_seed'][str(s)]
        perf = p['per_archetype']['perfect']
        # P1: a perfect participant attains every engine bar
        assert perf['l1_ok'] is True and perf['l2_ok'] is True
        assert perf['c1_ok'] is True and perf['c2_ok'] is True
        assert perf['c3_ok'] is True
        # P2: a random non-learner fails L1 and C1
        rand = p['per_archetype']['random']
        assert rand['l1_ok'] is False and rand['c1_ok'] is False
        assert rand['l1_ceiling'] <= 0.30
        assert rand['yield']['mid']['creative'] <= 0.06
        # P3: the joint criterion binds on both sides (the human C3)
        y = perf['yield']
        assert y['mid']['creative'] >= 0.15
        assert y['mid']['creative'] > y['trivial']['creative']
        assert y['mid']['creative'] > y['wild']['creative']
        assert y['trivial']['valid'] > y['trivial']['novel']
        assert y['wild']['novel'] > y['wild']['valid']
        assert p['per_archetype']['copycat']['yield']['mid']['creative'] == 0.0
        # P4: the C2 constraint holds on the human scale
        assert p['per_archetype']['perfect']['null']['novel'] >= 0.90
        assert p['per_archetype']['perfect']['null']['creative'] <= 0.05

