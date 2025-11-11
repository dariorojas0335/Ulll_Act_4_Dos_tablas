# Segunda Parte: Implementación del CRUD para Clientes

## Estructura Actualizada

```
UIII_Construccion_0335/
├── backend_Construccion/
│   ├── backend_Construccion/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── app_Construccion/
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── templates/
│   │   │   ├── empleado/
│   │   │   │   ├── agregar_empleado.html
│   │   │   │   ├── ver_empleado.html
│   │   │   │   ├── actualizar_empleado.html
│   │   │   │   └── borrar_empleado.html
│   │   │   ├── cliente/
│   │   │   │   ├── agregar_cliente.html
│   │   │   │   ├── ver_cliente.html
│   │   │   │   ├── actualizar_cliente.html
│   │   │   │   └── borrar_cliente.html
│   │   │   ├── base.html
│   │   │   ├── header.html
│   │   │   ├── navbar.html
│   │   │   ├── footer.html
│   │   │   └── inicio.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   └── db.sqlite3
└── .venv/
```

## Archivos Actualizados

### 1. models.py (corregido)
```python
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_cliente = models.CharField(
        max_length=50,
        choices=[
            ("Residencial", "Residencial"),
            ("Comercial", "Comercial"),
            ("Gubernamental", "Gubernamental"),
        ],
        default="Residencial"
    )
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"

class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="proyectos")
    empleados = models.ManyToManyField(Empleado, related_name="proyectos")
    estado = models.CharField(
        max_length=50,
        choices=[
            ("En planificación", "En planificación"),
            ("En curso", "En curso"),
            ("Finalizado", "Finalizado"),
        ],
        default="En planificación",
    )

    def __str__(self):
        return self.nombre
```

### 2. views.py (actualizado con funciones para Cliente)
```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Cliente

def inicio_construccion(request):
    return render(request, 'inicio.html')

# Funciones para Empleados
def agregar_empleado(request):
    if request.method == 'POST':
        empleado = Empleado(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            cargo=request.POST['cargo'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario']
        )
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleado/agregar_empleado.html')

def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleado/ver_empleado.html', {'empleados': empleados})

def actualizar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.cargo = request.POST['cargo']
        empleado.telefono = request.POST['telefono']
        empleado.email = request.POST['email']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleado/actualizar_empleado.html', {'empleado': empleado})

def realizar_actualizacion_empleado(request, empleado_id):
    return actualizar_empleado(request, empleado_id)

def borrar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleado/borrar_empleado.html', {'empleado': empleado})

# Funciones para Clientes
def agregar_cliente(request):
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            tipo_cliente=request.POST['tipo_cliente'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            direccion=request.POST['direccion']
        )
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'cliente/agregar_cliente.html')

def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/ver_cliente.html', {'clientes': clientes})

def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.tipo_cliente = request.POST['tipo_cliente']
        cliente.telefono = request.POST['telefono']
        cliente.email = request.POST['email']
        cliente.direccion = request.POST['direccion']
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente})

def realizar_actualizacion_cliente(request, cliente_id):
    return actualizar_cliente(request, cliente_id)

def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})
```

