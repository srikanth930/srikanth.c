"""
Comprehensive Test Suite for AI Resume Analyser & Job Assistant.
Tests parser, extractor, scorer, matcher, AI assistant, and FastAPI endpoints.
"""

from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.core.parser import extract_resume_document
from app.core.extractor import extract_full_profile
from app.core.scorer import calculate_ats_score
from app.core.matcher import analyze_job_description_match
from app.core.ai_assistant import AIAssistant

client = TestClient(app)
SAMPLE_DIR = Path(__file__).resolve().parent / "sample_resumes"


def test_core_pipeline():
    print("\n--- Testing Core NLP & Scoring Pipeline ---")
    sample_file = SAMPLE_DIR / "senior-software-engineer.txt"
    assert sample_file.exists(), "Sample file does not exist!"
    
    file_bytes = sample_file.read_bytes()
    doc_data = extract_resume_document(file_bytes, "senior-software-engineer.txt")
    
    assert doc_data["word_count"] > 100
    assert len(doc_data["bullet_points"]) >= 4
    print(f"[PASS] Parser: Extracted {doc_data['word_count']} words, {len(doc_data['bullet_points'])} bullet points.")

    profile = extract_full_profile(doc_data)
    assert profile["contact"]["name"] == "Alex Chen"
    assert profile["contact"]["email"] == "alex.chen@email.com"
    assert profile["skills"]["total_skills_count"] >= 10
    print(f"[PASS] Extractor: Found Candidate '{profile['contact']['name']}', {profile['skills']['total_skills_count']} skills, {profile['metrics']['quantified_count']} quantified metrics.")

    ats_score = calculate_ats_score(profile)
    assert ats_score["overall_score"] >= 75
    print(f"[PASS] ATS Scorer: Overall Score = {ats_score['overall_score']}/100, Badge = '{ats_score['rating_badge']}'.")

    # Match against a sample JD
    sample_jd = "Looking for a Lead Engineer with Python, FastAPI, React, AWS, Docker, Kubernetes, and PostgreSQL."
    jd_match = analyze_job_description_match(
        {"raw_text": doc_data["raw_text"], "skills": profile["skills"]},
        sample_jd
    )
    assert jd_match["has_jd"] is True
    assert jd_match["match_percentage"] >= 70
    print(f"[PASS] JD Matcher: Match Score = {jd_match['match_percentage']}%, Matched Skills = {len(jd_match['matched_skills'])}.")

    # AI Assistant Tools
    assistant = AIAssistant()
    cover_letter = assistant.generate_cover_letter(profile, "Senior Software Engineer", "TechCorp")
    assert "Alex Chen" in cover_letter
    assert "TechCorp" in cover_letter
    print("[PASS] AI Assistant: Cover Letter generated successfully.")

    interview_q = assistant.generate_interview_prep(profile, "Senior Software Engineer")
    assert len(interview_q) >= 4
    assert "star_sample_answer" in interview_q[0]
    print(f"[PASS] AI Assistant: Generated {len(interview_q)} STAR interview questions.")

    outreach = assistant.generate_cold_outreach(profile, "Lead Engineer", "Google")
    assert "linkedin_connection_note" in outreach
    assert len(outreach["linkedin_connection_note"]) <= 300
    print("[PASS] AI Assistant: Generated LinkedIn note under 300 characters.")


def test_fastapi_endpoints():
    print("\n--- Testing FastAPI Endpoints ---")
    
    # 1. Landing Page
    resp = client.get("/")
    assert resp.status_code == 200
    assert "ResumeAI" in resp.text
    print("[PASS] Endpoint GET / passed.")

    # 2. Form Submission with Sample ID
    resp = client.post("/analyze-form", data={"sample_id": "senior-software-engineer", "job_description": "Python, AWS, Docker"})
    assert resp.status_code == 200
    assert "Alex Chen" in resp.text
    assert "Overall ATS Readiness Score" in resp.text
    print("[PASS] Endpoint POST /analyze-form (HTML) passed.")

    # 3. REST API Analyze
    resp = client.post("/api/analyze", data={"sample_id": "ai-data-scientist", "job_description": "PyTorch, Python, NLP, LLM"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["profile"]["contact"]["name"] == "Sarah Jenkins"
    assert data["ats_scoring"]["overall_score"] > 60
    print("[PASS] Endpoint POST /api/analyze (JSON) passed.")


if __name__ == "__main__":
    test_core_pipeline()
    test_fastapi_endpoints()
    print("\n[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!")
