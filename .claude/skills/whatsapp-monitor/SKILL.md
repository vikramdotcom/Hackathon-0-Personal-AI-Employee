# WhatsApp Monitor - Message Watcher

Monitor WhatsApp messages and create actionable tasks in the AI Employee vault.

## Description

This skill enables the AI Employee to:
- Monitor WhatsApp messages (personal or business account)
- Filter messages by priority and sender
- Create tasks for important messages
- Draft replies for common inquiries
- Flag urgent messages requiring immediate attention
- Integrate with existing approval workflow

## Prerequisites

- WhatsApp Business API or Web WhatsApp access
- MCP server for WhatsApp integration
- Authentication credentials
- Phone number linked to WhatsApp

## Usage

```bash
/whatsapp-monitor [action]
```

### Actions:
- `check` - Check for new messages and create tasks (default)
- `status` - Show message monitoring status
- `configure` - Set up WhatsApp monitoring rules

## Examples

```bash
# Check for new messages
/whatsapp-monitor check

# View monitoring status
/whatsapp-monitor status

# Configure monitoring rules
/whatsapp-monitor configure
```

## Behavior

### Message Processing Workflow:
1. Connect to WhatsApp via MCP server or API
2. Fetch unread messages
3. Analyze each message:
   - Extract sender name and number
   - Extract message content
   - Check for media attachments
   - Assess priority based on keywords
   - Determine if action is needed
4. Create task files in Needs_Action/
5. Mark messages as read (optional)
6. Log all activity
7. Update Dashboard

### Priority Detection:
- **High Priority**: urgent, asap, help, emergency, problem, issue
- **Medium Priority**: question, inquiry, request, when, how
- **Low Priority**: thanks, ok, received, noted

### Auto-Response Capability:
- Draft replies for common inquiries
- Store drafts in Pending_Approval/
- Require human approval before sending
- Support quick replies for FAQs

## Message Task Format

Create in `Needs_Action/WHATSAPP_[sender]_[date].md`:

```markdown
---
type: whatsapp_message
sender_name: John Doe
sender_number: +1234567890
received: 2026-03-03T10:30:00Z
priority: high
status: pending
has_media: false
chat_type: individual
requires_response: true
---

## New WhatsApp Message

**From**: John Doe (+1234567890)
**Received**: 2026-03-03 10:30 AM
**Priority**: High
**Chat Type**: Individual / Group

## Message Content

[Message text here]

[If media: Image/Video/Document attached - saved to Inbox/]

## Context

**Previous Messages**: [Last 3 messages for context]

## Suggested Actions

- [ ] Read full conversation in WhatsApp
- [ ] Draft response
- [ ] Forward to appropriate person
- [ ] Schedule follow-up
- [ ] Mark as resolved

## Draft Response (if applicable)

[AI-generated draft response if appropriate]

**Note**: Draft requires human approval before sending.

## WhatsApp Link

[Deep link to conversation if available]

## Notes

Add any relevant notes or observations here.
```

## Integration

Works with:
- AI Employee task processor (`/ai-employee`)
- WhatsApp sender (future skill)
- Existing approval workflow

## Media Handling

When message contains media:
1. Download media file
2. Save to `AI_Employee_Vault/Inbox/`
3. Reference in task file
4. Create thumbnail if image
5. Extract text if document (OCR)

## Group Chat Handling

For group messages:
- Track group name and participants
- Only create tasks for mentions or keywords
- Summarize group activity
- Flag important group announcements

## Security

- Read-only access by default
- No messages sent without approval
- All actions logged
- Secure authentication
- Privacy-compliant

## Configuration

Create `AI_Employee_Vault/Config/whatsapp_rules.json`:
```json
{
  "check_interval": 300,
  "priority_keywords": {
    "high": ["urgent", "asap", "help", "emergency"],
    "medium": ["question", "inquiry", "request"],
    "low": ["thanks", "ok", "received"]
  },
  "auto_mark_read": false,
  "skip_groups": false,
  "important_contacts": ["+1234567890"],
  "max_messages_per_check": 50,
  "download_media": true,
  "create_task_for_groups": false
}
```

## Auto-Reply Templates

Support common responses:
- "Thank you for your message. I'll get back to you shortly."
- "I'm currently unavailable. I'll respond as soon as possible."
- "Your request has been received and is being processed."

All require approval before sending.

## Logging

Log to `AI_Employee_Vault/Logs/[date]_whatsapp_log.json`:

```json
{
  "timestamp": "2026-03-03T10:30:00Z",
  "action_type": "whatsapp_monitored",
  "sender": "+1234567890",
  "sender_name": "John Doe",
  "message_preview": "First 50 chars...",
  "priority": "high",
  "task_created": "WHATSAPP_john_doe_20260303.md",
  "requires_response": true,
  "has_media": false
}
```

## Error Handling

- If WhatsApp API fails: Log error, retry later
- If rate limit hit: Wait and retry
- If message parsing fails: Create task with raw data
- Always maintain graceful degradation

## Privacy & Compliance

- Respect user privacy
- No message content shared outside vault
- Comply with WhatsApp Terms of Service
- Secure storage of credentials
- Option to disable monitoring

## Notes

- Silver Tier feature
- Requires WhatsApp API or Web access
- Human approval for all responses
- Media files stored locally
- Group chat support optional
