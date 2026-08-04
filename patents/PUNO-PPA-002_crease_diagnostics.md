---
title: "Provisional Patent Application"
subtitle: "System and Method for Crease-Density-Based Diagnostics of Neural Networks"
docket: "PUNO-PPA-002"
inventor: "Michael Grafiel Sayson Puno"
date: "2026-08-04"
---

# PROVISIONAL PATENT APPLICATION

## System and Method for Crease-Density-Based Diagnostics, Pruning, Early Stopping, and Out-of-Distribution Detection in Neural Networks

**Docket:** PUNO-PPA-002
**Inventor:** Michael Grafiel Sayson Puno
**Filed (priority date basis):** 2026-08-04
**Corpus reference:** Puno Calculus (`Universals/crease_metrics.py`, `Universals/exp_pruning.py`, `Universals/exp3_early_stop.py`, `Universals/demo_ood.py`, `Universals/exp1b_crease_subgradient.py`, `data/exp_pruning_results.json`, `data/exp3_early_stop_results.json`, `data/exp_ood_results.json`, `data/exp2_results.json`, `data/exp1b_results.json`, `data/crease_data.json`)

---

## 1. TITLE OF THE INVENTION

System and Method for Crease-Density-Based Diagnostics of Neural Networks, including a Crease-Aware Pruning Criterion, a Label-Free Early-Stopping Signal, an Out-of-Distribution Detector, and a Crease-Aware Subgradient Selection.

## 2. FIELD OF THE INVENTION

The invention relates to the training, compression, and validation of artificial neural networks, and more particularly to diagnostics derived from the distribution of hidden-unit pre-activations near the folds (non-differentiable kinks) of piecewise-linear activations such as ReLU. The invention provides: (a) a pruning criterion that removes neurons whose pre-activations rarely approach the fold; (b) a label-free early-stopping signal based on the stabilization of fold ("crease") density; (c) an out-of-distribution (OOD) score based on fold proximity; and (d) a subgradient-selection rule for units at the fold.

## 3. BACKGROUND OF THE INVENTION

### 3.1 ReLU folds

A ReLU unit computes z = w·x + b and y = max(z, 0). The function is non-differentiable at the "fold" z = 0. Standard backpropagation selects the subgradient 1 if z > 0 else 0 (gradient is killed at and below the fold). Practitioners conventionally treat the fold as a negligible measure-zero set. The inventors have found, to the contrary, that the fraction of units whose pre-activations lie within a small band |z| < ε around the fold is a rich, measurable, data-dependent diagnostic.

### 3.2 Crease density

For a layer l with weights w_l, bias b_l and activation σ, define the soft crease intensity

    C_l = E_x[ |σ''(w_l^T x + b_l)| · ||w_l|| ]

For ReLU, σ''(x) = δ(x) (Dirac delta at the fold), so the quantity reduces to the density of near-fold units: the fraction of (sample, unit) pairs with |z| < ε for a chosen band ε. This quantity is cheap to compute during a forward pass with no labels and no modification of the network.

### 3.3 Prior approaches and their limitations

1. **Magnitude-based pruning** (remove smallest |w| columns): standard and effective at mild ratios, but it ignores the *usage* of each unit on the data distribution.
2. **Activation-based pruning** (e.g., average activation, APoZ): uses activation statistics but not the fold structure; does not single out units that are persistently undecided between on and off.
3. **Validation-based early stopping** (stop when val loss plateaus): requires a labeled validation set and a user-chosen patience; wastes epochs because plateaus are detected late.
4. **Confidence-based OOD detection (MSP)**: strong for far OOD but weak for in-support ("near") OOD where the model is over-confident.
5. **Random subgradient perturbations** at non-differentiable points: not guided by fold proximity.

## 4. SUMMARY OF THE INVENTION

The invention provides computer-implemented methods, all sharing a common measured signal — the crease density (fraction of near-fold hidden units on the data distribution):

1. **Crease-aware pruning.** Rank units by crease density (fraction of training samples with |z| < ε); prune the lowest-density units first. Measured advantage over weight-magnitude pruning: 7 of 10 tested pruning ratios, with the largest gap +0.1347 (+13.47 accuracy points) at 25% removal on the test set (0.7200 vs 0.5853), no retraining.
2. **Crease-stabilization early stopping.** Monitor the per-epoch relative change in mean crease count across layers; stop training when the relative change stays below a threshold for a patience window. Measured epoch savings of 79.8% (shallow), 64.0% (medium), and 71.0% (deep) of a 500-epoch budget, versus 26.2%, 47.0%, 52.0% for a val-loss plateau policy, with test-accuracy cost of about 12.3, 2.6, and 2.8 points respectively. The signal is label-free.
3. **Crease-density OOD detection.** Score each input by the fraction of hidden units near their folds. Measured AUROC 0.8835 on in-support ("center noise") OOD vs 0.7061 for MSP — the crease signal is the better detector where the model is over-confident and MSP fails. On far OOD, MSP remains stronger (0.9868 vs 0.6798 on far Gaussian), so a preferred embodiment fuses the two signals.
4. **Crease-aware subgradient selection.** For units with |z| < ε, select the subgradient explicitly (always-on, randomized, or inverted) instead of the default kill. Measured: all selections reach identical best accuracy (0.9983), while measurably changing the density of near-fold units during training — demonstrating a behavior-neutral control over fold topology.

