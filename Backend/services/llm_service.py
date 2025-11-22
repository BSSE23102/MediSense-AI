"""
LLM Service - Handles interactions with Large Language Models using LangChain
"""

import os
import json
from config import Config

class LLMService:
    """Service for LLM interactions using LangChain (Gemini, OpenAI, Groq)"""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER.lower()
        self.llm = None
        self._init_llm()
    
    def _init_llm(self):
        """Initialize LLM based on provider using LangChain"""
        if self.provider == 'gemini':
            self._init_gemini_langchain()
        elif self.provider == 'openai':
            self._init_openai_langchain()
        elif self.provider == 'groq':
            self._init_groq_langchain()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _init_gemini_langchain(self):
        """Initialize Google Gemini using LangChain or direct API"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Use the model from config, or default to gemini-pro
        model_name = Config.GEMINI_MODEL if Config.GEMINI_MODEL else "gemini-pro"
        
        # Check if using newer model (2.0+, 2.5+, etc.) that might not work with langchain-google-genai
        use_direct_api = any(x in model_name.lower() for x in ['2.0', '2.5', '1.5-flash', '1.5-pro'])
        
        if use_direct_api:
            # Use direct google-generativeai for newer models
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(model_name)
                self.use_direct_api = True
                self.genai = genai
                print(f"Using direct Google Generative AI API for model: {model_name}")
                return
            except ImportError:
                raise ImportError("google-generativeai is required for newer models. Install with: pip install google-generativeai")
            except Exception as e:
                print(f"Warning: Direct API failed for {model_name}, trying LangChain: {str(e)}")
                use_direct_api = False
        
        # Try LangChain wrapper (works for gemini-pro and older models)
        if not use_direct_api:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=Config.GEMINI_API_KEY,
                    temperature=0.7
                )
                self.use_direct_api = False
            except ImportError:
                raise ImportError("langchain-google-genai is required. Install with: pip install langchain-google-genai")
            except Exception as e:
                # If LangChain fails, try direct API as fallback
                print(f"Warning: LangChain failed, trying direct API: {str(e)}")
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=Config.GEMINI_API_KEY)
                    self.model = genai.GenerativeModel(model_name)
                    self.use_direct_api = True
                    self.genai = genai
                    print(f"Using direct Google Generative AI API (fallback) for model: {model_name}")
                except Exception as e2:
                    raise Exception(f"Both LangChain and direct API failed. LangChain error: {str(e)}, Direct API error: {str(e2)}")
    
    def _init_openai_langchain(self):
        """Initialize OpenAI GPT using LangChain"""
        try:
            from langchain_openai import ChatOpenAI
            
            if not Config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=Config.OPENAI_API_KEY,
                temperature=0.7
            )
        except ImportError:
            raise ImportError("langchain-openai is required. Install with: pip install langchain-openai")
    
    def _init_groq_langchain(self):
        """Initialize Groq using LangChain"""
        try:
            from langchain_groq import ChatGroq
            
            if not Config.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            self.llm = ChatGroq(
                model_name="llama-3.1-70b-versatile",
                groq_api_key=Config.GROQ_API_KEY,
                temperature=0.7
            )
        except ImportError:
            raise ImportError("langchain-groq is required. Install with: pip install langchain-groq")
    
    def _call_llm_with_prompt(self, prompt):
        """Call LLM with a prompt using LangChain or direct API"""
        try:
            if hasattr(self, 'use_direct_api') and self.use_direct_api:
                # Use direct Google Generative AI API
                response = self.model.generate_content(prompt)
                return response.text
            else:
                # Use LangChain
                if not self.llm:
                    raise ValueError("LLM not initialized")
                response = self.llm.invoke(prompt)
                # LangChain returns AIMessage object, extract content
                if hasattr(response, 'content'):
                    return response.content
                return str(response)
        except Exception as e:
            raise Exception(f"LLM call failed: {str(e)}")
    
    def summarize_medical_report(self, text):
        """
        Generate patient-friendly and doctor-focused summaries using LangChain
        
        Args:
            text: Medical report text
            
        Returns:
            Dictionary with summaries and key information
        """
        try:
            # Try LangChain 0.2.x imports first
            try:
                from langchain_core.prompts import PromptTemplate
                from langchain_core.output_parsers import PydanticOutputParser
                from langchain.chains import LLMChain
            except ImportError:
                # Fallback to 0.1.x imports
                from langchain.prompts import PromptTemplate
                from langchain.chains import LLMChain
                from langchain.output_parsers import PydanticOutputParser
            from pydantic import BaseModel, Field
            from typing import List
            
            # Define output structure
            class MedicalSummary(BaseModel):
                patient_summary: str = Field(description="Clear, simple explanation in plain language for patients (2-3 paragraphs)")
                doctor_summary: str = Field(description="Technical summary for healthcare professionals with medical terminology (2-3 paragraphs)")
                key_findings: List[str] = Field(description="List of key medical findings")
                medications: List[str] = Field(description="List of medications with dosages")
                critical_warnings: List[str] = Field(description="List of critical warnings or alerts")
                follow_up: str = Field(description="Follow-up recommendations")
            
            # Create output parser
            parser = PydanticOutputParser(pydantic_object=MedicalSummary)
            
            # Create prompt template
            prompt_template = PromptTemplate(
                input_variables=["text"],
                template="""You are a medical AI assistant. Analyze the following medical report and provide a comprehensive summary.

