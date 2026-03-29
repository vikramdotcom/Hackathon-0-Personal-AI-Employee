# Gmail Monitor - Email Watcher

Monitor Gmail inbox for new emails and create actionable tasks in the AI Employee vault.

## Description

This skill enables the AI Employee to:
- Monitor Gmail inbox for new emails
- Filter emails by priority (urgent, client, invoice keywords)
- Create tasks in Needs_Action folder for important emails
- Draft replies for common inquiries
- Flag emails requiring human attention
- Integrate with existing approval workflow

## Prerequisites

- Gmail API MCP server configured
- OAuth2 credentials for Gmail access
- MCP server running: `@gmail` or `@google-gmail`

## Usage

```bash
/gmail-monitor [action]
```

### Actions:
- `check` - Check for new emails and create tasks (default)
- `status` - Show email monitoring status
- `configure` - Set up Gmail monitoring rules

## Examples

```bash
# Check for new emails
/gmail-monitor check

# View monitoring status
/gmail-monitor status

# Configure monitoring rules
/gmail-monitor configure
```

## Behavior

### Email Processing Workflow:
1. Connect to Gmail via MCP server
2. Fetch unread emails from inbox
3. Analyze each email:
   - Extract sender, subject, body
   - Assess priority based on keywords
   - Determine if action is needed
4. Create task files in Needs_Action/
5. Mark emails as processed (add label)
6. Log all activity
7. Update Dashboard

### Priority Detection:
- **High Priority**: urgent, asap, invoice, payment, client, deadline
- **Medium Priority**: inquiry, question, request, follow-up
- **Low Priority**: newsletter, notification, update

### Auto-Response Capability:
- Draft replies for common inquiries
- Store drafts in Pending_Approval/
- Require human approval before sending

## Integration

Works with:
- AI Employee task processor (`/ai-employee`)
- Email sender skill (`/send-email`)
- Existing approval workflow

## Security

- Read-only access to Gmail by default
- No emails sent without approval
- All actions logged
- OAuth2 secure authentication

## Configuration

Create `AI_Employee_Vault/Config/gmail_rules.json`:
```json
{
  "check_interval": 300,
  "priority_keywords": {
    "high": ["urgent", "asap", "invoice", "payment"],
    "medium": ["inquiry", "question", "request"],
    "low": ["newsletter", "notification"]
  },
  "auto_label": "AI_Employee_Processed",
  "skip_senders": ["noreply@", "no-reply@"],
  "max_emails_per_check": 20
}
```

## Notes

- Silver Tier feature
- Requires MCP server setup
- Respects Gmail API rate limits
- Maintains human oversight for all responses
