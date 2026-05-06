# GUIDELINES.md — Resume-AI-Gen Usage Guide
## How to Use Every Tool in the Resume Genie Suite

---

## QUICK START

1. **Launch the app:** `streamlit run main_dashboard.py`
2. **Select a tool** from the left sidebar
3. **Upload your resume** (PDF format) and/or **paste a job description**
4. **Click the action button** and let Grok-4 do the work
5. **Download** your generated content

---

## TOOL-BY-TOOL GUIDE

---

### 1. JD Decoder & Analyzer
**What it does:** Breaks down a job description into actionable hiring insights.

**Input:** Job description text (paste directly)  
**Output:** Table with:
- Core responsibilities
- Required skills
- Nice-to-have skills
- ATS keywords
- Standout traits

**When to use:** First step for any job application. Understand what the employer really wants before you customize anything.

**Pro tip:** Copy the ATS keywords list — you'll need them for your resume and cover letter.

---

### 2. CV Tailor
**What it does:** Rewrites your resume specifically for a target job.

**Input:** Resume PDF + Job Description  
**Output:** Complete rewritten CV in the same structure

**Rules:**
- NEVER adds false information
- Improves summary, bullets, and skills order
- Aligns language with JD keywords

**When to use:** After decoding the JD (Tool 1). Tailor your resume before applying.

**Pro tip:** Compare the output with your original resume to understand what changed and why.

---

### 3. Bullet Sharpener
**What it does:** Rewrites resume bullets in the ATS-friendly "Action + Task + Result" format.

**Input:** Your raw bullet points + Job Description  
**Output:** Side-by-side comparison: Original vs Improved

**Format:** `[Strong Verb] + [What you did] + [Measurable Result]`

**Example:**
- Original: "Worked on machine learning models"
- Improved: "Built ML pipeline that reduced fraud false positives by [ADD METRIC]%"

**When to use:** When your resume bullets feel weak or generic.

**Pro tip:** Replace [ADD METRIC] placeholders with real numbers before submitting.

---

### 4. Cover Letter Generator
**What it does:** Creates a tailored, natural-sounding cover letter.

**Input:** Resume PDF + Job Description  
**Output:** 300-450 word cover letter

**Structure:**
- Opening hook + why this role/company
- 2-4 key achievements matched to JD
- Confident closing with call to action

**When to use:** Every job application. Never skip the cover letter.

**Pro tip:** Personalize the company name and hiring manager name if you know them.

---

### 5. Role-Fit Matrix
**What it does:** Strategic analysis of how you match each JD requirement.

**Input:** Resume PDF + Job Description  
**Output:** 6-column matrix:

| Area from JD | My Strengths | Gaps | CV Focus | Cover Letter Angle | Interview Story |
|---|---|---|---|---|---|

**When to use:** Before interviews — it gives you talking points for every requirement.

**Pro tip:** Focus on the "Gaps" column to know what skills to develop or address proactively.

---

### 6. ATS Alignment Fixer
**What it does:** Optimizes your resume for Applicant Tracking Systems.

**Input:** Resume PDF + Job Description  
**Output:**
- Missing keywords list
- Weak/vague sections flagged
- Redundant content identified
- Rewritten professional summary
- Change-log (what changed and why)

**When to use:** When you're getting no callbacks despite being qualified.

**Pro tip:** Run this tool BEFORE submitting any application. Most rejections happen at the ATS level.

---

### 7. Resume-JD Matcher
**What it does:** Quick compatibility score between your resume and the job.

**Input:** Resume PDF + Job Description  
**Output:**
- Match score (X/100)
- Keywords matched vs missing
- Readability score
- ATS compatibility score
- Skill gap analysis
- Industry-specific suggestions

**When to use:** Quick reality check before investing time in an application.

**Pro tip:** Aim for 70%+ match score. Below 60%, consider whether this role is a good fit.

---

### 8. Interview Question Predictor
**What it does:** Predicts 15 likely interview questions based on the job.

**Input:** Resume PDF + Job Description  
**Output:** 15 questions grouped as:
- 5-7 Technical questions
- 4-6 Behavioral questions
- 2-4 Culture/Values questions

Each question includes 1-2 bullet points for answer guidance.

**When to use:** 2-3 days before the interview.

**Pro tip:** Practice answering all 15 questions out loud. Record yourself.

---

### 9. STAR Answer Builder
**What it does:** Creates 8 structured interview answers using the STAR method.

**Input:** Resume PDF + Job Description  
**Output:** 8 answers covering:
1. Leadership
2. Problem-solving
3. Teamwork
4. Conflict resolution
5. Ownership/Accountability
6. Failure/Mistake
7. Achievement/Success
8. Adaptability/Change

