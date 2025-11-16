from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.shortcuts import get_object_or_404
import threading
import os
import json

from .models import PDFDocument
from .serializers import PDFUploadSerializer, PDFDocumentSerializer
from .ocr_scripts.ocr_processor import process_pdf_file

class PDFUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        if 'original_file' not in request.FILES:
            return Response({
                'error': 'no file provided. please include a pdf file with key original_file'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES["original_file"]
        
        if not uploaded_file.name.lower().endswith('.pdf'):
            return Response({
                'error': 'sussy baka only pdfs!!!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        pdf_document = PDFDocument(original_file=uploaded_file)
        pdf_document.save()
        
        processing_thread = threading.Thread(
            target=self.process_pdf_background,
            args=(pdf_document.id,)
        )
        processing_thread.daemon = True
        processing_thread.start()
        
        return Response({
            'message': 'processing pdf',
            'document_id': str(pdf_document.id),
            'status': 'processing',
            'filename': uploaded_file.name
        }, status=status.HTTP_201_CREATED)
    
    def process_pdf_background(self, document_id):
        pdf_document = PDFDocument.objects.get(id=document_id)
        
        try:
            result = process_pdf_file(pdf_document)
            
            if result['success']:
                pdf_document.processed = True
                pdf_document.processing_time = result['processing_time']
                pdf_document.save()
                
                self.save_processing_result(document_id, result['data'])
                print(f"processing completed for document {document_id}")
            else:
                print(f"processing failed for document {document_id}: {result['error']}")
                
        except Exception as e:
            print(f"processing error for document {document_id}: {e}")
    
    def save_processing_result(self, document_id, result_data):
        result_file_path = f"media/ocr_results/{document_id}.json"
        os.makedirs(os.path.dirname(result_file_path), exist_ok=True)
        
        with open(result_file_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

class PDFStatusView(APIView):
    def get(self, request, document_id):
        try:
            pdf_document = get_object_or_404(PDFDocument, id=document_id)
            serializer = PDFDocumentSerializer(pdf_document)
            
            response_data = serializer.data
            
            result_file_path = f"media/ocr_results/{document_id}.json"
            if os.path.exists(result_file_path):
                with open(result_file_path, 'r', encoding='utf-8') as f:
                    response_data['ocr_result'] = json.load(f)
            
            return Response(response_data)
        except Exception as e:
            return Response({
                'error': f'bad document ID: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

class PDFResultView(APIView):
    def get(self, request, document_id):
        try:
            pdf_document = get_object_or_404(PDFDocument, id=document_id)
            
            if not pdf_document.processed:
                return Response({
                    'error': 'processing not completed yet',
                    'status': 'processing'
                }, status=status.HTTP_425_TOO_EARLY)
            
            result_file_path = f"media/ocr_results/{document_id}.json"
            if not os.path.exists(result_file_path):
                return Response({
                    'error': 'result not found (error in uuid?)'
                }, status=status.HTTP_404_NOT_FOUND)
            
            with open(result_file_path, 'r', encoding='utf-8') as f:
                result_data = json.load(f)
            
            return Response({
                'document_id': str(document_id),
                'status': 'completed',
                'result': result_data
            })
        except Exception as e:
            return Response({
                'error': f'bsd document ID: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)