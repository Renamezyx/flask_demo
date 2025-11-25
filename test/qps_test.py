import asyncio
import aiohttp
import time
import statistics

URL = "http://120.79.202.59/api/io"

CONCURRENCY = 100  # 并发数
REQUESTS = 1000 # 总请求数

success = 0
fail = 0
latencies = []   # 记录每个请求耗时（毫秒）


async def worker(session, queue):
    global success, fail, latencies
    while True:
        try:
            _ = queue.get_nowait()
        except asyncio.QueueEmpty:
            return

        start = time.time()
        try:
            async with session.get(URL, timeout=5) as resp:
                cost = (time.time() - start) * 1000   # ms
                latencies.append(cost)

                if resp.status == 200:
                    success += 1
                else:
                    fail += 1
        except:
            fail += 1


async def run_test():
    queue = asyncio.Queue()

    # 放入任务
    for i in range(REQUESTS):
        queue.put_nowait(i)

    conn = aiohttp.TCPConnector(limit=CONCURRENCY)
    async with aiohttp.ClientSession(connector=conn) as session:
        start = time.time()

        tasks = [asyncio.create_task(worker(session, queue))
                 for _ in range(CONCURRENCY)]

        await asyncio.gather(*tasks)

    duration = time.time() - start

    # === 计算 P99 ===
    lat_sorted = sorted(latencies)
    def percentile(p):
        k = int(len(lat_sorted) * p)
        return lat_sorted[min(k, len(lat_sorted)-1)]

    print(f"总请求数: {REQUESTS}")
    print(f"并发数: {CONCURRENCY}")
    print(f"成功: {success}, 失败: {fail}, 成功率: {success/REQUESTS:.2f}")
    print(f"总耗时: {duration:.2f}s")
    print(f"QPS: {REQUESTS / duration:.2f}")

    if latencies:
        print("\n==== 耗时统计 (毫秒) ====")
        print(f"P50: {percentile(0.50):.2f} ms")
        print(f"P90: {percentile(0.90):.2f} ms")
        print(f"P95: {percentile(0.95):.2f} ms")
        print(f"P99: {percentile(0.99):.2f} ms")
        print(f"平均: {statistics.mean(latencies):.2f} ms")


if __name__ == "__main__":
    asyncio.run(run_test())
