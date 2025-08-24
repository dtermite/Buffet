from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Grado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.grado})"

class FormaPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Consumo(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=255)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.alumno.nombre}: {self.detalle} (${self.importe})"

class CuentaCorriente(models.Model):
    alumno = models.OneToOneField(Alumno, on_delete=models.CASCADE)
    total_consumido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def saldo(self):
        return self.total_consumido - self.total_pagado

    def __str__(self):
        return f"{self.alumno.nombre} - Saldo: ${self.saldo}"

class Pago(models.Model):
    fecha = models.DateField()
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.alumno.nombre}: ${self.importe} ({self.forma_pago})"

@receiver(post_save, sender=Alumno)
def crear_cuenta_corriente(sender, instance, created, **kwargs):
    if created:
        CuentaCorriente.objects.create(alumno=instance)

@receiver(post_save, sender=Consumo)
def actualizar_cuenta_por_consumo(sender, instance, created, **kwargs):
    if created:
        cuenta, _ = CuentaCorriente.objects.get_or_create(alumno=instance.alumno)
        cuenta.total_consumido += instance.importe
        cuenta.save()

@receiver(post_delete, sender=Consumo)
def revertir_cuenta_por_consumo(sender, instance, **kwargs):
    cuenta, _ = CuentaCorriente.objects.get_or_create(alumno=instance.alumno)
    cuenta.total_consumido -= instance.importe
    cuenta.save()

@receiver(post_save, sender=Pago)
def actualizar_cuenta_por_pago(sender, instance, created, **kwargs):
    if created:
        cuenta, _ = CuentaCorriente.objects.get_or_create(alumno=instance.alumno)
        cuenta.total_pagado += instance.importe
        cuenta.save()

@receiver(post_delete, sender=Pago)
def revertir_cuenta_por_pago(sender, instance, **kwargs):
    cuenta, _ = CuentaCorriente.objects.get_or_create(alumno=instance.alumno)
    cuenta.total_pagado -= instance.importe
    cuenta.save()