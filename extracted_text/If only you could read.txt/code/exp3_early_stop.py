#!/usr/bin/env python3
"""
Experiment 3: Early Stopping via Crease Stabilization
======================================================
Tests the Puno Calculus prediction: when crease density stabilizes
(units stop toggling between on/off states), the network's partition
of input space has converged, making further training unnecessary.

Compares three strategies:
  A) Standard: early stop on validation loss plateau
  B) Crease:   early stop on crease density stabilization
  C) Full:     train full budget (baseline)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

# ============================
# 1. DATA
# ============================
def make_multiscale(n=4000):
    """Checkerboard with coarse outer / fine inner."""
    X = np.random.uniform(-5, 5, (n, 2))
    coarse = ((np.floor(X[:,0] * 0.4) + np.floor(X[:,1] * 0.4)) % 2)
    fine_mask = (np.abs(X[:,0]) < 2) & (np.abs(X[:,1]) < 2)
    fine = ((np.floor(X[:,0] * 1.5) + np.floor(X[:,1] * 1.5)) % 2)
    y = coarse.copy()
    y[fine_mask] = fine[fine_mask]
    flip = np.random.random(n) < 0.02
    y[flip] = 1 - y[flip]
    return X, y

# ============================
# 2. NETWORK
# ============================
CREASE_THRESH = 0.05

class Net:
    def __init__(self, dims):
        self.L = []
        for i in range(len(dims)-1):
            fan_in, fan_out = dims[i], dims[i+1]
            W = np.random.randn(fan_in, fan_out) * np.sqrt(2.0 / fan_in)
            b = np.zeros(fan_out)
            self.L.append({'W': W, 'b': b,
                          'mW': np.zeros_like(W), 'vW': np.zeros_like(W),
                          'mb': np.zeros_like(b), 'vb': np.zeros_like(b)})

    def forward(self, x, track_creases=False):
        self.zs = []
        self.acts = [x]
        h = x
        crease_count = 0
        for i, layer in enumerate(self.L):
            z = h @ layer['W'] + layer['b']
            self.zs.append(z)
            if i < len(self.L) - 1:
                mask = (z > 0).astype(float)
                if track_creases:
                    crease_count += (np.abs(z) < CREASE_THRESH).sum()
                h = z * mask
            else:
                h = z
            self.acts.append(h)
        return h, crease_count

    def backward(self, grad):
        n = len(self.L)
        self.grads = []
        for i in range(n - 1, -1, -1):
            if i < n - 1:
                mask = (self.zs[i] > 0).astype(float)
                grad = grad * mask
            layer = self.L[i]
            x_in = self.acts[i]
            dW = x_in.T @ grad
            db = grad.sum(axis=0)
            self.grads.insert(0, {'dW': dW, 'db': db})
            if i > 0:
                grad = grad @ layer['W'].T

    def update(self, lr, t, beta1=0.9, beta2=0.999, eps=1e-8):
        for i, layer in enumerate(self.L):
            g = self.grads[i]
            for pk, mk, vk in [('W','mW','vW'), ('b','mb','vb')]:
                p = layer[pk]; m = layer[mk]; v = layer[vk]
                gv = g['d' + pk]
                m[:] = beta1*m + (1-beta1)*gv
                v[:] = beta2*v + (1-beta2)*(gv**2)
                mh = m/(1-beta1**t); vh = v/(1-beta2**t)
                p -= lr * mh / (np.sqrt(vh) + eps)

# ============================
# 3. BCE LOSS
# ============================
def bce(logits, y):
    return np.mean(np.maximum(logits,0) - logits*y + np.log(1+np.exp(-np.abs(logits))))

# ============================
# 4. TRAINING WITH EARLY STOP
# ============================
def accuracy(model, X, y):
    logits, _ = model.forward(X)
    preds = 1.0/(1.0+np.exp(-logits))
    return np.mean((preds > 0.5).ravel() == y)

def train(model, X_tr, y_tr, X_va, y_va, lr=1e-3, max_epochs=500, batch=128,
          stop_mode='full', patience=30, crease_patience=None, crease_delta=0.008):
    """
    stop_mode: 'full' (no stop), 'val_loss', 'crease', 'both'
    Returns dict with full training history and stopping info.
    """
    n = len(X_tr)
    hist = {'loss': [], 'va_loss': [], 'va_acc': [], 'crease_density': []}
    step = 0
    best_va_loss = float('inf')
    best_va_acc = 0.0
    stop_epoch = max_epochs
    stop_reason = 'max_epochs'

    # For crease stabilization: track rate of change
    prev_cre = None
    crease_stable_count = 0
    cp = crease_patience if crease_patience else patience
    # For val loss plateau
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
            loss = bce(logits, yb.reshape(-1,1))
            y_pred = 1.0/(1.0+np.exp(-logits))
            grad = y_pred - yb.reshape(-1,1)

            ep_cre += creases / batch
            nb += 1

            model.backward(grad)
            model.update(lr, step)
            ep_loss += loss

        # Validation
        va_logits, _ = model.forward(X_va)
        va_loss = bce(va_logits, y_va.reshape(-1,1))
        va_acc = accuracy(model, X_va, y_va)

        avg_cre = ep_cre / nb
        hist['loss'].append(ep_loss / nb)
        hist['va_loss'].append(va_loss)
        hist['va_acc'].append(va_acc)
        hist['crease_density'].append(avg_cre)

        if va_loss < best_va_loss:
            best_va_loss = va_loss
            best_va_acc = va_acc
            val_loss_count = 0
        else:
            val_loss_count += 1

        # === EARLY STOP CHECKS ===
        should_stop = False

        if stop_mode in ('val_loss', 'both'):
            if val_loss_count >= patience:
                should_stop = True
                stop_reason = 'val_loss'
                stop_epoch = ep

        if stop_mode in ('crease', 'both'):
            if prev_cre is not None:
                # Relative delta: what fraction of crease density changed
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

    # Post-training: evaluate on all data to get clean test estimate
    # But we don't have a separate test set here; use validation as proxy
    final_va_acc = best_va_acc

    hist['stop_epoch'] = stop_epoch
    hist['stop_reason'] = stop_reason
    hist['final_va_acc'] = final_va_acc

    return hist

# ============================
# 5. MAIN
# ============================
def run():
    print('=' * 70)
    print('EXPERIMENT 3: Early Stopping via Crease Stabilization')
    print('=' * 70)

    # Data
    X, y = make_multiscale(6000)
    # 60/20/20 split: train/val/test
    n = len(X)
    X_tr, y_tr = X[:3600], y[:3600]
    X_va, y_va = X[3600:4800], y[3600:4800]
    X_te, y_te = X[4800:], y[4800:]
    print(f'Data: {len(X_tr)} train, {len(X_va)} val, {len(X_te)} test')

    architectures = [
        ('Shallow (2L)', [2, 128, 128, 1]),
        ('Medium (3L)',  [2, 64, 64, 64, 1]),
        ('Deep (5L)',    [2, 32, 32, 32, 32, 32, 1]),
    ]
    stop_modes = [
        ('Full (baseline)', 'full'),
        ('Val Loss Plateau', 'val_loss'),
        ('Crease Stable',    'crease'),
        ('Both (first)',     'both'),
    ]

    results = {}
    max_ep = 500

    for arch_name, dims in architectures:
        print(f'\n=== {arch_name} ({len(dims)-1} layers) ===')
        results[arch_name] = {}

        for stop_label, stop_mode in stop_modes:
            # Re-init with same seed for fair comparison
            np.random.seed(42)
            model = Net(dims)
            # Adjust patience
            pat = max_ep if stop_mode == 'full' else 25
            cre_pat = 15  # shorter patience for crease
            cre_delta = 0.015  # 1.5% relative change threshold
            print(f'\n  [{stop_label}]')
            h = train(model, X_tr, y_tr, X_va, y_va, lr=1e-3,
                      max_epochs=max_ep, stop_mode=stop_mode, patience=pat,
                      crease_patience=cre_pat, crease_delta=cre_delta)
            # Final test accuracy
            te_acc = accuracy(model, X_te, y_te)
            h['te_acc'] = te_acc

            results[arch_name][stop_label] = h
            print(f'  >> Stopped at ep {h["stop_epoch"]} ({h["stop_reason"]}) | '
                  f'va_acc={h["final_va_acc"]:.4f} | te_acc={te_acc:.4f}')

    # ============================
    # 6. SUMMARY
    # ============================
    print('\n' + '=' * 70)
    print('SUMMARY: Stopping Epoch and Accuracy')
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

    # ============================
    # 7. PLOT
    # ============================
    fig, axes = plt.subplots(3, 4, figsize=(20, 14))
    colors = {'Full (baseline)': '#1f77b4', 'Val Loss Plateau': '#ff7f0e',
              'Crease Stable': '#2ca02c', 'Both (first)': '#d62728'}

    for row, (arch_name, _) in enumerate(architectures):
        for col, (metric, label) in enumerate([
            ('loss', 'Train Loss'), ('va_acc', 'Val Accuracy'),
            ('crease_density', 'Crease Density'), ('diff', 'Delta Crease/Ep')
        ]):
            ax = axes[row, col]
            for stop_label, _ in stop_modes:
                h = results[arch_name][stop_label]
                c = colors[stop_label]
                if metric == 'diff':
                    cre = np.array(h['crease_density'])
                    diffs = np.abs(np.diff(cre))
                    ax.plot(diffs, color=c, lw=1.2, alpha=0.8, label=stop_label)
                    stop_ep = h['stop_epoch']
                    if stop_ep < len(diffs):
                        ax.axvline(stop_ep, color=c, ls='--', lw=1, alpha=0.6)
                    ax.set_ylabel('|Delta Crease|')
                else:
                    ax.plot(h[metric], color=c, lw=1.5, label=stop_label)
                    stop_ep = h['stop_epoch']
                    if stop_ep < len(h[metric]):
                        ax.axvline(stop_ep, color=c, ls='--', lw=1, alpha=0.6)
                    ax.set_ylabel(metric)

            ax.set_xlabel('Epoch')
            ax.set_title(f'{arch_name} — {label}')
            ax.legend(fontsize=7)
            ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('exp3_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('\nSaved exp3_results.png')

    # Puno Calculus interpretation
    print('\n--- Puno Calculus Interpretation ---')
    print('If crease stabilization predicts convergence better than (or as')
    print('well as) validation loss plateau, it provides a training diagnostic')
    print('that does not require labels — useful for self-supervised/online learning.')
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

    print('\nExperiment 3 complete.')

if __name__ == '__main__':
    run()
