"""
sigma.chassis: The Removable Singularity Chassis
=================================================

Modules:
    core: Singularity identification and classification
    bridge: Chi(rho) bridge between zeta(s) and zeta(1-s)
    e8: E8 exceptional Lie algebra
    currency: Sigma knowledge-backed currency
    book: "The Removable Singularity" book integration
    verification: 38-test verification suite
"""

from .core import Singularity, Chassis
from .bridge import chi, chi_modulus, chi_at_zeros, verify_bridge
from .e8 import exponents, degrees, weyl_order, verify_e8
from .currency import SigmaCurrency
from .book import BookIntegration, EpistemicClassifier, REAL, CAREFUL, NOT_SAME

__all__ = [
    'Singularity', 'Chassis',
    'chi', 'chi_modulus', 'chi_at_zeros', 'verify_bridge',
    'exponents', 'degrees', 'weyl_order', 'verify_e8',
    'SigmaCurrency',
    'BookIntegration', 'EpistemicClassifier', 'REAL', 'CAREFUL', 'NOT_SAME',
]
