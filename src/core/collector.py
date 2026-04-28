import asyncio
import aiohttp
import base64
from typing import List

SOURCE_URLS = [
    "https://raw.githubusercontent.com/VP01596/vless-top15/refs/heads/main/All.txt",
    "https://raw.githubusercontent.com/T3stAcc/V2Ray/refs/heads/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/1.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/2.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/3.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/4.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/5.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/6.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/7.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/8.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/9.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/10.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/11.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/12.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/13.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/14.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/15.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/16.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/17.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/18.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/19.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/20.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/21.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/22.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/23.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/24.txt",
    "https://raw.githubusercontent.com/rtwo2/FastNodes/refs/heads/main/sub/everything.txt",
    "https://raw.githubusercontent.com/Veid09/vless-list/refs/heads/main/list.txt",
]

class ConfigCollector:
    async def fetch_all(self) -> List[str]:
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_url(session, url) for url in SOURCE_URLS]
            results = await asyncio.gather(*tasks)
        unique = set()
        for cfg_list in results:
            unique.update(cfg_list)
        print(f"Collected {len(unique)} unique configs")
        return list(unique)

    async def _fetch_url(self, session: aiohttp.ClientSession, url: str) -> List[str]:
        try:
            async with session.get(url, timeout=15) as resp:
                if resp.status != 200:
                    return []
                text = await resp.text()
                if not text.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                    try:
                        text = base64.b64decode(text.strip()).decode('utf-8', errors='ignore')
                    except:
                        pass
                configs = []
                for line in text.splitlines():
                    line = line.strip()
                    if line.startswith(('vless://', 'trojan://', 'ss://', 'hysteria2://', 'tuic://')):
                        if not line.startswith('vmess://'):
                            configs.append(line)
                return configs
        except:
            return []
