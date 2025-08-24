# --- IMPORTS ---
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from decimal import Decimal
import requests
from .models import Alumno, Consumo, CuentaCorriente, FormaPago, Pago, Grado
from .forms import (GradoForm, AlumnoForm, PagoForm, ConsumoForm, FormaPagoForm, 
                    RegistrarConsumoForm, RegistrarPagoForm)

# --- HELPERS ---
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

# --- GRADOS ---
@login_required
@user_passes_test(is_admin)
def grados_list(request):
    grados = Grado.objects.all().order_by('nombre')
    return render(request, 'core/grados_list.html', {'grados': grados})

@login_required
@user_passes_test(is_admin)
def grado_create(request):
    if request.method == 'POST':
        form = GradoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grados_list')
    else:
        form = GradoForm()
    return render(request, 'core/grado_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def grado_edit(request, pk):
    grado = get_object_or_404(Grado, pk=pk)
    if request.method == 'POST':
        form = GradoForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()
            return redirect('grados_list')
    else:
        form = GradoForm(instance=grado)
    return render(request, 'core/grado_form.html', {'form': form, 'grado': grado})

@login_required
@user_passes_test(is_admin)
def grado_delete(request, pk):
    grado = get_object_or_404(Grado, pk=pk)
    if request.method == 'POST':
        grado.delete()
        return redirect('grados_list')
    return render(request, 'core/grado_confirm_delete.html', {'grado': grado})

# --- PAGOS ---
@login_required
@user_passes_test(is_admin)
def pagos_list(request):
    alumnos = Alumno.objects.all().order_by('nombre')
    alumno_id = request.GET.get('alumno')
    pagos = Pago.objects.select_related('alumno', 'forma_pago').order_by('-fecha')
    if alumno_id:
        pagos = pagos.filter(alumno_id=alumno_id)
    return render(request, 'core/pagos_list.html', {'pagos': pagos, 'alumnos': alumnos, 'alumno_id': alumno_id})

@login_required
@user_passes_test(is_admin)
def pago_create(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagos_list')
    else:
        form = PagoForm(initial={'fecha': timezone.now().date()})
    return render(request, 'core/pago_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def pago_edit(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            return redirect('pagos_list')
    else:
        form = PagoForm(instance=pago)
    return render(request, 'core/pago_form.html', {'form': form, 'pago': pago})

@login_required
@user_passes_test(is_admin)
def pago_delete(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        pago.delete()
        return redirect('pagos_list')
    return render(request, 'core/pago_confirm_delete.html', {'pago': pago})

# --- ALUMNOS ---
@login_required
@user_passes_test(is_admin)
def alumnos_list(request):
    alumnos = Alumno.objects.all().order_by('nombre')
    return render(request, 'core/alumnos_list.html', {'alumnos': alumnos})

@login_required
@user_passes_test(is_admin)
def alumno_create(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alumnos_list')
    else:
        form = AlumnoForm()
    return render(request, 'core/alumno_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('alumnos_list')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'core/alumno_form.html', {'form': form, 'alumno': alumno})

# --- CONSUMOS ---
@login_required
@user_passes_test(is_admin)
def consumos_list(request):
    alumnos = Alumno.objects.all().order_by('nombre')
    alumno_id = request.GET.get('alumno')
    consumos = Consumo.objects.select_related('alumno').order_by('-fecha', '-hora')
    if alumno_id:
        consumos = consumos.filter(alumno_id=alumno_id)
    return render(request, 'core/consumos_list.html', {'consumos': consumos, 'alumnos': alumnos, 'alumno_id': alumno_id})

@login_required
@user_passes_test(is_admin)
def consumo_edit(request, pk):
    consumo = get_object_or_404(Consumo, pk=pk)
    if request.method == 'POST':
        form = ConsumoForm(request.POST, instance=consumo)
        if form.is_valid():
            form.save()
            return redirect('consumos_list')
    else:
        initial = {'fecha': consumo.fecha.strftime('%Y-%m-%d') if consumo.fecha else ''}
        form = ConsumoForm(instance=consumo, initial=initial)
    return render(request, 'core/consumo_form.html', {'form': form, 'consumo': consumo})

@login_required
@user_passes_test(is_admin)
def consumo_delete(request, pk):
    consumo = get_object_or_404(Consumo, pk=pk)
    if request.method == 'POST':
        consumo.delete()
        return redirect('consumos_list')
    return render(request, 'core/consumo_confirm_delete.html', {'consumo': consumo})

# --- FORMAS DE PAGO ---
@login_required
@user_passes_test(is_admin)
def formas_pago_list(request):
    formas = FormaPago.objects.all()
    return render(request, "core/formas_pago_list.html", {"formas": formas})

@login_required
@user_passes_test(is_admin)
def forma_pago_create(request):
    if request.method == 'POST':
        form = FormaPagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formas_pago_list')
    else:
        form = FormaPagoForm()
    return render(request, 'core/forma_pago_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def forma_pago_edit(request, pk):
    forma = get_object_or_404(FormaPago, pk=pk)
    if request.method == 'POST':
        form = FormaPagoForm(request.POST, instance=forma)
        if form.is_valid():
            form.save()
            return redirect('formas_pago_list')
    else:
        form = FormaPagoForm(instance=forma)
    return render(request, 'core/forma_pago_form.html', {'form': form, 'forma': forma})

# --- OTRAS VISTAS ---
def index(request):
    # Determinar la IP del cliente de forma más robusta
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    city = None
    if ip:
        try:
            geo_url = f"https://ip-api.com/json/{ip}?fields=city,status"
            geo_resp = requests.get(geo_url, timeout=3)
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            if geo_data.get('status') == 'success':
                city = geo_data.get('city')
        except requests.exceptions.RequestException:
            city = None
    return render(request, 'core/index.html', {'city': city})

def deuda_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    cuenta, _ = CuentaCorriente.objects.get_or_create(alumno=alumno)
    texto = f"Hola {alumno.nombre}, tu deuda actual en el buffet escolar es de ${cuenta.saldo:.2f}."
    return render(request, "core/deuda_alumno.html", {"alumno": alumno, "cuenta": cuenta, "texto": texto})

def deuda_general(request):
    cuentas = CuentaCorriente.objects.select_related("alumno")
    deudas = [
        {
            "alumno": c.alumno,
            "saldo": c.saldo,
            "texto": f"Hola {c.alumno.nombre}, tu deuda actual en el buffet escolar es de ${c.saldo:.2f}."
        } for c in cuentas if c.saldo > 0
    ]
    return render(request, "core/deuda_general.html", {"deudas": deudas})

@login_required
@user_passes_test(is_admin)
def registrar_consumo(request):
    if request.method == "POST":
        form = ConsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("registrar_consumo")
    else:
        initial = {"fecha": timezone.now().date()}
        form = ConsumoForm(initial=initial)
    return render(request, "core/registrar_consumo.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def registrar_pago(request):
    if request.method == "POST":
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("registrar_pago")
    else:
        initial = {"fecha": timezone.now().date()}
        form = PagoForm(initial=initial)
    return render(request, "core/registrar_pago.html", {"form": form})