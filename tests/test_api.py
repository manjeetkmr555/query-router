import logging

from fastapi.testclient import TestClient

from query_router.api.app import create_app
from query_router.contracts import Destination, RouteDecision


def _classifier(destination: Destination, question: str | None = None):
    def classify(query: str) -> RouteDecision:
        return RouteDecision(
            destination=destination,
            intent=f"classified: {query}",
            confidence=0.91,
            clarifying_question=question,
        )

    return classify


def test_route_returns_the_github_stub() -> None:
    client = TestClient(create_app(_classifier(Destination.GITHUB)))
    response = client.post("/api/route", json={"query": "list open pull requests"})
    assert response.status_code == 200
    body = response.json()
    assert body["destination"] == "github"
    assert body["intent"] == "classified: list open pull requests"
    assert body["confidence"] == 0.91
    assert body["reply"] == "You have reached your GitHub agent"


def test_route_returns_the_linear_stub() -> None:
    client = TestClient(create_app(_classifier(Destination.LINEAR)))
    response = client.post("/api/route", json={"query": "show my issues"})
    assert response.status_code == 200
    assert response.json()["reply"] == "You have reached your Linear agent"


def test_unclear_and_not_available_stay_in_routing() -> None:
    unclear = TestClient(
        create_app(_classifier(Destination.UNCLEAR, "Do you mean GitHub or Linear?"))
    )
    unavailable = TestClient(create_app(_classifier(Destination.NOT_AVAILABLE)))

    unclear_body = unclear.post("/api/route", json={"query": "show the issue"}).json()
    unavailable_body = unavailable.post("/api/route", json={"query": "weather"}).json()

    assert unclear_body["reply"] == "Do you mean GitHub or Linear?"
    assert unavailable_body["reply"] == "I cannot answer this question"


def test_blank_query_is_rejected() -> None:
    client = TestClient(create_app(_classifier(Destination.GITHUB)))
    response = client.post("/api/route", json={"query": "   "})
    assert response.status_code == 422
    assert response.json()["detail"] == "Enter a query."


def test_route_is_logged(caplog) -> None:
    caplog.set_level(logging.INFO, logger="query_router")
    client = TestClient(create_app(_classifier(Destination.GITHUB)))
    client.post("/api/route", json={"query": "list open pull requests"})

    messages = [record.getMessage() for record in caplog.records if record.name == "query_router"]
    assert len(messages) == 1
    message = messages[0]
    assert "query=list open pull requests" in message
    assert "destination=github" in message
    assert "intent=classified: list open pull requests" in message
    assert "confidence=0.91" in message
    assert "reply=You have reached your GitHub agent" in message
    duration_ms = float(message.rsplit("duration_ms=", 1)[1])
    assert duration_ms >= 0


def test_rejected_query_is_not_logged(caplog) -> None:
    caplog.set_level(logging.INFO, logger="query_router")
    client = TestClient(create_app(_classifier(Destination.GITHUB)))
    response = client.post("/api/route", json={"query": "   "})
    assert response.status_code == 422
    assert [record for record in caplog.records if record.name == "query_router"] == []


def test_index_page_is_served() -> None:
    client = TestClient(create_app(_classifier(Destination.GITHUB)))
    response = client.get("/")
    assert response.status_code == 200
    assert "Query router" in response.text
    assert 'id="query"' in response.text
