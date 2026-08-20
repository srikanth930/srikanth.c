"""
ATS Scoring Engine: Evaluates resumes across 5 key pillars:
1. Section Completeness & Contact Health (20%)
2. Quantifiable Impact & Metrics (25%)
3. Action Verb & Voice Strength (20%)
4. Skills Density & Taxonomy Distribution (20%)
5. Readability, Formatting & Length (15%)
"""

import math
from typing import Dict, Any, List


def calculate_readability_and_length(word_count: int, lines: List[str]) -> Dict[str, Any]:
    """Evaluate resume word count, page density, and sentence structure."""
    # Ideal single/two-page resume word count: 400 - 900 words
    if 450 <= word_count <= 850:
        score = 15
        status = "Optimal"
        message = f"Perfect word count ({word_count} words). Concise and recruiter-friendly."
    elif 300 <= word_count < 450:
        score = 11
        status = "Slightly Short"
        message = f"Resume is {word_count} words. Consider adding more details on project outcomes and achievements."
    elif 850 < word_count <= 1200:
        score = 11
        status = "Slightly Long"
        message = f"Resume is {word_count} words. Consider condensing older roles to maintain high signal-to-noise ratio."
    elif word_count < 300:
        score = 6
        status = "Too Short"
        message = f"Resume contains only {word_count} words. It may lack sufficient detail for ATS screening."
    else:
        score = 7
        status = "Too Long"
        message = f"Resume is {word_count} words. High risk of ATS truncation and recruiter fatigue."

    return {
        "score": score,
        "max_score": 15,
        "status": status,
        "message": message,
        "word_count": word_count
    }


