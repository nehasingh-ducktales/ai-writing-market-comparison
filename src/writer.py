import re
from datetime import datetime
from pathlib import Path


class OutputWriter:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, content: str, company: str) -> Path:
        slug = re.sub(r"[^\w]+", "_", company.lower()).strip("_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"{slug}_{timestamp}.md"
        path.write_text(content, encoding="utf-8")
        return path
