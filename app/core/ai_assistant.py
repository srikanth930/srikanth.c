"""
AI Job Assistant Suite:
Generates custom cover letters, role-specific interview prep with STAR answers,
cold outreach messages, bullet point rewrites, and career upskilling roadmaps.
Includes both an intelligent offline contextual engine and dynamic Gemini/OpenAI integration.
"""

import json
import os
import re
from typing import Dict, Any, List, Optional
import requests


class AIAssistant:
    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = provider.lower()

    def generate_cover_letter(self, profile: Dict[str, Any], job_title: str = "Target Role", company_name: str = "Hiring Team", job_description: str = "") -> str:
        """Generate a tailored, persuasive cover letter."""
        # Try LLM if configured
        if self.api_key:
            llm_result = self._call_llm_cover_letter(profile, job_title, company_name, job_description)
            if llm_result:
                return llm_result

        # Smart Contextual Offline Generator
        return self._generate_offline_cover_letter(profile, job_title, company_name, job_description)

    def generate_interview_prep(self, profile: Dict[str, Any], job_title: str = "Software Professional", job_description: str = "") -> List[Dict[str, Any]]:
        """Generate role-specific interview questions with STAR answers and recruiter tips."""
        if self.api_key:
            llm_result = self._call_llm_interview_prep(profile, job_title, job_description)
            if llm_result:
                return llm_result

        return self._generate_offline_interview_prep(profile, job_title, job_description)

    def generate_cold_outreach(self, profile: Dict[str, Any], job_title: str = "Target Role", company_name: str = "Company", recruiter_name: str = "Hiring Manager") -> Dict[str, str]:
        """Generate LinkedIn connection notes and cold email templates."""
        candidate_name = profile.get("contact", {}).get("name", "Candidate")
        skills = profile.get("skills", {}).get("all_skills", ["Software Engineering", "Problem Solving"])
        top_skills = ", ".join(s.title() for s in skills[:3]) if skills else "Full Stack Engineering"
        metrics = profile.get("metrics", {}).get("quantified_bullets", [])
        highlight_metric = metrics[0] if metrics else "driving measurable technical improvements"

        # LinkedIn Note (< 300 chars)
        linkedin_note = (
            f"Hi {recruiter_name}, I came across the {job_title} opening at {company_name} and was inspired by your team's work. "
            f"With hands-on experience in {top_skills}, I'd love to connect and share how I could contribute to your current roadmap. Best, {candidate_name}."
        )
        if len(linkedin_note) > 295:
            linkedin_note = (
                f"Hi {recruiter_name}, I saw the {job_title} role at {company_name}. "
                f"With expertise in {top_skills}, I'd love to connect and discuss how my background aligns with your team's goals. Best, {candidate_name}."
            )

        # InMail / Recruiter Direct Message
        inmail_msg = f"""Hi {recruiter_name},

I hope this message finds you well!

I have been following {company_name}'s recent developments and was thrilled to see your opening for the {job_title} position. 

Given my background specializing in {top_skills} and my track record of {highlight_metric.lower() if highlight_metric else 'delivering high-impact systems'}, I believe my skills would allow me to hit the ground running on your team.

I would welcome the opportunity to connect for a brief 10-minute conversation to learn more about your current technical priorities.

Thank you for your time and consideration!

Warm regards,
{candidate_name}
{profile.get('contact', {}).get('email', '')}
{profile.get('contact', {}).get('phone', '') or ''}"""

        # Cold Email to Hiring Manager
        cold_email = f"""Subject: Application / Quick Inquiry: {job_title} - {candidate_name}

Dear {recruiter_name},

I hope you are having a productive week.

I am writing to express my strong enthusiasm for the {job_title} role at {company_name}. Having closely followed {company_name}'s innovative work in the industry, I am eager to bring my expertise in {top_skills} to your engineering initiatives.

A few highlights of what I bring to the table:
• Proven technical proficiency across {top_skills}.
• Track record of delivering scalable solutions: {highlight_metric if highlight_metric else 'Architected performant systems with measurable user and performance gains.'}
• Strong dedication to clean code, agile execution, and cross-functional collaboration.

I have attached my resume for your review. Would you be open to a brief 10-15 minute introductory chat next week?

Thank you very much for your time and consideration.

Best regards,

{candidate_name}
{profile.get('contact', {}).get('email', '')}
{profile.get('contact', {}).get('linkedin', '')}
"""
        return {
            "linkedin_connection_note": linkedin_note,
            "recruiter_inmail": inmail_msg,
            "cold_email_to_manager": cold_email
        }

    def generate_bullet_enhancements(self, bullet_points: List[str]) -> List[Dict[str, str]]:
        """Rewrites weak or unquantified resume bullet points into high-impact STAR bullets."""
        enhanced = []
        action_verbs = ["Architected", "Spearheaded", "Engineered", "Optimized", "Automated", "Streamlined", "Pioneered"]

        for idx, bullet in enumerate(bullet_points[:6]):
            b_clean = bullet.strip().lstrip("•-* ").strip()
            if not b_clean:
                continue

            # Identify weakness
            weakness = "Lacks quantifiable metrics and strong active verb."
            if any(num in b_clean for num in ["%", "$", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                weakness = "Can be restructured for stronger executive impact using the Action + Context + Result formula."

            verb = action_verbs[idx % len(action_verbs)]
            
            # Formulate improved version
            improved = f"{verb} {b_clean[0].lower() + b_clean[1:] if len(b_clean) > 1 else b_clean}, resulting in a ~35% efficiency boost and improved system reliability."
            
            enhanced.append({
                "original": b_clean,
                "diagnosis": weakness,
                "improved": improved,
                "formula_tip": "Formula: Strong Action Verb + Specific Technology/Task + Measurable Business Outcome (% or $)"
            })

        return enhanced

    def generate_career_roadmap(self, missing_skills: List[str], target_role: str = "Target Position") -> List[Dict[str, Any]]:
        """Generate a structured 3-phase skill gap roadmap."""
        roadmap = []
        if not missing_skills:
            missing_skills = ["Advanced System Design", "Cloud Infrastructure (AWS/GCP)", "CI/CD & Container Orchestration"]

        chunks = [missing_skills[i:i + 2] for i in range(0, min(len(missing_skills), 6), 2)]
        if not chunks:
            chunks = [[missing_skills[0]]]

        phases = [
            ("Phase 1: Immediate Fundamentals (Weeks 1-3)", "High Priority", "emerald"),
            ("Phase 2: Practical Projects & Tooling (Weeks 4-6)", "Medium Priority", "teal"),
            ("Phase 3: Production Mastery & Architecture (Weeks 7-9)", "Advanced", "indigo")
        ]

        for i, chunk in enumerate(chunks[:3]):
            phase_title, priority, color = phases[i] if i < len(phases) else (f"Phase {i+1}", "Elective", "slate")
            skills_str = ", ".join(chunk)
            roadmap.append({
                "phase": phase_title,
                "priority": priority,
                "color": color,
                "skills_to_master": chunk,
                "recommended_actions": [
                    f"Complete hands-on tutorials and build a demo repo integrating {skills_str}.",
                    f"Implement real-world test cases and benchmarks showcasing {chunk[0]} on GitHub.",
                    f"Add concrete accomplishment bullet points mentioning {skills_str} on your resume."
                ]
            })

        return roadmap

    # ------------------------------------------------------------------
    # Offline Intelligent Generators
    # ------------------------------------------------------------------
    def _generate_offline_cover_letter(self, profile: Dict[str, Any], job_title: str, company_name: str, job_description: str) -> str:
        contact = profile.get("contact", {})
        name = contact.get("name", "Candidate Name")
        email = contact.get("email", "your.email@example.com")
        phone = contact.get("phone", "+1 (555) 000-0000")
        linkedin = contact.get("linkedin", "linkedin.com/in/yourprofile")
        
        skills_data = profile.get("skills", {})
        all_skills = skills_data.get("all_skills", [])
        top_skills = [s.title() for s in all_skills[:4]] if all_skills else ["Python", "System Design", "Cloud Computing"]
        skills_phrase = ", ".join(top_skills[:-1]) + f", and {top_skills[-1]}" if len(top_skills) > 1 else top_skills[0]

        metrics = profile.get("metrics", {}).get("quantified_bullets", [])
        highlight_achievement = metrics[0] if metrics else "delivered scalable solutions resulting in a 40% improvement in performance"

        return f"""{name}
{email} | {phone} | {linkedin}

Date: August 20, 2026

Hiring Team
{company_name}

Subject: Application for {job_title} position

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my comprehensive background in {skills_phrase} and a proven track record of engineering high-impact, reliable software solutions, I am excited about the opportunity to contribute directly to your team's mission and engineering excellence.

Throughout my career, I have focused on translating business requirements into robust, high-performance systems. In my previous work, I {highlight_achievement.lower().rstrip('.')}. My core philosophy centers on clean architecture, continuous improvement, and cross-functional synergy to ensure projects are delivered with high quality and on schedule.

What particularly excites me about {company_name} is your commitment to technical innovation and building solutions that deliver genuine value at scale. The requirements outlined for the {job_title} role closely align with my hands-on expertise in {top_skills[0]} and scalable system design. I am confident that my technical problem-solving abilities and collaborative mindset will allow me to make an immediate, positive impact on your roadmap.

I would welcome the opportunity to discuss how my skill set and enthusiasm align with your goals for this role. Thank you for your time, consideration, and review of my application.

Sincerely,

{name}
{email}
{phone}"""

    def _generate_offline_interview_prep(self, profile: Dict[str, Any], job_title: str, job_description: str) -> List[Dict[str, Any]]:
        skills = profile.get("skills", {}).get("all_skills", ["Python", "FastAPI", "Databases", "System Design"])
        top_tech = skills[0].title() if skills else "Python"
        second_tech = skills[1].title() if len(skills) > 1 else "Cloud Architecture"

        metrics = profile.get("metrics", {}).get("quantified_bullets", [])
        metric_hint = metrics[0] if metrics else "successfully optimized a critical application subsystem under strict deadlines"

        questions = [
            {
                "category": "Behavioral (STAR Method)",
                "difficulty": "Medium",
                "question": f"Can you describe a challenging technical obstacle you faced while building a system with {top_tech}, and how you resolved it?",
                "what_interviewer_looks_for": "Structured problem-solving, root-cause debugging methodology, resilience, and clear communication.",
                "star_sample_answer": {
                    "Situation": f"While scaling our core services built with {top_tech}, we encountered unexpected latency spikes during peak load hours.",
                    "Task": "I was tasked with identifying the root cause, eliminating the bottleneck, and ensuring 99.9% uptime without breaking existing API contracts.",
                    "Action": "I profiled the database queries, introduced asynchronous processing, and implemented caching layers to offload repetitive I/O operations.",
                    "Result": f"Reduced average API response time by over 45% and prevented system degradations during subsequent traffic surges."
                }
            },
            {
                "category": "System Architecture & Scalability",
                "difficulty": "Hard",
                "question": f"How would you design a scalable, fault-tolerant backend system for a modern {job_title} application handling millions of daily requests?",
                "what_interviewer_looks_for": "Understanding of distributed systems, database indexing, caching strategies (Redis), async workers, and load balancing.",
                "star_sample_answer": {
                    "Situation": "Designing the architecture for an end-to-end data processing workflow with high concurrency requirements.",
                    "Task": "Architect a decoupled, modular service with automated failover and horizontal scalability.",
                    "Action": "Implemented stateless microservices behind an Nginx/API gateway, utilized a Redis cache layer for hot reads, and decoupled heavy tasks with asynchronous queues.",
                    "Result": "Achieved sub-100ms P95 latency while smoothly supporting a 3x increase in concurrent users."
                }
            },
            {
                "category": "Code Quality & Engineering Practices",
                "difficulty": "Medium",
                "question": "How do you balance rapid feature delivery with code quality, unit testing, and technical debt management?",
                "what_interviewer_looks_for": "Pragmatism, testing standards (TDD/CI-CD), clean code principles, and long-term maintainability mindset.",
                "star_sample_answer": {
                    "Situation": "Working under tight release schedules where shipping fast was critical for business milestones.",
                    "Task": "Deliver key features on time without compromising test coverage or accumulating crippling tech debt.",
                    "Action": "Instituted automated CI/CD pipelines with linting and coverage gates (aiming for >80% coverage on core logic) and scheduled weekly mini-refactoring cycles.",
                    "Result": "Shipped releases on schedule while decreasing post-deployment bugs by 30%."
                }
            },
            {
                "category": f"Technical Deep-Dive: {top_tech} & {second_tech}",
                "difficulty": "Medium",
                "question": f"What are common performance pitfalls when working with {top_tech}, and what tools/techniques do you use to diagnose them?",
                "what_interviewer_looks_for": "Deep runtime knowledge, memory management, concurrency models, and profiling tooling.",
                "star_sample_answer": {
                    "Situation": "Investigating high CPU utilization and memory leaks in production microservices.",
                    "Task": "Isolate the offending code paths and optimize memory footprint.",
                    "Action": "Used APM tracing and profilers to locate unclosed connection pools and redundant data serialization loops.",
                    "Result": "Halved memory consumption per container and eliminated container restart crashes."
                }
            },
            {
                "category": "Conflict Resolution & Team Collaboration",
                "difficulty": "Medium",
                "question": "Tell me about a time you had a technical disagreement with a team member or stakeholder. How did you handle it?",
                "what_interviewer_looks_for": "Emotional intelligence, data-driven reasoning, active listening, and putting the team/product outcome first.",
                "star_sample_answer": {
                    "Situation": "Our team was divided between adopting a relational database schema vs a NoSQL document store for a new feature.",
                    "Task": "Reach a consensus that fulfilled the project's performance and reporting requirements without stalling delivery.",
                    "Action": "Organized a short spike to benchmark query performance against realistic data schemas and presented the comparative metrics objectively.",
                    "Result": "The team aligned unanimously on the benchmarked solution, delivering the feature two weeks ahead of schedule."
                }
            }
        ]
        return questions

    # ------------------------------------------------------------------
    # Optional LLM API Integrations
    # ------------------------------------------------------------------
    def _call_llm_cover_letter(self, profile: Dict[str, Any], job_title: str, company_name: str, job_description: str) -> Optional[str]:
        prompt = f"""Write a compelling, tailored cover letter for candidate {profile.get('contact', {}).get('name', 'Candidate')} applying for the role of {job_title} at {company_name}.
Skills: {', '.join(profile.get('skills', {}).get('all_skills', []))}
Target Job Description: {job_description[:1000]}
Format clearly with sender contact info, date, recipient, formal salutation, 3-4 structured body paragraphs, and professional closing."""
        return self._query_llm_endpoint(prompt)

    def _call_llm_interview_prep(self, profile: Dict[str, Any], job_title: str, job_description: str) -> Optional[List[Dict[str, Any]]]:
        prompt = f"""Generate 5 role-specific interview questions with STAR answers for a {job_title}.
Candidate skills: {', '.join(profile.get('skills', {}).get('all_skills', []))}
Return JSON array with objects containing 'category', 'difficulty', 'question', 'what_interviewer_looks_for', and 'star_sample_answer' (Situation, Task, Action, Result)."""
        res = self._query_llm_endpoint(prompt)
        if res:
            try:
                # Find JSON block
                json_match = re.search(r"\[.*\]", res, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
            except Exception:
                pass
        return None

    def _query_llm_endpoint(self, prompt: str) -> Optional[str]:
        """Generic lightweight LLM query wrapper."""
        if not self.api_key:
            return None
        try:
            if "gemini" in self.provider or self.api_key.startswith("AIza"):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                resp = requests.post(url, json=payload, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            elif "openai" in self.provider or self.api_key.startswith("sk-"):
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
                resp = requests.post(url, headers=headers, json=payload, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
        except Exception:
            return None
        return None
