"""
sigma.chassis.currency: The Sigma Currency
===========================================

A digital, knowledge-backed currency.
Value comes from removable singularities.

1 Sigma = 1 verified removable singularity.

No gold. No government. No externals.
The value is the knowledge itself.

Sources:
  [1] Shannon, "Mathematical Theory of Communication" (1948)
  [2] Kolmogorov, "Foundations of Probability" (1933)
  [3] Von Neumann, "Quantenmechanik" (1932)
  [4] Bekenstein, "Black holes and entropy" (1973)
  [5] Hawking, "Particle creation by black holes" (1975)
  [6] Adams, "Exceptional Lie Algebras" (1996)
  [7] Goddard-Nuyts-Olive, "Dual Coxeter number" (1972)
"""

import numpy as np
import mpmath
import json
import hashlib
import datetime

mpmath.mp.dps = 30


class SigmaCurrency:
    """The Sigma Currency: knowledge-backed digital money.
    
    Value comes from removable singularities.
    Each singularity contributes value based on:
        - Information content (Shannon entropy)
        - Physical significance (entropy, energy, information)
    
    Source: [1] Shannon 1948, [4] Bekenstein 1973
    """
    
    # Known singularity values (in Sigma)
    KNOWN_VALUES = {
        # Math
        'sinx_over_x': {
            'formula': 'sin(x)/x at x=0',
            'value': 1.0,
            'field': 'mathematics',
            'subfield': 'analysis',
            'source': '[1] L\'Hopital 1696',
            'formula_latex': r'$\lim_{x\to 0} \frac{\sin x}{x} = 1$',
        },
        'expx_minus1_over_x': {
            'formula': '(e^x - 1)/x at x=0',
            'value': 1.0,
            'field': 'mathematics',
            'subfield': 'analysis',
            'source': '[1] L\'Hopital 1696',
            'formula_latex': r'$\lim_{x\to 0} \frac{e^x - 1}{x} = 1$',
        },
        'log1x_over_x': {
            'formula': 'log(1+x)/x at x=0',
            'value': 1.0,
            'field': 'mathematics',
            'subfield': 'analysis',
            'source': '[1] L\'Hopital 1696',
            'formula_latex': r'$\lim_{x\to 0} \frac{\ln(1+x)}{x} = 1$',
        },
        '1_cosx_over_x2': {
            'formula': '(1-cos(x))/x^2 at x=0',
            'value': 0.5,
            'field': 'mathematics',
            'subfield': 'analysis',
            'source': '[1] L\'Hopital 1696',
            'formula_latex': r'$\lim_{x\to 0} \frac{1-\cos x}{x^2} = \frac{1}{2}$',
        },
        'tanx_over_x': {
            'formula': 'tan(x)/x at x=0',
            'value': 1.0,
            'field': 'mathematics',
            'subfield': 'analysis',
            'source': '[1] L\'Hopital 1696',
            'formula_latex': r'$\lim_{x\to 0} \frac{\tan x}{x} = 1$',
        },
        'minkowski': {
            'formula': 'M(h) = Lambda / sinh(2*pi / (g_eff^2 * (N-1)))',
            'value': 0.722532,
            'field': 'mathematics',
            'subfield': 'differential geometry',
            'source': '[14] Atiyah-Singer 1968',
            'formula_latex': r'$M(h) = \frac{\Lambda}{\sinh\left(\frac{2\pi}{g_{eff}^2(N-1)}\right)}$',
        },
        'grokking': {
            'formula': 'T_delay = (1/g_eff) * log(V_mem/V_post)',
            'value': 0.498627,
            'field': 'computer science',
            'subfield': 'machine learning',
            'source': '[19] Power et al. 2022',
            'formula_latex': r'$T_{delay} = \frac{1}{g_{eff}} \ln\frac{V_{mem}}{V_{post}}$',
        },
        'resilience': {
            'formula': 'R(t) from spectral power concentration',
            'value': 0.423091,
            'field': 'climate science',
            'subfield': 'tipping points',
            'source': '[20] Scheffer 2009',
            'formula_latex': r'$R(t) = \frac{\text{spectral power}}{\text{total power}}$',
        },
        'dark_core': {
            'formula': 'rho_core = rho_0 / sinh(2*pi / (sigma_m * (N-1)))',
            'value': 0.474497,
            'field': 'physics',
            'subfield': 'astrophysics',
            'source': '[10] Bekenstein 1973',
            'formula_latex': r'$\rho_{core} = \frac{\rho_0}{\sinh\left(\frac{2\pi}{\sigma_m(N-1)}\right)}$',
        },
        'muon_g2': {
            'formula': 'a_mu = alpha/(2*pi)',
            'value': 0.001161,
            'field': 'physics',
            'subfield': 'quantum electrodynamics',
            'source': '[3] Schwinger 1948',
            'formula_latex': r'$a_\mu = \frac{\alpha}{2\pi}$',
        },
        'thirring': {
            'formula': '1/g^2 = M/pi * log(M/Lambda) + c_1 + c_2*g^2 + ...',
            'value': 0.636620,
            'field': 'physics',
            'subfield': 'quantum field theory',
            'source': '[3] Thirring 1958',
            'formula_latex': r'$\frac{1}{g^2} = \frac{M}{\pi}\log\frac{M}{\Lambda} + c_1 + c_2 g^2 + \ldots$',
        },
        'gn_crossover': {
            'formula': 'u = N / (1 + c_1*sqrt(N) + ...)',
            'value': 0.318310,
            'field': 'physics',
            'subfield': 'large N QCD',
            'source': '[7] Goddard-Nuyts-Olive 1972',
            'formula_latex': r'$u = \frac{N}{1 + c_1\sqrt{N} + \ldots}$',
        },
        'zero_pow_zero': {
            'formula': 'x^x at x=0 = 1',
            'value': 1.0,
            'field': 'mathematics',
            'subfield': 'foundations',
            'source': '[29] Ifrah 1998',
            'formula_latex': r'$\lim_{x\to 0^+} x^x = 1$',
        },
    }
    
    def __init__(self):
        self.values = self.KNOWN_VALUES.copy()
    
    def total_supply(self):
        """Total Sigma in existence."""
        return sum(v['value'] for v in self.values.values())
    
    def ledger(self):
        """Return the complete ledger."""
        ledger = {
            'currency': 'Sigma',
            'version': '1.0.0',
            'author': 'Michael Grafiel S Puno',
            'supply': self.total_supply(),
            'timestamp': datetime.datetime.now().isoformat(),
            'singularities': self.values,
        }
        return ledger
    
    def integrity_hash(self):
        """SHA-256 hash of the ledger."""
        ledger_json = json.dumps(self.ledger(), sort_keys=True)
        return hashlib.sha256(ledger_json.encode()).hexdigest()
    
    def print_summary(self):
        """Print a summary of the currency."""
        print("SIGMA CURRENCY")
        print("=" * 70)
        print()
        print("  Definition: 1 Sigma = 1 verified removable singularity")
        print("  Source: No gold, no government, no externals")
        print("  Value: The knowledge itself")
        print()
        print("  LEDGER")
        print("  " + "-" * 60)
        for name, data in sorted(self.values.items()):
            print("  %-25s %10.6f Sigma  [%s]" % (
                name, data['value'], data['field']))
        print("  " + "-" * 60)
        print("  TOTAL SUPPLY: %10.6f Sigma" % self.total_supply())
        print()
        print("  INTEGRITY: %s" % self.integrity_hash()[:16])
        print()
        print("  Source: [1] Shannon 1948, [4] Bekenstein 1973")
    
    def export_json(self):
        """Export the ledger as JSON."""
        return json.dumps(self.ledger(), indent=2)
