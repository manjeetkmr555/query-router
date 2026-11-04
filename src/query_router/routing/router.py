from pydantic_ai import Agent, ModelSettings

from query_router.contracts import RouteDecision
from query_router.routing.prompts import ROUTER_INSTRUCTIONS


def build_router(model: str) -> Agent[None, RouteDecision]:
    return Agent(
        model,
        output_type=RouteDecision,
        instructions=ROUTER_INSTRUCTIONS,
        model_settings=ModelSettings(temperature=0),
    )


async def classify(query: str, *, model: str) -> RouteDecision:
    result = await build_router(model).run(query)
    return result.output
