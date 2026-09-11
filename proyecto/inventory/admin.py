# Register your models here.
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'cantidad', 'fecha_creacion', 'fecha_actualizacion')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
