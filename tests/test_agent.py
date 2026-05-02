import pytest
from tests.helpers import make_response, make_tool_use_block
from agent import ResearchAgent, AgentError, _extract_text, _build_tool_results
from tests.helpers import make_text_block, make_tool_use_block


class TestExtractText:
    def test_extracts_text_from_text_blocks(self):
        content = [make_text_block("Hello"), make_text_block("World")]
        assert _extract_text(content) == "Hello\n\nWorld"

    def test_skips_non_text_blocks(self):
        content = [make_tool_use_block("id1"), make_text_block("Found it")]
        assert _extract_text(content) == "Found it"

    def test_empty_content_returns_empty_string(self):
        assert _extract_text([]) == ""


class TestBuildToolResults:
    def test_builds_result_for_each_tool_use_block(self):
        content = [make_tool_use_block("abc123"), make_tool_use_block("def456")]
        results = _build_tool_results(content)
        assert len(results) == 2
        assert results[0]["type"] == "tool_result"
        assert results[0]["tool_use_id"] == "abc123"
        assert results[1]["tool_use_id"] == "def456"

    def test_ignores_non_tool_use_blocks(self):
        content = [make_text_block("text"), make_tool_use_block("id1")]
        results = _build_tool_results(content)
        assert len(results) == 1

    def test_empty_content_returns_empty_list(self):
        assert _build_tool_results([]) == []


class TestResearchAgent:
    def test_returns_text_on_end_turn(self, mock_client, end_turn_response):
        mock_client.messages.create.return_value = end_turn_response
        agent = ResearchAgent(mock_client, "claude-sonnet-4-6")
        result = agent.run("Tesla", "EV market")
        assert "Research findings here." in result

    def test_handles_tool_use_then_end_turn(self, mock_client, tool_use_then_end_responses):
        mock_client.messages.create.side_effect = tool_use_then_end_responses
        agent = ResearchAgent(mock_client, "claude-sonnet-4-6")
        result = agent.run("Tesla", "")
        assert "Final research results." in result
        assert mock_client.messages.create.call_count == 2

    def test_raises_on_max_turns_exceeded(self, mock_client):
        mock_client.messages.create.return_value = make_response(
            "tool_use", [make_tool_use_block("id1")]
        )
        agent = ResearchAgent(mock_client, "claude-sonnet-4-6")
        with pytest.raises(AgentError, match="exceeded"):
            agent.run("Tesla", "")

    def test_raises_on_unexpected_stop_reason(self, mock_client):
        mock_client.messages.create.return_value = make_response("max_tokens", [])
        agent = ResearchAgent(mock_client, "claude-sonnet-4-6")
        with pytest.raises(AgentError, match="Unexpected"):
            agent.run("Tesla", "")

    def test_sends_tool_results_back_in_next_turn(self, mock_client, tool_use_then_end_responses):
        mock_client.messages.create.side_effect = tool_use_then_end_responses
        agent = ResearchAgent(mock_client, "claude-sonnet-4-6")
        agent.run("Tesla", "")
        second_call_kwargs = mock_client.messages.create.call_args_list[1].kwargs
        messages = second_call_kwargs["messages"]
        tool_result_msgs = [
            m for m in messages
            if m["role"] == "user"
            and isinstance(m.get("content"), list)
            and m["content"]
            and isinstance(m["content"][0], dict)
            and m["content"][0].get("type") == "tool_result"
        ]
        assert len(tool_result_msgs) == 1
        assert tool_result_msgs[0]["content"][0]["tool_use_id"] == "tool_123"
