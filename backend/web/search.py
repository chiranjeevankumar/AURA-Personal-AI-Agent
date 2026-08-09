"""
Web search operations for AURA.
"""

from html import unescape
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote_plus, unquote, urlparse
from urllib.request import Request, urlopen
import re


SEARCH_URL = "https://html.duckduckgo.com/html/?q={query}"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)


def _clean_text(value: str) -> str:
    """Remove HTML and normalize whitespace."""

    value = unescape(value)
    value = re.sub(r"<[^>]*>", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def _clean_url(value: str) -> str:
    """Normalize a search result URL."""

    value = unescape(value).strip()

    try:
        parsed = urlparse(value)
        query = parse_qs(parsed.query)

        if "uddg" in query and query["uddg"]:
            return unquote(query["uddg"][0])

    except Exception:
        pass

    return value


def _search_web(
    query: str,
    max_results: int = 5,
) -> List[Dict[str, str]]:
    """Fetch and parse DuckDuckGo HTML results."""

    url = SEARCH_URL.format(
        query=quote_plus(query)
    )

    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    with urlopen(request, timeout=15) as response:
        html = response.read().decode(
            "utf-8",
            errors="replace",
        )

    results: List[Dict[str, str]] = []

    link_pattern = re.compile(
        r"""<a[^>]+class=["'][^"']*result__a[^"']*["'][^>]+href=["']([^"']+)["'][^>]*>(.*?)</a>""",
        flags=re.IGNORECASE | re.DOTALL,
    )

    for match in link_pattern.finditer(html):

        if len(results) >= max_results:
            break

        result_url = _clean_url(match.group(1))
        title = _clean_text(match.group(2))

        if not result_url or not title:
            continue

        nearby = html[
            match.end():
            match.end() + 5000
        ]

        snippet_match = re.search(
            r"""class=["'][^"']*result__snippet[^"']*["'][^>]*>(.*?)</""",
            nearby,
            flags=re.IGNORECASE | re.DOTALL,
        )

        snippet = ""

        if snippet_match:
            snippet = _clean_text(
                snippet_match.group(1)
            )

        results.append(
            {
                "title": title,
                "url": result_url,
                "snippet": snippet,
            }
        )

    return results


def search(
    query: str,
    max_results: int = 5,
) -> Dict[str, Any]:
    """
    Perform a web search.

    Returns structured results without pretending that
    a search succeeded when it did not.
    """

    value = str(query).strip()

    if not value:
        return {
            "success": False,
            "message": "Search query cannot be empty.",
            "error": "invalid_query",
            "query": value,
            "results": [],
        }

    try:
        limit = int(max_results)
    except (TypeError, ValueError):
        limit = 5

    limit = max(1, min(limit, 10))

    try:
        results = _search_web(
            value,
            max_results=limit,
        )

        if not results:
            return {
                "success": False,
                "message": (
                    "Web search completed, but no results "
                    "were returned."
                ),
                "error": "no_results",
                "query": value,
                "results": [],
            }

        return {
            "success": True,
            "message": (
                f"Web search completed with "
                f"{len(results)} result(s)."
            ),
            "error": None,
            "query": value,
            "results": results,
        }

    except HTTPError as error:
        return {
            "success": False,
            "message": (
                "Web search provider returned "
                f"HTTP {error.code}."
            ),
            "error": "http_error",
            "query": value,
            "results": [],
        }

    except URLError as error:
        return {
            "success": False,
            "message": (
                "Unable to reach the web search provider."
            ),
            "error": "network_unavailable",
            "query": value,
            "details": str(error.reason),
            "results": [],
        }

    except TimeoutError:
        return {
            "success": False,
            "message": "Web search provider timed out.",
            "error": "search_timeout",
            "query": value,
            "results": [],
        }

    except Exception as error:
        return {
            "success": False,
            "message": "Web search failed unexpectedly.",
            "error": "web_search_error",
            "query": value,
            "details": str(error),
            "results": [],
        }
