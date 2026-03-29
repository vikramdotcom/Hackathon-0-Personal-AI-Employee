@echo off
REM Quick Gmail Watcher Test Script

echo ==========================================
echo Gmail Watcher - Quick Test
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

echo Step 2: Running Gmail watcher...
echo ------------------------------------------
echo.
echo This will:
echo 1. Open browser for Google OAuth2 (first time only)
echo 2. Check your Gmail inbox for unread emails
echo 3. Create task files in Needs_Action/
echo 4. Save token for future automatic runs
echo.
echo Press Ctrl+C to stop after first check
echo.

cd AI_Employee_Vault\watchers
uv run python gmail_watcher.py

echo.
echo ==========================================
echo Gmail Watcher Test Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Check AI_Employee_Vault\Needs_Action\ for email tasks
echo 2. Run: claude /ai-employee process
echo 3. Review drafts in Pending_Approval\
echo.

pause
