from rest_framework import serializers
from .models import PDFDocument

class PDFUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['original_file']

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['id', 'original_file', 'uploaded_at', 'processed', 'processing_time']
        read_only_fields = ['id', 'uploaded_at', 'processed', 'processing_time']