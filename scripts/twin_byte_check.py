"""twin_byte_check: planner-only, read-only byte-normalization audit.

The register's own truth is that the SHA-512 closure over the seven
vendored twin sources recomputes byte-identically to SUITE_CLOSURE_SHA
(also check #10 of the meta-audit).  This script re-derives that AND
normalizes the vendored twins against every on-disk mirror of the
twin project, so a domain reviewer can see, byte-for-byte, that the
vendored tree equals the origin checkout.  Planner-only: mirror diffs
are REPORTED, not gated; exit 0 requires ONLY the closure pin match.
Read-only: no file is written; nothing is staged.
"""
import hashlib
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PW = WORKSPACE / "PunoCalculus" / "PunoCalculus"
VENDOR = PW / "PunoTwin"

SUITE_CLOSURE_SHA = \
    "9fff39883f799f96bca6d283d225f053a4f5232b067f73798c2e12d54d57d0c5d\
302612de5b3e5e4a5b3f46252811e4d71a281e586f95001cf9cf599c88b7794"

TWINS = ["EcaIsometry.lean", "MillenniumBridge.lean",
         "TwinAnalyticLaws.lean", "TwinRingLaws.lean",
         "MPOperator.lean", "CollatzReach.lean", "DirichletLaws.lean"]

# On-disk mirrors of the twin project (origin checkout copies), checked
# for byte-equality of the derivable 5 (the prose two are vendor-only).
MIRRORS = [
    WORKSPACE / "fcc2" / "Millennium-Prize-Problem-Lean-4-Proof" / "PunoTwin",
    Path("C:/Users/Me/Desktop/Mamamogobyerno/fcc2/"
         "Millennium-Prize-Problem-Lean-4-Proof/PunoTwin"),
]


def per_file_digests() -> dict[str, bytes]:
    digest = {}
    for name in TWINS:
        p = PW / name
        if not p.exists():
            p = VENDOR / name
        digest[name] = p.read_bytes()
    return digest


def closure_digest(blobs: dict[str, bytes]) -> str:
    agg = hashlib.sha512()
    for name in sorted(blobs):
        agg.update(name.encode("utf-8") + b"\x00")
        agg.update(blobs[name])
    return agg.hexdigest()


def main() -> int:
    print("twin byte-normalization audit (planner-only, read-only)")
    blobs = per_file_digests()
    closed = closure_digest(blobs)
    ok = closed == SUITE_CLOSURE_SHA
    print("  closure recompute: %s%s" %
          (closed[:12] + "...",
           "  ==  pinned" if ok else "  !=  pinned %s..." %
           SUITE_CLOSURE_SHA[:12]))
    print("  per-file SHA-512 (vendored tree):")
    for name in sorted(blobs):
        print("    %s  %s" % (hashlib.sha512(blobs[name]).hexdigest()[:16],
                              name))
    for mirror in MIRRORS:
        if not mirror.is_dir():
            print("  mirror not found (informational): %s" % mirror)
            continue
        for name in ["TwinAnalyticLaws.lean", "TwinRingLaws.lean",
                     "MPOperator.lean", "CollatzReach.lean",
                     "DirichletLaws.lean"]:
            p = mirror / name
            if not p.exists():
                print("  admin mirror MISSING twin (informational): %s"
                      % p)
                continue
            same = p.read_bytes() == blobs[name]
            print("  mirror byte-equal: %s  %s  <- %s" %
                  ("yes" if same else "NO ", name, mirror.parent))
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())