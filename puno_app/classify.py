"""Puno Classify - a usable, numpy-only text classifier built on the
self-organizing puno_flow network.

One or more prototype units per class, each with a private home (its
identity) and its own hash-chained ledger; routing is plain nearest-unit.
The whole classifier *is* a FlowEngine population, so you get the
decentralized-net properties for free: local-only dynamics, spacing and
consensus reports, a verifiable audit trail of what each prototype was
seated on, and no central table of "the model".

No ML framework, no scikit-learn: TF-IDF vectorization is implemented on
numpy + the standard library, so the base install (numpy only) runs it.

Usage:
  puno-classify train --data demo --model net.pkl --report
  puno-classify train --data emails.csv --text-col body --label-col label
  puno-classify train --data docs/                 (each subfolder = class)
  puno-classify predict --model net.pkl "pork shoulder braised low and slow"
  puno-classify predict --model net.pkl --interactive
  puno-classify serve --model net.pkl --port 8877
"""

import argparse
import csv
import json
import pickle
import re
import sys
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import numpy as np

from puno_flow.engine import FlowEngine

HTML_PATH = Path(__file__).resolve().parent / "classify.html"

DEFAULT_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "to", "for", "on",
    "in", "at", "by", "with", "from", "as", "is", "are", "was", "were",
    "be", "been", "being", "it", "its", "this", "that", "these", "those",
    "i", "you", "he", "she", "we", "they", "my", "your", "our", "their",
    "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "should", "not", "no", "yes", "so", "very", "just", "get",
    "got", "one", "two", "like", "about", "more", "then", "there",
}

_TOKEN_RE = re.compile(r"[a-z0-9']+")


# ---------------------------------------------------------------------- #
class TfidfVectorizer:
    """Token-count TF-IDF with l2 row normalization, numpy-only."""

    def __init__(self, max_features=2000, min_df=1, max_df=0.85,
                 stopwords=None):
        self.max_features = max_features
        self.min_df = min_df
        self.max_df = max_df
        self.stopwords = DEFAULT_STOPWORDS if stopwords is None else set(stopwords)
        self.vocab = {}
        self.idf = np.zeros(0)
        self._built = False

    def _tokenize(self, text):
        return [t for t in _TOKEN_RE.findall((text or "").lower())
                if t not in self.stopwords]

    def fit(self, docs):
        docs = list(docs)
        counts = []
        df = Counter()
        for doc in docs:
            tokens = self._tokenize(doc)
            c = Counter(tokens)
            counts.append(c)
            df.update(c.keys())
        if not df:
            raise ValueError("no tokens after stopword filtering")
        n = len(docs)

        def keep(term, f):
            if self.min_df > 1 and f < self.min_df:
                return False
            if self.min_df < 1 and f / n < self.min_df:
                return False
            if self.max_df > 1 and f > self.max_df:
                return False
            if self.max_df < 1 and f / n > self.max_df:
                return False
            return True

        terms = [t for t, f in df.items() if keep(t, f)]
        terms.sort(key=lambda t: (-df[t], t))
        if self.max_features and len(terms) > self.max_features:
            terms = terms[:self.max_features]
        self.vocab = {t: i for i, t in enumerate(terms)}
        self.idf = np.array([np.log((1 + n) / (1 + df[t])) + 1.0
                             for t in terms])
        self._built = True
        return self._matrix(counts)

    def transform(self, docs):
        if not self._built:
            raise ValueError("fit() before transform()")
        counts = [Counter(self._tokenize(d)) for d in docs]
        return self._matrix(counts)

    def fit_transform(self, docs):
        return self.fit(docs)

    def _matrix(self, counts):
        X = np.zeros((len(counts), len(self.vocab)))
        for i, c in enumerate(counts):
            for term, f in c.items():
                j = self.vocab.get(term)
                if j is not None:
                    X[i, j] = f * self.idf[j]
        norms = np.linalg.norm(X, axis=1)
        X /= np.maximum(norms[:, None], 1e-9)
        return X