Medical Report:
{text}

{format_instructions}

Provide detailed, accurate, and helpful summaries. For patient_summary, use simple language that non-medical professionals can understand. For doctor_summary, use proper medical terminology and technical details.""",
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
            
            # Check if using direct API (for newer models)
            if hasattr(self, 'use_direct_api') and self.use_direct_api:
                # Use direct API - format prompt and call directly
                formatted_prompt = prompt_template.format(text=text)
                formatted_prompt += f"\n\n{parser.get_format_instructions()}"
                llm_response = self._call_llm_with_prompt(formatted_prompt)
                # Parse JSON from response
                import json
                llm_response = llm_response.strip()
                if llm_response.startswith('```json'):
                    llm_response = llm_response[7:]
                if llm_response.startswith('```'):
                    llm_response = llm_response[3:]
                if llm_response.endswith('```'):
                    llm_response = llm_response[:-3]
                llm_response = llm_response.strip()
                result_dict = json.loads(llm_response)
                # Convert to Pydantic model for consistency
                result = MedicalSummary(**result_dict)
            else:
                # Use LangChain pattern
                try:
                    # Try new pattern first (LangChain 0.2.x) - using pipe operator
                    chain = prompt_template | self.llm | parser
                    result = chain.invoke({"text": text})
                except (TypeError, AttributeError, Exception) as e:
                    # Fallback: use LLMChain with invoke method
                    try:
                        chain = LLMChain(llm=self.llm, prompt=prompt_template, output_parser=parser)
                        if hasattr(chain, 'invoke'):
                            result = chain.invoke({"text": text})
                        else:
                            result = chain.run(text=text)
                    except Exception:
                        # Last resort: call LLM directly and parse manually
                        formatted_prompt = prompt_template.format(text=text)
                        llm_response = self._call_llm_with_prompt(formatted_prompt)
                        result = parser.parse(llm_response)
            
            # Convert Pydantic model to dict
            if isinstance(result, MedicalSummary):
                # Pydantic v2 uses model_dump() instead of dict()
                if hasattr(result, 'model_dump'):
                    return result.model_dump()
                else:
                    return result.dict()
            return result
            
        except ImportError as e:
            # Fallback to JSON-based approach if Pydantic not available
            return self._summarize_with_json(text)
        except Exception as e:
            # Fallback on any error
            print(f"LangChain summarization failed, using fallback: {str(e)}")
            return self._summarize_with_json(text)
    
    def _summarize_with_json(self, text):
        """Fallback JSON-based summarization"""
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
            response = self._call_llm_with_prompt(prompt)
            
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
        Analyze symptoms and provide possible conditions using LangChain
        
        Args:
            symptoms: User's symptom description
            context: Retrieved medical context from RAG
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Try LangChain 0.2.x imports first
            try:
                from langchain_core.prompts import PromptTemplate
                from langchain_core.output_parsers import PydanticOutputParser
                from langchain.chains import LLMChain
            except ImportError:
                # Fallback to 0.1.x imports
                from langchain.prompts import PromptTemplate
                from langchain.chains import LLMChain
                from langchain.output_parsers import PydanticOutputParser
            from pydantic import BaseModel, Field
            from typing import List
            
            # Define output structure
            class ConditionInfo(BaseModel):
                name: str
                probability: str
                description: str
            
            class SymptomAnalysis(BaseModel):
                possible_conditions: List[ConditionInfo] = Field(description="List of possible conditions")
                urgency: str = Field(description="Urgency level: low, medium, or high")
                explanation: str = Field(description="Detailed explanation of the analysis (2-3 paragraphs)")
                recommendations: List[str] = Field(description="List of recommendations")
                citations: List[str] = Field(description="List of source citations")
                seek_immediate_care_if: List[str] = Field(description="Red flag symptoms requiring immediate care")
            
            # Create output parser
            parser = PydanticOutputParser(pydantic_object=SymptomAnalysis)
            
            # Build context text
            context_text = f"\n\nRelevant Medical Information:\n{context}" if context else ""
            
            # Create prompt template
            prompt_template = PromptTemplate(
                input_variables=["symptoms", "context"],
                template="""You are a medical AI assistant. Analyze the following symptoms and provide evidence-based medical insights.

