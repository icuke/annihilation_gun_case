from django.contrib import admin
from .models import PDFDocument

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_file', 'uploaded_at', 'processed', 'processing_time']
    list_filter = ['processed', 'uploaded_at']
    readonly_fields = ['id', 'uploaded_at']