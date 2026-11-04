from query_router.contracts import Destination


class GithubAgent:
    name = Destination.GITHUB.value

    async def handle(self, query: str) -> str:
        return "You have reached your GitHub agent"
