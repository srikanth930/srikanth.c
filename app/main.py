"""
AI Resume Analyser and Job Assistant - FastAPI Web Application
"""

import json
import os
from typing import Optional, List
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.config import (
    APP_TITLE, APP_DESCRIPTION, APP_VERSION,
    STATIC_DIR, TEMPLATES_DIR, SAMPLE_DIR
)
from app.core.parser import extract_resume_document
from app.core.extractor import extract_full_profile
from app.core.scorer import calculate_ats_score
from app.core.matcher import analyze_job_description_match
from app.core.ai_assistant import AIAssistant

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Mount Static Files & Templates
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# -----------------------------------------------------------------
# Request Models
# -----------------------------------------------------------------
class CoverLetterRequest(BaseModel):
    profile: dict
    job_title: Optional[str] = "Target Role"
    company_name: Optional[str] = "Hiring Team"
    job_description: Optional[str] = ""
    api_key: Optional[str] = None


class InterviewPrepRequest(BaseModel):
    profile: dict
    job_title: Optional[str] = "Software Professional"
    job_description: Optional[str] = ""
    api_key: Optional[str] = None


class ColdOutreachRequest(BaseModel):
    profile: dict
    job_title: Optional[str] = "Target Role"
    company_name: Optional[str] = "Company"
    recruiter_name: Optional[str] = "Hiring Manager"


class BulletRewriteRequest(BaseModel):
    bullet_points: List[str]


class CareerRoadmapRequest(BaseModel):
    missing_skills: List[str]
    target_role: Optional[str] = "Target Position"


# -----------------------------------------------------------------
# Web Page Routes
# -----------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render landing page with upload zone and sample selector."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_title": APP_TITLE,
            "app_version": APP_VERSION
        }
    )


@app.post("/analyze-form", response_class=HTMLResponse)
async def analyze_form(
    request: Request,
    resume_file: Optional[UploadFile] = File(None),
    job_description: Optional[str] = Form(""),
    sample_id: Optional[str] = Form(None)
):
    """Process form submission and render comprehensive interactive results dashboard."""
    file_bytes = None
    filename = "resume.txt"

    if resume_file and resume_file.filename:
        filename = resume_file.filename
        file_bytes = await resume_file.read()
    elif sample_id:
        sample_path = SAMPLE_DIR / f"{sample_id}.txt"
        if sample_path.exists():
            filename = f"{sample_id}.txt"
            file_bytes = sample_path.read_bytes()
        else:
            raise HTTPException(status_code=404, detail="Sample resume not found.")
    else:
        raise HTTPException(status_code=400, detail="Please upload a resume file or select a sample.")

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # 1. Parse Document
    doc_data = extract_resume_document(file_bytes, filename)
    # 2. Extract Profile
    profile = extract_full_profile(doc_data)
    # 3. ATS Scoring
    ats_score_data = calculate_ats_score(profile)
    # 4. Job Description Matcher
    jd_match_data = analyze_job_description_match(
        {"raw_text": doc_data["raw_text"], "skills": profile["skills"]},
        job_description or ""
    )
    # 5. Pre-generate assistant assets
    assistant = AIAssistant()
    candidate_role = "Senior Software Engineer"
    if jd_match_data.get("has_jd"):
        candidate_role = "Target Position"
        
    cover_letter = assistant.generate_cover_letter(
        profile,
        job_title=candidate_role,
        company_name="Prospective Employer",
        job_description=job_description or ""
    )
    interview_questions = assistant.generate_interview_prep(
        profile,
        job_title=candidate_role,
        job_description=job_description or ""
    )
    cold_outreach = assistant.generate_cold_outreach(
        profile,
        job_title=candidate_role,
        company_name="Target Company"
    )
    bullet_enhancements = assistant.generate_bullet_enhancements(
        profile.get("metrics", {}).get("unquantified_bullets", []) or doc_data.get("bullet_points", [])
    )
    missing_for_roadmap = jd_match_data.get("missing_skills", []) if jd_match_data.get("has_jd") else ["Cloud Architecture (AWS)", "Docker & Kubernetes", "System Design"]
    career_roadmap = assistant.generate_career_roadmap(missing_for_roadmap)

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "app_title": APP_TITLE,
            "filename": filename,
            "doc_data": doc_data,
            "profile": profile,
            "ats_score": ats_score_data,
            "jd_match": jd_match_data,
            "cover_letter": cover_letter,
            "interview_questions": interview_questions,
            "cold_outreach": cold_outreach,
            "bullet_enhancements": bullet_enhancements,
            "career_roadmap": career_roadmap,
            "job_description_raw": job_description or ""
        }
    )


