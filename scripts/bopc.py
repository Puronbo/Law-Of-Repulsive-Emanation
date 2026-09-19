"""
BOPC v1 runner: read a BOPC contract, build the fixed corpus deterministically,
run the counted operator and independent reference over every token, and
exit 0 only if (a) every measured resource usage <= upper_bound and
(b) every semantic output is byte-identical to the reference.

Application lane only: this runner never touches the soliton register's
pinned counts (89 validators / 125 certificates).
"""

import json
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments"))

from bopc_candidate import eca_step_ref, eca_step_counted, bound_for

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    contract_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        REPO, "experiments", "bopc_contract.json")
    with open(contract_path) as fh:
        contract = json.load(fh)

    print("=" * 70)
    print("BOPC v1 runner  %s" % contract["ticket_id"])
    print("=" * 70)
    print("operator : %s" % contract["operator"])
    print("resource : %s" % contract["resource"])
    print("bound    : %s (proven closed)" % contract["upper_bound"]["formula"])
    print("semantics: %s (reference must byte-match)" % contract["semantics"])

    corpus = contract["corpus"]
    tokens = []
    for seed in range(corpus["seed_min"], corpus["seed_max"] + 1):
        for n in corpus["sizes"]:
            rng = random.Random(seed)
            cells = bytes(rng.getrandbits(1) for _ in range(n))
            for rule in corpus["rules"]:
                tokens.append((seed, n, rule, cells))
    print("corpus   : %d tokens (seeds %d..%d, sizes %s, rules %s)"
          % (len(tokens), corpus["seed_min"], corpus["seed_max"],
             corpus["sizes"], corpus["rules"]))

    failures = []
    measured_max = 0
    bound_max = 0
    for (seed, n, rule, cells) in tokens:
        ref = eca_step_ref(rule, cells)
        out, count = eca_step_counted(rule, cells)
        B = bound_for(n)
        measured_max = max(measured_max, count)
        bound_max = max(bound_max, B)
        if out != ref:
            failures.append((seed, n, rule, "semantic", len(cells)))
        if count > B:
            failures.append((seed, n, rule, "bound", count))

    print("\nmeasured max comparisons = %d   over all tokens" % measured_max)
    print("largest allowed bound    = %d   (n = %d)"
          % (bound_max, max(corpus["sizes"])))
    if failures:
        print("FAILURES: %d" % len(failures))
        for f in failures[:10]:
            print("  token seed=%d n=%d rule=%d kind=%s detail=%s" % f)
        print("=" * 70)
        sys.exit(1)
    print("\nBOPC - all %d tokens: outputs byte-identical, counts <= bound."
          % len(tokens))
    print("Exit 0 => contract {0} holds on the frozen corpus.".format(
        contract["ticket_id"]))
    print("=" * 70)
    sys.exit(0)


if __name__ == "__main__":
    main()