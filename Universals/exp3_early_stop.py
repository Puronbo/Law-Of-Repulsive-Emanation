#!/usr/bin/env python3
"""
Experiment 3: Early Stopping via Crease Stabilization
======================================================
Puno Calculus prediction: when crease density stabilizes (units stop
toggling between on/off states), the network's partition of input space
has converged, making further training unnecessary.

Compares four strategies:
  A) Full:     train full budget (baseline)
  B) Val Loss: early stop on validation loss plateau
  C) Crease:   early stop on crease density stabilization
  D) Both:     first triggers wins

Ported from Book of Puno exp3_early_stop.py with JSON export.
"""

import json
import math
import os
import numpy as np
from puno_utils import Net, make_multiscale, bce, accuracy, auroc, boundary_complexity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

np.random.seed(42)

CREASE_THRESH = 0.05


def forward_with_crease(model, x):
    """Forward pass that also counts crease-adjacent units."""
    logits, _ = model.forward(x)
    crease_count = 0
    for layer in model.L:
        z = layer.get('_last_z')
        if z is not None:
            crease_count += int(np.sum(np.abs(z) < CREASE_THRESH))
    return logits, crease_count


def train(model, X_tr, y_tr, X_va, y_va, lr=1e-3, max_epochs=500, batch=128,
          stop_mode='full', patience=30, crease_patience=None, crease_delta=0.008):
    n = len(X_tr)
    hist = {'loss': [], 'va_loss': [], 'va_acc': [], 'crease_density': []}
    step = 0
    best_va_loss = float('inf')
    best_va_acc = 0.0
    stop_epoch = max_epochs
    stop_reason = 'max_epochs'

    prev_cre = None
    crease_stable_count = 0
    cp = crease_patience if crease_patience else patience
    val_loss_count = 0

    for ep in range(1, max_epochs + 1):
        idx = np.random.permutation(n)
        ep_loss = 0
        ep_cre = 0
        nb = 0

        for start in range(0, n, batch):
            end = min(start + batch, n)
            Xb = X_tr[idx[start:end]]
            yb = y_tr[idx[start:end]]
            step += 1

            logits, creases = model.forward(Xb, track_creases=True)
            loss = bce(logits, yb.reshape(-1, 1))
            y_pred = 1.0 / (1.0 + np.exp(-logits))
            grad = y_pred - yb.reshape(-1, 1)

            ep_cre += float(np.sum(creases)) / batch
            nb += 1

            model.backward(grad)
            model.update(lr, step)
            ep_loss += loss

        va_logits, _ = model.forward(X_va)
        va_loss = bce(va_logits, y_va.reshape(-1, 1))
        va_acc = accuracy(model, X_va, y_va)

        avg_cre = ep_cre / nb
        hist['loss'].append(float(ep_loss / nb))
        hist['va_loss'].append(float(va_loss))
        hist['va_acc'].append(float(va_acc))
        hist['crease_density'].append(float(avg_cre))

        if va_loss < best_va_loss:
            best_va_loss = va_loss
            best_va_acc = va_acc
            val_loss_count = 0
        else:
            val_loss_count += 1

        should_stop = False

        if stop_mode in ('val_loss', 'both'):
            if val_loss_count >= patience:
                should_stop = True
                stop_reason = 'val_loss'
                stop_epoch = ep

        if stop_mode in ('crease', 'both'):
            if prev_cre is not None:
                rel_delta = abs(avg_cre - prev_cre) / max(avg_cre, 0.001)
                if rel_delta < crease_delta:
                    crease_stable_count += 1
                else:
                    crease_stable_count = 0
                if crease_stable_count >= cp:
                    if stop_mode == 'both':
                        if not should_stop:
                            should_stop = True
                            stop_reason = 'crease'
                            stop_epoch = ep
                    else:
                        should_stop = True
                        stop_reason = 'crease'
                        stop_epoch = ep

        prev_cre = avg_cre

        if should_stop:
            break

        if ep % 50 == 0 or ep == 1:
            print(f'  Ep {ep:3d} | loss={hist["loss"][-1]:.4f} | va_acc={va_acc:.4f} | crease={avg_cre:.3f}')

    hist['stop_epoch'] = stop_epoch
    hist['stop_reason'] = stop_reason
    hist['final_va_acc'] = float(best_va_acc)

    return hist


