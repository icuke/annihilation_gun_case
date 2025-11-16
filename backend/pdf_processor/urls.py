from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.PDFUploadView.as_view(), name='pdf-upload'),
    path('status/<uuid:document_id>/', views.PDFStatusView.as_view(), name='pdf-status'),
    path('result/<uuid:document_id>/', views.PDFResultView.as_view(), name='pdf-result'),
]