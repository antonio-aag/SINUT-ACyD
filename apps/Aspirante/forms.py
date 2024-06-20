from django import forms
from .models import documentos

class PdfFileForm(forms.ModelForm):
    class Meta:
        model = documentos
        fields = ['file']