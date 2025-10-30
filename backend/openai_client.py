"""
OpenAI Client Module
Generates AI-powered email replies
Future: Integrate with OpenAI GPT API for dynamic, context-aware responses
"""

import random
from typing import Dict


class OpenAIClient:
    """
    Mock OpenAI client for generating email replies
    In production, this would use the OpenAI API with GPT models
    """

    def __init__(self, api_key=None):
        """
        Initialize OpenAI client

        Args:
            api_key (str): OpenAI API key (optional for mock)
        """
        self.api_key = api_key
        self.response_templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load response templates for different email types"""

        return {
            'Important': [
                "Thank you for bringing this to my attention. I've reviewed the details and will {action}. I'll keep you updated on the progress.",
                "I appreciate the update. I'll prioritize this and ensure {action} by the specified deadline. Please let me know if you need anything else.",
                "Understood. I'll {action} and circle back with you shortly. Thank you for the heads up."
            ],
            'Meeting': [
                "Thank you for reaching out. The proposed time works well for me. I've added it to my calendar.",
                "I appreciate you letting me know. Unfortunately, I have a conflict at that time. Would {alternative} work instead?",
                "Thanks for the update. I'll adjust my schedule accordingly and see you then."
            ],
            'Proposal': [
                "Thank you for your feedback on the proposal. I'd be happy to schedule a call to discuss your questions in detail.",
                "I appreciate your thorough review. Let me address your concerns about {topic} and we can set up a time to discuss further.",
                "Great to hear you found the proposal valuable. I'm available for a call this week to clarify any points."
            ],
            'General': [
                "Thank you for your email. I've noted your message and will respond in detail soon.",
                "I appreciate you reaching out. I'll review this and get back to you with more information.",
                "Thanks for the update. I'll look into this and follow up accordingly."
            ],
            'Promotional': [
                "Thank you for the offer, but I'm not interested at this time.",
                "I appreciate the information. I'll keep this in mind for future reference."
            ]
        }

    def generate_reply(self, subject: str, body: str, sender: str = "Unknown") -> Dict:
        """
        Generate an AI-powered email reply

        Args:
            subject (str): Email subject
            body (str): Email body
            sender (str): Sender's email/name

        Returns:
            dict: Generated reply with metadata
        """
        # Analyze the email to determine reply type
        reply_type = self._determine_reply_type(subject, body)

        # Select a template
        templates = self.response_templates.get(reply_type, self.response_templates['General'])
        template = random.choice(templates)

        # Customize the template
        reply_body = self._customize_template(template, subject, body)

        # Add greeting and signature
        greeting = f"Hi,\n\n"
        signature = f"\n\nBest regards,\nYour Digital Twin Assistant"

        full_reply = greeting + reply_body + signature

        return {
            'reply_body': full_reply,
            'reply_type': reply_type,
            'confidence': round(random.uniform(0.75, 0.95), 2),
            'tone': 'Professional',
            'subject': f"Re: {subject}"
        }

    def _determine_reply_type(self, subject: str, body: str) -> str:
        """Determine the type of reply needed based on email content"""

        text = f"{subject} {body}".lower()

        if any(word in text for word in ['meeting', 'schedule', 'reschedule', 'call', 'appointment']):
            return 'Meeting'
        elif any(word in text for word in ['proposal', 'feedback', 'review', 'client']):
            return 'Proposal'
        elif any(word in text for word in ['urgent', 'deadline', 'critical', 'important']):
            return 'Important'
        elif any(word in text for word in ['sale', 'offer', 'discount', 'promotion']):
            return 'Promotional'
        else:
            return 'General'

    def _customize_template(self, template: str, subject: str, body: str) -> str:
        """Customize reply template with context from original email"""

        # Simple placeholder replacement
        customizations = {
            '{action}': self._extract_action(body),
            '{alternative}': 'tomorrow afternoon or Friday morning',
            '{topic}': self._extract_topic(subject, body)
        }

        for placeholder, value in customizations.items():
            template = template.replace(placeholder, value)

        return template

    def _extract_action(self, body: str) -> str:
        """Extract potential action from email body"""

        actions = [
            'complete the requested task',
            'review the materials',
            'provide the necessary information',
            'follow up on this matter',
            'address your concerns'
        ]

        # Simple keyword matching for demo
        if 'submit' in body.lower():
            return 'submit the deliverables'
        elif 'review' in body.lower():
            return 'review the document'
        elif 'confirm' in body.lower():
            return 'confirm the details'
        else:
            return random.choice(actions)

    def _extract_topic(self, subject: str, body: str) -> str:
        """Extract main topic from email"""

        # Simple extraction - take first few words of subject
        words = subject.split()[:3]
        return ' '.join(words).lower()

    def analyze_tone(self, text: str) -> str:
        """
        Analyze the tone of the original email

        Args:
            text (str): Email text

        Returns:
            str: Detected tone
        """
        text_lower = text.lower()

        if any(word in text_lower for word in ['urgent', 'asap', 'immediately', 'critical']):
            return 'Urgent'
        elif any(word in text_lower for word in ['thanks', 'appreciate', 'grateful']):
            return 'Friendly'
        elif any(word in text_lower for word in ['please', 'kindly', 'would you']):
            return 'Polite'
        else:
            return 'Neutral'


# Example usage
if __name__ == '__main__':
    client = OpenAIClient()

    # Test email
    subject = "Project Deadline Approaching"
    body = "Hi, the deadline for the Q4 project is this Friday. Please submit your final deliverables by EOD Thursday."

    reply = client.generate_reply(subject, body, "manager@company.com")

    print(f"Subject: {reply['subject']}")
    print(f"Type: {reply['reply_type']}")
    print(f"Confidence: {reply['confidence']}")
    print(f"\nReply:\n{reply['reply_body']}")