# ---------------------------------------------------------------------- #
def _seeded_medoids(rows, k):
    """Deterministic greedy farthest-from-centroid medoids (no rng)."""
    if len(rows) <= k:
        return list(range(len(rows)))
    centroid = rows.mean(axis=0)
    picked = [int(np.argmax(np.linalg.norm(rows - centroid, axis=1)))]
    for _ in range(k - 1):
        d = np.min(np.linalg.norm(rows[:, None, :] - rows[picked][None, :, :],
                                  axis=-1), axis=1)
        picked.append(int(np.argmax(d)))
    return picked


class PunoClassifier:
    """A self-organizing prototype classifier: a population of units, each
    with a private home, whose nearest unit decides the label."""

    def __init__(self, k=8, mu0=1.0, max_r=2.0, seed=7, prototypes=1,
                 absorb=40, flow=0, max_features=2000):
        self.k = k
        self.mu0 = mu0
        self.max_r = max_r
        self.seed = seed
        self.prototypes = prototypes
        self.absorb = absorb
        self.flow = flow
        self.vec = TfidfVectorizer(max_features=max_features)
        self.engine = FlowEngine(dim=1, k=k, mu0=mu0, max_r=max_r,
                                 use_index=True)
        self.classes = []
        self.unit_class = []
        self.class_centroids = np.zeros((0, 0))
        self.meta = {}

    # ------------------------------------------------------------------ #
    def fit(self, docs, labels):
        docs = list(docs)
        labels = list(labels)
        if len(docs) != len(labels) or len(docs) == 0:
            raise ValueError("fit needs matching, non-empty docs and labels")
        self.classes = sorted({str(l) for l in labels})
        y = np.array([self.classes.index(str(l)) for l in labels])
        X = self.vec.fit_transform(docs)
        dim = X.shape[1]

        self.engine = FlowEngine(dim=dim, k=min(self.k, len(self.classes)),
                                 mu0=self.mu0, max_r=self.max_r,
                                 use_index=True)
        self.class_centroids = np.zeros((len(self.classes), dim))
        self.unit_class = []
        placed = np.zeros((0, dim))

        for c, label in enumerate(self.classes):
            rows = X[y == c]
            centroid = rows.mean(axis=0)
            cn = np.linalg.norm(centroid)
            if cn > 1e-9:
                centroid = centroid / cn
            self.class_centroids[c] = centroid
            if self.prototypes <= 1:
                seeds = [centroid]
            else:
                seeds = [rows[i] for i in _seeded_medoids(rows, self.prototypes)]
            for p in seeds:
                p = np.asarray(p, dtype=float)
                pn = np.linalg.norm(p)
                if pn < 1e-9:
                    p = centroid.copy()
                else:
                    p = p / pn
                if placed.size and np.any(
                        np.linalg.norm(placed - p, axis=1) < 1e-9):
                    continue
                self.engine.add(p)
                placed = np.vstack([placed, p])
                self.unit_class.append(c)

        self.unit_class = np.array(self.unit_class)
        if self.engine.n == 0:
            raise ValueError("no prototype units could be placed")
        if self.absorb:
            self.engine.absorb(self.absorb)
        if self.flow:
            self.engine.settle(self.flow)
            self.engine.absorb(min(self.flow, 50))
        self.meta = dict(
            n_docs=len(docs), n_units=self.engine.n,
            n_classes=len(self.classes), dim=dim,
            vocab_size=len(self.vec.vocab), seed=self.seed,
            prototypes=self.prototypes, flow=self.flow, k=self.k,
            mu0=self.mu0)
        return self

    def predict(self, texts):
        single = isinstance(texts, str)
        docs = [texts] if single else list(texts)
        X = self.vec.transform(docs)
        idx = self.engine.predict(X)
        labels = [self.classes[int(self.unit_class[i])] for i in idx]
        return labels[0] if single else labels

    def predict_with_confidence(self, text):
        X = self.vec.transform([text])
        hits, dist = self.engine.search(X[0], k=min(self.k, self.engine.n))
        scores = Counter()
        for h, d in zip(hits, dist):
            scores[self.classes[int(self.unit_class[h])]] += 1.0 / (d * d + 1e-9)
        total = sum(scores.values()) or 1.0
        out = sorted(((c, s / total) for c, s in scores.items()),
                     key=lambda kv: -kv[1])
        return out

    def baseline_predict(self, docs):
        X = self.vec.transform(docs)
        D = np.linalg.norm(X[:, None, :]
                           - self.class_centroids[None, :, :], axis=-1)
        return np.argmin(D, axis=1)

    def evaluate(self, docs, labels):
        y = np.array([str(l) for l in labels])
        puno_units = self.engine.predict(self.vec.transform(docs))
        puno = np.array([self.classes[int(self.unit_class[i])]
                         for i in puno_units])
        base_units = self.baseline_predict(docs)
        base = np.array([self.classes[int(b)] for b in base_units])
        return (float(np.mean(puno == y)), float(np.mean(base == y)))

    def info(self):
        s = self.engine.status()
        return dict(classes=self.classes, meta=self.meta,
                    spacing=s["spacing"], consensus=s["consensus"],
                    ledger_chains=s["ledger_chains"],
                    ledger_blocks=s["ledger_blocks"],
                    spacing_text=f"{s['spacing']:.4f}",
                    consensus_text=f"{s['consensus']:.3f}")

    def save(self, path):
        payload = dict(version=1, vec=_vec_state(self.vec),
                       engine=_engine_state(self.engine),
                       classes=self.classes, unit_class=self.unit_class,
                       class_centroids=self.class_centroids, meta=self.meta)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(payload, f)
        return str(path)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            payload = pickle.load(f)
        clf = cls()
        clf.vec = _restore_vec(payload["vec"])
        clf.engine = _restore_engine(payload["engine"])
        clf.classes = payload["classes"]
        clf.unit_class = payload["unit_class"]
        clf.class_centroids = payload["class_centroids"]
        clf.meta = payload.get("meta", {})
        clf.k = clf.engine.k
        clf.mu0 = clf.engine.mu0
        clf.max_r = clf.engine.max_r
        return clf


