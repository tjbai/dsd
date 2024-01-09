import logging
from datetime import datetime
from typing import Optional

from django.views import generic
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

from .models import Document, Chat
from .services import query_service, upload_service

logging.basicConfig(
    level='DEBUG',
    format='LOG: %(lineno)s:%(funcName)s:%(message)s'
    )

logger = logging.getLogger(__name__)


class HomeView(generic.ListView):
    template_name = 'chat/base_home.html'
    context_object_name = 'documents'
    
    def get_queryset(self): return Document.objects.all()
    
class DocumentView(generic.DetailView):
    template_name = 'chat/base_document.html'
    model = Document
    pk_url_kwarg = 'doc_id'
    
    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['chat_history'] = Chat.objects.filter(document__id=res['object'].id)
        return res
    
def upload_document(request: HttpRequest) -> HttpResponseRedirect:
    message_id: Optional[str] = upload_service.upload_document(document=request.POST['text'])    
    if message_id is None: HttpResponseRedirect('/error')
    
    Document(
        name=request.POST['name'],
        text=request.POST['text'],
        message_id=message_id
    ).save()
    
    return HttpResponseRedirect('/')

def upload_document_callback(request: HttpRequest) -> HttpResponse:
    # TODO -- check request status (worker side)
    
    # TODO -- call upload service (our side)
    
    # TODO -- saved embedded chunks
    
    # TODO -- update embedded status
    
    return HttpResponse(status=204)

def delete_document(request: HttpRequest) -> HttpResponseRedirect:
    return HttpResponseRedirect('/')

# TODO -- decouple schema?
def chat(request: HttpRequest, doc_id: int):
    question = request.POST['question']
    document = get_object_or_404(Document, pk=doc_id)
    chat_history_list = list(Chat.objects.filter(document__pk=doc_id))
    
    answer = query_service.generate_answer(question, document, chat_history_list)
    
    Chat(
        document=document,
        question=question,
        answer=answer,
        date_chatted=datetime.now()
    ).save()
    
    return HttpResponseRedirect(f'/{doc_id}')