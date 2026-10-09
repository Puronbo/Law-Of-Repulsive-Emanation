namespace Goldbach

def isPrimeLoop (d n fuel : Nat) : Bool :=
  match fuel with
  | 0 => true
  | fuel + 1 =>
    if d * d > n then true
    else if n % d = 0 then false
    else isPrimeLoop (d + 2) n fuel

def isPrime (n : Nat) : Bool :=
  if n < 2 then false
  else if n = 2 then true
  else if n % 2 = 0 then false
  else isPrimeLoop 3 n (n / 3 + 1)

def goldbachRepsGo (p n acc fuel : Nat) : Nat :=
  match fuel with
  | 0 => acc
  | fuel + 1 =>
    if p > n / 2 then acc
    else
      let q := n - p
      let acc' := if isPrime p && isPrime q then acc + 1 else acc
      goldbachRepsGo (p + 1) n acc' fuel

def goldbachReps (n : Nat) : Nat :=
  if n < 4 || n % 2 = 1 then 0
  else goldbachRepsGo 2 n 0 (n / 2)

def verifyGoldbach100 : Bool :=
  (List.range' 4 49 2).all (fun n => goldbachReps n > 0)

#eval verifyGoldbach100

/-! ## Computational-certificate boundary (roadmap P1 item 6)

The extended checks of this project verify Goldbach for **all even
`n <= 100 000`** (`02_Experimental_Implementations_and_Verification/
06_Miscellaneous_Experiments/goldbach_large.py`, `MAX = 100000`,
`even_numbers_tested = 49999`, `failures = 0`).  Below, that verification
is packaged as a decidable Lean certificate closed by `native_decide` --
a P-style computational certificate, NOT a proof of Goldbach.

Honest walls, recorded and never crossed:

* the strong Goldbach conjecture itself stays OPEN (marker below);
* the 4 x 10^18 record (Oliveira e Silva 2013) is an external citation
  (`EXPLICIT_GAPS.md`), never computed and never certified here;
* `native_decide` certificates trust the compiler for the finite bound
  only, exactly like `EcaIsometry`'s `count_affine_sector` and
  `MillenniumBridge`'s census theorems.
-/

/-- Eratosthenes sieve: mark multiples of `d` starting at `d * d`,
    up to `arr.size - 1` inclusive. -/
def markMultiples (arr : Array Bool) (d : Nat) : Array Bool :=
  (List.range ((arr.size - 1 - d * d) / d + 1)).foldl
    (fun a i => a.set! (d * d + d * i) true) arr

/-- Sieve pass (fuel-bounded; `arr[d] = false` means `d` is prime). -/
def sieveGo (arr : Array Bool) (d fuel : Nat) : Array Bool :=
  match fuel with
  | 0 => arr
  | fuel + 1 =>
    if d * d >= arr.size then arr
    else if arr[d]! then sieveGo arr (d + 1) fuel
    else sieveGo (markMultiples arr d) (d + 1) fuel

/-- `sieve n`: array of size `n + 1`, index `i` is `true` iff `i` is prime. -/
def sieve (n : Nat) : Array Bool :=
  sieveGo (((List.replicate (n + 1) false).toArray).set! 0 true |>.set! 1 true) 2 (n + 1)

/-- Primality by sieve lookup: the sieve stores `true` for *marked
    (composite)* entries, so prime = `!s[p]`.  Index 0, 1 are marked. -/
def isPrimeSieve (s : Array Bool) (p : Nat) : Bool :=
  p < s.size && !(s[p]!)

/-- First Goldbach witness search: any `p` in `2 .. n/2` with both `p` and
    `n - p` prime.  Early exit on success; fuel-bounded. -/
def goldbachWitness (s : Array Bool) (n p fuel : Nat) : Bool :=
  match fuel with
  | 0 => false
  | fuel + 1 =>
    if p > n / 2 then false
    else if isPrimeSieve s p && isPrimeSieve s (n - p) then true
    else goldbachWitness s n (p + 1) fuel

/-- Certificate: every even `n` in `[4, limit]` has a prime pair.
    The sieve is built ONCE and shared across all `n`. -/
def goldbachCertificate (limit : Nat) : Bool :=
  let s := sieve limit
  (List.range' 4 ((limit - 4) / 2 + 1) 2).all
    (fun n => goldbachWitness s n 2 (n / 2 + 1))

/-- The certificate boundary of this project's extended checks: matches
    `goldbach_large.py` `MAX = 100000` exactly. -/
def certificateBoundary : Nat := 100000

/-- External record, citation only: 4 x 10^18 (Oliveira e Silva 2013).
    Never computed, never certified in this repository. -/
def citedExternalRecord : Nat := 4000000000000000000

/-- Honest wall: the strong Goldbach conjecture itself is OPEN. -/
def goldbach_conjecture_open : Bool := true  -- genuinely open

/-- Computational certificate (P-style, `native_decide`): every even `n`
    with `4 <= n <= 100000` is a sum of two primes.  This certifies the
    finite bound only; the conjecture remains OPEN. -/
theorem goldbach_even_4_to_100000 : goldbachCertificate 100000 = true := by
  native_decide

/-- The certificate sits exactly at the declared boundary. -/
theorem goldbach_certificate_at_boundary :
    goldbachCertificate certificateBoundary = true :=
  goldbach_even_4_to_100000

/-- The certificate does not reach the cited external record: 100000 < 4e18. -/
theorem certificate_below_citation : certificateBoundary < citedExternalRecord := by
  native_decide

end Goldbach