A preferred embodiment uses the crease density measured on a batch of training or unlabeled data; no labels are required for any of the four methods.

## 5. DETAILED DESCRIPTION

### 5.1 Measuring crease density

Let the model have layers l = 1..L with pre-activations z_l(x) = w_l x + b_l for input x. For a batch B:

    crease_count_l  = |{ (x, u) ∈ B × units_l : |z_l,u(x)| < ε }|
    density_l       = crease_count_l / (|B| · units_l)
    aggregate       = Σ_l crease_count_l / Σ_l (|B| · units_l)

Default ε = 0.05. Optionally, a "sign-straddle" variant counts only units that genuinely straddle zero (samples on both sides of the fold). The soft intensity variant evaluates |σ''(z)|·||w|| numerically (central differences with step 1e-4) for smooth activations (e.g., GELU with max |σ''(0)| ≈ 0.798; Swish with σ'' extremum near x ≈ −1.28).

### 5.2 Crease-aware pruning (measured protocol)

- Dataset: synthetic checkerboard with coarse + fine cells; 3500 train / 1500 test.
- Model: 2-hidden-layer MLP, 256 hidden units; Adam lr 1e-3, 300 epochs; baseline test accuracy 0.8327.
- Prune score per unit u: fraction of training samples with |z_u| < 0.05. Mean per-unit density 0.01043, std 0.01080.
- Pruning = zero the incoming weight column of the chosen units; no retraining. Ratios 0–50% in 5% steps.
- Measured test accuracies:

| Ratio | crease | magnitude | random | crease−mag |
|---|---|---|---|---|
| 5% | 0.8327 | 0.8227 | 0.7477 | +0.0100 |
| 10% | 0.7553 | 0.7600 | 0.6715 | −0.0047 |
| 15% | 0.7580 | 0.6880 | 0.6029 | +0.0700 |
| 20% | 0.7533 | 0.6207 | 0.6273 | +0.1327 |
| 25% | 0.7200 | 0.5853 | 0.5820 | +0.1347 |
| 30% | 0.6147 | 0.5213 | 0.5557 | +0.0933 |
| 35% | 0.5780 | 0.5020 | 0.5405 | +0.0760 |
| 40% | 0.5327 | 0.5167 | 0.5624 | +0.0160 |
| 45% | 0.5400 | 0.5633 | 0.5705 | −0.0233 |
| 50% | 0.4773 | 0.5000 | 0.5484 | −0.0227 |

Crease pruning is best in the practical mid-range (15–35% removal), with the maximum advantage of +13.47 points at 25%. Honest limits: below random at 40–50% and below magnitude at 10%, 45%, 50%.

### 5.3 Crease-stabilization early stopping (measured protocol)

- Dataset: 6000 samples; 3600 train / 1200 val / 1200 test. Architectures: shallow [2,128,128,1], medium [2,64,64,64,1], deep [2,32,32,32,32,32,1]. Budget 500 epochs.
- Crease count per batch = number of units with |z| < 0.05 summed over layers, averaged per sample.
- Stop rule: relative per-epoch change |Δcre|/max(cre, 0.001) < 0.015 for 15 consecutive epochs.

| Architecture | mode | stop epoch | epochs saved | savings | test acc |
|---|---|---|---|---|---|
| Shallow | full | 500 | 0 | 0% | 0.9033 |
| Shallow | val plateau | 369 | 131 | 26.2% | 0.8708 |
| Shallow | crease stable | 101 | 399 | 79.8% | 0.7808 |
| Medium | full | 500 | 0 | 0% | 0.9150 |
| Medium | val plateau | 265 | 235 | 47.0% | 0.8933 |
| Medium | crease stable | 180 | 320 | 64.0% | 0.8892 |
| Deep | full | 500 | 0 | 0% | 0.9117 |
| Deep | val plateau | 240 | 260 | 52.0% | 0.9042 |
| Deep | crease stable | 145 | 355 | 71.0% | 0.8842 |

The crease-stabilization rule always stops earliest and saves the most epochs; it trades test accuracy relative to full 500-epoch training (12.3 / 2.6 / 2.8 points) in exchange for roughly 3×, 1.4×, and 1.4× the epoch savings of the val-loss policy. It requires no labels.

