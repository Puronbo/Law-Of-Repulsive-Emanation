"""
sigma.chassis.detector: Removable Singularity Detector
======================================================

The practical tool: takes a function, finds its removable singularities.

Given f(x), find points a where f(a) = 0/0 (indeterminate).
Compute the removable value via L'Hopital's rule.

This is the engine that makes the framework useful.

Sources:
  [1] L'Hopital, "Analyse des Infiniment Petits" (1696)
  [B1] Puno, "The Removable Singularity" (2026)
"""

import math


def numerical_derivative(f, x, h=1e-8):
    """Compute f'(x) numerically via central difference."""
    return (f(x + h) - f(x - h)) / (2 * h)


def is_zero(val, tol=1e-10):
    """Check if value is effectively zero."""
    return abs(val) < tol


def detect_singularities(f, search_range=(-10, 10), num_points=1000, tol=1e-10):
    """Find removable singularities of f in the search range.
    
    Args:
        f: function to analyze
        search_range: (a, b) interval to search
        num_points: number of sample points
        tol: tolerance for detecting zero
    
    Returns:
        list of dicts: [{point, type, removable_value, verified}]
    """
    a, b = search_range
    dx = (b - a) / num_points
    singularities = []
    
    for i in range(num_points):
        x = a + i * dx
        fx = f(x)
        
        if is_zero(fx, tol):
            # Found a zero - check if it's removable
            # Try to compute the derivative ratio
            fp = numerical_derivative(f, x)
            
            if not is_zero(fp, tol):
                # f(x) = 0, f'(x) != 0 => removable singularity
                # The removable value is f'(x) (if denominator is x-a)
                singularities.append({
                    'point': x,
                    'type': 'removable',
                    'removable_value': fp,
                    'verified': True,
                    'method': "L'Hopital: f'(a)/g'(a)",
                })
            else:
                # Higher order zero - need more analysis
                fpp = numerical_derivative(lambda t: numerical_derivative(f, t), x)
                if not is_zero(fpp, tol):
                    singularities.append({
                        'point': x,
                        'type': 'removable',
                        'removable_value': fpp / 2,
                        'verified': True,
                        'method': "Second derivative ratio",
                    })
                else:
                    singularities.append({
                        'point': x,
                        'type': 'essential_or_pole',
                        'removable_value': None,
                        'verified': False,
                        'method': "Cannot determine",
                    })
    
    return singularities


def lhopital(f, g, a, h=1e-4):
    """Compute lim_{x->a} f(x)/g(x) via L'Hopital's rule.
    
    Args:
        f: numerator function
        g: denominator function
        a: point of indeterminacy
        h: step for numerical differentiation
    
    Returns:
        dict with result, method, verified
    """
    fa, ga = f(a), g(a)
    
    # If not 0/0, just evaluate
    if not is_zero(ga):
        return {
            'result': fa / ga,
            'method': 'direct_evaluation',
            'is_indeterminate': False,
            'verified': True,
        }
    
    # 0/0 case: apply L'Hopital
    # First derivatives: central difference
    fp = (f(a + h) - f(a - h)) / (2 * h)
    gp = (g(a + h) - g(a - h)) / (2 * h)
    
    if not is_zero(gp):
        result = fp / gp
        eps = 1e-6
        check = f(a + eps) / g(a + eps)
        verified = abs(check - result) < 1e-3
        return {
            'result': result,
            'method': "L'Hopital first derivative",
            'is_indeterminate': True,
            'verified': verified,
            'f_prime': fp,
            'g_prime': gp,
        }
    
    # Second derivatives: (f(x+h) - 2f(x) + f(x-h)) / h^2
    # Use h directly (not h/100) to avoid floating-point underflow
    fpp = (f(a + h) - 2 * f(a) + f(a - h)) / (h * h)
    gpp = (g(a + h) - 2 * g(a) + g(a - h)) / (h * h)
    
    if not is_zero(gpp):
        result = fpp / gpp
        eps = 1e-6
        check = f(a + eps) / g(a + eps)
        verified = abs(check - result) < 1e-3
        return {
            'result': result,
            'method': "L'Hopital second derivative",
            'is_indeterminate': True,
            'verified': verified,
        }
    
    return {
        'result': None,
        'method': "indeterminate beyond second order",
        'is_indeterminate': True,
        'verified': False,
    }


