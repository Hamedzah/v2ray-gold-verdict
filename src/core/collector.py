import asyncio
import aiohttp
import base64
from typing import List

SOURCE_URLS = [
"https://raw.githubusercontent.com/mahdibland/V2RayAggregator/refs/heads/master/sub/sub_merge.txt", 
    "https://raw.githubusercontent.com/VP01596/vless-top15/refs/heads/main/All.txt",
    "https://raw.githubusercontent.com/T3stAcc/V2Ray/refs/heads/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/miladtahanian/Config-Collector/main/mixed_iran.txt",
"https://raw.githubusercontent.com/Farid-Karimi/Config-Collector/main/mixed_iran.txt",
"https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/README.md",
"https://raw.githubusercontent.com/SoroushImanian/BlackKnight/main/subscribes.txt",
    "https://raw.githubusercontent.com/VoroninaYanina/free-nodes/main/All_Configs_Sub.txt",
"https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
"https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_base64.txt",
"https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
"https://raw.githubusercontent.com/freefq/free/master/v2ray",
"https://raw.githubusercontent.com/PojavLauncherTeam/v2ray/main/configs.txt",
"https://raw.githubusercontent.com/Mahanzaman/V2Ray-Configs/main/All_Configs_Sub.txt",
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
