import httpx


async def handle_arxiv(params, req_id):
    query = params.get("query", "astro-ph")
    max_results = params.get("max_results", 3)
    url = f"http://export.arxiv.org/api/query?search_query=cat:{query}&start=0&max_results={max_results}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise Exception("API call failed")

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "papers": f"Fetched {max_results} papers on '{query}' (response omitted for brevity)",
                "context": {"type": "arxiv", "query": query}
            }
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32000, "message": str(e)}
        }