### 5.4 Crease-density OOD detection (measured protocol)

- Model [2,64,64,1] trained on the checkerboard (ID accuracy 0.815).
- Crease OOD score = per-sample fraction of near-fold hidden units (|z| < 0.05 across concatenated hidden layers).
- OOD sets (each 1200 samples): far-uniform U(−10,10)²; far-Gaussian N(0,3²·I)+(15,15); near-shifted U(−5,5)²; center noise U(−1,1)².

| OOD set | crease AUROC | MSP AUROC | better |
|---|---|---|---|
| far-uniform | 0.6085 | 0.7707 | MSP |
| far-Gaussian | 0.6798 | 0.9868 | MSP |
| near-shifted | 0.5114 | 0.5047 | crease |
| center noise | 0.8835 | 0.7061 | **crease** |

Mean crease density rises from 0.00932 (ID) to 0.03429 on center noise (≈3.7×), while MSP confidence falls to 0.70 — the crease signal peaks precisely where the model is least confident, i.e., near-support OOD. A preferred embodiment fuses crease score and MSP (e.g., weighted or max-combined) to be strong on both near and far OOD.

### 5.5 Crease-aware subgradient selection (measured protocol)

- Dataset: ring dataset 3000 samples, 80/20 split, z-scored; model [2,64,64,1]; Adam lr 1e-3, 300 epochs.
- At units with |z| < ε (ε = 0.05 or 0.01), replace the default gate (z > 0) with: random (Bernoulli 0.5), oppose (invert), or always-on (mask 1).
- Measured: best accuracy identical at 0.9983 across standard/random/oppose/always-on; average crease counts differ (119.63 / 122.98 / 124.33 / 84.92 at ε = 0.01), showing the subgradient choice at the folds is a behavior-neutral control over fold topology.

### 5.6 Related measured facts

- Crease density correlates with boundary complexity r = −0.7658 (deeper networks crease less).
- Kawasaki foldability test (alternating sum of vertex angles = 0, an N-dimensional generalization of Kawasaki's flat-foldability theorem): of 1000 tested decision-region vertices, mean deviation 0.4866 with 72.4% satisfied at ε = 0.5 — a genuine open problem, included as a diagnostic.

## 6. CLAIMS (provisional)

1. A computer-implemented method for pruning a neural network, comprising: computing, for each hidden unit, a crease density equal to the fraction of input samples for which the unit's pre-activation lies within a band ε of the unit's non-differentiable fold; ranking units by crease density; and removing or disabling the lowest-density units.

2. The method of claim 1, further comprising pruning a fraction in a range of 15% to 35% of the units, whereby the retained network's accuracy exceeds that of magnitude-pruned networks at the same fraction.

3. A computer-implemented method for early stopping of neural network training, comprising: monitoring, across epochs, a crease count equal to the number of hidden units with pre-activation within a band ε of a fold, averaged over samples; and stopping training when the relative per-epoch change in the crease count remains below a threshold for a patience window, without reference to any labeled validation set.

4. The method of claim 3, wherein the stopping is executed earlier than a validation-loss plateau rule and achieves greater epoch savings.

5. A computer-implemented method for detecting out-of-distribution inputs to a neural network, comprising: computing a per-input crease score equal to the fraction of hidden units whose pre-activation lies within a band ε of a fold; and flagging the input as out-of-distribution when the crease score exceeds a threshold.

6. The method of claim 5, further comprising fusing the crease score with a confidence score such that near-support out-of-distribution inputs are detected by the crease score and far out-of-distribution inputs by the confidence score.

7. A computer-implemented method for training a neural network with piecewise-linear activations, comprising: identifying hidden units whose pre-activation lies within a band ε of a non-differentiable fold; and selecting a subgradient for those units from a set comprising always-on, randomized, and inverted, while leaving all other units on the standard gradient gate.

8. A system comprising one or more processors and memory configured to perform the method of any of claims 1–7.

## 7. ABSTRACT

Methods and systems for neural-network diagnostics based on the crease density — the fraction of hidden units whose pre-activations lie near the non-differentiable folds of piecewise-linear activations. Measured on real runs: crease-proximity pruning beats weight-magnitude pruning at 7 of 10 ratios (best +13.47 accuracy points at 25% removal); crease-stabilization provides a label-free early-stopping signal saving 64–79.8% of epochs; a crease-density score detects in-support out-of-distribution inputs (AUROC 0.8835 vs 0.7061 for confidence) where confidence-based methods fail; and fold-adjacent subgradient selection controls fold topology without changing generalization.

---

*This document is a provisional disclosure establishing a priority date for the subject matter described. All measured values are reproduced from the inventor's verified corpus (2026-08-04); no assertion is made regarding patentability beyond enablement and written description.*
