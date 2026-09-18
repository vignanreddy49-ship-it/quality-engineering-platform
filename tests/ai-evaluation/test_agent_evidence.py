from agent_evidence import AgentTrace, validate_trace
from test_agent_workflow import ToolCall

def test_trace_preserves_correlation_and_tool_order():
    calls = (
        ToolCall("get_order","o-123",'{"status":"CREATED"}'),
        ToolCall("check_inventory","o-123",'{"available":true}'),
        ToolCall("send_notification","o-123","accepted"),
    )
    validate_trace(AgentTrace("order-o-123", calls, "completed"))

def test_trace_rejects_secret_output():
    calls = (ToolCall("get_order","o-123","secret=token"),)
    try:
        validate_trace(AgentTrace("order-o-123", calls, "failed"))
    except AssertionError:
        return
    raise AssertionError("secret output must fail evidence validation")
