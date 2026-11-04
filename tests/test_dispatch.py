import asyncio

import pytest

from query_router.agents.registry import AgentRegistry, build_registry
from query_router.contracts import Destination, RouteDecision
from query_router.dispatch import dispatch
from query_router.routing.replies import NOT_AVAILABLE_REPLY


def _decision(destination: Destination, **extra: object) -> RouteDecision:
    payload: dict[str, object] = {
        "destination": destination,
        "intent": "demo intent",
        "confidence": 0.9,
    }
    payload.update(extra)
    return RouteDecision.model_validate(payload)


def test_github_route_returns_the_stub_reply() -> None:
    reply = asyncio.run(
        dispatch(_decision(Destination.GITHUB), "list my pull requests", build_registry())
    )
    assert reply == "You have reached your GitHub agent"


def test_linear_route_returns_the_stub_reply() -> None:
    reply = asyncio.run(
        dispatch(_decision(Destination.LINEAR), "list my issues", build_registry())
    )
    assert reply == "You have reached your Linear agent"


def test_not_available_does_not_call_an_agent() -> None:
    class ExplodingAgent:
        name = "github"

        async def handle(self, query: str) -> str:
            raise AssertionError(query)

    registry = AgentRegistry()
    registry.register(ExplodingAgent())
    reply = asyncio.run(
        dispatch(_decision(Destination.NOT_AVAILABLE), "what is the weather", registry)
    )
    assert reply == NOT_AVAILABLE_REPLY


def test_unclear_returns_the_clarifying_question() -> None:
    question = "Do you mean a GitHub issue or a Linear issue?"
    reply = asyncio.run(
        dispatch(
            _decision(Destination.UNCLEAR, clarifying_question=question, confidence=0.4),
            "show the issue",
            build_registry(),
        )
    )
    assert reply == question


def test_missing_agent_raises() -> None:
    with pytest.raises(KeyError):
        asyncio.run(dispatch(_decision(Destination.LINEAR), "list issues", AgentRegistry()))
