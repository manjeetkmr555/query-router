import argparse
import asyncio

from query_router.config import load_settings
from query_router.service import configure_logging, route_query


def main() -> None:
    configure_logging()
    parser = argparse.ArgumentParser(description="Route a query to GitHub or Linear.")
    parser.add_argument("query", nargs="+")
    args = parser.parse_args()
    query = " ".join(args.query)

    settings = load_settings()
    asyncio.run(route_query(query, model=settings.router_model))


if __name__ == "__main__":
    main()
