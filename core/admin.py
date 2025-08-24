from django.contrib import admin
from .models import Alumno, FormaPago, Consumo, CuentaCorriente

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
	list_display = ("nombre", "grado", "whatsapp")
	search_fields = ("nombre", "grado", "whatsapp")

@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
	list_display = ("nombre",)
	search_fields = ("nombre",)

@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
	list_display = ("fecha", "alumno", "detalle", "importe")
	list_filter = ("fecha", "alumno")
	search_fields = ("detalle",)

@admin.register(CuentaCorriente)
class CuentaCorrienteAdmin(admin.ModelAdmin):
	list_display = ("alumno", "total_consumido", "total_pagado", "saldo")
