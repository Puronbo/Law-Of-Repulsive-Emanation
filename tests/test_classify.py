"""Tests for Puno Classify, the numpy-only text classifier on puno_flow."""

import csv
import json
import urllib.request

import pytest

from puno_app.classify import (
    PunoClassifier,
    TfidfVectorizer,
    make_classify_server,
    make_demo,
)


def _fast(**kw):
    kw.setdefault("seed", 3)
    return PunoClassifier(**kw)


def _demo_clf(per_class=40, **kw):
    docs, labels = make_demo(per_class=per_class)
    clf = _fast(**kw)
    clf.fit(docs, labels)
    return clf


class TestVectorizer:
    def test_fit_transform_normalizes(self):
        v = TfidfVectorizer()
        X = v.fit_transform(["the quick brown fox",
                             "the lazy dog barks loudly"])
        assert X.shape == (2, len(v.vocab))
        assert X.shape[1] > 0
        norms = (X @ X.T).diagonal()
        assert all(abs(n - 1.0) < 1e-6 for n in norms)
        assert v._built

    def test_empty_text_vectors_to_zero(self):
        v = TfidfVectorizer()
        v.fit(["alpha beta", "beta gamma"])
        X = v.transform([""])
        assert (X == 0).all()

    def test_stopwords_removed(self):
        v = TfidfVectorizer(max_df=1.0)
        v.fit(["the and or if fox", "fox fox"])
        assert "the" not in v.vocab
        assert "fox" in v.vocab


class TestTrain:
    def test_demo_accuracy_high(self):
        docs, labels = make_demo(per_class=50)
        clf = _demo_clf(per_class=50)
        acc_p, acc_b = clf.evaluate(docs, labels)
        assert acc_p >= 0.9
        assert acc_b >= 0.9

    def test_holds_out_train_test(self):
        docs, labels = make_demo(per_class=30)
        idx = list(range(len(docs)))
        train, test = idx[::2], idx[1::2]
        clf = _demo_clf(per_class=30)
        clf.fit([docs[i] for i in train], [labels[i] for i in train])
        acc, _ = clf.evaluate([docs[i] for i in test],
                              [labels[i] for i in test])
        assert acc >= 0.8

    def test_known_phrase_classified(self):
        clf = _demo_clf()
        assert clf.predict("braised pork shoulder with garlic and herbs") == "food"
        assert clf.predict("the striker scored in the final match") == "sports"
        assert clf.predict("heavy rain and thunder overnight") == "weather"

    def test_multi_prototype_places_units(self):
        clf = _demo_clf(per_class=40, prototypes=3)
        assert clf.engine.n == 4 * 3
        assert len(clf.unit_class) == clf.engine.n
        assert sorted(clf.classes) == ["food", "sports", "tech", "weather"]

    def test_confidence_sums_to_one(self):
        clf = _demo_clf()
        conf = clf.predict_with_confidence("the lazy dog")
        assert abs(sum(c for _, c in conf) - 1.0) < 1e-6
        assert conf[0][1] >= conf[-1][1]

    def test_single_class_survives(self):
        docs, labels = make_demo(per_class=20)
        clf = _demo_clf(per_class=20)
        clf.fit(docs, ["food"] * len(docs))
        assert clf.predict("anything at all") == "food"

    def test_ledgers_verify(self):
        clf = _demo_clf()
        ok, _, _ = clf.engine.verify_ledger()
        assert ok
        assert clf.info()["ledger_chains"] == clf.engine.n


class TestRoundTrip:
    def test_save_load_predicts_same(self, tmp_path):
        clf = _demo_clf(per_class=40)
        texts = ["braised pork with garlic",
                 "the striker scored a goal",
                 "heavy rain and thunder"]
        before = [clf.predict(t) for t in texts]
        path = tmp_path / "model.pkl"
        clf.save(path)
        loaded = PunoClassifier.load(path)
        after = [loaded.predict(t) for t in texts]
        assert after == before
        assert loaded.meta["n_classes"] == 4

    def test_flow_flag_runs(self):
        clf = _demo_clf(per_class=40, flow=50, mu0=4.0)
        assert clf.predict("heavy rain and thunder overnight") == "weather"


class TestDataLoading:
    def test_csv_loading(self, tmp_path):
        rows = [["label", "text"],
                ["food", "braised pork with garlic"],
                ["sports", "striker scored in the final"],
                ["food", "simmer the broth and herbs"]]
        path = tmp_path / "data.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)
        clf = PunoClassifier(seed=3)
        clf.fit(["braised pork with garlic", "simmer the broth and herbs",
                 "striker scored in the final"],
                ["food", "food", "sports"])
        assert clf.predict("roast with herbs") == "food"
        assert clf.predict("score in the final match") == "sports"

    def test_directory_loading(self, tmp_path):
        for label, text in (("alpha", "fizz buzz"), ("beta", "wizz wazz")):
            d = tmp_path / label
            d.mkdir()
            (d / "doc.txt").write_text(text, encoding="utf-8")
        from puno_app.classify import load_data
        docs, labels = load_data(str(tmp_path))
        assert sorted(labels) == ["alpha", "beta"]
        assert len(docs) == 2


class TestServe:
    def _server(self, clf):
        server = make_classify_server(clf, "127.0.0.1", 0)
        port = server.server_address[1]
        import threading
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        return server, port

    def test_endpoints(self, tmp_path):
        clf = _demo_clf(per_class=30)
        server, port = self._server(clf)
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/",
                                        timeout=10) as resp:
                assert resp.status == 200
                html = resp.read().decode("utf-8")
            assert "Puno" in html and "<script>" in html
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/info",
                                        timeout=10) as resp:
                info = json.loads(resp.read())
            assert info["meta"]["n_classes"] == 4
            body = json.dumps({"text": "braised pork with garlic herbs"}).encode()
            req = urllib.request.Request(
                f"http://127.0.0.1:{port}/api/predict", data=body,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                pred = json.loads(resp.read())
            assert pred["ok"] and pred["label"] == "food"
            assert pred["confidences"][0]["label"] == "food"
        finally:
            server.shutdown()

    def test_empty_text_rejected(self):
        clf = _demo_clf(per_class=20)
        server, port = self._server(clf)
        import urllib.error
        try:
            body = json.dumps({"text": "  "}).encode()
            req = urllib.request.Request(
                f"http://127.0.0.1:{port}/api/predict", data=body,
                headers={"Content-Type": "application/json"})
            with pytest.raises(urllib.error.HTTPError) as exc:
                urllib.request.urlopen(req, timeout=10)
            assert exc.value.code == 400
        finally:
            server.shutdown()
