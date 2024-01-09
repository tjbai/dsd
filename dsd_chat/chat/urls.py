from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # display
    path('', views.HomeView.as_view(), name='home_page'),
    path('<int:doc_id>', views.DocumentView.as_view(), name='document_page'),
    path('upload', TemplateView.as_view(template_name='chat/base_upload.html'), name='upload_document_page'),
    
    # api 
    path('api/upload', views.upload_document, name='upload_document_api'),
    path('api/upload/callback', views.upload_document_callback, name='upload_document_callback_api'),
    path('api/chat/<int:doc_id>', views.chat, name='chat_api'),
]