# PHASE 4: JSON CV Mapper — Structured Resume Generator
## Status: ✅ COMPLETED

**Goal:** Convert raw CV/resume text into structured JSON format suitable for automated PDF rendering via react-pdf or ReportLab.

---

## OVERVIEW

The JSON CV Mapper is a new AI-powered tool that bridges the gap between free-form resume text and template-driven PDF generation. It takes raw CV/Resume data and produces a clean, structured JSON object that can be directly injected into PDF template engines.

---

## FEATURES

### 1. Name-Entity Mapping
- Extracts all key entities: Name, Contact, Dates, Skills, Companies, Schools
- Maps to standardized JSON keys (`header`, `experience`, `skills`, `education`)

### 2. Template Style Selection
Five layout styles supported:
| Style | Description |
|-------|-------------|
| Modern two-column | ATS-friendly, skills sidebar |
| Minimalist single-page | Clean, one-page layout |
| Academic with publications | Research-focused, publication list |
| Tech/startup bold | Impact-driven, metrics-heavy |
| Classic professional | Traditional chronological |

### 3. Custom Sections
- User can specify additional sections: patents, awards, languages, volunteer, etc.
- Extra context field for custom instructions

### 4. Output Format
```json

{
  "schema_version": "1.0.0",
  "schema_type": "curriculum_vitae",
  "metadata": {
    "language": "en-US",
    "target_roles": ["Data Scientist", "ML Engineer", "LLM Engineer"],
    "last_updated": "2026-05-06",
    "ats_optimized": true,
    "page_format": {
      "margins": {
        "left": "8mm",
        "right": "8mm",
        "top": "8mm",
        "bottom": "8mm"
      },
      "font": "Mulish",
      "theme_color": "#0F83C0"
    }
  },
  "personal_info": {
    "full_name": "Venkateshwarlu Sarangi",
    "title": "Ph.D",
    "location": {
      "city": "Hong Kong",
      "country": "HK",
      "map_link": "https://www.google.com/maps/place/Hong+Kong"
    },
    "contact": [
      {
        "type": "linkedin",
        "label": "LinkedIn",
        "url": "https://www.linkedin.com/in/dr-venkateshwarlu-sarangi-ph-d-96688321"
      },
      {
        "type": "github",
        "label": "Github",
        "url": "https://github.com/SARANGIVenkateshwarlu"
      },
      {
        "type": "email",
        "label": "venky.sarangi@gmail.com",
        "url": "mailto:venky.sarangi@gmail.com"
      },
      {
        "type": "academic_profile",
        "label": "CityU HK",
        "url": "https://scholars.cityu.edu.hk/en/persons/vsarangi2/"
      }
    ]
  },
  "professional_summary": {
    "headline": "AI/ML Engineer & LLM Specialist",
    "years_experience": 10,
    "core_competencies": [
      "LLM Fine-Tuning",
      "Multimodal RAG Systems",
      "MLOps/LLMOps",
      "Domain-Specific SLM Optimization",
      "Vision-Language Model Integration",
      "End-to-End AI System Architecture"
    ],
    "narrative": "AI/ML Engineer & LLM Specialist with 10+ years of research and applied data science experience and a Ph.D. in Physics. Expert in LLM fine-tuning, multimodal RAG systems, and production MLOps/LLMOps. Combines deep scientific rigor with practical AI deployment—specializing in domain-specific small-language model (SLM) optimization, RAG-systems, Vision-Language Model (VLM) integration, and end-to-end AI system architecture. Proven track record of translating complex research into scalable, production-ready solutions across industry and academic collaborations."
  },
  "technical_skills": {
    "categories": [
      {
        "category": "Machine Learning & Data Science",
        "skills": [
          "Supervised/Unsupervised Learning",
          "Feature Engineering",
          "Model Selection & Validation",
          "Hyperparameter Optimization",
          "Time Series Forecasting",
          "Anomaly Detection",
          "Statistical Modeling",
          "Scikit-learn",
          "XGBoost",
          "LightGBM"
        ]
      },
      {
        "category": "RAG & Information Retrieval",
        "skills": [
          "Dense/Sparse Retrieval",
          "Vector DBs (Chroma, FAISS, Pinecone, Weaviate, Milvus)",
          "Re-ranking & Hybrid Search",
          "Embedding Models",
          "Query Expansion",
          "Document Chunking & Preprocessing",
          "Grounding & Hallucination Detection",
          "Evaluation Metrics"
        ]
      },
      {
        "category": "MLOps & Infrastructure",
        "skills": [
          "Docker",
          "Kubernetes (K8s)",
          "Helm",
          "CI/CD (GitHub Actions, Jenkins, GitLab CI)",
          "Terraform",
          "MLflow",
          "DVC",
          "Weights & Biases",
          "Prometheus",
          "Grafana",
          "Evidently",
          "Feature Stores (Feast, Tecton)",
          "A/B Testing & Experimentation",
          "Blue-Green & Canary Deployments",
          "Model Registry & Versioning"
        ]
      },
      {
        "category": "Cloud Platforms",
        "skills": [
          "AWS (SageMaker, EC2, EKS, S3, Lambda)",
          "Azure Machine Learning",
          "GCP Vertex AI",
          "Serverless & Edge Deployment"
        ]
      },
      {
        "category": "Development & Tooling",
        "skills": [
          "Python",
          "PyTorch",
          "NumPy",
          "Pandas",
          "FastAPI",
          "Flask",
          "Git",
          "GitHub",
          "Streamlit",
          "Gradio",
          "SQL",
          "Spark",
          "Airflow"
        ]
      }
    ]
  },
  "work_experience": {
    "entries": [
      {
        "id": "exp_001",
        "role": "Data Scientist & ML Engineer",
        "company": "XRadio Ltd",
        "location": "Hong Kong",
        "employment_type": "Freelance",
        "start_date": "2025-08",
        "end_date": "2026-03",
        "is_current": false,
        "duration_months": 8,
        "domain": "Deep Learning and Multimodal Systems for ECG Signal Intelligence",
        "achievements": [
          {
            "description": "Built an explainable deep learning model for 12-lead ECG arrhythmia classification, addressing challenges from non-stationary signals and inter-patient variability.",
            "technologies": ["Deep Learning", "ECG Signal Processing", "Explainable AI"],
            "impact": null
          },
          {
            "description": "Evaluated multiple deep learning and vision architectures including ResNet34, ResNet50, DenseNet, VGG16, Vision Transformers (ViT), and Vision-Language Models (VLMs) for multimodal AI systems in healthcare prediction tasks.",
            "technologies": ["ResNet34", "ResNet50", "DenseNet", "VGG16", "ViT", "VLM"],
            "impact": null
          },
          {
            "description": "Achieved strong model performance with ResNet34, reaching AUROC 0.98 and F1-score 0.826 across nine arrhythmia categories.",
            "technologies": ["ResNet34"],
            "metrics": {
              "auroc": 0.98,
              "f1_score": 0.826,
              "categories": 9
            },
            "impact": "High diagnostic accuracy across multiple arrhythmia types"
          }
        ]
      },
      {
        "id": "exp_002",
        "role": "Data Scientist & Research Engineer",
        "company": "Gense Technologies Ltd",
        "location": "Hong Kong",
        "employment_type": "Full-time",
        "start_date": "2022-10",
        "end_date": "2025-08",
        "is_current": false,
        "duration_months": 34,
        "domain": "Biomedical Signal Processing & Clinical ML Systems",
        "projects": [
          {
            "project_name": "End-to-End Clinical ML Pipelines",
            "achievements": [
              {
                "description": "Designed and deployed end-to-end supervised learning pipelines (Random Forest, XGBoost, Gradient Boosting, logistic regression) for clinical prediction tasks, achieving 87% sensitivity and >99% specificity on imbalanced biomedical datasets.",
                "algorithms": ["Random Forest", "XGBoost", "Gradient Boosting", "Logistic Regression"],
                "metrics": {
                  "sensitivity_percent": 87,
                  "specificity_percent": 99
                },
                "techniques": ["Imbalanced Data Handling", "Clinical Prediction"],
                "impact": "High diagnostic reliability for clinical decision support"
              },
              {
                "description": "Engineered feature extraction and signal processing workflows using Python (NumPy, Pandas, Scikit-learn) to improve SNR and diagnostic quality in time-series bio-conductivity data.",
                "technologies": ["Python", "NumPy", "Pandas", "Scikit-learn"],
                "techniques": ["Feature Extraction", "Signal Processing", "SNR Optimization"],
                "impact": "Improved signal quality for diagnostic applications"
              },
              {
                "description": "Achieved a 100% improvement in skin electrode contact impedance without conductive gels, improving signal sensitivity.",
                "technologies": ["Dry Electrode Systems", "Impedance Analysis"],
                "metrics": {
                  "impedance_improvement_percent": 100
                },
                "impact": "Eliminated need for conductive gels while maintaining signal fidelity"
              },
              {
                "description": "Developed and validated signal enhancement and impedance analysis models for ECG and EIT datasets, improving signal-to-noise ratio and diagnostic reliability.",
                "technologies": ["ECG", "EIT", "Signal Enhancement"],
                "techniques": ["Impedance Analysis", "SNR Improvement"],
                "impact": "Enhanced diagnostic reliability across multiple modalities"
              }
            ]
          },
          {
            "project_name": "MLOps & Cloud Infrastructure",
            "achievements": [
              {
                "description": "Built automated MLOps workflows with Docker, CI/CD, and MLflow for experiment tracking, model versioning, and reproducible deployments across cloud environments.",
                "technologies": ["Docker", "CI/CD", "MLflow"],
                "techniques": ["Experiment Tracking", "Model Versioning", "Reproducible Deployments"],
                "impact": "Streamlined model lifecycle management"
              },
              {
                "description": "Applied statistical validation frameworks (k-fold cross-validation, ROC-AUC optimization, hypothesis testing) to ensure diagnostic-grade model reliability and regulatory compliance.",
                "techniques": ["K-Fold Cross-Validation", "ROC-AUC Optimization", "Hypothesis Testing"],
                "impact": "Ensured regulatory compliance and clinical-grade reliability"
              }
            ]
          },
          {
            "project_name": "Data Augmentation & Production Systems",
            "achievements": [
              {
                "description": "Developed synthetic data augmentation strategies (SMOTE, bootstrapping) to address limited clinical datasets, improving model generalization by 20%.",
                "techniques": ["SMOTE", "Bootstrapping", "Synthetic Data Generation"],
                "metrics": {
                  "generalization_improvement_percent": 20
                },
                "impact": "Overcame data scarcity in clinical settings"
              },
              {
                "description": "Proficient in Python, SQL, PyTorch, Scikit-learn, and cloud ML platforms (GCP, Firebase, AWS SageMaker) for scalable production systems.",
                "technologies": ["Python", "SQL", "PyTorch", "Scikit-learn", "GCP", "Firebase", "AWS SageMaker"],
                "impact": "Enabled scalable production ML deployments"
              }
            ]
          }
        ]
      },
      {
        "id": "exp_003",
        "role": "Data Scientist and Computational Analyst",
        "company": "Anvipro IT Solutions",
        "location": "India",
        "employment_type": "Full-time",
        "start_date": "2021-12",
        "end_date": "2022-06",
        "is_current": false,
        "duration_months": 7,
        "domain": "Materials Science & Computational Modeling",
        "achievements": [
          {
            "description": "Conducted physics-based simulation and data analysis using COMSOL Multiphysics to study material flexibility (>90%), stress distribution, hardness, and structural behavior.",
            "technologies": ["COMSOL Multiphysics"],
            "metrics": {
              "flexibility_percent": 90
            },
            "impact": "Comprehensive material characterization"
          },
          {
            "description": "Performed materials data preprocessing, cleaning, and simulations using MATLAB and Python basic libraries to improve analysis quality and model readiness.",
            "technologies": ["MATLAB", "Python"],
            "techniques": ["Data Preprocessing", "Data Cleaning", "Simulation"],
            "impact": "Improved model readiness for downstream analysis"
          },
          {
            "description": "Applied supervised learning and statistical modeling techniques to analyze material properties, identify trends, and support predictive insights.",
            "techniques": ["Supervised Learning", "Statistical Modeling"],
            "impact": "Enabled predictive insights for materials engineering"
          },
          {
            "description": "Improved simulation and analytical workflows through iterative model refinement, results evaluation, and reliability analysis for engineering and materials-focused projects.",
            "techniques": ["Iterative Refinement", "Reliability Analysis"],
            "impact": "Enhanced workflow efficiency and result reliability"
          }
        ],
        "technologies_used": ["Python", "Data Processing", "Feature Engineering", "EDA", "NumPy", "Pandas", "Scikit-learn", "OriginLab", "SQL", "Power BI", "Statistical Modeling"]
      },
      {
        "id": "exp_004",
        "role": "Ph.D Research Scholar",
        "company": "City University of Hong Kong",
        "location": "Hong Kong",
        "employment_type": "Research",
        "start_date": "2015-08",
        "end_date": "2021-10",
        "is_current": false,
        "duration_months": 75,
        "domain": "Materials Engineering / Computational Modeling / Data Analysis",
        "achievements": [
          {
            "description": "Designed piezoelectric electrodes, applied advanced statistical and computational modeling for material structure analysis using X-ray and neutron diffraction datasets.",
            "technologies": ["X-ray Diffraction", "Neutron Diffraction"],
            "techniques": ["Statistical Modeling", "Computational Modeling"],
            "impact": "Advanced materials characterization methodology"
          },
          {
            "description": "Performed Rietveld refinement and data processing, feature engineering, and regression-based parameter optimization, fine-tuning methods, hyperparameter tuning, model optimization to extract structural insights from complex datasets.",
            "techniques": ["Rietveld Refinement", "Feature Engineering", "Regression Optimization", "Hyperparameter Tuning", "Model Optimization"],
            "impact": "Extracted high-fidelity structural insights from complex data"
          },
          {
            "description": "Published research in Nature Communications, Communications Physics, Physical Review B, Scientific Reports, and other high-impact journals.",
            "impact": "Established academic credibility through high-impact publications"
          }
        ],
        "technologies_used": ["FullProf", "GSAS-II", "Pair Distribution Function (PDF) Analysis", "Python", "MATLAB", "OriginLab", "Scikit-learn", "Statistical Modeling"]
      }
    ]
  },
  "publications": {
    "entries": [
      {
        "authors": "S. Venkateshwarlu et al.",
        "journal": "Nature Communications Physics",
        "year": 2020,
        "type": "journal_article"
      },
      {
        "authors": "S. Venkateshwarlu et al.",
        "journal": "Journal of Materials Research",
        "publisher": "Cambridge University Press",
        "reference": "JMR-0830",
        "year": 2019,
        "type": "journal_article"
      },
      {
        "authors": "S. Nayak, S. Venkateshwarlu, et al.",
        "journal": "Journal of the American Ceramic Society",
        "year": 2019,
        "type": "journal_article"
      },
      {
        "authors": "Frederick, Sarangi Venkateshwarlu, et al.",
        "journal": "Chemistry of Materials",
        "year": 2021,
        "type": "journal_article"
      },
      {
        "authors": "A. Pramanick, S. Venkateshwarlu, et al.",
        "journal": "Physical Review B",
        "year": 2021,
        "type": "journal_article"
      },
      {
        "authors": "Liang, Zhuoxin Liu, S. Venkateshwarlu, et al.",
        "journal": "Nature, Light: Science & Applications",
        "year": 2021,
        "type": "journal_article"
      },
      {
        "authors": "G. Srinivas, S. Venkateshwarlu, et al.",
        "journal": "Applied Physics Letters",
        "year": 2015,
        "type": "journal_article"
      },
      {
        "authors": "S. Venkateshwarlu, et al.",
        "journal": "Journal of Modern Materials",
        "year": 2016,
        "type": "journal_article"
      },
      {
        "authors": "Pramanick, Venkateshwarlu",
        "journal": "Journal of the European Ceramic Society",
        "year": 2023,
        "type": "journal_article"
      },
      {
        "authors": "Nirmal and Sarangi Venkateshwarlu et al.",
        "journal": "arXiv",
        "reference": "2508.10940",
        "year": 2025,
        "type": "preprint"
      },
      {
        "authors": "Kwok, W.C., Sarangi Venkateshwarlu et al.",
        "journal": "Nature Scientific Reports",
        "year": 2025,
        "type": "journal_article"
      }
    ]
  },
  "education": {
    "entries": [
      {
        "degree": "Ph.D",
        "field": "Materials Science and Engineering (Physics)",
        "institution": "City University of Hong Kong",
        "location": "Hong Kong",
        "graduation_date": "2021-10",
        "duration_years": 6
      },
      {
        "degree": "M.Tech",
        "field": "Materials Science and Engineering (Physics)",
        "institution": "IIT Bombay",
        "location": "India",
        "graduation_date": "2013-06",
        "duration_years": 2
      }
    ]
  },
  "certifications": {
    "entries": [
      {
        "name": "Generative AI with Large Language Models (LLMs)",
        "provider": "DeepLearning.AI & Amazon Web Services",
        "platform": "Coursera",
        "completion_date": "2026-02",
        "skills": [
          "Transformers Architecture",
          "FLAN-T5",
          "BERT",
          "GPT",
          "DeepSeek",
          "Qwen",
          "Phi-2",
          "Gemma",
          "RL models",
          "PyTorch",
          "PEFT",
          "Fine-tuning",
          "LoRA",
          "QLoRA",
          "Knowledge Distillation",
          "RAG",
          "LangChain",
          "LangGraph",
          "Deployment",
          "vLLM",
          "OpenWebUI",
          "FastAPI",
          "Streamlit",
          "RunPOD",
          "LightningAI",
          "HuggingFace",
          "Optuna Optimization"
        ]
      },
      {
        "name": "Machine Learning Specialization",
        "provider": "Stanford University & DeepLearning.AI",
        "platform": "Coursera",
        "completion_date": "2025-08"
      },
      {
        "name": "Deep Learning and NLP Specialization",
        "provider": "Stanford University & DeepLearning.AI",
        "platform": "Coursera",
        "completion_date": "2026-01"
      },
      {
        "name": "End-to-End MLOPS Bootcamp",
        "provider": "Udemy",
        "status": "ongoing",
        "completion_date": "2026-04"
      }
    ]
  },
  "projects": {
    "entries": [
      {
        "name": "ECG Arrhythmia Classification System",
        "description": "Explainable deep learning model for 12-lead ECG arrhythmia classification using ResNet34, achieving AUROC 0.98 and F1-score 0.826 across nine categories.",
        "technologies": ["ResNet34", "Deep Learning", "ECG Signal Processing", "Explainable AI"],
        "metrics": {
          "auroc": 0.98,
          "f1_score": 0.826
        },
        "domain": "Healthcare AI"
      },
      {
        "name": "CKD Prediction from Bio-Conductivity",
        "description": "End-to-end clinical ML pipeline using Random Forest, XGBoost, and logistic regression to predict CKD from portable fdEIT bio-conductivity data, achieving 87% sensitivity and >99% specificity.",
        "algorithms": ["Random Forest", "XGBoost", "Logistic Regression"],
        "metrics": {
          "sensitivity_percent": 87,
          "specificity_percent": 99
        },
        "domain": "Clinical Diagnostics"
      },
      {
        "name": "EIT Image Reconstruction Pipeline",
        "description": "Algorithmic pipeline for Electrical Impedance Tomography image reconstruction with statistical validation frameworks for diagnostic-grade imaging outputs.",
        "technologies": ["EIT", "Statistical Validation", "Image Reconstruction"],
        "domain": "Medical Imaging"
      }
    ]
  },
  "ats_keywords": {
    "primary": [
      "Machine Learning",
      "Deep Learning",
      "Data Science",
      "MLOps",
      "LLMOps",
      "Python",
      "PyTorch",
      "Scikit-learn",
      "XGBoost",
      "Random Forest",
      "Logistic Regression",
      "Feature Engineering",
      "Signal Processing",
      "Time Series",
      "Statistical Modeling",
      "Docker",
      "Kubernetes",
      "CI/CD",
      "MLflow",
      "AWS",
      "GCP",
      "Azure",
      "SQL",
      "FastAPI",
      "Transformers",
      "RAG",
      "Vector Databases",
      "Fine-tuning",
      "LoRA",
      "HuggingFace"
    ],
    "secondary": [
      "NumPy",
      "Pandas",
      "LightGBM",
      "Gradient Boosting",
      "Cross-Validation",
      "ROC-AUC",
      "Hypothesis Testing",
      "SMOTE",
      "Bootstrapping",
      "GitHub Actions",
      "Jenkins",
      "Terraform",
      "Prometheus",
      "Grafana",
      "Airflow",
      "Spark",
      "Streamlit",
      "Gradio",
      "LangChain",
      "LangGraph",
      "vLLM",
      "OpenWebUI",
      "RunPOD",
      "LightningAI",
      "Optuna"
    ]
  }
}
 
```