# ---------------------------------------------------------------------- #
def _class_vocab():
    return {
        "weather": ["rain", "sunny", "storm", "cloud", "snow", "forecast",
                    "thunder", "fog", "humid", "breeze", "shower", "frost",
                    "temperature", "sky", "degrees"],
        "sports": ["goal", "match", "pitch", "player", "score", "league",
                   "tournament", "final", "kick", "trophy", "coach", "season",
                   "win", "defense", "stadium"],
        "food": ["recipe", "bake", "sauce", "simmer", "garlic", "dough",
                 "braise", "roast", "sliced", "broth", "pan", "onion",
                 "herbs", "chef", "taste"],
        "tech": ["code", "server", "compile", "kernel", "branch", "binary",
                 "debug", "port", "thread", "commit", "socket", "query",
                 "cache", "stack", "compile"],
    }


def make_demo(seed=42, per_class=60):
    """A small, deterministic labeled text corpus for instant demos/tests."""
    rng = np.random.RandomState(seed)
    fillers = ["the", "with", "from", "into", "after", "before", "under",
               "over", "this", "that", "again", "still"]
    vocab = _class_vocab()
    classes = sorted(vocab)
    docs, labels = [], []
    for cls in classes:
        words = vocab[cls]
        for _ in range(per_class):
            n = int(rng.randint(2, 4))
            pick = rng.choice(len(words), size=n, replace=False)
            parts = [words[i] for i in pick]
            for _ in range(int(rng.randint(0, 2))):
                parts.append(fillers[rng.randint(len(fillers))])
            rng.shuffle(parts)
            docs.append(" ".join(parts))
            labels.append(cls)
    return docs, labels


