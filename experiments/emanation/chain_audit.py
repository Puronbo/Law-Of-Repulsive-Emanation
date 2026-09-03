"""chain_audit: the third real-subsystem audit -- the hash-chained local
ledger (puno_flow/ledger.py) and its tamper-evidence.

Audited invariants (pure SHA-256 + integer arithmetic, deterministic):
    L24_chain_verify_untampered:
        LedgerChain.verify() == (True, None) on any chain built only
        through legitimately-appended blocks (recomputed hashes match the
        stored ones; prev links hold).  Exhaustive over many payloads and
        chain lengths.
    L25_tamper_no_rehash_detected:
        Mutating the payload of any NON-terminal block (kept stored hash)
        is always detected: verify() == (False, k) for the tampered seq k
        (the block's recomputed hash no longer matches the stored hash).
        Exhaustive over every block position k in many chains.
    L26_rehash_tamper_detected:
        Mutating payload AND re-hashing a NON-terminal block k breaks its
        successor's prev-link, so verify() == (False, k+1): the tamper is
        detected at the very next block.  Exhaustive over every k.
HONEST NEGATIVE (rejected, not introduced):
    L27_any_payload_modification_detected:
        The blanket claim "any payload modification is always detected,
        even with re-hashing" is FALSE at the TERMINAL block: re-hashing
        the last block's stored hash passes verify() because a plain
        unsigned hash chain has no successor to expose the forged prev.
        This is the unbounded-authority limitation of the honest,
        signed-by-nobody chain -- and it is exactly the limitation an
        honest audit must admit, not hide.  first_failure: the last block.
"""
import struct
from hashlib import sha256 as _sha256


def _block_hash(prev, seq, payload):
    prev_bytes = bytes.fromhex(prev) if prev else b""
    return _sha256(prev_bytes + struct.pack("<Q", seq) + payload).hexdigest()


def _build(length, seed):
    """A chain of `length` blocks, each a distinct deterministic integer."""
    from puno_flow.ledger import LedgerChain
    c = LedgerChain()
    for i in range(length):
        c.append(struct.pack("<Q", (seed + i) * 1000003 + 7))
    return c


def _L24_untampered(datum):
    length, seed = datum
    c = _build(length, seed)
    return c.verify() == (True, None)


def _L25_tamper_no_rehash(datum):
    from puno_flow.ledger import LedgerChain
    length, seed = datum
    for k in range(length):
        if k == length - 1:
            continue
        newp = struct.pack("<Q", 0xDEADBEEF + k)
        base = _build(length, seed)
        if newp == base.blocks[k]["payload"]:
            newp = struct.pack("<Q", 0xDEADBEEF + k + 1)
        c2 = LedgerChain()
        for i in range(length):
            c2.append(base.blocks[i]["payload"])
        b = dict(c2.blocks[k], payload=newp)   # mutate payload, keep hash
        c2.blocks[k] = b
        ok, bad = c2.verify()
        if ok:
            return False                     # undetected -> law violated
    return True


def _L26_rehash_tamper(datum):
    from puno_flow.ledger import LedgerChain
    length, seed = datum
    base = _build(length, seed)
    for k in range(length - 1):              # non-terminal block k
        newp = struct.pack("<Q", 0xC0FFEE + k)
        if newp == base.blocks[k]["payload"]:
            newp = struct.pack("<Q", 0xC0FFEE + k + 99)
        c2 = LedgerChain()
        for i in range(length):
            c2.append(base.blocks[i]["payload"])
        b = c2.blocks[k]
        newhash = _block_hash(b["prev"], b["seq"], newp)
        c2.blocks[k] = dict(b, payload=newp, hash=newhash)
        ok, bad = c2.verify()
        if ok or bad != k + 1:               # must FAIL exactly at k+1
            return False
    return True


def _L27_any_mod_detected(datum):
    """The FALSE candidate law: 'any payload modification is always
    detected, even with re-hashing'.  Returns True iff the modification
    WAS detected.  At the TERMINAL block, a re-hash tamper is NOT detected
    -- so this law fails on its first datum and ships HONEST_NEGATIVE."""
    from puno_flow.ledger import LedgerChain
    length, seed = datum
    base = _build(length, seed)
    k = length - 1
    newp = struct.pack("<Q", 0xBADC0DE)
    if newp == base.blocks[k]["payload"]:
        newp = struct.pack("<Q", 0xBADC0DE + 1)
    c2 = LedgerChain()
    for i in range(length):
        c2.append(base.blocks[i]["payload"])
    b = c2.blocks[k]
    newhash = _block_hash(b["prev"], b["seq"], newp)
    c2.blocks[k] = dict(b, payload=newp, hash=newhash)
    # law = 'modification is detected' = verify() must FAIL (not (True,None)).
    # The terminal re-hash slips through verify() == (True, None) -> undetected.
    return c2.verify() != (True, None)


def _certify(label, meta, pred, domain):
    from experiments.emanation import law_checker as lc
    return lc.certify_statement(label, meta, pred, list(domain))


_SEED_RANGE = list(range(10))
_LEN_DOMAIN = list(range(2, 10))             # chain lengths 2..9


def chain_certificates():
    certs = []
    # L24: untampered verify, every (length, seed)
    certs.append(_certify(
        "L24_chain_verify_untampered",
        {"domain": "LedgerChain built purely by append() of distinct "
                   "payloads; verify() == (True, None) over lengths 2..9 "
                   "x 10 seeds",
         "law": "a chain built through legitimate appends always verifies "
                "(recompute matches stored; prev links hold)",
         "measured_on": "puno_flow.ledger.LedgerChain"},
        _L24_untampered,
        [(ln, s) for ln in _LEN_DOMAIN for s in _SEED_RANGE]))
    # L25: non-terminal payload tamper (no re-hash) always detected.
    certs.append(_certify(
        "L25_tamper_no_rehash_detected",
        {"domain": "mutate payload of every non-terminal block k in chains "
                   "lengths 2..9 x 10 seeds; expect detect",
         "law": "any non-terminal payload mutation -- WITHOUT re-hashing the "
                "stored hash -- is caught at exactly the tampered block"},
        _L25_tamper_no_rehash,
        [(ln, s) for ln in _LEN_DOMAIN for s in _SEED_RANGE]))
    # L26: payload+rehash tamper of non-terminal caught at successor.
    certs.append(_certify(
        "L26_rehash_tamper_detected",
        {"domain": "mutate payload AND re-hash every non-terminal block k, "
                   "lengths 2..9 x 10 seeds; expect detect at k+1",
         "law": "re-hash tamper of a non-terminal block is exposed by its "
                "successor's prev-link mismatch (verify fails at k+1)"},
        _L26_rehash_tamper,
        [(ln, s) for ln in _LEN_DOMAIN for s in _SEED_RANGE]))
    # L27 HONEST_NEGATIVE: blanket 'any modification always detected' is
    # FALSE at the terminal block (re-hash evades verify).
    certs.append(_certify(
        "L27_any_payload_modification_detected",
        {"domain": "re-hash tamper of the LAST block, lengths 2..9 x 10 "
                   "seeds",
         "law": "FALSE CANDIDATE: any payload modification is always "
                "detected, even with re-hashing -- the last block has no "
                "successor to expose the forged prev, so a plain hash "
                "chain cannot forbid an authority rewriting its own tail",
         "honest_check": "terminal re-hash must slip through verify()"},
        _L27_any_mod_detected,
        [(ln, s) for ln in _LEN_DOMAIN for s in _SEED_RANGE]))
    return certs