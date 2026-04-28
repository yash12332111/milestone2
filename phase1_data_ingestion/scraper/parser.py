"""
parser.py — HTML parsing helpers for Groww mutual fund pages.

Extracts structured sections (Basic Info, Expense & Loads, Investment Details,
Holdings, etc.) from the rendered HTML of a Groww scheme page.
"""

from __future__ import annotations

import re
import logging
from typing import Optional
from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


def _clean_text(text: str) -> str:
    """Collapse whitespace and strip."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _safe_text(tag: Optional[Tag]) -> str:
    """Return cleaned inner text of a tag, or empty string."""
    if tag is None:
        return ""
    return _clean_text(tag.get_text(separator=" "))


def _extract_key_value_pairs(container: Tag) -> list[str]:
    """
    Many Groww info sections render as label-value pairs inside div rows.
    This tries to pull them as "Label: Value" strings.
    """
    pairs: list[str] = []
    # Look for table rows or div-based key-value structures
    rows = container.select("tr, [class*='row'], [class*='Row']")
    for row in rows:
        cells = row.find_all(["td", "div", "span"], recursive=False)
        if len(cells) >= 2:
            label = _clean_text(cells[0].get_text())
            value = _clean_text(cells[1].get_text())
            if label and value:
                pairs.append(f"{label}: {value}")
    return pairs


def parse_scheme_page(html: str, source_url: str) -> list[dict]:
    """
    Parse a Groww mutual fund page HTML and return a list of sections.

    Each section is a dict with:
        {"title": str, "content": str}

    The parser is designed to be resilient — if a section can't be found,
    it is simply omitted rather than raising an error.
    """
    soup = BeautifulSoup(html, "html.parser")
    sections: list[dict] = []

    # -----------------------------------------------------------------------
    # 1. Scheme Name & Basic Category
    # -----------------------------------------------------------------------
    basic_info_parts = []

    # Scheme name from the page title / h1
    h1 = soup.find("h1")
    if h1:
        basic_info_parts.append(f"Scheme Name: {_safe_text(h1)}")

    # Category, sub-category, risk from the breadcrumb-like tags near the top
    for link_text in ["Equity", "Large Cap", "Mid Cap", "Small Cap", "ELSS",
                      "Flexi Cap", "Focused", "Multi Cap",
                      "Very High Risk", "High Risk", "Moderate Risk",
                      "Low Risk", "Very High"]:
        if soup.find(string=re.compile(re.escape(link_text), re.I)):
            # Avoid duplicates
            tag_line = f"Tag: {link_text}"
            if tag_line not in basic_info_parts:
                basic_info_parts.append(tag_line)

    # -----------------------------------------------------------------------
    # 2. NAV & Key Metrics
    #    Groww renders NAV prominently — look for common patterns
    # -----------------------------------------------------------------------
    nav_section = []

    # Try to find NAV value (usually in a large-font span near the top)
    nav_patterns = soup.find_all(string=re.compile(r"₹\s*[\d,]+\.?\d*"))
    if nav_patterns:
        nav_val = _clean_text(nav_patterns[0])
        nav_section.append(f"NAV: {nav_val}")

    # AUM
    aum_label = soup.find(string=re.compile(r"Fund\s*Size|AUM", re.I))
    if aum_label:
        parent = aum_label.find_parent()
        if parent:
            aum_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            # Extract the numeric AUM from surrounding text
            aum_match = re.search(r"₹?\s*[\d,]+\.?\d*\s*(Cr|Crore|L|Lakh)?", aum_text, re.I)
            if aum_match:
                nav_section.append(f"AUM: {aum_match.group(0).strip()}")

    if basic_info_parts or nav_section:
        combined = basic_info_parts + nav_section
        sections.append({
            "title": "Basic Info",
            "content": ". ".join(combined) + "."
        })

    # -----------------------------------------------------------------------
    # 3. Expense Ratio, Exit Load, Stamp Duty
    # -----------------------------------------------------------------------
    expense_parts = []

    expense_label = soup.find(string=re.compile(r"Expense\s*Ratio", re.I))
    if expense_label:
        parent = expense_label.find_parent()
        if parent:
            sibling_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            ratio_match = re.search(r"\d+\.?\d*\s*%", sibling_text)
            if ratio_match:
                expense_parts.append(f"Expense Ratio: {ratio_match.group(0)}")

    exit_label = soup.find(string=re.compile(r"Exit\s*Load", re.I))
    if exit_label:
        parent = exit_label.find_parent()
        if parent:
            exit_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            if exit_text:
                expense_parts.append(f"Exit Load: {exit_text}")

    stamp_label = soup.find(string=re.compile(r"Stamp\s*Duty", re.I))
    if stamp_label:
        parent = stamp_label.find_parent()
        if parent:
            stamp_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            duty_match = re.search(r"\d+\.?\d*\s*%", stamp_text)
            if duty_match:
                expense_parts.append(f"Stamp Duty: {duty_match.group(0)}")

    if expense_parts:
        sections.append({
            "title": "Expense & Loads",
            "content": ". ".join(expense_parts) + "."
        })

    # -----------------------------------------------------------------------
    # 4. Investment Details: Min SIP, Min Lumpsum, Lock-in
    # -----------------------------------------------------------------------
    invest_parts = []

    sip_label = soup.find(string=re.compile(r"Min\.?\s*SIP|Minimum\s*SIP", re.I))
    if sip_label:
        parent = sip_label.find_parent()
        if parent:
            sip_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            sip_match = re.search(r"₹?\s*[\d,]+", sip_text)
            if sip_match:
                invest_parts.append(f"Minimum SIP: {sip_match.group(0).strip()}")

    lump_label = soup.find(string=re.compile(r"Min\.?\s*Lumpsum|Minimum.*Investment", re.I))
    if lump_label:
        parent = lump_label.find_parent()
        if parent:
            lump_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            lump_match = re.search(r"₹?\s*[\d,]+", lump_text)
            if lump_match:
                invest_parts.append(f"Minimum Lumpsum: {lump_match.group(0).strip()}")

    lock_label = soup.find(string=re.compile(r"Lock.?in\s*Period", re.I))
    if lock_label:
        parent = lock_label.find_parent()
        if parent:
            lock_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            if lock_text:
                invest_parts.append(f"Lock-in Period: {lock_text}")

    if invest_parts:
        sections.append({
            "title": "Investment Details",
            "content": ". ".join(invest_parts) + "."
        })

    # -----------------------------------------------------------------------
    # 5. Benchmark & Riskometer
    # -----------------------------------------------------------------------
    bench_parts = []

    bench_label = soup.find(string=re.compile(r"Benchmark|Index", re.I))
    if bench_label:
        parent = bench_label.find_parent()
        if parent:
            bench_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            if bench_text and len(bench_text) < 200:
                bench_parts.append(f"Benchmark: {bench_text}")

    risk_label = soup.find(string=re.compile(r"Riskometer|Risk\s*Level", re.I))
    if risk_label:
        parent = risk_label.find_parent()
        if parent:
            risk_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            if risk_text and len(risk_text) < 100:
                bench_parts.append(f"Riskometer: {risk_text}")

    if bench_parts:
        sections.append({
            "title": "Benchmark & Risk",
            "content": ". ".join(bench_parts) + "."
        })

    # -----------------------------------------------------------------------
    # 6. Fund Manager
    # -----------------------------------------------------------------------
    fm_parts = []
    fm_label = soup.find(string=re.compile(r"Fund\s*Manager", re.I))
    if fm_label:
        parent = fm_label.find_parent()
        if parent:
            # Try to get the manager name from sibling or parent
            fm_text = _safe_text(parent.find_next_sibling()) or _safe_text(parent.parent)
            if fm_text and len(fm_text) < 200:
                fm_parts.append(f"Fund Manager: {fm_text}")

    if fm_parts:
        sections.append({
            "title": "Fund Manager",
            "content": ". ".join(fm_parts) + "."
        })

    # -----------------------------------------------------------------------
    # 7. Top Holdings
    # -----------------------------------------------------------------------
    holdings_header = soup.find(string=re.compile(r"Holdings?\s*\(\d+\)", re.I))
    if holdings_header:
        parent = holdings_header.find_parent()
        if parent:
            # Walk forward and collect stock links
            container = parent.find_next_sibling() or parent.parent
            if container:
                stock_links = container.find_all("a", href=re.compile(r"/stocks/"))
                holdings = [_clean_text(a.get_text()) for a in stock_links[:10]]
                if holdings:
                    sections.append({
                        "title": "Top Holdings",
                        "content": f"Top {len(holdings)} Holdings: " + ", ".join(holdings) + "."
                    })

    # -----------------------------------------------------------------------
    # 8. About / Investment Objective (from the "About" section)
    # -----------------------------------------------------------------------
    about_header = soup.find(string=re.compile(r"About\s+.*Fund|Investment\s+Objective", re.I))
    if about_header:
        parent = about_header.find_parent()
        if parent:
            about_container = parent.find_next_sibling() or parent.parent
            if about_container:
                about_text = _safe_text(about_container)
                if about_text and len(about_text) > 20:
                    # Truncate to reasonable size
                    sections.append({
                        "title": "About / Investment Objective",
                        "content": about_text[:1000]
                    })

    # -----------------------------------------------------------------------
    # Fallback — if no sections extracted, dump cleaned page text
    # -----------------------------------------------------------------------
    if not sections:
        logger.warning(f"No structured sections found for {source_url}. Using full-text fallback.")
        full_text = _safe_text(soup.find("body") or soup)
        if full_text:
            # Split into ~500 char blocks
            for i in range(0, len(full_text), 500):
                sections.append({
                    "title": f"Page Content (block {i // 500 + 1})",
                    "content": full_text[i:i + 500]
                })

    return sections
