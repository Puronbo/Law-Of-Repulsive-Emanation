"""
T55i: FILL THE NET WITH MORE WIDELY-USED WEBSITES.

T55h showed the ~20k ceiling is FLOW (all-pairs kNN), not capacity -
holding sites is ~2 KB each (dim=128 q+h), so 60% of this machine's
31.7 GB RAM would hold ~9.3 million sites.  This experiment uses that
headroom: it merges TWO independent real top-1M popularity lists
(Cisco Umbrella + Majestic Million), dedupes, orders by best rank
(most widely used first), embeds every domain, loads the whole union,
verifies routing + outage survival, and PERSISTS the result as a
reusable internet-net checkpoint (net + domain label map).

  PART 1  union + dedupe of two real top-1M lists
  PART 2  capacity: n sites in q+h, RAM usage, how far 60% RAM goes
  PART 3  nearest-centroid routing of widely-used sites
  PART 4  outage: kill 20% of the union; survivors keep routing
  PART 5  persist checkpoint; reload and verify identical routing

Usage: python decentral_net_union.py  (uses both CSVs from top1m dir)
"""

import numpy as np
import sys, os, time, pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.decentral_net import DecentralNet
from sklearn.feature_extraction.text import HashingVectorizer

TOP = os.path.expandvars(r'%LOCALAPPDATA%\Temp\opencode\top1m')
UMB = os.path.join(TOP, 'top-1m.csv')
MJS = os.path.join(TOP, 'majestic_million.csv')
OUT = os.path.join(TOP, 'internet_net.pkl')

DIM = 128
NGRAM = (2, 4)
FAMOUS = ['google.com', 'wikipedia.org', 'amazon.com', 'youtube.com',
          'github.com', 'openai.com', 'apple.com', 'netflix.com',
          'stackoverflow.com', 'reddit.com',
          'microsoft.com', 'cloudflare.com', 'baidu.com', 'tiktok.com',
          'linkedin.com', 'bing.com', 'x.com', 'zoom.us']


def embed(domains):
    t0 = time.time()
    hv = HashingVectorizer(analyzer='char_wb', ngram_range=NGRAM,
                           n_features=DIM, norm='l2', alternate_sign=True)
    X = hv.transform(domains).toarray().astype(np.float64)
    print(f"  embedded {len(domains):,} domains -> {X.shape} "
          f"({X.nbytes/1e6:.0f} MB) in {time.time()-t0:.1f}s")
    return X


def neighbors(anchors, q, k=4):
    sims = anchors @ q                       # unit-norm rows => cosine
    order = np.argsort(-sims)[:k]
    return order, sims[order]


print("=" * 72)
print("T55i: FILL THE NET WITH MORE WIDELY-USED WEBSITES")
print(f"  dim={DIM} char-ngram={NGRAM}")
print("=" * 72)

# -------------------- PART 1: union + dedupe -------------------- #
t0 = time.time()
rank = {}
n_umb = 0
for l in open(UMB, encoding='utf-8', errors='ignore'):
    _, d = l.split(',', 1)
    d = d.strip().lower()
    rank[d] = 1                                # Umbrella rank ~ popularity
    n_umb += 1
n_mjs = 0
with open(MJS, encoding='utf-8', errors='ignore') as f:
    next(f)                                    # header
    for l in f:
        parts = l.split(',')
        if len(parts) < 3:
            continue
        d = parts[2].strip().lower()
        r = int(parts[0])
        if d not in rank or r < rank[d]:
            rank[d] = r
        n_mjs += 1
ranked = sorted(rank.items(), key=lambda kv: kv[1])     # most-used first
domains = [d for d, _ in ranked]
print(f"\nPART 1: UNION of two real top-1M popularity lists "
      f"({time.time()-t0:.1f}s)")
print(f"  Umbrella {n_umb:,} + Majestic {n_mjs:,} "
      f"entries -> {len(domains):,} unique domains after dedupe")

