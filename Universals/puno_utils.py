"""
puno_utils.py

Shared utilities for Puno Calculus experiments.

Provides the Net class, training loop, dataset generators, and OOD scoring
used by exp1, exp1b, exp2, exp3, demo_ood, and exp_pruning.

From the Book of Puno, Appendix B.
"""

import numpy as np

CREASE_THRESH = 0.05  # |z| < 0.05 ≈ 4% of N(0,1) pre-activations detected as creases


# ---------------------------------------------------------------------------
# Dataset generators
# ---------------------------------------------------------------------------

def make_ring_dataset(n=2000, noise=0.12):
    """Concentric rings -- binary classification with crease-relevant geometry."""
    n0 = n // 2
    t0 = np.random.uniform(0, 2 * np.pi, n0)
    r0 = np.random.uniform(0, 0.5, n0)
    x0 = np.column_stack([r0 * np.cos(t0), r0 * np.sin(t0)])

    n1 = n - n0
    t1 = np.random.uniform(0, 2 * np.pi, n1)
    r1 = np.random.uniform(1.0, 1.5, n1)
    x1 = np.column_stack([r1 * np.cos(t1), r1 * np.sin(t1)])

    X = np.vstack([x0, x1])
    y = np.hstack([np.zeros(n0), np.ones(n1)])
    X += np.random.randn(n, 2) * noise
    idx = np.random.permutation(n)
    return X[idx], y[idx]


def make_multiscale(n=4000):
    """Checkerboard with both coarse and fine cells."""
    X = np.random.uniform(-5, 5, (n, 2))
    coarse = ((np.floor(X[:, 0] * 0.4) + np.floor(X[:, 1] * 0.4)) % 2)
    fine_mask = (np.abs(X[:, 0]) < 2) & (np.abs(X[:, 1]) < 2)
    fine = ((np.floor(X[:, 0] * 1.5) + np.floor(X[:, 1] * 1.5)) % 2)
    y = coarse.copy()
    y[fine_mask] = fine[fine_mask]
    flip = np.random.random(n) < 0.02
    y[flip] = 1 - y[flip]
    return X, y


# ---------------------------------------------------------------------------
# Network class (dict-based layers with Adam)
# ---------------------------------------------------------------------------

class Net:
    """Minimal ReLU network using numpy arrays directly.

    Each layer is a dict: {'W', 'b', 'mW', 'vW', 'mb', 'vb'}.
    """

    def __init__(self, dims):
        self.L = []
        for i in range(len(dims) - 1):
            fan_in, fan_out = dims[i], dims[i + 1]
            W = np.random.randn(fan_in, fan_out) * np.sqrt(2.0 / fan_in)
            b = np.zeros(fan_out)
            self.L.append({
                'W': W, 'b': b,
                'mW': np.zeros_like(W), 'vW': np.zeros_like(W),
                'mb': np.zeros_like(b), 'vb': np.zeros_like(b),
            })

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
            for pk, mk, vk in [('W', 'mW', 'vW'), ('b', 'mb', 'vb')]:
                p = layer[pk]
                m = layer[mk]
                v = layer[vk]
                gv = g['d' + pk]
                m[:] = beta1 * m + (1 - beta1) * gv
                v[:] = beta2 * v + (1 - beta2) * (gv ** 2)
                mh = m / (1 - beta1 ** t)
                vh = v / (1 - beta2 ** t)
                p -= lr * mh / (np.sqrt(vh) + eps)

    def copy(self):
        """Deep copy of the network."""
        import copy
        return copy.deepcopy(self)


# ---------------------------------------------------------------------------
# Loss and accuracy
# ---------------------------------------------------------------------------

def bce(logits, y):
    """Numerically stable BCE loss."""
    logits = np.asarray(logits).ravel()
    y = np.asarray(y).ravel()
    return np.mean(np.maximum(logits, 0) - logits * y + np.log(1 + np.exp(-np.abs(logits))))


def accuracy(model, X, y):
    """Classification accuracy."""
    logits, _ = model.forward(X)
    probs = 1.0 / (1.0 + np.exp(-logits))
    return np.mean((probs.ravel() > 0.5) == y)


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------

