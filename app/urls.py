from django.contrib import admin
from django.urls import path
from .views import (
    index, contactanos, nosotros,
    agregar_PC, Listar_PC, modificar_PC, 
    eliminar_pc, registro, agregar_software, listar_software, 
    agregar_al_carrito, ver_carrito, modificar_software, eliminar_software, eliminar_producto, finalizar_compra, productos_view,  limpiar_carrito, agregar_al_carrito
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='index'),
    path('nosotros/', nosotros, name='nosotros'),
    path('contactanos/', contactanos, name='contactanos'),
    path('agregar-PC/', agregar_PC, name='agregar_PC'),
    path('listar-pc/', Listar_PC, name='listar_pc'),
    path('modificar-pc/<int:id>/', modificar_PC, name='modificar_pc'),
    path('eliminar-pc/<int:id>/', eliminar_pc, name='eliminar_pc'),
    path('registro/', registro, name='registro'),
    path('agregar_software/', agregar_software, name='agregar_software'),
    path('listar-software/', listar_software, name='listar_software'),
    path('agregar-al-carrito/<str:producto_tipo>/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver-carrito/', ver_carrito, name='ver_carrito'),
    path('modificar-software/<int:id>/', modificar_software, name='modificar_software'),
    path('eliminar-software/<int:id>/', eliminar_software, name='eliminar_software'), 
    path('eliminar-producto/<int:item_id>/', eliminar_producto, name='eliminar_producto'),
    path('finalizar_compra/', finalizar_compra, name='finalizar_compra'),  
    path('productos/', productos_view, name='productos'),
    path('agregar-al-carrito/<str:producto_tipo>/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('limpiar-carrito/', limpiar_carrito, name='limpiar_carrito'),
 
]
