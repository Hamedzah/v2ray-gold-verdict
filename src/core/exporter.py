import base64
from typing import List, Tuple

class ResultsExporter:
    MAX_OUTPUT = 15

    def save(self, configs: List[Tuple[str, float, float]]):
        if not configs:
            print("No valid configs found")
            return
        top = configs[:self.MAX_OUTPUT]
        plain_links = [cfg for cfg, _, _ in top]
        plain_text = "\n".join(plain_links)
        b64_text = base64.b64encode(plain_text.encode()).decode()
        with open("configs.txt", "w") as f:
            f.write(plain_text)
        with open("sub.txt", "w") as f:
            f.write(b64_text)
        print(f"Exported {len(plain_links)} high-quality configs")