# -----------------------------------------------------------------
# REST API Endpoints
# -----------------------------------------------------------------
@app.post("/api/analyze")
async def api_analyze_resume(
    file: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None),
    job_description: Optional[str] = Form(""),
    api_key: Optional[str] = Form(None)
):
    """REST API endpoint returning complete JSON analytics."""
    if file and file.filename:
        filename = file.filename
        file_bytes = await file.read()
    elif sample_id:
        sample_path = SAMPLE_DIR / f"{sample_id}.txt"
        if sample_path.exists():
            filename = f"{sample_id}.txt"
            file_bytes = sample_path.read_bytes()
        else:
            raise HTTPException(status_code=404, detail="Sample resume not found.")
    else:
        raise HTTPException(status_code=400, detail="Missing resume file or sample ID.")

    doc_data = extract_resume_document(file_bytes, filename)
    profile = extract_full_profile(doc_data)
    ats_score = calculate_ats_score(profile)
    jd_match = analyze_job_description_match(
        {"raw_text": doc_data["raw_text"], "skills": profile["skills"]},
        job_description or ""
    )

    return JSONResponse(content={
        "status": "success",
        "document": {
            "filename": filename,
            "file_type": doc_data["file_type"],
            "stats": profile["document_stats"]
        },
        "profile": {
            "contact": profile["contact"],
            "skills": profile["skills"],
            "metrics": {
                "quantified_count": profile["metrics"]["quantified_count"],
                "unquantified_count": profile["metrics"]["unquantified_count"],
                "action_verbs": profile["metrics"]["action_verbs_used"]
            }
        },
        "ats_scoring": ats_score,
        "job_match": jd_match
    })


@app.post("/api/generate-cover-letter")
async def api_cover_letter(req: CoverLetterRequest):
    assistant = AIAssistant(api_key=req.api_key)
    letter = assistant.generate_cover_letter(
        req.profile,
        job_title=req.job_title or "Target Role",
        company_name=req.company_name or "Hiring Team",
        job_description=req.job_description or ""
    )
    return {"cover_letter": letter}


@app.post("/api/interview-prep")
async def api_interview_prep(req: InterviewPrepRequest):
    assistant = AIAssistant(api_key=req.api_key)
    questions = assistant.generate_interview_prep(
        req.profile,
        job_title=req.job_title or "Software Professional",
        job_description=req.job_description or ""
    )
    return {"interview_questions": questions}


@app.post("/api/cold-outreach")
async def api_cold_outreach(req: ColdOutreachRequest):
    assistant = AIAssistant()
    outreach = assistant.generate_cold_outreach(
        req.profile,
        job_title=req.job_title or "Target Role",
        company_name=req.company_name or "Company",
        recruiter_name=req.recruiter_name or "Hiring Manager"
    )
    return outreach


@app.post("/api/bullet-rewrites")
async def api_bullet_rewrites(req: BulletRewriteRequest):
    assistant = AIAssistant()
    enhancements = assistant.generate_bullet_enhancements(req.bullet_points)
    return {"enhancements": enhancements}


@app.post("/api/career-roadmap")
async def api_career_roadmap(req: CareerRoadmapRequest):
    assistant = AIAssistant()
    roadmap = assistant.generate_career_roadmap(req.missing_skills, req.target_role or "Target Position")
    return {"roadmap": roadmap}
