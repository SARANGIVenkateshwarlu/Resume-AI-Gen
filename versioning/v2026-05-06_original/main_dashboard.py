# main_dashboard.py — Resume AI Toolkit (Multi-Provider)
import streamlit as st
import os
import re
import tempfile
import pickle
from PIL import Image

from config import PROVIDER_CONFIG, TOKEN_BUDGETS, STEP_NAMES, CANDIDATE_RULES, INPUT_COST_PER_1M, OUTPUT_COST_PER_1M, GOOGLE_SCOPES, USERNAME, get_job_title
from dummy_data import DUMMY_PREFIX, DUMMY_JD_DECODER, DUMMY_CV_TAILOR, DUMMY_BULLETS, DUMMY_COVER_LETTER, DUMMY_ROLE_FIT, DUMMY_ATS, DUMMY_MATCHER, DUMMY_INTERVIEW_Q, DUMMY_STAR, DUMMY_RECRUITER, DUMMY_FULL_PACKAGE, DUMMY_GENERIC
from utils import extract_resume_text, generate_docx, generate_docx_cover_letter, generate_pdf, estimate_tokens, estimate_cost, create_run_folder, save_run_file, show_folder_summary, cl_filename, cv_filename
from google_module import google_auth, get_or_create_sheet, add_job_application, get_all_applications, check_duplicate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SCOPES = GOOGLE_SCOPES

st.set_page_config(
    page_title="Resume Genie",
    page_icon=":page_facing_up:",
    layout="wide",
    initial_sidebar_state="expanded"
)

logo = Image.open("logo.png")
st.sidebar.image(logo, width=80)
st.sidebar.markdown("**Resume Genie**")

ALL_KEYS = {}
for provider_name, config in PROVIDER_CONFIG.items():
    key_env = config["key_env"]
    key_val = os.getenv(key_env, "")
    if key_val:
        ALL_KEYS[provider_name] = key_val

st.sidebar.markdown("---")
st.sidebar.subheader(":robot_face: LLM Provider")

if ALL_KEYS:
    provider_names = list(ALL_KEYS.keys())
    if "provider" not in st.session_state:
        st.session_state.provider = provider_names[0]
    provider = st.sidebar.selectbox(
        "Provider",
        provider_names,
        index=provider_names.index(st.session_state.provider)
            if st.session_state.provider in provider_names
            else 0,
        key="provider_select"
    )
    st.session_state.provider = provider

    models = PROVIDER_CONFIG[provider]["models"]
    if "model" not in st.session_state:
        st.session_state.model = models[0]
    model = st.sidebar.selectbox(
        "Model",
        models,
        index=models.index(st.session_state.model)
            if st.session_state.model in models
            else 0,
        key="model_select"
    )
    st.session_state.model = model
    st.session_state.api_key = ALL_KEYS[provider]
    st.sidebar.caption(PROVIDER_CONFIG[provider]["desc"])
    DUMMY_MODE = False
else:
    st.sidebar.warning(":warning: No API keys found in `.env`")
    st.sidebar.caption("Running in DUMMY MODE")
    DUMMY_MODE = True


class DummyResponse:
    def __init__(self, content):
        self.content = content


class DummyLLM:
    DUMMY_MAP = {
        "jd_decoder": DUMMY_JD_DECODER,
        "cv_tailor": DUMMY_CV_TAILOR,
        "bullet_sharpener": DUMMY_BULLETS,
        "cover_letter": DUMMY_COVER_LETTER,
        "role_fit_matrix": DUMMY_ROLE_FIT,
        "ats_fixer": DUMMY_ATS,
        "resume_matcher": DUMMY_MATCHER,
        "interview_q": DUMMY_INTERVIEW_Q,
        "star_builder": DUMMY_STAR,
        "recruiter_review": DUMMY_RECRUITER,
        "full_package": DUMMY_FULL_PACKAGE,
    }

    def _get_response(self):
        key = st.session_state.get("current_tool_key", "")
        return self.DUMMY_MAP.get(key, DUMMY_GENERIC)

    def invoke(self, prompt):
        import time
        time.sleep(0.5)
        text = self._get_response()
        return DummyResponse(text)

    def stream(self, prompt):
        import time
        text = self._get_response()
        words = text.split()
        for i in range(0, len(words), 3):
            time.sleep(0.015)
            yield DummyResponse(" ".join(words[:i + 3]))
        yield DummyResponse(text)


@st.cache_resource(show_spinner=":arrows_counterclockwise: Initializing LLM...")
def init_llm(provider_name, model_name, api_key):
    config = PROVIDER_CONFIG[provider_name]
    pkg = config["pkg"]

    if pkg == "langchain_xai":
        from langchain_xai import ChatXAI
        return ChatXAI(
            model=model_name,
            api_key=api_key,
            temperature=0.2,
            max_tokens=4000
        )
    elif pkg == "langchain_openai":
        from langchain_openai import ChatOpenAI
        kwargs = {
            "model": model_name,
            "api_key": api_key,
            "temperature": 0.2,
            "max_tokens": 4000,
        }
        if "base_url" in config:
            kwargs["base_url"] = config["base_url"]
        return ChatOpenAI(**kwargs)
    elif pkg == "langchain_anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model_name,
            api_key=api_key,
            temperature=0.2,
            max_tokens=4000
        )
    else:
        raise ValueError(f"Unsupported package: {pkg}")


if not DUMMY_MODE:
    llm = init_llm(
        st.session_state.provider,
        st.session_state.model,
        st.session_state.api_key
    )
else:
    llm = DummyLLM()

if "completed_steps" not in st.session_state:
    st.session_state.completed_steps = set()
if "shared_jd" not in st.session_state:
    st.session_state.shared_jd = ""
if "shared_resume_text" not in st.session_state:
    st.session_state.shared_resume_text = ""
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0
if "total_calls" not in st.session_state:
    st.session_state.total_calls = 0
if "current_tool_key" not in st.session_state:
    st.session_state.current_tool_key = ""
if "gsheet_service" not in st.session_state:
    st.session_state.gsheet_service = None
if "gsheet_id" not in st.session_state:
    st.session_state.gsheet_id = None
if "career_chat_history" not in st.session_state:
    st.session_state.career_chat_history = []


def mark_step_done(n):
    st.session_state.completed_steps.add(n)


def is_step_done(n):
    return n in st.session_state.completed_steps


DAILY_LIMIT = float(os.getenv("DAILY_LIMIT", "2.00"))

st.sidebar.markdown("---")
st.sidebar.subheader(":moneybag: Budget")
st.sidebar.metric("Session Cost", f"${st.session_state.total_cost:.4f}")
if DAILY_LIMIT > 0:
    pct = min(st.session_state.total_cost / DAILY_LIMIT, 1.0)
    st.sidebar.progress(pct)
    st.sidebar.caption(f"Daily Limit: ${DAILY_LIMIT:.2f}")
st.sidebar.metric("API Calls", st.session_state.total_calls)


def get_llm_with_tokens(max_tokens):
    if DUMMY_MODE:
        return llm
    provider_name = st.session_state.get("provider", "")
    model_name = st.session_state.get("model", "")
    api_key = st.session_state.get("api_key", "")

    config = PROVIDER_CONFIG[provider_name]
    pkg = config["pkg"]

    if pkg == "langchain_xai":
        from langchain_xai import ChatXAI
        return ChatXAI(
            model=model_name,
            api_key=api_key,
            temperature=0.2,
            max_tokens=max_tokens
        )
    elif pkg == "langchain_openai":
        from langchain_openai import ChatOpenAI
        kwargs = {
            "model": model_name,
            "api_key": api_key,
            "temperature": 0.2,
            "max_tokens": max_tokens,
        }
        if "base_url" in config:
            kwargs["base_url"] = config["base_url"]
        return ChatOpenAI(**kwargs)
    elif pkg == "langchain_anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model_name,
            api_key=api_key,
            temperature=0.2,
            max_tokens=max_tokens
        )
    else:
        raise ValueError(f"Unsupported package: {pkg}")


def call_llm(prompt, tool_budget):
    if DUMMY_MODE:
        return llm.invoke(prompt).content

    input_chars = len(prompt)
    response = llm.invoke(prompt)
    output_text = response.content

    output_tokens = estimate_tokens(output_text)
    in_tokens, cost = estimate_cost(input_chars, output_tokens)

    st.session_state.total_cost += cost
    st.session_state.total_calls += 1

    return output_text


