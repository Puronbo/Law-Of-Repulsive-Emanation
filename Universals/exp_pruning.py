"""
Experiment: Pruning via Crease Proximity
==========================================
Tests whether neurons whose pre-activation is persistently near zero
(crease) are redundant and can be pruned.

Compares:
  A) Crease proximity: remove neurons with highest near-threshold fraction
  B) Weight magnitude: remove neurons with smallest L2 weight norm
  C) Random: remove random neurons (baseline)

Ported from extracted_text/code/exp_pruning.py
"""

import numpy as np
import json
import os
import sys

np.random.seed(42)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from puno_utils import Net, accuracy, train_model, make_multiscale, CREASE_THRESH


def run():
    print('=' * 60)
    print('PRUNING VIA CREASE PROXIMITY')
    print('=' * 60)

    X, y = make_multiscale(5000)
    X_tr, y_tr = X[:3500], y[:3500]
    X_te, y_te = X[3500:], y[3500:]

    model = Net([2, 128, 128, 1])
    print('\nTraining model...')
    train_model(model, X_tr, y_tr, X_te, y_te, lr=1e-3, epochs=300, verbose=False)
    baseline_acc = accuracy(model, X_te, y_te)
    print(f'Baseline accuracy: {baseline_acc:.4f}')

    # Measure per-neuron crease density
    all_zs = [np.zeros((len(X_tr), model.L[i]['W'].shape[1])) for i in range(len(model.L) - 1)]
    h = X_tr
    for i, layer in enumerate(model.L):
        z = h @ layer['W'] + layer['b']
        if i < len(model.L) - 1:
            all_zs[i] = z
            h = z * (z > 0).astype(float)

    crease_densities = [((np.abs(z_layer) < CREASE_THRESH).astype(float).mean(axis=0)) for z_layer in all_zs]
    all_crease_scores = np.concatenate(crease_densities)
    n_neurons = len(all_crease_scores)

    weight_norms = np.concatenate([
        np.linalg.norm(model.L[i]['W'], axis=0) for i in range(len(model.L) - 1)
    ])

    # Build neuron index list
    all_neurons = []
    for l in range(len(model.L) - 1):
        n_units = model.L[l]['W'].shape[1]
        for u in range(n_units):
            all_neurons.append((l, u))
    assert len(all_neurons) == n_neurons

    order_crease = np.argsort(all_crease_scores)[::-1]
    order_magnitude = np.argsort(weight_norms)

    # Ablation experiment
    prune_ratios = np.linspace(0, 0.5, 11)
    results_crease = {'ratios': [], 'accs': []}
    results_magnitude = {'ratios': [], 'accs': []}
    results_random = {'ratios': [], 'accs': []}

    for ratio in prune_ratios:
        n_prune = int(ratio * n_neurons)

        # Crease pruning
        model_cr = model.copy()
        for idx in order_crease[:n_prune]:
            l, u = all_neurons[idx]
            model_cr.L[l]['W'][:, u] = 0
        acc_cr = accuracy(model_cr, X_te, y_te)

        # Magnitude pruning
        model_mag = model.copy()
        for idx in order_magnitude[:n_prune]:
            l, u = all_neurons[idx]
            model_mag.L[l]['W'][:, u] = 0
        acc_mag = accuracy(model_mag, X_te, y_te)

        # Random pruning (5 trials)
        accs_rand = []
        for _ in range(5):
            model_rand = model.copy()
            rand_idx = np.random.permutation(n_neurons)[:n_prune]
            for idx in rand_idx:
                l, u = all_neurons[idx]
                model_rand.L[l]['W'][:, u] = 0
            accs_rand.append(accuracy(model_rand, X_te, y_te))
        acc_rand = float(np.mean(accs_rand))

        results_crease['ratios'].append(float(ratio))
        results_crease['accs'].append(float(acc_cr))
        results_magnitude['ratios'].append(float(ratio))
        results_magnitude['accs'].append(float(acc_mag))
        results_random['ratios'].append(float(ratio))
        results_random['accs'].append(acc_rand)

        if ratio > 0:
            print(f'  Prune {ratio*100:3.0f}% | crease={acc_cr:.4f} | magnitude={acc_mag:.4f} | random={acc_rand:.4f}')

    output = {
        'experiment': 'exp_pruning',
        'baseline_acc': baseline_acc,
        'n_neurons': n_neurons,
        'crease_density_stats': {
            'mean': float(all_crease_scores.mean()),
            'std': float(all_crease_scores.std()),
            'pct_above_01': float((all_crease_scores > 0.1).mean()),
            'pct_above_02': float((all_crease_scores > 0.2).mean()),
        },
        'results': {
            'crease': results_crease,
            'magnitude': results_magnitude,
            'random': results_random,
        },
    }

    with open(os.path.join(BASE_DIR, 'exp_pruning_results.json'), 'w') as f:
        json.dump(output, f, indent=2)
    print(f'\n[EXPORTED] exp_pruning_results.json')
    print('Pruning experiment complete.')


if __name__ == '__main__':
    run()
