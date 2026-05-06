# sheet_handler.py — Push scraped JD data to Google Sheets
import os, sys
from datetime import datetime
import pandas as pd
import streamlit as st

# Use the main google_module for auth
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from google_module import google_auth

def get_google_service(credentials_json=None):
    """Get authenticated Google Sheets service via google_module."""
    if not credentials_json:
        st.error("No credentials provided.")
        return None
    return google_auth(credentials_json)

def push_batch_to_sheet(service, sheet_id, results):
    """Push a batch of scraped results to Google Sheets."""
    try:
        rows = []
        for r in results:
            rows.append([
                r.get("title", ""),
                r.get("company", ""),
                r.get("description", "")[:500],
                r.get("url", ""),
                r.get("board", ""),
                r.get("location", ""),
                r.get("status", ""),
                r.get("error", ""),
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ])

        if not rows:
            return 0

        body = {"values": rows}
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="A:I",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        return len(rows)
    except Exception as e:
        st.error(f"Sheet update error: {e}")
        return 0

def create_scraper_sheet(service, sheet_name="JD_Scraper_Results"):
    """Create a new sheet for scraper results."""
    try:
        spreadsheet = service.spreadsheets().create(body={
            'properties': {'title': sheet_name}
        }).execute()
        sheet_id = spreadsheet['spreadsheetId']

        headers = [['Job Title', 'Company', 'Description', 'URL', 'Board', 'Location', 'Status', 'Error', 'Scraped At']]
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range='A1:I1',
            valueInputOption='RAW', body={'values': headers}
        ).execute()

        # Bold header
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={
            'requests': [{
                'repeatCell': {
                    'range': {'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 1},
                    'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
                    'fields': 'userEnteredFormat(textFormat)'
                }
            }]
        }).execute()
        return sheet_id
    except Exception as e:
        st.error(f"Error creating scraper sheet: {e}")
        return None