def stream_llm(prompt, tool_budget):
    if DUMMY_MODE:
        for chunk in llm.stream(prompt):
            yield chunk.content
        return

    input_chars = len(prompt)
    full_text = ""

    for chunk in llm.stream(prompt):
        c = chunk.content if hasattr(chunk, "content") else str(chunk)
        full_text += c
        yield c

    output_tokens = estimate_tokens(full_text)
    in_tokens, cost = estimate_cost(input_chars, output_tokens)

    st.session_state.total_cost += cost
    st.session_state.total_calls += 1


st.title(":rocket: Resume Genie")
st.markdown(
    "**AI-Powered Resume Toolkit** \u2022 "
    "JD Decoder \u2022 CV Tailor \u2022 Cover Letters \u2022 "
    "ATS Optimization \u2022 Interview Prep \u2022 Career Coaching"
)

st.sidebar.markdown("---")
st.sidebar.subheader(":hammer_and_wrench: Select Tool")

tool = st.sidebar.radio(
    "Choose a service:",
    [
        "0. AUTO-PILOT (Run All Steps)",
        "1. JD Decoder",
        "7. Resume-JD Matcher",
        "Resume Checker (Standalone)",
        "4. Cover Letter",
        "2. CV Tailor",
        "3. Bullet Sharpener",
        "5. Role-Fit Matrix",
        "6. ATS Fixer",
        "8. Interview Q Predictor",
        "9. STAR Builder",
        "10. Recruiter Simulator",
        "11. Full Package",
        "12. Job Tracker",
        "Career Coach Chat",
        "JSON CV Mapper",
    ],
    index=0,
    horizontal=False
)

st.sidebar.markdown("---")
st.sidebar.subheader(":clipboard: Progress")
done_count = len(st.session_state.completed_steps)
st.sidebar.progress(done_count / 12)
st.sidebar.caption(f"{done_count}/12 steps completed")

for step_num in range(1, 13):
    name = STEP_NAMES.get(step_num, f"Step {step_num}")
    done = is_step_done(step_num)
    icon = ":white_check_mark:" if done else ":white_large_square:"
    st.sidebar.markdown(f"{icon} {name}")

st.sidebar.markdown("---")
st.sidebar.caption("**Pro Tip**: Use sidebar to switch tools instantly :zap:")


if tool == "0. AUTO-PILOT (Run All Steps)":
    st.header(":rocket: AUTO-PILOT — Complete 12-Step Workflow")
    st.markdown("Upload everything once. The AI runs all 12 steps automatically. No further input needed.")
    st.markdown("---")

    # ── Collect ALL inputs once ──
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.subheader(":clipboard: Job Description *")
        jd_text = st.text_area("Paste the full job description", height=200, key="auto_jd",
                               value=st.session_state.shared_jd)
        st.session_state.shared_jd = jd_text

    with col_b:
        st.subheader(":page_facing_up: Resume / CV *")
        cv_file = st.file_uploader("Upload CV", type=["pdf","md","txt","typ"], key="auto_cv")
        st.subheader(":pencil: Bullet Points (optional)")
        bullets_text = st.text_area("Paste your resume bullets", height=100, key="auto_bullets",
                                    placeholder="One bullet per line...")

    st.subheader(":love_letter: Cover Letter Draft (optional)")
    cl_draft_text = st.text_area("Paste or edit cover letter text", height=100, key="auto_cl",
                                 value=st.session_state.shared_resume_text,
                                 placeholder="Paste here, or upload a file below...")
    cl_file = st.file_uploader("Or upload Cover Letter file", type=["md","txt","typ","docx"], key="auto_cl_file",
                               help="Upload .md, .txt, .typ or .docx cover letter")
    if cl_file:
        try:
            cl_content = cl_file.getvalue()
            if cl_file.name.endswith('.docx'):
                from docx import Document
                from io import BytesIO
                doc = Document(BytesIO(cl_content))
                cl_draft_text = "\n".join(p.text for p in doc.paragraphs)
            else:
                cl_draft_text = cl_content.decode('utf-8')
            st.success(f"Loaded: {cl_file.name}")
        except Exception:
            st.warning("Could not read file. Please paste text instead.")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        job_title = st.text_input("Job Title (for tracker)", key="auto_title")
    with col_t2:
        company = st.text_input("Company (for tracker)", key="auto_company")

    # ── RUN ALL button ──
    st.markdown("---")
    if st.button(":rocket: RUN ALL 12 STEPS", type="primary", disabled=not (jd_text and cv_file),
                 use_container_width=True):
        cv_text = extract_resume_text(cv_file)
        st.session_state.shared_resume_text = cv_text
        run_folder = create_run_folder(f"AutoPilot_{re.sub(r'[^a-zA-Z0-9_-]','_',jd_text[:40])}")
        all_results = {}
        all_saved = []

        # Progress display
        progress_bar = st.progress(0, text="Starting Auto-Pilot...")
        result_container = st.container()

        # ── Define step runner ──
        def run_step(step_num, budget, prompt_fn, label):
            if DAILY_LIMIT > 0 and st.session_state.total_cost >= DAILY_LIMIT:
                return "Budget limit reached."
            progress_bar.progress(step_num / 12, text=f"Step {step_num}/12: {label}...")
            try:
                p = prompt_fn()
                if step_num in (2, 4, 9, 11):  # streaming steps
                    l = get_llm_with_tokens(TOKEN_BUDGETS.get(budget, 1000))
                    r = ""
                    rc = st.empty()
                    for chunk in l.stream(p):
                        r += chunk.content if hasattr(chunk, 'content') else str(chunk)
                    in_t, cost = estimate_cost(str(p), TOKEN_BUDGETS.get(budget, 1000))
                else:
                    l = get_llm_with_tokens(TOKEN_BUDGETS.get(budget, 1000))
                    resp = l.invoke(p)
                    r = resp.content if hasattr(resp, 'content') else str(resp)
                    in_t, cost = estimate_cost(str(p), TOKEN_BUDGETS.get(budget, 1000))
                st.session_state.total_cost += cost
                st.session_state.total_calls += 1
                progress_bar.progress(step_num / 12, text=f"Step {step_num}/12: {label} done")
                mark_step_done(step_num)
                return r
            except Exception as e:
                return f"Error: {e}"

        # ── Step 1: JD Decoder ──
        r1 = run_step(1, "jd_decoder", lambda: f"""You are a hiring manager. Analyze this job description:
{jd_text}
Return a table: | Area | Extracted from JD |
Rows: Core Responsibilities, Required Skills, Nice-to-Have Skills, ATS Keywords, Standout Traits.""", "JD Decoder")
        all_results["Step 1 - JD Analysis"] = r1
        fn1 = save_run_file(r1, "step1_jd_analysis.md", run_folder)
        all_saved.append(os.path.basename(fn1))

        # ── Step 2: CV Tailor ──
        r2 = run_step(2, "cv_tailor", lambda: f"""{CANDIDATE_RULES}
Rewrite this FULL CV for the job. DO NOT invent facts. Preserve 90% verbatim, 50% flexible on Capstone.
IMPORTANT: Output the COMPLETE CV - include ALL experience roles, ALL bullet points, skills, education, and contact info. Do NOT truncate.
- Rewrite summary to align with JD keywords
- Reorder bullets so JD-matching content appears first
- Rephrase using strong action verbs (Led, Built, Delivered, Architected)
- Add Key Qualifications section at top
- Use [ADD METRIC] where numbers unavailable
Job: {jd_text}
CV: {cv_text}""", "CV Tailor")
        all_results["Step 2 - Tailored CV"] = r2
        fn2 = save_run_file(r2, cv_filename("md", job_title), run_folder)
        all_saved.append(os.path.basename(fn2))
        # Also save docx/pdf for CV
        save_run_file(generate_docx(r2, "CV"), cv_filename("docx", job_title), run_folder)
        save_run_file(generate_pdf(r2, "CV"), cv_filename("pdf", job_title), run_folder)

        # ── Step 3: Bullet Sharpener ──
        btext = bullets_text if bullets_text.strip() else cv_text[:2000]
        r3 = run_step(3, "bullet_sharpener", lambda: f"""Rewrite each bullet in Action+Task+Result format.
Job: {jd_text[:500]}
Bullets: {btext}
Show: Original -> Improved. Use [ADD METRIC] where numbers missing.""", "Bullet Sharpener")
        all_results["Step 3 - Sharpened Bullets"] = r3
        fn3 = save_run_file(r3, "step3_bullets.md", run_folder)
        all_saved.append(os.path.basename(fn3))

        # ── Step 4: Cover Letter ──
        cl_prompt = f"""{CANDIDATE_RULES}
Improve and tailor this cover letter draft for the job. 300-450 words. Do not invent facts.
End with: Sincerely,\\nDr. Venkateshwarlu Sarangi (Ph.D)\\nCityU & HKUST, HK\\nContact: +851-5316757\\nDate: [today]
Job: {jd_text}
Draft: {cl_draft_text}
Background: {cv_text[:2000]}""" if cl_draft_text.strip() else f"""{CANDIDATE_RULES}
Write a 300-450 word cover letter for this job using the resume background.
End with: Sincerely,\\nDr. Venkateshwarlu Sarangi (Ph.D)\\nCityU & HKUST, HK\\nContact: +851-5316757\\nDate: [today]
Job: {jd_text}
Background: {cv_text[:2000]}"""
        r4 = run_step(4, "cover_letter", lambda: cl_prompt, "Cover Letter")
        all_results["Step 4 - Cover Letter"] = r4
        fn4 = save_run_file(r4, cl_filename("md", job_title), run_folder)
        all_saved.append(os.path.basename(fn4))
        save_run_file(generate_docx_cover_letter(r4), cl_filename("docx", job_title), run_folder)
        save_run_file(generate_pdf(r4, "Cover Letter"), cl_filename("pdf", job_title), run_folder)

        # ── Step 5: Role-Fit Matrix ──
        r5 = run_step(5, "role_fit_matrix", lambda: f"""Create a Role-Fit Matrix (6 columns: Area, Strengths, Gaps, CV Focus, CL Angle, Interview Story). 5-7 key areas.
Job: {jd_text}
Candidate: {cv_text}""", "Role-Fit Matrix")
        all_results["Step 5 - Role-Fit Matrix"] = r5
        fn5 = save_run_file(r5, "step5_role_fit.md", run_folder)
        all_saved.append(os.path.basename(fn5))

        # ── Step 6: ATS Fixer ──
        r6 = run_step(6, "ats_fixer", lambda: f"""{CANDIDATE_RULES}
ATS analysis. Return: ---SCORES--- ATS_SCORE: X JD_MATCH_PCT: X VERDICT: X ---DETAILS---
Missing keywords, weak sections, rewritten summary, change-log.
Job: {jd_text}
Resume: {cv_text}""", "ATS Fixer")
        all_results["Step 6 - ATS Analysis"] = r6
        fn6 = save_run_file(r6, "step6_ats_report.md", run_folder)
        all_saved.append(os.path.basename(fn6))

        # ── Step 7: Resume-JD Matcher ──
        r7 = run_step(7, "resume_matcher", lambda: f"""Score this resume against JD. Return: Score X/100, Match X%, Keywords matched, Missing keywords, Readability, ATS score, summary, gaps, suggestions.
Job: {jd_text}
Resume: {cv_text}""", "Resume-JD Matcher")
        all_results["Step 7 - Match Score"] = r7
        fn7 = save_run_file(r7, "step7_match_report.md", run_folder)
        all_saved.append(os.path.basename(fn7))

        # ── Step 8: Interview Q ──
        r8 = run_step(8, "interview_q", lambda: f"""Generate 15 interview questions (7 technical, 5 behavioral, 3 culture) with answer guidance.
Job: {jd_text}
Candidate: {cv_text}""", "Interview Questions")
        all_results["Step 8 - Interview Questions"] = r8
        fn8 = save_run_file(r8, "step8_interview_q.md", run_folder)
        all_saved.append(os.path.basename(fn8))

        # ── Step 9: STAR Builder ──
        r9 = run_step(9, "star_builder", lambda: f"""Build 8 STAR answers (Leadership, Problem-solving, Teamwork, Conflict, Ownership, Failure, Achievement, Adaptability). Use real experiences.
Job: {jd_text}
Background: {cv_text}""", "STAR Builder")
        all_results["Step 9 - STAR Answers"] = r9
        fn9 = save_run_file(r9, "step9_star_answers.md", run_folder)
        all_saved.append(os.path.basename(fn9))

        # ── Step 10: Recruiter Simulator ──
        r10 = run_step(10, "recruiter_review", lambda: f"""Hiring manager review. Return: Verdict (Shortlist/Maybe/Reject), Top 3-4 Strengths, Top 3-4 Weaknesses, 3-5 Quick-Fix Suggestions.
Job: {jd_text}
Resume: {cv_text}
Cover Letter: {r4}""", "Recruiter Review")
        all_results["Step 10 - Recruiter Review"] = r10
        fn10 = save_run_file(r10, "step10_recruiter_review.md", run_folder)
        all_saved.append(os.path.basename(fn10))

        # ── Step 11: Full Package ──
        r11 = run_step(11, "full_package", lambda: f"""{CANDIDATE_RULES}
Assemble complete application package: 1.CV Summary 2.Key Skills 3.Cover Letter 4.Interview Questions 5.LinkedIn DM 6.Follow-up Email.
Job: {jd_text}
Candidate: {cv_text}
Cover Letter: {r4}""", "Full Package")
        all_results["Step 11 - Full Package"] = r11
        fn11 = save_run_file(r11, "step11_full_package.md", run_folder)
        all_saved.append(os.path.basename(fn11))

        # ── Step 12: Complete ──
        progress_bar.progress(1.0, text="All 12 steps complete!")
        mark_step_done(12)

        # ── Display all results ──
        st.markdown("---")
        st.success(f":tada: **Auto-Pilot Complete!** All 12 steps finished.")
        show_folder_summary(run_folder, all_saved)

        st.subheader(":package: Results")
        for title, content in all_results.items():
            with st.expander(title, expanded=False):
                st.markdown(content)

        st.download_button(":floppy_disk: Download Full Report (.md)", r11, "full_application_package.md", use_container_width=True)

    elif not jd_text:
        st.info(":point_up: Paste a Job Description and upload your CV to start the Auto-Pilot.")
    elif not cv_file:
        st.info(":point_up: Upload your CV to start the Auto-Pilot.")


