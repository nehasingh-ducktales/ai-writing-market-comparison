from unittest.mock import MagicMock


def make_text_block(text: str):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return block


def make_tool_use_block(tool_id: str, name: str = "web_search"):
    block = MagicMock()
    block.type = "tool_use"
    block.id = tool_id
    block.name = name
    block.input = {"query": "test query"}
    return block


def make_response(stop_reason: str, content):
    response = MagicMock()
    response.stop_reason = stop_reason
    response.content = content
    return response
