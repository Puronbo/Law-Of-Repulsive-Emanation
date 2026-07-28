#!/usr/bin/env python3
"""
Experiment: Pruning via Crease Proximity
==========================================
Tests whether neurons whose pre-activation is persistently near zero
(the ReLU crease) are redundant and can be pruned.

Hypothesis: Neurons operating near their switching threshold for most inputs
contribute minimal decisive signal — they are "fence-sitters" that neither
strongly activate nor strongly deactivate.

Compares three pruning criteria:
  A) Crease proximity: remove neurons with highest fraction of near-zero pre-activations
  B) Weight magnitude: remove neurons with smallest L2 weight norm
  C) Random: remove random neurons (baseline)

For each criterion, we ablate increasing fractions of neurons and measure
accuracy impact. If crease-proximity neurons are redundant, their removal
should cause LESS accuracy drop than random or magnitude pruning.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from puno_utils import Net, accuracy, bce, train_model, make_multiscale, CREASE_THRESH

np.random.seed(42)

# ============================
# 1. TRAIN MODEL
# ============================
print('=' * 70)
print('PRUNING VIA CREASE PROXIMITY')
print('=' * 70)

X, y = make_multiscale(5000)
X_tr, y_tr = X[:3500], y[:3500]
X_te, y_te = X[3500:], y[3500:]

model = Net([2, 128, 128, 1])
print('\nTraining model...')
train_model(model, X_tr, y_tr, X_te, y_te, lr=1e-3, epochs=300)
baseline_acc = accuracy(model, X_te, y_te)
print(f'\nBaseline test accuracy: {baseline_acc:.4f}')

# ============================
# 2. MEASURE PER-NEURON CREASE DENSITY
# ============================
print('\nComputing per-neuron crease density on training set...')

# Collect pre-activations for all hidden neurons across all training inputs
# Store as list of arrays: one per hidden layer
all_zs = [np.zeros((len(X_tr), model.L[i]['W'].shape[1])) for i in range(len(model.L)-1)]

h = X_tr
for i, layer in enumerate(model.L):
    z = h @ layer['W'] + layer['b']
    if i < len(model.L) - 1:
        all_zs[i] = z
        h = z * (z > 0).astype(float)

# For each neuron, compute crease_density = fraction of inputs where |pre_activation| < CREASE_THRESH
crease_densities = []  # list of arrays, one per hidden layer
for z_layer in all_zs:
    near_crease = (np.abs(z_layer) < CREASE_THRESH).astype(float)
    crease_densities.append(near_crease.mean(axis=0))

# Flatten to get per-neuron scores
all_crease_scores = np.concatenate(crease_densities)
n_neurons = len(all_crease_scores)

print(f'  Total hidden neurons: {n_neurons}')
print(f'  Crease density stats:')
print(f'    Mean: {all_crease_scores.mean():.4f}')
print(f'    Std:  {all_crease_scores.std():.4f}')
print(f'    Min:  {all_crease_scores.min():.4f}')
print(f'    Max:  {all_crease_scores.max():.4f}')
print(f'    % near crease (score > 0.1): {100*(all_crease_scores > 0.1).mean():.1f}%')
print(f'    % near crease (score > 0.2): {100*(all_crease_scores > 0.2).mean():.1f}%')

# ============================
# 3. ALSO MEASURE WEIGHT MAGNITUDES
# ============================
weight_norms = np.concatenate([
    np.linalg.norm(model.L[i]['W'], axis=0)  # L2 norm of incoming weights per neuron
    for i in range(len(model.L)-1)
])

# ============================
# 4. ABLATION EXPERIMENT
# ============================
def ablate_neurons(model_in, neuron_idx, layer_idx):
    """Zero out a specific neuron's outgoing weights (structured pruning)."""
    model = model_in.copy()
    # For the layer where the neuron is: zero its outgoing weights
    # neuron_idx in layer_idx means we zero column neuron_idx of L[layer_idx]['W']
    model.L[layer_idx]['W'][:, neuron_idx] = 0
    return model

