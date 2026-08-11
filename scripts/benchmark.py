import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.engine import CXEngine

engine = CXEngine(ROOT / "data" / "kb.json")
evals = json.loads((ROOT / "data" / "eval.json").read_text(encoding="utf-8"))


def rank(scores):
    return np.argsort(-scores)


def evaluate(mode: str):
    recalls = {1: 0, 3: 0}
    rr = []
    for row in evals:
        ws, cs, hs = engine.retriever.scores(row["q"])
        scores = {"word": ws, "char": cs, "hybrid": hs}[mode]
        order = rank(scores)
        ids = [engine.docs[i].id for i in order]
        pos = ids.index(row["gold"]) + 1
        recalls[1] += pos <= 1
        recalls[3] += pos <= 3
        rr.append(1 / pos)
    n = len(evals)
    return {
        "Recall@1": recalls[1] / n,
        "Recall@3": recalls[3] / n,
        "MRR": float(np.mean(rr)),
    }


if __name__ == "__main__":
    print("Arabic CX Retrieval Benchmark (synthetic KB/eval set)\n")
    for mode in ["word", "char", "hybrid"]:
        m = evaluate(mode)
        print(f"{mode:7s}  R@1={m['Recall@1']:.3f}  R@3={m['Recall@3']:.3f}  MRR={m['MRR']:.3f}")
