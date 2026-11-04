from query_router.agents.registry import build_registry
from query_router.contracts import ROUTING_ONLY, Destination


def test_every_agent_destination_is_registered() -> None:
    names = set(build_registry().names())
    expected = {item.value for item in Destination if item not in ROUTING_ONLY}
    assert names == expected