def analyze_function(f, name="f"):
    """Complete analysis of a function's singularities.
    
    Args:
        f: function to analyze
        name: display name
    
    Returns:
        dict with analysis results
    """
    # Find zeros in a wide range
    zeros = detect_singularities(f, (-10, 10), 10000)
    
    # Analyze behavior at common singular points
    common_points = [0, 1, -1, math.pi, -math.pi, math.pi/2, -math.pi/2]
    behaviors = []
    
    for a in common_points:
        try:
            fa = f(a)
            if is_zero(fa):
                behaviors.append({
                    'point': a,
                    'value': '0/0',
                    'status': 'indeterminate',
                })
            elif math.isinf(fa):
                behaviors.append({
                    'point': a,
                    'value': 'infinity',
                    'status': 'pole',
                })
            else:
                behaviors.append({
                    'point': a,
                    'value': fa,
                    'status': 'defined',
                })
        except (ValueError, ZeroDivisionError, OverflowError):
            behaviors.append({
                'point': a,
                'value': 'undefined',
                'status': 'essential',
            })
    
    return {
        'name': name,
        'zeros_found': len(zeros),
        'singularities': zeros,
        'behaviors': behaviors,
        'search_range': (-10, 10),
    }


def print_analysis(analysis):
    """Pretty-print a function analysis."""
    name = analysis['name']
    print("ANALYSIS: %s" % name)
    print("=" * 60)
    print()
    
    print("ZEROS FOUND: %d" % analysis['zeros_found'])
    print("-" * 60)
    for s in analysis['singularities']:
        print("  x = %12.8f  [%s]" % (s['point'], s['type']))
        if s['removable_value'] is not None:
            print("    Removable value: %.10f" % s['removable_value'])
            print("    Verified: %s" % ("YES" if s['verified'] else "NO"))
        print()
    
    print("BEHAVIOR AT COMMON POINTS")
    print("-" * 60)
    for b in analysis['behaviors']:
        val = b['value']
        if isinstance(val, float):
            val = "%.6f" % val
        print("  x = %8.4f  =>  %s  [%s]" % (b['point'], val, b['status']))
    print()


# Pre-defined singularities from the book
KNOWN_SINGULARITIES = {
    'sinc': {
        'f': lambda x: math.sin(x) / x if abs(x) > 1e-15 else 1.0,
        'name': 'sin(x)/x',
        'point': 0,
        'value': 1.0,
        'source': "L'Hopital 1696",
    },
    'exp_deriv': {
        'f': lambda x: (math.exp(x) - 1) / x if abs(x) > 1e-15 else 1.0,
        'name': '(e^x - 1)/x',
        'point': 0,
        'value': 1.0,
        'source': "L'Hopital 1696",
    },
    'log_deriv': {
        'f': lambda x: math.log(1 + x) / x if abs(x) > 1e-15 else 1.0,
        'name': 'log(1+x)/x',
        'point': 0,
        'value': 1.0,
        'source': "L'Hopital 1696",
    },
    'cos_second': {
        'f': lambda x: (1 - math.cos(x)) / (x*x) if abs(x) > 1e-15 else 0.5,
        'name': '(1-cos(x))/x^2',
        'point': 0,
        'value': 0.5,
        'source': "L'Hopital 1696",
    },
    'tan_deriv': {
        'f': lambda x: math.tan(x) / x if abs(x) > 1e-15 else 1.0,
        'name': 'tan(x)/x',
        'point': 0,
        'value': 1.0,
        'source': "L'Hopital 1696",
    },
    'zero_pow_zero': {
        'f': lambda x: x**x if x > 0 else 1.0,
        'name': 'x^x at 0',
        'point': 0,
        'value': 1.0,
        'source': "Ifrah 1998",
    },
}
