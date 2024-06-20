//validaciones del formulario
function validarForm() {
    var certificado = document.getElementById('certificado').files[0];
    var constancia = document.getElementById('constancia').files[0];
    if (!certificado && !constancia) {//Valida la carga de un certificado de preparatoria o constancia de estudios
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "Debes cargar un certificado o una constancia",
            confirmButtonText: "Aceptar",
            customClass: {
                confirmButton: 'custom-confirm-button-class'
            }
        });
        return false;
    } else {
        var carrera1 = document.getElementById("carrera1").value;
        var carrera2 = document.getElementById("carrera2").value;
        if (carrera1 == carrera2) { //valida que las carrearas sean diferentes
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Debes elegir dos carreras diferentes",
                confirmButtonText: "Aceptar",
                customClass: {
                    confirmButton: 'custom-confirm-button-class'
                }
            });
            return false;
        } else {
            var pass1 = document.getElementById('pass1').value;
            var pass2 = document.getElementById('pass2').value;
            if (pass1 != pass2) { //Valida que las contraseñas sean iguales
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "Las contraseñas no coinciden",
                    confirmButtonText: "Aceptar",
                    customClass: {
                        confirmButton: 'custom-confirm-button-class'
                    }
                });
                return false;
            } else {
                let ingreso = parseInt(document.getElementById('ingreso').value);
                let egreso = parseInt(document.getElementById('egreso').value);
                if (egreso < ingreso) {
                    Swal.fire({
                        icon: "error",
                        title: "Error",
                        text: "El año de ingreso no puede ser mayor al año de egreso de la preparatoria",
                        confirmButtonText: "Aceptar",
                        customClass: {
                            confirmButton: 'custom-confirm-button-class'
                        }
                    });
                    return false;
                }
            }
        }

    }

    const checkbox = document.getElementById('indigena');
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;// El checkbox está seleccionado, asignar valor 1
        } else {
            this.value = 0;// El checkbox no está seleccionado, asignar valor 0
        }
    });

    const checkbox2 = document.getElementById('afroamericano');
    checkbox2.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;// El checkbox está seleccionado, asignar valor 1
        } else {
            this.value = 0;// El checkbox no está seleccionado, asignar valor 0
        }
    });

    const checkbox3 = document.getElementById('migrante');
    checkbox3.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;// El checkbox está seleccionado, asignar valor 1
        } else {
            this.value = 0;// El checkbox no está seleccionado, asignar valor 0
        }
    });

    const checkbox4 = document.getElementById('hipertensos');
    checkbox4.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;// El checkbox está seleccionado, asignar valor 1
        } else {
            this.value = 0;// El checkbox no está seleccionado, asignar valor 0
        }
    });
    const checkbox5 = document.getElementById('diabeticos');
    checkbox5.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;// El checkbox está seleccionado, asignar valor 1
        } else {
            this.value = 0;// El checkbox no está seleccionado, asignar valor 0
        }
    });
    const checkbox6 = document.getElementById('cardiacos');
    checkbox6.addEventListener('change', function () {
        if (this.checked) {
            this.value = 1;// El checkbox está seleccionado, asignar valor 1
        } else {
            this.value = 0;// El checkbox no está seleccionado, asignar valor 0
        }
    });
    return true;
}

//Validación de carreras
function validarUniversidad() {
    var univ1 = document.getElementById('otrauni');
    var univ2 = document.getElementById('cualuni');
    if (univ1.value == 0) {//Valida si se eligió otra universidad
        univ2.value = 0
        univ2.disabled = true;
    } else {
        univ2.disabled = false;
    }
    return true;
}


