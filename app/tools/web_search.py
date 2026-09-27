from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web and return a small set of relevant results.
    """

    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=max_results,
            )

            for result in search_results:
                results.append(
                    {
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                    }
                )

    except Exception as e:
        results.append(
            {
                "title": "Search Error",
                "url": "",
                "snippet": str(e),
            }
        )

    return results