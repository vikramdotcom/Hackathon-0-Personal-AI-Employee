# Schedule Task - Calendar & Task Scheduler

Schedule tasks, meetings, and reminders with calendar integration.

## Description

This skill enables the AI Employee to:
- Create calendar events from email requests
- Schedule recurring tasks
- Set reminders for deadlines
- Integrate with Google Calendar
- Parse natural language date/time
- Send meeting invitations
- Track scheduled items

## Prerequisites

- Google Calendar API MCP server configured
- OAuth2 credentials for Calendar access
- MCP server running: `@google-calendar` or similar

## Usage

```bash
/schedule-task [action]
```

### Actions:
- `create` - Create new calendar event or scheduled task
- `list` - Show upcoming scheduled items
- `parse` - Parse scheduling request from email/text

## Examples

```bash
# Create a new scheduled task
/schedule-task create

# List upcoming events
/schedule-task list

# Parse scheduling from email
/schedule-task parse
```

## Behavior

### Event Creation Workflow:
1. Extract event details (title, date, time, duration)
2. Parse natural language dates ("next Monday", "tomorrow at 3pm")
3. Validate date/time format
4. Create approval request if needed
5. Add to Google Calendar
6. Send invitations if attendees specified
7. Log scheduled event
8. Update Dashboard

### Natural Language Parsing:
- "Meeting with John tomorrow at 2pm" → Event on [tomorrow] 14:00
- "Call client next Monday 10am" → Event on [next Monday] 10:00
- "Deadline March 15" → All-day event on March 15
- "Weekly standup every Monday 9am" → Recurring event

### Reminder System:
- Create reminders for deadlines
- Alert before important events
- Track pending tasks with due dates

## Event Format

Create approval request in `Pending_Approval/SCHEDULE_[event]_[date].md`:

```markdown
---
type: calendar_event
title: Meeting with Client ABC
date: 2026-03-05
time: 14:00
duration: 60
timezone: America/New_York
attendees:
  - client@example.com
  - colleague@company.com
location: Conference Room A / Zoom Link
description: Discuss Q1 results
recurrence: none
reminder: 15
status: awaiting_approval
---

## Calendar Event for Approval

**Event**: Meeting with Client ABC
**Date**: March 5, 2026
**Time**: 2:00 PM - 3:00 PM (EST)
**Duration**: 60 minutes
**Location**: Conference Room A

## Attendees
- client@example.com
- colleague@company.com

## Description

Discuss Q1 results and plan for Q2.

## Reminders
- 15 minutes before event

---

## Approval Instructions

### ✅ To Approve:
1. Review event details above
2. Edit if needed
3. Move to `/Approved` folder
4. Event will be created in Google Calendar

### ❌ To Reject:
1. Move to `/Rejected` folder
2. Add reason below

### ✏️ To Edit:
1. Modify details above
2. Keep in `/Pending_Approval` until ready

## Notes

[Add any notes or context]
```

## Integration

Works with:
- Gmail Monitor (parse meeting requests from emails)
- AI Employee processor
- Google Calendar API
- Email sender (send invitations)

## Date/Time Parsing

Supports:
- Absolute: "March 5, 2026 at 2pm"
- Relative: "tomorrow", "next week", "in 3 days"
- Day names: "Monday", "next Friday"
- Time formats: "2pm", "14:00", "2:30 PM"
- Durations: "1 hour", "30 minutes", "2h"

## Recurring Events

Supports:
- Daily: "every day at 9am"
- Weekly: "every Monday at 10am"
- Monthly: "first Monday of each month"
- Custom: "every 2 weeks on Tuesday"

## Security

- Calendar modifications require approval
- No automatic event deletion
- All scheduling logged
- OAuth2 authentication

## Configuration

Create `AI_Employee_Vault/Config/calendar_settings.json`:
```json
{
  "default_duration": 60,
  "default_reminder": 15,
  "timezone": "America/New_York",
  "working_hours": {
    "start": "09:00",
    "end": "17:00"
  },
  "auto_decline_conflicts": false,
  "require_approval": true
}
```

## Notes

- Silver Tier feature
- Requires Calendar API MCP server
- Human approval for all events
- Supports recurring events
