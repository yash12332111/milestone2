"""
scraper.py — Core scraping logic for Groww mutual fund pages.

Uses Playwright (headless Chromium) to render JavaScript-heavy Groww pages,
then passes the rendered HTML to the parser for structured extraction.

Falls back to requests + BeautifulSoup if Playwright is unavailable.
"""

from __future__ import annotations

import logging
import random
import time
from datetime import datetime, timezone, timedelta
from typing import Optional

from phase1_data_ingestion.config import TARGET_URLS, SCRAPE_DELAY_SECONDS, USER_AGENTS
from phase1_data_ingestion.scraper.parser import parse_scheme_page

logger = logging.getLogger(__name__)

# IST timezone
IST = timezone(timedelta(hours=5, minutes=30))


def _get_random_user_agent() -> str:
    """Pick a random realistic user-agent string."""
    return random.choice(USER_AGENTS)


def _scrape_with_playwright(url: str) -> Optional[str]:
    """
    Render the page with Playwright headless Chromium and return the full HTML.
    Returns None if Playwright is not installed or fails.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.warning("Playwright not installed. Install with: pip install playwright && playwright install chromium")
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=_get_random_user_agent(),
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()

            logger.info(f"[Playwright] Navigating to {url}")
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait a bit for any lazy-loaded data to appear
            page.wait_for_timeout(3000)

            html = page.content()
            browser.close()
            return html

    except Exception as e:
        logger.error(f"[Playwright] Failed for {url}: {e}")
        return None


def _scrape_with_requests(url: str) -> Optional[str]:
    """
    Fallback: fetch page with plain requests.
    Many Groww pages are server-side rendered via Next.js, so this may work
    for some content, but JS-only data will be missing.
    """
    try:
        import requests
    except ImportError:
        logger.error("requests library not installed.")
        return None

    try:
        headers = {
            "User-Agent": _get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text

    except Exception as e:
        logger.error(f"[Requests] Failed for {url}: {e}")
        return None


def scrape_url(url: str, scheme_name: str, category: str) -> Optional[dict]:
    """
    Scrape a single Groww mutual fund URL and return structured data.

    Returns a dict matching the architecture spec:
    {
        "scheme_name": str,
        "source_url": str,
        "category": str,
        "scraped_at": str (ISO format),
        "sections": [{"title": str, "content": str}, ...]
    }

    Returns None if scraping fails completely.
    """
    # Try Playwright first (renders JS), fall back to requests
    html = _scrape_with_playwright(url)
    method = "Playwright"

    if html is None:
        logger.info(f"Falling back to requests for {url}")
        html = _scrape_with_requests(url)
        method = "Requests"

    if html is None:
        logger.error(f"All scraping methods failed for {url}")
        return None

    logger.info(f"[{method}] Got HTML for {scheme_name} ({len(html)} bytes)")

    # Parse the HTML into structured sections
    sections = parse_scheme_page(html, url)

    if not sections:
        logger.warning(f"No sections extracted for {scheme_name}")
        return None

    result = {
        "scheme_name": scheme_name,
        "source_url": url,
        "category": category,
        "scraped_at": datetime.now(IST).isoformat(),
        "sections": sections,
    }

    logger.info(f"✅ {scheme_name}: {len(sections)} sections extracted")
    return result


def scrape_all_urls() -> list[dict]:
    """
    Scrape all target URLs defined in config.py.
    Applies rate limiting between requests.

    Returns a list of successfully scraped results.
    Failed URLs are logged and skipped.
    """
    results: list[dict] = []

    for i, target in enumerate(TARGET_URLS):
        url = target["url"]
        scheme_name = target["scheme_name"]
        category = target["category"]

        logger.info(f"[{i + 1}/{len(TARGET_URLS)}] Scraping: {scheme_name}")

        result = scrape_url(url, scheme_name, category)
        if result:
            results.append(result)
        else:
            logger.error(f"❌ Skipped: {scheme_name}")

        # Rate limiting: don't hammer the server
        if i < len(TARGET_URLS) - 1:
            delay = SCRAPE_DELAY_SECONDS + random.uniform(0, 1)
            logger.info(f"Waiting {delay:.1f}s before next request...")
            time.sleep(delay)

    logger.info(f"Scraping complete. {len(results)}/{len(TARGET_URLS)} URLs succeeded.")
    return results
