"""
Summarize Route - Handles medical report summarization
"""

from flask import Blueprint, request, jsonify
from services.llm_service import LLMService
from services.text_cleaner import TextCleaner

summarize_bp = Blueprint('summarize', __name__)
llm_service = LLMService()
text_cleaner = TextCleaner()

@summarize_bp.route('/summarize', methods=['POST'])
def summarize_report():
    """
    Summarize medical report text into patient-friendly and doctor-focused summaries
    
    Request Body:
        {
            "text": str  # Medical report text
        }
    
    Response:
        {
            "success": bool,
            "patient_summary": str,
            "doctor_summary": str,
            "key_findings": [str],
            "medications": [str],
            "critical_warnings": [str],
            "follow_up": str
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Text field is required'
            }), 400
        
        text = data['text']
        
        if not text or not text.strip():
            return jsonify({
                'success': False,
                'error': 'Text cannot be empty'
            }), 400
        
        # Clean and preprocess text
        cleaned_text = text_cleaner.clean_text(text)
        
        # Generate summaries using LLM
        result = llm_service.summarize_medical_report(cleaned_text)
        
        return jsonify({
            'success': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

