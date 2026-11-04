from query_router.agents.base import QueryAgent
from query_router.agents.github.agent import GithubAgent
from query_router.agents.linear.agent import LinearAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, QueryAgent] = {}

    def register(self, agent: QueryAgent) -> None:
        if agent.name in self._agents:
            raise ValueError(f"Agent '{agent.name}' is already registered")
        self._agents[agent.name] = agent

    def get(self, name: str) -> QueryAgent:
        try:
            return self._agents[name]
        except KeyError as exc:
            raise KeyError(f"No agent registered for '{name}'") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(self._agents)


def build_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(GithubAgent())
    registry.register(LinearAgent())
    return registry
