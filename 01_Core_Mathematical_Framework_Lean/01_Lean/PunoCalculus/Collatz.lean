namespace Collatz

def collatzStep (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else 3 * n + 1

def collatzSteps (n : Nat) (fuel : Nat := 100000) : Nat :=
  match fuel with
  | 0 => 0
  | fuel + 1 =>
    if n <= 1 then 0 else 1 + collatzSteps (collatzStep n) fuel

def verifyCollatz100 : Bool :=
  (List.range' 2 99).all (fun n => collatzSteps n > 0)

def maxStopN (N : Nat) : Nat :=
  (List.range' 1 N).foldl (fun acc n => Nat.max acc (collatzSteps n)) 0

#eval verifyCollatz100
#eval maxStopN 10000

end Collatz
