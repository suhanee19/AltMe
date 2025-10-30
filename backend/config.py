"""
Configuration Module
Application settings and environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""

    # Flask settings
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GMAIL_API_CREDENTIALS = os.getenv('GMAIL_API_CREDENTIALS', '')

    # Database settings
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'email_assistant_db')

    # Email settings
    EMAIL_FETCH_LIMIT = int(os.getenv('EMAIL_FETCH_LIMIT', '10'))
    AUTO_CLASSIFY = os.getenv('AUTO_CLASSIFY', 'True') == 'True'

    # AI settings
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '150'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))

    # Security
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @staticmethod
    def validate():
        """Validate configuration"""
        warnings = []

        if Config.ENV == 'production':
            if Config.SECRET_KEY == 'dev-secret-key-change-in-production':
                warnings.append('WARNING: Using default SECRET_KEY in production!')

            if not Config.OPENAI_API_KEY:
                warnings.append('WARNING: OPENAI_API_KEY not set!')

            if not Config.GMAIL_API_CREDENTIALS:
                warnings.append('WARNING: GMAIL_API_CREDENTIALS not set!')

        return warnings


# Example usage
if __name__ == '__main__':
    print("Configuration loaded:")
    print(f"  Environment: {Config.ENV}")
    print(f"  Debug: {Config.DEBUG}")
    print(f"  Database: {Config.DATABASE_NAME}")
    print(f"  Email Fetch Limit: {Config.EMAIL_FETCH_LIMIT}")

    # Validate configuration
    warnings = Config.validate()
    if warnings:
        print("\nConfiguration warnings:")
        for warning in warnings:
            print(f"  - {warning}")
