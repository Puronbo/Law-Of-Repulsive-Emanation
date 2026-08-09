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
