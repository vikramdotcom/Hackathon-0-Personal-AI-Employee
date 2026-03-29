#!/bin/bash
# Silver Tier Verification Script
# Checks if all Silver Tier components are properly configured

echo "=========================================="
echo "Silver Tier Verification Script"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 - File not found: $1"
        ((FAILED++))
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 - Directory not found: $1"
        ((FAILED++))
    fi
}

# Function to check if command exists
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 - Command not found: $1"
        ((FAILED++))
    fi
}

echo "Checking Prerequisites..."
echo "----------------------------------------"
check_command "claude" "Claude Code CLI installed"
check_command "python" "Python installed"
check_command "node" "Node.js installed"
check_command "npm" "NPM installed"
echo ""

echo "Checking Bronze Tier (Required)..."
echo "----------------------------------------"
check_dir "AI_Employee_Vault" "Vault directory exists"
check_file "AI_Employee_Vault/Dashboard.md" "Dashboard exists"
check_file "AI_Employee_Vault/Company_Handbook.md" "Company Handbook exists"
check_dir "AI_Employee_Vault/Inbox" "Inbox folder exists"
check_dir "AI_Employee_Vault/Needs_Action" "Needs_Action folder exists"
check_dir "AI_Employee_Vault/Done" "Done folder exists"
check_dir "AI_Employee_Vault/Logs" "Logs folder exists"
check_file ".claude/skills/ai-employee/SKILL.md" "AI Employee skill exists"
echo ""

echo "Checking Silver Tier Skills..."
echo "----------------------------------------"
check_file ".claude/skills/gmail-monitor/SKILL.md" "Gmail Monitor skill"
check_file ".claude/skills/gmail-monitor/prompt.md" "Gmail Monitor prompt"
check_file ".claude/skills/send-email/SKILL.md" "Send Email skill"
check_file ".claude/skills/send-email/prompt.md" "Send Email prompt"
check_file ".claude/skills/schedule-task/SKILL.md" "Schedule Task skill"
check_file ".claude/skills/schedule-task/prompt.md" "Schedule Task prompt"
check_file ".claude/skills/whatsapp-monitor/SKILL.md" "WhatsApp Monitor skill"
check_file ".claude/skills/whatsapp-monitor/prompt.md" "WhatsApp Monitor prompt"
check_file ".claude/skills/linkedin-automation/SKILL.md" "LinkedIn Automation skill"
check_file ".claude/skills/linkedin-automation/prompt.md" "LinkedIn Automation prompt"
echo ""

echo "Checking Configuration Files..."
echo "----------------------------------------"
check_dir "AI_Employee_Vault/Config" "Config directory exists"
check_file "AI_Employee_Vault/Config/gmail_rules.json" "Gmail rules config"
check_file "AI_Employee_Vault/Config/email_settings.json" "Email settings config"
check_file "AI_Employee_Vault/Config/calendar_settings.json" "Calendar settings config"
check_file "AI_Employee_Vault/Config/whatsapp_rules.json" "WhatsApp rules config"
check_file "AI_Employee_Vault/Config/linkedin_settings.json" "LinkedIn settings config"
echo ""

echo "Checking Python Watchers..."
echo "----------------------------------------"
check_file "AI_Employee_Vault/watchers/gmail_watcher.py" "Gmail watcher"
check_file "AI_Employee_Vault/watchers/whatsapp_watcher.py" "WhatsApp watcher"
check_file "AI_Employee_Vault/watchers/base_watcher.py" "Base watcher"
check_file "AI_Employee_Vault/watchers/filesystem_watcher.py" "Filesystem watcher"
echo ""

echo "Checking Additional Folders..."
echo "----------------------------------------"
check_dir "AI_Employee_Vault/Pending_Approval" "Pending_Approval folder"
check_dir "AI_Employee_Vault/Approved" "Approved folder"
check_dir "AI_Employee_Vault/Rejected" "Rejected folder"
check_dir "AI_Employee_Vault/Plans" "Plans folder"
check_dir "AI_Employee_Vault/Reports" "Reports folder"
echo ""

echo "Checking Documentation..."
echo "----------------------------------------"
check_file "README.md" "Main README"
check_file "SILVER_TIER_README.md" "Silver Tier README"
check_file "MCP_SETUP_GUIDE.md" "MCP Setup Guide"
echo ""

echo "Testing Skill Availability..."
echo "----------------------------------------"

# Test if skills are recognized by Claude Code
if claude --help &> /dev/null; then
    echo -e "${GREEN}✓${NC} Claude Code is responsive"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Claude Code is not responding"
    ((FAILED++))
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Silver Tier is ready.${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. Configure MCP servers (see MCP_SETUP_GUIDE.md)"
    echo "2. Test skills: claude /gmail-monitor check"
    echo "3. Test skills: claude /schedule-task list"
    echo "4. Review configuration files in AI_Employee_Vault/Config/"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review the errors above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "- Ensure Bronze Tier is complete"
    echo "- Run from project root directory"
    echo "- Check file permissions"
    echo "- Reinstall missing components"
    exit 1
fi