if tool == "1. JD Decoder":
    st.header(":clipboard: JD Decoder")
    st.markdown("Extract structured insights from any job description -- responsibilities, skills, keywords, and more.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the full job description here",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_decoder_jd"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":bulb: What This Does")
        st.markdown("""
        - Extracts **Core Responsibilities**
        - Identifies **Required & Nice-to-Have Skills**
        - Lists **ATS Keywords** for optimization
        - Highlights **Standout Traits** sought
        - Infers **Company/Industry Insights**
        """)

    if st.button(":mag: Decode JD", type="primary", key="btn_jd_decoder"):
        if not job_description:
            st.warning("Please paste a job description first.")
        else:
            with st.spinner("Decoding job description..."):
                st.session_state.current_tool_key = "jd_decoder"

                prompt = (
                    "You are an expert job description analyst. "
                    "Analyze the following job description and extract structured information.\n\n"
                    "Job Description:\n"
                    f"{job_description}\n\n"
                    "Provide a structured analysis with these EXACT sections:\n"
                    "1. **Core Responsibilities** -- list the key responsibilities (bullet points)\n"
                    "2. **Required Skills** -- must-have technical and soft skills (bullet points)\n"
                    "3. **Nice-to-Have Skills** -- preferred or optional skills (bullet points)\n"
                    "4. **ATS Keywords** -- all important keywords for ATS optimization (comma-separated)\n"
                    "5. **Standout Traits** -- what makes a candidate exceptional for this role\n"
                    "6. **Company/Industry Insights** -- inferred from the JD (2-3 sentences)\n\n"
                    "Use clear markdown formatting with headings and bullet points. "
                    "Be comprehensive and extract everything relevant."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["jd_decoder"])
                st.markdown("### :bar_chart: JD Analysis")
                st.markdown(result)

                run_folder = create_run_folder("JD_Decoder")
                save_run_file(result, "jd_decoder.md", run_folder)
                docx_buf = generate_docx(result, "JD Decoder")
                save_run_file(docx_buf, "jd_decoder.docx", run_folder)
                pdf_buf = generate_pdf(result, "JD Decoder")
                save_run_file(pdf_buf, "jd_decoder.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "jd_decoder.md",
                    "jd_decoder.docx",
                    "jd_decoder.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "jd_decoder.md",
                        key="dl_jd_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "jd_decoder.docx",
                        key="dl_jd_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "jd_decoder.pdf",
                        key="dl_jd_pdf"
                    )

                mark_step_done(1)

elif tool == "7. Resume-JD Matcher":
    st.header(":bar_chart: Resume-JD Matcher")
    st.markdown("Score how well your resume matches the job description with detailed gap analysis.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the full job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_matcher"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_matcher"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":chart_with_upwards_trend: Analyze Match", type="primary", key="btn_matcher"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Analyzing match..."):
                st.session_state.current_tool_key = "resume_matcher"

                prompt = (
                    "You are an expert resume evaluator. Score how well the following "
                    "resume matches the job description.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "Provide analysis with this EXACT structure:\n\n"
                    "**Score**: X/100\n"
                    "**Overall Match**: X%\n\n"
                    "Keywords matched: \u2022 ...\n"
                    "Missing keywords: \u2022 ...\n\n"
                    "Readability Score: X/100\n"
                    "ATS Compatibility Score: X/100\n\n"
                    "**Summary**: 2-3 sentence summary\n\n"
                    "**Skill gap analysis**: \u2022 bullet list of gaps\n"
                    "**Improvement suggestions**: \u2022 bullet list of actionable suggestions\n\n"
                    "Be honest and specific. Use markdown formatting."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["resume_matcher"])
                st.markdown("### :bar_chart: Match Analysis")
                st.markdown(result)

                run_folder = create_run_folder("Resume_JD_Matcher")
                save_run_file(result, "resume_jd_matcher.md", run_folder)
                docx_buf = generate_docx(result, "Resume-JD Matcher")
                save_run_file(docx_buf, "resume_jd_matcher.docx", run_folder)
                pdf_buf = generate_pdf(result, "Resume-JD Matcher")
                save_run_file(pdf_buf, "resume_jd_matcher.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "resume_jd_matcher.md",
                    "resume_jd_matcher.docx",
                    "resume_jd_matcher.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "resume_jd_matcher.md",
                        key="dl_matcher_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "resume_jd_matcher.docx",
                        key="dl_matcher_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "resume_jd_matcher.pdf",
                        key="dl_matcher_pdf"
                    )

                mark_step_done(7)


elif tool == "Resume Checker (Standalone)":
    st.header(":mag: Resume Checker (Standalone)")
    st.markdown("Evaluate your resume as a standalone document -- no JD needed. Get format, content, and ATS scores.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":page_facing_up: Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_checker"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    with col2:
        st.subheader(":bulb: What's Checked")
        st.markdown("""
        - **Format & Layout** -- clarity, organization, length
        - **Content Quality** -- action verbs, metrics, bullet strength
        - **ATS Compatibility** -- keyword density, parsing issues
        - **Skills Analysis** -- what's present vs. expected
        - **Career Stage**: Entry / Mid / Senior / Executive
        """)

    if st.button(":pencil: Evaluate Resume", type="primary", key="btn_checker"):
        if not st.session_state.shared_resume_text:
            st.warning("Please upload your resume first.")
        else:
            with st.spinner("Evaluating resume..."):
                st.session_state.current_tool_key = "resume_checker"

                prompt = (
                    "You are an expert resume reviewer. Evaluate the following resume "
                    "as a standalone document (no JD comparison).\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "Provide evaluation with these EXACT sections:\n\n"
                    "**Overall Score**: X/100\n\n"
                    "**Format & Layout**: assessment of clarity, organization, length, visual hierarchy\n\n"
                    "**Content Quality**: bullet strength, action verbs, use of metrics, specificity\n\n"
                    "**ATS Compatibility**: keyword optimization, section headers, potential parsing issues\n\n"
                    "**Strengths**: \u2022 bullet list of what works well\n\n"
                    "**Weaknesses**: \u2022 bullet list of what needs improvement\n\n"
                    "**Skills Analysis**: skills mentioned vs. industry expectations for the candidate's level\n\n"
                    "**Recommended Additions**: skills, certs, or sections to add\n\n"
                    "**Next Career Steps**: 3-4 actionable suggestions based on profile level\n\n"
                    "Use markdown formatting throughout."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["resume_checker"])
                st.markdown("### :clipboard: Resume Evaluation")
                st.markdown(result)

                run_folder = create_run_folder("Resume_Checker")
                save_run_file(result, "resume_checker.md", run_folder)
                docx_buf = generate_docx(result, "Resume Checker")
                save_run_file(docx_buf, "resume_checker.docx", run_folder)
                pdf_buf = generate_pdf(result, "Resume Checker")
                save_run_file(pdf_buf, "resume_checker.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "resume_checker.md",
                    "resume_checker.docx",
                    "resume_checker.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "resume_checker.md",
                        key="dl_chk_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "resume_checker.docx",
                        key="dl_chk_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "resume_checker.pdf",
                        key="dl_chk_pdf"
                    )


elif tool == "4. Cover Letter":
    st.header(":envelope: AI Cover Letter Generator")
    st.markdown("Generate a tailored cover letter matching your resume to the job description.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.shared_jd,
            height=250,
            key="jd_cover"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":pencil: Additional Background")
        background = st.text_area(
            "Resume text (pre-loaded) -- add any extra context below",
            value=st.session_state.shared_resume_text,
            height=250,
            key="bg_cover"
        )

    if st.button(":sparkles: Generate Cover Letter", type="primary", key="btn_cover"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume first using another tool (e.g., CV Tailor or Resume Checker).")
        else:
            with st.spinner("Generating cover letter..."):
                st.session_state.current_tool_key = "cover_letter"

                prompt = (
                    f"{CANDIDATE_RULES}\n\n"
                    "You are a professional cover letter writer. Write a compelling, "
                    "tailored cover letter for the following job application.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Candidate's Background:\n{st.session_state.shared_resume_text}\n\n"
                    f"Additional Context:\n{background}\n\n"
                    "Requirements:\n"
                    "- 300-450 words\n"
                    "- Professional but conversational tone\n"
                    "- Standard business letter format with date, salutation, body, closing\n"
                    "- Opening paragraph: express genuine enthusiasm and summarize fit in 1 sentence\n"
                    "- Body paragraph 1: match top 2-3 JD requirements to specific experience from resume\n"
                    "- Body paragraph 2: highlight additional relevant strengths and achievements\n"
                    "- Closing paragraph: call to action, thank the reader, express interest in interviewing\n"
                    "- NEVER invent facts, company names, job titles, or metrics -- use only information from the resume\n"
                    "- Address the hiring manager by name if available, otherwise use \"Hiring Team\"\n"
                    "- End with this exact signature block:\n"
                    "  Sincerely,\n"
                    "  Dr. Venkateshwarlu Sarangi (Ph.D)\n"
                    "  CityU & HKUST, HK\n"
                    "  Contact: +851-5316757\n"
                    "  Date: [current date]\n\n"
                    "Output in clean markdown format."
                )

                full_text = ""
                placeholder = st.empty()
                for chunk in stream_llm(prompt, TOKEN_BUDGETS["cover_letter"]):
                    full_text += chunk
                    placeholder.markdown(full_text + "\u258c")
                placeholder.markdown(full_text)

                run_folder = create_run_folder("Cover_Letter")
                job_title = get_job_title(job_description)
                save_run_file(full_text, cl_filename("md", job_title), run_folder)
                docx_buf = generate_docx_cover_letter(full_text)
                save_run_file(docx_buf, cl_filename("docx", job_title), run_folder)
                pdf_buf = generate_pdf(full_text, "Cover Letter")
                save_run_file(pdf_buf, cl_filename("pdf", job_title), run_folder)
                show_folder_summary(run_folder, [
                    cl_filename("md", job_title),
                    cl_filename("docx", job_title),
                    cl_filename("pdf", job_title)
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        full_text,
                        cl_filename("md", job_title),
                        key="dl_cl_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        cl_filename("docx", job_title),
                        key="dl_cl_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        cl_filename("pdf", job_title),
                        key="dl_cl_pdf"
                    )

                mark_step_done(4)


elif tool == "2. CV Tailor":
    st.header(":page_facing_up: CV Tailor")
    st.markdown("Rewrite and optimize your CV/resume to match the target job description while preserving your real experience.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the target job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_cv"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_cv"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":hammer: Tailor CV", type="primary", key="btn_cv"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Tailoring your CV..."):
                st.session_state.current_tool_key = "cv_tailor"

                prompt = (
                    f"{CANDIDATE_RULES}\n\n"
                    "You are an expert CV writer and career coach. Tailor the following "
                    "resume/CV to match the job description below. PRESERVE the candidate's "
                    "real experience -- only adjust wording for relevance and impact.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "Instructions:\n"
                    "1. Rewrite the professional summary to align with JD keywords (use exact phrases from JD)\n"
                    "2. Reorder experience bullets so JD-matching content appears first\n"
                    "3. Rephrase bullets to use strong action verbs and include JD keywords naturally\n"
                    "4. Update the skills section -- prioritize JD-matching skills, then add related skills\n"
                    "5. Add a \"Key Qualifications\" or \"Core Competencies\" section at the top\n"
                    "6. Maintain 90% of the original resume content -- only adjust for relevance and impact\n"
                    "7. Use strong action verbs (Led, Built, Delivered, Architected, Optimized, etc.)\n"
                    "8. Add [ADD METRIC] placeholders where specific numbers are unavailable\n"
                    "9. NEVER invent new projects, company names, job titles, or metrics\n"
                    "10. IMPORTANT: Output the COMPLETE and FULL CV -- include ALL experience roles, "
                    "ALL bullet points, skills, education, and contact info. Do NOT truncate any section.\n\n"
                    "Output the full tailored CV in clean markdown format with clear section headings."
                )

                full_text = ""
                placeholder = st.empty()
                for chunk in stream_llm(prompt, TOKEN_BUDGETS["cv_tailor"]):
                    full_text += chunk
                    placeholder.markdown(full_text + "\u258c")
                placeholder.markdown(full_text)

                run_folder = create_run_folder("CV_Tailor")
                job_title = get_job_title(job_description)
                save_run_file(full_text, cv_filename("md", job_title), run_folder)
                docx_buf = generate_docx(full_text, "CV Tailor")
                save_run_file(docx_buf, cv_filename("docx", job_title), run_folder)
                pdf_buf = generate_pdf(full_text, "CV Tailor")
                save_run_file(pdf_buf, cv_filename("pdf", job_title), run_folder)
                show_folder_summary(run_folder, [
                    "cv_tailor.md",
                    "cv_tailor.docx",
                    "cv_tailor.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        full_text,
                        "cv_tailor.md",
                        key="dl_cv_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "cv_tailor.docx",
                        key="dl_cv_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "cv_tailor.pdf",
                        key="dl_cv_pdf"
                    )

                mark_step_done(2)


elif tool == "3. Bullet Sharpener":
    st.header(":mortar_board: Bullet Sharpener")
    st.markdown("Transform weak resume bullets into powerful ATR (Action-Task-Result) format that recruiters love.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description (for context)")
        job_description = st.text_area(
            "Paste job description for keyword alignment",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_bullet"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_bullet"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":sparkles: Sharpen Bullets", type="primary", key="btn_bullet"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Sharpening bullets..."):
                st.session_state.current_tool_key = "bullet_sharpener"

                prompt = (
                    "You are an expert resume bullet writer. Convert weak or generic resume bullets "
                    "into powerful ATR (Action-Task-Result) format bullets. Use the job description "
                    "to align keywords and priorities.\n\n"
                    f"Job Description (for context):\n{job_description}\n\n"
                    f"Resume (extract all experience bullets):\n{st.session_state.shared_resume_text}\n\n"
                    "For each original bullet found in the resume, provide:\n"
                    "- The original bullet text\n"
                    "- An improved ATR version with: strong Action verb, specific Task/deliverable, "
                    "quantified Result or [ADD METRIC] placeholder\n\n"
                    "Format as a markdown table with two columns:\n"
                    "| Original | Improved (ATR Format) |\n"
                    "|---|---|\n\n"
                    "Rules:\n"
                    "- Every improved bullet MUST start with a strong action verb "
                    "(Led, Built, Delivered, Architected, Optimized, Reduced, Launched, etc.)\n"
                    "- Include real numbers/metrics from the resume where available\n"
                    "- Use [ADD METRIC] placeholders when specific numbers are unknown\n"
                    "- Align bullets with JD keywords naturally\n"
                    "- Maximum 15 bullet pairs\n"
                    "- NEVER invent achievements -- only improve existing content\n\n"
                    "After the table, add a short summary of key improvements made."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["bullet_sharpener"])
                st.markdown("### :clipboard: Sharpened Bullets")
                st.markdown(result)

                run_folder = create_run_folder("Bullet_Sharpener")
                save_run_file(result, "bullet_sharpener.md", run_folder)
                docx_buf = generate_docx(result, "Bullet Sharpener")
                save_run_file(docx_buf, "bullet_sharpener.docx", run_folder)
                pdf_buf = generate_pdf(result, "Bullet Sharpener")
                save_run_file(pdf_buf, "bullet_sharpener.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "bullet_sharpener.md",
                    "bullet_sharpener.docx",
                    "bullet_sharpener.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "bullet_sharpener.md",
                        key="dl_bs_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "bullet_sharpener.docx",
                        key="dl_bs_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "bullet_sharpener.pdf",
                        key="dl_bs_pdf"
                    )

                mark_step_done(3)

elif tool == "5. Role-Fit Matrix":
    st.header(":jigsaw: Role-Fit Matrix")
    st.markdown("Map your strengths and gaps against each JD requirement with a strategic action plan.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_rolefit"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_rolefit"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":jigsaw: Analyze Fit", type="primary", key="btn_rolefit"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Building role-fit matrix..."):
                st.session_state.current_tool_key = "role_fit_matrix"

                prompt = (
                    "You are a career strategist. Analyze how well the candidate's resume "
                    "fits the job description and create a role-fit matrix.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "Create a markdown table with exactly 6 columns:\n"
                    "| JD Requirement Area | My Strengths | Gaps | CV Focus | "
                    "Cover Letter Angle | Interview Story |\n"
                    "|---|---|---|---|---|---|\n\n"
                    "Each row should cover one key JD requirement area. Be specific and honest.\n\n"
                    "Also provide:\n"
                    "- **Overall Fit Score**: X% (estimate based on match)\n"
                    "- **Top 3 Strengths**: bullet list of most relevant experiences\n"
                    "- **Top 3 Gaps to Address**: bullet list of what's missing or weak\n"
                    "- **Recommended Strategy**: 2-3 sentences on how to position yourself\n\n"
                    "Use markdown formatting throughout. Be detailed and actionable."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["role_fit_matrix"])
                st.markdown("### :jigsaw: Role-Fit Analysis")
                st.markdown(result)

                run_folder = create_run_folder("Role_Fit_Matrix")
                save_run_file(result, "role_fit_matrix.md", run_folder)
                docx_buf = generate_docx(result, "Role-Fit Matrix")
                save_run_file(docx_buf, "role_fit_matrix.docx", run_folder)
                pdf_buf = generate_pdf(result, "Role-Fit Matrix")
                save_run_file(pdf_buf, "role_fit_matrix.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "role_fit_matrix.md",
                    "role_fit_matrix.docx",
                    "role_fit_matrix.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "role_fit_matrix.md",
                        key="dl_rf_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "role_fit_matrix.docx",
                        key="dl_rf_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "role_fit_matrix.pdf",
                        key="dl_rf_pdf"
                    )

                mark_step_done(5)


elif tool == "6. ATS Fixer":
    st.header(":robot_face: ATS Fixer")
    st.markdown("Score your resume against ATS algorithms and get a fix-it plan to boost compatibility.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_ats"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_ats"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":robot_face: Run ATS Check", type="primary", key="btn_ats"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Running ATS analysis..."):
                st.session_state.current_tool_key = "ats_fixer"

                prompt = (
                    f"{CANDIDATE_RULES}\n\n"
                    "You are an ATS (Applicant Tracking System) optimization expert. "
                    "Analyze the resume against the job description and provide an "
                    "ATS compatibility report.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "First, output these three values on separate lines EXACTLY as shown:\n"
                    "---SCORES---\n"
                    "ATS_SCORE: [0-100]\n"
                    "JD_MATCH_PCT: [0-100]\n"
                    "VERDICT: [STRONG MATCH / GOOD MATCH / NEEDS WORK / WEAK MATCH]\n"
                    "---DETAILS---\n\n"
                    "Then provide a detailed report with:\n"
                    "1. **Missing Keywords** -- keywords from JD not found in resume\n"
                    "2. **Weak/Vague Sections** -- areas that need strengthening\n"
                    "3. **Redundant Content** -- overused phrases or repeated content\n"
                    "4. **Rewritten Professional Summary** -- JD-aligned version (2-3 sentences)\n"
                    "5. **Change-Log** -- bullet list of ALL recommended changes\n\n"
                    "Use markdown formatting throughout. Be thorough and specific."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["ats_fixer"])

                score_match = re.search(r'ATS_SCORE:\s*(\d+)', result)
                jd_match = re.search(r'JD_MATCH_PCT:\s*(\d+)', result)
                verdict_match = re.search(r'VERDICT:\s*(.+)', result)

                if score_match and jd_match:
                    ats_score = int(score_match.group(1))
                    jd_pct = int(jd_match.group(1))
                    verdict = verdict_match.group(1).strip() if verdict_match else "N/A"

                    st.markdown("### :bar_chart: ATS Dashboard")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("ATS Score", f"{ats_score}/100")
                    with col_m2:
                        st.metric("JD Match", f"{jd_pct}%")
                    with col_m3:
                        st.metric("Verdict", verdict)

                st.markdown("### :clipboard: Full ATS Report")
                st.markdown(result)

                run_folder = create_run_folder("ATS_Fixer")
                save_run_file(result, "ats_fixer.md", run_folder)
                docx_buf = generate_docx(result, "ATS Fixer")
                save_run_file(docx_buf, "ats_fixer.docx", run_folder)
                pdf_buf = generate_pdf(result, "ATS Fixer")
                save_run_file(pdf_buf, "ats_fixer.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "ats_fixer.md",
                    "ats_fixer.docx",
                    "ats_fixer.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "ats_fixer.md",
                        key="dl_ats_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "ats_fixer.docx",
                        key="dl_ats_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "ats_fixer.pdf",
                        key="dl_ats_pdf"
                    )

                mark_step_done(6)


elif tool == "8. Interview Q Predictor":
    st.header(":microphone: Interview Q Predictor")
    st.markdown("Predict the most likely interview questions based on the JD and your resume profile.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_iq"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_iq"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":microphone: Predict Questions", type="primary", key="btn_iq"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Predicting interview questions..."):
                st.session_state.current_tool_key = "interview_q"

                prompt = (
                    "You are an expert technical recruiter and interview coach. "
                    "Based on the job description and candidate resume, predict the most "
                    "likely interview questions.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Resume (for context on candidate's profile):\n{st.session_state.shared_resume_text}\n\n"
                    "Provide questions organized by category:\n\n"
                    "1. **Technical Questions** (7-10) -- based on JD requirements and any gaps in the resume\n"
                    "   - For each: note what skill/knowledge the interviewer is testing\n\n"
                    "2. **Behavioral Questions** (5-7) -- STAR-format friendly, based on the role's challenges\n"
                    "   - For each: suggest which experience from the resume could be used to answer\n\n"
                    "3. **Culture Fit Questions** (3-5) -- based on company/industry inferred from JD\n"
                    "   - For each: note what value/cultural trait is being assessed\n\n"
                    "4. **Role-Specific Questions** (3-5) -- deep-dive on the core responsibilities\n"
                    "   - For each: what the interviewer wants to hear\n\n"
                    "Use clear markdown formatting with headings and bullet points."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["interview_q"])
                st.markdown("### :microphone: Predicted Interview Questions")
                st.markdown(result)

                run_folder = create_run_folder("Interview_Q")
                save_run_file(result, "interview_q.md", run_folder)
                docx_buf = generate_docx(result, "Interview Q Predictor")
                save_run_file(docx_buf, "interview_q.docx", run_folder)
                pdf_buf = generate_pdf(result, "Interview Q Predictor")
                save_run_file(pdf_buf, "interview_q.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "interview_q.md",
                    "interview_q.docx",
                    "interview_q.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "interview_q.md",
                        key="dl_iq_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "interview_q.docx",
                        key="dl_iq_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "interview_q.pdf",
                        key="dl_iq_pdf"
                    )

                mark_step_done(8)

elif tool == "9. STAR Builder":
    st.header(":star: STAR Builder")
    st.markdown("Build complete STAR (Situation-Task-Action-Result) stories from your experience for the 8 most common behavioral interview categories.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description (for context)")
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_star"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_star"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":star: Build STAR Stories", type="primary", key="btn_star"):
        if not job_description:
            st.warning("Please paste a job description for context.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Building STAR stories..."):
                st.session_state.current_tool_key = "star_builder"

                prompt = (
                    "You are an expert interview coach. Based on the candidate's resume "
                    "and target job, create STAR (Situation-Task-Action-Result) stories for "
                    "the 8 most common behavioral interview categories.\n\n"
                    f"Job Description (for context):\n{job_description}\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "Create a detailed STAR story for each category:\n\n"
                    "1. **Leadership** -- leading a team or initiative\n"
                    "2. **Problem-Solving** -- overcoming a complex technical challenge\n"
                    "3. **Teamwork** -- collaborating effectively across functions\n"
                    "4. **Conflict Resolution** -- handling disagreement or misalignment\n"
                    "5. **Ownership/Accountability** -- taking responsibility for outcomes\n"
                    "6. **Failure/Mistake** -- learning from an error or setback\n"
                    "7. **Achievement/Success** -- proudest professional accomplishment\n"
                    "8. **Adaptability/Change** -- handling ambiguity or rapid change\n\n"
                    "For each story, use this exact structure:\n"
                    "- **Situation**: [1-2 sentences setting the context from resume]\n"
                    "- **Task**: [1 sentence on what needed to be accomplished]\n"
                    "- **Action**: [3-4 specific steps taken, always using \"I\" statements]\n"
                    "- **Result**: [quantified outcome or [ADD METRIC] if numbers unavailable]\n"
                    "- **Key Takeaway**: [1 sentence on the lesson or skill demonstrated]\n\n"
                    "Use real experiences from the resume. If specific details are missing, "
                    "use reasonable inferences based on the candidate's profile. "
                    "Mark inferred details with [INFERRED]. NEVER invent major achievements "
                    "or job titles. Target each story to be 2-3 minutes when spoken aloud.\n\n"
                    "Output in clean markdown with clear headings."
                )

                full_text = ""
                placeholder = st.empty()
                for chunk in stream_llm(prompt, TOKEN_BUDGETS["star_builder"]):
                    full_text += chunk
                    placeholder.markdown(full_text + "\u258c")
                placeholder.markdown(full_text)

                run_folder = create_run_folder("STAR_Builder")
                save_run_file(full_text, "star_builder.md", run_folder)
                docx_buf = generate_docx(full_text, "STAR Builder")
                save_run_file(docx_buf, "star_builder.docx", run_folder)
                pdf_buf = generate_pdf(full_text, "STAR Builder")
                save_run_file(pdf_buf, "star_builder.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "star_builder.md",
                    "star_builder.docx",
                    "star_builder.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        full_text,
                        "star_builder.md",
                        key="dl_star_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "star_builder.docx",
                        key="dl_star_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "star_builder.pdf",
                        key="dl_star_pdf"
                    )

                mark_step_done(9)


elif tool == "10. Recruiter Simulator":
    st.header(":bust_in_silhouette: Recruiter Simulator")
    st.markdown("Get an honest recruiter-style review of how your application stacks up against the competition.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_recruiter"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_recruiter"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":bust_in_silhouette: Simulate Review", type="primary", key="btn_recruiter"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Running recruiter simulation..."):
                st.session_state.current_tool_key = "recruiter_review"

                prompt = (
                    "You are a senior technical recruiter reviewing a candidate's application. "
                    "Provide an honest, constructive review of how this resume stacks up against "
                    "the job description.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "Provide:\n"
                    "1. **Verdict**: [SHORTLIST / MAYBE / PASS] with 1-sentence explanation\n"
                    "2. **Top 3 Strengths** -- what stands out compared to other applicants\n"
                    "3. **Top 3 Weaknesses** -- what hurts the application the most\n"
                    "4. **Competitive Analysis** -- how this candidate compares to typical applicants (2-3 sentences)\n"
                    "5. **Quick-Fix Suggestions** -- 5 things to improve in < 30 minutes each\n"
                    "6. **Red Flags** (if any) -- anything that might concern a recruiter or hiring manager\n\n"
                    "Be direct, recruiter-style honest. No sugarcoating. Use markdown formatting."
                )

                result = call_llm(prompt, TOKEN_BUDGETS["recruiter_review"])
                st.markdown("### :bust_in_silhouette: Recruiter Review")
                st.markdown(result)

                run_folder = create_run_folder("Recruiter_Simulator")
                save_run_file(result, "recruiter_review.md", run_folder)
                docx_buf = generate_docx(result, "Recruiter Review")
                save_run_file(docx_buf, "recruiter_review.docx", run_folder)
                pdf_buf = generate_pdf(result, "Recruiter Review")
                save_run_file(pdf_buf, "recruiter_review.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "recruiter_review.md",
                    "recruiter_review.docx",
                    "recruiter_review.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        result,
                        "recruiter_review.md",
                        key="dl_recr_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "recruiter_review.docx",
                        key="dl_recr_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "recruiter_review.pdf",
                        key="dl_recr_pdf"
                    )

                mark_step_done(10)


elif tool == "11. Full Package":
    st.header(":package: Full Application Package")
    st.markdown("Generate a complete job application package: CV summary, cover letter, interview prep, outreach messages, and more.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":clipboard: Job Description")
        job_description = st.text_area(
            "Paste the job description",
            value=st.session_state.shared_jd,
            height=300,
            key="jd_full"
        )
        st.session_state.shared_jd = job_description

    with col2:
        st.subheader(":page_facing_up: Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "md", "txt", "typ"],
            key="resume_full"
        )
        if uploaded_file:
            resume_text = extract_resume_text(uploaded_file)
            st.session_state.shared_resume_text = resume_text
            st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if st.button(":package: Generate Full Package", type="primary", key="btn_full"):
        if not job_description:
            st.warning("Please paste a job description.")
        elif not st.session_state.shared_resume_text:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Generating full application package..."):
                st.session_state.current_tool_key = "full_package"

                prompt = (
                    f"{CANDIDATE_RULES}\n\n"
                    "You are an AI career assistant. Generate a COMPLETE application "
                    "package for the following job.\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    f"Resume:\n{st.session_state.shared_resume_text}\n\n"
                    "Generate ALL of the following sections:\n\n"
                    "1. **CV SUMMARY** -- 3-4 line professional summary tailored to JD\n"
                    "2. **KEY SKILLS** -- comma-separated list of 12-15 JD-aligned skills\n"
                    "3. **COVER LETTER** -- 300-400 words tailored cover letter\n"
                    "4. **PREDICTED INTERVIEW QUESTIONS** -- 5 technical + 3 behavioral + 2 culture fit\n"
                    "5. **LINKEDIN OUTREACH DM** -- short message (3-4 sentences) to send to HR/recruiter\n"
                    "6. **FOLLOW-UP EMAIL** -- email template for 1 week after application\n"
                    "7. **SALARY NEGOTIATION TIPS** -- 3-4 tips based on role/industry/level\n"
                    "8. **PORTFOLIO/PROJECT HIGHLIGHTS** -- 3 projects from resume to emphasize with JD context\n\n"
                    "Output in comprehensive markdown format with clear headings. "
                    "Make every section detailed and immediately usable."
                )

                full_text = ""
                placeholder = st.empty()
                for chunk in stream_llm(prompt, TOKEN_BUDGETS["full_package"]):
                    full_text += chunk
                    placeholder.markdown(full_text + "\u258c")
                placeholder.markdown(full_text)

                run_folder = create_run_folder("Full_Package")
                save_run_file(full_text, "full_package.md", run_folder)
                docx_buf = generate_docx(full_text, "Full Package")
                save_run_file(docx_buf, "full_package.docx", run_folder)
                pdf_buf = generate_pdf(full_text, "Full Package")
                save_run_file(pdf_buf, "full_package.pdf", run_folder)
                show_folder_summary(run_folder, [
                    "full_package.md",
                    "full_package.docx",
                    "full_package.pdf"
                ])

                col_dl1, col_dl2, col_dl3 = st.columns(3)
                with col_dl1:
                    st.download_button(
                        ":floppy_disk: Download .md",
                        full_text,
                        "full_package.md",
                        key="dl_fp_md"
                    )
                with col_dl2:
                    st.download_button(
                        ":floppy_disk: Download .docx",
                        docx_buf,
                        "full_package.docx",
                        key="dl_fp_docx"
                    )
                with col_dl3:
                    st.download_button(
                        ":floppy_disk: Download .pdf",
                        pdf_buf,
                        "full_package.pdf",
                        key="dl_fp_pdf"
                    )

                mark_step_done(11)

elif tool == "12. Job Tracker":
    st.header(":ledger: Job Tracker (Google Sheets)")
    st.markdown("Track your job applications in Google Sheets. Connect with a service account JSON and log every application.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(":key: Google Sheets Setup")
        st.markdown("""
        1. Create a Google Cloud project
        2. Enable Google Sheets API
        3. Create a Service Account
        4. Download the JSON key
        5. Share your sheet with the service account email
        """)

        creds_file = st.file_uploader(
            "Upload Google Service Account JSON",
            type=["json"],
            key="gsheets_creds"
        )

        if creds_file and st.button(":link: Connect to Google Sheets", key="btn_connect_gs"):
            with st.spinner("Connecting to Google Sheets..."):
                try:
                    credentials_json = creds_file.read().decode("utf-8")
                    service = google_auth(credentials_json)
                    if service:
                        sheet_id = get_or_create_sheet(service)
                        st.session_state.gsheet_service = service
                        st.session_state.gsheet_id = sheet_id
                        st.success(f":white_check_mark: Connected! Sheet ID: `{sheet_id}`")
                        st.info("Share this sheet with your service account email for viewing.")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

    with col2:
        st.subheader(":pencil: Add Application")
        if st.session_state.gsheet_service and st.session_state.gsheet_id:
            default_title = ""
            if st.session_state.shared_jd:
                lines = st.session_state.shared_jd.strip().split("\n")
                if lines:
                    default_title = lines[0][:80]

            job_title = st.text_input("Job Title", value=default_title, key="gs_job_title")
            company = st.text_input("Company", key="gs_company")
            app_date = st.date_input("Application Date", key="gs_date")
            status = st.selectbox(
                "Status",
                ["Applied", "Phone Screen", "Interview", "Onsite", "Offer", "Rejected", "Withdrawn"],
                key="gs_status"
            )
            cold_email = st.selectbox("Cold Email Sent?", ["No", "Yes"], key="gs_cold")
            linkedin_hr = st.text_input("LinkedIn HR Contact", key="gs_hr")
            jd_link = st.text_input("JD Link (URL)", key="gs_jdlink")
            notes = st.text_area("Notes", height=80, key="gs_notes")

            if st.button(":heavy_plus_sign: Add Application", type="primary", key="btn_add_gs"):
                if not job_title or not company:
                    st.warning("Job Title and Company are required.")
                else:
                    service = st.session_state.gsheet_service
                    sheet_id = st.session_state.gsheet_id

                    df = get_all_applications(service, sheet_id)
                    if check_duplicate(df, job_title, company):
                        st.warning(f":warning: Duplicate: `{job_title}` at `{company}` already exists.")
                    else:
                        data = {
                            "job_title": job_title,
                            "company": company,
                            "app_date": app_date.strftime("%Y-%m-%d"),
                            "status": status,
                            "cold_email": cold_email,
                            "linkedin_hr": linkedin_hr,
                            "notes": notes,
                            "result": "",
                            "jd_link": jd_link,
                        }
                        if add_job_application(service, sheet_id, data):
                            st.success(f":white_check_mark: `{job_title}` at `{company}` added!")
                            st.balloons()
                            mark_step_done(12)
        else:
            st.info(":arrow_left: Upload a service account JSON and click Connect first.")

    st.markdown("---")
    st.subheader(":bar_chart: Your Applications")

    if st.session_state.gsheet_service and st.session_state.gsheet_id:
        if st.button(":arrows_counterclockwise: Refresh Applications", key="btn_refresh_gs"):
            with st.spinner("Loading applications..."):
                df = get_all_applications(
                    st.session_state.gsheet_service,
                    st.session_state.gsheet_id
                )
                st.session_state.gsheet_df = df

        if "gsheet_df" in st.session_state and not st.session_state.gsheet_df.empty:
            st.dataframe(st.session_state.gsheet_df, use_container_width=True)
            st.caption(f"{len(st.session_state.gsheet_df)} applications tracked")
        elif "gsheet_df" in st.session_state:
            st.info("No applications added yet. Use the form on the left.")
        else:
            if st.button(":mag: Load Applications", key="btn_load_gs"):
                with st.spinner("Loading applications..."):
                    df = get_all_applications(
                        st.session_state.gsheet_service,
                        st.session_state.gsheet_id
                    )
                    st.session_state.gsheet_df = df
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No applications added yet.")
    else:
        st.info("Connect to Google Sheets first to view applications.")


elif tool == "Career Coach Chat":
    st.header(":speech_balloon: Career Coach Chat")
    st.markdown("Upload your resume and chat with an AI career coach for personalized advice.")

    uploaded_file = st.file_uploader(
        "Upload Resume to start",
        type=["pdf", "md", "txt", "typ"],
        key="chat_resume"
    )
    if uploaded_file:
        resume_text = extract_resume_text(uploaded_file)
        st.session_state.shared_resume_text = resume_text
        st.success(f":white_check_mark: Resume loaded ({len(resume_text):,} chars)")

    if not st.session_state.shared_resume_text:
        st.warning(":point_up: Upload your resume to start chatting!")
        st.stop()

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader(":page_facing_up: Your Resume")
        with st.expander("View full text", expanded=True):
            st.text_area(
                "",
                st.session_state.shared_resume_text,
                height=450,
                disabled=True,
                key="chat_resume_view"
            )

    with right_col:
        st.subheader(":robot_face: Career Coach")

        for msg in st.session_state.career_chat_history:
            role = msg["role"]
            with st.chat_message(role):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask about career, resume improvements, interviews..."):
            st.session_state.career_chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                chat_llm = get_llm_with_tokens(TOKEN_BUDGETS["career_coach"])

                system_prompt = (
                    "You are an expert career coach with deep knowledge of tech industry hiring. "
                    "You have full access to the candidate's resume below. Provide specific, "
                    "personalized advice referencing their actual experience.\n\n"
                    f"CANDIDATE RESUME:\n{st.session_state.shared_resume_text}\n\n"
                    "Guidelines:\n"
                    "- Reference specific experiences from the resume\n"
                    "- Be encouraging but honest\n"
                    "- Give actionable advice, not generic platitudes\n"
                    "- Suggest concrete next steps\n"
                    "- Keep responses focused and practical (2-4 paragraphs max)\n"
                    "- If asked about salary, provide market ranges based on role/industry\n"
                    "- If asked about skill gaps, suggest specific courses/certifications"
                )

                messages = [SystemMessage(content=system_prompt)]
                for msg in st.session_state.career_chat_history:
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    else:
                        messages.append(AIMessage(content=msg["content"]))

                full_text = ""
                placeholder = st.empty()
                try:
                    for chunk in chat_llm.stream(messages):
                        c = chunk.content if hasattr(chunk, "content") else str(chunk)
                        full_text += c
                        placeholder.markdown(full_text + "\u258c")
                except Exception as e:
                    full_text = f"Error: {e}"
                placeholder.markdown(full_text)

                st.session_state.career_chat_history.append(
                    {"role": "assistant", "content": full_text}
                )

                if not DUMMY_MODE:
                    input_chars = sum(len(str(m.content)) for m in messages)
                    output_tokens = estimate_tokens(full_text)
                    in_tokens, cost = estimate_cost(input_chars, output_tokens)
                    st.session_state.total_cost += cost
                    st.session_state.total_calls += 1


elif tool == "JSON CV Mapper":
    st.header(":page_with_curl: JSON CV Mapper — Structured Resume Generator")
    st.markdown("Convert raw CV/resume text into structured JSON for automated PDF rendering (react-pdf / ReportLab).")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader(":pencil: Raw CV / Resume Text")
        cv_raw = st.text_area("Paste your CV or resume text", value=st.session_state.shared_resume_text,
                              height=300, key="json_cv_raw",
                              placeholder="Name: ...\nContact: ...\nExperience:\n- ...\nEducation:\n- ...")
        st.session_state.shared_resume_text = cv_raw

        st.subheader(":art: Template Style")
        template_style = st.selectbox("Choose layout style:", [
            "Modern two-column (ATS-friendly)",
            "Minimalist single-page",
            "Academic with publications",
            "Tech/startup bold",
            "Classic professional",
        ], key="json_style")

    with col2:
        st.subheader(":wrench: Extra Context")
        extra_context = st.text_area("Additional instructions (optional)", height=100, key="json_extra",
                                     placeholder="e.g. Include 3 most relevant publications, hide GPA...")

        st.subheader(":memo: Custom Sections")
        custom_sections = st.text_area("Custom sections to include (comma-separated)", height=80, key="json_sections",
                                       placeholder="e.g. patents, awards, languages, volunteer")

    if st.button(":gear: Generate Structured JSON", type="primary", key="btn_json_cv",
                 disabled=not cv_raw.strip()):
        with st.spinner("Mapping CV to structured JSON..."):
            sections_instruction = ""
            if custom_sections.strip():
                sections_instruction = f"Also include these custom sections: {custom_sections}"

            prompt = f"""You are an expert technical writer and automated document generation engineer.
Convert the following professional experience into a clean, structured JSON format suitable for automated PDF rendering.

Template style: {template_style}
{sections_instruction}

Requirements:
- Map ALL name-entities (Name, Contact, Dates, Skills, Companies) to specific keys
- Keep text professional, concise, and ATS-friendly
- Output ONLY valid JSON (no markdown, no explanation)
- Use consistent key naming (snake_case)

JSON structure should include these top-level keys (adapt based on available data):
- header: {{ name, title, email, phone, linkedin, location }}
- summary: string (2-3 lines)
- experience: array of {{ title, company, dates, highlights: [string, ...] }}
- skills: {{ languages: [], frameworks: [], tools: [], domains: [] }}
- education: array of {{ degree, school, year }}
- Optionally: publications, certifications, awards, languages, patents

{f'Extra instructions: {extra_context}' if extra_context.strip() else ''}

Raw CV/Resume text:
{cv_raw}

Output ONLY the JSON object. No markdown fences.""" 

            try:
                l = get_llm_with_tokens(1500)
                resp = l.invoke(prompt)
                raw_output = resp.content if hasattr(resp, 'content') else str(resp)

                # Clean markdown code fences if present
                json_text = raw_output.strip()
                if json_text.startswith("```"):
                    json_text = re.sub(r'^```\w*\n?', '', json_text)
                    json_text = re.sub(r'\n?```$', '', json_text)

                # Validate JSON
                try:
                    cv_json = json.loads(json_text)
                    st.success(":white_check_mark: Valid JSON generated!")

                    # Display preview
                    st.markdown("### :package: JSON Preview")
                    with st.expander("View full JSON structure", expanded=True):
                        st.json(cv_json)

                    # Save
                    label = re.sub(r'\s+', ' ', cv_raw[:40]).strip()
                    run_folder = create_run_folder(f"JSON_CV_{label}")
                    save_run_file(json.dumps(cv_json, indent=2, ensure_ascii=False), "cv_structured.json", run_folder)

                    # Download
                    json_str = json.dumps(cv_json, indent=2, ensure_ascii=False)
                    st.download_button(":floppy_disk: Download .json", json_str, "cv_structured.json",
                                       "application/json", use_container_width=True)

                    # Also show key stats
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        st.metric("Top-level keys", len(cv_json))
                    with col_s2:
                        exp_count = len(cv_json.get("experience", []))
                        st.metric("Experience entries", exp_count)
                    with col_s3:
                        edu_count = len(cv_json.get("education", []))
                        st.metric("Education entries", edu_count)

                except json.JSONDecodeError:
                    st.warning(":warning: LLM output wasn't valid JSON. Showing raw output:")
                    st.code(raw_output[:3000], language="text")
                    run_folder = create_run_folder("JSON_CV_raw")
                    save_run_file(raw_output, "cv_raw_output.txt", run_folder)

                in_t, cost = estimate_cost(str(prompt), 1500)
                st.session_state.total_cost += cost
                st.session_state.total_calls += 1

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.info(":point_up: Paste your raw CV text above and click Generate to create structured JSON.")


est_step = 0.05 if DUMMY_MODE else 30  # seconds per step
est_total = est_step * 12
est_min = est_total / 60
st.caption(f":hourglass_flowing_sand: **Estimated time**: ~{est_min:.0f} min ({est_step:.0f}s/step) for full run")

st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.caption(":white_check_mark: **Ready**: All 15 tools live")
with col_f2:
    if DUMMY_MODE:
        st.caption(":test_tube: **Mode**: DUMMY (add API keys to `.env`)")
    else:
        st.caption(f":zap: **Provider**: {st.session_state.get('provider', 'N/A')}")
with col_f3:
    st.caption(":calendar: **Built**: May 2026 \u2022 Resume Genie")

st.sidebar.markdown("---")
st.sidebar.caption("**Pro Tip**: Upload your resume once -- it persists across all tools via sidebar :zap:")