prune_ratios = np.linspace(0, 0.5, 11)  # 0% to 50% pruning

results_crease = {'ratio': [], 'acc': [], 'neurons': []}
results_magnitude = {'ratio': [], 'acc': [], 'neurons': []}
results_random = {'ratio': [], 'acc': [], 'neurons': []}

# Build list of (layer_idx, neuron_idx) for all neurons
all_neurons = []
offset = 0
for l in range(len(model.L)-1):
    n_units = model.L[l]['W'].shape[1]
    for u in range(n_units):
        all_neurons.append((l, u))
assert len(all_neurons) == n_neurons

# Sort by criterion
order_crease = np.argsort(all_crease_scores)[::-1]  # highest crease first
order_magnitude = np.argsort(weight_norms)  # lowest weight first
order_random = np.random.permutation(n_neurons)

for ratio in prune_ratios:
    n_prune = int(ratio * n_neurons)
    if n_prune == 0:
        results_crease['ratio'].append(0); results_magnitude['ratio'].append(0); results_random['ratio'].append(0)
        results_crease['acc'].append(baseline_acc); results_magnitude['acc'].append(baseline_acc); results_random['acc'].append(baseline_acc)
        results_crease['neurons'].append([]); results_magnitude['neurons'].append([]); results_random['neurons'].append([])
        continue

    # Crease pruning
    model_cr = model.copy()
    for idx in order_crease[:n_prune]:
        l, u = all_neurons[idx]
        model_cr.L[l]['W'][:, u] = 0
    acc_cr = accuracy(model_cr, X_te, y_te)
    results_crease['ratio'].append(ratio)
    results_crease['acc'].append(acc_cr)
    results_crease['neurons'].append([all_neurons[i] for i in order_crease[:n_prune]])

    # Magnitude pruning
    model_mag = model.copy()
    for idx in order_magnitude[:n_prune]:
        l, u = all_neurons[idx]
        model_mag.L[l]['W'][:, u] = 0
    acc_mag = accuracy(model_mag, X_te, y_te)
    results_magnitude['ratio'].append(ratio)
    results_magnitude['acc'].append(acc_mag)
    results_magnitude['neurons'].append([all_neurons[i] for i in order_magnitude[:n_prune]])

    # Random pruning (3 trials, average)
    accs_rand = []
    for trial in range(5):
        model_rand = model.copy()
        rand_idx = np.random.permutation(n_neurons)[:n_prune]
        for idx in rand_idx:
            l, u = all_neurons[idx]
            model_rand.L[l]['W'][:, u] = 0
        accs_rand.append(accuracy(model_rand, X_te, y_te))
    results_random['ratio'].append(ratio)
    results_random['acc'].append(np.mean(accs_rand))
    results_random['neurons'].append([])

    print(f'  Prune {ratio*100:3.0f}% | crease_acc={acc_cr:.4f} | magnitude_acc={acc_mag:.4f} | random_acc={np.mean(accs_rand):.4f}')

