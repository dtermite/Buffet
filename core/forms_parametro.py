from django import forms
from .models import Parametro

class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = ['mensaje_whatsapp']
        widgets = {
            'mensaje_whatsapp': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'mensaje_whatsapp': 'Texto base para WhatsApp',
        }
