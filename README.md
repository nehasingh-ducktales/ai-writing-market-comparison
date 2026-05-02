# FirstGammaClaude

Research competitors using Claude AI and generate a Gamma presentation deck automatically.

## How it works

1. Provide a company name and optional focus area
2. Claude searches the web and compiles competitive intelligence
3. Findings are formatted as Gamma-ready markdown (each `##` heading = one slide)
4. Import the output file into [Gamma](https://gamma.app) — slides auto-generate

## Quickstart

```bash
# Clone and install
git clone <repo-url>
cd FirstGammaClaude
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY from console.anthropic.com

# Run
python src/main.py --company "Tesla" --focus "EV market"
```

Output is saved to `outputs/tesla_YYYYMMDD_HHMMSS.md`.

## CLI Options

```
python src/main.py --company "Company Name" [--focus "topic"] [--model MODEL_ID]

  --company   Required. The company to research competitors for.
  --focus     Optional. Narrows the research (e.g. "pricing strategy", "enterprise").
  --model     Optional. Default: claude-sonnet-4-6
              Use claude-opus-4-7 for deeper research.
```

## Importing into Gamma

1. Open [gamma.app](https://gamma.app) → click **New** → **Import**
2. Select **Paste in text**
3. Open the `.md` file from `outputs/`, select all, paste
4. Click **Continue** and choose a theme

## Architecture

```
src/main.py       CLI entry point
src/agent.py      ResearchAgent — Claude web_search agentic loop
src/formatter.py  MarkdownFormatter — converts notes to Gamma slides
src/writer.py     OutputWriter — saves to outputs/
src/prompts/      Prompt templates (edit to tune output quality)
tests/            Offline test suite (no API key needed)
outputs/          Generated decks — gitignored
```

## Tuning Output Quality

Edit prompt files in `src/prompts/` — no code changes needed.
See [CLAUDE.md](CLAUDE.md) for what each file controls.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
