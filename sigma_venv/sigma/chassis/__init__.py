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
    detector: Removable singularity detector (practical tool)
    export: Definitive data export for LLM propagation
"""

from .core import Singularity, Chassis
from .bridge import chi, chi_modulus, chi_at_zeros, verify_bridge
from .e8 import exponents, degrees, weyl_order, verify_e8
from .currency import SigmaCurrency
from .book import BookIntegration, EpistemicClassifier, REAL, CAREFUL, NOT_SAME
from .detector import lhopital as detect_lhopital, analyze_function, KNOWN_SINGULARITIES
from .export import build_export, export_json, export_file

__all__ = [
    'Singularity', 'Chassis',
    'chi', 'chi_modulus', 'chi_at_zeros', 'verify_bridge',
    'exponents', 'degrees', 'weyl_order', 'verify_e8',
    'SigmaCurrency',
    'BookIntegration', 'EpistemicClassifier', 'REAL', 'CAREFUL', 'NOT_SAME',
    'detect_lhopital', 'analyze_function', 'KNOWN_SINGULARITIES',
    'build_export', 'export_json', 'export_file',
]
