@echo off
REM Silver Tier Verification Script (Windows)
REM Checks if all Silver Tier components are properly configured

echo ==========================================
echo Silver Tier Verification Script
echo ==========================================
echo.

set PASSED=0
set FAILED=0

echo Checking Prerequisites...
echo ----------------------------------------

where claude >nul 2>&1
if %errorlevel% equ 0 (
    echo [32m✓[0m Claude Code CLI installed
    set /a PASSED+=1
) else (
    echo [31m✗[0m Claude Code CLI not found
    set /a FAILED+=1
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [32m✓[0m Python installed
    set /a PASSED+=1
) else (
    echo [31m✗[0m Python not found
    set /a FAILED+=1
)

where node >nul 2>&1
if %errorlevel% equ 0 (
    echo [32m✓[0m Node.js installed
    set /a PASSED+=1
) else (
    echo [31m✗[0m Node.js not found
    set /a FAILED+=1
)

echo.
echo Checking Bronze Tier (Required)...
echo ----------------------------------------

if exist "AI_Employee_Vault" (
    echo [32m✓[0m Vault directory exists
    set /a PASSED+=1
) else (
    echo [31m✗[0m Vault directory not found
    set /a FAILED+=1
)

if exist "AI_Employee_Vault\Dashboard.md" (
    echo [32m✓[0m Dashboard exists
    set /a PASSED+=1
) else (
    echo [31m✗[0m Dashboard not found
    set /a FAILED+=1
)

if exist "AI_Employee_Vault\Company_Handbook.md" (
    echo [32m✓[0m Company Handbook exists
    set /a PASSED+=1
) else (
    echo [31m✗[0m Company Handbook not found
    set /a FAILED+=1
)

if exist ".claude\skills\ai-employee\SKILL.md" (
    echo [32m✓[0m AI Employee skill exists
    set /a PASSED+=1
) else (
    echo [31m✗[0m AI Employee skill not found
    set /a FAILED+=1
)

echo.
echo Checking Silver Tier Skills...
echo ----------------------------------------

if exist ".claude\skills\gmail-monitor\SKILL.md" (
    echo [32m✓[0m Gmail Monitor skill
    set /a PASSED+=1
) else (
    echo [31m✗[0m Gmail Monitor skill not found
    set /a FAILED+=1
)

if exist ".claude\skills\send-email\SKILL.md" (
    echo [32m✓[0m Send Email skill
    set /a PASSED+=1
) else (
    echo [31m✗[0m Send Email skill not found
    set /a FAILED+=1
)

if exist ".claude\skills\schedule-task\SKILL.md" (
    echo [32m✓[0m Schedule Task skill
    set /a PASSED+=1
) else (
    echo [31m✗[0m Schedule Task skill not found
    set /a FAILED+=1
)

if exist ".claude\skills\whatsapp-monitor\SKILL.md" (
    echo [32m✓[0m WhatsApp Monitor skill
    set /a PASSED+=1
) else (
    echo [31m✗[0m WhatsApp Monitor skill not found
    set /a FAILED+=1
)

if exist ".claude\skills\linkedin-automation\SKILL.md" (
    echo [32m✓[0m LinkedIn Automation skill
    set /a PASSED+=1
) else (
    echo [31m✗[0m LinkedIn Automation skill not found
    set /a FAILED+=1
)

echo.
echo Checking Configuration Files...
echo ----------------------------------------

if exist "AI_Employee_Vault\Config" (
    echo [32m✓[0m Config directory exists
    set /a PASSED+=1
) else (
    echo [31m✗[0m Config directory not found
    set /a FAILED+=1
)

if exist "AI_Employee_Vault\Config\gmail_rules.json" (
    echo [32m✓[0m Gmail rules config
    set /a PASSED+=1
) else (
    echo [31m✗[0m Gmail rules config not found
    set /a FAILED+=1
)

if exist "AI_Employee_Vault\Config\email_settings.json" (
    echo [32m✓[0m Email settings config
    set /a PASSED+=1
) else (
    echo [31m✗[0m Email settings config not found
    set /a FAILED+=1
)

if exist "AI_Employee_Vault\Config\calendar_settings.json" (
    echo [32m✓[0m Calendar settings config
    set /a PASSED+=1
) else (
    echo [31m✗[0m Calendar settings config not found
    set /a FAILED+=1
)

echo.
echo Checking Documentation...
echo ----------------------------------------

if exist "SILVER_TIER_README.md" (
    echo [32m✓[0m Silver Tier README
    set /a PASSED+=1
) else (
    echo [31m✗[0m Silver Tier README not found
    set /a FAILED+=1
)

if exist "MCP_SETUP_GUIDE.md" (
    echo [32m✓[0m MCP Setup Guide
    set /a PASSED+=1
) else (
    echo [31m✗[0m MCP Setup Guide not found
    set /a FAILED+=1
)

echo.
echo ==========================================
echo Verification Summary
echo ==========================================
echo Passed: %PASSED%
echo Failed: %FAILED%
echo.

if %FAILED% equ 0 (
    echo [32m✓ All checks passed! Silver Tier is ready.[0m
    echo.
    echo Next Steps:
    echo 1. Configure MCP servers (see MCP_SETUP_GUIDE.md^)
    echo 2. Test skills: claude /gmail-monitor check
    echo 3. Test skills: claude /schedule-task list
    echo 4. Review configuration files in AI_Employee_Vault\Config\
) else (
    echo [31m✗ Some checks failed. Please review the errors above.[0m
    echo.
    echo Common fixes:
    echo - Ensure Bronze Tier is complete
    echo - Run from project root directory
    echo - Check file permissions
    echo - Reinstall missing components
)

pause
