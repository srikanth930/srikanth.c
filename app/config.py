"""
Application Configuration and Environment Setup.
"""

import os
from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"
SAMPLE_DIR = BASE_DIR / "sample_resumes"

# Application Metadata
APP_TITLE = "AI Resume Analyser & Job Assistant"
APP_DESCRIPTION = "Advanced ATS scoring, job description matching, and intelligent career acceleration suite."
APP_VERSION = "2.0.0"

# AI Configuration (Optional API keys)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")

# File Upload Limits
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md"}
