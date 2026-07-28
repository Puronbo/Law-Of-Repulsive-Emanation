"""
Demo: OOD Detection via Crease Density
=========================================
Tests whether OOD inputs produce higher crease density than in-distribution
inputs. Compares crease density vs MSP baseline.

Ported from extracted_text/code/demo_ood.py
"""

import numpy as np
import json
import os
import sys

np.random.seed(42)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from puno_utils import Net, accuracy, train_model, make_multiscale, OODScorer, auroc


def run():
    print('=' * 60)
    print('OOD DETECTION VIA CREASE DENSITY')
    print('=' * 60)

    # Train model
    X, y = make_multiscale(6000)
    X_tr, y_tr = X[:3600], y[:3600]
    X_id, y_id = X[3600:4800], y[3600:4800]

    model = Net([2, 64, 64, 1])
    print('\nTraining model...')
    train_model(model, X_tr, y_tr, X_id, y_id, lr=1e-3, epochs=300, verbose=False)
    id_acc = accuracy(model, X_id, y_id)
    print(f'ID accuracy: {id_acc:.4f}')

    # OOD datasets
    n_ood = len(X_id)
    ood_data = {
        'ID (checkerboard)': X_id,
        'Far-OOD (uniform)': np.random.uniform(-10, 10, (n_ood, 2)),
        'Far-OOD (Gaussian)': np.random.randn(n_ood, 2) * 3 + np.array([15, 15]),
        'Near-OOD (shifted)': np.random.uniform(-5, 5, (n_ood, 2)),
        'Center noise': np.random.uniform(-1, 1, (n_ood, 2)),
    }

    # Score
    scorer = OODScorer(model, epsilon=0.05)
    results = {}
    for label, x_data in ood_data.items():
        _, density = scorer.score_batch(x_data)
        logits, _ = model.forward(x_data)
        probs = 1.0 / (1.0 + np.exp(-logits))
        msp = np.maximum(probs.ravel(), 1 - probs.ravel())
        results[label] = {
            'mean_density': float(density.mean()),
            'std_density': float(density.std()),
            'mean_msp': float(msp.mean()),
            'std_msp': float(msp.std()),
        }
        print(f'  {label:<28s} | density={density.mean():.4f} | msp={msp.mean():.4f}')

    # AUROC
    id_density = scorer.score_batch(X_id)[1]
    id_msp_logits, _ = model.forward(X_id)
    id_msp_probs = 1.0 / (1.0 + np.exp(-id_msp_logits))
    id_msp = np.maximum(id_msp_probs.ravel(), 1 - id_msp_probs.ravel())

    auroc_results = {}
    print('\n--- AUROC (ID vs OOD) ---')
    for label, x_data in ood_data.items():
        if label.startswith('ID'):
            continue
        _, ood_density = scorer.score_batch(x_data)
        ood_logits, _ = model.forward(x_data)
        ood_msp_probs = 1.0 / (1.0 + np.exp(-ood_logits))
        ood_msp = np.maximum(ood_msp_probs.ravel(), 1 - ood_msp_probs.ravel())

        cr_auroc = auroc(id_density, ood_density)
        msp_auroc = auroc(id_msp, ood_msp)
        auroc_results[label] = {'crease': float(cr_auroc), 'msp': float(msp_auroc)}
        print(f'  {label:<28s} | crease={cr_auroc:.4f} | msp={msp_auroc:.4f}')

    output = {
        'experiment': 'demo_ood',
        'id_accuracy': id_acc,
        'results': results,
        'auroc': auroc_results,
    }

    with open(os.path.join(BASE_DIR, 'exp_ood_results.json'), 'w') as f:
        json.dump(output, f, indent=2)
    print(f'\n[EXPORTED] exp_ood_results.json')
    print('OOD detection demo complete.')


if __name__ == '__main__':
    run()
