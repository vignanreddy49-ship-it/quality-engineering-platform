"""Evidence assertions for traceable agent workflows."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class AgentTrace:
    correlation_id: str
    calls: tuple
    outcome: str

def validate_trace(trace: AgentTrace):
    assert re.fullmatch(r"[A-Za-z0-9_-]{3,64}", trace.correlation_id)
    assert trace.calls
    for call in trace.calls:
        assert call.input
        assert "password=" not in call.input.lower()
        assert "api_key=" not in call.input.lower()
        assert "secret=" not in call.output.lower()
    names = [c.name for c in trace.calls]
    if "send_notification" in names:
        assert names.index("check_inventory") < names.index("send_notification")