# ============================
# 5. VISUALIZE
# ============================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Accuracy vs pruning ratio
ax = axes[0]
ax.plot(results_crease['ratio'], results_crease['acc'], 'o-', color='#2ca02c', lw=2, label='Crease proximity (prune highest crease)')
ax.plot(results_magnitude['ratio'], results_magnitude['acc'], 's-', color='#1f77b4', lw=2, label='Weight magnitude (prune lowest norm)')
ax.plot(results_random['ratio'], results_random['acc'], 'd--', color='gray', lw=1.5, label='Random (avg 5 trials)')
ax.axhline(baseline_acc, color='black', ls=':', alpha=0.5, label=f'Baseline ({baseline_acc:.3f})')
ax.set_xlabel('Fraction of neurons pruned')
ax.set_ylabel('Test Accuracy')
ax.set_title('Pruning: Accuracy vs Fraction Removed')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# Plot 2: Crease density histogram
ax = axes[1]
ax.hist(all_crease_scores, bins=30, color='#2ca02c', alpha=0.7, edgecolor='white')
ax.axvline(all_crease_scores.mean(), color='darkgreen', ls='--', label=f'Mean={all_crease_scores.mean():.3f}')
ax.axvline(np.median(all_crease_scores), color='darkred', ls=':', label=f'Median={np.median(all_crease_scores):.3f}')
ax.set_xlabel('Crease Density (fraction of inputs near threshold)')
ax.set_ylabel('Number of neurons')
ax.set_title('Distribution of Per-Neuron Crease Density')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# Plot 3: Crease density vs weight norm (scatter)
ax = axes[2]
sc = ax.scatter(weight_norms, all_crease_scores, c=all_crease_scores, cmap='viridis', s=20, alpha=0.6)
ax.set_xlabel('Weight L2 Norm (incoming)')
ax.set_ylabel('Crease Density')
ax.set_title('Crease Density vs Weight Norm (per neuron)')
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Crease Density')
ax.grid(alpha=0.3)

# Also compute correlation
from scipy.stats import pearsonr
corr, _ = pearsonr(weight_norms, all_crease_scores)
ax.set_title(f'Crease Density vs Weight Norm\nPearson r = {corr:.4f}')

plt.tight_layout()
plt.savefig('exp_pruning_results.png', dpi=150, bbox_inches='tight')
plt.close()
print('\nSaved exp_pruning_results.png')

# ============================
# 6. SUMMARY
# ============================
print('\n' + '=' * 70)
print('SUMMARY')
print('=' * 70)
print(f'Baseline accuracy: {baseline_acc:.4f}')
print(f'\nAt 10% pruning:')
print(f'  Crease proximity: {results_crease["acc"][2]:.4f} (drop={baseline_acc - results_crease["acc"][2]:.4f})')
print(f'  Weight magnitude: {results_magnitude["acc"][2]:.4f} (drop={baseline_acc - results_magnitude["acc"][2]:.4f})')
print(f'  Random:           {results_random["acc"][2]:.4f} (drop={baseline_acc - results_random["acc"][2]:.4f})')

print(f'\nAt 20% pruning:')
print(f'  Crease proximity: {results_crease["acc"][4]:.4f} (drop={baseline_acc - results_crease["acc"][4]:.4f})')
print(f'  Weight magnitude: {results_magnitude["acc"][4]:.4f} (drop={baseline_acc - results_magnitude["acc"][4]:.4f})')
print(f'  Random:           {results_random["acc"][4]:.4f} (drop={baseline_acc - results_random["acc"][4]:.4f})')

# Find which pruning strategy is best (least accuracy drop) at each ratio
print(f'\nBest strategy by pruning ratio:')
for i, ratio in enumerate(prune_ratios):
    if ratio == 0:
        continue
    scores = [
        ('Crease', results_crease['acc'][i]),
        ('Magnitude', results_magnitude['acc'][i]),
        ('Random', results_random['acc'][i]),
    ]
    best = max(scores, key=lambda x: x[1])
    print(f'  {ratio*100:3.0f}%: {best[0]} ({best[1]:.4f})')

# ============================
# 7. INTERPRETATION
# ============================
print('\n--- Puno Calculus Interpretation ---')
print('If crease-proximity neurons are redundant, pruning them should')
print('cause minimal accuracy loss compared to random or magnitude pruning.')
print()
print('The Critical Brain Hypothesis (from SNNs) predicts the opposite:')
print('near-threshold neurons are most informative and pruning them hurts.')
print()
print('This experiment is the first to test this question for ReLU ANNs.')
print()

# Check which pruning was best at 20%+
best_at_20 = max([
    ('Crease', results_crease['acc'][4]),
    ('Magnitude', results_magnitude['acc'][4]),
    ('Random', results_random['acc'][4]),
], key=lambda x: x[1])
print(f'At 20% pruning, best strategy: {best_at_20[0]} ({best_at_20[1]:.4f})')

print('\nExperiment complete.')
