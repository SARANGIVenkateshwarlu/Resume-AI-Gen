# Bulk JD Scrape.py — Standalone Bulk JD Scraper (Phase 5)
# Run: cd scraper && streamlit run "Bulk JD Scrape.py"
import streamlit as st
import json, os, time

# Direct imports from same folder
from scraper import scrape_batch
from sheet_handler import get_google_service, create_scraper_sheet, push_batch_to_sheet

st.set_page_config(page_title="Bulk JD Scraper", page_icon="🌐", layout="wide")
st.title("🌐 Bulk JD Scraper")
st.markdown("Scrape multiple job descriptions from URLs and push results to Google Sheets.")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📎 Job Description URLs")
    urls_text = st.text_area(
        "Paste URLs (one per line or comma-separated)",
        height=250,
        placeholder="https://www.linkedin.com/jobs/view/12345\nhttps://www.indeed.com/viewjob?jk=abc\nhttps://boards.greenhouse.io/company/jobs/7890"
    )

with col2:
    st.subheader("⚙️ Settings")
    st.caption("Supported: LinkedIn, Indeed, Glassdoor, Greenhouse, Lever, Generic")
    with st.expander("Board Detection", expanded=False):
        st.markdown("""
        **Auto-detected from URL:**
        - `linkedin.com` → LinkedIn
        - `indeed.com` → Indeed
        - `glassdoor.com` → Glassdoor
        - `greenhouse.io` → Greenhouse
        - `lever.co` → Lever
        - Other → Generic (auto-detect)
        """)

    st.subheader("📊 Google Sheets")
    scraper_creds = st.file_uploader("Upload Google OAuth JSON", type=["json"])
    existing_sheet = st.text_input("Or existing Sheet ID", placeholder="1a2B3c4D...")

# Parse URLs
urls = []
for line in urls_text.replace(",", "\n").split("\n"):
    u = line.strip()
    if u and u.startswith("http"):
        urls.append(u)

if urls:
    st.info(f"📎 **{len(urls)} URLs** ready to scrape")
    st.markdown("---")

    if st.button("🚀 Scrape All & Push to Sheets", type="primary", use_container_width=True):
        if not scraper_creds:
            st.warning("⚠️ Upload Google OAuth credentials JSON first.")
        else:
            # Connect
            with st.spinner("Connecting to Google Sheets..."):
                creds_json = scraper_creds.read().decode()
                service = get_google_service(creds_json)
                if not service:
                    st.error("Google auth failed. Check credentials.")
                    st.stop()

                if existing_sheet.strip():
                    sheet_id = existing_sheet.strip()
                else:
                    sheet_id = create_scraper_sheet(service)
                st.success(f"✅ Sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")

            # Scrape
            progress_bar = st.progress(0)
            status_text = st.empty()

            def on_progress(current, total, status):
                progress_bar.progress(current / total)
                status_text.text(f"Scraping {current}/{total}... ({status})")

            results = scrape_batch(urls, on_progress)

            # Push
            if results:
                with st.spinner("Pushing to Google Sheets..."):
                    pushed = push_batch_to_sheet(service, sheet_id, results)
                    st.success(f"✅ {pushed} rows pushed to Google Sheets")

            # Summary
            st.markdown("---")
            success_count = sum(1 for r in results if r["status"] == "success")
            fail_count = len(results) - success_count

            col_s1, col_s2, col_s3 = st.columns(3)
            col_s1.metric("✅ Success", success_count)
            col_s2.metric("❌ Failed", fail_count)
            col_s3.metric("📎 Total", len(results))

            # Table
            import pandas as pd
            table = []
            for r in results:
                table.append({
                    "Status": r["status"],
                    "Title": (r.get("title") or "N/A")[:60],
                    "Company": (r.get("company") or "N/A")[:40],
                    "Board": r.get("board", "?"),
                    "Error": r.get("error", "")[:50]
                })
            st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

            # Download
            csv = pd.DataFrame(table).to_csv(index=False)
            st.download_button("💾 Download CSV", csv, "scraped_jds.csv", "text/csv", use_container_width=True)

            # Save locally
            os.makedirs("scraper_outputs", exist_ok=True)
            import time
            ts = time.strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"scraper_outputs/results_{ts}.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            st.caption(f"📁 Saved to: scraper_outputs/results_{ts}.json")

elif urls_text.strip():
    st.warning("⚠️ No valid URLs found. URLs must start with http:// or https://")
else:
    st.info("👆 Paste job URLs above, upload Google credentials, and click Scrape.")
