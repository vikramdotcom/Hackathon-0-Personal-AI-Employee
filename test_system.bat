@echo off
REM Test the AI Employee System (Windows)

echo Test 1: Creating test file in Inbox...
echo This is a test document for the AI Employee system. > AI_Employee_Vault\Inbox\test_document.txt

echo Waiting 2 seconds for watcher to process...
timeout /t 2 /nobreak > nul

echo Checking if file was processed...
if exist "AI_Employee_Vault\Needs_Action\FILE_test_document.txt.md" (
    echo [32m✓ Test 1 PASSED: File was detected and metadata created[0m
) else (
    echo [31m✗ Test 1 FAILED: Metadata file not found[0m
)

echo.
echo Test 2: Testing multiple file types...
echo Sample CSV data > AI_Employee_Vault\Inbox\data.csv
echo {"test": "json"} > AI_Employee_Vault\Inbox\config.json
echo # Markdown test > AI_Employee_Vault\Inbox\notes.md

timeout /t 3 /nobreak > nul

echo Checking processed files...
dir AI_Employee_Vault\Needs_Action\

echo.
echo Test complete! Check AI_Employee_Vault\Needs_Action\ for processed files.
echo Run 'claude /ai-employee process' to process the tasks.
pause
