from django.urls import path

from . import views


urlpatterns = [
    path('', views.all_documents, name='home'),
    path('<int:doc_id>', views.document, name='document')
]