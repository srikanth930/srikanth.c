# 🚀 AI Resume Analyser & Job Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Modern UI](https://img.shields.io/badge/UI-Glassmorphic%20Design-6366f1.svg)](https://github.com)
[![Status](https://img.shields.io/badge/Status-Active%20%26%20Ready-emerald.svg)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <strong>An intelligent, full-stack ATS Resume Analyser, Keyword Matcher & AI Career Acceleration Copilot.</strong>
</p>

</div>

---

## 📖 Overview

**AI Resume Analyser & Job Assistant** evaluates resumes against modern Applicant Tracking System (ATS) benchmarks, performs keyword gap analysis against target job postings, and provides a full generative career toolkit (Tailored Cover Letters, STAR Interview Prep, Cold Outreach Drafter, Metric-Driven Bullet Enhancer, and 3-Phase Upskilling Roadmap).

> [!TIP]
> **Zero API Key Requirement:** Includes a high-precision, rule-based NLP heuristic engine that works 100% offline out-of-the-box, with optional Gemini/OpenAI cloud integration.

---

## 🌟 Key Features

### 1. 📊 Multi-Pillar ATS Scoring Engine (0–100 Score)
- **Section Completeness & Contact Health (20%)**: Validates email, phone, LinkedIn, GitHub, and standard resume headers.
- **Quantifiable Impact & Metrics (25%)**: Detects percentages, dollar figures, multipliers, and scale numbers.
- **Action Verbs & Voice Strength (20%)**: Identifies strong power verbs vs. passive/weak clichés.
- **Skills Density & Breadth (20%)**: 1,000+ categorized skill taxonomies (Languages, Frameworks, Cloud, Databases, AI, Soft Skills).
- **Readability & Length (15%)**: Evaluates word count, bullet length, and formatting risk.

### 2. 🎯 Job Description Matcher & Keyword Gap Analysis
- Calculates target role match percentage score.
- Highlights critical missing hard skills and keywords.
- Delivers actionable tips to customize your resume for specific job descriptions.

### 3. 🤖 AI Job Assistant Suite
- **Tailored Cover Letter Generator**: Creates persuasive 3-4 paragraph letters highlighting verified achievements.
- **STAR Interview Prep**: Generates role-specific behavioral and technical questions with complete Situation-Task-Action-Result answers.
- **Cold Outreach Drafter**: Crafts concise (under 300 character) LinkedIn connection notes, recruiter InMails, and executive cold emails.
- **Bullet Point Optimizer**: Rewrites weak bullets into quantified STAR achievements.
- **3-Phase Skill Roadmap**: Week-by-week upskilling milestones for missing competencies.

### 4. 🎨 Modern Glassmorphic UI
- Dark and Light mode themes with persistence.
- Animated Chart.js ATS Gauge and Skill Domain Radar Chart.
- Instant 1-click test presets for Senior Full-Stack, AI Data Scientist, and Cloud DevOps Engineer.
- Print & PDF export ready.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI, Python 3.10+, Uvicorn, Jinja2 |
| **Document Parsing** | `pypdf`, `python-docx` |
| **Frontend** | Vanilla CSS (Glassmorphic Design System), Vanilla JavaScript, Chart.js, Lucide Icons |
| **AI / NLP** | Smart NLP heuristic engine + optional Google Gemini / OpenAI LLM integration |

---

## 📂 Project Structure

```text
CODE X/
├── .codesandbox/              # CodeSandbox devbox & browser preview configuration
│   └── tasks.json
├── .devcontainer/             # GitHub Codespaces automatic environment configuration
│   └── devcontainer.json
├── app/
│   ├── config.py              # Application settings & environment config
│   ├── main.py                # FastAPI routes & web endpoints
│   ├── core/
│   │   ├── ai_assistant.py    # Cover letter, STAR prep, cold outreach generator
│   │   ├── extractor.py       # Entity & contact info extraction
│   │   ├── matcher.py         # Job description matching & keyword gap engine
│   │   ├── parser.py          # PDF / DOCX / TXT multi-format document parser
│   │   ├── scorer.py          # 5-pillar ATS scoring calculation engine
│   │   └── skills_database.py # 1,000+ categorized skills taxonomies
│   ├── static/
│   │   ├── css/style.css      # Glassmorphism styling, 1-page report & print layout
│   │   └── js/
│   │       ├── app.js         # UI interactions, 1-page modal, drag & drop, tab switching
│   │       └── charts.js      # Chart.js ATS gauge & radar charts
│   └── templates/
│       ├── base.html          # Base layout template with header & footer
│       ├── index.html         # Main upload landing page
│       └── results.html       # Analytics dashboard, 1-page report & AI suite
├── sample_resumes/            # Sample resumes for 1-click testing
│   ├── ai-data-scientist.txt
│   ├── cloud-devops-engineer.txt
│   └── senior-software-engineer.txt
├── Dockerfile                 # Container image for Docker & cloud deployment
├── Procfile                   # Cloud process runner for Render/Heroku
├── sandbox.config.json        # CodeSandbox container template configuration
├── requirements.txt           # Project dependencies
├── run.py                     # Application runner script (0.0.0.0 host binding)
└── test_app.py                # Automated test suite
```

---

## 🚀 Quick Start

### Option A: Local Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Web Application:**
   ```bash
   python run.py
   ```

3. **Open in Browser:**
   ```text
   http://127.0.0.1:8000
   ```

### Option B: 1-Click Cloud Preview (CodeSandbox & GitHub Codespaces)

- **CodeSandbox**: Open the repository in [CodeSandbox](https://codesandbox.io). CodeSandbox automatically reads `.codesandbox/tasks.json` and boots up the interactive browser preview on port 8000.
- **GitHub Codespaces**: On GitHub, click **Code** → **Codespaces** → **Create codespace on main**. Dependencies and port forwarding will launch automatically.

---

### Run Automated Tests
```bash
python test_app.py
```

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze` | Multipart form upload (`file`, `job_description`) returning full JSON analytics |
| `POST` | `/api/generate-cover-letter` | Generates tailored cover letter JSON |
| `POST` | `/api/interview-prep` | Generates STAR interview guide JSON |
| `POST` | `/api/cold-outreach` | Generates networking notes and emails |
| `POST` | `/api/bullet-rewrites` | Transforms unquantified bullets into STAR statements |
| `POST` | `/api/career-roadmap` | Generates 3-phase learning milestones |

---

## 📄 License

This project is licensed under the MIT License.
