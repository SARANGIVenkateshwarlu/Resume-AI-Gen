# PHASE 6: Template-Based CV Generation — Format & Specifications
## Status: ✅ COMPLETED

**Goal:** Generate CVs in `.docx` format that exactly match the Sarangi template, then convert to `.pdf`. Eliminate manual formatting work.

---

## REFERENCE TEMPLATE

**Source:** `data/cv_venkateshwarlu_sarangi.docx`
**Template Markdown:** `data/CV_template.md`

---

## DOCX FORMAT SPECIFICATIONS

### Page Setup
| Property | Value |
|----------|-------|
| Page size | A4 (210mm x 297mm) |
| Left margin | 1.143 inches (29mm) |
| Right margin | 1.143 inches (29mm) |
| Top margin | 0.914 inches (23mm) |
| Bottom margin | 0.914 inches (23mm) |
| Default font | Calibri |

### Section 1 — Name (Heading 1)
| Property | Value |
|----------|-------|
| Style | Heading 1 (built-in Word style) |
| Font | Calibri |
| Content | `{name}` e.g. "Venkateshwarlu Sarangi, Ph.D" |
| Spacing | Default heading spacing |

### Section 2 — Contact Info (Normal paragraph with bold labels)
| Property | Value |
|----------|-------|
| Style | Normal |
| Font | Calibri 10pt |
| Format | Bold labels, normal values, pipe-separated |
| Labels | Location, Phone, Email, LinkedIn, GitHub, Google Scholar |
| Example | `**Location:** Hong Kong \| **Email:** email@example.com \| **LinkedIn:** linkedin.com/in/...` |
| Spacing after | 4pt |

### Section 3 — Professional Summary
| Property | Value |
|----------|-------|
| Header | Heading 2, Calibri |
| Body | Normal paragraph, Calibri 10pt |
| Spacing before header | 10pt |
| Spacing after body | 2pt |
| Content | 2-3 sentence professional summary aligned with JD |

### Section 4 — Technical Skills
| Property | Value |
|----------|-------|
| Header | Heading 2, Calibri |
| Sub-categories | Heading 3, Calibri (6pt before, 2pt after) |
| Items | Normal paragraph, Calibri 10pt |
| Categories | Machine Learning & Data Science, LLM & GenAI, MLOps & Infrastructure, Cloud Platforms, Development & Tooling |
| Format | Comma-separated skills per category |

### Section 5 — Work Experience
| Property | Value |
|----------|-------|
| Header | Heading 2, Calibri |
| Job Title | Heading 3, Calibri (6pt before, 2pt after) |
| Company/Date line | Normal paragraph, **Bold**, Calibri 10pt |
| Format | `Company | Location | Month Year – Month Year` |
| Project name | Normal paragraph, Calibri 10pt (optional) |
| Bullet points | Normal paragraph, Calibri 10pt, left indent 0.25", line spacing 1.0, 1pt after |
| Technologies line | Normal paragraph, **Bold**, Calibri 10pt |
| Format | `Technologies: Python, PyTorch, AWS, ...` |

