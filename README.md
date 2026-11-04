# Query router

A small app that classifies one query and sends it to a GitHub agent, a Linear agent, a clarifying question, or a refusal. The page is at `http://127.0.0.1:8000`.

Requires Python 3.11 or newer and an OpenAI API key. The classifier uses `openai:gpt-4o-mini` unless you set another model.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Edit `.env` and set your key:

```bash
OPENAI_API_KEY=sk-your-key
ROUTER_MODEL=openai:gpt-4o-mini
```

`OPENAI_API_KEY` is required. `ROUTER_MODEL` is optional.

## Run the web app

```bash
query-router-api
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000), type a query, and submit it. The page shows the destination, intent, confidence, and reply.

The server listens on `127.0.0.1:8000`. A missing `OPENAI_API_KEY` returns HTTP 503 when you submit a query.

## Run one query from the terminal

```bash
query-router "List open pull requests"
```

The result is a single log line with the destination, intent, confidence, reply, and duration. This command uses the same classifier as the web app and needs `.env`.

## Tests

```bash
pytest
```

Tests stub the classifier, so they run without an API key.
