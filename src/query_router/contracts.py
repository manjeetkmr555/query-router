from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

from query_router.routing.replies import DEFAULT_CLARIFYING_QUESTION


class Destination(StrEnum):
    GITHUB = "github"
    LINEAR = "linear"
    UNCLEAR = "unclear"
    NOT_AVAILABLE = "not_available"


ROUTING_ONLY = frozenset({Destination.UNCLEAR, Destination.NOT_AVAILABLE})


class RouteDecision(BaseModel):
    """Classifier output. Agents never build this."""

    destination: Destination
    intent: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    clarifying_question: str | None = None

    @model_validator(mode="after")
    def fill_unclear_question(self) -> "RouteDecision":
        if self.destination is Destination.UNCLEAR and not self.clarifying_question:
            self.clarifying_question = DEFAULT_CLARIFYING_QUESTION
        if self.destination is not Destination.UNCLEAR:
            self.clarifying_question = None
        return self
