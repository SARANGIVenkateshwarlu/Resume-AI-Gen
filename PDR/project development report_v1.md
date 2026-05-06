### Prompt: Project Development Report – “My Job Application Engine”

You are my AI career strategist and project‑design partner.

My goal: Turn a single job description into a **complete, high‑conversion application package**, including tailored CV, ATS‑optimized bullets, cover letter, interview prep, and recruitment‑style feedback.

Use the 10‑step framework below as your **Project Development Report (PDR)**. For each step, return a clearly labeled section with concise, actionable output.

---

🎯 STEP 1 — DECODE THE JOB DESCRIPTION

Job: [paste full job description]

Task:
- Act as a **hiring manager / recruiter** for this role.
- Extract:
  - Core responsibilities (bullet list).
  - Required skills (bullet list).
  - Nice‑to‑have skills (bullet list).
  - ATS keywords (words/phrases that would be in resumes).
  - Standout traits (what would make a candidate truly noticeable).
- Present as a **table**:
  - Column 1: “Area” (e.g., Responsibilities, Skills, Keywords, Traits).
  - Column 2: “Extracted from JD” (short, ATS‑friendly phrases).

---

🎯 STEP 2 — TAILOR THE CV

My CV: [paste CV text]  
Job: [paste job description]

Task:
- Rewrite my CV **for this specific role** without adding false information.
- Keep the same structure:
  - Contact, Summary, Experience, Skills, Education, etc.
- Improve:
  - Professional summary (1–2 sentences, role‑aligned).
  - Bullet points under each role (focus on relevance to this JD).
  - Skills section (reorder, rename, add keywords from Step 1).
- Output: A clean, **ready‑to‑copy CV text** (no markdown, no extra commentary).

---

🎯 STEP 3 — SHARPEN THE BULLETS

Role: [job title]  
Job: [paste job description]  
Bullets: [paste the bullets you want improved]

Task:
- Rewrite each bullet in **action + task + result** format:
  - Action: strong verb (e.g., “Led”, “Built”, “Optimized”).
  - Task: what you actually did.
  - Result: impact; if metric is missing, write [ADD METRIC].
- Do not fabricate numbers; leave placeholders where needed.
- Return:
  - Original bullet.
  - Improved bullet (side‑by‑side or one after the other).

---

🎯 STEP 4 — WRITE THE COVER LETTER

Background: [paste your background / summary]  
Job: [paste job description]

Task:
- Write a **tailored, natural‑sounding cover letter** (no template language).
- Structure:
  - 1 paragraph: hook + why this role / company.
  - 1–2 paragraphs: highlight 2–4 key achievements matched directly to the job’s needs.
  - 1 paragraph: closing (why you, what you bring, call to action).
- Tone: professional but human, not robotic or overly formal.

---

🎯 STEP 5 — BUILD A ROLE‑FIT MATRIX

Background: [paste your background]  
Job: [paste job description]

Task:
- Create a **Role‑Fit Matrix** (table) with:
  - Column 1: “Area from JD” (e.g., “Fraud risk modeling”, “AI/ML”, “project management”).  
  - Column 2: “My Strengths” (how you match).  
  - Column 3: “Gaps” (what’s missing).  
  - Column 4: “CV Focus” (how to emphasize this in the CV).  
  - Column 5: “Cover Letter Angle” (how to frame it in the letter).  
  - Column 6: “Interview Story” (1–2 short story ideas per area).

---

🎯 STEP 6 — FIX ATS ALIGNMENT

CV: [paste CV text]  
Job: [paste job description]

Task:
- Analyze ATS alignment:
  - Missing keywords from the JD.
  - Weak or vague sections.
  - Redundant or fluff content.
- Rewrite:
  - The **professional summary** to better mirror the JD and key ATS terms.
  - A short note explaining what changed and why (2–3 bullet points).

---

🎯 STEP 7 — PREDICT THE INTERVIEW

Background: [paste your background]  
Job: [paste job description]

