import Mathlib

namespace RoleCollision

/-- The *equation* reading: `x = x + 1` as a statement of equality. -/
def EqReading (x : ℤ) : Prop := x = x + 1

/-- The equation reading is unsatisfiable: it forces `0 = 1`. -/
theorem eq_reading_unsat (x : ℤ) : ¬ EqReading x := by
  unfold EqReading; omega

/-- From the equation reading, *anything* follows (ex falso): here `0 = 1`. -/
theorem eq_reading_implies_zero_eq_one (x : ℤ) (h : EqReading x) : (0 : ℤ) = 1 := by
  unfold EqReading at h; omega

/-- The *recurrence* reading: `x_{t+1} = x_t + 1`, a state map. -/
def Step (x : ℤ) : ℤ := x + 1

/-- The recurrence is fine and has a closed form: starting at `x₀`, the value at
step `t` is `x₀ + t`. -/
theorem recurrence_closed_form (x0 : ℤ) (t : ℕ) : (Step^[t]) x0 = x0 + t := by
  induction t with
  | zero => simp
  | succ t ih => simp [Function.iterate_succ_apply', Step, ih]; ring

/-- Reading the recurrence as an *equation on a single variable* is exactly the
role collision: it would require `x = Step x`. -/
theorem recurrence_as_equation_is_collision (x : ℤ) : Step x = x ↔ (0 : ℤ) = 1 := by
  unfold Step; omega

/-- The two readings are *different propositions*: the recurrence at a fixed
`t ≥ 1` is satisfiable, the equation never is. No contradiction arises once the
role (state vs. value) is kept distinct. -/
theorem readings_differ (x0 : ℤ) : (Step^[1]) x0 = x0 + 1 ∧ ¬ EqReading x0 := by
  refine ⟨?_, ?_⟩
  · simp [Step]
  · exact eq_reading_unsat x0

end RoleCollision

#eval (RoleCollision.Step 0)      -- 1
#eval ((RoleCollision.Step^[5]) 0) -- 5
