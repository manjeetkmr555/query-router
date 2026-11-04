import logging
import time
from collections.abc import Callable
from dataclasses import dataclass

from query_router.agents.registry import AgentRegistry, build_registry
from query_router.contracts import RouteDecision
from query_router.dispatch import dispatch
from query_router.routing.router import classify

logger = logging.getLogger("query_router")

Classifier = Callable[[str], RouteDecision]


def configure_logging() -> None:
    """Print route lines to the terminal. Uvicorn does not configure this logger."""
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)


@dataclass(frozen=True)
class RoutedQuery:
    decision: RouteDecision
    reply: str


async def route_query(
    query: str,
    *,
    model: str | None = None,
    registry: AgentRegistry | None = None,
    classifier: Classifier | None = None,
) -> RoutedQuery:
    """Classify a query, then dispatch. The classifier is the only model call."""
    agents = registry if registry is not None else build_registry()
    started = time.perf_counter()
    if classifier is not None:
        decision = classifier(query)
    elif model is None:
        raise ValueError("model is required when no classifier is provided")
    else:
        decision = await classify(query, model=model)
    reply = await dispatch(decision, query, agents)
    duration_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "query=%s destination=%s intent=%s confidence=%.2f reply=%s duration_ms=%.1f",
        query,
        decision.destination.value,
        decision.intent,
        decision.confidence,
        reply,
        duration_ms,
    )
    return RoutedQuery(decision=decision, reply=reply)
