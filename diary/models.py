from django.utils import timezone
from django.db import models
from user.models import User

class Diary(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500, null = True, blank = True)
    update = models.DateTimeField(default = timezone.now)
    timestamp = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name_plural = 'Diaries'
    
    def __str__(self):
        return self.name
    
class Entry(models.Model):
    diary = models.ForeignKey(Diary)
    title = models.CharField(max_length = 100)
    body = models.TextField()
    update = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name_plural = 'Entries'
    
    def __str__(self):
        return self.title