from django.shortcuts import render, redirect, get_object_or_404
from .models import PC, Software, ItemCarrito, Carrito, ItemOrden , Orden
from .forms import ContactanosForm, PCForm, SoftwareForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import HttpResponse
from django.contrib.contenttypes.models import ContentType
import json

# Create your views here.

def index(request):
    pcs = PC.objects.all()
    software = Software.objects.all()
    return render(request, 'app/index.html', {'pcs': pcs, 'software': software})


def nosotros(request):
    return render(request, 'app/nosotros.html')



def contactanos(request):
    data = {
        'form': ContactanosForm()
    }
    if request.method == 'POST':
        formulario = ContactanosForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()  # Guarda el formulario si es válido
            data["mensaje"] = "¡Contacto guardado!"
        else:
            data["form"] = formulario  # Pasa el formulario con errores de vuelta al contexto
    return render(request, 'app/contactanos.html', data)
    


@login_required
@permission_required('app.add_pc', raise_exception=True)
def agregar_PC(request):
    data = {}
    if request.method == 'POST':
        form = PCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto Registrado")
            form = PCForm()  # Limpiar el formulario para un nuevo ingreso
    else:
        form = PCForm()
    
    return render(request, 'app/productos/agregar_PC.html', {'form': form, 'mensaje': data.get('mensaje', '')})

@login_required
@permission_required('app.add_software', raise_exception=True)
def agregar_software(request):
    data = {}
    if request.method == 'POST':
        form = SoftwareForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto Registrado")
            form = SoftwareForm()  # Limpiar el formulario para un nuevo ingreso
    else:
        form = SoftwareForm()
    
    return render(request, 'app/productos/agregar_software.html', {'form': form, 'mensaje': data.get('mensaje', '')})

@login_required
@permission_required('app.view_pc')
def Listar_PC(request):
    pcs = PC.objects.all()  # Obtener todos los objetos PC de la base de datos

    context = {
        'pcs': pcs,  # Pasar 'pcs' como contexto a la plantilla
    }

    return render(request, 'app/productos/listar_pc.html', context)


@login_required
@permission_required('app.view_software', raise_exception=True)
def listar_software(request):
    software_list = Software.objects.all()
    return render(request, 'app/productos/listar_software.html', {'software_list': software_list})




@login_required
@permission_required('app.change_pc', raise_exception=True)
def modificar_PC(request, id):
    pc = get_object_or_404(PC, id=id)
    if request.method == 'POST':
        form = PCForm(request.POST, request.FILES, instance=pc)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto modificado correctamente")
            return redirect("listar_pc")
    else:
        form = PCForm(instance=pc)

    context = {'form': form, 'pc': pc}
    return render(request, 'app/productos/modificar_pc.html', context)

@login_required
@permission_required('app.delete_pc', raise_exception=True)
def eliminar_pc(request, id):
    pc = get_object_or_404(PC, id=id)
    pc.delete()
    messages.success(request, "Producto eliminado correctamente")
    return redirect("listar_pc")

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            if user is not None:
                login(request, user)
                messages.success(request, "Te has registrado correctamente")
                return redirect(to="index")
            else:
                messages.error(request, "Error en la autenticación")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)


@login_required
def agregar_al_carrito(request, producto_tipo, producto_id):
    usuario = request.user
    carrito, created = Carrito.objects.get_or_create(usuario=usuario)

    if producto_tipo == 'pc':
        producto = get_object_or_404(PC, id=producto_id)
    elif producto_tipo == 'software':
        producto = get_object_or_404(Software, id=producto_id)
    else:
        return HttpResponse('Tipo de producto no válido', status=400)

    item, item_created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        content_type=ContentType.objects.get_for_model(producto),
        object_id=producto.id
    )

    if not item_created:
        item.cantidad += 1
        item.save()

    messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('ver_carrito')


