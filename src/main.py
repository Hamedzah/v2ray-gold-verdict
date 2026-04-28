import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from core.collector import ConfigCollector
from core.validator import ConfigValidator
from core.exporter import ResultsExporter

async def main():
    print("Starting V2Ray Golden Verdict System")
    collector = ConfigCollector()
    validator = ConfigValidator()
    exporter = ResultsExporter()

    configs = await collector.fetch_all()
    if not configs:
        print("No configs found")
        return

    validated = await validator.run_pipeline(configs)
    exporter.save(validated)
    print("Audit completed")

if __name__ == "__main__":
    asyncio.run(main())
