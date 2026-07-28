#!/usr/bin/env python3
"""
Experiment 1: Crease-Aware Subgradient Selection
=================================================
Tests whether different subgradient choices at ReLU creases affect
training dynamics and generalization.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

np.random.seed(42)


# ============================
# 1. DATASET
# ============================
def make_ring_dataset(n=2000, noise=0.12):
    """Concentric rings — binary classification with crease-relevant geometry."""
    n0 = n // 2
    t0 = np.random.uniform(0, 2*np.pi, n0)
    r0 = np.random.uniform(0, 0.5, n0)
    x0 = np.column_stack([r0*np.cos(t0), r0*np.sin(t0)])

    n1 = n - n0
    t1 = np.random.uniform(0, 2*np.pi, n1)
    r1 = np.random.uniform(1.0, 1.5, n1)
    x1 = np.column_stack([r1*np.cos(t1), r1*np.sin(t1)])

    X = np.vstack([x0, x1])
    y = np.hstack([np.zeros(n0), np.ones(n1)])
    X += np.random.randn(n, 2) * noise
    idx = np.random.permutation(n)
    return X[idx], y[idx]


# ============================
# 2. NETWORK COMPONENTS
# ============================
class Layer:
    """Linear layer with stored momentum (for Adam)."""
    def __init__(self, fan_in, fan_out):
        self.W = np.random.randn(fan_in, fan_out) * np.sqrt(2.0 / fan_in)
        self.b = np.zeros(fan_out)
        self.reset_adam()

    def reset_adam(self):
        self.mW = np.zeros_like(self.W)
        self.vW = np.zeros_like(self.W)
        self.mb = np.zeros_like(self.b)
        self.vb = np.zeros_like(self.b)

    def forward(self, x):
        self.x = x
        return x @ self.W + self.b

    def backward(self, grad):
        self.dW = self.x.T @ grad
        self.db = grad.sum(axis=0)
        return grad @ self.W.T

    def update(self, lr, t, beta1=0.9, beta2=0.999, eps=1e-8):
        for p, m, v, g in [(self.W, self.mW, self.vW, self.dW),
                           (self.b, self.mb, self.vb, self.db)]:
            m[:] = beta1 * m + (1 - beta1) * g
            v[:] = beta2 * v + (1 - beta2) * (g ** 2)
            m_h = m / (1 - beta1 ** t)
            v_h = v / (1 - beta2 ** t)
            p -= lr * m_h / (np.sqrt(v_h) + eps)


def relu_forward(x):
    return np.maximum(x, 0)

def relu_backward(grad, x, mask_override=None):
    """If mask_override is provided, force those subgradient choices."""
    if mask_override is not None:
        return grad * mask_override
    return grad * (x > 0).astype(float)


# ============================
# 3. FORWARD / BACKWARD (manual, no class overhead)
# ============================
class Net:
    """Minimal 2-hidden-layer ReLU network using numpy arrays directly."""
    def __init__(self, dims):
        self.L = [Layer(dims[i], dims[i+1]) for i in range(len(dims)-1)]

    def forward(self, x):
        self.zs = []  # pre-activations (inputs to ReLU)
        self.acts = [x]  # post-activations
        h = x
        for i, layer in enumerate(self.L):
            z = layer.forward(h)
            self.zs.append(z)
            if i < len(self.L) - 1:
                h = relu_forward(z)
            else:
                h = z  # output: linear
            self.acts.append(h)
        return h  # logits

    def backward(self, grad, crease_mode='standard'):
        """
        Backprop with crease-aware subgradient selection.
        crease_mode: 'standard' | 'always_on' | 'always_off' | 'random'
        """
        n_layers = len(self.L)
        for i in range(n_layers - 1, -1, -1):
            if i < n_layers - 1:
                # Hidden layer: apply ReLU backward
                z = self.zs[i]
                if crease_mode == 'standard':
                    mask = (z > 0).astype(float)
                elif crease_mode == 'always_on':
                    mask = np.ones_like(z)
                elif crease_mode == 'always_off':
                    mask = (z > 0).astype(float)  # same as standard
                elif crease_mode == 'random':
                    mask = (z > 0).astype(float)
                    # At crease, randomly pick 0 or 1
                    at_crease = (np.abs(z) < 1e-10)
                    if at_crease.any():
                        mask[at_crease] = np.random.randint(0, 2, size=at_crease.sum()).astype(float)
                grad = grad * mask
            # Linear layer backward
            grad = self.L[i].backward(grad)
        return grad

    def update(self, lr, step):
        for layer in self.L:
            layer.update(lr, step)

    def count_creases(self, x):
        """Count activations near 0."""
        h = x
        total = 0
        for i, layer in enumerate(self.L[:-1]):
            h = layer.forward(h)
            total += (np.abs(h) < 1e-6).sum()
            h = relu_forward(h)
        return total

    def reset_adam(self):
        for l in self.L:
            l.reset_adam()


# ============================
# 4. TRAINING
# ============================
def bce_with_logits(logits, y):
    """Numerically stable BCE loss."""
    return np.mean(np.maximum(logits, 0) - logits * y + np.log(1 + np.exp(-np.abs(logits))))

def train(model, X, y, X_test, y_test, mode='standard',
          lr=3e-4, epochs=200, batch_size=128, verbose=True):
    n = len(X)
    losses, accs, creases = [], [], []
    best_acc = 0.0
    step_counter = 0

    for ep in range(1, epochs + 1):
        idx = np.random.permutation(n)
        ep_loss = 0.0
        ep_cre = 0
        nb = 0

        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            Xb = X[idx[start:end]]
            yb = y[idx[start:end]]
            step_counter += 1

            logits = model.forward(Xb)
            loss = bce_with_logits(logits, yb.reshape(-1, 1))

            # Gradient of BCE w.r.t. logits
            y_pred = 1.0 / (1.0 + np.exp(-logits))
            grad = y_pred - yb.reshape(-1, 1)

            # Count creases
            ep_cre += model.count_creases(Xb)
            nb += 1

            model.backward(grad, mode)
            model.update(lr, step_counter)

            ep_loss += loss

        # Eval
        test_logits = model.forward(X_test)
        test_pred = 1.0 / (1.0 + np.exp(-test_logits))
        acc = np.mean((test_pred > 0.5).ravel() == y_test)
        best_acc = max(best_acc, acc)

        avg_loss = ep_loss / nb
        avg_cre = ep_cre / nb
        losses.append(avg_loss)
        accs.append(acc)
        creases.append(avg_cre)

        if verbose and (ep % 50 == 0 or ep == 1):
            print(f'  Ep {ep:3d} | loss={avg_loss:.4f} | test_acc={acc:.4f} | cre/batch={avg_cre:.1f}')

    return losses, accs, creases, best_acc


# ============================
# 5. MAIN: Experiment 1
# ============================
def run_experiment():
    print('=' * 70)
    print('EXPERIMENT 1: Crease-Aware Subgradient Selection')
    print('=' * 70)

    # Data
    print('\nGenerating ring dataset...')
    X, y = make_ring_dataset(3000, noise=0.12)
    split = int(0.8 * len(X))
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]
    print(f'Train: {len(X_tr)}, Test: {len(X_te)}')

    # Normalize
    m, s = X_tr.mean(0), X_tr.std(0)
    X_tr = (X_tr - m) / s
    X_te = (X_te - m) / s

    # Plot data
    plt.figure(figsize=(7, 5))
    plt.scatter(X_tr[y_tr==0,0], X_tr[y_tr==0,1], c='#2196F3', alpha=0.4, s=8)
    plt.scatter(X_tr[y_tr==1,0], X_tr[y_tr==1,1], c='#F44336', alpha=0.4, s=8)
    plt.title('Ring Dataset (2D binary classification)')
    plt.savefig('exp1_dataset.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved exp1_dataset.png')

    # Run strategies
    dims = [2, 64, 64, 1]
    modes = ['standard', 'random', 'always_on']
    colors = {'standard': '#2196F3', 'random': '#FF9800', 'always_on': '#4CAF50'}
    results = {}

    print('\nTraining with different subgradient strategies...')
    print('-' * 60)

    for mode in modes:
        print(f'\n--- Mode: {mode.upper()} ---')
        np.random.seed(42)
        model = Net(dims)
        l, a, c, ba = train(model, X_tr, y_tr, X_te, y_te, mode=mode,
                           lr=1e-3, epochs=300)
        results[mode] = {'losses': l, 'accs': a, 'creases': c, 'best_acc': ba, 'final_acc': a[-1]}
        print(f'  >> Best: {ba:.4f}  Final: {a[-1]:.4f}  Final loss: {l[-1]:.4f}')

    # Summary
    print('\n' + '=' * 70)
    print('RESULTS')
    print('=' * 70)
    print(f'{"Mode":<12} {"Best Acc":<10} {"Final Acc":<10} {"Final Loss":<10} {"Avg Crease":<10}')
    print('-' * 52)
    for mode in modes:
        r = results[mode]
        ac = np.mean(r['creases'])
        print(f'{mode:<12} {r["best_acc"]:<10.4f} {r["final_acc"]:<10.4f} {r["losses"][-1]:<10.4f} {ac:<10.1f}')

    # Plots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for mode in modes:
        c = colors[mode]
        axes[0].plot(results[mode]['losses'], color=c, label=mode.upper(), lw=1.5)
        axes[1].plot(results[mode]['accs'], color=c, label=mode.upper(), lw=1.5)
        axes[2].plot(results[mode]['creases'], color=c, label=mode.upper(), lw=1.5)

    axes[0].set_title('Training Loss (BCE)')
    axes[0].set_xlabel('Epoch')
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].set_title('Test Accuracy')
    axes[1].set_xlabel('Epoch')
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    axes[2].set_title('Creases per Batch')
    axes[2].set_xlabel('Epoch')
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('exp1_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('\nSaved exp1_results.png')

    # Fold-depth analysis snapshot
    print('\n--- Fold Depth Analysis ---')
    np.random.seed(42)
    probe = Net(dims)
    _ = probe.forward(X_tr[:256])
    crease_count = probe.count_creases(X_tr[:256])
    print(f'Creases in forward pass (batch=256): {crease_count} '
          f'(avg {crease_count/256:.2f}/sample)')
    print(f'Ratio: {crease_count/(256*64*2):.4f} of all ReLU units activated at crease')

    print('\nExperiment 1 complete.')


if __name__ == '__main__':
    run_experiment()
