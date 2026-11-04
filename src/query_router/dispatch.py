from query_router.agents.registry import AgentRegistry
from query_router.contracts import Destination, RouteDecision
from query_router.routing.replies import DEFAULT_CLARIFYING_QUESTION, NOT_AVAILABLE_REPLY


async def dispatch(decision: RouteDecision, query: str, registry: AgentRegistry) -> str:
    if decision.destination is Destination.NOT_AVAILABLE:
        return NOT_AVAILABLE_REPLY
    if decision.destination is Destination.UNCLEAR:
        return decision.clarifying_question or DEFAULT_CLARIFYING_QUESTION
    return await registry.get(decision.destination.value).handle(query)