### 5. Validation
- Automatic JSON parsing with syntax validation
- Stats display: key count, experience entries, education entries
- Fallback to raw output if JSON is malformed

### 6. Integration Ready
- Download as `.json` file
- Compatible with react-pdf (pass JSON as props)
- Compatible with ReportLab (iterate JSON to place at x,y coordinates)
- Compatible with any PDF template engine

---

## IMPLEMENTATION DETAILS

### LLM Prompt
```
You are an expert technical writer and automated document generation engineer.
Convert the following professional experience into a clean, structured JSON
format suitable for automated PDF rendering.

Template style: {style}
Custom sections: {sections}

Requirements:
- Map ALL name-entities to specific keys
- Keep text professional, concise, and ATS-friendly
- Output ONLY valid JSON

JSON structure:
- header: { name, title, email, phone, linkedin, location }
- summary: string
- experience: array of { title, company, dates, highlights: [...] }
- skills: { languages, frameworks, tools, domains }
- education: array of { degree, school, year }
```

### UI Layout
- Two-column split: raw CV input (left) + options (right)
- Template style dropdown with 5 options
- Custom sections text input (comma-separated)
- Extra context text area for fine-tuning
- JSON preview in expandable `st.json()` viewer
- Download button for `.json` file

### Token Budget
- 1500 output tokens allocated
- Cost tracked in session budget

