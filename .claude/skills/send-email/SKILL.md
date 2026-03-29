# Send Email - Email Sender

Send emails through Gmail with human approval workflow.

## Description

This skill enables the AI Employee to:
- Send emails via Gmail API
- Require human approval for all outgoing emails
- Support draft review and editing
- Handle replies to existing threads
- Track sent emails in logs
- Integrate with approval workflow

## Prerequisites

- Gmail API MCP server configured
- OAuth2 credentials with send permission
- MCP server running: `@gmail` or `@google-gmail`

## Usage

```bash
/send-email [action]
```

### Actions:
- `send` - Send approved emails from Approved/ folder
- `draft` - Create email draft for approval
- `status` - Show pending outgoing emails

## Examples

```bash
# Send all approved emails
/send-email send

# Create a new email draft
/send-email draft

# Check pending emails
/send-email status
```

## Behavior

### Email Sending Workflow:
1. Scan Approved/ folder for email drafts
2. Validate email format and recipients
3. Send via Gmail API
4. Log sent email details
5. Move to Done/ folder
6. Update Dashboard

### Draft Creation:
1. Prompt for recipient, subject, body
2. Create draft file in Pending_Approval/
3. Wait for human review
4. Send only after moved to Approved/

### Reply Handling:
- Maintains thread context
- Includes original message
- Preserves conversation history

## Email Draft Format

Create in `Pending_Approval/DRAFT_EMAIL_[recipient]_[date].md`:

```markdown
---
type: email_draft
to: recipient@example.com
cc:
bcc:
subject: Email subject
reply_to_thread: gmail_thread_id (optional)
priority: medium
status: awaiting_approval
created: 2026-03-03T10:00:00Z
---

## Email Draft for Approval

**To**: recipient@example.com
**Subject**: Email subject
**Type**: New email / Reply

## Email Body

[Email content here]

Best regards,
[Your Name]

---

## Approval Instructions

### ✅ To Approve and Send:
1. Review email content above
2. Edit if needed
3. Move this file to `/Approved` folder
4. Run: `claude /send-email send`

### ❌ To Reject:
1. Move this file to `/Rejected` folder
2. Add rejection reason below

### ✏️ To Edit:
1. Modify email body above
2. Keep in `/Pending_Approval` until ready
3. Move to `/Approved` when finalized

## Notes

Add any notes or context here.
```

## Integration

Works with:
- Gmail Monitor (`/gmail-monitor`)
- AI Employee processor (`/ai-employee`)
- Approval workflow

## Security

- All emails require human approval
- No automatic sending
- OAuth2 secure authentication
- Complete audit trail
- Rate limit compliance

## Configuration

Create `AI_Employee_Vault/Config/email_settings.json`:
```json
{
  "default_signature": "Best regards,\n[Your Name]\n[Your Title]",
  "reply_prefix": "Re: ",
  "max_recipients": 10,
  "require_approval": true,
  "log_all_emails": true
}
```

## Notes

- Silver Tier feature
- Requires MCP server setup
- Human approval mandatory
- All sends logged
