from typing import Protocol


class QueryAgent(Protocol):
    name: str

    async def handle(self, query: str) -> str:
        """Run this agent. The route has already been chosen."""