### Section 6 — Journal Publications
| Property | Value |
|----------|-------|
| Header | Heading 2, Calibri |
| Entries | Bullet format (left indent 0.25"), Calibri 10pt |
| Format | `Author, **Title**, Venue, Year` |
| Templates | `{authors}, Nature Communications Physics, (2020)` |
| Line spacing | 1.0, 1pt after |

### Section 7 — Education
| Property | Value |
|----------|-------|
| Header | Heading 2, Calibri |
| Entries | Bullet format, degree in **bold**, Calibri 10pt |
| Format | `**Ph.D in Materials Science**, City University of Hong Kong, (2021)` |
| Line spacing | 1.0, 1pt after |

### Section 8 — Certifications
| Property | Value |
|----------|-------|
| Header | Heading 2, Calibri |
| Entries | Bullet format, title in **bold**, Calibri 10pt |
| Format | `**Certification Title**, Issuer, Date` |
| Line spacing | 1.0, 1pt after |

---

## JSON SCHEMA (LLM Output)

```json
{
  "name": "Dr. Venkateshwarlu Sarangi (Ph.D)",
  "contact": {
    "location": "Hong Kong",
    "phone": "+852-5316757",
    "email": "email@example.com",
    "linkedin": "linkedin.com/in/username",
    "github": "github.com/username",
    "scholar": "scholar.google.com/..."
  },
  "summary": "2-3 sentence professional summary...",
  "skills": [
    {
      "category": "Machine Learning & Data Science",
      "items": "Supervised/Unsupervised Learning, Feature Engineering, PyTorch, TensorFlow..."
    },
    {
      "category": "LLM & GenAI",
      "items": "LLM Fine-tuning, RAG, Embeddings, Vector DBs, Prompt Engineering..."
    }
  ],
  "experience": [
    {
      "title": "Senior Data Scientist & ML Engineer",
      "company": "XRadio Ltd",
      "location": "Hong Kong",
      "dates": "Aug 2025 – March 2026",
      "project_name": "Deep Learning for ECG Signal Intelligence",
      "highlights": [
        "Built explainable deep learning model for 12-lead ECG classification...",
        "Evaluated ResNet34, ResNet50, ViT architectures achieving AUROC 0.98..."
      ],
      "technologies": "Python, PyTorch, Scikit-learn, AWS SageMaker, Docker"
    }
  ],
  "publications": [
    "S. Venkateshwarlu et al., Nature Communications Physics, (2020)",
    "S. Venkateshwarlu et al., Journal of Materials Research, (2021)"
  ],
  "education": [
    {
      "degree": "Ph.D in Materials Science and Engineering (Physics)",
      "school": "City University of Hong Kong",
      "year": "2021"
    },
    {
      "degree": "M.Tech in Materials Science and Engineering",
      "school": "IIT Bombay",
      "year": "2013"
    }
  ],
  "certifications": [
    {
      "title": "Generative AI with Large Language Models",
      "details": "DeepLearning.AI & AWS | 2024"
    }
  ]
}
```

---

## IMPLEMENTATION

### Files Created/Modified

| File | Change |
|------|--------|
| `utils.py` | Added `generate_docx_cv_template(cv_data)` — 130 lines |
| `main_dashboard.py` | CV Tailor prompt now asks for JSON output |
| `main_dashboard.py` | CV Tailor save section parses JSON → template DOCX |
| `main_dashboard.py` | Auto-Pilot CV step uses JSON prompt |
| `PDR/phase-6.md` | This document |

### Flow

```
User: Uploads CV + Pastes JD
  │
  ▼
LLM: Outputs JSON matching template schema
  │
  ├─► .md file: Raw JSON saved
  ├─► generate_docx_cv_template(json) → .docx (exact template)
  └─► generate_pdf(text) → .pdf
  │
  ▼
User: Downloads all 3 formats
```

### Key Design Decisions

1. **Dual fallback**: If LLM doesn't output valid JSON, falls back to generic `generate_docx()` — never breaks
2. **JSON-first**: The JSON structure is the canonical format; DOCX/PDF are renderings
3. **Auto-Pilot compatible**: Same JSON schema used in both manual and auto modes
4. **10/90 split preserved**: 10% original (dates/titles/companies), 90% adjusted for JD keywords

---

## USAGE

### In Web App
1. Select **"2. CV Tailor"** from sidebar
2. Upload CV + Paste JD
3. Click **"Tailor CV"**
4. LLM outputs JSON → rendered as template DOCX
5. Download `.md` / `.docx` / `.pdf`

### In Auto-Pilot
- Step 2 automatically uses the template JSON format
- DOCX rendered with `generate_docx_cv_template()`

---

**End of Phase 6 Report**
