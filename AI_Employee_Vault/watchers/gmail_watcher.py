"""Gmail watcher for monitoring inbox and creating tasks using Google Gmail API."""
import os
import json
import pickle
import base64
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']


class GmailWatcher(BaseWatcher):
    """Watcher for monitoring Gmail inbox using Google Gmail API."""

    def __init__(self, vault_path: str, check_interval: int = 300):
        super().__init__(vault_path, check_interval)
        self.config = self._load_config()
        self.credentials_file = Path(__file__).parent.parent.parent / 'credentials.json'
        self.token_file = Path(__file__).parent / 'token.pickle'
        self.service = None
        self.processed_message_ids = self._load_processed_ids()

    def _load_config(self):
        """Load Gmail monitoring configuration."""
        config_file = self.vault_path / 'Config' / 'gmail_rules.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)

        # Default configuration
        return {
            "check_interval": 300,
            "priority_keywords": {
                "high": ["urgent", "asap", "invoice", "payment", "client", "deadline"],
                "medium": ["inquiry", "question", "request", "meeting", "schedule"],
                "low": ["newsletter", "notification", "update", "unsubscribe"]
            },
            "skip_senders": ["noreply@", "no-reply@", "notifications@", "donotreply@"],
            "max_emails_per_check": 20,
            "auto_label": "AI_Employee_Processed",
            "create_drafts": True
        }

    def _load_processed_ids(self):
        """Load set of already processed message IDs."""
        processed_file = self.vault_path / 'Logs' / 'processed_emails.json'
        if processed_file.exists():
            with open(processed_file, 'r') as f:
                data = json.load(f)
                return set(data.get('processed_ids', []))
        return set()

    def _save_processed_ids(self):
        """Save processed message IDs."""
        processed_file = self.vault_path / 'Logs' / 'processed_emails.json'
        processed_file.parent.mkdir(exist_ok=True)
        with open(processed_file, 'w') as f:
            json.dump({'processed_ids': list(self.processed_message_ids)}, f, indent=2)

    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2."""
        if not GOOGLE_API_AVAILABLE:
            self.logger.error("Google API libraries not installed. Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return None

        creds = None

        # Load existing token
        if self.token_file.exists():
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Refreshing expired credentials...")
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.error(f"Failed to refresh credentials: {e}")
                    creds = None

            if not creds:
                if not self.credentials_file.exists():
                    self.logger.error(f"Credentials file not found: {self.credentials_file}")
                    self.logger.error("Please add credentials.json to the project root")
                    return None

                self.logger.info("Starting OAuth2 authentication flow...")
                self.logger.info("A browser window will open for authentication...")
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_file), SCOPES)
                    creds = flow.run_local_server(port=0)
                    self.logger.info("Authentication successful!")
                except Exception as e:
                    self.logger.error(f"Authentication failed: {e}")
                    return None

            # Save credentials for next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def _connect_gmail(self):
        """Connect to Gmail API."""
        if self.service:
            return self.service

        try:
            creds = self._authenticate()
            if not creds:
                return None

            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Connected to Gmail API successfully")
            return self.service

        except Exception as e:
            self.logger.error(f"Failed to connect to Gmail: {e}")
            return None

    def check_for_updates(self) -> list:
        """Check Gmail for new unread emails."""
        self.logger.info("Checking Gmail for new messages...")

        if not GOOGLE_API_AVAILABLE:
            self.logger.error("Google API libraries not installed")
            return []

        service = self._connect_gmail()
        if not service:
            self.logger.error("Could not connect to Gmail")
            return []

        try:
            # Get unread messages
            results = service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=self.config['max_emails_per_check']
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                self.logger.info("No unread messages found")
                return []

            new_emails = []
            for msg in messages:
                msg_id = msg['id']

                # Skip if already processed
                if msg_id in self.processed_message_ids:
                    continue

                # Get full message details
                message = service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='full'
                ).execute()

                # Extract message data
                email_data = self._extract_email_data(message)

                # Skip if from blocked sender
                if self._should_skip_sender(email_data['sender']):
                    self.logger.info(f"Skipping email from: {email_data['sender']}")
                    self.processed_message_ids.add(msg_id)
                    continue

                new_emails.append(email_data)
                self.processed_message_ids.add(msg_id)

            # Save processed IDs
            self._save_processed_ids()

            self.logger.info(f"Found {len(new_emails)} new emails to process")
            return new_emails

        except HttpError as error:
            self.logger.error(f"Gmail API error: {error}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return []

    def _extract_email_data(self, message):
        """Extract relevant data from Gmail message."""
        headers = message['payload']['headers']

        # Extract headers
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')

        # Extract body
        body = self._get_message_body(message['payload'])

        # Extract sender email
        sender_email = sender
        if '<' in sender and '>' in sender:
            sender_email = sender.split('<')[1].split('>')[0]

        return {
            'id': message['id'],
            'thread_id': message['threadId'],
            'sender': sender,
            'sender_email': sender_email,
            'subject': subject,
            'date': date,
            'body': body,
            'snippet': message.get('snippet', '')
        }

    def _get_message_body(self, payload):
        """Extract message body from payload."""
        if 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        # Fallback to HTML if no plain text
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')

        return ""

    def _should_skip_sender(self, sender):
        """Check if sender should be skipped."""
        sender_lower = sender.lower()
        for skip_pattern in self.config['skip_senders']:
            if skip_pattern.lower() in sender_lower:
                return True
        return False
        """Load Gmail monitoring configuration."""
        config_file = self.vault_path / 'Config' / 'gmail_rules.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)

        # Default configuration
        return {
            "check_interval": 300,
            "priority_keywords": {
                "high": ["urgent", "asap", "invoice", "payment", "deadline"],
                "medium": ["inquiry", "question", "request", "follow-up"],
                "low": ["newsletter", "notification", "update"]
            },
            "auto_label": "AI_Employee_Processed",
            "skip_senders": ["noreply@", "no-reply@", "notifications@"],
            "max_emails_per_check": 20
        }

    def check_for_updates(self) -> list:
        """
        Check Gmail for new unread emails.

        NOTE: This requires Gmail MCP server to be running.
        The actual implementation will use MCP tools via Claude Code.
        This is a placeholder that demonstrates the structure.
        """
        self.logger.info("Checking Gmail for new messages...")

        # In actual implementation, this would call Gmail MCP server
        # For now, return empty list as this is a template
        # The actual email fetching happens via Claude Code skills

        new_emails = []

        # Placeholder: In real implementation, fetch emails via MCP
        # emails = gmail_mcp.list_messages(max_results=self.config['max_emails_per_check'])

        # Filter out already processed emails
        # for email in emails:
        #     if email['id'] not in self.processed_message_ids:
        #         new_emails.append(email)
        #         self.processed_message_ids.add(email['id'])

        return new_emails

    def create_action_file(self, email_data) -> Path:
        """Create action file for email in Needs_Action folder."""
        # Extract sender name
        sender = email_data['sender']
        sender_name = sender.split('<')[0].strip() if '<' in sender else sender

        # Create safe filename
        safe_sender = "".join(c for c in sender_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_sender = safe_sender.replace(' ', '_')[:50]  # Limit length
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'EMAIL_{safe_sender}_{date_str}.md'

        # Assess priority
        priority = self._assess_priority(email_data['subject'], email_data['body'], email_data['sender_email'])

        # Determine if response needed
        requires_response = self._requires_response(email_data['body'])

        # Create metadata content
        content = f"""---
