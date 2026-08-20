"""
Resume Extractor Module: Extracts structured entities from resume text:
Contact information, skills breakdown, section segments, education, and metrics.
"""

import re
from typing import Dict, Any, List, Set
from app.core.skills_database import SKILLS_TAXONOMY, ALL_SKILLS_SET, ALL_ACTION_VERBS, WEAK_WORDS


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
LINKEDIN_REGEX = re.compile(r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(?:in|profile)\/([a-zA-Z0-9_-]+)", re.IGNORECASE)
GITHUB_REGEX = re.compile(r"(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_-]+)", re.IGNORECASE)
PORTFOLIO_REGEX = re.compile(r"(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+\.(?:dev|io|me|tech|app|com|org|net))(?:\/[^\s]*)?", re.IGNORECASE)

METRIC_PATTERNS = [
    re.compile(r"\b\d+%\b"),                      # e.g., 40%, 99.9%
    re.compile(r"\$\s?\d+(?:[.,]\d+)?\s?[kKmMbB]?"), # e.g., $1.5M, $500k, $200
    re.compile(r"\b\d+x\b", re.IGNORECASE),       # e.g., 10x, 3x
    re.compile(r"\b\d{1,3}(?:,\d{3})+\b"),        # e.g., 50,000, 1,000,000
    re.compile(r"\b(?:reduced|increased|boosted|saved|grew|accelerated|improved)\s+by\s+\d+", re.IGNORECASE),
    re.compile(r"\b\d+\+?\s*(?:users|clients|customers|engineers|members|downloads|requests|qps|rps|stars)\b", re.IGNORECASE)
]

SECTION_HEADERS = {
    "experience": ["experience", "work experience", "employment history", "work history", "professional experience"],
    "education": ["education", "academic background", "academics", "qualifications", "educational background"],
    "skills": ["skills", "technical skills", "core competencies", "technologies", "skill set", "tools & technologies"],
    "projects": ["projects", "personal projects", "academic projects", "key projects", "notable projects"],
    "certifications": ["certifications", "certificates", "licenses", "courses", "professional certifications"],
    "summary": ["summary", "professional summary", "executive summary", "about me", "profile", "objective", "career objective"]
}


def extract_contact_info(text: str, lines: List[str]) -> Dict[str, Any]:
    """Extract candidate name, email, phone, and links."""
    emails = EMAIL_REGEX.findall(text)
    phones = PHONE_REGEX.findall(text)
    linkedin = LINKEDIN_REGEX.findall(text)
    github = GITHUB_REGEX.findall(text)
    
    # Extract website/portfolio (filtering out common email or git domains)
    urls = []
    for match in PORTFOLIO_REGEX.findall(text):
        if match.lower() not in ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "linkedin.com", "github.com"]:
            urls.append(match)

    # Name heuristic: inspect first 5 non-empty lines
    candidate_name = "Candidate"
    ignore_name_words = {
        "resume", "curriculum", "vitae", "cv", "page", "email", "phone", "contact",
        "profile", "summary", "experience", "education", "skills", "projects", "software", "engineer"
    }
    for line in lines[:6]:
        cleaned_line = line.strip()
        # Look for a line with 2-4 words, mostly alphabetic and Title-cased
        words = cleaned_line.split()
        if 2 <= len(words) <= 4:
            if not any(w.lower() in ignore_name_words for w in words):
                if all(w.replace(".", "").isalpha() for w in words):
                    candidate_name = cleaned_line
                    break

    return {
        "name": candidate_name,
        "email": emails[0] if emails else None,
        "all_emails": list(set(emails)),
        "phone": phones[0] if phones else None,
        "linkedin": f"linkedin.com/in/{linkedin[0]}" if linkedin else None,
        "github": f"github.com/{github[0]}" if github else None,
        "portfolio": urls[0] if urls else None
    }


