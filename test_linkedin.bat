@echo off
REM Quick LinkedIn Watcher Test Script

echo ==========================================
echo LinkedIn Watcher - Quick Test
echo ==========================================
echo.

echo Step 1: Checking prerequisites...
echo ------------------------------------------

REM Check if in correct directory
if not exist "AI_Employee_Vault" (
    echo [ERROR] Please run from project root directory
    pause
    exit /b 1
)

echo [OK] In correct directory
echo.

echo Step 2: Checking Playwright installation...
echo ------------------------------------------

where playwright >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Playwright is installed
) else (
    echo [WARN] Playwright not found
    echo Installing Playwright...
    pip install playwright
    playwright install chromium
)

echo.

echo Step 3: Running LinkedIn watcher...
echo ------------------------------------------
echo.
echo This will:
echo 1. Open browser window (visible, not headless)
echo 2. Navigate to LinkedIn
echo 3. Wait for you to login manually (FIRST TIME ONLY)
echo 4. Check your LinkedIn messages
echo 5. Create task files in Needs_Action/
echo 6. Save session for future automatic runs
echo.
echo IMPORTANT: Login to LinkedIn when browser opens
echo Session will be saved for future automated checks
echo.

cd AI_Employee_Vault\watchers
uv run python linkedin_watcher.py

echo.
echo ==========================================
echo LinkedIn Watcher Test Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Check AI_Employee_Vault\Needs_Action\ for LinkedIn tasks
echo 2. Run: claude /ai-employee process
echo 3. Review drafts in Pending_Approval\
echo.
echo Future runs will be automatic (no login needed)
echo.

pause
