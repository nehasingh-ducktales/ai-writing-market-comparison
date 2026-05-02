import pytest
from unittest.mock import MagicMock
from tests.helpers import make_text_block, make_tool_use_block, make_response


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def end_turn_response():
    return make_response("end_turn", [make_text_block("Research findings here.")])


@pytest.fixture
def tool_use_then_end_responses():
    return [
        make_response("tool_use", [make_tool_use_block("tool_123")]),
        make_response("end_turn", [make_text_block("Final research results.")]),
    ]
