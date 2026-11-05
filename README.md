# Query router

## Description

Query Router is a Python-based application that analyzes user queries, identifies their intent, and routes them to the appropriate handlers to generate relevant responses. The application runs locally at http://127.0.0.1:8000.



## Project Structure

## Project Structure

```text
query-router/
│
├── src/
│   └── query_router/
│       ├── main.py                 # Terminal entry: one query
│       ├── config.py               # OPENAI_API_KEY and ROUTER_MODEL
│       ├── service.py              # Classify, dispatch, and log
│       ├── dispatch.py             # Send decision to the right place
│       ├── contracts.py            # Destination and RouteDecision
│       │
│       ├── api/
│       │   ├── app.py              # Web server and POST /api/route
│       │   └── schemas.py          # Request and response models
│       │
│       ├── routing/
│       │   ├── router.py           # Classifier (one model call)
│       │   ├── prompts.py          # Classifier instructions
│       │   └── replies.py          # Clarifying question and refusal text
│       │
│       ├── agents/
│       │   ├── base.py             # Agent interface
│       │   ├── registry.py         # GitHub and Linear lookup
│       │   ├── github/
│       │   │   └── agent.py
│       │   └── linear/
│       │       └── agent.py
│       │
│       └── web/
│           ├── index.html
│           ├── app.js
│           └── styles.css
│
├── tests/
│   ├── test_api.py
│   ├── test_dispatch.py
│   └── test_registry.py
│
├── pyproject.toml
├── .env.example
└── README.md
```

## Features


- Accepts user queries.
- Classifies user intent.
- Routes queries to appropriate handlers.
- Returns structured responses.




## Tech Stack

- Python
- FastAPI – Backend framework.
- Pydantic – Data validation.
- Uvicorn – Runs the FastAPI application.
- Pytest – Automated testing.


## Installation and Setup


1. Prerequisites — Python 3.11+, an OpenAI API key, and git. 

2. git clone https://github.com/manjeetkmr555/query-router.git
   cd query-router

3. Create and activate a virtualenv — python3 -m venv .venv, then source .venv/bin/activate on macOS/Linux and .venv\Scripts\activate on Windows.

4. Install — pip install -e ".[dev]" so both console scripts and pytest are available.

5. Configure — cp .env.example .env (Windows: copy .env.example .env), then set OPENAI_API_KEY. Note that .env is gitignored and must stay in the project root, because the app loads it       from the current directory.


## Tests

```bash
pytest
```

Tests stub the classifier, so they run without an API key.
