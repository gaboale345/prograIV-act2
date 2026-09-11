# Create your models here.
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad en stock")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} (Stock: {self.cantidad} - ${self.precio})"
