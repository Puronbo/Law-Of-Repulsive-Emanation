"""Hardened launcher for the Multi-Chain Wallet Matrix API.

Environment (all optional):
  IMAM_MNEMONIC  the ONLY secret -- the anchor mnemonic. Injected before import.
  HOST           bind address; default 127.0.0.1 (loopback only -- do NOT expose
                 0.0.0.0 to an untrusted network without TLS + a token).
  PORT           listen port; default 8000.
  TLS_CERT       path to a PEM certificate; enables HTTPS when set with TLS_KEY.
  TLS_KEY        path to the matching PEM private key.
  API_TOKEN      if set, every /api/* route requires 'Authorization: Bearer <token>'.

Key custody: the mnemonic comes from the environment only, private keys are
derived in memory and never persisted, and consensus verifiers hold public keys
only. See SECURITY.md for the full threat model.
"""

import os

IMAM_MNEMONIC = os.environ.get("IMAM_MNEMONIC", "")
if not IMAM_MNEMONIC:
    raise SystemExit("IMAM_MNEMONIC is not set; refusing to boot without the secret.")

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))
TLS_CERT = os.environ.get("TLS_CERT", "")
TLS_KEY = os.environ.get("TLS_KEY", "")
API_TOKEN = os.environ.get("API_TOKEN", "")

import uvicorn

if __name__ == "__main__":
    ssl_kwargs = {}
    if TLS_CERT and TLS_KEY:
        ssl_kwargs = {"ssl_certfile": TLS_CERT, "ssl_keyfile": TLS_KEY}
    scheme = "https" if ssl_kwargs else "http"
    print(f"[run_server] {scheme}://{HOST}:{PORT} "
          f"(tls={'on' if ssl_kwargs else 'off'}, "
          f"token={'on' if API_TOKEN else 'off'})")
    uvicorn.run("server:app", host=HOST, port=PORT, **ssl_kwargs)
