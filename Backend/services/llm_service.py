"""
LLM Service - Handles interactions with Large Language Models
"""

import os
import json
from config import Config

class LLMService:
    """Service for LLM interactions (Gemini, OpenAI, Groq)"""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER.lower()
        self._init_llm()
    
    def _init_llm(self):
        """Initialize LLM based on provider"""
        if self.provider == 'gemini':
            self._init_gemini()
        elif self.provider == 'openai':
            self._init_openai()
        elif self.provider == 'groq':
            self._init_groq()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _init_gemini(self):
        """Initialize Google Gemini"""
        try:
            import google.generativeai as genai
            
            if not Config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            self.genai = genai
        except ImportError:
            raise ImportError("google-generativeai is required. Install with: pip install google-generativeai")
    
    def _init_openai(self):
        """Initialize OpenAI GPT"""
        try:
            import openai
            
            if not Config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            openai.api_key = Config.OPENAI_API_KEY
            self.client = openai
        except ImportError:
            raise ImportError("openai is required. Install with: pip install openai")
    
    def _init_groq(self):
        """Initialize Groq"""
        try:
            from groq import Groq
            
            if not Config.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            self.client = Groq(api_key=Config.GROQ_API_KEY)
        except ImportError:
            raise ImportError("groq is required. Install with: pip install groq")
    
    def _call_llm(self, prompt):
        """Call LLM with prompt based on provider"""
        if self.provider == 'gemini':
            response = self.model.generate_content(prompt)
            return response.text
        elif self.provider == 'openai':
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        elif self.provider == 'groq':
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
    
    def summarize_medical_report(self, text):
        """
        Generate patient-friendly and doctor-focused summaries
        
        Args:
            text: Medical report text
            
        Returns:
            Dictionary with summaries and key information
        """
        prompt = f"""Analyze the following medical report and provide a comprehensive summary.

Medical Report:
{text}

Please provide a JSON response with the following structure:
{{
    "patient_summary": "A clear, simple explanation in plain language that a patient can understand (2-3 paragraphs)",
    "doctor_summary": "A technical summary for healthcare professionals with medical terminology (2-3 paragraphs)",
    "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
    "medications": ["Medication 1 with dosage", "Medication 2 with dosage"],
    "critical_warnings": ["Warning 1", "Warning 2"],
    "follow_up": "Follow-up recommendations"
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self._call_llm(prompt)
            
            # Parse JSON response
            # Sometimes LLM adds markdown code blocks
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            result = json.loads(response)
            return result
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "patient_summary": "Unable to parse detailed summary. Please consult with your healthcare provider.",
                "doctor_summary": text[:500] + "..." if len(text) > 500 else text,
                "key_findings": ["Report analysis in progress"],
                "medications": [],
                "critical_warnings": [],
                "follow_up": "Consult with healthcare provider"
            }
        except Exception as e:
            raise Exception(f"LLM summarization failed: {str(e)}")
    
    def analyze_symptoms(self, symptoms, context=""):
        """
        Analyze symptoms and provide possible conditions
        
        Args:
            symptoms: User's symptom description
            context: Retrieved medical context from RAG
            
        Returns:
            Dictionary with analysis results
        """
        context_text = f"\n\nRelevant Medical Information:\n{context}" if context else ""
        
        prompt = f"""Analyze the following symptoms and provide medical insights.

Symptoms: {symptoms}{context_text}

Please provide a JSON response with the following structure:
{{
    "possible_conditions": [
        {{
            "name": "Condition Name",
            "probability": "high|medium|low",
            "description": "Brief description"
        }}
    ],
    "urgency": "low|medium|high",
    "explanation": "Detailed explanation of the analysis (2-3 paragraphs)",
    "recommendations": ["Recommendation 1", "Recommendation 2"],
    "citations": ["Source 1", "Source 2"],
    "seek_immediate_care_if": ["Red flag symptom 1", "Red flag symptom 2"]
}}

Only return valid JSON, no additional text."""
        
        try:
            response = self._call_llm(prompt)
            
            # Parse JSON response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            result = json.loads(response)
            return result
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "possible_conditions": [
                    {
                        "name": "General Consultation Needed",
                        "probability": "medium",
                        "description": "Please consult with a healthcare provider for proper diagnosis"
                    }
                ],
                "urgency": "medium",
                "explanation": "Symptom analysis is being processed. Please consult with a healthcare professional for accurate diagnosis.",
                "recommendations": ["Consult with healthcare provider", "Monitor symptoms"],
                "citations": [],
                "seek_immediate_care_if": ["Severe pain", "Difficulty breathing", "Loss of consciousness"]
            }
        except Exception as e:
            raise Exception(f"LLM symptom analysis failed: {str(e)}")

