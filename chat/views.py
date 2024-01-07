from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest

from .models import Document


def all_documents(request) -> HttpResponse:
    return render(request, 'chat/base_home.html', {'documents': Document.objects.all()})

def document(request: HttpRequest, doc_id: int) -> HttpResponse:
    doc = get_object_or_404(Document, pk=doc_id)
    return render(request, 'chat/base_document.html', {'doc': doc})