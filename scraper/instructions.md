# Bulk JD Scraper — Instructions

## Overview
Scrapes multiple Job Description URLs in one click. Extracts Job Title, Company, JD Text, and Location from 6+ job boards. Pushes results to Google Sheets automatically.

## Folder Structure
```
scraper/
├── instructions.md          ← This file
├── scraper.py               ← Core scraping engine
├── scraper_config.json      ← Board selectors + settings
└── sheet_handler.py         ← Google Sheets push
```

---

## Quick Start

### 1. Install Dependencies
```bash
pip install beautifulsoup4 requests
```

### 2. Get Google OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable **Google Sheets API**
3. Create **OAuth 2.0 Client ID** (Desktop application type)
4. Download the JSON credentials file

### 3. Run Standalone
```bash
cd scraper
streamlit run "Bulk JD Scrape.py"
```

### 4. Use in Main Web App
1. Launch the app: `streamlit run main_dashboard.py`
2. Select **"Bulk JD Scraper"** from the sidebar
3. Paste job URLs (one per line)
4. Upload your Google OAuth credentials JSON
5. Click **"Scrape All & Push to Sheets"**

### 4. Standalone Execution (Python)
```python
from scraper.scraper import scrape_batch
from scraper.sheet_handler import get_google_service, create_scraper_sheet, push_batch_to_sheet

# Prepare URLs
urls = [
    "https://www.linkedin.com/jobs/view/12345",
    "https://www.indeed.com/viewjob?jk=abc123",
    "https://boards.greenhouse.io/example/jobs/7890"
]

# Scrape
results = scrape_batch(urls)
print(f"Scraped: {sum(1 for r in results if r['status']=='success')}/{len(results)}")

# Push to Google Sheets (requires OAuth JSON file)
with open("credentials.json") as f:
    creds = f.read()
service = get_google_service(creds)
sheet_id = create_scraper_sheet(service)
push_batch_to_sheet(service, sheet_id, results)
print(f"Results: https://docs.google.com/spreadsheets/d/{sheet_id}")
```

---

## Supported Job Boards

| Board | URL Pattern | Auto-Detected |
|-------|------------|:---:|
| LinkedIn | `linkedin.com/jobs/` | ✅ |
| Indeed | `indeed.com/viewjob` | ✅ |
| Glassdoor | `glassdoor.com/` | ✅ |
| Greenhouse | `greenhouse.io/` | ✅ |
| Lever | `lever.co/` | ✅ |
| Generic | Any other | ✅ |

---

## Configuration (scraper_config.json)

### Adding a New Job Board
Edit `scraper_config.json` and add a new entry under `job_boards`:

```json
"example_board": {
  "name": "Example Board",
  "selectors": {
    "title": "h1.job-title, div.position-name",
    "company": "span.employer, div.company-info",
    "description": "div.job-body, section.details",
    "location": "span.city, div.location"
  },
  "headers": {"User-Agent": "Mozilla/5.0 ..."}
}
```

### Settings
```json
"settings": {
  "request_timeout": 15,        // seconds
  "retry_count": 2,             // retries on failure
  "retry_delay": 2,             // seconds between retries
  "max_jd_length": 8000,        // max chars per description
  "delay_between_requests": 1.0 // politeness delay
}
```

---

## Error Handling

| Status | Meaning | Batch Continues? |
|--------|---------|:---:|
| `success` | JD extracted successfully | ✅ |
| `not_found` | 404 — page removed | ✅ |
| `blocked` | 403 — access denied | ✅ |
| `timeout` | Request timed out (after retries) | ✅ |
| `connection_error` | Network/DNS failure | ✅ |
| `skipped` | Invalid URL format | ✅ |

No single URL failure stops the entire batch.

---

## Google Sheets Output

| Column | Content |
|--------|---------|
| A | Job Title |
| B | Company |
| C | Description (first 500 chars) |
| D | URL |
| E | Board (linkedin/indeed/etc.) |
| F | Location |
| G | Status |
| H | Error message |
| I | Scraped timestamp |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "403 Blocked" on LinkedIn | Use public LinkedIn job URLs (not login-required) |
| No description extracted | Board HTML may have changed — update selectors in config |
| Google auth fails | Re-download OAuth JSON from Cloud Console |
| Timeout on all URLs | Increase `request_timeout` in config |
| "Invalid URL" | Ensure URLs start with `http://` or `https://` |
