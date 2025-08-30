"""
Run FastAPI app directly.

    uv run fastapi dev src/dev.py
"""

from app import create_app

app = create_app()
