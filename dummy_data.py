# dummy_data.py — All DUMMY MODE response templates
DUMMY_PREFIX = "\U0001f9ea **DUMMY MODE — Add your xAI API key to `.env` for real AI generation.**\n\n---\n\n"

DUMMY_JD_DECODER = DUMMY_PREFIX + """
### JD Decoder — Structured Analysis

| Area | Extracted from JD |
|------|-------------------|
| **Core Responsibilities** | • Lead cross-functional engineering teams to deliver product milestones\n• Design and implement scalable cloud-native architectures\n• Drive technical strategy and roadmap planning |
| **Required Skills** | • Python, AWS/GCP, Kubernetes, Docker\n• System design & architecture patterns\n• Agile/Scrum methodology |
| **Nice-to-Have Skills** | • Machine Learning / AI experience\n• Open-source contributions\n• Speaking at tech conferences |
| **ATS Keywords** | cloud-native, scalable systems, technical leadership, cross-functional, roadmap, architecture, CI/CD, microservices, stakeholder management |
| **Standout Traits** | • Track record of shipping complex systems on time\n• Strong written and verbal communication\n• Mentorship and team growth |
"""

DUMMY_CV_TAILOR = DUMMY_PREFIX + """
## Tailored CV

**Professional Summary:**
Results-driven engineer with X years of experience delivering scalable cloud-native solutions and leading cross-functional teams. Proven track record in system architecture, CI/CD pipelines, and driving technical roadmaps from conception to production.

**Experience:**

**Senior Engineer | Company Name | Dates**
- Led cross-functional team of X engineers to deliver cloud-native microservices platform, reducing deployment time by [ADD METRIC]%
- Designed and implemented scalable architecture serving [ADD METRIC] daily active users
- Drove technical roadmap planning across X product lines, aligning engineering with business goals
- Built CI/CD pipelines using Docker and Kubernetes, improving release frequency by [ADD METRIC]

**Skills:**
Python, AWS/GCP, Kubernetes, Docker, System Design, CI/CD, Microservices, Agile/Scrum, Technical Leadership, Stakeholder Management
"""

DUMMY_BULLETS = DUMMY_PREFIX + """
### Bullet Sharpener — ATR Format

| Original | Improved (Action + Task + Result) |
|----------|-----------------------------------|
| "Worked on machine learning models" | **Built** ML pipeline that processed X records/day, reducing false positives by [ADD METRIC]% |
| "Managed a team" | **Led** cross-functional team of X engineers to deliver 3 major product milestones on schedule |
| "Did data analysis" | **Analyzed** Y TB of user behavior data to identify growth opportunities, driving [ADD METRIC]% revenue increase |
| "Used AWS" | **Architected** cloud-native infrastructure on AWS, achieving 99.9% uptime and [ADD METRIC]% cost reduction |
"""

DUMMY_COVER_LETTER = DUMMY_PREFIX + """
[Cover letter template - DUMMY MODE placeholder]
"""

DUMMY_ROLE_FIT = DUMMY_PREFIX + """
### Role-Fit Matrix

| Area from JD | My Strengths | Gaps | CV Focus | Cover Letter Angle | Interview Story |
|---|---|---|---|---|---|
| Cloud-native architecture | 5+ years AWS/GCP | Kubernetes at scale | Highlight cloud migration wins | "Scalable by default" mindset | Migration: monolith to microservices |
| Technical leadership | Managed team of 5 | Executive stakeholders | Team outcomes, not headcount | Amplify team output | Turnaround: delayed project in 3 months |
| System design | Designed 4 production systems | Interview practice | Architecture diagrams | Specific design patterns | Real-time event system: 10K/sec |
| Agile/Scrum | Scrum Master certified, 3 years | SAFe framework | Facilitation wins | Sprint velocity improvements | Sprint spillover: 40% to 5% |
| CI/CD pipelines | Docker, Jenkins | GitHub Actions, ArgoCD | Release frequency | CI/CD to business agility | Deployment: 2 days to 2 hours |
"""

DUMMY_ATS = DUMMY_PREFIX + """
---SCORES---
ATS_SCORE: 65
JD_MATCH_PCT: 72
VERDICT: NEEDS WORK

---DETAILS---
### ATS Alignment Analysis

**Missing Keywords:** • microservices • stakeholder management • roadmap • cloud-native • CI/CD • Kubernetes

**Weak/Vague Sections:**
• Professional summary is generic — lacks role-specific keywords
• "Worked on" should be replaced with strong action verbs
• No mention of team size or project scale

**Redundant Content:**
• "Responsible for" appears 4 times — use varied language
• Skills list duplicates experience section content

### Rewritten Professional Summary:
Results-driven engineer with X years leading cross-functional teams to deliver scalable, cloud-native microservices platforms on AWS/GCP. Proven track record driving technical roadmaps, building CI/CD pipelines with Kubernetes, and aligning engineering strategy with business outcomes through effective stakeholder management.

### Change-Log:
• Added missing ATS keywords: microservices, stakeholder management, roadmap, cloud-native, CI/CD, Kubernetes
• Replaced weak "worked on" verbs with "led", "delivered", "built"
• Consolidated skills section to focus on JD-aligned keywords
• Added quantification placeholders [ADD METRIC] for impact metrics
"""

