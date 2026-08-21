def energyDecay (E0 nu t : Float) : Float :=
  if t <= 0.0 then E0
  else E0 / (1.0 + 2.0 * nu * t)^2

def enstrophyDecay (Z0 nu t : Float) : Float :=
  if t <= 0.0 then Z0
  else Z0 / (1.0 + 2.0 * nu * t)

def cascadeRatio (E0 Z0 nu t : Float) : Float :=
  if enstrophyDecay Z0 nu t > 0.0
  then (energyDecay E0 nu t) / (nu * enstrophyDecay Z0 nu t)
  else 0.0

def verifyRDecays : Bool :=
  cascadeRatio 1.0 1.0 0.01 0.0 > cascadeRatio 1.0 1.0 0.01 10.0 &&
  cascadeRatio 1.0 1.0 0.01 10.0 > cascadeRatio 1.0 1.0 0.01 50.0 &&
  cascadeRatio 1.0 1.0 0.01 50.0 > cascadeRatio 1.0 1.0 0.01 100.0

def verifyAllNSCases : Bool :=
  cascadeRatio 1.0 1.0 0.01 0.0 > cascadeRatio 1.0 1.0 0.01 10.0 &&
  cascadeRatio 1.0 1.0 0.1 0.0 > cascadeRatio 1.0 1.0 0.1 10.0 &&
  cascadeRatio 2.0 4.0 0.01 0.0 > cascadeRatio 2.0 4.0 0.01 10.0 &&
  cascadeRatio 0.5 0.5 0.01 0.0 > cascadeRatio 0.5 0.5 0.01 10.0 &&
  cascadeRatio 1.0 2.0 0.01 0.0 > cascadeRatio 1.0 2.0 0.01 10.0 &&
  cascadeRatio 3.0 1.0 0.01 0.0 > cascadeRatio 3.0 1.0 0.01 10.0 &&
  cascadeRatio 1.0 1.0 0.001 0.0 > cascadeRatio 1.0 1.0 0.001 10.0 &&
  cascadeRatio 5.0 5.0 0.01 0.0 > cascadeRatio 5.0 5.0 0.01 10.0 &&
  cascadeRatio 0.1 0.1 0.1 0.0 > cascadeRatio 0.1 0.1 0.1 10.0 &&
  cascadeRatio 10.0 10.0 0.01 0.0 > cascadeRatio 10.0 10.0 0.01 10.0 &&
  cascadeRatio 1.0 100.0 0.01 0.0 > cascadeRatio 1.0 100.0 0.01 10.0 &&
  cascadeRatio 100.0 1.0 0.01 0.0 > cascadeRatio 100.0 1.0 0.01 10.0

#eval verifyRDecays
#eval verifyAllNSCases
