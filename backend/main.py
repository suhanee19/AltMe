"""
Context-Aware Digital Twin Email Assistant - Main Backend Application
Flask-based REST API server for email management and AI-driven automation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from email_client import EmailClient
from classifier import EmailClassifier
from openai_client import OpenAIClient
from db import Database
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load configuration
app.config.from_object(Config)

# Initialize components
email_client = EmailClient()
classifier = EmailClassifier()
openai_client = OpenAIClient()
db = Database()


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Context-Aware Digital Twin Email Assistant API',
        'version': '1.0.0'
    }), 200


@app.route('/fetch_emails', methods=['GET'])
def fetch_emails():
    """
    Fetch emails from the email client (currently mocked)
    Returns a list of email objects with metadata
    """
    try:
        logger.info("Fetching emails...")
        emails = email_client.fetch_emails()
        logger.info(f"Successfully fetched {len(emails)} emails")

        return jsonify({
            'success': True,
            'count': len(emails),
            'emails': emails
        }), 200

    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/classify', methods=['POST'])
def classify_email():
    """
    Classify an email based on its content
    Expects JSON: { "subject": "...", "body": "..." }
    """
    try:
        data = request.get_json()

        if not data or 'subject' not in data or 'body' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: subject and body'
            }), 400

        subject = data['subject']
        body = data['body']

        logger.info(f"Classifying email: {subject}")
        classification = classifier.classify(subject, body)

        return jsonify({
            'success': True,
            'classification': classification['category'],
            'confidence': classification['confidence'],
            'keywords': classification.get('keywords', [])
        }), 200

    except Exception as e:
        logger.error(f"Error classifying email: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/generate_reply', methods=['POST'])
def generate_reply():
    """
    Generate an AI-powered reply to an email
    Expects JSON: { "subject": "...", "body": "...", "sender": "..." }
    """
    try:
        data = request.get_json()

        if not data or 'subject' not in data or 'body' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: subject and body'
            }), 400

        subject = data['subject']
        body = data['body']
        sender = data.get('sender', 'Unknown')

        logger.info(f"Generating reply for email: {subject}")
        reply = openai_client.generate_reply(subject, body, sender)

        return jsonify({
            'success': True,
            'reply': reply
        }), 200

    except Exception as e:
        logger.error(f"Error generating reply: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/save', methods=['POST'])
def save_action():
    """
    Save user actions and AI decisions to database
    Expects JSON: { "email_id": "...", "classification": "...", "reply": "...", "action": "..." }
    """
    try:
        data = request.get_json()

        if not data or 'email_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: email_id'
            }), 400

        logger.info(f"Saving action for email: {data['email_id']}")
        result = db.save_action(data)

        return jsonify({
            'success': True,
            'message': 'Action saved successfully',
            'id': result.get('id')
        }), 200

    except Exception as e:
        logger.error(f"Error saving action: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """
    Get user statistics and productivity metrics
    """
    try:
        stats = db.get_statistics()

        return jsonify({
            'success': True,
            'stats': stats
        }), 200

    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info("Starting Context-Aware Digital Twin Email Assistant...")
    logger.info(f"Environment: {app.config['ENV']}")

    # Run the Flask application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