---

## INTEGRATION GUIDE

### With react-pdf (Frontend)
```jsx
import { Document, Page, Text, View, StyleSheet } from '@react-pdf/renderer';

const CVTemplate = ({ data }) => (
  <Document>
    <Page>
      <View style={styles.header}>
        <Text>{data.header.name}</Text>
        <Text>{data.header.email}</Text>
      </View>
      {data.experience.map((exp, i) => (
        <View key={i}>
          <Text>{exp.title} at {exp.company}</Text>
          {exp.highlights.map((h, j) => <Text key={j}>• {h}</Text>)}
        </View>
      ))}
    </Page>
  </Document>
);
```

### With ReportLab (Python Backend)
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def render_cv(json_data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    y = 750  # start from top
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, json_data["header"]["name"])
    y -= 30
    for exp in json_data.get("experience", []):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{exp['title']} | {exp['company']}")
        y -= 20
        for h in exp.get("highlights", []):
            c.setFont("Helvetica", 10)
            c.drawString(70, y, f"• {h}")
            y -= 15
    c.save()
```

---

## FILES MODIFIED

| File | Changes |
|------|---------|
| `main_dashboard.py` | Added "JSON CV Mapper" tool (~120 lines) |
| `config.py` | Added `json_cv_mapper` token budget |
| `phase-4.md` | This document |

---

**End of Phase 4 Report**
