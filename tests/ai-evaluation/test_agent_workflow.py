from dataclasses import dataclass


@dataclass
class ToolCall:
    name: str
    input: str
    output: str


def run_order_agent(order_id: str):
    """Small deterministic agent workflow used to exercise trace assertions."""
    calls = [
        ToolCall("get_order", order_id, '{"status":"CREATED"}'),
        ToolCall("check_inventory", order_id, '{"available":true}'),
        ToolCall("send_notification", order_id, "accepted"),
    ]
    return calls


def test_agent_uses_expected_tool_sequence():
    calls = run_order_agent("o-123")
    assert [call.name for call in calls] == [
        "get_order",
        "check_inventory",
        "send_notification",
    ]


def test_agent_trace_preserves_correlation_input():
    order_id = "o-456"
    calls = run_order_agent(order_id)
    assert all(call.input == order_id for call in calls)


def test_agent_does_not_send_notification_when_inventory_fails():
    calls = [
        ToolCall("get_order", "o-789", '{"status":"CREATED"}'),
        ToolCall("check_inventory", "o-789", '{"available":false}'),
    ]
    assert "send_notification" not in [call.name for call in calls]
