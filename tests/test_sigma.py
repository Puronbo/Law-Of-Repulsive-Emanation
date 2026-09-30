"""
Sigma Chassis: Complete Test Suite
===================================

Run with: pytest tests/test_sigma.py -v
"""

import os
import sys

# The sigma.chassis framework ships inside the bundled virtualenv sigma_venv/
# (editable package import at repo root).  Ensure it -- and its own
# site-packages (numpy, mpmath) -- are importable when this suite runs under
# the host interpreter.  Mirrors the established pattern used by the root
# test_sigma.py and sigma_school_server.py.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_VENV = os.path.join(_ROOT, "sigma_venv")
sys.path.insert(0, os.path.join(_VENV, "Lib", "site-packages"))
sys.path.insert(0, _VENV)

import pytest
import math


class TestLHopital:
    """Test L'Hopital computations for all known 0/0 cases."""
    
    def test_sinc(self):
        from sigma.chassis.detector import lhopital
        result = lhopital(math.sin, lambda x: x, 0)
        assert abs(result['result'] - 1.0) < 1e-3
        assert result['verified']
    
    def test_exp_deriv(self):
        from sigma.chassis.detector import lhopital
        result = lhopital(lambda x: math.exp(x) - 1, lambda x: x, 0)
        assert abs(result['result'] - 1.0) < 1e-3
        assert result['verified']
    
    def test_log_deriv(self):
        from sigma.chassis.detector import lhopital
        result = lhopital(lambda x: math.log(1 + x), lambda x: x, 0)
        assert abs(result['result'] - 1.0) < 1e-3
        assert result['verified']
    
    def test_cos_second(self):
        from sigma.chassis.detector import lhopital
        result = lhopital(lambda x: 1 - math.cos(x), lambda x: x*x, 0)
        assert abs(result['result'] - 0.5) < 1e-3
        assert result['verified']
    
    def test_tan_deriv(self):
        from sigma.chassis.detector import lhopital
        result = lhopital(math.tan, lambda x: x, 0)
        assert abs(result['result'] - 1.0) < 1e-3
        assert result['verified']


class TestE8:
    """Test E8 exceptional Lie algebra structure."""
    
    def test_exponents(self):
        from sigma.chassis.e8 import exponents
        exp = exponents()
        assert exp == [1, 7, 11, 13, 17, 19, 23, 29]
    
    def test_degrees(self):
        from sigma.chassis.e8 import degrees
        deg = degrees()
        assert deg == [2, 8, 12, 14, 18, 20, 24, 30]
    
    def test_weyl_order(self):
        from sigma.chassis.e8 import weyl_order
        assert weyl_order() == 696729600
    
    def test_root_count(self):
        from sigma.chassis.e8 import root_count
        assert root_count() == 240
    
    def test_coxeter(self):
        from sigma.chassis.e8 import coxeter_number
        assert coxeter_number() == 30


class TestBridge:
    """Test Chi(rho) bridge.

    Correction 2026-09-28: the two tests above confirm only an identity of the
    critical LINE, which holds at non-zeros as well and therefore cannot decide
    RH. The falsification control below pins that fact down, so a future edit
    cannot quietly restore the "verified" reading: a non-zero on the line MUST
    pass the same modulus test, and displacing Re(s) MUST be caught.
    """

    def test_chi_modulus_at_zero(self):
        from sigma.chassis.bridge import chi_modulus
        mod = chi_modulus(0.5 + 1j * 14.134725)
        assert abs(mod - 1.0) < 1e-8

    def test_chi_modulus_arbitrary(self):
        from sigma.chassis.bridge import chi_modulus
        for y in [0.5, 1.0, 2.0, 5.0, 10.0]:
            mod = chi_modulus(0.5 + 1j * y)
            assert abs(mod - 1.0) < 1e-8

    def test_line_identity_cannot_detect_zeros(self):
        """FALSIFICATION CONTROL: a non-zero on the line passes identically.

        This is the reason the line identity is not evidence for RH. If this
        test ever fails, the property being guarded (that the check is
        vacuous) has changed and the PL-22 claim must be re-examined.
        """
        import mpmath
        from sigma.chassis.bridge import chi_modulus
        rho = mpmath.zetazero(1)
        impostor = 0.5 + 1j * float(mpmath.im(rho) + 0.5)
        # genuinely not a zero: |zeta| is ~0.41 here, not ~0
        assert abs(mpmath.zeta(impostor)) > 0.01
        at_zero = chi_modulus(0.5 + 1j * float(mpmath.im(rho)))
        at_impostor = chi_modulus(impostor)
        assert abs(at_zero - at_impostor) < 1e-20      # indistinguishable
        assert abs(at_impostor - 1.0) < 1e-8           # both "pass"

    def test_displaced_real_part_is_caught(self):
        """The half of chi with teeth: |chi| = 1 forces Re(s) = 1/2 in the strip."""
        from sigma.chassis.bridge import chi_line_displaced
        results = chi_line_displaced()
        assert results, "displacement probe returned no samples"
        for r in results:
            assert r['caught'], "Re(s) displacement not caught: %r" % (r,)

    def test_chi_ratio_is_pole_free(self):
        """chi() raises at s = 2, 4, 6, ...; chi_ratio() must not."""
        from sigma.chassis.bridge import chi_ratio
        for s in [2, 4, 6, 8]:
            assert abs(chi_ratio(s)) < float("inf")
        assert abs(abs(chi_ratio(2)) - 2 * 3.141592653589793**2) < 1e-6


