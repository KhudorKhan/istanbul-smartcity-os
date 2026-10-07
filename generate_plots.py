import json
import os
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(__file__)
BACKEND_JSON = os.path.join(ROOT, "benchmark_backend.json")
RAG_JSON = os.path.join(ROOT, "benchmark_rag.json")

REFERENCE_BACKEND = {
    "vus": [50, 200, 500],
    "tps": [72.72, 72.06, 73.84],
    "avg_lat": [494.76, 1480.36, 3943.91],
    "p95_lat": [2507.51, 4063.61, 15803.03],
    "p99_lat": [3200.00, 5200.00, 18500.00]
}

REFERENCE_RAG = {
    "metrics": ["Faithfulness", "Hallucination Rate", "Source Grounding"],
    "baseline": [62.5, 37.5, 25.0],
    "proposed": [100.0, 0.0, 100.0]
}

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.autolayout": True
})


def load_backend_series():
    if not os.path.exists(BACKEND_JSON):
        print(f"No {BACKEND_JSON}; using reference backend series.")
        return REFERENCE_BACKEND, True

    with open(BACKEND_JSON, "r", encoding="utf-8") as f:
        payload = json.load(f)

    results = payload.get("results") or []
    by_vu = {int(row["concurrency"]): row for row in results if "concurrency" in row}
    vus = [50, 200, 500]
    if not all(vu in by_vu for vu in vus):
        print("benchmark_backend.json missing VU 50/200/500; using reference series.")
        return REFERENCE_BACKEND, True

    return {
        "vus": vus,
        "tps": [float(by_vu[vu]["throughput_rps"]) for vu in vus],
        "avg_lat": [float(by_vu[vu]["avg_latency_ms"]) for vu in vus],
        "p95_lat": [float(by_vu[vu]["p95_latency_ms"]) for vu in vus],
        "p99_lat": [float(by_vu[vu].get("p99_latency_ms", 0.0)) for vu in vus]
    }, False


def load_rag_series():
    if not os.path.exists(RAG_JSON):
        print(f"No {RAG_JSON}; using reference RAG series.")
        return REFERENCE_RAG, True

    with open(RAG_JSON, "r", encoding="utf-8") as f:
        payload = json.load(f)

    try:
        proposed = [
            float(payload["faithfulness"]),
            float(payload["hallucination_rate"]),
            float(payload["grounding_score"])
        ]
    except (KeyError, TypeError, ValueError):
        print("benchmark_rag.json incomplete; using reference RAG series.")
        return REFERENCE_RAG, True

    return {
        "metrics": REFERENCE_RAG["metrics"],
        "baseline": REFERENCE_RAG["baseline"],
        "proposed": proposed
    }, False


backend, backend_ref = load_backend_series()
rag, rag_ref = load_rag_series()

fig, ax1 = plt.subplots(figsize=(6.5, 4.2))
color = "#1f77b4"
ax1.set_xlabel("Concurrent Virtual Users (VUs)")
ax1.set_ylabel("Throughput (TPS)", color=color)
line1 = ax1.plot(backend["vus"], backend["tps"], color=color, marker="o", linewidth=2.2, label="Throughput (TPS)")
ax1.tick_params(axis="y", labelcolor=color)
tps_max = max(backend["tps"]) if backend["tps"] else 1.0
tps_min = min(backend["tps"]) if backend["tps"] else 0.0
ax1.set_ylim(max(0.0, tps_min * 0.7), max(tps_max * 1.3, 1.0))
ax1.grid(True, linestyle="--", alpha=0.5)

ax2 = ax1.twinx()
ax2.set_ylabel("Latency (ms)", color="#d62728")
line2 = ax2.plot(backend["vus"], backend["avg_lat"], color="#ff7f0e", marker="s", linestyle="--", linewidth=2, label="Avg Latency (ms)")
line3 = ax2.plot(backend["vus"], backend["p95_lat"], color="#d62728", marker="^", linewidth=2, label="p95 Latency (ms)")
line4 = ax2.plot(backend["vus"], backend["p99_lat"], color="#9467bd", marker="d", linestyle=":", linewidth=2, label="p99 Latency (ms)")
ax2.tick_params(axis="y", labelcolor="#d62728")

lines = line1 + line2 + line3 + line4
labels = [item.get_label() for item in lines]
ax1.legend(lines, labels, loc="upper left", frameon=True)
title_suffix = " (reference)" if backend_ref else ""
plt.title(f"High-Concurrency Stress Testing (Spring Boot Gateway){title_suffix}")
plt.savefig("fig_backend_performance.pdf", format="pdf", dpi=300)
plt.savefig("fig_backend_performance.png", format="png", dpi=300)
plt.close()
print("Saved fig_backend_performance.png / .pdf")

metrics = rag["metrics"]
baseline = rag["baseline"]
proposed = rag["proposed"]
x = np.arange(len(metrics))
width = 0.35

fig, ax = plt.subplots(figsize=(6.5, 4.2))
rects1 = ax.bar(x - width / 2, baseline, width, label="Baseline LLM", color="#7f7f7f", alpha=0.85, edgecolor="black")
rects2 = ax.bar(x + width / 2, proposed, width, label="Proposed RAG Orchestrator", color="#2ca02c", alpha=0.9, edgecolor="black")
ax.set_ylabel("Percentage (%)")
rag_suffix = " (reference)" if rag_ref else ""
ax.set_title(f"Hallucination Suppression & Accuracy Benchmark{rag_suffix}")
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylim(0, 120)
ax.legend(loc="upper right", frameon=True)
ax.grid(True, axis="y", linestyle="--", alpha=0.5)


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f"{height:.1f}%",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=9
        )


autolabel(rects1)
autolabel(rects2)

plt.savefig("fig_rag_evaluation.pdf", format="pdf", dpi=300)
plt.savefig("fig_rag_evaluation.png", format="png", dpi=300)
plt.close()
print("Saved fig_rag_evaluation.png / .pdf")
