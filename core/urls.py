

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Consumos
    path('consumos/', views.consumos_list, name='consumos_list'),
    path('consumos/<int:pk>/editar/', views.consumo_edit, name='consumo_edit'),
    path('consumos/<int:pk>/eliminar/', views.consumo_delete, name='consumo_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('deuda/<int:alumno_id>/', views.deuda_alumno, name='deuda_alumno'),
    path('deuda/', views.deuda_general, name='deuda_general'),
    path('registrar_consumo/', views.registrar_consumo, name='registrar_consumo'),
    path('registrar_pago/', views.registrar_pago, name='registrar_pago'),

    # Grados
    path('grados/', views.grados_list, name='grados_list'),
    path('grados/nuevo/', views.grado_create, name='grado_create'),
    path('grados/<int:pk>/editar/', views.grado_edit, name='grado_edit'),
    path('grados/<int:pk>/eliminar/', views.grado_delete, name='grado_delete'),

    # Alumnos
    path('alumnos/', views.alumnos_list, name='alumnos_list'),
    path('alumnos/nuevo/', views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/editar/', views.alumno_edit, name='alumno_edit'),

    # Formas de pago
    path('formas_pago/', views.formas_pago_list, name='formas_pago_list'),
    path('formas_pago/nuevo/', views.forma_pago_create, name='forma_pago_create'),
    path('formas_pago/<int:pk>/editar/', views.forma_pago_edit, name='forma_pago_edit'),
    # Pagos
    path('pagos/', views.pagos_list, name='pagos_list'),
    path('pagos/nuevo/', views.pago_create, name='pago_create'),
    path('pagos/<int:pk>/editar/', views.pago_edit, name='pago_edit'),
    path('pagos/<int:pk>/eliminar/', views.pago_delete, name='pago_delete'),

    # Cuentas Corrientes
    path('cuentas_corrientes/', views.cuentas_corrientes, name='cuentas_corrientes'),
    path('cuentas_corrientes/exportar/', views.exportar_cuentas_corrientes_excel, name='exportar_cuentas_corrientes_excel'),
    path('cuentas_corrientes/exportar_excel/', views.exportar_cuentas_corrientes_excel, name='exportar_cuentas_corrientes_excel_alias'),

    # Parámetros
    path('parametros/', views.parametros_edit, name='parametros_edit'),
]