# ---------------------------------------------------------------------- #
def load_data(source, text_col=None, label_col=None, max_per_class=None):
    """Load (docs, labels) from 'demo', a CSV, or a directory tree."""
    if source == "demo":
        return make_demo()
    path = Path(source)
    if not path.exists():
        raise ValueError(f"data source not found: {source}")
    docs, labels = [], []
    if path.is_dir():
        for sub in sorted(p for p in path.iterdir() if p.is_dir()):
            label = sub.name
            files = [f for f in sorted(sub.iterdir())
                     if f.is_file() and f.suffix.lower() in (".txt", ".md")]
            if max_per_class:
                files = files[:max_per_class]
            for f in files:
                text = f.read_text(encoding="utf-8", errors="ignore")
                if text.strip():
                    docs.append(text)
                    labels.append(label)
        if not docs:
            raise ValueError(f"no text files under {path}")
        return docs, labels
    if path.suffix.lower() == ".csv":
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            raise ValueError("empty CSV")
        tc = text_col or ("text" if "text" in rows[0] else next(iter(rows[0])))
        lc = label_col or "label"
        if tc not in rows[0] or lc not in rows[0]:
            raise ValueError(f"CSV needs columns {tc!r} and {lc!r}; "
                             f"have {sorted(rows[0])}")
        for r in rows:
            text = (r[tc] or "").strip()
            if text:
                docs.append(text)
                labels.append(r[lc])
        if not docs:
            raise ValueError("CSV has no non-empty text rows")
        return docs, labels
    raise ValueError("unsupported source (use demo, a CSV, or a directory)")


# ---------------------------------------------------------------------- #
def _vec_state(v):
    return dict(max_features=v.max_features, min_df=v.min_df, max_df=v.max_df,
                stopwords=sorted(v.stopwords), vocab=v.vocab, idf=v.idf,
                built=v._built)


def _restore_vec(st):
    v = TfidfVectorizer(max_features=st["max_features"], min_df=st["min_df"],
                        max_df=st["max_df"], stopwords=st["stopwords"])
    v.vocab = st["vocab"]
    v.idf = np.asarray(st["idf"])
    v._built = st["built"]
    return v


def _engine_state(e):
    return dict(q=e.q, h=e.h, k=e.k, mu0=e.mu0, A=e.A, dt=e.dt, max_r=e.max_r,
                eps=e.eps, use_index=e.use_index, index_min_n=e.index_min_n,
                chains=e.chains)


def _restore_engine(st):
    dim = st["q"].shape[1] if len(st["q"]) else 1
    e = FlowEngine(dim=dim, k=st["k"], mu0=st["mu0"], A=st["A"], dt=st["dt"],
                   max_r=st["max_r"], eps=st["eps"], use_index=st["use_index"],
                   index_min_n=st["index_min_n"])
    e.q = np.asarray(st["q"])
    e.h = np.asarray(st["h"])
    e.chains = st["chains"]
    return e


