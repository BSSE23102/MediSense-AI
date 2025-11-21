"""
OCR Route - Handles text extraction from medical documents
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from services.ocr_service import OCRService
from utils.pdf_reader import PDFReader
from config import Config

ocr_bp = Blueprint('ocr', __name__)
ocr_service = OCRService()
pdf_reader = PDFReader()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@ocr_bp.route('/ocr', methods=['POST'])
def extract_text():
    """
    Extract text from uploaded medical document (PDF or image)
    
    Request:
        - file: PDF or image file (multipart/form-data)
    
    Response:
        {
            "success": bool,
            "extracted_text": str,
            "confidence": float,
            "file_type": str
        }
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Extract text based on file type
            file_ext = filename.rsplit('.', 1)[1].lower()
            
            if file_ext == 'pdf':
                # Extract text from PDF
                extracted_text = pdf_reader.extract_text(filepath)
                confidence = 0.95  # PDF extraction is generally reliable
            else:
                # Extract text from image using OCR
                extracted_text, confidence = ocr_service.extract_text_from_image(filepath)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'extracted_text': extracted_text,
                'confidence': confidence,
                'file_type': file_ext
            }), 200
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

