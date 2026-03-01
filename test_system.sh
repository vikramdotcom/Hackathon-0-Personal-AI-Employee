# Test the AI Employee System

This script creates test files to verify the system is working correctly.

## Test 1: File Drop Detection

echo "Test 1: Creating test file in Inbox..."
echo "This is a test document for the AI Employee system." > AI_Employee_Vault/Inbox/test_document.txt

echo "Waiting 2 seconds for watcher to process..."
sleep 2

echo "Checking if file was processed..."
if [ -f "AI_Employee_Vault/Needs_Action/FILE_test_document.txt.md" ]; then
    echo "✅ Test 1 PASSED: File was detected and metadata created"
else
    echo "❌ Test 1 FAILED: Metadata file not found"
fi

## Test 2: Multiple File Types

echo ""
echo "Test 2: Testing multiple file types..."
echo "Sample CSV data" > AI_Employee_Vault/Inbox/data.csv
echo '{"test": "json"}' > AI_Employee_Vault/Inbox/config.json
echo "# Markdown test" > AI_Employee_Vault/Inbox/notes.md

sleep 3

echo "Checking processed files..."
ls -la AI_Employee_Vault/Needs_Action/

echo ""
echo "Test complete! Check AI_Employee_Vault/Needs_Action/ for processed files."
echo "Run 'claude /ai-employee process' to process the tasks."
