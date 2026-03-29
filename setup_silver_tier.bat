@echo off
REM Silver Tier Setup Script (Windows)
REM Sets up Gmail and LinkedIn watchers with all dependencies

echo ==========================================
echo Silver Tier Setup - AI Employee
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "AI_Employee_Vault" (
    echo Error: Please run this script from the project root directory
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
echo ------------------------------------------
cd AI_Employee_Vault\watchers

REM Install dependencies using UV
where uv >nul 2>&1
if %errorlevel% equ 0 (
    echo Using UV package manager...
    uv sync
) else (
    echo UV not found. Installing with pip...
    pip install -r requirements.txt
)

echo.
echo Step 2: Installing Playwright browsers...
echo ------------------------------------------
where playwright >nul 2>&1
if %errorlevel% equ 0 (
    playwright install chromium
    echo Playwright browsers installed!
) else (
    echo Warning: Playwright not found. Run: pip install playwright ^&^& playwright install
)

cd ..\..

echo.
echo Step 3: Checking credentials.json...
echo ------------------------------------------
if exist "credentials.json" (
    echo [32m✓[0m credentials.json found
) else (
    echo [31m✗[0m credentials.json not found
    echo.
    echo Please add your Google OAuth2 credentials:
    echo 1. Go to Google Cloud Console
    echo 2. Create OAuth2 credentials
    echo 3. Download as credentials.json
    echo 4. Place in project root
    echo.
    echo See MCP_SETUP_GUIDE.md for detailed instructions
)

echo.
echo Step 4: Creating configuration files...
echo ------------------------------------------

REM Create Config directory if it doesn't exist
if not exist "AI_Employee_Vault\Config" mkdir AI_Employee_Vault\Config

REM Create gmail_rules.json if it doesn't exist
if not exist "AI_Employee_Vault\Config\gmail_rules.json" (
    (
        echo {
        echo   "check_interval": 300,
        echo   "priority_keywords": {
        echo     "high": ["urgent", "asap", "invoice", "payment", "client", "deadline"],
        echo     "medium": ["inquiry", "question", "request", "meeting", "schedule"],
        echo     "low": ["newsletter", "notification", "update", "unsubscribe"]
        echo   },
        echo   "skip_senders": ["noreply@", "no-reply@", "notifications@", "donotreply@"],
        echo   "max_emails_per_check": 20,
        echo   "auto_label": "AI_Employee_Processed",
        echo   "create_drafts": true
        echo }
    ) > AI_Employee_Vault\Config\gmail_rules.json
    echo [32m✓[0m Created gmail_rules.json
) else (
    echo [32m✓[0m gmail_rules.json already exists
)

REM Create email_settings.json if it doesn't exist
if not exist "AI_Employee_Vault\Config\email_settings.json" (
    (
        echo {
        echo   "default_signature": "Best regards,\\nYour Name",
        echo   "reply_prefix": "Re: ",
        echo   "max_recipients": 10,
        echo   "require_approval": true,
        echo   "log_all_emails": true,
        echo   "blocked_domains": []
        echo }
    ) > AI_Employee_Vault\Config\email_settings.json
    echo [32m✓[0m Created email_settings.json
) else (
    echo [32m✓[0m email_settings.json already exists
)

REM Create calendar_settings.json if it doesn't exist
if not exist "AI_Employee_Vault\Config\calendar_settings.json" (
    (
        echo {
        echo   "default_duration": 60,
        echo   "default_reminder": 15,
        echo   "timezone": "America/New_York",
        echo   "working_hours": {
        echo     "start": "09:00",
        echo     "end": "17:00"
        echo   },
        echo   "auto_decline_conflicts": false,
        echo   "require_approval": true,
        echo   "max_event_duration": 480
        echo }
    ) > AI_Employee_Vault\Config\calendar_settings.json
    echo [32m✓[0m Created calendar_settings.json
) else (
    echo [32m✓[0m calendar_settings.json already exists
)

REM Create whatsapp_rules.json if it doesn't exist
if not exist "AI_Employee_Vault\Config\whatsapp_rules.json" (
    (
        echo {
        echo   "check_interval": 300,
        echo   "priority_keywords": {
        echo     "high": ["urgent", "asap", "help", "emergency", "problem"],
        echo     "medium": ["question", "inquiry", "request", "when", "how"],
        echo     "low": ["thanks", "ok", "received", "noted"]
        echo   },
        echo   "auto_mark_read": false,
        echo   "skip_groups": false,
        echo   "important_contacts": [],
        echo   "max_messages_per_check": 50,
        echo   "download_media": true,
        echo   "create_task_for_groups": false
        echo }
    ) > AI_Employee_Vault\Config\whatsapp_rules.json
    echo [32m✓[0m Created whatsapp_rules.json
) else (
    echo [32m✓[0m whatsapp_rules.json already exists
)

REM Create linkedin_settings.json (already exists from earlier)
if not exist "AI_Employee_Vault\Config\linkedin_settings.json" (
    echo [31m✗[0m linkedin_settings.json not found - should have been created earlier
) else (
    echo [32m✓[0m linkedin_settings.json already exists
)

echo.
echo Step 5: Creating necessary directories...
echo ------------------------------------------
if not exist "AI_Employee_Vault\Reports" mkdir AI_Employee_Vault\Reports
if not exist "AI_Employee_Vault\Logs" mkdir AI_Employee_Vault\Logs
echo [32m✓[0m Directories created

echo.
echo ==========================================
echo Silver Tier Setup Complete!
echo ==========================================
echo.
echo Next Steps:
echo 1. Ensure credentials.json is in project root
echo 2. Test Gmail watcher: cd AI_Employee_Vault\watchers ^&^& uv run python gmail_watcher.py
echo 3. Test LinkedIn watcher: cd AI_Employee_Vault\watchers ^&^& uv run python linkedin_watcher.py
echo 4. Read MCP_SETUP_GUIDE.md for MCP server configuration
echo 5. Run verification: verify_silver_tier.bat
echo.
echo For detailed instructions, see:
echo - SILVER_TIER_README.md
echo - MCP_SETUP_GUIDE.md
echo - SILVER_TIER_QUICK_REFERENCE.md
echo.

pause
