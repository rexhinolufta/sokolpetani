import httpx


async def quick_web_search(query: str) -> dict:
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    return {
        "query": query,
        "heading": data.get("Heading"),
        "abstract": data.get("AbstractText"),
        "abstract_url": data.get("AbstractURL"),
        "related_topics_count": len(data.get("RelatedTopics", [])),
    }