def extract_skills(text: str) -> Dict[str, Any]:
    """
    Extract skills from text categorized by taxonomy.
    Uses regex word boundaries to avoid false positives.
    """
    text_lower = f" {text.lower()} "
    # Replace punctuation for clean tokenization
    normalized_text = re.sub(r"[,\(\)\[\]\{\}\/\|;]", " ", text_lower)
    
    found_by_category = {}
    found_all: Set[str] = set()

    for category, skill_list in SKILLS_TAXONOMY.items():
        matched_in_category = []
        for skill in skill_list:
            skill_clean = skill.lower()
            # Handle special characters in skill names (e.g., c++, c#, .net, node.js)
            pattern = r"(?:\b|(?<=\s))" + re.escape(skill_clean) + r"(?:\b|(?=\s))"
            if re.search(pattern, normalized_text):
                matched_in_category.append(skill.title() if len(skill) > 3 else skill.upper())
                found_all.add(skill_clean)
        if matched_in_category:
            found_by_category[category] = matched_in_category

    # Distinguish Hard vs Soft skills
    soft_skills = found_by_category.get("Soft Skills & Leadership", [])
    hard_skills_count = sum(
        len(skills) for cat, skills in found_by_category.items()
        if cat != "Soft Skills & Leadership"
    )

    return {
        "categorized": found_by_category,
        "all_skills": sorted(list(found_all)),
        "total_skills_count": len(found_all),
        "hard_skills_count": hard_skills_count,
        "soft_skills": soft_skills,
        "soft_skills_count": len(soft_skills)
    }


def extract_sections(lines: List[str]) -> Dict[str, List[str]]:
    """Partition lines into recognized resume sections."""
    sections: Dict[str, List[str]] = {key: [] for key in SECTION_HEADERS}
    sections["other"] = []
    
    current_section = "summary"
    
    for line in lines:
        line_clean = line.strip().lower()
        # Remove trailing punctuation or colons
        header_candidate = re.sub(r"[:\-_#\*\d\.]", "", line_clean).strip()
        
        matched_header = None
        for section_key, aliases in SECTION_HEADERS.items():
            if header_candidate in aliases or any(alias == header_candidate for alias in aliases):
                matched_header = section_key
                break
        
        if matched_header:
            current_section = matched_header
        else:
            sections[current_section].append(line)
            
    return sections


def extract_metrics_and_action_verbs(bullet_points: List[str], raw_text: str) -> Dict[str, Any]:
    """Find quantifiable metrics and evaluate action verb usage across bullet points."""
    quantified_bullets = []
    unquantified_bullets = []
    active_bullets = []
    weak_bullets = []
    
    verbs_used: Set[str] = set()
    weak_phrases_found: Set[str] = set()
    
    for bp in bullet_points:
        bp_lower = bp.lower()
        first_word = re.sub(r"[^a-zA-Z]", "", bp_lower.split()[0]) if bp_lower.split() else ""
        
        # Check action verbs
        has_action_verb = first_word in ALL_ACTION_VERBS
        if has_action_verb:
            verbs_used.add(first_word)
            active_bullets.append(bp)
            
        # Check weak phrases
        has_weak = any(wp in bp_lower for wp in WEAK_WORDS)
        if has_weak:
            weak_bullets.append(bp)
            for wp in WEAK_WORDS:
                if wp in bp_lower:
                    weak_phrases_found.add(wp)
                    
        # Check quantifiable metrics
        has_metric = any(pat.search(bp) for pat in METRIC_PATTERNS)
        if has_metric:
            quantified_bullets.append(bp)
        else:
            unquantified_bullets.append(bp)

    return {
        "quantified_count": len(quantified_bullets),
        "unquantified_count": len(unquantified_bullets),
        "quantified_bullets": quantified_bullets,
        "unquantified_bullets": unquantified_bullets,
        "action_verbs_used": sorted(list(verbs_used)),
        "action_verb_count": len(verbs_used),
        "weak_phrases_found": sorted(list(weak_phrases_found)),
        "weak_bullets_count": len(weak_bullets)
    }


def extract_full_profile(document_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run full extraction pipeline on document data."""
    raw_text = document_data.get("raw_text", "")
    lines = document_data.get("lines", [])
    bullet_points = document_data.get("bullet_points", [])

    contact = extract_contact_info(raw_text, lines)
    skills_data = extract_skills(raw_text)
    sections = extract_sections(lines)
    metrics_data = extract_metrics_and_action_verbs(bullet_points, raw_text)

    # Detect present sections
    present_sections = [
        sec for sec, sec_lines in sections.items()
        if sec != "other" and len(sec_lines) > 0
    ]

    return {
        "contact": contact,
        "skills": skills_data,
        "sections": {k: len(v) for k, v in sections.items()},
        "present_sections": present_sections,
        "metrics": metrics_data,
        "document_stats": {
            "word_count": document_data.get("word_count", 0),
            "character_count": document_data.get("character_count", 0),
            "line_count": document_data.get("line_count", 0),
            "bullet_count": len(bullet_points)
        }
    }
