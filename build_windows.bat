@echo off
setlocal

if not exist .venv (
    echo [ERROR] .venv not found. Create it first with: python -m venv .venv
    exit /b 1
)

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    exit /b 1
)

pyinstaller --noconfirm --windowed --name YTDownloader app.py
if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    exit /b 1
)

echo.
echo Build complete.
echo Run: dist\YTDownloader\YTDownloader.exe
endlocal
