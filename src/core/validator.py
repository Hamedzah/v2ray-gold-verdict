import asyncio
import socket
import time
import statistics
from typing import List, Tuple, Optional
from urllib.parse import urlparse

class ConfigValidator:
    def __init__(self):
        self.TCP_TIMEOUT = 8.0
        self.STABILITY_SAMPLES = 2
        self.MAX_JITTER = 500.0
        self.MAX_LATENCY = 3000.0
        self.CONCURRENCY_LIMIT = 100

    async def run_pipeline(self, configs: List[str]) -> List[Tuple[str, float, float]]:
        semaphore = asyncio.Semaphore(self.CONCURRENCY_LIMIT)
        tasks = [self._validate_single(cfg, semaphore) for cfg in configs]
        results = await asyncio.gather(*tasks)
        valid = [r for r in results if r is not None]
        if not valid:
            print("No config passed strict criteria. Trying rescue mode with softer limits...")
            self.MAX_LATENCY = 1500.0
            self.MAX_JITTER = 300.0
            self.TCP_TIMEOUT = 5.0
            tasks = [self._validate_single(cfg, semaphore) for cfg in configs[:500]]
            results = await asyncio.gather(*tasks)
            valid = [r for r in results if r is not None]
        return valid

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
            score = 1000.0 / (avg_lat + 1.0)
            return (cfg, avg_lat, score)

    def _parse_config(self, cfg: str) -> Optional[Tuple[str, int]]:
        try:
            parsed = urlparse(cfg)
            if parsed.scheme not in ('vless', 'trojan', 'ss', 'v2ray', 'vmess'):
                return None
            host = parsed.hostname
            port = parsed.port
            if not host or not port:
                return None
            return (host, port)
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
            await asyncio.sleep(0.3)
        if len(latencies) == 0:
            return float('inf'), float('inf')
        if len(latencies) == 1:
            return latencies[0], 0.0
        avg = statistics.mean(latencies)
        jitter = statistics.stdev(latencies)
        return avg, jitter
