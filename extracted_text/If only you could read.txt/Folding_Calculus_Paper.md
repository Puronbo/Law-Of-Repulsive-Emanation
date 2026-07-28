# Folding Calculus
**Derivatives as Folds, Integrals as Unfolds, and Creases as Primary Objects**

**Michael Grafiel Sayson Puno**  
Second Edition — July 2026  

**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)  
You are free to share and adapt this work for any purpose, including commercial use, as long as you give appropriate credit to the author.  
https://creativecommons.org/licenses/by/4.0/

---

## Abstract
The fundamental operations of calculus have a simple geometric meaning: differentiation is *folding* (compressing global information to local slope), and integration is *unfolding* (expanding local slopes into global structure). At a 90-degree crease (e.g., f(x) = |x| at x=0), folding reveals a set of possible slopes rather than a single number. This reframing makes creases central rather than exceptional and directly illuminates ReLU neural networks as layered folding machines. We formalize the framework, introduce crease density as a diagnostic, and present supporting experiments.

---

## 1. The 90-Degree Fold — The Core Intuition
(Insert image from PDF: title/cover page or Chapter 1 screenshot here)

Consider the graph of **f(x) = |x|** — two straight lines meeting at a sharp **90-degree crease** at x=0.

- **Folding at the crease**: Press the left and right arms flat together. All global shape information collapses to the local possibilities at the hinge: any supporting line with slope m where -1 ≤ m ≤ 1. This set *is* the subdifferential ∂f(0) = [-1, 1].
- **Unfolding**: Take local slopes and integrate them. You recover piecewise linear functions consistent with the original crease.

This is exact mathematics. For smooth functions (no sharp crease, e.g. x²), the fold yields a single tangent slope. The Fundamental Theorem of Calculus states that fold and unfold are inverses.

---

## 2. Formal Definitions
- **Fold (Differentiation)**: Maps a function to its local linear approximations.
- **Unfold (Integration)**: Reconstructs the global function from local approximations.
- **Crease**: Point where the subdifferential is an interval (positive diameter) rather than a singleton.
- **Crease Density**: Fraction of ReLU pre-activations near zero in a neural network (quantifies undecided folds).

---

## 3. ReLU Networks as Layered Folding
Each ReLU layer applies a 90-degree-style fold along a hyperplane. Deeper networks perform more folds, creating complex decision boundaries. Crease density tracks how many units remain at their switching hinges during training.

(Insert relevant experiment table images from PDF pages 10–16)

---

## 4. Experiments & Results
(Summarized from provided PDF — small but consistent effects on toy problems. Crease density drops as networks settle their folds.)

## 5. Discussion & Open Problems
The 90-degree fold provides a unifying geometric language. Future work: formal fold depth complexity, soft creases for modern activations, and applications in geometry.

## References
- Keup, C., & Helias, M. (2022). Origami in N dimensions. arXiv:2203.11355.
- Lewandowski, M. et al. (2025). On Space Folds of ReLU Neural Networks.
- Rockafellar, R.T. (1970). Convex Analysis (subdifferentials).

## Appendix: Code & Visuals
(See fold_visual.py and attachments.)

**Everything folds. Everything unfolds. The crease is where the action is.**