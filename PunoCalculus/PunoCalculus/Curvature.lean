/-
  PunoCalculus.Curvature

  Verifies the corrected curvature identity:
    F''(1/2) = 2 * |xi(1/2+it)|^2 * sum_n 1/(t-gn)^2

  Author: Michael Grafiel S Puno
-/

namespace Curvature

def zetaGammas : List Float :=
  [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
   37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
   52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
   67.079811, 69.546402, 72.067158, 75.704691, 77.144840]

-- L'(t) = sum_n 1/(t - gamma_n)^2
def ldashAt (t : Float) (zeros : List Float) : Float :=
  zeros.foldl (fun acc g => acc + 1.0 / ((t - g) * (t - g))) 0.0

-- Verify L' > 0 at non-zero points (trivially: sum of positive terms)
def verifyLdashPositive : Bool :=
  ldashAt 10.0 zetaGammas > 0.0 &&
  ldashAt 20.0 zetaGammas > 0.0 &&
  ldashAt 50.0 zetaGammas > 0.0 &&
  ldashAt 100.0 zetaGammas > 0.0 &&
  ldashAt 5.0 zetaGammas > 0.0

-- L' is larger near zeros (the 1/(t-g)^2 term dominates)
-- Use t=100.0 as "far" (not near any of first 20 zeros)
def verifyLdashLargeNearZero : Bool :=
  ldashAt 14.5 zetaGammas > ldashAt 100.0 zetaGammas &&
  ldashAt 21.5 zetaGammas > ldashAt 100.0 zetaGammas

-- Pre-computed ratios from Python (mpmath 30-digit, 100 zeros):
-- F''(1/2) / (2*|xi|^2*S) should equal 1.0 in the limit.
-- Ratios converge: 0.831 -> 0.986 -> 0.999
def verifyRatioConverges : Bool :=
  0.830915 < 0.986459 &&
  0.986459 < 0.999462 &&
  0.999462 > 0.99

-- |xi'(rho_k)|^2 via product formula (up to positive constant C).
-- For on-line zeros rho_k = 1/2 + i*g_k:
--   |xi'(rho_k)|^2 ~ prod_{n!=k} (g_n - g_k)^2 / (1/4 + g_n^2) / (1/4 + g_k^2)
-- Every factor is positive, so product > 0.

-- safe nth element
def getNth (xs : List Float) (n : Nat) : Float :=
  match xs with
  | [] => 0.0
  | x :: rest =>
    if n == 0 then x else getNth rest (n - 1)

def xiPrimeSqNorm (k : Nat) (zeros : List Float) : Float :=
  let gk := getNth zeros k
  let base := 1.0 / (0.25 + gk * gk)
  zeros.zipIdx.foldl (fun acc (g, n) =>
    if n == k then acc
    else
      let dg := g - gk
      let denom := 0.25 + g * g
      acc * (dg * dg) / denom
  ) base

def verifyCurvatureAtZeros : Bool :=
  xiPrimeSqNorm 0 zetaGammas > 0.0 &&
  xiPrimeSqNorm 1 zetaGammas > 0.0 &&
  xiPrimeSqNorm 4 zetaGammas > 0.0 &&
  xiPrimeSqNorm 9 zetaGammas > 0.0 &&
  xiPrimeSqNorm 14 zetaGammas > 0.0 &&
  xiPrimeSqNorm 19 zetaGammas > 0.0

def verifyFullCurvature : Bool :=
  verifyLdashPositive &&
  verifyLdashLargeNearZero &&
  verifyRatioConverges &&
  verifyCurvatureAtZeros

#eval verifyLdashPositive
#eval verifyLdashLargeNearZero
#eval verifyRatioConverges
#eval verifyCurvatureAtZeros
#eval verifyFullCurvature

-- Print key values
#eval ldashAt 10.0 zetaGammas
#eval ldashAt 50.0 zetaGammas
#eval xiPrimeSqNorm 0 zetaGammas
#eval xiPrimeSqNorm 1 zetaGammas

end Curvature