def train_model(model, X, y, X_val, y_val, lr=1e-3, epochs=300, batch_size=128,
                crease_mode='standard', verbose=True):
    """Train a Net model with BCE loss and Adam optimizer.

    Returns dict with loss, acc, crease_density history.
    """
    n = len(X)
    hist = {'loss': [], 'acc': [], 'crease_density': []}
    step = 0

    for ep in range(1, epochs + 1):
        idx = np.random.permutation(n)
        ep_loss = 0
        ep_cre = 0
        nb = 0

        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            Xb = X[idx[start:end]]
            yb = y[idx[start:end]]
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

        te_logits, _ = model.forward(X_val)
        te_pred = 1.0 / (1.0 + np.exp(-te_logits))
        acc = np.mean((te_pred.ravel() > 0.5) == y_val)

        hist['loss'].append(ep_loss / nb)
        hist['acc'].append(acc)
        hist['crease_density'].append(ep_cre / nb)

        if verbose and (ep % 50 == 0 or ep == 1):
            print(f'  Ep {ep:3d} | loss={hist["loss"][-1]:.4f} | acc={acc:.4f} | crease={hist["crease_density"][-1]:.2f}')

    hist['best_acc'] = max(hist['acc']) if hist['acc'] else 0.0
    return hist


# ---------------------------------------------------------------------------
# OOD Scorer
# ---------------------------------------------------------------------------

class OODScorer:
    """Compute per-sample crease density as an OOD score.

    High crease density = many near-threshold units = likely OOD.
    """

    def __init__(self, model, epsilon=0.05):
        self.model = model
        self.epsilon = epsilon

    def score_sample(self, x):
        """Score a single sample. Returns (raw_pre_activations, crease_density)."""
        h = np.atleast_2d(x)
        all_z = []
        for i, layer in enumerate(self.model.L):
            z = h @ layer['W'] + layer['b']
            if i < len(self.model.L) - 1:
                all_z.append(z)
                h = z * (z > 0).astype(float)
        all_z = np.concatenate(all_z, axis=1)
        near_crease = (np.abs(all_z) < self.epsilon).astype(float)
        density = near_crease.mean(axis=1)
        return all_z, density

    def score_batch(self, X):
        """Score a batch. Returns (raw_array, density_array)."""
        h = np.atleast_2d(X)
        all_z = []
        for i, layer in enumerate(self.model.L):
            z = h @ layer['W'] + layer['b']
            if i < len(self.model.L) - 1:
                all_z.append(z)
                h = z * (z > 0).astype(float)
        all_z = np.concatenate(all_z, axis=1)
        near_crease = (np.abs(all_z) < self.epsilon).astype(float)
        density = near_crease.mean(axis=1)
        return all_z, density


# ---------------------------------------------------------------------------
# Boundary complexity
# ---------------------------------------------------------------------------

def boundary_complexity(model, res=100):
    """Measure decision boundary crossings on a grid."""
    x = np.linspace(-5, 5, res)
    y = np.linspace(-5, 5, res)
    Xg, Yg = np.meshgrid(x, y)
    grid = np.column_stack([Xg.ravel(), Yg.ravel()])
    logits, _ = model.forward(grid)
    preds = (logits > 0).astype(float).reshape(res, res)
    h_cross = np.sum(preds[:, 1:] != preds[:, :-1])
    v_cross = np.sum(preds[1:, :] != preds[:-1, :])
    return int(h_cross + v_cross)


# ---------------------------------------------------------------------------
# AUROC
# ---------------------------------------------------------------------------

def auroc(score_id, score_ood):
    """Compute AUROC between ID and OOD score arrays."""
    scores = np.concatenate([score_id, score_ood])
    labels = np.concatenate([np.ones(len(score_id)), np.zeros(len(score_ood))])
    order = np.argsort(scores)[::-1]
    labels_sorted = labels[order]
    pos = labels_sorted.sum()
    neg = len(labels_sorted) - pos
    if pos == 0 or neg == 0:
        return 0.5
    tpr = np.cumsum(labels_sorted) / pos
    fpr = np.cumsum(1 - labels_sorted) / neg
    auc = np.trapezoid(tpr, fpr)
    return max(auc, 1 - auc)
