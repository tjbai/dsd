from datetime import datetime
import logging

from django.views import generic
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Document, Chat
from .lib.rag import generate_answer

logging.basicConfig(
    level='DEBUG',
    format='%(lineno)s:%(funcName)s:%(message)s'
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
    
def upload_document(request: HttpRequest):
    Document(
        name=request.POST['name'],
        text=request.POST['text'],
        uploaded=datetime.now()
    ).save()
    
    logger.debug(request.POST)
    
    return HttpResponseRedirect('/')

# TODO -- think about changing up schema to be less coupled between question/answer
def chat(request: HttpRequest, doc_id: int):
    question = request.POST['question']
    document = get_object_or_404(Document, pk=doc_id)
    
    # TODO -- convert to some dictionary/string representation
    _chat_history = Chat.objects.filter(document__pk=doc_id)
    
    answer = generate_answer(question, document)
    
    Chat(
        document=document,
        question=question,
        answer=answer,
        when=datetime.now()
    ).save()
    
    return HttpResponseRedirect(f'/{doc_id}')