### 3. urls.py (app_Construccion - actualizado)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_construccion, name='inicio_construccion'),
    
    # URLs para Empleados
    path('empleado/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleado/ver/', views.ver_empleados, name='ver_empleados'),
    path('empleado/actualizar/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleado/realizar_actualizacion/<int:empleado_id>/', views.realizar_actualizacion_empleado, name='realizar_actualizacion_empleado'),
    path('empleado/borrar/<int:empleado_id>/', views.borrar_empleado, name='borrar_empleado'),
    
    # URLs para Clientes
    path('cliente/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('cliente/ver/', views.ver_clientes, name='ver_clientes'),
    path('cliente/actualizar/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cliente/realizar_actualizacion/<int:cliente_id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('cliente/borrar/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
]
```

### 4. admin.py (actualizado)
```python
from django.contrib import admin
from .models import Empleado, Cliente, Proyecto

admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Proyecto)
```

### 5. navbar.html (actualizado)
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="{% url 'inicio_construccion' %}">
            🏗️ Sistema de Administración Construcción
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'inicio_construccion' %}">
                        🏠 Inicio
                    </a>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        👥 Empleados
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'agregar_empleado' %}">Agregar Empleado</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_empleados' %}">Ver Empleados</a></li>
                    </ul>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        👨‍💼 Clientes
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'agregar_cliente' %}">Agregar Cliente</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_clientes' %}">Ver Clientes</a></li>
                        <li><a class="dropdown-item" href="#">Actualizar Clientes</a></li>
                        <li><a class="dropdown-item" href="#">Borrar Clientes</a></li>
                    </ul>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        📋 Proyectos
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Agregar Proyecto</a></li>
                        <li><a class="dropdown-item" href="#">Ver Proyectos</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

## Nuevos Templates para Cliente

### 6. agregar_cliente.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0">Agregar Nuevo Cliente</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {% csrf_token %}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nombre" class="form-label">Nombre</label>
                            <input type="text" class="form-control" id="nombre" name="nombre" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="apellido" class="form-label">Apellido</label>
                            <input type="text" class="form-control" id="apellido" name="apellido" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="tipo_cliente" class="form-label">Tipo de Cliente</label>
                        <select class="form-select" id="tipo_cliente" name="tipo_cliente" required>
                            <option value="Residencial">Residencial</option>
                            <option value="Comercial">Comercial</option>
                            <option value="Gubernamental">Gubernamental</option>
                        </select>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="telefono" class="form-label">Teléfono</label>
                            <input type="text" class="form-control" id="telefono" name="telefono" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="direccion" class="form-label">Dirección</label>
                        <textarea class="form-control" id="direccion" name="direccion" rows="3" required></textarea>
                    </div>
                    
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'ver_clientes' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-success">Guardar Cliente</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 7. ver_cliente.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="card">
    <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
        <h4 class="mb-0">Lista de Clientes</h4>
        <a href="{% url 'agregar_cliente' %}" class="btn btn-light">➕ Agregar Cliente</a>
    </div>
    <div class="card-body">
        {% if clientes %}
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Nombre</th>
                        <th>Apellido</th>
                        <th>Tipo Cliente</th>
                        <th>Teléfono</th>
                        <th>Email</th>
                        <th>Dirección</th>
                        <th>Fecha Registro</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for cliente in clientes %}
                    <tr>
                        <td>{{ cliente.nombre }}</td>
                        <td>{{ cliente.apellido }}</td>
                        <td>
                            <span class="badge 
                                {% if cliente.tipo_cliente == 'Residencial' %}bg-primary
                                {% elif cliente.tipo_cliente == 'Comercial' %}bg-warning
                                {% else %}bg-info{% endif %}">
                                {{ cliente.tipo_cliente }}
                            </span>
                        </td>
                        <td>{{ cliente.telefono }}</td>
                        <td>{{ cliente.email }}</td>
                        <td>{{ cliente.direccion }}</td>
                        <td>{{ cliente.fecha_registro }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <a href="{% url 'actualizar_cliente' cliente.id %}" class="btn btn-warning btn-sm">✏️ Editar</a>
                                <a href="{% url 'borrar_cliente' cliente.id %}" class="btn btn-danger btn-sm">🗑️ Borrar</a>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="alert alert-info text-center">
            <h5>No hay clientes registrados</h5>
            <p>Comienza agregando el primer cliente al sistema.</p>
            <a href="{% url 'agregar_cliente' %}" class="btn btn-success">Agregar Primer Cliente</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### 8. actualizar_cliente.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-warning text-dark">
                <h4 class="mb-0">Actualizar Cliente</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {% csrf_token %}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nombre" class="form-label">Nombre</label>
                            <input type="text" class="form-control" id="nombre" name="nombre" value="{{ cliente.nombre }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="apellido" class="form-label">Apellido</label>
                            <input type="text" class="form-control" id="apellido" name="apellido" value="{{ cliente.apellido }}" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="tipo_cliente" class="form-label">Tipo de Cliente</label>
                        <select class="form-select" id="tipo_cliente" name="tipo_cliente" required>
                            <option value="Residencial" {% if cliente.tipo_cliente == "Residencial" %}selected{% endif %}>Residencial</option>
                            <option value="Comercial" {% if cliente.tipo_cliente == "Comercial" %}selected{% endif %}>Comercial</option>
                            <option value="Gubernamental" {% if cliente.tipo_cliente == "Gubernamental" %}selected{% endif %}>Gubernamental</option>
                        </select>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="telefono" class="form-label">Teléfono</label>
                            <input type="text" class="form-control" id="telefono" name="telefono" value="{{ cliente.telefono }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" value="{{ cliente.email }}" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="direccion" class="form-label">Dirección</label>
                        <textarea class="form-control" id="direccion" name="direccion" rows="3" required>{{ cliente.direccion }}</textarea>
                    </div>
                    
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'ver_clientes' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-warning">Actualizar Cliente</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 9. borrar_cliente.html
```html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h4 class="mb-0">Confirmar Eliminación</h4>
            </div>
            <div class="card-body text-center">
                <h5>¿Está seguro que desea eliminar al cliente?</h5>
                <p class="lead">{{ cliente.nombre }} {{ cliente.apellido }}</p>
                <p><strong>Tipo Cliente:</strong> {{ cliente.tipo_cliente }}</p>
                <p><strong>Email:</strong> {{ cliente.email }}</p>
                <p><strong>Teléfono:</strong> {{ cliente.telefono }}</p>
                
                <form method="POST">
                    {% csrf_token %}
                    <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <a href="{% url 'ver_clientes' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Confirmar Eliminación</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Comandos para Ejecutar

### Paso 2: Realizar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 10: Registrar modelos y migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 16: Ejecutar servidor
```bash
python manage.py runserver 8032
```

## Características Implementadas

✅ **CRUD completo para Clientes**:
- Agregar nuevos clientes
- Ver lista de clientes en tabla
- Actualizar información de clientes
- Borrar clientes

✅ **Diseño moderno y atractivo**:
- Colores suaves (verde para clientes)
- Bootstrap 5 para diseño responsivo
- Iconos y badges para mejor visualización
- Tablas responsivas

✅ **Estructura organizada**:
- Carpeta `cliente` dentro de templates
- URLs específicas para operaciones CRUD
- Vistas separadas para cada funcionalidad

✅ **Funcionalidades**:
- Navegación actualizada en navbar
- Formularios sin validación (como se solicitó)
- Mensajes de confirmación para borrado
- Diseño consistente con el resto del sistema

El proyecto está totalmente funcional y listo para usar en el puerto 8032.
