"""
Email Classifier Module
Rule-based email classification system
Future: Enhance with ML models (Naive Bayes, SVM, or Transformers)
"""

import re
from typing import Dict, List


class EmailClassifier:
    """
    Rule-based email classifier
    Categorizes emails into: Important, Promotional, Social, or General
    """

    def __init__(self):
        # Define keyword patterns for each category
        self.patterns = {
            'Important': {
                'keywords': [
                    'urgent', 'deadline', 'action required', 'important',
                    'asap', 'critical', 'priority', 'immediately',
                    'meeting', 'reschedule', 'confirm', 'approval',
                    'review', 'feedback', 'proposal', 'contract'
                ],
                'senders': [
                    'manager', 'ceo', 'director', 'hr', 'admin',
                    'team', 'client', 'partner'
                ]
            },
            'Promotional': {
                'keywords': [
                    'sale', 'offer', 'discount', 'deal', 'promotion',
                    'limited time', 'free', 'save', 'shop now',
                    'exclusive', 'clearance', 'bargain', 'coupon',
                    'subscribe', 'unsubscribe'
                ],
                'senders': [
                    'deals', 'marketing', 'newsletter', 'promo',
                    'offers', 'sales'
                ]
            },
            'Social': {
                'keywords': [
                    'connection request', 'tagged you', 'liked',
                    'commented', 'shared', 'follow', 'friend request',
                    'notification', 'activity'
                ],
                'senders': [
                    'facebook', 'twitter', 'linkedin', 'instagram',
                    'notifications', 'noreply'
                ]
            },
            'Finance': {
                'keywords': [
                    'statement', 'balance', 'transaction', 'payment',
                    'invoice', 'receipt', 'billing', 'account',
                    'credit', 'debit', 'transfer'
                ],
                'senders': [
                    'bank', 'paypal', 'support', 'billing',
                    'finance', 'accounts'
                ]
            }
        }

    def classify(self, subject: str, body: str) -> Dict:
        """
        Classify an email based on subject and body

        Args:
            subject (str): Email subject line
            body (str): Email body content

        Returns:
            dict: Classification result with category, confidence, and matched keywords
        """
        # Combine subject and body for analysis
        text = f"{subject} {body}".lower()

        # Score each category
        scores = {}
        matched_keywords = {}

        for category, patterns in self.patterns.items():
            score = 0
            keywords_found = []

            # Check for keyword matches
            for keyword in patterns['keywords']:
                if keyword.lower() in text:
                    score += 2
                    keywords_found.append(keyword)

            # Check for sender patterns (if sender info in subject/body)
            for sender_pattern in patterns['senders']:
                if sender_pattern.lower() in text:
                    score += 1

            scores[category] = score
            matched_keywords[category] = keywords_found

        # Determine the category with highest score
        if max(scores.values()) == 0:
            category = 'General'
            confidence = 0.5
            keywords = []
        else:
            category = max(scores, key=scores.get)
            max_score = scores[category]
            total_score = sum(scores.values())
            confidence = round(max_score / total_score, 2) if total_score > 0 else 0.5
            keywords = matched_keywords[category]

        return {
            'category': category,
            'confidence': confidence,
            'keywords': keywords,
            'scores': scores
        }

    def extract_action_items(self, body: str) -> List[str]:
        """
        Extract potential action items from email body

        Args:
            body (str): Email body content

        Returns:
            list: List of action items
        """
        action_patterns = [
            r'please\s+([^.!?]+)',
            r'could you\s+([^.!?]+)',
            r'can you\s+([^.!?]+)',
            r'need to\s+([^.!?]+)',
            r'should\s+([^.!?]+)',
            r'must\s+([^.!?]+)'
        ]

        action_items = []
        body_lower = body.lower()

        for pattern in action_patterns:
            matches = re.findall(pattern, body_lower)
            action_items.extend(matches)

        # Clean and deduplicate
        action_items = list(set([item.strip()[:100] for item in action_items]))

        return action_items[:5]  # Return top 5 action items

    def detect_sentiment(self, text: str) -> str:
        """
        Basic sentiment detection

        Args:
            text (str): Text to analyze

        Returns:
            str: Sentiment (Positive, Negative, or Neutral)
        """
        positive_words = [
            'thanks', 'great', 'excellent', 'good', 'appreciate',
            'wonderful', 'fantastic', 'perfect', 'happy', 'glad'
        ]

        negative_words = [
            'issue', 'problem', 'error', 'concern', 'disappointed',
            'unfortunately', 'urgent', 'critical', 'fail', 'wrong'
        ]

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return 'Positive'
        elif negative_count > positive_count:
            return 'Negative'
        else:
            return 'Neutral'


# Example usage
if __name__ == '__main__':
    classifier = EmailClassifier()

    # Test emails
    test_cases = [
        {
            'subject': 'Urgent: Project Deadline Tomorrow',
            'body': 'Please submit your work by EOD. This is critical for the client presentation.'
        },
        {
            'subject': '50% OFF - Limited Time Sale!',
            'body': 'Shop now and save big on electronics. Free shipping on orders over $50.'
        },
        {
            'subject': 'Your Monthly Bank Statement',
            'body': 'Your account statement for October is ready. Download it from your dashboard.'
        }
    ]

    for test in test_cases:
        result = classifier.classify(test['subject'], test['body'])
        print(f"Subject: {test['subject']}")
        print(f"Category: {result['category']} (Confidence: {result['confidence']})")
        print(f"Keywords: {result['keywords']}")
        print()
