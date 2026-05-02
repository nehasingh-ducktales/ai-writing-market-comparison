# Contributing to FirstGammaClaude

## Local Setup

```bash
git clone <repo-url>
cd FirstGammaClaude
cp .env.example .env          # add your ANTHROPIC_API_KEY
pip install -r requirements.txt
pytest tests/                 # all tests should pass (no API key needed)
ruff check src tests          # should report zero errors
```

## Branch Strategy

`main` is protected — no direct pushes. All changes go through pull requests.

**Branch naming** — prefix + kebab-case:
```
feature/add-batch-company-mode
fix/agent-loop-max-turns-edge-case
docs/update-readme-gamma-steps
chore/bump-anthropic-sdk
test/add-formatter-edge-cases
```

```bash
git checkout -b feature/your-feature-name
```

## Commit Style

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add --output-format flag for JSON export
fix: handle empty focus argument in research agent
docs: add Gamma import steps to README
chore: bump anthropic to 0.98.0
test: add test for writer filename sanitization
```

Rules: subject under 72 chars, present tense, no trailing period.

## Pull Request Process

1. Ensure CI passes: `ruff check src tests` and `pytest tests/`
2. PR title follows Conventional Commits style
3. PR description explains **what** changed and **why**
4. At least one team member review before merging
5. Use **squash merge** to keep `main` history linear

**PR description template:**
```
## What
Brief description of the change.

## Why
The motivation or problem being solved.

## How to test
Steps to verify the change works end-to-end.
```

## Important Rules

- **Never commit `.env`** — it contains your API key. `.gitignore` enforces this.
- **Never commit from `outputs/`** — generated decks may contain proprietary research.
- **No direct pushes to `main`** — always use a PR.

## Editing Prompts

The files in `src/prompts/` are the primary way to tune output quality.
After editing, run an end-to-end test and check the output in Gamma:

```bash
python src/main.py --company "Notion" --focus "note-taking"
# then open outputs/*.md and import into gamma.app
```