Task:
- Generate **15 likely interview questions**.
- Group them:
  - 5–7 technical questions.
  - 4–6 behavioral questions.
  - 2–4 culture / values questions.
- For each question, add 1–2 short bullet points of what a good answer should cover (not full answers yet).

---

🎯 STEP 8 — BUILD STAR ANSWERS

Background: [paste your background]  
Job: [paste job description]

Task:
- Create **8 STAR‑formatted answers** (Situation, Task, Action, Result):
  1. Leadership  
  2. Problem‑solving  
  3. Teamwork  
  4. Conflict resolution  
  5. Ownership / accountability  
  6. Failure / mistake  
  7. Achievement / success  
  8. Adaptability / change  
- For each:
  - Use real experiences from your background.
  - If you need to adjust details, keep them truthful and close to reality.
  - Structure clearly with “Situation”, “Task”, “Action”, “Result” headings.

---

🎯 STEP 9 — RECRUITER‑STYLE REVIEW

CV: [paste CV text]  
Cover Letter: [paste cover letter]  
Job: [paste job description]

Task:
- Review everything as if you are a hiring manager.
- Give a verdict:
  - “Shortlist”, “Maybe”, or “Reject” (with a 1‑sentence explanation).
- Then list:
  - Top 3–4 strengths.
  - Top 3–4 weaknesses.
  - 3–5 quick‑fix suggestions (e.g., “add metric X”, “rephrase summary Y”).

---

🎯 STEP 10 — GENERATE THE FULL PACK

Background: [paste your background]  
Job: [paste job description]

Task:
- Assemble a **complete application pack** for this role:
  1. CV summary (1–2 sentences).  
  2. Key skills section (bullet list, ATS‑friendly).  
  3. Cover letter (fresh, tailored).  
  4. List of predicted interview questions (Step 7).  
  5. Recruiter‑style DM / LinkedIn outreach message (short, 3–4 sentences).  
  6. Follow‑up email (after applying / interview).  
- Format as a clean, labeled document (no markdown; use clear section headers).

---

Output format
- Use clear section headers for each step (e.g., “🎯 STEP 1 — DECODE THE JOB DESCRIPTION”).  
- Keep text concise and actionable.  
- Replace [paste] items with the real content you provide.
```




🎯 STEP 11 — JOB TRACKING DATABASE (Google Sheets)

Task:
- Maintain a real-time job application tracking database.
- Link a Google Sheet via Google OAuth 2.0 (Gmail / G-Drive auth).
- Tracked fields:
  - Job Title
  - Company
  - Application Date
  - Status (Applied / Interview / Offer / Rejected / Ghosted)
  - Cold Email Sent to HR on LinkedIn (Yes/No)
  - LinkedIn HR Contact Name
  - Notes
  - Result
  - JD Link
  - Last Updated Timestamp
- Features:
  - Add new applications via form
  - View all applications in an interactive table
  - Duplicate detection (same Job Title + Company)
  - Summary statistics (total, interviews, offers, rejected)
  - Export to CSV
  - Real-time sync with Google Sheets (any change in app reflects in Sheets and vice versa)
- Technology: google-api-python-client, google-auth-oauthlib, pandas


🎯 STEP 12 — STREAMLIT WEB APP (Unified Dashboard)

Task:
- Build a single Streamlit web app (`main_dashboard.py`) that bundles all 12 PDR steps.
- Sidebar tool selector with categorized tools (Analysis, Creation, Strategy, Interview, Review, Tracking, Coach).
- Shared inputs (Resume PDF upload + Job Description text area) across tools.
- Dummy Grok API mode: app works without xAI API key using pre-formatted placeholder responses.
- Google OAuth integration for Step 11 (Job Tracker).
- Features:
  - PDF resume text extraction via PyPDF
  - Grok-4 LLM integration via LangChain (streaming + batch)
  - Downloadable outputs (Markdown files) for all generated content
  - Session-persisted chat history for Career Coach
  - Responsive wide layout with logo branding
- All tools accessible from a single sidebar — no page navigation needed.




