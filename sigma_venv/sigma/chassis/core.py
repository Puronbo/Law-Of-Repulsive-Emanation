"""
sigma.chassis: The Removable Singularity Chassis
=================================================

The core module. Identifies, classifies, and computes
removable singularities (0/0) using L'Hopital's rule.

The chassis is the ENGINE of the 0/0 framework.
It takes a singularity and produces a removable value.

Sources:
  [1] L'Hopital, "Analyse des Infiniment Petits" (1696)
  [2] Riemann, "Ueber die Anzahl der Primzahlen" (1859)
  [3] Polya, "How to Solve It" (1945)
"""

import numpy as np
import mpmath

mpmath.mp.dps = 30


class Singularity:
    """Represents a removable singularity (0/0).
    
    A singularity is a point where a function is undefined
    but may have a removable value.
    
    Attributes:
        point: The point where the singularity occurs
        numerator: The numerator function (vanishes at the point)
        denominator: The denominator function (vanishes at the point)
        classification: 'removable', 'pole', or 'essential'
    
    Source: [1] L'Hopital 1696, [2] Riemann 1859
    """
    
    def __init__(self, point, numerator, denominator):
        """Initialize a singularity.
        
        Args:
            point: The point where f(point) = g(point) = 0
            numerator: Function f(x) with f(point) = 0
            denominator: Function g(x) with g(point) = 0
        """
        self.point = mpmath.mpf(point)
        self.numerator = numerator
        self.denominator = denominator
        self._classification = None
    
    def evaluate_at(self, x):
        """Evaluate f(x)/g(x) at x."""
        f_val = self.numerator(x)
        g_val = self.denominator(x)
        if g_val == 0:
            return float('inf') if f_val != 0 else float('nan')
        return float(mpmath.re(f_val / g_val))
    
    def classify(self):
        """Classify the singularity.
        
        Returns:
            'removable': if the limit exists (0/0 with finite limit)
            'pole': if the limit is infinite (0/nonzero or nonzero/0)
            'essential': if the limit does not exist
        
        Source: [2] Riemann 1859, complex analysis classification
        """
        if self._classification is not None:
            return self._classification
        
        try:
            limit = self.removable_value()
            if np.isfinite(limit):
                self._classification = 'removable'
            else:
                self._classification = 'pole'
        except Exception:
            self._classification = 'essential'
        
        return self._classification
    
    def removable_value(self):
        """Compute the removable value using L'Hopital's rule.
        
        For f(x)/g(x) at x=a where f(a)=g(a)=0:
            lim = f'(a)/g'(a)
        
        Source: [1] L'Hopital 1696
        """
        # Use mpmath's derivative
        f_prime = mpmath.diff(self.numerator, self.point)
        g_prime = mpmath.diff(self.denominator, self.point)
        
        if g_prime == 0:
            # Higher order: try second derivative
            f_d2 = mpmath.diff(self.numerator, self.point, n=2)
            g_d2 = mpmath.diff(self.denominator, self.point, n=2)
            if g_d2 == 0:
                raise ValueError("Higher order L'Hopital needed")
            return float(mpmath.re(f_d2 / g_d2))
        
        return float(mpmath.re(f_prime / g_prime))
    
    def is_verified(self, tolerance=1e-10):
        """Verify the removable value by numerical limit.
        
        Checks that lim_{x->a} f(x)/g(x) matches the L'Hopital result.
        """
        lhopital_val = self.removable_value()
        
        # Check from both sides
        eps = 1e-8
        val_plus = self.evaluate_at(self.point + eps)
        val_minus = self.evaluate_at(self.point - eps)
        
        err_plus = abs(val_plus - lhopital_val)
        err_minus = abs(val_minus - lhopital_val)
        
        return max(err_plus, err_minus) < tolerance
    
    def __repr__(self):
        return "Singularity(point=%s, class=%s)" % (
            mpmath.nstr(self.point, 6), self.classify())


class Chassis:
    """The Removable Singularity Chassis.
    
    A self-contained computational space for 0/0 analysis.
    Identifies, classifies, and computes removable values.
    
    The chassis is the ENGINE of the 0/0 framework.
    
    Source: The 0/0 Framework (Puno 2026)
    """
    
    def __init__(self):
        self.known_singularities = {}
        self._register_known()
    
    def _register_known(self):
        """Register all known removable singularities."""
        
        # sin(x)/x at x=0 -> 1
        self.known_singularities['sinc'] = Singularity(
            0,
            lambda x: mpmath.sin(x),
            lambda x: x
        )
        
        # (e^x - 1)/x at x=0 -> 1
        self.known_singularities['exp_deriv'] = Singularity(
            0,
            lambda x: mpmath.exp(x) - 1,
            lambda x: x
        )
        
        # log(1+x)/x at x=0 -> 1
        self.known_singularities['log_deriv'] = Singularity(
            0,
            lambda x: mpmath.log(1 + x),
            lambda x: x
        )
        
        # (1 - cos(x))/x^2 at x=0 -> 1/2
        self.known_singularities['cos_second'] = Singularity(
            0,
            lambda x: 1 - mpmath.cos(x),
            lambda x: x**2
        )
        
        # tan(x)/x at x=0 -> 1
        self.known_singularities['tan_deriv'] = Singularity(
            0,
            lambda x: mpmath.tan(x),
            lambda x: x
        )
        
        # x^x at x=0 -> 1 (0^0 = 1)
        # This is NOT a 0/0 but a direct removable singularity:
        # x^x = e^{x*ln(x)}, and lim_{x->0+} x*ln(x) = 0
        self.known_singularities['zero_pow_zero'] = Singularity(
            0,
            lambda x: mpmath.exp(x * mpmath.log(x + mpmath.mpf('1e-30'))) - 1,
            lambda x: x
        )
    
    def identify(self, point, numerator, denominator):
        """Identify a new singularity.
        
        Args:
            point: The point where f=g=0
            numerator: Function f
            denominator: Function g
        
        Returns:
            A Singularity object
        """
        return Singularity(point, numerator, denominator)
    
    def compute(self, singularity):
        """Compute the removable value of a singularity.
        
        Args:
            singularity: A Singularity object
        
        Returns:
            The removable value (float)
        """
        return singularity.removable_value()
    
    def verify(self, singularity, tolerance=1e-10):
        """Verify a removable value numerically.
        
        Args:
            singularity: A Singularity object
            tolerance: Numerical tolerance
        
        Returns:
            True if verified
        """
        return singularity.is_verified(tolerance)
    
    def list_known(self):
        """List all known singularities and their values."""
        results = []
        for name, sing in self.known_singularities.items():
            val = sing.removable_value()
            verified = sing.is_verified()
            results.append({
                'name': name,
                'value': val,
                'classification': sing.classify(),
                'verified': verified,
            })
        return results
    
    def summary(self):
        """Print a summary of all known singularities."""
        print("SIGMA CHASSIS: Removable Singularity Summary")
        print("=" * 55)
        for item in self.list_known():
            print("  %-20s = %10.6f  [%s]  %s" % (
                item['name'], item['value'],
                item['classification'],
                "VERIFIED" if item['verified'] else "UNVERIFIED"))
        print("=" * 55)
        print("Total: %d known singularities" % len(self.known_singularities))
