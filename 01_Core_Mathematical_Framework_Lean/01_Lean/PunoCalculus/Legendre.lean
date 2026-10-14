namespace Legendre

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

def primesBetweenCount (n count fuel lo hi : Nat) : Nat :=
  match fuel with
  | 0 => count
  | fuel + 1 =>
    if n >= hi then count
    else primesBetweenCount (n + 1) (if isPrime n then count + 1 else count) fuel lo hi

def primesBetween (lo hi : Nat) : Nat :=
  primesBetweenCount (lo + 1) 0 (hi - lo) lo hi

def verifyLegendre100 : Bool :=
  (List.range' 1 100).all (fun n =>
    primesBetween (n * n) ((n + 1) * (n + 1)) > 0)

def minPrimeCount100 : Nat :=
  (List.range' 1 100).foldl (fun acc n =>
    Nat.min acc (primesBetween (n * n) ((n + 1) * (n + 1)))) 10000

#eval verifyLegendre100
#eval minPrimeCount100

end Legendre
