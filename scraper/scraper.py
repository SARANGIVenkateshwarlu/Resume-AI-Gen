# scraper.py — Bulk JD Scraper with configurable selectors
import json, re, time, os
import requests
from bs4 import BeautifulSoup

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "scraper_config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_board(url):
    """Detect job board from URL pattern."""
    url_lower = url.lower()
    if "linkedin.com" in url_lower:
        return "linkedin"
    elif "indeed.com" in url_lower:
        return "indeed"
    elif "glassdoor.com" in url_lower:
        return "glassdoor"
    elif "greenhouse.io" in url_lower:
        return "greenhouse"
    elif "lever.co" in url_lower:
        return "lever"
    return "generic"

def extract_text(soup, selectors):
    """Try multiple CSS selectors, return first match text."""
    if isinstance(selectors, str):
        selectors = [s.strip() for s in selectors.split(",")]
    for sel in selectors:
        try:
            el = soup.select_one(sel)
            if el:
                text = el.get_text(separator=" ", strip=True)
                if text:
                    return text
        except Exception:
            continue
    return ""

def scrape_single_url(url, config=None):
    """Scrape a single JD URL. Returns dict with title, company, description, url, status."""
    if config is None:
        config = load_config()

    board = detect_board(url)
    board_config = config["job_boards"].get(board, config["job_boards"]["generic"])
    settings = config["settings"]
    headers = board_config.get("headers", {})

    result = {
        "url": url,
        "board": board,
        "title": "",
        "company": "",
        "description": "",
        "location": "",
        "status": "pending",
        "error": ""
    }

    # Retry loop
    for attempt in range(settings["retry_count"] + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=settings["request_timeout"])
            if resp.status_code == 404:
                result["status"] = "not_found"
                result["error"] = "404 — Page not found"
                return result
            if resp.status_code == 403:
                result["status"] = "blocked"
                result["error"] = "403 — Access blocked (try LinkedIn public mode or different URL)"
                return result
            if resp.status_code != 200:
                if attempt < settings["retry_count"]:
                    time.sleep(settings["retry_delay"])
                    continue
                result["status"] = "error"
                result["error"] = f"HTTP {resp.status_code}"
                return result

            soup = BeautifulSoup(resp.text, "html.parser")
            selectors = board_config["selectors"]

            result["title"] = extract_text(soup, selectors.get("title", "h1"))
            result["company"] = extract_text(soup, selectors.get("company", ""))
            result["description"] = extract_text(soup, selectors.get("description", ""))
            result["location"] = extract_text(soup, selectors.get("location", ""))

            # Trim description
            if len(result["description"]) > settings["max_jd_length"]:
                result["description"] = result["description"][:settings["max_jd_length"]] + "..."

            # Fallback: if no specific selectors worked, try body text
            if not result["description"]:
                body = soup.find("body")
                if body:
                    result["description"] = body.get_text(separator=" ", strip=True)[:settings["max_jd_length"]]

            result["status"] = "success"
            return result

        except requests.exceptions.Timeout:
            if attempt < settings["retry_count"]:
                time.sleep(settings["retry_delay"])
                continue
            result["status"] = "timeout"
            result["error"] = "Request timed out"
        except requests.exceptions.ConnectionError:
            result["status"] = "connection_error"
            result["error"] = "Connection failed — check URL or network"
            return result
        except Exception as e:
            if attempt < settings["retry_count"]:
                time.sleep(settings["retry_delay"])
                continue
            result["status"] = "error"
            result["error"] = str(e)[:200]

    return result

def scrape_batch(urls, progress_callback=None):
    """Scrape multiple URLs sequentially. Returns list of result dicts."""
    config = load_config()
    results = []
    total = len(urls)

    for i, url in enumerate(urls):
        url = url.strip()
        if not url or not url.startswith("http"):
            results.append({"url": url, "status": "skipped", "error": "Invalid URL", "title": "", "company": "", "description": ""})
            if progress_callback:
                progress_callback(i + 1, total, "skipped")
            continue

        result = scrape_single_url(url, config)
        results.append(result)

        if progress_callback:
            progress_callback(i + 1, total, result["status"])

        # Delay between requests
        if i < total - 1:
            time.sleep(config["settings"]["delay_between_requests"])

    return results
