# google_module.py — Google Sheets Auth & CRUD
import os, json, pickle, tempfile
import pandas as pd
import streamlit as st
from config import GOOGLE_SCOPES

def google_auth(credentials_json):
    """Authenticate with Google. Supports both Service Account JSON and OAuth Client JSON."""
    try:
        from google.oauth2.credentials import Credentials
        from google.oauth2 import service_account
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        client_config = json.loads(credentials_json) if isinstance(credentials_json, str) else credentials_json

        # Check if this is a Service Account key
        if client_config.get("type") == "service_account":
            creds = service_account.Credentials.from_service_account_info(
                client_config, scopes=GOOGLE_SCOPES
            )
            return build('sheets', 'v4', credentials=creds)

        # OAuth Client flow
        creds = None
        token_file = os.path.join(tempfile.gettempdir(), "resume_genie_google_token.pickle")

        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(client_config, GOOGLE_SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        return build('sheets', 'v4', credentials=creds)
    except ImportError:
        st.error("Google API libraries not installed.")
        return None
    except Exception as e:
        st.error(f"Google auth error: {e}")
        return None
def get_or_create_sheet(service, sheet_name="ResumeAI_JobTracker"):
    """Get existing sheet by name, or create a new one."""
    try:
        # Search for existing sheet with this name
        results = service.spreadsheets().get(spreadsheetId=service._spreadsheet_id) if hasattr(service, '_spreadsheet_id') else None
        # Actually search by name
        try:
            query = f'name = "{sheet_name}"'
            search_result = service.files().list(q=query, fields="files(id, name)").execute()
            # Note: Drive API scope needed for this. Fall back to creating new.
        except Exception:
            pass

        # Always create new for simplicity (user can provide existing sheet ID)
        spreadsheet = service.spreadsheets().create(body={
            'properties': {'title': sheet_name}
        }).execute()
        sheet_id = spreadsheet['spreadsheetId']

        headers = [['Job Title', 'Company', 'Application Date', 'Status', 'Cold Email Sent',
                     'LinkedIn HR Contact', 'Notes', 'Result', 'JD Link', 'Last Updated']]
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range='A1:J1',
            valueInputOption='RAW', body={'values': headers}
        ).execute()

        return sheet_id
    except Exception as e:
        st.error(f"Error creating sheet: {e}")
        return None

def add_job_application(service, sheet_id, data):
    try:
        from datetime import datetime
        values = [[
            data.get('job_title', ''), data.get('company', ''),
            data.get('app_date', datetime.now().strftime('%Y-%m-%d')),
            data.get('status', 'Applied'), data.get('cold_email', 'No'),
            data.get('linkedin_hr', ''), data.get('notes', ''),
            data.get('result', ''), data.get('jd_link', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M')
        ]]
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id, range='A1',
            valueInputOption='RAW', insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()
        return True
    except Exception as e:
        st.error(f"Error adding application: {e}")
        return False

def get_all_applications(service, sheet_id):
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range='A:J'
        ).execute()
        values = result.get('values', [])
        if not values:
            return pd.DataFrame()
        return pd.DataFrame(values[1:], columns=values[0]) if len(values) > 1 else pd.DataFrame(columns=values[0])
    except Exception as e:
        st.error(f"Error reading applications: {e}")
        return pd.DataFrame()

def check_duplicate(df, job_title, company):
    if df.empty:
        return False
    matches = df[(df['Job Title'].str.lower() == job_title.lower()) &
                 (df['Company'].str.lower() == company.lower())]
    return len(matches) > 0