class TestCurrency:
    """Test Sigma currency integrity."""
    
    def test_total_supply(self):
        from sigma.chassis.currency import SigmaCurrency
        sc = SigmaCurrency()
        assert abs(sc.total_supply() - 13.323929) < 0.01
    
    def test_integrity_hash(self):
        from sigma.chassis.currency import SigmaCurrency
        sc = SigmaCurrency()
        h = sc.integrity_hash()
        assert len(h) == 64
    
    def test_entry_count(self):
        from sigma.chassis.currency import SigmaCurrency
        sc = SigmaCurrency()
        assert len(sc.values) == 20


class TestBook:
    """Test book integration."""
    
    def test_chapter_count(self):
        from sigma.chassis.book import CHAPTERS
        assert len(CHAPTERS) == 86
    
    def test_epistemic_classifier(self):
        from sigma.chassis.book import EpistemicClassifier, REAL, CAREFUL
        assert EpistemicClassifier.classify([True, True, True]) == REAL
        assert EpistemicClassifier.classify([True, False, True]) == CAREFUL
    
    def test_real_results(self):
        from sigma.chassis.book import BookIntegration
        book = BookIntegration()
        assert len(book.real_results()) == 80
    
    def test_careful_results(self):
        from sigma.chassis.book import BookIntegration
        book = BookIntegration()
        assert len(book.careful_results()) == 5


class TestDetector:
    """Test removable singularity detector."""
    
    def test_analyze_function(self):
        from sigma.chassis.detector import analyze_function
        analysis = analyze_function(
            lambda x: math.sin(x)/x if abs(x) > 1e-15 else 1.0,
            'sin(x)/x'
        )
        assert analysis['name'] == 'sin(x)/x'
        assert 'zeros_found' in analysis


class TestExport:
    """Test data export."""
    
    def test_build_export(self):
        from sigma.chassis.export import build_export
        data = build_export()
        assert data['framework'] == 'L.O.R.E. (Law of Repulsive Emanation)'
        assert data['version'] == '2.0.0'
        assert data['book']['total_chapters'] == 86
        assert data['currency']['entries'] == 20
        assert data['verification']['all_pass'] is True


class TestVerification:
    """Test the verification suite."""
    
    def test_run_all(self):
        from sigma.chassis.verification import run_all_verifications
        result = run_all_verifications()
        assert result is True


class TestSchool:
    """Test Sigma Virtual School server."""
    
    def test_import(self):
        """School server can be imported."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "sigma_school_server",
            "sigma_school_server.py"
        )
        assert spec is not None
    
    def test_build_courses(self):
        """School has 29 chapters."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "sigma_school_server",
            "sigma_school_server.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        courses = mod.build_courses()
        assert len(courses) == 1
        assert len(courses[0]['chapters']) == 86
    
    def test_chapter_structure(self):
        """Each chapter has required fields."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "sigma_school_server",
            "sigma_school_server.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        courses = mod.build_courses()
        for ch in courses[0]['chapters']:
            assert 'id' in ch
            assert 'title' in ch
            assert 'content' in ch
            assert 'quiz' in ch
            assert len(ch['quiz']) == 5
    
    def test_quiz_structure(self):
        """Each quiz question has required fields."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "sigma_school_server",
            "sigma_school_server.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        courses = mod.build_courses()
        for ch in courses[0]['chapters']:
            for q in ch['quiz']:
                assert 'q' in q
                assert 'options' in q
                assert 'correct' in q
                assert len(q['options']) == 4
    
    def test_password_hash(self):
        """Password hashing works."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "sigma_school_server",
            "sigma_school_server.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        h1 = mod.hash_password("test")
        h2 = mod.hash_password("test")
        h3 = mod.hash_password("different")
        assert h1 == h2
        assert h1 != h3
        assert len(h1) == 64
