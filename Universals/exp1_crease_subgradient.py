"""
Experiment 1: Crease-Aware Subgradient Selection
==================================================
Tests whether different subgradient choices at ReLU creases affect
training dynamics and generalization.

Ported from extracted_text/code/exp1_crease_subgradient.py
"""

import numpy as np
import json
import os
import sys

np.random.seed(42)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from puno_utils import Net, bce, accuracy, make_ring_dataset

CREASE_THRESH = 1e-10


class SubgradNet(Net):
    """Net with crease-aware subgradient selection."""

    def backward(self, grad, crease_mode='standard'):
        n_layers = len(self.L)
        self.grads = []
        for i in range(n_layers - 1, -1, -1):
            if i < n_layers - 1:
                z = self.zs[i]
                if crease_mode == 'standard':
                    mask = (z > 0).astype(float)
                elif crease_mode == 'always_on':
                    mask = np.ones_like(z)
                elif crease_mode == 'always_off':
                    mask = np.zeros_like(z)
                elif crease_mode == 'random':
                    mask = (z > 0).astype(float)
                    at_crease = (np.abs(z) < CREASE_THRESH)
                    if at_crease.any():
                        mask[at_crease] = np.random.randint(0, 2, size=at_crease.sum()).astype(float)
                else:
                    mask = (z > 0).astype(float)
                grad = grad * mask
            layer = self.L[i]
            x_in = self.acts[i]
            dW = x_in.T @ grad
            db = grad.sum(axis=0)
            self.grads.insert(0, {'dW': dW, 'db': db})
            if i > 0:
                grad = grad @ layer['W'].T


def train_with_mode(dims, X_tr, y_tr, X_te, y_te, mode='standard',
                    lr=1e-3, epochs=300, batch_size=128):
    np.random.seed(42)
    model = SubgradNet(dims)
    n = len(X_tr)
    losses, accs, creases = [], [], []
    step = 0

    for ep in range(1, epochs + 1):
        idx = np.random.permutation(n)
        ep_loss = 0; ep_cre = 0; nb = 0

        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            Xb = X_tr[idx[start:end]]
            yb = y_tr[idx[start:end]]
            step += 1

            logits, _ = model.forward(Xb, track_creases=True)
            loss = bce(logits, yb.reshape(-1, 1))
            y_pred = 1.0 / (1.0 + np.exp(-logits))
            grad = y_pred - yb.reshape(-1, 1)

            model.backward(grad, crease_mode=mode)
            model.update(lr, step)
            ep_loss += loss

            # Count creases
            h = Xb
            for i, layer in enumerate(model.L[:-1]):
                z = h @ layer['W'] + layer['b']
                ep_cre += (np.abs(z) < 1e-6).sum()
                h = z * (z > 0).astype(float)
            nb += 1

        acc = accuracy(model, X_te, y_te)
        losses.append(float(ep_loss / nb))
        accs.append(float(acc))
        creases.append(float(ep_cre / nb))

        if ep % 50 == 0 or ep == 1:
            print(f'  {mode:12s} Ep {ep:3d} | loss={losses[-1]:.4f} | acc={accs[-1]:.4f}')

    return {
        'losses': losses[::10],
        'accs': accs[::10],
        'creases': creases[::10],
        'best_acc': max(accs),
        'final_acc': accs[-1],
        'final_loss': losses[-1],
        'avg_crease': float(np.mean(creases)),
    }


def run():
    print('=' * 60)
    print('EXPERIMENT 1: Crease-Aware Subgradient Selection')
    print('=' * 60)

    X, y = make_ring_dataset(3000, noise=0.12)
    split = int(0.8 * len(X))
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]

    m, s = X_tr.mean(0), X_tr.std(0)
    X_tr = (X_tr - m) / s
    X_te = (X_te - m) / s

    dims = [2, 64, 64, 1]
    modes = ['standard', 'random', 'always_on']
    results = {}

    for mode in modes:
        np.random.seed(42)
        results[mode] = train_with_mode(dims, X_tr, y_tr, X_te, y_te, mode=mode)

    # Summary
    print('\n--- Results ---')
    for mode in modes:
        r = results[mode]
        print(f'  {mode:12s}: best={r["best_acc"]:.4f} final={r["final_acc"]:.4f} '
              f'loss={r["final_loss"]:.4f} crease={r["avg_crease"]:.1f}')

    # Fold depth snapshot
    np.random.seed(42)
    probe = SubgradNet(dims)
    _ = probe.forward(X_tr[:256])
    total_units = sum(dims[i] * dims[i + 1] for i in range(len(dims) - 2))
    crease_count = 0
    h = X_tr[:256]
    for i, layer in enumerate(probe.L[:-1]):
        z = h @ layer['W'] + layer['b']
        crease_count += (np.abs(z) < 1e-6).sum()
        h = z * (z > 0).astype(float)

    output = {
        'experiment': 'exp1_crease_subgradient',
        'results': results,
        'fold_depth': {
            'crease_count': int(crease_count),
            'total_units': total_units,
            'ratio': float(crease_count / (256 * total_units)) if total_units > 0 else 0,
        },
    }

    with open(os.path.join(BASE_DIR, 'exp1_results.json'), 'w') as f:
        json.dump(output, f, indent=2)
    print(f'\n[EXPORTED] exp1_results.json')
    print('Experiment 1 complete.')


if __name__ == '__main__':
    run()
