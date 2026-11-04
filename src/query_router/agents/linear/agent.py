from query_router.contracts import Destination


class LinearAgent:
    name = Destination.LINEAR.value

    async def handle(self, query: str) -> str:
        return "You have reached your Linear agent"
