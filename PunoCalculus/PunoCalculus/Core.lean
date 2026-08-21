structure ZetaZero where gamma : Float

def hadamardTerm (sigma t : Float) (z : ZetaZero) : Float :=
  (sigma - 0.5) / ((sigma - 0.5)^2 + (t - z.gamma)^2)

def hadamardSum (sigma t : Float) (zeros : List ZetaZero) : Float :=
  zeros.foldl (fun acc z => acc + hadamardTerm sigma t z) 0.0

def zetaZeros : List ZetaZero :=
  [ ⟨14.134725⟩, ⟨21.022040⟩, ⟨25.010858⟩, ⟨30.424876⟩,
    ⟨32.935062⟩, ⟨37.586178⟩, ⟨40.918719⟩, ⟨43.327073⟩,
    ⟨48.005151⟩, ⟨49.773832⟩ ]

def checkTermsPositive : Bool :=
  zetaZeros.all (fun z => hadamardTerm 0.6 10.0 z > 0.0)

def checkSumPositive : Bool :=
  hadamardSum 0.6 10.0 zetaZeros > 0.0

def checkNearLinePositive : Bool :=
  hadamardSum 0.51 100.0 zetaZeros > 0.0

def checkAllTestPoints : Bool :=
  hadamardSum 0.6 5.0 zetaZeros > 0.0 &&
  hadamardSum 0.55 14.13 zetaZeros > 0.0 &&
  hadamardSum 0.7 20.0 zetaZeros > 0.0 &&
  hadamardSum 0.51 100.0 zetaZeros > 0.0 &&
  hadamardSum 0.8 10.0 zetaZeros > 0.0

#eval checkTermsPositive
#eval checkSumPositive
#eval checkNearLinePositive
#eval checkAllTestPoints
