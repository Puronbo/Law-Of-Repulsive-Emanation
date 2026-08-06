"""Autonomous applications built on puno_flow.

Each app is self-contained and runs without any central controller - the
units spread, repair, route, and audit themselves using the local-only
dynamics, the exact search index, creation, and per-unit ledgers.

    guard_mesh     - self-deploying, self-healing coverage mesh
    search_service - autonomous search-engine daemon with an op ledger
    router         - greedy geographic routing with self-healing reroutes
"""
