import numpy as np
import json
import os

np.random.seed(42)

def hyperbolic_dist(u, v):
    """Calculates exact geodesic distance in the Poincaré disk."""
    sq_norm_u = np.sum(u**2)
    sq_norm_v = np.sum(v**2)
    sq_dist = np.sum((u - v)**2)
    denom = max((1.0 - sq_norm_u) * (1.0 - sq_norm_v), 1e-12)
    return np.arccosh(1.0 + 2.0 * sq_dist / denom)

# Core global taxonomy setup (The Universe of Knowledge)
knowledge_base = {
    "nodes": [
        {"id": "Origin", "label": "C_0: Pure Awareness", "tier": 0},
        {"id": "System", "label": "Abstract System", "tier": 1},
        {"id": "Matter", "label": "Physical Matter", "tier": 1},
        {"id": "Idea", "label": "Conceptual Idea", "tier": 1},
        {"id": "Bio", "label": "Biological Organisms", "tier": 2},
        {"id": "Tech", "label": "Computing Infrastructure", "tier": 2},
        {"id": "Art", "label": "Creative Arts", "tier": 2},
        {"id": "Mammal", "label": "Mammalian Branch", "tier": 3},
        {"id": "Silicon", "label": "Silicon Hard Systems", "tier": 3},
        {"id": "Music", "label": "Sonic Wave Theory", "tier": 3}
    ],
    "edges": [
        {"source": "Origin", "target": "System"},
        {"source": "Origin", "target": "Matter"},
        {"source": "Origin", "target": "Idea"},
        {"source": "System", "target": "Tech"},
        {"source": "Matter", "target": "Bio"},
        {"source": "Idea", "target": "Art"},
        {"source": "Bio", "target": "Mammal"},
        {"source": "Tech", "target": "Silicon"},
        {"source": "Art", "target": "Music"}
    ]
}

# Initializing trained coordinates based on hyperbolic radial tiers
positions = {
    "Origin": np.array([0.0, 0.0]),
    "System": np.array([-0.15, 0.10]),
    "Matter": np.array([0.18, -0.05]),
    "Idea": np.array([-0.05, -0.18]),
    "Tech": np.array([-0.40, 0.30]),
    "Bio": np.array([0.45, -0.20]),
    "Art": np.array([-0.10, -0.45]),
    "Mammal": np.array([0.70, -0.35]),
    "Silicon": np.array([-0.65, 0.50]),
    "Music": np.array([-0.20, -0.75])
}

def inject_and_evaluate_novelty(query_text, context_affinities):
    """
    Simulates your Universal Novelty Detector. If context affinities are poor,
    the mathematical repulsion vector flings the probe toward the boundary horizon (r -> 1).
    """
    print(f"\nEvaluating Input Probe: '{query_text}'")
    
    if not context_affinities:
        xq = (np.random.rand(2) - 0.5) * 0.05
    else:
        xq = np.mean([positions[k] for k in context_affinities], axis=0) * 0.5
        
    lr = 0.02
    epochs = 200
    alpha = 2.5 
    
    for epoch in range(epochs):
        grad = np.zeros(2)
        eps = 1e-5
        
        for node_id, pos in positions.items():
            if node_id in context_affinities:
                continue 
            
            d = hyperbolic_dist(xq, pos)
            if d < alpha:
                xq_p0 = xq.copy(); xq_p0[0] += eps
                d_p0 = hyperbolic_dist(xq_p0, pos)
                g0 = (max(0, alpha - d_p0)**2 - max(0, alpha - d)**2) / eps
                
                xq_p1 = xq.copy(); xq_p1[1] += eps
                d_p1 = hyperbolic_dist(xq_p1, pos)
                g1 = (max(0, alpha - d_p1)**2 - max(0, alpha - d)**2) / eps
                
                grad += np.array([g0, g1])
        
        riemannian_factor = ((1.0 - np.sum(xq**2))**2) / 4.0
        xq = xq - lr * grad * riemannian_factor
        
        radius = np.linalg.norm(xq)
        if radius >= 0.99:
            xq = (xq / radius) * 0.99
            
    final_radius = np.linalg.norm(xq)
    print(f"-> Settled Position: {xq}")
    print(f"-> Universal Novelty Score (Radius): {final_radius:.4f}")
    
    if final_radius > 0.85:
        print("-> ALERT: Absolute Out-Of-Distribution Novelty Detected at the Horizon!")
    else:
        print("-> STATUS: Element safely integrated into structural tree taxonomy.")
        
    return xq.tolist(), final_radius

pos1, r1 = inject_and_evaluate_novelty("Advanced Multi-threaded Silicon Processor", ["Tech", "Silicon"])
pos2, r2 = inject_and_evaluate_novelty("The quadratic equation ate a very sad banana for breakfast", [])

visualization_export = []
for node_id, pos in positions.items():
    node_meta = next(n for n in knowledge_base["nodes"] if n["id"] == node_id)
    visualization_export.append({
        "id": node_id, "label": node_meta["label"], "tier": node_meta["tier"], "x": pos[0], "y": pos[1], "type": "known"
    })

visualization_export.append({"id": "Probe_Structured", "label": "Structured Input", "tier": 4, "x": pos1[0], "y": pos1[1], "type": "probe"})
visualization_export.append({"id": "Probe_Anomaly", "label": "Universal Chaos Anomaly", "tier": 4, "x": pos2[0], "y": pos2[1], "type": "anomaly"})

with open("web_data.json", "w") as f:
    json.dump(visualization_export, f, indent=4)
print("\n[Engine Execution Complete: Exported metadata map to web_data.json]")