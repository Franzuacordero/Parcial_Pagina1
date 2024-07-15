from django.contrib import admin
from .models import PC, Software, Contactanos, ItemCarrito

# Register your models here.

admin.site.register(PC)
admin.site.register(Software)
admin.site.register(Contactanos)
class ItemCarritoAdmin(admin.ModelAdmin):
    actions = None # Eliminar acciones por defecto para evitar agregar o eliminar desde la administración


