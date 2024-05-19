document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();
    validateAndSubmitForm();
});

// Cargar datos del formulario desde localStorage al cargar la página
document.addEventListener('DOMContentLoaded', (event) => {
    loadFormData();
});

function validateAndSubmitForm() {
    const name = document.getElementById('nombre').value;
    const email = document.getElementById('correo').value;
    const message = document.getElementById('mensaje').value;
    const phone = document.getElementById('telefono').value;

    if (!validateName(name)) {
        alert('El nombre debe tener al menos 3 caracteres.');
        return;
    }

    if (!validateEmail(email)) {
        alert('Por favor, introduce un correo electrónico válido.');
        return;
    }

    if (message.length < 10) {
        alert('El mensaje debe tener al menos 10 caracteres.');
        return;
    }

    // Guardar datos del formulario en localStorage
    saveFormData({ name, email, phone, message });

    sendFormData({ name, email, phone, message });
}

function validateName(name) {
    return name.length >= 3;
}

function validateEmail(email) {
    const emailPattern = /\S+@\S+\.\S+/;
    return emailPattern.test(email);
}

function sendFormData(formData) {
    fetch('https://pgy-api.vercel.app/api/formulario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        return response.json().then(data => {
            if (!response.ok) {
                throw new Error(data.mensaje || 'Network response was not ok');
            }
            return data;
        });
    })
    .then(data => {
        console.log('Server response:', data); // Verifica la respuesta del servidor en la consola
        if (data.mensaje === 'Formulario recibido') {
            alert('Formulario enviado con éxito');
            document.getElementById('contactForm').reset();
            // Limpiar localStorage después de enviar el formulario con éxito
            clearFormData();
        } else {
            alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo. Detalles del error: ' + (data.mensaje || 'Error desconocido'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo. Detalles del error: ' + error.message);
    });
}

function saveFormData(formData) {
    localStorage.setItem('formData', JSON.stringify(formData));
}

function loadFormData() {
    const formData = JSON.parse(localStorage.getItem('formData'));
    if (formData) {
        document.getElementById('nombre').value = formData.name || '';
        document.getElementById('correo').value = formData.email || '';
        document.getElementById('telefono').value = formData.phone || '';
        document.getElementById('mensaje').value = formData.message || '';
    }
}

function clearFormData() {
    localStorage.removeItem('formData');
}
