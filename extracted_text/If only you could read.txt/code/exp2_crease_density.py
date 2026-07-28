#!/usr/bin/env python3
"""
Experiment 2: Crease Density and Decision Boundary Complexity
==============================================================
Tests the Puno Calculus prediction: networks with higher crease density
(more units operating near their switching threshold) develop more
fragmented decision boundaries that capture fine-grained structure,
while low-crease-density networks produce smoother boundaries.

Tests on a multi-scale checkerboard problem with both coarse and fine regions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

# ============================
# 1. MULTI-SCALE CHECKERBOARD
# ============================
def make_multiscale(n=4000):
    """Checkerboard with both coarse and fine cells."""
    X = np.random.uniform(-5, 5, (n, 2))
    # Coarse grid (2x2 cells)
    coarse = ((np.floor(X[:,0] * 0.4) + np.floor(X[:,1] * 0.4)) % 2)
    # Fine grid in center region (4x4 cells)
    fine_mask = (np.abs(X[:,0]) < 2) & (np.abs(X[:,1]) < 2)
    fine = ((np.floor(X[:,0] * 1.5) + np.floor(X[:,1] * 1.5)) % 2)
    y = coarse.copy()
    y[fine_mask] = fine[fine_mask]
    # Add small noise
    flip = np.random.random(n) < 0.02
    y[flip] = 1 - y[flip]
    return X, y


# ============================
# 2. NETWORK WITH CREASE TRACKING
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
        crease_mask_total = np.zeros(x.shape[0])
        for i, layer in enumerate(self.L):
            z = h @ layer['W'] + layer['b']
            self.zs.append(z)
            if i < len(self.L) - 1:
                mask = (z > 0).astype(float)
                if track_creases:
                    at_crease = (np.abs(z) < CREASE_THRESH)
                    crease_mask_total += at_crease.sum(axis=1)
                h = z * mask
            else:
                h = z
            self.acts.append(h)
        return h, crease_mask_total

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
                p -= lr * mh / (np.sqrt(vh) + 1e-8)


# ============================
# 3. TRAINING
# ============================
def bce(logits, y):
    return np.mean(np.maximum(logits,0) - logits*y + np.log(1+np.exp(-np.abs(logits))))

def train(model, X, y, X_te, y_te, lr=1e-3, epochs=300, batch=128):
    n = len(X)
    hist = {'loss': [], 'acc': [], 'crease_density': []}
    best_acc = 0
    step = 0

    for ep in range(1, epochs+1):
        idx = np.random.permutation(n)
        ep_loss = 0
        ep_cre = 0
        nb = 0

        for start in range(0, n, batch):
            end = min(start+batch, n)
            Xb = X[idx[start:end]]
            yb = y[idx[start:end]]
            step += 1

            logits, creases = model.forward(Xb, track_creases=True)
            loss = bce(logits, yb.reshape(-1,1))
            y_pred = 1.0/(1.0+np.exp(-logits))
            grad = y_pred - yb.reshape(-1,1)

            ep_cre += creases.mean()
            nb += 1

            model.backward(grad)
            model.update(lr, step)
            ep_loss += loss

        te_logits, _ = model.forward(X_te)
        te_pred = 1.0/(1.0+np.exp(-te_logits))
        acc = np.mean((te_pred>0.5).ravel() == y_te)
        best_acc = max(best_acc, acc)

        hist['loss'].append(ep_loss/nb)
        hist['acc'].append(acc)
        hist['crease_density'].append(ep_cre/nb)

        if ep % 50 == 0 or ep == 1:
            print(f'  Ep {ep:3d} | loss={hist["loss"][-1]:.4f} | '
                  f'acc={acc:.4f} | crease_density={hist["crease_density"][-1]:.2f}')

    hist['best_acc'] = best_acc
    return hist


# ============================
# 4. DECISION BOUNDARY COMPLEXITY
# ============================
def boundary_complexity(model, res=100):
    """Measure how many times the decision boundary changes sign along a grid."""
    x = np.linspace(-5, 5, res)
    y = np.linspace(-5, 5, res)
    Xg, Yg = np.meshgrid(x, y)
    grid = np.column_stack([Xg.ravel(), Yg.ravel()])
    logits, _ = model.forward(grid)
    preds = (logits > 0).astype(float).reshape(res, res)
    # Count boundary crossings between adjacent cells
    h_cross = np.sum(preds[:,1:] != preds[:,:-1])
    v_cross = np.sum(preds[1:,:] != preds[:-1,:])
    return h_cross + v_cross


# ============================
# 5. MAIN
# ============================
def run():
    print('=' * 70)
    print('EXPERIMENT 2: Crease Density & Decision Boundary Complexity')
    print('=' * 70)

    # Data
    X, y = make_multiscale(5000)
    split = int(0.8 * len(X))
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]
    print(f'Data: {len(X_tr)} train, {len(X_te)} test')
    print(f'  Multi-scale checkerboard (coarse outer, fine inner)')

    # Test different depths
    architectures = [
        ('Shallow (1 layer)', [2, 256, 1]),
        ('Medium (2 layers)', [2, 128, 128, 1]),
        ('Deep (4 layers)',  [2, 64, 64, 64, 64, 1]),
        ('Wide-shallow',     [2, 512, 1]),
        ('Narrow-deep',      [2, 32, 32, 32, 32, 1]),
    ]
    results = {}

    print(f'\nTrain on multi-scale checkerboard...')
    print('-' * 70)

    for name, dims in architectures:
        print(f'\n--- {name} ({len(dims)-1} layers, params={sum(dims[i]*dims[i+1] for i in range(len(dims)-1))}) ---')
        np.random.seed(42)
        model = Net(dims)
        h = train(model, X_tr, y_tr, X_te, y_te, lr=1e-3, epochs=300)

        # Measure boundary complexity
        comp = boundary_complexity(model)
        avg_cre = np.mean(h['crease_density'])

        results[name] = {**h, 'complexity': comp, 'avg_crease': avg_cre,
                        'n_layers': len(dims)-1,
                        'n_params': sum(dims[i]*dims[i+1] for i in range(len(dims)-1))}
        print(f'  >> Acc={h["best_acc"]:.4f} | Boundary crossings={comp} | '
              f'Crease density={avg_cre:.2f}')

    # Summary
    print('\n' + '=' * 70)
    print('FINAL RESULTS')
    print('=' * 70)
    print(f'{"Architecture":<20} {"Best Acc":<10} {"Boundary":<10} {"Crease Dens":<12} {"Layers":<8} {"Params":<8}')
    print('-' * 68)
    for name, r in results.items():
        print(f'{name:<20} {r["best_acc"]:<10.4f} {r["complexity"]:<10} {r["avg_crease"]:<12.2f} '
              f'{r["n_layers"]:<8} {r["n_params"]:<8}')

    # Plot
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(results)))

    for idx, (name, r) in enumerate(results.items()):
        c = colors[idx]
        # Loss
        axes[0,0].plot(r['loss'], color=c, label=name, lw=1.5)
        # Accuracy
        axes[0,1].plot(r['acc'], color=c, label=name, lw=1.5)
        # Crease density
        axes[0,2].plot(r['crease_density'], color=c, label=name, lw=1.5)
        # Scatter: crease density vs complexity
        axes[1,0].scatter(r['avg_crease'], r['complexity'], color=c, s=80, label=name)
        # Scatter: layers vs complexity
        axes[1,1].scatter(r['n_layers'], r['complexity'], color=c, s=80, label=name)
        # Crease density vs accuracy
        axes[1,2].scatter(r['avg_crease'], r['best_acc'], color=c, s=80, label=name)

    axes[0,0].set_title('Training Loss')
    axes[0,0].set_xlabel('Epoch')
    axes[0,0].legend(fontsize=8)
    axes[0,0].grid(alpha=0.3)

    axes[0,1].set_title('Test Accuracy')
    axes[0,1].set_xlabel('Epoch')
    axes[0,1].legend(fontsize=8)
    axes[0,1].grid(alpha=0.3)

    axes[0,2].set_title('Crease Density (avg near-crease units/step)')
    axes[0,2].set_xlabel('Epoch')
    axes[0,2].legend(fontsize=8)
    axes[0,2].grid(alpha=0.3)

    axes[1,0].set_title('Crease Density vs Boundary Complexity')
    axes[1,0].set_xlabel('Avg Crease Density')
    axes[1,0].set_ylabel('Boundary Crossings')
    axes[1,0].grid(alpha=0.3)

    axes[1,1].set_title('Network Depth vs Boundary Complexity')
    axes[1,1].set_xlabel('Number of Layers')
    axes[1,1].set_ylabel('Boundary Crossings')
    axes[1,1].grid(alpha=0.3)

    axes[1,2].set_title('Crease Density vs Accuracy')
    axes[1,2].set_xlabel('Avg Crease Density')
    axes[1,2].set_ylabel('Best Test Accuracy')
    axes[1,2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('exp2_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('\nSaved exp2_results.png')

    # Puno Calculus interpretation
    print('\n--- Puno Calculus Interpretation ---')
    print('Fold depth prediction: deeper networks (more ReLU folds) should')
    print('produce more complex decision boundaries, but crease density')
    print('(how many units are actively folding at any given input) should')
    print('be a better predictor of boundary complexity than layer count alone.')
    print()
    # Correlation check
    from scipy.stats import pearsonr
    names_l = list(results.keys())
    cre_dens = np.array([results[n]['avg_crease'] for n in names_l])
    comps = np.array([results[n]['complexity'] for n in names_l])
    layers = np.array([results[n]['n_layers'] for n in names_l])
    params = np.array([results[n]['n_params'] for n in names_l])
    accs = np.array([results[n]['best_acc'] for n in names_l])

    if len(names_l) >= 3:
        c_cre, _ = pearsonr(cre_dens, comps)
        c_lay, _ = pearsonr(layers, comps)
        c_par, _ = pearsonr(params, comps)
        print(f'Correlation: crease_density vs complexity  = {c_cre:+.4f}')
        print(f'Correlation: layer_count    vs complexity  = {c_lay:+.4f}')
        print(f'Correlation: param_count    vs complexity  = {c_par:+.4f}')
        if abs(c_cre) > abs(c_lay):
            print('✓ Crease density predicts boundary complexity BETTER than layer count')
        else:
            print('— Layer count predicts boundary complexity as well or better than crease density')

    print('\nExperiment 2 complete.')


if __name__ == '__main__':
    run()
