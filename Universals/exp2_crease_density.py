"""
Experiment 2: Crease Density and Decision Boundary Complexity
==============================================================
Tests the Puno Calculus prediction: networks with higher crease density
develop more fragmented decision boundaries that capture fine-grained
structure.

Ported from extracted_text/code/exp2_crease_density.py
"""

import numpy as np
import json
import os
import sys

np.random.seed(42)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from puno_utils import Net, bce, accuracy, make_multiscale, boundary_complexity


def train_and_measure(dims, X_tr, y_tr, X_te, y_te, lr=1e-3, epochs=300, batch_size=128):
    np.random.seed(42)
    model = Net(dims)
    n = len(X_tr)
    hist = {'loss': [], 'acc': [], 'crease_density': []}
    step = 0

    for ep in range(1, epochs + 1):
        idx = np.random.permutation(n)
        ep_loss = 0; ep_cre = 0; nb = 0

        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            Xb = X_tr[idx[start:end]]
            yb = y_tr[idx[start:end]]
            step += 1

            logits, creases = model.forward(Xb, track_creases=True)
            loss = bce(logits, yb.reshape(-1, 1))
            y_pred = 1.0 / (1.0 + np.exp(-logits))
            grad = y_pred - yb.reshape(-1, 1)

            ep_cre += creases.mean()
            nb += 1

            model.backward(grad)
            model.update(lr, step)
            ep_loss += loss

        acc = accuracy(model, X_te, y_te)
        hist['loss'].append(float(ep_loss / nb))
        hist['acc'].append(float(acc))
        hist['crease_density'].append(float(ep_cre / nb))

        if ep % 50 == 0 or ep == 1:
            print(f'  Ep {ep:3d} | loss={hist["loss"][-1]:.4f} | acc={acc:.4f} | crease={hist["crease_density"][-1]:.2f}')

    hist['best_acc'] = max(hist['acc'])
    return hist, model


def run():
    print('=' * 60)
    print('EXPERIMENT 2: Crease Density & Boundary Complexity')
    print('=' * 60)

    X, y = make_multiscale(5000)
    split = int(0.8 * len(X))
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]
    print(f'Data: {len(X_tr)} train, {len(X_te)} test')

    architectures = [
        ('Shallow_1L', [2, 256, 1]),
        ('Medium_2L', [2, 128, 128, 1]),
        ('Deep_4L', [2, 64, 64, 64, 64, 1]),
        ('WideShallow', [2, 512, 1]),
        ('NarrowDeep', [2, 32, 32, 32, 32, 1]),
    ]

    results = {}
    for name, dims in architectures:
        n_params = sum(dims[i] * dims[i + 1] for i in range(len(dims) - 1))
        n_layers = len(dims) - 1
        print(f'\n--- {name} ({n_layers}L, {n_params} params) ---')
        hist, model = train_and_measure(dims, X_tr, y_tr, X_te, y_te)
        comp = boundary_complexity(model)
        avg_cre = float(np.mean(hist['crease_density']))

        results[name] = {
            'losses': hist['loss'][::10],
            'accs': hist['acc'][::10],
            'creases': hist['crease_density'][::10],
            'best_acc': hist['best_acc'],
            'complexity': comp,
            'avg_crease': avg_cre,
            'n_layers': n_layers,
            'n_params': n_params,
        }
        print(f'  >> Acc={hist["best_acc"]:.4f} | Boundary={comp} | Crease={avg_cre:.2f}')

    # Correlations
    names = list(results.keys())
    cre_dens = np.array([results[n]['avg_crease'] for n in names])
    comps = np.array([results[n]['complexity'] for n in names])
    layers = np.array([results[n]['n_layers'] for n in names])

    correlations = {}
    if len(names) >= 3:
        from scipy.stats import pearsonr
        c_cre, _ = pearsonr(cre_dens, comps)
        c_lay, _ = pearsonr(layers, comps)
        correlations = {
            'crease_vs_complexity': float(c_cre),
            'layers_vs_complexity': float(c_lay),
        }
        print(f'\nCorrelation: crease vs complexity = {c_cre:+.4f}')
        print(f'Correlation: layers vs complexity = {c_lay:+.4f}')

    output = {
        'experiment': 'exp2_crease_density',
        'results': results,
        'correlations': correlations,
    }

    with open(os.path.join(BASE_DIR, 'exp2_results.json'), 'w') as f:
        json.dump(output, f, indent=2)
    print(f'\n[EXPORTED] exp2_results.json')
    print('Experiment 2 complete.')


if __name__ == '__main__':
    run()
