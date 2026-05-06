# PHASE 5: Bulk JD Scraper — Automated Job Description Ingestion
## Status: ✅ COMPLETED

**Goal:** Enable bulk processing of multiple Job Description URLs via a one-click scraping pipeline that extracts Job Title, Company, and JD Text, then pushes results to Google Sheets.

---

## ARCHITECTURE

```
User Input (URLs)
    │
    ▼
scraper.py (BeautifulSoup + requests)
    │  ├─ detect_board(url) → linkedin/indeed/glassdoor/greenhouse/lever/generic
    │  ├─ scrape_single_url(url) → {title, company, description, status}
    │  └─ scrape_batch(urls) → [results...]
    │
    ▼
sheet_handler.py (Google Sheets API)
    ├─ get_google_service(creds) → authenticated Sheets v4 service
    ├─ create_scraper_sheet() → new sheet with headers
    └─ push_batch_to_sheet(results) → append rows
    │
    ▼
Google Sheets (live results)
```

---

## FEATURES

### 1. Multi-Board Support
Scraper auto-detects job board from URL pattern and applies board-specific CSS selectors:

| Board | URL Pattern | Selectors Configured |
|-------|------------|---------------------|
| LinkedIn | `linkedin.com` | Title, Company, Description, Location |
| Indeed | `indeed.com` | Title, Company, Description, Location |
| Glassdoor | `glassdoor.com` | Title, Company, Description, Location |
| Greenhouse | `greenhouse.io` | Title, Company, Description, Location |
| Lever | `lever.co` | Title, Company, Description, Location |
| Generic | Any other | Auto-detect from h1, common class names |

### 2. Configurable Selectors
All CSS selectors are stored in `scraper_config.json` — no hardcoded logic:
```json
{
  "job_boards": {
    "linkedin": {
      "selectors": {
        "title": "h1.top-card-layout__title, h1.jobs-unified-top-card__job-title",
        "company": "a.topcard__org-name-link, span.jobs-unified-top-card__company-name",
        "description": "div.description__text, div.jobs-description__content"
      }
    }
  }
}
```

### 3. Error Resilience
- 404 → marked `not_found`, batch continues
- 403 → marked `blocked`, batch continues
- Timeout → retries up to 2 times
- Connection error → marked, batch continues
- Invalid URL → skipped with warning

### 4. Google Sheets Push
- One-click OAuth authentication
- Creates dedicated `JD_Scraper_Results` sheet
- Batch-inserts all scraped rows in single API call
- Columns: Job Title, Company, Description, URL, Board, Location, Status, Error, Scraped At

### 5. Versioning Safety
- Before Phase 5 changes: `versioning/v2026-05-06_original/` contains all original source files
- Original implementations preserved untouched

### 6. Results Dashboard
- Progress bar during scrape
- Summary metrics: Success/Failed/Total/Sheet ID
- Detailed results table with status, title, company, board
- CSV download + JSON output saved to job folder

---

## FILES CREATED

| File | Purpose |
|------|---------|
| `scraper.py` | Core scraping engine (detect_board, scrape_single_url, scrape_batch) |
| `scraper_config.json` | CSS selectors for 6 job boards + settings |
| `sheet_handler.py` | Google Sheets auth + batch push functions |
| `versioning/v2026-05-06_original/` | Pre-Phase-5 source backup |
| `PDR/phase-5.md` | This document |

## FILES MODIFIED

| File | Changes |
|------|---------|
| `main_dashboard.py` | Added "Bulk JD Scraper" tool (sidebar + UI) |
| `requirements.txt` | Added `beautifulsoup4`, `requests` |

---

## SETUP

```bash
pip install beautifulsoup4 requests
# Google Sheets: upload OAuth credentials JSON in-app
```

---

**End of Phase 5 Report**
