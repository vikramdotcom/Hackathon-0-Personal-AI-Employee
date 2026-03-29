"""LinkedIn watcher for monitoring messages and activity using browser automation."""
import json
import time
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class LinkedInWatcher(BaseWatcher):
    """Watcher for monitoring LinkedIn messages and activity."""

    def __init__(self, vault_path: str, check_interval: int = 3600):
        super().__init__(vault_path, check_interval)
        self.config = self._load_config()
        self.processed_message_ids = self._load_processed_ids()
        self.browser = None
        self.context = None
        self.page = None

    def _load_config(self):
        """Load LinkedIn monitoring configuration."""
        config_file = self.vault_path / 'Config' / 'linkedin_settings.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)

        # Default configuration
        return {
            "check_messages_interval": 3600,
            "max_messages_per_check": 10,
            "auto_accept_connections": False,
            "track_engagement": True,
            "require_approval": True,
            "headless": True,
            "session_file": "linkedin_session.json"
        }

    def _load_processed_ids(self):
        """Load set of already processed message IDs."""
        processed_file = self.vault_path / 'Logs' / 'processed_linkedin.json'
        if processed_file.exists():
            with open(processed_file, 'r') as f:
                data = json.load(f)
                return set(data.get('processed_ids', []))
        return set()

    def _save_processed_ids(self):
        """Save processed message IDs."""
        processed_file = self.vault_path / 'Logs' / 'processed_linkedin.json'
        processed_file.parent.mkdir(exist_ok=True)
        with open(processed_file, 'w') as f:
            json.dump({'processed_ids': list(self.processed_message_ids)}, f, indent=2)

    def _init_browser(self):
        """Initialize Playwright browser."""
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Playwright not installed. Run: pip install playwright && playwright install")
            return False

        try:
            playwright = sync_playwright().start()
            self.browser = playwright.chromium.launch(
                headless=self.config.get('headless', True)
            )
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.logger.info("Browser initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            return False

    def _login_linkedin(self):
        """Login to LinkedIn (requires manual login first time)."""
        try:
            self.page.goto('https://www.linkedin.com/messaging/', wait_until='networkidle')

            # Check if already logged in
            if 'feed' in self.page.url or 'messaging' in self.page.url:
                self.logger.info("Already logged in to LinkedIn")
                return True

            # If not logged in, user needs to login manually
            self.logger.warning("Not logged in to LinkedIn")
            self.logger.warning("Please login manually in the browser window")
            self.logger.warning("Session will be saved for future use")

            # Wait for user to login (check for messaging page)
            try:
                self.page.wait_for_url('**/messaging/**', timeout=120000)  # 2 minutes
                self.logger.info("Login successful!")

                # Save session
                self._save_session()
                return True
            except PlaywrightTimeout:
                self.logger.error("Login timeout - please try again")
                return False

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False

    def _save_session(self):
        """Save browser session for future use."""
        try:
            session_file = Path(__file__).parent / self.config['session_file']
            storage_state = self.context.storage_state()
            with open(session_file, 'w') as f:
                json.dump(storage_state, f)
            self.logger.info("Session saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")

    def _load_session(self):
        """Load saved browser session."""
        try:
            session_file = Path(__file__).parent / self.config['session_file']
            if session_file.exists():
                with open(session_file, 'r') as f:
                    storage_state = json.load(f)

                # Create new context with saved session
                self.context = self.browser.new_context(storage_state=storage_state)
                self.page = self.context.new_page()
                self.logger.info("Session loaded successfully")
                return True
        except Exception as e:
            self.logger.error(f"Failed to load session: {e}")
        return False

    def check_for_updates(self) -> list:
        """Check LinkedIn for new messages."""
        self.logger.info("Checking LinkedIn for new messages...")

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Playwright not installed")
            return []

        if not self._init_browser():
            return []

        # Try to load saved session
        if not self._load_session():
            # If no session, need to login
            if not self._login_linkedin():
                self._cleanup_browser()
                return []

        try:
            # Navigate to messaging
            self.page.goto('https://www.linkedin.com/messaging/', wait_until='networkidle')
            time.sleep(2)  # Wait for messages to load

            # Extract messages
            messages = self._extract_messages()

            # Filter new messages
            new_messages = []
            for msg in messages:
                msg_id = msg.get('id', msg.get('sender', '') + msg.get('timestamp', ''))
                if msg_id not in self.processed_message_ids:
                    new_messages.append(msg)
                    self.processed_message_ids.add(msg_id)

            # Save processed IDs
            self._save_processed_ids()

            self.logger.info(f"Found {len(new_messages)} new LinkedIn messages")
            return new_messages

        except Exception as e:
            self.logger.error(f"Error checking LinkedIn: {e}")
            return []
        finally:
            self._cleanup_browser()

    def _extract_messages(self):
        """Extract messages from LinkedIn messaging page."""
        messages = []

        try:
            # Wait for message list to load
            self.page.wait_for_selector('.msg-conversations-container__conversations-list', timeout=10000)

            # Get conversation items
            conversations = self.page.query_selector_all('.msg-conversation-listitem')

            for conv in conversations[:self.config['max_messages_per_check']]:
                try:
                    # Extract sender name
                    sender_elem = conv.query_selector('.msg-conversation-listitem__participant-names')
                    sender = sender_elem.inner_text() if sender_elem else 'Unknown'

                    # Extract message preview
                    preview_elem = conv.query_selector('.msg-conversation-listitem__message-snippet')
                    preview = preview_elem.inner_text() if preview_elem else ''

                    # Extract timestamp
                    time_elem = conv.query_selector('time')
                    timestamp = time_elem.get_attribute('datetime') if time_elem else datetime.now().isoformat()

                    # Check if unread
                    is_unread = 'msg-conversation-card__unread' in conv.get_attribute('class')

                    if is_unread:
                        messages.append({
                            'id': f"{sender}_{timestamp}",
                            'sender': sender,
                            'preview': preview,
                            'timestamp': timestamp,
                            'unread': True
                        })

                except Exception as e:
                    self.logger.warning(f"Failed to extract message: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"Failed to extract messages: {e}")

        return messages

    def _cleanup_browser(self):
        """Cleanup browser resources."""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            self.logger.info("Browser cleaned up")
        except Exception as e:
            self.logger.error(f"Error cleaning up browser: {e}")

    def create_action_file(self, message) -> Path:
        """Create action file for LinkedIn message in Needs_Action folder."""
        sender = message.get('sender', 'Unknown')
        preview = message.get('preview', '')
        timestamp = message.get('timestamp', datetime.now().isoformat())

        # Create safe filename
        safe_sender = "".join(c for c in sender if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_sender = safe_sender.replace(' ', '_')[:50]
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'LINKEDIN_MSG_{safe_sender}_{date_str}.md'

        # Assess priority
        priority = self._assess_priority(preview)

        # Create metadata content
        content = f"""---
type: linkedin_message
sender: {sender}
received: {timestamp}
priority: {priority}
status: pending
requires_response: true
---

## New LinkedIn Message

**From**: {sender}
**Received**: {timestamp}
**Priority**: {priority.capitalize()}

## Message Preview

{preview}

## Suggested Actions

- [ ] Read full message in LinkedIn
- [ ] Draft professional response
- [ ] Connect if not already connected
- [ ] Schedule follow-up if needed

## LinkedIn Link

[View in LinkedIn](https://www.linkedin.com/messaging/)

## Notes

Add any relevant notes or observations here.
"""

        # Write to Needs_Action folder
        action_file = self.needs_action / filename
        action_file.write_text(content, encoding='utf-8')

        self.logger.info(f"Created LinkedIn message task: {filename}")
        return action_file

    def _assess_priority(self, text: str) -> str:
        """Assess message priority based on content."""
        text_lower = text.lower()

        high_keywords = ['urgent', 'asap', 'opportunity', 'interview', 'offer', 'partnership']
        medium_keywords = ['question', 'inquiry', 'connect', 'meeting', 'call']

        for keyword in high_keywords:
            if keyword in text_lower:
                return 'high'

        for keyword in medium_keywords:
            if keyword in text_lower:
                return 'medium'

        return 'low'


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent

    print("=" * 60)
    print("LinkedIn Watcher - Silver Tier")
    print("=" * 60)
    print()
    print("This watcher monitors LinkedIn messages using browser automation.")
    print()
    print("Prerequisites:")
    print("- Playwright installed: pip install playwright")
    print("- Browsers installed: playwright install")
    print()
    print("First run will require manual LinkedIn login.")
    print("Session will be saved for future automated checks.")
    print()
    print("=" * 60)
    print()

    # Create and run the watcher
    watcher = LinkedInWatcher(str(vault_path))

    try:
        # Run one check
        print("Running LinkedIn check...")
        messages = watcher.check_for_updates()
        print(f"Found {len(messages)} new messages")

        # Create tasks for messages
        for msg in messages:
            watcher.create_action_file(msg)

        print("LinkedIn check complete!")

    except KeyboardInterrupt:
        print("\nLinkedIn Watcher stopped by user")
    except Exception as e:
        print(f"Error: {e}")
