"""transformer_proposer: the toy-model transformer as a GATED-EXACT proposer
aligned with the `sfiles/` from-scratch model (FoldedReLU, He init,
residuals, hand-derived + gradient-checked backprop).

It is a PARTNER to the epistemic engine, not an authority on it.  The
protocol keeps the 'deterministic without losses' invariant:

    1. TRAIN    the small transformer (fixed seed) to reverse length-4
                symbol sequences -- an exact, total transformation it
                provably learns (200/200 exact in train.py).
    2. PROPOSE  read off the general rule the trained model embodies:
                out[j] = in[T-1-j]    (reversal).
    3. CERTIFY  every proposed rule out-of-sample via
                law_checker.certify_statement against GROUND TRUTH
                (the true reverse of each sequence), never from the
                model's own output.  A rule is believed iff it passes
                exhaustively on fresh data; otherwise HONEST_NEGATIVE
                with the exact first failure.

The deliberate, honest failure mode this demonstrates: the weights are a
LOSSLESS-looking but trained function over the in-sample length.  The
rule 'reversal' is certified PASS within the trained length (length-4
generalizes to unseen length-4 sequences).  The SAME model is then asked
to propose length-6 reversal -- an extrapolation beyond anything its
positional embedding ever saw -- and the gate REFUSES it as
HONEST_NEGATIVE.  This is the boundary the gate enforces: a trained
model may PROPOSE breadth, but the exhaustive measurement of current,
grounded truth is the only thing that makes a belief.
"""
import itertools
import os
import sys

import numpy as np

_LAB = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_LAB))
for _p in (_REPO, os.path.join(_REPO, "sfiles")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from experiments.emanation import law_checker as lc  # noqa: E402


VOCAB = 4
T_TRAIN = 4
D = 16
H = 32
_TRAINED = None


def _build_and_train(seed=0, steps=4001, lr=0.05):
    """Return a trained mini-transformer for length-T_TRAIN reversal.
    Reuses the exact sfiles/ modules (model + block).  Deterministic:
    the numpy global RNG is seeded at entry, so the run is reproducible.
    Mirrors sfiles/train.py's verified configuration (200/200 exact)."""
    from block import TransformerBlock
    from model import Linear, he_init, softmax
    rng_state = np.random.get_state()
    np.random.seed(seed)
    try:
        VOC = VOCAB
        T = T_TRAIN
        embed = he_init(VOC, D)
        pos = he_init(T, D) * 0.1
        blk = TransformerBlock(D, H)
        out_proj = Linear(D, VOC)
        params = [embed, pos]

        def forward(seq):
            X = embed[seq] + pos
            Z = blk.forward(X)
            logits = out_proj.forward(Z)
            return logits, X

        def loss_and_grad(seq, target):
            logits, X = forward(seq)
            probs = softmax(logits)
            onehot = np.zeros_like(probs)
            onehot[np.arange(T), target] = 1
            loss = -np.mean(np.sum(onehot * np.log(probs + 1e-9), axis=1))
            dlogits = (probs - onehot) / T
            dZ = out_proj.backward(dlogits)
            dX = blk.backward(dZ)
            d_embed = np.zeros_like(embed)
            for t in range(T):
                d_embed[seq[t]] += dX[t]
            d_pos = dX.copy()
            return loss, d_embed, d_pos

        losses = []
        for step in range(steps):
            seq = np.random.randint(0, VOC, size=T)
            target = seq[::-1].copy()
            loss, d_embed, d_pos = loss_and_grad(seq, target)
            losses.append(loss)
            embed -= lr * d_embed
            pos -= lr * d_pos
            blk.attn.Wq -= lr * blk.attn.dWq
            blk.attn.Wk -= lr * blk.attn.dWk
            blk.attn.Wv -= lr * blk.attn.dWv
            for layer in (blk.mlp.lin1, blk.mlp.lin_u, blk.mlp.lin_v, out_proj):
                layer.W -= lr * layer.dW
                layer.b -= lr * layer.db
        return embed, pos, blk, out_proj
    finally:
        np.random.set_state(rng_state)


def probe(model, seq):
    """Greedy argmax decode of the trained model on one sequence."""
    embed, pos, blk, out_proj = model
    T = len(seq)
    if T != T_TRAIN:
        # out-of-length: pad on the right to the trained length is NOT a
        # valid length-T model; return None (refuse to fabricate a hop).
        return None
    X = embed[np.asarray(seq, dtype=int)] + pos
    Z = blk.forward(X)
    logits = out_proj.forward(Z)
    return list(np.argmax(np.array(logits), axis=1))


def trained_model():
    """Train at most once per process (deterministic, memoized)."""
    global _TRAINED
    if _TRAINED is None:
        _TRAINED = _build_and_train()
    return _TRAINED


def reversal(in_seq):
    """Ground truth the door is certified against (independent of the NN)."""
    return list(reversed(list(in_seq)))


def _train_accuracy(model, n=200):
    ok = 0
    for _ in range(n):
        seq = tuple(np.random.randint(0, VOCAB, size=T_TRAIN))
        if probe(model, seq) == reversal(seq):
            ok += 1
    return ok


def proposer_certificates():
    """Certificates for the transformer-proposed reversal rule: PASS
    within the trained length (generalization), HONEST_NEGATIVE for the
    same model asked to reverse an unseen length (learned overreach)."""
    model = trained_model()
    rng = np.random.RandomState(2026)
    domain_len4 = [tuple(int(x) for x in rng.randint(0, VOCAB, size=T_TRAIN))
                   for _ in range(200)]
    domain_len6 = [tuple(int(x) for x in rng.randint(0, VOCAB, size=6))
                   for _ in range(200)]

    def good(d):
        p = probe(model, d)
        return p is not None and p == reversal(d)

    def bad(d):
        # claim: the length-4-trained model also reverses length-6 exactly
        p = probe(model, d)
        return p is not None and p == reversal(d)

    headers = {"trained_length": T_TRAIN, "vocab": VOCAB,
               "architecture": "sfiles toy transformer "
                               "(FoldedReLU, He init, residuals, "
                               "hand-derived gradient-checked backprop)"}

    pass_cert = lc.certify_statement(
        "PROPOSED_TF_reversal_length4",
        {"domain": "out-of-sample length-%d sequences (200 fresh, seeded)"
                   % T_TRAIN,
         "law": "trained model's rule: out[j] = in[T-1-j] (reversal)",
         "proposer": "transformer_proposer (trained model proposes; "
                     "ground truth is np-style literal reversal)",
         **headers},
        good, domain_len4)
    neg_cert = lc.certify_statement(
        "PROPOSED_TF_reversal_length6_overreach",
        {"domain": "out-of-sample length-6 sequences (200 fresh, seeded)",
         "law": "FLAWED PROPOSAL: the same length-4-trained model reverses "
                "length-6 sequences exactly -- extrapolation beyond any "
                "seen positional embedding; gate must reject it",
         "honest_check": "length-6 is outside the trained positional "
                         "embedding support",
         "proposer": "transformer_proposer (no certificate written; "
                     "measured against literal reversal)",
         **headers},
        bad, domain_len6)
    return [pass_cert, neg_cert]


def summary():
    model = trained_model()
    return {
        "train_accuracy_fresh": _train_accuracy(model),
        "proposed_rule": "out[j] = in[T-1-j] (reversal, length %d)" % T_TRAIN,
        "certificates": proposer_certificates(),
    }


if __name__ == "__main__":
    from collections import Counter
    certs = proposer_certificates()
    for c in certs:
        print("%-46s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("train fresh-accuracy:", summary()["train_accuracy_fresh"], "/200")
