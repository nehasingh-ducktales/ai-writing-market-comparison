from pathlib import Path

MAX_TURNS = 10
PROMPTS_DIR = Path(__file__).parent / "prompts"


class AgentError(Exception):
    pass


class ResearchAgent:
    def __init__(self, client, model: str):
        self.client = client
        self.model = model
        self.system_prompt = (PROMPTS_DIR / "research_system.txt").read_text(encoding="utf-8")
        self._user_template = (PROMPTS_DIR / "research_user.txt").read_text(encoding="utf-8")

    def run(self, company: str, focus: str) -> str:
        user_content = self._user_template.format_map(
            {"company": company, "focus": focus or "general competitive landscape"}
        )
        messages = [{"role": "user", "content": user_content}]

        for _ in range(MAX_TURNS):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=[{"type": "web_search_20250305", "name": "web_search"}],
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                return _extract_text(response.content)

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": _build_tool_results(response.content)})
                continue

            raise AgentError(f"Unexpected stop_reason: {response.stop_reason!r}")

        raise AgentError(f"Research agent exceeded {MAX_TURNS} turns without completing")


def _extract_text(content) -> str:
    return "\n\n".join(
        block.text
        for block in content
        if getattr(block, "type", None) == "text"
    )


def _build_tool_results(content) -> list:
    return [
        {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": "Search executed.",
        }
        for block in content
        if getattr(block, "type", None) == "tool_use"
    ]
