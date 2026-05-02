# CLAUDE.md

## Project Goal
Python CLI that researches company competitors via Claude's web_search tool
and outputs Gamma-ready markdown presentation decks.

## Architecture
```
src/main.py       CLI entry — parses args, wires agent -> formatter -> writer
src/agent.py      ResearchAgent — web_search agentic loop (web_search_20250305)
src/formatter.py  MarkdownFormatter — raw notes -> Gamma markdown (single call)
src/writer.py     OutputWriter — saves to outputs/{company}_{timestamp}.md
src/prompts/      Prompt templates — edit these to tune output quality
tests/            Offline pytest suite — all API calls mocked
outputs/          Generated decks — gitignored, import into Gamma manually
```

## Running the tool
```bash
cp .env.example .env        # fill in ANTHROPIC_API_KEY
pip install -r requirements.txt
python src/main.py --company "Tesla" --focus "EV market"
python src/main.py --company "OpenAI" --focus "LLM APIs" --model claude-opus-4-7
```

## Running tests (offline — no API key needed)
```bash
pytest tests/
```

## Linting
```bash
ruff check src tests
ruff format src tests
```

## Environment variables
- `ANTHROPIC_API_KEY` — required, get from console.anthropic.com
- `DEFAULT_MODEL` — optional, defaults to `claude-sonnet-4-6`

## Models
- Standard: `claude-sonnet-4-6` (fast, good web search quality)
- Premium: `claude-opus-4-7` (deeper research, pass `--model claude-opus-4-7`)

## Prompt editing conventions
Variables use `{curly_brace}` syntax, loaded via `str.format_map()`.

| File | What it controls |
|------|-----------------|
| `research_system.txt` | What the agent searches for and how it structures raw notes |
| `research_user.txt` | The specific request per run — `{company}` and `{focus}` |
| `format_system.txt` | Gamma slide structure and bullet density — most impactful to edit |
| `format_user.txt` | How research notes are handed to the formatter |

## Adding new slide sections
Edit `src/prompts/format_system.txt` — add a line to the Required slide structure list.
Example: `7. ## Funding & Investors  (key investors, total raised, valuation)`

## Web search tool
Uses `web_search_20250305` (Claude's server-side built-in tool — no external API needed).
The agentic loop in `agent.py` handles `tool_use` / `end_turn` automatically.
Typical research: 3–5 turns. Safety limit: 10 turns.

## Output files
Saved to `outputs/{company_slug}_{YYYYMMDD_HHMMSS}.md` — gitignored.
Import into Gamma: New Deck → Import → Paste text.
