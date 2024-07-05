// carrito.js

document.addEventListener('DOMContentLoaded', () => {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    function actualizarCarrito() {
        const carritoContainer = document.getElementById('carrito');
        carritoContainer.innerHTML = '';
        carrito.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.classList.add('carrito-item', 'card', 'mb-3');
            itemElement.innerHTML = `
                <div class="card-body d-flex justify-content-between align-items-center">
                    <div>
                        <h5 class="card-title">${item.nombre}</h5>
                        <p class="card-text">Precio: $${item.precio}</p>
                        <p class="card-text">Cantidad: ${item.cantidad}</p>
                    </div>
                    <button class="btn btn-danger btn-eliminar" data-nombre="${item.nombre}"><i class="fas fa-trash"></i></button>
                </div>
            `;
            carritoContainer.appendChild(itemElement);
        });
        const total = carrito.reduce((sum, item) => sum + item.precio * item.cantidad, 0);
        document.getElementById('total').textContent = `Total: $${total.toFixed(2)}`;
    }

    function guardarCarrito() {
        localStorage.setItem('carrito', JSON.stringify(carrito));
    }

    document.querySelectorAll('.btn-agregar-carrito').forEach(button => {
        button.addEventListener('click', () => {
            const nombre = button.getAttribute('data-nombre');
            const precio = parseFloat(button.getAttribute('data-precio'));
            const imagen = button.getAttribute('data-imagen');
            const itemIndex = carrito.findIndex(item => item.nombre === nombre);

            if (itemIndex !== -1) {
                carrito[itemIndex].cantidad++;
            } else {
                carrito.push({ nombre, precio, imagen, cantidad: 1 });
            }

            actualizarCarrito();
            guardarCarrito();
        });
    });

    document.getElementById('carrito').addEventListener('click', (e) => {
        if (e.target.closest('.btn-eliminar')) {
            const nombre = e.target.closest('.btn-eliminar').getAttribute('data-nombre');
            const itemIndex = carrito.findIndex(item => item.nombre === nombre);
            if (itemIndex !== -1) {
                carrito.splice(itemIndex, 1);
                actualizarCarrito();
                guardarCarrito();
            }
        }
    });

    document.getElementById('confirmPurchase').addEventListener('click', () => {
        if (carrito.length > 0) {
            alert('Compra realizada con éxito');
            carrito.length = 0;
            guardarCarrito();
            actualizarCarrito();
            $('#confirmModal').modal('hide');
        } else {
            alert('El carrito está vacío.');
        }
    });

    actualizarCarrito();
});
