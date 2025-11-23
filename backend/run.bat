@echo off
echo Starting Edu na Bazar Backend...
call venv\Scripts\activate
uvicorn main:app --reload --port 8000
