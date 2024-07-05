from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PC(models.Model):
    nombre = models.CharField(max_length=100)
    procesador = models.CharField(max_length=100)
    tarjeta_grafica = models.CharField(max_length=100)
    placa_base = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    almacenamiento = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="PC", null=True)

    def __str__(self):
        return self.nombre
    
class Software(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="software", null=True)

    def __str__(self):
        return self.nombre

opciones_consultas = [
     [0, "consulta"],
     [1, "reclamo"],
     [2, "sugerencia"],
     [3, "felicitaciones"] 
]

class Contactanos(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre



class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = 0
        for item in self.items.all():
            if item.producto_tipo == 'PC':
                total += item.cantidad * PC.objects.get(id=item.producto_id).precio
            elif item.producto_tipo == 'Software':
                total += item.cantidad * Software.objects.get(id=item.producto_id).precio
        return total


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto_tipo = models.CharField(max_length=20)  # 'PC' o 'Software'
    producto_id = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.producto_tipo} - {self.producto_id}'

    class Meta:
        verbose_name = 'Item de Carrito'
        verbose_name_plural = 'Items de Carrito'