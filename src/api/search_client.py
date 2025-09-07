import requests
from typing import List, Dict, Any
from src import config

import logging


logger = logging.getLogger(__name__)

SERPAPI_ENDPOINT = "https://serpapi.com/search"

def get_search_results(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Fetches search results from SerpApi for a given query.

    Args:
        query: The search term.
        num_results: The number of results to return.

    Returns:
        A list of dictionaries, where each dictionary represents a search result
        containing keys like 'position', 'title', 'link', and 'snippet'.
        Returns an empty list if the request fails or no results are found.
     posizione | titolo | link | snippet
    """
    if not query:
        logger.warning("No Query was passed... Returning empty results list.")
        return []

    logger.info(f"Fetching search results for query: '{query}'...")

    params = {
        "api_key": config.SERPAPI_API_KEY,
        "engine": "google",
        "q": query,
        "num": str(num_results),
    }

    try:
        response = requests.get(SERPAPI_ENDPOINT, params=params, timeout=10)
        
        response.raise_for_status()

        data = response.json()

        organic_results = data.get("organic_results", [])
        
        if not organic_results:
            logger.warning("No organic results found in API response.")
            return []
        
        scraped_urls = [result.get("link") for result in organic_results]

        logger.info(f"Successfully fetched {len(scraped_urls)} results.")
        return scraped_urls

    except requests.exceptions.RequestException as e:
        logger.error(f"Network request to SerpApi failed: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred during search API call: {e}")
        return []