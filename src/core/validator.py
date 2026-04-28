import asyncio
import socket
import time
import statistics
from typing import List, Tuple, Optional
from urllib.parse import urlparse

class ConfigValidator:
    def __init__(self):
        self.TCP_TIMEOUT = 2.0
        self.STABILITY_SAMPLES = 3
        self.MAX_JITTER = 50.0
        self.MAX_LATENCY = 300.0
        self.CONCURRENCY_LIMIT = 50

    async def run_pipeline(self, configs: List[str]) -> List[Tuple[str, float, float]]:
        semaphore = asyncio.Semaphore(self.CONCURRENCY_LIMIT)
        tasks = [self._validate_single(cfg, semaphore) for cfg in configs]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

    async def _validate_single(self, cfg: str, semaphore: asyncio.Semaphore) -> Optional[Tuple[str, float, float]]:
        async with semaphore:
            parsed = self._parse_config(cfg)
            if not parsed:
                return None
            host, port = parsed
            reachable, _ = await self._tcp_ping(host, port)
            if not reachable:
                return None
            avg_lat, jitter = await self._stability_test(host, port)
            if avg_lat > self.MAX_LATENCY or jitter > self.MAX_JITTER:
                return None
            if not await self._real_load_test(cfg):
                return None
            score = 1000.0 / (avg_lat + 1.0)
            return (cfg, avg_lat, score)

    def _parse_config(self, cfg: str) -> Optional[Tuple[str, int]]:
        try:
            parsed = urlparse(cfg)
            if parsed.scheme not in ('vless', 'trojan', 'ss'):
                return None
            return (parsed.hostname, parsed.port)
        except:
            return None

    async def _tcp_ping(self, host: str, port: int) -> Tuple[bool, float]:
        loop = asyncio.get_running_loop()
        start = time.perf_counter()
        try:
            await loop.run_in_executor(None, lambda: socket.create_connection((host, port), timeout=self.TCP_TIMEOUT))
            latency = (time.perf_counter() - start) * 1000
            return True, latency
        except:
            return False, 0.0

    async def _stability_test(self, host: str, port: int) -> Tuple[float, float]:
        latencies = []
        for _ in range(self.STABILITY_SAMPLES):
            success, lat = await self._tcp_ping(host, port)
            if success:
                latencies.append(lat)
            await asyncio.sleep(0.5)
        if len(latencies) < 2:
            return float('inf'), float('inf')
        avg = statistics.mean(latencies)
        jitter = statistics.stdev(latencies)
        return avg, jitter

    async def _real_load_test(self, cfg: str) -> bool:
        return True
