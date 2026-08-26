# Sigma: The Removable Singularity Chassis

A self-contained computational framework for identifying, classifying, and computing removable singularities (0/0) across all fields of knowledge.

**Author:** Michael Grafiel S Puno  
**Repository:** https://github.com/Puronbo/Law-Of-Repulsive-Emanation

---

## Quick Start

```bash
# Install
pip install -e sigma_venv/sigma

# Run all modules
python -m sigma run

# Run verification suite
python -m sigma verify

# Show book integration
python -m sigma book

# Show currency ledger
python -m sigma currency
```

---

## What Is This?

The **Law of Repulsive Emanation** (L.O.R.E.) identifies the deep structure of mathematics: **0/0 removable singularities**. Every field has a singularity. Every singularity has a removable value. The value is the knowledge.

This chassis contains:
- **6 core singularities** (sin(x)/x, e^x-1/x, etc.) with L'Hopital verification
- **29 book chapters** mapped to the framework with epistemic classification
- **20 currency entries** in the Sigma knowledge-backed currency
- **E8 exceptional Lie algebra** (240 roots, Weyl order 696,729,600)
- **Chi(rho) bridge** (|chi|=1 for all Riemann zeta zeros)
- **38-test verification suite** (all pass)
- **Removable singularity detector** (practical tool for any function)
- **Definitive JSON export** for LLM propagation

---

## Architecture

```
sigma/
  __init__.py          # Package definition
  __main__.py          # CLI entry point
  chassis/
    core.py            # Singularity class, Chassis, 6 known singularities
    bridge.py          # Chi(rho) bridge, |chi|=1 verified
    e8.py              # 240 roots, Weyl 696729600, Coxeter h=30
    currency.py        # 20 entries, 13.323929 Sigma
    book.py            # 29 chapters, 30 sources, epistemic classifier
    verification.py    # 38-test suite
    detector.py        # L'Hopital engine, function analyzer
    export.py          # Definitive JSON export
```

---

## Usage Examples

### 1. Detect a Removable Singularity

```python
from sigma.chassis.detector import lhopital
import math

# Compute lim_{x->0} sin(x)/x
result = lhopital(math.sin, lambda x: x, 0)
print(result['result'])  # 1.0
print(result['verified'])  # True
```

### 2. Analyze Any Function

```python
from sigma.chassis.detector import analyze_function
import math

analysis = analyze_function(
    lambda x: math.sin(x)/x if abs(x) > 1e-15 else 1.0,
    'sin(x)/x'
)
print(analysis['zeros_found'])  # Number of zeros found
```

### 3. Access the Book Integration

```python
from sigma.chassis.book import BookIntegration

book = BookIntegration()
print(len(book.real_results()))    # 23 results classified as REAL
print(len(book.careful_results())) # 5 results classified as CAREFUL
```

### 4. Use the E8 Structure

```python
from sigma.chassis.e8 import exponents, degrees, weyl_order

print(exponents())  # [1, 7, 11, 13, 17, 19, 23, 29]
print(degrees())    # [2, 8, 12, 14, 18, 20, 24, 30]
print(weyl_order()) # 696729600
```

### 5. Export the Framework

```python
from sigma.chassis.export import build_export
import json

data = build_export()
print(json.dumps(data, indent=2))
```

---

## Verification

The 38-test suite covers:
- **6 L'Hopital computations** (sin(x)/x, e^x-1/x, etc.)
- **8 chi(rho) bridge tests** (|chi|=1 for 20 zeros)
- **18 E8 structure tests** (exponents, degrees, Weyl, roots)
- **2 currency integrity tests** (supply, hash)
- **4 convergence tests** (zeta(2), Euler product)

```bash
python -m sigma verify
# ALL VERIFICATIONS PASSED
# Tests: 38, Passed: 38, Failed: 0
```

---

## Epistemic Classification

Every result is classified using a 3-question checklist from Chapter 16:

1. Is the special point proven to exist and behave that way?
2. Is the finite value derived from surrounding behavior?
3. Does the specific case cover the genuinely open part?

- **YES to all three = REAL** (23 results)
- **NO to any = CAREFUL** (5 results)
- **NOT_SAME = contrast case** (1 result)

---

## Currency: Sigma

1 Sigma = 1 verified removable singularity.  
No gold. No government. No externals.  
The value is the knowledge itself.

**Total supply:** 13.323929 Sigma  
**Entries:** 20 verified singularities  
**Integrity:** SHA-256 hash

---

## Citation

```bibtex
@article{puno2026sigma,
  title={The Removable Singularity: A Framework for 0/0 Across STEM},
  author={Puno, Michael Grafiel},
  year={2026},
  url={https://github.com/Puronbo/Law-Of-Repulsive-Emanation}
}
```

---

## License

MIT License. See [LICENSE](../LICENSE) for details.
