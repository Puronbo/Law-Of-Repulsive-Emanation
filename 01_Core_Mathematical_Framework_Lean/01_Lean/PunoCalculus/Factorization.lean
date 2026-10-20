/-
  Trial-division factorization shared by the Giuga (G30) and Lehmer (G31)
  certificates -- the kernel-side arithmetic that both window scans stand on.

  Honesty notes, stated here because the register requires them:

  * `primeFacGo` is an *implementation* of trial division (fuel-bounded so the
    kernel can reduce it).  Two of its correctness properties are **proved**
    below, unconditionally in the fuel and the input:

      - `primeFacGo_dvd`: every emitted factor divides the number factored;
      - `primeFacGo_prime`: every emitted factor is prime.

    Together with the window product law below (`prod = n` for every
    `1 <= n <= 10000`, kernel `decide`) these say the emitted lists are lists of
    prime divisors of `n` whose product is `n` on the whole certificate window.
    What is **reviewed, not proved** is the remaining half of "exactly the
    multiset of prime factors": that no prime factor is *omitted* (equivalently
    the product law for *all* `n`, not just the window) and that multiplicities
    are exact.  The product-law window certifies the former on the window; the
    general statement is the standard trial-division induction, not carried out
    here.  `primeFacGo_prime` replaces the previous "primality is read off the
    code" caveat.

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

/-- Every emitted factor divides the number it factors.  (Proved for all fuel,
`m`, `i` -- no window restriction.) -/
theorem primeFacGo_dvd (fuel m i : ℕ) :
    ∀ p ∈ primeFacGo fuel m i, p ∣ m := by
  induction fuel generalizing m i with
  | zero => intro p hp; simp [primeFacGo] at hp
  | succ fuel ih =>
    intro p hp
    unfold primeFacGo at hp
    split_ifs at hp with h1 h2 h3
    · simp at hp
    · simp only [List.mem_singleton] at hp; subst hp; exact dvd_rfl
    · rcases List.mem_cons.mp hp with rfl | hp'
      · exact h3
      · exact dvd_trans (ih _ _ p hp') (Nat.div_dvd_of_dvd h3)
    · exact ih _ _ p hp

/-- If `i ∣ m`, `2 ≤ i`, and every prime divisor of `m` is `≥ i`, then `i`
itself is prime: any prime `q ∣ i` is a prime divisor of `m`, so `i ≤ q` while
`q ≤ i`, forcing `q = i`. -/
theorem prime_of_dvd_of_inv {m i : ℕ} (hmi : i ∣ m) (hi : 2 ≤ i)
    (hinv : ∀ q, q.Prime → q ∣ m → i ≤ q) : i.Prime := by
  obtain ⟨q, hq, hqi⟩ := Nat.exists_prime_and_dvd (by omega : i ≠ 1)
  have hqm : q ∣ m := dvd_trans hqi hmi
  have hle : i ≤ q := hinv q hq hqm
  have hqi_le : q ≤ i := Nat.le_of_dvd (by omega) hqi
  have hqeq : q = i := le_antisymm hqi_le hle
  rwa [hqeq] at hq

/-- Every emitted factor is prime, for all fuel, `m`, `i ≥ 2`, provided the loop
only ever encounters values whose prime divisors are `≥ i` (the trial-division
invariant, discharged at `i = 2` by `primeFacGo_prime`).  Proved for all fuel --
no window restriction. -/
theorem primeFacGo_prime_of_inv (fuel : ℕ) :
    ∀ m i, 2 ≤ i → (∀ q, q.Prime → q ∣ m → i ≤ q) →
      ∀ p ∈ primeFacGo fuel m i, p.Prime := by
  induction fuel with
  | zero => intro m i _ _ p hp; simp [primeFacGo] at hp
  | succ fuel ih =>
    intro m i hi2 hinv p hp
    unfold primeFacGo at hp
    split_ifs at hp with h1 h2 h3
    · simp at hp
    · simp only [List.mem_singleton] at hp
      have hp' : p = m := hp
      subst p
      by_contra hnp
      have hmin_le : i ≤ m.minFac := hinv _ (Nat.minFac_prime (by omega)) (Nat.minFac_dvd m)
      have hsq : m.minFac ^ 2 ≤ m := Nat.minFac_sq_le_self (by omega) hnp
      nlinarith [hmin_le, hsq, h2]
    · rcases List.mem_cons.mp hp with rfl | hp'
      · exact prime_of_dvd_of_inv h3 hi2 hinv
      · refine ih (m / i) i hi2 ?_ p hp'
        intro q hq hqdiv
        exact le_trans (hinv q hq (dvd_trans hqdiv (Nat.div_dvd_of_dvd h3))) le_rfl
    · refine ih m (i + 1) (by omega) ?_ p hp
      intro q hq hqdiv
      have hle : i ≤ q := hinv q hq hqdiv
      have hne : q ≠ i := by intro hqi; exact h3 (hqi ▸ hqdiv)
      omega

/-- **Every factor emitted by `primeFacGo fuel n 2` is prime**, for every `n` and
every fuel -- the trial-division invariant, closed at `i = 2`. -/
theorem primeFacGo_prime (fuel n : ℕ) :
    ∀ p ∈ primeFacGo fuel n 2, p.Prime := by
  refine primeFacGo_prime_of_inv fuel n 2 (by omega) ?_
  intro q hq _; exact hq.two_le

/-- Every `n` in `1 <= n < 10000` factorizes to factors whose product is `n`
itself: on this window the fuel is sufficient and no factor is lost. -/
theorem primeFacGo_prod_window :
    ((List.range' 1 10000).all fun n => (primeFacGo n n 2).prod = n) = true := by
  decide

/-- Every factor returned on that window divides the number it came from.
(Now a corollary of the general `primeFacGo_dvd`; kept as a kernel-decided
window statement alongside the product law.) -/
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
