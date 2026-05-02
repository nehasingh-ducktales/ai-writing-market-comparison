from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"


class MarkdownFormatter:
    def __init__(self, client, model: str):
        self.client = client
        self.model = model
        self.system_prompt = (PROMPTS_DIR / "format_system.txt").read_text(encoding="utf-8")
        self._user_template = (PROMPTS_DIR / "format_user.txt").read_text(encoding="utf-8")

    def format(self, research_notes: str, company: str) -> str:
        user_content = self._user_template.format_map(
            {"research_notes": research_notes, "company": company}
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        return response.content[0].text
