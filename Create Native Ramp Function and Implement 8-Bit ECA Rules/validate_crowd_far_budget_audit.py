import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_crowd_far_budget_audit import (  # noqa: E402
    _PEARSON_FLOOR,
    _SPEARMAN_CEIL,
    budget_certificates,
    far_data,
)

certs, stats = budget_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_fb_cells_indep"] == "PASS"
assert status["L_fb_ratio_f1"] == "PASS"
assert status["L_fb_budget"] == "HONEST_NEGATIVE"

f1, f2, far, ratio = far_data()
assert abs(stats["spearman"]) <= _SPEARMAN_CEIL
assert stats["pearson"] <= _PEARSON_FLOOR
assert stats["spearman"] > -_SPEARMAN_CEIL

print("crowd far budget audit validation passed")