def calculate_ats_score(extracted_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes a weighted, multi-dimensional ATS score out of 100
    along with granular feedback and actionable tips.
    """
    contact = extracted_profile.get("contact", {})
    skills_data = extracted_profile.get("skills", {})
    metrics_data = extracted_profile.get("metrics", {})
    doc_stats = extracted_profile.get("document_stats", {})
    present_sections = extracted_profile.get("present_sections", [])

    suggestions: List[Dict[str, str]] = []
    strengths: List[str] = []

    # -------------------------------------------------------------
    # 1. Section Completeness & Contact Health (Max: 20 pts)
    # -------------------------------------------------------------
    section_score = 0
    if contact.get("email"):
        section_score += 4
    else:
        suggestions.append({
            "type": "critical",
            "category": "Contact Info",
            "text": "Missing candidate email address. Recruiters and ATS require a direct email contact."
        })

    if contact.get("phone"):
        section_score += 3
    else:
        suggestions.append({
            "type": "warning",
            "category": "Contact Info",
            "text": "No phone number detected. Ensure a standard formatted phone number is present."
        })

    if contact.get("linkedin"):
        section_score += 3
        strengths.append("Includes LinkedIn profile link for recruiter validation.")
    else:
        suggestions.append({
            "type": "suggestion",
            "category": "Online Presence",
            "text": "Add your customized LinkedIn URL (e.g., linkedin.com/in/yourname) in the header."
        })

    if contact.get("github") or contact.get("portfolio"):
        section_score += 2
        strengths.append("Includes GitHub or technical portfolio link.")

    # Check key resume sections
    if "experience" in present_sections:
        section_score += 3
    else:
        suggestions.append({
            "type": "critical",
            "category": "Structure",
            "text": "Work Experience section not clearly recognized. Use standard headings like 'Work Experience'."
        })

    if "education" in present_sections:
        section_score += 2
    if "skills" in present_sections:
        section_score += 3
    else:
        suggestions.append({
            "type": "critical",
            "category": "Structure",
            "text": "Dedicated 'Skills' section missing. Group hard skills into a clear section for ATS keyword scanners."
        })

    section_score = min(20, section_score)

    # -------------------------------------------------------------
    # 2. Quantifiable Impact & Metrics (Max: 25 pts)
    # -------------------------------------------------------------
    quantified_count = metrics_data.get("quantified_count", 0)
    unquantified_count = metrics_data.get("unquantified_count", 0)
    total_bullets = quantified_count + unquantified_count

    if total_bullets == 0:
        impact_score = 5
        suggestions.append({
            "type": "critical",
            "category": "Impact",
            "text": "No clear bullet points detected. Structure your experience with bullet points highlighting accomplishments."
        })
    else:
        quantified_ratio = quantified_count / total_bullets
        if quantified_ratio >= 0.5:
            impact_score = 25
            strengths.append(f"Outstanding quantifiable impact ({quantified_count} metric-driven achievements detected).")
        elif quantified_ratio >= 0.3:
            impact_score = 19
            strengths.append(f"Good use of numbers/metrics ({quantified_count} quantified bullet points).")
            suggestions.append({
                "type": "suggestion",
                "category": "Impact",
                "text": "Increase quantifiable results (%, $, user scale) in remaining experience bullet points."
            })
        elif quantified_ratio >= 0.15:
            impact_score = 13
            suggestions.append({
                "type": "warning",
                "category": "Impact",
                "text": f"Only {quantified_count} of your {total_bullets} bullet points contain numbers or measurable outcomes."
            })
        else:
            impact_score = 7
            suggestions.append({
                "type": "critical",
                "category": "Impact",
                "text": "Resume is heavily task-focused rather than result-focused. Add metrics like '% efficiency boost', 'latency cut by X ms', or 'revenue generated'."
            })

    # -------------------------------------------------------------
    # 3. Action Verbs & Voice Strength (Max: 20 pts)
    # -------------------------------------------------------------
    action_verb_count = metrics_data.get("action_verb_count", 0)
    weak_phrases = metrics_data.get("weak_phrases_found", [])

    if action_verb_count >= 8:
        verb_score = 20
        strengths.append(f"Strong, varied action verbs ({action_verb_count} distinct power verbs identified).")
    elif action_verb_count >= 4:
        verb_score = 15
        strengths.append(f"Solid active voice across bullet points ({action_verb_count} action verbs).")
    elif action_verb_count >= 2:
        verb_score = 10
        suggestions.append({
            "type": "warning",
            "category": "Action Verbs",
            "text": "Begin every bullet point with strong power verbs like 'Architected', 'Spearheaded', 'Optimized', or 'Automated'."
        })
    else:
        verb_score = 5
        suggestions.append({
            "type": "critical",
            "category": "Action Verbs",
            "text": "Lacks strong action verbs. Avoid passive phrasing and lead with direct impact words."
        })

    if weak_phrases:
        verb_score = max(0, verb_score - (len(weak_phrases) * 2))
        suggestions.append({
            "type": "warning",
            "category": "Weak Phrasing",
            "text": f"Remove passive cliché phrases: {', '.join(f'\"{w}\"' for w in weak_phrases[:3])}."
        })

    # -------------------------------------------------------------
    # 4. Skills Density & Categorization (Max: 20 pts)
    # -------------------------------------------------------------
    total_skills = skills_data.get("total_skills_count", 0)
    hard_skills = skills_data.get("hard_skills_count", 0)
    soft_skills = skills_data.get("soft_skills_count", 0)
    categorized_count = len(skills_data.get("categorized", {}))

    if total_skills >= 15 and categorized_count >= 3:
        skills_score = 20
        strengths.append(f"Comprehensive skill coverage ({total_skills} verified skills across {categorized_count} technical domains).")
    elif total_skills >= 8:
        skills_score = 15
        strengths.append(f"Good core skills identified ({total_skills} skills).")
    elif total_skills >= 4:
        skills_score = 10
        suggestions.append({
            "type": "warning",
            "category": "Keywords",
            "text": f"Only {total_skills} industry keywords detected. Expand your technologies, tools, and libraries list."
        })
    else:
        skills_score = 5
        suggestions.append({
            "type": "critical",
            "category": "Keywords",
            "text": "Very low technical skill keyword density. Modern ATS relies heavily on explicit skill matches."
        })

    # -------------------------------------------------------------
    # 5. Length & Readability (Max: 15 pts)
    # -------------------------------------------------------------
    readability = calculate_readability_and_length(
        doc_stats.get("word_count", 0),
        extracted_profile.get("lines", [])
    )
    readability_score = readability["score"]
    if readability_score >= 14:
        strengths.append(readability["message"])
    else:
        suggestions.append({
            "type": "suggestion",
            "category": "Length & Readability",
            "text": readability["message"]
        })

    # -------------------------------------------------------------
    # Total Calculation & Grade
    # -------------------------------------------------------------
    total_ats_score = section_score + impact_score + verb_score + skills_score + readability_score
    total_ats_score = max(0, min(100, total_ats_score))

    if total_ats_score >= 85:
        rating_badge = "Excellent (Top 10%)"
        rating_color = "emerald"
    elif total_ats_score >= 70:
        rating_badge = "Competitive (Above Average)"
        rating_color = "teal"
    elif total_ats_score >= 50:
        rating_badge = "Needs Polish (Moderate Match)"
        rating_color = "amber"
    else:
        rating_badge = "High ATS Risk (Action Required)"
        rating_color = "rose"

    return {
        "overall_score": total_ats_score,
        "rating_badge": rating_badge,
        "rating_color": rating_color,
        "breakdown": {
            "section_completeness": {
                "score": section_score,
                "max": 20,
                "percentage": int((section_score / 20) * 100),
                "label": "Sections & Contact"
            },
            "impact_and_metrics": {
                "score": impact_score,
                "max": 25,
                "percentage": int((impact_score / 25) * 100),
                "label": "Quantifiable Impact"
            },
            "action_verbs": {
                "score": verb_score,
                "max": 20,
                "percentage": int((verb_score / 20) * 100),
                "label": "Action Verb Strength"
            },
            "skills_density": {
                "score": skills_score,
                "max": 20,
                "percentage": int((skills_score / 20) * 100),
                "label": "Skills & Keywords"
            },
            "readability": {
                "score": readability_score,
                "max": 15,
                "percentage": int((readability_score / 15) * 100),
                "label": "Length & Readability"
            }
        },
        "strengths": strengths,
        "suggestions": suggestions
    }
