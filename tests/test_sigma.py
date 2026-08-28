"""
Sigma Chassis: Complete Test Suite
===================================

Run with: pytest tests/test_sigma.py -v
"""

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
    """Test Chi(rho) bridge."""
    
    def test_chi_modulus_at_zero(self):
        from sigma.chassis.bridge import chi_modulus
        mod = chi_modulus(0.5 + 1j * 14.134725)
        assert abs(mod - 1.0) < 1e-8
    
    def test_chi_modulus_arbitrary(self):
        from sigma.chassis.bridge import chi_modulus
        for y in [0.5, 1.0, 2.0, 5.0, 10.0]:
            mod = chi_modulus(0.5 + 1j * y)
            assert abs(mod - 1.0) < 1e-8


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
        assert len(CHAPTERS) == 70
    
    def test_epistemic_classifier(self):
        from sigma.chassis.book import EpistemicClassifier, REAL, CAREFUL
        assert EpistemicClassifier.classify([True, True, True]) == REAL
        assert EpistemicClassifier.classify([True, False, True]) == CAREFUL
    
    def test_real_results(self):
        from sigma.chassis.book import BookIntegration
        book = BookIntegration()
        assert len(book.real_results()) == 64
    
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
        assert data['book']['total_chapters'] == 70
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
        assert len(courses[0]['chapters']) == 70
    
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
