from collections.abc import Callable


class IdempotentEventConsumer:
    """Small deterministic consumer model used to test event-processing semantics."""

    def __init__(self, side_effect: Callable[[dict], None]):
        self._processed_event_ids: set[str] = set()
        self.side_effect = side_effect

    def process(self, event: dict) -> bool:
        event_id = event["event_id"]
        if event_id in self._processed_event_ids:
            return False

        self.side_effect(event)
        self._processed_event_ids.add(event_id)
        return True