# ---------------------------------------------------------------------- #
def _json_default(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    return str(obj)


class ClassifyHandler(BaseHTTPRequestHandler):
    server_version = "PunoClassify/1.0"
    classifier = None

    def log_message(self, fmt, *args):
        sys.stderr.write("puno_classify: %s\n" % (fmt % args))

    def _send(self, code, payload, ctype="application/json"):
        body = json.dumps(payload, default=_json_default).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, msg, code=400):
        self._send(code, {"ok": False, "error": str(msg)})

    def _post_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        return json.loads(raw) if raw else {}

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            html = HTML_PATH.read_text(encoding="utf-8")
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/info":
            self._send(200, {"ok": True, **self.classifier.info()})
        else:
            self._error(f"unknown path {path}", 404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/predict":
            self._error(f"unknown path {path}", 404)
            return
        body = self._post_json()
        text = (body.get("text") or "").strip()
        if not text:
            self._error("empty text")
            return
        try:
            label = self.classifier.predict(text)
            conf = self.classifier.predict_with_confidence(text)
            self._send(200, {"ok": True, "label": label,
                             "confidences": [{"label": c, "confidence": float(v)}
                                             for c, v in conf]})
        except Exception as exc:
            self._error(str(exc))


def make_classify_server(classifier, host="127.0.0.1", port=8877):
    _clf = classifier

    class BoundHandler(ClassifyHandler):
        classifier = _clf

    server = ThreadingHTTPServer((host, port), BoundHandler)
    server.daemon_threads = True
    return server


# ---------------------------------------------------------------------- #
def _train(args):
    docs, labels = load_data(args.data, args.text_col, args.label_col,
                             args.max_per_class)
    n_docs = len(docs)
    idx = list(range(n_docs))
    rng = np.random.RandomState(args.split_seed)
    rng.shuffle(idx)
    n_test = max(1, int(round(n_docs * args.split)))
    test_idx, train_idx = idx[:n_test], idx[n_test:]
    if not train_idx:
        raise ValueError("training split is empty; raise --split or add data")
    clf = PunoClassifier(k=args.k, mu0=args.mu0, seed=args.seed,
                         prototypes=args.prototypes, flow=args.flow,
                         absorb=args.absorb,
                         max_features=args.max_features)
    clf.fit([docs[i] for i in train_idx], [labels[i] for i in train_idx])
    path = clf.save(args.model)
    report = [f"trained on {len(train_idx)} docs ({len(test_idx)} held out)",
              f"saved -> {path}",
              f"classes: {', '.join(clf.classes)}"]
    if args.report:
        acc_p, acc_b = clf.evaluate(
            [docs[i] for i in test_idx], [labels[i] for i in test_idx])
        report.append(f"held-out accuracy: puno={acc_p:.3f} "
                      f"baseline-centroid={acc_b:.3f}")
        info = clf.info()
        report.append(f"units={info['meta']['n_units']} "
                      f"dim={info['meta']['dim']} "
                      f"vocab={info['meta']['vocab_size']} "
                      f"spacing={info['spacing_text']} "
                      f"consensus={info['consensus_text']}")
        report.append(f"ledgers: {info['ledger_chains']} chains / "
                      f"{info['ledger_blocks']} blocks")
    print("\n".join(report))
    return 0


def _predict(args):
    clf = PunoClassifier.load(args.model)
    if args.interactive:
        print("Puno Classify - type text, empty line to quit")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                break
            label = clf.predict(line)
            conf = clf.predict_with_confidence(line)
            top = "  ".join(f"{c}={v:.2f}" for c, v in conf[:3])
            print(f"{label}   [{top}]")
        return 0
    text = " ".join(args.text)
    if not text:
        print("no text to predict", file=sys.stderr)
        return 1
    label = clf.predict(text)
    conf = clf.predict_with_confidence(text)
    print(label)
    for c, v in conf:
        print(f"  {c:<10} {v:.3f}")
    return 0


def _serve(args):
    clf = PunoClassifier.load(args.model)
    if not HTML_PATH.exists():
        print(f"missing UI file: {HTML_PATH}", file=sys.stderr)
        return 1
    server = make_classify_server(clf, args.host, args.port)
    host, port = server.server_address[:2]
    print(f"Puno Classify: http://{host}:{port}")
    print(f"classes: {', '.join(clf.classes)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        server.shutdown()
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="puno-classify",
        description="Puno Classify: a numpy-only text classifier built on "
                    "the self-organizing puno_flow network")
    sub = ap.add_subparsers(dest="cmd", required=True)

    tr = sub.add_parser("train", help="train a model from demo/CSV/directory")
    tr.add_argument("--data", required=True,
                    help="demo | path.csv | path/to/docs/")
    tr.add_argument("--model", required=True)
    tr.add_argument("--text-col", default=None)
    tr.add_argument("--label-col", default=None)
    tr.add_argument("--max-per-class", type=int, default=None)
    tr.add_argument("--split", type=float, default=0.2)
    tr.add_argument("--split-seed", type=int, default=7)
    tr.add_argument("--report", action="store_true")
    tr.add_argument("--k", type=int, default=8)
    tr.add_argument("--mu0", type=float, default=1.0)
    tr.add_argument("--seed", type=int, default=7)
    tr.add_argument("--prototypes", type=int, default=1,
                    help="units seated per class (medoids for >1)")
    tr.add_argument("--flow", type=int, default=0,
                    help="local settle steps after seating (self-organize)")
    tr.add_argument("--absorb", type=int, default=40)
    tr.add_argument("--max-features", type=int, default=2000)
    tr.set_defaults(func=_train)

    pr = sub.add_parser("predict", help="classify text")
    pr.add_argument("--model", required=True)
    pr.add_argument("--interactive", action="store_true")
    pr.add_argument("text", nargs="*")
    pr.set_defaults(func=_predict)

    sv = sub.add_parser("serve", help="run the web UI")
    sv.add_argument("--model", required=True)
    sv.add_argument("--host", default="127.0.0.1")
    sv.add_argument("--port", type=int, default=8877)
    sv.set_defaults(func=_serve)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
