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
import importlib.util

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments"))


def load_operator(contract):
    """Dynamically load the operator module and extract functions."""
    spec = contract["operator"]  # e.g., "eca_step@experiments/bopc_candidate.py"
    if "@" not in spec:
        raise ValueError("operator must be 'func@path/to/module.py'")
    func_name, mod_path = spec.split("@", 1)
    # Load module from path
    full_path = os.path.join(REPO, mod_path)
    module_name = os.path.splitext(os.path.basename(mod_path))[0]
    spec_obj = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec_obj)
    spec_obj.loader.exec_module(module)
    # Get the required functions
    ref_func = getattr(module, f"{func_name}_ref")
    counted_func = getattr(module, f"{func_name}_counted")
    bound_func = getattr(module, "bound_for")
    return ref_func, counted_func, bound_func


def build_corpus(contract):
    """Build corpus tokens from contract spec. Supports three formats."""
    corp = contract["corpus"]
    tokens = []

    # Format 1: ECA-style with sizes list and rules list
    if "sizes" in corp and "rules" in corp:
        for seed in range(corp["seed_min"], corp["seed_max"] + 1):
            for n in corp["sizes"]:
                rng = random.Random(seed)
                cells = bytes(rng.getrandbits(1) for _ in range(n))
                for rule in corp["rules"]:
                    tokens.append((seed, n, rule, cells))
        desc = f"seeds {corp['seed_min']}..{corp['seed_max']}, sizes {corp['sizes']}, rules {corp['rules']}"

    # Format 2: fixed-size arrays with single size
    elif "size" in corp:
        n = corp["size"]
        for seed in range(corp["seed_min"], corp["seed_max"] + 1):
            rng = random.Random(seed)
            arr = [rng.randint(0, 255) for _ in range(n)]
            tokens.append((seed, n, None, arr))
        desc = f"seeds {corp['seed_min']}..{corp['seed_max']}, size {n}"

    # Format 3: SipHash-style with max_msg_len
    elif "max_msg_len" in corp:
        for seed in range(corp["seed_min"], corp["seed_max"] + 1):
            rng = random.Random(seed)
            # 16-byte key
            key = bytes(rng.getrandbits(8) for _ in range(16))
            # Random message length 0..max_msg_len
            msg_len = rng.randint(0, corp["max_msg_len"])
            msg = bytes(rng.getrandbits(8) for _ in range(msg_len))
            tokens.append((seed, msg_len, None, (key, msg)))
        desc = f"seeds {corp['seed_min']}..{corp['seed_max']}, max_msg_len {corp['max_msg_len']}"

    else:
        raise ValueError("corpus must have either 'sizes'+'rules' or 'size' or 'max_msg_len'")

    return tokens, desc


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

    ref_func, counted_func, bound_func = load_operator(contract)
    tokens, desc = build_corpus(contract)
    print("corpus   : %d tokens (%s)" % (len(tokens), desc))

    failures = []
    measured_max = 0
    bound_max = 0
    for token in tokens:
        seed, n, rule, inp = token
        if rule is not None:
            ref = ref_func(rule, inp)
            out, count = counted_func(rule, inp)
        elif isinstance(inp, tuple) and len(inp) == 2:
            # SipHash format: (key, msg)
            key, msg = inp
            ref = ref_func(key, msg)
            out, count = counted_func(key, msg)
        else:
            ref = ref_func(inp)
            out, count = counted_func(inp)
        B = bound_func(n)
        measured_max = max(measured_max, count)
        bound_max = max(bound_max, B)
        if out != ref:
            failures.append((seed, n, rule, "semantic", len(inp) if hasattr(inp, '__len__') else n))
        if count > B:
            failures.append((seed, n, rule, "bound", count))

    print("\nmeasured max %s = %d   over all tokens" % (contract["resource"], measured_max))
    print("largest allowed bound    = %d" % bound_max)
    if failures:
        print("FAILURES: %d" % len(failures))
        for f in failures[:10]:
            print("  token seed=%d n=%d rule=%s kind=%s detail=%s" % f)
        print("=" * 70)
        sys.exit(1)
    print("\nBOPC - all %d tokens: outputs byte-identical, counts <= bound."
          % len(tokens))
    print("Exit 0 => contract {%s} holds on the frozen corpus." % contract["ticket_id"])
    print("=" * 70)
    sys.exit(0)


if __name__ == "__main__":
    main()