from datetime import datetime

from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    date_uploaded = models.DateTimeField(default=datetime.now())
    date_completed = models.DateTimeField(default=datetime.now())
    completed = models.BooleanField()
    
    def __str__(self) -> str: return f'{self.uploaded.date()}\n{self.text[:50]}'
    
class Chat(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    date_chatted = models.DateTimeField()
    
    def __str__(self) -> str: return f'{self.question}\n{self.answer}'