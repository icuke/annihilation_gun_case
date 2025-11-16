import os
import json
import time
from .ocr_caller import process_pdf

def process_pdf_file(pdf_document) -> dict:
    start_time = time.time()
    
    try:
        pdf_path = pdf_document.original_file.path
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        result = process_pdf(pdf_path)
        
        processing_time = time.time() - start_time
        
        return {
            'success': True,
            'data': result,
            'processing_time': processing_time
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'processing_time': time.time() - start_time
        }