"""
Data Models
Define data structures for emails, actions, and user preferences
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Email:
    """Email data model"""
    id: str
    sender: str
    subject: str
    body: str
    timestamp: datetime
    unread: bool = True
    classification: Optional[str] = None
    priority: Optional[int] = None

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'sender': self.sender,
            'subject': self.subject,
            'body': self.body,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            'unread': self.unread,
            'classification': self.classification,
            'priority': self.priority
        }


@dataclass
class EmailClassification:
    """Email classification result"""
    category: str
    confidence: float
    keywords: List[str]
    sentiment: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'category': self.category,
            'confidence': self.confidence,
            'keywords': self.keywords,
            'sentiment': self.sentiment
        }


@dataclass
class EmailReply:
    """Generated email reply"""
    subject: str
    body: str
    tone: str
    confidence: float
    reply_type: str

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'subject': self.subject,
            'body': self.body,
            'tone': self.tone,
            'confidence': self.confidence,
            'reply_type': self.reply_type
        }


@dataclass
class UserAction:
    """User action record"""
    id: str
    email_id: str
    action_type: str  # 'classify', 'reply', 'archive', 'delete'
    timestamp: datetime
    metadata: Optional[dict] = None

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email_id': self.email_id,
            'action_type': self.action_type,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            'metadata': self.metadata
        }


@dataclass
class UserPreferences:
    """User preferences and settings"""
    user_id: str
    auto_classify: bool = True
    auto_reply_promotional: bool = False
    notification_important: bool = True
    preferred_tone: str = 'Professional'
    working_hours: Optional[dict] = None

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'auto_classify': self.auto_classify,
            'auto_reply_promotional': self.auto_reply_promotional,
            'notification_important': self.notification_important,
            'preferred_tone': self.preferred_tone,
            'working_hours': self.working_hours
        }
