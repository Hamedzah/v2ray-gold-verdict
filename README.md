# V2Ray Golden Verdict

Automated subscription validator for VLESS/Trojan/SS configs.  
Runs hourly on GitHub Actions. Outputs only the most stable and low-latency proxies.

## Subscription URL

`https://raw.githubusercontent.com/Hamedzah/v2ray-gold-verdict/config/configs.txt`

## Parameters

- Max output: 15 configs
- Max avg latency: 300 ms
- Max jitter: 50 ms
- TCP timeout: 2 sec
- Stability samples: 3

## Local usage

```bash
pip install -r requirements.txt
python src/main.py
