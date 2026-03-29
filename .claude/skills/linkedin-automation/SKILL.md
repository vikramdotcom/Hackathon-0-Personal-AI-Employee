# LinkedIn Automation - Professional Network Manager

Automate LinkedIn activities including connection requests, post scheduling, and message monitoring.

## Description

This skill enables the AI Employee to:
- Monitor LinkedIn messages and notifications
- Schedule posts and articles
- Send connection requests with personalized messages
- Respond to comments and messages
- Track engagement metrics
- Manage professional network activities

## Prerequisites

- LinkedIn account (personal or business)
- Browser automation via Playwright MCP
- LinkedIn API access (optional, for advanced features)
- Authentication credentials

## Usage

```bash
/linkedin-automation [action]
```

### Actions:
- `check-messages` - Check for new LinkedIn messages
- `schedule-post` - Schedule a LinkedIn post
- `send-connection` - Send connection request
- `monitor-engagement` - Track post engagement
- `status` - Show LinkedIn activity status

## Examples

```bash
# Check for new messages
/linkedin-automation check-messages

# Schedule a post
/linkedin-automation schedule-post

# Send connection request
/linkedin-automation send-connection

# Monitor engagement
/linkedin-automation monitor-engagement
```

## Behavior

### Message Monitoring:
1. Connect to LinkedIn via browser automation
2. Check inbox for new messages
3. Analyze message content and sender
4. Create tasks for important messages
5. Draft replies for common inquiries
6. Log all activity

### Post Scheduling:
1. Accept post content and schedule time
2. Create approval request
3. After approval, schedule post
4. Track post performance
5. Monitor engagement (likes, comments, shares)

### Connection Management:
1. Accept connection request details
2. Generate personalized message
3. Create approval request
4. Send connection after approval
5. Track acceptance rate

### Engagement Tracking:
1. Monitor posts for comments
2. Track likes and shares
3. Identify engagement opportunities
4. Create tasks for responses needed

## Message Task Format

Create in `Needs_Action/LINKEDIN_MSG_[sender]_[date].md`:

```markdown
---
type: linkedin_message
sender_name: John Doe
sender_profile: linkedin.com/in/johndoe
received: 2026-03-03T10:30:00Z
priority: medium
status: pending
message_type: direct_message
requires_response: true
---

## New LinkedIn Message

**From**: John Doe
**Profile**: [LinkedIn Profile URL]
**Received**: 2026-03-03 10:30 AM
**Priority**: Medium

## Message Content

[Message text here]

## Sender Context

**Title**: [Job Title]
**Company**: [Company Name]
**Connection**: [1st/2nd/3rd degree]
**Mutual Connections**: [Count]

## Suggested Actions

- [ ] Review sender's profile
- [ ] Draft response
- [ ] Schedule call if appropriate
- [ ] Add to CRM
- [ ] Mark as resolved

## Draft Response

[AI-generated professional response]

**Note**: Draft requires human approval before sending.

## LinkedIn Link

[Direct link to conversation]

## Notes

Add any relevant notes or observations here.
```

## Post Scheduling Format

Create in `Pending_Approval/LINKEDIN_POST_[date].md`:

```markdown
---
type: linkedin_post
scheduled_date: 2026-03-05
scheduled_time: 09:00
timezone: America/New_York
post_type: text
status: awaiting_approval
visibility: public
tags: []
---

## LinkedIn Post for Approval

**Scheduled**: March 5, 2026 at 9:00 AM EST
**Type**: Text Post / Article / Image / Video
**Visibility**: Public / Connections Only

## Post Content

[Post text here]

[Hashtags: #tag1 #tag2 #tag3]

[If media: Image/Video attached - path to file]

---

## Approval Instructions

### ✅ To Approve:
1. Review post content above
2. Edit if needed
3. Move to `/Approved` folder
4. Post will be published at scheduled time

### ❌ To Reject:
1. Move to `/Rejected` folder
2. Add reason below

### ✏️ To Edit:
1. Modify content above
2. Keep in `/Pending_Approval` until ready

## Notes

[Context or strategy notes]
```

## Connection Request Format

Create in `Pending_Approval/LINKEDIN_CONNECT_[name]_[date].md`:

```markdown
---
type: linkedin_connection
recipient_name: Jane Smith
recipient_profile: linkedin.com/in/janesmith
connection_degree: 2nd
mutual_connections: 5
status: awaiting_approval
---

## LinkedIn Connection Request for Approval

**Recipient**: Jane Smith
**Profile**: [LinkedIn URL]
**Current Connection**: 2nd degree
**Mutual Connections**: 5

## Recipient Context

**Title**: Senior Product Manager
**Company**: Tech Corp
**Location**: San Francisco, CA
**Industry**: Technology

## Personalized Message

Hi Jane,

I noticed we have several mutual connections and share an interest in [topic]. I'd love to connect and learn more about your work at Tech Corp.

Best regards,
[Your Name]

---

## Approval Instructions

### ✅ To Approve:
1. Review message above
2. Edit if needed
3. Move to `/Approved` folder
4. Connection request will be sent

### ❌ To Reject:
1. Move to `/Rejected` folder

## Notes

[Reason for connection, context, etc.]
```

## Integration

Works with:
- Browser automation (Playwright MCP)
- AI Employee task processor
- Email sender (for LinkedIn notifications)
- Schedule task (for post timing)

## Engagement Tracking

Monitor and report:
- Post views and impressions
- Likes, comments, shares
- Profile views
- Connection acceptance rate
- Message response rate

Create weekly report in `AI_Employee_Vault/Reports/`:

```markdown
# LinkedIn Activity Report - Week of [Date]

## Posts Published
- [Date] [Post title/preview] - [Views] views, [Likes] likes, [Comments] comments

## Messages
- Received: X messages
- Responded: Y messages
- Response rate: Z%

## Connections
- Sent: X requests
- Accepted: Y connections
- Acceptance rate: Z%

## Engagement
- Profile views: X
- Post impressions: Y
- Top performing post: [Link]

## Recommendations
- Best time to post: [Time analysis]
- Trending topics: [Topics]
- Engagement opportunities: [List]
```

## Security

- All actions require human approval
- No automated spamming
- Respect LinkedIn Terms of Service
- Rate limiting to avoid restrictions
- Secure credential storage

## Configuration

Create `AI_Employee_Vault/Config/linkedin_settings.json`:
```json
{
  "check_messages_interval": 3600,
  "auto_accept_connections": false,
  "post_approval_required": true,
  "max_connections_per_day": 10,
  "max_messages_per_day": 20,
  "engagement_tracking": true,
  "personalize_connection_requests": true,
  "default_post_time": "09:00",
  "default_visibility": "public"
}
```

## Best Practices

- Personalize all connection requests
- Engage authentically with content
- Post consistently (2-3 times per week)
- Respond to messages within 24 hours
- Track what content performs best
- Build genuine relationships

## Compliance

- Follow LinkedIn Terms of Service
- No automation that violates policies
- Respect user privacy
- No scraping without permission
- Maintain professional conduct

## Notes

- Silver Tier feature
- Requires browser automation or API
- Human approval for all actions
- Engagement tracking included
- Weekly reporting
