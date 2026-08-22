"""Part 2: Print results from the separatrix integration."""
import pickle, math

with open('sep_results.pkl', 'rb') as f:
    results = pickle.load(f)

def GeV_to_s(E):
    return 6.582e-25 / E if E > 0 else float('inf')
def GeV2_to_m2(G2):
    return G2 * 2.568e31

G_N = 6.709e-39
print("=" * 130)
print("PHYSICAL SCALE SETTING ALONG THE SEPARATRIX")
print("=" * 130)
print(f"{'k (GeV)':>12} {'G_tilde':>10} {'L_tilde':>10} {'G*L':>10} {'G_phys(1/GeV2)':>16} {'L_phys(GeV2)':>16} {'L_phys(1/m2)':>16}")
print("-" * 130)

n = len(results)
key_exps = [19, 18, 17, 16, 15, 14, 13, 12, 10, 5, 0, -5, -10, -20]
for exp in key_exps:
    k_target = 10.0**exp
    best = min(range(n), key=lambda i: abs(results[i][1] - k_target))
    t_RG, k, G_t, L_t, G_p, L_p, H, t_c = results[best]
    L_m2 = GeV2_to_m2(L_p)
    print(f"{k:12.2e} {G_t:10.6f} {L_t:10.6f} {G_t*L_t:10.6f} {G_p:16.6e} {L_p:16.6e} {L_m2:16.6e}")

r = results[-1]
print(f"\nFINAL: k={r[1]:.4e} GeV, G_t={r[2]:.6f}, L_t={r[3]:.6f}")
print(f"G_phys = {r[4]:.6e} GeV^-2 (observed: {G_N:.4e})")
L_m2 = GeV2_to_m2(r[5])
print(f"L_phys = {r[5]:.6e} GeV^2 = {L_m2:.6e} m^-2")
print(f"Observed L = 1.06e-52 m^-2")
if L_m2 != 0:
    print(f"Predicted / Observed = {L_m2 / 1.06e-52:.2e}")
print(f"Cosmic time: {r[7]:.6e} s")

# Find spiral minimum (closest to GFP)
min_d = 1e30
min_i = 0
for i, r in enumerate(results):
    d = math.sqrt(r[2]**2 + r[3]**2)
    if d < min_d:
        min_d = d
        min_i = i
rm = results[min_i]
print(f"\nSpiral minimum (closest to GFP):")
print(f"  k = {rm[1]:.4e} GeV, G_t = {rm[2]:.6f}, L_t = {rm[3]:.6f}")
print(f"  Distance to origin: {min_d:.6f}")
print(f"  G_phys = {rm[4]:.6e}, L_phys = {GeV2_to_m2(rm[5]):.6e} m^-2")
