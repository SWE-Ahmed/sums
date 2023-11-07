from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Create your models here.

class Submission(models.Model):
    
    title = models.TextField(max_length=100)
    field = models.CharField(max_length=50)
    paper = models.FileField(null=True, validators=[FileExtensionValidator( ['pdf'] ) ])
    startSection = models.CharField(max_length=50, blank=True)
    endSection = models.CharField(max_length=50, blank=True)
    summary = models.TextField(max_length=1000, blank=True, editable=False)
    date = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self) -> str:
        return self.title