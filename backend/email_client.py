"""
Email Client Module
Simulates Gmail API interaction for fetching emails
Future: Replace with actual Gmail API integration using OAuth2.0
"""

import random
from datetime import datetime, timedelta


class EmailClient:
    """
    Mock Email Client that simulates fetching emails
    In production, this would use Google Gmail API
    """

    def __init__(self):
        self.mock_emails = self._generate_mock_emails()

    def _generate_mock_emails(self):
        """Generate realistic mock email data"""

        mock_data = [
            {
                'id': 'email_001',
                'sender': 'team@company.com',
                'subject': 'Project Deadline Approaching - Action Required',
                'body': 'Hi, the deadline for the Q4 project is this Friday. Please submit your final deliverables by EOD Thursday. Let me know if you need any support.',
                'timestamp': datetime.now() - timedelta(hours=2),
                'unread': True
            },
            {
                'id': 'email_002',
                'sender': 'deals@amazon.com',
                'subject': '50% OFF - Limited Time Offer on Electronics',
                'body': 'Do not miss our exclusive sale! Get up to 50% discount on laptops, headphones, and more. Offer valid until midnight. Shop now!',
                'timestamp': datetime.now() - timedelta(hours=5),
                'unread': True
            },
            {
                'id': 'email_003',
                'sender': 'hr@workplace.com',
                'subject': 'Reminder: Complete Your Annual Performance Review',
                'body': 'This is a reminder to complete your annual performance review by November 5th. Please log in to the portal and submit your self-assessment.',
                'timestamp': datetime.now() - timedelta(days=1),
                'unread': False
            },
            {
                'id': 'email_004',
                'sender': 'newsletter@techcrunch.com',
                'subject': 'Daily Tech News Digest',
                'body': 'Todays top stories: AI breakthrough in medical imaging, new smartphone launches, and startup funding news. Read more inside.',
                'timestamp': datetime.now() - timedelta(hours=8),
                'unread': True
            },
            {
                'id': 'email_005',
                'sender': 'manager@company.com',
                'subject': 'Meeting Reschedule - New Time Proposed',
                'body': 'Hi, I need to reschedule our 1:1 meeting from Wednesday to Thursday at 3 PM. Does this work for you? Please confirm.',
                'timestamp': datetime.now() - timedelta(hours=3),
                'unread': True
            },
            {
                'id': 'email_006',
                'sender': 'notifications@linkedin.com',
                'subject': 'You have 5 new connection requests',
                'body': 'People are trying to connect with you on LinkedIn. Review and accept their requests to grow your professional network.',
                'timestamp': datetime.now() - timedelta(hours=12),
                'unread': False
            },
            {
                'id': 'email_007',
                'sender': 'support@bankofamerica.com',
                'subject': 'Your Monthly Statement is Ready',
                'body': 'Your account statement for October 2025 is now available. Log in to view your transactions and download the PDF.',
                'timestamp': datetime.now() - timedelta(days=2),
                'unread': True
            },
            {
                'id': 'email_008',
                'sender': 'client@partner.com',
                'subject': 'Proposal Review Feedback',
                'body': 'Thank you for the detailed proposal. Overall it looks great. I have a few questions about the timeline in section 3. Can we schedule a call to discuss?',
                'timestamp': datetime.now() - timedelta(hours=6),
                'unread': True
            }
        ]

        return mock_data

    def fetch_emails(self, limit=10):
        """
        Fetch emails from inbox

        Args:
            limit (int): Maximum number of emails to fetch

        Returns:
            list: List of email dictionaries
        """
        # Return mock emails (limited)
        emails = self.mock_emails[:limit]

        # Convert datetime to string for JSON serialization
        for email in emails:
            email['timestamp'] = email['timestamp'].isoformat()

        return emails

    def fetch_email_by_id(self, email_id):
        """
        Fetch a specific email by ID

        Args:
            email_id (str): The email ID

        Returns:
            dict: Email object or None
        """
        for email in self.mock_emails:
            if email['id'] == email_id:
                email_copy = email.copy()
                email_copy['timestamp'] = email_copy['timestamp'].isoformat()
                return email_copy

        return None

    def mark_as_read(self, email_id):
        """
        Mark an email as read

        Args:
            email_id (str): The email ID

        Returns:
            bool: Success status
        """
        for email in self.mock_emails:
            if email['id'] == email_id:
                email['unread'] = False
                return True

        return False

    def send_email(self, to, subject, body):
        """
        Send an email (mocked)

        Args:
            to (str): Recipient email address
            subject (str): Email subject
            body (str): Email body

        Returns:
            dict: Send status
        """
        # In production, this would use Gmail API to send emails
        print(f"[MOCK] Sending email to {to}")
        print(f"[MOCK] Subject: {subject}")
        print(f"[MOCK] Body: {body[:100]}...")

        return {
            'success': True,
            'message_id': f'sent_{random.randint(1000, 9999)}',
            'timestamp': datetime.now().isoformat()
        }


# Example usage
if __name__ == '__main__':
    client = EmailClient()
    emails = client.fetch_emails()

    print(f"Fetched {len(emails)} emails:")
    for email in emails:
        print(f"  - {email['subject']} (from {email['sender']})")
