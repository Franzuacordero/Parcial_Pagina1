// Añade un event listener al formulario con id 'contactForm' para manejar el evento 'submit'
document.getElementById('contactForm').addEventListener('submit', function(event) {
    // Previene el comportamiento por defecto del formulario (que sería recargar la página)
    event.preventDefault();
    // Llama a la función que valida y envía el formulario
    validateAndSubmitForm();
});

// Cargar datos del formulario desde localStorage al cargar la página
document.addEventListener('DOMContentLoaded', (event) => {
    // Llama a la función que carga los datos del formulario
    loadFormData();
});

// Función que valida y envía el formulario
function validateAndSubmitForm() {
    // Obtiene los valores de los campos del formulario
    const name = document.getElementById('nombre').value;
    const email = document.getElementById('correo').value;
    const message = document.getElementById('mensaje').value;
    const phone = document.getElementById('telefono').value;

    // Valida el nombre
    if (!validateName(name)) {
        alert('El nombre debe tener al menos 3 caracteres.');
        return;
    }

    // Valida el correo electrónico
    if (!validateEmail(email)) {
        alert('Por favor, introduce un correo electrónico válido.');
        return;
    }

    // Valida el mensaje
    if (message.length < 10) {
        alert('El mensaje debe tener al menos 10 caracteres.');
        return;
    }

    // Guarda los datos del formulario en localStorage
    saveFormData({ name, email, phone, message });

    // Envía los datos del formulario
    sendFormData({ name, email, phone, message });
}

// Función que valida el nombre
function validateName(name) {
    // Retorna true si el nombre tiene al menos 3 caracteres, de lo contrario, retorna false
    return name.length >= 3;
}

// Función que valida el correo electrónico
function validateEmail(email) {
    // Patrón regex para validar el formato del correo electrónico
    const emailPattern = /\S+@\S+\.\S+/;
    // Retorna true si el correo cumple con el patrón, de lo contrario, retorna false
    return emailPattern.test(email);
}

// Función que envía los datos del formulario a un servidor
function sendFormData(formData) {
    // Realiza una petición fetch al endpoint especificado
    fetch('https://pgy-api.vercel.app/api/formulario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        // Procesa la respuesta y verifica si fue exitosa
        return response.json().then(data => {
            if (!response.ok) {
                throw new Error(data.mensaje || 'Network response was not ok');
            }
            return data;
        });
    })
    .then(data => {
        console.log('Server response:', data); // Verifica la respuesta del servidor en la consola
        // Verifica si el formulario fue recibido con éxito
        if (data.mensaje === 'Formulario recibido') {
            alert('Formulario enviado con éxito');
            // Resetea el formulario
            document.getElementById('contactForm').reset();
            // Limpia los datos del formulario almacenados en localStorage
            clearFormData();
        } else {
            alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo. Detalles del error: ' + (data.mensaje || 'Error desconocido'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Muestra un mensaje de error si la petición falló
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo. Detalles del error: ' + error.message);
    });
}

// Función que guarda los datos del formulario en localStorage
function saveFormData(formData) {
    localStorage.setItem('formData', JSON.stringify(formData));
}

// Función que carga los datos del formulario desde localStorage
function loadFormData() {
    const formData = JSON.parse(localStorage.getItem('formData'));
    if (formData) {
        document.getElementById('nombre').value = formData.name || '';
        document.getElementById('correo').value = formData.email || '';
        document.getElementById('telefono').value = formData.phone || '';
        document.getElementById('mensaje').value = formData.message || '';
    }
}

// Función que limpia los datos del formulario almacenados en localStorage
function clearFormData() {
    localStorage.removeItem('formData');
}

