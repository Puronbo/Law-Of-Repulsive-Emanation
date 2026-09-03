"""Gate tests for the toy transformer as a gated-exact proposer: the
proposed reversal rule is certified PASS within the trained length, and
the same model's extrapolation beyond its positional embedding support is
rejected HONEST_NEGATIVE with an exact counter-example."""
import json
import os

from experiments.emanation import transformer_proposer as tp
from experiments.emanation import repo_audit as ra


def test_length4_reversal_proposal_passes_out_of_sample():
    certs = tp.proposer_certificates()
    good = [c for c in certs if c["label"] == "PROPOSED_TF_reversal_length4"][0]
    assert good["status"] == "PASS"
    assert good["n_ok"] > 0 and good["n_fail"] == 0


def test_length6_overreach_is_honest_negative():
    certs = tp.proposer_certificates()
    neg = [c for c in certs
           if c["label"] == "PROPOSED_TF_reversal_length6_overreach"][0]
    assert neg["status"] == "HONEST_NEGATIVE"
    assert neg["n_fail"] > 0 and neg["n_ok"] == 0
    assert neg["first_failure"] is not None


def test_trained_model_generalizes_within_trained_length():
    model = tp.trained_model()
    assert tp._train_accuracy(model, n=200) == 200


def test_labels_present_in_full_table():
    labels = {c["label"] for c in ra.full_table()}
    assert "PROPOSED_TF_reversal_length4" in labels
    assert "PROPOSED_TF_reversal_length6_overreach" in labels