Each with: Situation → Task → Action → Result

**When to use:** After generating interview questions (Tool 8).

**Pro tip:** Customize the stories with your real metrics and names. Practice until natural.

---

### 10. Recruiter Simulator
**What it does:** Reviews your application materials as a hiring manager would.

**Input:** Resume PDF + Cover Letter + Job Description  
**Output:**
- Verdict: Shortlist / Maybe / Reject
- Top 3-4 strengths
- Top 3-4 weaknesses
- 3-5 quick-fix suggestions

**When to use:** Final quality check before submitting.

**Pro tip:** Take the "Reject" or "Maybe" verdict seriously. Fix the issues before applying.

---

### 11. Full Package Generator
**What it does:** Assembles a complete application dossier.

**Input:** Resume PDF + Job Description  
**Output (all-in-one):**
1. CV summary (1-2 sentences)
2. Key skills (ATS-friendly bullet list)
3. Fresh cover letter
4. Predicted interview questions
5. LinkedIn outreach DM (3-4 sentences)
6. Follow-up email template

**When to use:** For your dream job. Go all-in with a complete package.

**Pro tip:** Download the output as Markdown and organize into separate files.

---

### 12. Job Application Tracker
**What it does:** Tracks all your job applications in Google Sheets.

**Setup (first time):**

1. **Enable Google Sheets API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a project (or use existing)
   - Enable "Google Sheets API"
   - Create OAuth 2.0 Client ID (Desktop application)
   - Download credentials JSON

2. **Connect in the app:**
   - Upload your credentials JSON file
   - Click "Connect Google Sheets"
   - Authorize in the browser popup
   - The app creates/manages your tracking sheet

**Tracked fields:**
- Job Title, Company, Application Date
- Status (Applied / Interview / Offer / Rejected / Ghosted)
- Cold Email Sent, LinkedIn HR Contact
- Notes, Result, JD Link

**When to use:** Start tracking from your first application. Stay organized.

**Pro tip:** Update status after each milestone. The data helps you see which companies/roles work best.

---

### 13. Resume Checker (Standalone)
**What it does:** Evaluates your resume without a job description.

**Input:** Resume PDF only  
**Output:**
- Overall score
- Strengths and weaknesses
- Skills mentioned
- Recommended skills to add
- Next career steps

**When to use:** When you're updating your resume generally, not for a specific job.

---

### 14. Career Coach Chat
**What it does:** Conversational AI that knows your resume.

**Input:** Resume PDF + Chat messages  
**Output:** Streaming AI responses

**Sample questions to ask:**
- "What roles am I best suited for?"
- "How should I explain the gap in my resume?"
- "What's the weakest part of my resume?"
- "What salary should I negotiate?"
- "How do I transition from X to Y role?"

**When to use:** Anytime you need career advice, interview prep, or strategy.

---

## DUMMY MODE (No API Key)

If you don't have an xAI API key:
- The app automatically runs in **DUMMY MODE**
- All tools work with pre-formatted placeholder responses
- You can explore the full UI and features
- To unlock real AI generation, add your key to `.streamlit/secrets.toml`:

```toml
XAI_API_KEY = "xai-your-real-key-here"
```

---

## WORKFLOW: JOB APPLICATION CHECKLIST

```
1. [ ] Find a job posting
2. [ ] Paste JD into JD Decoder → understand requirements
3. [ ] Upload resume + JD into Resume-JD Matcher → score match
4. [ ] If 70%+ match: Tailor CV (CV Tailor)
5. [ ] Sharpen key bullets (Bullet Sharpener)
6. [ ] Fix ATS issues (ATS Fixer)
7. [ ] Generate cover letter (Cover Letter Generator)
8. [ ] Build Role-Fit Matrix → interview strategy
9. [ ] Predict interview questions → practice
10. [ ] Build STAR answers → rehearse
11. [ ] Run Recruiter Simulator → final check
12. [ ] Generate Full Package → submit
13. [ ] Log application in Job Tracker
14. [ ] Send LinkedIn outreach DM
15. [ ] Set follow-up reminder (7 days)
```

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "XAI_API_KEY missing" error | Set key in `.streamlit/secrets.toml` or use dummy mode |
| PDF not extracting correctly | Ensure text-based PDF (not scanned image) |
| Google Sheets connection fails | Re-upload credentials JSON and re-authorize |
| Tool takes too long | Grok-4 calls take 20-60 seconds; check internet |
| Output seems generic | Provide more detailed JD and resume for better personalization |
| Chat history lost | Chat resets on page refresh by design |

---

**End of Guidelines**
