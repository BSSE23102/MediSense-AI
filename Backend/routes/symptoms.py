"""
Symptoms Route - Handles AI-powered symptom checking
"""

from flask import Blueprint, request, jsonify
from services.rag_service import RAGService
from services.llm_service import LLMService

symptoms_bp = Blueprint('symptoms', __name__)
rag_service = RAGService()
llm_service = LLMService()

@symptoms_bp.route('/symptom-check', methods=['POST'])
def check_symptoms():
    """
    Analyze symptoms and provide possible conditions with RAG-based insights
    
    Request Body:
        {
            "symptoms": str  # Comma-separated or natural language symptoms
        }
    
    Response:
        {
            "success": bool,
            "possible_conditions": [
                {
                    "name": str,
                    "probability": str,
                    "description": str
                }
            ],
            "urgency": str,
            "explanation": str,
            "recommendations": [str],
            "citations": [str],
            "seek_immediate_care_if": [str]
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return jsonify({
                'success': False,
                'error': 'Symptoms field is required'
            }), 400
        
        symptoms = data['symptoms']
        
        if not symptoms or not symptoms.strip():
            return jsonify({
                'success': False,
                'error': 'Symptoms cannot be empty'
            }), 400
        
        # Retrieve relevant medical context using RAG
        relevant_context = rag_service.retrieve_medical_context(symptoms)
        
        # Analyze symptoms with LLM using retrieved context
        result = llm_service.analyze_symptoms(symptoms, relevant_context)
        
        return jsonify({
            'success': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

