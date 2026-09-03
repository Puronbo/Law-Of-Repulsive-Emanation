import json
import os
import subprocess
import sys

from experiments.emanation import repo_audit as ra

_DATA = os.path.join(os.path.dirname(os.path.abspath(ra.__file__)), "data")
_CRT = os.path.join(_DATA, "law_certificates.json")


def _backup_true():
    return os.path.exists(os.path.join(_DATA, "_law_cert_backup.json"))


def _backup_restore():
    if _backup_true():
        os.replace(os.path.join(_DATA, "_law_cert_backup.json"), _CRT)


def test_l14_gate6_conservation_pass():
    certs = ra.system_certificates()
    good = [c for c in certs if c["label"] == "L14_gate6_conservation"][0]
    assert good["status"] == "PASS"
    assert good["n_ok"] == 30 and good["n_fail"] == 0
    assert "credit_commons" in good["meta"]["measured_on"]


def test_l14_bad_credit_sum_invariant_fails():
    bad = [c for c in ra.system_certificates()
           if c["label"] == "L14_bad_credit_sum_invariant"][0]
    assert bad["status"] == "HONEST_NEGATIVE"
    assert bad["n_fail"] == 30 and bad["n_ok"] == 0


def test_full_table_contains_system_certs():
    labels = {c["label"] for c in ra.full_table()}
    assert "L14_gate6_conservation" in labels
    assert "L14_bad_credit_sum_invariant" in labels


def test_fresh_table_detects_drift():
    # backs up the real table, generates a full fresh table, tampers a
    # verdict field, and asserts the drift detector sees it
    os.replace(_CRT, os.path.join(_DATA, "_law_cert_backup.json"))
    try:
        ra.write_full_table()
        with open(_CRT, encoding="utf-8") as fh:
            tab = json.load(fh)
        for c in tab:
            if c["label"] == "L1_free_streaming_29":
                c["status"] = "HONEST_NEGATIVE"
        with open(_CRT, "w", encoding="utf-8") as fh:
            json.dump(tab, fh, indent=1, sort_keys=True)
        ok, drift = ra.fresh_table_matches()
        assert ok is False
        assert any("L1_free_streaming_29" in d for d in drift)
    finally:
        _backup_restore()


def test_cli_gate_ok():
    from experiments.emanation import law_discovery as ld
    env = dict(os.environ)
    r = subprocess.run([sys.executable, "scripts/certify_repo.py", "--gate"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    n_disco = len(ld.discovery_claims()[0])
    assert "all %d claims believed" % (18 + n_disco) in r.stdout


def test_cli_gate_covers_discovery_laws():
    from experiments.emanation import law_discovery as ld
    claims, veto = ld.discovery_claims()
    assert len(claims) == 48 and 105 in veto and 150 in veto
    r = subprocess.run([sys.executable, "scripts/certify_repo.py", "--gate"],
                       capture_output=True, text=True,
                       env=dict(os.environ))
    assert r.returncode == 0
    assert "all %d claims believed" % (18 + len(claims)) in r.stdout


def test_cli_claims_listing():
    r = subprocess.run([sys.executable, "scripts/certify_repo.py", "--claims"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert "commons reserve conservation" in r.stdout


def test_cli_regenerate_and_gate():
    r = subprocess.run([sys.executable,
                        "scripts/certify_repo.py", "--regenerate"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    r2 = subprocess.run([sys.executable, "scripts/certify_repo.py", "--gate"],
                        capture_output=True, text=True)
    assert r2.returncode == 0, r2.stdout + r2.stderr