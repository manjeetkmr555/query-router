from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from query_router.api.schemas import QueryRequest, QueryResponse
from query_router.config import load_settings
from query_router.service import Classifier, configure_logging, route_query

WEB_DIR = Path(__file__).resolve().parents[1] / "web"


def create_app(classifier: Classifier | None = None) -> FastAPI:
    configure_logging()
    app = FastAPI(title="Query router")
    app.state.classifier = classifier

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @app.post("/api/route", response_model=QueryResponse)
    async def route(body: QueryRequest) -> QueryResponse:
        query = body.query.strip()
        if not query:
            raise HTTPException(status_code=422, detail="Enter a query.")

        model = None
        if app.state.classifier is None:
            try:
                model = load_settings().router_model
            except ValidationError as exc:
                raise HTTPException(
                    status_code=503,
                    detail="Set OPENAI_API_KEY in .env before routing a query.",
                ) from exc

        # calling the main router
        routed = await route_query(query, model=model, classifier=app.state.classifier)
        decision = routed.decision
        return QueryResponse(
            destination=decision.destination,
            intent=decision.intent,
            confidence=decision.confidence,
            reply=routed.reply,
        )

    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run("query_router.api.app:app", host="127.0.0.1", port=8000)
