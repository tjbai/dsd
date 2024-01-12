from django.db import models
from django.utils import timezone


class Document(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    embedded_successfully = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self) -> str: return f'{self.uploaded.date()}\n{self.text[:50]}'
    
class Chat(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    date_chatted = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str: return f'{self.question}\n{self.answer}'
    
class EmbeddedChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    index = models.IntegerField()
    summary = models.CharField(max_length=int(1e6))
    raw_chunk = models.CharField(max_length=int(1e6))