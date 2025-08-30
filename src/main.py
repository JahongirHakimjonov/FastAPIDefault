"""
Run FastAPI app with uvicorn.

    uv run src/main.py
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:create_app",
        app_dir="src",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
    )
