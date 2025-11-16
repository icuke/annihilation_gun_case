from django.db import models
import uuid
import os

def pdf_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('pdf_uploads', filename)

class PDFDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_file = models.FileField(upload_to=pdf_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processing_time = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'pdf_documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"PDF {self.id} - {'Processed' if self.processed else 'Pending'}"
    
    def delete(self, *args, **kwargs):
        if self.original_file:
            if os.path.isfile(self.original_file.path):
                os.remove(self.original_file.path)
        super().delete(*args, **kwargs)