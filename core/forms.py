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


# NUEVO PagoForm desde cero
from django.utils import timezone
class PagoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import CuentaCorriente
        if self.instance and self.instance.pk:
            # Edición: solo mostrar el alumno actual y deshabilitar el campo
            self.fields['alumno'].queryset = Alumno.objects.filter(pk=self.instance.alumno.pk)
            self.fields['alumno'].disabled = True
        else:
            alumnos_con_deuda = [c.alumno.pk for c in CuentaCorriente.objects.select_related('alumno') if c.saldo > 0]
            self.fields['alumno'].queryset = Alumno.objects.filter(pk__in=alumnos_con_deuda).order_by('nombre')
        self.fields['forma_pago'].queryset = FormaPago.objects.all().order_by('nombre')
        self.fields['fecha'].initial = timezone.now().date()
        self.fields['alumno'].widget.attrs.update({'class': 'form-control'})
        self.fields['forma_pago'].widget.attrs.update({'class': 'form-control'})
        self.fields['importe'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        self.fields['fecha'].widget.attrs.update({'class': 'form-control', 'type': 'date'})

    def clean(self):
        cleaned_data = super().clean()
        alumno = self.instance.alumno if self.instance and self.instance.pk else cleaned_data.get('alumno')
        importe = cleaned_data.get('importe')
        if alumno and importe is not None:
            from .models import CuentaCorriente, Pago
            cuenta = CuentaCorriente.objects.get(alumno=alumno)
            deuda = cuenta.saldo
            if self.instance and self.instance.pk:
                # Si está editando, sumar el importe anterior a la deuda
                deuda += self.instance.importe
            if importe > deuda:
                self.add_error('importe', f'El importe no puede ser mayor a la deuda (${deuda:.2f})')
        return cleaned_data

    class Meta:
        model = Pago
        fields = ['alumno', 'forma_pago', 'importe', 'fecha']

class ConsumoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].queryset = Alumno.objects.all().order_by('nombre')
        from django.utils import timezone
        if not self.instance.pk:
            self.fields['fecha'].initial = timezone.now().date()
            self.fields['hora'].initial = timezone.now().time().strftime('%H:%M')
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
