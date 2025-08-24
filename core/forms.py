from django import forms
from .models import Alumno, Consumo, FormaPago, Pago, Grado

class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ['nombre']

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'grado', 'whatsapp']
        widgets = {
            'grado': forms.Select(attrs={'class': 'form-control'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['alumno', 'forma_pago', 'importe', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'alumno': forms.Select(attrs={'class': 'form-control'}),
            'forma_pago': forms.Select(attrs={'class': 'form-control'}),
        }

class ConsumoForm(forms.ModelForm):
    class Meta:
        model = Consumo
        fields = ['fecha', 'hora', 'alumno', 'detalle', 'importe']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'alumno': forms.Select(attrs={'class': 'form-control'}),
            'detalle': forms.TextInput(attrs={'class': 'form-control'}),
            'importe': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }

class FormaPagoForm(forms.ModelForm):
    class Meta:
        model = FormaPago
        fields = ['nombre']

class RegistrarConsumoForm(forms.Form):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all().order_by('nombre'))
    detalle = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    importe = forms.DecimalField(max_digits=10, decimal_places=2)

class RegistrarPagoForm(forms.Form):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all().order_by('nombre'))
    forma_pago = forms.ModelChoiceField(queryset=FormaPago.objects.all().order_by('nombre'))
    importe = forms.DecimalField(max_digits=10, decimal_places=2)
