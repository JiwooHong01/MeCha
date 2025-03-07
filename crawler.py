# crawler.py

import requests
import time
import json
from collections import deque
from urllib.parse import urlparse, urljoin

# lxml for HTML parsing + XPath
from lxml import etree


def bfs_crawl_with_xpath(
    start_url: str,
    max_depth: int = 2,
    max_pages: int = 30,
    sleep_sec: float = 0.5,
    custom_user_agent: str = "MyCrawler/1.0"
) -> dict:
    """
    A BFS crawler that:
      1) Starts from `start_url`
      2) Restricts to the same domain
      3) Extracts <a href="..."> using an XPath expression
      4) Respects max_depth, max_pages
      5) Returns { url: {"title": <title_text>, "text": <page_text>} }

    Args:
        start_url (str): The initial URL to begin crawling.
        max_depth (int): The maximum link-following depth (0 = only start_url).
        max_pages (int): The maximum number of pages to visit.
        sleep_sec (float): Delay between requests (courtesy to the server).
        custom_user_agent (str): Custom User-Agent header.

    Returns:
        dict: A dictionary { url: { "title": ..., "text": ... } }
    """

    # We'll restrict ourselves to the same domain as start_url
    start_domain = urlparse(start_url).netloc  # e.g. 'www.cdc.gov'

    visited = set()
    results = {}

    # Queue for BFS, each entry is (url, depth)
    queue = deque()
    queue.append((start_url, 0))

    headers = {
        "User-Agent": custom_user_agent
    }

    while queue:
        current_url, depth = queue.popleft()

        # Depth check
        if depth > max_depth:
            continue

        # Page limit check
        if len(visited) >= max_pages:
            print(f"[Info] Reached max_pages={max_pages}. Stopping.")
            break

        # Avoid revisiting
        if current_url in visited:
            continue
        visited.add(current_url)

        # Fetch the page
        try:
            resp = requests.get(current_url, timeout=10, headers=headers)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[Error] {current_url} fetch failed: {e}")
            continue

        content_bytes = resp.content  # We'll parse from bytes to better handle encoding issues

        # Parse with lxml
        try:
            parser = etree.HTMLParser(recover=True, encoding=resp.encoding if resp.encoding else "utf-8")
            doc = etree.fromstring(content_bytes, parser=parser)
        except Exception as e:
            print(f"[Parse Error] {current_url}: {e}")
            continue

        # Extract <title> (fallback to "No Title")
        print("[currenturl] =", current_url)
        try:
            title_nodes = doc.xpath("//title/text()")
            title_text = title_nodes[0].strip()
        except:
            title_text = "No Title"
            continue

        # Extract all text (naive approach: get the text content of the entire doc)
        # lxml doesn't have a single method for "doc.get_text()", so we do:
        all_text = "".join(doc.xpath("//text()")).strip()

        # Store in results
        results[current_url] = {
            "title": title_text,
            "text": all_text
        }

        print(f"[Visited] {current_url} (depth={depth}, title='{title_text}')")

        # Use XPath to find all <a> elements' href attributes
        # For example, use a generic:  //a/@href
        # Or you can use your full path: /html/body/div[4]/main/... 
        # if you only want specific anchors. 
        anchor_hrefs = doc.xpath("//a/@href")

        for link_href in anchor_hrefs:
            # Convert to absolute
            absolute_link = urljoin(current_url, link_href)

            # Only follow if same domain
            if urlparse(absolute_link).netloc == start_domain:
                postfixes = ["other", "spanish", "Other"]
                flag = 0
                for postfix in postfixes:
                    if absolute_link.startswith("https://www.cdc.gov/" + postfix):
                        flag = 1
                        break
                if flag == 0:
                    queue.append((absolute_link, depth + 1))

        # Politeness: wait a bit
        time.sleep(sleep_sec)

    return results


if __name__ == "__main__":
    # Example usage
    START_URL = "https://www.cdc.gov/health-topics.html"
    MAX_DEPTH = 10
    MAX_PAGES = 3000
    SLEEP_SEC = 0.5

    print(f"[Info] Starting BFS crawl from: {START_URL}")

    crawled_data = bfs_crawl_with_xpath(
        start_url=START_URL,
        max_depth=MAX_DEPTH,
        max_pages=MAX_PAGES,
        sleep_sec=SLEEP_SEC,
        custom_user_agent="MyCrawler/1.0 (XPath Demo)"
    )

    print(f"[Info] Crawl finished! Visited {len(crawled_data)} pages total.\n")

    # Save to JSON
    out_file = "crawled_data.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(crawled_data, f, ensure_ascii=False, indent=2)

    print(f"[Info] Saved results to '{out_file}'")
