"""WhatsApp watcher for monitoring messages and creating tasks."""
import time
import json
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher


class WhatsAppWatcher(BaseWatcher):
    """Watcher for monitoring WhatsApp messages."""

    def __init__(self, vault_path: str, check_interval: int = 300):
        super().__init__(vault_path, check_interval)
        self.config = self._load_config()
        self.processed_message_ids = set()

    def _load_config(self):
        """Load WhatsApp monitoring configuration."""
        config_file = self.vault_path / 'Config' / 'whatsapp_rules.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)

        # Default configuration
        return {
            "check_interval": 300,
            "priority_keywords": {
                "high": ["urgent", "asap", "help", "emergency", "problem"],
                "medium": ["question", "inquiry", "request", "when", "how"],
                "low": ["thanks", "ok", "received", "noted"]
            },
            "auto_mark_read": False,
            "skip_groups": False,
            "important_contacts": [],
            "max_messages_per_check": 50,
            "download_media": True,
            "create_task_for_groups": False
        }

    def check_for_updates(self) -> list:
        """
        Check WhatsApp for new messages.

        NOTE: This requires WhatsApp API or Web WhatsApp access.
        The actual implementation will use MCP tools or browser automation.
        This is a placeholder that demonstrates the structure.
        """
        self.logger.info("Checking WhatsApp for new messages...")

        # In actual implementation, this would call WhatsApp API or browser automation
        # For now, return empty list as this is a template
        # The actual message fetching happens via Claude Code skills

        new_messages = []

        # Placeholder: In real implementation, fetch messages
        # messages = whatsapp_api.get_unread_messages(limit=self.config['max_messages_per_check'])

        # Filter out already processed messages
        # for message in messages:
        #     if message['id'] not in self.processed_message_ids:
        #         new_messages.append(message)
        #         self.processed_message_ids.add(message['id'])

        return new_messages

    def create_action_file(self, message) -> Path:
        """
        Create action file for WhatsApp message in Needs_Action folder.

        Args:
            message: Message data dict with keys: id, sender, body, timestamp, chat_type
        """
        # Extract message details
        sender_number = message.get('sender', 'unknown')
        sender_name = message.get('sender_name', sender_number)
        body = message.get('body', '')
        timestamp = message.get('timestamp', datetime.now().isoformat())
        chat_type = message.get('chat_type', 'individual')
        has_media = message.get('has_media', False)
        message_id = message.get('id', '')

        # Assess priority
        priority = self._assess_priority(body, sender_number)

        # Determine if response needed
        requires_response = self._requires_response(body, chat_type)

        # Create safe filename
        safe_sender = "".join(c for c in sender_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_sender = safe_sender.replace(' ', '_')
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'WHATSAPP_{safe_sender}_{date_str}.md'

        # Create metadata content
        content = f"""---
type: whatsapp_message
sender_name: {sender_name}
sender_number: {sender_number}
received: {timestamp}
priority: {priority}
status: pending
has_media: {has_media}
chat_type: {chat_type}
requires_response: {requires_response}
message_id: {message_id}
---

## New WhatsApp Message

**From**: {sender_name} ({sender_number})
**Received**: {timestamp}
**Priority**: {priority.capitalize()}
**Chat Type**: {chat_type.capitalize()}

## Message Content

{body}

{f'**Media Attached**: Yes (saved to Inbox/)' if has_media else ''}

## Suggested Actions

- [ ] Read full conversation in WhatsApp
- [ ] Draft response
- [ ] Forward to appropriate person
- [ ] Schedule follow-up
- [ ] Mark as resolved

## WhatsApp Link

[Open in WhatsApp](whatsapp://send?phone={sender_number})

## Notes

Add any relevant notes or observations here.
"""

        # Write to Needs_Action folder
        action_file = self.needs_action / filename
        action_file.write_text(content, encoding='utf-8')

        return action_file

    def _assess_priority(self, body: str, sender: str) -> str:
        """Assess message priority based on content and sender."""
        text = body.lower()

        # Check if sender is in important contacts
        if sender in self.config.get('important_contacts', []):
            return 'high'

        # Check high priority keywords
        for keyword in self.config['priority_keywords']['high']:
            if keyword.lower() in text:
                return 'high'

        # Check medium priority keywords
        for keyword in self.config['priority_keywords']['medium']:
            if keyword.lower() in text:
                return 'medium'

        return 'low'

    def _requires_response(self, body: str, chat_type: str) -> bool:
        """Determine if message requires a response."""
        # Group messages typically don't require individual response
        if chat_type == 'group' and not self.config.get('create_task_for_groups', False):
            return False

        response_indicators = ['?', 'please', 'could you', 'can you', 'would you',
                              'need', 'help', 'urgent', 'asap']

        body_lower = body.lower()
        return any(indicator in body_lower for indicator in response_indicators)


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent

    # Create and run the watcher
    watcher = WhatsAppWatcher(str(vault_path))

    print("=" * 60)
    print("WhatsApp Watcher - Silver Tier")
    print("=" * 60)
    print()
    print("NOTE: This watcher requires WhatsApp API or Web access.")
    print("The actual message fetching is handled by Claude Code skills.")
    print()
    print("This watcher serves as a scheduled checker that triggers")
    print("the /whatsapp-monitor skill at regular intervals.")
    print()
    print("To use WhatsApp monitoring:")
    print("1. Configure WhatsApp API or browser automation")
    print("2. Run: claude /whatsapp-monitor check")
    print("3. Or run this watcher to check periodically")
    print()
    print("=" * 60)

    # For now, just log that we're ready
    watcher.logger.info("WhatsApp Watcher initialized and ready")
    watcher.logger.info("Waiting for API/browser automation integration...")

    # In production, this would run the monitoring loop
    # watcher.run()
