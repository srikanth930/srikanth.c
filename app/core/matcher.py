"""
Job Description Matcher & Keyword Gap Analysis Module:
Compares parsed resume against target Job Description (JD) to calculate match %,
identify missing hard/soft skills, and deliver actionable alignment advice.
"""

import re
from typing import Dict, Any, List, Set
from app.core.extractor import extract_skills


def analyze_job_description_match(resume_data: Dict[str, Any], job_description_text: str) -> Dict[str, Any]:
    """
    Compares candidate resume text and extracted skills against target JD text.
    """
    if not job_description_text or not job_description_text.strip():
        return {
            "has_jd": False,
            "match_percentage": None,
            "message": "No Job Description provided for targeted comparison."
        }

    # Extract skills present in the Job Description
    jd_skills_data = extract_skills(job_description_text)
    jd_skills_set = set(jd_skills_data.get("all_skills", []))
    
    resume_skills_data = resume_data.get("skills", {})
    resume_skills_set = set(resume_skills_data.get("all_skills", []))

    # Matched & Missing Skills
    matched_skills = sorted(list(resume_skills_set.intersection(jd_skills_set)))
    missing_skills = sorted(list(jd_skills_set - resume_skills_set))
    extra_skills = sorted(list(resume_skills_set - jd_skills_set))

    # Categorize missing skills
    missing_by_category: Dict[str, List[str]] = {}
    for category, cat_skills in jd_skills_data.get("categorized", {}).items():
        missing_in_cat = [s for s in cat_skills if s.lower() in missing_skills]
        if missing_in_cat:
            missing_by_category[category] = missing_in_cat

    # Calculate match percentage
    if len(jd_skills_set) > 0:
        skill_match_ratio = len(matched_skills) / len(jd_skills_set)
    else:
        skill_match_ratio = 0.5  # Neutral default if no specific taxonomy skills detected

    # Calculate broad vocabulary / token overlap (excluding common stop words)
    stop_words = {
        "and", "the", "to", "of", "in", "for", "with", "a", "an", "is", "on", "that", "by", "this",
        "you", "we", "our", "are", "as", "at", "be", "from", "or", "will", "your", "have", "experience",
        "work", "skills", "team", "role", "years", "working", "knowledge", "ability", "strong", "must"
    }
    
    def tokenize(txt: str) -> Set[str]:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", txt.lower())
        return {w for w in words if w not in stop_words}

    resume_tokens = tokenize(resume_data.get("raw_text", ""))
    jd_tokens = tokenize(job_description_text)
    
    token_overlap = len(resume_tokens.intersection(jd_tokens))
    token_ratio = (token_overlap / len(jd_tokens)) if jd_tokens else 0.5

    # Blended Match Score: 70% skill match + 30% general semantic keyword match
    blended_score = int(round((skill_match_ratio * 0.70 + token_ratio * 0.30) * 100))
    match_percentage = max(10, min(99, blended_score))

    # Fit level
    if match_percentage >= 80:
        fit_level = "Strong Match"
        fit_color = "emerald"
        fit_message = "Your background is strongly aligned with this job posting. Highlight your matching achievements."
    elif match_percentage >= 60:
        fit_level = "Moderate Match"
        fit_color = "teal"
        fit_message = "Good baseline match. Incorporating top missing keywords into your experience bullets will boost interview calls."
    elif match_percentage >= 40:
        fit_level = "Partial Match"
        fit_color = "amber"
        fit_message = "Some overlap, but critical qualifications or tech stack skills are missing from your resume."
    else:
        fit_level = "Low Alignment / Stretch Role"
        fit_color = "rose"
        fit_message = "Significant skill gaps. Consider targeting adjacent roles or upskilling on key missing technologies."

    # Top priority missing keywords
    priority_missing = missing_skills[:8]

    return {
        "has_jd": True,
        "match_percentage": match_percentage,
        "fit_level": fit_level,
        "fit_color": fit_color,
        "fit_message": fit_message,
        "matched_skills": [s.title() if len(s) > 3 else s.upper() for s in matched_skills],
        "matched_count": len(matched_skills),
        "missing_skills": [s.title() if len(s) > 3 else s.upper() for s in missing_skills],
        "missing_count": len(missing_skills),
        "missing_by_category": missing_by_category,
        "priority_missing": [s.title() if len(s) > 3 else s.upper() for s in priority_missing],
        "extra_skills": [s.title() if len(s) > 3 else s.upper() for s in extra_skills[:10]],
        "jd_skills_count": len(jd_skills_set)
    }
