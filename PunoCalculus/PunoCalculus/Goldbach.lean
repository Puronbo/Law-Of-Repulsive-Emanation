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
  (List.range' 4 97 2).all (fun n => goldbachReps n > 0)

#eval verifyGoldbach100

end Goldbach
