"""
Database Module
Mock database interface for storing email actions and user preferences
Future: Integrate with MongoDB Atlas for persistent storage
"""

from datetime import datetime
from typing import Dict, List


class Database:
    """
    Mock database for storing email metadata and user actions
    In production, this would connect to MongoDB Atlas
    """

    def __init__(self):
        # In-memory storage (simulating database)
        self.actions = []
        self.preferences = {}
        self.statistics = {
            'total_emails_processed': 0,
            'emails_classified': 0,
            'replies_generated': 0,
            'actions_saved': 0
        }

    def save_action(self, action_data: Dict) -> Dict:
        """
        Save user action to database

        Args:
            action_data (dict): Action metadata

        Returns:
            dict: Saved action with ID
        """
        # Generate unique ID
        action_id = f"action_{len(self.actions) + 1:04d}"

        # Add timestamp and ID
        action_data['id'] = action_id
        action_data['timestamp'] = datetime.now().isoformat()

        # Save to in-memory storage
        self.actions.append(action_data)

        # Update statistics
        self.statistics['actions_saved'] += 1

        print(f"[DB] Saved action: {action_id}")
        print(f"[DB] Email ID: {action_data.get('email_id')}")
        print(f"[DB] Classification: {action_data.get('classification')}")

        return {'id': action_id, 'success': True}

    def get_action(self, action_id: str) -> Dict:
        """
        Retrieve an action by ID

        Args:
            action_id (str): Action ID

        Returns:
            dict: Action data or None
        """
        for action in self.actions:
            if action['id'] == action_id:
                return action

        return None

    def get_all_actions(self) -> List[Dict]:
        """
        Get all saved actions

        Returns:
            list: List of all actions
        """
        return self.actions

    def save_preference(self, key: str, value) -> bool:
        """
        Save user preference

        Args:
            key (str): Preference key
            value: Preference value

        Returns:
            bool: Success status
        """
        self.preferences[key] = value
        print(f"[DB] Saved preference: {key} = {value}")
        return True

    def get_preference(self, key: str, default=None):
        """
        Get user preference

        Args:
            key (str): Preference key
            default: Default value if not found

        Returns:
            Preference value or default
        """
        return self.preferences.get(key, default)

    def update_statistics(self, metric: str, increment: int = 1):
        """
        Update statistics counter

        Args:
            metric (str): Metric name
            increment (int): Amount to increment
        """
        if metric in self.statistics:
            self.statistics[metric] += increment

    def get_statistics(self) -> Dict:
        """
        Get all statistics

        Returns:
            dict: Statistics data
        """
        return self.statistics.copy()

    def clear_all(self):
        """Clear all data (for testing)"""
        self.actions = []
        self.preferences = {}
        self.statistics = {
            'total_emails_processed': 0,
            'emails_classified': 0,
            'replies_generated': 0,
            'actions_saved': 0
        }
        print("[DB] All data cleared")


# Example usage
if __name__ == '__main__':
    db = Database()

    # Save sample action
    action = {
        'email_id': 'email_001',
        'classification': 'Important',
        'reply': 'Thank you for the update...',
        'action': 'saved'
    }

    result = db.save_action(action)
    print(f"Saved with ID: {result['id']}")

    # Get statistics
    stats = db.get_statistics()
    print(f"Statistics: {stats}")