DUMMY_MATCHER = DUMMY_PREFIX + """
### Resume-JD Match Analysis

**Score**: 72/100  **Overall Match**: 72%

**Keywords matched:** • Python • AWS • Docker • agile • team leadership • system design • CI/CD

**Missing keywords:** • Kubernetes • microservices • stakeholder management • cloud-native • roadmap planning

**Readability Score:** 78/100  **ATS Compatibility Score:** 65/100

**Summary:** Strong technical foundation and leadership. Main gap: Kubernetes and stakeholder management terminology.

**Skill gap analysis:**
• Kubernetes — get certification or add side project
• Stakeholder management — reframe as cross-functional influence
• Cloud-native — update terminology from existing AWS experience

**Improvement suggestions:**
• Add "microservices" and "cloud-native" to skills section
• Quantify bullets with numbers (team size, users, revenue)
• Add "roadmap" and "stakeholder" keywords to summary
• Replace generic verbs with strong action verbs
"""

DUMMY_INTERVIEW_Q = DUMMY_PREFIX + """
### Predicted Interview Questions

**Technical (7):** System design, Kubernetes, debugging, CI/CD, trade-offs, code quality, cloud migration
**Behavioral (5):** Behind-schedule project, PM disagreement, mentorship, failure, prioritization
**Culture (3):** Why here, engineering culture, staying current

(Full detailed questions available with real API key.)
"""

DUMMY_STAR = DUMMY_PREFIX + """
### STAR Answer Templates — 8 categories ready

1. Leadership | 2. Problem-solving | 3. Teamwork | 4. Conflict resolution
5. Ownership/Accountability | 6. Failure/Mistake | 7. Achievement/Success | 8. Adaptability/Change

(Full detailed STAR answers with Situation/Task/Action/Result available with real API key.)
"""

DUMMY_RECRUITER = DUMMY_PREFIX + """
### Recruiter-Style Review

**Verdict: SHORTLIST** — Strong technical profile with relevant leadership. With keyword additions and metrics, high potential.

**Top Strengths:** Cloud infrastructure depth, team management, relevant tech stack, professional tone

**Top Weaknesses:** Missing ATS keywords (Kubernetes, microservices), bullets lack metrics, generic summary

**Quick-Fix Suggestions:**
1. Add "Kubernetes" to skills and 2+ bullets
2. Quantify 3-4 bullets with real metrics
3. Rewrite summary: "cloud-native", "microservices", "stakeholder"
4. Add "Notable Projects" with architecture highlights
5. Run ATS Fixer and apply recommendations
"""

DUMMY_FULL_PACKAGE = DUMMY_PREFIX + """
# COMPLETE APPLICATION PACKAGE

## 1. CV SUMMARY
Results-driven PhD engineer with 4 years delivering scalable cloud-native microservices platforms. Proven track record leading cross-functional teams, driving technical roadmaps, and building CI/CD pipelines with Kubernetes and Docker.

## 2. KEY SKILLS
Python • AWS/GCP • Kubernetes • Docker • CI/CD • Microservices • System Design • Agile/Scrum • Technical Leadership • Stakeholder Management • Cloud-Native Architecture • Roadmap Planning

## 3. COVER LETTER
[Tailored cover letter generated separately]

## 4. PREDICTED INTERVIEW QUESTIONS
Technical (7) | Behavioral (5) | Culture (3)

## 5. LINKEDIN OUTREACH DM
Hi [Name] — I recently applied for [Role] at [Company]. I bring 4 years building scalable cloud platforms and leading engineering teams. I'm drawn to [Company]'s work in [area]. Open to a brief chat? Thanks!

## 6. FOLLOW-UP EMAIL
Subject: Following Up — [Role] Application — [Your Name]
[Template with placeholders for company name, date, key skills]
"""

DUMMY_GENERIC = DUMMY_PREFIX + """
### DUMMY MODE Response — Add API key to `.env` for real AI generation

1. Get an API key from your provider (xAI, OpenAI, Anthropic, DeepSeek, or Qwen)
2. Add it to the `.env` file in the project root
3. Restart the app

All tools will then generate real, personalized content based on your resume and job description.
"""
