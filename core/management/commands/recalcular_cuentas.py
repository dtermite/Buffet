from django.core.management.base import BaseCommand
from core.models import CuentaCorriente, Alumno
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Recalcula y actualiza los totales de consumos y pagos en todas las cuentas corrientes.'

    def handle(self, *args, **options):
        cuentas = CuentaCorriente.objects.select_related('alumno')
        for cuenta in cuentas:
            total_consumido = cuenta.alumno.consumo_set.aggregate(s=Sum('importe'))['s'] or 0
            total_pagado = cuenta.alumno.pago_set.aggregate(s=Sum('importe'))['s'] or 0
            cuenta.total_consumido = total_consumido
            cuenta.total_pagado = total_pagado
            cuenta.save()
            self.stdout.write(self.style.SUCCESS(
                f'Cuenta de {cuenta.alumno.nombre}: consumido={total_consumido}, pagado={total_pagado}, saldo={cuenta.saldo}'
            ))
        self.stdout.write(self.style.SUCCESS('¡Todas las cuentas corrientes fueron recalculadas!'))
