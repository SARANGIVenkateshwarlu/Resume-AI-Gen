# MASTER PROJECT DEVELOPMENT REPORT v2.0
## Resume-AI-Gen: My Job Application Engine

**Author:** Satyajit  
**Date:** May 2026  
**Stack:** Python 3.9+, Streamlit, Multi-LLM (Grok/OpenAI/Claude/DeepSeek/Qwen), LangChain, Google Sheets API  
**Repository:** https://github.com/pik1989/Resume-AI-Gen

---

## EXECUTIVE SUMMARY

Resume-AI-Gen is a full-stack Streamlit web application that transforms a single job description into a **complete, high-conversion job application package**. Supporting 5 LLM providers (Grok, OpenAI, Claude, DeepSeek, Qwen), integrated with Google Sheets for job tracking, and featuring an Auto-Pilot mode that runs all 12 PDR steps sequentially without human intervention. Includes a JSON CV Mapper for structured resume generation compatible with react-pdf and ReportLab.

---

## TABLE OF CONTENTS

1. [Project Architecture](#1-project-architecture)
2. [The 12-Step PDR Framework](#2-the-12-step-pdr-framework)
3. [Auto-Pilot Mode](#3-auto-pilot-mode)
4. [JSON CV Mapper (Phase 4)](#4-json-cv-mapper-phase-4)
5. [Technical Stack](#5-technical-stack)
6. [Feature Matrix](#6-feature-matrix)
7. [File Naming Convention](#7-file-naming-convention)
8. [Multi-Provider LLM](#8-multi-provider-llm)
9. [Token Budget & Cost Tracking](#9-token-budget--cost-tracking)
10. [Google Sheets Integration](#10-google-sheets-integration)
11. [Development Phases](#11-development-phases)
12. [Deployment Guide](#12-deployment-guide)
13. [Testing & QA Checklist](#13-testing--qa-checklist)
14. [Future Roadmap](#14-future-roadmap)

---

## 1. PROJECT ARCHITECTURE

```
Resume-AI-Gen/
├── main_dashboard.py          # Main app (15 tools, 2100+ lines)
├── config.py                  # Provider config, token budgets, constants
├── dummy_data.py              # All 12 DUMMY_* response templates
├── utils.py                   # PDF/DOCX/PDF generation, save helpers, naming
├── google_module.py           # Google Sheets OAuth + CRUD
├── requirements.txt           # Python dependencies
├── logo.png                   # App branding
├── .env                       # API keys (git-ignored)
├── .gitignore                 # venv, outputs, .env
├── README.md                  # User-facing readme
├── GUIDELINES.md              # Full usage guidelines
├── PDR/
│   ├── master_v1.md           # This document
│   ├── phase-1.md             # Phase 1: Core AI Engine
│   ├── phase-2.md             # Phase 2: PDR Steps 1-6
│   ├── phase-3.md             # Phase 3: PDR Steps 7-12
│   └── phase-4.md             # Phase 4: JSON CV Mapper
├── project development report_v1.md  # Original PDR prompt template
└── data/
    ├── cover_letter_format.docx        # Reference cover letter template
    ├── cover_letter_venkat_sarangi2.docx
    ├── Sarangi_CV_Data_Scientist.pdf
    ├── Sarangi_CV_Data_Scientist.typ
    └── Sarangi_CV_llm.typ
```

### Output Structure

```
outputs/
└── Senior_ML_Engineer/                    ← Job-specific folder
    ├── 2026-05-06_14-30_JD_/
    │   └── jd_analysis.md
    ├── 2026-05-06_14-31_CV_/
    │   ├── CV_Senior_ML_Engineer_SARANGI.md
    │   ├── CV_Senior_ML_Engineer_SARANGI.docx
    │   └── CV_Senior_ML_Engineer_SARANGI.pdf
    ├── 2026-05-06_14-32_CoverLetter_/
    │   ├── Cover_letter_Senior_ML_Engineer_SARANGI.md
    │   ├── Cover_letter_Senior_ML_Engineer_SARANGI.docx
    │   └── Cover_letter_Senior_ML_Engineer_SARANGI.pdf
    └── 2026-05-06_14-35_AutoPilot_/
        ├── step1_jd_analysis.md
        ├── step2_tailored_cv.md
        └── ...
```

---

## 2. THE 12-STEP PDR FRAMEWORK

| Step | Tool | Input | Output | Token Budget |
|------|------|-------|--------|-------------|
| 1 | JD Decoder | JD text | Structured analysis table (5 areas) | 600 |
| 2 | CV Tailor | CV + JD | Full tailored CV (all sections, no truncation) | 4000 |
| 3 | Bullet Sharpener | Bullets + JD | ATR-formatted bullets (side-by-side) | 800 |
| 4 | Cover Letter | CV + JD + Draft | 300-450 word letter + signature block | 1000 |
| 5 | Role-Fit Matrix | CV + JD | 6-column matrix (Strengths, Gaps, Strategy) | 1200 |
| 6 | ATS Fixer | CV + JD | ATS Score + JD Match % + fixes | 1200 |
| 7 | Resume-JD Matcher | CV + JD | Score /100 + keyword analysis | 1000 |
| 8 | Interview Q Predictor | CV + JD | 15 questions (Tech/Behavioral/Culture) | 1500 |
| 9 | STAR Builder | CV + JD | 8 STAR answers (Situation→Task→Action→Result) | 2000 |
| 10 | Recruiter Simulator | CV + Cover Letter + JD | Shortlist/Maybe/Reject + feedback | 1000 |
| 11 | Full Package | CV + JD | Complete dossier (6 sections) | 2000 |
| 12 | Job Tracker | Google Sheets OAuth | Synced tracking database | N/A |

### Bonus Tools
| Tool | Description |
|------|-------------|
| Resume Checker | Standalone resume evaluation (no JD needed) |
| Career Coach Chat | Conversational AI that knows your resume |
| JSON CV Mapper | Structured JSON output for react-pdf / ReportLab |

### Key Rules (injected into all prompts)
- Candidate: PhD + 4 years experience — highly qualified
- Keep 10% original content (dates, titles, companies)
- Adjust 90% for ATS keywords and JD requirements
- Capstone/Research projects: up to 90% flexibility
- NEVER invent facts — use [ADD METRIC] placeholders

---

## 3. AUTO-PILOT MODE

**One-click complete workflow** — upload everything once, runs all steps automatically.

**Inputs (collected once):**
- Job Description (text area)
- CV (PDF/MD/TXT/TYP upload)
- Bullet points (optional)
- Cover Letter draft (text or .md/.txt/.typ/.docx upload)
- Job Title + Company (for tracker)

**Process:**
1. User clicks "RUN ALL 12 STEPS"
2. Progress bar shows `Step X/12: ToolName...` as each step executes
3. All 11 LLM calls run sequentially with shared session state
4. CV Tailor uses 4000-token budget for full CV generation
5. Cover letter includes signature block format
6. Files named with convention: `Cover_letter_JobTitle_USERNAME.ext`
7. Results displayed in collapsible accordion sections
8. All files saved to single job-specific timestamped folder

**Estimated time:** ~6 minutes (30s/step) with real LLM, ~1 second in dummy mode.

---

## 4. JSON CV MAPPER (Phase 4)

Converts raw CV text into structured JSON for automated PDF rendering.

**Template Styles:** Modern two-column, Minimalist single-page, Academic with publications, Tech/startup bold, Classic professional

**Output Structure:**
```json
{
  "header": {"name", "title", "email", "phone", "linkedin", "location"},
  "summary": "string",
  "experience": [{"title", "company", "dates", "highlights": [...]}],
  "skills": {"languages": [], "frameworks": [], "tools": [], "domains": []},
  "education": [{"degree", "school", "year"}]
}
```

**Integration:** Compatible with react-pdf (pass JSON as props) and ReportLab (iterate JSON for x,y coordinate placement). Download as `.json`.

---

## 5. TECHNICAL STACK

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Streamlit 1.32+ | Web UI framework |
| **LLM Providers** | Grok-4, GPT-4o, Claude 3.5 Sonnet, DeepSeek, Qwen | Multi-provider AI engine |
| **LLM Integration** | LangChain (xai/openai/anthropic) | Provider abstraction |
| **LLM Fallback** | DummyLLM class (15 pre-formatted templates) | Offline dev mode |
| **PDF Parsing** | PyPDF + plain text (.md/.txt/.typ) | Multi-format resume extraction |
| **DOCX Gen** | python-docx (Calibri, 1.15 spacing, justified) | Professional Word output |
| **PDF Gen** | fpdf2 with Unicode sanitization | PDF output |
| **Auth (Google)** | google-auth-oauthlib | Google Sheets OAuth |
| **Sheets API** | google-api-python-client | Google Sheets CRUD |
| **Config** | .env + python-dotenv | API key management |
| **File Naming** | Cover_letter_{JobTitle}_{USERNAME}.{ext} | Standardized convention |

---

## 6. FEATURE MATRIX

| # | Tool Name | Step | Status | Outputs |
|---|-----------|------|--------|---------|
| 0 | Auto-Pilot | All | ✅ Live | All 12 steps in one click |
| 1 | JD Decoder | Step 1 | ✅ Live | jd_analysis.md |
| 2 | CV Tailor | Step 2 | ✅ Live | CV_Job_SARANGI.{md,docx,pdf} |
| 3 | Bullet Sharpener | Step 3 | ✅ Live | sharpened_bullets.md |
| 4 | Cover Letter | Step 4 | ✅ Live | Cover_letter_Job_SARANGI.{md,docx,pdf} |
| 5 | Role-Fit Matrix | Step 5 | ✅ Live | role_fit_matrix.md |
| 6 | ATS Fixer | Step 6 | ✅ Live | ATS score + ats_report.md |
| 7 | Resume-JD Matcher | Step 7 | ✅ Live | match_report.md |
| 8 | Interview Q | Step 8 | ✅ Live | interview_questions.md |
| 9 | STAR Builder | Step 9 | ✅ Live | star_answers.md |
| 10 | Recruiter Simulator | Step 10 | ✅ Live | recruiter_review.md |
| 11 | Full Package | Step 11 | ✅ Live | full_application_package.md |
| 12 | Job Tracker | Step 12 | ✅ Live | Google Sheets sync |
| — | Resume Checker | Standalone | ✅ Live | resume_evaluation.md |
| — | Career Coach | Standalone | ✅ Live | Streaming chat |
| — | JSON CV Mapper | Phase 4 | ✅ Live | cv_structured.json |

---

## 7. FILE NAMING CONVENTION

All generated files follow standardized naming:

```
Cover_letter_{JobTitle}_{USERNAME}.{ext}
CV_{JobTitle}_{USERNAME}.{ext}
```

| Component | Source | Example |
|-----------|--------|---------|
| JobTitle | Extracted from JD first line (3-4 words) | Data_Engineer |
| USERNAME | `.env` variable `USERNAME=SARANGI` | SARANGI |
| ext | md / docx / pdf | md |

**Examples:**
- `Cover_letter_Data_Engineer_SARANGI.md`
- `Cover_letter_Data_Engineer_SARANGI.docx`
- `CV_Data_Engineer_SARANGI.pdf`

Cover letter DOCX includes professional formatting:
- Title: "Cover Letter" centered, Bold 14pt Calibri
- Body: Justified 11pt, 1.15 line spacing
- Signature block: compact (no spacing between lines)
- "Sincerely,", name, institution, contact, date
- 1-inch margins all sides

---

## 8. MULTI-PROVIDER LLM

| Provider | Models | API Key Env | Best For |
|----------|--------|------------|----------|
| Grok (xAI) | grok-4, grok-3 | XAI_API_KEY | Structured outputs |
| OpenAI | gpt-4o, o1, o3-mini | OPENAI_API_KEY | All-rounder |
| Claude (Anthropic) | claude-3-5-sonnet, opus | ANTHROPIC_API_KEY | Writing/cover letters |
| DeepSeek | deepseek-chat, reasoner | DEEPSEEK_API_KEY | Cost-effective |
| Qwen (Alibaba) | qwen-plus, max, turbo | DASHSCOPE_API_KEY | Multilingual |

- Switch providers anytime via sidebar — no restart needed
- Each provider reads its own API key from `.env` file
- No key → automatic DUMMY MODE with pre-formatted responses

---

## 9. TOKEN BUDGET & COST TRACKING

**Pricing Reference (Grok-4.3):**
- Input: $1.25/1M tokens
- Cached: $0.20/1M tokens
- Output: $2.50/1M tokens

**Per-tool budgets:**
| Tool | Output Tokens | Est. Cost |
|------|-------------|-----------|
| JD Decoder | 600 | ~$0.002 |
| CV Tailor | 4000 | ~$0.012 |
| Cover Letter | 1000 | ~$0.004 |
| STAR Builder | 2000 | ~$0.007 |
| Full Package | 2000 | ~$0.007 |

**Session tracking:**
- Total cost counter in sidebar
- API call counter
- Daily budget limit (via `DAILY_LIMIT` env var, default $2.00)
- Hard stop when budget exceeded
- Estimated time display at page bottom (~6 min for full run)

---

## 10. GOOGLE SHEETS INTEGRATION

| Column | Field | Type |
|--------|-------|------|
| A | Job Title | String |
| B | Company | String |
| C | Application Date | Date |
| D | Status | Applied/Interview/Offer/Rejected/Ghosted |
| E | Cold Email Sent | Yes/No |
| F | LinkedIn HR Contact | String |
| G | Notes | String |
| H | Result | String |
| I | JD Link | URL |
| J | Last Updated | Timestamp |

---

## 11. DEVELOPMENT PHASES

### Phase 1 — Core AI Engine ✅
Streamlit scaffold, Grok-4 integration, 4 core tools (Cover Letter, Matcher, Checker, Coach)

### Phase 2 — PDR Steps 1-6 ✅
JD Decoder, CV Tailor, Bullet Sharpener, Role-Fit Matrix, ATS Fixer, Dummy mode

### Phase 3 — PDR Steps 7-12 ✅
Interview Q, STAR Builder, Recruiter Simulator, Full Package, Job Tracker, Google Sheets

### Phase 4 — JSON CV Mapper ✅
Structured JSON output, 5 template styles, react-pdf/ReportLab compatible

### Current (May 2026) — Polish & Automation ✅
- Auto-Pilot mode (one-click full workflow)
- Multi-provider LLM (5 providers)
- Professional DOCX formatting (reference template)
- File naming convention (Cover_letter_Job_USERNAME.ext)
- Shared JD/resume session state
- Progress tracking sidebar (12-step checklist)
- Token budget + cost tracking
- Multi-format resume upload (PDF/MD/TXT/TYP)
- Job-specific output folders
- Cover letter file upload (DOCX/TXT/MD/TYP)
- Unicode-safe PDF generation

---

## 12. DEPLOYMENT GUIDE

### Local Development
```bash
git clone https://github.com/pik1989/Resume-AI-Gen.git
cd Resume-AI-Gen
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Edit .env with your API keys
streamlit run main_dashboard.py
```

### Environment Variables (.env)
```
XAI_API_KEY=xai-your-key
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
DEEPSEEK_API_KEY=sk-your-key
DASHSCOPE_API_KEY=sk-your-key
USERNAME=SARANGI
DAILY_LIMIT=2.00
```

---

## 13. TESTING & QA CHECKLIST

- [x] All 15 tools load without errors
- [x] Multi-format resume upload (PDF/MD/TXT/TYP) works
- [x] 5 LLM providers switchable at runtime
- [x] Dummy mode activates when no API key
- [x] Auto-Pilot runs all 12 steps sequentially
- [x] Shared JD persists across all tools
- [x] Google Sheets auth flow completes
- [x] Job tracker reads/writes to Sheets
- [x] All outputs downloadable (MD/DOCX/PDF)
- [x] DOCX formatting matches reference template
- [x] File naming convention applied (JobTitle_USERNAME)
- [x] Signature block in cover letter DOCX
- [x] Token cost tracking functional
- [x] Progress sidebar updates after each step
- [x] JSON CV Mapper produces valid JSON
- [x] Job-specific output folders created
- [x] Estimated timer displayed at bottom

---

## 14. FUTURE ROADMAP

| Priority | Feature | Timeline |
|----------|---------|----------|
| P0 | LinkedIn profile scraper integration | Q3 2026 |
| P1 | Multi-language resume support | Q3 2026 |
| P1 | Resume template gallery (LaTeX/Word) | Q4 2026 |
| P1 | Automated job board scraping | Q4 2026 |
| P2 | Interview simulation (voice/chat) | Q1 2027 |
| P2 | Direct email sending via Gmail API | Q1 2027 |
| P3 | Chrome extension for 1-click apply | Q2 2027 |

---

**End of Master PDR v2.0 — May 2026**
