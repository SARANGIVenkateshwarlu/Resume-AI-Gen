# config.py — Constants, provider config, token budgets
import os, re
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# ── Provider Configuration ──
PROVIDER_CONFIG = {
    "Grok (xAI)": {
        "key_env": "XAI_API_KEY",
        "models": ["grok-4", "grok-4-latest", "grok-3", "grok-3-latest"],
        "pkg": "langchain_xai",
        "desc": "Best for structured outputs & reasoning",
    },
    "OpenAI": {
        "key_env": "OPENAI_API_KEY",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1", "o3-mini"],
        "pkg": "langchain_openai",
        "desc": "Most widely used, strong all-rounder",
    },
    "Claude (Anthropic)": {
        "key_env": "ANTHROPIC_API_KEY",
        "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
        "pkg": "langchain_anthropic",
        "desc": "Best for nuanced writing & cover letters",
    },
    "DeepSeek": {
        "key_env": "DEEPSEEK_API_KEY",
        "models": ["deepseek-chat", "deepseek-reasoner"],
        "pkg": "langchain_openai",
        "base_url": "https://api.deepseek.com",
        "desc": "Cost-effective, strong reasoning",
    },
    "Qwen (Alibaba)": {
        "key_env": "DASHSCOPE_API_KEY",
        "models": ["qwen-plus", "qwen-max", "qwen-turbo"],
        "pkg": "langchain_openai",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "desc": "Strong multilingual & technical",
    },
}

# ── Token Budgets per tool ──
TOKEN_BUDGETS = {
    "jd_decoder": 600,
    "cv_tailor": 4000,
    "bullet_sharpener": 800,
    "cover_letter": 1000,
    "role_fit_matrix": 1200,
    "ats_fixer": 1200,
    "resume_matcher": 1000,
    "interview_q": 1500,
    "star_builder": 2000,
    "recruiter_review": 1000,
    "full_package": 2000,
    "resume_checker": 800,
    "career_coach": 1000,
    "json_cv_mapper": 1500,
}

# ── Token Pricing (Grok-4.3 reference) ──
INPUT_COST_PER_1M = 1.25
OUTPUT_COST_PER_1M = 2.50
CACHED_COST_PER_1M = 0.20

# ── Step Names ──
STEP_NAMES = {
    1: "JD Decoder", 2: "CV Tailor", 3: "Bullet Sharpener",
    4: "Cover Letter", 5: "Role-Fit Matrix", 6: "ATS Fixer",
    7: "Resume-JD Matcher", 8: "Interview Q", 9: "STAR Builder",
    10: "Recruiter Review", 11: "Full Package", 12: "Job Tracker",
}

# ── Candidate Profile Rules ──
CANDIDATE_RULES = """
[IMPORTANT CONTEXT — Follow these rules strictly]
The candidate holds a PhD and has 4 years of industry experience — highly qualified for senior-level roles.

When rewriting or tailoring resume/CV/cover letter content:
- PRESERVE 90% of the original experience text verbatim. Do NOT rewrite entire sections.
- Only adjust up to 10% of wording per project (rephrase for clarity, relevance to JD, or stronger action verbs).
- CAPSTONE / RESEARCH PROJECTS: up to 50% of content may be adapted to align with JD keywords and requirements.
- NEVER invent new projects, company names, job titles, or metrics.
- NEVER add fake achievements — use [ADD METRIC] placeholders where numbers are unavailable.
- The goal is ATS alignment while keeping the candidate's real experience intact.
"""

# ── Google Sheets Scopes ──
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# ── User Identity ──
USERNAME = os.getenv("USERNAME", "USER").upper()

def get_job_title(jd_text=""):
    """Extract a clean job title from JD text."""
    if not jd_text:
        return "Job"
    first_line = jd_text.split('\n')[0].strip()
    for prefix in ['Job Description:', 'Job Title:', 'Position:', 'Role:', 'About the role', 'About this role']:
        if first_line.lower().startswith(prefix.lower()):
            first_line = first_line[len(prefix):].strip()
    # Take first 3-4 words as job title
    words = first_line.split()
    title = '_'.join(words[:4]) if len(words) >= 4 else '_'.join(words)
    title = re.sub(r'[^a-zA-Z0-9_-]', '', title)[:60]
    return title if title else "Job"
