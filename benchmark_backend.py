import asyncio
import httpx
import json
import os
import time
import statistics

BACKEND_BASE_URL = os.getenv("BENCHMARK_BACKEND_URL", "http://localhost:8080").rstrip("/")
BACKEND_URL = f"{BACKEND_BASE_URL}/api/v1/payments/process"
PAYLOAD = {"userId": 1, "serviceId": 1, "amount": 17.70}
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "benchmark_backend.json")
SCENARIOS = [(50, 500), (200, 1000), (500, 2500)]


def calculate_percentile(data, percentile):
    if not data:
        return 0.0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (percentile / 100.0)
    f = int(k)
    c = f + 1
    if c < len(sorted_data):
        return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])
    return sorted_data[f]


async def send_request(client, latencies, status_codes):
    start = time.perf_counter()
    try:
        resp = await client.post(BACKEND_URL, json=PAYLOAD, timeout=30.0)
        lat = (time.perf_counter() - start) * 1000
        latencies.append(lat)
        status_codes.append(resp.status_code)
    except Exception:
        status_codes.append(500)


async def run_stress_level(concurrency: int, total_requests: int):
    latencies = []
    status_codes = []

    limits = httpx.Limits(max_keepalive_connections=concurrency, max_connections=concurrency * 2)
    async with httpx.AsyncClient(limits=limits) as client:
        start_total = time.perf_counter()
        tasks = []
        for _ in range(total_requests):
            tasks.append(send_request(client, latencies, status_codes))
            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)
        total_time = time.perf_counter() - start_total

    success_count = sum(1 for c in status_codes if c == 200)
    error_rate = ((len(status_codes) - success_count) / len(status_codes)) * 100
    throughput = len(status_codes) / total_time if total_time > 0 else 0.0

    return {
        "concurrency": concurrency,
        "total_requests": total_requests,
        "throughput_rps": round(throughput, 2),
        "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0.0,
        "p95_latency_ms": round(calculate_percentile(latencies, 95), 2),
        "p99_latency_ms": round(calculate_percentile(latencies, 99), 2),
        "error_rate_pct": round(error_rate, 2)
    }


async def main():
    print("=== ISTANBUL SMARTCITY FINANCIAL GATEWAY BENCHMARK ===")
    print(f"Target: {BACKEND_URL}")
    print("| Concurrent VUs | Total Requests | Throughput (TPS) | Avg Latency (ms) | p95 (ms) | p99 (ms) | Error Rate (%) |")
    print("|---|---|---|---|---|---|---|")
    results = []
    for vus, reqs in SCENARIOS:
        res = await run_stress_level(vus, reqs)
        results.append(res)
        print(
            f"| {res['concurrency']} | {res['total_requests']} | {res['throughput_rps']} | "
            f"{res['avg_latency_ms']} | {res['p95_latency_ms']} | {res['p99_latency_ms']} | {res['error_rate_pct']}% |"
        )
        await asyncio.sleep(2)

    payload = {
        "target": BACKEND_URL,
        "scenarios": SCENARIOS,
        "results": results
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