Symptoms: {symptoms}{context}

{format_instructions}

Provide accurate, helpful analysis based on medical knowledge. Include possible conditions with probability assessments, urgency level, and clear recommendations.""",
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
            
            # Check if using direct API (for newer models)
            if hasattr(self, 'use_direct_api') and self.use_direct_api:
                # Use direct API - format prompt and call directly
                formatted_prompt = prompt_template.format(symptoms=symptoms, context=context_text)
                formatted_prompt += f"\n\n{parser.get_format_instructions()}"
                llm_response = self._call_llm_with_prompt(formatted_prompt)
                # Parse JSON from response
                import json
                llm_response = llm_response.strip()
                if llm_response.startswith('```json'):
                    llm_response = llm_response[7:]
                if llm_response.startswith('```'):
                    llm_response = llm_response[3:]
                if llm_response.endswith('```'):
                    llm_response = llm_response[:-3]
                llm_response = llm_response.strip()
                result_dict = json.loads(llm_response)
                # Convert to Pydantic model for consistency
                result = SymptomAnalysis(**result_dict)
            else:
                # Use LangChain pattern
                try:
                    # Try new pattern first (LangChain 0.2.x) - using pipe operator
                    chain = prompt_template | self.llm | parser
                    result = chain.invoke({"symptoms": symptoms, "context": context_text})
                except (TypeError, AttributeError, Exception) as e:
                    # Fallback: use LLMChain with invoke method
                    try:
                        chain = LLMChain(llm=self.llm, prompt=prompt_template, output_parser=parser)
                        if hasattr(chain, 'invoke'):
                            result = chain.invoke({"symptoms": symptoms, "context": context_text})
                        else:
                            result = chain.run(symptoms=symptoms, context=context_text)
                    except Exception:
                        # Last resort: call LLM directly and parse manually
                        formatted_prompt = prompt_template.format(symptoms=symptoms, context=context_text)
                        llm_response = self._call_llm_with_prompt(formatted_prompt)
                        result = parser.parse(llm_response)
            
            # Convert Pydantic model to dict
            if isinstance(result, SymptomAnalysis):
                # Pydantic v2 uses model_dump() instead of dict()
                if hasattr(result, 'model_dump'):
                    return result.model_dump()
                else:
                    return result.dict()
            return result
            
        except ImportError:
            # Fallback to JSON-based approach
            return self._analyze_symptoms_with_json(symptoms, context)
        except Exception as e:
            # Fallback on any error
            print(f"LangChain symptom analysis failed, using fallback: {str(e)}")
            return self._analyze_symptoms_with_json(symptoms, context)
    
    def _analyze_symptoms_with_json(self, symptoms, context=""):
        """Fallback JSON-based symptom analysis"""
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
            response = self._call_llm_with_prompt(prompt)
            
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
