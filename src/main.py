import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
import anthropic

from agent import ResearchAgent
from formatter import MarkdownFormatter
from writer import OutputWriter

DEFAULT_MODEL = "claude-sonnet-4-6"


def main():
    load_dotenv()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: ANTHROPIC_API_KEY not set. Copy .env.example to .env and fill it in.")

    parser = argparse.ArgumentParser(
        description="Research competitors and generate a Gamma presentation deck."
    )
    parser.add_argument("--company", required=True, help="Company to research (e.g. 'Tesla')")
    parser.add_argument("--focus", default="", help="Optional focus area (e.g. 'EV market')")
    parser.add_argument(
        "--model",
        default=os.environ.get("DEFAULT_MODEL", DEFAULT_MODEL),
        help="Claude model ID",
    )
    args = parser.parse_args()

    client = anthropic.Anthropic(api_key=api_key)

    print(f"Researching competitors for: {args.company}")
    notes = ResearchAgent(client, args.model).run(args.company, args.focus)

    print("Formatting into Gamma deck...")
    markdown = MarkdownFormatter(client, args.model).format(notes, args.company)

    output_path = OutputWriter(Path(__file__).parent.parent / "outputs").save(markdown, args.company)
    print(f"Deck saved to: {output_path}")
    print("Import into Gamma: New Deck -> Import -> Paste text")


if __name__ == "__main__":
    main()
