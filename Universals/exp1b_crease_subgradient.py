#!/usr/bin/env python3
"""
Experiment 1b: Crease-Aware Subgradient Selection (narrower threshold)
======================================================================
Uses tighter crease detection (|z| < 0.01, vs default 0.05) and additional
strategies: standard, random, oppose, always_on

Ported from Book of Puno exp1b_crease_subgradient.py with JSON export.
"""

import json
import os
import numpy as np
from puno_utils import Net, make_ring_dataset, bce, accuracy, auroc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

np.random.seed(42)

CREASE_THRESH = 0.01


class CreaseNet:
    def __init__(self, dims):
        self.L = []
        for i in range(len(dims) - 1):
            fan_in = dims[i]
            fan_out = dims[i + 1]
            W = np.random.randn(fan_in, fan_out) * np.sqrt(2.0 / fan_in)
            b = np.zeros(fan_out)
            self.L.append({'W': W, 'b': b,
                          'mW': np.zeros_like(W), 'vW': np.zeros_like(W),
                          'mb': np.zeros_like(b), 'vb': np.zeros_like(b)})

    def forward(self, x):
        self.zs = []
        self.acts = [x]
        h = x
        for i, layer in enumerate(self.L):
            z = h @ layer['W'] + layer['b']
            self.zs.append(z)
            h = np.maximum(z, 0) if i < len(self.L) - 1 else z
            self.acts.append(h)
        return h

    def backward(self, grad, crease_strategy='standard'):
        n = len(self.L)
        self.grads = []
        for i in range(n - 1, -1, -1):
            if i < n - 1:
                z = self.zs[i]
                if crease_strategy == 'always_on':
                    mask = np.ones_like(z)
                elif crease_strategy == 'random':
                    mask = (z > 0).astype(float)
                    at_crease = np.abs(z) < CREASE_THRESH
                    if at_crease.any():
                        mask[at_crease] = np.random.randint(0, 2, size=at_crease.sum()).astype(float)
                elif crease_strategy == 'oppose':
                    mask = (z > 0).astype(float)
                    at_crease = np.abs(z) < CREASE_THRESH
                    mask[at_crease] = 1.0 - mask[at_crease]
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
        return grad

    def update(self, lr, t, beta1=0.9, beta2=0.999, eps=1e-8):
        for i, layer in enumerate(self.L):
            g = self.grads[i]
            for p_key, m_key, v_key in [('W', 'mW', 'vW'), ('b', 'mb', 'vb')]:
                p = layer[p_key]
                m = layer[m_key]
                v = layer[v_key]
                g_val = g['d' + p_key]
                m[:] = beta1 * m + (1 - beta1) * g_val
                v[:] = beta2 * v + (1 - beta2) * (g_val ** 2)
                m_h = m / (1 - beta1 ** t)
                v_h = v / (1 - beta2 ** t)
                p -= lr * m_h / (np.sqrt(v_h) + eps)

    def count_near_creases(self, x):
        h = x
        total = 0
        for i, layer in enumerate(self.L[:-1]):
            z = h @ layer['W'] + layer['b']
            total += (np.abs(z) < CREASE_THRESH).sum()
            h = np.maximum(z, 0)
        return total


def train(model, X_tr, y_tr, X_te, y_te, strategy='standard',
          lr=1e-3, epochs=300, batch=128):
    n = len(X_tr)
    history = {'loss': [], 'acc': [], 'creases': []}
    best_acc = 0
    step = 0

    for ep in range(1, epochs + 1):
        idx = np.random.permutation(n)
        ep_loss = 0
        ep_cre = 0
        nb = 0

        for start in range(0, n, batch):
            end = min(start + batch, n)
            Xb = X_tr[idx[start:end]]
            yb = y_tr[idx[start:end]]
            step += 1

            logits = model.forward(Xb)
            loss = bce(logits, yb.reshape(-1, 1))
            y_pred = 1.0 / (1.0 + np.exp(-logits))
            grad = y_pred - yb.reshape(-1, 1)

            cre = model.count_near_creases(Xb)
            ep_cre += cre
            nb += 1

            model.backward(grad, strategy)
            model.update(lr, step)
            ep_loss += loss

        te_logits = model.forward(X_te)
        te_pred = 1.0 / (1.0 + np.exp(-te_logits))
        acc = np.mean((te_pred > 0.5).ravel() == y_te)
        best_acc = max(best_acc, acc)

        history['loss'].append(float(ep_loss / nb))
        history['acc'].append(float(acc))
        history['creases'].append(float(ep_cre / nb))

        if ep % 50 == 0 or ep == 1:
            print(f'  Ep {ep:3d} | loss={history["loss"][-1]:.4f} | '
                  f'acc={acc:.4f} | cre={history["creases"][-1]:.1f}')

    history['best_acc'] = float(best_acc)
    history['final_acc'] = float(history['acc'][-1])
    return history


def run():
    print('=' * 70)
    print('EXPERIMENT 1b: Crease-Aware Subgradient (wider threshold)')
    print('=' * 70)

    X, y = make_ring_dataset(3000, noise=0.12)
    split = int(0.8 * len(X))
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]
    m, s = X_tr.mean(0), X_tr.std(0)
    X_tr = (X_tr - m) / s
    X_te = (X_te - m) / s
    print(f'Data: {len(X_tr)} train, {len(X_te)} test')

    dims = [2, 64, 64, 1]
    strategies = ['standard', 'random', 'oppose', 'always_on']
    results = {}

    print(f'\nCrease threshold: |z| < {CREASE_THRESH}')
    print('Training strategies...\n')

    for strat in strategies:
        print(f'--- {strat.upper()} ---')
        np.random.seed(42)
        model = CreaseNet(dims)
        h = train(model, X_tr, y_tr, X_te, y_te, strat, lr=1e-3, epochs=300)
        results[strat] = h
        print(f'  >> Best: {h["best_acc"]:.4f}  Final: {h["final_acc"]:.4f}  '
              f'Avg creases: {np.mean(h["creases"]):.1f}\n')

    print('=' * 70)
    print('FINAL RESULTS')
    print('=' * 70)
    print(f'{"Strategy":<12} {"Best Acc":<10} {"Final Acc":<10} {"Final Loss":<10} {"Avg Crease":<10}')
    print('-' * 52)
    for s in strategies:
        r = results[s]
        ac = np.mean(r['creases'])
        print(f'{s:<12} {r["best_acc"]:<10.4f} {r["final_acc"]:<10.4f} {r["loss"][-1]:<10.4f} {ac:<10.1f}')

    summary = {s: {
        'best_acc': results[s]['best_acc'],
        'final_acc': results[s]['final_acc'],
        'final_loss': results[s]['loss'][-1],
        'avg_creases': float(np.mean(results[s]['creases'])),
    } for s in strategies}

    history = {s: {
        'loss': results[s]['loss'],
        'acc': results[s]['acc'],
        'creases': results[s]['creases'],
    } for s in strategies}

    export = {
        'summary': summary,
        'history': history,
        'crease_threshold': CREASE_THRESH,
        'strategies': strategies,
    }

    out_path = os.path.join(BASE_DIR, 'exp1b_results.json')
    with open(out_path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f'\n[EXPORTED] {out_path}')

    print('\nExperiment 1b complete.')


if __name__ == '__main__':
    run()