def run():
    print('=' * 70)
    print('EXPERIMENT 3: Early Stopping via Crease Stabilization')
    print('=' * 70)

    X, y = make_multiscale(6000)
    n = len(X)
    X_tr, y_tr = X[:3600], y[:3600]
    X_va, y_va = X[3600:4800], y[3600:4800]
    X_te, y_te = X[4800:], y[4800:]
    print(f'Data: {len(X_tr)} train, {len(X_va)} val, {len(X_te)} test')

    architectures = [
        ('Shallow (2L)', [2, 128, 128, 1]),
        ('Medium (3L)', [2, 64, 64, 64, 1]),
        ('Deep (5L)', [2, 32, 32, 32, 32, 32, 1]),
    ]
    stop_modes = [
        ('Full (baseline)', 'full'),
        ('Val Loss Plateau', 'val_loss'),
        ('Crease Stable', 'crease'),
        ('Both (first)', 'both'),
    ]

    results = {}
    max_ep = 500

    for arch_name, dims in architectures:
        print(f'\n=== {arch_name} ({len(dims)-1} layers) ===')
        results[arch_name] = {}

        for stop_label, stop_mode in stop_modes:
            np.random.seed(42)
            model = Net(dims)
            pat = max_ep if stop_mode == 'full' else 25
            cre_pat = 15
            cre_delta = 0.015
            print(f'\n  [{stop_label}]')
            h = train(model, X_tr, y_tr, X_va, y_va, lr=1e-3,
                      max_epochs=max_ep, stop_mode=stop_mode, patience=pat,
                      crease_patience=cre_pat, crease_delta=cre_delta)
            te_acc = accuracy(model, X_te, y_te)
            h['te_acc'] = float(te_acc)

            results[arch_name][stop_label] = h
            print(f'  >> Stopped at ep {h["stop_epoch"]} ({h["stop_reason"]}) | '
                  f'va_acc={h["final_va_acc"]:.4f} | te_acc={te_acc:.4f}')

    print('\n' + '=' * 70)
    print('SUMMARY')
    print('=' * 70)
    header = f'{"Architecture":<16} {"Mode":<20} {"Stop Ep":<8} {"Reason":<14} {"Val Acc":<10} {"Test Acc":<10}'
    print(header)
    print('-' * 78)
    for arch_name in [a[0] for a in architectures]:
        for stop_label, _ in stop_modes:
            h = results[arch_name][stop_label]
            print(f'{arch_name:<16} {stop_label:<20} {h["stop_epoch"]:<8} '
                  f'{h["stop_reason"]:<14} {h["final_va_acc"]:<10.4f} {h["te_acc"]:<10.4f}')
        print()

    crease_wins = 0
    val_wins = 0
    for arch_name in [a[0] for a in architectures]:
        cre_ep = results[arch_name]['Crease Stable']['stop_epoch']
        val_ep = results[arch_name]['Val Loss Plateau']['stop_epoch']
        cre_acc = results[arch_name]['Crease Stable']['te_acc']
        val_acc = results[arch_name]['Val Loss Plateau']['te_acc']
        if cre_ep <= val_ep and cre_acc >= val_acc - 0.01:
            crease_wins += 1
        if val_ep < cre_ep and val_acc >= cre_acc - 0.01:
            val_wins += 1
        print(f'  {arch_name}: crease@ep{cre_ep}({cre_acc:.3f}) vs val@ep{val_ep}({val_acc:.3f})')
    print(f'\nCrease stabilization wins: {crease_wins}/{len(architectures)}')
    print(f'Val loss plateau wins: {val_wins}/{len(architectures)}')

    summary = {}
    for arch_name in [a[0] for a in architectures]:
        summary[arch_name] = {}
        for stop_label, _ in stop_modes:
            h = results[arch_name][stop_label]
            summary[arch_name][stop_label] = {
                'stop_epoch': h['stop_epoch'],
                'stop_reason': h['stop_reason'],
                'va_acc': h['final_va_acc'],
                'te_acc': h['te_acc'],
                'epochs_saved': max_ep - h['stop_epoch'],
                'savings_pct': round(100.0 * (max_ep - h['stop_epoch']) / max_ep, 1),
            }

    export = {
        'summary': summary,
        'crease_wins': crease_wins,
        'val_wins': val_wins,
        'n_architectures': len(architectures),
        'max_epochs': max_ep,
        'history': {arch: {label: {
            'loss': results[arch][label]['loss'],
            'va_loss': results[arch][label]['va_loss'],
            'va_acc': results[arch][label]['va_acc'],
            'crease_density': results[arch][label]['crease_density'],
        } for label, _ in stop_modes} for arch in [a[0] for a in architectures]},
    }

    out_path = os.path.join(BASE_DIR, 'exp3_early_stop_results.json')
    with open(out_path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f'\n[EXPORTED] {out_path}')

    print('\nExperiment 3 complete.')


if __name__ == '__main__':
    run()
