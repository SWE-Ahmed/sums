from django import forms
from .models import Submission

class sumForm(forms.ModelForm):
    
    class Meta:
        model = Submission
        fields = "__all__"