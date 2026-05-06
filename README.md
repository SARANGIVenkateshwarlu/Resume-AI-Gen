# 🚀 Resume-AI-Gen: AI Career & Resume Toolkit
**Powered by Grok-4 (xAI) + Streamlit + Google Sheets**

A powerful, all-in-one AI-powered job application engine that implements a **12-step Project Development Report (PDR)** framework. Upload your resume + paste a job description, and get a complete application package: tailored CV, ATS-optimized bullets, cover letter, interview prep, recruiter-style feedback, and a Google Sheets job tracker — **all in one beautiful Streamlit app**.

---

<p align="center">
  <a href="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  </a>
  <a href="https://img.shields.io/badge/xAI-Grok--4-black?style=for-the-badge">
    <img src="https://img.shields.io/badge/xAI-Grok--4-black?style=for-the-badge" alt="Grok-4">
  </a>
  <a href="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://img.shields.io/badge/Google-Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white">
    <img src="https://img.shields.io/badge/Google-Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white" alt="Google Sheets">
  </a>
  <a href="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
  </a>
</p>

---

## ✨ FEATURES — The 12-Step PDR Framework

| # | Tool | Category | What it does |
|---|------|----------|--------------|
| 1 | 🔍 JD Decoder | Analysis | Extracts skills, keywords, responsibilities, and standout traits from any JD |
| 2 | 📝 CV Tailor | Creation | Rewrites your resume specifically for the target job (no false info) |
| 3 | 🔫 Bullet Sharpener | Creation | Rewrites resume bullets in Action+Task+Result (ATR) format |
| 4 | ✉️ Cover Letter Generator | Creation | Tailored 300-450 word cover letter with hook + achievements + closing |
| 5 | 🧩 Role-Fit Matrix | Strategy | 6-column matrix: JD areas vs Your strengths, gaps, CV focus, CL angle, interview stories |
| 6 | 🛠️ ATS Alignment Fixer | Strategy | Identifies missing keywords, fixes weak sections, rewrites summary for ATS |
| 7 | 📊 Resume-JD Matcher | Analysis | Quick compatibility score (X/100) with keyword overlap, readability, ATS score |
| 8 | ❓ Interview Q Predictor | Interview | 15 predicted questions (technical, behavioral, culture) with answer guidance |
| 9 | ⭐ STAR Answer Builder | Interview | 8 STAR-formatted answers (Leadership, Problem-solving, Teamwork, etc.) |
| 10 | 🎯 Recruiter Simulator | Review | Hiring manager review with Shortlist/Maybe/Reject verdict + feedback |
| 11 | 📦 Full Package Generator | Package | Complete application dossier: CV, skills, CL, interview Qs, LinkedIn DM, follow-up email |
| 12 | 📋 Job Tracker | Tracking | Google Sheets-integrated application tracker (status, emails, results) |

### Bonus Tools
| Tool | What it does |
|------|-------------|
| 📋 Resume Checker | Standalone resume evaluation (no JD needed) |
| 💬 Career Coach Chat | Conversational AI mentor that knows your resume |

---

## 🎯 THE PDR WORKFLOW

```
Job Description ──► Step 1: Decode JD ──► Step 7: Match Score
                         │
                   Step 2: Tailor CV
                   Step 3: Sharpen Bullets
                   Step 6: Fix ATS Issues
                         │
                   Step 4: Cover Letter ──► Step 5: Role-Fit Matrix
                                                 │
                                           Step 8: Interview Qs
                                           Step 9: STAR Answers
                                                 │
                                           Step 10: Recruiter Review
                                                 │
                                           Step 11: Full Package ──► SUBMIT
                                                                      │
                                                                Step 12: Track in Sheets
```

---

## 🚀 QUICK START

```bash
# 1. Clone the repo
git clone https://github.com/pik1989/Resume-AI-Gen.git
cd Resume-AI-Gen

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Add your xAI API key for real AI generation
# Create .streamlit/secrets.toml:
echo 'XAI_API_KEY = "xai-your-real-key-here"' > .streamlit/secrets.toml

# Without a key, the app runs in DUMMY MODE — fully functional UI
# with placeholder responses for testing

# 5. Run the app
streamlit run main_dashboard.py
```

---

## 📊 GOOGLE SHEETS INTEGRATION (Job Tracker)

The Job Application Tracker syncs with Google Sheets. Setup takes 2 minutes:

### One-Time Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable **Google Sheets API**
3. Create **OAuth 2.0 Client ID** (Desktop application type)
4. Download credentials JSON
5. Upload the JSON in the app's Job Tracker tool
6. Click **Connect Google Sheets** → authorize in browser

### What Gets Tracked
| Field | Description |
|-------|-------------|
| Job Title | Position name |
| Company | Company name |
| Application Date | When you applied |
| Status | Applied → Interview → Offer → Rejected → Ghosted |
| Cold Email Sent | Did you reach out to HR? |
| LinkedIn HR Contact | Name of HR person |
| Notes | Any additional info |
| Result | Final outcome |
| JD Link | URL to job posting |

---

## 📂 PROJECT STRUCTURE

```
Resume-AI-Gen/
├── main_dashboard.py          # Main app (14 tools)
├── requirements.txt           # Python dependencies
├── logo.png                   # App branding
├── .streamlit/
│   └── secrets.toml           # API keys (git-ignored)
├── README.md                  # This file
├── GUIDELINES.md              # Full usage guide
├── master_v1.md               # Master PDR v1.0
├── phase-1.md                 # Phase 1 dev report
├── phase-2.md                 # Phase 2 dev report
├── phase-3.md                 # Phase 3 dev report
└── project development report_v1.md  # Original PDR template
```

---

## 🛠️ TECH STACK

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit 1.32+ |
| AI Engine | Grok-4 (xAI) via LangChain |
| PDF Parsing | PyPDF (langchain_community) |
| Google Integration | google-api-python-client, google-auth-oauthlib |
| Prompt Engineering | LangChain PromptTemplate |
| Data Handling | Pandas |

---

## 🔑 API KEYS

| Key | Required? | Where to set |
|-----|-----------|--------------|
| `XAI_API_KEY` | No (dummy mode) | `.streamlit/secrets.toml` or env var |
| Google OAuth JSON | For Job Tracker | Upload in-app |

Without `XAI_API_KEY`, the app runs in **DUMMY MODE** — all 14 tools are functional with placeholder responses for testing and UI exploration.

---

## 📖 DOCUMENTATION

| Document | Purpose |
|----------|---------|
| [`GUIDELINES.md`](GUIDELINES.md) | Step-by-step usage guide for every tool |
| [`master_v1.md`](master_v1.md) | Full project architecture & PDR framework |
| [`phase-1.md`](phase-1.md) | Phase 1: Core AI Engine build report |
| [`phase-2.md`](phase-2.md) | Phase 2: PDR Steps 1-6 implementation |
| [`phase-3.md`](phase-3.md) | Phase 3: PDR Steps 7-12 + Google Sheets |

---

## 🧪 DUMMY MODE

No API key? No problem. The app launches in dummy mode:

```
🧪 DUMMY MODE ACTIVE
Real AI generation requires an xAI API key.
All tools work with placeholder responses for testing.

Add to .streamlit/secrets.toml:
XAI_API_KEY = "xai-your-key-here"
```

---

## 📝 LICENSE

MIT License — free to use, modify, and distribute.

---

**Built by Satyajit • May 2026 • Powered by Grok-4 (xAI)**
