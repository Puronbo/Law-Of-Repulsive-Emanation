"""Demo: elastic soliton scattering -- the new physics rules 29/71 unlock.

Compares, side by side, what the original shift-bus rules (12/44/68/100)
CAN and CANNOT do against the density-conserving elastic rules 29/71.

Key result to observe:
  * rule 12 (original bus):   {10,11} --collide--> {12}     MERGE, 1 bit lost
  * rule 29 (elastic):        {a,a+1} --collide--> elastic phase shift,
                              count conserved, BOTH labels delivered.

ASCII trace of a rule-29 gap-1 collision carrying two labels.
"""
import shift_bus as sh
from experiments.emanation import elastic_shift as es


def trace(rule, a, b, T, width_show, origin):
    row = [0] * (origin + width_show + 2)
    row[a] = 1; row[b] = 1
    frames = []
    for t in range(T):
        if t % 1 == 0:
            s = "".join("1" if v else "." for v in row[origin:origin + width_show])
            frames.append((t, s))
        row = sh.step(rule, row)
    return frames


def main():
    print("=" * 62)
    print(" ELASTIC SOLITON SCATTERING (rules 29 / 71)")
    print("=" * 62)
    print()
    print("Original bus rules collide DESTRUCTIVELY:")
    print("  rule 12:  {10,11} -> {12}   (two packets -> one: info destroyed)")
    print()
    print("Elastic rules collide CONSERVATIVELY:")
    print("  rule 29:  {2000,2001} -> phase-shift, count stays 2")
    print()
    land, form, ok = es.collide(29, 2000, 2001, 60)
    print("  true landing:", sorted(land), " closed form:", sorted(form),
          " exact:", ok)
    tags = es.collide_tags(29, (2000, "A"), (2001, "B"), 60)
    print("  delivered labels:", tags)    # both survive
    print()
    print("ASCII evolution (rule 29, gap-1 couple, 'X' = occupied):")
    for t, s in trace(29, 1500, 1501, 16, 26, 1499):
        print("  t=%2d  %s" % (t, s))
    print()
    print("Compare rule 12 (destructive) same start:")
    for t, s in trace(12, 1500, 1501, 16, 26, 1499):
        print("  t=%2d  %s" % (t, s))
    print()
    print("Verdict: rules 29/71 add a conserved charge and elastic")
    print("scattering -- a reversible, label-preserving interaction the")
    print("original bus could not express.  This is 'physics' (elastic,")
    print("integrable, count-conserving) as opposed to pure delay-line.")


if __name__ == "__main__":
    main()