type: email
sender: {email_data['sender_email']}
sender_name: {sender_name}
subject: {email_data['subject']}
received: {email_data['date']}
priority: {priority}
status: pending
thread_id: {email_data['thread_id']}
message_id: {email_data['id']}
requires_response: {requires_response}
---

## New Email Received

**From**: {sender_name} <{email_data['sender_email']}>
**Subject**: {email_data['subject']}
**Received**: {email_data['date']}
**Priority**: {priority.capitalize()}

## Email Preview

{email_data['snippet']}

## Email Content (First 1000 chars)

{email_data['body'][:1000]}

{'...(truncated - full email in Gmail)' if len(email_data['body']) > 1000 else ''}

## Suggested Actions

- [ ] Read full email in Gmail
- [ ] Draft response
- [ ] Forward to appropriate person
- [ ] Add to calendar if meeting request
- [ ] Mark as resolved

## Gmail Link

[View in Gmail](https://mail.google.com/mail/u/0/#inbox/{email_data['thread_id']})

## Notes

Add any relevant notes or observations here.
"""

        # Write to Needs_Action folder
        action_file = self.needs_action / filename
        action_file.write_text(content, encoding='utf-8')

        self.logger.info(f"Created email task: {filename}")
        return action_file

    def _assess_priority(self, subject: str, body: str, sender: str) -> str:
        """Assess email priority based on content and sender."""
        text = f"{subject} {body}".lower()

        # Check high priority keywords
        for keyword in self.config['priority_keywords']['high']:
            if keyword.lower() in text:
                return 'high'

        # Check medium priority keywords
        for keyword in self.config['priority_keywords']['medium']:
            if keyword.lower() in text:
                return 'medium'

        return 'low'

    def _requires_response(self, body: str) -> bool:
        """Determine if email requires a response."""
        response_indicators = ['?', 'please', 'could you', 'can you', 'would you',
                              'request', 'need', 'require', 'asking', 'inquiry']

        body_lower = body.lower()
        return any(indicator in body_lower for indicator in response_indicators)


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent

    print("=" * 60)
    print("Gmail Watcher - Silver Tier")
    print("=" * 60)
    print()
    print("This watcher monitors your Gmail inbox using Google Gmail API")
    print("and creates tasks for important emails.")
    print()
    print("Prerequisites:")
    print("- credentials.json in project root")
    print("- Gmail API enabled in Google Cloud Console")
    print("- Python packages: google-auth, google-api-python-client")
    print()
    print("First run will open browser for OAuth2 authentication.")
    print()
    print("=" * 60)
    print()

    # Create and run the watcher
    watcher = GmailWatcher(str(vault_path))

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nGmail Watcher stopped by user")
