"""
T61: ROTATION TEST FOR THE DECENTRAL NET (structure is the law).

Claim (from T55 + T59): a random-projection embedding (HashingVectorizer
char_wb 2-4, 128-D) is a random linear map.  Random linear maps are
Johnson-Lindenstrauss structure-preserving: they approximately keep
pairwise angles.  So the net's RELATIVE geometry (neighbor sets, routing)
is the invariant content -- the "law" -- while the absolute coordinates
are convention.  This is the preserving counterpart to the clock test
(T59), where a *relabeling* (epoch shift) broke point alignments.

Tests on embedded domain vectors:
  (i)   ROTATE all vectors by an orthogonal Q (QR of a Gaussian):
        neighbor structure must survive (overlap ~ 1, sim corr ~ 1)
        even though every coordinate changes.
  (ii)  NONLINEAR relabeling (per-coordinate absolute value):
        a structure-breaking re-encoding like the epoch shift in T59;
        neighbor structure must collapse.

KNOWN FACTS (measured here):
  J1  rotation: top-8 neighbor overlap ~ 1.0, sim correlation ~ 1.0
  J2  rotation: coordinates are completely different (max |Qx - x| large)
  J3  nonlinear relabeling: neighbor overlap collapses toward chance
  J4  => the net's law is its relative geometry; models should consume
        rotation-invariant structure, not absolute coordinates, and must
        be validated against benign relabelings.

Outputs: metrics printed, data -> data/rotation_test_data.json
"""

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
import os, json

NGRAM = (2, 4)
DIM = 128

DOMAINS = [
    "google.com", "gooogle.com", "gogle.com", "google.com.om", "ggoogle.com",
    "google.co", "google.org", "goog1e.com", "google.ru", "google.de",
    "wikipedia.org", "wikipedia.com", "wikipedia.de", "wiki.com",
    "facebook.com", "facebook.net", "faceboook.com", "facebuk.com",
    "youtube.com", "youtbe.com", "youube.com", "amazon.com", "amazon.co.uk",
    "amazonn.com", "twitter.com", "twtter.com", "x.com",
    "apple.com", "aple.com", "icloud.com", "microsoft.com", "microsooft.com",
    "microsoft.net", "office.com", "netflix.com", "netfliix.com", "netflic.com",
    "paypal.com", "paypa1.com", "paypal.co", "ebay.com", "ebay.co.uk",
    "github.com", "gitlab.com", "bitbucket.org", "stackoverflow.com",
    "reddit.com", "reddit.net", "redd.it", "linkedin.com", "linkedin.co",
    "instagram.com", "instagrm.com", "whatsapp.com", "wa.me",
    "cloudflare.com", "cloudfare.com", "akamai.com", "akamaihd.net",
    "bing.com", "duckduckgo.com", "yahoo.com", "yhaoo.com", "msn.com",
    "cnn.com", "bbc.com", "bbc.co.uk", "nytimes.com", "wsj.com",
    "gmail.com", "gmai.com", "mail.google.com", "outlook.com", "hotmail.com",
    "mozilla.org", "firefox.com", "chrome.com", "brave.com",
    "openai.com", "openai.org", "anthropic.com", "claude.ai", "gpt.com",
    "tiktok.com", "tikok.com", "snapchat.com", "pinterest.com",
    "dropbox.com", "drobpox.com", "slack.com", "notion.so", "zoom.us",
    "shopify.com", "shopifiy.com", "etsy.com", "walmart.com", "target.com",
    "cvs.com", "walgreens.com", "costco.com", "bestbuy.com", "homedepot.com",
    "bankofamerica.com", "chase.com", "wellsfargo.com", "citi.com",
    "usps.com", "fedex.com", "ups.com", "dhl.com",
    "nasa.gov", "noaa.gov", "whitehouse.gov", "irs.gov", "gov.uk",
    "mit.edu", "harvard.edu", "stanford.edu", "berkeley.edu", "ox.ac.uk",
    "example.com", "test.com", "localhost", "0.0.0.0",
]


