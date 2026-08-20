"""
Runner script for AI Resume Analyser & Job Assistant.
Launches the FastAPI application using Uvicorn.
"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    # Ensure UTF-8 output on Windows consoles
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
            
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"Starting AI Resume Analyser & Job Assistant on http://{host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
