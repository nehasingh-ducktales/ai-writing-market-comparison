from tests.helpers import make_text_block, make_response
from formatter import MarkdownFormatter


class TestMarkdownFormatter:
    def _make_formatter(self, mock_client, markdown_output: str) -> MarkdownFormatter:
        mock_client.messages.create.return_value = make_response(
            "end_turn", [make_text_block(markdown_output)]
        )
        return MarkdownFormatter(mock_client, "claude-sonnet-4-6")

    def test_returns_string(self, mock_client):
        formatter = self._make_formatter(mock_client, "# Title\n## Slide 1\n- bullet")
        assert isinstance(formatter.format("some research", "Tesla"), str)

    def test_output_has_h1(self, mock_client):
        formatter = self._make_formatter(
            mock_client, "# Tesla Competitive Landscape\n## Slide 1\n- bullet"
        )
        result = formatter.format("some research", "Tesla")
        assert "# " in result

    def test_output_has_at_least_one_h2(self, mock_client):
        formatter = self._make_formatter(
            mock_client, "# Tesla\n## Competitor: BYD\n- bullet\n## SWOT\n- S: strength"
        )
        result = formatter.format("some research", "Tesla")
        assert result.count("\n## ") >= 1

    def test_makes_exactly_one_api_call(self, mock_client):
        formatter = self._make_formatter(mock_client, "# Tesla\n## Slide\n- bullet")
        formatter.format("notes", "Tesla")
        assert mock_client.messages.create.call_count == 1

    def test_includes_company_in_user_prompt(self, mock_client):
        formatter = self._make_formatter(mock_client, "# Result\n## Slide\n- bullet")
        formatter.format("some research notes", "Notion")
        messages = mock_client.messages.create.call_args.kwargs["messages"]
        assert "Notion" in messages[0]["content"]
