from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_construccion, name='inicio_construccion'),
    
    # URLs para Empleados
    path('empleado/agregar_empleado/', views.agregar_empleado, name='agregar_empleado'),
    path('empleado/ver_empleado/', views.ver_empleados, name='ver_empleados'),
    path('empleado/actualizar_empleado/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleado/realizar_actualizacion_empleado/<int:empleado_id>/', views.realizar_actualizacion_empleado, name='realizar_actualizacion_empleado'),
    path('empleado/borrar_empleado/<int:empleado_id>/', views.borrar_empleado, name='borrar_empleado'),
    
    # URLs para Clientes
    path('cliente/agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('cliente/ver_cliente/', views.ver_clientes, name='ver_clientes'),
    path('cliente/actualizar_cliente/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cliente/realizar_actualizacion_cliente/<int:cliente_id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('cliente/borrar_cliente/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
]