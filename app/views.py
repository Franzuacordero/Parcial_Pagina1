from django.shortcuts import render, redirect, get_object_or_404
from .models import PC, Software, ItemCarrito, Carrito
from .forms import ContactanosForm, PCForm, SoftwareForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

# Create your views here.

def index(request):
    pcs = PC.objects.all()
    software = Software.objects.all()
    return render(request, 'app/index.html', {'pcs': pcs, 'software': software})

def VistaPC(request):
    pcs = PC.objects.all()
    return render(request, 'app/VistaPC.html', {'pcs': pcs})

def VistaSoftware(request):
    software = Software.objects.all()
    return render(request, 'app/VistaSoftware.html', {'software': software})

def carrito(request):
    # Aquí deberías obtener los items del carrito del usuario actual.
    # Por simplicidad, obtendremos todos los PCs y software. 
    # Modifica según tu lógica de carrito.
    pcs = PC.objects.all()
    software = Software.objects.all()
    return render(request, 'app/carrito.html', {'pcs': pcs, 'software': software})

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
    


@permission_required('app.add_pc')
def agregar_PC(request):
    data = {}
    if request.method == 'POST':
        form = PCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto Registrado")
            # Limpiar el formulario para un nuevo ingreso
            form = PCForm()
    else:
        form = PCForm()
    
    return render(request, 'app/productos/agregar_PC.html', {'form': form, 'mensaje': data.get('mensaje', '')})

def agregar_software(request):
    data = {}
    if request.method == 'POST':
        form = SoftwareForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            data["mensaje"] = "Producto guardado correctamente."
            # Limpiar el formulario para un nuevo ingreso
            form = SoftwareForm()
    else:
        form = SoftwareForm()
    
    return render(request, 'app/productos/agregar_software.html', {'form': form, 'mensaje': data.get('mensaje', '')})


@permission_required('app.view_pc')
def Listar_PC(request):
    pcs = PC.objects.all()  # Obtener todos los objetos PC de la base de datos

    context = {
        'pcs': pcs,  # Pasar 'pcs' como contexto a la plantilla
    }

    return render(request, 'app/productos/listar_pc.html', context)


def listar_software(request):
    software_list = Software.objects.all()  # Obtener todos los objetos de Software de la base de datos

    context = {
        'software_list': software_list,  # Pasar 'software_list' como contexto a la plantilla
    }

    return render(request, 'app/productos/listar_software.html', context)




@permission_required('app.change_pc')
def modificar_PC(request, id):
    pc = get_object_or_404(PC, id=id)
    if request.method == 'POST':
        form = PCForm(request.POST, request.FILES, instance=pc)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "modificado correctamente")
            return redirect("listar_pc")
    else:
        form = PCForm(instance=pc)

    context = {
        'pc': pc,
        'form': form,
    }
    return render(request, 'app/productos/modificar_pc.html', context)
@permission_required('app.delete_pc')
def eliminar_pc(request, id):
    pc = get_object_or_404(PC, id=id)
    pc.delete()
    messages.success(request, "eliminado correctamente")
    return redirect(to="listar_pc")

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
        item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto_tipo='PC', producto_id=producto.id)
    elif producto_tipo == 'Software':
        producto = get_object_or_404(Software, id=producto_id)
        item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto_tipo='Software', producto_id=producto.id)

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
        if item.producto_tipo == 'PC':
            producto = get_object_or_404(PC, id=item.producto_id)
            subtotal = producto.precio * item.cantidad
            items_list.append({
                'nombre': producto.nombre,
                'cantidad': item.cantidad,
                'precio': producto.precio,
                'subtotal': subtotal,
                'pc': producto
            })
        elif item.producto_tipo == 'Software':
            producto = get_object_or_404(Software, id=item.producto_id)
            subtotal = producto.precio * item.cantidad
            items_list.append({
                'nombre': producto.nombre,
                'cantidad': item.cantidad,
                'precio': producto.precio,
                'subtotal': subtotal,
                'software': producto
            })
        total += subtotal

    context = {
        'items': items_list,
        'total': total,
    }

    return render(request, 'app/ver_carrito.html', context)



@require_POST
@login_required
def eliminar_del_carrito(request, id):
    try:
        item = get_object_or_404(ItemCarrito, id=id)
        item.delete()
        return JsonResponse({'message': 'Producto eliminado correctamente del carrito'}, status=200)
    except ItemCarrito.DoesNotExist:
        return JsonResponse({'error': 'El producto no existe en el carrito'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@login_required
def finalizar_compra(request):
    try:
        carrito = get_object_or_404(Carrito, usuario=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)

        with transaction.atomic():
            # Verificar y procesar cada item del carrito
            for item in items:
                if item.pc:
                    # Verificar si hay suficiente stock para el PC
                    if item.pc.stock < item.cantidad:
                        messages.error(request, f'No hay suficiente stock para {item.pc.nombre}.')
                        return redirect('ver_carrito')

                    # Reducir el stock del PC
                    item.pc.stock -= item.cantidad
                    item.pc.save()

                elif item.software:
                    # Verificar si hay suficiente stock para el software
                    if item.software.stock < item.cantidad:
                        messages.error(request, f'No hay suficiente stock para {item.software.nombre}.')
                        return redirect('ver_carrito')

                    # Reducir el stock del software
                    item.software.stock -= item.cantidad
                    item.software.save()

            # Eliminar todos los items del carrito después de procesar la compra
            items.delete()

        messages.success(request, 'Compra realizada con éxito.')
        return redirect('index')

    except Exception as e:
        messages.error(request, f'Error al procesar la compra: {str(e)}')
        return redirect('ver_carrito')



@login_required
@permission_required('app.delete_software', raise_exception=True)
def eliminar_software(request, id):
    software = get_object_or_404(Software, id=id)
    software.delete()
    messages.success(request, "Software eliminado con éxito.")
    return redirect('listar_software')

@login_required
@permission_required('app.change_software', raise_exception=True)
def modificar_software(request, id):
    software = get_object_or_404(Software, id=id)
    if request.method == 'POST':
        form = SoftwareForm(request.POST, request.FILES, instance=software)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, '¡Software modificado correctamente!')
            return redirect('listar_software')  # Redirigir a la lista de software o a otra vista
    else:
        form = SoftwareForm(instance=software)
    
    return render(request, 'app/productos/modificar_software.html', {'form': form, 'software': software})