function actualizarTotal() {
    let total = 0;
    document.querySelectorAll('.card-body').forEach(item => {
        const precio = parseFloat(item.querySelector('.card-text').textContent.replace('Precio: $', ''));
        const cantidad = parseInt(item.querySelector('.card-text:nth-child(3)').textContent.replace('Cantidad: ', ''));
        total += precio * cantidad;
    });
    document.getElementById('total').textContent = 'Total: $' + total.toFixed(2);
}

// Event listener para eliminar productos
document.querySelectorAll('.btn-danger').forEach(button => {
    button.addEventListener('click', function() {
        this.closest('.card').remove();
        actualizarTotal();
    });
});

// Event listener para confirmar la compra
document.getElementById('confirmPurchase').addEventListener('click', function() {
    alert('Compra confirmada. Gracias por tu compra!');
    // Aquí podrías agregar lógica para enviar los datos de la compra a un servidor, etc.
    $('#confirmModal').modal('hide');
});

// Inicializar el total al cargar la página
actualizarTotal();