import re
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

import httpx


async def search_news(topic: str, max_results: int = 5) -> list[dict]:
    """
    Search Google News RSS for recent articles on a topic.
    Returns a list of {title, summary, source, url, date} dicts.
    Falls back to empty list on any error so script generation still works.
    """
    url = (
        f"https://news.google.com/rss/search"
        f"?q={quote_plus(topic)}&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        async with httpx.AsyncClient(timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except Exception:
        return []

    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError:
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    articles = []
    for item in channel.findall("item")[:max_results]:
        raw_title = item.findtext("title", "")
        # Google appends " - Source Name" to titles — strip it
        title = raw_title.rsplit(" - ", 1)[0].strip()

        # Description is HTML — strip tags
        raw_desc = item.findtext("description", "")
        summary = re.sub(r"<[^>]+>", "", raw_desc).strip()[:600]

        link = item.findtext("link", "")

        source_el = item.find("source")
        source_name = source_el.text.strip() if source_el is not None else "Unknown"
        source_url = source_el.get("url", "") if source_el is not None else ""

        pub_date = item.findtext("pubDate", "")

        if title:
            articles.append({
                "title": title,
                "summary": summary,
                "source": source_name,
                "source_url": source_url or link,
                "date": pub_date,
            })

    return articles
