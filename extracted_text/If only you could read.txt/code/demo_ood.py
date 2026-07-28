#!/usr/bin/env python3
"""
Demo: OOD Detection via Crease Density
========================================
Tests whether OOD inputs produce higher crease density than in-distribution
inputs. The hypothesis: inputs landing near many ReLU creases are likely OOD,
because the network has not learned decisive activation patterns for them.

Compares crease density vs. maximum softmax probability (MSP) baseline.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

from puno_utils import Net, accuracy, bce, train_model, make_multiscale, OODScorer

np.random.seed(42)

# ============================
# 1. TRAIN MODEL
# ============================
print('=' * 70)
print('OOD DETECTION VIA CREASE DENSITY')
print('=' * 70)

X, y = make_multiscale(6000)
X_tr, y_tr = X[:3600], y[:3600]
X_id, y_id = X[3600:4800], y[3600:4800]  # in-distribution validation

model = Net([2, 64, 64, 1])
print('\nTraining model...')
train_model(model, X_tr, y_tr, X_id, y_id, lr=1e-3, epochs=300)
print(f'Final ID accuracy: {accuracy(model, X_id, y_id):.4f}')

# ============================
# 2. BUILD OOD SCORER
# ============================
scorer = OODScorer(model, epsilon=0.05)

# ============================
# 3. GENERATE OOD DATASETS
# ============================
n_ood = len(X_id)

# OOD Type 1: Uniform noise (far-OOD)
X_ood_unif = np.random.uniform(-10, 10, (n_ood, 2))

# OOD Type 2: Gaussian blob far from data
X_ood_gauss = np.random.randn(n_ood, 2) * 3 + np.array([15, 15])

# OOD Type 3: Near-OOD (shifted checkerboard — similar structure, different phase)
X_ood_near = np.random.uniform(-5, 5, (n_ood, 2))
# Same distributional support but shifted boundaries

# OOD Type 4: Concentrated noise in center (ambiguous region)
X_ood_center = np.random.uniform(-1, 1, (n_ood, 2))

ood_labels = {
    'ID (checkerboard)': X_id,
    'Far-OOD (uniform ±10)': X_ood_unif,
    'Far-OOD (Gaussian far)': X_ood_gauss,
    'Near-OOD (shifted)': X_ood_near,
    'Center noise (±1)': X_ood_center,
}

# ============================
# 4. COMPUTE CREASE DENSITY SCORES
# ============================
print('\nComputing crease density scores...')
results = {}
for label, x_data in ood_labels.items():
    raw, density = scorer.score_batch(x_data)
    # Also compute MSP (max softmax probability)
    logits, _ = model.forward(x_data)
    probs = 1.0 / (1.0 + np.exp(-logits))
    msp = np.maximum(probs.ravel(), 1 - probs.ravel())
    results[label] = {
        'raw': raw, 'density': density, 'msp': msp,
        'mean_density': density.mean(),
        'mean_msp': msp.mean(),
        'std_density': density.std(),
        'std_msp': msp.std(),
    }
    print(f'  {label:<30s} | crease_density={density.mean():.4f}±{density.std():.4f} | msp={msp.mean():.4f}±{msp.std():.4f}')

# ============================
# 5. AUROC EVALUATION
# ============================
def auroc(score_id, score_ood):
    """AUROC: higher score → more ID-like. Returns (auc, direction).
    direction: '+' means ID scores higher, '-' means OOD scores higher."""
    scores = np.concatenate([score_id, score_ood])
    labels = np.concatenate([np.ones(len(score_id)), np.zeros(len(score_ood))])
    order = np.argsort(scores)[::-1]
    labels_sorted = labels[order]
    pos = labels_sorted.sum()
    neg = len(labels_sorted) - pos
    if pos == 0 or neg == 0:
        return 0.5, '+'
    tpr = np.cumsum(labels_sorted) / pos
    fpr = np.cumsum(1 - labels_sorted) / neg
    auc = np.trapezoid(tpr, fpr)
    direction = '+' if auc >= 0.5 else '-'
    return max(auc, 1 - auc), direction

id_density = results['ID (checkerboard)']['density']
id_msp = results['ID (checkerboard)']['msp']

print('\n--- AUROC (ID vs OOD) ---')
print(f'{"OOD Type":<30s} {"Crease AUROC":<18s} {"MSP AUROC":<18s}')
print('-' * 68)
for label, r in results.items():
    if label == 'ID (checkerboard)':
        continue
    au_cr, dir_cr = auroc(id_density, r['density'])
    au_msp, dir_msp = auroc(id_msp, r['msp'])
    # For crease: '-' means OOD has higher crease density (hypothesis correct)
    # For MSP: '+' means ID has higher confidence (standard OOD convention)
    print(f'{label:<30s} {au_cr:<15.4f}({dir_cr}) {au_msp:<15.4f}({dir_msp})')

# ============================
# 6. VISUALIZE
# ============================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Plot 1: Data distributions
ax = axes[0, 0]
colors_id = np.where(y_id == 1, '#d62728', '#1f77b4')
ax.scatter(X_id[:, 0], X_id[:, 1], c=colors_id, s=8, alpha=0.6, label='ID')
ax.scatter(X_ood_unif[:200, 0], X_ood_unif[:200, 1], c='gray', s=8, alpha=0.3, marker='x', label='OOD (unif)')
ax.set_title('ID (checkerboard) + OOD (uniform)')
ax.legend(fontsize=7)
ax.set_xlim(-11, 11); ax.set_ylim(-11, 11)
ax.grid(alpha=0.2)

# Plot 2: Crease density histogram (ID vs far-OOD)
ax = axes[0, 1]
ax.hist(id_density, bins=30, alpha=0.6, color='#1f77b4', label='ID', density=True)
ax.hist(results['Far-OOD (uniform ±10)']['density'], bins=30, alpha=0.6, color='#d62728', label='OOD (unif)', density=True)
ax.set_xlabel('Crease Density (fraction of near-threshold units)')
ax.set_ylabel('Density')
ax.set_title('Crease Density: ID vs Far-OOD')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# Plot 3: MSP histogram
ax = axes[0, 2]
ax.hist(id_msp, bins=30, alpha=0.6, color='#1f77b4', label='ID', density=True)
ax.hist(results['Far-OOD (uniform ±10)']['msp'], bins=30, alpha=0.6, color='#d62728', label='OOD (unif)', density=True)
ax.set_xlabel('Max Softmax Probability')
ax.set_ylabel('Density')
ax.set_title('MSP: ID vs Far-OOD')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# Plot 4: Crease histogram (ID vs center noise — hard case)
ax = axes[1, 0]
ax.hist(id_density, bins=30, alpha=0.6, color='#1f77b4', label='ID', density=True)
ax.hist(results['Center noise (±1)']['density'], bins=30, alpha=0.6, color='#ff7f0e', label='OOD (center)', density=True)
ax.set_xlabel('Crease Density')
ax.set_ylabel('Density')
ax.set_title('Crease Density: ID vs Center Noise')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# Plot 5: MSP histogram (center noise)
ax = axes[1, 1]
ax.hist(id_msp, bins=30, alpha=0.6, color='#1f77b4', label='ID', density=True)
ax.hist(results['Center noise (±1)']['msp'], bins=30, alpha=0.6, color='#ff7f0e', label='OOD (center)', density=True)
ax.set_xlabel('Max Softmax Probability')
ax.set_ylabel('Density')
ax.set_title('MSP: ID vs Center Noise')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# Plot 6: AUROC comparison bar chart
ax = axes[1, 2]
ood_names = [l for l in ood_labels if l != 'ID (checkerboard)']
cr_aucs = []
msp_aucs = []
for l in ood_names:
    cr_aucs.append(auroc(id_density, results[l]['density'])[0])
    msp_aucs.append(auroc(id_msp, results[l]['msp'])[0])

x = np.arange(len(ood_names))
w = 0.35
bars1 = ax.bar(x - w/2, cr_aucs, w, label='Crease Density', color='#2ca02c')
bars2 = ax.bar(x + w/2, msp_aucs, w, label='MSP', color='#1f77b4')
ax.set_xticks(x)
ax.set_xticklabels([n[:12] + '..' if len(n) > 14 else n for n in ood_names], fontsize=8, rotation=15)
ax.set_ylabel('AUROC')
ax.set_title('OOD Detection Performance')
ax.legend(fontsize=8)
ax.set_ylim(0, 1)
ax.axhline(0.5, color='gray', ls='--', alpha=0.5)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('demo_ood_results.png', dpi=150, bbox_inches='tight')
plt.close()
print('\nSaved demo_ood_results.png')

# ============================
# 7. INTERPRETATION
# ============================
print('\n--- Puno Calculus Interpretation ---')
print('If crease density separates ID from OOD, it provides a lightweight,')
print('label-free OOD signal that uses the network\'s own geometry.')
print('Unlike MSP, it does not rely on calibrated probabilities, and')
print('unlike distance-based methods, it requires no stored training data.')
print()
print('Key questions this demo addresses:')
print('  1. Do OOD inputs land near more creases than ID inputs?')
print('  2. Is crease density competitive with MSP for OOD detection?')
print('  3. Does performance vary by OOD type (near vs far)?')

print('\nDemo complete.')
