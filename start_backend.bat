@echo off
cd backend
call venv\Scripts\activate.bat
python -m uvicorn main:app --reload
pause
