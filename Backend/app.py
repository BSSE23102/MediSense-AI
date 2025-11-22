"""
MediSense AI - Main Flask Application
Unified Medical Report Summarizer & Symptom Checker Backend
"""

from flask import Flask
from flask_cors import CORS
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, origins=app.config['CORS_ORIGINS'])

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CHROMA_DB_PATH'], exist_ok=True)
os.makedirs(app.config['EMBEDDINGS_PATH'], exist_ok=True)

# Register blueprints
from routes.summarize import summarize_bp
from routes.symptoms import symptoms_bp
from routes.ocr import ocr_bp

app.register_blueprint(summarize_bp, url_prefix='/api')
app.register_blueprint(symptoms_bp, url_prefix='/api')
app.register_blueprint(ocr_bp, url_prefix='/api')

@app.route('/')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'MediSense AI Backend',
        'version': '1.0.0'
    }, 200

@app.route('/api/health')
def api_health():
    """API health check endpoint"""
    return {
        'status': 'healthy',
        'endpoints': {
            'ocr': '/api/ocr',
            'summarize': '/api/summarize',
            'symptom-check': '/api/symptom-check'
        }
    }, 200

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG if app.config['DEBUG'] else logging.INFO)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])

