/-
  PunoCalculus - Main verification entry point

  Runs all formal verifications and reports results.

  Author: Michael Grafiel S Puno
  Date: August 2026
-/

import PunoCalculus.Core
import PunoCalculus.CascadeRatio
import PunoCalculus.Goldbach
import PunoCalculus.MassGap
import PunoCalculus.Collatz
import PunoCalculus.Legendre
import PunoCalculus.Curvature
import PunoCalculus.BSD
import PunoCalculus.Hodge
import PunoCalculus.Poincare
import PunoCalculus.PvsNP
import PunoCalculus.TwinPrime

def main : IO Unit := do
  IO.println "=========================================="
  IO.println "  PunoCalculus Formal Verification"
  IO.println "  The Indeterminate Structure of Truth"
  IO.println "=========================================="
  IO.println ""

  IO.println "  [RH] Hadamard terms positive (sigma=0.6):"
  IO.println s!"    Result: {checkTermsPositive}"
  IO.println ""

  IO.println "  [RH] Hadamard sum positive (sigma=0.6, t=10):"
  IO.println s!"    Result: {checkSumPositive}"
  IO.println ""

  IO.println "  [RH] Near-line sum positive (sigma=0.51, t=100):"
  IO.println s!"    Result: {checkNearLinePositive}"
  IO.println ""

  IO.println "  [RH] All 5 test points positive:"
  IO.println s!"    Result: {checkAllTestPoints}"
  IO.println ""

  IO.println "  [NS] Cascade ratio decays:"
  IO.println s!"    Result: {verifyRDecays}"
  IO.println ""

  IO.println "  [NS] All 12 IC cases pass:"
  IO.println s!"    Result: {verifyAllNSCases}"
  IO.println ""

  IO.println "  [Goldbach] All even 4..100 have r(n) > 0:"
  IO.println s!"    Result: {Goldbach.verifyGoldbach100}"
  IO.println ""

  IO.println "  [YM] Mass gap positive for 8 couplings:"
  IO.println s!"    Result: {verifyMassGapPositive}"
  IO.println ""

  IO.println "  [Collatz] All n=2..100 reach 1:"
  IO.println s!"    Result: {Collatz.verifyCollatz100}"
  IO.println s!"    Max stopping time in [1,10000]: {Collatz.maxStopN 10000}"
  IO.println ""

  IO.println "  [Legendre] All intervals n=1..100 contain primes:"
  IO.println s!"    Result: {Legendre.verifyLegendre100}"
  IO.println s!"    Min prime count: {Legendre.minPrimeCount100}"
  IO.println ""

  IO.println "  [Curvature] L' positive at non-zero points:"
  IO.println s!"    Result: {Curvature.verifyLdashPositive}"
  IO.println ""

  IO.println "  [Curvature] L' larger near zeros than far away:"
  IO.println s!"    Result: {Curvature.verifyLdashLargeNearZero}"
  IO.println ""

  IO.println "  [Curvature] Corrected formula ratio converges to 1:"
  IO.println s!"    Result: {Curvature.verifyRatioConverges}"
  IO.println ""

  IO.println "  [Curvature] |xi'(rho)|^2 > 0 at all 20 zeros:"
  IO.println s!"    Result: {Curvature.verifyCurvatureAtZeros}"
  IO.println ""

  IO.println "  [Curvature] Full check:"
  IO.println s!"    Result: {Curvature.verifyFullCurvature}"
  IO.println ""

  IO.println "  [BSD] Formula verified for 4 curves (rank 0,1,2):"
  IO.println s!"    Result: {BSD.verifyFullBSD}"
  IO.println ""

  IO.println "  [Hodge] CP^n, products, abelian, quintic:"
  IO.println s!"    Result: {Hodge.verifyFullHodge}"
  IO.println ""

  IO.println "  [Poincare] Hamilton ratio + classification:"
  IO.println s!"    Result: {Poincare.verifyFullPoincare}"
  IO.println ""

  IO.println "  [PvsNP] Complexity ordering + singularity structure:"
  IO.println s!"    Result: {PvsNP.verifyFullPvsNP}"
  IO.println ""

  IO.println "  [TwinPrime] pi_2(100)=8, pi_2(1000)=35, Brun convergence:"
  IO.println s!"    Result: {TwinPrime.verifyFullTwinPrime}"
  IO.println ""

  IO.println "=========================================="
  IO.println "  All verifications complete."
  IO.println "=========================================="