# -------------------- PART 2: capacity -------------------- #
X = embed(domains)
n, dim = X.shape
idx = {d: i for i, d in enumerate(domains)}
t0 = time.time()
net = DecentralNet(dim=dim, k=8, mu0=0.12)
net.add_many(X)                              # one neuron per site, home = embed
load_s = time.time() - t0
gb = (net.q.nbytes + net.h.nbytes) / 1e9
print("\n" + "-" * 72)
print("PART 2: CAPACITY - flow is the only ceiling, holding is ~2 KB/site")
print(f"  {net.n:,} neurons  q+h = {gb:.2f} GB  load {load_s:.1f}s (vectorized)")
print(f"  60% of this 31.7 GB machine would hold ~{0.6*31.7e9/2048/1e6:.1f}M")
print(f"  widely-used sites at dim=128 - many multiples of the top-1M.")
print(f"  (the whole top-{len(domains)//1000}k union needs only {gb:.2f} GB)")

# -------------------- PART 3: routing -------------------- #
print("\n" + "-" * 72)
print("PART 3: NEAREST-CENTROID ROUTING - query a site, get its web")
print("  neighbors across the merged popularity lists")
present = [d for d in FAMOUS if d in idx]
for q in present:
    j, s = neighbors(net.q, X[idx[q]], k=3)
    print(f"  {'%-20s' % q} -> "
          f"{' | '.join('%-24s %.3f' % (domains[k], v) for k, v in zip(j, s))}")

# -------------------- PART 4: outage -------------------- #
print("\n" + "-" * 72)
print("PART 4: OUTAGE - kill 20% of the union (random)")
rng = np.random.RandomState(42)
kill = rng.choice(n, size=int(0.2 * n), replace=False)
surv_idx = np.setdiff1d(np.arange(n), kill)
surv_domains = [domains[i] for i in surv_idx]
net.remove(list(kill))
print(f"  killed {len(kill):,} sites -> survivors {net.n:,} "
      f"(no repair unit)")
for q in present:
    j, s = neighbors(net.q, X[idx[q]], k=3)
    print(f"  {'%-20s' % q} -> "
          f"{' | '.join('%-24s %.3f' % (surv_domains[k], v) for k, v in zip(j, s))}")

# -------------------- PART 5: persist + reload -------------------- #
print("\n" + "-" * 72)
print("PART 5: PERSIST the internet net as a reusable checkpoint")
t0 = time.time()
with open(OUT, 'wb') as f:
    pickle.dump({'net': net, 'domains': surv_domains}, f, protocol=4)
save_s = time.time() - t0
sz = os.path.getsize(OUT) / 1e6
print(f"  saved {net.n:,} survivors + domain map -> {os.path.basename(OUT)} "
      f"({sz:.0f} MB, {save_s:.1f}s)")
t0 = time.time()
with open(OUT, 'rb') as f:
    art = pickle.load(f)
load_s = time.time() - t0
net2, dom2 = art['net'], art['domains']
same_q = np.array_equal(net.q, net2.q)
ok = all(np.array_equal(net.q[i], net2.q[i]) for i in range(0, net.n, max(1, net.n // 5)))
print(f"  reloaded {net2.n:,} neurons in {load_s:.1f}s; "
      f"q identical: {same_q and ok}")
j, s = neighbors(net2.q, X[idx['google.com']], k=3)
print(f"  post-reload google.com -> "
      f"{' | '.join('%-24s %.3f' % (dom2[k], v) for k, v in zip(j, s))}")

print("\n" + "=" * 72)
print("SUMMARY")
print("=" * 72)
print(f"  The net now holds {net2.n:,} widely-used real websites "
      f"({gb:.2f} GB),")
print(f"  persisted to {os.path.basename(OUT)} for reuse.  The remaining")
print(f"  RAM headroom (~{0.6*31.7e9/2048/1e6:.0f}M sites) is capacity-only;")
print(f"  FLOWING that population still needs the O(1)-per-neuron search.")
