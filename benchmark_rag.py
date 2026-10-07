import httpx
import json
import os
import time

EVAL_DATASET = [
    {"q": "Metrobüs ve otobüs tek geçiş ücreti ne kadar?", "expected_entity": "17.70", "topic": "transit"},
    {"q": "Öğrenci İstanbulkart bilet fiyatı kaç TL?", "expected_entity": "8.85", "topic": "transit"},
    {"q": "Kaçak geçiş ve usulsüz kart kullanım cezası ne kadar?", "expected_entity": "500.00", "topic": "transit"},
    {"q": "İSKİ su faturası 15 metreküpe kadar birim fiyatı nedir?", "expected_entity": "25.50", "topic": "utility"},
    {"q": "Su faturaları ayın kaçına kadar ödenmelidir?", "expected_entity": "20", "topic": "utility"},
    {"q": "İSPARK A Bölgesi ilk 1 saat otopark ücreti kaç TL?", "expected_entity": "40.00", "topic": "parking"},
    {"q": "İSPARK 1 saatten sonraki her ek saat ücreti nedir?", "expected_entity": "20.00", "topic": "parking"},
    {"q": "İSPARK tam gün otopark abonman ücreti ne kadar?", "expected_entity": "150.00", "topic": "parking"}
]

AI_BASE_URL = os.getenv("BENCHMARK_AI_URL", "http://localhost:8001").rstrip("/")
AI_SERVICE_URL = f"{AI_BASE_URL}/api/v1/ai/orchestrate"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "benchmark_rag.json")


def evaluate_rag():
    correct_count = 0
    grounded_count = 0
    total = len(EVAL_DATASET)
    cases = []

    print("=== ISTANBUL SMARTCITY RAG FAITHFULNESS BENCHMARK ===")
    print(f"Target: {AI_SERVICE_URL}")

    with httpx.Client(timeout=60.0) as client:
        for idx, item in enumerate(EVAL_DATASET, 1):
            case = {
                "question": item["q"],
                "expected_entity": item["expected_entity"],
                "ok": False,
                "grounded": False,
                "latency_s": None,
                "source": ""
            }
            try:
                start_t = time.perf_counter()
                resp = client.post(AI_SERVICE_URL, json={"message": item["q"], "language": "tr"})
                latency_s = round(time.perf_counter() - start_t, 2)
                case["latency_s"] = latency_s

                if resp.status_code == 200:
                    data = resp.json()
                    answer_text = data.get("message", "").replace(",", ".")
                    source = data.get("grounded_source", "")
                    action_str = str(data.get("action", "")).replace(",", ".")

                    entity = item["expected_entity"]
                    is_factually_correct = (entity in answer_text) or (entity in action_str)
                    is_grounded = bool(source and source != "None")

                    case["ok"] = is_factually_correct
                    case["grounded"] = is_grounded
                    case["source"] = source

                    if is_factually_correct:
                        correct_count += 1
                    if is_grounded:
                        grounded_count += 1

                    status_icon = "OK" if is_factually_correct else "MISS"
                    print(f"[{idx}/{total}] ({latency_s}s) {status_icon} | {item['q'][:35]}... | {source}")
                else:
                    print(f"[{idx}/{total}] HTTP {resp.status_code} | {item['q'][:35]}...")
            except Exception as e:
                print(f"[{idx}/{total}] request failed: {e}")
            cases.append(case)

    accuracy = (correct_count / total) * 100 if total else 0.0
    hallucination_rate = 100 - accuracy
    grounding_score = (grounded_count / total) * 100 if total else 0.0

    payload = {
        "target": AI_SERVICE_URL,
        "total": total,
        "correct_count": correct_count,
        "grounded_count": grounded_count,
        "faithfulness": round(accuracy, 1),
        "hallucination_rate": round(hallucination_rate, 1),
        "grounding_score": round(grounding_score, 1),
        "cases": cases
    }

    print("\n=== METRICS ===")
    print("| Metric | Value |")
    print("|---|---|")
    print(f"| Total scenarios | {total} |")
    print(f"| Correct entity matches | {correct_count} |")
    print(f"| Faithfulness | {accuracy:.1f}% |")
    print(f"| Hallucination Rate | {hallucination_rate:.1f}% |")
    print(f"| Source Grounding Score | {grounding_score:.1f}% |")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    evaluate_rag()
