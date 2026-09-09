"""End-to-end showcase for shift_dsl: verified shift-spec language.

Three views of one spec:
  - two opposite-direction lanes with expect clauses
  - bus mode: two packets sharing one lane (multiplexed), separated
  - verification report + fused-lane separation differential
"""

import sys

if __name__ == '__main__':
    sys.path.insert(0, r'C:\\Users\\Me\\Downloads\\Puno_Calculus')

import shift_dsl as sd

SPEC = """
# --- verified shift-bus spec -------------------------------------------
lane right1 rule 12        # pure +1 single-cell shifter
lane left1  rule 100       # period-2 blob, head -1
packet A on right1 at 1000, 1003, 1007
packet B on left1  at 4000, 4010
run 250
expect A at 1250, 1253, 1257
expect B at 3750, 3760
"""

BUS_SPEC = """
# --- bus mode: two packets multiplexed on ONE lane ----------------------
lane trunk rule 12
packet A on trunk at 500
packet B on trunk at 900
run 100
expect A at 600
expect B at 1000
"""

if __name__ == '__main__':
    for label, spec in (('two-lane spec', SPEC), ('bus mode', BUS_SPEC)):
        print('=== %s ===' % label)
        evolved, report, separation = sd.run_spec(spec)
        for name, res in sorted(report.items()):
            print('  %-4s: %s -> %s  [ok=%s%s]' % (
                name, res['expected'], res['actual'], res['ok'],
                ' boundary' if res['boundary_affected'] else ''))
        print('  lane separation:', {k: 'OK' if v else 'VIOLATED'
                                     for k, v in separation.items()})