from django.db import models

class Document(models.Model):
    text = models.CharField(max_length=1000)
    uploaded = models.DateTimeField()
    
    def __str__(self) -> str: return f'{self.uploaded.date()}\n{self.text[:50]}'
    
class Chat(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    
    def __str__(self) -> str: return f'{self.question}\n{self.answer}'