/-
  Trial-division factorization shared by the Giuga (G30) and Lehmer (G31)
  certificates -- the kernel-side arithmetic that both window scans stand on.

  Honesty notes, stated here because the register requires them:

  * `primeFacGo` is an *implementation* of trial division (fuel-bounded so the
    kernel can reduce it).  Its total correctness -- that every output element
    is prime and that the output is exactly the multiset of prime factors --
    is **reviewed, not proved**.  What *is* machine-checked below: the product
    law `prod = n` for every `1 <= n <= 10000`, and that every output element
    divides `n`.  Together those two certify on the whole certificate window
    that the fuel never runs out (starvation would break the product) and that
    the factor lists are divisors of `n`; the primality of the individual
    factors is the standard trial-division invariant (a composite factor would
    have a smaller prime divisor, removed at an earlier stage), read off the
    code rather than derived by the kernel.
  * `totientFac` derives Euler's phi from that factorization,
    `phi(n) = n * prod_{p | n} (1 - 1/p)`.  On each of the six 2-Lehmer
    numbers it is cross-checked against Mathlib's *proved* `Nat.totient`, so
    the two independent computations agree everywhere the certificate's
    conclusions actually rest.
-/
import Mathlib

set_option maxRecDepth 100000
set_option maxHeartbeats 6000000

namespace PunoCalculus.Factorization

/-- Trial-division factorization: `primeFacGo fuel m i` returns the prime
factors of `m` (with multiplicity), scanning candidates from `i` upward.
`fuel` bounds the recursion so the kernel can reduce it; the certificate
calls it with `fuel = n`, which the product-law window below verifies is
always sufficient. -/
def primeFacGo : ℕ → ℕ → ℕ → List ℕ
  | 0, _, _ => []
  | fuel + 1, m, i =>
    if m ≤ 1 then []
    else if i * i > m then [m]
    else if i ∣ m then i :: primeFacGo fuel (m / i) i
    else primeFacGo fuel m (i + 1)

/-- Every `n` in `1 <= n < 10000` factorizes to factors whose product is `n`
itself: on this window the fuel is sufficient and no factor is lost. -/
theorem primeFacGo_prod_window :
    ((List.range' 1 10000).all fun n => (primeFacGo n n 2).prod = n) = true := by
  decide

/-- Every factor returned on that window divides the number it came from. -/
theorem primeFacGo_dvd_window :
    ((List.range' 1 10000).all fun n =>
      (primeFacGo n n 2).all fun p => p ∣ n) = true := by
  decide

/-- Euler's phi derived from the factorization: divide out each *distinct*
prime `p` once, replacing `n` by `n/p * (p-1)`.  (Applying the step per
distinct factor is the classical `phi(n) = n ∏ (1 - 1/p)` evaluated left to
right, in exact integer arithmetic.) -/
def totientFac (n : ℕ) : ℕ :=
  (primeFacGo n n 2).eraseDups.foldl (fun acc p => acc / p * (p - 1)) n

end PunoCalculus.Factorization
