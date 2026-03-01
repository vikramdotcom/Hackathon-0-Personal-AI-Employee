# AI Employee - Task Processor

Process tasks from the Needs_Action folder according to Company Handbook rules.

## Description

This skill enables Claude Code to act as an autonomous AI Employee that:
- Monitors and processes tasks from the Needs_Action folder
- Follows rules defined in Company_Handbook.md
- Creates plans for complex tasks
- Updates the Dashboard with current status
- Moves completed tasks to Done folder
- Requests human approval for sensitive actions

## Usage

```bash
/ai-employee [action]
```

### Actions:
- `process` - Process all pending tasks in Needs_Action (default)
- `status` - Show current system status and pending tasks
- `update-dashboard` - Update Dashboard.md with latest information

## Examples

```bash
# Process all pending tasks
/ai-employee process

# Check system status
/ai-employee status

# Update dashboard
/ai-employee update-dashboard
```

## Behavior

### Task Processing Workflow:
1. Read Company_Handbook.md to understand rules and priorities
2. Scan Needs_Action folder for pending tasks
3. For each task:
   - Assess priority level (high/medium/low)
   - Determine if approval is needed
   - Create a plan if task is complex
   - Execute or request approval
   - Log all actions
   - Update Dashboard
   - Move to Done when complete

### Approval Requirements:
- Financial actions: Always require approval
- External communications: Require approval for new contacts
- File deletions: Require approval
- Any action outside defined thresholds

### Logging:
- All actions logged to Logs folder with timestamp
- Audit trail maintained for review
- Errors logged with full context

## Vault Structure

The AI Employee expects this folder structure:
```
AI_Employee_Vault/
├── Dashboard.md              # Current status overview
├── Company_Handbook.md       # Rules and guidelines
├── Inbox/                    # Drop folder for new items
├── Needs_Action/            # Tasks to process
├── Plans/                   # Task plans
├── Done/                    # Completed tasks
├── Logs/                    # Action logs
├── Pending_Approval/        # Actions awaiting approval
├── Approved/                # Approved actions
└── Rejected/                # Rejected actions
```

## Notes

- This is a Bronze tier implementation focusing on core functionality
- Human-in-the-loop is enforced for sensitive actions
- All actions are logged for audit purposes
- The AI Employee operates within the vault directory only