@login_required
def ver_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)

    items_list = []
    total = 0

    for item in items:
        try:
            # Obtener el modelo de producto basado en content_type
            producto_model = item.content_type.model_class()

            # Obtener el producto específico
            producto = get_object_or_404(producto_model, id=item.object_id)

            # Calcular subtotal del producto en el carrito
            subtotal = producto.precio * item.cantidad

            # Añadir detalles del producto al listado de items
            item_details = {
                'id': item.id,  # Agregar el ID del item para identificación en la plantilla
                'nombre': producto.nombre,
                'cantidad': item.cantidad,
                'precio': producto.precio,
                'subtotal': subtotal,
            }

            # Agregar el tipo específico de producto (PC o Software) al diccionario de detalles
            if isinstance(producto, PC):
                item_details['pc'] = producto
            elif isinstance(producto, Software):
                item_details['software'] = producto

            items_list.append(item_details)
            total += subtotal

        except producto_model.DoesNotExist as e:
            print(f"Error al recuperar producto: {e}")
            continue
        except Exception as e:
            print(f"Error general: {e}")
            continue

    context = {
        'items': items_list,
        'total': total,
    }

    return render(request, 'app/carrito/ver_carrito.html', context)



@login_required
@require_POST
def eliminar_producto(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            item = ItemCarrito.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'message': 'Producto eliminado correctamente del carrito.'})
        except ItemCarrito.DoesNotExist:
            return JsonResponse({'error': 'El producto no existe en el carrito.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)


@login_required
def limpiar_carrito(request):
    # Obtener todos los ítems del carrito y eliminarlos
    items_carrito = ItemCarrito.objects.all()
    items_carrito.delete()

    # Redirigir de vuelta a la página del carrito
    return redirect('ver_carrito')
    
    
@login_required
def finalizar_compra(request):
    if request.method == 'POST':
        usuario = request.user
        carrito = Carrito.objects.get(usuario=usuario)
        items_carrito = ItemCarrito.objects.filter(carrito=carrito)

        if not items_carrito:
            messages.warning(request, 'Tu carrito está vacío.')
            return redirect('ver_carrito')

        total = sum(item.producto.precio * item.cantidad for item in items_carrito)
        orden = Orden.objects.create(usuario=usuario, total=total)

        for item in items_carrito:
            ItemOrden.objects.create(
                orden=orden,
                content_type=item.content_type,
                object_id=item.object_id,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.producto.precio
            )

        items_carrito.delete()
        messages.success(request, 'Compra finalizada con éxito.')
        return redirect('ver_carrito')
    else:
        return redirect('ver_carrito')



@login_required
@permission_required('app.delete_software', raise_exception=True)
def eliminar_software(request, id):
    software = get_object_or_404(Software, id=id)
    software.delete()
    messages.success(request, "Producto eliminado correctamente")
    return redirect('listar_software')

@login_required
@permission_required('app.change_software', raise_exception=True)
def modificar_software(request, id):
    software = get_object_or_404(Software, id=id)
    if request.method == 'POST':
        form = SoftwareForm(request.POST, request.FILES, instance=software)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto modificado correctamente")
            return redirect('listar_software')
    else:
        form = SoftwareForm(instance=software)

    context = {'form': form, 'software': software}
    return render(request, 'app/productos/modificar_software.html', context)


def productos_view(request):  
    tipo_producto = request.GET.get('tipo_producto', 'todos')

    if tipo_producto == 'pc':
        productos_pc = PC.objects.filter(visible_al_usuario=True)
        productos_software = []
    elif tipo_producto == 'software':
        productos_pc = []
        productos_software = Software.objects.filter(visible_al_usuario=True)
    else:
        productos_pc = PC.objects.filter(visible_al_usuario=True)
        productos_software = Software.objects.filter(visible_al_usuario=True)

    tipos_productos = {
        'pc': 'PCs',
        'software': 'Software'
    }

    return render(request, 'app/productos.html', {
        'productos_pc': productos_pc,
        'productos_software': productos_software,
        'tipos_productos': tipos_productos,
        'seleccionados': [tipo_producto]
    })