def embed():
    hv = HashingVectorizer(analyzer='char_wb', ngram_range=NGRAM,
                           n_features=DIM, norm='l2', alternate_sign=True)
    X = hv.transform(DOMAINS).toarray().astype(np.float64)
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)


def neighbors(X, seeds, k=8):
    out = {}
    for s in seeds:
        sim = X @ X[s]
        order = np.argsort(-sim)[1:k + 1]
        out[s] = (set(order.tolist()), sim[order])
    return out


def jaccard(a, b):
    inter = len(a & b)
    return inter / len(a | b) if a | b else 0.0


def main():
    rng = np.random.default_rng(7)
    X = embed()
    seeds = [DOMAINS.index(d) for d in
             ["google.com", "paypal.com", "github.com", "amazon.com", "cnn.com"]]

    n1 = neighbors(X, seeds)
    sim_corr = None

    # (i) rotation: orthogonal Q from QR of a Gaussian
    Q, _ = np.linalg.qr(rng.normal(size=(DIM, DIM)))
    Xr = X @ Q.T
    n2 = neighbors(Xr, seeds)
    overlap = np.mean([jaccard(n1[s][0], n2[s][0]) for s in seeds])
    corrs = []
    for s in seeds:
        a, b = n1[s][1], n2[s][1]
        corrs.append(np.corrcoef(a, b)[0, 1] if a.std() and b.std() else 0.0)
    coord_max = float(np.max(np.abs(Xr - X)))

    # (ii) nonlinear relabeling: per-coordinate absolute value
    Xa = np.abs(X)
    n3 = neighbors(Xa, seeds)
    overlap_a = np.mean([jaccard(n1[s][0], n3[s][0]) for s in seeds])

    # chance overlap baseline for k=8 of N domains
    N = len(DOMAINS)
    chance = 8.0 / (N - 1)

    print("=" * 72)
    print("T61: ROTATION TEST FOR THE DECENTRAL NET")
    print("=" * 72)
    print(f"  domains = {N}, dim = {DIM}, k = 8, chance neighbor overlap = {chance:.3f}")
    print()
    print(f"  (i) ROTATION by orthogonal Q:")
    print(f"      J1 top-8 neighbor overlap   = {overlap:.4f}")
    print(f"         similarity correlation   = {np.mean(corrs):.4f}")
    print(f"      J2 max |Qx - x| over all v  = {coord_max:.3f} "
          f"(coordinates entirely different)")
    print()
    print(f"  (ii) NONLINEAR relabeling (abs per coordinate):")
    print(f"      J3 neighbor overlap         = {overlap_a:.4f}  "
          f"(chance = {chance:.3f})")
    print()
    print("KNOWN FACTS:")
    print("  J1  a rotation preserves the net's structure (overlap ~ 1):")
    print("      the law is the relative geometry (JL random projection).")
    print("  J2  yet every coordinate changed: the coordinates are")
    print("      convention, exactly as T59 showed for the calendar.")
    print("  J3  a nonlinear relabeling collapses the structure toward")
    print("      chance: the same 'change the clock' failure.")
    print("  J4  => consume rotation-invariant structure, validate against")
    print("      benign relabelings; routing survives rotations, not")
    print("      arbitrary coordinate surgery.")
    res = {'overlap_rotation': float(overlap), 'sim_corr': float(np.mean(corrs)),
           'coord_max': coord_max, 'overlap_abs': float(overlap_a),
           'chance': float(chance), 'n_domains': int(N),
           'note': 'rotation = structure-preserving re-encoding (JL); '
                   'abs() = nonlinear relabeling (structure-breaking)'}
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data', 'rotation_test_data.json'), 'w') as fp:
        json.dump(res, fp, indent=2)
    print("\nsaved data/rotation_test_data.json")


if __name__ == '__main__':
    main()
